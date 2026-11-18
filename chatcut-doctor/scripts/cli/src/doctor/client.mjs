import { randomUUID } from "node:crypto";

import { errorDetails } from "./hosted/mcp-doctor.mjs";

export const CLIENT_DIAGNOSTIC_CASES = Object.freeze([
  {
    action: "normal_client_sign_in",
    excludes: ["MCP OAuth or Web cookies inferred from another surface"],
    id: "account",
    recheck: "actual selected client project read",
    repair: false,
    requiredEvidence: "Selected client credential-presence check",
    source: "Desktop account and project runtime",
    symptom: "Cloud account unavailable",
    userAction:
      "Sign in through the selected client's normal account flow; then recheck this case.",
  },
  {
    action: "check_selected_connection",
    excludes: ["anonymous MCP401", "old independent success"],
    id: "backend",
    recheck: "actual selected service read",
    repair: false,
    requiredEvidence: "Current selected backend connectivity result",
    source: "Existing backend connectivity monitor",
    symptom: "Selected backend unavailable",
    userAction:
      "Check the selected backend connection without changing another profile or login.",
  },
  {
    action: "inspect_original_project_error",
    excludes: ["tools/list", "configuration", "different project"],
    id: "project",
    recheck: "actual read_project on the same project",
    repair: false,
    requiredEvidence: "Actual read_project error and projectId",
    source: "Selected client project runtime",
    symptom: "Current project cannot be read",
    userAction:
      "Keep the original error and follow its actual cause; do not infer an authentication failure.",
  },
]);

export function clientDiagnosticCases(target, facts) {
  if (facts.checks.some((check) => check.status === "unknown")) return [];
  return CLIENT_DIAGNOSTIC_CASES.flatMap((entry) => {
    const check = facts.checks.find((value) => value.id === entry.id);
    if (
      !check ||
      check.status !== "needs_user" ||
      (entry.id === "account" &&
        (typeof check.evidence !== "string" ||
          ![
            "selected_client_credential_presence",
            "selected_client_session_validated",
          ].some((source) => check.evidence.startsWith(source))))
    )
      return [];
    return [
      {
        ...entry,
        applicability: {
          capability: "selected_client_runtime_checks",
          contractVersion: 1,
          host: target.host,
          observedAppVersion:
            facts.checks.find((value) => value.id === "runtime")?.appVersion ??
            null,
          projectId: target.projectId ?? null,
          releasedVersionCoverage:
            "unverified; requires runtime capability, not an assumed release range",
          surface: target.surface,
        },
        observedStatus: check.status,
        unknowns: [
          "external_host_session_and_authorization",
          "all_user_recovery",
          ...(check.status === "unknown" ? ["root_cause_unconfirmed"] : []),
        ],
      },
    ];
  });
}

const EXTERNAL_DIAGNOSTIC_CASES = [
  {
    action: "respect_disabled_connection",
    excludes: ["A missing tool alone"],
    id: "disabled_connection",
    requiredEvidence:
      "Selected target or native registration reports disabled/opted-out",
    symptom: "Selected connection is intentionally disabled",
    userAction:
      "Enable the original connection yourself only if intended; Doctor must not override the opt-out.",
  },
  {
    action: "review_missing_registration",
    excludes: [
      "CLI lookup failed or timed out",
      "A different host registration",
    ],
    id: "missing_registration",
    requiredEvidence:
      "Completed native no-entry response or selected Desktop integration not-connected",
    symptom: "Selected ChatCut registration is absent",
    userAction:
      "Review the exact host and scope before explicitly authorizing a supported registration repair.",
  },
  {
    action: "review_original_registration",
    excludes: ["An anonymous HTTP401", "Another profile's configuration"],
    id: "registration_conflict",
    requiredEvidence:
      "Selected native endpoint/scope mismatch or Desktop conflicting registration IDs",
    symptom: "Selected connection has a conflicting or different registration",
    userAction:
      "Keep the original configuration and choose the intended connection; do not overwrite it automatically.",
  },
  {
    action: "normal_client_sign_in",
    excludes: [
      "Hosted MCP OAuth",
      "Browser cookies",
      "Credential presence alone",
    ],
    id: "desktop_account",
    requiredEvidence: "Selected Desktop doctor account status sign-in-required",
    symptom: "Selected Desktop account requires sign-in",
    userAction:
      "Use the selected Desktop's normal sign-in, then repeat the actual read in the original host.",
  },
  {
    action: "native_host_read",
    excludes: ["Tool lists", "Local-client success", "Standalone HTTP success"],
    id: "external_read_unverified",
    requiredEvidence:
      "Configuration/connection diagnostics without a matching actual native safe read",
    symptom: "Original external-host tool availability is not verified",
    userAction:
      "Repeat the affected safe read in the original host and append its actual result to this case.",
  },
];

