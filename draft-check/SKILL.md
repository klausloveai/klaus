---
name: draft-check
description: >-
  House-style + content self-check that Klaus runs whenever Claude drafts ANY
  Lingtu Law / Law Office of Shenqi Cai (or Hernan Simo / dog-bite) document —
  letters (LOR / LOP / withdrawal / POE / lien-reduction / disbursement / demand /
  general correspondence), pleadings/complaints, court forms, provider-facing
  emails, and client WeChat bulletins. Trigger whenever any of these are said:
  draft-check, "自检", "格式检查", "查一下格式", "draft 前/后检查", "按 house style",
  "/draft-check", or right before/after drafting a firm document. Consolidates
  every format + tone calibration Klaus has given (esp. the recurring ones:
  日期居中, official letterhead, bold RE/SUBJECT, justified body, no-attorney-driven
  wording, no fabrication). It is a CHECKLIST + self-audit only — it does not
  send, file, or upload anything; it verifies a draft conforms before Klaus sees it.
---

# draft-check — Lingtu house-style & content self-check

Purpose: **stop repeating the same corrections.** Every rule below is something
Klaus has already corrected at least once. Run this whenever you draft a firm
document — ideally BEFORE producing the draft (so you build it right) and AGAIN as
a final pass BEFORE showing it to Klaus.

## How to run it

1. **Identify the document type** → pick the matching section below (A letters /
   B pleadings / C court forms / D provider email / E client bulletin).
2. **Apply the Universal rules (§0)** — they hold for everything.
3. **Draft (or re-open the draft) and self-audit** line-by-line against the
   checklist for that type.
4. **Report to Klaus what you checked** — a short "✅ house-style pass" list of the
   items you verified (date centered, letterhead, no yellow, numbers foot, …), so
   he can see the calibration was applied and doesn't have to re-catch it.
5. If anything can't be satisfied (missing info, ambiguous signer, etc.) **flag it,
   don't guess.**

> This skill never sends/files/uploads. It only makes the draft correct.

---

## §0 · Universal rules (every document)

- **NO fabrication, NO missing info.** Never invent facts, numbers, dates, ICD
  codes, findings, providers, or citations. If a value isn't in the source, leave
  a clear placeholder and flag it — don't guess. Verify every number twice.
- **No yellow highlight in the finished product.** Yellow/`FFFF00` highlight (and
  red instruction text) belongs ONLY in blank templates. Strip ALL of it from the
  shipped docx/PDF. (Demand templates also hide fill-ins as yellow FONT on black
  total rows — clear those too.)
- **Dates:** default to **today's date** unless told otherwise; write them out
  **Month D, YYYY** (e.g. July 10, 2026), not 07/10/2026.
- **Language:** talk to Klaus in 简体中文; the document content itself stays in its
  proper language (legal English for letters/pleadings, 中文 for client bulletins).
- **Fix objective typos silently; FLAG substantive wording changes** for the
  attorney to accept — never silently rewrite legal wording in the attorney's draft.
- **Right signer / right mailbox** — see §A.8 and the memory rules
  ([[feedback_send_from_case_mailbox]], [[feedback_email_signature_sender]]).

---

## §A · Firm LETTERS (LOR, LOP, withdrawal, POE, lien-reduction, disbursement, demand, any correspondence)

This is the house style Klaus has re-corrected the most. A conforming firm letter
(the Jiayu Ma / Zhiping Liu / Chao Zheng exemplars) has ALL of:

1. **Official letterhead** — build on the firm's letterhead shell, never a
   hand-typed text header. Source: **"6. Letter Header.docx"** (Drive id
   `1amZfOdIUtNMH1fwrvU-4JUYcy6xpotxc`) = 凌图 / Lingtu logo + black/gold banner
   top-left, contact block top-right. Set section **top margin ~3240 DXA (2.25")**
   so the body doesn't overlap the logo. See [[firm-letterhead]].
   - Demand letters use the demand template's own letterhead (City of Industry,
     13191 Crossroads Pkwy N STE 295) — see [[demand-package-workflow]].
