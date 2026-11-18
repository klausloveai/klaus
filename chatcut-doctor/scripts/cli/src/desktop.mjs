import { execFile, spawn } from "node:child_process";
import { constants } from "node:fs";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const BUNDLE_ID = "io.chatcut.desktop";
const MAC_REQUIREMENT = `identifier "${BUNDLE_ID}" and anchor apple generic and certificate leaf[subject.OU] = "7WK2VURFPK"`;
const PUBLISHER = "ChatCut Inc.";
const DOWNLOAD_ROOT = "https://api.chatcut.io/desktop/download/";
const UPDATE_GUIDE_ROOT =
  "https://d2k0dx41dpnoir.cloudfront.net/desktop-update";
const MAX_DOWNLOAD_BYTES = 4 * 1024 ** 3;
const DOWNLOAD_TIMEOUT = 15 * 60_000;

export class DesktopError extends Error {
  constructor(code, stage, message, { cause, ...details } = {}) {
    super(message, cause ? { cause } : undefined);
    this.name = "DesktopError";
    this.code = code;
    this.stage = stage;
    this.details = details;
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      stage: this.stage,
      ...this.details,
      ...(this.cause ? { cause: describeCause(this.cause) } : {}),
    };
  }
}

/** Install an absent Desktop only with an explicit grant, then open the signed app. */
export async function ensureDesktop(options = {}) {
  const ctx = context(options);
  let installed = await inspect(ctx);
  let action = "launched";
  let warnings;
  if (!installed.installed) {
    requireInstallPermission(options);
    const result = await install(ctx, installed, false);
    installed = result.desktop;
    warnings = result.warnings;
    action = "installed";
  }
  progress(ctx, "launch", "Opening ChatCut Desktop");
  try {
    if (ctx.platform === "darwin") {
      await native(ctx, "launch", "/usr/bin/open", ["-a", installed.appPath]);
    } else {
      await native(ctx, "launch", installed.appPath, [], {
        waitForExit: false,
      });
    }
  } catch (cause) {
    throw new DesktopError(
      "launch_failed",
      "launch",
      "ChatCut is installed but could not be opened. Open it from Applications or the Start menu; use chatcut doctor for connection checks.",
      { appPath: installed.appPath, cause },
    );
  }
  return { ...installed, action, ...(warnings?.length ? { warnings } : {}) };
}

/**
 * Native boundaries are injectable for fixtures: platform, arch, release, home,
 * env, tmpdir, fs (node:fs/promises compatible), run(command, args, options), and
 * download(url, destination). Overrides are a programmatic test seam, never CLI
 * flags. run resolves { stdout, stderr }; waitForExit:false only waits for spawn.
 * onProgress receives { stage, message }. Inspection never launches or installs.
 */
export async function inspectDesktop(options = {}) {
  return inspect(context(options));
}

/** Canonical production profile paths, also available before Desktop is installed. */
export function resolveDesktopPaths(options = {}) {
  const ctx = context(options);
  return profilePaths(ctx);
}

/** Explicit update; never terminates a running app or opens it after updating. */
export async function updateDesktop(options = {}) {
  const ctx = context(options);
  try {
    const installed = await inspect(ctx);
    if (!installed.installed) requireInstallPermission(options);
    if (installed.installed) await requireClosed(ctx, installed.appPath);
    if (ctx.platform === "win32" && installed.scope === "machine") {
      throw new DesktopError(
        "app_updater_required",
        "update",
        "This ChatCut installation is shared by all users. Update it from ChatCut's app updater or run the official installer interactively.",
        { appPath: installed.appPath },
      );
    }
    const result = await install(ctx, installed, true);
    return {
      ...result.desktop,
      action: result.unchanged
        ? "up_to_date"
        : installed.installed
          ? "updated"
          : "installed",
      ...(result.warnings.length ? { warnings: result.warnings } : {}),
    };
  } catch (error) {
    if (error instanceof DesktopError) {
      const guide = new URL(UPDATE_GUIDE_ROOT);
      guide.search = new URLSearchParams({
        arch: ctx.arch,
        channel: "production",
        package: ctx.platform === "darwin" ? "dmg" : "exe",
        platform: ctx.platform,
      }).toString();
      error.details.guideUrl = guide.toString();
      error.message += ` Manual update guide: ${guide}`;
    }
    throw error;
  }
}

