---
name: weekly-pinerd-sync
description: 每周一 8:30 把 PI Nerd (nerdgroup.co) listserv 的新帖/新回复同步进 Drive 知识库
---

Invoke the `pinerd-sync` skill to sync the past week's Pre-Litigation Nerd (nerdgroup.co) listserv activity into Klaus's private "PI Nerd" knowledge base.

Run it end to end, unattended:

1. `python3 ~/.claude/skills/pinerd-sync/scripts/pinerd_pull.py --workdir <scratchpad>/pinerd` — no `--since`, so it resumes from the newest date in the Master Index's "Updates Log" tab. It reads klaus@ Gmail only (every group message is delivered there as an individual email) — NO website login, NO browser needed for the normal sync.
2. If it reports 0 threads: report "本周无新内容" in one line and STOP. Do not touch the spreadsheet.
3. Otherwise read `digest.txt` in full and write one Summary per thread per the skill's rules — conclusion first, statutes/citations kept verbatim (Ins. Code / CCR / Veh. Code), every dollar amount, date, phone, address, clinic name and attorney name copied exactly and NEVER invented, `No recommendation posted as of <today>.` when nobody answered, and any of your own additions marked `[KB note: …]`. Name the answerer when it is Lydia Santiago, Paul Zuckerman, Ivy Callahan or Michael Geragos.
4. Pull out any new providers / clinics / imaging / lien networks / investigators / records-retrieval vendors / out-of-state referral attorneys / body shops / DV appraisers / arbitrators / software vendors. Read the Provider Database's column A FIRST — existing names get an appended ` ➕[M/YYYY] …` note, not a duplicate row.
5. Write the payload JSON and apply it with `python3 ~/.claude/skills/pinerd-sync/scripts/pinerd_write.py payload.json`.
   **NEVER write to Sheet1 / Updates Log / Provider Database by any other means.** Do not call `values update`, `values append`, or any other Sheets write on this spreadsheet yourself, and do not 'just append the new rows at the top' — Sheet1 is a SORTED table and an out-of-band write silently OVERWRITES existing rows. That has already happened twice (2026-09-09 grid limit, 2026-09-13 rows clobbered at A2), destroying rows both times. The script is the only sanctioned writer: it is idempotent (same topic id never lands twice, same [UPD] block never appends twice, same log entry never duplicates), it grows the grid before writing, and it VERIFIES after writing that no topic was lost — if it aborts, STOP and report, do not retry blind and do not work around it.
6. Only if the digest contains a `Replay Now Available` / `Webinar Notes` / `Event: … Webinar` post, refresh the "Webinar Library" tab from Box via Claude-in-Chrome per the skill's step 5. Otherwise skip the browser entirely.

Then report to Klaus in 简体中文, short: how many new threads and how many old threads got replies; 3–5 items that actually matter for 凌图律所 right now (dog bite, lien reduction, UM/UIM, carrier deadlines, demand escalation, litigation procedure); whether any thread Klaus himself posted got answers (his posts come from "Klaus Liu"); which providers were added or updated; and any new webinar recording. Do NOT recite the whole table.

HARD BOUNDARIES: this listserv's content is member-confidential (Terms §6a) — the backup stays private, never redistributed. Read klaus@ Gmail and write ONLY to Klaus's own Master Index sheet (1sbSGUq0Bu3khRoxKLk9wdi0CvDyaeJnF50EehvvS1p4). Never post or reply on the listserv, never send email, never change the Groups.io subscription settings.