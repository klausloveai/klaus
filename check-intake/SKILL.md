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
  collecting money, otherwise the case folder's own settlement subfolder), creates the
  Pending Disbursed tab whenever it created a Case Disbursements folder, and finally verifies
  every page against its archived copy before moving the scan out of Downloads. It NEVER deposits,
  never writes a disbursement check, and never decides a coverage question it cannot prove
  from the PI Master Sheet — those stop and ask Klaus. The OUTGOING side (disbursement
  packets, provider/client checks, Pending→Completed) belongs to `accounting-agent` and
  `case-settles`, not here.
---

# Check Intake — incoming settlement checks, pre-deposit

The money has arrived but is not in the bank yet. This skill is the whole path from the
scanner to "ready to deposit", run once per check.

## Files & IDs

- **IOLTA#3618 folder** — Drive id **`1Le1fdsT7d8rQDOVER1nLXw2kd4pQTWrf`**, today at
  `~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/Documents/Lingtu Law-Disbursement/IOLTA#3618/`.
  ⚠️ **The local path moves.** It was `My Drive/Lingtu Law-Disbursement/…` until 2026-10-13, when the whole tree
  was dropped into a new `Documents` folder and the old path began throwing FileNotFoundError. The folder **id**
  is stable — if the path fails, resolve it from the id rather than creating a file at the stale path.
- **Account Journal** — `Account-Journal.xlsx` in that folder, sheet `Account journal`. Back it up to
  `Backups/` before every write.
- **`_STATE.md`** — same folder. The live state file; append a block after every batch.
- **Pending Disbursed Sheet** — gsheet `1b_vPr9WD7P9arR6DTTJRxeWs0apk8DTiTgc2iAzIrR0`. Templates: `Template of 1/3` **sheetId 0**, `Template of 50/50` **sheetId 1179762877**. Index tab `🔍 Search` **sheetId 2016288373**.
- **Case Disbursements** — Drive folder **`1wIM0orXM7t4ogE6RgQIUAEYYU6pSRj2v`** (one folder per client, multi-client joined with `:`).
- **PI Master Sheet** — gsheet `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`, client tabs `Claims@` / `Piteam@` / `Picase@(Amos)` / `Picase@(Jenkins)` / `Picase@(Eeve)` / `Klaus@`. ⚠️ `Picase@` was split into three on 2026-10-16 — a batchGet naming the old single tab fails. Status here lags; see Step 5. Columns: **A DOL · B Client Name · C Retainer · E Case Status · G 1LOR · H 1Coverage · I 1Liability · J 3LOR · K 3Coverage · L 3Liability · M Property Damage**.
- Google Chat case spaces are named `<Client>-<DOL>(<X>)` where X = owning CM group (A/J/R/K). Always Klaus@ identity.

---

## Step 0 — Get the right file

The scanner leaves several files per batch. `<name> (dragged) N.pdf` fragments are **NOT
reliably subsets** of the same-timestamp full PDF — on 2026-08-24 the 21-page "full" file was
an OUTGOING disbursement packet while the 9-page fragment Klaus attached was a completely
different set of incoming checks.

0. **Copy every attached file into the scratchpad first, and work only from the copy.** A `(dragged)` file is a
   temporary drag copy and can vanish mid-run — on 2026-10-20 one disappeared between being read and being
   split, leaving a recorded check with no archivable PDF.
1. `ls ~/Downloads | grep <timestamp>`, then hash **each page's embedded image** of every sibling. Same-timestamp
   files have held entirely different documents (2026-10-16: four distinct pages across two "same" files).
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
surfaces co-claimants on the same claim. **Match the check number against column D as a whole field, never as a
substring of the joined row** — short IOLTA numbers false-positive inside long carrier numbers (`80490` sits
inside `1646804903`, 2026-10-15).

### A new check number is not proof of new money — test for a REISSUE

**Same claim # + same amount + same payee + a later check date** than a check already in the
journal means the carrier reissued, not that it paid twice. Dedup on the number alone would
book the money a second time: Xiaohang Li's AFICS $6,000 would have read as $12,000 collected
on a $6,000 claim. Then split on whether the earlier check was deposited:

- **Earlier check still pending (no cleared date)** → one recovery. **Update the existing row in
  place** — new check number, and a purpose line recording the supersession and that the old
  check must not be deposited. Do not add a second row. Re-read the client's total afterwards to
  confirm it did not double. Rename the filed PDF with `REISSUE` and the new number.
  (Xiaohang Li, chk 0012858411 → 0012883228, 2026-10-12.)
- **Earlier check already deposited** → ⛔ **STOP, record nothing, ask Klaus.** Three readings
  lead to opposite entries: the deposit was returned and the carrier reissued (one recovery);
  the carrier paid twice (overpayment — book both and arrange a refund, per the Danny Qin /
  Wei Feng precedent); or the "deposited" note was wrong. Name the split PDF
  `… - SECOND CHECK HOLD.pdf`. (Pu Tang, Wawanesa chk 0000188972 deposited 9/23 → chk
  0000197141 arrived 10/8, 2026-10-13.)

### Is it trust money?

