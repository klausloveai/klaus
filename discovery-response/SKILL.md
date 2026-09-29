---
name: discovery-response
description: >-
  Draft a complete written-discovery response package for a 凌图律所 / Law Office of Shenqi
  Cai APC (Hernán Simó / dog-bite / PI / litigation) case — responses to Form
  Interrogatories (DISC-001), Special Interrogatories, Requests for Production and
  Requests for Admission, plus the Bates-stamped production, the index of documents
  produced, the verification with Declaration of Translator, and the proofs of service.
  Use whenever opposing counsel serves written discovery and the responses are due:
  triggers include "discovery responses", "respond to FROG", "respond to RFP", "RFA
  responses", "prepare the discovery responses", "准备 discovery 回复", "做 FROG 回复",
  "回复对方的 discovery", "/discovery-response" for a named case. It DRAFTS ONLY — leaves
  the client verification and the attorney signature blank, never serves and never
  e-files. The calibration standard is Hernán's own signed work; run `preflight.py`
  before handing anything to him and fix every finding first.
---

# discovery-response — written discovery response package

Goal: **hand the attorney a draft that needs the fewest possible corrections.** The
measure of success is not "a complete draft" — it is how little Hernán has to change.
`references/hernan-standard.md` is the catalogue of what he actually changed the first
time (Yi Cong, Sept 2026) and every item in it is a check you must run yourself.

## Gold references — read before drafting

| What | Where |
|---|---|
| **Response format + objection style** | Zhiping Liu v. State Farm, *Claimant's Responses to FROG, Set One* (DocuSign, signed by Hernán). 19 of 63 answers carry an objection; each is **one ground with a statutory or constitutional cite**, never a stack. |
| **Full package standard** | Yi Cong v. Edpao, `4.4 Discovery – From Defense` → the three `HERNAN FINAL` PDFs. Caption, POS, verification + translator declaration, "no document withheld" line, calculation shown in the answer. |
| **Pleading paper** | Any of the above; the docx engine in `scripts/common.py` clones the paragraph prototypes so fonts and line numbers survive. |

Do **not** calibrate against another attorney's file. Cassie's responses run a 73%
objection rate with stacked boilerplate; Hernán's run ~30% with single cited grounds.
Match the attorney whose name goes on the document.

## Workflow

1. **Compute the real deadline before anything else.** 30 days from service
   (CCP §2030.260, §2031.260, §2033.250), **+5 calendar days if served by mail**
   (§1013), **+2 court days if served electronically** (§1010.6(a)(3)(B)). Check the
   opposing POS for which box is ticked — do not assume. Calendar it, and tell Klaus
   when it differs from what the attorney has on his calendar.
   **Untimely = all objections waived, including privilege** (§2030.290(a),
   §2031.300(a)). **RFAs are worse: unanswered requests can be deemed admitted**
   (§2033.280). If an RFA set is in the batch, say so loudly.

2. **Read the served documents yourself.** Render the checked boxes with **ghostscript**
   and read them page by page — poppler shows tofu on non-embedded fonts, and a summary
   of which interrogatories are checked is not evidence. Note the Sec. 4(a) INCIDENT
   definition; a defence template written for a motor-vehicle case is a real defect worth
   preserving on the record.

3. **Build the fact inventory before writing a word.** Every answer must trace to a
   document. List the sources (client questionnaire, DL, medical records and bills,
   agency reports, photographs, payment records) and answer *from* them.

4. **Cross-check the client's answers against the documents.** This is the highest-value
   step and the one only the paralegal can do. In Yi Cong it produced three findings the
   discovery itself never would have: prescriptions predating the incident, an office
   visit with no records, and a wage timeline contradicted by our own intake sheet.

5. **Draft.** `scripts/common.py` carries the objection library and the docx engine.
   Objections: one ground, one cite, no stacking. Where you object but still produce
   everything, add the withholding sentence (see the standard).

6. **Build the production.** `scripts/make_production.py` Bates-stamps in a clear strip
   at the foot of each page (it scales the page content up rather than covering it).
   Produce documents as received, transmittal covers included, so no completeness
   objection can be made. Wire the Bates ranges into the responses themselves —
   §2031.280(a) requires produced documents be identified with the request number.

7. **Run `scripts/preflight.py`.** It fails the build on anything in the standard that
   can be checked mechanically. Fix every finding before the attorney sees it.

8. **Flag what is genuinely his.** Yellow-highlight only real attorney decisions, each
   prefixed `[FOR <ATTORNEY> — REMOVE BEFORE SERVICE]` so a single colour scan clears the
   document before service. Facts you can source are not decisions; go find them.

9. **File to the case folder** (`4.4 Discovery – From Defense` or the matching subfolder)
   and append one Activity Log line. Never leave the working copy in ~/Downloads as the
   authoritative version.

## Hard rules

- **Never write a fact the documents contradict.** If the client's account and a document
  disagree, answer to the document, disclose the client's account, and say the record has
  been requested. The client signs the verification under penalty of perjury.
- **Verification must match the answers.** If FROG 2.9/2.10 say the client does not read
  English with ease, the verification cannot say he "read" the responses — it must say it
  was translated to him, and a **Declaration of Translator** goes below his signature.
- **Serve every appeared party.** Check the docket for co-defendants who have answered;
  they get the responses too, and the caption picks up `AND RELATED CROSS-ACTION` when a
  cross-complaint is on file.
- **Draft only.** Verification unsigned, attorney signature blank, nothing served.

## Output

To the case folder, as `.docx` for the responses and index (the attorney edits in Word;
the served PDF is exported from Word), and `.pdf` for the production. Plus a short memo
of the open decisions if there are more than two.
