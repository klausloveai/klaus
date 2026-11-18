import { createHash } from "node:crypto";
import { open } from "node:fs/promises";
import { pathToFileURL } from "node:url";

export const DOCTOR_REPORT_LIMITS = Object.freeze({
  maxFragments: 128,
  maxInputBytes: 16 * 1024 * 1024,
  maxRecords: 20_000,
  maxReportBytes: 512 * 1024,
});

const HASH = /^[a-f0-9]{64}$/i;

export async function readDoctorReportFile(file, options = {}) {
  let limits;
  try {
    limits = limitsFor(options);
  } catch (error) {
    return invalid("invalid_limits", error.message);
  }
  let handle;
  let content;
  let failure;
  try {
    handle = await open(file, "r");
    const info = await handle.stat();
    if (!info.isFile())
      failure = invalid("invalid_file", "Input must be a regular file");
    else if (info.size > limits.maxInputBytes)
      failure = invalid(
        "input_byte_limit",
        "Input file exceeds the byte limit",
        {
          inputBytes: info.size,
          limit: limits.maxInputBytes,
        },
      );
    const chunks = [];
    let inputBytes = 0;
    while (!failure && inputBytes <= limits.maxInputBytes) {
      const chunk = Buffer.alloc(
        Math.min(64 * 1024, limits.maxInputBytes - inputBytes + 1),
      );
      const { bytesRead } = await handle.read(chunk);
      if (!bytesRead) break;
      inputBytes += bytesRead;
      if (inputBytes > limits.maxInputBytes) {
        failure = invalid(
          "input_byte_limit",
          "Input file exceeds the byte limit",
          {
            inputBytes,
            limit: limits.maxInputBytes,
          },
        );
        break;
      }
      chunks.push(chunk.subarray(0, bytesRead));
    }
    if (!failure) content = Buffer.concat(chunks, inputBytes);
  } catch (error) {
    failure = invalid("input_read_failed", error.message, {
      errorCode: error.code ?? null,
    });
  } finally {
    try {
      await handle?.close();
    } catch (error) {
      const closeFailure = invalid("input_close_failed", error.message, {
        errorCode: error.code ?? null,
      });
      if (failure) failure.issues.push(...closeFailure.issues);
      else failure = closeFailure;
    }
  }
  if (failure) return failure;
  return reassembleDoctorReport(content, options);
}

