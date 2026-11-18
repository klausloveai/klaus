import { lstat, readFile, realpath, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { caseStatus, loadCase, readInput, sanitize, sha256 } from "./cases.mjs";

const GUIDES = ["recovery-paths", "https-inspection", "authorized-no-tools"];
const LIMIT = 256 * 1024;
export async function createCaseHandoff(
  caseInfo,
  { evidenceGaps = [], guidanceDir, originalTask, scope } = {},
) {
  guidanceDir ??= await defaultGuidanceDir();
  const evidence = await readCaseEvidence(caseInfo, { guidanceDir });
  const state = await caseStatus(caseInfo);
  const instruction =
    "Investigate this ChatCut problem using the original evidence and relevant guidance. Use supported actions within the user's authorization, verify the original path, and state remaining evidence gaps. Never replay edits or generation to test connectivity.";
  const handoff = sanitize({
    caseId: state.caseId,
    createdAt:
      state.observations.at(-1)?.recordedAt ?? caseInfo.manifest.createdAt,
    evidence,
    evidenceGaps: [
      ...evidenceGaps,
      "private_host_logs_excluded",
      "snapshot_does_not_prove_original_conversation_recovered",
    ],
    guidance: await Promise.all(
      evidence.entries
        .filter((entry) => entry.kind === "guidance")
        .map(async (entry) => ({
          ref: entry.ref,
          value: await boundedFile(
            path.join(guidanceDir, `${entry.ref.slice("guidance:".length)}.md`),
            guidanceDir,
          ),
        })),
    ),
    instruction,
    observations: state.observations
      .filter((entry) => entry.kind !== "detailed_collection")
      .slice(-20)
      .map((entry) => ({
        evidenceRef: `observation:${entry.observationId}`,
        kind: entry.kind,
        observationId: entry.observationId,
        operation: entry.operation,
        outcome: entry.outcome,
        recordedAt: entry.recordedAt,
        repairPerformed: entry.repairPerformed,
      })),
    original: caseInfo.original,
    originalSha256: state.originalSha256,
    originalTask,
    schemaVersion: 1,
    scope,
    source: "chatcut_product_doctor_handoff",
    status: state.status,
    target: state.target,
    targetFingerprint: state.targetFingerprint,
  });
  const bytes = JSON.stringify(handoff, null, 2) + "\n";
  if (Buffer.byteLength(bytes) > LIMIT)
    throw new Error(
      "Handoff exceeds its bounded size; original case remains available.",
    );
  const handoffPath = path.join(
    caseInfo.dir,
    `${sha256(bytes)}.doctor-handoff.json`,
  );
  try {
    await writeFile(handoffPath, bytes, { flag: "wx", mode: 0o600 });
  } catch (error) {
    if (error.code !== "EEXIST") throw error;
  }
  return {
    caseId: state.caseId,
    handoffPath,
    instruction: `Please investigate the ChatCut failure in the product-generated handoff at ${JSON.stringify(handoffPath)} (SHA-256 ${sha256(bytes)}). Read that file if your host has local file access, or use the attached copy. ${instruction}`,
    originalSha256: state.originalSha256,
    sha256: sha256(bytes),
  };
}

export async function readCaseEvidence(
  caseInfo,
  { evidenceRef, guidanceDir } = {},
) {
  guidanceDir ??= await defaultGuidanceDir();
  const state = await caseStatus(caseInfo);
  const entries = [];
  const gaps = [];
  let selected;
  const add = (ref, kind, value) => {
    const safe = sanitize(value);
    const bytes =
      typeof safe === "string" ? safe : JSON.stringify(safe, null, 2) + "\n";
    entries.push({
      bytes: Buffer.byteLength(bytes),
      kind,
      ref,
      sha256: sha256(bytes),
    });
    if (evidenceRef === ref) {
      if (Buffer.byteLength(bytes) > LIMIT)
        throw new Error(
          "Selected evidence exceeds the response budget; original file retained.",
        );
      selected = { ref, value: safe };
    }
  };
  add("original", "original", caseInfo.original);
  entries[0].sha256 = state.originalSha256;
  entries[0].bytes = (
    await lstat(path.join(caseInfo.dir, "original.json"))
  ).size;
  const observations = state.observations.filter(
    (entry) => entry.kind !== "detailed_collection",
  );
  for (const entry of observations.slice(-40)) {
    add(`observation:${entry.observationId}`, entry.kind, entry);
    if (entry.resultArtifact && entry.resultSha256) {
      const ref = `artifact:${entry.observationId}`;
      const artifact = await lstat(entry.resultArtifact).catch(() => undefined);
      if (!artifact?.isFile())
        gaps.push(`artifact_unavailable:${entry.observationId}`);
      entries.push({
        bytes: artifact?.isFile() ? artifact.size : 0,
        kind: "native_result",
        ref,
        sha256: entry.resultSha256,
      });
      if (evidenceRef === ref) {
        const bytes = await boundedFile(
          entry.resultArtifact,
          caseInfo.dir,
          512 * 1024,
        );
        if (sha256(bytes) !== entry.resultSha256)
          throw new Error("Native evidence changed.");
        selected = { ref, value: sanitize(JSON.parse(bytes)) };
      }
    }
  }
  if (guidanceDir) {
    for (const guide of GUIDES) {
      try {
        add(
          `guidance:${guide}`,
          "guidance",
          await boundedFile(path.join(guidanceDir, `${guide}.md`), guidanceDir),
        );
      } catch (error) {
        gaps.push(`guidance_unavailable:${guide}`);
        if (evidenceRef === `guidance:${guide}`) throw error;
      }
    }
  }
  if (evidenceRef && !selected)
    throw new Error("Unknown evidence reference; use the returned directory.");
  return {
    caseId: state.caseId,
    entries,
    originalSha256: state.originalSha256,
    targetFingerprint: state.targetFingerprint,
    ...(selected ? { selected } : {}),
    evidenceGaps: [
      ...state.evidenceGaps,
      ...gaps,
      ...(observations.length > 40 ? ["older_observations_omitted"] : []),
    ],
  };
}

export async function readProductHandoff(
  file,
  { evidenceRef, guidanceDir } = {},
) {
  const input = await readInput(file, ".doctor-handoff.json", LIMIT);
  const bytes = await readFile(file, "utf8");
  if (path.basename(file) !== `${sha256(bytes)}.doctor-handoff.json`)
    throw new Error("Handoff hash does not match its product reference.");
  if (
    input.schemaVersion !== 1 ||
    input.source !== "chatcut_product_doctor_handoff"
  )
    throw new Error("Use a product-generated Doctor handoff.");
  const info = await loadCase(path.dirname(file));
  if (
    input.caseId !== info.manifest.caseId ||
    input.originalSha256 !== info.manifest.originalSha256 ||
    input.targetFingerprint !== info.manifest.targetFingerprint
  )
    throw new Error("Handoff does not match the immutable case.");
  return evidenceRef
    ? readCaseEvidence(info, { evidenceRef, guidanceDir })
    : input;
}

async function boundedFile(file, directory, limit = LIMIT) {
  const info = await lstat(file);
  const parent = await realpath(directory);
  const resolved = await realpath(file);
  if (
    !info.isFile() ||
    info.size > limit ||
    !resolved.startsWith(parent + path.sep)
  )
    throw new Error("Selected evidence is unavailable or outside this case.");
  return readFile(file, "utf8");
}

async function defaultGuidanceDir() {
  const directory = path.dirname(fileURLToPath(import.meta.url));
  for (const candidate of [
    path.resolve(directory, "../../../../references"),
    path.resolve(
      directory,
      "../../../../packages/skills/content/doctor/references",
    ),
  ]) {
    try {
      if ((await lstat(candidate)).isDirectory()) return candidate;
    } catch {
      /* A source-only CLI may not include guidance. */
    }
  }
}