2. **Date — CENTERED.** (Klaus's single most-repeated correction. Always confirm
   the date is horizontally centered.) Default = today.
3. **RE / recipient / provider block — BOLD.** (Provider name, RE line.)
4. **SUBJECT / title — BOLD, and CENTERED below the letterhead** (above e.g.
   `PAYMENT REMIT TO` on lien/dis letters).
5. **Body — double-spaced, JUSTIFIED.**
6. **Numbered requests — bold lead-in sentence** for each numbered item.
7. **Bold the substantive anchors** — key legal terms, deadlines, the Statute of
   Limitations line + SOL date, dollar amounts on totals — but don't bold whole
   paragraphs (on a liability ¶, bold+italic only the actual cited code).
8. **Signature block — correct signer & format:**
   - General firm PI correspondence / demands → **Shenqi Cai, Esq.**
   - Dog-bite / "Hernan Simo Cases" litigation (pleadings, LOR, POE, GAL) →
     **Hernán S. Simó, Esq.**, SBN 354175, Direct (626) 479-2207, **Fax (626) 479-2207
     (SAME as phone — NOT 626-240-2046)**, hernan.s@lingtulaw.com. See [[hernan-litigation-conventions]].
   - Withdrawal of Representation → signature line is just **Lingtu Law Office**.
   - Signature block on pleadings lives in a TABLE (see §B).
9. **Header/contact phone = the HANDLING CM's direct line**, NOT the 888 office line.
   - ⚖️ **ALL LITIGATION / dog-bite documents: use Klaus's direct `626-479-2207` as BOTH
     the phone AND the fax** (his signature reads `D: 626-479-2207 | F: 626-479-2207`) —
     he handles these files. Klaus-set, 2026-07.
   - Hernán's *own* direct is **(323) 412-7274**; the general firm fax is **626-240-2046**.
     Don't mix the three up.
   - See [[feedback-form-firm-phone-cm]], [[hernan-litigation-conventions]], [[firm-directory]].
10. **Provider-facing letters also pass §D** (no attorney-driven wording).

> **LOP = LOR format.** A Letter of Protection uses the SAME layout as the current
> LOR — only the content differs (Klaus, 2026-07). More generally, when aligning one
> letter type to an established one, copy the established letter's format exactly.

Final letter audit: letterhead ✔ · date centered ✔ · RE/SUBJECT bold ✔ · body
justified+double-spaced ✔ · correct signer ✔ · CM phone ✔ · no yellow ✔.

---

## §B · Pleadings / COMPLAINTS

Follow the firm's existing template — **do not rebuild the layout from scratch**
(Klaus pushed back hard on this). See [[lingtu-complaint-format]].

- **28-line pleading paper:** line numbers 1–28 + double vertical rule live in the
  **page HEADER** (textbox/frame), not Word line-numbering. Body paragraphs use
  **EXACTLY 24pt** line spacing to hit the grid.
- **Caption is in a borderless table**; **signature block is in a table** at the
  end. When QC-ing a firm .docx, parse tables too — `doc.paragraphs` MISSES them.
- Section headings centered **bold + underline**; allegation ¶ auto-numbered,
  0.5" first-line indent.
- **Method:** start from the firm template .docx and edit content in place (keeps
  the header grid). Rebuilding via python-docx loses the look.
- Fix typos only; flag legal-wording changes for Hernán/Klaus.

---

## §C · Court FORMS (Summons SUM-100, CM-010, CIV 109, CIV-010/011, Cert of Assignment)

See [[hernan-litigation-conventions]] and [[file-complaint-skill]].

- **Caption verbatim-matches the complaint** — parties exactly as the complaint
  reads (incl. `, an individual` after each defendant, full GAL wording).
