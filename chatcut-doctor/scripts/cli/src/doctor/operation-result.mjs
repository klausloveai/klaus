import { randomUUID } from "node:crypto";
import { lstat, realpath, rename, unlink, writeFile } from "node:fs/promises";
import path from "node:path";

import {
  appendObservation,
  caseStatus,
  loadCase,
  readInput,
  sha256,
  withCaseLock,
} from "./cases.mjs";
import { recordExternalFinish } from "./finish.mjs";
import { deliverHostedOperation } from "./hosted-operation-delivery.mjs";
import { errorDetails } from "./hosted/mcp-doctor.mjs";
import { runUnifiedDoctor } from "./unified.mjs";

const OBSERVED_ACTIONS = new Set([
  "check",
  "native-recheck",
  "record-recheck",
  "repair",
]);

export async function recordCliOperation(info, operation) {
  if (!Array.isArray(operation.precedingObservationIds))
    throw new Error("CLI operation observation baseline is unavailable.");
  const state = await caseStatus(info);
  const requestId = randomUUID();
  const eventId = `doctor-${sha256(JSON.stringify([state.caseId, requestId]))}`;
  const binding = await deliveryBinding(info).catch(() => undefined);
  const preceding = new Set(operation.precedingObservationIds);
  const currentObservations = state.observations.filter(
    (entry) =>
      !preceding.has(entry.observationId) &&
      ["check", "diagnostic_action", "native_recheck", "repair"].includes(
        entry.kind,
      ),
  );
  const observations = currentObservations.slice(-30);
  const repairs = currentObservations.filter(
    (entry) => entry.kind === "repair",
  );
  const repairPerformed = repairs.some(
    (entry) => entry.repairPerformed === true,
  )
    ? true
    : operation.action === "repair"
      ? repairs.length &&
        repairs.every((entry) => entry.repairPerformed === false)
        ? false
        : null
      : false;
  const result = await appendObservation(info, {
    action: operation.action,
    completionKind: "operation",
    durationMs: Math.max(
      0,
      Date.parse(operation.finishedAt) - Date.parse(operation.startedAt),
    ),
    eventId,
    finishedAt: operation.finishedAt,
    kind: "investigation_result",
    outcome: operation.cancelled
      ? "cancelled"
      : operation.error
        ? "error"
        : "completed",
    requestId,
    source: "actual_cli_operation_lifecycle",
    startedAt: operation.startedAt,
    ...(operation.error
      ? { terminalError: errorDetails(operation.error) }
      : {}),
    caseRepairPerformed: state.repairPerformed,
    originalFailureEventId: info.original.record?.failureEventId,
    originalSha256: state.originalSha256,
    repairPerformed,
    targetFingerprint: state.targetFingerprint,
    verifiedCaseStatus: state.status,
    ...(binding
      ? {
          deliveryBackendOrigin: binding.identity.backendOrigin,
          deliveryIdentity: {
            projectId: binding.projectId,
            userId: binding.identity.userId,
          },
        }
      : {}),
    checksAndVerification: observations.map((entry) => ({
      after: entry.after,
      checks: entry.checks,
      diagnosticCases: entry.diagnosticCases,
      diagnosticChecks: entry.report
        ? {
            collectedAt: entry.report.collectedAt,
            diagnosticId: entry.report.diagnosticId,
            gaps: entry.report.gaps,
            probes: entry.report.probes,
            wireProbes: entry.report.wireProbes,
          }
        : undefined,
      error: entry.error,
      kind: entry.kind,
      lookup: entry.lookup,
      nativeCallId: entry.nativeCallId,
      nativeCallIdKind: entry.nativeCallIdKind,
      observationId: entry.observationId,
      operation: entry.operation,
      outcome: entry.outcome,
      recordedAt: entry.recordedAt,
      repairPerformed: entry.repairPerformed,
      resultSha256: entry.resultSha256,
      sessionBoundary: entry.sessionBoundary,
      source: entry.source,
    })),
    evidenceGaps: [
      ...state.evidenceGaps,
      "external_ai_turn_lifecycle_and_assessment_unobserved",
      "external_cli_chat_and_model_unobserved",
      ...(binding || info.manifest.target.surface === "hosted"
        ? []
        : ["automatic_result_delivery_requires_a_bound_current_desktop_case"]),
    ],
    observationIds: observations.map((entry) => entry.observationId),
    omittedObservations: Math.max(
      0,
      currentObservations.length - observations.length,
    ),
    qualification:
      "actual_case_action_completion_before_lock_release_and_cli_exit; external_ai_turn_unobserved",
  });
  if (binding) {
    try {
      const current = await deliveryBinding(info);
      if (JSON.stringify(current) === JSON.stringify(binding))
        await signalResult(binding.root, result);
    } catch {
      /* The saved journal remains eligible for the authenticated Desktop recovery. */
    }
  }
  return result;
}

