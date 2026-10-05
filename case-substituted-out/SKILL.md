---
name: case-substituted-out
description: |
  Handle a PI case being TAKEN OVER by another law firm — we are the FORMER attorney being
  discharged — for 凌图律所 / Lingtu Law Office (Law Office of Shenqi Cai APC). Use this skill
  whenever any of the following appear: a substitution / termination letter from another firm,
  a "Designation of Attorney", "your service is now terminated", "cease all work and forward
  the entire file", 换律师, 客人转去别家了, 案子被别的律所接走, sub out, "/case-substituted-out"
  for a named client. Typical invocation: the other firm's PDF packet (often emailed to the case
  team mailbox and forwarded to klaus@). The skill locates the case in Drive, verifies the client
  and the signature, confirms whether a 1P claim actually exists, fills the firm's three Notice
  of Attorney Lien templates (1P carrier / 3P carrier / successor counsel) plus a provider notice,
  packages the client file (excluding internal documents), sizes the delivery against the 25 MB
  email limit, drafts every email from the case mailbox (or klaus@ if told), and on explicit
  approval sends them, then logs the substitution to the Activity Log and posts to the case Chat
  space. It DRAFTS by default — it never sends without an explicit go. This is the OUT direction
  only (we lose the case); it does not handle taking a case IN from another firm.
---

# Case Substituted Out — another firm takes over

We are being discharged. California gives the client an **absolute right** to discharge counsel at
any time (*Fracasse v. Brent* (1972) 6 Cal.3d 784). There is nothing to contest. The entire job is:
**stop work, hand over the file promptly and completely, and perfect the lien so we get paid when
the case resolves.**

Everything downstream depends on the lien being asserted against the right parties, in writing,
before anybody disburses money.

## What the other firm's packet usually demands