function asDesktopError(error, stage) {
  return error instanceof DesktopError
    ? error
    : new DesktopError(
        "install_failed",
        stage,
        "Desktop installation failed. Your projects and application data were not changed.",
        { cause: error },
      );
}

function context(options) {
  const ctx = {
    arch: options.arch ?? process.arch,
    download: options.download ?? downloadOfficial,
    env: options.env ?? process.env,
    fs: options.fs ?? fs,
    home: options.home ?? os.homedir(),
    onProgress: options.onProgress,
    platform: options.platform ?? process.platform,
    release: options.release ?? os.release(),
    run: options.run ?? runNative,
    tmpdir: options.tmpdir ?? os.tmpdir(),
  };
  if (
    !(
      (ctx.platform === "darwin" && ["arm64", "x64"].includes(ctx.arch)) ||
      (ctx.platform === "win32" &&
        ctx.arch === "x64" &&
        !/arm/i.test(
          ctx.env.PROCESSOR_ARCHITEW6432 ??
            ctx.env.PROCESSOR_ARCHITECTURE ??
            "",
        ))
    )
  ) {
    throw new DesktopError(
      "unsupported_platform",
      "platform",
      "ChatCut Desktop supports macOS 13+ on Apple Silicon or Intel, and Windows x64.",
      { arch: ctx.arch, platform: ctx.platform },
    );
  }
  if (ctx.platform === "darwin" && Number.parseInt(ctx.release, 10) < 22) {
    throw new DesktopError(
      "unsupported_os",
      "platform",
      "ChatCut Desktop requires macOS 13 or newer.",
      { release: ctx.release },
    );
  }
  ctx.paths = ctx.platform === "win32" ? path.win32 : path.posix;
  return ctx;
}

function describeCause(error) {
  const parts = [];
  for (let depth = 0; error && depth < 5; depth++, error = error.cause)
    parts.push(String(error.message ?? error).slice(0, 2000));
  return parts.join(": ");
}

async function downloadOfficial(url, destination) {
  const controller = new AbortController();
  const timer = setTimeout(
    () => controller.abort(new Error("Desktop download timed out")),
    DOWNLOAD_TIMEOUT,
  );
  let file;
  let primary;
  try {
    let response;
    for (let redirects = 0; redirects <= 5; redirects++) {
      const parsed = new URL(url);
      if (parsed.protocol !== "https:" || parsed.username || parsed.password)
        throw new Error("Desktop downloads require HTTPS");
      response = await fetch(parsed, {
        redirect: "manual",
        signal: controller.signal,
      });
      if (![301, 302, 303, 307, 308].includes(response.status)) break;
      const location = response.headers.get("location");
      await response.body?.cancel();
      if (!location || redirects === 5)
        throw new Error("Too many or invalid Desktop download redirects");
      url = new URL(location, parsed).href;
    }
    if (!response.ok || !response.body)
      throw new Error(`Desktop download returned HTTP ${response.status}`);
    const length = Number(response.headers.get("content-length"));
    if (length > MAX_DOWNLOAD_BYTES)
      throw new Error("Desktop download exceeds the size limit");
    file = await fs.open(destination, "wx", 0o600);
    let bytes = 0;
    for await (const chunk of response.body) {
      bytes += chunk.byteLength;
      if (bytes > MAX_DOWNLOAD_BYTES) {
        controller.abort();
        throw new Error("Desktop download exceeds the size limit");
      }
      for (let offset = 0; offset < chunk.byteLength; ) {
        const { bytesWritten } = await file.write(
          chunk,
          offset,
          chunk.byteLength - offset,
        );
        if (!bytesWritten)
          throw new Error("Desktop download could not be written to disk");
        offset += bytesWritten;
      }
    }
    if (!bytes || (length > 0 && bytes !== length))
      throw new Error("Desktop download was incomplete");
  } catch (error) {
    primary = error;
    throw error;
  } finally {
    clearTimeout(timer);
    controller.abort();
    try {
      await file?.close();
    } catch (error) {
      if (!primary) throw error;
    }
  }
}

