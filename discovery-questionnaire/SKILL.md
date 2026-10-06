---
name: discovery-questionnaire
description: |
  Turn written discovery that opposing counsel just served into a questionnaire the CLIENT
  can actually fill in, for 凌图律所 / Law Office of Shenqi Cai APC (Hernán Simó / dog-bite /
  PI / litigation). Use whenever a discovery packet arrives and the next move is to get the
  answers out of the client: triggers include "对方发来了 discovery", "做一份问卷发给客人",
  "把 FROG 翻译成中文给客户填", "客户问卷", "discovery questionnaire", "which FROGs did they
  check", "prepare the client questionnaire", "/discovery-questionnaire" for a named case.
  Typical invocation: the Gmail thread or the PDFs Hernán forwarded. It reads what was
  actually served (reading checked boxes off scanned FROGs page by page), builds a bilingual
  working copy on firm letterhead with every served interrogatory verbatim, builds a
  simplified Chinese client questionnaire that merges the duplicate questions across FROGs /
  SROGs / RFP and carries a back-reference so answers map home, drafts the WeChat message,
  and logs the Activity Log line. It DRAFTS ONLY — never sends to the client, never serves,
  never e-files. Hand off to `discovery-response` once the client's answers come back.
---

# discovery-questionnaire — served discovery → client questionnaire

This skill owns the gap between "OPC served discovery" and "we have the client's answers."

| Stage | Skill |
|---|---|
| OPC serves → get answers from the client | **this skill** |
| Answers → response package, Bates production, verification | `discovery-response` |
| Finalised responses → Chinese copy for client verification | `discovery-translation-zh` |

Never draft the formal responses here. This output goes to the client, not to the court.

## What the client sees, and why

Two documents, both on firm letterhead (`assets/letterhead.docx`, first page only,
footer with firm name + page number on the rest):

1. **Bilingual working copy** (`case` mode) — every interrogatory OPC actually served,
   English verbatim from the form / their pleading, Chinese underneath in yellow highlight.
   This is the audit trail: when drafting responses, each answer maps to a numbered item.
2. **Simplified Chinese questionnaire** (`client` mode) — what actually gets sent. FROGs
   and SROGs overlap heavily (医疗机构 gets asked three times); this merges them into
   grouped plain-Chinese questions, each carrying a small grey `（对应 FROG 6.4、SROG 31）`
   back-reference so the answers map home when drafting.

Send the client the **.docx** (they type into the cells); the PDF is only for Klaus to
check the rendering.

## Formatting contract — do not regress these

Earned the hard way; `scripts/render.py` enforces all of it.

- **Answers live in table cells**, never on an underline. A leader-tab underline gets
  pushed right as the client types and the text ends up beside the line, not on it. Fixed
  column widths (3.0" label / 3.5" answer), cells grow downward only.
- **`w:noProof` on every run** + `hideSpellingErrors` / `hideGrammaticalErrors` in
  settings.xml. Mixed EN/ZH otherwise renders under a carpet of red squiggles on the
  client's machine, and turning it off locally does not travel with the file.
- **East-Asian font pinned to SimSun** on every run. The letterhead's Normal style defaults
  CJK to Arial Unicode MS, which looks nothing like the firm's other templates.
- **Yellow highlight = the Chinese question** (the line the client reads). **Red bold =
  the warnings that cost cases.** Never yellow a warning — it disappears into the other
  hundred yellow lines.
- **`cantSplit` on every row** so an item never breaks across a page.
- The letterhead carries `Fax: 626-240-2046`, which is barred from firm letterhead;
  `render.py` rewrites it to the General Fax **626-323-8181** on every build and prints
  what it changed. See `firm_directory` / `feedback_header_fax_pairing`.

## Workflow

1. **Pull everything that was served.** Work from the Gmail thread, not from whatever is
   already in Downloads — Klaus usually downloaded only one attachment. Save the whole set
   into `~/Downloads/<Client> Discovery/`. A packet is typically 6 files: Answer, Demand for
   Jury + Notice of Posting Jury Fees, Demand for Production, Special Interrogatories,
   FROGs, Notice of Deposition. Only three need written responses.
2. **Read what they actually asked.** `pdftotext -layout` first. SROGs and RFP normally
   carry a text layer; **the FROGs are a scan with no text layer** — render each page
   (`pdftoppm -png -r 100`) and read the checked boxes off the image, page by page. Record
   the result in the case module with the date you read it. Also read page 1: who is the
   propounding / responding party, the set number, and which `INCIDENT` definition is checked.
3. **Count and sanity-check.** See `references/reading-served-discovery.md` — the 35-SROG
   limit and its §2030.050 declaration, boilerplate the defence checked that cannot apply to
   a plaintiff, and questions that must not be put to the client at all (SSN, Medicare HICN).
4. **Write the case module.** Copy `cases/bo-tao-2026CUPO069898.py` and edit. It holds the
   caption, the checked list, who answers each SROG, the Chinese groupings, and the document
   list. Nothing else is case-specific.
5. **Build both documents** and render each to PDF to eyeball the layout:
   ```
   python3 scripts/build.py case   cases/<case>.py
   python3 scripts/build.py client cases/<case>.py
   ```
6. **Fill the gaps before it goes out.** Date of incident (the dog-bite folder name
   `<Client>-<MMDDYY>` carries the DOL) and the response deadline. Compute the deadline
   (30 days + 2 court days for e-service, + court holidays) but **flag it for Hernán's
   calendar rather than asserting it.**
7. **Draft the WeChat message** — plain text, 全角, no markdown, in a code block. Covers:
   this is a mandatory court procedure, the return-by date, write 不适用 rather than leaving
   blanks, do not guess, disclose old injuries, preserve any physical evidence OPC named,
   and the materials list.
8. **Stop.** Show Klaus the rendered PDF and the message. He sends it.
9. **Log one Activity Log line** — Category 起草, Source Local, Ref/ID the case number.

## Hard rules

- **Draft-only.** Never send to the client, never serve, never e-file.
- **Never put the client's SSN or Medicare HICN on a questionnaire that travels by email
  or WeChat.** Render those items with no answer box and a red note that the firm handles
  them separately. They are also squarely objectionable on privacy grounds.
- **Strip the items the client cannot sensibly answer.** FROG 15.1 (denials and affirmative
  defenses) and most of 16.0 are propounded *by* a plaintiff *to* a defendant; defence
  counsel check them out of habit. Keep them in `ATTORNEY_ONLY` so the bilingual copy still
  shows all 54 served items while the client sees only the 52 that are theirs.
- **Preserve-evidence warnings go in red and in the WeChat message, not just in the doc.**
  When the RFP names a physical item ("the shoes the Plaintiff was wearing"), the client
  has to be told today, not when they open a 19-page attachment.
- **Never state a filing or payment conclusion from the Drive case folder alone.** Filings
  are routinely accepted by the court and never archived. One Legal billing is the record:
  a `Notice of Posting of Jury Fees` shows up as disbursed **$155.25–155.94** / total
  **≈$180** (`/app/matters/{id}/billing`, or the `document` field on
  `/api/v1/Matter/{id}/Invoices`). See `posting-jury-fee`.

## Output

- `~/Downloads/<Client> Discovery/` — the served PDFs, the two .docx, and the preview PDFs
- The WeChat message in a code block
- One Activity Log row
- A short note of anything that still needs Klaus or Hernán: the deadline, the DOL, and any
  objection worth preserving (over-limit SROGs, a defective §2030.050 declaration, an
  unapproved preface under §2030.060(d), privacy items)
