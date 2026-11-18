# Local Doctor case contract

Use a CLI with `doctor --context` support. In a source checkout:

```sh
node <checkout>/apps/cli/bin/chatcut.mjs doctor --context <selected.doctor-context.json> --failure-record <original.mcp-failure.json> --case-root <private-results> --json
node <checkout>/apps/cli/bin/chatcut.mjs doctor --case <caseDir> --context <selected.doctor-context.json> --action repair --json
node <checkout>/apps/cli/bin/chatcut.mjs doctor --case <caseDir> --context <selected.doctor-context.json> --action record-recheck --result <native.doctor-recheck.json> --json
node <checkout>/apps/cli/bin/chatcut.mjs doctor --case <caseDir> --action status --json
node <checkout>/apps/cli/bin/chatcut.mjs doctor --resume-file <conversation.doctor-resume.json> --action native-recheck --json
```

The agent writes dedicated inputs from observed host facts. Do not pass a host
configuration, credential file, whole conversation or guessed field as input.

For successful authorization followed by missing tools, use the
[host continuation guidance](authorized-no-tools.md). Its append-only companion
notes retain completed steps and separately scoped browser evidence; they do
not replace a native recheck or change the CLI's recovery status.

## Local candidate entry and follow-ups

### Product-generated independent handoff

Desktop's `handoff` action creates a hash-named `.doctor-handoff.json` for the
authenticated selected case. It contains its immutable original, task text when
available, a bounded evidence directory and relevant guidance; private host log
collections are excluded. The product's copy action supplies its exact path and
hash. A local path requires this host's real file access; use the supported
attachment route otherwise, rather than asking the user to find logs.

The prepared helper can read it while the target editing MCP is unavailable:

```sh
<this-skill>/scripts/run-doctor.sh --handoff <product-file.doctor-handoff.json> --json
<this-skill>/scripts/run-doctor.sh --handoff <same-file> --evidence-ref original --json
```

Windows uses `run-doctor.ps1 -Handoff <file> -EvidenceRef original`, with an
existing `-Runtime` when necessary. `--evidence-ref` accepts only references from
the directory, including `observation:<id>`, `artifact:<id>` and
`guidance:recovery-paths`; it never accepts arbitrary filesystem paths. The reader
checks the file hash, immutable case identity and selected artifact boundaries.
Detailed reads require the original local case files; a copied snapshot alone
does not grant access to files or another account's case.

Reading material does not prove that another AI received it or that its arbitrary
conversation lifecycle was observed. Desktop records its actual managed
investigation lifecycle automatically under existing reporting settings; the
independent reader does not manufacture an external AI completion or cloud receipt.

### Preparation and supported runtimes

The developer prepares a new self-contained candidate directory with:

```sh
node apps/cli/scripts/prepare-doctor-candidate.mjs --destination <new-absolute-directory> --runtime <existing-Node-or-ChatCut-Electron>
```

The default host is Codex. For Claude Code, prepare a separate new directory
with `--host claude-code`; its `SKILL.md` explicitly declares `chatcut-doctor`
so Claude's own `/doctor` remains available. Do not use the generic Codex
candidate unchanged as a Claude Skill.

Preparation copies only this Skill and the CLI's dependency-free sources. It
does not install globally, copy a runtime, copy credentials or change any host
registration. The receipt records source HEAD, dirty state and file hashes.
The Desktop resource staging script also includes this CLI with the Skill.
Unprepared source Skill copies retain the direct source CLI route above.