export function reassembleDoctorReport(input, options = {}) {
  let limits;
  try {
    limits = limitsFor(options);
  } catch (error) {
    return invalid("invalid_limits", error.message);
  }
  const parsed = parseRows(input, limits);
  if (parsed.status) return parsed;
  const { inputBytes, rows } = parsed;
  const issues = [];
  const fragments = [];
  const groups = new Map();
  const sourceCounts = {};
  let ignoredRecords = 0;
  for (const [index, row] of rows.entries()) {
    if (!object(row)) {
      issues.push({
        code: "invalid_row",
        message: "Each event must be an object",
        row: index + 1,
      });
      continue;
    }
    const extracted = payloadsFor(row, index + 1);
    issues.push(...extracted.issues);
    if (!extracted.payloads.length) ignoredRecords++;
    for (const { path, value } of extracted.payloads) {
      sourceCounts[path] = (sourceCounts[path] ?? 0) + 1;
      const errors = fragmentIssues(value, limits);
      if (errors.length) {
        issues.push({
          code: "invalid_fragment",
          message: errors.join("; "),
          path,
          row: index + 1,
        });
        continue;
      }
      const fragment = {
        ...value,
        reportSha256: value.reportSha256.toLowerCase(),
      };
      const key = JSON.stringify([
        fragment.diagnosticId,
        fragment.reportSha256,
      ]);
      const group = groups.get(key) ?? {
        diagnosticId: fragment.diagnosticId,
        fragmentPayloads: 0,
        reportSha256: fragment.reportSha256,
      };
      group.fragmentPayloads++;
      groups.set(key, group);
      fragments.push({ ...fragment, path, row: index + 1 });
    }
  }
  const result = {
    availableReports: [...groups.values()],
    diagnosticId: options.diagnosticId ?? null,
    ignoredRecords,
    inputBytes,
    issues,
    recordCount: rows.length,
    reportSha256:
      typeof options.reportSha256 === "string"
        ? options.reportSha256.toLowerCase()
        : null,
    sourceCounts,
    status: "invalid",
  };
  if (
    typeof options.diagnosticId !== "string" ||
    !options.diagnosticId.trim() ||
    typeof options.reportSha256 !== "string" ||
    !HASH.test(options.reportSha256)
  ) {
    issues.push({
      code: "selector_required",
      message:
        "Select both diagnosticId and reportSha256; reports are never selected implicitly",
    });
    return result;
  }
  if (issues.length) return result;
  const selected = fragments.filter(
    (fragment) =>
      fragment.diagnosticId === options.diagnosticId &&
      fragment.reportSha256 === options.reportSha256.toLowerCase(),
  );
  const count = selected[0]?.fragmentCount ?? null;
  result.matchedRecords = new Set(
    selected.map((fragment) => fragment.row),
  ).size;
  result.matchedPayloads = selected.length;
  result.expectedFragments = count;
  result.duplicateFragments = 0;
  const chunks = new Map();
  let reportBytes = 0;
  for (const fragment of selected) {
    if (fragment.fragmentCount !== count) {
      issues.push({
        code: "inconsistent_fragment_count",
        message: "Selected report has conflicting fragmentCount values",
        row: fragment.row,
      });
      continue;
    }
    if (chunks.has(fragment.fragmentIndex)) {
      if (chunks.get(fragment.fragmentIndex) !== fragment.fragment) {
        issues.push({
          code: "conflicting_fragment",
          fragmentIndex: fragment.fragmentIndex,
          message:
            "Selected report has different content for the same fragmentIndex",
          row: fragment.row,
        });
      } else result.duplicateFragments++;
      continue;
    }
    chunks.set(fragment.fragmentIndex, fragment.fragment);
    reportBytes += Buffer.byteLength(fragment.fragment);
    if (reportBytes > limits.maxReportBytes) {
      issues.push({
        code: "report_byte_limit",
        limit: limits.maxReportBytes,
        message: "Reassembled report exceeds the byte limit",
      });
      break;
    }
  }
  result.uniqueFragments = chunks.size;
  result.reportBytes = reportBytes;
  result.missingFragmentIndexes =
    count === null
      ? []
      : Array.from({ length: count }, (_, index) => index).filter(
          (i) => !chunks.has(i),
        );
  if (issues.length) return result;
  if (!selected.length || result.missingFragmentIndexes.length) {
    result.status = "incomplete";
    issues.push({
      code: selected.length ? "missing_fragments" : "report_not_found",
      message: selected.length
        ? "Selected report is missing fragments"
        : "No selected report found",
    });
    return result;
  }
  const reportJson = Array.from({ length: count }, (_, index) =>
    chunks.get(index),
  ).join("");
  const verifiedSha256 = createHash("sha256")
    .update(reportJson, "utf8")
    .digest("hex");
  if (verifiedSha256 !== result.reportSha256) {
    issues.push({
      code: "hash_mismatch",
      message: "Reassembled content does not match reportSha256",
    });
    return result;
  }
  let report;
  try {
    report = JSON.parse(reportJson);
  } catch (error) {
    issues.push({ code: "invalid_report_json", message: error.message });
    return result;
  }
  if (!object(report) || report.diagnosticId !== options.diagnosticId) {
    issues.push({
      code: "report_identity_mismatch",
      message: "Report must be an object with the selected diagnosticId",
    });
    return result;
  }
  return { ...result, report, reportJson, status: "complete", verifiedSha256 };
}

function fragmentIssues(fragment, limits) {
  const issues = [];
  if (!object(fragment)) return ["Fragment payload must be an object"];
  if (
    typeof fragment.diagnosticId !== "string" ||
    !fragment.diagnosticId.trim()
  )
    issues.push("diagnosticId must be a nonempty string");
  if (
    typeof fragment.reportSha256 !== "string" ||
    !HASH.test(fragment.reportSha256)
  )
    issues.push("reportSha256 must be a SHA-256 hex digest");
  if (
    !Number.isSafeInteger(fragment.fragmentCount) ||
    fragment.fragmentCount < 1 ||
    fragment.fragmentCount > limits.maxFragments
  )
    issues.push(
      "fragmentCount exceeds the fragment limit or is not a positive integer",
    );
  if (
    !Number.isSafeInteger(fragment.fragmentIndex) ||
    fragment.fragmentIndex < 0 ||
    fragment.fragmentIndex >= fragment.fragmentCount
  )
    issues.push("fragmentIndex must be an integer within fragmentCount");
  if (
    typeof fragment.fragment !== "string" ||
    !fragment.fragment.isWellFormed()
  )
    issues.push("fragment must be a well-formed Unicode string");
  else if (Buffer.byteLength(fragment.fragment) > limits.maxReportBytes)
    issues.push("fragment exceeds the report byte limit");
  return issues;
}

function invalid(code, message, details = {}) {
  return {
    issues: [{ code, message, ...details }],
    status: "invalid",
  };
}

