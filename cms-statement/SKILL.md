---
name: cms-statement
description: >-
  Draft the CM-110 Case Management Statement (CMS) for a 凌图律所 / Law Office of
  Shenqi Cai (Hernán Simó / dog-bite / PI / litigation) case — a filled, flattened,
  signature-ready 5-page PDF plus the short email sending it to Hernán for review and
  signature. Use whenever a CMC is calendared and the statement is due, or on any of:
  "CMC statement", "CM-110", "case management statement", "prep a CMC", "file and serve
  CMC statement", "做 CMS", "案件管理陈述", "/cms-statement" for a named case. It
  DRAFTS ONLY — leaves DATE + SIGNATURE blank for the attorney and never e-files or
  serves. Always compute the real CRC 3.725 deadline (15 calendar days before the CMC)
  and flag it when the calendar task disagrees. Always trigger for any "prepare the CMC
  statement / CM-110" request, even a partial one.
---

# cms-statement — CM-110 Case Management Statement

One filled CM-110 → Hernán reviews and signs → Klaus files and serves. Draft-only.

## Deadline — compute it, never trust the calendar task
**CRC 3.725: the CM-110 must be filed and served no later than 15 CALENDAR DAYS before
the CMC.** Hernán's calendar often carries a "File and serve CMC Statement" task whose
date was computed from an *earlier* CMC and never moved when the CMC was continued.
- Read the CMC date off Klaus's Google Calendar (`gws calendar events list -q "<Client>"`),
  not off the task title.
- Worked example (Guolin Zhao): CMC continued to **11/23/2026** → rule date **11/08/2026**,
  but the calendar task still read **09/29/2026** (that tracked the original 10/13 CMC).
- If the two disagree, **prepare it now and ask Hernán which date to file by.**

## Facts to verify before filling (never guess — CLAUDE.md red line)
| Item | Source of truth |
|---|---|
| CMC date / time / dept | Google Calendar + the Notice of Case Assignment (judge + dept) |
| Complaint filing date | the **conformed** complaint's e-filing stamp (render it; the stamp is an image) |
| Case no., court, branch | conformed complaint / Notice of Case Assignment |
| Service status per defendant | One Legal order history + POS on file + any default request |
| Attorney block | the complaint caption; **FAX = 626-479-2207** per [[litigation_doc_header_phone]] |

## Hernán's standing answers (confirmed on his signed Guolin Zhao CM-110, 2026-09-25)
These are baked into the script — do not leave them for him to fill:
1. **Item 10a(1)** — Counsel **has** provided the ADR information package. ✔
2. **Item 10a(2)** — Party **has** reviewed the ADR information package. ✔
   *He checks BOTH sub-items even though the party is represented — this was his only
   edit to 10a on the Guolin Zhao draft.*
3. **Item 10c ADR matrix** — elect **Mediation** AND **Settlement conference**; for each,
   check the process column plus "**… not yet scheduled**" (4 boxes total). No dates.
4. Everything else in Klaus's draft he accepted unchanged: 5-day trial estimate, jury
   demanded, item 8 "by the attorney listed in the caption", items 11/12/13/14/15/17/18
   left blank, item 16b anticipated discovery, item 19a unchecked + explanation, item 20 = 0.

## Defaults that were accepted
- **Item 5** jury trial (the firm demands jury and posts fees).
- **Item 6b** no trial date set. ⚠️ The form **pre-prints "within 12 months"** — the blank
  next to it is the "(if not, explain)" line. Leave it EMPTY; writing "12" there is wrong.
- **Item 7a** days — 5 for a dog bite. Confirm with Hernán if the case is unusual.
- **Item 16b** two rows: written discovery to each appearing defendant; depositions +
  records subpoenas (animal control, medical). Date column = "Per Code".
- **Item 19a** leave the box UNCHECKED when no defendant has appeared, and explain in the
  blank (who was served, when, any default request, who is still being served).
- **Item 20** total pages attached = 0. **Date + signature blank.**

## Item 3 — service, the part that actually gets read
Check 3b, then the sub-boxes that apply:
- **(1) not served** — defendants still being served, plus the remaining DOES ("names not
  yet ascertained").
- **(2) served but not appeared** — name, service method and date, and any Request for
  Entry of Default already filed.
- **(3) default entered** — only once the clerk has actually ENTERED it, not when the
  request was merely filed.
These are **single-line** fields (~460pt): keep each under ~100 characters or the script
shrinks the type to stay inside the box.

## How to build
1. Write a config JSON (schema in the script header; worked example lives beside this file).
2. `python3 ~/.claude/skills/cms-statement/scripts/make_cm110.py <config.json>`
   → `<prefix> - CM-110 Case Management Statement.pdf` in `output_dir` (default ~/Downloads).
3. **Verify with ghostscript**, never pdftoppm: `gs -o /tmp/cm_%d.png -sDEVICE=png16m -r110 <pdf>`
   (the Judicial Council forms use non-embedded Arial; poppler renders tofu).
   Eyeball all 5 pages: no clipped text, every intended box marked, date/signature blank.
4. Draft the email to Hernán — **one sentence**, per [[feedback_drafts_keep_simple]]:
   > Attached is the Case Management Statement for \<Client\> for your review and signature.
   To Hernán, Cc Cassie + Joe, preset Gmail signature, PDF attached. **Never send without
   Klaus's explicit go** ([[feedback_show_draft_before_send]]).

## Implementation notes (why the script looks like it does)
- **Never fill CM-110 text through the AcroForm.** `qpdf --generate-appearances` does not
  word-wrap multiline fields — it draws one line and silently clips the rest (item 4b lost
  most of the case summary), single-line fields clip too, and leaving `/NeedAppearances`
  true makes some renderers draw a value twice.
- The working order is **checkboxes on the AcroForm → flatten → overlay text** with
  reportlab at the real field rects, wrapping and auto-shrinking to fit. Overlay-then-flatten
  is the wrong order: flattening paints the widgets' blank appearance over your text.
- Accents (Hernán S. Simó) survive because the overlay embeds Arial.
- The CM-110's own "Print / Save / Clear this form" footer buttons remain on page 5 even in
  the court-accepted copies — harmless, leave them.
- `assets/EXAMPLE_Guolin_Zhao_signed_CM110.pdf` is Hernán's signed copy; diff new drafts
  against it when in doubt.

Related: [[litigation_service_of_process]] · [[doe-amendment]] · [[hernan_litigation_conventions]]