For a local Codex installation, copy the complete prepared directory to a new
`<workspace>/.agents/skills/doctor` and open that workspace in Codex. Keep the
CLI, wrappers, references and receipt together; there are no runtime imports
from the source checkout. Natural requests use ordinary Skill discovery.
Codex also supports selecting a discovered Skill with `$doctor` or its Skills
picker; the folder does not register a bare `/doctor` command. Verify the
installed host's discovery and actual invocation before claiming acceptance.
For Claude Code, install the complete candidate in a new
`<workspace>/.claude/skills/chatcut-doctor` directory. Desktop synchronization
uses `<CLAUDE_CONFIG_DIR>/skills/chatcut-doctor` (the default home is `.claude`).
The Claude-specific candidate and Desktop-rendered Claude Skill both declare
`name: chatcut-doctor`. Use `/chatcut-doctor` for this local entry;
the host also has its own Doctor. A ChatCut plugin may namespace its entry;
verify the actual Skill name and invocation before advertising it. Existing Desktop-managed or plugin-managed
Skill installations retain their own ownership and names; do not overwrite
them or add a competing user-wide copy. This local preparation path does not
publish or update a hosted plugin.

On Windows the user/agent can run a prepared candidate without a global Node:

```powershell
& '<candidate>/scripts/run-doctor.ps1' -Context '<selected.doctor-context.json>' -FailureRecord '<original.mcp-failure.json>' -ResumeFile '<conversation.doctor-resume.json>'
& '<candidate>/scripts/run-doctor.ps1' -ResumeFile '<same.doctor-resume.json>' -Action native-recheck
```

`-Runtime` may explicitly select an existing ChatCut Electron executable. The
wrapper runs it in Node mode and waits for its exit; it does not open the app.
It can also resolve the executable from the selected Desktop launcher's last
invocation line. Hosted-only users without Node or a compatible existing
runtime still need a supported distribution; no portable binary or published
npm command is established by this candidate. On Unix use `run-doctor.sh` and
`CHATCUT_DOCTOR_RUNTIME` or an existing Node22+.

The resume link binds case ID, original hash and target fingerprint. Existing
links cannot be overwritten with another incident. `native-recheck` resumes
that immutable target; no new context file or original capture is required.
Codex verifies the selected native registration and launcher metadata first,
then makes and saves a safe native app-server call in a new ephemeral session,
with zero model turns. Desktop uses `read_project` with a real `projectId`;
Hosted uses `list_projects`. Native failures retain their raw code, message,
cause/data, stage and available RPC ID namespace. RPC IDs are not HTTP request
IDs or Responses tool call IDs. A failed capture/save cannot close the case.
The selected Desktop registration can be verified without editor IPC, including
when the existing bridge serves local projects headlessly. This is not evidence
that a closed editor window or original user conversation has recovered.

For directly registered targets the helper disables unrelated plugin/app catalog
startup only in its native child process. Plugin-managed targets keep their native
catalog. It closes its own pipes after the bounded host shutdown so background
catalog work cannot keep the reporting CLI open. Persistent host settings are unchanged.

Claude Code still needs the read in its actual conversation and the actual
output recorded with `record-recheck`. The local program saves `needs_user`
when it cannot perform that read; it does not use configuration/health output
as a replacement. Native Skill catalog discovery, direct wrapper execution and
AI selection are separate acceptance checks. Missing legitimate model-host
authorization blocks only the relevant AI/host acceptance, not offline checks.

### Automatic external AI conclusion

For a writable case, begin the investigation with an actual `check` and retain
that operation's `eventId` from its `investigation_result` observation as the
`attemptId`. This is an operation anchor for this investigation, not a host turn
ID. Continue using the same case and collect actual observation references.
Before your normal final reply, including when unresolved or needing the user,
write a small dedicated `.doctor-finish.json` and call:

```sh
<this-skill>/scripts/run-doctor.sh --resume-file <same.doctor-resume.json> --action finish --result <answer.doctor-finish.json> --json
```

An existing `--case <caseDir>` can replace `--resume-file`. On Windows use
`run-doctor.ps1 -ResumeFile <file> -Action finish -Result <file>`. The statement is:

```json
{
  "schemaVersion": 1,
  "caseId": "actual-case-id",
  "targetFingerprint": "actual-target-fingerprint",
  "originalSha256": "actual-original-hash",
  "attemptId": "actual-first-operation-event-id",
  "outcome": "unresolved",
  "assessment": "The original connection still fails; the available evidence does not establish why.",
  "stopReason": "No further supported check can distinguish the remaining causes.",
  "nextStep": "Ask the responsible IT team to inspect this connection.",
  "observationIds": [],
  "guidance": []
}
```

Use the actual conclusion; `outcome` is `completed`, `needs_user` or `unresolved`.
`nextStep` may be `null` when none is known. Include IDs of relevant actual case
observations since the anchor; the anchor's own observations are included
automatically. Referenced guidance uses `{ "ref": "guidance:recovery-paths",
"sha256": "actual-directory-hash" }`. Optional `model`, `provider` and
`modelVersion` are self-reported only when actually available; do not guess.
Input is limited to 32 KiB, with bounded text and references. Do not supply
identity/backend, `recovered`, `repairPerformed`, credentials or a transcript.

The helper records this as `agent_statement`, separate from actual checks,
repair facts and verified case status. It saves and automatically queues the
useful conclusion under existing reporting settings, using the bound Desktop
sender or selected Hosted relay. No full-report upload checkbox is needed.
Exit zero means the statement was recorded, not that the problem recovered or
remote storage was verified. Inspect `automaticResultDelivery` or the existing
Desktop delivery status for pending/disabled/unavailable outcomes.

Reuse the exact statement and anchor on retry: the stable event ID is
idempotent. Different content for an already-finished anchor is rejected; a new
investigation starts with a new actual operation anchor. Read-only handoff
snapshots do not grant write or account access. If this host lacks a writable
case/helper, state that conclusion delivery is unavailable. A killed host or
failed model may never call `finish`; prior operation facts remain automatically
recorded, and the product does not claim it observed the whole external turn.

## Target context

Use an absolute path ending `.doctor-context.json` with `schemaVersion: 1` and:

| Field        | Source and accepted values                                                                                 |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| `surface`    | Failed tool's actual surface: `desktop` or `hosted`                                                        |
| `host`       | Current native host: `codex` or `claude-code`                                                              |
| `hostHome`   | Effective absolute `CODEX_HOME` or `CLAUDE_CONFIG_DIR`, including the host's documented default when unset |
| `cwd`        | Actual absolute project/working directory                                                                  |
| `scope`      | Native registration scope: `user`, `project`, `local`; Codex and Desktop require `user`                    |
| `serverName` | `chatcut_desktop` for Desktop; actual `chatcut` or `plugin:chatcut:chatcut` for Hosted                     |
| `management` | `desktop`, `manual`, or `plugin`; Desktop requires `desktop`                                               |
| `enabled`    | Observed boolean, or `null` when unavailable                                                               |
| `platform`   | Optional current `win32`, `darwin`, or `linux`; cannot operate a different platform                        |

Hosted also uses `endpoint` (actual registered URL or `null` when unavailable)
and `cliPath` (resolved absolute native executable). Approved destinations are
ChatCut API domains and loopback; arbitrary URLs are rejected. Optional
`logLocations` selects known absolute `sqlite`, `text`, `app`, `stderr` paths
for this host. No default scan of another home is permitted.

Desktop also requires `profile` (`local`, `beta`, `production`, `custom`),
`userData` and its exact `launcher` path. The authenticated IPC must answer for
that launcher, profile and selected host home. Never paste the launcher's
capability or auth-token contents into an input/report. Doctor does not start
or install an instance to satisfy these checks. Optional Desktop `cliPath`
selects the actual native Codex executable for an automatic recheck;
`projectId` binds the actual full Desktop project ID. If initially unavailable,
`--project-id` may select it for the first native recheck; later reads preserve
that project. Optional `backendOrigin` must
come from that launcher's actual backend origin and is checked again before
explicit telemetry delivery; without it, the report remains local.

