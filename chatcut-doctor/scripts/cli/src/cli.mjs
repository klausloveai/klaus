import { readFile } from "node:fs/promises";
import { parseArgs } from "node:util";

import packageInfo from "../package.json" with { type: "json" };
import { manageAcquisitionSkills } from "./acquisition-skills.mjs";
import { connectAgent, runAgentCommand } from "./agent.mjs";
import { CLIENTS } from "./clients.mjs";
import { ensureDesktop, updateDesktop } from "./desktop.mjs";
import { readDoctorReportFile } from "./doctor-reports.mjs";
import { errorEvidence, runDoctor } from "./doctor.mjs";
import { runObservedDoctor } from "./doctor/operation-result.mjs";
import {
  normalizeInstallSource,
  writeInstallHandoff,
} from "./install-handoff.mjs";

const HELP = `ChatCut — your desktop video editor

Usage:
  chatcut                         Open an installed Desktop
  chatcut app                     Same as chatcut
  chatcut connect [--json]         Make Desktop tools and skills ready via CLI
  chatcut connect --client <name>  Also repair a known native host integration
  chatcut doctor [--json]          Check Desktop, MCP and managed skills
  chatcut doctor --fix [--json]    Ask the running Desktop to repair integrations
  chatcut doctor --context FILE [--json]   Start a target-bound local case
  chatcut doctor --case DIR --context FILE --action ACTION [--json]
  chatcut doctor --report-file FILE --diagnostic-id ID --report-sha256 HASH --json
  chatcut update [--json]          Update Desktop after closing it
  chatcut tools list --json        Discover Desktop tools through this CLI
  chatcut tools describe <name>    Read a tool's live input schema
  chatcut tools call <name>        Call a Desktop tool without host registration
  chatcut skills list --json       Discover Desktop's bundled agent skills
  chatcut skills read <name>       Read a bundled skill
  chatcut skills install           Install acquisition skills for Claude and Codex
  chatcut skills remove            Remove unchanged owned acquisition skills

Options:
  --no-install                    Connect/open only an installed Desktop
  --allow-install                 Permit a first Desktop download/install
                                  Agents: requires an explicit host approval
  --client <name>                  Limit connect or doctor to one integration
                                  ${CLIENTS.join(", ")}
                                  skills install/remove: claude-code or codex
  --context FILE                  Dedicated .doctor-context.json; selects one surface and scope
  --case DIR                      Resume the original case; preserve its evidence
  --case-root DIR                 Directory for new local cases
  --failure-record FILE           Dedicated original .mcp-failure.json or .doctor-failure.json
  --action check|repair|native-recheck|record-recheck|finish|status|upload|evidence|handoff
  --handoff FILE                  Read a product-generated .doctor-handoff.json without MCP
  --source-event list|ID          Select an existing program-recorded source without MCP
  --user-data DIR                 Explicit failing Desktop profile for source selection
  --evidence-ref REF              Read an opaque reference from the evidence directory
  --resume-file FILE              Bind follow-ups to one .doctor-resume.json
  --project-id ID                 Actual Desktop project for source material or native-recheck
  --result FILE                   Native .doctor-recheck.json or agent .doctor-finish.json
  --online                        Allow bounded anonymous Hosted checks at the selected endpoint
  --source <channel>               Record which channel installed ChatCut
                                  (or set CHATCUT_INSTALL_SOURCE)
  --json                          Write one structured result to stdout
  --args <json>                    Tool argument object (defaults to {})
  --args-file <path|->             Read tool arguments from a file or stdin
  --timeout <seconds>              Tool call timeout, 1–1800 (default 300)
  --file <relative-path>           Read a skill reference instead of SKILL.md
  --help                          Show help without opening Desktop
  --version                       Show CLI version

First use: npx --yes @chatcut/cli connect --allow-install --json
Agents must obtain a host permission click for that exact command first.
Local candidate: node <checkout>/apps/cli/bin/chatcut.mjs doctor --context FILE --json
Public npm availability must be verified separately before using npx.
Desktop supports macOS 13+ and Windows x64. Node.js 22+ is required for this CLI.
`;

