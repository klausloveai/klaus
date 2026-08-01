---
name: gal-appointment
description: >-
  Prepare the Guardian ad Litem (GAL) appointment forms for a MINOR (or legally
  incapacitated) plaintiff in a 凌图律所 / Law Office of Shenqi Cai (Hernán Simó /
  dog-bite / PI) litigation case — fill BOTH the Application (CIV-010/FL-935) AND the
  proposed Order (CIV-011/FL-936) from the firm's Judicial Council templates, ready to
  file alongside the complaint. Use whenever a case has a minor plaintiff and the next
  step is appointing the parent as guardian ad litem: triggers include "guardian ad
  litem", "GAL", "CIV-010", "CIV-011", "appoint the mother/parent as GAL", "监护人申请",
  "诉讼监护人", "prepare the GAL forms", "/gal-appointment" for a named case, or when a
  complaint names a minor "by and through his/her Guardian Ad Litem". It does NOT draft
  the complaint and NEVER e-files — it produces flattened, signature-ready PDFs and
  leaves the case number, signatures, and dates blank. Effective 1/1/2024 the Judicial
  Council SPLIT the old combined form into two: CIV-010 = Application, CIV-011 = Order,
  and BOTH must be filed together. Always trigger for any "prepare the GAL / CIV-010 /
  CIV-011" request for a minor-plaintiff case, even a partial one.
---

# gal-appointment — Guardian ad Litem forms (CIV-010 + CIV-011)

A minor cannot sue in their own name; a parent must be appointed **guardian ad litem
(GAL)** to represent the child. The **clerk will NOT issue the Summons without the GAL
paperwork.** Effective **January 1, 2024** the Judicial Council split the old combined
"Application AND Order" into two mandatory forms — **you file BOTH together**:

- **CIV-010/FL-935 — Application** → signed by the **attorney** (item 7) and the
  **parent** (as applicant + as proposed GAL — two signatures, same person).
- **CIV-011/FL-936 — Order** → a *proposed order*; the **judge** signs it. No party signs.

This skill fills both from the firm's templates, **flattens** them (so the values show
in every viewer, incl. macOS Preview), stamps the **full caption** (all parties named,
per the complaint), and leaves **case number, signatures, and dates blank**. Draft/prep
only — never e-file.

## Inputs
The case's **finalized complaint** (source of truth for caption, minor's DOB, parties)
and the **intake sheet** (parent/GAL name, address, phone, email). If only a client
name is given, find the case folder the way other Lingtu skills do and confirm with Klaus.

## Step 1 — Gather the data from the complaint + intake
- **Caption — SHORT form on these small JC caption boxes** (Hernán's directive, 2026-07):
  - Plaintiff: `<MINOR>, a minor, etc., et al.` (the "etc." = the GAL wording, "et al." = the
    parent-plaintiff), e.g. `MUDONG HUANG, a minor, etc., et al.`
  - Defendant: `<FIRST DEFENDANT>, et al.`, e.g. `CHELSEA PINPIN, et al.`
  - **Why short, not the full list:** the caption box is one 245pt line per party; the full
    verbatim defendant list overflows onto the "Other Parent/Party" line and looks messy.
    CRC 2.111 permits the short caption on a subsequent paper. **The SUMMONS (SUM-100) still
    names every defendant in full** — that's for service, a different form (see file-complaint).
- **Minor**: legal name + **date of birth** (MM/DD/YYYY) — from complaint ¶ / intake ID.
- **Parent / proposed GAL**: name, home address, phone, email; **relationship** to the
  minor (`Mother` / `Father`). The GAL must be a parent, guardian, conservator, party,
  the 14+ minor, or (UPA actions) an adult relative — a minor may not self-represent.
- **Attorney block** = Hernán S. Simó, SBN 354175 … **Fax = 626-479-2207 (SAME as phone)**,
  never the 626-240-2046 firm fax (🚩 see [[litigation-doc-header-phone]]).
- **Attorney for** = **all** plaintiffs, e.g. `Plaintiffs Mudong Huang, a minor, and Baiyun Jiang`.
- **Court** = the complaint's district/courthouse (LA PI → determined in file-complaint;
  e.g. Northeast District → Pasadena Courthouse, 300 East Walnut Street, Pasadena, CA 91101).