## Original failure

Use `.mcp-failure.json` or `.doctor-failure.json`. Preserve the original exposed
error with `schemaVersion: 1`, `source`, `serverName`, `occurredAt` (or `null`),
`error` including message/code/type/cause and available call/session IDs. The
Hosted collector also accepts its newer original-response evidence fields.
For Hosted the exact allowed top-level keys are `schemaVersion`, `source`,
`serverName`, `occurredAt`, `conversationId`, `callId`, `operation`, `requestId`,
`httpResponse`, `error`. `source` is `host_tool_result`, `host_runtime_event`, or
`captured_stderr`, matching the actual evidence. Put a real host conversation
ID in `conversationId`, not `sessionId`; unavailable IDs may be null or omitted.
Do not put an app-server RPC request ID into `requestId` (which identifies the
original server HTTP request). For example, copy the actual values into:

```json
{
  "schemaVersion": 1,
  "source": "host_tool_result",
  "serverName": "plugin:chatcut:chatcut",
  "occurredAt": null,
  "conversationId": null,
  "callId": null,
  "operation": "list_projects",
  "error": {
    "message": "<actual original message>",
    "code": "<actual code or null>"
  }
}
```

An omitted file produces an explicit unavailable original; a retry's output
must not be relabelled as that original. Secrets are redacted at capture.

## Native recheck

Use `.doctor-recheck.json` with:

```json
{
  "schemaVersion": 1,
  "source": "native_host_tool_result",
  "host": "codex",
  "serverName": "chatcut",
  "targetFingerprint": "<from the existing case>",
  "sessionBoundary": "same_session",
  "sessionId": "<actual ID or null>",
  "nativeCallId": "<actual ID or null>",
  "nativeCallIdKind": "<actual ID namespace or unavailable>",
  "observedAt": "<actual observed timestamp or null>",
  "operation": "list_projects",
  "outcome": "success",
  "result": "<replace with the actual complete native result object>"
}
```

This is a shape reference, not success evidence. `outcome: failed` retains the
real `error`/result. For `needsUser: true`, include a specific `nextAction`.
Optional `precedingAction` records the operator's actual action before this
read, without inferring a change from a successful result. Both fields are
nonempty text of at most 4096 characters and are retained in case observations
and authorized uploads. `new_session` must be stated
when applicable. The recorder validates identity and safe-read response shape,
copies the sanitized artifact into the case and verifies its hash before
reporting recovered. It cannot prove an agent's statement of provenance.

The program reports `repairPerformed` separately from recovery: `true` means
an actual Doctor change was reported, `false` means no Doctor repair occurred,
and `null` means an attempted repair lacks a conclusive change receipt. A
partial repair remains `true` even if a later verification fails. A native
read never becomes a Doctor repair; record any real user/IT or fixture action
in `precedingAction` instead. Legacy repair observations without change evidence
remain unknown. Status and authorized uploads retain this distinction.

## Delivery and offline reconstruction

`upload` is explicit and separate from repair/recovery. A failed delivery never
replaces the incident's original or successful native read. Intentional
disablement blocks upload. No production fallback is selected. The local
candidate supports Hosted and explicitly selected Desktop telemetry delivery;
Desktop keeps its local report when its backend origin is unavailable.

For an authorized telemetry query's downloaded rows, use:

```sh
node <checkout>/apps/cli/bin/chatcut.mjs doctor --report-file <rows.json-or-ndjson> --diagnostic-id <ID> --report-sha256 <SHA256> --json
```

`reportFileSha256` hashes local report file bytes; delivery `reportSha256`
hashes the canonical wire content used for fragments and the reader selector.
These hashes intentionally describe different encodings.

The reader is offline and returns `complete`, `incomplete` or `invalid`. It
handles nested/map attributes, stringified JSON attributes, legacy nesting and
projected fragment columns. Missing fragments are not successful storage proof.
