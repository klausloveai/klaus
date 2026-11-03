---
name: skye-submission
description: "Assemble a finalized Lingtu Law / SIA 高徒 USCIS filing into the electronic-submission PDF set, then split it and upload it to Drive. Covers locating the finalized folder in the client's PL folder, pulling the SIGNED forms from the case drive's 表格 / Forms folder (telling signed scans apart from the *-waiting signature drafts and verifying each signature by eye), and the pre-merge audit — per-case-type Checklist, missing translations, exhibits with no source-URL footer, AI-tool markers such as source=chatgpt in a URL, junk pages — all CONFIRMED with the attorney before merging. Then it merges in filing order behind cover pages, splits into the per-case-type set, under 11.92 MB each, and uploads into a 电子提交拆分 folder. Use for 电子提交 / 电子拆分, combining or splitting a package, finding the signed forms, auditing exhibits for missing 角标 / links / translations, or re-splitting an oversized file."
---

# Electronic Submission Assembly (Lingtu Law / SIA 高徒)

USCIS e-filing takes a handful of PDFs with a hard per-file size cap. This skill turns a
finalized case folder into that set: audit first, merge once, split last.

**The audit is the point.** Merging and splitting are mechanical. What actually protects the
filing is catching, *before* anything is combined, that a form is the unsigned draft, that a
criterion is missing a document the firm's checklist requires, that a Chinese exhibit shipped
without its translation, that a web capture has no source URL in its footer, or that a captured
URL carries `source=chatgpt` — which tells the adjudicator the research was done by an AI tool.

So the run is deliberately front-loaded and has a stop in the middle: audit everything, report
it, **wait for the attorney to confirm**, and only then merge. Steps 0-3 are cheap to redo;
everything after step 3 is not.

Work in this order. Each step's output is the next step's input.

```
0  locate folder, identify case type
1  preflight audit
2  collect the SIGNED forms
3  report  ──►  WAIT FOR CONFIRMATION
4  convert to PDF
5  cover pages + merge
6  split
7  verify + upload to 0.PL/电子提交拆分
```

---

## Step 0 — Locate the finalized folder and identify the case type

The case type drives the split plan, so settle it first. It is in the case-drive name
(`Yuqian Tao O1A`, `Bo Wang EB1A`) or the petition letter's RE line.

Finalized material lives under the client's case drive in the **PL folder** — usually
`0.PL/` — with the assembled evidence in a subfolder such as
`0.PL/EXHIBITS — O-1A Evidence Package` and prior submission sets in `0.PL/电子提交拆分`.
Names vary between cases; list the PL folder and confirm which subfolder is the finalized one
rather than assuming. If two look plausible, ask — filing a superseded draft is the one
mistake that cannot be walked back.

The firm's shared drive is `0AIXy3tjXMf-MUk9PVA`, with case-type folders at its root:
`O-1`, `EB1A`, `NIW`, `NVC`. Each holds per-client case drives plus a `0 Sample （X）`
template whose `6. Checklist` folder carries that type's checklist.

Master checklists (real `.docx` binaries — fetch with `files get --alt=media`, **not**
`files export`, which only works on native Google Docs):

| Type | File | ID |
|---|---|---|
| O-1 | `O1 Checklist.docx` | `10Pt70XyKsrvIIhpjJiXpO0ZdnIM1YT6r` |
| EB-1A | `EB1A Checklist.docx` | `19Wf_MQp1SHt4ToCycTgvYy1JJ1fKuKVG` |
| NIW | `NIW Checklist.docx` | `1ymGWx9-IpEtQ2xEcB5zbVHPpGye3mcvG` |

`gws` refuses any `-o` or `--upload` path outside the current directory, and takes the file id
inside `--params` (there is no `--file-id` flag). Run it with `cwd` set to the destination and
pass a bare filename.

---

## Step 1 — Preflight audit

Run all four checks and report findings **before** merging. Read
`references/preflight.md` for the procedures and the scripts to use.

1. **Checklist** — every item the case type's checklist requires, plus each criterion the
   petition letter actually argues. Report what is missing; do not silently substitute.
