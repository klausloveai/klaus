import { spawn } from "node:child_process";
import { connect } from "node:net";
import { StringDecoder } from "node:string_decoder";

import packageInfo from "../package.json" with { type: "json" };

const MAX_MESSAGE_BYTES = 4 * 1024 * 1024;
const PROTOCOL_VERSIONS = [
  "2025-11-25",
  "2025-06-18",
  "2025-03-26",
  "2024-11-05",
];

export class DiagnosticError extends Error {
  constructor(code, stage, message, options = {}) {
    super(message, options);
    this.code = code;
    this.stage = stage;
  }
}

export async function listMcpTools(channel) {
  const tools = [];
  const names = new Set();
  let cursor;
  const cursors = new Set();
  for (let page = 0; page < 20; page++) {
    const result = await channel.request(
      "tools/list",
      cursor ? { cursor } : {},
    );
    if (!Array.isArray(result?.tools))
      throw new DiagnosticError(
        "invalid_tools_list",
        "tools/list",
        "The server returned no tools array.",
      );
    for (const tool of result.tools)
      if (typeof tool.name === "string" && !names.has(tool.name)) {
        names.add(tool.name);
        tools.push(tool);
      }
    cursor = result.nextCursor;
    if (!cursor) break;
    if (typeof cursor !== "string" || cursors.has(cursor) || page === 19)
      throw new DiagnosticError(
        "invalid_tools_pagination",
        "tools/list",
        "MCP tool pagination did not complete within 20 pages.",
      );
    cursors.add(cursor);
  }
  return tools;
}

export async function probeMcp(options) {
  return withMcp(options, async (channel, initialized) => {
    const tools = await listMcpTools(channel);
    const names = new Set(tools.map((tool) => tool.name));
    if (!names.has("get_active_project"))
      throw new DiagnosticError(
        "missing_discovery_tool",
        "tools/list",
        "ChatCut's get_active_project tool is missing.",
      );
    const result = await channel.request("tools/call", {
      arguments: {},
      name: "get_active_project",
    });
    if (result?.isError) {
      const message = result.content
        ?.filter((item) => item.type === "text")
        .map((item) => item.text)
        .join("\n");
      throw new DiagnosticError(
        "tool_call_failed",
        "tools/call",
        message || "get_active_project returned an error.",
      );
    }
    if (!result || !Array.isArray(result.content))
      throw new DiagnosticError(
        "invalid_tool_result",
        "tools/call",
        "get_active_project returned an invalid MCP tool result.",
      );
    const server = initialized.serverInfo;
    return {
      hostSessionDiscovery: "unobserved",
      protocolVersion: initialized.protocolVersion,
      server: {
        name: server?.name,
        title: server?.title,
        version: server?.version,
      },
      status: "pass",
      toolCall: { name: "get_active_project", status: "pass" },
      toolCount: names.size,
    };
  });
}

export async function requestDesktop({
  capability,
  client,
  method,
  repairMode,
  signal,
  socketPath,
  timeoutMs = 30_000,
}) {
  signal?.throwIfAborted();
  const socket = connect(socketPath);
  const channel = createRpcChannel(
    socket,
    (message) => socket.write(`${JSON.stringify(message)}\n`),
    timeoutMs,
  );
  const aborted = () => channel.fail(signal.reason);
  signal?.addEventListener("abort", aborted, { once: true });
  try {
    return await channel.request(
      method,
      { ...(client ? { client } : {}), ...(repairMode ? { repairMode } : {}) },
      {
        invocationCapability: capability,
      },
    );
  } finally {
    signal?.removeEventListener("abort", aborted);
    socket.destroy();
  }
}