function limitsFor(options) {
  const limits = { ...DOCTOR_REPORT_LIMITS, ...options.limits };
  for (const [name, value] of Object.entries(limits)) {
    if (
      !Object.hasOwn(DOCTOR_REPORT_LIMITS, name) ||
      !Number.isSafeInteger(value) ||
      value < 1 ||
      value > DOCTOR_REPORT_LIMITS[name]
    ) {
      throw new Error(
        `${name} must be a positive integer no greater than its default limit`,
      );
    }
  }
  return limits;
}

async function main(args) {
  const [file, diagnosticId, reportSha256, ...rest] = args;
  if (!file || !diagnosticId || !reportSha256 || rest.length) {
    process.stderr.write(
      "Usage: node doctor-reports.mjs <events.json|events.ndjson> <diagnosticId> <reportSha256>\n",
    );
    process.exitCode = 2;
    return;
  }
  const result = await readDoctorReportFile(file, {
    diagnosticId,
    reportSha256,
  });
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  process.exitCode =
    result.status === "complete" ? 0 : result.status === "incomplete" ? 3 : 2;
}

function object(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function parseRows(input, limits) {
  let rows;
  let inputBytes;
  if (Array.isArray(input)) {
    if (input.length > limits.maxRecords)
      return invalid("record_limit", "Input exceeds the record limit", {
        limit: limits.maxRecords,
        recordCount: input.length,
      });
    inputBytes = 2;
    try {
      for (const [index, row] of input.entries()) {
        inputBytes +=
          Buffer.byteLength(JSON.stringify(row) ?? "null") + (index ? 1 : 0);
        if (inputBytes > limits.maxInputBytes) break;
      }
    } catch (error) {
      return invalid("invalid_input", error.message);
    }
    rows = input;
  } else {
    if (typeof input !== "string" && !(input instanceof Uint8Array))
      return invalid(
        "invalid_input",
        "Input must be an array, JSON array text or NDJSON",
      );
    inputBytes =
      typeof input === "string" ? Buffer.byteLength(input) : input.byteLength;
    if (inputBytes > limits.maxInputBytes)
      return invalid("input_byte_limit", "Input exceeds the byte limit", {
        inputBytes,
        limit: limits.maxInputBytes,
      });
    let text;
    try {
      text =
        typeof input === "string"
          ? input
          : new TextDecoder("utf-8", { fatal: true }).decode(input);
    } catch (error) {
      return invalid("invalid_utf8", error.message);
    }
    text = text.replace(/^\uFEFF/, "").trim();
    try {
      if (text.startsWith("[")) {
        rows = JSON.parse(text);
      } else {
        rows = [];
        for (const [index, line] of text.split(/\r?\n/).entries()) {
          if (!line.trim()) continue;
          if (rows.length >= limits.maxRecords)
            return invalid("record_limit", "Input exceeds the record limit", {
              limit: limits.maxRecords,
              line: index + 1,
            });
          try {
            rows.push(JSON.parse(line));
          } catch (error) {
            return invalid("invalid_json", error.message, { line: index + 1 });
          }
        }
      }
    } catch (error) {
      return invalid("invalid_json", error.message);
    }
  }
  if (inputBytes > limits.maxInputBytes)
    return invalid("input_byte_limit", "Input exceeds the byte limit", {
      inputBytes,
      limit: limits.maxInputBytes,
    });
  if (rows.length > limits.maxRecords)
    return invalid("record_limit", "Input exceeds the record limit", {
      limit: limits.maxRecords,
      recordCount: rows.length,
    });
  return { inputBytes, rows };
}

function payloadsFor(row, rowIndex) {
  const payloads = [];
  const issues = [];
  const add = (path, value) => {
    if (value !== undefined) payloads.push({ path, value });
  };
  add("attributes.mcpDoctor", row.attributes?.mcpDoctor);
  add("properties.attributes.mcpDoctor", row.properties?.attributes?.mcpDoctor);
  add("attributes.mcpDoctor (projected)", row["attributes.mcpDoctor"]);
  add(
    "properties.attributes.mcpDoctor (projected)",
    row["properties.attributes.mcpDoctor"],
  );
  for (const [path, value] of [
    ["attributesJson", row.attributesJson],
    ["properties.attributesJson", row.properties?.attributesJson],
  ]) {
    if (value === undefined || value === null) continue;
    try {
      const attributes = typeof value === "string" ? JSON.parse(value) : value;
      if (!object(attributes))
        throw new Error(`${path} must contain a JSON object`);
      add(`${path}.mcpDoctor`, attributes.mcpDoctor);
    } catch (error) {
      issues.push({
        code: "invalid_attributes_json",
        message: error.message,
        path,
        row: rowIndex,
      });
    }
  }
  return { issues, payloads };
}

if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(process.argv[1]).href
) {
  main(process.argv.slice(2)).catch((error) => {
    process.stderr.write(`${error.stack ?? error.message}\n`);
    process.exitCode = 2;
  });
}