export async function runObservedDoctor(options, dependencies = {}) {
  const startedAt = new Date().toISOString();
  let captured;
  let result;
  let failed = false;
  let failure;
  try {
    result = await runUnifiedDoctor(options, {
      ...dependencies,
      async finish(info, file) {
        const binding = await deliveryBinding(info).catch(() => undefined);
        const operation = await recordExternalFinish(info, file, binding);
        captured = { info, operation };
        if (binding) {
          try {
            if (
              JSON.stringify(await deliveryBinding(info)) ===
              JSON.stringify(binding)
            )
              await signalResult(binding.root, operation);
          } catch {
            /* Authenticated journal recovery can deliver the preserved statement later. */
          }
        }
        return operation;
      },
      async onOperationComplete(info, operation) {
        if (!OBSERVED_ACTIONS.has(operation.action)) return;
        captured = {
          info,
          operation: await recordCliOperation(info, {
            ...operation,
            finishedAt: new Date().toISOString(),
            startedAt,
          }),
        };
      },
    });
  } catch (error) {
    failed = true;
    failure = error;
  }
  let delivery;
  try {
    const info =
      captured?.info ??
      (result?.caseDir ? await loadCase(result.caseDir) : undefined);
    if (info?.manifest.target.surface === "hosted") {
      const state = await caseStatus(info);
      const admitted = new Set(
        state.observations
          .filter(
            (entry) =>
              entry.kind === "result_delivery" &&
              (entry.enqueued === true ||
                entry.resumedExistingPackets === true ||
                !["not_durably_enqueued", "pending"].includes(entry.outcome)),
          )
          .map((entry) => entry.eventId),
      );
      const recoverable = state.observations.find(
        (entry) =>
          entry.kind === "investigation_result" &&
          [
            "actual_cli_operation_lifecycle",
            "external_ai_skill_finish",
          ].includes(entry.source) &&
          !admitted.has(entry.eventId),
      );
      const operation =
        captured?.operation && !admitted.has(captured.operation.eventId)
          ? captured.operation
          : recoverable;
      try {
        delivery = await deliverHostedOperation(info, operation, {
          ...dependencies.hostedResultOptions,
          state,
        });
      } catch (error) {
        delivery = {
          error: errorDetails(error),
          outcome: "pending",
          storageVerified: false,
        };
      }
      await withCaseLock(info, async () => {
        const latestState = await caseStatus(info);
        const knownResults = new Set(
          latestState.observations
            .filter((entry) => entry.kind === "investigation_result")
            .map((entry) => entry.eventId),
        );
        const { settledEvents = [], ...summary } = delivery;
        const receipts = settledEvents.filter((entry) =>
          knownResults.has(entry.eventId),
        );
        if (
          operation &&
          !receipts.some((entry) => entry.eventId === operation.eventId)
        )
          receipts.push({
            eventId: operation.eventId,
            outcome: delivery.outcome,
          });
        for (const receipt of receipts) {
          if (
            latestState.observations.some(
              (entry) =>
                entry.kind === "result_delivery" &&
                entry.eventId === receipt.eventId &&
                entry.outcome === receipt.outcome,
            )
          )
            continue;
          await appendObservation(info, {
            ...summary,
            ...receipt,
            kind: "result_delivery",
            source: "existing_shared_frontend_transport",
            storageVerified: false,
          });
        }
      });
      if (!failed && result?.caseDir)
        result = {
          ...(await caseStatus(info)),
          ...(result.externalFinish
            ? { externalFinish: result.externalFinish }
            : {}),
        };
    }
  } catch {
    /* Delivery bookkeeping never replaces the observed case operation. */
  }
  if (failed) throw failure;
  return delivery ? { ...result, automaticResultDelivery: delivery } : result;
}

