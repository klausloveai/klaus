# Limited-Civil Court Rules (per county + contract subtype)

Per-county first-paper requirements for filing a **limited civil (≤ $35,000),
NON-PI, contract/collection** complaint. **"做一个记一个"**: only counties/subtypes
actually used are recorded. New one appears → verify against the court's own site,
then add it. Never fabricate a rule.

Every county needs, at minimum (statewide): **Summons (SUM-100)** + **Complaint** +
**Civil Case Cover Sheet (CM-010)**. Attorney-filed civil is **mandatory e-file**
(CRC 2.253(b)) via One Legal. Leave case #, signature, date blank.

---

## Los Angeles County — limited civil, contract/lease (status: IMPLEMENTED — verified on Brian Wu v. Azucanela LLC, 2026-07-27)

### The courthouse fork (decide FIRST)
LASC Local Rule 2.3(a)(2) routes limited civil by CRC 3.740 classification:
- **CRC 3.740 collections case** (sum stated certain ≤ $35,000, arising from a
  **credit** transaction; excludes tort, indemnity, recovery of property) →
  **Norwalk Courthouse**, 12720 Norwalk Blvd., Norwalk, CA 90650.
- **All other limited civil** (non-collection, non-UD, non-small-claims) →
  **MANDATORY Central District** → **Stanley Mosk Courthouse, 111 North Hill Street,
  Los Angeles, CA 90012** (limited-civil hub; Dept 94).

A lease/rent case that also pleads **indemnity and/or guaranty** (not a pure
sum-certain credit debt) is **non-collection → Stanley Mosk / Central**. Confirm the
complaint's venue paragraph says as much before filling.

### Forms + fill values (non-collection contract/lease → Central)
- **CM-010:** `"amount": "limited"` + `"case_type_tooltip": "Breach of contract/warranty (06)"`.
- **CIV-109** (SCLAC CIV 109, Rev 04/26 — mandatory addendum). Template Drive id
  `19U8ASWcSwDXOXwGo-wGmdOo6ICwESOyT` (in `get_templates.sh`). Contract subtypes /
  action codes (Column B) and their Column-C reasons **as printed on the form**:
  - **`0601` Breach of Rental/Lease Contract (not UD / wrongful eviction)** → reasons **2, 5**
  - `0602` Contract/Warranty Breach – Seller Plaintiff → 2, 5
  - `0603` Negligent Breach of Contract/Warranty → 1, 2, 5
  - `0604` Other Breach of Contract/Warranty (no fraud/negligence) → 1, 2, 5
  - (Collections `0901`–`0904` → reasons include **11** → **Norwalk**, not here.)
- **District/reason used:** `"district": "Central"`, `"civ109_reason": "2"` (Permissive
  Central). ⚠️ **Flag to Hernán:** the form lists only **2 and 5** under Column C for
  `0601`; **reason 11** ("Mandatory filing location — Hub Cases: unlawful detainer,
  limited non-collection, limited collection") is the truest fit for a limited
  non-collection case under LR 2.3(a)(2) but the form does NOT offer 11 for 0601. Both
  2 and 5 land the case in Central. Used **2** (permissive Central); confirm 2 vs 5 with
  Hernán. Reason 5 = "location where performance required, or defendant resides" (for a
  lease: rent payable in LA County; defendant in LA County) is an equally valid substantive fit.
- **Statement of Location address** = the leased premises (street/city/state/zip).

### Fee + e-file
- First-paper limited civil **over $10,000** = **$370** (Gov. Code §70613; the statewide
  tier boundary is $10,000, though One Legal's UI bands it as "Over $12,500 up to
  $35,000"). $10,000 or less = $225.
- Plus One Legal EFSP fee ~**$18.95** (+ ~3.5% card fee). Jury demanded → **$150** advance
  jury fee (CCP §631), due on/before the initial CMC (not at filing).
- E-file mandatory for attorneys via One Legal.

### Engine notes (shared fill_forms.py)
- CIV-109 action box is a **static glyph** stamped via the coord path; the 4-digit code
  regex matches `0601` fine (mirrors how dog-bite `2301` is stamped).
- Chinese-translation script must **strip `<w:hyperlink>`** elements (e.g. the email) or
  text duplicates.
- Limited-civil contract complaints use **plain (non-line-numbered) pleading paper**
  (paragraphs + footer; the 1–28 line numbers on the margin come from the template border).

### Sources
- LASC Local Rules (2.3(a)(2)) https://www.lacourt.org/ ; CRC 3.740 (collections case)
  https://courts.ca.gov/cms/rules/index.cfm ; Statewide Civil Fee Schedule (eff.
  01/01/2026) https://courts.ca.gov/system/files/file/statewide-civil-fee-schedule-eff-01012026.pdf
- **First run:** Brian Wu v. Azucanela LLC (401 E. Foothill Blvd., Azusa 91702) → package
  built to the case's `2. Pleadings`; principal $15,150, 4 causes, jury demanded.

### Worked config (Brian Wu — copy + adapt)
```json
{
  "templates": {
    "sum100": "<scratch>/sum100.pdf",
    "cm010":  "<scratch>/cm010.pdf",
    "civ109": "<scratch>/civ109.pdf"
  },
  "out_dir": "<scratch>/out",

  "county": "LOS ANGELES",
  "courthouse_name": "Stanley Mosk Courthouse",
  "courthouse_street": "111 North Hill Street",
  "courthouse_city_zip": "Los Angeles, CA 90012",
  "branch_name": "Stanley Mosk Courthouse",

  "plaintiff": "BRIAN C. WU",
  "defendant_block": "AZUCANELA LLC, a California limited liability company; ROBERT KENNEDY LEIVA, an individual; and DOES 1 through 10, inclusive",
  "case_name": "BRIAN C. WU v. AZUCANELA LLC, et al.",
  "case_short_title": "WU v. AZUCANELA LLC, et al.",
  "plaintiff_for": "Plaintiff BRIAN C. WU",
  "attorney_print_name": "Hernán S. Simó",

  "amount": "limited",
  "case_type_tooltip": "Breach of contract/warranty (06)",
  "num_causes": "4",
  "punitive": false,

  "addendum": "civ109",
  "district": "Central",
  "civ109_action_code": "0601",
  "civ109_reason": "2",
  "incident_address": "401 East Foothill Boulevard",
  "incident_city": "Azusa",
  "incident_state": "CA",
  "incident_zip": "91702"
}
```