## Step 2 — Build the config
Copy `scripts/config.example.json` and fill it in. Notes:
- `summons_issued`: **false** when filing the GAL app *with/before* the complaint (checks
  CIV-010 item 5a "summons has not been issued"); `true` only if the minor is a defendant
  or the summons already issued (rare here).
- `ex_parte`: **true** for the normal parent-for-minor appointment (no hearing).
- `civ010_name` / `civ011_name`: house filenames (see Step 5). `out_dir`: where to write.

## Step 3 — Run the fill script
```bash
python3 scripts/fill_gal.py config.json
```
This fills both forms and **flattens** them with `qpdf --generate-appearances
--flatten-annotations=all` (so text + ✖ checkboxes render everywhere — pypdf-only fills
look blank in macOS Preview). The short caption fits the box, so it is set as a normal
field (no stamping). Requires the `qpdf` CLI (`brew install qpdf`) and `pypdf`.

What it sets (verified against Hernán's 2026-07 review):
- **CIV-010**: EX PARTE; item 1 applicant + **1a "parent of" minor + 1d "a party to the
  suit"** (the parent is BOTH the minor's parent AND a plaintiff — check all that apply);
  item 2 GAL info; item 3 represented minor; item 4a minor + DOB; item 5a (summons not
  issued); **item 6c "has no guardian or conservator of the estate"**; item 7 attorney
  name; applicant name; **item 8b familial relationship = <relationship>** (e.g. Mother);
  item 9a "not aware of conflicts"; applicant consent name. Signatures + both dates blank.
- **CIV-011**: EX PARTE; **item 3 "all notices required by law have been given"** (minor is
  a plaintiff and the summons has not issued → no notice required, so the finding is proper
  and the judge need only date + sign); item 1 applicant + minor; item 4a minor + DOB; item
  5c "does not have a guardian or conservator of the estate"; item 6 GAL appointed for minor;
  **item 7 "is NOT" authorized to waive/disclaim substantive rights** (the protective option
  the bench expects for a minor — leaving it blank invites rejection). Hearing block (item 2),
  date, and the **judge's signature** left blank.

## Step 4 — Verify by rendering (do not skip)
JC forms render as garbage in poppler — use **Ghostscript**. Render every page and LOOK:
```bash
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r140 -sOutputFile=chk_%d.png "<out>/…CIV-010….pdf"
```
Confirm: full caption (all defendants visible, not clipped), DOB, the ✖ in items
5a/6c/8b(CIV-010) and 4a/5c(CIV-011), attorney block Fax = phone, correct courthouse,
and that all signature/date lines are blank. Run [[draft-check]] §C mentally.

## Step 5 — Deliver (house naming)
Save both to `~/Downloads/<Client>/` and, if it exists, the case's `Filing Package…`
folder using the filing-order names:
- `5 - Application for Appointment of Guardian ad Litem (CIV-010).pdf`
- `6 - Order Appointing Guardian ad Litem (CIV-011).pdf`
Also mirror the signature copies as
`<Client> - CIV-010 (GAL Application) for Hernan signature.pdf` and
`<Client> - CIV-011 (Proposed Order Appointing GAL).pdf`.
Update the filing checklist: clerk needs **CIV-010 + CIV-011** to issue the Summons;
file the proposed Order together with the Application.

## Guardrails
- **Prep only — never e-file.** Case number, signatures, dates stay blank.
- **File BOTH forms together** (Application + Order). Missing the Order gets rejected.
- **Flatten before delivering** (macOS Preview won't render un-flattened JC fields).
- **Caption = SHORT form** ("<MINOR>, a minor, etc., et al." / "<DEFENDANT>, et al.") so each
  party sits on one line and nothing overflows onto Other Parent/Party (Hernán's directive).
- **No fabrication** — DOB/names/relationship come from the complaint + intake ID; if a
  value is missing, flag it, don't guess.
- Templates: `assets/civ010.pdf`, `assets/civ011.pdf` (Judicial Council blanks, Rev/New
  Jan 1 2024). If the state posts a newer revision, drop it in `assets/` — the caption
  coords are read from the form itself, so stamping stays robust; re-verify field names.

See [[file-complaint-skill]], [[dogbite-file-complaint-skill]],
[[hernan-litigation-conventions]], [[draft-check-skill]].
