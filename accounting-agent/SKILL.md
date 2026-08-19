---
name: accounting-agent
description: >
  IOLTA trust-accounting workflow for 凌图律所 / Law Office of Shenqi Cai APC (active
  account #3618). Use whenever the user uploads a settlement breakdown screenshot +
  disbursement-checks PDF ("record this disbursement", "update the disbursement sheet",
  a settled case — including a bare `<Client>-Disbursements.pdf` dropped with no instruction;
  for that end-to-end case, `结案` is the entry point that sequences this skill),
  or a month-end bank record/CSV ("reconcile", "monthly reconcile",
  "update account journal to the bank"). Per settled case: verify math + funding →
  update Disbursement Sheet (color-coded, today's disburse date) → record Account Journal
  (content only) → archive PDF to case sub-folder 6 + move folder to "8. Settled" →
  green-flag & move the case Pending→Completed disbursed sheet, delete from Pending →
  draft the "Case settled" team email (owning team read off the PI Master Sheet tab, Klaus's
  signature, disbursements PDF attached, case label) for Klaus to approve before sending.
  Also triggers on "发结案邮件 / 通知 team 案子结了 / case settled email".
  Then (PI auto only) hand off to `settled-case-marketing-pkg` to extract marketing material and
  file the case folder into its DOL-year folder.
  At month-end: mirror Journal to bank → build Client Ledgers → three-way Monthly Reconciliation.
---

# Accounting Agent — IOLTA #3618 Workflow

## Files & IDs
- Root: `~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/Lingtu Law-Disbursement/IOLTA#3618/`
  - `2026-Disbursement Sheet.gsheet` → Google Sheet id **`1Av8_fj3MAekCM6RujmGWuFsYRnSG6MMbAskvPkFcs2U`**, tab **`Internal `** (trailing space)
  - `Account-Journal.xlsx` · `Client-Ledger.xlsx` (1 tab/client) · `Templates/` · `Monthly Reconciliations/`
- Active acct **#3618** = `3252 1786 3618` (opened 5/4/2026). Closed acct **#4854** = `3252 1006 4854` (READ-ONLY reference; wired $386,306.90 carryover into #3618).
- W9 folder (for provider hyperlinks): Drive folder id `1oWX7kFan5W8M7uW6RHkvRu1RiJRFAf9Y`.
- Read Google Sheets via `gws sheets +read`; write via `gws sheets spreadsheets values batchUpdate`. Edit xlsx with openpyxl.

## Disbursement Sheet column map (tab `Internal `)
A Date of Disbursed · B Client · C DOL · D 3P · E UM · F UIM · G MP (received) ·
H MP post-subrogation · I Total · J Client Recovery · K Attorney Fee · L Case Cost ·
M Medical Liens · N Amount Check `=I-J-K-L-M` **must = $0** · O Firm `=K*0.65` ·
P Dept `=K*0.35` · Q Referrer / R Referral Fee = **USER fills, never touch** ·
provider lien columns alphabetical from **U** onward (header = `=HYPERLINK(w9url,"Name")`).

---

## TRIGGER A0 — Incoming settlement check(s) received (scanned before deposit)
Klaus scans every settlement check he receives and sends it here BEFORE mailing/depositing. For each check:
1. **First check "存过吗?"** — dedup by **CHECK NUMBER**, not client name (one client can have several separate deposits — Stephen Li had a Tesla $1k MedPay AND a Kemper $30k BI; a name-only match falsely flagged the new one as a dup and nearly skipped recording it).
2. **Record it as a pending DEPOSIT** in the Account Journal JULY/…-PENDING block (payor, check#, amount, client, claim#, "to deposit"/deposited date). Deposit-only, no cleared date until month-end bank.
3. **EXCLUDE non-trust checks** — do NOT record (and warn Klaus): a check whose coverage is **Property Damage / Collision**, or where the **law firm is NOT a payee** (body-shop money, client-only PD). E.g. Kemper PD to a collision center; Mercury Collision payable to client only.
4. **Build a Pending Disbursed Sheet tab for the case** (Sheet `1b_vPr…`) so lien-reduction can start later:
   - If the client already has a tab, skip. Otherwise `duplicateSheet` from **Template** (sheetId 0), name = client (multi-client `/`-joined, driver first).
   - Fill A1 client, B1 DOL, and the settlement amount(s): **B2 3P / B3 UM-UIM** (Total B4, Fee B6, Recovery B7 are formulas — auto). Green the received-settlement amount cell(s). Providers left blank — filled during lien reduction.
   - Add a row to the Pending **🔍 Search** tab (sheetId 263451925), alphabetical by client: col A = `=HYPERLINK(".../edit#gid=<tab gid>","<client>")` (click-to-jump), B = DOL, C = tab name.
5. This is the pre-work for the eventual disbursement (Trigger A) — the tab is where Amos computes the lien reductions.

---

## TRIGGER A — Single settled case (screenshot + checks PDF)

**Step 1 — Verify amounts AND funding**
1. From screenshot: client, DOL, coverage (3P/UM/UIM/MP), Total, Client Recovery, Attorney Fee, Case Cost, each provider's lien (original + reduced).
2. From checks PDF: every check's #, payee, amount, memo.
3. Identity: `Total = Recovery + Fee + Case Cost + Σ(reduced liens)`.
4. Match every check to a breakdown line (1 client-recovery check + 1 per provider).
5. **Funding check — is the settlement money actually IN trust?** Search the #3618 journal for the client's deposit(s); if not there, search #4854 (money may be pre-5/2026 carryover, e.g. Wei Feng's 3P was a 3/19 #4854 deposit). Still missing → it may be in **Lashine Law Office IOLTA-5429** (a third, affiliated-firm trust account — Yu Ren's $3,001.83 MP was found there; older checks paid to "Lashine Law Office" land there). Money in 5429 is NOT in #3618 — it must be transferred/accounted for before disbursing against it. Sum of confirmed deposits must ≥ the disbursement total. **If underfunded, STOP and tell the user — never disburse on another client's funds.** An incoming check may also be issued-but-not-yet-deposited (e.g. Cheng Peng's USAA check dated 6/30 arrived after the 6/30 bank cutoff) — record its deposit as pending and say so.
6. **Any mismatch → raise it immediately. Never guess.** DOL on the sheet vs the letter/checks differing, or coverage type differing (sheet UM vs screenshot "3P") → ask the user which is right before writing.

**Step 2 — Update Disbursement Sheet**
1. Locate the client's row by fresh name search (the user re-sorts the sheet — NEVER reuse a cached row number). No row → append after the last used client row with the full formula set (`I=SUM(D:F,H)`, `M=SUM(Y{r}:DX{r})`, `N=I-J-K-M-L`, `O=K*0.65`, `P=K*0.35`).
2. Write D–M; N is the `=I-J-K-L-M` formula (confirm it shows $0); O/P firm/dept formulas.
3. Leave Q/R alone.
4. Each provider lien column = reduced amount; **yellow-highlight that cell** (bg RGB 1,1,0). User manually flips it green when that provider cashes.
4b. **Status color-code the row** (green = RGB 0,1,0 · yellow = RGB 1,1,0 · confirmed by user on Cheng Peng row). ⚠️ **Re-search the client's row number IMMEDIATELY before every color batch** — the user re-sorts constantly; coloring a stale row number paints another client's row (happened once: Cheng Peng's colors landed on Xiuhuan Xie). Values-write and color-write must each do their own fresh row lookup.
   - **D/E/F/G/H (settlement cols)**: GREEN each coverage whose incoming check is actually received; $0 / not-received cols stay UNCOLORED.
   - **I Total**: GREEN (final amount confirmed).
   - **J Client Recovery & K Attorney Fee**: YELLOW (checks not yet cashed / fee not swept) — user flips green later.
   - **L Case Cost**: GREEN if $0; YELLOW if nonzero (until cleared).
   - **M Medical Liens**: GREEN when it matches both the disbursement letter and the computed Σ.
   - **N Amount Check**: GREEN if $0, YELLOW otherwise.
   - **O Firm**: GREEN (default). **P Dept**: YELLOW (default — user flips manually).
5. New provider → insert a column in alphabetical position; header = HYPERLINK to its W9 (search the W9 folder; if no W9 found, plain name + tell user to add W9). Gotchas: (a) if the new column exceeds the grid, `appendDimension` COLUMNS first (400-error "exceeds grid limits"); (b) older rows' **M formula only sums `Y:DK`** — if a provider lands past DK, widen THAT row's M to `=SUM(Y{r}:DX{r})` or the new cell won't count and N ≠ 0; (c) column letters shift after every insert — re-read header positions before writing values.
6. Read back and confirm N = $0.

**Step 3 — Record in Account Journal (CONTENT ONLY, NO DATES)**
1. Append rows: payor/payee, check #, amount, client, purpose (deposit row for the settlement, one disbursement row per check).
2. **Do NOT fill deposit/disburse dates** — dates are assigned only when the bank record clears them (Trigger B). Mark these as pending.

**Step 4 — Archive the PDF + move the case folder to Settled**
1. Find the client's CASE folder in Drive (search `corpora=allDrives` + `supportsAllDrives=true`; folder name = client name, sometimes with a DOL suffix like "Cheng Peng  2:5:2026"). Case folders live under the stage folders (`1. Pending` … `7. Reduction`), all children of parent `1JwQtWURVoHxzYOLnOXvljc8ayBJTPRpp`. If several same-name folders match, pick the one containing the `N#Folder-…` numbered subfolders / matching DOL; still ambiguous → ask.
2. Upload the disbursement-checks PDF into the case folder's **sub folder 6** — match by the leading `6#` (naming varies: `6#Folder-Signed Releases&Checks&Invoice&Disbursements`, `6#Settlement Documents`, …). If the PDF is already somewhere in Drive, `gws drive files copy` (with `--json '{"name":…,"parents":[…]}'`) instead of re-uploading. If the case folder sits in `8. Completed`, still move it to `8. Settled`. Gotcha: `gws drive files create --upload` stringifies the `parents` array (file lands in the shared-drive ROOT as "Untitled"). Do it in 2 calls: (a) `files create --upload <path> --params '{"supportsAllDrives":true}'`, then (b) `files update` with `--json '{"name":"<Client>-Disbursements.pdf"}'` + params `addParents=<subfolder6 id>`, `removeParents=0AInzY7WhoRguUk9PVA` (shared-drive root), `supportsAllDrives:true`.
3. Move the case folder to **`8. Settled`** (id `1P35bCgC82Lh6Xftpbt03TX1Cs20G6BoB`): `gws drive files update --params '{"fileId":"<caseFolderId>","addParents":"1P35bCgC82Lh6Xftpbt03TX1Cs20G6BoB","removeParents":"<currentStageFolderId>","supportsAllDrives":true}'`.
4. ⚠️ A sibling `8. Completed` also exists — always use `8. Settled`.

**Step 4b — Pending → Complete transfer (mark the case done)**
Two Google sheets: **Pending Disbursed** `1b_vPr9WD7P9arR6DTTJRxeWs0apk8DTiTgc2iAzIrR0` (Amos computes cases here; one tab per case, multi-client tabs stack blocks vertically) and **Completed Disbursed** `1EvsbLjAuRdTTfH3uyEmV3qFjmAtKCdfBPByVCMAF1kA` (archive; one tab per case; has a `🔍 Search` index tab). Do this when the user says "转到 complete / 把 X 结案":
1. **Pending tab**: for every client block, GREEN (RGB 0,1,0) all non-zero figures ($0 stays blank); prefix each client-name header with ✅; write **Date of Disburse = today** into the cell right of the DOL (col C of each block's row-1). (This is the disburse date because accounting isn't cleared yet.)
2. **copyTo → Completed sheet**: `gws sheets spreadsheets sheets copyTo` (params `{spreadsheetId:PENDING, sheetId:<tabId>}`, json `{destinationSpreadsheetId:COMPLETE}`). Rename the copy: tab name = all clients joined by `/`, **driver first** (e.g. `Yida Gao/Zihan He/Anci Yang`).
3. **Multi-client case, only SOME clients done**: in the Completed copy, `deleteDimension` the not-yet-disbursed clients' block rows (keep only completed). In the Pending original, delete the completed blocks and rename the tab to the remaining client(s) (e.g. drop Yida Gao once he's moved, rename tab to `Yike Li`).
4. **🔍 Search index** (Completed sheet): `insertDimension` a row at index 1 and write `[Date of Disburse, Client Name(s), DOL, Tab]` — kept sorted disburse-date descending (newest on top). The **Tab (col D) MUST be a clickable link to the tab** — get the copied tab's gid (`spreadsheets.get` → sheets.properties.sheetId), then write `=HYPERLINK("https://docs.google.com/spreadsheets/d/1EvsbLjAuRdTTfH3uyEmV3qFjmAtKCdfBPByVCMAF1kA/edit#gid=<gid>","<tab name>")`.
5. **Delete from Pending** = the case is done. (Whole-case tab: delete it. Partial: delete the moved blocks only, per step 3.)
Green helper: `repeatCell` with `userEnteredFormat.backgroundColor {red:0,green:1,blue:0}`. Row indexes are 0-based; re-read the tab first (blocks shift when clients are deleted).

**Step 4c — "Case settled" team notification email** (do this LAST, after 4b — the email links the Completed tab, so 4b must be finished or there is no gid to link)
1. **Determine the owning team from the PI Master Sheet** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM` — it has one tab per team: **`Claims@` / `Piteam@` / `Picase@`**. Find the client in col B of each tab; the tab it lives in IS the team → send from that team's mailbox. (Also confirms DOL + settlement amount — cross-check them.)
2. **Switch gws identity to that mailbox** with `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` (NOT `GWS_CONFIG_DIR`, which is silently ignored): `~/.config/gws-claims` = claims@, `~/.config/gws-piteam` = piteam@, `~/.config/gws-picase` = picase@, default `~/.config/gws` = klaus@. Verify with `gmail users getProfile` before composing.
3. **Compose** — To: **cassie@lingtulaw.com, joe@lingtulaw.com, elena.j@lingtulaw.com** (Elena is `elena.j@`, NOT `elena@`). Subject: **`<Client>-<DOL M/D/YYYY>-Disbursements`**. Body (flowing HTML paragraphs, no hard wrap):
   `<p>Hi Team,</p><p>Case settled.</p><p><a href="<link>"><link></a></p>` where `<link>` = `https://docs.google.com/spreadsheets/d/1EvsbLjAuRdTTfH3uyEmV3qFjmAtKCdfBPByVCMAF1kA/edit?gid=<gid>#gid=<gid>` (the Completed tab's gid from 4b step 4).
4. **Signature = KLAUS's**, not the team mailbox's preset. ⚠️ claims@'s default signature is **Amos Feng's** — using the mailbox preset would sign the wrong person. Pull Klaus's: default-config `gws gmail users settings sendAs list` → the `isDefault` entry's `signature`, and append that HTML verbatim.
5. **Attach the disbursements PDF** (`<Client>-Disbursements.pdf` from `PI Team Folder/3. Disbursements/Case Disbursements/<Client>/`).
6. **Create as a DRAFT and show Klaus — never auto-send.** ⚠️ The raw MIME is ~1–2.5 MB, which blows the shell arg limit (`argument list too long`) if passed via `--json`. Write the message to a `.eml` and upload:
   `gws gmail users drafts create --params '{"userId":"me","uploadType":"multipart"}' --upload <file>.eml --upload-content-type "message/rfc822"`
   (`uploadType":"media"` FAILS with "Media type 'multipart/related' is not supported" — must be `multipart`.)
7. **Label the draft** with that case's Gmail label in that mailbox (`labels list`, match the client name; case labels are ONE combined label per case, e.g. `Lirong Huang/Chun Yin Chiu/Jialin He`). If the label does NOT exist in the team mailbox, that usually means the case was actually run out of **klaus@** — check klaus@'s labels and ASK Klaus which mailbox to send from rather than creating a new label there.
8. **After Klaus approves, send** with `drafts send`. ⚠️ **Sending DROPS the case label** (the sent message comes back with `['SENT']` only) — immediately re-apply it with `messages modify --json '{"addLabelIds":["<labelId>"]}'` and verify.

**Step 4d — Marketing material extraction + file the case by DOL year** (PI AUTO only; skip dog-bite / Hernán litigation)
Step 4 dropped the case folder into `8. Settled`, whose lobby is exactly the queue for this. Hand off to the
**`settled-case-marketing-pkg`** skill: it pulls the carrier's settlement check out of the Folder 6 disbursement PDF
+ the PD photos/videos out of Folder 2, packages them into `0. Marketing/人伤/<Clients>-<M-D-YY>/`, then moves the
case folder out of the lobby into its **DOL-year** folder (`2024`/`2025`/`2026`).
⚠️ Do NOT hand marketing the disbursement PDF itself — it contains the client's home address (client-recovery check),
the fee/lien breakdown, and the provider lien amounts. Only the incoming settlement check page(s) go out.
Every settled PI-auto case gets one (no amount threshold); client consent for marketing use is covered per Klaus 2026-08-18.

> Client Ledgers are NOT built per-case. They are built once at month-end (Trigger B) so each ledger carries the real bank-clearing dates and isn't reworked.

---

## TRIGGER B — Month-end bank record (CSV / statement)

**Step 5 — Mirror Account Journal to the bank**
1. The Account Journal records **only transactions that appear in the bank record (cleared)**. Outstanding/uncleared checks go in an `--- OUTSTANDING ---` memo section (no dates, no running balance); new-month activity after the close goes in a `--- <MONTH> PENDING ---` section.
2. Assign each posted row its bank clearing date; order chronologically; running-balance formula in col H.
3. **Dry-run first**: parse the bank CSV, verify its own running balance is zero-error, build the rows, compute the projected ending balance — only write to the journal when it ties the bank ending to the cent. Back up the xlsx before writing.
4. **Batched deposits (Counter Credit): HOLDING-list protocol.** User uploads component checks over several messages. Log each batch into `_STATE.md` (client, insurer, amount, check#, claim#) — do NOT record to the journal yet. Only itemize when (a) user says it's complete AND (b) the components sum EXACTLY to the bank's CC amount. Sanity-check dates: a check issued after the CC date can't be in it. Checks with no client name on them → record "(confirm — client TBD)" and ask.
5. Match checks by CHECK NUMBER (not amount). Attribute remaining unknowns: unique-amount match against the Disbursement Sheet → auto-assign; ambiguous amounts ($450/$500/$1,000…) → check-number adjacency (same case = consecutive run) → still unclear, ask. Verify EVERY txn row ends with a client in col I — full-table scan, 0 gaps.
6. #4854 carryover arrives as "FUNDS TRANSFER CREDIT" deposits — label client "Carryover (#4854)".
7. **Anomalies to record, not hide**: duplicate/double-cashed checks and insurer overpayment checks stay in the journal (money really moved) but get purpose "DUPLICATE/OVERPAYMENT — refund requested"; post the +credit when the refund lands. (Examples: Danny Qin 80089/800089 dup; Wei Feng extra Tesla 2732647.)

**Step 6 — Build Client Ledgers (one tab per client, month-end)**
1. For every client with activity, create a tab: opening (carryover from #4854 if any) + their journal rows in date order + live running-balance formula.
2. Gate: no ledger may go negative; Σ all ledger ending balances = Journal balance.

**Step 7 — Monthly Reconciliation (three-way tie)**
1. Generate `Monthly Reconciliations/Recon-3618-YYYY-MM-Month.xlsx` from the template.
2. Tie: **Trust Account Journal balance = Σ Client Ledger balances = Adjusted Bank Statement balance** (= bank ending + outstanding deposits − outstanding checks).
3. Preparer **Klaus Liu** (date = month-end); Attorney **Shenqi Cai, Bar# 348794** (date = month-end).

---

## Provider alias map (clinic brand ≠ W9/check-payee entity — do NOT flag as an error)
Name the provider column after the **W9/check-payee entity**, add the clinic brand in parens, record per the CHECK payee:
- **AZ PI Center** (Arizona Personal Injury Centers) → payee/W9 **Recalibrate Chiropractic LLC**
- **Prime MRI** → payee **Prime Rad Inc** · **One Health Medical** → payee **AVEVA Medical Aesthetics, Inc**
- **Exer Urgent Care** → payee **Exer Medical Corporation** · **San Gabriel ASC** → payee **MMB Solutions Group**
- **USC Arcadia / Methodist Hospital (L.A. Care / Medi-Cal subrogation)** → payee **Katch** (subrogation collector)
- A signed lien-reduction letter isn't always in the packet — provider email confirmation is acceptable (per Klaus).

## Invariants
- One consistent spelling per client — a name variant splits the ledger and creates phantom negatives; a similar-name confusion mis-attributes money (real case: Wei **Lin** vs Wei **Feng** — a $30k deposit sat under the wrong client until the funding check exposed it). Merge minor-guardian variants to one canonical form ("X (minor)").
- Flag any uncertain attribution in Notes as "confirm"; never silently guess.
- #4854 workbook is read-only for balances, but ATTRIBUTION errors found there may be corrected (back it up first, verify the per-client total is unchanged).
- Read back and verify key figures after every write; back up `Account-Journal.xlsx` before any full rebuild.
- Insert/delete operations leave stray H-formula ghost rows below the data — they fool "find last row" scans; wipe them when found.
- **`_STATE.md` (in the IOLTA#3618 Drive folder) is the live state file — update it after EVERY case/change** (last processed case, holding lists, pending items, refunds due). It survives session loss; the Drive folder is its durable home.

## State anchors (see _STATE.md for live detail)
- May 2026 reconciled **$780,092.77**; **June 2026 reconciled $1,049,028.91** (6/30, three-way tie, `Recon-3618-2026-06-June.xlsx`).
- Journal structure: cleared bank-mirror ends at bank cutoff | OUTSTANDING memo (33 checks $75,668.52 as of 6/30) | JULY PENDING.
- All 4 June CCs itemized (6/15 $250,500 · 6/22 $149,756.76 · 6/22 $75,000 · 6/26 $119,757.28); every cleared txn client-attributed (0 gaps).
- Client-Ledger.xlsx rebuilt: Summary + 24 completed pure-#3618 clients (book basis, each tab ends at retained fee; Σ $223,397.82).
- Refunds pending: Danny Qin 800089 $450 (dup check); Wei Feng Tesla 2732647 $20,000 (insurer overpayment).
- Blocked: carryover-client ledgers need the attorney-fee-sweep split ($209,076.13 in #4854 + $79,240.90 in #3618) allocated per client.