export async function withDesktopRpc(
  {
    capability,
    timeoutMs = 300_000,
    overallTimeoutMs = timeoutMs + 30_000,
    socketPath,
  },
  operation,
) {
  const socket = connect(socketPath);
  const write = (message) => socket.write(`${JSON.stringify(message)}\n`);
  const channel = createRpcChannel(socket, write, timeoutMs, (message) => {
    if (
      message.method === "chatcut/elicitation" &&
      typeof message.params?.elicitationId === "string"
    )
      write({
        invocationCapability: capability,
        jsonrpc: "2.0",
        method: "chatcut/elicitation-reply",
        params: {
          code: "CLI_FORM_UNSUPPORTED",
          elicitationId: message.params.elicitationId,
          error:
            "This CLI cannot display native permission forms. Complete the permission step in ChatCut Desktop or a host with form support; no approval was granted.",
        },
      });
  });
  const timer = setTimeout(
    () =>
      channel.fail(
        new DiagnosticError(
          "timeout",
          "desktop",
          "The Desktop tool operation timed out. Inspect Desktop state before repeating a mutation.",
        ),
      ),
    overallTimeoutMs,
  );
  try {
    return await operation({
      request(method, params) {
        const mapped = {
          "tools/call": "tools.call",
          "tools/list": "tools.list",
        }[method];
        if (!mapped)
          throw new Error(`Unsupported Desktop tool operation: ${method}`);
        return channel.request(mapped, params, {
          invocationCapability: capability,
        });
      },
    });
  } finally {
    clearTimeout(timer);
    socket.destroy();
  }
}

