# GEICO — Third-Party (3P) Online Claim Playbook

Filing a **bodily-injury / property-damage claim against a GEICO insured** (our client is
NOT a GEICO policyholder). Source: firm tutorial "Geico File 1P.docx" (filename says 1P but
the content is the **3P third-party** flow — always file as third party here).

Site: `https://www.geico.com` → **Claims Center**. Screenshots for each step are in
`geico-screens/stepNN.png` — Read the matching one if the live page doesn't match the
description.

## Field map — intake field → form field

`read_intake_claim.py` keys on the left. Verify every ⚠️ field with the user before filing.

| Form field | Value | Source |
|---|---|---|
| Reporter identity | "I had an incident with a GEICO customer" | constant (3P) |
| Policy Number | at-fault GEICO policy # | `p3_policy` |
| ⚠️ Last Name | **policyholder's** last name (NOT driver's); if `p3_insured` lists 2+ people, use the **first** person's last name | `p3_insured` |
| Contact First/Last | Case Manager | firm-directory |
| Contact Phone | CM direct line, type Mobile | firm-directory |
| Contact Email | CM team email | firm-directory |
| Contact ZIP | `91746` (firm) | constant |
| What was damaged | Auto / Motorcycle | constant |
| Facts of Loss | client-perspective 1–2 sentences | built (see templates) |
| Date | date of loss | `dol` |
| Time | approximate | `time` |
| State | California | from `accident_location` |
| ⚠️ County | derived from accident city | from `accident_location` (ask if unsure) |
| Your vehicle Year/Make/Model | OUR client's vehicle | `our_vehicle` |
| Your vehicle owner? | Yes (if client owns) | confirm |
| Were you in the vehicle? | **No** (office files on behalf) | constant |
| GEICO vehicle Make/Model | at-fault vehicle | `p3_vehicle` |

**Two classic mistakes — guard against both:**
1. **Last Name** = the *policyholder* (`p3_insured`), not the driver (`p3_driver`). If they
   differ (e.g. driver Contreras, policyholder Velazco) the driver's name is rejected. If
   `p3_insured` is blank or equals the driver, confirm with the user.
2. **County** isn't in the intake sheet. Derive it from the accident city (e.g. Ontario →
   San Bernardino) and **confirm with the user** before selecting.

## Steps

Use Claude-in-Chrome tools (navigate / read_page / find / computer / form_input). After
each navigation, read the page and match it to the screenshot before acting. The flow can
re-order or A/B-test fields — adapt to what's on screen; the playbook is intent, not a
pixel script.

**Step 1 — Claims Center.** Go to `www.geico.com`. Click **CLAIMS CENTER** in the top nav
(2nd item). `step01.png`

**Step 2 — Report a GEICO Claim.** In the dropdown, under *Manage Claim* click **Report a
GEICO Claim**. NOT "Track a Claim" / "Report Glass Damage". `step02.png`

**Step 3 — Who is reporting.** Select **"I had an incident with a GEICO customer"** (2nd
option). NEVER "I am insured with GEICO" — our client is the third party. `step03.png`

**Step 4 — Policy # + Last Name.** "Policy Number" tab (default). Enter `p3_policy`. Last
Name = **`p3_insured`** (policyholder). CONTINUE. `step04.png`
- ✅ **EXPIRED 3P policy is NOT a blocker (confirmed 2026-06-07, Liye Zhang).** The front-end
  validates only that policy # + policyholder last name **match a policy on record**; an
  `[EXPIRED]` policy passes Step 4 AND files all the way to a claim number
  (`8844066210000001`). Coverage/denial is decided later by the adjuster — you can still file.
- ⚠️ **The real failure mode is SESSION TIMEOUT, not the policy.** Earlier "Something Went
  Wrong" errors after the date/State step were caused by **pausing too long between steps**
  (the report session times out). When the same expired-policy case was run **quickly and
  continuously**, every step passed and the claim filed. **Lesson: move through the flow
  briskly — don't leave the report sitting idle between actions.** If you hit "Something Went
  Wrong", it's almost certainly a timeout: restart the report (re-navigate to
  `claims.geico.com/ReportClaim#/`) and run straight through without long gaps.

**Step 5 — Contact info (law firm).** First/Last = CM name. Phone Type Mobile. Phone = CM
direct line. Text consent = Yes. Use firm/CM info, never client's. `step05.png`

**Step 6 — Email + ZIP.** Email = CM team email. ZIP = `91746`. CONTINUE. `step06.png`

