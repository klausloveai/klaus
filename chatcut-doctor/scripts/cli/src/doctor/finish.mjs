import {
  appendObservation,
  caseStatus,
  readInput,
  sanitize,
  sha256,
} from "./cases.mjs";
import { readCaseEvidence } from "./evidence.mjs";

const FIELDS = new Set([
  "assessment",
  "attemptId",
  "caseId",
  "guidance",
  "model",
  "modelVersion",
  "nextStep",
  "observationIds",
  "originalSha256",
  "outcome",
  "provider",
  "schemaVersion",
  "stopReason",
  "targetFingerprint",
]);
const FACT_KINDS = new Set([
  "check",
  "company_evidence",
  "diagnostic_action",
  "native_recheck",
  "repair",
]);

export async function recordExternalFinish(info, file, binding) {
  if (typeof file !== "string")
    throw new Error(
      "Doctor finish needs a dedicated .doctor-finish.json statement.",
    );
  const input = await readInput(file, ".doctor-finish.json", 32 * 1024);
  if (
    !input ||
    typeof input !== "object" ||
    Array.isArray(input) ||
    Object.keys(input).some((key) => !FIELDS.has(key)) ||
    input.schemaVersion !== 1
  )
    throw new Error(
      "Invalid Doctor finish statement; identity and recovery fields are not accepted.",
    );
  const state = await caseStatus(info);
  if (
    input.caseId !== state.caseId ||
    input.originalSha256 !== state.originalSha256 ||
    input.targetFingerprint !== state.targetFingerprint
  )
    throw new Error(
      "Doctor finish does not match the immutable case and selected target.",
    );
  const anchor = state.observations.find(
    (entry) =>
      entry.eventId === input.attemptId &&
      entry.kind === "investigation_result" &&
      entry.source === "actual_cli_operation_lifecycle" &&
      entry.completionKind === "operation",
  );
  if (!anchor || !Number.isFinite(Date.parse(anchor.startedAt)))
    throw new Error(
      "Doctor finish needs an actual operation eventId from this case as its attempt anchor.",
    );
  if (!["completed", "needs_user", "unresolved"].includes(input.outcome))
    throw new Error(
      "Doctor finish outcome must be completed, needs_user or unresolved; it is an agent statement, not recovery evidence.",
    );
  const selectedIds = input.observationIds ?? [];
  if (
    !Array.isArray(selectedIds) ||
    selectedIds.length > 100 ||
    selectedIds.some((id) => typeof id !== "string")
  )
    throw new Error(
      "Doctor finish accepts at most 100 actual observation references.",
    );
  const ids = [
    ...new Set([...(anchor.observationIds ?? []), ...selectedIds]),
  ].sort();
  const anchoredIds = new Set(anchor.observationIds ?? []);
  const earliest = state.observations.findIndex(
    (entry) => entry === anchor || anchoredIds.has(entry.observationId),
  );
  const observations = ids.map((id) => {
    const entry = state.observations.find(
      (candidate) => candidate.observationId === id,
    );
    if (
      !entry ||
      !FACT_KINDS.has(entry.kind) ||
      state.observations.indexOf(entry) < earliest
    )
      throw new Error(
        "Doctor finish observation is unavailable or precedes this attempt anchor.",
      );
    return entry;
  });
  const guidance = input.guidance ?? [];
  if (!Array.isArray(guidance) || guidance.length > 10)
    throw new Error("Doctor finish accepts at most 10 guidance references.");
  const guides = guidance
    .map((guide) => {
      if (
        !guide ||
        typeof guide !== "object" ||
        Array.isArray(guide) ||
        Object.keys(guide).some((key) => !["ref", "sha256"].includes(key)) ||
        typeof guide.ref !== "string" ||
        typeof guide.sha256 !== "string" ||
        !/^guidance:[a-z-]{1,64}$/.test(guide.ref) ||
        !/^[a-f0-9]{64}$/.test(guide.sha256)
      )
        throw new Error(
          "Doctor finish guidance must match an actual directory reference and hash.",
        );
      return { ref: guide.ref, sha256: guide.sha256 };
    })
    .sort((a, b) => a.ref.localeCompare(b.ref));
  const statement = sanitize({
    assessment: text(input.assessment, "assessment", 4000),
    attemptId: anchor.eventId,
    guidance: guides,
    ...(input.model !== undefined
      ? { model: text(input.model, "model", 256) }
      : {}),
    ...(input.modelVersion !== undefined
      ? { modelVersion: text(input.modelVersion, "modelVersion", 256) }
      : {}),
    nextStep: text(input.nextStep, "nextStep", 1000, true),
    observationIds: ids,
    outcome: input.outcome,
    ...(input.provider !== undefined
      ? { provider: text(input.provider, "provider", 256) }
      : {}),
    stopReason: text(input.stopReason, "stopReason", 1000),
  });
  const statementSha256 = sha256(JSON.stringify(statement));
  const requestId = `finish-${sha256(JSON.stringify([state.caseId, anchor.eventId]))}`;
  const eventId = `doctor-${sha256(JSON.stringify([state.caseId, requestId]))}`;
  const existing = state.observations.find(
    (entry) => entry.eventId === eventId,
  );
  if (existing) {
    if (
      existing.source !== "external_ai_skill_finish" ||
      existing.statementSha256 !== statementSha256
    )
      throw new Error(
        "Doctor finish attempt already has a different statement; the saved result was preserved. Start a new investigation with a new operation anchor.",
      );
    return existing;
  }
  if (guides.length) {
    const directory = await readCaseEvidence(info);
    if (
      guides.some(
        (guide) =>
          !directory.entries.some(
            (entry) =>
              entry.kind === "guidance" &&
              entry.ref === guide.ref &&
              entry.sha256 === guide.sha256,
          ),
      )
    )
      throw new Error(
        "Doctor finish guidance must match an actual directory reference and hash.",
      );
  }
  const repairs = observations.filter((entry) => entry.kind === "repair");
  return appendObservation(info, {
    action: "finish",
    agentStatement: statement,
    assessment: statement.assessment,
    assessmentQualification:
      "agent_statement; not_independent_recovery_evidence",
    attemptId: anchor.eventId,
    caseRepairPerformed: state.repairPerformed,
    checksAndVerification: observations.map((entry) => ({
      checks: entry.checks,
      error: entry.error,
      kind: entry.kind,
      nativeCallId: entry.nativeCallId,
      observationId: entry.observationId,
      operation: entry.operation,
      outcome: entry.outcome,
      recordedAt: entry.recordedAt,
      repairPerformed: entry.repairPerformed,
      resultSha256: entry.resultSha256,
      sessionBoundary: entry.sessionBoundary,
      source: entry.source,
    })),
    completionKind: "investigation",
    ...(binding
      ? {
          deliveryBackendOrigin: binding.identity.backendOrigin,
          deliveryIdentity: {
            projectId: binding.projectId,
            userId: binding.identity.userId,
          },
        }
      : {}),
    eventId,
    evidenceGaps: [
      ...state.evidenceGaps,
      "external_ai_turn_lifecycle_unobserved; finish_is_an_agent_statement",
      input.model
        ? "external_ai_model_identity_self_reported"
        : "external_ai_model_identity_unavailable",
      ...(guides.length ? [] : ["external_ai_guidance_use_unreported"]),
      ...(binding || info.manifest.target.surface === "hosted"
        ? []
        : ["automatic_result_delivery_requires_a_bound_current_desktop_case"]),
    ],
    finishedAt: new Date().toISOString(),
    kind: "investigation_result",
    observationIds: ids,
    originalFailureEventId: info.original.record?.failureEventId,
    outcome: "completed",
    qualification:
      "explicit_external_ai_skill_finish; no_host_terminal_hook; no_recovery_or_identity_authority",
    repairPerformed: repairs.some((entry) => entry.repairPerformed === true)
      ? true
      : repairs.some((entry) => entry.repairPerformed !== false)
        ? null
        : false,
    requestId,
    source: "external_ai_skill_finish",
    startedAt: anchor.startedAt,
    statementSha256,
    verifiedCaseStatus: state.status,
  });
}

function text(value, field, limit, nullable = false) {
  if (nullable && value === null) return null;
  if (typeof value !== "string" || !value.trim() || value.length > limit)
    throw new Error(`Doctor finish needs a bounded ${field}.`);
  return value;
}