export async function withMcp(
  {
    args = [],
    command,
    env = process.env,
    overallTimeoutMs = 60_000,
    platform = process.platform,
    spawnProcess = spawn,
    timeoutMs = 20_000,
  },
  operation,
) {
  const childEnv = { ...env };
  for (const key of Object.keys(childEnv)) {
    if (key.startsWith("CHATCUT_MCP_")) delete childEnv[key];
  }
  const isWindowsScript = platform === "win32" && /\.(cmd|bat)$/i.test(command);
  if (isWindowsScript && (/[\r\n\0"]/u.test(command) || args.length))
    throw new DiagnosticError(
      "invalid_launcher",
      "transport",
      "The Windows MCP launcher must be an unquoted path without arguments.",
    );
  if (isWindowsScript) childEnv.CHATCUT_DOCTOR_LAUNCHER = command;
  const child = spawnProcess(
    isWindowsScript ? (env.ComSpec ?? env.COMSPEC ?? "cmd.exe") : command,
    isWindowsScript
      ? ["/d", "/s", "/c", '""%CHATCUT_DOCTOR_LAUNCHER%""']
      : args,
    {
      env: childEnv,
      shell: false,
      stdio: ["pipe", "pipe", "pipe"],
      windowsHide: true,
      ...(isWindowsScript ? { windowsVerbatimArguments: true } : {}),
    },
  );
  let stderr = "";
  let stopped = false;
  child.stderr.on("data", (chunk) => {
    if (stderr.length < 64 * 1024)
      stderr += chunk.toString("utf8").slice(0, 64 * 1024 - stderr.length);
  });
  const channel = createRpcChannel(
    child.stdout,
    (message) => child.stdin.write(`${JSON.stringify(message)}\n`),
    timeoutMs,
  );
  const overallTimer = setTimeout(
    () =>
      channel.fail(
        new DiagnosticError(
          "timeout",
          "mcp",
          `The MCP operation exceeded ${overallTimeoutMs} ms. A timed-out tool may still have changed Desktop state; inspect it before retrying.`,
        ),
      ),
    overallTimeoutMs,
  );
  child.on("error", (cause) =>
    channel.fail(
      new DiagnosticError(
        cause.code ?? "spawn_failed",
        "transport",
        cause.message,
        { cause },
      ),
    ),
  );
  child.stdin.on("error", (cause) => channel.fail(cause));
  child.on("exit", (code, signal) => {
    stopped = true;
    channel.fail(
      new DiagnosticError(
        "process_exited",
        "transport",
        `MCP process exited (${signal ?? code}).${stderr ? ` ${stderr.trim()}` : ""}`,
      ),
    );
  });
  try {
    const initialized = await channel.request("initialize", {
      capabilities: {},
      clientInfo: { name: "chatcut-cli", version: packageInfo.version },
      protocolVersion: PROTOCOL_VERSIONS[0],
    });
    if (
      !PROTOCOL_VERSIONS.includes(initialized?.protocolVersion) ||
      !initialized.capabilities?.tools
    ) {
      throw new DiagnosticError(
        "unsupported_mcp_server",
        "initialize",
        "The server did not negotiate a supported MCP version with tools.",
      );
    }
    channel.notify("notifications/initialized");
    return await operation(channel, initialized);
  } finally {
    clearTimeout(overallTimer);
    child.stdin.end();
    if (!stopped) {
      child.kill();
      const timer = setTimeout(() => {
        if (!stopped) child.kill("SIGKILL");
      }, 1_000);
      timer.unref();
    }
  }
}

function createRpcChannel(stream, write, timeoutMs, onNotification) {
  const pending = new Map();
  const decoder = new StringDecoder("utf8");
  let buffer = "";
  let nextId = 0;
  let failure;

  function fail(error) {
    failure ??= error;
    for (const request of pending.values()) {
      clearTimeout(request.timer);
      request.reject(error);
    }
    pending.clear();
  }

  stream.on("data", (chunk) => {
    buffer += decoder.write(chunk);
    if (Buffer.byteLength(buffer) > MAX_MESSAGE_BYTES) {
      fail(
        new DiagnosticError(
          "response_too_large",
          "transport",
          "MCP response exceeded 4 MiB.",
        ),
      );
      return;
    }
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";
    for (const line of lines) {
      if (!line.trim()) continue;
      let message;
      try {
        message = JSON.parse(line);
      } catch (cause) {
        fail(
          new DiagnosticError(
            "invalid_rpc_response",
            "transport",
            "The MCP process wrote non-JSON data to stdout.",
            { cause },
          ),
        );
        return;
      }
      if (
        !message ||
        typeof message !== "object" ||
        message.jsonrpc !== "2.0"
      ) {
        fail(
          new DiagnosticError(
            "invalid_rpc_response",
            "transport",
            "Invalid JSON-RPC response.",
          ),
        );
        return;
      }
      if (message.method) {
        if (message.id === undefined && onNotification) {
          try {
            onNotification(message);
          } catch (error) {
            fail(error);
          }
        }
        if (message.id !== undefined) {
          write({
            id: message.id,
            jsonrpc: "2.0",
            ...(message.method === "ping"
              ? { result: {} }
              : {
                  error: {
                    code: -32601,
                    message: "Unsupported diagnostic client request",
                  },
                }),
          });
        }
        continue;
      }
      const waiting = pending.get(message.id);
      if (!waiting) continue;
      clearTimeout(waiting.timer);
      pending.delete(message.id);
      if (message.error) {
        waiting.reject(
          new DiagnosticError(
            message.error.code ?? "rpc_error",
            waiting.method,
            message.error.message ?? "JSON-RPC request failed.",
          ),
        );
      } else if (Object.hasOwn(message, "result")) {
        waiting.resolve(message.result);
      } else {
        waiting.reject(
          new DiagnosticError(
            "invalid_rpc_response",
            waiting.method,
            "JSON-RPC response contains neither result nor error.",
          ),
        );
      }
    }
  });
  stream.on("error", fail);
  stream.on("end", () =>
    fail(
      new DiagnosticError(
        "connection_closed",
        "transport",
        "The MCP connection closed before completing the diagnostic.",
      ),
    ),
  );

  return {
    fail,
    notify(method, params = {}) {
      write({ jsonrpc: "2.0", method, params });
    },
    request(method, params = {}, extra = {}) {
      if (failure) return Promise.reject(failure);
      return new Promise((resolve, reject) => {
        const id = ++nextId;
        const timer = setTimeout(() => {
          pending.delete(id);
          reject(
            new DiagnosticError(
              "timeout",
              method,
              `${method} did not respond within ${timeoutMs} ms.`,
            ),
          );
        }, timeoutMs);
        pending.set(id, { method, reject, resolve, timer });
        try {
          write({ id, jsonrpc: "2.0", method, params, ...extra });
        } catch (error) {
          clearTimeout(timer);
          pending.delete(id);
          reject(error);
        }
      });
    },
  };
}
