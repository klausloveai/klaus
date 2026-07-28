---
name: dogbite-file-complaint
description: >-
  Prepare the civil-complaint FILING PACKAGE for a Hernán Simó / 凌图律所 (Law Office
  of Shenqi Cai APC) DOG BITE case, ready to e-file via One Legal — fill the Summons
  (SUM-100), the Civil Case Cover Sheet (CM-010), and — only if the county requires it
  for this case type — the county cover-sheet addendum (LA PI → CIV 109; Ventura PI →
  none; other counties verified & learned on first use) from the firm's Drive
  templates, then package everything into the case's
  "4. Litigation" folder. Use whenever Hernán has finished drafting a dog-bite
  complaint and the next step is 立案 / filing: triggers include "prepare the filing
  package", "prep summons and cover sheet", "get this complaint ready to file",
  "file via One Legal", "立案", "准备起诉文件", "/dogbite-file-complaint" for a named
  case, or dropping a drafted dog-bite Complaint in and asking to prep the court
  forms. It does NOT draft the complaint (Hernán does) and NEVER e-files or submits —
  it prepares fillable PDFs, leaves case number / signature / date blank, and writes a
  county-specific filing checklist. Multi-county by design: it does the county at hand
  and RECORDS that county's rules so the next case in the same county is fast. Always
  trigger for any "prepare/fill the dog-bite filing forms" request, even a partial one.
---

# Dog-Bite Complaint — Prepare the One Legal Filing Package

Given a dog-bite case whose **Complaint is already drafted by Hernán**, this skill
produces the court forms needed to e-file it via One Legal, in the firm's house
format, for **whatever California county the complaint is filed in**.

Sibling of `file-complaint` (LA-only PI). This one is dog-bite + Hernán + **multi-county**,
and saves into the dog-bite case's `4. Litigation` folder.

**It prepares (never files):**
- `1 - Summons.pdf` (SUM-100)
- `2 - Complaint.docx` — copy of Hernán's drafted complaint, kept as the **editable .docx,
  NOT a PDF** (Klaus, 2026-07-21): the client's feedback still comes back on it and Hernán
  edits it directly. Never convert it, and never delete the source .docx.
- `3 - Civil Case Cover Sheet.pdf` (CM-010)
- `4 - <county addendum>.pdf` — **only if the county requires one for this case type**
  (LA PI → CIV 109; Ventura PI → none — its VN278 addendum doesn't cover PI; other
  counties verified per case)
- `0 - READ ME - Filing Checklist.txt` — what's filled, what's blank, the county's
  One Legal filing steps + fee

Leave the **case number, attorney signature, and date blank** — added at filing.
Never submit, e-file, drive One Legal, or pay. (Scope was set with Klaus: prep-only.)

## Inputs

The drafted **Complaint** (docx/PDF) + the dog-bite case folder in the "Hernan Simo
Cases" shared drive. If only a client name is given, find the case folder by name
(Drive search) and confirm with the user.

## Step 1 — Read the complaint, extract the case data

The complaint is the source of truth (caption + body already state everything). Extract:

- **County / court** → the caption's "SUPERIOR COURT … COUNTY OF ___". This drives
  everything (which addendum, which court-rules module). e.g. Bo Tao → **VENTURA**.
- **Plaintiff(s)** — copy the plaintiff block VERBATIM for the SUM-100, incl. any
  minor/GAL wording. Note city of residence.
- **Defendant(s)** — copy VERBATIM incl. `, an individual` / DOE range, e.g.
  `EUTIMEO BEAS, an individual; RACHEL R. BEAS, an individual; BECKY BEAS, an individual; and DOES 1 through 20, inclusive`.
  **Never abbreviate defendants to "et al."** (they must be named for service).
- **Case short title** → `TAO v. BEAS` (LAST v. LAST).
- **Incident / Subject Property address** (city + ZIP) — determines venue/branch.
- **Number of causes of action** (count CAUSE OF ACTION headers). Dog bite is
  usually 3: Strict Liability (Civ. Code §3342), Negligence, Premises Liability.
- **Amount** → "unlimited" (injury damages > $35k, the norm).
- **Jury demand?** (note for the checklist).

## Step 2 — Determine the filing court (DOUBLE VERIFICATION — Klaus's rule)

Never settle the courthouse from one source, and never guess it from geography.

1. **One Legal first (authoritative).** Start a Case Initiation order in One Legal for the
   county and read the courthouse / filing-location options it offers. One Legal is wired
   straight into the courts, so what it accepts is what the court accepts — this narrows
   the candidates to the real, currently-valid filing locations. (Exploring the dropdowns
   is read-only; NEVER submit or pay.)
2. **Then confirm on the court's own website.** Take the courthouse One Legal gives and
   verify its identity + street address + that it hears unlimited civil, on the county
   court's official locations page (LA: also the LASC Filing Court Locator with the
   incident city+ZIP, since LA assigns PI by where the incident occurred).

Only when both agree do you fill the forms. If they disagree, stop and ask Klaus.
Record: courthouse name, street address + city/ZIP, and (LA/multi-district counties) the
district — plus both source URLs for the completion report.

