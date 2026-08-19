---
name: file-complaint
description: >-
  Prepare the civil-complaint FILING PACKAGE for 凌图律所 / Lingtu Law (Law Office
  of Shenqi Cai APC) — fill the Summons (SUM-100), Civil Case Cover Sheet (CM-010),
  and (for LA County) the Civil Case Cover Sheet Addendum & Statement of Location
  (CIV 109) from the firm's Drive templates, ready to e-file. Use this skill
  whenever the attorney has drafted a complaint and the next step is立案 / filing:
  triggers include "prepare the filing package", "prepare summons and cover sheet",
  "fill the SUM-100 / CM-010 / CIV 109", "get this ready to file", "立案文件",
  "准备起诉文件", "/file-complaint" for a named case, or dropping a drafted
  Complaint into a case folder and asking to prep the court forms. Scope v1: Los
  Angeles County, personal-injury (PI) cases. It does NOT draft the complaint
  (the attorney does) and NEVER e-files or submits — it prepares fillable PDFs and
  leaves the case number, signature, and date blank. Always trigger for any
  "prepare/fill the filing forms" request for a case whose complaint is ready,
  even a partial one.
---

# File Complaint — Prepare the LA County PI Filing Package

> **Every complaint → translate for the client before filing.** Once the complaint is
> finalized, run the **`complaint-client-translation`** skill: Chinese translation
> (**PDF only — never docx**) + a bilingual client email (Chinese first, then English)
> for the client to confirm the facts. **That client email ALWAYS Cc's Hernán
> (hernan.s@lingtulaw.com).** Draft-only; Klaus sends. (Klaus's standing rule, 2026-07.)

Given a case whose **Complaint is already drafted by the attorney**, this skill
produces the court forms needed to file it, matching the firm's house format.

**It prepares (never files):**
- `1 - Summons.pdf` (SUM-100)
- `3 - Civil Case Cover Sheet.pdf` (CM-010)
- `4 - Civil Case Cover Sheet Addendum and Statement of Location.pdf` (CIV 109)
- copies the drafted complaint in as `2 - Complaint.pdf`
- writes a `0 - READ ME - Filing Checklist.txt`

Leave the **case number, attorney signature, and date blank** — those are added at
filing. Never submit, e-file, or drive the EFSP.

## Inputs

A case folder (local `~/Downloads/...` or the Drive case folder) that contains the
attorney's drafted **Complaint** (PDF or docx) and usually the **intake sheet**
(`.xlsx`). If the user only names a client, find the case folder the way other
Lingtu skills do (Drive search by name), and confirm with the user before proceeding.

## Step 1 — Read the complaint, extract the case data

Read the drafted complaint (it is the source of truth — the caption and body
already state everything). Extract:

- **Plaintiff(s)** — copy the caption's plaintiff block **VERBATIM** for the SUM-100
  (`plaintiff` in config), incl. the exact minor/GAL wording, e.g.
  `MUDONG HUANG, a minor, by and through his Guardian Ad Litem, BAIYUN JIANG; and BAIYUN JIANG, individually`.
  Match the complaint's own capitalization ("Guardian Ad Litem" vs "ad Litem"). Also
  note each plaintiff's city of residence (for the CIV 109 reason if it applies).
- **Defendant(s)** — copy the caption's defendant block **VERBATIM** incl.
  `, an individual` (or `, a business entity`, etc.) after each name and the DOE range,
  e.g. `CHELSEA PINPIN, an individual; LOUIS ARCA, an individual; MICHAEL A. CABANALAN, an individual; and DOES 1 through 50, inclusive`.
  **Never abbreviate defendants to "et al."** — they must be named for service. The
  SUM-100 caption boxes auto-wrap to the field width (fill_forms.py), so long
  multi-defendant / minor-by-GAL captions fit on 2–3 lines; do not hand-truncate.
- **Case caption / short title** → `ZHAO v. VELAZQUEZ` (LAST v. LAST)
- **Incident address** (the "Subject Property" / where it happened) incl. city + ZIP
- **Number of causes of action** (count the CAUSE OF ACTION headers)
- **Case type** → for v1 this is PI; note the specific tort (dog bite, slip/fall,
  auto, etc.) to pick the CIV 109 action code (see reference).

Cross-check the incident city/ZIP against the intake if anything is ambiguous.
**Do not confuse the incident address with the firm's address** (the firm is at
City of Industry, CA 91746 — that is never the incident location).

## Step 2 — Determine the filing court (LA County)

LA County assigns PI cases to the district **where the incident occurred** (per the
5/17/2024 General Order — the old central "PI Hub" model is retired). You do NOT
guess the district from geography.

Use the LASC **Filing Court Locator** with the incident **city + ZIP**:
`https://www.lacourt.ca.gov/pages/lp/online-services/tp/os-court-forms-and-filing/cp/os-filing-court-locator`
(direct form: `https://www.lacourt.ca.gov/filinglocatornet/ui/filingsearch.aspx`).
Read the **Unlimited Civil** column → that is the **courthouse**. Click it to see its
**district** (e.g. Norwalk Courthouse → Southeast District). If the locator is down,
drive it with Claude-in-Chrome, or confirm with the user. See
`references/la-county-pi.md` for the courthouse→district→address table for common
PI ZIPs.