**Step 7 — What was damaged.** Check **Auto / Motorcycle** (BI links automatically later).
CONTINUE. `step07.png`

**Step 8 — Facts of Loss.** ⛔ **Do NOT compose / free-write the FOL.** Copy the intake `fol`
**verbatim** (paste exactly what's in the sheet). If the intake FOL is blank, **skip it or
enter a minimal filler ("1")** — never invent a narrative. A fabricated FOL can put wrong
facts or an admission on the record; a verbatim copy (or a harmless filler) cannot. CONTINUE.
`step08.png`

**Step 9 — Date / Time / State / County.** Date = `dol` (MM/DD/YYYY). Time = three dropdowns
(Hour / Minute / AM-PM). State = California. **The County dropdown only appears AFTER State is
set** (same page) and is **required** — derive from the accident city + confirm. CONTINUE.
`step09.png`
- **County unknown (client doesn't remember the location)** → fallback rule: use the county of
  the **client's home address** (`client_address`, intake `C7`) — i.e. a nearby, requirement-
  satisfying placeholder that lets the report proceed. The **CM updates the exact location with
  the adjuster afterward** (same "fill an acceptable value, adjuster corrects later" pattern as
  Step 11). Tell the user which county you're using as the placeholder and why; flag it in the
  Step-4 verification table so they know it's a stand-in, not confirmed.
- ⚠️ **Re-render gotcha:** selecting State (which injects the County field) can reset the Hour
  dropdown. Set/verify Hour AFTER choosing State, or re-set it before CONTINUE.

**Step 10 — Your vehicle (OUR client's).** Vehicle Type Auto. Year/Make/Model from
`our_vehicle` (pick the system's dropdown spelling, e.g. LEXUS). Owner = Yes. `step10.png`

**Step 11 — Were you in the vehicle?** Select **"No, I was not in the vehicle"** — office
staff filing on behalf was not in the car. Harmless; adjuster can correct. `step11.png`

**Step 12 — GEICO insured's vehicle (at-fault).** Vehicle Type Auto. Make/Model from
`p3_vehicle`. (Plate/VIN `p3_lp`/`p3_vin` for reference.) Note CA fraud warning — no action.
`step12.png`

**Step 13 — Submit → Claim Number.** ⛔ **STOP before the final submit and get the user's
explicit OK** (see SKILL Step 6). After submit: page shows "Your claim has been reported."
**Screenshot immediately** and record the **Claim Number**. Click CONTINUE for any extra
prompts. Confirmation email goes to the CM email. `step13.png`

## Facts of Loss — the rule is VERBATIM, not authored

The firm rule: the FOL field gets the intake `fol` text **copied exactly**. Do not paraphrase,
"improve", add a client-favorable spin, or write your own — even though the result reads rough.
If the intake `fol` is blank, **skip the field or put a minimal filler ("1")**. The reason: a
narrative you author can introduce wrong facts or an inadvertent admission onto the carrier's
record; a verbatim paste (or a harmless filler) carries no such risk. Same rule applies to any
"Purpose of Trip" / free-text narrative field on any carrier form.

## Post-filing checklist (carry out in SKILL Step 8) — firm-confirmed flow
1. **Screenshot the confirmation page IMMEDIATELY and save it to disk** (`save_to_disk: true`)
   the moment the claim number shows — that page is one-time; once the tab closes it's gone.
2. **Write Claim # into the intake sheet `L19`** (3P; `I15` for 1P) — see SKILL Step 8 (the
   intake is an `.xlsx`; edit the cell inline + re-upload). Done for the case row too.
3. **Post to the case Google Chat space** (NOT the Drive folder): a message
   `【Claude AI】 3P filed online, and claim# <CLAIM#>` (use `1P`/`3P` per party) + the confirmation
   screenshot. Recipe + the screenshot-bridge caveat are in SKILL Step 8.2 (text always works;
   image upload via `gws chat media` needs a Bash-visible file — the browser screenshot file
   isn't reachable from Bash in this sandbox).
4. **Auto-draft + fax the LOR:** immediately run `lor-send` for the same party — it drafts the
   LOR from the template (claim #, DOL, client) and **sends via fax** (GEICO has an LOR fax in
   the insurance-list directory; fax is the firm's primary channel). lor-send keeps its own
   pre-send approval gate.
- Then: contact the GEICO adjuster to confirm coverage + BI limits (in writing); remind the
  client not to speak with GEICO directly.