async function exists(ctx, filePath) {
  try {
    await ctx.fs.lstat(filePath);
    return true;
  } catch (error) {
    if (error.code === "ENOENT") return false;
    throw asDesktopError(error, "discover");
  }
}

async function inspect(ctx) {
  // Codex's macOS sandbox denies spctl and ps, so a healthy app would otherwise
  // fail as a Gatekeeper or process-list error that the user cannot fix.
  if (ctx.platform === "darwin" && ctx.env.CODEX_SANDBOX === "seatbelt")
    throw new DesktopError(
      "sandboxed",
      "inspect",
      "This command is running inside the Codex sandbox, which blocks macOS app verification. Run it again outside the sandbox by requesting escalated permissions.",
    );
  const base = {
    arch: ctx.arch,
    installed: false,
    platform: ctx.platform,
    ...profilePaths(ctx),
  };
  const candidates =
    ctx.platform === "darwin"
      ? [
          "/Applications/ChatCut.app",
          ctx.paths.join(ctx.home, "Applications", "ChatCut.app"),
        ].map((appPath) => ({ appPath }))
      : await windowsCandidates(ctx);
  for (const candidate of candidates) {
    if (!(await exists(ctx, candidate.appPath))) continue;
    const version = await verifyApp(ctx, candidate.appPath, "verify_installed");
    return {
      ...base,
      ...candidate,
      installed: true,
      resourcesSkillsDir:
        ctx.platform === "darwin"
          ? ctx.paths.join(candidate.appPath, "Contents", "Resources", "skills")
          : ctx.paths.join(
              ctx.paths.dirname(candidate.appPath),
              "resources",
              "skills",
            ),
      version,
    };
  }
  return base;
}

