# Lead Details — field guide

Question set is **Morgan & Morgan's**, from `Klaus Template.docx` (Babatunde, 04/27/2026).
**Never rename, reorder, add or drop a field** — their intake team reads it positionally.
Only the formatting is ours.

JSON keys consumed by `scripts/build_referral_lead_details.py`:

| Section | Label (verbatim) | key | What goes in |
|---|---|---|---|
| LEAD | Name | `name` | Every client + role + DOB. Multi-client: `A (driver, DOB …) · B (front-seat passenger, DOB …) — N clients, <language/occupation>`. |
| | Case Type | `case_type` | `Auto — 3-vehicle intersection collision`, `Auto — rear-end`, `Premises`, etc. |
| INCIDENT | Where did the accident happen? | `where` | `<State> — <City> (<cross streets>, <County>)`. State first: it is why we are referring. |
| | Incident Date | `date` | `MM/DD/YYYY, H:MM a.m./p.m.` |
| | Summary | `summary` | The full narrative **including the liability read and the damage-pattern evidence**. This is where the analysis Klaus cuts from the email belongs. Attribute observations to their source ("scene photographs show…", "per client…"); never assert fault as settled. |
| | Police on scene | `police` | `Yes — TCR Yes.` + agency, report #, local #, officer + badge, and whether the full report is obtainable yet (NY DMV holds MV-104A 14 days; CHP has an NCIC#). |
| COVERAGE | PC's Insurance | `pc_ins` | Our client's own carrier, policy #, named insured, policy period, whether the dec page is in hand. |
| | Limits | `pc_limits` | PIP / MedPay / collision deductible / rental — and explicitly note coverages **not** purchased. |
| | UIM/UM | `um` | `Yes` / `No` / `Pending dec page` |
| | Limits | `um_limits` | `UM $100,000/$300,000 · UIM $100,000/$300,000` |
| | Def's Insurance | `def_ins` | Every adverse driver: name, DOB, address, vehicle, plate + state, registered owner, carrier. Unidentified carriers are a finding — say so in caps (`NOT YET IDENTIFIED`) with the police code. |
| | Limits | `def_limits` | Limits or `Pending`; note whether a claim/LOR has issued; flag if UM/UIM is the likely real recovery. |
| INJURIES & TREATMENT | Injuries | `injuries` | Plain words. Include psychological complaints and prior-accident/prior-injury history. |
| | Emergency room or Urgent Care | `er` | `No`, or provider + date of service. |
| | Transported via Ambulance | `ambulance` | `No`, or the EMS agency + destination. |
| | Health Insurance | `health_ins` | Per client; `pending` is an acceptable answer, a blank is not. |
| | Treatment | `treatment` | Duration + modalities + whether complete; or `None to date` + why. Note wage loss. |

Rules:
- **`Pending` beats a guess.** Every field ships with a value; "still being gathered" is a value.
- Never fabricate an amount, date, carrier or diagnosis.
- Worked example: `references/example-bingcheng-ye.json`.
