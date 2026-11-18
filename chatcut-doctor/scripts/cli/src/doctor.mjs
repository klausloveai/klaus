import { readFile } from "node:fs/promises";
import path from "node:path";
import { setTimeout as delay } from "node:timers/promises";

import { CLIENT_FAMILIES, hostHandoff } from "./clients.mjs";
import { inspectDesktop } from "./desktop.mjs";
import { DiagnosticError, probeMcp, requestDesktop } from "./rpc.mjs";

export function errorEvidence(error) {
  if (typeof error.toJSON === "function") return error.toJSON();
  return {
    code: error.code ?? "diagnostic_failed",
    message: error.message ?? String(error),
    stage: error.stage ?? "diagnostic",
    ...(error.cause
      ? {
          cause: {
            code: error.cause.code,
            message: error.cause.message ?? String(error.cause),
          },
        }
      : {}),
  };
}

export async function readDesktopEndpoint(desktop) {
  const contents = await readFile(desktop.launcherPath, "utf8");
  let socketPath;
  if (desktop.platform === "win32") {
    socketPath = contents.match(
      /^set "CHATCUT_MCP_SOCKET=([^\r\n]*)"\r?$/m,
    )?.[1];
  } else {
    const quoted = contents.match(/^export CHATCUT_MCP_SOCKET=('.*')$/m)?.[1];
    if (quoted && /^'(?:[^']|'\\'')*'$/.test(quoted))
      socketPath = quoted.slice(1, -1).replaceAll("'\\''", "'");
  }
  if (!socketPath)
    throw new DiagnosticError(
      "invalid_launcher",
      "desktop",
      "The Desktop MCP launcher has no readable socket path. Open ChatCut to refresh it.",
    );
  const capability = (
    await readFile(
      path.join(desktop.userDataPath, "mcp-invocation-capability"),
      "utf8",
    )
  ).trim();
  if (!/^[A-Za-z0-9_-]{43}$/.test(capability))
    throw new DiagnosticError(
      "invalid_capability",
      "desktop",
      "The Desktop IPC capability is missing or invalid. Open ChatCut to refresh it.",
    );
  return { capability, socketPath };
}

