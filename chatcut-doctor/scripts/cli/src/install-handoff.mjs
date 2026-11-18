import fs from "node:fs/promises";
import path from "node:path";

import { resolveDesktopPaths } from "./desktop.mjs";

const INSTALL_SOURCE = /^[a-z][a-z0-9_]{1,47}$/u;

// Same rule as @chatcut/telemetry's normalizeInstallSource; this package ships
// without workspace dependencies.
export function normalizeInstallSource(value) {
  if (typeof value !== "string" || value.length > 200) return null;
  const normalized = value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/gu, "_")
    .replace(/^_+|_+$/gu, "");
  return INSTALL_SOURCE.test(normalized) ? normalized : null;
}

/**
 * Leaves the install channel for Desktop, which adopts it on its next start or
 * maintenance request. Attribution never blocks installing or connecting.
 */
export async function writeInstallHandoff(
  installSource,
  { userDataPath } = resolveDesktopPaths(),
) {
  const target = path.join(userDataPath, "install-handoff.json");
  const temporary = `${target}.${process.pid}.tmp`;
  try {
    await fs.mkdir(userDataPath, { recursive: true });
    await fs.writeFile(
      temporary,
      JSON.stringify({
        createdAt: new Date().toISOString(),
        installSource,
        version: 1,
      }),
      { mode: 0o600 },
    );
    await fs.rename(temporary, target);
    return true;
  } catch {
    await fs.rm(temporary, { force: true }).catch(() => undefined);
    return false;
  }
}
