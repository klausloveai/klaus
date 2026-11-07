---
name: chatcut-widget-forms
description: |
  Show file inputs, structured questions and preview choices (文件输入/表单/预览选择) for another ChatCut skill using the current host's form controls. Load when that skill needs user input, not for general app or website form development.
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


# Widget Forms

### In-app screen recording

When the user wants to record a screen in ChatCut, emit `<record-screen/>` directly
in assistant text, outside a widget or code block, then end the reply. This is a
native action button, not a tool and not a form submit. The user's click selects
screen mode and opens the existing recorder. Explain that they choose the shared
surface and optional microphone/camera there; never claim capture started merely
because the button or picker is visible. Do not append another confirmation CTA.
After successful import, the host submits a follow-up with the recorded asset
references; verify those assets before continuing. Cancellation or save failure
is not completion. Use this tag only inside embedded ChatCut Desktop/Web chat;
external clients must guide the user to the timeline's screen recorder instead.

Host scope: the `ask_followup_questions` MCP-App widget below renders in hosts that support ChatCut form widgets (Codex). Claude Code does not render MCP-App widgets — use the Claude Code recipe below for the same moments with the same content. Single-question fields and user-language labels apply to every host. The no-file-upload restriction below applies to standalone Codex forms, not the embedded ChatCut Desktop runtime, which supports `<form-files>`.

## Claude Code Runtime (verified 2026-07-15)

Hard boundary: Claude Code does not render ChatCut MCP-App results. Never call
`ask_followup_questions` in this runtime. Use the host-native `show_widget` tool
on the `visualize` server:

1. Discover `visualize.show_widget`, then load its `read_me` with the
   `elicitation` module for the current desktop platform. Follow the current
   contract rather than examples remembered from an earlier session. Load it
   once and reuse it for the rest of the session; do not rediscover or reread it
   for each form. Read
   [references/elicit-recipes.md](references/elicit-recipes.md) only when the
   form contains visual or voice media cards. A plain single/multi/text form
   needs only the current `read_me` contract.
2. Infer first from the conversation, project state, and attachments. Ask only
   for information that is both necessary for the next step and not already
   known. Then render exactly one host-wired `<form class="elicit">` using the canonical header, body,
   group, footer, and fixed
   chrome from `read_me`. Put all related questions, media previews, and the
   single submit action in this one widget; never render a preview widget plus a
   second question UI. Claude Desktop already draws the outer `show_widget`
   frame, so keep the required `.elicit` structure but flatten only its visual
   wrapper with
   `style="border:0; border-radius:0; box-shadow:none; background:transparent"`.
   Do not remove or rename the form, header, body, or footer classes; they remain
   required for answer collection and submission.
3. Map single/multi choices to
   `.elicit-pills[data-name][data-multi]` containing
   `.elicit-pill[data-value]`; use the documented Elicitation controls for
   text and Other values. For an off-list answer, use exactly one
   `.elicit-pill[data-other]` and one adjacent `.elicit-other[data-for]`;
   `data-for` must exactly match the pill group's `data-name`. Visual, voice,
   cards remain selectable `.elicit-pill` controls with clean `data-value`
   attributes. Ordinary and visual choices use buttons. A voice
   choice uses one non-button `.elicit-pill` card that directly contains its
   title, description, and native audio player; current Claude Desktop wires
   selection by the `.elicit-pill` class rather than the element tag.
4. Submit only through `<button type="button"
class="elicit-submit">...</button>`. In Claude Code Desktop this fills the
   composed answer into the user's prompt box; it does not press Send. Use an
   honest fill-oriented action label such as "Fill editing brief".
   Never claim "sent" before that user message appears in chat. Stop the current
   turn and wait for the user to send the filled prompt.
5. Build canonical option tuples before reading media or writing HTML. This is
   a hard preflight gate; do not call `show_widget` until every visible media
   option has an authoritative `(id, display label, description/tags)` source:
   - MG style cards: reuse the active MG skill's shortlist and catalog previews,
     keeping each Design Style UUID mapped to its title. Do not restart discovery
     with `list_presets` when rendering these choices.
   - Explicit Design Style catalog cards: call `manage_design_style` with
     `action: "list_presets"` and `locale` matching the conversation language.
     Choose from that result and copy each returned `id` and `name` exactly.
     Never derive, translate, shorten, or improve a preset name from its image.
   - Voice cards: load the `chatcut-voice` skill and call `manage_voice` with
     `action:"list"`, normally `voiceType:"all"`, plus the target narration
     language and conversation locale. Choose one returned tuple per card. Keep
     the returned `voiceRef` for official voices, or `customVoiceId` + the exact
     `previewUrl` for custom voices, together with the tuple's type, localized
     name, and summary. Never create a voice name from broad traits or a
     filename.
     Every voice recommendation/selection group also includes a label-only
     clone pill and an Other pill with its adjacent text input, as shown in
     `references/elicit-recipes.md`. Keep the existing voice players in that
     same group. Map the localized clone label to the `chatcut-voice` skill's
     `clone_voice` branch; do not give clone or Other a player or a voice id.
     If either authoritative source is unavailable or times out, do not fabricate
     options and do not render a misleading form. Report the catalog problem
     concisely and retry only after the source is available.
   - Character cards: follow `chatcut-digital-human`, using `manage_character action="get"`
     for each candidate's main image URL. Keep `characterId`, name, description,
     and image together. Follow the character recipe in `references/elicit-recipes.md`.
     If the current host cannot display those images, ask a concise text question
     instead of substituting a public portrait.