async function install(ctx, previous, updating) {
  progress(
    ctx,
    "download",
    updating
      ? "Downloading the current production Desktop"
      : "Downloading ChatCut Desktop",
  );
  const workspace = await ctx.fs.mkdtemp(
    ctx.paths.join(ctx.tmpdir, "chatcut-desktop-"),
  );
  const artifact = ctx.paths.join(
    workspace,
    ctx.platform === "darwin" ? "ChatCut.dmg" : "ChatCut-Setup.exe",
  );
  const warnings = [];
  let mounted = false;
  let mountAttempted = false;
  let mountPath;
  let primary;
  let result;
  try {
    const target =
      ctx.platform === "darwin"
        ? ctx.arch === "arm64"
          ? "macos"
          : "macos-x64"
        : "windows";
    try {
      await ctx.download(`${DOWNLOAD_ROOT}${target}?src=cli`, artifact);
    } catch (cause) {
      throw new DesktopError(
        "download_failed",
        "download",
        "The official Desktop download failed. Retry chatcut app when the network is available.",
        { cause },
      );
    }
    if (ctx.platform === "darwin") {
      mountPath = ctx.paths.join(workspace, "mount");
      await ctx.fs.mkdir(mountPath);
      mountAttempted = true;
      await native(
        ctx,
        "mount",
        "/usr/bin/hdiutil",
        [
          "attach",
          "-readonly",
          "-nobrowse",
          "-mountpoint",
          mountPath,
          artifact,
        ],
        { timeout: 120_000 },
      );
      mounted = true;
      const source = ctx.paths.join(mountPath, "ChatCut.app");
      const version = await verifyApp(ctx, source, "verify_download");
      if (
        previous.installed &&
        versionsEqualOrNewer(previous.version, version)
      ) {
        result = { desktop: previous, unchanged: true };
      } else {
        const installed = await installMac(ctx, source, previous, updating);
        warnings.push(...installed.warnings);
        result = {
          desktop: installed.desktop,
          unchanged: installed.unchanged,
        };
      }
    } else {
      const version = await verifyWindows(
        ctx,
        artifact,
        "verify_download",
        true,
      );
      const beforeInstall = await inspect(ctx);
      if (
        beforeInstall.installed &&
        (!previous.installed ||
          beforeInstall.appPath.toLowerCase() !==
            previous.appPath.toLowerCase())
      )
        throw new DesktopError(
          "install_conflict",
          "install",
          "The ChatCut installation changed while the download was in progress. Retry the command to use the current app.",
          { appPath: beforeInstall.appPath },
        );
      if (
        beforeInstall.installed &&
        versionsEqualOrNewer(beforeInstall.version, version)
      ) {
        result = { desktop: beforeInstall, unchanged: true };
      } else {
        if (beforeInstall.installed)
          await requireClosed(ctx, beforeInstall.appPath);
        progress(
          ctx,
          "install",
          "Installing signed ChatCut Desktop for the current user",
        );
        await native(ctx, "install", artifact, ["/S", "/currentuser"], {
          timeout: 10 * 60_000,
        });
        const desktop = await inspect(ctx);
        if (!desktop.installed)
          throw new DesktopError(
            "install_failed",
            "verify_destination",
            "The installer completed, but a signed production ChatCut installation was not found.",
          );
        if (
          previous.installed &&
          desktop.appPath.toLowerCase() !== previous.appPath.toLowerCase()
        )
          throw new DesktopError(
            "install_location_changed",
            "verify_destination",
            "The installer registered a different application location. Open ChatCut from the Start menu and check the installation before retrying.",
            { appPath: desktop.appPath, previousAppPath: previous.appPath },
          );
        if (!versionsEqualOrNewer(desktop.version, version))
          throw new DesktopError(
            "update_not_applied",
            "verify_destination",
            "The installer completed, but the installed app is older than the verified download. Use the updater inside ChatCut or the official installer interactively.",
            {
              appPath: desktop.appPath,
              downloadedVersion: version,
              installedVersion: desktop.version,
            },
          );
        result = { desktop, unchanged: false };
      }
    }
  } catch (error) {
    primary = asDesktopError(error, "install");
  } finally {
    if (mountAttempted) {
      try {
        await native(
          ctx,
          "cleanup",
          "/usr/bin/hdiutil",
          ["detach", mountPath],
          { timeout: 30_000 },
        );
        mounted = false;
      } catch (error) {
        // A failed attach can leave a mounted volume. Never remove its parent
        // recursively unless detach succeeded, even when attach itself failed.
        mounted = true;
        warnings.push({
          code: "mount_cleanup_failed",
          message: error.message,
          path: mountPath,
        });
      }
    }
    if (!mounted) {
      try {
        await ctx.fs.rm(workspace, { force: true, recursive: true });
      } catch (error) {
        warnings.push({
          code: "cleanup_failed",
          message: error.message,
          path: workspace,
        });
      }
    }
  }
  if (primary) {
    if (warnings.length)
      primary.details.cleanupWarnings = [
        ...(primary.details.cleanupWarnings ?? []),
        ...warnings,
      ];
    throw primary;
  }
  return { ...result, warnings };
}

