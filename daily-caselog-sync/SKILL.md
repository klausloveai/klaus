---
name: daily-caselog-sync
description: >
  Daily sweep of klaus@ Gmail + Drive case folders + the Case Log master sheet + klaus@
  Google Calendar for each of Hernán Simó's DOG-BITE cases, and auto-append any NEW
  activity to that case's Case Log — the 5-column table EMBEDDED in its intake sheet at
  row 30/31 (Date | Case Activity | Status | Owner/Next Step | Source), color-coded by
  status (Urgent/To-do/In progress/Done).
  Then post ONE concise 简体中文 Summary to the "Dog Bite Cases" Chat space as claude@.
  Use when: "daily case-log sync", "跑一下每日案件更新", "/daily-caselog-sync", or when the
  daily scheduled task fires. AUTO-WRITES (append-only), then reports a digest. Sibling of
  [[weekly-case-update]]. Format mirrors the firm's Labor Law Case Log template.
---

# Daily Case-Log Sync (dog-bite cases)

Each run: for every active dog-bite case, find genuinely-new activity since the last logged
row and APPEND it to that case's **standalone Case Log** spreadsheet. **Append-only: never
edit or delete existing rows; never cross cases; never send email.**

## Tooling
Local `gws` CLI (klaus@) for all Drive/Gmail/Sheets/Calendar ops (filter out the
`Using keyring` banner). Shared-drive ops need `supportsAllDrives`.

## The Case Log lives INSIDE each case's intake sheet (tab "Sheet 1"), NOT a separate file
Below the intake form: **header at row 30, data from row 31 down**. Each row is split into
**5 merged column-groups** across the 15-column width (A:O) so the intake form's column
widths above are untouched:
`Date = A:B | Case Activity = C:I | Status = J:K | Owner/Next Step = L:M | Source = N:O`
(value anchors: A, C, J, L, N). Row 30 header = grey #d9d9d9, bold, same 5 groups.
Sorted DATE-DESCENDING: future-dated deadlines/hearings on top (newest at row 31), then
most-recent activity, oldest at the bottom (the date-of-loss row anchors the bottom).

**Status values + row background color (color the WHOLE row A:E):**
- `Urgent` #e99999 — hard deadline inside 3 days, or a miss forfeits a right (default, waiver, statutory bar), or Hernán/Klaus flags it. Sorts above everything.
- `To-do` #ffe39d — an action still owed OR a known date NOT yet on the calendar.
- `In progress` #c2e7ff — work under way but unfinished, OR a date that IS on the calendar.
- `Done` #d4edbd — completed activity, stated factually in the past tense.

(Date rows follow Klaus's rule: **on calendar → In progress (blue); date known but NOT on
calendar → To-do (yellow)**.)

## Cases → intake sheet IDs (the Case Log is embedded in each, row 30/31+)
- Yi Cong — `1mJS1igGOGzEtUSo9Zv0rEXDJlh88gJPd54Tn6AYqlaM`
- Bo Tao — `1KVlWgMA9-R-vUbFmjbnQ0ylPW4jbyiArTdB-wWG3KCw`
- Guolin Zhao — `1l64yyrv72Ewm-1BrqvwLjCu4R0TLeESb5V9oE1_6Vqs`
- Lina Lu — `1raX2R2-49z5nseVGsGXQqyQ6vMP7xoHksvVT3HTWA34`
- Mudong Huang — `1S_XQ5h_d7PP-WQi_RP3jF84oR3CE9x8udabwPfzv64g`
- Weicong Lin — `1ik1aFfziXOUP2wmSFeQDd7V4Dg6EZb6xZ7QUcuUo6oI`

