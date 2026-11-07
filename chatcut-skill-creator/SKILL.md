---
name: chatcut-skill-creator
description: |
  Save or update a validated ChatCut editing process as a reusable Workflow Skill (保存流程/复用剪辑技能), only when the user explicitly asks. Not for general agent skills or ordinary edits to the current video.
user-invocable: false
---

## Desktop connection in an external host

Use this procedure only for a ChatCut route compatible with the user's goal.
With working Desktop tools, continue. If tools are missing/disconnected, first
reconnect without installing Desktop:

`npx --yes --prefer-online @chatcut/cli@latest connect --no-install --json`

Use existing authorization for connection and ordinary recovery. Honor actual
host permission requirements without adding a repeated installation approval.
Never remove --no-install to accommodate an older CLI: unguarded connect may
install Desktop. An unsupported flag does not establish that Desktop is absent.
Read-only doctor, an installed trusted launcher and supported host connection
mechanisms can establish availability while the published CLI lacks the guard.

Only an actual Desktop installation requires a host permission click for:

`npx --yes --prefer-online @chatcut/cli@latest connect --allow-install --json`

Explain that this may download/install the signed production Desktop, open it
and connect CLI access. Submit the exact command through the host's supported
permission prompt so the user clicks approval. Auto-allow, standing grants,
bypass mode and a never-approve host cannot supply this installation click.
Do not add permission rules or skill tool pre-approvals. Without a supported
prompt, show the manual command without running it. If installation approval is denied,
respect it; do not retry installation through another tool, installer or flags.
The flag records approval already obtained; it cannot itself prove permission.
Never remove --allow-install or bypass publisher validation to work around a
CLI rejection. Preserve credentials, native-host opt-outs and ownership/path
boundaries during targeted configuration repair.

Check exit code, ok and the original result. Preserve the original error,
diagnose recoverable package, transport or inspection failures within existing
authorization, and inspect current state before retrying an uncertain mutation.
Resume the original task after recovery; continue independent authorized work
when a step remains blocked, honoring any refusal and upload restrictions.
A successful connection proves CLI access separately from native host loading.
Use skills read <name>, tools describe <name> --json and tools call as needed;
preserve projectId and follow actual sign-in/service permission results.
Before any paid generation, obtain a current supported quote for the exact
parameters and explicit approval covering that price and scope. Reuse an
existing approval that still covers the operation; do not invent pricing or
resubmit an uncertain paid job without inspecting its task and billing state.


# ChatCut Skill Creator

This skill turns a proven ChatCut editing approach into a user-owned Workflow Skill.

A Workflow Skill should help the agent repeat an editing method later. It should not be a chat
transcript, a frozen tool-call recipe, or a bundle of fragile internal parameters.

## Decide Whether to Save Now

Use judgment from the current conversation and project state.

- Save only from a completed, user-approved, or clearly validated workflow.
- If the user is only describing a desired skill, rough idea, or unfinished process, do not save yet.
  Help them run the workflow or collect enough detail first.
- If key details are missing, ask focused follow-up questions until the reusable workflow would be
  accurate. Do not optimize for one-turn creation.
- If the edit is just starting, still experimental, or has no stable outcome yet, tell the user the
  workflow can be saved after the edit is finished or the successful approach is clearer.
- Before calling `manage_skill`, recap the proposed skill name, use case, workflow, principles, and
  checks, then ask the user to confirm. Save only after that confirmation, unless the user already
  confirmed those exact details.
- If the user is correcting an existing skill, update that skill instead of creating a duplicate.

Do not change the timeline, assets, captions, design style, or generated media while creating a
skill. This workflow is for capturing knowledge, not editing the video.

## What to Capture

Capture durable editing intent and process:

- When this skill should be used, in the user's own editing language.
- Inputs the agent should look for, such as source footage type, target platform, target length,
  brand/design style, references, script, product info, or examples.
- The repeatable workflow steps, from understanding the source through final QA.
- Preferences the user validated, such as pacing, structure, caption style, B-roll taste, MG density,
  tone, checkpoints, export expectations, or recurring wording.
- Rules that prevent common mistakes for this user's workflow.
- Quality checks that the agent can apply before saying the edit is done.
- Lightweight reusable references only when useful. Stable official or product-managed ids are OK
  when they are meant to travel across projects, such as design styles, templates, voice presets,
  or other curated presets.