async function installMac(ctx, source, previous, updating) {
  let destination = previous.appPath;
  if (!destination) {
    let parent = "/Applications";
    try {
      await ctx.fs.access(parent, constants.W_OK);
    } catch {
      parent = ctx.paths.join(ctx.home, "Applications");
    }
    destination = ctx.paths.join(parent, "ChatCut.app");
  }
  const parent = ctx.paths.dirname(destination);
  await ctx.fs.mkdir(parent, { recursive: true });
  // Both app renames stay on the destination filesystem. ditto receives a new
  // absent destination, so app updates can never merge old and new bundles.
  const stageRoot = await ctx.fs.mkdtemp(
    ctx.paths.join(parent, ".chatcut-install-"),
  );
  const staged = ctx.paths.join(stageRoot, "ChatCut.app");
  const backup = ctx.paths.join(stageRoot, "previous.app");
  const warnings = [];
  let movedPrevious = false;
  let movedNew = false;
  let keepBackup = false;
  let primary;
  let desktop;
  try {
    progress(
      ctx,
      "stage",
      "Checking the signed application before installation",
    );
    await native(ctx, "stage", "/usr/bin/ditto", [source, staged], {
      timeout: 5 * 60_000,
    });
    const stagedVersion = await verifyApp(ctx, staged, "verify_stage");
    if (await exists(ctx, destination)) {
      if (!updating || !previous.installed)
        throw new DesktopError(
          "install_conflict",
          "activate",
          "A ChatCut app appeared while installation was in progress. Retry chatcut app to use it.",
          { appPath: destination },
        );
      const currentVersion = await verifyApp(
        ctx,
        destination,
        "verify_existing",
      );
      if (versionsEqualOrNewer(currentVersion, stagedVersion)) {
        return {
          desktop: { ...previous, version: currentVersion },
          unchanged: true,
          warnings,
        };
      }
      await requireClosed(ctx, destination);
      await ctx.fs.rename(destination, backup);
      movedPrevious = true;
    }
    await ctx.fs.rename(staged, destination);
    movedNew = true;
    const version = await verifyApp(ctx, destination, "verify_destination");
    desktop = {
      arch: ctx.arch,
      installed: true,
      platform: ctx.platform,
      ...profilePaths(ctx),
      appPath: destination,
      resourcesSkillsDir: ctx.paths.join(
        destination,
        "Contents",
        "Resources",
        "skills",
      ),
      version,
    };
  } catch (error) {
    primary = asDesktopError(error, "activate");
    try {
      if (movedNew)
        await ctx.fs.rm(destination, { force: true, recursive: true });
      if (movedPrevious) await ctx.fs.rename(backup, destination);
    } catch (rollbackError) {
      keepBackup = movedPrevious;
      primary.details.rollback = {
        backupPath: movedPrevious ? backup : undefined,
        message: rollbackError.message,
      };
    }
  } finally {
    if (!keepBackup) {
      try {
        await ctx.fs.rm(stageRoot, { force: true, recursive: true });
      } catch (cleanupError) {
        warnings.push({
          code: "cleanup_failed",
          message: cleanupError.message,
          path: stageRoot,
        });
      }
    }
  }
  if (primary) {
    if (warnings.length)
      primary.details.cleanupWarnings = [
        ...(primary.details.cleanupWarnings ?? []),
        ...warnings,
      ];
    throw primary;
  }
  return { desktop, unchanged: false, warnings };
}

async function native(ctx, stage, command, args, options = {}) {
  const env = { ...ctx.env };
  if (options.waitForExit === false) {
    delete env.ELECTRON_RUN_AS_NODE;
    delete env.ELECTRON_NO_ATTACH_CONSOLE;
  }
  try {
    return await ctx.run(command, args, {
      env,
      maxBuffer: 1024 * 1024,
      timeout: 30_000,
      ...options,
    });
  } catch (cause) {
    throw new DesktopError(
      "native_command_failed",
      stage,
      `Desktop ${stage.replaceAll("_", " ")} failed.`,
      {
        cause,
        command,
        ...(typeof cause.stderr === "string"
          ? { stderr: cause.stderr.slice(0, 4000) }
          : {}),
        ...(cause.code !== undefined ? { exitCode: cause.code } : {}),
      },
    );
  }
}

async function powershellJson(ctx, stage, script) {
  const executable = ctx.paths.join(
    ctx.env.SystemRoot || ctx.env.WINDIR || "C:\\Windows",
    "System32",
    "WindowsPowerShell",
    "v1.0",
    "powershell.exe",
  );
  const { stdout } = await native(ctx, stage, executable, [
    "-NoProfile",
    "-NonInteractive",
    "-InputFormat",
    "None",
    "-Command",
    `$ErrorActionPreference = 'Stop'; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; ${script}`,
  ]);
  try {
    return JSON.parse(stdout.replace(/^\uFEFF/, ""));
  } catch (cause) {
    throw new DesktopError(
      "invalid_native_output",
      stage,
      "A Windows system check returned invalid data.",
      { cause },
    );
  }
}

