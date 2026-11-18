import { execFile } from "node:child_process";
import { writeFile } from "node:fs/promises";
import path from "node:path";
import { promisify } from "node:util";

import { sanitize } from "./cases.mjs";
import {
  collectHostLogs,
  errorDetails,
  runDoctor,
} from "./hosted/mcp-doctor.mjs";
import { doctorMessage } from "./messages.mjs";

const execute = promisify(execFile);

export async function checkHosted(
  target,
  {
    collectLogs = true,
    dir,
    online = false,
    original,
    repair = false,
    ...dependencies
  },
) {
  if (target.enabled === false)
    return {
      needsUser: true,
      nextAction: doctorMessage("hostedDisabled"),
      outcome: "intentionally_disabled",
      repairAvailable: false,
      repairPerformed: false,
    };
  const lookup = await lookupHosted(target, dependencies);
  const repairAvailable =
    lookup.status === "not_found" &&
    target.management === "manual" &&
    target.serverName === "chatcut" &&
    Boolean(target.endpoint);
  if (repair) {
    if (!repairAvailable)
      return {
        lookup,
        needsUser: true,
        nextAction: doctorMessage("hostedRepairUnavailable"),
        outcome: "repair_not_supported",
        repairAvailable: false,
        repairPerformed: false,
      };
    const args =
      target.host === "codex"
        ? ["mcp", "add", target.serverName, "--url", target.endpoint]
        : [
            "mcp",
            "add",
            "--transport",
            "http",
            "--scope",
            target.scope,
            target.serverName,
            target.endpoint,
          ];
    await runHost(target, args, dependencies.execute, dependencies.signal);
    const after = await lookupHosted(target, dependencies);
    const restored =
      after.status === "found" &&
      after.endpoint === target.endpoint &&
      after.scope === target.scope;
    return {
      after,
      command: { args, executable: target.cliPath },
      lookup,
      needsUser: restored,
      nextAction: doctorMessage("hostedAuthenticateAndRecheck"),
      outcome: restored ? "repaired" : "repair_failed",
      repairAvailable: false,
      repairPerformed: true,
      rollback:
        target.host === "codex"
          ? ["mcp", "remove", target.serverName]
          : ["mcp", "remove", "--scope", target.scope, target.serverName],
    };
  }
  const configurationMatches =
    lookup.status !== "found" ||
    (lookup.endpoint === target.endpoint && lookup.scope === target.scope);
  const disabled = lookup.enabled === false;
  const snapshot = {
    observations: [
      {
        lookupResult: lookup.status,
        message:
          lookup.message ??
          `Native lookup ${lookup.status}; active session unobserved.`,
        observedAt: new Date().toISOString(),
        operation: "lookup_registered_server",
        outcome: lookup.status === "found" ? "success" : "failed",
        source: "cli_configuration",
        stage: "host_registration",
      },
    ],
    observedAt: new Date().toISOString(),
    schemaVersion: 1,
  };
  if (lookup.status === "found" && configurationMatches && target.endpoint)
    snapshot.configuration = {
      enabled: lookup.enabled,
      serverName: target.serverName,
      source: "cli_configuration",
      url: target.endpoint,
    };
  const snapshotFile = path.join(dir, "current.mcp-snapshot.json");
  await writeFile(snapshotFile, JSON.stringify(snapshot), {
    flag: "wx",
    mode: 0o600,
  });
  let failureRecord;
  if (original.status === "recorded") {
    failureRecord = path.join(dir, "original.mcp-failure.json");
    await writeFile(failureRecord, JSON.stringify(sanitize(original.record)), {
      flag: "wx",
      mode: 0o600,
    });
  }
  const reportPath = path.join(dir, "diagnostic.mcp-report.json");
  const collected = await (dependencies.collect ?? runDoctor)(
    {
      failureRecord,
      host: target.host === "codex" ? "codex" : "claude",
      hostSnapshot: snapshotFile,
      offline: !online || !configurationMatches || disabled,
      output: reportPath,
      serverUrl: target.endpoint,
      upload: false,
    },
    {
      collectLogs: (host, options) =>
        collectLogs
          ? collectSelectedHostLogs(target, host, options)
          : {
              entries: [],
              gaps: [
                {
                  reason: "explicit_collection_consent_not_given",
                  source: "host_logs",
                },
              ],
            },
    },
  );
  return {
    diagnosticId: collected.report.diagnosticId,
    lookup,
    needsUser:
      disabled || !configurationMatches || lookup.status === "unavailable",
    nextAction: doctorMessage(
      disabled
        ? "connectionDisabled"
        : !configurationMatches
          ? "hostedTargetMismatch"
          : "hostedNativeRecheck",
    ),
    outcome: !configurationMatches ? "endpoint_mismatch" : "checked",
    repairAvailable: repairAvailable && !disabled,
    report: collected.report,
    reportPath,
  };
}

