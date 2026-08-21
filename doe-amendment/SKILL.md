---
name: doe-amendment
description: >-
  Draft a CIV 105 (Amendment to Complaint — Fictitious/Incorrect Name) PLUS the
  matching First Amended Summons (SUM-100) to ADD a newly-identified defendant to a
  凌图律所 / Law Office of Shenqi Cai (Hernán Simó / dog-bite / PI / litigation) case by
  substituting their true name for a DOE. Use whenever a later record (Animal Control
  report, deed, police report, discovery) reveals the real name of a defendant sued as a
  DOE and the next step is to bring them in: triggers include "DOE amendment", "add a
  Doe defendant", "CIV 105", "amend to add <name>", "amended summons", "first amended
  summons", "§474 / 474 Doe amendment", "加被告 / 把真名加进去 / DOE 改真名", "prepare the
  amendment and summons for <name>", "/doe-amendment" for a named case. It DRAFTS/PREPS
  ONLY — produces flattened, sign-ready PDFs to ~/Downloads, leaves the CIV 105
  DATE+SIGNATURE blank for the attorney and the summons DATE/Clerk blank for the court,
  and NEVER e-files. Fictitious-name (§474 Doe), NOT incorrect-name — this ADDS the new
  defendant, it does not replace an existing one. Always trigger for any "prepare the DOE
  amendment / amended summons" request, even a partial one.
---

# doe-amendment — CIV 105 + First Amended Summons (add a DOE defendant)

When you sue "DOES 1–50" and later learn a DOE's true name, you bring that person in by a
**CCP §474 fictitious-name amendment**. Two documents, filed together, then served:

1. **CIV 105 — Amendment to Complaint (Fictitious/Incorrect Name)** — LA local form.
   Check **Box 1, "FICTITIOUS NAME (No Order required)"**: substitute the true name for
   the DOE. No filing fee, no court order. Signed by the attorney.
