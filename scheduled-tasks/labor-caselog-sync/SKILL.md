---
name: labor-caselog-sync
description: Labor Law Case-Log — 工作日(周一–五)早上扫 klaus@ 邮件+案folder+日历，自动补进展到各劳工案 Case Log（红/黄/蓝/绿），并用 claude@ 发 Summary 到 Labor Law Notification 群
---

Daily Labor Law Case-Log sync for 凌图律所 / Law Office of Shenqi Cai APC (attorney Hernán Simó).

GOAL: for each active LABOR LAW case, find genuinely-new activity since the last logged entry and AUTO-APPEND it to that case's standalone "Case Log" sheet in correct chronological position, re-assess urgency, then post ONE 简体中文 digest to the "Labor Law Notification" Chat space as claude@.

This is the LABOR-LAW twin of `daily-caselog-sync` (which handles DOG BITE cases). They are separate on purpose — do NOT touch dog-bite cases or their sheets here, and never modify the dog-bite routine.

WEEKDAYS ONLY. Run `date` FIRST, before any other work. If today is Saturday or Sunday, STOP
immediately — write nothing to any Case Log and post NOTHING to Chat. Just report "周末不更新".
This also covers a run that starts Friday and spills past midnight: re-check the date before the
sheet writes and before the Chat post, and if the clock has rolled into Saturday, stop there
rather than posting a weekend-dated digest. Klaus asked for this on 08/01/2026 — 双休不需要更新.

======================= CASES =======================
"1. Labor Law Cases" folder = 1eiGtE1cN465hf4VtAQLUXBDYQL8FMqOw (in the "Hernan Simo Cases" shared drive, driveId 0APtYw9adyTl8Uk9PVA). Also DISCOVER any new case folder there and handle it if it already contains a "… — Case Log" sheet; if a new folder has no Case Log sheet yet, SKIP it and report that in the digest.

1) Hansen Li v Aligcus, Inc (CM-1046135)
   - case folder  1AqLxGoWivKqaQcusyuNKw1PhkSM-6nt3
   - Case Log     1apfFyorDKDze4_YIxJzp6r04MdzICAzbRiGH52liCNc
   - WE REPRESENT THE PLAINTIFF/EMPLOYEE (Hansen Li). Adverse party = Aligcus, Inc.;
     their contact is Kevin Li, HR Generalist (hrg@aligcus.com / HRConnect@aligcus.com).
   - Pre-litigation settlement negotiation + a pending CA Labor Commissioner (DLSE) claim CM-1046135.
   - Gmail search terms: "Hansen Li", Aligcus, aligcus.com, CM-1046135, 1046135.

2) CB Kitchen and Bathroom, Inc. v Zelaya (26CHCV01306)
   - case folder  1uC8D9dl4I4vwbyXeESEmhmCkEPHJeBNS
   - Case Log     1AJTs46B3DrGQ80n0HcL7s_uS02AhbubcwZyjPgs35mw
   - WE REPRESENT THE DEFENDANT/EMPLOYER (CB Kitchen and Bathroom, Inc.; Saihui Tan signs for
     the company). The PLAINTIFF Luis Miguel Mariona Zelaya is the ADVERSE party — never write
     as though the firm acts for him. Opposing counsel = Comley Fresch LLP (Stephen Fresch
     steve@comleylaw.com, R. Alexander Comley alex@comleylaw.com, Denis Cuadra). Prior defense
     counsel = Helen Wong (helenwong.law@gmail.com).
   - LA Superior Court, Chatsworth. Filed 04/01/2026, served 06/05/2026.
   - Gmail search terms: "CB Kitchen", Zelaya, Mariona, 26CHCV01306, comleylaw.com, "Saihui Tan".

Blank-template reference (structure/colors only, never write case data into it):
Labor Law Cases Tracking Sheet Template = 180IHfqlDgG8dYnGNKr5VYs4g2Z6B2pYWT13roLBhXs4

