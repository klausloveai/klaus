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
- **Which DOE number** → decide by the person's ROLE, matching how the complaint blocks its Does. In the house dog-bite complaint: **DOES 1–20 = dog owner/keeper/harborer**; **DOES 21–50 = property owner/landlord/manager**. Take the next unused DOE in the block that fits the person's role (a dog owner → DOE 1, DOE 2, …; a landlord → DOE 21, …). Confirm the number with Klaus/Hernán.

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
