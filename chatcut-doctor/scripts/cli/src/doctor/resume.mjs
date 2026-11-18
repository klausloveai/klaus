import { writeFile } from "node:fs/promises";
import path from "node:path";

import { canonicalPath, loadCase, readInput } from "./cases.mjs";

export async function resumeOptions(options) {
  if (!options.resumeFile) return options;
  let reference;
  try {
    reference = await readInput(
      options.resumeFile,
      ".doctor-resume.json",
      16 * 1024,
    );
  } catch (error) {
    if (error.code === "ENOENT") return options;
    throw error;
  }
  if (
    reference.schemaVersion !== 1 ||
    typeof reference.caseDir !== "string" ||
    !path.isAbsolute(reference.caseDir)
  )
    throw new Error("Invalid dedicated Doctor resume reference.");
  const saved = await loadCase(reference.caseDir);
  if (options.failureRecord || options.caseRoot)
    throw new Error(
      "An existing resume reference cannot replace its original capture or case root.",
    );
  if (
    reference.targetFingerprint !== saved.manifest.targetFingerprint ||
    reference.originalSha256 !== saved.manifest.originalSha256 ||
    (options.casePath &&
      canonicalPath(path.resolve(options.casePath)) !==
        canonicalPath(saved.dir))
  )
    throw new Error(
      "Resume reference does not match the original case; no operation executed.",
    );
  return { ...options, casePath: saved.dir };
}

export async function saveResumeReference(caseInfo, file) {
  if (!file) return;
  if (!file.endsWith(".doctor-resume.json"))
    throw new Error("Use a dedicated .doctor-resume.json reference.");
  const reference = {
    caseDir: caseInfo.dir,
    caseId: caseInfo.manifest.caseId,
    originalSha256: caseInfo.manifest.originalSha256,
    schemaVersion: 1,
    targetFingerprint: caseInfo.manifest.targetFingerprint,
  };
  try {
    await writeFile(file, JSON.stringify(reference, null, 2) + "\n", {
      flag: "wx",
      mode: 0o600,
    });
  } catch (error) {
    if (error.code !== "EEXIST")
      throw new Error(
        `Resume reference could not be saved. The original case remains at ${caseInfo.dir}.`,
        { cause: error },
      );
    const existing = await readInput(file, ".doctor-resume.json", 16 * 1024);
    if (
      existing.caseId !== reference.caseId ||
      existing.targetFingerprint !== reference.targetFingerprint ||
      existing.originalSha256 !== reference.originalSha256 ||
      canonicalPath(existing.caseDir) !== canonicalPath(reference.caseDir)
    )
      throw new Error(
        "Existing resume reference belongs to a different case and was preserved.",
      );
  }
}
