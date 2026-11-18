import { randomUUID } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

import {
  appendObservation,
  caseStatus,
  createCase,
  loadCase,
  readInput,
  readTarget,
  sanitize,
  sha256,
  withCaseLock,
  withTargetRepairLock,
} from "./cases.mjs";
import { externalDiagnosticCases, inspectClient } from "./client.mjs";
import {
  checkDesktop,
  checkDesktopNativeRegistration,
  selectedDesktopTelemetryOrigin,
} from "./desktop.mjs";
import {
  createCaseHandoff,
  readCaseEvidence,
  readProductHandoff,
} from "./evidence.mjs";
import { recordExternalFinish } from "./finish.mjs";
import { checkHosted, lookupHosted } from "./hosted.mjs";
import { errorDetails, fragmentEvents } from "./hosted/mcp-doctor.mjs";
import { doctorMessage } from "./messages.mjs";
import { codexNativeRead } from "./native-codex.mjs";
import { resumeOptions, saveResumeReference } from "./resume.mjs";
import { createSourceHandoff } from "./source-handoff.mjs";

export { externalDoctorNextActionId } from "./client.mjs";

const ACTIONS = [
  "check",
  "repair",
  "record-recheck",
  "native-recheck",
  "status",
  "upload",
  "evidence",
  "handoff",
  "finish",
];

function toolData(result) {
  if (result?.isError || result?.error)
    throw new Error(
      "The native tool returned an error, not a successful recheck.",
    );
  if (result?.structuredContent) return result.structuredContent;
  if (Array.isArray(result?.content)) {
    const text = result.content
      .filter((item) => item.type === "text")
      .map((item) => item.text)
      .join("\n");
    return JSON.parse(text);
  }
  return result;
}

const record = (value) =>
  value && typeof value === "object" && !Array.isArray(value);
const identifier = (value) =>
  typeof value === "string" && value.trim().length > 0;

