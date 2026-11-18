import { createHash, randomUUID } from "node:crypto";
import {
  closeSync,
  fsyncSync,
  lstatSync,
  mkdirSync,
  openSync,
  readdirSync,
  readFileSync,
  realpathSync,
  renameSync,
  statSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import path from "node:path";

const hash = (value) => createHash("sha256").update(value).digest("hex");
const FILE_LIMIT = 256 * 1024;

export function createDoctorFileStorage(directory) {
  const info = lstatSync(directory);
  if (!info.isDirectory() || info.isSymbolicLink())
    throw new Error("Doctor telemetry needs an owned regular directory.");
  let cachedStamp;
  let cachedKeys = [];
  const fileFor = (key) => path.join(directory, `${hash(key)}.json`);
  const read = (file) => {
    const entry = lstatSync(file);
    if (!entry.isFile() || entry.isSymbolicLink() || entry.size > FILE_LIMIT)
      throw new Error(
        "Doctor telemetry storage entry is not a bounded regular file.",
      );
    const row = JSON.parse(readFileSync(file, "utf8"));
    if (
      typeof row.key !== "string" ||
      typeof row.value !== "string" ||
      fileFor(row.key) !== file
    )
      throw new Error("Doctor telemetry storage key mismatch.");
    return row;
  };
  const keys = () => {
    const stamp = statSync(directory, { bigint: true });
    const revision = `${stamp.mtimeNs}:${stamp.ctimeNs}`;
    if (revision !== cachedStamp) {
      const names = readdirSync(directory).filter((name) =>
        /^[a-f0-9]{64}\.json$/.test(name),
      );
      if (names.length > 1024)
        throw new Error("Doctor telemetry storage index exceeds its budget.");
      cachedKeys = names
        .flatMap((name) => {
          try {
            return [read(path.join(directory, name)).key];
          } catch (error) {
            if (error.code === "ENOENT") return [];
            throw error;
          }
        })
        .sort();
      cachedStamp = revision;
    }
    return cachedKeys;
  };
  return {
    getItem(key) {
      try {
        return read(fileFor(key)).value;
      } catch (error) {
        if (error.code === "ENOENT") return null;
        throw error;
      }
    },
    key(index) {
      return keys()[index] ?? null;
    },
    get length() {
      return keys().length;
    },
    removeItem(key) {
      try {
        read(fileFor(key));
        unlinkSync(fileFor(key));
      } catch (error) {
        if (error.code !== "ENOENT") throw error;
      }
      cachedStamp = undefined;
    },
    setItem(key, value) {
      if (typeof key !== "string" || typeof value !== "string")
        throw new Error(
          "Doctor telemetry storage requires string keys and values.",
        );
      const bytes = JSON.stringify({ key, value });
      if (Buffer.byteLength(bytes) > FILE_LIMIT)
        throw new Error("Doctor telemetry storage entry exceeds its budget.");
      const temporary = path.join(directory, `.${randomUUID()}.tmp`);
      try {
        const fd = openSync(temporary, "wx", 0o600);
        try {
          writeFileSync(fd, bytes);
          fsyncSync(fd);
        } finally {
          closeSync(fd);
        }
        renameSync(temporary, fileFor(key));
      } finally {
        try {
          unlinkSync(temporary);
        } catch (error) {
          if (error.code !== "ENOENT") throw error;
        }
        cachedStamp = undefined;
      }
    },
  };
}

export function hostedTelemetryDirectory(hostHome, relay) {
  const home = realpathSync(hostHome);
  let directory = home;
  for (const name of [
    ".chatcut-doctor",
    "telemetry",
    hash(relay).slice(0, 20),
  ]) {
    directory = path.join(directory, name);
    try {
      mkdirSync(directory, { mode: 0o700 });
    } catch (error) {
      if (error.code !== "EEXIST") throw error;
    }
    const entry = lstatSync(directory);
    if (
      !entry.isDirectory() ||
      entry.isSymbolicLink() ||
      !realpathSync(directory).startsWith(home + path.sep)
    )
      throw new Error(
        "Hosted telemetry storage escaped the selected host home.",
      );
  }
  return directory;
}