**Discover new cases:** list folders in `1. Dog Bite Cases`
(`1ewaJIoeLHoc3lG3dIyDTfWwuSt6HYRVt`); for any case whose intake sheet has no Case Log at
row 30/31 yet, skip it and note it in the digest (don't build one — separate migration).

## Per case
1. **Read the existing Case Log** (`'Sheet 1'!A30:O`; data from row 31 — read anchor cols
   A=date, C=activity, J=status, L=owner, N=source). Newest activity is the first data row
   whose date ≤ today. Keep every row's date + Case Activity text to **dedupe**.
2. **Gather candidate new activity** since the newest logged activity date, from:
   - **Case Log master sheet** `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA` (human-curated).
   - **klaus@ Gmail** — client, defendant, case #, One Legal order #, and the case's Gmail
     label, `newer_than:2d`. (Court/One Legal notices may route to hernan.s@/cassie@.)
   - **Case folder** — new files since the last logged date (medical records, HIPAA auths,
     injury photos, filed pleadings, receipts) — each is a log-worthy step.
   - **klaus@ Calendar** (`q=<Client>`) — any NEW deadline/hearing/appointment or SOL not
     already represented as a date row.
3. **Dedupe hard.** Drop anything already in the log. When unsure, do NOT add (a missed item
   reappears tomorrow; a duplicate is noise).
4. **Compose rows** — for each new item: `Date | Case Activity | Status | Owner/Next Step |
   Source`. Case Activity = **professional, complete English** (team-facing: name the doc,
   party, case #, action, and what's next). Assign Status/color per the table above. Owner =
   Klaus / Hernán / Client / OPC / — . Source = the email + date, the document, "Calendar",
   or "Case folder — <date>".
5. **Insert, date-sorted (append-only).** Find the row where the new item's date belongs
   (below future-dated rows, above the first older row) and `insertDimension`
   {dimension:"ROWS", startIndex:<that row-1>, endIndex:<+N>, inheritFromBefore:false}. Each
   inserted row needs the 5 column-group merges rebuilt: `mergeCells` MERGE_ALL for
   {0,2},{2,9},{9,11},{11,13},{13,15}. Write the 5 values to anchors A/C/J/L/N. `repeatCell`
   the WHOLE row A:O (cols 0–15) to the Status color + TOP align + WRAP. Never overwrite an
   existing row. If a previously un-calendared date row (To-do/yellow) is now calendared,
   add a NEW "calendared X" Done row rather than editing the old one (append-only).
6. If a case has zero new activity, leave its sheet untouched.

## Then — post the daily Summary to Chat (as claude@)
Post EXACTLY ONE 简体中文 concise digest to **"Dog Bite Cases"** `spaces/AAQAJFB3j-o` as
claude@:
```
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claude
gws chat spaces messages create --params '{"parent":"spaces/AAQAJFB3j-o"}' --json '{"text":"<digest>"}'
```
Format rules (strict): every bullet on its OWN line, **NO leading spaces/indentation**
(Chat collapses indent and mashes lines); max 3 bullets per case; priority 🟡>🔵>🟢; one
short clause per bullet (~20 中文字); case name on its own line as `*Name*`; blank line
between cases; omit cases with no change. **Always close with a 📅 重要日期 section** (≤~6
lines): every date in the next ~60 days plus any 🟡 un-calendared date no matter how far out
(un-calendared SOLs especially). Shape:
```
【Claude】Dog Bite 每日更新 — <MM/DD/YYYY>

*<客户名>*
🟡 <一句话>
🔵 <一句话>

📅 重要日期
🔵 <M/D> <客户> <事项>
🟡 <M/D> <客户> <事项>，未上日历
```
**ALWAYS post one message — even when nothing changed** (silence = the routine FAILED, not a
quiet day). If nothing new, still post the 📅 section + "今日无新进展". If a case was skipped
or a step errored, say so in the same message. ONE message per run — never spam. This is the
ONLY outbound message allowed; no email, no other Chat posts, no client contact.

## Run's private completion report
Per case: rows added + status; un-calendared dates found; cases with nothing new; folders
skipped (no Case Log yet); anything deliberately not added; confirm the Chat digest posted.

## Guardrails
- Append-only to each case's own Case Log; never edit/delete existing rows; never cross cases.
- Calendar is READ-ONLY — never create/move/delete events; only surface the gap.
- Idempotent — running twice a day must not duplicate (watermark + dedupe).
- Colors/format must match the Labor Case Log template exactly.