export async function recordNativeRecheck(caseInfo, resultFile, source) {
  const input = await readInput(resultFile, ".doctor-recheck.json", 512 * 1024);
  const target = caseInfo.manifest.target;
  if (
    input.projectId !== undefined &&
    input.projectId !== null &&
    (typeof input.projectId !== "string" ||
      !/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(input.projectId))
  )
    throw new Error(
      "Native recheck needs the actual complete projectId, or an unavailable value.",
    );
  if (target.enabled === false && input.outcome === "success")
    throw new Error(doctorMessage("disabledRecheckRejected"));
  if (
    input.schemaVersion !== 1 ||
    input.source !== "native_host_tool_result" ||
    input.host !== target.host ||
    input.serverName !== target.serverName ||
    input.targetFingerprint !== caseInfo.manifest.targetFingerprint ||
    !["new_session", "same_session"].includes(input.sessionBoundary) ||
    !["failed", "success"].includes(input.outcome)
  )
    throw new Error(
      "Native recheck source, session boundary or target does not match this case.",
    );
  for (const key of ["nextAction", "precedingAction"])
    if (
      input[key] !== undefined &&
      (typeof input[key] !== "string" ||
        !input[key].trim() ||
        input[key].length > 4096)
    )
      throw new Error(
        `${key} must be nonempty text of at most 4096 characters.`,
      );
  if (
    input.outcome === "failed" &&
    input.needsUser === true &&
    !input.nextAction
  )
    throw new Error("A needs_user recheck requires the specific nextAction.");
  const originalThreadId =
    caseInfo.original.record?.conversationId ??
    (caseInfo.original.record?.source === "native_host_tool_result"
      ? caseInfo.original.record.sessionId
      : null);
  // Only Codex's host thread identifiers are comparable across these fields.
  if (
    target.host === "codex" &&
    input.sessionBoundary === "same_session" &&
    identifier(originalThreadId) &&
    identifier(input.sessionId) &&
    input.sessionId !== originalThreadId
  )
    throw Object.assign(
      new Error(
        "The same_session Codex recheck contradicts the original host thread ID.",
      ),
      { code: "HOST_SESSION_MISMATCH" },
    );
  const safe =
    target.surface === "hosted" ? ["list_projects"] : ["read_project"];
  if (!safe.includes(input.operation))
    throw new Error(
      "Only an actual safe native read may be recorded; never replay a mutation or generation.",
    );
  if (input.outcome === "success") {
    const data = toolData(input.result);
    if (!validNativeRead(input.operation, data))
      throw new Error(
        "The supplied native output does not match the selected read schema; configuration text and tool lists cannot close a case.",
      );
    if (
      input.operation === "read_project" &&
      input.projectId &&
      data.project.projectId !== input.projectId
    )
      throw new Error(
        "Native read returned a different Desktop project; recovery is not verified.",
      );
    if (
      target.projectId &&
      (input.operation !== "read_project" ||
        data.project?.projectId !== target.projectId)
    )
      throw new Error(
        "The selected Desktop project requires its actual read_project result.",
      );
  }
  const previous = (await caseStatus(caseInfo)).observations.find(
    (entry) => entry.kind === "native_recheck" && entry.projectId,
  )?.projectId;
  const projectId =
    input.projectId ??
    (input.operation === "read_project" && input.outcome === "success"
      ? toolData(input.result).project.projectId
      : null);
  if (
    projectId &&
    (target.projectId ?? previous) &&
    projectId !== (target.projectId ?? previous)
  )
    throw new Error(
      "Native recheck project differs from this case's selected project.",
    );
  const bytes = JSON.stringify(sanitize(input), null, 2) + "\n";
  const artifact = path.join(
    caseInfo.dir,
    `native-recheck-${randomUUID()}.json`,
  );
  await writeFile(artifact, bytes, { flag: "wx", mode: 0o600 });
  return appendObservation(caseInfo, {
    kind: "native_recheck",
    nativeCallId: input.nativeCallId ?? null,
    nativeCallIdKind: input.nativeCallIdKind ?? "unavailable",
    observedAt: input.observedAt ?? null,
    operation: input.operation,
    ...(projectId ? { projectId } : {}),
    outcome: input.outcome,
    repairPerformed: false,
    resultArtifact: artifact,
    resultSha256: sha256(bytes),
    sessionBoundary: input.sessionBoundary,
    sessionId: input.sessionId ?? null,
    source:
      source ??
      "agent_supplied_native_host_tool_result; not_independently_attested",
    ...(input.precedingAction
      ? { precedingAction: input.precedingAction }
      : {}),
    ...(input.outcome === "failed"
      ? {
          error: input.error ?? input.result,
          needsUser: input.needsUser === true,
          ...(input.nextAction ? { nextAction: input.nextAction } : {}),
        }
      : {}),
  });
}