function profilePaths(ctx) {
  const userDataPath =
    ctx.platform === "darwin"
      ? ctx.paths.join(ctx.home, "Library", "Application Support", "ChatCut")
      : ctx.paths.join(
          ctx.env.APPDATA || ctx.paths.join(ctx.home, "AppData", "Roaming"),
          "ChatCut",
        );
  return {
    launcherPath: ctx.paths.join(
      userDataPath,
      ctx.platform === "darwin" ? "chatcut-mcp" : "chatcut-mcp.cmd",
    ),
    userDataPath,
  };
}

function progress(ctx, stage, message) {
  ctx.onProgress?.({ message, stage });
}

function psQuote(value) {
  return `'${value.replaceAll("'", "''")}'`;
}

async function requireClosed(ctx, appPath) {
  let running;
  if (ctx.platform === "darwin") {
    const { stdout } = await native(ctx, "check_running", "/bin/ps", [
      "-wwaxo",
      "args=",
    ]);
    // Agent connections run the app binary as Node on a bundled script. They
    // hold no work to save, and the agent asking for the update owns one.
    running = stdout
      .split(/\r?\n/)
      .map((line) => line.trim())
      .some(
        (line) =>
          line.startsWith(`${appPath}/Contents/`) &&
          !line.includes(`${appPath}/Contents/Resources/`),
      );
  } else {
    running = await powershellJson(
      ctx,
      "check_running",
      `$target = ${psQuote(appPath)}; $processes = @(Get-CimInstance Win32_Process -Filter "Name='ChatCut.exe'"); [bool](@($processes | Where-Object { !$_.ExecutablePath -or $_.ExecutablePath -eq $target }).Count -gt 0) | ConvertTo-Json -Compress`,
    );
    if (typeof running !== "boolean")
      throw new DesktopError(
        "invalid_native_output",
        "check_running",
        "Could not determine whether ChatCut is running.",
      );
  }
  if (running)
    throw new DesktopError(
      "close_app_required",
      "check_running",
      "ChatCut is running. Save your work and close ChatCut before retrying chatcut update, or use the updater inside the app.",
      { appPath },
    );
}

function requireInstallPermission(options) {
  if (options.allowInstall === true) return;
  throw new DesktopError(
    "install_permission_required",
    "permission",
    "ChatCut Desktop is not installed. Nothing was downloaded or installed. An agent must request this command through a host permission prompt requiring your approval before adding --allow-install. If approval is denied, stop. If that prompt is unavailable, run chatcut connect --allow-install --json yourself when ready.",
  );
}

async function runNative(command, args, options) {
  const { waitForExit, ...execOptions } = options;
  const env = { ...execOptions.env };
  // Prevent caller-provided module search paths from replacing system cmdlets.
  if (command.toLowerCase().endsWith("\\powershell.exe"))
    env.PSModulePath = path.win32.join(path.win32.dirname(command), "Modules");
  if (waitForExit === false) {
    await new Promise((resolve, reject) => {
      const child = spawn(command, args, {
        detached: true,
        env,
        stdio: "ignore",
        windowsHide: false,
      });
      child.once("error", reject);
      child.once("spawn", () => {
        child.unref();
        resolve();
      });
    });
    return { stderr: "", stdout: "" };
  }
  return execFileAsync(command, args, {
    ...execOptions,
    encoding: "utf8",
    env,
    windowsHide: true,
  });
}