2. **Translations** — every Chinese-language exhibit needs an English rendering, and the
   Translation Certificate must enumerate all of them.
3. **Footers (角标)** — every web-sourced exhibit needs a capture stamp and its source URL.
   Downloaded report/white-paper PDFs legitimately have none; letters and agreements never do.
4. **AI markers** — no captured URL may carry `source=chatgpt`, `utm_source=chatgpt.com`,
   or any similar AI-tool attribution. Re-capture from the clean canonical URL.

Also flag junk pages for removal (ad blocks, related-news lists, site footers, blank
lazy-load placeholders) — but keep author/editor attribution, which is provenance, not junk.

Report everything, then get confirmation before deleting evidence pages. Removing a page is
not reversible from the client's point of view.

---

## Step 2 — Collect the SIGNED forms

Forms live in the case drive's own folder — named `表格` or `Forms`, often numbered like
`13_表格 Forms (I-129)`. What matters is filing the *signed* version, and the folder holds both.

- **Unsigned drafts are named for it**: `i-129-waiting signature.pdf`,
  `g-28-waiting signature.pdf`. Never file these.
- **Signed forms come back as scanner output** — `FedEx Scan <date>_<time>.pdf` or similar.
  They have no text layer, are landscape (792×612 pt) because of how the scanner feeds, and
  the first page often comes in rotated 90°. Straighten the rotation before merging.
- A signed form may not be in the forms folder at all. Scans get dropped wherever the person
  scanning them was working. Search the case drive by page count and date before concluding a
  form is missing.

Because the scans carry no text, identify each form and confirm each signature **by rendering
the page and looking**. Where the signatures live:

| Form | Signature |
|---|---|
| I-129 | Part 7 (petitioner/authorized signatory), and again in the O/P Supplement's Section 2 |
| G-28 | Part 4 (client) and Part 5 (attorney) |
| I-907 | signature block on the last substantive page |
| G-1650 | one per fee, each its own single-page form |

Two things the checklist wants that are easy to miss:

- **The I-129 scan usually contains all 38 pages**, including the E-1/E-2, Trade Agreement, H,
  Q-1 and R-1 supplements that do not apply. The O-1 checklist says to print only **P1-8 and
  P28-30** (the main form plus the O and P Classifications Supplement). Filing the unused
  supplements is not fatal but it is not what the checklist asks for.
- **G-1650 amounts depend on the petitioner's size.** The small-entity case is $530 base +
  $300 asylum program; a petitioner with more than 25 US employees pays $1,055 + $600. Premium
  processing is $2,965 on its own form. Read the employee count off I-129 Part 5 and confirm
  the prepared forms match, rather than assuming whichever set is sitting in the folder.

## Step 3 — Report the findings and wait for confirmation

**Stop here and confirm before merging anything.** This is a gate, not a status update.

Everything downstream — cover pages, merge, split, upload — is built on the set of documents
you are about to combine. If a form turns out to be the unsigned draft, or a criterion is
missing an exhibit, or a page has to come out, fixing it after the merge means redoing every
later step. And the pages you would delete are evidence: that call is the attorney's, not
yours.

Report, in one message:

- what the checklist requires and what is missing
- which forms were found, which are signed, and where each signature was verified
- exhibits with no source-URL footer, and any AI-tool marker found
- missing translations, and any certificate item describing material that is not there
- pages proposed for deletion, with the reason for each
- anything you could not resolve

Then wait. Merge only once the attorney has confirmed, and note anything they told you to
leave alone so a later pass does not "fix" it again.

## Step 4 — Convert everything to PDF

The folder will mix `.pdf`, `.docx`, `.pptx` and images. `references/conversion.md` has the
route for each, and the traps — several of them fail *silently* and produce a PDF with the
wrong content, so verify every conversion by comparing text against the source.

---

## Step 5 — Build cover pages and merge

Filing order:

```
forms  →  identity documents  →  petition letter  →  index of exhibit  →  exhibits
```