export async function runDoctor(options = {}, dependencies = {}) {
  const { client, fix = false } = options;
  const inspect = dependencies.inspect ?? inspectDesktop;
  const probe = dependencies.probe ?? probeMcp;
  const checks = [];
  const findings = [];
  const hostHandoffs = [];
  let desktop = await inspect(options);
  let repair;
  let state;
  checks.push({
    id: "desktop",
    message: desktop.installed
      ? `ChatCut ${desktop.version ?? ""} is installed.`.replaceAll("  ", " ")
      : "ChatCut Desktop is not installed. Run chatcut app.",
    path: desktop.appPath,
    status: desktop.installed ? "pass" : "fail",
  });
  if (desktop.installed) {
    try {
      const result = await inspectRunningDesktop(desktop, {
        ...dependencies,
        client,
        env: options.env,
        fix,
        platform: desktop.platform,
      });
      repair = result.repair;
      state = result;
      checks.push({
        id: "desktop-inspection",
        message: "Desktop answered the authenticated diagnostic request.",
        status: "pass",
      });
      for (const [name, integration] of Object.entries(
        result.integrations ?? {},
      )) {
        if (integration.actionRequired || integration.trustPending)
          findings.push({
            id: `action-${name}`,
            message:
              integration.actionRequired ??
              `${name}: approve trust for chatcut_desktop inside the host.`,
            status: "info",
          });
        if (
          client === name &&
          integration.actionRequired &&
          integration.status === "unavailable"
        ) {
          checks.push({
            id: `integration-${name}`,
            message: integration.actionRequired,
            status: "fail",
          });
          continue;
        }
        if (
          integration.status === "unavailable" ||
          integration.status === "disabled" ||
          integration.status === "opted-out"
        ) {
          findings.push({
            id: `integration-${name}`,
            message: `${name}: ${integration.status}.`,
            status: "info",
          });
          continue;
        }
        const connected =
          integration.status === "connected" && !integration.errorMessage;
        checks.push({
          id: `integration-${name}`,
          message: `${name}: ${integration.status}.`,
          status: connected ? "pass" : "fail",
          ...(integration.errorMessage
            ? {
                error: {
                  code: integration.errorCode,
                  message: integration.errorMessage,
                  stage: integration.stage,
                },
              }
            : {}),
        });
        const handoff = connected ? hostHandoff(name, integration) : undefined;
        if (handoff && (client === name || fix || integration.restartRequired))
          hostHandoffs.push({
            ...handoff,
            skillsRoot: result.skills?.targets?.[CLIENT_FAMILIES[name]]?.root,
          });
        if (integration.restartRequired && handoff)
          findings.push({
            id: `restart-${name}`,
            message: handoff.instruction,
            status: "info",
          });
      }
      if (result.account?.status === "sign-in-required")
        findings.push({
          id: "account",
          message:
            "Account-dependent tools guide sign-in on their next call. Local editing remains available while signed out.",
          status: "info",
        });
      for (const [target, skills] of Object.entries(
        result.skills?.targets ?? {},
      )) {
        const host = Object.keys(CLIENT_FAMILIES).find(
          (hostClient) => CLIENT_FAMILIES[hostClient] === target,
        );
        const required =
          !host || result.integrations?.[host]?.status === "connected";
        const stale =
          skills.stale?.filter((name) => !skills.modified?.includes(name)) ??
          [];
        checks.push({
          id: `skills-${target}`,
          message: `${skills.names?.length ?? 0} ChatCut skills expected for ${target}${required ? "" : " (host unavailable, disconnected or opted out)"}.`,
          path: skills.root,
          status:
            !required ||
            (!skills.errorMessage &&
              !skills.missing?.length &&
              !stale.length &&
              !skills.outdated?.length)
              ? "pass"
              : "fail",
          ...(skills.errorMessage
            ? {
                error: {
                  code: skills.errorCode,
                  message: skills.errorMessage,
                  stage: skills.stage,
                },
              }
            : {}),
          ...(skills.missing?.length ? { missing: skills.missing } : {}),
          ...(stale.length ? { stale } : {}),
          ...(skills.outdated?.length ? { outdated: skills.outdated } : {}),
        });
        if (skills.modified?.length || skills.foreign?.length)
          findings.push({
            foreign: skills.foreign,
            id: `preserved-skills-${target}`,
            message:
              "User-modified or foreign skill paths are preserved; inspect overlaps before changing them.",
            modified: skills.modified,
            path: skills.root,
            status: "info",
          });
        if (skills.overlaps?.length)
          findings.push({
            id: `skill-overlaps-${target}`,
            message:
              "These skill names overlap. A name match alone does not prove duplicate loading or justify deletion.",
            overlaps: skills.overlaps,
            path: skills.root,
            status: "info",
          });
      }
      if (repair?.errors?.length)
        checks.push({
          errors: repair.errors,
          id: "repair",
          message: "Some repairs failed; see the original errors.",
          status: "fail",
        });
    } catch (error) {
      checks.push({
        error: errorEvidence(error),
        id: "desktop-inspection",
        message:
          "Desktop inspection did not complete. Open ChatCut, or update it if doctor support is unavailable.",
        status: "fail",
      });
    }
    try {
      const mcp = await probe({
        command: desktop.launcherPath,
        env: options.env,
        platform: desktop.platform,
      });
      checks.push({
        evidence: mcp,
        id: "mcp",
        message:
          "MCP initialization, tool discovery and get_active_project succeeded.",
        status: "pass",
      });
    } catch (error) {
      checks.push({
        error: errorEvidence(error),
        id: "mcp",
        message: "The MCP connection did not complete a read-only tool call.",
        status: "fail",
      });
    }
  }
  findings.push({
    id: "host-session",
    message:
      "This probes a separate local MCP client. Check the current host's loaded tools and skills in that host, and follow its specific hostHandoffs instructions if a restart or new conversation is needed. Do not apply one generic reload instruction to every client.",
    status: "info",
  });
  findings.push({
    id: "task-continuation",
    message: `Carry the user's task forward

Choose the content below based on the user's request. If this conversation has verified access, act on it directly. Follow the hostHandoffs action for the specific host; do not require both a restart and a new conversation for every host. Prefer continuing through verified local CLI access when available. If a new conversation is required, prepare it automatically through the host's supported handoff when possible so the user only clicks. Also write a self-contained, ready-to-copy prompt now, in the user's voice and language, inside one fenced text block. Include the verified setup, supplied media (paths, URLs or asset IDs), selected workflow, project/workspace context, answers and decisions already provided, and any remaining setup steps so the next agent can verify access and continue. Include any files the user must reattach; do not assume conversation attachments transfer. Distinguish verified facts from pending setup, and never include credentials.

If the user already has a clear request, continue it and ask only for information still missing. For a new conversation, carry that same request and the answers already provided into the prompt. Do not replace their task with generic onboarding.

If the user has no creative request yet, follow the creation guidance in this example once access is verified, or include it in the prompt for the new conversation. Adapt the opening to the verified setup and the capabilities to the tools and Skills available. Keep the setup context and all requested next steps inside the copyable prompt; explanations outside it will not reach the next conversation.

Example (only retain installation and sign-in claims if verified):
ChatCut Desktop is already installed and signed in on this computer. Please confirm that you can use ChatCut, then help me start creating.

Tell me how you can help with video editing, motion graphics, and asset generation, including images, videos, voiceovers, music and sound effects.

Ask what materials I have and what kind of video I want to make, then guide me step by step based on my answers. Also let me know that I can open ChatCut Desktop at any time to adjust the timeline, captions and motion graphics myself.`,
    status: "info",
  });
  const ok = checks.every((check) => check.status !== "fail");
  return {
    checks,
    cliAccess: {
      instruction:
        "From a shell on the user's computer, use chatcut skills list/read and chatcut tools list/describe/call to continue immediately without native host registration or reload. These commands use Desktop's real MCP server. Verify the actual CLI result before claiming readiness; a cloud shell cannot reach this local socket.",
      verification:
        "Run chatcut connect --json in this host to verify CLI access separately from the STDIO diagnostic.",
    },
    command: "doctor",
    desktop,
    findings,
    hostAcceptance: "requires-verification-in-host",
    hostHandoffs,
    ok,
    repairRequested: fix,
    schemaVersion: 1,
    ...(repair ? { repair } : {}),
    ...(state ? { state } : {}),
  };
}

