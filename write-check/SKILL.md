---
name: write-check
description: |
  Write provider settlement / disbursement checks AND the client recovery check in
  Rentec Direct (rentecdirect.com) for 凌图律所 / Lingtu Law Office, driving the site in
  the browser (Claude-in-Chrome). Use whenever any of the following are mentioned: write a
  check, write checks, 开支票, 写支票, Rentec / Rentec Direct, "post expense", pay a
  provider, provider reimbursement, settlement disbursement check, client recovery check,
  cut a check to a clinic / to the client, pay the lien, "/write-check". Typical
  invocation: a case (client/driver name) + a disbursement letter / set of signed
  lien-reduction letters (often one multi-page PDF) → one check per provider (+ optionally
  the client recovery check), drafted from the IOLTA trust account. The skill checks/creates
  each vendor, fills the Post Expense form for every payee, and saves each as a DRAFT. It
  NEVER commits ("Post Expenses") without explicit approval — IOLTA trust money. Always
  trigger for any "write a check in Rentec / pay providers / pay the client" request.
---

# Write Check (Rentec Direct)

Cut disbursement checks from the firm's trust account in **Rentec Direct**
(`secure.rentecdirect.com`, logged in as Klaus Liu) by driving the browser with
**Claude-in-Chrome**. The "cut the checks" step only — not the surrounding
ledger/journal/reconcile bookkeeping.

**Trust money. The commit is irreversible. NEVER click `Post Expenses` until Klaus says so
(e.g. "确认过账"). Klaus often posts it himself — if he says "我处理了 / I handled it",
do NOT post; verify on the Ledger instead (see Step 5).**

## What gets a check (read the disbursement PDF once)

- **Each provider** → reduced amount from its **signed lien-reduction letter** (NOT the
  original lien). A plain bill with no reduction is paid at the bill's total. Category
  **7000 Provider Reimbursement**, memo `<Client>, DOL-<MM/DD/YYYY>`.
- **The client** (if the client recovery check is wanted) → **AMOUNT TO CLIENT** from the
  disbursement letter. Payee = the client. Category **7010 Client Compensation**, memo
  `Case Settlement, DOL-<MM/DD/YYYY>`, **address from the case intake sheet**.
