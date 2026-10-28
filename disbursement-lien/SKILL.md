---
name: disbursement-lien
description: |
  Disbursement letters and lien reduction letters for 凌图律所 / Lingtu Law (Law Office of Shenqi
  Cai APC) PI settlements, as PDFs. Use for "/disbursement-lien", "write a dis", "draft dis",
  "disbursement letter", "lien redu", "lien reduction", "write lien", "出 dis", "写 lien", or a
  Pending Disbursed Sheet tab / tracker screenshot with a request to draft from it. Reads the
  client's tab in the Pending Disbursed Sheet, reconciles the numbers, finds each provider's
  remit-to from the W-9 folder or the team mailbox, and writes the lien reduction PDFs and the
  disbursement letter PDF plus the client's WeChat message. PDF ONLY — it never emails, never
  sends DocuSign, never writes checks. For the same run plus Gmail drafts use
  `disbursement-lien-email`.
---

# /disbursement-lien

`/disbursement-lien <client> [lien [providers]] [dis] [--detail | --formal] [--en]`

- No scope → full run: lien letters for every provider not yet agreed, then the dis.
- `lien` → lien letters only; name providers to limit (e.g. `lien TBI, Dr. Wu`).
- `dis` → disbursement letter only. Default is the 1-page simple version; `--detail` adds the
  per-provider "original lien → paid" rows; `--formal` is the multi-page statement with the
  protective clauses and a separate signature page (use only when Klaus asks for it).
- `--en` → client message in English instead of Chinese.

Scripts (in this skill's `scripts/`): `read_tracker.py` (sheet → case JSON), `disb.py`
(case JSON → PDFs). Templates are pulled live from Drive each run, so edits Klaus makes in
Drive take effect immediately:
- Disbursement Letter Template.docx `1wLq7KWY26XdO3NnD3BFS86RcMTVukucN`
- Lien Reduction Template.docx `15tADzza9OwXvBVqkNQrXUNkEpZjQvCEY` (universal, in "3. Disbursements")

Work in a scratch folder; deliver PDFs to `~/Downloads/<Client> Disbursement/`.

## Step 1 · Read the anchor numbers

The anchor is the client's tab in the **Pending Disbursed Sheet**
(`1b_vPr9WD7P9arR6DTTJRxeWs0apk8DTiTgc2iAzIrR0`), not a screenshot. Use a screenshot only when
the case has no tab yet.

```bash
python3 scripts/read_tracker.py "<tab name>" [--client "<name>"] [--letter-date "October 21, 2026"] > case.json
```

- One tab can hold several clients (`A/B/C`); pass `--client` to pick that client's block.
- It records each provider's Reduced-cell colour: **green = agreed**, yellow/white = still open.
- Letter date = today (`date`) unless Klaus gives one; he sometimes backdates to the negotiation date.

## Step 2 · Reconcile (every time)

`disb.py check case.json --out x` runs it. Three figures must agree:

1. the sum of the individual Reduced amounts = the tab's Total Reduced cell;
2. Total − Attorney Fee − Case Cost − sum of Reduced = Client Recovery;
3. multi-source: 3P + UM/UIM + Med Pay = Total.

If anything disagrees, **stop and ask which cell governs.** The two figures that agree usually
show which cell is wrong; say so. Never pick one silently. Fee: use the tab's figure and its
label (1/3, 40%, 50/50). `Settlement/3` is sometimes truncated (.66 not .67) so the column
sums exactly; match the tab.

Lines with no Reduced amount (e.g. "Client's out-of-pocket expenses") are excluded from the
dis and flagged; ask Klaus how to treat them.

## Step 3 · Remit-to for each lien letter

For every provider that gets a letter, fill `payee`, `addr1`, `csz` in case.json, in this order:

1. **W-9 folder**: Shared drives/PI Team Folder/3. Disbursements/W9/ (local mirror under
   `~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/`). Read the W-9 itself.
2. **Team mailbox**: the case's owning mailbox (its tab in the PI Master Sheet
   `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`: Claims@ / Piteam@ / Picase@). Old LaShine
   cases live in klaus@ under the client's label. Look for the provider's billing / lien / W-9 mail.
3. **Neither** → **stop for that provider**: no lien letter until the W-9 is in. Tell Klaus.
   (`disbursement-lien-email` drafts the W-9 request.)

Watch for:
- **Billing company / funding company owns the receivable.** If a funder bought the account
  (e.g. TBI Specialists → Apogee Capital Fund 5, LLC), the letter's payee, signature line and
  address are the funder's, using the address in its payment-remittance notice. Do not follow
  a provider's request to route payment back to itself.
- The provider's own bill or email address is fine for `addr1/csz` when it matches the W-9 entity.
- Fallback address table below is for names already verified in past cases; still prefer the W-9.

Skip a letter when Reduced == Lien (no reduction), for Medi-Cal / already-paid lines, and (in a
full run) when the Reduced cell is green (already agreed).

## Step 4 · Generate

```bash
python3 scripts/disb.py run case.json --out <dir> --lien all|none|"A,B" --dis simple|detail|formal|none
```