2. **First Amended Summons (SUM-100)** — a new summons naming the added defendant, with
   the **NOTICE TO THE PERSON SERVED** box **2** checked ("as the person sued under the
   fictitious name of") specifying the DOE number. §474 bars a later default without this
   endorsement. The clerk issues it (stamps Date/Clerk).

**This ADDS a defendant; it does NOT replace one.** That is why it is the **fictitious**
box, not the **incorrect-name** box: incorrect-name = the same party was misnamed
(replace); fictitious = a previously-unknown DOE is now identified (add). Existing named
defendants stay in the case. See [[litigation_service_of_process]].

## Court variant — which form (READ FIRST)
The Amendment form is **county-specific**; pick by the case-number prefix:
- **`CIVSB…` → San Bernardino Superior Court → local form SB-16778** ("Amendment to
  Complaint"), top **FICTITIOUS NAME (No order required)** section. Use
  `scripts/make_sb_amendment.py` (below). This is the default for Hernán dog-bite cases.
- **LA (`…NWCV…`, etc.) → CIV 105** (LA local form) via `make_doe_amendment.py`.
- Other counties: find that county's Doe/fictitious-name amendment form and add a variant.

### San Bernardino SB-16778 (`make_sb_amendment.py`)
- **Template source (Klaus's standing rule, 2026-08-20):** the SB-16778 blank is pulled
  **fresh at run time from Klaus's Drive file** so template edits flow through automatically —
  `Amendent to Complaint.pdf`, id **`184p3wdnweubmMwkuU4sB8EJQ5cUgMDgj`**. Falls back to the
  bundled cache `assets/SB-16778_blank.pdf` if Drive is unreachable. (gws forbids `--output`
  outside cwd → the script fetches with a relative name inside a tempdir.)
- **One run can add several Does** — config takes a `defendants` LIST; each yields its own
  SB-16778 **and** its own First Amended Summons endorsed with that Doe number (item 2). It
  reuses `make_doe_amendment.make_fa_summons` for the summons.
- **Doe block is per-complaint, not fixed.** Read the filed complaint's Doe allocation. Yi Cong
  v. Edpao: **Does 1–10 = dog owner (strict liability, Civ. Code §3342)**, **Does 11–20 =
  premises/landlord**. A landlord goes in 11–20, never 1–10. Confirm the number with Hernán.
- **Confirm each entity's exact legal name + agent for service via CA Secretary of State
  (bizfileonline.sos.ca.gov) before finalizing** — the exact legal name goes on the form; the
  agent is needed for service. Never fabricate the agent. Run: `python3
  scripts/make_sb_amendment.py <config.json>` (schema in the script header).
- Post-filing: service + POS due **within 30 days of filing** (calendar it); the summons/POS
  must carry the fictitious-name notice or no default can be taken.

## Summons court block — repeat the issued summons verbatim (Klaus, 2026-08-20)
The SUM-100 "name and address of the court" block has only **two usable line slots**,
and **both must stop before the CASE NUMBER box** (its left edge is **x=362.8**). A long
one-line court name prints straight through the case number.
- **If the case already has an issued/accepted summons, copy its court block verbatim** —
  pass `issued_summons_pdf` in the config and the script scrapes it (it also lifts the
  attorney line, so the amended summons matches what the court accepted). It prints
  `court block (issued summons): …` so you can eyeball what it took.
- **If there is no issued summons**, follow that format, keep it inside the box, and wrap
  onto the second line — never let a value run past x≈358.
- Yi Cong's accepted split, as the worked example: line 1 = `Superior Court of California`,
  line 2 = `County of San Bernardino, 247 West 3rd Street, San Bernardino, CA 92415-0210`.
  Note it is **not** "Superior Court of California, County of San Bernardino" on one line.
- `_draw_fitted()` shrinks the font as a backstop, but a correct split beats shrinking.

## Draft-only (hard rule)
Prep only. Output flattened PDFs to **~/Downloads**. Leave CIV 105 **DATE + SIGNATURE**
blank (the attorney — usually Hernán — signs). Leave summons **DATE / Clerk / Deputy**
blank (the court issues). **Never e-file, never serve.** Klaus e-files (via One Legal) and
arranges service.

## Inputs to gather (from the case, confirm with Klaus)
Read the case's **filed/conformed complaint** (source of truth) + intake sheet:
- **Attorney of record** (name, SBN, firm, address, tel, fax, email) — from the complaint caption.
- **Court** name + street address + branch/district — from the conformed complaint / One Legal acceptance. (e.g. case no. prefix `NWCV` = Norwalk Courthouse, SE District.)
- **Case number.**
- **Plaintiff** name.
- **Complaint's DEFENDANT caption** verbatim (e.g. `JORGE VELAZQUEZ; and DOES 1 through 50, inclusive`) — this is the pre-amendment caption; it goes on the CIV 105 unchanged.
- **The new defendant's true name** (from the Animal Control report / deed / etc.).
- **Which DOE number** → **read the FILED complaint's own Doe allocation. Never assume a
  house default — it varies case to case.** Open the complaint, find how it blocks its
  Does by theory of liability, and take the next unused Doe in the block matching this
  person's ROLE. Worked examples:
  - *Yi Cong* (CIVSB2619725): Does **1–10** = dog owner (strict liability, Civ. Code
    §3342); Does **11–20** = premises/landlord. Camden entities → Does 11 and 12.
  - *Guolin Zhao* (26NWCV02260): pleads Does 1–50; the dog owner went in at Doe 1.
  These differ — that is the point. Confirm the number with Hernán before generating.

Then confirm the DOE number and true name before generating.

## Two captions — do NOT confuse them
- **CIV 105 DEFENDANT field** = the complaint's caption **unchanged** (e.g. `JORGE
  VELAZQUEZ; and DOES 1 through 50, inclusive`). The form's BODY does the work
  (DOE N → true name). Do **not** add the new name to the CIV 105 caption.
- **Summons NOTICE TO DEFENDANT** = the complaint's named defendants **plus** the new
  one (e.g. `JORGE VELAZQUEZ; BENJAMIN VELAZQUEZ LOPEZ; and DOES 1 through 50,
  inclusive`), because the summons is served on and identifies the new defendant. The
  DOE endorsement lives in the person-served box (item 2 = the DOE number).
  Klaus's house preference: name the new defendant AND keep `DOES 1 through 50` to match
  the complaint boilerplate. (A cleaner variant "sued herein as DOE N; and DOES N+1
  through 50" is acceptable — offer it, but default to matching the complaint.)

## How to generate
1. Build a config JSON (see schema below) from the gathered inputs.
2. Run:
   ```
   python3 ~/.claude/skills/doe-amendment/scripts/make_doe_amendment.py <config.json>
   ```
3. It writes two flattened PDFs to `output_dir`:
   - `<prefix> - CIV 105 Amendment to Complaint (<DOE N true name>).pdf`
   - `<prefix> - First Amended Summons (<DOE N true name>).pdf`
4. Render each (macOS: `gs -sDEVICE=png16m -r120 -o out.png in.pdf`; the SUM-100/CIV 105
   fonts are non-embedded Arial, so **ghostscript renders correctly but poppler/pdftoppm
   shows tofu** — use gs). Eyeball: fictitious box checked, DOE number + true name, item 2
   checked with the DOE number, accents intact, DATE/signature blank.
5. Present to Klaus. On his go, the flow is: **Hernán signs the CIV 105 → e-file CIV 105 +
   summons via One Legal (Amendment to Complaint = no fee; summons issued by clerk) →
   personal service on the new defendant** with the packet **issued Amended Summons +
   Complaint + filed CIV 105**. Instruct the server to log GPS + a door photo per attempt.

## Config schema
```json
{
  "output_dir": "/Users/klaus/Downloads",
  "file_prefix": "Guolin Zhao",
  "case_number": "26NWCV02260",
  "plaintiff": "GUOLIN ZHAO",
  "attorney": {
    "name": "Hernán S. Simó", "sbn": "354175",
    "firm": "Law Office of Shenqi Cai APC",
    "addr1": "13191 Crossroads Pkwy N, Suite 295",
    "addr2": "City of Industry, CA 91746",
    "tel": "(626) 479-2207", "fax": "(626) 479-2207",
    "email": "hernan.s@lingtulaw.com"
  },
  "court_name": "Norwalk Courthouse",
  "court_address": "12720 Norwalk Blvd, Norwalk, CA 90650",
  "court_branch_note": "Southeast District",
  "complaint_defendant_caption": "JORGE VELAZQUEZ; and DOES 1 through 50, inclusive",
  "summons_defendant_caption": "JORGE VELAZQUEZ; BENJAMIN VELAZQUEZ LOPEZ; and DOES 1 through 50, inclusive",
  "doe_number": "DOE 1",
  "true_name": "BENJAMIN VELAZQUEZ LOPEZ"
}
```
Optional: `summons_attorney_line` to override the auto-built attorney line on the summons.

## Assets & implementation notes
- `assets/FA-Summons-template.pdf` — Hernán's First Amended Summons template (Drive
  shared drive "Legal Form": file id `1mpnI1wWxt_NGfDnBFCBoe_wikMas7reA`). It already
  carries the centered **"FIRST AMENDED SUMMONS"** heading. The script strips its widget
  fields (dropping the prior case's pre-filled Pasadena court + attorney), flattens, then
  overlays this case's values. To refresh the template, re-download that Drive file over
  the asset.
- `assets/CIV105_blank.pdf` — official LASC CIV 105 (`lascpubstorage.blob.core.windows.net/
  forms/Forms Comprehensive List/1886-LASC CIV 105.pdf`).
- **Why overlay, not AcroForm fill:** both forms' AcroForm fonts mangle accents (é/ó → ?)
  and drop the checkbox mark when flattened by qpdf. The script flattens a clean base
  first, then draws every value with an embedded Unicode TTF at the exact field rects.
- Requires: `qpdf`, `reportlab`, `pypdf`, and the macOS Arial TTFs. Render/verify with
  `ghostscript` (not pdftoppm).

Related: [[litigation_service_of_process]] · [[file-complaint]] · [[gal-appointment]] ·
[[onelegal_complaint_sop]].
