import { fileURLToPath } from "node:url";

import { errorEvidence } from "./doctor.mjs";

const TARGETS = { "claude-code": "claudeCode", codex: "agents" };

/** Explicit instruction-file distribution; never probes, installs or opens Desktop. */
export async function manageAcquisitionSkills(options, dependencies = {}) {
  const managed =
    dependencies.managed ??
    (await import("../dist/managed-skills.cjs")).default;
  const selected = options.client
    ? [TARGETS[options.client]]
    : ["agents", "claudeCode"];
  if (selected.some((target) => !target))
    throw new Error(
      "Skill installation supports --client claude-code or codex.",
    );
  const locations = {
    env: dependencies.env ?? process.env,
    ...(dependencies.homeDir ? { homeDir: dependencies.homeDir } : {}),
  };
  const rootErrors = managed.desktopSkillRootErrors(locations);
  const targets = {};
  for (const target of selected) {
    const input = { ...locations, enabled: { [target]: true } };
    const root = managed.getDesktopUserSkillsRoot(target, input);
    try {
      if (rootErrors[target]) throw rootErrors[target];
      const report =
        options.action === "remove"
          ? managed.removeManagedDesktopSkillsFromUserDirs(input)
          : managed.syncDesktopSkillsToUserDirs({
              ...input,
              mode: "materialized",
              sourceDir: fileURLToPath(
                new URL(`../dist/skills/${target}/`, import.meta.url),
              ),
            });
      const result = report[target];
      targets[target] = {
        ...result,
        ...(result.error ? { error: errorEvidence(result.error) } : {}),
        ...(result.legacyCleanupErrors?.length
          ? {
              legacyCleanupErrors:
                result.legacyCleanupErrors.map(errorEvidence),
            }
          : {}),
        root,
      };
    } catch (error) {
      targets[target] = { error: errorEvidence(error), root };
    }
  }
  return {
    action: options.action,
    command: "skills",
    instruction:
      options.action === "remove"
        ? "Check each target's removed, skippedForeign and error fields before claiming removal. Only unchanged owned ChatCut skill files are removed. User edits, foreign entries and native MCP registration are preserved."
        : "Check each target's materialized, skippedForeign and error fields before claiming discovery. Start a new host session after successful installation. Desktop has not been downloaded, installed, opened or connected. A later Desktop install requires a fresh host permission click for connect --allow-install.",
    ok: Object.values(targets).every(
      (target) => !target.error && !target.skippedForeign.length,
    ),
    schemaVersion: 1,
    targets,
  };
}
