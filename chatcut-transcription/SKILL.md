---
name: transcription
description: Use for ChatCut Desktop built-in and ACP Agent tasks involving source transcript or ASR corrections, captions, subtitles, layout, animation, translation, transcript search, speech cleanup, or transcription readiness.
---

# Transcription

Desktop may already have started transcription when media became available. Actual project transcript and request state is the authority; explicit transcription remains available when needed. Read `browse_assets` or `inspect_asset` for the source identity, current transcript, timing capability and any active request. An empty accepted transcript, a missing transcript, a failed attempt and a source with no audio are different facts.

When the user's task needs words, choose the relevant sources and obtain missing transcripts. `trigger_transcript` automatically selects the recognition service based on language by default and uploads the full source's first audio stream. It returns promptly; `track_progress target:"transcription" action:"wait"` awaits that attempt while editing remains available. Reads and caption visibility changes never start work. A caption task can compose these operations without asking the user to command each stage.

Choose transcription based on the task, not merely because an asset was imported. Request it for speech needed for captions, transcript search, or speech-led editing. Skip known instrumental music, sound effects, silent visuals and unrelated sources. Reuse accepted transcripts and wait for existing requests instead of starting duplicates. Use `trigger_transcript` for cloud speech recognition; do not install or run Whisper or another local ASR engine. If the user requires local-only processing, explain that the supported recognition service needs an upload and do not start it. Existing user-supplied normalized transcripts may still be imported through `manage_transcript action:"replace"`; this is not an alternative recognition workflow.

An explicit `replace:true` requests reanalysis or replacement. Accepted text remains usable while work runs; the writer retains recovery files and rejects late results after source or text changes. `manage_transcript` corrects the accepted source content directly. No separate readiness flag or caption regeneration step is needed: the project writer and file watcher update derived views. Existing authored caption overrides and translations keep their own editorial meaning.

## Adding captions and choosing a style

Apply Plain directly for a simple “add captions” request, and apply concrete
requested edits directly. When the user asks to see, compare, or choose caption
styles, load `widget-forms` and present its caption preview cards for the current host before
changing the project. For an explicit request for several custom styles, author
that many valid ordinary-caption candidates using `caption-style-id` and
`caption-style` JSON; optional `caption-base-preset-id` starts from a built-in.
Use actual transcript/caption context and the intended language, track, or Card.
Leave the project unchanged until the chooser is submitted. Other allows typed
customization. The submitted hidden context retains exact normalized Desktop
Memory settings and executable application calls; apply those settings and target
rather than interpreting the visible label. Desktop Card targets support appearance;
wrapping/page limits need the intended track or all captions. Ordinary custom
candidates clear token motion and progressive reveal on their recorded target.
Custom candidate previews do not
create durable presets or generation assets, and do not support arbitrary CSS,
MG templates, or unsupported animations. For generated animated caption templates,
follow the template workflow below.

## Caption refinement

Finish source corrections before polishing the derived display. Read the transcript against the speech and use `manage_transcript` FIX for confirmed ASR mistakes; preview a multi-command batch first. Preserve the speaker's meaning and do not invent missing words. `set_card_text` changes only viewer-facing caption text, so it is suitable for display wording or a translated Card, not a substitute for correcting source transcription. Finish intended clip edits as well: source changes rebuild affected caption tracks and can replace their direct Card edits.

Read `read_captions` with `words:true` and use the returned Card and token IDs. Improve sentence grouping with `split_card` and `merge_cards`, then adjust spacing and readable scale with caption style fields and `set_card_layout`. Check long phrases and short isolated words in the real video rather than assuming a maximum line length gives good phrasing. Card/token start and end times are microseconds; frame queries and frame-based placement require conversion using the project frame rate.

Batch a shared baseline style first, then re-read Cards: style changes can regroup them and invalidate old Card IDs. Use `edit_captions {action:"batch",edits:[...]}` for up to 100 ordered synchronous edits with one commit; a failing edit writes nothing. Batch independent Card layouts and styles, including multiple bindings to one template. For example, each binding is `{action:"set_card_style",cardId,style:{template:{path,runtime}},mode:"merge"}`. Do not carry old Card IDs across a regrouping style edit in the same batch. For splitting, pass `{cardId:card.id,beforeTokenId:card.words[n].id}` from a fresh `read_captions` result, choosing a word after the first. Transcript correction locations and caption split boundaries are different contracts.

