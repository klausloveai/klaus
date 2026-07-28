# Document Extraction Rules

## Driver License (1P)
- Extract: full legal name, DOB, address, DL#, expiry, gender
- W-prefix = AB 60 (undocumented/DACA); U-prefix = AB 60 variant — note in summary, no coverage impact
- LIMITED-TERM = DACA/visa — note in summary
- If STATE ID: file as "Firstname Lastname-California ID Card.ext", yellow I9, flag CRITICAL
- If PASSPORT: file as "Firstname Lastname-Passport.ext", yellow I9
- If INSTRUCTION PERMIT: file as "Firstname Lastname-Instruction Permit.ext",
  enter permit# in I9 with "(CA INSTRUCTION PERMIT — NOT DL)", yellow I9+I8, flag CRITICAL
- Expired DL at DOL: yellow I9, flag
- DL address takes priority over form address; note discrepancy, yellow address field
- DOB 1-day discrepancy form vs DL: use DL, no flag
- DOB 2+ days discrepancy: use DL, yellow, note in summary

### CA DL — DD field trap (common OCR error)
CA driver licenses have two date-like fields that look similar:
- `3 DOB MM/DD/YYYY` — the actual date of birth → USE THIS
- `5 DD MM/DD/YYYY...` — Document Discriminator (a serial string starting with issue/print date) → IGNORE for DOB

The DD field begins with a date that is NOT the DOB. If you read "5 DD 01/20/2026531219..." do NOT use 01/20 as any part of the DOB. Always read the field explicitly labeled `3 DOB`.

## Auto Insurance Card (1P)
- Extract: insurer, policy#, policyholder, vehicle(s), VIN, LP, policy period, listed drivers
- Multi-vehicle AIC: cross-ref LP photo to identify involved vehicle; yellow I11/I12 until confirmed
- Named insured ≠ driver: note in I8, yellow I8
- Temp/binder AIC: yellow I5/I6/I11/I12/I13/I30; filename "[Temporary] Firstname Lastname-AIC.ext"
- Expired AIC at DOL: yellow all 1P fields; filename "[EXPIRED] Firstname…-AIC.ext"; flag CRITICAL
- Same-day AIC (eff date = DOL): yellow I5/I6/I30; flag CRITICAL
- Vehicle in LP photo not on AIC: yellow I11/I12/I13; flag CRITICAL

### Digital / app-based AIC (e.g. Progressive, GEICO, Mercury apps)
These are phone app screenshots, NOT physical cards. Layout differs from physical cards but contains the same data. Key locations:
- Policy number: displayed prominently at top of screen (large text or under "Auto Policy")
- Vehicles: listed in a table with columns Year / Make / Model / VIN
- Read ALL vehicles listed and their VINs

### Accident vehicle not on the AIC
If the client's accident vehicle (from intake form or LP photo) is NOT listed on the AIC:
1. Record the vehicles that ARE on the AIC in the sheet
2. Write the accident vehicle info from intake form / LP photo into I11/I12/I13
3. Yellow I11/I12/I13
4. Flag CRITICAL: "⚠️ Accident vehicle ([Year Make Model]) not found on this AIC — may not be covered; verify with client"
**Never write "unknown" for vehicle fields when data is available from other sources (form or LP photo).**

## Auto Insurance Card (3P)
- Use only California Auto Insurance Identification Cards; discard roadside/loyalty cards
- CAARP/LCA temp card: compute expiry = eff date + 60 days
  - Expired at DOL: filename "[EXPIRED] 3P-AIC (CAARP).ext"; yellow ALL 3P fields; flag CRITICAL
  - Valid at DOL: filename "[Temporary] 3P-AIC (CAARP).ext"; yellow L5/L6/L7; note for permanent carrier
- Expired at DOL (non-CAARP): yellow all 3P fields; flag CRITICAL
- Same-day AIC: yellow L5/L6/L7; flag CRITICAL

## Police Card
- Extract: officer name/badge, agency, report#, crash date/time, NCIC#
- Police card crash date overrides form DOL (Priority 1)
- Yellow F18/F19 if date/time not visible
- CHP, SJPD, LAPD, LexisNexis BuyCrash, Utah DIE all valid formats
- Multiple clients uploading same police card: file one as "Police Card.ext", others as "[DUPLICATE] Police Card.ext"

## License Plate Photos
- Extract 1P and 3P plate numbers
- If 3P LP shows VIN sticker on windshield: extract VIN
- Confirm LP matches vehicle described on AIC

## Health Insurance Card
- Extract: carrier, member ID/policy#, effective date
- May be phone app screenshot — extract same fields
- CA Medi-Cal Benefits ID Card → enter in C14
- File in Folder 4 (NOT Folder 2)
- Combine front+back into single PDF

## Scene Photos / Videos
- Look for visible phone clock → corroborates DOL date/time
- Dashcam: extract iPhone metadata (com.apple.quicktime.creationdate) and GPS if present
- TeslaCam: read timestamp/speed/FSD status on screen
- WeChat filename timestamp (YYYYMMDDHHMMSS): supplementary DOL evidence
- Copy .mov/.mp4 as-is to 2#Accident Info; cannot convert to PDF

## Vehicle Registration
- Extract: owner name, VIN, LP, validity
- File as "[Party]-Vehicle Registration.pdf" in 2#Accident Info

## Gig/Delivery App Screenshots
- File as "[Platform] Delivery Screenshot.png" in 2#Accident Info
- Flag as TNC/gig evidence; yellow I5/I6/I11 if active at DOL

## Injury Photos
- If misfiled in Scene Photos: refile as "Injury Photos.pdf" in 2#Accident Info; note misfiling
