# Dog Bite Intake Sheet — cell map (for building fields.json)

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

## Client — value column C
```
C2  Date of Loss (MM/DD/YYYY)     C3  Time (HH:MM)            C4  Client Name
C5  DOB (MM/DD/YYYY)              C6  Phone                   C7  Address
C8  Email                        C9  Gender                  C10 Marital Status
C11 Guardian (if minor; "N/A (adult)" when adult)            C12 Occupation/Employer
C13 SSN                          C14 Medi-Cal?               C15 Medicare?
C16 Health Insurance             C17 Prior Injuries/Claims?  C18 Ambulance?
C19 Emergency? (Provider, DOS)   C20 UrgentCare?             C21 Primary Doctor Visited?
C22 Injuries / Bite Location (short, comma-separated)
```

## Incident Information — value column F
```
F2  Incident Location (full address)      F3  Location Type (Public park / Private
                                              residence / Apartment common area / Other)
F4  Fact of Loss (brief narrative)        F5  Body Part(s) Bitten & Wounds
F6  Provoked? (Yes/No — describe)         F7  Leash / Restraint Status
F8  Owner/Handler Present & Conduct       F9  Witnesses (names, phones)
F10 Scene Photos / Videos? (describe)     F11 Client Activity
F12 Animal Control Called? (agency)       F13 Animal Control Report#
F14 Quarantine Ordered?                   F15 Prior Bite / Aggression History?
F16 Other Victims / Companions            F17 Police Report (agency / none)
F18 Incident Date (per report)            F19 Incident Time
F20 Evidence to Preserve (Ring/CCTV, photos, texts — the POE targets)
F21 Officer / Badge#                      F22 Police Report#
```

## Dog & Responsible Party — value column I
```
I2  Dog Name        I3  Breed          I5  Color / Markings   I6  Sex
I7  Weight (lbs)    I8  Dog DOB / Age  I9  Rabies/Vax Status  I11 Veterinarian
I12 Dog License#    I13 Prior Bite History?                   I15 Dog Owner Name
I16 Owner Address   I17 Owner Phone    I18 Owner Email        I19 Handler (if not owner)
I20 Renter / Homeowner   I21 Owner is: Homeowner / Tenant     I22 Relationship / Notes
```
- **Do not assert the dog owner's identity** unless the intake states it. The Amazon
  delivery *recipient* name is a lead, not proof — put it in I22 (Notes) and leave
  I15 yellow. Owner identity is confirmed later from the property **deed** / investigation.

## Homeowner's / Renter's / CGL Insurance — value column L
```
L2  Coverage Status (template pre-fills "Pending" — leave)
L3  Liability Status (template pre-fills "Pending" — leave)
L5  Insurer  L6 Policy#  L7 Period  L8 Policyholder  L9 Named Insured / Dog Owner
L12 Insured Phone  L13 Insured/Property Address  L19 Claim#  L20 Adjuster
L21 Phone  L22 Email  L23 Adjuster  L24 Phone  L25 Email  L27 Policy Limits
```
At intake the homeowner's/renter's carrier is almost always unknown → these stay
yellow. That is expected; coverage is run down in Stage 2 (Investigation).

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