## Step 2b — Load the county's rule set

Open `references/court-rules.md` and find the county. Each county entry says:
its required addendum form (or none), how the branch/venue is determined, the
CM-010 case-type box, the addendum action code/reason, the fillable-template Drive id,
and the fill-script map name.

- **If the county is already recorded** → use it directly (fast path).
- **If the county is NOT yet recorded** → LEARN IT (see "Adding a new county" below),
  then record it in `court-rules.md` so it's a fast path next time. This is the
  "做一个记一个" design — never guess a court rule; verify it, then persist it.

Dog bite → CM-010 Item 1 box is **Other PI/PD/WD (23)**; the tort is premises/animal
(LA CIV 109 code `2301` reason `4`; other counties' equivalents recorded per county).

## Step 3 — Get the templates from Drive

`bash scripts/get_templates.sh <scratch>` pulls the Hernán SUM-100 + CM-010 (+ LA
CIV 109). For other counties, also download that county's addendum template from the
**Litigation Forms** Drive folder (id `1XWPPpjckqzcxus2A8BuNJKNt8BwY6fHb`) — add its
id to `get_templates.sh` once the form is in that folder (see "Adding a new county").
CM-010 + SUM-100 already carry Hernán's attorney block (**Hernán S. Simó, SBN 354175** —
verify the SBN against the actual template; do not overwrite the block).

## Step 4 — Build the config + fill

Write `config.json` for `scripts/fill_forms.py` (see the LA example in
`references/la-county-pi.md`), setting `county`, the courthouse/branch fields per the
county rule set, `num_causes`, the verbatim plaintiff/defendant blocks, incident
address, and the addendum action code/reason. Then:

```bash
python3 scripts/fill_forms.py config.json
```

The engine strips XFA, writes real appearance streams, checks the CM-010 box, stamps
the addendum action box, and preserves Hernán's attorney block.

## Step 5 — Verify by rendering (do not skip)

JC/local forms render as garbage in poppler — **use Ghostscript**:

```bash
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r120 -dFirstPage=1 -dLastPage=1 \
   -sOutputFile=chk.png "<out_dir>/1 - Summons.pdf"
```

Look at each filled page: parties, court/branch, checked case-type box, complex=No,
monetary, causes count, jury demand, and the addendum's action/reason/incident/branch.
If a checkbox didn't land, fix the coord map in `fill_forms.py` and re-run.

## Step 6 — Package into the case's `4. Litigation`

Assemble in the case's **`4. Litigation`** folder (dog-bite template structure:
`0. Intake Sheet / 1. Incident & Liability / 2. Legal Documents / 3. Medical Record & Bill /
4. Litigation / 5. Cost & Receipt / 6. Settlement & Disbursement`). For legacy-structure
cases (Bo Tao etc.), use the case's existing "Legal Documents" or create a "Litigation"
subfolder — confirm with the user.

1. `1 - Summons.pdf`, `3 - Civil Case Cover Sheet.pdf`, `4 - <county addendum>.pdf`
2. Copy the complaint in as **`2 - Complaint.docx`** — keep it editable; do NOT convert to
   PDF, and never delete the source .docx from `~/Downloads`
3. `0 - READ ME - Filing Checklist.txt` — filled vs blank (case #, signature, date),
   the county's One Legal steps, first-paper fee, and service note (serve conformed
   Summons + Complaint + addendum on each named defendant).

Naming = plain document type in filing order (no form codes, no "(filled)" suffix).
Deliver the folder to the user. **Do not e-file.**

## Step 7 — Client Chinese translation + WeChat review message (always)

After the package is built, produce two client-facing deliverables so Klaus can send the
complaint to the client for verification BEFORE filing:

1. **Chinese translation of the complaint — SAME pleading format, in place.** Do NOT
   reformat into a summary. Work on a COPY of Hernán's complaint .docx and translate
   EACH paragraph / caption-table cell / heading / footer in place to 简体中文, preserving
   the exact structure (line-numbered pleading paper, attorney block, caption tables,
   numbered allegation paragraphs, causes-of-action headings, prayer, signature block).
   Keep proper nouns in English (party names, firm name, street addresses, statute cites
   like §3342, "Amazon Flex", hospital names, dates). **Chinese font = SimSun (宋体)** —
   set `w:ascii/hAnsi/eastAsia/cs` = `SimSun` on every run. Save docx + PDF into the
   package folder as `<Client> - Complaint (中文译本).<ext>`.
   - Technique (python-docx): copy the docx; for each non-empty paragraph replace runs
     with SimSun run(s) carrying the translation (rebuild line breaks with `add_break`);
     also strip stray `<w:hyperlink>` elements (e.g. the email) so text isn't duplicated;
     translate section footers/headers too. Verify by rendering the PDF and eyeballing
     that the caption tables, line numbers, and numbering survived.
2. **A short WeChat message (文案)** — use the fixed generic version (Klaus's preference —
   keep it simple, do NOT itemize the facts):
   `您好，这是起诉状的中文版本，请您仔细查看，如有任何问题或需要补充，请告诉我们，谢谢！`
   Plain text, full-width punctuation. Present it in a code block. Generate only — Klaus
   sends it himself (with the 中文译本 attached).

