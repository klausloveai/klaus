import { createHash, randomUUID } from "node:crypto";
import { constants } from "node:fs";
import {
  lstat,
  mkdir,
  open,
  opendir,
  readdir,
  readFile,
  realpath,
  unlink,
  writeFile,
} from "node:fs/promises";
import { hostname } from "node:os";
import path from "node:path";

import { errorDetails, redact, serverUrl } from "./hosted/mcp-doctor.mjs";
import { doctorMessage } from "./messages.mjs";

export const sha256 = (value) =>
  createHash("sha256").update(value).digest("hex");
const json = (value) => JSON.stringify(value, null, 2) + "\n";
const object = (value) =>
  value && typeof value === "object" && !Array.isArray(value);

export function canonicalPath(value, platform = process.platform) {
  if (typeof value !== "string" || !value || /[\r\n\0]/u.test(value))
    throw new Error("An explicit absolute target path is required.");
  const paths = platform === "win32" ? path.win32 : path.posix;
  if (!paths.isAbsolute(value))
    throw new Error("Target paths must be absolute.");
  const result = paths.normalize(value);
  return platform === "win32" ? result.toLowerCase() : result;
}

export function normalizeTarget(input) {
  if (
    !object(input) ||
    input.schemaVersion !== 1 ||
    !["desktop", "hosted"].includes(input.surface) ||
    !["chatcut", "claude-code", "codex"].includes(input.host) ||
    !["local", "project", "user"].includes(input.scope) ||
    !["desktop", "manual", "plugin"].includes(input.management)
  )
    throw new Error("Unsupported Doctor target context.");
  const platform = input.platform ?? process.platform;
  if (!["darwin", "linux", "win32"].includes(platform))
    throw new Error("Unsupported target platform.");
  const target = {
    cwd: canonicalPath(input.cwd, platform),
    enabled: input.enabled ?? null,
    host: input.host,
    hostHome: canonicalPath(input.hostHome, platform),
    management: input.management,
    platform,
    schemaVersion: 1,
    scope: input.scope,
    serverName: input.serverName,
    surface: input.surface,
  };
  if (target.enabled !== null && typeof target.enabled !== "boolean")
    throw new Error("enabled must be boolean or null.");
  if (target.host === "chatcut") {
    if (
      target.surface !== "desktop" ||
      target.management !== "desktop" ||
      target.scope !== "local" ||
      target.serverName !== "chatcut_client"
    )
      throw new Error(
        "ChatCut client diagnosis must remain bound to its local Desktop instance.",
      );
    if (!["beta", "custom", "local", "production"].includes(input.profile))
      throw new Error("Select the actual Desktop profile.");
    target.profile = input.profile;
    target.userData = canonicalPath(input.userData, platform);
    if (target.hostHome !== target.userData)
      throw new Error("Client home must be its selected userData.");
    if (input.backendOrigin) {
      const origin = new URL(input.backendOrigin);
      if (origin.href !== `${origin.origin}/`)
        throw new Error(
          "Select a backend origin without credentials, path or query.",
        );
      target.backendOrigin = serverUrl(
        new URL("/api/external-mcp/mcp", origin).href,
      ).origin;
    }
    if (input.projectId !== undefined) {
      if (
        typeof input.projectId !== "string" ||
        !/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(input.projectId)
      )
        throw new Error("Select the actual complete projectId.");
      target.projectId = input.projectId;
    }
    return target;
  }
  if (target.surface === "hosted") {
    if (!["chatcut", "plugin:chatcut:chatcut"].includes(target.serverName))
      throw new Error("Select the actual hosted ChatCut service name.");
    target.endpoint = input.endpoint ? serverUrl(input.endpoint).href : null;
    target.cliPath = input.cliPath
      ? canonicalPath(input.cliPath, platform)
      : null;
    if (target.host === "codex" && target.scope !== "user")
      throw new Error(
        "Codex manual registration is scoped to the selected CODEX_HOME; use scope user.",
      );
    if (input.logLocations) {
      target.logLocations = {};
      for (const key of ["sqlite", "text", "app", "stderr"])
        if (input.logLocations[key])
          target.logLocations[key] = canonicalPath(
            input.logLocations[key],
            platform,
          );
    }
  } else {
    if (
      target.serverName !== "chatcut_desktop" ||
      target.management !== "desktop" ||
      target.scope !== "user"
    )
      throw new Error(
        "Desktop maintenance requires its owned chatcut_desktop user registration.",
      );
    if (!["beta", "custom", "local", "production"].includes(input.profile))
      throw new Error("Select the actual Desktop profile.");
    target.profile = input.profile;
    target.userData = canonicalPath(input.userData, platform);
    target.launcher = canonicalPath(input.launcher, platform);
    if (input.cliPath) target.cliPath = canonicalPath(input.cliPath, platform);
    if (input.projectId !== undefined) {
      if (
        typeof input.projectId !== "string" ||
        !/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(input.projectId)
      )
        throw new Error(
          "Desktop projectId must be the actual complete project identifier.",
        );
      target.projectId = input.projectId;
    }
    if (input.backendOrigin) {
      const origin = new URL(input.backendOrigin);
      if (origin.href !== `${origin.origin}/`)
        throw new Error(
          "Desktop backendOrigin must be an origin without credentials, path, query or fragment.",
        );
      target.backendOrigin = serverUrl(
        new URL("/api/external-mcp/mcp", origin).href,
      ).origin;
    }
    const paths = platform === "win32" ? path.win32 : path.posix;
    if (
      canonicalPath(paths.dirname(target.launcher), platform) !==
      target.userData
    )
      throw new Error(
        "Launcher must belong to the selected userData directory.",
      );
  }
  return target;
}