export async function runUnifiedDoctor(options, dependencies = {}) {
  if (options.sourceEvent) {
    if (
      options.context ||
      options.casePath ||
      options.handoff ||
      options.fix ||
      options.online ||
      options.failureRecord ||
      options.caseRoot ||
      options.resumeFile ||
      options.result
    )
      throw new Error(
        "Source selection cannot replace another case or authorize connection operations.",
      );
    if (options.action && !["evidence", "handoff"].includes(options.action))
      throw new Error(
        "Source material preparation cannot execute checks or repairs.",
      );
    return createSourceHandoff({
      projectId: options.projectId,
      sourceEvent: options.sourceEvent,
      userData: options.userData,
    });
  }
  if (options.handoff) {
    if (options.action && options.action !== "evidence")
      throw new Error(
        "A handoff supports independent read-only evidence access.",
      );
    return readProductHandoff(options.handoff, {
      evidenceRef: options.evidenceRef,
    });
  }
  options = await resumeOptions(options);
  const action = options.action ?? (options.fix ? "repair" : "check");
  if (!ACTIONS.includes(action)) throw new Error("Unknown Doctor action.");
  if (!options.casePath && !options.context)
    throw new Error(
      "Select a dedicated .doctor-context.json before checking, repairing or recording a recheck.",
    );
  if (!options.casePath && action !== "check" && action !== "repair")
    throw new Error(
      "Resume the existing --case; do not replace the incident with a new capture.",
    );
  let target = options.context ? await readTarget(options.context) : undefined;
  if (!target && options.casePath)
    target = (await loadCase(options.casePath)).manifest.target;
  if (target.host === "chatcut" && action === "repair")
    throw new Error(
      "Client diagnosis has no automatic repair. Follow the recorded next action; existing integration maintenance is a separate authorized operation.",
    );
  const clientCheck =
    target.host === "chatcut" && action === "check"
      ? await inspectClient(target, dependencies.clientDependencies)
      : null;
  if (
    clientCheck?.originalError &&
    !options.casePath &&
    !options.failureRecord
  ) {
    const inputDir =
      options.caseRoot ?? path.join(target.cwd, ".chatcut-doctor");
    await mkdir(inputDir, { mode: 0o700, recursive: true });
    options.failureRecord = path.join(
      inputDir,
      `${randomUUID()}.doctor-failure.json`,
    );
    const { callId, failureEventId, occurredAt, operation, ...error } =
      clientCheck.originalError;
    await writeFile(
      options.failureRecord,
      JSON.stringify({
        callId,
        error,
        failureEventId,
        occurredAt,
        operation,
        schemaVersion: 1,
        serverName: target.serverName,
        source: "client_runtime_event",
      }),
      { flag: "wx", mode: 0o600 },
    );
  }
  const caseInfo = options.casePath
    ? await loadCase(options.casePath, target)
    : await createCase({
        originalFile: options.failureRecord,
        root: options.caseRoot ?? path.join(target.cwd, ".chatcut-doctor"),
        target,
      });
  target ??= caseInfo.manifest.target;
  if (action === "evidence")
    return readCaseEvidence(caseInfo, { evidenceRef: options.evidenceRef });
  if (action === "handoff") return createCaseHandoff(caseInfo);
  if (action !== "status")
    await saveResumeReference(caseInfo, options.resumeFile);
  if (action === "status") return caseStatus(caseInfo);
  if (action === "finish") {
    dependencies.signal?.throwIfAborted();
    const finish = await withCaseLock(caseInfo, () =>
      (dependencies.finish ?? recordExternalFinish)(caseInfo, options.result),
    );
    return {
      ...(await caseStatus(caseInfo)),
      externalFinish: {
        attemptId: finish.attemptId,
        eventId: finish.eventId,
        statementSha256: finish.statementSha256,
      },
    };
  }
  const executeCaseAction = async () => {
    if (clientCheck) {
      const {
        originalError: _originalError,
        projectRead,
        ...checked
      } = clientCheck;
      await appendObservation(caseInfo, {
        ...checked,
        kind: "check",
        source: "selected_client_runtime; no_model_required",
      });
      if (projectRead && target.projectId) {
        const result = path.join(
          caseInfo.dir,
          `client-read-${randomUUID()}.doctor-recheck.json`,
        );
        await writeFile(
          result,
          JSON.stringify({
            error: projectRead.error ? errorDetails(projectRead.error) : null,
            host: target.host,
            nativeCallId: projectRead.callId ?? null,
            nativeCallIdKind: "client_runtime_call",
            observedAt: projectRead.observedAt ?? null,
            operation: "read_project",
            outcome: projectRead.error ? "failed" : "success",
            projectId: target.projectId,
            result: projectRead.result ?? null,
            schemaVersion: 1,
            serverName: target.serverName,
            sessionBoundary: "same_session",
            sessionId: projectRead.sessionId ?? null,
            source: "native_host_tool_result",
            targetFingerprint: caseInfo.manifest.targetFingerprint,
          }),
          { flag: "wx", mode: 0o600 },
        );
        try {
          await recordNativeRecheck(
            caseInfo,
            result,
            "selected_client_runtime_actual_read",
          );
        } catch (error) {
          await appendObservation(caseInfo, {
            error: errorDetails(error),
            kind: "native_recheck",
            needsUser: false,
            nextAction: "inspect_original_project_error",
            outcome: "invalid_evidence",
            repairPerformed: false,
            source: "selected_client_runtime_validation",
          });
        }
      }
      return;
    }
    if (action === "native-recheck") {
      const prior = await caseStatus(caseInfo);
      const boundProject =
        target.projectId ??
        prior.observations.find(
          (entry) => entry.kind === "native_recheck" && entry.projectId,
        )?.projectId;
      if (
        options.projectId &&
        boundProject &&
        options.projectId !== boundProject
      )
        throw new Error(
          "Selected project differs from the original case; no native call executed.",
        );
      const projectId = boundProject ?? options.projectId;
      if (target.surface === "hosted" && projectId)
        throw new Error(
          "A Hosted connection recheck uses list_projects without changing project scope.",
        );
      const lastConnectionState = prior.observations.findLast(
        (entry) =>
          typeof entry.lookup?.enabled === "boolean" ||
          entry.report?.integrations?.[target.host]?.status === "opted-out",
      );
      if (
        target.enabled === false ||
        lastConnectionState?.lookup?.enabled === false ||
        lastConnectionState?.report?.integrations?.[target.host]?.status ===
          "opted-out"
      ) {
        await appendObservation(caseInfo, {
          kind: "native_recheck",
          needsUser: true,
          nextAction: doctorMessage("connectionDisabled"),
          outcome: "not_run",
          source: "local_precondition",
        });
        return;
      }
      if (
        target.host !== "codex" ||
        !target.cliPath ||
        (target.surface === "desktop" && !projectId)
      ) {
        await appendObservation(caseInfo, {
          kind: "native_recheck",
          needsUser: true,
          operation:
            target.surface === "desktop" ? "read_project" : "list_projects",
          outcome: "not_run",
          source: "local_precondition",
          ...(projectId ? { projectId } : {}),
          nextAction: doctorMessage("nativeHostReadRequired"),
        });
        return;
      }
      const output = path.join(
        caseInfo.dir,
        `native-host-${randomUUID()}.doctor-recheck.json`,
      );
      try {
        const current = dependencies.nativePrecheck
          ? await dependencies.nativePrecheck(target)
          : target.surface === "hosted"
            ? await lookupHosted(target, dependencies.hostedDependencies)
            : await checkDesktopNativeRegistration(
                target,
                dependencies.hostedDependencies,
              );
        const ready =
          target.surface === "hosted"
            ? current.status === "found" &&
              current.endpoint === target.endpoint &&
              current.scope === target.scope &&
              current.enabled !== false
            : current.status === "ready";
        if (!ready) {
          await appendObservation(caseInfo, {
            kind: "native_recheck",
            needsUser: true,
            nextAction: doctorMessage("nativeHostReadRequired"),
            outcome: "not_run",
            precheck: current,
            source: "selected_target_precheck",
          });
          return;
        }
        await (dependencies.nativeRead ?? codexNativeRead)({
          executable: target.cliPath,
          operation:
            target.surface === "desktop" ? "read_project" : "list_projects",
          output,
          projectId,
          signal: dependencies.signal,
          target,
        });
        await recordNativeRecheck(caseInfo, output);
      } catch (error) {
        await appendObservation(caseInfo, {
          error: errorDetails(error),
          kind: "native_recheck",
          nextAction: doctorMessage("invalidNativeEvidence"),
          outcome: "failed",
          source: "native_capture_or_save_failure",
        });
      }
      return;
    }
    if (action === "record-recheck") {
      try {
        await recordNativeRecheck(caseInfo, options.result);
      } catch (error) {
        await appendObservation(caseInfo, {
          error: errorDetails(error),
          kind: "native_recheck",
          nextAction: doctorMessage("invalidNativeEvidence"),
          outcome: "invalid_evidence",
          source: "recheck_input_validation",
        });
      }
      return;
    }
    if (action === "upload") {
      await uploadCase(caseInfo, dependencies);
      return;
    }
    const runDir = path.join(caseInfo.dir, `check-${randomUUID()}`);
    await mkdir(runDir, { mode: 0o700 });
    try {
      const execute = async () =>
        target.surface === "desktop"
          ? await (dependencies.desktop ?? checkDesktop)(target, {
              repair: action === "repair",
              ...dependencies.desktopDependencies,
              ...(dependencies.signal ? { signal: dependencies.signal } : {}),
            })
          : await (dependencies.hosted ?? checkHosted)(target, {
              dir: runDir,
              online: options.online === true,
              original: caseInfo.original,
              repair: action === "repair",
              ...dependencies.hostedDependencies,
            });
      const result =
        action === "repair"
          ? await withTargetRepairLock(target, execute)
          : await execute();
      if (dependencies.signal?.aborted) {
        await appendObservation(caseInfo, {
          action,
          kind: "diagnostic_action",
          outcome: "canceled",
          repairPerformed: false,
          source: "client_user_action",
        });
        return;
      }
      const attachment = result.reportPath
        ? {
            reportFileSha256: sha256(await readFile(result.reportPath)),
            reportPath: result.reportPath,
          }
        : {};
      await appendObservation(caseInfo, {
        diagnosticId: result.diagnosticId ?? randomUUID(),
        kind: action,
        source: "independent_local_program; current_host_session_unobserved",
        ...result,
        diagnosticCases: externalDiagnosticCases(target, result),
        ...attachment,
        repairPerformed:
          action === "repair" ? (result.repairPerformed ?? null) : false,
      });
    } catch (error) {
      if (dependencies.signal?.aborted) {
        await appendObservation(caseInfo, {
          action,
          kind: "diagnostic_action",
          outcome: "canceled",
          repairPerformed: false,
          source: "client_user_action",
        });
        return;
      }
      await appendObservation(caseInfo, {
        error: errorDetails(error),
        kind: action,
        needsUser: [
          -32601,
          "ECONNREFUSED",
          "ENOENT",
          "HOST_CLI_UNAVAILABLE",
        ].includes(error.code),
        nextAction: doctorMessage("localProgramUnavailable"),
        outcome: "failed",
        repairPerformed: action === "repair" ? null : false,
        source: "independent_local_program",
      });
    }
  };
  await withCaseLock(
    caseInfo,
    observedCaseAction(
      caseInfo,
      target,
      action,
      dependencies,
      executeCaseAction,
    ),
  );
  return caseStatus(caseInfo);
}

