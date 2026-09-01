# Dog Bite Intake Sheet — cell map (for building fields.json)

> ⚠️ **VERIFY BEFORE YOU USE THIS FILE.** The template has drifted from this map at least
> once. On 2026-09-01 (Peiyun Zhou) the whole **Incident** block was **off by one row from
> row 5 down**, so every value from "Provoked?" onward landed against the wrong label, and
> the client block's C11 turned out to be *Spouse Name*, not *Guardian*. Dump the real
> labels first (see Step 5 in SKILL.md), map against those, then **read the sheet back and
> diff**. The layout below is what was verified on **2026-09-01** — treat it as the most
> recent observation, not as a guarantee.

The "0. Intake Sheet" is a label/value grid. **The value cell is always the column
immediately to the RIGHT of its label.** `fill_intake_sheet.py` locates value cells
by scanning label columns **B, E, H, K** — so it is robust to row drift. You (Claude)
only build `fields.json`, a flat map of **value-cell A1 → string**.

Fill every field the intake supports. Leave a value cell OUT of fields.json when the
intake does not establish it — the script auto-fills it **empty + yellow (#FFE599)**,
the firm's "pending / needs attention" highlight. Do NOT invent facts to avoid yellow;
yellow is the correct state for unknowns.

**Formatting rule:** written values are **NON-bold** — only the question labels (cols
B/E/H/K) stay bold. `fill_intake_sheet.py` enforces this (sets `textFormat.bold=false` on
every value it writes); the template's value columns C/F/I/L are also un-bolded.

## Client — value column C  *(verified 2026-09-01)*
```
C2  Date of Loss (MM/DD/YYYY)   C3  Date of Time (HH:MM)    C4  Client Name
C5  Date Birth (MM/DD/YYYY)     C6  Phone                   C7  Address
C8  Email                       C9  Gender (Male/Female)    C10 Marital Status
C11 Spouse Name  ← NOT Guardian C12 Occupation/Employer     C13 SSN
C14 Medi-Cal?                   C15 Medicare?               C16 Health Insurance
C17 Prior Injuries?             C18 Ambulance? (Yes/No)     C19 Emergency? (Provider, DOS)
C20 UrgentCare? (Provider, DOS) C21 PCP Visited?            C22 Injuries?
C23 Guardian (if minor) — Name & relationship  ← the Guardian row
```

## Incident Information — value column F  *(verified 2026-09-01 — this is the block that drifted)*
```
F2  Incident Location            F3  Location Type          F4  Fact of Loss
F5  Provoked?                    F6  Leash / Restraint      (row 7 has NO label — skip)
F8  Owner/Handler Present & Conduct                         F9  Independent Witnesses
F10 Scene Photos?                F11 Scene Video?           F12 Surveillance?
F13 Purpose of activities        F14 Animal Control Called? F15 Animal Control Report#
F16 Quarantine Ordered?          F17 Prior Bite / Aggression History?
F18 Other Victims / Companions   F19 Evidence to Preserve (Ring/CCTV, photos, texts — POE targets)
F20 Dog Warning Sign             F21 Police Report?         F22 Officer / Badge#
F23 Police Report#               F24 Lit-Case Number
```
- **There is no "Body Part(s) Bitten" row** in this template — an earlier version of this
  map invented one at F5. Put the wound description in **C22 (Injuries?)**, and the
  per-client detail on the second-client tab for joint cases.
- **F20 Dog Warning Sign:** leave it YELLOW unless the client was actually asked and
  answered. Do not infer "No" from silence in the narrative — the Bo Tao animal-control
  record turned out to recite a "BEWARE OF DOG" sign the client said did not exist, and
  that contradiction is exactly what the defense will build on.
- **F15:** if two documents give different activity numbers, record BOTH and mark it
  CONFLICT rather than picking one.

## Dog & Responsible Party — value column I  *(verified 2026-09-01)*
```
I2  Dog Name        I3  Breed          I5  Color / Markings   I6  Sex (Male/Female)
I7  Dog Size        I8  Dog Age        I9  Rabies / Vaccination Status
I11 Veterinarian    I12 Dog License#   I13 Prior Bite History?
I15 Dog Owner Name  I16 Owner Address  I17 Owner Phone        I18 Owner Email
I19 Handler (if not owner)             I20 Renter / Homeowner
I21 Owner is: Homeowner / Tenant       I22 Relationship to client  (use as the Notes cell)
I23 Landlord / Property Mgmt
```
- **Do not assert the dog owner's identity** unless the intake states it. A delivery
  *recipient* name off a package label is a lead, not proof — put it in **I22** clearly
  marked "LEAD ONLY, NOT CONFIRMED" and leave I15 yellow. Owner identity is confirmed later
  from the recorded **deed** and the animal-control investigation.
- Multi-dog incidents: I3/I5/I6 describe the pack; note the count in I3.

## Homeowner's / Renter's / CGL Insurance — value column L  *(verified 2026-09-01)*
```
L2  Coverage Status (template pre-fills "Pending" — leave)
L3  Liability Status (template pre-fills "Pending" — leave)
L5  Insurer   L6  Policy#    L7  Period    L8  Policyholder   L9  Named Insured
L10 Dog Owner L11 Phone      L12 Address
L14 Claim#    L15 Adjuster   L16 Phone     L17 Email
L18 Adjuster  L19 Phone      L20 Email     L22 Policy Limits
```
At intake the homeowner's/renter's carrier is almost always unknown → these stay yellow.
That is expected; coverage is run down in Stage 2 (Investigation).

## NOT auto-filled in v1 (leave untouched — the script does not scan these)
- **SOP** (col N/O) — a live checklist the CM works through by stage. Leave blank.
- **Treatments** (col Q–V) — unknown at intake.
- **Other Party Insurance** (col X/Y) and **Vehicle** (col AA/AB) — vestigial from the
  auto-accident template; N/A for a dog bite. Leave blank.

## Where the data lives in the intake docx
- **Structured tables** (deterministic): Date/Time, client Legal Name, Phone, Email, DOB,
  Address, Occupation, ID received; Incident Date/time & Location; procedural posture.
- **Narrative** ("案件事实与时间线 / Case Facts & Timeline" paragraphs): the dog-bite
  facts — how the bite happened (F4), wounds/body part (F5/C22), leash status (F7), owner
  conduct (F8), animal control contact (F12), ER treatment (C19), evidence to preserve
  (F20), dog description (I3/I5). Read the narrative and map these into fields.json.
