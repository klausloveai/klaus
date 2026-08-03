---
name: weekly-case-update
description: >
  Generate a weekly LITIGATION status update for attorney Hernán Simó's cases at
  凌图律所 / Law Office of Shenqi Cai APC, and deliver it as (1) a Gmail DRAFT to
  Hernán in English and (2) a Chinese self-reminder Gmail DRAFT to Klaus. Use this
  skill whenever any of these are mentioned: weekly case update, 每周案件更新, weekly
  litigation update, "跑一下 Hernán 的周更新", "Yi Cong weekly update", "/weekly-case-update",
  or when a scheduled weekly task fires. Given a case name (or "all Hernán cases"),
  the skill reads the Drive case folder + intake sheet + filed pleadings + One Legal /
  court receipts + the Case Log, computes the key deadlines, and drafts the two
  updates. It DRAFTS ONLY — it never sends email, never posts to Chat, never files
  anything. Klaus reviews and sends every outbound himself. Serves goal ② (litigation
  with Hernán → learn → systematize → scale).
---

# Weekly Case Update (Hernán litigation)

Produce a weekly update for one or more of Hernán Simó's litigation cases and leave
it for Klaus as Gmail DRAFTS. **Draft-only. Never send, never post, never file.**

## Scope / rollout
- **v1 (test):** case = **Yi Cong** (dog bite, San Bernardino, Case No. CIVSB2619725).
- **Target:** all of Hernán's active litigation cases — enumerate from the
  **"Hernan Simo Cases"** shared drive (one folder per case) cross-checked against
  the **Case Log** sheet (id `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA`).
  Skip closed/settled folders. When run with no case named, do ALL active ones,
  one update section per case in the Hernán draft, and one combined reminder for Klaus.

## Inputs to read per case
1. The case folder in Drive (intake sheet, filed **Complaint**, **Summons SUM-100**,
   **CM-010**, **Certificate of Assignment**, **POS-010 / affidavit of service**,
   **One Legal order receipt**, any **POE / preservation letters**, USPS tracking).
2. The case **Intake Sheet** (dog-bite intake has an "SOP / Stage" + "Litigation"
   block with filed/served dates, case number, SOL, insurance status, treatment stage).
3. The **Case Log** sheet (chronological email-anchored log) for the newest activity.
4. Gmail: search klaus@ for the client name, defendant name, case number, and the
   One Legal order # to pull any new correspondence. (Note: court/One Legal notices
   often route to hernan.s@ / cassie@, so absence in klaus@ ≠ no activity — say so.)

## Deadlines to compute (always show, label assumptions)
- **Answer deadline** = date defendant personally served + 30 days (CCP §412.20).
  Flag it and note "evaluate default if no answer."
- **SOL** (from intake; CA dog bite / PI = 2 yrs from DOL unless out-of-state).
- Any pending POE re-service / evidence-preservation follow-ups.
- **CMC / TSC / OSC + CMC-Statement-due dates** — get the ACTUAL dates, don't leave
  "not yet on file / obtaining." Source them from the court-returned documents in the
  One Legal order (the Notice of Case Assignment / hearing notice attached at acceptance)
  or the conformed complaint. (e.g. Yi Cong: CMC statement due 12/21/2026, TSC 1/4/2027.)
- **Advance jury fee (CCP §631)** — if jury demanded, $150/side is due on or before
  the initial CMC; list it as a pending reminder ("Jury trial fee pending").

## Calibration from Klaus's edits — MATCH THESE. Depth scales to case stage.

**Yi Cong weekly (dog-bite, FILED case, 07/26/2026):**
- **Timeline**: dated milestone lines — Klaus keeps these in full.
- **Important Dates**: list the REAL court dates (CMC-statement-due, TSC, answer deadline,
  SOL, and any set treatment appt like the initial psych eval). No "obtaining/TBD" if it
  can be found.
- **Notes / Reminders**: keep to **2–4 short, genuinely-pending items for the attorney**
  (e.g. "Working on obtaining ER record and bill", "Jury trial fee pending"). Do NOT dump
  the full internal to-do inventory here — Klaus's own tactical items (spoliation re-serve,
  Camden/DOE substitution, expert CV follow-up, default prep, Ring-video discovery, template
  signing) are tracked internally and were cut from the attorney update. Lean and crisp.