async function inspectRunningDesktop(
  desktop,
  {
    client,
    endpoint = readDesktopEndpoint,
    env = process.env,
    expectedProfile = "production",
    fix,
    platform = process.platform,
    request = requestDesktop,
    wait = delay,
  },
) {
  const deadline = Date.now() + (fix ? 20_000 : 0);
  const target = { client, env, expectedProfile, platform };
  for (;;) {
    try {
      const connection = await endpoint(desktop);
      const report = await request({
        ...connection,
        client,
        method: "desktop.doctor",
      });
      await validateDesktopReport(report, target);
      if (!fix) return report;
      const repaired = await request({
        ...connection,
        client,
        method: "desktop.repair",
      });
      await validateDesktopReport(repaired, target);
      return repaired;
    } catch (error) {
      if (
        fix &&
        ["ECONNREFUSED", "ENOENT"].includes(error.code) &&
        Date.now() < deadline
      ) {
        await wait(250);
        continue;
      }
      if (error.code === -32601)
        throw new DiagnosticError(
          "desktop_update_required",
          "desktop",
          "This Desktop version does not provide doctor diagnostics. Run chatcut update after closing ChatCut.",
          { cause: error },
        );
      throw error;
    }
  }
}

async function validateDesktopReport(
  report,
  { client, env, expectedProfile, platform },
) {
  if (report?.version !== 1)
    throw new DiagnosticError(
      "unsupported_doctor_report",
      "desktop",
      "Desktop returned an unsupported doctor report.",
    );
  if (report.profileId !== expectedProfile)
    throw new DiagnosticError(
      "profile_mismatch",
      "desktop",
      `Expected the ${expectedProfile} Desktop profile, received ${report.profileId}. Repair must target the selected profile.`,
    );
  for (const [host, target, variable] of [
    ["claude-code", "claudeCode", "CLAUDE_CONFIG_DIR"],
    ["hermes", "hermes", "HERMES_HOME"],
    ["deepseek-harness", "deepseekHarness", "DSH_HOME"],
  ]) {
    const root = report.skills?.targets?.[target]?.root;
    const paths = platform === "win32" ? path.win32 : path.posix;
    const selectedRoot =
      env[variable] && paths.resolve(env[variable], "skills");
    const reportedRoot = root && paths.resolve(root);
    let sameRoot =
      platform === "win32"
        ? selectedRoot?.toLowerCase() === reportedRoot?.toLowerCase()
        : selectedRoot === reportedRoot;
    if (
      (!client || client === host) &&
      selectedRoot &&
      root &&
      !sameRoot &&
      platform === process.platform
    ) {
      const { default: managed } = await import("../dist/managed-skills.cjs");
      try {
        sameRoot =
          managed.physicalSkillRoot(selectedRoot) ===
          managed.physicalSkillRoot(root);
      } catch (error) {
        if (error.code !== "ENOENT") throw error;
      }
    }
    if ((!client || client === host) && env[variable] && root && !sameRoot)
      throw new DiagnosticError(
        "agent_home_mismatch",
        "desktop",
        `${host} in Desktop uses a different ${variable} skill root (${root}). Start Desktop in the intended host environment before repair.`,
      );
  }
}
