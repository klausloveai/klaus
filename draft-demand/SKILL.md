---
name: draft-demand
description: >-
  Draft (do NOT send) a pre-litigation DEMAND LETTER and assemble the full demand
  package for 凌图律所 / Lingtu Law Office (Law Office of Shenqi Cai APC). Trigger
  whenever any of these are mentioned: draft demand, demand letter, demand package,
  policy limits demand, settlement demand, 3P / UM / UIM demand, UM/UIM reasonable-value
  demand, early settlement demand, "写 demand", "做 demand package", "/draft-demand"
  for a named client. Typical invocation: a client/driver name (+ optional demand type
  and the assigned case manager). The skill finds the case in Drive, reads the intake
  sheet + medical records & bills + police report, auto-selects the correct template
  (3P / UM / UIM / Early-Settlement), fills every {{token}}, builds the damages tables
  with self-checked per-diem math, drafts the demand letter (docx + PDF), renames and
  assembles the exhibits into one bookmarked package PDF, and saves everything to a local
  client folder (and, on request, the Drive case folder). It DRAFTS ONLY — it never
  emails, faxes, files a claim, or updates a tracking sheet. Always trigger for any
  "draft a demand / build a demand package" request, even a partial one.
---

# Draft Demand (Lingtu Law)

Produce a **ready-for-review** demand package. **Draft only — never send.** Numbers and
injuries come strictly from the records; never invent them.

## Core rules — NEVER violate (a wrong number or a made-up fact can sink the claim)
1. **No fabrication.** Every injury, ICD code, MRI/imaging finding, diagnosis, provider,
   treatment date, visit count, dollar amount, carrier, claim #, adjuster, and policy limit
   must come from the actual records / bills / intake sheet / police report. If a value is
   not in the source, it does NOT go in the letter. Copy ICD codes and MRI impressions
   **verbatim** — do not paraphrase, round, or "fill in" plausible-looking ones.
2. **No missing information.** Every provider in the records gets a Past-Medical row; every
   bill total is captured; every exhibit referenced exists and is in the list; every header
   field (carrier, adjuster, claim #, DOL, limits, handler contact, deadline) is filled.
3. **Every number is verified twice.** Re-derive the per-diem from the real dates, make every
   table foot, and confirm the totals tables agree with each other. Run the QC script (Step 6.5).
4. **Flag, don't guess.** If something is unknown or assumed (deadline, a missing bill, an
   ambiguous date), say so explicitly in the review hand-off — never paper over a gap.

## Assets (bundled in this skill's `assets/`)
- `3P Demand Template.docx` — third-party policy-limits demand (full bad-faith / EXPOSURE).
- `UM Demand Template.docx` — uninsured-motorist (own carrier; hit-and-run / uninsured at-fault).
- `UIM Demand Template.docx` — underinsured-motorist (own carrier; after 3P limits exhausted).
- `Early Settlement Demand Template.docx` — quick good-faith early resolution (specific number, no EXPOSURE machinery).
- `Reference Sheet (ICD codes + optional future-care).docx` — common ICD codes + optional future-care procedures to copy from.
- `Client Impact Questionnaire (案件价值问卷).docx` / `.pdf` — bilingual form the firm sends the client to collect their real day-in-life experience (pain, work, sleep, activities, emotions); feeds the Pain & Suffering section. Also in Drive `2. Demand Letter Template`.
- `Assemble Package (tool).py` — merges the letter + exhibits into one bookmarked PDF.
- `qc_check.py` — automated QC: flags leftover tokens/red-notes/highlights, wrong-carrier cites, per-diem & totals math errors, cross-table mismatches, a wrong deadline weekday, and broken exhibit refs; prints every ICD/MRI/provider/number to eyeball against the source. Run it in Step 6.5.

