---
name: limited-civil-file-complaint
description: >
  Prepare the One Legal e-filing package for a LIMITED CIVIL case (commercial /
  contract — breach of a written lease or contract, collection of money owed,
  guaranty, common counts, indemnity) whose Complaint is already drafted by
  attorney Hernán Simó at 凌图律所 / Law Office of Shenqi Cai APC. Use this skill
  whenever the next step for a NON-personal-injury, ≤ $35,000 civil complaint is
  立案 / filing: triggers include "prepare the filing package", "prep summons and
  cover sheet for the contract/lease case", "limited civil filing package",
  "get this complaint ready to file", "commercial collection filing", "立案",
  "准备起诉文件" for a commercial/contract matter, "/limited-civil-file-complaint"
  for a named case, or dropping a drafted limited-civil Complaint in and asking to
  prep the court forms. It fills the Summons (SUM-100), Civil Case Cover Sheet
  (CM-010), and — for Los Angeles — the CIV-109 Addendum & Statement of Location,
  from the firm's Drive templates, and packages them into the case's "2. Pleadings"
  folder. It does NOT draft the complaint (Hernán does) and NEVER e-files, submits,
  drives One Legal to payment, or pays. Prep-only: fillable PDFs with case number,
  signature, and date left blank. This is the LIMITED-CIVIL / contract sibling of
  `dogbite-file-complaint` (dog bite / PI) and `file-complaint` (LA PI); it shares
  their fill engine but carries the limited-civil court-rule brain. Always trigger
  for any "prepare/fill the limited-civil filing forms" request, even a partial one.
---

# Limited-Civil / Commercial Complaint — Prepare the One Legal Filing Package

Given a **limited civil** case (commercial / contract: unpaid rent, breach of a
written lease or contract, money owed, guaranty, indemnity, common counts) whose
**Complaint is already drafted by Hernán**, this skill produces the court forms
needed to e-file it via One Legal, in the firm's house format.

Sibling of `dogbite-file-complaint` (dog bite / PI) and `file-complaint` (LA PI).
This one is **limited civil (≤ $35,000), NON-PI, contract/collection**, and saves
into the limited-civil case's **`2. Pleadings`** folder.

**It prepares (never files):**
- `1 - Summons.pdf` (SUM-100)
- `2 - Complaint.docx` — copy of Hernán's drafted complaint, kept as the **editable
  .docx, NOT a PDF**: the client's feedback comes back on it and Hernán edits it
  directly. Never convert it, never delete the source .docx.
- `3 - Civil Case Cover Sheet.pdf` (CM-010)
- `4 - Civil Case Cover Sheet Addendum and Statement of Location.pdf` (CIV-109) —
  **LA County requires it for limited civil**; other counties verified per case.
- `0 - READ ME - Filing Checklist.txt` — what's filled, what's blank, the filing
  steps + fee.

Leave the **case number, attorney signature, and date blank** — added at filing.
Never submit, e-file, drive One Legal to payment, or pay. (Prep-only, set with Klaus.)

## Shared engine — do NOT fork it

The fill engine is **ONE engine, shared with `dogbite-file-complaint`**. This skill
carries only the limited-civil *brain* (the court rules + config); the mechanics are
reused:

- `~/.claude/skills/dogbite-file-complaint/scripts/get_templates.sh`
- `~/.claude/skills/dogbite-file-complaint/scripts/fill_forms.py`

Same statewide forms (SUM-100 / CM-010 / CIV-109) apply to every California civil
case; the engine already supports the CM-010 contract box and the CIV-109 4-digit
action stamp. Fix bugs in the one engine, never copy it here. (Long-term: extract the
engine to a shared location referenced by all three skills.)

## Inputs

The drafted **Complaint** (docx/PDF) + the case folder in the **"Hernan Simo Cases"**
shared drive under **`1. Limited Civil / Commercial Cases`**. If only a client name
is given, find the case folder by name (Drive search) and confirm with the user.

## Step 1 — Read the complaint, extract the case data

The complaint is the source of truth. Extract:

