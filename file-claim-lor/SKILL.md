---
name: file-claim-lor
description: |
  End-to-end "file the claim online, then send the LOR" workflow for 凌图律所 / Lingtu
  Law Office (Law Office of Shenqi Cai APC). Use this skill whenever the user wants BOTH
  steps for a case in one go — e.g. "file claim and send LOR", "网上报案 + 发 LOR",
  "report the claim then notify the carrier", "file-claim-lor", or files a claim and then
  asks for the LOR right after. Typical invocation: a driver/client name + party (1P own
  carrier / 3P at-fault) + the case manager. It orchestrates the two existing skills in
  order — first **file-claim** (drive the carrier portal, get the Claim #, write it to the
  intake sheet), then the connective bookkeeping (resolve the carrier adjuster email from
  the claim #, un-highlight confirmed intake fields, post to the case Chat space), then
  **lor-send** (draft + fax/email the Letter of Representation with the new claim #), then
  log the LOR send date on the Master tracking sheet. Both irreversible/outbound actions
  keep their own mandatory approval gates. Always trigger for any combined "file claim +
  LOR" request, even a partial one.
---

# File Claim + Send LOR (orchestrator)

A thin orchestrator over two durable skills — **`file-claim`** (online portal filing) and
**`lor-send`** (Letter of Representation) — plus the connective bookkeeping that ties them
together. It does NOT re-implement either; it runs them in order and fills the gaps between.

> This skill is **v1 / living** — Klaus keeps optimizing it. When you learn something during
> a run (a new carrier portal quirk, a field convention, a tab rename), fold it back in here.

## When to use
The user wants both halves for one case: file the claim online **and** send the LOR. If they
only want one, defer to the single skill (`file-claim` or `lor-send`) directly.

## Inputs
- **Case** — driver/client name (to find the Drive case folder).
- **Party** — `1P` (client's own carrier) or `3P` (at-fault carrier).
- **Case manager** — for the form contact block + LOR signature (ask if not a directory CM;
  for a non-listed CM like a new hire, get their callback line + team email — see
  [[onboarding_cindy]] for Cindy Zhang's: 626-860-0173 / picase@lingtulaw.com).

Ask only for whatever is missing.

## Two hard approval gates (never auto-pass)
1. **Claim submit** — inside `file-claim`, the last screen before submission.
2. **LOR send** — inside `lor-send`, before the fax/email goes out.
Each is owned by its sub-skill; honor both. If the user says "dry run" for the LOR, stop at
the draft (deliver PDF to Downloads, no send/file/log).

---

## Step 1 — File the claim (run `file-claim`)
Invoke the **file-claim** skill for the case + party. It finds the case, reads the intake,
verifies every field, drives the carrier portal, PAUSES for submit approval, captures the
**Claim #**, and writes it to the intake sheet (1P→`I15`, 3P→`L19`) + posts to the case Chat.

**Carry forward from this run:** carrier `Claim #`, the case folder id, intake `.xlsx` id,
`1#Legal Documents` folder id, the CM, and the party.

### Carrier portal discipline (critical — learned on Mercury 1P)
- **Mercury files online with no login** at `https://mercury.assured.claims` (the "Assured"
  digital flow): File a new claim → Auto → answer the wizard. The insured name + policy #
  screen does a live policy match ("We've found a match").
- **NEVER fabricate facts of loss / collision dynamics.** For every narrative or substantive
  field the intake marks "Pending" (FOL, point of impact, moving-vs-stationary, collision
  type, signaling, driver behavior, hit-and-run, departure/destination, body type/color/make,
  plates, seatbelt, airbags, hospital admission) → use the form's **"I don't know" / Skip**.
  Confirm genuinely-uncertain binary facts with the user (driving vs parked; hit-and-run);
  don't guess.
- **Logistical fields may be approximate.** Unknown accident location → use the client's
  home address (intake C7) as a **placeholder** and tell the user; the CM corrects exact
  details with the adjuster. Date/time picker is 30-min granularity (10:25 → 10:30).
- **Injuries:** fill the body-map only from the intake's documented injury list (ask the
  user for it if not parsed); pick "muscle soreness / generalized pain" for plain "X pain",
  never a specific diagnosis you don't have; skip symptoms with no matching option
  (dizziness/tinnitus) — they reach the adjuster via records later.
- File on behalf: "Someone else" → relationship **Attorney** → firm contact block.

## Step 2 — Resolve adjuster email + un-highlight confirmed intake fields
Now that the claim # exists, finalize the intake fields it determines (see
[[intake_sheet_highlight_convention]]):
- **Derive the adjuster email where the carrier templates it from the claim #.** Mercury:
  intake stores `MyClaim+[CLAIM#]@mercuryinsurance.com` → write the resolved
  `MyClaim+<CLAIM#>@mercuryinsurance.com` into **I18** (1P) / **L22** (3P).
- **Un-highlight the now-confirmed cells** (claim #, adjuster email): the intake `.xlsx`
  marks pending fields yellow via cell style **`s="9"`**; swap to its un-highlighted twin
  **`s="8"`** (same font/border, no fill — the style other confirmed cells use). Leave still
  -pending fields (e.g. PD adjuster "Pending") yellow. Edit `xl/worksheets/sheet1.xml` by
  regex (openpyxl is NOT installed), values as `t="inlineStr"`, re-zip, `gws drive files
  update --upload` same fileId with `supportsAllDrives`. Verify with `read_intake_claim.py`.

## Step 3 — Send the LOR (run `lor-send`)
Invoke the **lor-send** skill for the SAME party, now that the claim # is in the intake (the
LOR template pulls `[Claim Number]` from it). It drafts from the latest Drive template,
renders the PDF, shows it for approval, sends **fax-first** (Mercury LOR fax `+1 866-268-8494`,
subject `Claim No. <claim#>`), files the PDF to `1#Legal Documents`, **posts a team notice to
the case Chat space** (`Claude sent <1P|3P> LOR via <fax|email>` — lor-send Step 8.5), and
proceeds to Step 4. Pass the CM so the signature/contact matches what was used on the form.

## Step 4 — Log the LOR on the Master tracking sheet
lor-send Step 8: find the case **row by client name** (NOT by CM→tab) in the PI Master Sheet
(`1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`) and write the send date with `values update`
(no formatting change).

- **⚠️ Use exact live tab titles** — they get renamed. The former `Picase` tab is now
  **`Picase(Cindy)`** ([[onboarding_cindy]]); reading range `Picase` returns empty and
  silently misses the case. Always `spreadsheets.get` the tab titles first if a name search
  comes up empty.
- **Picase(Cindy) / Piteam(Jerry):** separate `1LOR` (col **F**) / `3LOR` (col **I**)
  columns, bare `M/D` date (e.g. `6/9`), replacing the `P` placeholder.
- **Claims(Amos):** single `LOR Status` column (col **E**), shorthand `M/D(s)1P` / `M/D(s)3P`
  (`(s)`=sent); don't clobber an existing entry — combine (`6/9(s)1P&3P`) or confirm.

## Step 5 — Confirm & clean up
Report end-to-end: carrier + party, **Claim #**, intake cells written (claim # + resolved
email, un-highlighted), Chat post, LOR channel + recipient + status, filed PDF link, and the
tracking cell updated. Remind the CM to confirm coverage/limits with the adjuster and to tell
the client not to speak with the carrier directly. Clean up scratch dirs (`~/claim_work`,
`~/lor_work`).

---

## Notes & gotchas (fold new learnings in here)
- **Don't double-file.** If a claim was already filed for this case/party (claim # present
  in intake), filing again creates a DUPLICATE carrier claim — stop and confirm first.
- Approval gates are non-negotiable: claim submit + LOR send. Outbound Chat posts may also
  be permission-gated — surface the exact message and ask.
- Brand-new cases may not be on the Master sheet yet (no row to log against) — say so rather
  than invent a row; offer to add it once the new-case flow has run.
- Sub-skills: [[file-claim]] portal playbooks live in its `references/`; [[lor-send]] channel
  = carrier `insurance list` tab (fax→email→draft-only). Both are dependency-free (`gws` CLI
  + bundled Python; fax via `send-fax`/RingCentral).
- Cross-refs: [[intake_sheet_highlight_convention]], [[onboarding_cindy]], [[firm_directory]],
  [[ringcentral_fax]].