export async function readInput(file, suffix, limit = 128 * 1024) {
  if (!file.endsWith(suffix))
    throw new Error(
      `Use a dedicated ${suffix} input; configuration and credential files are not inputs.`,
    );
  const info = await lstat(file);
  if (!info.isFile() || info.size > limit)
    throw new Error(
      `Input must be a regular file no larger than ${limit} bytes; source retained unchanged.`,
    );
  return JSON.parse(await readFile(file, "utf8"));
}

export function sanitize(value) {
  return JSON.parse(
    JSON.stringify(value, (key, item) =>
      /^(?:authorization|proxy-authorization|cookie|set-cookie|access_token|refresh_token|id_token|client_secret|api_key|mcp-session-id)$/i.test(
        key,
      )
        ? "[REDACTED]"
        : typeof item === "string"
          ? redact(item)
          : item,
    ),
  );
}

export const targetFingerprint = (target) =>
  sha256(JSON.stringify(sortedKeys(normalizeTarget(target))));

export async function appendObservation(caseInfo, observation) {
  await loadCase(caseInfo.dir);
  const saved = sanitize({
    observationId: randomUUID(),
    recordedAt: new Date().toISOString(),
    schemaVersion: 1,
    ...observation,
    caseId: caseInfo.manifest.caseId,
    originalSha256: caseInfo.manifest.originalSha256,
    targetFingerprint: caseInfo.manifest.targetFingerprint,
  });
  const count = (await readdir(path.join(caseInfo.dir, "observations"))).filter(
    (name) => name.endsWith(".json"),
  ).length;
  if (count >= 1000)
    throw new Error(
      "Case observation limit reached; local originals remain available.",
    );
  const file = path.join(
    caseInfo.dir,
    "observations",
    `${String(count + 1).padStart(4, "0")}-${saved.observationId}.json`,
  );
  await writeFile(file, json(saved), { flag: "wx", mode: 0o600 });
  await loadCase(caseInfo.dir);
  return saved;
}

