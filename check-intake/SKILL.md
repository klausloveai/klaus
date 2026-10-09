---
name: check-intake
description: |
  Intake of INCOMING settlement checks for 凌图律所 / Law Office of Shenqi Cai APC —
  everything that happens between "Klaus scanned the checks" and "the money is ready to
  deposit". Trigger it whenever a scanned check or a batch of them arrives, usually as a
  bare attachment with no instruction: a file named `收据_YYYY-MM-DD_HHMMSS.pdf` or
  `MX-M476WH_YYYYMMDD_HHMMSS.pdf` (the office scanner), or on "收到支票", "新收到的支票",
  "这些支票", "记录一下这几张支票", "存入前先记一下", "/check-intake". For each check it
  records the deposit in the IOLTA Account Journal, splits the scan and renames one PDF per
  client, posts a one-line notice WITH THE CHECK ATTACHED to that case's Google Chat space,
  files the PDF into the right Drive folder (Case Disbursements if the case has finished
  collecting money, otherwise the case folder's own settlement subfolder), and creates the
  Pending Disbursed tab whenever it created a Case Disbursements folder. It NEVER deposits,
  never writes a disbursement check, and never decides a coverage question it cannot prove
  from the PI Master Sheet — those stop and ask Klaus. The OUTGOING side (disbursement
  packets, provider/client checks, Pending→Completed) belongs to `accounting-agent` and
  `case-settles`, not here.
---

# Check Intake — incoming settlement checks, pre-deposit

The money has arrived but is not in the bank yet. This skill is the whole path from the
scanner to "ready to deposit", run once per check.

## Files & IDs

- **Account Journal** — `~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/Lingtu Law-Disbursement/IOLTA#3618/Account-Journal.xlsx`, sheet `Account journal`. Back it up to `Backups/` before every write.
- **`_STATE.md`** — same folder. The live state file; append a block after every batch.
- **Pending Disbursed Sheet** — gsheet `1b_vPr9WD7P9arR6DTTJRxeWs0apk8DTiTgc2iAzIrR0`. Templates: `Template of 1/3` **sheetId 0**, `Template of 50/50` **sheetId 1179762877**. Index tab `🔍 Search` **sheetId 2016288373**.
- **Case Disbursements** — Drive folder **`1wIM0orXM7t4ogE6RgQIUAEYYU6pSRj2v`** (one folder per client, multi-client joined with `:`).
- **PI Master Sheet** — gsheet `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`, tabs `Claims@` / `Piteam@` / `Picase@` / `Klaus@`. Columns: **A DOL · B Client Name · C Retainer · E Case Status · G 1LOR · H 1Coverage · I 1Liability · J 3LOR · K 3Coverage · L 3Liability · M Property Damage**.
- Google Chat case spaces are named `<Client>-<DOL>(<X>)` where X = owning CM group (A/J/R/K). Always Klaus@ identity.

---

## Step 0 — Get the right file

The scanner leaves several files per batch. `<name> (dragged) N.pdf` fragments are **NOT
reliably subsets** of the same-timestamp full PDF — on 2026-08-24 the 21-page "full" file was
an OUTGOING disbursement packet while the 9-page fragment Klaus attached was a completely
different set of incoming checks.

1. `ls ~/Downloads | grep <timestamp>` and print the page count of each sibling.
2. **Read the file Klaus actually attached.** Only reach for a larger sibling to check whether it holds
   *additional* checks, and say so when you do.
3. Scans are often **mixed** — incoming checks on some pages, outgoing disbursement checks on others.
   Process only the incoming ones; name the outgoing pages and leave them.

## Step 1 — Read every check and dedup

Pull from each: carrier, **check number**, amount, issue date, claim #, policy #, DOL, insured,
claimant, coverage type (3P BI / UM / UIM / MedPay), payee line, memo.

**Dedup by CHECK NUMBER, never by client name.** One client can have several unrelated
deposits (Stephen Li: a Tesla $1k MedPay and a Kemper $30k BI — a name match nearly skipped
the new one). Search the journal for the check number *and* for the claim number, which
surfaces co-claimants on the same claim.

### Is it trust money?

Record it only if the **law firm is a payee** AND the coverage is bodily-injury-side
(BI / UM / UIM / MedPay).

> ⛔ **Property Damage / Collision never enters the IOLTA — not even when the firm is the
> payee "f/b/o" the client.** Klaus ruled this 2026-08-20 on Kemper check 6153439518 ($3,000,
> Allen Ning Wang): do not record, do not deposit, route it to the client outside trust.
> The earlier, narrower version of this rule (exclude only when the firm is not a payee) is
> wrong. Journal row 362 was recorded under the old reading and is a known inconsistency.

## Step 2 — Journal

Append at the **tail** of `Account journal`; do not insert rows above the `--- AUGUST PENDING ---`
marker — other sessions append at the tail too and inserting renumbers rows they have recorded.

Per row: A blank (no date — the deposit date comes from the bank at month end) · B payor ·
C `Deposit` · D check # · E purpose · F amount · G/H blank · I client.

The purpose string carries everything a reader needs three months later: coverage, claim #,
policy #, DOL, insured, whether it is policy limits, who else is on the claim, the check date,
the scan date, and `to deposit`.

- Copy the row style from the row above (`openpyxl`, `copy.copy(cell._style)`).
- **Client naming**: one consistent spelling per client. When a client has more than one matter,
  qualify with the DOL — `Dacheng Xu (5/13/2026)`, `Jingrui Hu (10/18/2025)` — or the ledger merges
  two accidents.
- Verify after writing: print the new rows, check the batch total, and confirm no stray column-H
  formula ghosts below row 240.

## Step 3 — Split and rename

One PDF per check into `~/Downloads/Checks <YYYY-MM-DD>/`:

```
<Client> - <Carrier> <Coverage> $<amount> (chk <number>) <MM-DD-YYYY>.pdf
```

When the client has several matters, put the DOL right after the name:
`Dacheng Xu 5-13-2026 - Tesla MedPay $1,000 (chk 2938261) 10-01-2026.pdf`.

## Step 4 — Chat the case space, with the check attached

**One line. English. No header, no field list, no closing sentence.** A six-line block with
carrier / check # / claim # / insured was rejected as 太复杂 (2026-10-06).

```
3P Settlement $20000 received and will deposit to IOLTA account
```

Swap the coverage word for MedPay / UM / UIM. Amount plain, no thousands separator. On a space
shared by several clients, prefix the client name only:
`Hanwen Li - 3P Settlement $5500 received and will deposit to IOLTA account`.

Find the space by `gws chat spaces list` and match the display name — carefully: `Shuang Li`
and `Shuangjiang Du` both contain "Shuang". When a client has several matters, pick the space
whose DOL matches the check.

Two calls, as Klaus@:

```bash
# 1. upload — "filename" in the BODY is required, or you get 400 "Specify file name of the attachment to upload."
gws chat media upload --params '{"parent":"spaces/XXX"}' \
  --json '{"filename":"<Client> - <Carrier> <Coverage> $<amt> (chk <no>).pdf"}' \
  --upload ./<local file>.pdf --upload-content-type application/pdf
# 2. post with the returned attachmentUploadToken
gws chat spaces messages create --params '{"parent":"spaces/XXX"}' \
  --json '{"text":"<one-liner>","attachment":[{"attachmentDataRef":{"attachmentUploadToken":"<token>"}}]}'
```

An existing message **cannot** have an attachment patched in — delete it
(`gws chat spaces messages delete --params '{"name":"<message name>"}'`) and repost.
`messages create` has thrown a spurious 401 ("no native root CA certificates found"); retry
before treating it as an auth problem.

## Step 5 — File it: has this case finished collecting money?

This is the only judgement call in the skill. Read the client's row on the **PI Master Sheet**.

| Situation | Where the check goes |
|---|---|
| MedPay only, 3P not received yet | case folder's own **`6#` settlement subfolder** — do NOT create a Case Disbursements folder |
| 3P received **and** no higher UM/UIM on our side | **Case Disbursements / `<Client>`** — create it if absent, even if MedPay is still outstanding |
| 3P received but a UIM claim is still open | case folder's `6#` subfolder — not done collecting |

Reading column **H (1Coverage)**:

- **Blank, with 1LOR and 1Liability also blank** → no 1P claim was ever opened → no UIM to wait
  for → decidable. (Xuezhi Hu, 2026-10-08.)
- **A dollar figure** → that is the UM/UIM limit; compare it to the 3P limit just collected.
  UIM pays only the excess, so limit ≤ 3P limit means no UIM recovery.
- **The word "Cleared"** → coverage was verified but the limit was never written down.
  **NOT decidable — stop and ask Klaus.** The intake sheet does not carry auto policy limits
  either (probed 2026-10-06), so there is nowhere else to look.

> To make this step mechanical, column H must carry the UM/UIM limit as a number instead of
> "Cleared". Worth raising with Klaus whenever it blocks a batch.

**Also sweep the case folder's `6#` subfolder** (`6#Settlement Documents` or
`6#Folder-Signed Releases&Checks&Invoice&Disbursements`): any earlier check scans already
sitting there get **copied** into the new Case Disbursements folder, renamed to the Step 3
convention, so the disbursement folder holds every check for the case. Leave the original in
place. Releases and invoices stay where they are — checks only.

