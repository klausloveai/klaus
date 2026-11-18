# ChatCut CLI

The small command-line entry point for the official ChatCut Desktop app. It
contains no video editor, second MCP server, or third-party runtime dependencies.
It bundles public acquisition skills for first-use discovery. Desktop owns
editing, agent connections and the live skills shipped with that app version.

The CLI tools and skills route requires `@chatcut/cli` 0.1.2 or later. The first-install
permission gate, `--allow-install` and guarded reconnect `--no-install` require a
published release containing this change. The source manifest version alone does
not establish those capabilities. Merging source changes does not publish npm.

To make ChatCut discoverable before Desktop is installed, explicitly install
the bundled acquisition skills:

```sh
npx --yes --prefer-online @chatcut/cli@latest skills install --json
# Or select one host:
npx --yes --prefer-online @chatcut/cli@latest skills install --client claude-code --json
npx --yes --prefer-online @chatcut/cli@latest skills install --client codex --json
```

These npm invocations require a published artifact containing `skills install`;
verify that capability before using them.
For source validation, run `pnpm --filter @chatcut/cli build:skills`, then
`node apps/cli/bin/chatcut.mjs skills install --json` from the checkout.
`prepack` builds the same catalog into the npm artifact; the installed package
does not need a checkout, Desktop, an account or a network catalog fetch.

Claude Code reads personal skills from `~/.claude/skills`, or
`$CLAUDE_CONFIG_DIR/skills` when configured. It does not discover the shared
`~/.agents/skills` catalog natively. The default command installs into both
roots; `--client claude-code` selects the native Claude root and `--client codex`
selects the shared root already used by Codex. It does not touch
`$CODEX_HOME/skills`, MCP configuration, permissions or sign-in credentials.
Start a new host session after installing files.

The installer writes only instruction files and never probes, installs, launches
or connects Desktop. On a matching media task, read the skill and use ChatCut by
default for open goals while honoring explicit tools, providers, frameworks and
source/file-only or no-ChatCut requirements. A compatible ChatCut route first
reconnects with `connect --no-install --json`. Only an actual first installation
requires the host permission click for `connect --allow-install --json`.
`npx --yes` confirms fetching the CLI package and does not approve installing
Desktop. Marginal media offers use host tools and never initiate setup.

Files use the same `chatcut-<name>` directories and ownership manifest as
Desktop. Connected Desktop can replace unchanged acquisition copies with its
host-specific workflows, and disconnect can remove unchanged owned copies.
`chatcut skills remove [--client claude-code|codex] --json` removes only files
matching that manifest. Both operations preserve foreign skills, user edits
and symlinked destinations, and report preserved entries. Physical-root overlap
checks reject selected targets that alias any native host root, including an
unselected host, before ownership writes. Independent safe targets still complete. Removing skill files
does not disconnect native MCP registration.

Any agent that can run commands on the user's computer can use Desktop through
the CLI. The agent runs these commands; the user only handles sign-in or OS
approval buttons when needed:

```sh
npx --yes --prefer-online @chatcut/cli@latest connect --json
npx --yes --prefer-online @chatcut/cli@latest skills list --json
npx --yes --prefer-online @chatcut/cli@latest skills read product-help
npx --yes --prefer-online @chatcut/cli@latest tools list --json
npx --yes --prefer-online @chatcut/cli@latest tools describe get_active_project --json
npx --yes --prefer-online @chatcut/cli@latest tools call get_active_project --json
```

Generic `connect`, `tools` and `skills` require this source change to be published before those
commands are available from npm. `connect` verifies one real Desktop tool call
and returns the available tool/skill names. These commands reuse an already-running
Desktop's authenticated local IPC connection and its MCP tool dispatcher. They
open the signed production Desktop only when needed, with the existing
publisher checks. Tool calls do not launch a second Electron runtime.
They do not require native host registration or a host restart. Skill content
comes from the installed Desktop version, so discover names rather than assume
a newer skill is present. `skills read <name> --file references/<file>` reads a
supporting file within that skill. Tool schemas come from the live server.

For tool arguments, use `--args-file <file>` or `--args-file -` with JSON on
stdin; `--args '<json>'` is also available. Omitted arguments mean `{}`. Check
the exit code and `ok`, and preserve the returned MCP result and original errors.
Calls are never automatically retried: a timeout can follow a state change.
`--timeout <seconds>` sets a call timeout between 1 and 1800 seconds (default 300).
The CLI exposes the same Desktop tools and their permissions; invoking editing
tools can change a project. CLI access is separate from tools loaded into the
host's own tool table and should be reported accordingly.