async function verifyApp(ctx, appPath, stage) {
  let version;
  try {
    const stat = await ctx.fs.lstat(appPath);
    if (
      stat.isSymbolicLink() ||
      (ctx.platform === "darwin" ? !stat.isDirectory() : !stat.isFile())
    )
      throw new Error("The app path is not a regular installed application");
    if (ctx.platform === "win32")
      return await verifyWindows(ctx, appPath, stage, true);
    const plist = ctx.paths.join(appPath, "Contents", "Info.plist");
    const { stdout } = await native(ctx, stage, "/usr/bin/plutil", [
      "-convert",
      "json",
      "-o",
      "-",
      plist,
    ]);
    const info = JSON.parse(stdout);
    if (
      info.CFBundleIdentifier !== BUNDLE_ID ||
      info.CFBundleExecutable !== "ChatCut"
    )
      throw new Error("The bundle is not the production ChatCut application");
    await native(ctx, stage, "/usr/bin/codesign", [
      "--verify",
      "--deep",
      "--strict",
      "--verbose=2",
      "-R",
      `=${MAC_REQUIREMENT}`,
      appPath,
    ]);
    version = info.CFBundleShortVersionString || info.CFBundleVersion || null;
  } catch (cause) {
    if (ctx.platform === "win32" && cause instanceof DesktopError) throw cause;
    throw new DesktopError(
      "signature_invalid",
      stage,
      "ChatCut's production identity or trusted signature could not be verified. The existing app has been left in place; install the official signed Desktop from chatcut.io/download.",
      { ...cause.details, appPath, cause },
    );
  }
  const assessmentStage = stage.replace(/^verify_/, "assess_");
  try {
    await native(ctx, assessmentStage, "/usr/sbin/spctl", [
      "--assess",
      "--type",
      "execute",
      "--verbose=2",
      appPath,
    ]);
  } catch (cause) {
    throw new DesktopError(
      "gatekeeper_assessment_failed",
      assessmentStage,
      "ChatCut's signature is valid, but macOS Gatekeeper could not approve this app. Check the system assessment details before retrying; the app has not been opened.",
      { ...cause.details, appPath, cause },
    );
  }
  return version;
}

async function verifyWindows(ctx, filePath, stage, requireProduct) {
  const result = await powershellJson(
    ctx,
    stage,
    [
      `$item = Get-Item -LiteralPath ${psQuote(filePath)}`,
      "$signature = Get-AuthenticodeSignature -LiteralPath $item.FullName",
      "[PSCustomObject]@{ Status=[int]$signature.Status; StatusMessage=$signature.StatusMessage; Subject=$signature.SignerCertificate.Subject; Path=$signature.Path; ProductName=$item.VersionInfo.ProductName; Version=$item.VersionInfo.ProductVersion } | ConvertTo-Json -Compress",
    ].join("; "),
  );
  const textField = (value) =>
    typeof value === "string" ? value.slice(0, 2048) : null;
  const observed = {
    productName: textField(result?.ProductName),
    signaturePath: textField(result?.Path),
    status: typeof result?.Status === "number" ? result.Status : null,
    statusMessage: textField(result?.StatusMessage),
    subject: textField(result?.Subject),
    version: textField(result?.Version),
  };
  const cn =
    typeof result?.Subject === "string"
      ? /(?:^|,\s*)CN=("(?:[^"]|"")*"|[^,]*)/i
          .exec(result.Subject)?.[1]
          ?.replace(/^"|"$/g, "")
          .replaceAll('""', '"')
      : undefined;
  // The native command binds verification to Get-Item -LiteralPath above.
  // Signature.Path is display metadata: Windows may expand an 8.3 path alias.
  if (result?.Status !== 0) {
    throw new DesktopError(
      "signature_invalid",
      stage,
      "Windows could not verify the file's Authenticode signature as trusted.",
      { appPath: filePath, observed },
    );
  }
  if (cn !== PUBLISHER)
    throw new DesktopError(
      "publisher_mismatch",
      stage,
      "The Windows file's signed publisher does not match ChatCut Inc.",
      { appPath: filePath, expectedPublisher: PUBLISHER, observed },
    );
  if (requireProduct && result.ProductName !== "ChatCut")
    throw new DesktopError(
      "product_mismatch",
      stage,
      "The Windows file's signed product is not the production ChatCut application.",
      { appPath: filePath, expectedProductName: "ChatCut", observed },
    );
  return observed.version;
}