- **Reconciliation check:** sum(all checks) must equal `Total Settlement − Attorney Fee`
  (= providers' reduced total + amount to client). State it; flag if it doesn't tie.
- Default bank account: **1001 Lingtu Law - IOLTA Account** (`bank_id=111793`). Constants
  every line: Payment Type **Print Check**, Property None, Date today, Check#/Ref# blank.

## Token-efficient execution (IMPORTANT — keep screenshots & round-trips low)

- **One screenshot per line, not per click.** Do a whole line in ONE browser_batch:
  open Payee dropdown → type name → (screenshot to confirm the match highlighted) → click
  it → set memo+amount by ref → done. Trust `form_input`'s text result instead of
  re-screenshotting; only screenshot to (a) confirm a dropdown match before clicking, and
  (b) verify the saved line / final ledger.
- **Verify totals via the Ledger, not by scrolling the draft.** The Post Expense viewport
  is short and fights scrolling. To see everything, open the permanent Ledger
  `/owners/bank_account.php?bank_id=111793` (or `get_page_text`) — don't burn screenshots scrolling.
  On that Ledger `get_page_text` returns nothing and `querySelectorAll('table')` is 0 (it renders without
  a real `<table>`); read it with `javascript_tool` over **`document.body.innerText`** split into lines —
  a 5-digit check number sits on its own line, so `L.slice(i-4, i+3)` around each one gives
  date / payee / category / memo / check# / amount / balance. Dumping every line at once trips the
  tool's cookie/query-string filter, so **filter to the check numbers you care about**.
- **Re-read refs only when they go stale.** Field refs (Memo/Amount) change after each
  Payee pick or New Transaction. One `read_page{filter:"interactive"}` per line is enough;
  Memo/Amount are the two you need.
- Resizing the window renumbers pixel coordinates — **prefer element `ref` clicks** (from
  read_page/find) over pixel coords for buttons like Add Vendor / Post Expenses.

## After posting: `case-settles` runs once the checks are PRINTED
Posting in Rentec is not the close-out. Klaus's order is **post → print → `/case-settles` on the signed packet**
(Klaus 2026-10-23: 结案我还没做 case settle，因为支票还没打印出来). So between posting and printing it is normal
for a case to have Rentec lines, sometimes even Internal / journal rows from a bank-recon backfill, while its
Pending tab still sits there marked ✅ — that is a case waiting on the printer, not a broken pipeline.
What IS a gap: checks **printed and handed out** with nothing downstream (Hongrui Ma / Tsz Shuen Chau, printed
10/8, found only at the 10/14 audit). When you finish posting, end with "checks posted — print, then run
`/case-settles`" so the next step has a name.

## Steps

0. **Funding check FIRST — was the settlement check deposited, and when?** (Klaus, 2026-10-13:
   "在这个 skill 前多做一个就是查找是否 deposit 支票，什么时候存入".) Before drafting anything,
   open `~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/Lingtu Law-Disbursement/IOLTA#3618/Account-Journal.xlsx`
   and search for the client. On a **Deposit** row, **column A IS the deposit date** (check rows leave
   A blank until the bank clears them), col D = the carrier's check #, col F = amount, col I = client.
   Report "deposited <date>, <carrier> check <#>, $<amt>" in the final table's header line.
   - **Dedup/match by CHECK NUMBER and amount, never by name alone** — the firm has repeat and
     near-duplicate clients (the journal itself warns "Jing Wang … NOT the same client as Jingjing Wang";
     Alejandra Rios and Angel Miner had two USD 7,594.62 checks on one claim).
   - **Not found in #3618?** Look in #4854 (pre-5/2026 carryover) and Lashine IOLTA-5429. Money in 5429
     is NOT in #3618. **Underfunded or not deposited → STOP and tell Klaus; never draft against
     another client's funds.**
   - Deposited but the month isn't reconciled yet is fine — say so rather than claiming it cleared.

1. **Connect & open.** select_browser → tabs_context_mcp. Go to
   **`https://secure.rentecdirect.com/owners/expense.php?bank_id=111793`**
   (Banking → IOLTA account → Post Expense). Confirm logged in as Klaus (one screenshot).
   ⚠️ **The app lives under `/owners/`, not `/Manager/`** — `secure.rentecdirect.com/Manager/…` returns a
   bare 404 and a bare `secure.rentecdirect.com/` bounces to the marketing site, both of which look like
   "logged out" and are not. If you land on the marketing page: LOGIN → **LOGIN TO RENTEC DIRECT**
   (`/owners/login.php`) → a Cloudflare "Just a moment…" interstitial clears itself in ~10s → a
   **"Continue as Klaus"** button resumes the saved session. Clicking that is fine; it asks for nothing.
   If it ever shows an actual password field or a CAPTCHA, STOP — never enter credentials, never solve a
   CAPTCHA; hand it to Klaus.
2. **Per payee** (provider or client), on the blank draft line:
   - Payment Type → **Print Check** (custom dropdown; resets to "Check" each new line).
   - Payee → custom type-ahead: click, type name, click the exact match (watch
     near-duplicates: "Advantage Plus MRI" ≠ "Open Advantage MRI"; "Sun Imaging, Inc" ≠
     "Sunnyvale Imaging Center"; "Integrative Physical Medicine Physicians" ≠ "Premier
     Integrative Health Center" ≠ "Prestige Integrative Health Center").
   - ⚠️ **Picking the payee auto-fills Mailing Address — read it and confirm it has a STREET.**
     Some vendors are **stub records** created inline by a past "Add …" and never filled in: the
     address box then shows the company name alone and **the check prints with no address**.
     (2026-10-14, Wei Lang: `Integrative Physical Medicine Physicians`, vendor id 991924, had no
     address, no Tax ID and Category 0000 — caught only because Klaus asked "这个是否是我们的 vendor?".)
     Name-only address ⇒ stop and fix the **vendor record** (Settings → Financial → Vendors &
     Payees) with the address + EIN off its W-9 and Category 7000, then fix the Mailing Address on
     the line itself — editing the vendor does NOT retro-fill a line (or an already-posted
     transaction) whose address was snapshotted at payee-pick time.
     See **"Provider W-9s"** below for where the W-9 is and, when it is a new one sitting in the case
     folder, **the backup copy you owe into `3. Disbursements/` afterwards**.
   - read_page → `form_input` Memo + Amount (digits only, e.g. `2841.00`).
   - **Category:** if the vendor has a default expense category it auto-fills correctly
     (verify it reads 7000 / 7010). If it shows **0000 Uncategorized**, fix it: click the
     Category dropdown, type the code (`7000`/`7010`), click the filtered result.
   - Click **+ New Transaction** for the next payee.
3. **Missing vendor?** If the Payee search shows only "Add …", create it first:
   Settings → Financial → Vendors & Payees → **Add Vendor**. Fill Company, address
   (`form_input` the location + City/State/Zip), and **Category**. For a provider: 1099
   Non-Employee, Tax ID = EIN if on a HCFA (else blank), category **7000**. For the
   **client**: **UNCHECK 1099** (PI settlement isn't 1099-reportable), category **7010**,
   address from the **intake sheet** (the client's mailing address). Save via the Add
   Vendor button's `ref`. Then return to `expense.php` (drafts persist) and fill the line.
   - **Vendor Category gotcha:** do NOT `form_input` the vendor Category select — it
     concatenates/garbles the label. Always click the dropdown → type the code → click the
     result. Setting the right default category here makes the expense line auto-fill it.
3b. **VERIFY EVERY LINE'S AMOUNT FROM THE SAVED DRAFT — never trust `form_input`'s return.**
   `form_input` reports `Set number input to 450.00` and the form *looks* right, but the value can
   fail to persist into the saved draft row and the line commits as **0.00**. This has now bitten
   twice: Jingxiang Lin's SimonMed USD 1,200 (found a session later, repaired via the row's edit pencil)
   and Jing Wang's **Sun Imaging USD 450 + Vanguard IPS USD 450**, which Klaus had to fill in himself
   ("sun imaging和vanguard没有加金额进去下次注意", 2026-10-13).
   After clicking **+ New Transaction** on each line, re-read the *Draft Expense Ledger* (not the form)
   and confirm that line's amount and running balance moved:
   ```
   javascript_tool: (()=>{const el=[...document.querySelectorAll('*')].find(e=>e.innerText&&e.innerText.includes('Balance Forward')&&e.children.length<40);
   const t=el.innerText.replace(/\n(Date|Check #|Description|Actions|Assignee:|Category:|Memo:|Amount|Balance)\n/g,' | ');return t.slice(t.indexOf('Balance Forward'))})()
   ```
   A line showing **0.00**, or a balance that did not move by that amount, means the write was lost —
   fix it with the row's edit pencil before moving on.

   ⚠️ **The in-page read is NOT proof. Only a RELOAD is.** On 2026-10-14 the Jun Hao client line read
   `3,666.67` in the draft ledger with "All changes saved." showing — and came back **0.00 with the memo
   gone** after the page was reloaded. The DOM can be ahead of what the server stored. So:
   **before reporting, `navigate` to `expense.php?bank_id=111793` again and re-run the read above.**
   Treat only that post-reload output as the truth, and only report once
   `last balance − Balance Forward` equals the reconciliation total to the cent.
   Re-check the same way at the start of any later turn that touches this batch — a line verified
   earlier can still be empty now, and these drafts sit around for days before Klaus posts.

   ⚠️ **Never type into the top form while an existing row is loaded in it.** Clicking a row's edit
   pencil loads that row into the same form; typing a payee there overwrites that saved line instead of
   starting a new one. After any edit-pencil repair, click **+ New Transaction** (or reload) before
   touching the form again.

4. **Review & STOP.** Show Klaus a table (payee, category, memo, amount, running balance,
   total) cross-checked against the signed letters + the reconciliation identity. Do NOT
   click Post Expenses.
5. **Commit / verify.** Only after Klaus says "确认过账": click **Post Expenses** (`ref`)
   once. If Klaus says he already posted ("我处理了"), DON'T post — open the Ledger
   `bank_account.php?bank_id=111793` and confirm the lines are there (check# is blank until
   Print Checks is run — that's normal) and the balance ties.

## Provider W-9s — where they live, and backing a new one up

**The library is `PI Team Folder/3. Disbursements/`** (Drive id `16klZfsFWR6SIL_s2646-4DATwPUNix32`) (Klaus, 2026-10-14: "所有的w9都会在 folder 3,
disbursements"). Three places to look, in this order:
- the folder **root**, named `<Payee Entity>.pdf` — e.g. `Integrative Physical Medicine Physicians.pdf`,
  `Cyrus Sedaghat, M.D. APMC.pdf`, `Dr. Anil Date, MD.pdf`, `Masrour Chiropractic, Inc..pdf`;
- the older **`W9/`** subfolder;
- the Drive W-9 folder **`1oWX7kFan5W8M7uW6RHkvRu1RiJRFAf9Y`** that the Disbursement Sheet's provider
  column headers hyperlink to.

**A NEW W-9 arrives in the case folder and YOU file the backup** (Klaus, 2026-10-14: "下次我会把新的
W9保留在case folder然后你抓取完后备份进 folder3"). So when a stub vendor sends you to a W-9:
1. Look for it in the **case folder** first (`3. Disbursements/Case Disbursements/<Client>/`) — it may be
   named after the clinic's brand, not the payee entity (`ISSrehab W-9.pdf` → Integrative Physical
   Medicine Physicians).
2. Read it, fill the RD vendor record, fix the line's Mailing Address.
3. **Then back it up into `3. Disbursements/` root as `<Payee Entity>.pdf`** — the W-9 entity on line 1,
   not the brand, so the next case finds it by payee name. Copy it, do **not** move it: Klaus keeps the
   original in the case folder.
   ```
   gws drive files copy --params '{"fileId":"<w9 id>","supportsAllDrives":true,"fields":"id,name,parents,md5Checksum"}' \
     --json '{"name":"<Payee Entity>.pdf","parents":["16klZfsFWR6SIL_s2646-4DATwPUNix32"]}'
   ```
   Verify the copy's `md5Checksum` equals the source's before calling it filed. Already a file of that
   name there? Compare MD5 — identical means it is already filed (do nothing); different means the
   provider re-issued one, so keep both and suffix the older `(SUPERSEDED <date>)`.
4. If it is genuinely nowhere — case folder, `3. Disbursements`, `W9/`, Drive W-9 folder — say so with
   the names you searched, and fill the vendor's address from the **signed reduction letter's PAYMENT
   REMIT TO block** (that is authoritative for where the check goes); leave Tax ID blank and tell Klaus
   the W-9 is missing. Never invent an EIN.

⚠️ **Read a W-9 with `pdftotext -layout`, not vision.** These are AcroForm PDFs whose filled values sit
in form fields that the renderer does not draw — a vision read shows a **blank** form while `pdftotext`
returns the entity name, d/b/a, address and EIN. (The EIN comes out digit-spaced, e.g.
`8 4 – 4 0 0 4 7 7 3` = 84-4004773.) `pypdf.get_fields()` returns None on them, so don't bother.
Line 1 = the payee entity (what goes on the check); line 2 = the d/b/a / brand the clinic is known by.

## Intake address lookup (client check)

Find the case intake sheet in Drive: it's a Google Sheet titled like `<Client Name>-<DOL>`
(search `fullText contains '<name>'`, pick the spreadsheet). The client's mailing address
is the `Address` row — use the one marked **现居 (current residence)** if several are listed.

## Notes / history

- Tutorial video Klaus recorded: `Rentec Direct(Issue a check).mp4` (Drive, Accounts &
  Tools folder, id `1T_zYKnurKMpWVeEjjs9CD-3o5MZxHD2a`).
- 6/16/2026 runs: Jiehui Xie (DOL 10/11/2025) 4 provider checks USD 9,869.52 (check# 80184-87);
  Martin Alejandro Guo (DOL 12/18/2025) 4 providers + 1 client = USD 20,000.00 (=USD 30k −USD 10k
  fee). Both committed by Klaus.
- Browser tier: rentecdirect is a web app → Claude-in-Chrome, not computer-use.