export async function caseStatus(caseInfo) {
  await loadCase(caseInfo.dir, caseInfo.manifest.target);
  const files = (await readdir(path.join(caseInfo.dir, "observations")))
    .filter((name) => name.endsWith(".json"))
    .sort();
  if (files.length > 1000)
    throw new Error(
      "Case observation limit exceeded; start a separately linked observation.",
    );
  const observations = [];
  for (const file of files) {
    const entry = await readInput(
      path.join(caseInfo.dir, "observations", file),
      ".json",
      4 * 1024 * 1024,
    );
    if (
      entry.caseId !== caseInfo.manifest.caseId ||
      entry.targetFingerprint !== caseInfo.manifest.targetFingerprint ||
      entry.originalSha256 !== caseInfo.manifest.originalSha256
    )
      throw new Error("Case observation identity mismatch.");
    observations.push(entry);
  }
  const latest = observations
    .filter(
      (entry) =>
        ![
          "automatic_capture",
          "company_evidence",
          "delivery",
          "detailed_collection",
          "diagnostic_action",
          "investigation_result",
          "result_delivery",
        ].includes(entry.kind),
    )
    .at(-1);
  const gap =
    latest?.kind === "native_recheck" && latest.outcome === "success"
      ? await recoveryEvidenceGap(caseInfo, latest)
      : null;
  const healthyClient =
    caseInfo.manifest.target.host === "chatcut" &&
    caseInfo.original.status === "unavailable" &&
    latest?.kind === "check" &&
    latest.outcome === "checked" &&
    latest.checks?.length > 0 &&
    latest.checks.every((entry) => ["not_run", "pass"].includes(entry.status));
  const clientAttention =
    caseInfo.manifest.target.host === "chatcut"
      ? observations
          .filter((entry) => entry.kind === "check")
          .at(-1)
          ?.checks?.find((entry) =>
            ["needs_user", "unknown"].includes(entry.status),
          )
      : null;
  const agentReadDoesNotVerifyRecovery =
    caseInfo.original.record?.source === "desktop_agent_source_event" &&
    latest?.kind === "native_recheck" &&
    latest.outcome === "success";
  const status = gap
    ? "unresolved"
    : clientAttention
      ? clientAttention.status === "needs_user"
        ? "needs_user"
        : "unresolved"
      : agentReadDoesNotVerifyRecovery
        ? "unresolved"
        : healthyClient
          ? "healthy"
          : latest?.kind === "native_recheck" && latest.outcome === "success"
            ? caseInfo.original.status === "unavailable" ||
              (caseInfo.manifest.target.host === "chatcut" &&
                caseInfo.original.record?.source === "desktop_mcp_source_event")
              ? "healthy"
              : "recovered"
            : latest?.needsUser
              ? "needs_user"
              : "unresolved";
  return {
    caseDir: caseInfo.dir,
    caseId: caseInfo.manifest.caseId,
    evidenceGaps: [
      ...(gap ? [gap] : []),
      ...(agentReadDoesNotVerifyRecovery
        ? [
            "basic_runtime_and_project_checks_do_not_verify_original_agent_recovery",
          ]
        : []),
    ],
    observations,
    originalEvidence: {
      callId: caseInfo.original.record?.callId ?? null,
      conversationId: caseInfo.original.record?.conversationId ?? null,
      occurredAt: caseInfo.original.record?.occurredAt ?? null,
      qualification:
        "supplied_original_metadata; unavailable_identifiers_remain_unknown",
      requestId: caseInfo.original.record?.requestId ?? null,
      sessionId: caseInfo.original.record?.sessionId ?? null,
      source: caseInfo.original.record?.source ?? "unavailable",
      status: caseInfo.original.status,
    },
    originalSha256: caseInfo.manifest.originalSha256,
    recoveryEvidence:
      status === "recovered"
        ? caseInfo.manifest.target.host === "chatcut"
          ? "selected_client_runtime_actual_read; inspect attached source"
          : "agent_supplied_native_tool_result; inspect attached source and session boundary"
        : "not_verified",
    repairPerformed: observations.some(
      (entry) => entry.kind === "repair" && entry.repairPerformed === true,
    )
      ? true
      : observations.some(
            (entry) =>
              entry.kind === "repair" && entry.repairPerformed !== false,
          )
        ? null
        : false,
    schemaVersion: 1,
    status,
    target: caseInfo.manifest.target,
    targetFingerprint: caseInfo.manifest.targetFingerprint,
    userResult: doctorMessage(
      {
        healthy: "resultHealthy",
        needs_user: "resultNeedsUser",
        recovered: "resultRecovered",
        unresolved: "resultUnresolved",
      }[status],
    ),
  };
}