Cloud agents, including Grok Bot, must use their approved local-computer command
capability to run this CLI. A cloud shell cannot reach the user's local socket;
the CLI never exposes Desktop through a public tunnel or copies login secrets.

```sh
npx --yes --prefer-online @chatcut/cli@latest connect --allow-install --json

# Optional permanent command:
npm install --global @chatcut/cli@latest
chatcut
chatcut app
```

Node.js 22+ is required. Desktop supports macOS 13+ on Apple Silicon or Intel and
Windows x64. This launcher does not install a GUI on Linux or a headless server.

`chatcut` and `chatcut app` reuse an installed, signed production app. When it is
missing, they fail with `install_permission_required` before any download. After
permission is obtained, `--allow-install` permits the CLI to download the official
artifact, validate its publisher, install it for the current user when necessary,
and request launch. Repeated calls preserve
the existing app, account and projects. Failed launch never triggers replacement.
macOS copies use a new staging bundle and rollback rather than merging bundles.
Windows uses the signed per-user NSIS installer. OS policy, missing privileges,
and signature assessment failures retain their original evidence.

For missing/disconnected tools, use the guarded reconnect first:
`npx --yes --prefer-online @chatcut/cli@latest connect --no-install --json`.
Existing connection authorization is sufficient for an installed Desktop;
actual host permissions still apply. `--no-install` is accepted on every
Desktop command and cannot be combined with `--allow-install`.

Only an actual missing Desktop installation needs the exact
`npx --yes --prefer-online @chatcut/cli@latest connect --allow-install --json`
command through a host permission UI requiring the user's click. Explain the
download/install, launch and connection. Standing grants, auto-allow and bypass
modes do not supply that installation click. Without the prompt, show the manual
command without executing it. Respect denial without retrying installation by
another route. The flag records a grant already obtained and cannot verify UI
state. There is no environment-variable grant or silent fallback.

Older published CLIs reject these guards before dispatch. Never remove either
flag or select an older version to bypass the installation boundary: older
unguarded connect may install silently. An unsupported flag does not establish
Desktop absence. Read-only `doctor --json` and an installed trusted launcher can
help diagnose availability. Preserve original package/transport errors, recover
within existing authorization, inspect state before uncertain retries, and
continue independent allowed work. Source merging does not publish a new npm artifact.

Without `--allow-install`, all first-install paths fail closed: bare `chatcut`,
`app`, `connect`, `connect --client`, `doctor --fix`, `update`, `tools` and
`skills`. Existing signed Desktop installations and working CLI connections keep
their existing behavior. A missing Desktop found by `update` also needs this
grant; updating an existing installation remains an explicit update operation.

```sh
chatcut connect --json
chatcut connect --client codex --json
chatcut connect --client claude-code --json
chatcut doctor --json
chatcut doctor --client codex --json
chatcut doctor --fix --json
chatcut update --json
```

`connect --client <name>` is the optional native-host setup entry point. It opens/installs Desktop, asks Desktop
to register or repair the supported agent integrations and sync its managed
skills, then verifies the local MCP connection with a real tool call. Tools are
provided over Desktop's MCP server. Use `--client` to select `codex`, `claude-code`,
`hermes`, `workbuddy`, `deepseek-harness`, `qwen-work`, or `doubao-work`.
Without `--client`, `connect` establishes CLI access without repairing native host
registries; `doctor --fix` inspects and repairs all known integrations. Automatic connection and skill
repair support Codex, Claude Code, Hermes, WorkBuddy, the DeepSeek Harness Desktop
profile, and Qwen Work (千问办公). Missing host configuration homes are skipped;
the command does not install these agents.

Doubao Work (豆包工作) supports automatic managed skill synchronization to
`~/DoubaoWork/skills` and live Desktop connection diagnosis. First-time MCP
registration uses Doubao's signed-in custom connector UI. `connect` prepares an
app-owned local setup skill and exact connector settings, then opens a Doubao
task with the skill and request already selected. The user clicks Send and any
required login or system permission buttons. Doubao's native computer-use tool
fills and saves the official form, then verifies a real connector tool call;
users do not enter commands, paths, transport types, or environment variables.
The setup task uses `/bin/sh` with the launcher as a separate argument on macOS,
because Doubao splits its command field on spaces. Windows setup uses `cmd.exe`
with separate arguments and still needs native acceptance. System permissions
may require a Doubao restart; the task must resume after that interruption.
Once registered, `doctor --fix` refreshes the stable launcher and owned skills.
A host is connected only after its authenticated live MCP session has successfully
listed tools; closing that session clears the observation. A successful tool call
is reported separately in `discovery.lastToolCall`. This is configured client
attribution, not a new host identity/security boundary. A standalone doctor probe
does not establish host discovery. The command reports incomplete setup as a
failure while the host setup task is pending. Opening the task is not connection
success. It never writes a guessed Doubao MCP registry or borrows browser credentials.