6. Read [references/widget-media.json](references/widget-media.json), relative
   to this Skill's directory, only after the canonical tuples exist. Desktop
   ships this file with the Skill, including standalone MCP installations; do
   not depend on `CLAUDE_PLUGIN_ROOT` or a separately installed hosted plugin.
   The manifest resolves public media, not display names. Resolve Design Styles
   with `entries["design-style/<UUID>"]` and official voices with their returned
   `sampleMediaKey`, then resolve each entry's `path` against `baseUrl`. Preserve
   the exact key, including a voice's language suffix. Missing entries use the
   exact authoritative label without a player or image; never substitute a
   different voice, language, or style. Character images come from the character's
   own `manage_character get` result, subject to the current host's media policy.
   Claude controls the widget's resource allowlist. Do not embed provider,
   ChatCut, S3, localhost, or private/runtime media URLs in the form, including
   custom voice `previewUrl`. Keep ready custom voices as label-only choices;
   audition through a supported host media surface or ChatCut before applying.
   Never download, resize, transcode, base64-encode, print, or save form media
   or build intermediate HTML/JSON files at runtime.
7. Keep visual sets focused: show 3 strong choices by default and expand toward
   6 only when the user asks to browse more broadly or the decision genuinely
   needs that range. Keep the HTML payload small; remote media bytes must never
   enter the prompt or widget arguments.
8. Write zero event handlers and zero custom scripts. Voice audition uses a
   single non-button `.elicit-pill` card with its native `<audio controls>`
   nested directly inside. Clicking the card or its player selects that voice
   through the host's delegated `.elicit-pill` handler, while playback remains
   browser-native. Do not wrap the player in a `<button>` and do not create a
   separate selector card above it. Do not use
   `sendPrompt(...)`: live testing shows that it also only fills Claude Code
   Desktop's prompt box despite its read-me wording.
9. Do not add file input to an Elicitation form: one file group currently breaks
   handoff for every answer. Ask for missing source media outside the form by
   telling the user to drag it into the chat input, then import the readable
   local path with Desktop's `push_asset` tool.
10. In the structured collection scenarios covered by this skill, do not replace
    the combined form with `AskUserQuestion`; that modal is more interruptive and
    loses the single multi-question intake experience. This does not restrict
    normal `AskUserQuestion` use in unrelated workflows. If `show_widget` is
    genuinely unavailable, ask concisely in ordinary chat.

For media forms, minimize first-render latency by starting all independent
preparation together after this skill loads: load the current Elicitation
`read_me`, read this skill's media recipe and manifest, and fetch only the
authoritative catalogs actually needed by the form. Call
`manage_voice action="list"` only for voice cards; call `manage_design_style list_presets`
only for explicit catalog-preset pickers. MG reference choices reuse the active MG
workflow's fetched shortlist and details.
Do not serialize independent reads, inspect unrelated skills, probe media URLs,
or create intermediate files. Reuse all loaded local contracts and catalogs for
later forms in the same session. Once the required option data is available,
`show_widget` is the final call.

Claude Elicitation file attachments are not ChatCut project imports. When the
attachment is available as a readable local path, use Desktop's `push_asset`.

Use user-language readable copy for `data-name` and `data-value`; the host puts
those strings directly into the filled answer line. Keep preset ids and voice
ids out of those attributes, and retain a label-to-id map from the
tool results in context. The host formats the answer as `<header> details —
<data-name>: <value> · ...`, with comma-separated multi-select values. Once that
line appears as a user message, map each visible label back to the internal id
from the candidate list and continue without asking the same questions again.

Immediately before `show_widget`, audit every media card in both directions:
the visible label must map to exactly one authoritative tuple. Its media must
resolve from that tuple's bundled manifest key for Design Styles and official
voices, or equal that character's main image URL from `manage_character get`
when the current host permits it. Custom voices have no inline player in this
public-media recipe. Use a text question for characters whose images cannot be
shown. A label copied from a different ID, an invented alias, a shortened official
voice name, or media chosen before the source lookup is a failed preflight.
Fix the tuple instead of rendering it.
