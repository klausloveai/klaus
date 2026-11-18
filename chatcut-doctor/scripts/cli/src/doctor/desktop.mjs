import { readFile } from "node:fs/promises";
import path from "node:path";

import { readDesktopEndpoint } from "../doctor.mjs";
import { requestDesktop } from "../rpc.mjs";
import { canonicalPath } from "./cases.mjs";
import { lookupHosted } from "./hosted.mjs";

export async function checkDesktop(
  target,
  {
    endpoint = readDesktopEndpoint,
    repair = false,
    request = requestDesktop,
    signal,
  } = {},
) {
  if (target.platform !== process.platform)
    throw new Error(
      "A different platform target cannot be operated from this machine.",
    );
  if (target.enabled === false)
    return {
      needsUser: true,
      nextAction: doctorMessage("connectionDisabled"),
      outcome: "intentionally_disabled",
      repairAvailable: false,
      repairPerformed: false,
    };
  const desktop = {
    launcherPath: target.launcher,
    platform: target.platform,
    userDataPath: target.userData,
  };
  const text = await readFile(target.launcher, "utf8");
  const profile =
    target.platform === "win32"
      ? text.match(/^set "CHATCUT_MCP_PROFILE=([^\r\n]*)"\r?$/m)?.[1]
      : text.match(/^export CHATCUT_MCP_PROFILE='([^']*)'$/m)?.[1];
  if (profile !== target.profile)
    throw new Error(
      "Selected launcher profile does not match; no repair executed.",
    );
  const connection = await endpoint(desktop);
  const invoke = async (method) =>
    validateReport(
      await request({
        ...connection,
        client: target.host,
        method,
        signal,
        ...(method === "desktop.repair"
          ? { repairMode: "missing-registration" }
          : {}),
      }),
      target,
    );
  const before = await invoke("desktop.doctor");
  const integration = before.integrations?.[target.host];
  const noConflicts =
    !integration?.conflictingPluginIds?.length &&
    !integration?.conflictingMcpNames?.length;
  const repairAvailable =
    integration?.status === "not-connected" &&
    noConflicts &&
    before.launcher?.status === "ready";
  if (repair && !repairAvailable)
    return {
      needsUser: true,
      nextAction: doctorMessage("desktopRepairUnavailable"),
      outcome: "repair_not_supported",
      repairAvailable: false,
      repairPerformed: false,
      report: before,
    };
  const report = repair ? await invoke("desktop.repair") : before;
  const current = report.integrations?.[target.host];
  const connected = current?.status === "connected";
  return {
    needsUser:
      report.account?.status === "sign-in-required" ||
      current?.status === "opted-out" ||
      current?.status === "unavailable" ||
      (repair && connected),
    nextAction: doctorMessage(
      current?.status === "opted-out"
        ? "connectionDisabled"
        : report.account?.status === "sign-in-required"
          ? "desktopSignIn"
          : repair && connected
            ? "desktopReloadAndRecheck"
            : "desktopNativeRecheck",
    ),
    outcome: repair
      ? connected && !report.repair?.errors?.length
        ? "repaired"
        : "repair_failed"
      : "checked",
    repairAvailable,
    repairPerformed: repair
      ? Array.isArray(report.repair?.changes)
        ? report.repair.changes.length > 0
        : null
      : false,
    report,
  };
}
import { doctorMessage } from "./messages.mjs";

export async function checkDesktopNativeRegistration(
  target,
  dependencies = {},
) {
  if (target.enabled === false) return { status: "disabled" };
  const text = await readFile(target.launcher, "utf8");
  const windows = target.platform === "win32";
  const profile = windows
    ? text.match(/^set "CHATCUT_MCP_PROFILE=([^\r\n]*)"\r?$/m)?.[1]
    : text.match(/^export CHATCUT_MCP_PROFILE='([^']*)'$/m)?.[1];
  const userData = windows
    ? text.match(/^set "CHATCUT_MCP_USER_DATA=([^\r\n]*)"\r?$/m)?.[1]
    : text.match(/^export CHATCUT_MCP_USER_DATA='([^']*)'$/m)?.[1];
  if (
    profile !== target.profile ||
    !userData ||
    canonicalPath(userData, target.platform) !== target.userData
  )
    return {
      source: "selected_launcher_profile_or_userData",
      status: "target_mismatch",
    };
  if (target.backendOrigin) await selectedDesktopTelemetryOrigin(target);
  const lookup = await lookupHosted(target, dependencies);
  const transport = lookup.desktopTransport;
  const ready =
    lookup.status === "found" &&
    lookup.enabled === true &&
    lookup.scope === target.scope &&
    transport?.type === "stdio" &&
    typeof transport.command === "string" &&
    canonicalPath(transport.command, target.platform) === target.launcher &&
    transport.client === "codex_app";
  return {
    lookup,
    source: "selected_native_configuration; not_recovery_proof",
    status: ready ? "ready" : "unverified",
  };
}

export async function selectedDesktopTelemetryOrigin(target) {
  if (!target.backendOrigin)
    throw new Error(
      "No selected Desktop telemetry origin is available; local report retained.",
    );
  const text = await readFile(target.launcher, "utf8");
  const profile =
    target.platform === "win32"
      ? text.match(/^set "CHATCUT_MCP_PROFILE=([^\r\n]*)"\r?$/m)?.[1]
      : text.match(/^export CHATCUT_MCP_PROFILE='([^']*)'$/m)?.[1];
  if (profile !== target.profile)
    throw new Error(
      "Desktop launcher profile differs from the selected target; no report sent.",
    );
  const backend =
    target.platform === "win32"
      ? text.match(/^set "CHATCUT_MCP_BACKEND_BASE_URL=([^\r\n]*)"\r?$/m)?.[1]
      : text.match(/^export CHATCUT_MCP_BACKEND_BASE_URL='([^']*)'$/m)?.[1];
  if (!backend || new URL(backend).origin !== target.backendOrigin)
    throw new Error(
      "Desktop launcher backend differs from the selected telemetry origin; no report sent.",
    );
  return target.backendOrigin;
}

function validateReport(report, target) {
  if (report?.version !== 1 || report.profileId !== target.profile)
    throw new Error(
      "Desktop doctor version/profile does not match the selected target; no repair executed.",
    );
  if (
    !report.launcher?.path ||
    canonicalPath(report.launcher.path, target.platform) !== target.launcher
  )
    throw new Error(
      "Desktop answered for another launcher or instance; no repair executed.",
    );
  const family = target.host === "codex" ? "chatGpt" : "claudeCode";
  const root = report.skills?.targets?.[family]?.root;
  const paths = target.platform === "win32" ? path.win32 : path.posix;
  if (
    !root ||
    canonicalPath(root, target.platform) !==
      canonicalPath(paths.join(target.hostHome, "skills"), target.platform)
  )
    throw new Error(
      "Desktop uses a different selected host home; no repair executed.",
    );
  return report;
}