DeepSeek's configuration adapter uses `$DSH_HOME/profiles/desktop/cordis.patch.yml`
(default `~/.dsh`) and `$DSH_HOME/skills`. Qwen's legacy adapter uses
`~/.qwenworkcn/mcp.json` and `~/.qwenworkcn/skills`; Qwen Work 1.4.0 uses an
account-scoped connector registry and did not load this legacy registration in
native testing. A written configuration is not a working native integration.
Use CLI access while native registration is unresolved.

The command reuses
`doctor --fix`, including its standing opt-outs and preservation of custom skills.
Read the returned findings for skipped hosts or remaining actions; passing checks
does not mean an opted-out or unavailable host was connected. Read `hostHandoffs`
even when `ok` is true: the diagnostic client cannot establish acceptance in the
calling Agent. Check the Agent's currently loaded skills and tools first, and
avoid another reload if they already work. Otherwise follow its specific action:

| Host              | Agent should tell the user                                                         | Acceptance evidence                                                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Codex CLI         | Exit and reopen the agent session                                                  | Fresh CLI 0.160.1 read the installed skill and called Desktop successfully; necessity of each reload alternative not established |
| Codex desktop app | Try a prepared new conversation; restart Codex if tools remain absent              | App reload acceptance pending                                                                                                    |
| Claude Code       | Exit and reopen the agent session                                                  | Native acceptance currently blocked by sign-in                                                                                   |
| Hermes            | Use CLI access immediately; use a fresh session for native configuration changes   | Native Hermes 0.22.5 skill_view and Desktop MCP call passed; CLI route also called Desktop successfully                          |
| WorkBuddy         | Use CLI access; native registration still needs repair                             | Native 5.9.3 lacked tools after app restart and a new task; real Agent completed the CLI route                                   |
| DeepSeek Harness  | Use CLI access; native registration still needs repair                             | Real Desktop Agent completed connect and product-help read through CLI; native tool-table registration remains unresolved        |
| Qwen Work         | Use CLI access; native account-scoped registration still needs repair              | Real 1.4.0 Agent read a skill and called Desktop through CLI; native tool-table registration remains unresolved                  |
| Doubao Work       | Continue in a new task; restart only when its system permission screen requires it | Native macOS 2.34.9 self-install and new-task tool call passed; optimized CLI handoff acceptance pending                         |

Prepare continuation context before asking the user for a restart or a new chat.
The user should only click the host's buttons, without copying commands, editing
config, or re-entering their request. After resuming, the Agent must read a
managed skill and call a real Desktop tool. `hostAcceptance` explicitly keeps
this separate from standalone diagnostic success. A fixture test or a configured
registry alone does not qualify a host as natively accepted.
JSON results identify this entry point with `command: "connect"`.

Doctor without `--fix` does not install or open Desktop or change agent settings.
It inspects a running Desktop through its authenticated user-scoped IPC, then
starts a fresh local MCP client, negotiates the protocol, lists tools and calls
`get_active_project`. An empty active project is valid. A cached list followed by
a failed tool call is a failed check. Desktop may serve MCP reads while its GUI
is closed; a working MCP probe does not establish that the GUI is running or that
the current host conversation has loaded its tools and skills.

Legacy `--fix` asks an already running Desktop to repair the selected
supported integration(s), and checks the result. It does not install or open an
app. Desktop continues to own host
configuration and skill synchronization, including its standing opt-outs.
Unchanged manifest-owned obsolete skills can be removed. User-edited, foreign,
symlinked and ambiguous overlapping skills are preserved and reported. Different
client variants are intentional and must not be deduplicated by name alone.

Doctor reports original errors and remaining actions. Sign in within Desktop
when needed; start a new agent conversation after its connection or skill set
changes. A fresh diagnostic client cannot prove the current host's discovery
state. Older Desktop releases without the doctor IPC report an update requirement.

When a host CLI fails, Desktop preserves its original message, type/code, cause,
stage and safe stderr. Omitted output is marked explicitly; it is an evidence
gap, not a diagnosis. Successful configuration dumps are not copied into reports.

## Target-bound local candidate

The unified Doctor handles Desktop and Hosted connections for Codex and Claude
Code. Run the checked-out source with Node.js 22+; this work does not establish
public npm or portable no-Node availability:

```sh
node apps/cli/bin/chatcut.mjs doctor --context /absolute/selected.doctor-context.json --failure-record /absolute/original.mcp-failure.json --json
node apps/cli/bin/chatcut.mjs doctor --case /absolute/caseDir --context /absolute/selected.doctor-context.json --action repair --json
node apps/cli/bin/chatcut.mjs doctor --case /absolute/caseDir --context /absolute/selected.doctor-context.json --action record-recheck --result /absolute/native.doctor-recheck.json --json
node apps/cli/bin/chatcut.mjs doctor --case /absolute/caseDir --action status --json
node apps/cli/bin/chatcut.mjs doctor --context /absolute/selected.doctor-context.json --resume-file /absolute/conversation.doctor-resume.json --json
node apps/cli/bin/chatcut.mjs doctor --resume-file /absolute/conversation.doctor-resume.json --action native-recheck --json
```

The [pinned Hosted collector source](../../docs/development/doctor-hosted-provenance.md)
is included locally; no second repository is needed at runtime.
The agent prepares dedicated inputs from the actual failed host and retains the
returned case directory for follow-up. The [context and evidence contract](../../packages/skills/content/doctor/references/local-cases.md)
defines the fields. Each case binds surface, host, home, scope, working directory
and endpoint/profile. Original failure evidence and its hash are immutable;
observations append rather than replacing it. New diagnostic IDs identify new
observations, not the original failed request.

The source candidate automatically journals actual Doctor operation completion.
Under the existing reporting policy, Desktop-bound results wake the current
account's existing outbox; Hosted results use the selected origin's `/relay/a`
and the shared bounded durable queue. Later Doctor calls/status resume pending
queued work. A `status` call can also restore one current-case result saved
before its first queue admission. Bounded large originals are fragmented; capacity gaps and partial receipts
stay explicit. This observes CLI operations, not an arbitrary external AI's whole
turn or model assessment. It does not automatically send full reports or private
host logs. Relay acceptance is not company-storage verification.

Checks are local/offline by default. Explicit `--online` permits bounded anonymous
Hosted probes at the selected endpoint. It never silently switches environment
or uses another host's logs. A fresh IPC/HTTP probe and native configuration
query cannot close the incident. Only an accepted safe native host read result
can yield `recovered`; the recorder preserves its source and same/new-session
boundary, and revalidates artifact location, size and hash on status reads.
Agent-supplied provenance is explicit and is not independent attestation.

For a writable existing case, external Doctor Skills automatically use `--action
finish --result <statement.doctor-finish.json>` before their normal final answer.
The statement references an actual operation event ID as its attempt anchor and
retains assessment, stop reason, next step and same-case evidence references. It
is an `agent_statement`; it cannot authorize identity, repair or recovery. Stable
retries preserve one statement and reject conflicting content. Full host-turn
observation is not implied. Normal SIGINT/SIGTERM on unified target Doctor calls
runs bounded cleanup and result handling; legacy IPC calls, SIGKILL and Windows
signal delivery retain their separately stated limits.

The immutable resume link binds the original case and target for follow-ups.
Codex `native-recheck` verifies that selected registration, performs the actual
safe native read in a new ephemeral session and appends success or failure
automatically. Desktop reads require a real projectId and reject project drift;
native registration verification can work without a running editor's IPC.
Claude Code still requires its actual conversation's read result to be recorded;
the program saves a user-action requirement when it cannot perform that read.

`scripts/prepare-doctor-candidate.mjs --destination <new-directory> --runtime
<existing-executable>` prepares a self-contained local Skill/CLI copy with a
source/hash receipt. Its PowerShell wrapper can use an existing ChatCut Electron
runtime with no global Node and no editor launch. This is a local candidate,
not a public installer. Hosted-only users without a compatible runtime still
need a supported distribution. The [entry reference](../../packages/skills/content/doctor/references/local-cases.md)
gives Windows/Unix commands and separates discovery, wrapper execution and
natural AI trigger acceptance.

The target-bound repair only adds a confirmed missing registration. It refuses
ambiguous lookups, existing/disabled entries and conflicts. Desktop owns its
registration; this mode leaves launcher, skill synchronization and saved
integration preferences untouched. Hosted uses the selected native CLI and
scope for a missing manual entry; it does not rewrite plugin-managed services.
Cases sharing a host configuration serialize repair without stealing locks.