- **SUM-100 (Summons): name every defendant in full** (`, an individual` each) — they must
  be named for service; "et al." not allowed there. **On the small JC caption boxes
  (CIV-010/CIV-011)** the full list overflows, so Hernán wants the **SHORT caption**
  (`<MINOR>, a minor, etc., et al.` / `<DEFENDANT>, et al.`) — CRC 2.111 permits it on a
  subsequent paper. So: full defendants on the Summons/Complaint, short "et al." on the GAL forms.
- Minor plaintiff → file **BOTH CIV-010 (Application) AND CIV-011 (Order)** together
  (clerk won't issue Summons without them). Effective 1/1/2024 the JC split the old combined
  "Application AND Order" into two forms. CIV-010: fill print-name lines, leave signatures/dates
  blank (Hernán = attorney item 7; parent = applicant + proposed GAL). On CIV-010 remember the
  minor's **DOB** (item 4a), check **"has no guardian or conservator of the estate"** (item 6c),
  specify the **relationship** e.g. "Mother" (item 8b), and check **item 1a AND 1d** (parent is
  also a plaintiff = "a party to the suit") — Hernán flags these. CIV-011 = proposed Order:
  pre-fill caption/appointment/findings incl. **item 3 "notices given"** and **item 7 "is NOT"
  authorized to waive substantive rights** (protective option the bench expects for a minor);
  leave the **judge's** date + signature blank. Use the `gal-appointment` skill — it bakes all
  this in and flattens (qpdf) so it displays in Preview.
- Leave case number, signature, and date blank (skill drafts, never e-files).
- Verify filled Judicial-Council PDFs by **Ghostscript** render (not poppler).
- **FLATTEN before delivery.** pypdf-filled JC forms store values in the AcroForm but
  macOS **Preview won't render** those appearances → the recipient sees empty fields or
  stray placeholder digits ("1"/"5") even though gs shows them. Bake the values into the
  page with: `qpdf --generate-appearances --flatten-annotations=all in.pdf out.pdf`
  (0 fields remain; checkboxes become real "X"). Deliver the flattened copy. Signatures on
  JC forms are lines, not fields, so flattening never blocks signing.
- Confirm the target city is in the courthouse's "Areas Served" before filling
  district — don't assume the nearest one.

---

## §D · PROVIDER-FACING communications (referral / lien / LOP / records requests)

Avoid any "attorney-driven / 律所转介/安排治疗" tone. See
[[feedback-no-attorney-driven-language]].

- ❌ "we are referring / sending / placing the client" → ✅ "our client intends to
  seek treatment at <provider>".
- ❌ "…on a lien basis" (firm framing) → ✅ "as <provider>'s lien program requires".
- ❌ "we arrange / set up the appointment" → ✅ state only that the patient seeks
  care and the firm submits the documents the provider requires.
- Signing the lien itself is fine; only the "we referred / we arranged" wording is
  the problem.
- Email mechanics: send FROM the case's owning team mailbox, use the mailbox's
  **preset Gmail signature** (HTML), per [[feedback-email-signature-sender]]
  (Exer referral notices are the exception — they go from klaus@).

---

## §E · Client WeChat BULLETINS (公告 / 解释 / 回答)

See [[client-bulletin-house-style]].

- Title = emoji + short noun phrase; open with `🔔 说明:` one-liner.
- Section headers = emoji + bold short title; sub-points = **bold lead term**:explanation.
- Concrete landing action ("拍照发群里,我们帮您…"); plain text + emoji (no markdown bold).
- **NO `凌图律所` signoff** on client 群公告.
- **Ethics (must pass):** treatment is symptom-/doctor-driven, never "so insurance
  pays more"; never guarantee outcome; encourage honest mitigation; settlement
  accept-vs-fight is the client's decision (present net both ways, don't steer).

---

## Note for maintenance
When Klaus gives a NEW format/content calibration during a draft, add it to the
correct section here (and, if it belongs to one specific skill's output, also to
that skill's template). This file is the single source of truth for "how a Lingtu
document should look and read." Keep it in sync with the house-style memories it
links to.