function versionsEqualOrNewer(installed, downloaded) {
  if (installed === downloaded && installed) return true;
  const pattern =
    /^(\d+(?:\.\d+){1,3})(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$/;
  const installedMatch = pattern.exec(installed ?? "");
  const downloadedMatch = pattern.exec(downloaded ?? "");
  if (!installedMatch || !downloadedMatch)
    throw new DesktopError(
      "version_unreadable",
      "compare_versions",
      "The installed and downloaded versions could not be compared safely. Use the updater inside ChatCut or the official installer interactively.",
      { downloadedVersion: downloaded, installedVersion: installed },
    );
  const left = installedMatch[1].split(".").map(Number);
  const right = downloadedMatch[1].split(".").map(Number);
  for (let i = 0; i < Math.max(left.length, right.length); i++) {
    if ((left[i] ?? 0) !== (right[i] ?? 0))
      return (left[i] ?? 0) > (right[i] ?? 0);
  }
  const leftPrerelease = installedMatch[2]?.split(".");
  const rightPrerelease = downloadedMatch[2]?.split(".");
  if (!leftPrerelease || !rightPrerelease) return !leftPrerelease;
  for (
    let i = 0;
    i < Math.max(leftPrerelease.length, rightPrerelease.length);
    i++
  ) {
    const a = leftPrerelease[i];
    const b = rightPrerelease[i];
    if (a === b) continue;
    if (a === undefined || b === undefined) return b === undefined;
    if (/^\d+$/.test(a) && /^\d+$/.test(b)) return Number(a) > Number(b);
    if (/^\d+$/.test(a) !== /^\d+$/.test(b)) return !/^\d+$/.test(a);
    return a > b;
  }
  return true;
}

async function windowsCandidates(ctx) {
  const programFiles = ctx.env.ProgramFiles || "C:\\Program Files";
  const local =
    ctx.env.LOCALAPPDATA || ctx.paths.join(ctx.home, "AppData", "Local");
  const script = [
    "$items = @()",
    "foreach ($entry in @(@{Root='HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall';Scope='user'}, @{Root='HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall';Scope='machine'}, @{Root='HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall';Scope='machine'})) { $items += @(Get-ItemProperty ($entry.Root + '\\*') -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -eq 'ChatCut' } | ForEach-Object { [PSCustomObject]@{ InstallLocation=$_.InstallLocation; DisplayIcon=$_.DisplayIcon; Scope=$entry.Scope } }) }",
    "ConvertTo-Json -InputObject @($items) -Compress",
  ].join("; ");
  const records = await powershellJson(ctx, "discover", script);
  if (!Array.isArray(records))
    throw new DesktopError(
      "invalid_native_output",
      "discover",
      "Windows installation discovery returned invalid data.",
    );
  const candidates = [];
  for (const record of records) {
    const icon =
      typeof record.DisplayIcon === "string"
        ? record.DisplayIcon.replace(/,\s*-?\d+$/, "").replace(/^"|"$/g, "")
        : "";
    const appPath =
      typeof record.InstallLocation === "string" && record.InstallLocation
        ? ctx.paths.join(record.InstallLocation, "ChatCut.exe")
        : icon;
    if (
      typeof appPath === "string" &&
      ctx.paths.isAbsolute(appPath) &&
      ctx.paths.basename(appPath).toLowerCase() === "chatcut.exe"
    ) {
      candidates.push({
        appPath,
        scope: record.Scope === "machine" ? "machine" : "user",
      });
    }
  }
  candidates.push(
    {
      appPath: ctx.paths.join(local, "Programs", "ChatCut", "ChatCut.exe"),
      scope: "user",
    },
    {
      appPath: ctx.paths.join(
        local,
        "Programs",
        "chatcut-desktop",
        "ChatCut.exe",
      ),
      scope: "user",
    },
    {
      appPath: ctx.paths.join(programFiles, "ChatCut", "ChatCut.exe"),
      scope: "machine",
    },
  );
  return [
    ...new Map(
      candidates.map((candidate) => [
        candidate.appPath.toLowerCase(),
        candidate,
      ]),
    ).values(),
  ];
}