async function deliveryBinding(info) {
  const target = info.manifest.target;
  if (target.surface !== "desktop" || !target.userData || !target.projectId)
    return;
  const userData = await realpath(target.userData);
  const rootPath = path.join(userData, "doctor-cases");
  const rootInfo = await lstat(rootPath);
  if (!rootInfo.isDirectory() || rootInfo.isSymbolicLink()) return;
  const root = await realpath(rootPath);
  const directory = await realpath(info.dir);
  const directoryInfo = await lstat(info.dir);
  if (
    !directoryInfo.isDirectory() ||
    directoryInfo.isSymbolicLink() ||
    !root.startsWith(userData + path.sep) ||
    !directory.startsWith(root + path.sep)
  )
    return;
  const auth = await readInput(
    path.join(userData, "auth-token.json"),
    "auth-token.json",
    64 * 1024,
  );
  const identity = profileIdentity(auth);
  if (
    !identity ||
    identity.profileId !== target.profile ||
    identity.backendOrigin !== target.backendOrigin ||
    info.original.record?.userId !== identity.userId
  )
    return;
  const reference = await readInput(
    path.join(root, "index", `${info.manifest.caseId}.json`),
    ".json",
    16 * 1024,
  );
  if (
    reference.caseId !== info.manifest.caseId ||
    reference.userId !== identity.userId ||
    reference.projectId !== target.projectId ||
    typeof reference.context !== "string" ||
    !Number.isFinite(Date.parse(reference.updatedAt)) ||
    reference.originalSha256 !== info.manifest.originalSha256 ||
    reference.targetFingerprint !== info.manifest.targetFingerprint ||
    (await realpath(reference.casePath)) !== directory
  )
    return;
  const context = await lstat(reference.context);
  if (
    !context.isFile() ||
    context.isSymbolicLink() ||
    !(await realpath(reference.context)).startsWith(root + path.sep)
  )
    return;
  const current = profileIdentity(
    await readInput(
      path.join(userData, "auth-token.json"),
      "auth-token.json",
      64 * 1024,
    ),
  );
  if (JSON.stringify(current) !== JSON.stringify(identity)) return;
  return { identity, projectId: target.projectId, root };
}

function profileIdentity(auth) {
  if (
    typeof auth.userId !== "string" ||
    !/^[A-Za-z0-9_-]{1,128}$/.test(auth.userId) ||
    !["beta", "custom", "local", "production"].includes(auth.profileId) ||
    typeof auth.backendOrigin !== "string"
  )
    return;
  const backend = new URL(auth.backendOrigin);
  if (backend.href !== `${backend.origin}/`) return;
  return {
    backendOrigin: backend.origin,
    profileId: auth.profileId,
    userId: auth.userId,
  };
}

async function signalResult(root, result) {
  const signal = path.join(root, "external-results.signal.json");
  const temporary = path.join(root, `.external-result-${randomUUID()}.tmp`);
  try {
    await writeFile(
      temporary,
      JSON.stringify({
        caseId: result.caseId,
        eventId: result.eventId,
        schemaVersion: 1,
      }),
      { flag: "wx", mode: 0o600 },
    );
    await rename(temporary, signal);
  } finally {
    await unlink(temporary).catch(() => {});
  }
}