Templates are TOKEN-based: every fill-in is `{{TOKEN}}` (yellow-highlighted); red italic `[...]`
notes are instructions to act on then delete. Masculine default — swap pronouns for a female client.
(Working masters also live in `~/Downloads/Lingtu Demand Templates/`; keep `assets/` in sync if edited.)

## Step 0 — Confirm scope
Get / confirm: **client name**, **demand type** (3P / UM / UIM / Early-Settle — infer if not given, see Step 3),
and the **handler + team** (for the closing contact). If the handler/team isn't given, ASK
(handler name, direct phone, and the team mailbox — claims@ / picase@ / piteam@lingtulaw.com).

## Step 1 — Locate the case in Drive
**Common invocation:** Klaus often says "find a case in the Drafting folder that has no demand yet
and write it." In that case, list the case folders in **`4. Drafting`** (id `1710DYUCyGB8iur-jF6fw96HuUmw9hZPz`),
check each one's `5#Folder-Demand Package`, and pick a case whose 5# folder has **no demand letter yet**
(empty, or only raw records). Confirm which one with Klaus before drafting.
Otherwise, search the PI Team shared drive for the named client's case folder (same locations as new-case / lor-send).
Identify: the **intake sheet** (the embedded gsheet), `4#Folder-Bodily Injury…` (records & bills),
`2#Folder-All Photos…` (police report, Dec page, photos/videos), `3#Folder-Property Damage…`,
and the `5#Folder-Demand Package` (where the finished package is saved — see Step 7).

## Step 2 — Read the data
From the **intake sheet**: client full name, gender, DOB/age at loss, date of loss, accident
location & facts (driver/passenger, vehicle yr/make/model, direction/road, how it happened),
1P & 3P carriers, adjuster name + email + claim #, **policy limits** (e.g. "30/60" → $30k/person),
SR-1 / liability status, the treating providers and treatment status.
From the **records & bills** (per provider): treatment period, **visit count**, **total billed**;
the **ICD codes** (from the chiropractic narrative's diagnosis list — copy ONLY what's there);
**MRI/imaging findings** (from the radiology report, if any).
From the **police report**: report #, parties, and the cited CVC violation (PCF).
Loss of income only if wage docs exist.