export async function createCase({
  caseId: selectedCaseId,
  originalFile,
  root,
  target,
}) {
  if (
    selectedCaseId !== undefined &&
    !/^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(
      selectedCaseId,
    )
  )
    throw new Error("A selected case identity must be a UUID.");
  target = normalizeTarget(target);
  let original = {
    error: null,
    occurredAt: null,
    source: "unavailable",
    status: "unavailable",
  };
  if (originalFile) {
    const suffix = originalFile.endsWith(".mcp-failure.json")
      ? ".mcp-failure.json"
      : ".doctor-failure.json";
    const input = await readInput(originalFile, suffix);
    if (
      !object(input.error) ||
      typeof input.error.message !== "string" ||
      !input.error.message.trim()
    )
      throw new Error(
        "Original failure needs the actual exposed error.message.",
      );
    if (
      input.serverName !== undefined &&
      input.serverName !== null &&
      input.serverName !== target.serverName
    )
      throw new Error(
        "Original failure serverName contradicts the selected target; source retained unchanged and no case created.",
      );
    original = sanitize({ record: input, status: "recorded" });
  }
  const caseId = selectedCaseId ?? randomUUID();
  const dir = path.resolve(root, caseId);
  await mkdir(dir, { mode: 0o700, recursive: true });
  const originalBytes = json(original);
  await writeFile(path.join(dir, "original.json"), originalBytes, {
    flag: "wx",
    mode: 0o600,
  });
  const manifest = {
    caseId,
    createdAt: new Date().toISOString(),
    originalEvidenceSource: "supplied_original; not_inferred_from_later_checks",
    originalSha256: sha256(originalBytes),
    schemaVersion: 1,
    target,
    targetFingerprint: targetFingerprint(target),
  };
  await writeFile(path.join(dir, "case.json"), json(manifest), {
    flag: "wx",
    mode: 0o600,
  });
  await mkdir(path.join(dir, "observations"), { mode: 0o700 });
  return { dir, manifest, original };
}

export async function loadCase(dir, target) {
  dir = path.resolve(dir);
  const manifest = await readInput(
    path.join(dir, "case.json"),
    "case.json",
    32 * 1024,
  );
  if (manifest.schemaVersion !== 1 || !/^[a-f0-9-]{36}$/i.test(manifest.caseId))
    throw new Error("Unsupported Doctor case.");
  const expected = targetFingerprint(manifest.target);
  if (
    manifest.targetFingerprint !== expected ||
    (target && targetFingerprint(target) !== expected)
  )
    throw new Error(
      "Doctor target mismatch: host, configuration scope, endpoint or Desktop profile changed. No action executed.",
    );
  const originalFile = path.join(dir, "original.json");
  const originalInfo = await lstat(originalFile);
  if (!originalInfo.isFile() || originalInfo.size > 512 * 1024)
    throw new Error("Original evidence is not a bounded regular file.");
  const originalBytes = await readFile(originalFile);
  if (sha256(originalBytes) !== manifest.originalSha256)
    throw new Error(
      "Original evidence hash mismatch. Preserve the case; no action executed.",
    );
  return { dir, manifest, original: JSON.parse(originalBytes) };
}

export async function readTarget(file) {
  return normalizeTarget(await readInput(file, ".doctor-context.json"));
}