Read it and answer **every** item. The standard packet (e.g. Welch & Chen's) demands four things:

1. Cease all work
2. Forward the **entire file**
3. **Advanced costs — amount and description**
4. **Attorney's fee — amount and itemized basis**

⚠️ Items 3 and 4 are easy to miss. The firm's precedent letters (Jinfa Lu, Shuhua Yan) do **not**
answer them, so copying a precedent blindly leaves the request unanswered. Answer both — see Step 6.

## Gates

- 🚩 **Gate 1 (Step 2)** — case identity + client signature confirmed before anything is drafted.
- 🚩 **Gate 2 (Step 8)** — Klaus sees every rendered PDF and approves before a single email goes out.

Never send, fax, or disburse without an explicit go. [[feedback_show_draft_before_send]]

---

## Step 1 — Find how the packet arrived (do this FIRST)

**Search the mail before concluding anything about contact details.** The other firm's letterhead
often prints only phone and fax, but the packet itself almost always arrives by **email**, and that
email carries their working address.

```
gws gmail users messages list --params '{"userId":"me","q":"\"<their phone>\" OR \"<their fax>\" OR \"<firm name>\"","maxResults":10}'
```

Then read the message `format=full` and pull every address out of the body — the packet is often
forwarded internally (team mailbox → klaus@), so the **original sender** is inside the forwarded
block, not in the headers.

Record: their email, the date they sent it, and the date it reached the handling desk. Those dates
decide whether the "letter was directed to our general information address and did not reach the
handling department until ___" sentence in the successor template stays or goes. **If the packet
went straight to the case mailbox, delete that sentence — do not imply misrouting that did not
happen.** [[feedback_negative_claims_need_premise]]

## Step 2 — Locate the case and verify 🚩 Gate 1

1. Drive search for the client name → case folder + `*Intake Sheet.xlsx`.
2. Confirm **name AND date of loss both match** the packet. One match is not enough.
3. Open the signed substitution/designation page and check **who signed and when**. On a
   multi-client case (driver + passengers), only the signers are substituted out — if a passenger
   has not signed, we still represent them. **Stop and ask.**
4. Determine the owning team/CM from the **PI Master Sheet**
   (`1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`) → Claims@ / Piteam@ / Picase@.
   That is the default sending mailbox. [[feedback_send_from_case_mailbox]]
5. Pre-lit or in litigation? **In litigation you also need a Substitution of Attorney (MC-050)
   filed with the court and the service list updated** — this skill covers the pre-lit lane only;
   flag the litigation extras to Klaus.

## Step 3 — Pull the facts from the intake sheet

From the intake `.xlsx` get: client name, DOB, DOL, 1P insurer / policy / claim / adjuster / email,
3P insurer / policy / claim / BI adjuster / email, insured (3P driver) name, and every treating
provider with contact details.

⚠️ **Verify the 1P policy period against the DOL before drafting a 1P letter.** On Jiajun He the
Progressive policy ran 08/17/2026–02/17/2027 against a DOL of 08/15/2026 — the policy incepted
*after* the loss, no 1P claim existed, and no 1P LOR had ever been sent. A 1P letter would have
been wasted and wrong. Signals that there is no 1P claim: claim # and adjuster still "Pending",
coverage status "Pending", and **no 1P LOR in the case folder**. Confirm with Klaus, and if there
is no 1P, **delete the whole 1P row** from the successor letter rather than leaving a blank.

## Step 4 — Read the retainer

Find the signed retainer in `1#Legal Documents` and extract:

- **Execution date** (DocuSign signature page) — the successor letter cites it by date.
- **The ATTORNEY LIEN clause** — current PI auto retainers grant an express lien on the recovery
  and expressly address discharge ("Attorney shall be entitled to recover the reasonable value of
  services provided up to the time of discharge"). That clause is what the successor letter relies
  on; confirm it is actually present in the version the client signed.
- Whether an **AUTHORIZATION FOR RELEASE OF RECORDS** is inside the retainer PDF. The successor
  letter promises "the retainer agreement and authorizations" — if the authorization only lived in
  a file you are excluding, reword rather than promise something not in the package.

## Step 5 — Fill the letters

Templates in Drive (pleading-format, firm letterhead, signature image, `{{yellow}}` fill slots):

| File | Drive ID |
| --- | --- |
| `Notice of Attorney Lien - 1st Party Insurance.docx` | `1sdLmiuckOA3KlrSkTr-uG7LLvQbY1UsV` |
| `Notice of Attorney Lien - 3rd Party Insurance.docx` | `1KQ1X6kEvvtVUF4HEH868qTv0Z1lUnU3M` |
| `Notice of Attorney Lien - Successor Attorney.docx` | `1JqY8Mfro1sQBm64FQoGMQQtvv1EyOyrI` |

Use `scripts/fill_letter.py`. House style, verified against the Shuhua Yan and Jinfa Lu precedents:

- Salutation is the adjuster's **bare full name** — `Dear John Grier:`, not `Dear Mr. Grier:`.
- A **yellow-highlighted** run is a fill slot; a same-named plain run is the **label**. Fill only
  the highlighted one or you will swap `Policy Number : 189661039` into `189661039 : Policy Number`.
- **Strip the yellow on every value you fill.** Leave yellow ONLY where the value is genuinely
  unknown, so Klaus can see it on the rendered page. [[feedback_highlight_missing_fields]]
- **The date line must be centered.** Templates default to left. [[feedback_letter_date_centered]]
- There is **no provider template** — build it from the 3P template: retitle the RE block to
  `SUBSTITUTION OF ATTORNEY – NOTICE TO PROVIDER`, delete the Your Insured / Policy Number /
  Claim Number rows, address it to the Records & Billing Department, replace the body with a
  plain redirect, and **delete the Siciliano lien paragraph** — a clinic is not a payor and the
  lien argument does not belong in their letter. Drop "upon resolution of this matter" from the
  closing too; they do not resolve claims.

### One page

Klaus wants these letters on one page. Levers, in order:

1. Merge body paragraphs (the successor template's 7 ship as 3 with nothing lost).
2. `w:after` paragraph spacing → 60–120.
3. Bottom margin `w:pgMar` → as low as 360 twips (0.25").
4. Remove the blank paragraph before `Very truly yours,`, then the one between the address block
   and the `RE:` block.

⚠️ **Never touch `word/header*.xml` and never reduce `w:top` below 1440.** The blank paragraphs in
the header are not padding — they position the logo, the gold band, and the black rule. Deleting
them visibly breaks the letterhead. Keep the blank paragraph that holds the signature image.
[[feedback_letter_date_centered]]

## Step 6 — Answer the costs and fee questions

Add one sentence to the successor letter. Standard wording when nothing was advanced:

> In response to your inquiries, this office has advanced no costs in this matter. No fee amount is
> stated at this time, as the lien is for the reasonable value of services rendered through the date
> of discharge, to be determined upon resolution.

**Give the costs figure. Do not give a fee figure.** Under *Fracasse*, a discharged contingency
attorney recovers in quantum meruit and the cause of action does not accrue until the contingency
occurs — quoting a number now is unsupported and boxes us in. Quantum meruit is also **not** an
hourly computation: it is the reasonable value of services, which may exceed hours × rate to
reflect the contingency factor and the delay in payment. Consistent with
[[referral_fee_never_quote_first]].

## Step 7 — Package the client file

Run `scripts/package_file.py`. It mirrors the Drive case folder, applies the exclusions, zips, and
reports the **base64-encoded** size.

**Exclusions — do not hand these over:**

- `*Intake Sheet.xlsx` — internal case-management record (contains SSN and our workflow checklist)
- `Intake Responses.zip` — internal intake capture

Everything else goes: retainer, LORs, police report, scene and vehicle photos, ID/plate/insurance
cards, the property damage file, and all medical records and bills **in our possession**.

⚠️ If `4#Bodily Injury Claim`, `5#Demand Package`, and `6#Settlement Documents` are empty, say so
to Klaus explicitly. "all medical records and bills in this office's possession" is literally true
with zero records, but he should know the package has no medicals before it leaves.

Mirror the package into a **`Case Sub` folder inside the case folder** (server-side `files.copy`,
so the copies are byte-identical) and put the letters there too, for Klaus to verify in Drive
before anything is sent.

### 25 MB is the ENCODED size

Gmail's limit applies after base64, which inflates by 4/3. A 15.4 MB zip becomes ~20.5 MB on the
wire. Compute `raw × 4/3 + letters` and compare against 25 MB:

- **Under** → attach the zip directly. Letter enclosure line reads `Client file (electronic copy)`.
- **Over** → Klaus puts the folder on Dropbox and gives you the link. Enclosure line reads
  `Client file (secure link)` and the link goes in the **email body, not the letter**.

Keep the wording of the letter and the actual delivery method in sync — they are easy to desync
when the size verdict flips late.

## Step 8 — Draft the emails 🚩 Gate 2

Three emails, each from the case mailbox unless Klaus says otherwise:

| To | Subject | Attach |
| --- | --- | --- |
| 3P carrier (and 1P if one exists) | `<Client> / Insured: <name> — Claim No. <#> — Sub Out Letter and Notice of Attorney's Lien` | that carrier's lien notice |
| Each treating provider | `<Client> (DOL <date>) — Notice of Substitution of Attorney` | provider notice |
| Successor counsel | `RE: <their subject>` — thread onto their own email | successor letter + **copies of the carrier lien notices** + the client file |

**Attach the carrier lien notices to successor counsel.** Successor counsel — not the adjuster —
is who will negotiate the settlement and direct how the draft is cut. Putting the actual notice in
their hands makes the co-payee requirement unavoidable and, if the fee is later disputed, "they
held the notice" is far stronger than "our letter said we had notified the carrier."

Email bodies: flowing HTML paragraphs, no hard wrapping, signature from the mailbox's own Gmail
settings (`settings.sendAs`), never scraped from an old message.
[[feedback_email_list_formatting]] [[gmail_signature_source]]

Always ask successor counsel to **confirm receipt in writing**. That receipt is the only proof we
discharged the CRPC 1.16(e)(1) delivery duty — see Retention below.

Show Klaus every rendered PDF. Send only on an explicit go.

## Step 9 — Send, then close out

After the go:

1. Send. Cc the case mailbox if Klaus asks.
2. **Activity Log** — one append-only row to `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA`,
   `Activity Log!A:J`, Category `律师指示`. Pack the Ref/ID column: successor firm + attorney +
   their email/phone, the sent Gmail message id, the carrier claim number, and the `Case Sub`
   Drive folder id. That column is the only handle three months out.
3. **Chat** — post to the case space as **Klaus@** (never picase@/piteam@ directory).
   [[feedback_chat_use_klaus]] Draft it in Klaus's own plain-text voice — short lines, no markdown,
   no bullets — and **post his wording verbatim** once he edits it.
   [[feedback_new_case_chat_verbatim]]
4. **PI Master Sheet** — mark the row substituted out and move it out of the active block.
5. Stop everything else: no further treatment referrals, no records requests, no client contact.

## Retention — what to keep and for how long

**There is no fixed retention period in California.** COPRAC Formal Opinion 2001-157 expressly
declines to set one; the familiar "five years" comes from LACBA Op. 475 (1994) reasoning by analogy
to the trust-account records rule (now **CRPC 1.15(d)(3)**), which COPRAC says was never meant to
govern case files. Proposed Formal Opinion Interim No. 19-0004 addresses this directly but remains
**proposed and unadopted** — do not cite it as authority.

What actually governs:

- **CRPC 1.16(e)(1)** — the duty is to *release* the file. It is discharged on delivery. A Dropbox
  link going dead later does not undo a delivery you can prove.
- After delivery we are a bailee: do not cause **reasonably foreseeable prejudice** to the former
  client. Originals, client-furnished property, and items of intrinsic value cannot be destroyed
  without consent.
- **CRPC 1.15(d)(3)** — trust-account records: **five years. This one is hard.**

Practical rules to tell Klaus:

- Keep a Dropbox link live until successor counsel **confirms download in writing**; floor of 90 days.
- File the transmittal email and their confirmation into the case folder. **That receipt is the
  asset, not the link.**
- Keep our own complete copy until the **lien is resolved and paid** — not merely until the case
  settles. Under *Fracasse* the quantum meruit claim does not even accrue until the contingency
  occurs, so settlement is when the fee fight *starts*.
- The contemporaneous record of what we did (LOR, claim filed, records ordered, referrals,
  Activity Log, Case Log) is what proves quantum meruit later. PI contingency firms keep no
  timesheets; those rows are the substitute.

## Authorities

- *Fracasse v. Brent* (1972) 6 Cal.3d 784 — absolute right to discharge; quantum meruit; accrues on the contingency
- *Siciliano v. Fireman's Fund Ins. Co.* (1976) 62 Cal.App.3d 745 — carrier must honor the lien (cited in the carrier letters)
- *Caesar v. Saenz* (1989) 208 Cal.App.3d 279 — apportionment between successive attorneys (cited in the successor letter)
- CRPC 1.16(e)(1) — release of the file · CRPC 1.15(d)(3) — five-year trust records
- COPRAC Formal Op. 2001-157 — no fixed file-retention period

## References

- `references/templates-and-precedents.md` — template IDs, prior sub-outs, what each precedent shows
- `references/worked-example-jiajun-he.md` — the 2026-10 run end to end, with the traps hit

Related: [[withdrawal_draft_skill]] (we drop the client — the mirror image), [[send_lor_skill]],
[[case_data_architecture]], [[referral_fee_never_quote_first]].
