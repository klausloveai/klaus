import { createHash, randomUUID } from "node:crypto";
import {
  link,
  lstat,
  mkdir,
  readdir,
  readFile,
  realpath,
  unlink,
  writeFile,
} from "node:fs/promises";
import path from "node:path";

import {
  canonicalPath,
  createCase,
  loadCase,
  normalizeTarget,
  readInput,
  sha256,
} from "./cases.mjs";
import { createCaseHandoff } from "./evidence.mjs";

const ID = /^[A-Za-z0-9_-]{1,128}$/;

export async function createSourceHandoff({
  projectId,
  sourceEvent,
  userData,
}) {
  if (
    !userData ||
    typeof sourceEvent !== "string" ||
    typeof projectId !== "string" ||
    !ID.test(sourceEvent) ||
    !ID.test(projectId)
  )
    throw new Error(
      "Select an explicit userData, source event and canonical project ID.",
    );
  userData = await realpath(canonicalPath(userData));
  const authPath = path.join(userData, "auth-token.json");
  const identity = await readIdentity(authPath);
  const origin = new URL(identity.backendOrigin);
  if (origin.href !== `${origin.origin}/`)
    throw new Error("The selected profile backend is not an origin.");
  const endpoint = new URL("relay/a", origin).href;
  const sourceDirectory = path.join(
    userData,
    "logs",
    "mcp-failures",
    sha256(endpoint).slice(0, 20),
  );
  if (sourceEvent === "list") {
    const entries = [];
    const files = await readdir(sourceDirectory).catch((error) => {
      if (error.code !== "ENOENT") throw error;
      return [];
    });
    if (files.length > 1024)
      throw new Error(
        "The selected source directory exceeds its bounded index budget.",
      );
    for (const file of files
      .filter((name) => /^[A-Za-z0-9_-]+\.json$/.test(name))
      .slice(0, 256)) {
      try {
        const location = path.join(sourceDirectory, file);
        await within(location, userData);
        const stored = await readInput(location, ".json", 264 * 1024);
        const event = stored.event;
        if (
          stored.destination !== endpoint ||
          event?.userId !== identity.userId ||
          event?.projectId !== projectId ||
          event?.eventName !== "desktop.mcp.failure" ||
          !["ipc", "stdio"].includes(event.source) ||
          stored.eventId !== event.eventId ||
          file !== `${event.eventId}.json`
        )
          continue;
        entries.push({
          code: event.error?.code,
          mcpClient: event.mcpClient,
          message:
            typeof event.error?.message === "string"
              ? event.error.message.slice(0, 1000)
              : null,
          messageTruncated:
            typeof event.error?.message === "string" &&
            event.error.message.length > 1000,
          occurredAt: event.occurredAt ?? null,
          operation: event.operation,
          sourceEventId: event.eventId,
          sourceTransport: event.source,
        });
      } catch {
        /* An unreadable record is not attributed to another event. */
      }
    }
    await assertIdentity(authPath, identity);
    return {
      entries: entries
        .sort((left, right) =>
          String(right.occurredAt).localeCompare(String(left.occurredAt)),
        )
        .slice(0, 32),
      evidenceGaps: entries.length
        ? ["original_external_host_session_unobserved"]
        : ["matching_original_source_event_unavailable"],
      scope: { ...identity, projectId },
      source: "current_profile_program_source_directory",
    };
  }
  const sourceFile = path.join(sourceDirectory, `${sourceEvent}.json`);
  await within(sourceFile, userData);
  const stored = await readInput(sourceFile, ".json", 264 * 1024);
  const event = stored.event;
  if (
    stored.schemaVersion !== 1 ||
    stored.destination !== endpoint ||
    stored.eventId !== sourceEvent ||
    event?.eventId !== sourceEvent ||
    event?.eventName !== "desktop.mcp.failure" ||
    event.userId !== identity.userId ||
    event.projectId !== projectId ||
    !["ipc", "stdio"].includes(event.source)
  )
    throw new Error(
      "This source is unavailable for the current profile, account and project.",
    );
  if (
    typeof event.error?.message !== "string" ||
    !event.error.message ||
    event.errorEvidenceOmitted
  )
    throw new Error(
      "Original source error is unavailable within the material budget; source retained.",
    );
  const target = normalizeTarget({
    backendOrigin: origin.origin,
    cwd: userData,
    host: "chatcut",
    hostHome: userData,
    management: "desktop",
    profile: identity.profileId,
    projectId,
    schemaVersion: 1,
    scope: "local",
    serverName: "chatcut_client",
    surface: "desktop",
    userData,
  });
  const eventSha256 = sha256(JSON.stringify(event, null, 2) + "\n");
  const original = {
    callId: event.localCallId,
    chatId: event.chatId,
    error: event.error,
    evidenceGaps: [
      "original_external_host_home_and_session_unobserved",
      "original_task_text_unavailable",
      "local_profile_identity_is_not_company_evidence_authorization",
    ],
    failureEventId: sourceEvent,
    mcpClient: event.mcpClient,
    occurredAt: event.occurredAt ?? null,
    operation: event.operation,
    originalConnection: {
      hostHome: null,
      hostSession: null,
      mcpClient: event.mcpClient,
      runtimeSource: event.runtimeSource,
      socket: event.error.path ?? null,
      transport: event.source,
    },
    projectId: event.projectId,
    requestedProjectId: event.requestedProjectId,
    requestId: event.requestId,
    runId: event.runId,
    runtimeSource: event.runtimeSource,
    schemaVersion: 1,
    serverName: target.serverName,
    sessionId: event.sessionId,
    source: "desktop_mcp_source_event",
    sourceEventSha256: eventSha256,
    sourceRecordedAt: event._time,
    sourceTransport: event.source,
    toolName: event.toolName,
    userId: event.userId,
  };
  const bytes = JSON.stringify(original, null, 2) + "\n";
  if (Buffer.byteLength(bytes) > 128 * 1024)
    throw new Error(
      "Original source exceeds the case material budget; no error was truncated.",
    );
  const root = path.join(userData, "doctor-cases");
  await mkdir(root, { mode: 0o700, recursive: true });
  await within(root, userData);
  const digest = createHash("sha256")
    .update(
      JSON.stringify([
        identity.userId,
        identity.profileId,
        identity.backendOrigin,
        projectId,
        sourceEvent,
      ]),
    )
    .digest();
  digest[6] = (digest[6] & 15) | 80;
  digest[8] = (digest[8] & 63) | 128;
  const hex = digest.toString("hex").slice(0, 32);
  const caseId = `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
  const sourceInputs = path.join(root, "source-inputs");
  await mkdir(sourceInputs, { mode: 0o700, recursive: true });
  await within(sourceInputs, userData);
  const originalFile = path.join(sourceInputs, `${caseId}.doctor-failure.json`);
  await immutableWrite(originalFile, bytes);
  await assertIdentity(authPath, identity);
  const casePath = path.join(root, caseId);
  const exists = await lstat(casePath).catch((error) => {
    if (error.code !== "ENOENT") throw error;
  });
  if (exists && (!exists.isDirectory() || exists.isSymbolicLink()))
    throw new Error(
      "The source case is not an owned regular directory; original event retained.",
    );
  const info = exists
    ? await loadCase(casePath, target)
    : await createCase({ caseId, originalFile, root, target });
  if (
    info.original.record?.failureEventId !== sourceEvent ||
    info.original.record?.sourceEventSha256 !== eventSha256 ||
    info.original.record?.userId !== identity.userId
  )
    throw new Error(
      "The existing source case does not match this immutable event; originals preserved.",
    );
  const context = path.join(info.dir, "source-selected.doctor-context.json");
  await immutableWrite(context, JSON.stringify(target, null, 2) + "\n");
  const index = path.join(root, "index");
  await mkdir(index, { mode: 0o700, recursive: true });
  await within(index, userData);
  const references = (await readdir(index)).filter((file) =>
    /^[a-f0-9-]{36}\.json$/.test(file),
  );
  if (references.length >= 256 && !references.includes(`${caseId}.json`))
    throw new Error(
      "The case index is full; original source and local case retained.",
    );
  const reference = {
    caseId,
    casePath: info.dir,
    chatId: event.chatId,
    context,
    originalSha256: info.manifest.originalSha256,
    projectId,
    targetFingerprint: info.manifest.targetFingerprint,
    updatedAt: info.manifest.createdAt,
    userId: identity.userId,
  };
  const indexFile = path.join(index, `${caseId}.json`);
  try {
    await immutableWrite(indexFile, JSON.stringify(reference, null, 2) + "\n");
  } catch (error) {
    const previous = await readInput(indexFile, ".json", 16 * 1024);
    if (
      previous.caseId !== caseId ||
      previous.casePath !== info.dir ||
      previous.userId !== identity.userId ||
      previous.originalSha256 !== info.manifest.originalSha256
    )
      throw error;
  }
  await assertIdentity(authPath, identity);
  const handoff = await createCaseHandoff(info, {
    evidenceGaps: original.evidenceGaps,
    scope: { userId: identity.userId },
  });
  await assertIdentity(authPath, identity);
  return {
    ...handoff,
    evidenceGaps: original.evidenceGaps,
    repairAvailable: false,
    repairPerformed: false,
    sourceEventId: sourceEvent,
    sourceEventSha256: eventSha256,
    sourceSelection:
      "exact_program_outbox_event; current_local_profile_account_and_project; no_upload_or_native_host_recovery",
    status: "unresolved",
  };
}

async function assertIdentity(file, expected) {
  if (JSON.stringify(await readIdentity(file)) !== JSON.stringify(expected))
    throw new Error(
      "The selected account or backend changed while preparing the material.",
    );
}

async function immutableWrite(file, bytes) {
  const temporary = path.join(path.dirname(file), `.${randomUUID()}.tmp`);
  try {
    await writeFile(temporary, bytes, { flag: "wx", mode: 0o600 });
    try {
      await link(temporary, file);
    } catch (error) {
      if (error.code !== "EEXIST") throw error;
      const existing = await lstat(file);
      if (
        !existing.isFile() ||
        existing.isSymbolicLink() ||
        existing.size > 264 * 1024 ||
        (await readFile(file, "utf8")) !== bytes
      )
        throw error;
    }
  } finally {
    await unlink(temporary).catch(() => {});
  }
}

async function readIdentity(file) {
  const auth = await readInput(file, "auth-token.json", 64 * 1024);
  if (
    typeof auth.userId !== "string" ||
    !ID.test(auth.userId) ||
    !["beta", "custom", "local", "production"].includes(auth.profileId) ||
    typeof auth.backendOrigin !== "string"
  )
    throw new Error(
      "The selected local profile has no available account identity.",
    );
  return {
    backendOrigin: auth.backendOrigin,
    profileId: auth.profileId,
    userId: auth.userId,
  };
}

async function within(file, root) {
  const info = await lstat(file);
  if (
    info.isSymbolicLink() ||
    !(await realpath(file)).startsWith((await realpath(root)) + path.sep)
  )
    throw new Error("Selected material escaped the chosen local profile.");
}