export async function runCli(args, dependencies = {}) {
  const stdout = dependencies.stdout ?? process.stdout;
  const stderr = dependencies.stderr ?? process.stderr;
  let json = args.includes("--json");
  try {
    const { positionals, values } = parseArgs({
      allowPositionals: true,
      args,
      options: {
        action: { type: "string" },
        "allow-install": { type: "boolean" },
        args: { type: "string" },
        "args-file": { type: "string" },
        case: { type: "string" },
        "case-root": { type: "string" },
        client: { type: "string" },
        context: { type: "string" },
        "diagnostic-id": { type: "string" },
        "evidence-ref": { type: "string" },
        "failure-record": { type: "string" },
        file: { type: "string" },
        fix: { type: "boolean" },
        handoff: { type: "string" },
        help: { short: "h", type: "boolean" },
        json: { type: "boolean" },
        "no-install": { type: "boolean" },
        online: { type: "boolean" },
        "project-id": { type: "string" },
        "report-file": { type: "string" },
        "report-sha256": { type: "string" },
        result: { type: "string" },
        "resume-file": { type: "string" },
        source: { type: "string" },
        "source-event": { type: "string" },
        timeout: { type: "string" },
        "user-data": { type: "string" },
        version: { short: "v", type: "boolean" },
      },
    });
    json = !!values.json;
    if (values["allow-install"] && values["no-install"])
      throw new Error("--allow-install and --no-install cannot be combined.");
    if (values.help || positionals[0] === "help") {
      stdout.write(HELP);
      return 0;
    }
    if (values.version) {
      stdout.write(`${packageInfo.version}\n`);
      return 0;
    }
    const command = positionals[0] ?? "app";
    const agentCommand = command === "tools" || command === "skills";
    const action = positionals[1] ?? "list";
    const name = positionals[2];
    const localSkills =
      command === "skills" && ["install", "remove"].includes(action);
    if (
      (!agentCommand && positionals.length > 1) ||
      !["app", "connect", "doctor", "skills", "tools", "update"].includes(
        command,
      )
    )
      throw new Error("Unknown command. Run chatcut --help.");
    if (
      agentCommand &&
      (!(
        command === "tools"
          ? ["list", "describe", "call"]
          : ["list", "read", "install", "remove"]
      ).includes(action) ||
        positionals.length > (action === "list" || localSkills ? 2 : 3) ||
        (!localSkills &&
          action !== "list" &&
          !/^[A-Za-z0-9_-]+$/.test(name ?? "")))
    )
      throw new Error("Invalid tool or skill command. Run chatcut --help.");
    const toolCall = command === "tools" && action === "call";
    if (
      (values.args !== undefined ||
        values["args-file"] !== undefined ||
        values.timeout !== undefined) &&
      !toolCall
    )
      throw new Error(
        "--args, --args-file and --timeout apply only to chatcut tools call.",
      );
    if (values.args !== undefined && values["args-file"] !== undefined)
      throw new Error("Choose --args or --args-file, not both.");
    if (
      values.file !== undefined &&
      !(command === "skills" && action === "read")
    )
      throw new Error("--file applies only to chatcut skills read.");
    const timeoutMs = Number(values.timeout ?? 300) * 1000;
    if (
      toolCall &&
      (!Number.isInteger(timeoutMs) ||
        timeoutMs < 1000 ||
        timeoutMs > 1_800_000)
    )
      throw new Error("--timeout must be between 1 and 1800 seconds.");
    if (values.fix && command !== "doctor")
      throw new Error("--fix applies only to chatcut doctor.");
    if (values["allow-install"] && command === "doctor" && !values.fix)
      throw new Error("--allow-install requires doctor --fix.");
    if (values["allow-install"] && localSkills)
      throw new Error(
        "skills install/remove never installs Desktop; omit --allow-install.",
      );
    if (
      values.client &&
      !["connect", "doctor"].includes(command) &&
      !localSkills
    )
      throw new Error(
        "--client applies only to chatcut connect, doctor or skills install/remove.",
      );
    if (
      localSkills &&
      values.client &&
      !["claude-code", "codex"].includes(values.client)
    )
      throw new Error(
        "Skill installation supports --client claude-code or codex.",
      );
    if (
      command !== "doctor" &&
      [
        "context",
        "case",
        "case-root",
        "failure-record",
        "action",
        "result",
        "online",
        "report-file",
        "diagnostic-id",
        "report-sha256",
        "resume-file",
        "project-id",
        "handoff",
        "evidence-ref",
        "source-event",
        "user-data",
      ].some((key) => values[key])
    )
      throw new Error(
        "Doctor options require the doctor command; no application was opened or installed.",
      );
    if (values.client && !CLIENTS.includes(values.client))
      throw new Error(`--client must be one of ${CLIENTS.join(", ")}.`);
    if (
      (values["diagnostic-id"] || values["report-sha256"]) &&
      !values["report-file"]
    )
      throw new Error(
        "Report selectors require --report-file; no default diagnostic executed.",
      );
    if (
      values["report-file"] &&
      [
        "context",
        "case",
        "case-root",
        "failure-record",
        "action",
        "result",
        "online",
        "fix",
        "client",
        "resume-file",
        "project-id",
        "handoff",
        "evidence-ref",
        "source-event",
        "user-data",
      ].some((key) => values[key])
    )
      throw new Error(
        "Offline report reconstruction cannot be combined with a connection operation.",
      );
    if ((values.context || values.case) && values.client)
      throw new Error(
        "The context selects the host; --client cannot override it.",
      );
    if (values.case && (values["failure-record"] || values["case-root"]))
      throw new Error(
        "Resume a case without replacing its original capture or root.",
      );
    if (values.result && !["finish", "record-recheck"].includes(values.action))
      throw new Error("--result requires --action record-recheck or finish.");
    if (values.action === "finish" && !values.result)
      throw new Error(
        "--action finish requires a dedicated --result .doctor-finish.json.",
      );
    if (values["user-data"] && !values["source-event"])
      throw new Error(
        "--user-data requires explicit --source-event list or ID.",
      );
    if (
      values["source-event"] &&
      (!values["user-data"] ||
        !values["project-id"] ||
        [
          "context",
          "case",
          "case-root",
          "failure-record",
          "resume-file",
          "fix",
          "online",
          "client",
          "handoff",
          "result",
          "evidence-ref",
        ].some((key) => values[key]))
    )
      throw new Error(
        "Source selection needs only its explicit userData, project and source reference; it cannot repair or replace another case.",
      );
    if (
      values["evidence-ref"] &&
      !values.handoff &&
      values.action !== "evidence"
    )
      throw new Error(
        "--evidence-ref requires --handoff or --action evidence.",
      );
    if (
      values.handoff &&
      [
        "context",
        "case",
        "case-root",
        "failure-record",
        "resume-file",
        "fix",
        "online",
        "client",
      ].some((key) => values[key])
    )
      throw new Error(
        "Read a handoff independently from connection operations.",
      );
    if (
      values["project-id"] &&
      values.action !== "native-recheck" &&
      !values["source-event"]
    )
      throw new Error("--project-id applies only to --action native-recheck.");
    if (values.fix && values.action && values.action !== "repair")
      throw new Error("--fix cannot be combined with a different action.");
    if (
      command === "doctor" &&
      !values.context &&
      !values.case &&
      !values["resume-file"] &&
      !values["report-file"] &&
      !values.handoff &&
      !values["source-event"] &&
      ["case-root", "failure-record", "action", "result", "online"].some(
        (key) => values[key],
      )
    )
      throw new Error(
        "Target-bound Doctor options need --context or --case; no default production check executed.",
      );
    // Every command that may install or open Desktop can carry the channel.
    const opensDesktop =
      command !== "doctor" && command !== "update" && !localSkills;
    if (values.source !== undefined && !opensDesktop)
      throw new Error(
        "--source applies only to commands that open Desktop, not doctor or update.",
      );
    if (values.source !== undefined && !normalizeInstallSource(values.source))
      throw new Error(
        "--source must name a channel such as oss_viral_cloner: 2-48 letters, digits or underscores, starting with a letter.",
      );
    // An ambient variable is never worth failing setup over.
    const installSource = opensDesktop
      ? normalizeInstallSource(
          values.source ??
            (dependencies.env ?? process.env).CHATCUT_INSTALL_SOURCE,
        )
      : null;
    const options = {
      allowInstall: values["allow-install"] === true,
      onProgress: (entry) =>
        stderr.write(`${typeof entry === "string" ? entry : entry.message}\n`),
    };
    if (installSource)
      await (dependencies.writeInstallHandoff ?? writeInstallHandoff)(
        installSource,
      );
    let result;
    if (localSkills) {
      result = await (
        dependencies.acquisitionSkills ?? manageAcquisitionSkills
      )(
        { action, client: values.client },
        { env: dependencies.env, homeDir: dependencies.homeDir },
      );
    } else if (agentCommand) {
      const input =
        values["args-file"] === "-"
          ? await readInput(dependencies.stdin ?? process.stdin)
          : values["args-file"] !== undefined
            ? await readFile(values["args-file"], "utf8")
            : (values.args ?? "{}");
      if (Buffer.byteLength(input) > 4 * 1024 * 1024)
        throw new Error("Tool arguments exceed 4 MiB.");
      result = await (dependencies.agent ?? runAgentCommand)(
        {
          ...options,
          action,
          command,
          name,
          ...(toolCall ? { arguments: JSON.parse(input), timeoutMs } : {}),
          ...(values.file !== undefined ? { file: values.file } : {}),
        },
        { ensure: dependencies.ensure, mcp: dependencies.mcp },
      );
    } else if (command === "connect" && !values.client) {
      result = await (dependencies.connect ?? connectAgent)(options, {
        ensure: dependencies.ensure,
        mcp: dependencies.mcp,
      });
    } else if (command === "doctor" || command === "connect") {
      if (values["report-file"]) {
        result = await readDoctorReportFile(values["report-file"], {
          diagnosticId: values["diagnostic-id"],
          reportSha256: values["report-sha256"],
        });
        stdout.write(`${JSON.stringify(result)}\n`);
        return result.status === "complete" ? 0 : 1;
      }
      result =
        values.context ||
        values.case ||
        values.action ||
        values["resume-file"] ||
        values.handoff ||
        values["source-event"]
          ? await (dependencies.unifiedDoctor ?? runObservedDoctor)(
              {
                action: values.action,
                casePath: values.case,
                caseRoot: values["case-root"],
                context: values.context,
                evidenceRef: values["evidence-ref"],
                failureRecord: values["failure-record"],
                fix: !!values.fix,
                handoff: values.handoff,
                online: values.online,
                projectId: values["project-id"],
                result: values.result,
                resumeFile: values["resume-file"],
                sourceEvent: values["source-event"],
                userData: values["user-data"],
              },
              { signal: dependencies.signal },
            )
          : await (dependencies.doctor ?? runDoctor)({
              ...options,
              client: values.client,
              fix: command === "connect" || !!values.fix,
            });
      result = { ...result, command };
    } else {
      const desktop = await (
        command === "app"
          ? (dependencies.ensure ?? ensureDesktop)
          : (dependencies.update ?? updateDesktop)
      )(options);
      result = { command, desktop, ok: true, schemaVersion: 1 };
    }
    if (
      json ||
      values.handoff ||
      values["source-event"] ||
      ["evidence", "finish", "handoff"].includes(values.action) ||
      (agentCommand && !(command === "skills" && action === "read"))
    )
      stdout.write(`${JSON.stringify(result)}\n`);
    else if (command === "skills" && action === "read")
      stdout.write(result.content);
    else if (result.caseId) {
      stdout.write(
        `ChatCut Doctor: ${result.userResult}\nCase: ${result.caseId}\nFiles: ${result.caseDir}\n`,
      );
      const latest = result.observations
        .filter((entry) => entry.kind !== "delivery")
        .at(-1);
      if (latest?.diagnosticCases?.length && latest.nextAction)
        stdout.write(`${latest.nextAction}\n`);
    } else if (result.access === "cli") {
      stdout.write(`ChatCut CLI access: ${result.ok ? "ready" : "failed"}\n`);
      if (result.ok)
        stdout.write(
          `${result.toolCount} Desktop tools; ${result.skillCount} bundled skills. ${result.instruction}\n`,
        );
      else stdout.write(`${JSON.stringify(result.verification)}\n`);
    } else if (command === "doctor" || command === "connect") {
      stdout.write(
        command === "connect"
          ? `ChatCut Connect: ${result.ok ? "checks passed" : "issues found"}\n`
          : `ChatCut Doctor: ${result.ok ? "healthy" : "issues found"}\n`,
      );
      for (const check of result.checks)
        stdout.write(
          `${check.status === "pass" ? "OK" : "FAIL"}  ${check.message}${check.error ? ` ${check.error.message ?? check.error}` : ""}\n`,
        );
      for (const finding of result.findings)
        stdout.write(`INFO  ${finding.message}\n`);
      if (result.hostHandoffs?.length)
        stdout.write(`NEXT  ${result.hostHandoffs[0].agentInstruction}\n`);
      for (const handoff of result.hostHandoffs ?? []) {
        if (
          !result.findings.some(
            (finding) => finding.id === `restart-${handoff.client}`,
          )
        )
          stdout.write(
            `NEXT  ${handoff.displayName}: ${handoff.instruction}\n`,
          );
      }
      for (const change of result.repair?.changes ?? [])
        stdout.write(`FIXED  ${change}\n`);
      if (!result.ok)
        stdout.write(
          "Run chatcut doctor --fix for supported repairs. Sign-in and agent-session reloads may still be needed.\n",
        );
    } else
      stdout.write(
        command === "app"
          ? "ChatCut launch requested. Run chatcut doctor to check the agent connection.\n"
          : `ChatCut Desktop: ${result.desktop.action}.\n`,
      );
    if (
      values.handoff ||
      values["source-event"] ||
      ["evidence", "finish", "handoff"].includes(values.action)
    )
      return 0;
    return result.caseId
      ? ["healthy", "recovered"].includes(result.status)
        ? 0
        : result.status === "needs_user"
          ? 3
          : 1
      : result.ok
        ? 0
        : 1;
  } catch (error) {
    const result = { error: errorEvidence(error), ok: false, schemaVersion: 1 };
    if (json) stdout.write(`${JSON.stringify(result)}\n`);
    else stderr.write(`ChatCut: ${result.error.message}\n`);
    return 1;
  }
}

async function readInput(stream) {
  const chunks = [];
  let size = 0;
  for await (const chunk of stream) {
    size += Buffer.byteLength(chunk);
    if (size > 4 * 1024 * 1024) throw new Error("Tool arguments exceed 4 MiB.");
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf8");
}
