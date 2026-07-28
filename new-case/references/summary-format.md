# Output Summary Format

After delivering the zip, provide a plain-text summary covering these sections in order:

## 1. DOL Source
State DOL confirmed or corrected, source used, and any discrepancy with form.
"DOL confirmed as 05/24/2026 — police card (Priority 1)."
"DOL corrected from 05/25/2026 to 05/24/2026 — WeChat filename timestamp + scene photo phone clock."

## 2. Document Vision Fields
List what was extracted from each document type:
- DL(s): name, DOB, DL#, address, any flags (LIMITED-TERM, AB 60, expiry)
- AIC(s): insurer, policy#, vehicle, VIN, LP, period, any flags
- 3P DL: name, DOB, DL#
- 3P AIC: insurer, policy#, vehicle, VIN, period, any flags
- Police card: agency, report#, crash date/time, NCIC#
- LP photos: plate numbers confirmed
- HIC: carrier, member ID
- Other docs noted

## 2b. Insurance Directory Lookup
For each insurer identified (1P and 3P), state the match result and what was filled.
Examples:
- "1P GEICO: matched → phone (I17) / fax (I22) / email (I18) filled ✓"
- "3P Mercury Insurance: matched → phone (L21) filled ✓; email (L22) set to MyClaim+[CLAIM#]@mercuryinsurance.com ⚠️ Update once CAPA# is received"
- "3P 'XYZ Insurance': no directory match — add to insurance list; L21/L22 left Pending+yellow"
- "Directory lookup skipped (read error) — all contact cells left Pending+yellow"

## 3. Yellow-Highlighted Fields
List all yellow fields and why each was flagged.

## 4. Missing Documents
List document categories with no uploads (e.g., "No police card uploaded").

## 5. Misfiled / Duplicate Documents
Note any documents moved from their submitted location and where they were refiled.
Note any duplicates and how they were handled.

## 6. Critical Flags
Use ⚠️ CRITICAL: prefix for each. Examples:
- ⚠️ CRITICAL: 3P AIC effective date = DOL (05/24/2026) — Mercury policy CAAP0000765734
- ⚠️ CRITICAL: Instruction permit only — policy rescission risk, escalate to lead attorney
- ⚠️ CRITICAL: CAARP temp card expired [date] — verify permanent carrier assignment
- ⚠️ CRITICAL: Named insured ≠ driver — verify coverage
- ⚠️ CRITICAL: Vehicle not on AIC — verify coverage
- ⚠️ CRITICAL: Same-day AIC — verify coverage
- ⚠️ CRITICAL: Expired DL at DOL
- ⚠️ CRITICAL: Active gig/TNC work — personal policy likely excludes delivery/TNC use
- ⚠️ CRITICAL: Minor client(s) — guardian authorization required
- ⚠️ CRITICAL: Commercial trucking — escalate, spoliation letter needed
- Note non-critical items (AB 60 DLs, prior accidents, no police report) without CRITICAL prefix

## 7. Intake Responses Zip
Confirm: "Original intake zip saved as 'Intake Responses.zip' in 1#Legal Documents."
