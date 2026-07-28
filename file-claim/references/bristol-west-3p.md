# Bristol West — Third-Party (3P) Online Claim Playbook

Filing a **bodily-injury / property-damage claim against a Bristol West insured** (our client
is NOT a Bristol West policyholder; Bristol West is a Farmers Insurance Group company).
First built live 2026-06-09 on Chenlu Zhao → claim **5043288542-1**.

Site: `https://www.bristolwest.com` → **Claims** → "Report/view a claim" (no login). The
report flow runs on a Salesforce portal at `https://claims.bristolwest.com/bwcmp/s/filealoss`
— a **3-step wizard** (Start claim → Policy details → Claim details). No per-step screenshots
yet; the page is text-clear.

## ⭐ Firm rule — give the OTHER carrier ZERO client contact info
On a 3P claim we are reporting to the **at-fault party's** carrier. **Never put the client's
address / phone / email on the form.** The only client datum that must appear is the injured
person's **name** (it identifies the BI claimant — unavoidable). All "Contact info" =
**the firm** (CM Cindy Zhang + firm address/phone/email). Set "How were you involved?" =
**Other** (NOT "I was involved in an incident with your insured" — that would imply the
contact person was in the crash). See Step 9.

## Field map — intake field → form field

| Form field | Value | Source |
|---|---|---|
| Who is reporting (claims page) | **"I'm someone else"** | constant (3P) |
| Start-with | **Policy number** (more reliable than phone) | — |
| Policy number | at-fault policy, **letters+digits, NO spaces** (e.g. `G01 7609110 00` → `G01760911000`) | `p3_policy` |
| Insured first / last name | at-fault **policyholder** | `p3_insured` (split first/last) |
| Date of loss | `MM/DD/YYYY` | `dol` |
| Time of loss | `H:MM AM/PM` | `time` |
| Vehicle or location involved | pick the policy's vehicle whose VIN tail matches `p3_vin` (validates the right policy) | `p3_vehicle`/`p3_vin` |
| What happened? | **Vehicle accident** | constant |
| Description of what happened | best-fit of the "Insured vehicle …" options; if none fits (e.g. backing/parking-lot), **"Another kind of accident took place"** — do NOT force a wrong category | from `fol` |
| Were there injuries? | **Yes** for a BI/PI case → severity **"the injury was not that severe"** (soft-tissue) | case type |
| Injured person first / last | OUR client (the claimant) | `client` |
| Where did it happen? | state = **California** | from `accident_location` |
| Who was driving the insured vehicle? | **"I have the driver's name"** → at-fault driver | `p3_driver` |
| How were you involved? | **Other** (law firm) — see firm rule above | constant |
| Contact name | **Cindy Zhang** (or signing CM) | firm-directory |
| Contact address / city / state / zip | **firm** — `13191 Crossroads Pkwy N STE 295` / `City of Industry` / `California` / `91746` | constant (firm) |
| Contact phone / email | CM line `626-860-0173` / `picase@lingtulaw.com` | firm-directory |
| Contact preferences (2 checkboxes) | **leave both unchecked** (2nd accepts T&C) | constant |
| Interpreter language | leave blank (optional) | — |

**No free-text FOL field exists on this form** — the structured "Description" dropdown is the
only place. So the verbatim facts of loss are NOT entered here (nothing to fabricate); they
reach the adjuster via the LOR / follow-up. The form takes only **one** injured person — a
passenger co-client (e.g. Haoyang Wang) is added later with the adjuster.

## Steps

**Step 1 — Claims page.** `bristolwest.com` → decline tracking cookies (Reject) → Quick Links
"**Report/view a claim**". On the Claims Service page choose **"I'm someone else"** → REPORT A
CLAIM. (NOT "current Bristol West customer" / "another insurance carrier".)

**Step 2 — Start claim (Step 1 of 3).** "Personal claim" tab. Choose **Policy number**. Enter
`p3_policy` (no spaces), insured first+last (`p3_insured`), date + time of loss → **Start
claim**. This live-validates the policy.

**Step 3 — Policy details (Step 2 of 3).** "Vehicle or location involved" dropdown lists the
policy's vehicles — pick the one whose masked VIN tail matches `p3_vin` (confirms the right
at-fault policy) → **Next**.

**Step 4 — What happened.** Claim details (Step 3 of 3): "What happened?" = **Vehicle
accident**; "Description" = best-fit / **Another kind of accident took place**.

**Step 5 — Injuries.** "Were there any injuries?" → **Yes** → severity **"not that severe"** →
injured person = **client** first/last.

**Step 6 — Where.** "Where did it happen?" = **California**.

**Step 7 — Insured driver.** "Who was driving the insured vehicle?" = **I have the driver's
name** → `p3_driver` first/last.

**Step 8 — (skip LiveOps checkbox.)** Leave "I am a LiveOps representative" unchecked.

**Step 9 — Contact info = FIRM only.** "How were you involved?" = **Other**. Name = **Cindy
Zhang**; address/city/state/zip/phone/email = **firm** (see field map). **No client contact
info.**

**Step 10 — Contact preferences.** Leave both checkboxes unchecked; interpreter blank.

**Step 11 — Submit (APPROVAL GATE).** Scroll to **Submit claim**. Show the user the final
state; submit ONLY on explicit approval. Confirmation page shows **Claim number** +
assigned claim representative — screenshot it AT ONCE (`save_to_disk`).

## Post-filing
- Write the claim # to intake **`L19`** (3P); un-highlight if the cell is yellow `s=9`→`s=8`
  (on Chenlu's sheet L19 was already `s=8`). Bristol West adjuster email is a real address
  (`docs@bristolwest.com`), not derivable from the claim #.
- **Next step after filing = send the 3P LOR** (lor-send skill) to Bristol West with the new
  claim #, then post the team Chat notice + log the tracking `3LOR` column. (This is the
  file-claim-lor chain.)

## Notes & gotchas
- **Firm-only contact (the headline rule)** — never expose the client's contact details to
  the opposing carrier; only the injured claimant's name appears.
- Policy number: strip spaces, keep the letter prefix (`G0…00`). Wrong format → 7–13 digit
  validation error.
- "Description of what happened" options are insured-vehicle-centric; when the real dynamics
  don't fit, the catch-all is correct — never mischaracterize (e.g. don't say "hit parked
  vehicle" if our client was moving/backing).
- One injured person per form; add passengers via the adjuster.
- Approval gate at Submit is non-negotiable (irreversible).
