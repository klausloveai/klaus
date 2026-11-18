import { spawn } from "node:child_process";
import { writeFile } from "node:fs/promises";
import readline from "node:readline";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { readTarget, sanitize, targetFingerprint } from "./cases.mjs";
import { hostEnvironment } from "./hosted.mjs";
import { errorDetails } from "./hosted/mcp-doctor.mjs";

export async function codexNativeRead({
  discoverSkills = false,
  executable,
  operation,
  output,
  projectId,
  signal,
  spawnProcess = spawn,
  target,
}) {
  signal?.throwIfAborted();
  const fingerprint = targetFingerprint(target);
  if (!output?.endsWith(".doctor-recheck.json"))
    throw new Error("Use a dedicated .doctor-recheck.json output.");
  if (
    target.host !== "codex" ||
    !(
      target.surface === "hosted"
        ? ["list_projects"]
        : ["get_active_project", "read_project", "list_projects"]
    ).includes(operation)
  )
    throw new Error("Select a safe read on the actual Codex target.");
  if (target.enabled === false)
    throw new Error(
      "The selected connection is intentionally disabled; no native call executed.",
    );
  if (
    target.surface === "desktop" &&
    operation === "read_project" &&
    (typeof projectId !== "string" || !projectId.trim())
  )
    throw new Error("Select the actual Desktop projectId before read_project.");
  const trace = [];
  const args =
    target.management === "plugin"
      ? ["app-server", "--stdio"]
      : [
          "-c",
          "features.plugins=false",
          "-c",
          "features.apps=false",
          "app-server",
          "--stdio",
        ];
  const child = spawnProcess(executable, args, {
    cwd: target.cwd,
    env: hostEnvironment(target),
    stdio: ["pipe", "pipe", "pipe"],
    windowsHide: true,
  });
  const pending = new Map();
  let childExit;
  const exited = new Promise((resolve) =>
    child.once("exit", (code, exitSignal) => {
      childExit = {
        code,
        observedAt: new Date().toISOString(),
        signal: exitSignal,
      };
      resolve();
    }),
  );
  let cancellationRequestedAt;
  let id = 0;
  let stage = "spawn_native_host";
  let bytes = 0;
  const retain = (direction, message) => {
    const entry = sanitize({
      direction,
      message,
      recordedAt: new Date().toISOString(),
    });
    bytes += Buffer.byteLength(JSON.stringify(entry));
    if (bytes > 512 * 1024)
      throw new Error("Native trace exceeded its 512 KiB bound.");
    trace.push(entry);
  };
  const rejectAll = (error) => {
    for (const item of pending.values()) {
      clearTimeout(item.timer);
      item.reject(error);
    }
    pending.clear();
  };
  const lines = readline.createInterface({ input: child.stdout });
  lines.on("line", (line) => {
    try {
      const message = JSON.parse(line);
      retain("from_native_codex", message);
      const entry = pending.get(message.id);
      if (entry) {
        pending.delete(message.id);
        clearTimeout(entry.timer);
        if (message.error)
          entry.reject(
            Object.assign(new Error(message.error.message), {
              code: message.error.code,
              data: message.error.data,
            }),
          );
        else entry.resolve(message.result);
      } else if (message.id !== undefined && message.method) {
        child.stdin.write(
          JSON.stringify({
            error: {
              code: -32601,
              message:
                "Read-only validation does not handle this interactive request.",
            },
            id: message.id,
          }) + "\n",
        );
      }
    } catch (error) {
      rejectAll(error);
    }
  });
  child.on("error", rejectAll);
  child.stdin.on("error", rejectAll);
  child.on("exit", (code) =>
    rejectAll(new Error(`Native Codex exited (${code}).`)),
  );
  child.stderr.on("data", (data) => {
    try {
      retain("native_stderr", data.toString());
    } catch (error) {
      rejectAll(error);
    }
  });
  const send = (method, params) => {
    signal?.throwIfAborted();
    stage = method;
    const request = { id: ++id, method, params };
    retain("to_native_codex", request);
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        pending.delete(request.id);
        reject(new Error(`Native ${method} timed out.`));
      }, 25_000);
      pending.set(request.id, { reject, resolve, timer });
      child.stdin.write(JSON.stringify(request) + "\n");
    });
  };
  let result;
  let threadId;
  let failure;
  let recheck;
  let traceSaveError;
  const abort = () => {
    cancellationRequestedAt ??= new Date().toISOString();
    rejectAll(
      signal.reason ?? new DOMException("Native read cancelled", "AbortError"),
    );
    if (child.exitCode === null && child.signalCode === null) child.kill();
  };
  signal?.addEventListener("abort", abort, { once: true });
  if (signal?.aborted) abort();
  try {
    await send("initialize", {
      capabilities: { experimentalApi: true },
      clientInfo: { name: "chatcut_doctor_local_validation", version: "0.1.0" },
    });
    child.stdin.write(
      JSON.stringify({ method: "initialized", params: {} }) + "\n",
    );
    const started = await send("thread/start", {
      approvalPolicy: "never",
      cwd: target.cwd,
      ephemeral: true,
      sandbox: "read-only",
    });
    threadId = started.thread.id;
    if (discoverSkills) {
      const skills = await send("skills/list", {
        cwds: [target.cwd],
        forceReload: true,
      });
      await writeFile(
        output + ".skills.json",
        JSON.stringify(sanitize(skills), null, 2) + "\n",
        {
          flag: "wx",
          mode: 0o600,
        },
      );
    }
    const listed = await send("mcpServerStatus/list", {
      detail: "toolsAndAuthOnly",
      serverName: target.serverName,
      threadId,
    });
    await writeFile(
      output + ".status.json",
      JSON.stringify(sanitize(listed), null, 2) + "\n",
      {
        flag: "wx",
        mode: 0o600,
      },
    );
    result = await send("mcpServer/tool/call", {
      arguments: operation === "read_project" ? { projectId } : {},
      server: target.serverName,
      threadId,
      tool: operation,
    });
    recheck = {
      host: "codex",
      nativeCallId: `app-server-rpc-${id}`,
      nativeCallIdKind: "codex_app_server_rpc_request",
      observedAt: new Date().toISOString(),
      operation,
      schemaVersion: 1,
      serverName: target.serverName,
      sessionBoundary: "new_session",
      sessionId: threadId,
      source: "native_host_tool_result",
      targetFingerprint: fingerprint,
      ...(projectId ? { projectId } : {}),
      outcome: result?.isError ? "failed" : "success",
      result,
    };
  } catch (error) {
    failure = {
      ...errorDetails(error),
      stage,
      ...(error.data ? { data: error.data } : {}),
    };
    recheck = {
      host: "codex",
      nativeCallId: id ? `app-server-rpc-${id}` : null,
      nativeCallIdKind: "codex_app_server_rpc_request",
      observedAt: new Date().toISOString(),
      operation,
      schemaVersion: 1,
      serverName: target.serverName,
      sessionBoundary: "new_session",
      sessionId: threadId ?? null,
      source: "native_host_tool_result",
      targetFingerprint: fingerprint,
      ...(projectId ? { projectId } : {}),
      error: failure,
      outcome: "failed",
      result: null,
    };
  } finally {
    signal?.removeEventListener("abort", abort);
    child.stdin.end();
    if (child.exitCode === null) {
      let timer;
      await Promise.race([
        exited,
        new Promise((resolve) => {
          timer = setTimeout(resolve, 1000);
        }),
      ]);
      clearTimeout(timer);
      if (child.exitCode === null && child.signalCode === null) {
        child.kill();
        await Promise.race([
          exited,
          new Promise((resolve) => {
            timer = setTimeout(resolve, 1000);
          }),
        ]);
        clearTimeout(timer);
      }
      if (child.exitCode === null && child.signalCode === null) {
        child.kill("SIGKILL");
        await Promise.race([
          exited,
          new Promise((resolve) => {
            timer = setTimeout(resolve, 1000);
          }),
        ]);
        clearTimeout(timer);
      }
    }
    if (cancellationRequestedAt)
      recheck.cancellation = {
        childExit: childExit ?? null,
        childExitObserved: Boolean(childExit),
        requestedAt: cancellationRequestedAt,
        scope: "owned_native_host_child; descendants_not_attested",
      };
    lines.close();
    rejectAll(new Error("Validation finished."));
    // Native descendants can retain inherited pipes after the host exits.
    child.stdin.destroy();
    child.stdout.destroy();
    child.stderr.destroy();
    child.unref();
    try {
      await writeFile(
        output + ".trace.json",
        JSON.stringify(
          {
            cancellationRequestedAt: cancellationRequestedAt ?? null,
            childExit: childExit ?? null,
            failure: failure ?? null,
            modelTurns: 0,
            nativeToolResult: result ?? null,
            targetFingerprint: fingerprint,
            threadId,
            trace,
          },
          null,
          2,
        ) + "\n",
        { flag: "wx", mode: 0o600 },
      );
    } catch (error) {
      traceSaveError = { ...errorDetails(error), stage: "save_native_trace" };
    }
  }
  if (traceSaveError) {
    recheck.evidenceGaps = [traceSaveError];
    if (recheck.outcome === "success") {
      recheck.outcome = "failed";
      recheck.error = traceSaveError;
    }
  }
  try {
    await writeFile(output, JSON.stringify(sanitize(recheck), null, 2) + "\n", {
      flag: "wx",
      mode: 0o600,
    });
  } catch (error) {
    if (recheck.error)
      throw new AggregateError(
        [recheck.error, error],
        "Native read failed and its result file could not be saved.",
        { cause: recheck.error },
      );
    throw error;
  }
  return recheck;
}

export async function runNativeReadCli(args = process.argv.slice(2)) {
  const { values } = parseArgs({
    args,
    options: {
      context: { type: "string" },
      "discover-skills": { type: "boolean" },
      executable: { type: "string" },
      operation: { type: "string" },
      output: { type: "string" },
      "project-id": { type: "string" },
    },
  });
  try {
    if (!values.output?.endsWith(".doctor-recheck.json"))
      throw new Error("Use a dedicated .doctor-recheck.json output.");
    const result = await codexNativeRead({
      discoverSkills: values["discover-skills"],
      executable: values.executable,
      operation: values.operation,
      output: values.output,
      projectId: values["project-id"],
      target: await readTarget(values.context),
    });
    process.stdout.write(
      JSON.stringify({
        modelTurns: 0,
        operation: result.operation,
        outcome: result.outcome,
        sessionId: result.sessionId,
      }) + "\n",
    );
    if (result.outcome !== "success") process.exitCode = 1;
  } catch (error) {
    console.error(
      JSON.stringify({
        error: sanitize({ code: error.code, message: error.message }),
      }),
    );
    process.exitCode = 1;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href)
  await runNativeReadCli();