export function externalDiagnosticCases(target, result) {
  const integration = result.report?.integrations?.[target.host];
  const id =
    target.enabled === false ||
    result.outcome === "intentionally_disabled" ||
    result.lookup?.enabled === false ||
    integration?.status === "opted-out"
      ? "disabled_connection"
      : result.outcome === "endpoint_mismatch" ||
          (Array.isArray(integration?.conflictingPluginIds) &&
            integration.conflictingPluginIds.length > 0) ||
          (Array.isArray(integration?.conflictingMcpNames) &&
            integration.conflictingMcpNames.length > 0)
        ? "registration_conflict"
        : result.lookup?.status === "not_found" ||
            integration?.status === "not-connected"
          ? "missing_registration"
          : target.surface === "desktop" &&
              integration?.status === "connected" &&
              result.report?.account?.status === "sign-in-required"
            ? "desktop_account"
            : "external_read_unverified";
  if (id === "external_read_unverified") return [];
  return [
    {
      ...EXTERNAL_DIAGNOSTIC_CASES.find((entry) => entry.id === id),
      applicability: {
        capability: "selected_native_registration_and_connection_diagnostics",
        contractVersion: 1,
        host: target.host,
        releasedVersionCoverage:
          "unverified; use the observed runtime and installed helper version",
        scope: target.scope,
        serverName: target.serverName,
        surface: target.surface,
      },
      recheck:
        target.surface === "hosted"
          ? "actual list_projects in the original host"
          : "actual read_project for the same project in the original host",
      repair: false,
      source:
        result.lookup?.source ??
        result.report?.source ??
        "selected_connection_program_observation",
      unknowns: [
        "original_host_session",
        "original_request_HTTP_bytes_unless_captured",
        "all_user_recovery",
      ],
    },
  ];
}

export function externalDoctorNextActionId(target, result = {}) {
  return externalDiagnosticCases(target, result)[0]?.action;
}

export async function inspectClient(target, { inspect } = {}) {
  if (target.host !== "chatcut")
    throw new Error("Select the ChatCut client target.");
  if (!inspect)
    return {
      checks: [],
      needsUser: true,
      nextAction: "open_selected_client",
      outcome: "unavailable",
      repairAvailable: false,
      repairPerformed: false,
    };
  const facts = await inspect(target);
  if (
    !facts ||
    !Array.isArray(facts.checks) ||
    facts.checks.length > 12 ||
    facts.checks.some(
      (check) =>
        !["needs_user", "not_run", "pass", "unknown"].includes(check.status) ||
        !["account", "backend", "project", "runtime"].includes(check.id),
    )
  )
    throw new Error(
      "Client checks must be bounded observations of the selected instance.",
    );
  const failed = facts.checks.find(
    (check) => check.status === "needs_user" || check.status === "unknown",
  );
  return {
    checks: facts.checks,
    diagnosticCases: clientDiagnosticCases(target, facts),
    ...(facts.projectRead ? { projectRead: facts.projectRead } : {}),
    diagnosticId: randomUUID(),
    needsUser: failed?.status === "needs_user",
    nextAction: failed
      ? `${failed.id}_attention`
      : target.projectId
        ? "continue_task"
        : "open_project_to_verify_tools",
    observedAt: new Date().toISOString(),
    originalError: facts.originalError
      ? {
          ...errorDetails(facts.originalError.error),
          callId: facts.originalError.callId ?? null,
          failureEventId: facts.originalError.failureEventId ?? null,
          occurredAt: facts.originalError.occurredAt ?? null,
          operation: facts.originalError.operation,
        }
      : null,
    outcome: "checked",
    repairAvailable: false,
    repairPerformed: false,
    scope:
      "selected_client_basic_checks; not_external_host_or_all_user_recovery",
  };
}