export function collectSelectedHostLogs(
  target,
  host,
  options,
  collect = collectHostLogs,
) {
  return collect(host, {
    ...options,
    claudeConfigDir: target.hostHome,
    codexAppLogDir: target.logLocations?.app,
    codexHome: target.hostHome,
    codexLogDir: target.logLocations?.text ?? path.join(target.hostHome, "log"),
    codexSqliteHome: target.logLocations?.sqlite ?? target.hostHome,
    codexStderrFile: target.logLocations?.stderr,
    platform: target.platform,
  });
}

export function hostEnvironment(target, env = process.env) {
  return {
    ...env,
    [target.host === "codex" ? "CODEX_HOME" : "CLAUDE_CONFIG_DIR"]:
      target.hostHome,
  };
}

export async function lookupHosted(target, dependencies = {}) {
  try {
    const result = await runHost(
      target,
      [
        "mcp",
        "get",
        target.serverName,
        ...(target.host === "codex" ? ["--json"] : []),
      ],
      dependencies.execute,
      dependencies.signal,
    );
    const text = result.stdout.trim();
    let endpoint;
    let enabled = null;
    let desktopTransport;
    let scope = target.host === "codex" ? "user" : null;
    if (target.host === "codex") {
      const config = JSON.parse(text);
      endpoint = config.transport?.url;
      enabled = typeof config.enabled === "boolean" ? config.enabled : null;
      if (target.surface === "desktop")
        desktopTransport = {
          client: config.transport?.env?.CHATCUT_MCP_CLIENT ?? null,
          command: config.transport?.command ?? null,
          type: config.transport?.type ?? null,
        };
    } else {
      endpoint = text.match(/^\s*URL:\s*(\S+)\s*$/m)?.[1];
      scope =
        text
          .match(/^\s*Scope:\s*(Local|Project|User) config/im)?.[1]
          ?.toLowerCase() ?? null;
    }
    return {
      enabled,
      endpoint: endpoint ?? null,
      scope,
      source: "native_cli_configuration; active_session_unobserved",
      ...(desktopTransport ? { desktopTransport } : {}),
      status: "found",
    };
  } catch (error) {
    const text = `${error.stdout ?? ""}\n${error.stderr ?? ""}`
      .replace(/\x1b\[[0-9;]*m/g, "")
      .trim();
    const absent =
      target.host === "codex"
        ? `Error: No MCP server named '${target.serverName}' found.`
        : `No MCP server named "${target.serverName}". Run \`claude mcp add\` to add one.`;
    if (error.code === 1 && text === absent)
      return {
        message: absent,
        source: "completed_native_no_entry_response",
        status: "not_found",
      };
    return {
      error: errorDetails(error),
      source: "native_cli_lookup",
      sourceOutputOmitted: true,
      status: "unavailable",
    };
  }
}

export async function runHost(target, args, run = execute, signal) {
  if (!target.cliPath)
    throw Object.assign(
      new Error(
        "The selected host CLI path is unavailable; no installation attempted.",
      ),
      { code: "HOST_CLI_UNAVAILABLE" },
    );
  if (target.platform !== process.platform)
    throw new Error(
      "A different platform host cannot be operated from this machine.",
    );
  return run(target.cliPath, args, {
    cwd: target.cwd,
    env: hostEnvironment(target),
    maxBuffer: 128 * 1024,
    timeout: 12_000,
    windowsHide: true,
    ...(signal ? { signal } : {}),
  });
}