Record: courthouse name, courthouse street address + city/zip, and district.

## Step 3 — Get the templates from Drive

Pull the firm's pre-filled templates from the **Litigation Forms** Drive folder
(id `1XWPPpjckqzcxus2A8BuNJKNt8BwY6fHb`). Download to a scratch dir with gws
(`scripts/get_templates.sh` does this):

- `cm010(Hernan).pdf`  → id `1bcU_7BhFx-XPgzASI_-RQcOp2hNrVrzj`
- `sum100(Hernan).pdf` → id `1eCAnesHkpmn2sVXleIgLVgaCIr4XPyi5`
- `LASC CIV 109.pdf`   → id `19U8ASWcSwDXOXwGo-wGmdOo6ICwESOyT`

The CM-010 and SUM-100 templates already carry the attorney block
(**Hernán S. Simó (SBN 354175)**, accented). The fill script preserves it — never
overwrite it. If a different attorney is handling the case, get their template
instead (this is a v1 limitation; ask the user).

## Step 4 — Build the config

Write a `config.json` for `scripts/fill_forms.py`. Court format follows the house
style: SUM-100 line 1 = courthouse **name**, line 2 = street + city/zip; CM-010
branch = courthouse **name**.

```json
{
  "case_short_title": "ZHAO v. VELAZQUEZ",
  "plaintiff": "GUOLIN ZHAO",
  "plaintiff_for": "Plaintiff Guolin Zhao",
  "defendant_block": "JORGE VELAZQUEZ; and DOES 1 through 50, inclusive",
  "case_name": "GUOLIN ZHAO v. JORGE VELAZQUEZ",
  "county": "LOS ANGELES",
  "courthouse_name": "Norwalk Courthouse",
  "courthouse_street": "12720 Norwalk Blvd.",
  "courthouse_city_zip": "Norwalk, CA 90650",
  "district": "Southeast",
  "amount": "unlimited",
  "num_causes": "3",
  "attorney_print_name": "Hernán S. Simó",
  "incident_address": "7653 Salt Lake Ave.",
  "incident_city": "Huntington Park",
  "incident_state": "CA",
  "incident_zip": "90255",
  "civ109_action_code": "2301",
  "civ109_reason": "4",
  "case_type_tooltip": "Other PI/PD/WD (23)",
  "templates": {
    "sum100": "<scratch>/sum100.pdf",
    "cm010":  "<scratch>/cm010.pdf",
    "civ109": "<scratch>/civ109.pdf"
  },
  "out_dir": "<case folder>/Filing Package"
}
```

- `amount`: "unlimited" when damages exceed $35,000 (the norm for injury cases),
  else "limited".
- `civ109_action_code` + `civ109_reason`: pick from `references/la-county-pi.md`
  (dog bite / premises = `2301`, reason `4`; generic PI = `2304`, reason `4`).
- `case_type_tooltip`: the CM-010 Item 1 box; PI = `Other PI/PD/WD (23)`. The script
  finds it by tooltip, so it works whether the form calls the field CheckBox23 or
  Item1Check[5].

## Step 5 — Run the fill script

```bash
python3 scripts/fill_forms.py config.json
```

This strips the XFA layer, generates real appearance streams, checks the right
boxes, stamps the CIV 109 Column B action box, and preserves the pre-filled
attorney block. See `references/la-county-pi.md` for why each of those steps
matters (XFA hybrids, form-revision field-name drift, non-fillable CIV 109
checkboxes).

## Step 6 — Verify by rendering (do not skip)

These Judicial Council forms render as garbage in poppler/pdftoppm — **use
Ghostscript**. Render each page you filled and actually look at it:

```bash
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r120 -dFirstPage=1 -dLastPage=1 \
   -sOutputFile=chk.png "<out_dir>/1 - Summons.pdf"
```

Confirm: defendant/plaintiff, court info, the checked case-type box, complex=No,
monetary, causes count, class=No, and — on CIV 109 — the ☒ in the correct Column B
action box, reason box, incident address, and district. If a checkbox didn't land
(e.g. the CIV 109 stamp is off for a new form revision), fix the coord in the
script's `CIV109_ACTION_XY` map and re-run.

## Step 7 — Assemble the package

In `<out_dir>` (default `<case folder>/Filing Package`):
1. `1 - Summons.pdf`, `3 - Civil Case Cover Sheet.pdf`,
   `4 - Civil Case Cover Sheet Addendum and Statement of Location.pdf` (from the script)
2. Copy the drafted complaint in as `2 - Complaint.pdf`
3. Write `0 - READ ME - Filing Checklist.txt` — what's filled, what's left blank
   (case #, signature, date), and the filing steps (e-file via One Legal → the
   determined courthouse; first-paper fee ~$435; serve conformed copies).

**Naming convention (house style):** documents the court sees are named by their
plain document type, in filing order — no form codes (SUM-100/CM-010) and no
"(filled)"/"(draft)" suffixes. For the internal case folder you may also keep a
`ZHAO v VELAZQUEZ - Summons.pdf`-style copy, and after filing save the conformed
versions with a `(Conformed <date>, Case No. ___)` suffix.

Deliver the folder to the user. Do not e-file. If the case is in a county other
than LA, or the attorney isn't Hernán, flag it — v1 covers LA County PI with the
Hernán templates only.
