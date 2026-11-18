import { readdir, readFile, realpath, stat } from "node:fs/promises";
import { connect } from "node:net";
import path from "node:path";
import { setTimeout as delay } from "node:timers/promises";

import { ensureDesktop, resolveDesktopPaths } from "./desktop.mjs";
import { readDesktopEndpoint } from "./doctor.mjs";
import { DiagnosticError, listMcpTools, withDesktopRpc } from "./rpc.mjs";

export async function connectAgent(options, dependencies = {}) {
  const proof = await runAgentCommand(
    {
      ...options,
      action: "call",
      arguments: {},
      command: "tools",
      name: "get_active_project",
    },
    dependencies,
  );
  if (!proof.ok)
    return {
      access: "cli",
      command: "connect",
      ok: false,
      schemaVersion: 1,
      verification: proof.result,
    };
  let active = proof.result.structuredContent;
  if (!active) {
    for (const entry of proof.result.content) {
      if (entry.type !== "text") continue;
      try {
        const parsed = JSON.parse(entry.text);
        if (parsed?.surface) {
          active = parsed;
          break;
        }
      } catch {}
    }
  }
  if (active?.surface !== "desktop")
    throw new DiagnosticError(
      "unexpected_surface",
      "connect",
      "get_active_project did not confirm the Desktop surface.",
    );
  const skills = await runAgentCommand(
    { ...options, action: "list", command: "skills" },
    dependencies,
  );
  if (!skills.skillCount)
    throw new DiagnosticError(
      "skills_unavailable",
      "connect",
      "This Desktop bundle exposes no external skills. Update ChatCut Desktop before continuing.",
    );
  const tools = await runAgentCommand(
    { ...options, action: "list", command: "tools" },
    dependencies,
  );
  return {
    access: "cli",
    command: "connect",
    instruction:
      "Continue in this agent through chatcut skills read <name> and chatcut tools describe/call <name>. Run the commands yourself; the user need not configure MCP or restart this host. This verifies CLI access, not native host tool-table registration.",
    ok: true,
    schemaVersion: 1,
    skillCount: skills.skillCount,
    skillNames: skills.skills.map((skill) => skill.name),
    toolCount: tools.toolCount,
    toolNames: tools.tools.map((tool) => tool.name),
    verification: proof.result,
  };
}

export async function runAgentCommand(options, dependencies = {}) {
  const { action, command, name } = options;
  if (command === "tools" && action === "call") {
    if (
      !options.arguments ||
      typeof options.arguments !== "object" ||
      Array.isArray(options.arguments)
    )
      throw new Error("Tool arguments must be a JSON object.");
  }
  const desktop = await (dependencies.ensure ?? prepareDesktop)(options);
  if (command === "skills") return readSkills(desktop, options);
  const timeoutMs = action === "call" ? (options.timeoutMs ?? 300_000) : 20_000;
  const access =
    dependencies.mcp ??
    (async (transport, operation) =>
      withDesktopRpc(
        { ...transport, ...(await readDesktopEndpoint(desktop)) },
        operation,
      ));
  return access(
    {
      command: desktop.launcherPath,
      overallTimeoutMs: timeoutMs + 30_000,
      platform: desktop.platform,
      timeoutMs,
    },
    async (channel) => {
      const tools = await listMcpTools(channel);
      if (action === "list")
        return {
          action,
          command,
          ok: true,
          schemaVersion: 1,
          toolCount: tools.length,
          tools: tools.map((entry) => ({
            description:
              typeof entry.description === "string"
                ? entry.description.split("\n")[0].slice(0, 300)
                : undefined,
            name: entry.name,
          })),
        };
      const tool = tools.find((entry) => entry.name === name);
      if (!tool)
        throw new DiagnosticError(
          "unknown_tool",
          "tools/list",
          `Desktop does not expose tool ${name}. Run chatcut tools list.`,
        );
      if (action === "describe")
        return {
          action,
          command,
          ok: true,
          routing:
            "Pass the task's projectId with project-tool arguments. Desktop enforces explicit project routing; get_active_project does not select a target for later calls.",
          schemaVersion: 1,
          tool,
        };
      const result = await channel.request("tools/call", {
        arguments: options.arguments,
        name,
      });
      if (!result || !Array.isArray(result.content))
        throw new DiagnosticError(
          "invalid_tool_result",
          "tools/call",
          `${name} returned an invalid MCP tool result.`,
        );
      return {
        action,
        command,
        name,
        ok: !toolResultFailed(result),
        result,
        schemaVersion: 1,
      };
    },
  );
}

function assertContained(root, target) {
  const relative = path.relative(root, target);
  if (
    relative === ".." ||
    relative.startsWith(`..${path.sep}`) ||
    path.isAbsolute(relative)
  )
    throw new Error(
      "Skill files must stay inside their bundled skill directory.",
    );
}

function outcomeFailed(outcome, taskOutcome = false) {
  if (!outcome || typeof outcome !== "object") return false;
  if (Array.isArray(outcome))
    return outcome.some((entry) => outcomeFailed(entry, taskOutcome));
  if (outcome.isError === true) return true;
  // Running tasks can report ok:false until completion; a failed sibling still counts.
  if (
    outcome.terminal !== false &&
    (outcome.ok === false ||
      outcome.success === false ||
      ["error", "failed"].includes(outcome.status) ||
      // Cancellation receipts can succeed; lifecycle states need task context.
      ((taskOutcome || outcome.terminal === true) &&
        ["cancelled", "interrupted", "paused", "stale", "superseded"].includes(
          outcome.status,
        )))
  )
    return true;
  return (
    Array.isArray(outcome.entries) &&
    outcome.entries.some((entry) => outcomeFailed(entry, true))
  );
}