## Step 3 — Pick the template
- **3P** — at-fault driver identified and their carrier is on the claim (3P liability accepted/clear).
- **UM** — at-fault uninsured OR hit-and-run / phantom vehicle (claim against client's own carrier; arbitration framing). Tortfeasor = "Unknown Hit-and-Run Driver" if fled.
- **UIM** — client's own carrier, AFTER the 3P policy limits were tendered/exhausted (fill the prior-settlement recital).
- **Early-Settlement** — minor injury, treatment ongoing, client wants speed, or value clearly under the limit (insert a specific `{{DEMAND_AMOUNT}}`, not "policy limits").
When unsure, state your pick and reasoning.

## Step 4 — Fill the template (in place; preserve formatting)
Copy the chosen template to a working file and replace tokens via python-docx (download template
binary; edit; don't regenerate from scratch). Key fills:

> **ALWAYS use the firm letterhead.** Every demand ships on the firm's official letterhead (the
> Lingtu logo + City of Industry address block — it lives in the template's `word/header2.xml`).
> For a **bespoke / non-template matter** (e.g. an out-of-state or non-auto claim like an AZ premises
> case) do NOT hand-build a plain text header — start from a firm template `.docx`, **clear its body
> but keep the final `<w:sectPr>`** (so the header/footer logo letterhead survive), then write the
> custom content into the shell. python-docx: `for ch in list(doc.element.body): ch.tag.endswith('}sectPr') or doc.element.body.remove(ch)`.
> (Templates have no "Table Grid" style — add table borders via a `w:tblBorders` OXML helper.)

- Header/RE: `{{LETTER_DATE}}` (today), `{{CARRIER}}`, `{{ADJUSTER_NAME}}`, `{{ADJUSTER_EMAIL}}`,
  `{{ADJUSTER_TITLE_LAST}}`, `{{CLIENT_NAME}}`, `{{CLIENT}}` (e.g. "Mr. Li"), `{{DOL}}`,
  `{{ATFAULT_NAME}}` / `{{TORTFEASOR}}`, `{{CLAIM_NO}}`, `{{AGE}}`, `{{REPORT_NO}}`.
- **Opening summary**: `{{DEMAND_AMOUNT}}` (3P = "your insured's policy limits of $___"; early = the number) + `{{DEADLINE}}`.
- **Facts**: write the real accident narrative over the facts placeholder; keep the CVC liability
  paragraph but **bold+italic only the Vehicle Code section the police report cited** (e.g. § 22350);
  delete § 21703 if following-too-closely wasn't the factor.
- **Causation / low-impact** lines: keep if applicable; delete if there's relevant prior history.
- **Injuries**: fill the ICD table from the records ONLY (copy from the Reference Sheet as needed —
  never include codes the records don't support). Add MRI findings as bullets only if there was imaging.
- **Damages**: Past Medical = one row per provider (period / visits / billed / Bills-exhibit ref).
  Future Medical = **chiropractic + pain management by default** ($2,000 + $1,920 = $3,920); add
  injections/surgery ONLY if a PM/ortho report recommends them (copy rows from the Reference Sheet,
  cite that report). Loss of Income subsection only if wage docs exist (else delete it + the totals row).
- **Pain & Suffering / day-in-life:** fill the guided impact scaffold with concrete, personal facts —
  work, daily tasks, sleep, activities/hobbies, emotions/driving. Source from (a) the **records**
  (providers note work status, activity restrictions, functional complaints) and (b) the client's answers
  to the **Client Impact Questionnaire**. If the questionnaire hasn't been returned, draft from the records,
  keep it truthful (never invent), and flag the case manager to send the questionnaire to enrich it.
- **Per-diem (verify the math):** Initial = (days from DOL to end of active treatment) × 16 × $25;
  Subsequent = 365 × 16 × $10 = $58,400; Total P&S = Initial + Subsequent. Total Damages = Past Med +
  Future Med + (Loss of Income) + Total P&S. Demand the policy limit even if total value < limit.
- **Closing**: `{{HANDLER_NAME}}`, `{{HANDLER_PHONE}}`, `{{TEAM_EMAIL}}`; deadline = a **Monday ~30 days out**, 5:00 P.M. P.S.T.
- **Gender**: if female, swap he→she / his→her / him→her / Mr.→Ms. / man→woman.
- After filling: clear leftover yellow highlight & recolor any yellow font, and **delete every red `[...]` instruction**.
  (See [[demand_package_workflow]] for the python-docx helpers, the per-diem detail, and gotchas — e.g.
  don't blanket-replace "Insurance Company" or you corrupt case names; footnote text can split across runs.)

## Step 5 — Exhibits
Download the supporting PDFs and rename to the convention: **TCR first**, then per provider
**Records before Bills**, numbered sequentially:
`Exhibit 1 - Traffic Crash Report.pdf`, `Exhibit 2 - <Provider> – Records.pdf`,
`Exhibit 3 - <Provider> – Bills.pdf`, … then Property-Damage Photographs and Loss-of-Income docs.
Make the Past-Medical "Reference" column point to each provider's **Bills** exhibit.
If PD damage exists only as **videos**, extract still frames (imageio + imageio-ffmpeg; brighten with
Pillow) — 1–2 of the client's vehicle (+ the other vehicle if any). Embed 1–2 in the Facts section.

## Step 6 — Render
Convert the letter to PDF (`soffice --headless --convert-to pdf`). **Do the Step 6.5 gate before
assembling** — then build the merged package:
`python3 "assets/Assemble Package (tool).py" "<local package folder>"` → one bookmarked
`<Client> - Demand Package (MERGED).pdf` (Demand Letter + divider+exhibit per exhibit).

## Step 6.5 — Verification gate (run until clean, THEN once more)
Do not save or present until this passes. **Verification is iterative — fix, re-run, repeat.**

**A. Automated QC.** Run on the letter `.docx`:
`python3 "assets/qc_check.py" "<local package folder>/<Client> - <Type> Demand Letter.docx"`
- Resolve **every** `❌ FAIL` (leftover tokens/red-notes/yellow, wrong-carrier cites, per-diem
  or totals math, cross-table mismatch, wrong deadline weekday, broken exhibit ref), then **re-run**.
  Repeat until it exits `0`. After ANY later edit (even a one-word fix), run it again.
- Read every `⚠️ WARN` and confirm it's intentional (e.g. a real female client → masculine count
  should be ~0; "his or her" generic phrasing is fine).

**B. Source cross-check (the part a script can't do — this is the anti-fabrication pass).**
For each `ℹ️ VERIFY-AGAINST-SOURCE` line the script prints, open the actual source and confirm:
- **ICD codes** — every code in the table appears in the chiropractic/medical record's diagnosis
  list. No extras, none missing, copied exactly.
- **MRI/imaging findings** — match the radiology report word-for-word (levels, mm, side). Omit if
  the client declined imaging.
- **Provider rows** — provider name, treatment period, **visit count**, and **billed amount** each
  match that provider's bill exactly. Every provider that treated has a row (none dropped).
- **Per-diem dates** — initial range = DOL → end of active treatment; recount the days.
- **Header/claim data** — carrier, adjuster, claim #, DOL, policy limits match the intake sheet.

**C. Consistency sweep.** Client name, gender/pronouns, DOL, claim #, and the demand amount read
consistently from salutation to signature; the deadline is a Monday ~30 days out.

Only when A exits clean and B/C are confirmed do you proceed. Re-run QC on the FINAL docx one last
time before assembling the package.

## Step 7 — Save (DIRECT to the case's Drive 5# folder; don't leave files in Downloads)
**Default (Klaus's standing preference): deliver straight into the case's Drive `5#Folder-Demand Package`,
not to local Downloads.** Build locally in a temp scratch dir only because the tools need it, then upload
the deliverables to 5# and **delete the entire local working folder when done** — Klaus does not want
demand files accumulating in `~/Downloads`. (Only keep a local copy if Klaus explicitly asks.)

The **5# folder must contain ONLY these four deliverable types and nothing else**:
1. `<Client> - Demand Package (MERGED).pdf` — the bookmarked merged package
2. `<Client> - <Type> Demand Letter.pdf` — the letter
3. `<Client> - <Type> Demand Letter.docx` — the editable letter
4. `Exhibit 1 … N - <desc>.pdf` — the renamed exhibits

Upload with `gws drive files create … --params '{"…","supportsAllDrives":true}'` into the 5# folder id.
If 5# already contains raw/un-renamed duplicate records (often pre-loaded there), **trash them** so 5#
holds only the clean package — verify the originals still exist in `4#Folder-Bodily Injury` first.
Never leave scratch in 5# or Downloads: no `_src/`, no `intake.xlsx`, no `*.py` fill/build scripts,
no downloaded template, no raw un-renamed records (the raw records' home is `4#Folder-Bodily Injury`).

## Step 8 — Review gate (DRAFT ONLY)
Present the drafted letter (and merged package) for review. **Do not email, fax, file, or update any
tracking sheet.** Flag anything you had to assume (deadline, handler, demand amount, missing records).

## Dependencies
`gws` (Drive), python-docx, LibreOffice `soffice` (docx→pdf), pypdf + reportlab (merge/dividers),
imageio + imageio-ffmpeg + Pillow (PD video frames). Install python libs with
`pip install --user --break-system-packages …`. See [[cowork_path_snapshot]], [[demand_package_workflow]].