export async function withCaseLock(caseInfo, action, dependencies = {}) {
  const lock = await acquireCaseGeneration(caseInfo, dependencies);
  const { file, handle, owner } = lock;
  let identity;
  let result;
  let failed = false;
  let failure;
  try {
    identity = await handle.stat();
    await handle.writeFile(owner);
    result = await action();
  } catch (error) {
    failed = true;
    failure = error;
  }
  const cleanupErrors = [];
  try {
    await handle.close();
  } catch (error) {
    cleanupErrors.push(error);
  }
  try {
    if (
      !identity ||
      !(await sameCaseLock(file, { bytes: owner, identity })) ||
      (lock.root &&
        !(await sameCaseLock(
          path.join(caseInfo.dir, "operation.lock"),
          lock.root,
        )))
    )
      throw Object.assign(
        new Error(
          "Case lock ownership changed; the replacement lock was preserved.",
        ),
        { code: "CASE_LOCK_CHANGED" },
      );
    await (dependencies.writeFile ?? writeFile)(file + ".released", owner, {
      flag: "wx",
      mode: 0o600,
    });
  } catch (error) {
    cleanupErrors.push(error);
  }
  if (cleanupErrors.length)
    throw new AggregateError(
      [...(failed ? [failure] : []), ...cleanupErrors],
      `${doctorMessage("caseLockCleanupFailed")}\n${JSON.stringify({
        actionError: failed ? errorDetails(failure) : null,
        cleanupErrors: cleanupErrors.map((error) => errorDetails(error)),
      })}`,
      { cause: failed ? failure : cleanupErrors[0] },
    );
  if (failed) throw failure;
  return result;
}

export async function withTargetRepairLock(input, action) {
  const target = normalizeTarget(input);
  if (target.platform !== process.platform)
    throw new Error(
      "A different platform repair cannot be locked on this machine.",
    );
  const home = await realpath(target.hostHome);
  const lockRoot = path.join(target.hostHome, ".chatcut-doctor-locks");
  try {
    await mkdir(lockRoot, { mode: 0o700 });
  } catch (error) {
    if (error.code !== "EEXIST") throw error;
  }
  const rootInfo = await lstat(lockRoot);
  if (
    !rootInfo.isDirectory() ||
    rootInfo.isSymbolicLink() ||
    canonicalPath(await realpath(lockRoot)) !==
      canonicalPath(path.join(home, ".chatcut-doctor-locks"))
  )
    throw new Error(
      "Repair lock directory must be owned by the selected host home; no repair executed.",
    );
  const resource = {
    host: target.host,
    hostHome: canonicalPath(home),
    scope: target.scope,
    ...(target.scope === "user"
      ? {}
      : { cwd: canonicalPath(await realpath(target.cwd)) }),
  };
  const file = path.join(
    lockRoot,
    `repair-${sha256(JSON.stringify(resource))}.lock`,
  );
  const handle = await open(file, "wx", 0o600);
  const owner = json({
    createdAt: new Date().toISOString(),
    ownerId: randomUUID(),
    processId: process.pid,
    resource,
  });
  let result;
  let failure;
  try {
    await handle.writeFile(owner);
    result = await action();
  } catch (error) {
    failure = error;
  }
  try {
    const identity = await handle.stat();
    await handle.close();
    const current = await lstat(file);
    if (
      !current.isFile() ||
      current.isSymbolicLink() ||
      current.dev !== identity.dev ||
      current.ino !== identity.ino ||
      current.size !== Buffer.byteLength(owner) ||
      (await readFile(file, "utf8")) !== owner
    )
      throw Object.assign(
        new Error(
          "Repair lock ownership changed; the replacement lock was preserved.",
        ),
        { code: "TARGET_REPAIR_LOCK_CHANGED" },
      );
    await unlink(file);
  } catch (error) {
    await handle.close().catch(() => {});
    if (error.code !== "ENOENT")
      failure = failure
        ? new AggregateError(
            [failure, error],
            "Repair failed and its lock could not be released.",
            { cause: failure },
          )
        : error;
  }
  if (failure) throw failure;
  return result;
}

