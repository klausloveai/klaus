---
name: hernan-case-daily-sync
description: Hernán 案件每日 sync — 工作日扫全部诉讼案(DB狗咬/LB劳工/LC小额民事/UIM)，自动补进展到各案 Case Log，claude@ 发一条 Summary 到 Hernan Cases Update 群
---

Daily Case-Log sync for ALL of attorney Hernán Simó's litigation cases at 凌图律所 / Law Office of Shenqi Cai APC — dog-bite (DB) + labor (LB) + limited-civil (LC) + UIM. For each active case, find genuinely-new activity since its last logged entry, APPEND to that case's Case Log in correct chronological position, re-assess urgency, then post ONE 简体中文 digest to "Hernan Cases Update" as claude@.

APPEND-ONLY; never edit/delete existing rows (except the narrow Status/tint exceptions below); never cross cases; never send email or contact anyone.

WEEKDAYS ONLY. Run `date` FIRST. If Sat/Sun → STOP: write nothing, post nothing, report "周末不更新". A Friday run that spills past midnight → re-check date before any sheet write and before the Chat post; if it rolled into Saturday, stop.

TOOLING: local gws as klaus@ (filter the "Using keyring" banner before parsing JSON). Shared-drive ops need supportsAllDrives=true. Retry transient "service unavailable" a few times.

═══════ CASES — 11, two log STRUCTURES ═══════

▶ STRUCTURE A · DOG-BITE (DB) — log EMBEDDED in intake sheet, tab 'Sheet 1', header row 30, data row 31+. 15-col width A:O, five MERGED column-groups: Date=A:B | Case Activity=C:I | Status=J:K | Owner/Next=L:M | Source=N:O (value anchors A,C,J,L,N). Sorted date-descending (future deadlines on top at row 31; DOL row at bottom).
  - Yi Cong        1mJS1igGOGzEtUSo9Zv0rEXDJlh88gJPd54Tn6AYqlaM
  - Bo Tao         1KVlWgMA9-R-vUbFmjbnQ0ylPW4jbyiArTdB-wWG3KCw
  - Guolin Zhao    1l64yyrv72Ewm-1BrqvwLjCu4R0TLeESb5V9oE1_6Vqs
  - Lina Lu        1raX2R2-49z5nseVGsGXQqyQ6vMP7xoHksvVT3HTWA34
  - Mudong Huang   1S_XQ5h_d7PP-WQi_RP3jF84oR3CE9x8udabwPfzv64g
  - Weicong Lin    1ik1aFfziXOUP2wmSFeQDd7V4Dg6EZb6xZ7QUcuUo6oI
  Discover new DB cases in "1. Dog Bite Cases" 1ewaJIoeLHoc3lG3dIyDTfWwuSt6HYRVt; a new folder whose intake sheet has NO log at row 30/31 → skip + note in digest.

▶ STRUCTURE B · STANDALONE (LB/LC/UIM) — each case has its OWN spreadsheet, single tab "Case Log": row 1 = A1:E1 merged gray title (never edit); row 2 = headers Date|Case Activity|Status|Owner / Next Step|Source (gray, frozen); row 3+ = entries NEWEST/FURTHEST-FUTURE FIRST, growing down. 5 cols A–E. Col A Date + col C Status = BOLD+CENTER; B/D/E left, TOP, WRAP. Widths A96·B1277·C95·D132·E242; row height 21px; Arial 10pt.
  LB (labor):
   - Hansen Li v Aligcus, Inc (CM-1046135) — folder 1AqLxGoWivKqaQcusyuNKw1PhkSM-6nt3, Case Log 1apfFyorDKDze4_YIxJzp6r04MdzICAzbRiGH52liCNc. WE REPRESENT PLAINTIFF/employee Hansen Li; adverse = Aligcus, Inc. (Kevin Li, hrg@aligcus.com). Gmail: "Hansen Li", Aligcus, aligcus.com, CM-1046135, 1046135.
   - CB Kitchen and Bathroom, Inc. v Zelaya (26CHCV01306) — folder 1uC8D9dl4I4vwbyXeESEmhmCkEPHJeBNS, Case Log 1AJTs46B3DrGQ80n0HcL7s_uS02AhbubcwZyjPgs35mw. WE REPRESENT DEFENDANT/employer CB Kitchen (Saihui Tan signs); PLAINTIFF Luis Miguel Mariona Zelaya is ADVERSE — never write as if we act for him. OPC = Comley Fresch LLP (steve@comleylaw.com, alex@comleylaw.com, Denis Cuadra). Gmail: "CB Kitchen", Zelaya, Mariona, 26CHCV01306, comleylaw.com, "Saihui Tan".
  LC (limited civil):
   - Brian Wu v. Azucanela LLC (Pending) — Case Log 1KL1IwxdNMnrYmR_PfwPAgQwj2req327TRTlusa2-WOY. Gmail: "Brian Wu", Azucanela.
  UIM:
   - Zhiping Liu v. State Farm (75-78X9-98Q) — Case Log 1iO8NKyDxpTY_UE_l8wKMNBlHU2vcko2bMc8GmS6wdhs. Gmail: "Zhiping Liu", "State Farm", 75-78X9-98Q.
   - Jiayu Ma v. Tesla (CL-70-93NTRL-1) — Case Log 1Q6g9ITkjiDiuqWkj41QVWirVKY7pkruIsCMkyU4zA8U. Gmail: "Jiayu Ma", Tesla, CL-70-93NTRL, "Colman Perkins", TIS-4624. ⚠️ A DUPLICATE Case Log (1VhwDDN2EZLgbxdbdvqsXPsXO-GLhf7Xqyuqyoqa-Xzk) exists — write ONLY to 1Q6g9ITk…, NEVER the duplicate.
  Discover new labor cases in "1. Labor Law Cases" 1eiGtE1cN465hf4VtAQLUXBDYQL8FMqOw (shared drive 0APtYw9adyTl8Uk9PVA); a new folder without a "… Case Log" sheet → skip + note.

