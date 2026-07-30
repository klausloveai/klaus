---
name: posting-jury-fee
description: >-
  Draft (do NOT file) a Notice of Posting of Jury Fees for a Hernán Simó litigation case at
  凌图律所 / Law Office of Shenqi Cai APC, from the firm's Drive template. Use whenever any of
  these are mentioned: notice of posting of jury fees, post jury fees, jury fee notice, 缴纳陪审费通知,
  jury fees for <client>, CCP 631 jury fee, "/posting-jury-fee" for a named case. Given a client/case,
  it pulls the Drive template, fills the caption (verbatim from the filed complaint), the case number,
  and today's date, renders docx + PDF to ~/Downloads, and reminds of the sign/post/file workflow.
  DRAFTS ONLY — it never posts the fee, never e-files, and never emails (Klaus reviews and routes).
---

# Posting of Jury Fees — Notice (draft only)

Produce a **Notice of Posting of Jury Fees** (Code Civ. Proc. § 631, $150.00 advance jury fee)
for a Hernán Simó litigation case, from the firm's Drive template. **Draft only** — do not post
the fee, do not e-file, do not email. Klaus reviews, then routes: post $150 → Hernán signs →
One Legal Subsequent Filing.

## Constants
- **Drive template:** `Notice of Posting of Jury Fees - TEMPLATE.docx`, id
  `1R7qORm5hARDjq323gmZajkqT4I3uGpUY`
  (https://docs.google.com/document/d/1R7qORm5hARDjq323gmZajkqT4I3uGpUY). It's a real **.docx**
  (not a Google Doc) → download with `alt:media`, do NOT `export`. Always re-fetch (the firm edits it).
- **Tokens in the template:** `[PLAINTIFF NAME]`, `[DEFENDANT NAME]`, `[CASE NO.]`, plus a hardcoded
  **"DOES 1 through 50"** and a Word DATE field.
- **Signer:** Hernán S. Simó, Esq. (SBN 354175) — already baked into the template. Do not change.
- **Format rule (Hernán, 2026-07-29):** the Plaintiff's name sits on its OWN line directly beneath
  "Attorney for Plaintiff" (both the top attorney block and the signature block). The template already
  encodes this with a `<w:br/>`; **fill tokens at the XML level so the line break survives** — a
  python-docx paragraph-level replace collapses the two runs and destroys it. `scripts/fill_jury_fee.py`
  does this correctly. See [[pleading_template_and_contact_standard]], [[jury_fee_notice_workflow]].
- **Scratch:** `~/lor_work` or a temp dir; `gws` rejects `-o` paths outside the cwd and the Bash cwd
  resets between calls — use absolute `$HOME/...` paths. Strip the `Using keyring backend` banner before
  `json.loads` (slice from the first `{`).

## Step 1 — Get the caption from the FILED complaint (verbatim)
The caption must verbatim-match the filed Complaint. Locate the case in the **"Hernan Simo Cases"**
shared drive (or the One Legal order PDF / the drafted Complaint the user points to) and read the
Complaint's first page to extract, exactly as written:
- **Plaintiff name(s)** — e.g. `LINA LU` (use the caption's casing).
- **Defendant name** — e.g. `ARLENE LUNA`.
- **DOES count** — the exact "DOES 1 through **N**" (Lina Lu = 25; the template default is 50, so this
  almost always needs changing). Do NOT assume 50.
- **Case number** — from the Notice of Case Assignment / E-Filing Confirmation / complaint caption
  (e.g. `26PSCV02595`).

If the complaint isn't findable, ask the user for these four values rather than guessing.

## Step 2 — Download the template
`gws` rejects `-o` paths outside the current directory, so **cd into the scratch dir and use a
relative `-o`** (all in one command, since the Bash cwd resets between calls):
```bash
mkdir -p ~/lor_work && cd ~/lor_work && gws drive files get --params '{"fileId":"1R7qORm5hARDjq323gmZajkqT4I3uGpUY","alt":"media","supportsAllDrives":true}' -o jf_template.docx
```
Note: the template lives as a Google-Docs-backed file that Klaus sometimes edits in the browser, so its
internal run/line structure varies (a name-below break may be a `<w:br/>` or a paragraph break). The fill
in Step 3 is token-based, so it works regardless — just inherit whatever line format the live template has.

## Step 3 — Fill it
Write the fields JSON and run the fill script. `date` = **today**, written `Month D, YYYY`.
```bash
cat > "$HOME/lor_work/jf_fields.json" <<'JSON'
{"plaintiff":"LINA LU","defendant":"ARLENE LUNA","case_no":"26PSCV02595","does_count":"25","date":"July 29, 2026"}
JSON
python3 ~/.claude/skills/posting-jury-fee/scripts/fill_jury_fee.py \
  "$HOME/lor_work/jf_template.docx" \
  "$HOME/Downloads/<Client> - Notice of Posting of Jury Fees.docx" \
  "$HOME/lor_work/jf_fields.json"
```
The script fills the tokens at the XML level (preserving the name-below `<w:br/>`), replaces
"1 through 50" with the real DOES count, sets a static Dated line (removing the DATE field), and
aborts if any `[TOKEN]` is left unfilled.

## Step 4 — Render PDF + QC
```bash
soffice --headless --convert-to pdf --outdir "$HOME/Downloads" "$HOME/Downloads/<Client> - Notice of Posting of Jury Fees.docx"
```
Render the PDF (qlmanage → PNG) and read it back to confirm: caption matches the complaint (incl. DOES N),
Case No. correct, "Attorney for Plaintiff" with the plaintiff name on the line BENEATH it (both places),
date correct, pleading line numbers 1–28 intact.

## Step 5 — Deliver + remind
Report the delivered paths (`~/Downloads/<Client> - Notice of Posting of Jury Fees.docx` and `.pdf`) and
the workflow that is NOT part of this skill:
1. **Post the $150.00 advance jury fee** with the court (CCP § 631, per side, due before the first CMC).
2. **Email Hernán the docx + PDF for signature** (cc Cassie & Joe) — Klaus routes this.
3. **File the signed notice via One Legal** (Subsequent Filing).

Never post the fee, e-file, or email from this skill. Draft only.