Choose the few Cards whose spoken meaning warrants emphasis. Use ordinary caption styles for the baseline, and reference a reusable Motion Graphic template to those Cards through `set_card_style` and `style.template` when a custom treatment serves the request. When `delegate_task` is available, delegate source creation with it, request `{action:"start",agent:"motion-graphic",output:"caption-template",name,task}`. The specialist receives the focused caption-template implementation skill. Request real caption Cards, not fixed title text. Supply representative short and long caption text, the spoken meaning, reading hierarchy, Card dimensions and timing. For expressive animation, describe how positions, rhythm and motion support that meaning; size and word highlighting alone do not satisfy a custom animated-template request. Reuse one source across distinct actual sentences, with properties for variations, while ordinary captions stay readable. Keep reusable source in a project-owned persistent location, including the project workspace. Wait for the returned `template:{path,runtime}` and pass it as `style.template`, optionally adding properties. Resume that same taskId with concrete feedback for template revisions, including after completion. Do not register a caption template in the asset library or call `push_asset`; ordinary MG asset creation/validation is not a prerequisite. The `template` action in `edit_captions` is only the built-in preset catalog. If delegation is unavailable, use the current surface's existing direct caption-creation capability; do not claim a specialist ran, and when the surface cannot produce the requested treatment, explain the actual limitation and what was completed.

For Remotion, the exported root receives `{ item }` and reads `item.props.caption`; caption is not a root component prop. For HTML, `mount` initially receives empty `props`; retain new values in the controller's `update({ props })` and read `props.caption` when rendering. The caption context includes `text`, `visibleText`, `words`, `frame`, `time`, `fps`, `geometry`, and Card/track IDs. Caption `start` is zero, `end` is Card duration in seconds, and word `start`/`end` are seconds relative to the Card; these are not the microseconds returned by `read_captions`. Use the actual supplied text and timings. An optional standalone preview may have no caption context. A fallback can make that preview possible, but it is not required for binding and does not verify real caption rendering.

A minimal Remotion binding (the final design still needs styling and real Card review):

```jsx
export default function CaptionTemplate({ item }) {
  const caption = item?.props?.caption;
  return <div>{caption?.text ?? "Template preview"}</div>;
}
```

Template overrides can be applied to the caption item, a track, or a Card. `template:null` explicitly chooses ordinary captions even if a parent has a template. To restore a Card's inheritance, replace its style with the remaining intended fields and omit `template`; simply omitting it from a merge leaves the old override in place. Read results retain the native source path and runtime.

Inspect representative **bound Cards** over the actual footage, including word changes and Card boundaries. A standalone MG preview or a successfully saved source reference does not validate caption rendering. Verify source corrections, grouping, spacing, text visibility, subject clearance, and emphasis across the complete clip. Reopen/read the saved project to check persistence, and inspect the requested export before claiming the refined video is finished.

## Caption Translation

Read `read_captions` first. Its `captions.tracks` includes hidden tracks and
identifies originals and translations with `role`, `contentLanguageCodes`, and
`sourceTrackId`. A null track-level `languageCode` does not mean the original
text is missing; use `contentLanguageCodes` to identify its language.

To restore existing original or bilingual subtitles, pass the hidden track's
returned `showAction` directly to `edit_captions`. To hide a language, use
`action: "track"` with its exact `trackId` and `visible: false`. Use `enable`
first only if `captions.visible` is false. Verify the resulting track visibility
with `read_captions`.

Use `edit_captions` action `translate` only to create or update a translation
in a language the user requested. Do not use translation to restore visibility,
invent a target language, or create a temporary translation and hide it.
Enable captions if none exist, then pass the requested target language in `json`:

```json
{
  "action": "translate",
  "json": "{\"languageCode\":\"es\",\"mode\":\"bilingual\"}"
}
```

This creates or updates a separate translation track. `mode` defaults to
`bilingual`; use `translation` to hide the source captions and show the translation.
Optional `trackId` in the payload selects a source caption track or its source
media track by id/prefix; omit it to translate visible source tracks and sources
with a visible translation in the target language.
Use `set_card_text` for individual wording corrections after translation.

## Progress and recovery

Use the actual attempt's progress and error. A wait timeout does not imply that execution failed; cancelling the wait does not cancel transcription. A failed or interrupted request can be started explicitly again. Opening a project only reattaches work that has a matching existing service job; it does not create a new paid request from an old pending flag. Transcript publication detects changed sources and concurrent text edits; stale results never replace accepted content.

`read_captions` includes source coverage, including when no caption item exists. Use that to distinguish missing/stale transcription from an empty recognized result or a selected clip outside speech. Do not infer absence of speech from missing text.

If captions read back as empty, check the source-time range of the timeline clip. A transcript can be ready while the current visible clip starts before the first spoken word; add or trim a clip so the transcribed source words fall inside the timeline range, then extend/update the captions item duration if needed.

Use the raw tools when you need finer control:

- `track_progress` with `target: "transcription"` for status/wait.
- `find_transcript` for query-based transcript lookup.
- `read_captions` and `edit_captions` for caption display edits.
- `manage_transcript` action `fix` for source transcript repair.
- `clean_script` for mechanical timeline playback cleanup of fixed fillers and batch pauses after transcript-ready media is on the timeline.

When a transcript-ready request becomes an editorial talking-head edit, follow the public-safe talking-head workflow in shared `talking-head-guide`. In short: use `clean_script` only for mechanical cleanup, then use Script (`read_script` -> edit `timeline.md` -> `apply_script`) for semantic repeated-take, silence, filler, or coherence edits, and verify the resulting script rather than trusting tool success alone.