═══════ STATUS + COLOR (both structures) ═══════
Urgent #EA9999 (hard deadline within 3 days / a miss forfeits a right: default·waiver·statutory bar·dismissal·sanctions / a date CONFLICT / Hernán·Klaus flags it) · To-do #FFE39E (our action still owed, OR a known date NOT yet calendared) · In progress #C2E7FF (our step done + item calendared/scheduled, waiting on other side or a date; a scheduled hearing/conference is BLUE) · Done #D4ECBD (finished, past tense).
YELLOW vs BLUE is Klaus's rule — apply every run incl. to existing rows: yellow = WE owe an action; blue = our step done, calendared, now waiting. Verify against klaus@ Calendar each run and re-color.
URGENT is a severity overlay: EVERY run re-assess existing To-do/In progress rows vs today and PROMOTE any now-qualifying to Urgent (change Status cell + re-tint red); list promotions in the digest; never auto-demote (only a completion→Done clears it).
CROSS-CHECK deadlines between klaus@ Calendar, the correspondence, and the Case Log; when they disagree, log an Urgent row naming both dates asking which controls, treat the EARLIER as operative.

═══════ GATHER / DEDUPE ═══════
Per case: (1) klaus@ Gmail with that case's search terms, newer_than:3d (court/OPC mail may route to hernan.s@/cassie@ and reach klaus@ only as forwards); (2) new files in the case folder (any subfolder) since the last logged entry; (3) klaus@ Calendar (also for the yellow/blue check). EXTRACT deadlines from the BODY of letters/emails, not just calendar invites — log each such deadline as its own future-dated row.
DEDUPE HARD: the watermark is NOT row 3 / row 31 (future-dated rows sort to the top). Read ALL existing entries (Date + Activity) and add an item only if no existing row already describes it. Unsure → do NOT add. Running twice in one day must not duplicate.

═══════ INSERT ═══════
Case Activity = professional COMPLETE English (name the document, party, case #, action, and what's next). Owner = Klaus / Hernán / Client / OPC / —. Source = email+date / document / "Calendar" / "Case folder — <date>" (never invent a source).
Insert at correct chronological position (below future-dated rows, above the first older row). Insert LOWEST position first when placing several in one run.
- DB embedded: insertDimension(ROWS, startIndex=targetRow-1, count N, inheritFromBefore false); rebuild the 5 merges MERGE_ALL {0,2}{2,9}{9,11}{11,13}{13,15}; write values to anchors A/C/J/L/N; repeatCell whole row A:O to the status color + TOP align + WRAP.
- Standalone: insertDimension(ROWS,…); write A:E; repeatCell tint + BOLD/CENTER on cols A and C + WRAP/TOP; set row height 21px.
Never edit Date/Activity of an existing row; never touch title/header rows; never delete/reorder; never cross cases; never restyle columns. If a previously yellow (un-calendared) date row is now calendared, add a NEW "calendared X" Done row rather than editing the old one (except the allowed Status/tint recolor).

═══════ CHAT DIGEST ═══════
THEN post exactly ONE 简体中文 message to "Hernan Cases Update" spaces/AAQAJFB3j-o AS claude@:
  export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claude
  gws chat spaces messages create --params '{"parent":"spaces/AAQAJFB3j-o"}' --json '{"text":"<digest>"}'
FORMAT:
  Header: 【Claude】Hernán 案件每日更新 — <MM/DD/YYYY>
  Blank line. Each case name on its OWN line in *asterisks* with a bucket tag prefix: *[DB] Yi Cong* / *[LB] Hansen Li* / *[LC] Brian Wu* / *[UIM] Jiayu Ma*. Blank line between cases. NO leading spaces (Chat eats indent).
  Under each case: one SHORT line per item (~20 中文字), colored circle 🔴紧急 / 🟢已完成 / 🔵进行中 / 🟡待办 — in that priority order, max 3 bullets/case.
  LIST EVERY CASE incl. no-activity ones → under them "今日无新进展，后续关键日期：" + upcoming 🔴/🔵/🟡 dates. Never silently omit a quiet case.
  Close with a 📅 重要日期 section (≤~8 lines): every date in the next ~60 days + any 🟡 un-calendared date / SOL however far out.
  Exactly ONE Chat message per run — the ONLY outbound. No email, no client contact.

═══════ PRIVATE RESULT ═══════
Per case: rows added (date + one-line + color); completion flips / urgency promotions / yellow→blue recolors; quiet cases; folders skipped for lack of a Case Log; date conflicts found; anything deliberately NOT added; Jiayu Ma duplicate-log status; and confirm the Chat digest posted.