**Brian Wu v. Azucanela LLC (limited civil, PRE-FILING, first update, 07/25/2026) — much leaner:**
Klaus cut my draft hard. When the case is **pre-filing AND the attorney already has the
background** (here Hernán had authored the roadmap memo two days prior), keep it minimal:
- **Timeline**: he DELETED every event before the current reporting period — cut the 2020
  lease execution, the Jan–May 2026 non-payment, and the June 2026 termination; KEPT only
  the 3 recent items (07/20 fee paid, 07/23 demand sent, 07/24 file assembled). Lead with
  THIS-period activity; do not recap history the attorney already knows.
- **Important Dates**: he KEPT only the 2 that matter now (demand response deadline; SOL).
  CUT "defendant's response — not yet running" and the "¶35 threshold" line. Non-dates and
  not-yet-live items don't belong here.
- **Notes / Reminders**: he DELETED the entire section. Open legal questions / flags
  (arbitration path, CLCA ¶34.D, security-deposit §1950.7) do NOT go in the weekly Case
  Update — they are raised in SEPARATE direct correspondence to the attorney. Keep the
  weekly recap lean and factual, not a place to surface analysis or asks.
- Kept verbatim: To Hernán / cc Cassie + Joe, the subject, the closing line; used the
  preset Gmail signature (fetched via `gws gmail users settings sendAs`, appended to the
  HTML body since API drafts don't auto-insert it).

**CB Kitchen and Bathroom, Inc. v. Zelaya (labor, FILED, SECOND weekly = delta, 08/03/2026) — baseline→delta:**
Week 1 was a full baseline recap (filing → present). Week 2 Klaus cut it hard to the delta —
this is the definitive example that **once a case's baseline recap has gone out, every later
weekly shows ONLY the past ~7 days, even a long-history filed case.**
- **Timeline**: only the ONE new event from the past week (07/27 — Hernán vacated the 07/29
  deadline; wait for the amended complaint). He re-listed NONE of the pre-existing history.
- **Intro line kept verbatim** ("Full recap of … from the filing of the complaint through
  today") — he does NOT rewrite the opener for a delta week, even though the Timeline is now
  one line. Leave it.
- **Important Dates**: kept the standing forward list (responsive-pleading due, CM-110 due,
  CMC) but stripped ALL strategy prose → `label: date (one short clause)`. My verbose "HELD
  pending the amended complaint; do not answer/demur/default per LaSalle…" was cut. Dates are
  dates, not analysis.
- **Notes / Reminders**: cut to the ONE genuinely-pending item ("Awaiting plaintiff's amended
  complaint; response deadline recalendared once served"). CUT: the now-RESOLVED deadline-
  conflict item, the internal payroll-records request, and the jury-fee reminder. Rule: drop
  what got resolved this week, and keep internal tactical asks OUT (separate correspondence).
- **Strategy in ONE sentence**, no case citation / rationale — the attorney authored it and
  doesn't need it recited back.

## Output — create the Gmail DRAFT (do NOT send)

**THE FORMAT below is authoritative — it is what Klaus actually sends** (verified against
the Bo Tao / Yi Cong / Guolin Zhao / Mudong Huang updates he sent 07/26/2026). It is a
**"Case Update" recap**, NOT a "Week of" sectioned memo — do not use Client/Incident /
Litigation-status section labels; use the Timeline structure.

### Draft — to Hernán (English)
- **to:** `Hernán Simó <hernan.s@lingtulaw.com>` · from klaus@
- **cc:** `"Shenqi Cai, Esq." <cassie@lingtulaw.com>, Joe Wu <joe@lingtulaw.com>` (always)
- **subject:** `<Client> v. <Lead Defendant> - Case Update | Case No. <#>`
  (if not yet on file: `Case No. Pending` / `Case No. Pending (Re-filing)`)
- **Continue the SAME email thread each week** — reply into the prior week's "Case Update"
  thread for that case, don't start a new one. Closing line is literally:
  *"I will continue weekly update case recap in this email thread, and please let me know if anything looks off."*
- **body — build it as REAL HTML. 🔴 NEVER use Markdown asterisks (`*text*`).** In an
  email `*Timeline*` renders as the literal characters `*Timeline*`, NOT bold. The draft
  MUST be an HTML alternative part with actual tags. This exact skeleton:
  1. `<p>Hi Hernán,</p>`
  2. `<p>Full recap of <Client> from the date of loss through today.</p>`
  3. **Timeline** — header as `<p style="font-style:italic;font-weight:bold">Timeline</p>`,
     then one `<p>` per event, each led by the **bold date** in `<b>` tags:
     `<p><b>MM/DD/YYYY</b> — <what happened></p>`, chronological.
  4. **Important Dates** — bold-italic header `<p>`, then a `<ul>` with one `<li>` per date,
     the **label bolded**: `<li><b>Defendant's Response due:</b> 08/17/2026</li>`
     (SOL; response/answer due; CMC + CMC-Statement due; hearing/eval dates).
  5. **Notes / Reminders** — bold-italic header `<p>`, then an `<ol>` of open items.
     *(Per the Brian Wu calibration above, OMIT this whole section for a pre-filing case
     whose attorney already has the background.)*
  6. Closing line as its **own** `<p>` — the verbatim line above. It must NOT end up as a
     `<li>` inside the Notes/Important-Dates list; close the list first, then the `<p>`.
- **signature:** append the mailbox's **preset HTML signature verbatim** — fetch it live:
  `gws gmail users settings sendAs list` → the default `klaus@lingtulaw.com` entry's
  `signature` HTML → paste that raw HTML at the end of the body `<div>`. Do NOT hand-type a
  plain-text `Klaus Liu | Paralegal` block (API drafts don't auto-insert the signature, and
  a re-typed one drifts from the real one). The preset already carries the paralegal title,
  firm address, O/D/F line, CCR 10205.6(b) disclaimer, and confidentiality notice.
- **Create the draft** by building a raw MIME message (`EmailMessage`: `set_content(<plain
  fallback>)` + `add_alternative(<html>, subtype="html")`), base64url it into
  `{"message":{"raw": …, "threadId": <thread>}}`, and `gws gmail users drafts create`
  (or `drafts update` to fix an existing one). Preserve `In-Reply-To` + `References` from the
  prior message in the thread so it stays threaded.

### (Optional) Klaus self-reminder — 中文, to `klaus@lingtulaw.com`
Only if Klaus asks. `【每周提醒】<Client> <案件类型> <Case No.> — 本周待办` · 3–7 条待办带截止日/状态.
Klaus's actual weekly deliverable is the ONE English Case Update above; don't create the
中文 draft by default.

## House rules
- Draft-only. Never send, never post to Chat, never e-file. Klaus sends everything.
- Never fabricate a date, case number, or fact. If a field is blank in the file, say
  "unknown / not yet on file" rather than guessing.
- Client-facing tone rules do NOT apply here — these are internal attorney/self notes;
  keep the Hernán draft crisp and professional.
- Money/coverage figures: quote only what the file shows.

## Known reference (Yi Cong test case)
- Client Yi Cong (DOB 01/30/1995), Gofo delivery worker, Corona CA.
- DOL 04/12/2026 ~9:41am, 950 N Duesenberg Dr Apt 6210, Ontario CA 91764 (Camden Landmark Apts).
- Defendant **Rhea Edpao** (tenant/dog owner); landlord **Camden Landmark LLC** (DOES 11–20).
- Rottweiler, unprovoked, right shoulder/arm, Animal Control **Level 2**, Bite No. B26-000401.
- **Case No. CIVSB2619725**, San Bernardino Superior (Justice Center); One Legal order #35058958.
- Complaint filed/accepted **07/09/2026**; Def served **07/16/2026**, POS-010 signed **07/20/2026**.
- POE/spoliation letter to Camden Landmark (06/17/2026) **USPS-returned undelivered 07/13/2026** → re-serve.
- Key evidence: owner's **Ring doorbell video**. SOL **04/12/2028**.
- Separate, unrelated matter for same client: auto PI `Yi Cong / Zouting Yu 03/20/2026` — do not conflate.