Upload with the two-call pattern (`files create --upload`, then `files update` with
`addParents` / `removeParents` + the real name) — a one-call create stringifies `parents` and
drops the file in the shared-drive root as "Untitled".

## Step 6 — Pending Disbursed tab (default, whenever Step 5 created a folder)

Creating a Case Disbursements folder ⇒ create the Pending tab. No longer ask (Klaus,
2026-10-06). If the check went to the `6#` subfolder instead, no tab.

- **Re-list the tabs immediately before creating one.** Other people add and rename tabs
  constantly — a `duplicateSheet` 400'd on "already exists" on 2026-08-17, and the tab count
  moved 77 → 75 inside seven minutes on 2026-08-20.
- **Retainer type comes from PI Master Sheet column C**, not from Klaus: `Standard 1/3` →
  `Template of 1/3` (sheetId 0); `New 50%` → `Template of 50/50` (sheetId 1179762877).
  The two templates compute differently — 1/3 takes the fee off the gross, 50/50 takes it off
  the net after costs and reduced liens.
- Fill **A1** client · **B1** DOL · **C1** status, e.g. `scanned 10/8/2026 (to deposit)` ·
  the settlement amount in its own row: **B2** 3P / **B3** 1P UM-UIM / **B4** 1P Medical Payment.
  Everything else is a formula. Green (`{red:0,green:1,blue:0}`) the settlement cell and B5.
