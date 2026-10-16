---
name: weekly-review
description: >-
  Weekly SETUP retrospective ("设置复盘") that reviews Klaus's recent Cowork sessions and
  proposes what — if anything — should be updated in his Claude setup: his global
  Instructions, his memory files, or his skills. Trigger on: "设置复盘", "/设置复盘",
  "setup review", "跑设置复盘", "weekly review", or a scheduled weekly reminder. (This is
  the SETUP review — its sibling is /项目复盘, which reviews the project portfolio.) It READS
  the last ~7 days of sessions, classifies every new signal (recurring calibration,
  role/scope change, new workflow, new operational fact) into the right container,
  and returns an APPROVAL-GATED proposal list. It NEVER auto-edits the global
  Instructions (those live in the Cowork app UI — Klaus pastes them himself); it may
  apply memory/skill changes to disk only on Klaus's explicit per-item approval.
---

# weekly-review — 周度复盘 & setup-update proposer

Goal: turn a week of ad-hoc corrections into durable updates, and decide whether the
global **Instructions** should change — **without ever silently rewriting them.**

## Core principle (the routing rule)

For every signal found, ask: **does it apply to ~everything Klaus does AND is it stable
(changes only every few months)?**
- **Yes → Instructions candidate** (rare; needs evidence across MULTIPLE sessions).
- **A "how I want this done" rule for one task domain → memory (feedback) or a skill.**
- **A repeatable multi-step workflow → a skill** (new or update).
- **A volatile operational fact (team roster/size, caseload, projects) → NOT
  Instructions.** Point it to the Master sheet / project memory instead.

## Steps

1. **Set the window.** Default = last 7 days (ask if Klaus wants a different span).
   Get today's date from the environment context.
2. **Gather sessions — READ TRANSCRIPTS, not just snippets.** `list_sessions` +
   `search_session_transcripts` only give titles/snippets and WILL make you miss most
   of the week (learned 2026-07-11: a snippet-only pass badly under-caught). For a real
   review, read the raw transcript bodies: the session `.jsonl` files live in
   `~/.claude/projects/-Users-klaus/` (filename = session id). Stream them and extract
   Klaus's own `type:"user"` messages that are short (<~400 chars = real instructions,
   not pasted docs) and carry calibration cues (下次/以后/记住/改成/不要/应该/格式/默认/
   每次/规范/统一/别/错). Files can be huge — skip lines >20KB, filter, don't load whole.
3. **Cross-reference existing memory FIRST.** Read `MEMORY.md` and skim the memory
   files. MOST of a busy week is already captured in-session (Klaus has 70+ memories).
   The review's job is the ~20% that slipped + the rare Instructions-level shift — do
   NOT re-propose what's already in a memory/skill. Say "already captured" and move on.
4. **Extract signals** into four buckets:
   - 🔴 **Instructions candidates** — stable + universal preferences repeated across
     sessions (e.g. a new default output habit; a genuine role/scope shift).
   - 🟡 **Memory / calibration** — a format or tone rule Klaus gave (does it belong in
     [[draft-check-skill]] or a memory feedback file?).
   - 🟢 **Skill** — a workflow he did manually more than once, or an existing skill
     that needs a tweak.
   - 🔵 **Operational state** — team/caseload/project changes → route to Master sheet /
     project memory, explicitly NOT to Instructions.
5. **Vet the 🔴 candidates hard.** Only promote to an Instructions change if seen
   across **multiple sessions/tasks** and clearly stable. Read
   `current-instructions.md` (the mirror in this skill folder) and draft the **exact
   before→after diff**. If a candidate is really operational or single-domain,
   down-route it and say so.
6. **Present the proposal — FIXED FORMAT (Klaus set 2026-07-11):**
   - (a) **Numbered four-color summary** — one concise page, each item numbered and
     tagged 🔴/🟡/🟢/🔵 with `批准 / 跳过`, most important first. Klaus approves by
     replying with numbers (e.g. "1、2、4"). Keep it short; no filler.
   - (b) **For every 🔴 Instructions change, render a highlighted before→after diff**
     via `mcp__visualize__show_widget` — the NEW full text with **added spans on a green
     background** (`--bg-success`/`--text-success`) and **removed spans struck through on
     red** (`--bg-danger`/`--text-danger`), unchanged text plain; collapse long unchanged
     paragraphs to "(unchanged)". A small legend (added / removed / unchanged) on top. So
     Klaus sees at a glance what grew vs shrank before pasting. (See the week-1 render as
     the reference pattern.)
7. **Apply on approval:**
   - 🟡 memory / 🟢 skill → **edit the files directly** (these are on disk).
   - 🔴 Instructions → **do NOT write anywhere automatically.** Output the ready-to-
     paste block; Klaus pastes it into the Cowork app (personal preferences). Then
     update `current-instructions.md` to match so the next review diffs correctly.
   - 🔵 operational → note where it should go; update if it's a memory/sheet Klaus
     approves.
8. **If nothing rises to the bar, say so plainly** — "本周无需更新 instructions;X 已
   固化进 memory/skill"。 A quiet week is a valid result; don't manufacture changes.

## Guardrails

- **Never auto-edit the global Instructions.** They live in the app UI; Klaus always
  pastes. Permanent gate, not just the first few weeks.
- **Evidence bar for Instructions:** repeated across ≥2 sessions/tasks and stable. One
  offhand comment is a memory note at most, not an Instructions change.
- **Don't double-store.** If a rule fits an existing skill/memory, update that — don't
  mint a duplicate. Prefer updating [[draft-check-skill]] for drafting calibrations.
- **No fabrication.** Only propose from what the sessions actually show; if unsure,
  list it as "to confirm with Klaus," not as a finding.
- Keep the report tight and skimmable (Klaus's standing preference: direct, concise).

## Two-tier system this fits into
- **Daily = in-the-moment capture** ("记住这个" during work → straight to memory/skill).
- **Weekly = this review** — the synthesis pass that also judges Instructions.
See [[draft-check-skill]] for the drafting-house-style self-check that captures format
calibrations as they happen.
