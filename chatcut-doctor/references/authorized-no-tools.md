# Authorized connection, unavailable tools

Use this path when registration or OAuth completed and ChatCut tools were
reported missing. Reuse the case and resume link. Preserve the original failure
and target. A chat predating registration or an old manifest without tools does
not establish its current capabilities or require a new chat.

## Keep the evidence scoped

| State          | Evidence to retain                                                                         | What it does not establish                                                     |
| -------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| Registration   | Selected service, endpoint, enabled state, host home and scope                             | Authorization or tools in this chat                                            |
| Authorization  | Actual CLI/host completion or authenticated server observation, time and source            | A matching original chat or a successful tool call                             |
| Tool discovery | Actual host manifest/startup evidence with chat/session identity when exposed              | `list_projects` success; server `tools/list` alone does not identify this chat |
| Native call    | Selected host's actual `list_projects`, or Desktop `read_project` with the bound projectId | Recovery of an earlier chat when this is a new session                         |
| Web login      | Browser/tab identity, observed URL, time and available session response status             | MCP bearer validity; a different tab's login state                             |

Keep unavailable IDs and timestamps null. An authenticated `initialize` or
`tools/list` from the same OAuth client establishes only that associated server
connection. Another thread's ready event, a later diagnostic, or temporal
proximity cannot supply the original chat's identity. Absence of authenticated
`tools/call` records does not establish that no unauthenticated request occurred.

Save nonsecret follow-up facts in a new `host-followup-<UUID>.json` beside the
case's `original.json`. Include `caseId`, `targetFingerprint`, `originalSha256`,
`source: "agent_supplied_followup_notes"`, observed times, source artifact
references and the five states above. For each state record its status,
chat/session or tab identity when known, and evidence limits. Retain completed
steps and one next action. Never overwrite prior notes, edit the original or
manually insert these notes into `observations`; the CLI does not consume them
as recovery evidence. No-tool observations are not fabricated failed tool calls.

## Read in the current host chat first

Check the tools currently available in the actual selected host conversation.
If its safe read is available, call Hosted `list_projects` once, or Desktop
`read_project` with the bound actual projectId. Do this before asking for a
refresh, new chat or another login. Do not create a separate app-server session
to substitute for this check. A historical missing-tool manifest, registration
time or stale browser URL cannot establish that this current call is unavailable.

On success, save the actual result with `record-recheck` into the same case,
using `same_session` and its actual conversation identity when applicable.
Keep the earlier failure and completed steps. If no recovery change was made,
say so; the recovery mechanism remains unknown unless separately established.
Do not attribute this success to Doctor, an automatic reload, a restart or a
new chat, or erase the earlier missing-tool observation. Web login remaining
unknown does not downgrade a successful MCP call. No further refresh, login or
new chat is needed for this successful check.

When only a sanitized original-machine receipt is available, retain its source
and session association alongside the original case. Do not reconstruct the
full native result from a project count or truncated project IDs to satisfy
the recorder. Keep the full result on its original machine. Preserve unavailable
MCP call/request IDs as unavailable; Codex outer orchestration/item IDs belong
to their own namespace, not the MCP request ID.

## Continue only when the current read is unavailable or fails

If the current safe tool really is unavailable, preserve that current discovery
observation. If a call fails, save its actual error and cause. These current
observations, rather than the older manifest, determine the next step.

If registration and authorization already completed, preserve them. Do not
loop through OAuth, reinstall the plugin, clear caches or change credentials.
If the selected running host exposes a verified normal MCP refresh/reconnect
control, use it once within the existing target and permissions. Do not assume
an app-server method is available in the user's installed UI, or launch another
app-server and describe its result as this chat's refresh.

When a user-controlled continuation is needed, report `needs_user` and state
that the current chat remains unverified. Save this required action in the
companion notes; it does not set the CLI's recovery status. Give one continuation:
open a normal new chat in the same host using the already configured service,
and paste a short handoff in the user's language containing:

> Continue Doctor case `<caseId>` using `<resume-file>` and `<caseDir>`. Registration
> and authorization already completed `<actual evidence references>`; do not
> repeat them. Keep the selected service, endpoint, home and scope. Call
> `<Hosted list_projects / Desktop read_project with the bound projectId>` once
> using this chat's native tool, then save the actual result to this case with
> record-recheck. Report this as a new-session result; the earlier chat remains
> unverified. If the tool is absent, retain this chat's startup/discovery error
> and stop with needs_user.

Fill placeholders from the case; do not ask the user to author JSON. State
which completed steps are observed and which are only reported. Do not create
a new chat or restart the user's application without authorization. For a
remote personal machine without access, this handoff is guidance, not an
executed refresh or successful recovery. If its Doctor case/resume link or
target context is unavailable, preserve the existing incident identifier and
mark those fields unavailable until that machine supplies them. Do not invent
its host home or create a replacement local-machine case for it.

After the real call, use the existing `.doctor-recheck.json` contract and
`record-recheck`. Save failures too, retaining their error and session boundary.
Only the selected host's actual read supports recovery of that tested session.
Configuration health, server tool lists, independent HTTP requests and the
local `native-recheck` helper's separate session cannot verify the original
chat. If the new chat still lacks tools, preserve its observed discovery/startup
failure and stop; do not resume the login/install loop.

## Check the browser separately

MCP OAuth bearer credentials and editor browser cookies are separate. A login
page does not invalidate a successful native call, and a successful native
call does not prove that a browser tab is logged in. Record the actual tab and
current state before attributing an old `/authenticate` observation to it.
Different simultaneous tabs are not a redirect sequence. No current browser
tab or session receipt means Web login is unknown, not a current login failure.

Once tools work, reuse the existing project/editor link or `get_editor_url`
handoff supported by that host. Use ChatCut's existing controlled editor-link
authentication flow; never build a bearer-to-cookie bridge, copy credentials,
or construct/extract an `editor-boot-token` URL. Follow the tool's presentation
instructions and retain only a clean link in diagnostic notes. Recheck the
selected browser tab separately; if it still needs normal web sign-in, report
that web action while preserving the native call's successful result.

The official [Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp)
and [app-server documentation](https://learn.chatgpt.com/docs/app-server) describe
configuration, OAuth, reload and tool calls separately. Their current API
capabilities do not establish refresh support in a particular installed host.