- Do not save project media asset ids in user skills; describe reusable asset taste or source
  expectations in normal editing language instead.

Avoid capturing:

- Low-level tool parameters, transient item ids, segment ids, clip ids, timestamps, or implementation
  details that may change as ChatCut evolves.
- Project media asset ids or heavyweight asset references. They are usually project-scoped and may
  not resolve in future projects.
- Private chat dumps, credentials, unrelated personal context, or one-off project details.
- Claims that the workflow always performs better than alternatives unless the user actually
  validated that.
- Overly broad trigger language that would make the skill fire for unrelated edits.

## Skill Shape

Create a standard Skill package, then save it with `manage_skill` using the transport available
in the current host. Desktop or ChatCut sandbox agents can use a workspace directory; hosted
Codex / Claude plugin agents send the package contents inline without a ChatCut sandbox.

Minimum package:

```text
SKILL.md
```

Optional lightweight files, only when they reduce clutter or add reusable detail:

```text
references/...
examples/...
scripts/...
```

Use one `SKILL.md` for simple workflows. Add `references/` for deeper guidance, `examples/` for
compact good/bad examples, and `scripts/` only for lightweight helpers that complement ChatCut
rather than duplicate its editing, download, transcode, or export tools.

In `SKILL.md`, use normal Claude skill conventions:

- Frontmatter `name` and `description`.
- A clear H1 title for the user-facing skill name.
- Short sections for when to use it, needed inputs, workflow, preferences/rules, and final checks.
- Links to optional files, so they load progressively only when useful.

These are guidance lenses, not a required schema. Include only what makes the workflow stable and
reproducible.

## Writing Guidelines

- Name the skill after the user's reusable outcome, not the current project title unless the project
  title is the recurring format.
- Keep the description short enough to scan in the skill list.
- Use normal editing language. Prefer "cut the strongest hook first" over internal command names.
- Preserve useful style/template concepts, but leave room for the current ChatCut tools to evolve.
- Be specific enough to guide future work, but not so specific that the skill only fits one old
  source video.
- If there are several distinct workflows in the conversation, save the one the user asked about; do
  not merge unrelated workflows into one vague skill.

## Save the Package

After the user confirms the proposed workflow, choose one transport. Keep the complete text package
under 1 MB, with `SKILL.md` at the root and optional files only under `references/`, `examples/`, or
`scripts/`. Use relative package paths; do not include absolute paths, parent-directory paths,
symlinks, or media.

**Desktop / ChatCut sandbox with a workspace:** write the package to a draft directory, then save:

```text
manage_skill({
  action: "create_from_directory",
  sourceDirectory: ".chatcut/skill-drafts/<slug>",
  name: "<user-facing skill name>"
})
```

**Hosted Codex / Claude plugin without a ChatCut sandbox:** send `packageFiles` as an object
mapping each relative path to its complete text contents. No ChatCut filesystem step is needed:

```text
manage_skill({
  action: "create_from_directory",
  name: "<user-facing skill name>",
  packageFiles: {
    "SKILL.md": "<complete SKILL.md text>",
    "references/checklist.md": "<optional reusable checklist text>"
  }
})
```

Pass either `sourceDirectory` or `packageFiles`, never both. The action names stay
`create_from_directory` and `update_from_directory` for either transport.

For an existing skill, call `manage_skill({ action: "get", agentSkillId })` first. Use the returned
skill ID for later edits: loading another user's shared skill can return your own independent copy.
Catalog skills remain read-only; fork one only when the user wants to change it, then update the
returned copy. Otherwise, create an additional copy only when explicitly requested.

- With a workspace, edit the full package materialized by `get`, or recreate it in the draft
  directory. Call `update_from_directory` with the returned `agentSkillId` and that `sourceDirectory`.
- Without a ChatCut workspace, edit the full returned `packageFiles` object and call
  `update_from_directory` with the returned `agentSkillId` and the complete `packageFiles` object.
  Keep unchanged references, examples, and scripts: this replaces the package, not individual files.

## After Saving

After a successful save, reply with a concise plain-language recap:

- Skill name
- When to use it
- Core editing steps
- Important preferences/rules/checks
- Where to reuse it: in ChatCut, select saved Skills from the book icon below the chat input. In a
  connected host, ask the agent by name so it can find and load the Skill with `manage_skill`.

If the user corrects anything later, update the same skill.