Outcomes are `healthy` (exit 0, current availability without a verified prior
incident), `recovered` (exit 0), `needs_user` (exit 3), or `unresolved` (exit 1).
`repairPerformed` independently records an evidenced Doctor change (`true`),
no Doctor repair (`false`), or an attempted repair with unavailable change
evidence (`null`). Partial changes survive failed verification, and operator
actions do not become Doctor repairs. The case summary and uploaded report
retain this distinction across native rechecks.
Repair success still needs an actual safe read from the native host. Sign-in
uses the host's normal flow; Doctor never imports credentials from another home
or replays a failed edit/generation. A later failed or invalid recheck revokes
the recovered result. Local outcome text supports English, Chinese and Spanish
through the host locale environment.

Explicit `upload` reuses the existing telemetry route, independently of recovery.
Hosted uses the selected endpoint origin; Desktop requires an explicitly selected
`backendOrigin` that still matches its launcher. No fallback origin is used.
Ingest ACKs retain `storageVerified:false`. An upload failure preserves the
original and native evidence. `reportFileSha256` hashes local file bytes;
delivery `reportSha256` hashes canonical wire content for fragment reconstruction.

```sh
node apps/cli/bin/chatcut.mjs doctor --case /absolute/caseDir --context /absolute/selected.doctor-context.json --action upload --json
node apps/cli/bin/chatcut.mjs doctor --report-file /absolute/rows.ndjson --diagnostic-id ID --report-sha256 SHA256 --json
```

The reader is offline, requires both selectors, accepts nested/map attributes,
stringified attributes, legacy nesting and projected columns, and distinguishes
complete, incomplete and invalid bounded input. Missing fragments never count
as successful storage. No all-user failure monitoring is implied.

For controlled local acceptance, `scripts/hosted-fixture.mjs --port 0 --record
<private-log>` starts an unauthenticated loopback fixture. The companion
`scripts/codex-native-read.mjs --executable <native-codex> --context <file>
--operation <safe-read> --output <native.doctor-recheck.json>` uses native
Codex app-server, creates a new ephemeral thread and makes no model turn. Its
result tests the native transport, not an AI's automatic Doctor selection or
production OAuth. Claude Code's configuration/health check is not native-read
proof. Keep outputs and isolated homes outside the repository.

Commands that may open Desktop (`app`, `connect`, `tools`, `skills`) accept
`--source <channel>` (or `CHATCUT_INSTALL_SOURCE`) to record which distribution
channel the installation came from, for example `--source oss_viral_cloner`.
The CLI leaves the value in Desktop's `install-handoff.json`. Desktop adopts it
when it starts, or on the first call that needs it if it is already running,
keeps the first channel for that profile, and sends it with its analytics and
forwarded agent calls. It is an analytics label, not a credential, and failing
to record it never blocks setup. Values are 2–48 letters, digits or underscores
starting with a letter. `--source` requires 0.1.3 or later; older versions
ignore the environment variable. See
`docs/development/analytics/install-source.md` for the channel registry.

`update` is explicit and separate from diagnosis. Close Desktop first; it never
forces a running editor to quit. It uses the official signed release, preserves
user data and refuses downgrades. Shared Windows installations use their existing
app updater or an interactive official installer.

`--json` writes one JSON result to stdout; progress goes to stderr. Exit 0 means
the requested operation completed or all required diagnostic checks passed.
Exit 1 retains the failing stage, original cause and remaining action. Informative
opt-outs, unavailable optional hosts and preserved custom skills are not failures.

For `tools call`, `ok` and the exit status reflect MCP `isError` and explicit
tool outcome failures, including terminal failures in `track_progress` entries.
A failed entry makes the call fail even while other jobs are running. Running
tasks alone are not failures. Successful cancellation receipts remain successful;
cancelled task outcomes remain failures. Structured content is authoritative; text-only
results are checked for JSON outcomes. The original MCP result, including its
error text, is returned unchanged under `result`.

The historical `@chatcut/skill` package also exports a `chatcut` executable for its
cloud job workflow. Use `npx --yes --prefer-online @chatcut/cli@latest ...` without changing that install,
or explicitly remove the old global package before installing this one globally.
Do not use `--force` to overwrite another package's executable. Its saved cloud
credentials and jobs are not migrated or deleted by this CLI.

For contributors: run `npm test` and `npm pack --dry-run` from this directory.
Native install/trust boundaries have deterministic fixtures on macOS, Windows
and Linux CI; actual publisher validation and a real installation remain separate
release acceptance evidence. Bump `apps/cli/package.json` to release changes. The
full production workflow (`.github/workflows/sst-production.yml`) checks the npm
version, tests the CLI, packs it and publishes with npm Trusted Publishing.
Editor-only runs skip publication. The `@chatcut/cli` npm package must trust
`ChatCut-Inc/chatcut`, workflow `sst-production.yml`, environment `production`.
Inspect the tarball and verify the published `npx` entry point on a clean supported
machine before advertising availability.