## Step 8 — Draft the reply to Hernán (always; generate-only, Klaus sends)

Hernán drafted the complaint, so the package goes back to him for review + signature.
Draft a **short, two-point** email reply in **Klaus's tone with Hernán: warm, thankful,
eager to learn** (never auto-send — Klaus sends it himself; see memory
`feedback_hernan_email_tone`). Keep it brief — just these two updates:

1. Translated the complaint into Chinese and sent it to the client to review for any
   corrections or additions.
2. Located the proper courthouse based on the incident location and prepared the
   complaint package accordingly — attached for his review and signature.

Warm one-line thanks/sign-off ("Best, Klaus"). Do NOT itemize the forms, filing fee, ZIP
flags, or next steps in the email (that detail lives in the package checklist). Example:

```
Hi Hernán,

Thank you for putting the complaint together! Two quick updates:

1. I translated the complaint into Chinese and sent it to the client to review for any
   corrections or additions.

2. I located the proper courthouse based on the incident location and prepared the
   complaint package accordingly — attached here for your review and signature.

Please let me know if you'd like anything adjusted. Thank you again for your guidance!

Best,
Klaus
```

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
   - **To:** LEAVE BLANK — Klaus adds the client (or the authorized contact) and sends.
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

## One Legal case-initiation (reference for the user's e-file step)

Klaus e-files; this is just the map so his selections are right (and a good way to CONFIRM
an unfamiliar county — One Legal's Case Initiation form lists that court's accepted case
types and required docs, so "test on One Legal" is a legit court-rule verification path):

- **Case Initiation** (new case) → **Order type**: `Filing` = file only (serve separately);
  `File + Serve` = One Legal also serves the defendants. Ask Klaus which he wants.
- Subject matter **State** → **California** → **Choose the court** = the county
  (e.g. `Ventura County, Superior Court of California`).
- **Case Category** = `Civil Unlimited` (for an unlimited PI complaint).
- **Case Type** = the PI/PD/WD type: dog bite → `PI/PD/WD - Premises Liability` OR
  `PI/PD/WD - Other` (mirrors the CM-010 "Other PI/PD/WD (23)" box) — both accepted.
- **Case Title** = the **party caption** `LAST v. LAST, et al.` (e.g.
  `BO TAO v. EUTIMEO BEAS, et al.`) — NOT the internal folder name.
- **Jurisdictional Amount** = `Over $35,000` (unlimited). Complex / Class Action / Sealed
  = unchecked for a standard dog-bite case.

## Firm standing rules

- **Phone & fax on ALL litigation documents = (626) 479-2207** (Klaus, 2026-07-09).
  The fill engine forces the CM-010 attorney phone AND fax to this number. If Hernán's
  complaint caption still shows the old fax (626) 240-2046, flag it (don't silently edit
  his pleading).

## On completion — ALWAYS report these two paths to Klaus

Klaus wants, every time a package is prepared, an explicit trail of HOW it was
determined — not just the result. End with:

1. **Court-finding path** — the DOUBLE verification: county from the complaint caption →
   ① what One Legal's Case Initiation offered for that county (authoritative shortlist) →
   ② confirmation on the court's own site (locations page; for LA also the LASC Filing
   Court Locator with the incident city+ZIP) → the exact courthouse + address (+ district),
   citing BOTH sources. Say so plainly if only one source could be checked.
2. **Court-rule path** — how you confirmed which forms/rules apply: which county rule set
   in `court-rules.md` (or, for a new county, the court's civil-filing-info + local-rules
   pages you read) → what's required to FILE vs to SERVE → the source URLs. State plainly
   if a rule could not be verified and was flagged for Klaus/Hernán.

## Adding a new county (the "learn one, remember it" loop)

When the complaint's county is not yet in `court-rules.md`:

1. **Research the county's civil first-paper requirements** (WebSearch the county
   Superior Court's civil filing info + local rules): does it require a local
   Civil Case Cover Sheet Addendum or any other local first-paper form — AND whether
   it actually covers THIS case type (e.g. LA's CIV 109 covers PI; Ventura's VN278 does
   NOT list PI(23), so a dog-bite case files none). How is branch/venue determined? Fee.
   **Never fabricate a court rule — cite the court's own page. If you can't verify,
   flag it and ask Klaus/Hernán rather than guessing.**
2. **Get the fillable form**: download the county's addendum PDF, upload it to the
   Litigation Forms Drive folder (`1XWPPpjckq…`), and add its id to `get_templates.sh`.
3. **Map the form** into `fill_forms.py`: add the county addendum's field names /
   checkbox stamp coordinates (mirror how CIV 109 is handled — `CIV109_ACTION_XY`),
   then render-verify (Step 5) until every box lands.
4. **Record the county** in `references/court-rules.md` (a new section with: addendum
   form + id, branch/venue rule, CM-010 box, action code/reason, fill map name).

Now that county is a fast path for every future case.