======================= SHEET FORMAT (do not restyle) =======================
Each Case Log is its own spreadsheet, single tab named "Case Log":
  - Row 1 = A1:E1 MERGED title (gray #D9D9D9, bold 11pt) — never edit.
  - Row 2 = headers: Date | Case Activity | Status | Owner / Next Step | Source (gray, bold, frozen).
  - Row 3 onward = log entries, NEWEST/FURTHEST-FUTURE FIRST, growing downward.
  - Column widths A96 · B1277 · C95 · D132 · E242; data row height fixed 21px; Arial 10pt.
  - Whole row tinted by status:
        Urgent      = #EA9999   (red)
        To-do       = #FFE39E   (yellow)
        In progress = #C2E7FF   (blue)
        Done        = #D4ECBD   (green)
  - Date (col A) and Status (col C) are BOLD + CENTER; B/D/E left-aligned, TOP vertical align, WRAP.
  - Entry text (col B) = professional COMPLETE ENGLISH, roughly 75–270 characters — the compact
    one-line-per-entry view. Name the document, party, case #, action and what's next.
  - Source (col E) must cite the origin, e.g. "Email — Hernán 07/23/2026", "Calendar invite
    07/22/2026", "Proof of Service", "Case file". NEVER invent a source.

YELLOW vs BLUE (Klaus's rule — apply it every run, including to existing rows):
  - YELLOW / To-do  = OUR side still owes an action (draft the demand, file the responsive pleading).
  - BLUE / In progress = our step is done, the item is calendared or scheduled, and we are now
    WAITING on the other side or on a date to arrive. A deadline we have served a request for and
    entered on the calendar is BLUE, not yellow. A scheduled hearing/conference is BLUE.
  - GREEN / Done = finished.
Check klaus@'s Google Calendar each run to see whether a deadline has actually been calendared, and
re-color accordingly. Do not assume — verify against the calendar.

======================= RED / URGENT =======================
"Urgent" is a severity overlay, not a lifecycle stage. Mark a row Urgent (red #EA9999) when ANY of:
  - a hard deadline (court, statutory, or one the firm committed to) falls within the next 3 days;
  - missing it forfeits a right — default, waiver, statutory bar, dismissal, sanctions;
  - a DATE CONFLICT exists (e.g. the calendar and the correspondence give different deadlines) —
    flag it red until a human confirms which controls, and treat the EARLIER date as operative;
  - Hernán or Klaus expressly calls it urgent.
EVERY RUN, re-assess the existing To-do / In progress rows against today's date and PROMOTE any that
now qualify to Urgent (change the Status cell + re-tint the row red). Promotions must be listed in the
digest. Never demote a row out of Urgent automatically — only a completion flip to Done clears it.
Keep Urgent rows sorted with the other future-dated rows by date.

CROSS-CHECK deadlines between (a) klaus@'s calendar, (b) the correspondence, and (c) the Case Log.
When they disagree, log an Urgent row naming both dates and asking which controls. This has already
happened once: the calendar carried 07/29/2026 for CB Kitchen's responsive pleading while opposing
counsel's 07/17/2026 email had extended it to 08/05/2026.

======================= WHAT TO GATHER =======================
Sources, per case: (1) klaus@ Gmail using the case's search terms, newer_than:3d — note that court
notices and opposing-counsel mail sometimes route to hernan.s@ / cassie@ and arrive in klaus@ only as
forwards; (2) new files added to the case folder (any subfolder) since the last logged entry;
(3) klaus@'s Google Calendar (also used for the yellow/blue check above).

Also EXTRACT DEADLINES FROM THE BODY of letters and emails, not just from calendar invites — e.g. the
07/23/2026 records request to Aligcus created two statutory deadlines (08/13/2026 under Labor Code
§226(c) and 08/22/2026 under §1198.5) that existed nowhere else. Log each such deadline as its own
future-dated row.

DEDUPE HARD. The watermark is NOT simply row 3's date — future-dated rows deliberately sort to the
top, so row 3 is usually a FUTURE date. Instead: read ALL existing entries (col A + B) and treat an
item as new only if no existing row already describes it. When unsure, do NOT add it — a missed item
reappears tomorrow, a duplicate is permanent noise. Running twice in one day must not duplicate.

======================= EDITING RULES =======================
APPEND-ONLY, with narrow exceptions that touch ONLY the Status cell and the row tint:
  (a) completion — clear evidence an item was carried out → Status "Done", re-tint green;
  (b) urgency promotion — the Urgent criteria are now met → Status "Urgent", re-tint red;
  (c) yellow→blue — our step is done and the item is calendared/scheduled → Status "In progress".
All of these must be listed in the digest. You may NEVER edit the Date or Case Activity text of an
existing row, never delete or reorder rows, never touch rows 1–2, never cross cases, never restyle
columns. Never fabricate dates, facts, amounts, or sources.

INSERT METHOD: insert each new row at its CORRECT CHRONOLOGICAL POSITION, not blindly at row 3 —
a new entry dated today belongs below any future-dated deadline rows. Use insertDimension(ROWS,
startIndex = target row - 1, count N, inheritFromBefore false) → write A{r}:E{r+N-1} → repeatCell the
tint + bold/center on cols A and C + WRAP/TOP → set those rows' height to 21px. When inserting at
several positions in one run, do the LOWEST position first so earlier indices don't shift.

Use the local gws CLI as klaus@ for all Drive/Gmail/Sheets/Calendar reads (filter out the "Using
keyring backend: keyring" banner line from stdout before parsing JSON). Shared-drive operations need
supportsAllDrives=true. Retry transient "service is currently unavailable" errors a few times with a
short backoff. Send NO email. Contact NO client or opposing party.

======================= CHAT DIGEST =======================
THEN post exactly ONE message, in concise 简体中文, to the "Labor Law Notification" space
spaces/AAQAV-bW80Y AS claude@:
  export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claude
  gws chat spaces messages create --params '{"parent":"spaces/AAQAV-bW80Y"}' --json '{"text":"<digest>"}'

FORMAT — mirror the Dog Bite digest exactly:
  - Header line: 【Claude】Labor Law 每日更新 — <MM/DD/YYYY>
  - Blank line, then per case: the case name on its own line wrapped in *asterisks* so Chat bolds it.
  - Under it, one line per item, each starting with a colored circle emoji:
    🔴 紧急 / 🟡 待办 / 🔵 进行中 / 🟢 已完成. Put 🔴 first, then 🟢 today's completions, then 🔵, then 🟡.
  - Keep each bullet SHORT — one line, Chinese, no full sentences from the sheet.

LIST EVERY CASE, INCLUDING ONES WITH NO NEW ACTIVITY. For a case with nothing new, put the line
「今日无新进展，后续关键日期：」under the case name and then list its upcoming deadlines / follow-up
dates as 🔴/🔵/🟡 bullets. Klaus explicitly asked for this — never silently omit a quiet case.
If NOTHING is new across ALL cases, still post the digest with each case's upcoming dates.
Exactly ONE Chat message per run — never spam. This digest is the ONLY outbound message allowed.

Reference (this exact shape was approved by Klaus on 07/24/2026):
【Claude】Labor Law 每日更新 — 07/24/2026

*Hansen Li v Aligcus*
🟢 记录调取函已发 Aligcus（Kevin Li），依 §§226(b)、1198.5，抄送 Hernán、Cassie
🔵 8/13 §226(c) 工资考勤、8/22 §1198.5 人事档案，已入日历，等 Aligcus 交
🟡 7/30 开口 demand 截止

*CB Kitchen v Zelaya*
今日无新进展，后续关键日期：
🔴 答辩期冲突 —— 日历写 7/29，但 OPC 7/17 邮件已同意延到 8/5，请确认以哪个为准
🔵 7/28 OPC 交修改版起诉状
🟡 8/5 答辩状／demurrer 截止

======================= PRIVATE RESULT =======================
Finally output a concise private digest for Klaus: per case, rows added (date + one-line summary +
color), any completion flips / urgency promotions / yellow→blue recolors, cases with nothing new,
folders skipped for lack of a Case Log sheet, any calendar-vs-email date conflicts found, anything
ambiguous you deliberately did NOT add, and whether the Chat message was posted.