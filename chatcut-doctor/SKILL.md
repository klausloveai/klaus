---
name: doctor
description: Diagnose ChatCut Desktop installation, external-agent MCP connections and managed editing skills, then apply requested repairs or app updates. Use when ChatCut tools or skills are missing, duplicated, stale or unable to connect.
---

# ChatCut Doctor

Use the ChatCut CLI for installation and diagnostics; Desktop remains the source
of the editing runtime, agent connections and bundled skills. For ordinary video
editing with working tools, continue the editing task.

Run `chatcut doctor --json`. When the command is missing, use
`npx --yes @chatcut/cli doctor --json`. Check `--help` when the installed version's
surface differs. If the package is unavailable, use the
[official Desktop installation instructions](https://chatcut.io/desktop-plugin)
and report that the CLI could not be obtained; do not substitute another npm
package or hosted MCP server.

Choose the operation that matches the user's request:

- Open or install Desktop: `chatcut app` (bare `chatcut` is equivalent).
- Diagnose one host: `chatcut doctor --client codex --json` or
  `chatcut doctor --client claude-code --json`.
- Repair a requested connection/skill problem: `chatcut doctor --fix --json`.
  When the request names one client, select it with `--client codex` or
  `--client claude-code`. Existing authorization to fix the problem is sufficient;
  diagnosis alone does not authorize repair.
- Update Desktop when requested or needed within an authorized repair:
  `chatcut update --json`. Close the app through its normal flow when required;
  preserve ongoing work. App update and npm CLI update are separate operations.

Read the individual checks and original errors. Installation, a running app,
host registration, readable managed skills, MCP discovery and a successful tool
call are different evidence. Doctor probes a fresh local MCP connection through
`initialize`, `tools/list` and `get_active_project`; cached discovery alone does
not establish success. An empty active project is valid.

Also inspect the current agent conversation's available `chatcut_desktop` tools
and skill catalog. A successful fresh probe cannot prove that this conversation
loaded them. After changes, use the host's supported reload or start a new
conversation, then verify a read-only tool call and access to the relevant
ChatCut workflow skill. Do not claim to have observed unavailable host state.

For repairs, let Desktop own connection setup and skill synchronization. It
respects explicit disconnections and checks the selected agent home. Preserve
user-edited or foreign skills and report their exact paths. Matching skill names
or similar text do not prove that copies are interchangeable: different hosts
can require different variants. Only obsolete, unchanged manifest-owned copies
are eligible for automatic removal. Do not clear an entire skill root, host
configuration, plugin cache, credentials or project directory.

When running inside a managed ChatCut Agent, its project-pinned MCP and built-in
skills are authoritative. Diagnose that project/session first; do not repair
external host integrations to fix an unrelated in-app tool failure.

Re-run diagnosis after repair. Report the failed stage and original cause,
changes actually completed, the final checks, preserved ambiguous paths and any
remaining sign-in, update or conversation-reload action. Sign-in happens inside
Desktop; never collect credentials. macOS/Windows policy or an unsupported
headless/Linux environment is a concrete limitation, not permission to bypass
publisher validation.

Research and consequential adoption decisions are recorded in
[sources](references/sources.md); read them when changing the diagnostic model.
