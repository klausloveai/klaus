# Supported recovery paths

Preserve the original failure and selected target first. Evidence categories
guide the next action; they never replace message/code/cause/stack or prove a
root cause by themselves. Use the existing case, resume link and safe native
read contract throughout.

| Observed condition                                                                                            | What Doctor can do                                                                                                      | One user/support next step                                                                                                                                     | Verification and reporting                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Native CLI conclusively says the selected manual registration is absent; no opt-out, plugin owner or conflict | Offer the existing authorized missing-registration repair and retain its rollback                                       | If normal host authorization or reload is still required, complete only that step in the same host/scope                                                       | Registration is not recovery. Read Hosted `list_projects` or Desktop `read_project` with the bound project, and save the real result                                   |
| Host actually reports missing/expired authorization                                                           | Retain the exact authorization error; keep account, endpoint and configuration scope                                    | Use the selected host's normal authorization flow; the user performs login                                                                                     | Never import tokens, repeat completed login because of stale logs, or treat `auth_status: o_auth` as token validity. Recheck natively afterward                        |
| Authorization completed but this chat's tools were reported missing                                           | Follow [authorized connection, unavailable tools](authorized-no-tools.md); try the current safe read first when exposed | If the current tool really remains absent, use one verified normal reconnect/continuation step and the existing case handoff                                   | A new session stays `new_session`. Tool catalogs, old manifests and another chat's success cannot prove this chat recovered                                            |
| Selected connection is disabled or plugin-managed, or another target conflicts                                | Preserve the setting and explain why the limited repair is inapplicable                                                 | For a plugin-owned entry, inspect its normal management/connection state; for an intentional disablement, leave it disabled unless the user requests otherwise | Do not add a competing registration, repoint environments, clear caches or upload against an opted-out target                                                          |
| Tool explicitly needs a connected editor/browser or reports a browser-job timeout                             | Preserve the actual project/job IDs and whether a job may still run                                                     | Keep/open the same authorized project in the existing editor tab when required; inspect an existing job's supported status rather than replaying it            | Browser cookies and MCP authorization are separate. Do not switch projects or infer that no execution occurred; use the normal safe Doctor read to verify connectivity |
| Timeout, failed lookup, busy or generic transport error without a supported cause                             | Retain the original failure and unmatched/unknown state                                                                 | Continue available, relevant read-only checks; when no effective next step remains, explain facts and the specific evidence gap                                | Do not delete locks or retry edits/generation. A safe read can verify current availability but cannot identify the old cause                                           |
| Native body-decoding error plus independently observed invalid HTTP framing                                   | Follow [HTTPS inspection evidence and recovery](https-inspection.md)                                                    | The user/IT checks vendor updates/repair and performs any permitted comparison; Doctor does not operate security software                                      | Distinguish a controlled framing test, suspected inspection involvement and actual affected-terminal recovery. Preserve failures and the same-case native recheck      |

Give `needs_user` only with the exact remaining human step. A failed actual
native read can be saved through `record-recheck` with `outcome: failed` and
`needsUser: true` and its specific `nextAction` when that step is supported by
evidence. Record an actual operator action before the read in `precedingAction`.
Keep the original
error in that artifact; a prose handoff alone does not set recovery status.
If the evidence only supports an unknown cause, save `unresolved` and the
missing evidence. Continue evidence-driven read-only investigation when it can
distinguish causes. Do not invent a cause or generic fix. A specific supported
repair requires its matched rule and exclusions; useful investigation does not
require a confirmed root cause.

Save diagnosis, actual operations and fresh rechecks before delivery. Upload
only under the applicable explicit authorization. Preserve failed delivery and
its original error locally. A relay ACK is not final storage: retrieve the
selected diagnostic ID and report hash and use the existing offline reader to
verify every fragment. Internal acceptance IDs/hashes must be registered and
excluded from natural-user samples; do not upload customer logs as test data.
