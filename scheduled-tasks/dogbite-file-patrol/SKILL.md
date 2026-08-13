---
name: dogbite-file-patrol
description: Daily 11am: tidy dog-bite case lobbies + scan klaus@ for case-progress → update the Hernán Litigation Tracker + summary to Dog Bite Cases chat
---

Run the daily HERNÁN LITIGATION daily routine. Two parts, then one combined summary. This run is autonomous with no memory of prior conversations — everything needed is below and in the skills' SKILL.md files. Do Drive/Gmail ops with the default `gws` (Klaus@, which has access to the Hernan Simo Cases shared drive and to klaus@ Gmail). Post the chat summary as claude@ (GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claude; fall back to default gws / Klaus@ if that store is unauthenticated).

═══ PART A — File patrol (tidy case-folder lobbies) ═══
Use the `dogbite-file-patrol` skill (invoke via the Skill tool; it lives at ~/.claude/skills/dogbite-file-patrol). Summary of what it does:
1. Run scripts/scan_lobbies.py to list loose LOBBY (root) files per NEW-TEMPLATE dog-bite case in "1. Dog Bite Cases" (Hernan Simo Cases shared drive, driveId 0APtYw9adyTl8Uk9PVA, folder 1ewaJIoeLHoc3lG3dIyDTfWwuSt6HYRVt). Legacy (non-6-folder) cases are auto-skipped — never touch them.
2. Classify each loose file: check references/routing_memory.json filename rules → a clearly descriptive filename → otherwise download it and INSPECT the content (Read images via vision; read/render PDFs). Route per the four rules: ID / driver license / scene / address / dog / liability photos & video / deed → "1. Incident & Liability"; retainer / POE / LOR / legal correspondence → "2. Legal Documents"; INJURY photos + ER / medical records & bills → "3. Medical Record & Bill"; summons / complaint / CMC / court docs → "4. Litigation"; invoices / receipts → "5. Cost & Receipt"; settlement / disbursement → "6. Settlement & Disbursement". Genuinely unsure → DO NOT guess; leave in the lobby and report it.
3. Build ~/dogpatrol_work/decisions.json and run scripts/apply_moves.py (MOVE-only, within the same case; never delete, never cross cases, never touch the whitelist: 0.* files, the "… Intake Sheet" Google Sheet, numbered subfolders).
4. If Klaus manually resolved a previously-unsure file, append a rule to references/routing_memory.json.

═══ PART B — Case-progress scan (update the litigation tracker) ═══
Tracker = "Hernán Litigation Tracker" Google Sheet, id 1GYM0ke371z4tSJnTQl8Z6Mg_bwTiypmzx82jaAaZy64 (columns: Client | Case Type | DOL | Current Stage | Court/Case# | Last Action (+date) | Next Due (+date) | SOL | Attorney/CM | Case Folder | Notes). Read it first to get the current case list + state.
1. Search klaus@ Gmail (default gws: `gws gmail users messages list`/threads) for messages received since the last run (use `newer_than:2d`, then dedupe against what the tracker already reflects). Look for THREE signal types tied to a tracked case (match by client name or case #):
   • Court / litigation — e-filing confirmations, Summons/Complaint filed, CMC or hearing notices, One Legal receipts, opposing counsel, court clerk.
   • Insurance / claims — adjuster replies, coverage / liability determinations, demand responses, settlement offers.
   • Internal actions — LOR / POE / demand sent (or their replies), DocuSign "Completed", records requests.
2. For each relevant email, identify the case and the progress event, then update the tracker:
   • LOW-RISK facts (Last Action + date; advance Current Stage; a Notes addition) → write them directly. Example: "LOR sent 7/14" → set Last Action = "LOR sent 07/14/2026".
   • HIGH-RISK — any DUE DATE / DEADLINE / court date (CMC, response due, hearing, discovery cutoff) → write it into "Next Due" but set that cell's background to YELLOW #FFE599 (red 1, green .898, blue .6). Yellow = needs Klaus's confirmation; never treat a parsed deadline as final.
   • Can't confidently match a case, or ambiguous event → DO NOT write; list it under "待你人工定" in the summary.
   Never invent case numbers, dates, or deadlines. Only write what an email actually states.
3. Do NOT add new case rows automatically — if an email references a Hernán litigation case not yet on the tracker, flag it in the summary for Klaus to add.

═══ SUMMARY (post to the "Dog Bite Cases" chat space, spaces/AAQAJFB3j-o, as claude@) ═══
Title: "🐕 【Claude】Dog Bite 日报 — <today's date>". Then:
 • 文件整理: N files sorted (bullet: <Case>: <file> → <subfolder>); "待你人工定" for unsure files.
 • 案件进度: per case that moved, "<Case>: <what advanced>"; a "⚠️ 待确认 due date" section listing every yellow deadline written; and "待你人工定" for unmatched/ambiguous emails.
 • If nothing moved in a part, say so in one line.
Keep the safety contract throughout: move-only, skip legacy, unsure→leave/flag, deadlines→yellow. Follow each skill's SKILL.md for detail.