Every exhibit and every exhibit section sits behind its own cover page, whose text is the
matching line from the INDEX OF EXHIBIT verbatim — so the index and the package cannot drift
apart. `scripts/cover.py` reproduces the firm's cover-page geometry exactly (Times New Roman
Bold 22 pt, US Letter, 1-inch margins, first baseline at y=340 pt, 36 pt line pitch).

Within an exhibit, each **English translation comes first, immediately followed by the
original it renders** — one-to-one, so an adjudicator never has to hunt for the pair.
`scripts/order.py` derives that ordering from the firm's filename suffixes.

---

## Step 6 — Split into the submission set

The split plan depends on the case type:

- **O-1** → read `references/o1.md`
- **EB-1A** → read `references/eb1a.md`

Shared rules:

- **11,920,000 bytes** per file. USCIS enforces 12 MB; this leaves headroom for the small
  size drift a re-save introduces.
- **At most 15 PDFs.** If the material cannot fit in 15 at a quality where captures stay
  legible, stop and ask rather than compressing until text turns to mush.
- **Never end a file on a cover page** — a cover orphaned from the evidence it introduces
  reads as a missing exhibit. And never emit a file that is only cover pages.
- Filenames use only letters, digits, space and `_ - . ( )`. USCIS rejects anything else.

Use `scripts/split_package.py`, which measures every candidate file and repairs oversized ones
instead of trusting an estimate. Size estimates from per-page image bytes run low by around
10% on image-heavy sections, which is exactly where the cap bites.

---

## Step 7 — Verify, then upload to Drive

Before handing anything over, confirm:

- **Page conservation** — pages across the split set plus any separately-filed document
  equals the merged master. This is the check that catches a dropped exhibit.
- Every file at or under the byte cap, filenames clean, bookmarks present.
- Every URL in a footer resolves and matches its exhibit.

Then create a folder named **`电子提交拆分`** inside the client's PL folder (`0.PL`) and upload
the complete set there — the split files, any separately-filed document, the identity-documents
PDF, the signed forms, and `00 CONTENTS.txt`.

If a `电子提交拆分` already exists — a re-split of a case that was filed once before, or work
someone else started — do not create a second one beside it. Upload into the existing folder
and trash whatever it holds that the new set supersedes, so nobody files last week's split by
mistake. Two folders with similar names is how the wrong version gets filed.

Creating the folder and uploading:

```
gws drive files create --params '{"supportsAllDrives":true}' \
  --json '{"name":"电子提交拆分","mimeType":"application/vnd.google-apps.folder","parents":["<0.PL folder id>"]}'

gws drive files create --params '{"supportsAllDrives":true,"uploadType":"multipart"}' \
  --json '{"name":"<file>","mimeType":"application/pdf","parents":["<folder id>"]}' --upload "<file>"
```

Run uploads with `cwd` set to the folder holding the files and pass a bare `--upload` filename;
`gws` rejects paths outside the current directory. Uploads of a 900-page package take minutes —
run them detached so a shell timeout cannot kill the transfer half-way, and **verify afterwards
by comparing names and byte sizes**. A partial upload looks identical to a complete one in the
Drive UI, which is how half a package gets filed.

Report to the attorney: file list with sizes and page counts, what the audit found, what was
removed and why, the Drive link, and anything still unresolved.

## Naming

```
<Client> - Exhibits <n> of <N> (<first exhibit> to <last exhibit>).pdf
<Client> - Exhibit <n> <Name> Letter.pdf          # separately-filed document
<Client> - Petition Letter and Index of Exhibit.pdf
<Client> - Identity Documents.pdf
```

Where the petition letter and index lead the first file, say so in its label. Write a
`00 CONTENTS.txt` beside the set listing each file with its size, page count and the exhibits
inside — the attorney checks the filing against that, not by opening five PDFs.

---

## References

- `references/preflight.md` — the four audits, with scripts and judgement calls
- `references/conversion.md` — file → PDF routes and the silent-failure traps
- `references/o1.md` — O-1 split plan
- `references/eb1a.md` — EB-1A split plan
- `references/annotation.md` — optional highlighting of what the letter relies on
