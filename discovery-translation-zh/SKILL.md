---
name: discovery-translation-zh
description: >-
  Produce the Chinese client-verification translation of a finalised discovery response
  package for 凌图律所 / Law Office of Shenqi Cai APC — responses to Form Interrogatories,
  Special Interrogatories, Requests for Production or Requests for Admission, the index of
  documents produced, and the verification with Declaration of Translator, all on the same
  pleading paper as the English original so the client can read them line for line against
  it. Use whenever a Chinese-speaking client must confirm his answers before signing the
  verification: triggers include "翻译成中文给客户核对", "把答复翻成中文", "中文译本",
  "discovery 中文版", "translate the responses for the client", "client verification
  translation", "/discovery-translation-zh". Required whenever the client answered Form
  Interrogatory 2.9 or 2.10 "no" — the verification then cannot say he read the responses,
  only that they were translated to him, and a translator must sign. Translation only:
  never served, never filed, never sent to opposing counsel.
---

# discovery-translation-zh — Chinese client-verification translation

The English set is what gets served. This translation exists for one purpose: so the
client can check that every answer is true **before** he swears to it. Hernán's standing
instruction on Yi Cong was to review the responses with him "in Mandarin Chinese, answer
by answer, before he signs." This is the document you do that with.

It also supplies the evidentiary basis for the verification itself. When Form Interrogatory
2.9/2.10 are answered "no" — the client does not read English with ease — a verification
saying he "read" the responses contradicts his own answers. It must say they were
**translated to him**, and the translator signs a **Declaration of Translator** below.
Producing the translation is what makes that declaration true.

## Translate only the final, attorney-approved English

Never translate a draft. A client who verifies a translation of superseded text has
verified nothing. Work from the version the attorney returned and confirm the answer count
matches before you start.

## What stays in English

- **Client, party, company and provider names** — YI CONG, RHEA EDPAO, KK NOW LA LLC,
  TY FLY EXPRESS INC, Healthier Minds, Inc. House rule: client and case names are never
  auto-translated, in any context.
- **Street addresses** — they are the real US addresses; translating them makes the
  document useless for checking against the English.
- **Bates numbers, policy numbers, check numbers, tracking numbers, ICD and CPT codes.**
- **Case citations and statute names** — `Britt v. Superior Court (1978) 20 Cal.3d 844`
  stays as it is; translate only the sentence around it.

Everything else is translated. Keep the answer numbering identical so the two documents
read side by side.

## Required elements

1. **A notice to the client at the top**, bracketed, in the body — that this is a
   translation of the English original for checking only, that opposing counsel receives
   the English, and that any inaccuracy must be raised *before* signing.
2. **The same pleading chrome** — line numbers, side rules, caption table, footer.
   `scripts/zh_shell.py` clones it from `discovery-response`'s base document.
3. **The translated verification** plus the **Declaration of Translator**, both with
   signature and date blank.
4. **Consistent terminology** — use `references/glossary.md`. The objection and
   supplementation boilerplate repeats dozens of times; one rendering, used everywhere.

## Workflow

1. Extract the final English answers:
   `pdftotext -layout <final>.pdf -` then split on `RESPONSE TO ... NO. n:`.
2. Author the translation as a data list mirroring the English structure.
3. Build with `scripts/zh_shell.py`. It sets `eastAsia` to a CJK face on every run and
   leaves the Latin runs in Times New Roman, so both scripts render correctly.
4. Run `scripts/zh_check.py` — it fails on a mismatched answer count, a client name that
   got translated, missing verification or translator declaration, and tofu.
5. Render and eyeball at least the first page, a middle page and the verification page.
   `pdftotext` is not proof that the glyphs drew.
6. **Deliver PDF only.** Client-facing translations are never handed over as `.docx` —
   an editable translation of a sworn document invites exactly the argument you do not want.
7. File to the case folder alongside the English set and log one Activity Log line.

## Hard rules

- Translation only. Never served, never filed, never sent to opposing counsel.
- Never soften an answer in translation to make it easier for the client to accept. If he
  disagrees with an answer, that is the point of the exercise — tell the attorney before
  anything is signed.
- If the English is corrected after the client has reviewed the translation, re-translate
  the changed answers and have him confirm again. A signature on the old text is stale.