- **County / court** → caption's "SUPERIOR COURT … COUNTY OF ___".
- **Plaintiff(s)** — copy VERBATIM for the SUM-100.
- **Defendant(s)** — copy VERBATIM incl. entity descriptor / individual / DOE range,
  e.g. `AZUCANELA LLC, a California limited liability company; ROBERT KENNEDY LEIVA,
  an individual; and DOES 1 through 10, inclusive`. **Never abbreviate to "et al."**
  (each must be named for service). Note any **guarantor** named as an individual
  defendant.
- **Case short title** → `WU v. AZUCANELA LLC, et al.` (LAST v. LAST, et al.).
- **Amount** → read the **JURISDICTION** paragraph: a limited civil complaint states
  "amount in controversy is $X, exclusive of attorney's fees, interest, and costs …
  does not exceed $35,000." Record that **principal $X** (it is the demand amount).
  → config `"amount": "limited"`.
- **Number of causes of action** (count CAUSE OF ACTION headers). A contract case is
  commonly 3–4 (Breach of Written Contract; Breach of Contractual Indemnity; Breach of
  Guaranty; Common Count).
- **Subject-property / performance address** (street + city + ZIP) — the address the
  CIV-109 Statement of Location keys off (usually the leased premises).
- **Jury demand?** (note for the checklist).
- **Is this a CRC 3.740 "collections case"?** — see Step 2. This one decision swings
  the courthouse.

## Step 2 — Determine the filing court (DOUBLE VERIFICATION — Klaus's rule)

Never settle the courthouse from one source, never guess from geography.

**2a. The collections-vs-non-collections fork (LA — decides the courthouse).**
Under LASC Local Rule 2.3(a)(2), a limited civil case is routed by whether it is a
**CRC 3.740 collections case**:
- **CRC 3.740 collections** (sum stated to be certain ≤ $35,000, arising from a
  transaction in which property/services/money was acquired **on credit**; excludes
  tort damages, indemnity, recovery of property) → **Norwalk Courthouse**.
- **All OTHER limited civil** (non-collection, non-UD) → **mandatory Central District,
  Stanley Mosk Courthouse** (LR 2.3(a)(2)).

A lease/rent case that also pleads **indemnity or guaranty**, or is not a pure
sum-certain credit debt, is **NON-collection → Central / Stanley Mosk**. (This is how
Brian Wu v. Azucanela filed: the ADA-settlement indemnity + Leiva guaranty took it out
of 3.740.) If the complaint pleads "limited non-collection … Central District" in its
venue paragraph, follow that. If it looks like a pure collections case, STOP and confirm
the Norwalk routing with Klaus/Hernán before filling.

**2b. Confirm on One Legal (authoritative) + the court's site.**
Start a One Legal **Case Initiation** order (read-only — NEVER submit/pay), choose the
county + **Case Category = Civil Limited** + the Case Type, enter the property ZIP, and
read the **Court Location** it returns. Then confirm the courthouse identity + street
address on the county court's own locations page. Only when both agree do you fill.
Record courthouse name, street + city/ZIP, district, and both source URLs.

## Step 2c — Load the limited-civil rule set

Open `references/court-rules-limited.md` and find the county + contract subtype. It
gives: the CM-010 case-type box, the CIV-109 action code + reason, the courthouse, and
the worked config. **If the county/subtype is already recorded → use it (fast path).
If NOT → LEARN it** (verify against the court's own site, then record it there — the
"做一个记一个" loop). Never guess a court rule.

LA limited civil → CM-010 Item 1 box = **Breach of contract/warranty (06)** (for a
lease/contract breach); CIV-109 code per subtype (breach of lease = **`0601`**,
reason **`2`** — see the rule file for the reason 2/5/11 note to flag to Hernán).

## Step 3 — Get the templates from Drive

`bash ~/.claude/skills/dogbite-file-complaint/scripts/get_templates.sh <scratch>`
pulls the Hernán SUM-100 + CM-010 + LA CIV-109. CM-010 + SUM-100 already carry Hernán's
attorney block (**Hernán S. Simó, SBN 354175** — verify against the template; do not
overwrite the block).

## Step 4 — Build the config + fill

Write `config.json` for the shared `fill_forms.py` — use the worked example in
`references/court-rules-limited.md`. Set `county`, the courthouse/branch fields,
`amount: "limited"`, `case_type_tooltip: "Breach of contract/warranty (06)"`,
`num_causes`, the verbatim plaintiff/defendant blocks, the addendum action code/reason,
and the subject-property address. Then:

```bash
python3 ~/.claude/skills/dogbite-file-complaint/scripts/fill_forms.py config.json
```

The engine strips XFA, writes real appearance streams, checks the CM-010 box, stamps
the CIV-109 action box, and preserves Hernán's attorney block (forcing phone + fax to
the firm standing number, below).

## Step 5 — Verify by rendering (do not skip)

JC/local forms render as garbage in poppler — **use Ghostscript**:

```bash
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r120 -dFirstPage=1 -dLastPage=1 \
   -sOutputFile=chk.png "<out_dir>/1 - Summons.pdf"
```

Check each filled page: parties, court/branch, **CM-010 Limited box + the contract
case-type box**, complex = No, the **CIV-109 action box (e.g. 0601) + reason + property
address + Central district** on the Statement-of-Location page (render the LAST page of
the CIV-109 — it is a multi-page form). If a checkbox/stamp didn't land, fix the coord
map in `fill_forms.py` (the ONE shared engine) and re-run.

## Step 6 — Package into the case's `2. Pleadings`

Assemble in the limited-civil case's **`2. Pleadings`** folder (template structure:
`1. Client & Retainer / 2. Pleadings / 3. Discovery / 4. Contract & Evidence /
5. Correspondence & Demand / 6. Settlement & Disbursement`, per memory
`limited-civil-commercial-cases`). Files:

1. `1 - Summons.pdf`, `3 - Civil Case Cover Sheet.pdf`,
   `4 - Civil Case Cover Sheet Addendum and Statement of Location.pdf`
2. Copy the complaint in as **`2 - Complaint.docx`** — keep it editable; do NOT convert
   to PDF, and never delete the source .docx from `~/Downloads`.
3. `0 - READ ME - Filing Checklist.txt` — filled vs blank (case #, signature, date),
   the One Legal steps, first-paper fee, and the service note (serve conformed Summons +
   Complaint + CM-010 + CIV-109 on each named defendant).

Naming = plain document type in filing order (no form codes, no "(filled)" suffix).
Deliver the folder to the user. **Do not e-file.**

## Step 7 — Client Chinese translation + WeChat review message (always)

Same as the dogbite skill: translate Hernán's complaint into 简体中文 **in place, same
pleading format** (do NOT summarize), on a COPY of the docx — SimSun (宋体) font on every
run, proper nouns kept in English (party names, firm, addresses, statute cites, dates).
Strip stray `<w:hyperlink>` elements so text isn't duplicated. Save docx + PDF into the
package folder as `<Client> - Complaint (中文译本).<ext>`. Then the fixed WeChat message
(plain text, full-width punctuation, in a code block; Klaus sends it himself):

```
您好，这是起诉状的中文版本，请您仔细查看，如有任何问题或需要补充，请告诉我们，谢谢！
```

## Step 8 — Draft the reply to Hernán (always; generate-only, Klaus sends)

Short, warm, two-point email in Klaus's tone with Hernán (thankful, eager to learn; see
memory `feedback_hernan_email_tone`). Never auto-send. Two updates: (1) translated the
complaint into Chinese and sent it to the client to review; (2) confirmed the filing
court from the venue allegations and prepared the package — attached for his review and
signature. Include the **one open question** if any (e.g. the CIV-109 reason 2 vs 5 for
action 0601). Warm sign-off ("Best, Klaus").

## Step 9 — Draft the client-review email (client + cc Hernán; bilingual; both complaint PDFs)

The step Klaus wants right after the package: draft (do NOT send) a Gmail email that
sends the complaint to the **client** for review, **cc Hernán**, with the complaint in
**both English and Chinese** attached. Klaus fills the client's address and sends.
(This is the email channel; the Step 7 WeChat 文案 is the WeChat channel — both deliver
the 中文译本 for the client to check BEFORE filing. Do whichever fits how the client
communicates, or both.)