- Existing tab → verify it matches the check to the dollar **and** on DOL, and leave it alone.
  Mismatch → raise it, never overwrite.

### 🔍 Search index

Current layout — **A** `=IFERROR(IF(INDIRECT("'"&D<r>&"'!C1")="","",INDIRECT("'"&D<r>&"'!C1")),"")`
(pulls the tab's own **C1**, which is why Step 6 writes a status there) · **B**
`=HYPERLINK("#gid=<gid>","<Client>")` · **C** DOL · **D** tab name.
Insert a row in alphabetical order by column B. *(The layout has changed before; re-read row 1
and a sample row before writing.)*

## Step 7 — Close out

Append a block to `_STATE.md`: the batch total, a row-by-row table (journal row, payor, check #,
amount, client, DOL), every folder and gid created, what was verified against what, and every
open question with enough context to act on it cold.

---

## Invariants

- **Never deposits, never cuts a check, never updates the 2026-Disbursement Sheet.** Those are
  `accounting-agent` (Trigger A) and `case-settles`, after the money clears.
- **Never guess an attribution.** No claim number and no DOL on the check, and the client has
  several matters → record the deposit with the client marked `(accident TBD)`, skip Chat and
  filing, and ask. (Tesla 2938261 sat that way from 10/5 to 10/6.)
- **Read every number off the check itself.** Never carry an amount over from the Pending tab or
  the Master Sheet — those are what you are checking it against.
- Report a tie-out when you find one (the five Allstate MedPay deposits summing to exactly the
  $5,000 on Shuang Li's tab), and report a mismatch the same way — e.g. Meifang Lai's journal
  deposit $26,756.76 vs her tab's 3P $30,000, the $3,243.24 difference being exactly the
  Medicare line, i.e. withheld at source and must not be paid again.
- Back up `Account-Journal.xlsx` before every write; verify after every write.