async function prepareDesktop(options) {
  let desktop = {
    ...resolveDesktopPaths(options),
    platform: options.platform ?? process.platform,
  };
  const ready = async () => {
    try {
      const { socketPath } = await readDesktopEndpoint(desktop);
      await new Promise((resolve, reject) => {
        const socket = connect(socketPath);
        const finish = (error) => {
          socket.destroy();
          error ? reject(error) : resolve();
        };
        socket.once("connect", () => finish());
        socket.once("error", finish);
        socket.setTimeout(1000, () =>
          finish(
            Object.assign(new Error("Desktop socket did not respond."), {
              code: "ETIMEDOUT",
            }),
          ),
        );
      });
      return true;
    } catch (error) {
      if (["EACCES", "EPERM"].includes(error.code))
        throw new DiagnosticError(
          error.code,
          "desktop-connection-permission",
          `${error.message} The agent's command environment cannot access Desktop's local connection. Ask the user to approve this same command in the host, then retry; do not ask them to copy commands or edit configuration. No Desktop tool was called.`,
          { cause: error },
        );
      if (
        [
          "ECONNREFUSED",
          "ENOENT",
          "ETIMEDOUT",
          "invalid_capability",
          "invalid_launcher",
        ].includes(error.code)
      )
        return false;
      throw error;
    }
  };
  if (await ready()) return desktop;
  desktop = await ensureDesktop(options);
  const deadline = Date.now() + 20_000;
  while (!(await ready())) {
    if (Date.now() >= deadline)
      throw new DiagnosticError(
        "desktop_startup_timeout",
        "desktop",
        "ChatCut opened but its local connection is not ready. Check the Desktop window for sign-in or startup errors.",
      );
    await delay(250);
  }
  return desktop;
}

async function readSkills(desktop, { action, file = "SKILL.md", name }) {
  const source = await readFile(desktop.launcherPath, "utf8");
  const quoted = source.match(/^export CHATCUT_MCP_SKILLS_DIR=('.*')$/m)?.[1];
  const directory =
    desktop.platform === "win32"
      ? source.match(/^set "CHATCUT_MCP_SKILLS_DIR=([^\r\n]*)"\r?$/m)?.[1]
      : quoted && /^'(?:[^']|'\\'')*'$/.test(quoted)
        ? quoted.slice(1, -1).replaceAll("'\\''", "'")
        : undefined;
  if (!directory)
    throw new DiagnosticError(
      "skills_unavailable",
      "skills",
      "Desktop's launcher does not expose bundled skills. Open or update ChatCut Desktop.",
    );
  const root = await realpath(directory);
  const skills = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    if (!entry.isDirectory() || (action === "read" && entry.name !== name))
      continue;
    const skillRoot = await realpath(path.join(root, entry.name));
    assertContained(root, skillRoot);
    let config;
    try {
      config = JSON.parse(
        await readFile(path.join(skillRoot, "skill.json"), "utf8"),
      );
    } catch (error) {
      if (error.code === "ENOENT") continue;
      throw error;
    }
    if (!config.surfaces?.includes("external")) continue;
    if (action === "read") {
      const target = await realpath(path.resolve(skillRoot, file));
      assertContained(skillRoot, target);
      if (!(await stat(target)).isFile())
        throw new Error("The skill reference must be a file.");
      return {
        action,
        command: "skills",
        content: await readFile(target, "utf8"),
        name,
        ok: true,
        path: target,
        schemaVersion: 1,
      };
    }
    const body = await readFile(path.join(skillRoot, "SKILL.md"), "utf8");
    skills.push({
      description: skillDescription(body),
      name: entry.name,
    });
  }
  if (action === "read")
    throw new DiagnosticError(
      "unknown_skill",
      "skills",
      `Desktop does not expose external skill ${name}. Run chatcut skills list.`,
    );
  return {
    action,
    command: "skills",
    ok: true,
    schemaVersion: 1,
    skillCount: skills.length,
    skills: skills.sort((a, b) => a.name.localeCompare(b.name)),
  };
}

function skillDescription(body) {
  const frontmatter = body.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
  const lines = (frontmatter ?? "").split(/\r?\n/);
  const index = lines.findIndex((line) => /^description:/.test(line));
  if (index < 0) return "";
  const scalar = lines[index].slice("description:".length).trim();
  if (/^[|>][+-]?$/.test(scalar)) {
    const parts = [];
    for (const line of lines.slice(index + 1)) {
      if (line.trim() && !/^\s/.test(line)) break;
      parts.push(line.trim());
    }
    return parts.join(" ").trim();
  }
  if (scalar.startsWith('"')) {
    try {
      return JSON.parse(scalar);
    } catch {
      return scalar;
    }
  }
  return scalar.startsWith("'") && scalar.endsWith("'")
    ? scalar.slice(1, -1).replaceAll("''", "'")
    : scalar;
}

function toolResultFailed(result) {
  if (result.isError === true) return true;
  if (result.structuredContent != null)
    return outcomeFailed(result.structuredContent);
  return result.content.some((entry) => {
    if (entry.type !== "text") return false;
    let payload;
    try {
      payload = JSON.parse(entry.text);
    } catch {
      return false;
    }
    return outcomeFailed(payload);
  });
}
