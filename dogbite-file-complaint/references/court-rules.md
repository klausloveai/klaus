# CA County Filing Rules — Dog-Bite Complaints (One Legal)

Per-county first-paper requirements for filing a dog-bite (PI, unlimited civil)
complaint. **"做一个记一个"**: only counties actually used are recorded here. When a
new county appears, verify its rules against the court's own site, then add a section
(see SKILL.md "Adding a new county"). Never fabricate a rule.

Every county needs, at minimum (statewide): **Summons (SUM-100)** + **Complaint** +
**Civil Case Cover Sheet (CM-010)**. Attorney-filed unlimited/limited civil is
**mandatory e-file** (Cal. Rules of Court 2.253(b)) via an approved EFSP — the firm
uses **One Legal**. Dog bite → CM-010 Item 1 = **Other PI/PD/WD (23)**. Leave case #,
signature, date blank.

---

## Los Angeles County  (status: implemented)

- **Local addendum:** YES — **CIV 109** (Civil Case Cover Sheet Addendum & Statement
  of Location). Template Drive id `19U8ASWcSwDXOXwGo-wGmdOo6ICwESOyT`. Fill map:
  `CIV109_ACTION_XY` in `fill_forms.py`.
- **Branch/venue:** district **where the incident occurred** (LASC General Order
  2024, PI Hub retired). Use the LASC Filing Court Locator with incident city+ZIP →
  read the Unlimited Civil column. See `la-county-pi.md` for the full detail +
  courthouse table.
- **Dog bite codes:** CIV 109 Column B `2301` (Premises Liability … dog attack),
  reason `4` (location where injury occurred).
- Full reference: **`references/la-county-pi.md`**.

---

## Ventura County  (status: IMPLEMENTED — verified on Bo Tao v. Beas, 2026-07-09)

- **Local addendum:** **NONE for a dog-bite / PI case.** Ventura's local Civil Case
  Cover Sheet Addendum (**Local Form VN278, New 07/26**) is an **Optional Form** whose
  Column A lists ONLY: Other Employment (15), Product Liability (24) [Song-Beverly/
  Lemon-Law], Writ of Mandate (02), Other Judicial Review (39), Civil Rights (08)
  [High-Frequency Filer]. It does **NOT** list Personal Injury / Other PI/PD/WD (23),
  so a dog-bite complaint does not use VN278. (Lesson: I originally assumed VN278 was
  Ventura's CIV-109 analog — WRONG. Verified against the actual form. Only add an
  addendum when the case type actually appears on it.)
  - Config: **`"addendum": "none"`** → `fill_forms.py` skips the addendum step.
- **Required first-paper set (FILE with the court):** Complaint + **Summons (SUM-100)**
  + **CM-010**. That's it — no addendum.
- **Serve-with-complaint set (NOT filed, but must be SERVED on each defendant):**
  1. **ADR Information Package = Local Form VN242** (CCP §1775.5, CRC 3.221) — plaintiff
     must serve it on each defendant with the complaint. Download:
     `https://ventura.courts.ca.gov/system/files/adr_packet-infosheet.pdf` (include a copy
     in the package folder as "Serve with Complaint - ADR Information (VN242).pdf").
  2. **Notice of Case Assignment and Mandatory Appearance** (Ventura LR 3.03.1(B)) —
     **court-issued at filing** (assigned dept + CMC/OSC date ~5 months out); the filing
     party then serves it on each defendant with the complaint. Not prepared in advance.
- **Court / venue:** single civil hub — **Hall of Justice, 800 S. Victoria Ave.,
  Ventura, CA 93009** (civil filing Room 80). No multi-district locator (unlike LA).
  **SUM-100 court-name line = the COURT, not the building.** Use
  `court_name_sum100 = "Ventura County Superior Court"` (the SUM-100 FillText3 box is
  narrow, ~150pt — the full "Superior Court of California, County of Ventura" (187pt @9)
  overflows into the CASE NUMBER box, so use the compact proper name). line2 =
  `800 S. Victoria Ave., Ventura, CA 93009`. **"Hall of Justice" is the building/branch**
  → put it ONLY in the CM-010 Branch Name (`branch_name = "Hall of Justice"`), never on
  the SUM-100 court-name line. CM-010 county = `VENTURA`. CM-010 box = Other PI/PD/WD (23).
- **E-file:** mandatory for attorneys (CRC 2.253(b)); via One Legal. First-paper fee
  ~$435 (unlimited civil UCF). Jury demanded → $150 jury fee deposit (CCP §631).
- **Sources:** Ventura civil filing info https://ventura.courts.ca.gov/system/files?file=civilfilinginformation.pdf ;
  Local Forms https://ventura.courts.ca.gov/forms-filing/local-forms ;
  eFiling https://ventura.courts.ca.gov/online-services/efiling
- **First run:** Bo Tao v. Beas (Oxnard incident) — package built to
  `~/Downloads/Bo Tao - Complaint Filing Package` (SUM-100 + Complaint + CM-010).

---

## San Bernardino County  (status: rules verified 2026-07-09; fill-map TBD on first SB case)

- **Local addendum:** YES, but it's a **Certificate of Assignment** (SB local form, fillable
  PDF on the court site; historically form 13-16503-360), NOT a CIV-109-style cover-sheet
  addendum. **Required with EVERY civil complaint** (except probate/trust/estate/
  conservatorship) — so it DOES apply to a dog-bite PI case (unlike Ventura's VN278).
  Its purpose: determine the proper **filing district** (SB is multi-district:
  San Bernardino, Rancho Cucamonga, Victorville, Joshua Tree, Barstow, Fontana, …), same
  role LA's CIV-109 plays. SB has NO separate local cover-sheet addendum beyond this.
- **Required first-paper set:** Complaint + Summons (SUM-100) + CM-010 + **Certificate of
  Assignment**.
- **Branch/venue:** district determined by the Certificate of Assignment's questions
  (typically where the cause arose / defendant resides). Verify the district on the first
  SB case from the form's criteria; record the district→courthouse mapping then.
- **TODO on first SB case:** download the Certificate of Assignment from
  `https://sanbernardino.courts.ca.gov/forms-filing/local-forms`, upload to the Litigation
  Forms Drive folder, add its id to `get_templates.sh`, add a `fill_sb_cert()` + config
  `addendum:"sb_cert"` branch to `fill_forms.py`, render-verify. Then SB is a fast path.
- **CM-010 box:** Other PI/PD/WD (23). **E-file:** mandatory (CRC 2.253(b)) via One Legal.
- **Sources:** SB local forms https://sanbernardino.courts.ca.gov/forms-filing/local-forms ;
  Certificate of Assignment (fillable) https://www.sb-court.org/sites/default/files/Forms%20and%20Rules/13-16503-360CertificateOfAssignmentfillable.pdf ;
  SB civil FAQ https://sanbernardino.courts.ca.gov/divisions/civil-general-information/frequently-asked-questions-civil

---

## Template for a new county section (copy, fill, verify — never guess)

```
## <County> County  (status: <verified date> / implemented)
- Local addendum: YES/NO — <form name + local code>; template Drive id `...`; fill map `...`.
- Required at first filing: Complaint + SUM-100 + CM-010 [+ addendum] [+ other local form].
- Branch/venue: <how the filing court/branch is determined>.
- E-file: mandatory (CRC 2.253(b)) via One Legal.
- CM-010 box: Other PI/PD/WD (23). Addendum action code/reason: <...>.
- First-paper fee: <$ + source>.
- Sources: <court's own URLs>.
```