async function acquireCaseGeneration(caseInfo, dependencies) {
  const rootFile = path.join(caseInfo.dir, "operation.lock");
  try {
    await lstat(rootFile);
  } catch (error) {
    if (error.code !== "ENOENT")
      throw caseLockBlocked(caseInfo, "unverified", error);
    for (const prior of [
      rootFile + ".released",
      path.join(caseInfo.dir, "operation-locks"),
    ]) {
      try {
        await lstat(prior);
        throw caseLockBlocked(caseInfo, "unverified");
      } catch (priorError) {
        if (priorError.code === "CASE_LOCK_BLOCKED") throw priorError;
        if (priorError.code !== "ENOENT")
          throw caseLockBlocked(caseInfo, "unverified", priorError);
      }
    }
  }
  const openLock = dependencies.open ?? open;
  const ownerBytes = (generation, rootSha256) =>
    Buffer.from(
      json({
        caseId: caseInfo.manifest.caseId,
        generation,
        hostname: hostname(),
        ownerId: randomUUID(),
        processId: process.pid,
        protocol: "case-generations",
        ...(rootSha256 ? { rootSha256 } : {}),
        schemaVersion: 2,
      }),
    );
  try {
    const handle = await openLock(rootFile, "wx", 0o600);
    return { file: rootFile, handle, owner: ownerBytes(0) };
  } catch (error) {
    if (!["EACCES", "EEXIST", "EPERM"].includes(error.code)) throw error;
    if (error.code !== "EEXIST")
      throw caseLockBlocked(caseInfo, "unverified", error);
  }
  try {
    const root = await caseLockSnapshot(rootFile);
    caseGenerationOwner(caseInfo, root, 0);
    const rootSha256 = sha256(root.bytes);
    const directory = path.join(caseInfo.dir, "operation-locks");
    const generation = await latestCaseGeneration(directory, caseInfo.dir);
    const file = generation
      ? path.join(directory, String(generation).padStart(4, "0") + ".lock")
      : rootFile;
    const current = generation ? await caseLockSnapshot(file) : root;
    const owner = caseGenerationOwner(
      caseInfo,
      current,
      generation,
      rootSha256,
    );
    let release;
    try {
      release = await caseLockSnapshot(file + ".released");
      if (!release.bytes.equals(current.bytes))
        throw caseLockBlocked(caseInfo, "unverified");
    } catch (releaseError) {
      if (releaseError.code !== "ENOENT") throw releaseError;
    }
    // Completed owners need no live-machine check when a network changes its hostname.
    if (!release) {
      if (owner.hostname !== hostname())
        throw caseLockBlocked(caseInfo, "unverified");
      try {
        (dependencies.kill ?? process.kill)(owner.processId, 0);
        throw caseLockBlocked(caseInfo, "active");
      } catch (ownerError) {
        if (ownerError.code !== "ESRCH") throw ownerError;
      }
    }
    if (generation >= 1024) throw caseLockBlocked(caseInfo, "capacity");
    if (
      !(await sameCaseLock(rootFile, root)) ||
      !(await sameCaseLock(file, current)) ||
      (release && !(await sameCaseLock(file + ".released", release)))
    )
      throw caseLockBlocked(caseInfo, "changed");
    try {
      await mkdir(directory, { mode: 0o700 });
    } catch (directoryError) {
      if (directoryError.code !== "EEXIST") throw directoryError;
    }
    await checkCaseGenerationDirectory(directory, caseInfo.dir);
    const next = generation + 1;
    const nextFile = path.join(
      directory,
      String(next).padStart(4, "0") + ".lock",
    );
    // Immutable generations make exclusive creation the cross-process ownership transfer.
    const handle = await openLock(nextFile, "wx", 0o600);
    return {
      file: nextFile,
      handle,
      owner: ownerBytes(next, rootSha256),
      root,
    };
  } catch (error) {
    if (error.code === "CASE_LOCK_BLOCKED") throw error;
    throw caseLockBlocked(caseInfo, "unverified", error);
  }
}