1. **Make an English PDF of the complaint** (attachment only — do NOT touch the editable
   `2 - Complaint.docx` in the package, do NOT add this PDF to the package):
   ```bash
   soffice --headless --convert-to pdf --outdir <scratch> "<pkg>/2 - Complaint.docx"
   ```
   Name it `<Client> - Complaint (English).pdf`; render page 1 (Ghostscript) to confirm
   the pleading paper / caption survived. The Chinese PDF is the `中文译本` from Step 7.
2. **Fetch the preset Gmail signature** (API drafts don't auto-insert it):
   `gws gmail users settings sendAs list` → take the default `klaus@lingtulaw.com`
   `signature` HTML; append it to the body.
3. **Build the Gmail DRAFT** (`gws gmail users drafts create`; a multipart message with the
   HTML body + BOTH PDFs — build it with Python `email.message.EmailMessage`,
   `set_content` + `add_alternative(html)` + two `add_attachment(..., subtype='pdf')`,
   then base64url the bytes into `{"message":{"raw": …}}`):
   - **To:** LEAVE BLANK — Klaus adds the client (or Richard / authorized contact) and sends.
   - **Cc:** `Hernán Simó <hernan.s@lingtulaw.com>`.
   - **Subject:** `<Case caption> — Complaint for Your Review / 起诉状请您审阅`.
   - **Body — bilingual, simple, English then 中文** (fixed text; do NOT itemize facts):
     - EN: *"Hello, Attached please find the Complaint we have prepared for your case, in
       both English and Chinese. Please review it carefully. If you have any questions, or
       if anything needs to be corrected or added, simply reply to this email and let us
       know. Thank you."*
     - 中文: *"您好，附件是我们为您的案件准备的起诉状，中英文各一份。请您仔细查看。如有任何问题，
       或发现有需要更正、补充的地方，直接回复此邮件告诉我们即可。谢谢！"*
   - **Attachments:** `<Client> - Complaint (English).pdf` + `<Client> - Complaint (中文译本).pdf`.
   - Verify the created draft has BOTH attachments + the Hernán Cc (fetch it back with
     `messages get … format=full`).
   **Generate-only.** Never send — Klaus reviews, adds the recipient, and sends.

## One Legal case-initiation (reference for the user's e-file step — Klaus files)

- **Case Initiation** (new case) → **Order type**: `Filing` (file only; serve
  separately) or `File + Serve`. Ask Klaus which.
- Subject matter **State** → **California** → **Choose the court** = the county
  (e.g. `Los Angeles County, Superior Court of California`).
- **Case Category** = `eFile: Civil Limited`.
- **Case Type** = the contract subtype mirroring the CIV-109 action — breach of lease →
  `Breach of Rental/Lease Contract (not unlawful detainer or wrongful eviction)`
  (**NOT** a Collections type — that routes to Norwalk; see Step 2a).
- **Case Title** = `LAST v. LAST` (e.g. `Brian Wu v. Azucanela LLC`) — court re-edits it.
- **Jurisdictional Amount** = the band covering the principal (e.g. `Over $12,500 and up
  to $35,000`). **Demand Amount** = the principal from the JURISDICTION paragraph
  (exclusive of attorney fees/interest — CCP §85), e.g. `$15,150`.
- **Incident Zip Code** = the subject-property ZIP (e.g. `91702`) → returns the Court
  Location (Stanley Mosk for LA non-collection). **Premise Address** = the leased premises.
- Add the individual **guarantor / co-defendant** on the later **Case Participants**
  screen (the Case Information screen only takes the lead defendant).

## Firm standing rules

- **Phone & fax on ALL litigation documents = (626) 479-2207.** The fill engine forces
  the CM-010 attorney phone AND fax to this number. If Hernán's complaint caption still
  shows the old fax `(626) 240-2046`, flag it — don't silently edit his pleading.

## On completion — ALWAYS report these two paths to Klaus

1. **Court-finding path** — county from the caption → the collections-vs-non-collections
   determination → what One Legal offered → confirmation on the court's site → the exact
   courthouse + address + district, citing BOTH sources.
2. **Court-rule path** — which rule set in `court-rules-limited.md` (or, for a new
   county/subtype, the court pages you read) → CM-010 box + CIV-109 code/reason → what's
   required to FILE vs to SERVE → the first-paper fee → source URLs. State plainly if any
   rule could not be verified and was flagged for Klaus/Hernán.
