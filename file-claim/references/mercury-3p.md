# Mercury Insurance — 3P (third-party) claim

Filing a claim against a **Mercury-insured at-fault driver** on behalf of our client.
Written 2026-09-04 (first Mercury 3P case: Qianqian Li, DOL 9/4/2026).

> ⚠️ **UNVERIFIED — first run.** The step numbers below are the intended flow, not yet
> confirmed against the live site. On the first run, read each page before acting and
> **correct this file afterwards** with what the site actually did.

## Reporting channels

| Channel | Detail | When to use |
|---|---|---|
| **Phone** | **888-917-6372** (insurance-list directory) | Fastest. Third-party claims are often handled by a rep who issues the claim # on the call. **Default for urgent PD** (client's car undrivable). |
| Web | mercuryinsurance.com → Claims → "File a claim" | Mercury's online flow is built mainly for **policyholders**. A third-party claimant may be routed to a phone number rather than a completed online report. Verify before relying on it. |

**Practical rule:** if the client's car is undrivable / a rental is needed, **call**. Only use
the web flow when it demonstrably produces a claim number for a non-policyholder.

## Field map (from `read_intake_claim.py`)

| Form field | Source | Notes |
|---|---|---|
| Their insured / policyholder | `p3_insured` | ⚠️ **often blank in intake** — the police exchange form's OWNER'S NAME column. If unknown, give the **driver** name and the **policy number**; Mercury can look it up on the policy #. |
| Their policy number | `p3_policy` | Primary lookup key. |
| Their driver | `p3_driver` (+ `p3_dl`, `p3_address`) | |
| Their vehicle | `p3_vehicle`, `p3_lp` | |
| Date / time of loss | `dol`, police card crash time | Use the **police card** time if it differs from the client's. |
| Location | `accident_location` | Paste verbatim; include GPS if the intake carries it. |
| Police agency + report # | intake F18–F22 | Mercury will ask. |
| Our client | `client`, DOB, DL#, `client_address`, phone | |
| Our vehicle | `our_vehicle`, `our_vin`, `our_lp` | |
| Our insurer | `p1_insurer`, `p1_policy` | Asked but not required. |
| Facts of loss | `fol` **verbatim** | ⚠️ Never compose. Copy the client's own sentence. |
| Damage / drivability | intake F6 | Say plainly if undrivable and where it is. |
| Contact for the claim | handling CM's **direct line** + team mailbox | Never the 888 main line — firm rule. |

## Steps (phone lane)

1. Confirm the field set with Klaus (skill Step 4) — **do not call before this.**
2. Klaus or the CM places the call to 888-917-6372; state: reporting a third-party claim
   against policy `<p3_policy>`, insured driver `<p3_driver>`, DOL `<dol>`.
3. Capture the **claim number** on the call, plus adjuster name / direct line if given.
4. Skill Step 8: write claim # to intake `L19`, post to the case Chat space, then run
   `lor-send` for the 3P.

## Mercury-specific gotchas

- **Adjuster email format**: `MyClaim+<CLAIM#>@mercuryinsurance.com` — only valid once the
  real claim # is known. Until then the intake keeps `MyClaim+[CLAIM#]@...` + yellow
  (new-case cell-map rule).
- **LOR fax**: `866-268-8494` (insurance-list directory).
- Mercury writes through several entities (Mercury Insurance Co / Mercury Casualty /
  California Automobile Insurance Co). The policy prefix on the card tells you which; it does
  not change the reporting number.