function caseGenerationOwner(caseInfo, snapshot, generation, rootSha256) {
  const owner = JSON.parse(snapshot.bytes.toString("utf8"));
  const legacy = generation === 0 && owner.schemaVersion === 1;
  if (
    (!legacy &&
      (owner.schemaVersion !== 2 ||
        owner.protocol !== "case-generations" ||
        owner.generation !== generation ||
        (generation > 0 && owner.rootSha256 !== rootSha256))) ||
    typeof owner.hostname !== "string" ||
    !owner.hostname.trim() ||
    /[\r\n\0]/u.test(owner.hostname) ||
    owner.caseId !== caseInfo.manifest.caseId ||
    !Number.isSafeInteger(owner.processId) ||
    owner.processId <= 0 ||
    typeof owner.ownerId !== "string" ||
    !/^[a-f0-9]{8}-(?:[a-f0-9]{4}-){3}[a-f0-9]{12}$/i.test(owner.ownerId)
  )
    throw caseLockBlocked(caseInfo, "unverified");
  return owner;
}

function caseLockBlocked(caseInfo, reason, cause) {
  return Object.assign(new Error(doctorMessage("caseLockBlocked"), { cause }), {
    caseId: caseInfo.manifest.caseId,
    code: "CASE_LOCK_BLOCKED",
    reason,
  });
}

async function caseLockSnapshot(file) {
  const before = await lstat(file);
  if (!before.isFile() || before.isSymbolicLink() || before.size > 4096)
    throw new Error("Case lock is not a bounded regular file.");
  const handle = await open(
    file,
    process.platform === "win32"
      ? "r"
      : constants.O_RDONLY | constants.O_NOFOLLOW,
  );
  try {
    const identity = await handle.stat();
    const bytes = Buffer.alloc(4097);
    const { bytesRead } = await handle.read(bytes, 0, bytes.length, 0);
    const current = await lstat(file);
    if (
      identity.dev !== before.dev ||
      identity.ino !== before.ino ||
      current.dev !== identity.dev ||
      current.ino !== identity.ino ||
      current.size !== identity.size ||
      current.mtimeMs !== identity.mtimeMs ||
      current.ctimeMs !== identity.ctimeMs ||
      !identity.isFile() ||
      bytesRead > 4096 ||
      bytesRead !== identity.size
    )
      throw new Error("Case lock changed while being read.");
    return { bytes: bytes.subarray(0, bytesRead), identity };
  } finally {
    await handle.close();
  }
}

async function checkCaseGenerationDirectory(directory, caseDirectory) {
  const info = await lstat(directory);
  if (
    !info.isDirectory() ||
    info.isSymbolicLink() ||
    canonicalPath(await realpath(directory)) !==
      canonicalPath(path.join(await realpath(caseDirectory), "operation-locks"))
  )
    throw new Error(
      "Case generation directory changed; preserved without a new action.",
    );
}

function isWithin(root, file) {
  const relative = path.relative(root, file);
  return (
    relative !== "" &&
    relative !== ".." &&
    !relative.startsWith(`..${path.sep}`) &&
    !path.isAbsolute(relative)
  );
}

