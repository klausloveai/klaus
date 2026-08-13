---
name: daily-caselog-sync
description: Daily Case-Log — 工作日扫 klaus@ 邮件+案folder，自动补进展到各狗咬案 log，并用 claude@ 发每日 Summary 到 Dog Bite Cases 群
---

Invoke the `daily-caselog-sync` skill and follow it exactly.

FIRST, get today's real date: run `date "+%m/%d/%Y (%A)"` and use THAT as "today" for the digest header, the Gmail newer_than window, the SOL / answer-deadline / service math, and the watermark. Never assume the date — in a scheduled run your own sense of the date can be wrong.

Goal: for each of Hernán Simó's active DOG-BITE cases at 凌图律所, find genuinely-new activity since that case's last logged row and APPEND it to that case's Case Log — the 5-column table EMBEDDED in its intake sheet (tab "Sheet 1"), header at row 30, data from row 31 down. Append-only: never edit or delete existing rows, never cross cases, never send email.

Case Log layout (inside the intake sheet, 15-col width A:O): each row split into 5 merged column-groups so the intake form's widths above are untouched — Date = A:B | Case Activity = C:I | Status = J:K | Owner/Next Step = L:M | Source = N:O (value anchors A, C, J, L, N). Row 30 = grey bold header. Sorted date-descending: future deadlines on top (newest at row 31), most-recent activity next, date-of-loss row at the bottom. Status + WHOLE-ROW color (A:O): Urgent #e99999 (deadline <3 days / forfeits a right / flagged); To-do #ffe39d (action owed, OR a known date NOT on the calendar); In progress #c2e7ff (work under way, OR a date that IS on the calendar); Done #d4edbd (completed, past tense).

Intake sheets (Case Log embedded at row 30/31):
- Yi Cong 1mJS1igGOGzEtUSo9Zv0rEXDJlh88gJPd54Tn6AYqlaM
- Bo Tao 1KVlWgMA9-R-vUbFmjbnQ0ylPW4jbyiArTdB-wWG3KCw
- Guolin Zhao 1l64yyrv72Ewm-1BrqvwLjCu4R0TLeESb5V9oE1_6Vqs
- Lina Lu 1raX2R2-49z5nseVGsGXQqyQ6vMP7xoHksvVT3HTWA34
- Mudong Huang 1S_XQ5h_d7PP-WQi_RP3jF84oR3CE9x8udabwPfzv64g
- Weicong Lin 1ik1aFfziXOUP2wmSFeQDd7V4Dg6EZb6xZ7QUcuUo6oI
(Also list folders in "1. Dog Bite Cases" 1ewaJIoeLHoc3lG3dIyDTfWwuSt6HYRVt; any case whose intake sheet has no Case Log at row 30/31 → skip and note in the digest, don't build one.)

Per case: read the embedded Case Log ('Sheet 1'!A30:O; data from row 31, anchors A=date C=activity J=status L=owner N=source) to find the newest logged activity date and to dedupe. Gather new activity since that date from (1) Case Log master sheet 1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA, (2) klaus@ Gmail (client/defendant/case#/One Legal order# + case Gmail label, newer_than:3d — court/One Legal notices may route to hernan.s@/cassie@), (3) new files in the case folder since the last logged date, (4) klaus@ Calendar (q=<Client>) for any NEW deadline/hearing/appointment or SOL not yet a date row. Dedupe hard — when unsure, do NOT add.

Compose each new row: Date | Case Activity (professional COMPLETE English — doc, party, case #, action, next step) | Status | Owner (Klaus/Hernán/Client/OPC/—) | Source (email+date / document / Calendar / Case folder—date). Insert date-sorted (append-only): find where the item's date belongs (below future-dated rows, above the first older row) and insertDimension(ROWS, startIndex there, count N, inheritFromBefore false); rebuild the 5 column-group merges for each inserted row — mergeCells MERGE_ALL for {0,2},{2,9},{9,11},{11,13},{13,15}; write the 5 values to anchors A/C/J/L/N; repeatCell the WHOLE row A:O (cols 0-15) to the Status color + TOP align + WRAP. Never overwrite an existing row. If a previously un-calendared (yellow To-do) date row is now calendared, add a NEW "calendared X" Done row rather than editing the old one. Idempotent — running twice must not duplicate. Calendar is READ-ONLY (never create/move/delete events; only surface gaps).

Use local gws CLI (klaus@; filter the "Using keyring" banner); shared-drive ops need supportsAllDrives.

THEN post EXACTLY ONE 简体中文 concise digest to "Dog Bite Cases" spaces/AAQAJFB3j-o AS claude@ (export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claude, then gws chat spaces messages create --params '{"parent":"spaces/AAQAJFB3j-o"}' --json '{"text":"<digest>"}'). Format: every bullet on its OWN line with NO leading spaces (Chat collapses indent); max 3 bullets per case; priority 🟡>🔵>🟢; one short clause (~20 中文字) per bullet; case name on its own line as *Name*; blank line between cases; omit unchanged cases. Always close with a 📅 重要日期 section (≤~6 lines): every date in the next ~60 days plus any 🟡 un-calendared date however far out (esp. SOLs). Header uses today's real date from `date`. Shape:
【Claude】Dog Bite 每日更新 — <MM/DD/YYYY>

*<客户名>*
🟡 <一句话>
🔵 <一句话>

📅 重要日期
🔵 <M/D> <客户> <事项>
🟡 <M/D> <客户> <事项>，未上日历

ALWAYS post one message — even when nothing changed (silence = the routine FAILED). If nothing new, still post the 📅 section + "今日无新进展". If a case was skipped or a step errored, say so in that message. ONE message per run. This is the ONLY outbound message; no email, no other Chat posts, no client contact.

Finally output a concise private DIGEST: per case rows added + status; un-calendared dates found; cases with nothing new; folders skipped; anything deliberately not added; confirm the Chat digest posted.