async function limitedText(response) {
  const reader = response.body?.getReader();
  if (!reader) return "";
  const chunks = [];
  let size = 0;
  try {
    for (;;) {
      const item = await reader.read();
      if (item.done) break;
      size += item.value.byteLength;
      if (size > 16 * 1024)
        throw new Error("Diagnostic ingest response exceeds 16 KiB.");
      chunks.push(item.value);
    }
  } finally {
    await reader.cancel().catch(() => {});
  }
  return Buffer.concat(chunks).toString("utf8");
}

function observedCaseAction(caseInfo, target, action, dependencies, execute) {
  return async () => {
    await loadCase(caseInfo.dir, target);
    const precedingObservationIds = dependencies.onOperationComplete
      ? (await caseStatus(caseInfo)).observations.map(
          (entry) => entry.observationId,
        )
      : undefined;
    let operationError;
    try {
      return await execute();
    } catch (error) {
      operationError = error;
      throw error;
    } finally {
      try {
        await dependencies.onOperationComplete?.(caseInfo, {
          action,
          cancelled: dependencies.signal?.aborted === true,
          error: operationError,
          precedingObservationIds,
        });
      } catch {
        /* Result recording cannot replace the observed operation's outcome. */
      }
    }
  };
}

async function uploadCase(caseInfo, dependencies) {
  const status = await caseStatus(caseInfo);
  const target = caseInfo.manifest.target;
  if (target.enabled === false)
    throw new Error(
      "The selected connection is intentionally disabled; no report sent.",
    );
  const telemetryOrigin =
    target.host === "chatcut"
      ? target.backendOrigin
      : target.surface === "desktop"
        ? await selectedDesktopTelemetryOrigin(target)
        : target.endpoint;
  if (!telemetryOrigin)
    throw new Error(
      "No selected telemetry origin is available. Local diagnosis is preserved; no fallback origin used.",
    );
  const observations = status.observations.filter(
    (entry) => entry.kind !== "delivery",
  );
  if (
    observations.some(
      (entry) =>
        entry.lookup?.enabled === false ||
        entry.outcome === "intentionally_disabled" ||
        entry.report?.integrations?.[target.host]?.status === "opted-out",
    )
  )
    throw new Error(
      "The selected native configuration reports intentional disablement; no report sent.",
    );
  const contentFingerprint = sha256(
    JSON.stringify({ observations, original: caseInfo.original }),
  );
  const prior = status.observations.find(
    (entry) =>
      entry.kind === "delivery" &&
      entry.contentFingerprint === contentFingerprint &&
      entry.outcome === "ingest_accepted",
  );
  if (prior) return prior;
  const report = {
    caseId: caseInfo.manifest.caseId,
    collectedAt: new Date().toISOString(),
    coverage: "triggered_case_only; not_all_users_or_failures",
    diagnosticId: randomUUID(),
    host: target.host,
    observations,
    originalFailure: caseInfo.original,
    originalSha256: caseInfo.manifest.originalSha256,
    repairPerformed: status.repairPerformed,
    schemaVersion: 1,
    scope: target.surface,
    target: {
      backendOrigin: target.backendOrigin ?? null,
      endpoint: target.endpoint ?? null,
      fingerprint: caseInfo.manifest.targetFingerprint,
      management: target.management,
      scope: target.scope,
      serverName: target.serverName,
    },
  };
  const file = path.join(
    caseInfo.dir,
    `delivery-report-${report.diagnosticId}.json`,
  );
  const reportBytes = JSON.stringify(report, null, 2) + "\n";
  await writeFile(file, reportBytes, { flag: "wx", mode: 0o600 });
  const reportFileSha256 = sha256(reportBytes);
  try {
    const events = fragmentEvents(report);
    for (const event of events)
      event.properties.attributes.mcpDoctor.scope = target.surface;
    const response = await (dependencies.fetch ?? fetch)(
      new URL("/telemetry/events", telemetryOrigin),
      {
        body: JSON.stringify(events),
        headers: { "content-type": "application/json" },
        method: "POST",
        redirect: "manual",
        signal: AbortSignal.timeout(3500),
      },
    );
    const text = await limitedText(response);
    if (!response.ok || JSON.parse(text).ok !== true)
      throw new Error(
        `Diagnostic ingest rejected: HTTP ${response.status}; ${text}`,
      );
    return appendObservation(caseInfo, {
      contentFingerprint,
      diagnosticId: report.diagnosticId,
      fragmentCount: events.length,
      kind: "delivery",
      outcome: "ingest_accepted",
      reportFileSha256,
      reportPath: file,
      reportSha256: events[0].properties.attributes.mcpDoctor.reportSha256,
      storageVerified: false,
    });
  } catch (error) {
    return appendObservation(caseInfo, {
      contentFingerprint,
      diagnosticId: report.diagnosticId,
      error: errorDetails(error),
      kind: "delivery",
      outcome: dependencies.signal?.aborted
        ? "canceled_acceptance_unknown"
        : "failed",
      reportFileSha256,
      reportPath: file,
      storageVerified: false,
    });
  }
}

function validNativeRead(operation, data) {
  if (!record(data) || data.error || data.isError) return false;
  if (operation === "list_projects")
    return (
      Array.isArray(data.projects) &&
      data.projects.every(
        (project) =>
          record(project) &&
          identifier(project.projectId ?? project.id) &&
          typeof project.name === "string",
      )
    );
  const project = data.project;
  return (
    record(project) &&
    identifier(project.projectId) &&
    typeof project.name === "string" &&
    Number.isFinite(project.frameRate) &&
    project.frameRate > 0 &&
    typeof project.readOnly === "boolean" &&
    Number.isInteger(project.schemaVersion) &&
    project.schemaVersion > 0 &&
    Array.isArray(data.timelines) &&
    data.timelines.every(
      (timeline) =>
        record(timeline) &&
        identifier(timeline.id) &&
        typeof timeline.name === "string" &&
        typeof timeline.active === "boolean" &&
        typeof timeline.hidden === "boolean",
    ) &&
    record(data.assets) &&
    Number.isInteger(data.assets.total) &&
    data.assets.total >= 0 &&
    Object.hasOwn(data, "activeTimeline") &&
    (data.activeTimeline === null || record(data.activeTimeline))
  );
}