Record it only if the **law firm is a payee** AND the coverage is bodily-injury-side
(BI / UM / UIM / MedPay).

**Read the whole payee line — it can name a lienholder.** GEICO chk 268503590 was payable to
"Law Office Of Shenqi Cai Apc **and** Peile Zhao **and Medi-Cal**" (2026-10-13). Record the
deposit as normal, but say so in the purpose and on the tab's C1: the check cannot be negotiated
until the lienholder endorses or is paid at source, and nobody downstream should assume the full
face amount is distributable.

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

One PDF per check into the **session scratchpad**, not Downloads — Downloads gets cleaned out
(the `~/Downloads/Checks <date>/` folders were gone within the hour on 2026-10-13) and Step 8
deletes the source from there anyway. The scan itself can always be re-split; the Drive copy is
the archive.

Name each one:

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

## Step 5 — File it: is this case still waiting on more money?

**The PI Master Sheet status lags — it is not updated in real time. Decide from the case's Google Chat
space** (Klaus, 2026-10-22). Read the recent messages there and answer one question: *after this check, is
another recovery still expected on this case?*

| What the case Chat says | Where the check goes |
|---|---|
| 3P settled, nothing else outstanding | **Case Disbursements / `<case>`** — create it if absent |
| 3P settled, **MedPay still to come** | **Case Disbursements** too — an outstanding MedPay does NOT hold it back |
| 3P settled **and a UIM claim will be made** | case folder's **`6#`** subfolder — no Case Disbursements folder |
| **MedPay on its own**, 3P not settled | case folder's **`6#`** subfolder |

So only two situations keep a check out of Case Disbursements: **a UIM claim still to come**, and **a
standalone MedPay**. Everything else gets the folder.

Column H (1Coverage) is no longer the test. A dollar figure there is still useful corroboration — if the
UM limit is at or below the 3P limit just collected, no UIM recovery is possible regardless of what anyone
says (Hongyu Luo, 2026-10-19: $20,000 UM vs $30,000 3P) — but "Cleared" means nothing and must not stall a
batch, and an explicit marker in the Master Sheet such as "11/10 Uber UM" or status 🔔Collecting is a reason
to look harder at the Chat, not a decision by itself.

When the Chat is silent or ambiguous on the UIM question, say so and ask Klaus rather than guessing.

**Also sweep the case folder's `6#` subfolder** (`6#Settlement Documents` or
`6#Folder-Signed Releases&Checks&Invoice&Disbursements`): any earlier check scans already sitting there get
**copied** into the new Case Disbursements folder, renamed to the Step 3 convention, so the disbursement
folder holds every check for the case. Leave the original in place. Releases and invoices stay where they are
— checks only.

### Folder naming — ONE folder per CASE, every client's name on it

Klaus, 2026-10-13: 一个案子一个 folder，加上所有客户的名字. Clients who share a claim share a
folder, names joined with `:` — `Li Liu Sun:Yanjun Pan`, `Alejandra Rios:Angel Michelle Miner:
Chantalle Verenice Miner`. Not one folder per client. The case folder's own name is the model
(`Li Liu Sun:Yanjun Pan 11:10:2025`).

**Add the DOL when the client has more than one live matter** — `Dacheng Xu 03/16/2026`, so his
3/16/2026 checks cannot land among the 9/11/2025 ones. Every other folder is plain names.

⚠️ Known violation to raise, not silently fix: claim 787612-GQ (DOL 10/19/2025) has one Pending
tab and one Chat space for Hanwen Li / Yehao Li / Zihan Liu but **two** folders — `Hanwen Li`
and `Yehao Li:Zihan Liu`. Merging moves files other people filed, so ask first.

### Uploading

Two calls, and **run them as two separate commands**, not chained: `gws drive files create
--upload`, then `gws drive files update` with `addParents` / `removeParents` + the real name.
A one-call create stringifies `parents` and drops the file in the shared-drive root as
"Untitled"; and a chained command that times out mid-way (a 1.5 MB PDF exceeded 120s on
2026-10-13) leaves exactly that orphan — recover it by running the `update` on its own.

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

## Step 8 — Verify the archive, then clear Downloads

Only after everything is filed. Klaus's rule: 先逐件比 MD5 再移废纸篓.

**Do not compare the source file's MD5** — what is in Drive are single-page splits, so the bytes
never match. Compare **the embedded scan image of each page**: hash every `page.images` payload
in the source PDF page, download the corresponding Drive file, hash its page image the same way,
and require an exact match per page.

- **Every page must be accounted for, including any check you HELD.** On 2026-10-13 six of seven
  pages were archived and the seventh — Pu Tang, held pending Klaus — had never been uploaded;
  deleting the source then would have left no copy of that scan. Filing the scan is independent
  of the hold: archive it with `HOLD` in the name and verify it too.
- All pages matched → **move the source to `~/.Trash`**, never `rm`. Reversible by design.
- Any page unmatched → file it, re-verify, and only then clear. Never delete on a partial match.

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
- **Run Python as `python3.14`.** Homebrew moved bare `python3` to 3.15 (2026-10-19), which lacks openpyxl and pypdf.