What the script guarantees (don't redo by hand):
- Letterhead and body contact = Klaus direct **(626) 479-2207, Fax (626) 479-2207** (VoiceFax) on
  lien letters. **Disbursement letter: keep the template header as is — phone only, no Fax line**
  (Klaus 2026-10-28).
  **626-240-2046 never appears** (claims@ fax-to-email); 614-6666 (personal cell) is removed.
  Header edits are text-only inside existing runs; header paragraphs are never added or removed.
- Lien letter: date centred; signature/Date columns aligned at 4.5" even for long payee names;
  30-day deposit clause present; "mentioned client".
- Dis: amounts right-aligned with dot leaders; fee label from the tab; case cost on its own row
  when non-zero (omitted when $0); medical-liens row removed when there are no liens; multi-source
  total shows "(3P $X + UIM $Y)"; minor clients use "(Minor), by and through Guardian …".
- Dis prints a PROVISIONAL warning while any reduction is still not green.

Output names: `<Client>-<Payee> Medical Lien Reduction and Release.pdf`,
`<Client>-Disbursement Letter.pdf` (formal: `<Client>-Settlement Disbursement Statement.pdf`).

## Step 5 · Verify before handing over

- Re-extract each PDF's text: client, DOL, every amount, payee twice on lien letters, address,
  no `[`/`]` tokens, no `240-2046`.
- Render page 1 of at least one letter (`pdftoppm -r 90`) and look: letterhead intact, date centred,
  signature line aligned.
- Dis: Fee + Liens (+ Cost) + Net == Total to the penny.

## Step 6 · Client message (with every dis)

Plain text in a code block, full-width Chinese punctuation, no markdown, blank line between
blocks (`--en` for English). Fill only the numbers:

```
您好 👋 好消息，您案件的和解支票我们已经收到 ✅ 现将您的最终分配明细列出，请您核对：

💰 总获赔金额：{总额}
⚖️ 律师费（{1/3}）：−{律师费}
🏥 折扣后医疗费：−{医疗}
✅ 您最终到手：{到手}

📧 结算分配单已发送至您的邮箱，请您核对后电子签字，我们收到签字即可为您放款。

签署后，款项可选择以下任一方式领取：
🏢 来办公室领取赔偿支票（需要预约）
📮 邮寄支票到您的地址（需要邮寄地址）
🏦 电汇 Wire（到账快，大额推荐；会产生银行手续费）

🏢 办公室地址：13191 Crossroads Pkwy N, Suite 295, City of Industry, CA 91746

如有疑问随时联系我们，谢谢！🙏
```
Add `🧾 案件成本：−{x}` when there is a case cost; multi-source → `（对方保险 $X + 自身 UIM $Y）` after 总获赔;
no 医疗 line when there are no liens; `--detail` adds the provider lines (原账单 → 折后).

## Step 7 · Hand over and file

- Report: files written, the reconcile line, every STOP (missing W-9), every SKIP, and any
  provisional warning, in one short list.
- PDFs stay in Downloads only until sent / signed back; then file into the case folder per the
  global filing rule.

## Never

Send email, send DocuSign, write or post a check, or edit the Drive templates without Klaus's go.

## Reference

**Fallback addresses** (verified on past cases; still prefer the W-9):

| Provider | Address |
|---|---|
| Advantage Healthcare Clinic | 9939 E. Garvey Ave. #A, El Monte, CA 91733 |
| Affinity Healthcare Clinic | 19031 Colima Rd, Rowland Heights, CA 91748 |
| Sun Imaging, Inc | 7715 Garvey Ave, Rosemead, CA 91770 |
| Precision Pain Care Center | 233 W Badillo St, Unit D, Covina, CA 91723 |
| RelivCare Surgery Center Inc | 233 W Badillo St, Unit C, Covina, CA 91723 |
| Premier Integrative Health Center | 529 E. Valley Blvd. #288A, San Gabriel, CA 91776 |
| Senlin Wang Medical Clinic | 123 E. Valley Blvd., Suite 207, San Gabriel, CA 91776 |
| Vanguard Interventional Pain Specialists | 707 S. Garfield Ave., Suite 304, Alhambra, CA 91801 |
| Exer Medical Corporation | 2381 Rosecrans Ave STE 115, El Segundo, CA 90245 |
| Nexus Healthcare | 14785 Jeffrey Rd. #102, Irvine, CA 92618 |
| Prime MRI (Prime Rad Inc) | 1400 S. San Gabriel Blvd, San Gabriel, CA 91776 |
| Providence Rezolut Imaging | PO Box #736339, Dallas, TX 75373 |
| Shin Imaging, LLC | PO Box 677146, Dallas, TX 75267-7146 |
| SimonMed Imaging | PO Box 207465, Dallas, TX 75320 |
| Samimi Orthopedic Group | P.O. Box 1628, West Covina, CA 91793 |
| Axis Chiropractic and Health Center | 13890 Peyton Dr. #C, Chino Hills, CA 91709 |
| A Plus Acupuncture Corp. | 1239 N Grand Ave, Walnut, CA 91789 |
| Riverside Elite Imaging Medical Corp | 21828 Cactus Ave, Riverside, CA 92518 |
| The Rawlings Company LLC | PO Box 2000, La Grange, KY 40031 |
| Apogee Capital Fund 5, LLC (TBI Specialists receivables) | 614 South Capital of Texas Highway, Austin, TX 78746 (payment notice 12/22/2025) |

**Naming notes:** "Advantage Healthcare Clinic" as is (not its W-9 legal name). Affinity ≠
Advantage. "Precision PM" = Precision Pain Care Center. Premier Integrative Health Center's W-9
legal name (Frank Chung Chiropractic Corp) does not go on the letter. Premier Spine and
Orthopedics Associates (Dr. Wei Wu, Fresno; formerly Neurosurgical Associates Medical Group)
bills through Stanford Medical Billing, liens@stanfordmedicalbilling.com.