async function latestCaseGeneration(directory, caseDirectory) {
  try {
    await checkCaseGenerationDirectory(directory, caseDirectory);
  } catch (error) {
    if (error.code === "ENOENT") return 0;
    throw error;
  }
  const generations = new Set();
  const releases = new Set();
  let count = 0;
  for await (const entry of await opendir(directory)) {
    const match = entry.name.match(/^(\d{4})\.lock(\.released)?$/);
    if (
      ++count > 2048 ||
      !entry.isFile() ||
      !match ||
      Number(match[1]) < 1 ||
      Number(match[1]) > 1024
    )
      throw new Error(
        "Case generation files are unknown or exceed their limit; preserved without a new action.",
      );
    (match[2] ? releases : generations).add(Number(match[1]));
  }
  const latest = generations.size ? Math.max(...generations) : 0;
  if (
    latest !== generations.size ||
    [...releases].some((value) => !generations.has(value))
  )
    throw new Error(
      "Case generation sequence is incomplete; preserved without a new action.",
    );
  return latest;
}

async function recoveryEvidenceGap(caseInfo, observation) {
  const limit = 512 * 1024;
  let handle;
  let gap = null;
  try {
    const requiredRead =
      caseInfo.manifest.target.surface === "desktop"
        ? "read_project"
        : "list_projects";
    if (observation.operation !== requiredRead)
      throw new Error(
        `Recovery requires an actual ${requiredRead} result for this target.`,
      );
    const file = observation.resultArtifact;
    if (
      typeof file !== "string" ||
      !path.isAbsolute(file) ||
      !isWithin(path.resolve(caseInfo.dir), path.resolve(file))
    )
      throw new Error("Native recheck artifact must belong to this case.");
    const info = await lstat(file);
    if (!info.isFile() || info.isSymbolicLink() || info.size > limit)
      throw new Error(
        "Native recheck artifact must be a bounded regular file, without a symlink.",
      );
    if (!isWithin(await realpath(caseInfo.dir), await realpath(file)))
      throw new Error("Native recheck artifact resolves outside this case.");
    if (
      typeof observation.resultSha256 !== "string" ||
      !/^[a-f0-9]{64}$/i.test(observation.resultSha256)
    )
      throw new Error("Native recheck artifact SHA-256 is unavailable.");
    handle = await open(
      file,
      process.platform === "win32"
        ? "r"
        : constants.O_RDONLY | constants.O_NOFOLLOW,
    );
    const opened = await handle.stat();
    if (
      !opened.isFile() ||
      opened.dev !== info.dev ||
      opened.ino !== info.ino ||
      opened.size > limit
    )
      throw new Error("Native recheck artifact changed while being opened.");
    const chunks = [];
    let size = 0;
    while (size <= limit) {
      const chunk = Buffer.alloc(Math.min(64 * 1024, limit - size + 1));
      const { bytesRead } = await handle.read(chunk);
      if (!bytesRead) break;
      size += bytesRead;
      if (size > limit)
        throw new Error("Native recheck artifact exceeds its byte limit.");
      chunks.push(chunk.subarray(0, bytesRead));
    }
    if (
      sha256(Buffer.concat(chunks, size)) !==
      observation.resultSha256.toLowerCase()
    )
      throw new Error("Native recheck artifact hash mismatch.");
  } catch (error) {
    gap = {
      code: "native_recheck_evidence_invalid",
      message: error.message,
      observationId: observation.observationId,
      ...(error.code ? { errorCode: error.code } : {}),
    };
  } finally {
    try {
      await handle?.close();
    } catch (error) {
      gap ??= {
        code: "native_recheck_evidence_unreadable",
        message: error.message,
        observationId: observation.observationId,
        ...(error.code ? { errorCode: error.code } : {}),
      };
    }
  }
  return gap;
}

async function sameCaseLock(file, expected) {
  const current = await caseLockSnapshot(file);
  return (
    current.identity.dev === expected.identity.dev &&
    current.identity.ino === expected.identity.ino &&
    current.bytes.equals(expected.bytes)
  );
}

function sortedKeys(value) {
  if (Array.isArray(value)) return value.map(sortedKeys);
  if (!object(value)) return value;
  return Object.fromEntries(
    Object.keys(value)
      .sort()
      .map((key) => [key, sortedKeys(value[key])]),
  );
}
