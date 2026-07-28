---
name: project-review
description: >-
  Work-portfolio retrospective ("项目复盘") that reconciles Klaus's project registry
  (the private "project management" Google Sheet) against his recent Cowork sessions —
  catches stalled/dropped projects, adds new ones that appeared in sessions, re-ranks by
  his north-star goals, and recommends push / pause / kill. Trigger on: "项目复盘",
  "/项目复盘", "project review", "跑项目复盘", or a scheduled reminder. Two modes: DAILY
  (light pulse — what moved / what stalled / anything new) and WEEKLY/Monday (full re-rank
  + push-pause-kill). It is APPROVAL-GATED: it proposes, and only writes to the Sheet on
  Klaus's per-item approval. Sibling of the /设置复盘 setup review (that one updates Claude
  config; this one updates the work portfolio). Does NOT touch Instructions.
---

# project-review — 项目复盘 (work portfolio retrospective)

Reconcile **intent** (the registry) with **activity** (the sessions), then re-prioritize.

- **Registry (intent):** the private Google Sheet **"project management"**, id
  `1b56G28Ti6CN2bTIflPfKYnVDB9o5RD-YWr8QjjQ8K5c` (Klaus's My Drive). Columns: 项目 · 服务目标 ·
  状态 · 优先级(P0–P3) · 影响(1-5) · 触达(1-3) · 剩余成本(1-5) · Score(=ROUND(Impact*Reach/Effort,1))
  · 下一步 · 归属/memory. Priority colors: P0 浅红 / P1 琥珀 / P2 天蓝 / P3 浅绿. See
  [[project-portfolio-registry]].
- **Goals (the ranking yardstick):** [[north-star-goals]] — ① team scaling (training +
  systematization) is #1; ② litigation with Hernán. Weight impact toward these two;
  deprioritize work serving neither.

## Two modes

**DAILY pulse** (the every-day reminder, Tue–Sun): light and fast.
1. Read the Sheet + today's (and any un-reviewed recent) sessions.
2. Report only: (a) which registry projects **moved today** → update their 状态 / 下一步;
   (b) anything that now looks **stalled** (no touch in ~10+ days); (c) any **new project**
   that showed up in sessions but isn't in the Sheet. Keep it to a few lines.
3. Apply the small updates on approval (status/next-action/new rows). No full re-rank.

**WEEKLY / Monday** (rides the "双复盘" reminder, run after /设置复盘): the real review.
1–2 as above, over the last ~7 days.
3. **Re-rank:** re-check each project's 影响/触达/剩余成本 inputs (Score recomputes itself);
   flag where **Score and 优先级 diverge** (e.g. a built-but-not-live P2 scoring high = a
   quick win to consider promoting).
4. **Recommend push / pause / kill:** given the ranking + Klaus's capacity, name 1 focus to
   push, what's stalled and should be revived-or-dropped, and what to explicitly park.

## Steps (each run)

1. **Read the registry.** `gws sheets spreadsheets values get` on the Sheet (range `Sheet1!A1:J`).
2. **Read recent sessions.** Same method as [[weekly-review-skill]]: list_sessions +
   read the raw `.jsonl` transcript bodies in `~/.claude/projects/-Users-klaus/` (filename =
   session id) — snippets alone under-catch. Extract which projects were worked on, and any
   NEW project/initiative not yet in the Sheet. Default window: DAILY = today; WEEKLY = 7 days.
3. **Reconcile → build the proposal:**
   - 🟢 **Moved** — projects touched this window → propose updated 状态 / 下一步.
   - 🔴 **Stalled** — in the Sheet, untouched ~10+ days (WEEKLY: also long-idle) → flag revive/drop.
   - 🟠 **New / uncaptured** — appeared in sessions, not in the Sheet → propose a new row
     (with a first-pass 服务目标 / 优先级 / 影响-触达-剩余成本 guess for Klaus to adjust).
   - 🔵 **(WEEKLY only) Re-rank + push/pause/kill** — Score-vs-priority divergences + a
     recommended focus.
4. **Present — numbered list, `批准 / 跳过` per item**, most important first, concise. Klaus
   approves by replying with numbers.
5. **Apply on approval — write to the Sheet** (`values update` for cell edits, `append`/insert
   for new rows). Recompute isn't needed (Score is a live formula). Re-read to confirm.
6. Report what changed + the Sheet link.

## Guardrails

- **Approval-gated writes only.** Propose first; edit the Sheet only on Klaus's per-item OK.
- **No fabrication.** Only surface projects/updates the sessions actually show; guesses for a
  new row's scores are explicitly "adjust me", not asserted fact.
- **Score = ROI signal, 优先级 = Klaus's strategic call.** Surface divergence, don't overwrite
  his priority silently.
- **Don't touch Instructions / setup** — that's /设置复盘's job. Stay on the work portfolio.
- Keep it tight (Klaus's standing preference: direct, concise). A quiet day is a valid result.

## Cadence & reminders (set 2026-07-12)
Email reminders on Klaus's Google Calendar, 11:00 AM America/Los_Angeles:
- **Daily (Tue–Sun):** "跑 /项目复盘" (id `7m83n1edf00djqd3v0vu6iajdo`).
- **Monday:** "跑 /设置复盘 + /项目复盘(周一双复盘)" (id `4jlrnc2d4s8o0u5qd8hfidmml0`) — run
  /设置复盘 first, then /项目复盘. Reminders are email; the review itself is interactive and
  Klaus triggers it (local sessions can't be read by an unattended cloud job).
