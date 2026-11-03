---
name: "skye-translate"
description: "Translate Chinese-language exhibit materials into English for a Lingtu Law / SIA 高徒 immigration filing, file them into the client's evidence package with the firm's naming and certification conventions, and mark the passages the petition letter relies on using Word comments (.docx) or PDF highlight-plus-popup annotations (.pdf). Covers auditing an exhibit package for untranslated Chinese, verifying that source captures are not truncated before translating, re-capturing defective web-page PDFs, translating literally per the firm's translation instructions, cross-checking every translated figure against what the petition letter asserts, and syncing everything to the case folder in Google Drive. Use whenever asked to translate exhibits or evidence, find what still needs translation, add translation certificates, or annotate/highlight the parts of the evidence that support the petition letter."
---

# Exhibit Translation & Annotation (Lingtu Law / SIA 高徒)

Two jobs that always travel together: get every Chinese-language exhibit into English,
and make it obvious to the reviewing officer which sentence in the exhibit supports
which sentence in the petition letter.

Use `gws` (CLI) for all Drive operations, never the web UI. Never invoke `gws` from a
stripped environment — it deletes its own credentials.

---

## The firm's own translation rules

These come from `翻译指示.pdf`, which the firm gives clients. They govern everything below:

- **a. 直译内容（不增加，不改动，不删减）** — literal translation. No additions, no
  alterations, no omissions.
- **b. 格式对齐** — preserve the layout: headers, breadcrumbs, bylines, tables, footers,
  licence numbers, page-capture stamps and URLs.
- **c. 翻译认证** — every translation needs a certificate. USCIS only requires that the
  translator attest bilingual competence and that the translation is complete and
  accurate, then sign with contact details. Template is page 2 of `翻译指示.pdf`.

The instructions also say materials have **already been trimmed to the minimum needed**
for evidentiary effect. That authorizes translating only the relevant pages of a long
document (e.g. one category out of a 9-page award list) — but state the excerpt scope,
and only when the client agrees.

### ⛔ Never add explanatory matter of your own

This firm wants the translation and nothing else. Do not append **any** of the following,
even though each feels helpful:

- a closing scope note — `Scope of this translation: …`, `This is a complete translation
  of the article text. The captured pages also carry the site's masthead navigation …`
- a capture line of your own invention — `[Capture stamp] Retrieved August 2026`
- any *italicised* remark about what was or was not reproduced, why a page was excerpted,
  how names were romanized, or what the source's character set is
- a bracketed translator's note of any kind, unless the client asks for one

Position labels **inside** the body stay (`[Photo caption]`, `[Chart]`, `[Page footer]`,
`[Top right]`) — those mark where text sits on the source and are part of format
alignment. So do the source's own printed artefacts: its print timestamp, its page
numbers, its URL, its footer.

The test is simple: **if the text is not on the source, it does not go in the file.** If
something genuinely needs saying — an excerpt boundary, a competing translation, a figure
that does not match the letter — say it in the Word comment (Step 5) or in the report to
the attorney, never in the translation itself. This was corrected twice; do not
reintroduce it.

---

## Step 0 — Audit the package before translating anything

Walk the whole evidence tree and classify every file. A file needs translation if it
contains Chinese and has no English counterpart in the same folder.

```
scripts/audit_translations.py <EXHIBITS_ROOT>
```

Two things the audit must not miss:

- **Image-only exhibits.** Screenshots (`.png/.jpg`) carry Chinese that no text scan
  will find. Enumerate them separately and open them to look.
- **Natively-English files that only look untranslated.** e.g. an NPPA registry page has
  an official English version — that is not a translation and needs a different note on
  the certificate.
- **Translations that do not say "translation" in the filename.** This is the audit's
  worst failure mode. The firm names many translations after their *content*, not their
  role: `Beijing Daily Group.docx`, `YNET.com.docx`, `From wandering to running.docx`,
  `7-4-1 Budget Approval - New Year Shopping Festival (Dec 3 2020).docx` are all
  translations. Pairing on a `translation|translated|English|译文` filename regex reports
  a dozen false gaps and sends you translating things that are already done.

  **Pair on the language of the content, not the name.** Extract the text, count CJK
  characters, and treat a folder as covered when it holds both a CJK-heavy file and an
  English file:

  ```python
  cjk = len(re.findall(r'[一-鿿㐀-䶿]', text))
  lang = 'ZH' if cjk >= 60 else ('EN' if len(text.strip()) >= 200 else 'SCAN')
  ```

  Two traps in that count: read only the body parts of a `.docx`/`.pptx`
  (`word/document.xml`, `ppt/slides/*.xml`) — whole-archive XML picks up Chinese from
  metadata and misreports an all-English translation as Chinese; and `SCAN` (image-only
  PDF, no text layer) means *unknown*, not *untranslated* — open it and look before
  reporting it.

Also check for **duplicate files by MD5**. Packages accumulate the same screenshot under
two names; translating both is waste and filing both looks careless.

---

## Step 1 — Verify the source is intact BEFORE translating

**This is the step that actually matters.** Web-page PDFs printed at a narrow window
lose the left margin, and the loss is in the image, not just the text layer. Translating
from a truncated capture produces invented characters.

Symptoms: body lines start mid-word — `家获悉` for `36氪独家获悉`, `城拍客` for
`京城拍客`, `闻奖是中国晚报界的最高奖项` for `赵超构新闻奖是…`.

```
scripts/check_truncation.py <file.pdf>      # flags suspicious line starts
```

Fix by re-capturing wide:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --window-size=1600,2400 --virtual-time-budget=35000 \
  --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36" \
  --print-to-pdf=out.pdf "<URL>"
```

Then replace the exhibit and verify the previously-missing characters are present.

**If the text layer is garbled rather than truncated** (custom fonts — 改革网 does this:
`砌任美国纳断达克上市鸽埠电商企业`), do not guess. Render the page to an image and read
it visually:

```
scripts/render_pages.py <file.pdf> <out_dir> [--zoom 3.4]
```

Sites that block automated capture entirely (Barron's, MarketWatch, Salary.com,
Glassdoor when logged out) cannot be captured. Say so and either find a substitute
source or ask the client to capture it from a logged-in session — never cite a source
that will not be in the binder.

---

## Step 2 — Translate in the house format

Learned from the firm's existing translations (`4-1 Article/01 - English Translation.docx`,
`7-4-1 Budget Approval…docx`, `7-1b Certified Translation.docx`):

- Plain `.docx`, Times New Roman 12 pt, 1-inch margins. No bilingual columns.
- **News articles:** centred bold title → `Source: X　Author: Y　Date: Z` → body paragraphs.
  Keep the site nav/breadcrumb, the "Related reading" list, the editor credit, the
  copyright and licence footer, and the capture stamp + URL.
- **Emails:** reproduce the client chrome (From / To / Cc / Time / Attachment / "This
  message has been replied to") as its own lines, then the body.
- **Screenshots and dashboards:** transcribe the on-screen text under bracketed position
  labels (`[Status bar]`, `[Top right]`, `[Backdrop behind the team]`). This is a
  transcription, not prose — say so to the certifying translator.
- **Award lists / tables:** rebuild as a real Word table with the source's column
  headings translated, one row per entry, all author and editor names romanized.
- **Optional:** the outlet's logo, cropped from the source PDF, small, top-left. Not
  required. Extract with `render_pages.py` using a tight clip rect.
- Money: keep the source unit and add nothing — `RMB 3.5 trillion`, `RMB150,000`.
- Names: romanize (康泽宇 → Kang Zeyu). Follow the source's own order; if the source
  writes 陶郁倩 as "Tao Yuqian", keep "Tao Yuqian" inside quotation marks even if the
  petition letter uses "Yuqian Tao" elsewhere.
- Licence numbers, ICP filings and serial publication numbers are often the whole point
  of a background exhibit. Always translate them.

---

## Step 3 — Cross-check every figure against the petition letter

Translating is also the last practical audit of the letter. As each figure is rendered,
compare it with what the letter asserts. Report every mismatch; do not silently
reconcile.

Real examples from the Yuqian Tao O-1A:

| Letter said | Source actually said |
|---|---|
| mobile matrix "more than 400 million users", "over 100 million daily visits" | **320 million** users; no daily-visit figure at all |
| "62 products 'Amazon's Choice' and five '#1 Best Seller'" | "numerous products" — **no counts exist** in any SEC filing |
| Glassdoor 90th percentile presented as met | 90th percentile is **above** the contracted rate |
| "ten in the 2020 cycle" (I had called this unsourced) | **correct** — the client had the source; verify before declaring a gap |

Also flag **competing translations of the same document**. If two versions exist with
different wording, the letter's block quotes must match whichever one is certified — and
only one may be filed. Never edit text inside a quotation to fit; change the letter, or
have the translator reissue.

---

## Step 4 — File with the package's naming convention

Translation sits next to its original, sharing the original's exhibit number:

```
5-4-6a Cooperation Confirmation Email (original).png
5-4-6  Cooperation Confirmation Email — Maybelline Grand Opening with Hua Chenyu (English translation).docx

4-2-3 Awards/01 - All-China Journalists Association — 35th China News Award…pdf
4-2-3 Awards/4-2-3 English Translation — 01 All-China Journalists Association…docx

7-3a Douyin … Training Materials (original).pdf
7-3b English Translation — Douyin … Training Materials.docx
```

Suffix pattern: bare number or `a` = original, `b`/`c`/`d` = translation or additional
captures of the same item. When an original is missing but a translation exists, look in
the client's own Drive `翻译材料` folder — the originals are usually all there.

Keep a `00 - SOURCES TO CAPTURE.md` per exhibit group recording, for each fact the letter
asserts: the fact, the file that proves it, and status ✓ / ○ / ✗. Record deliberate
exclusions and *why*, so a later reader does not reinstate a claim that was removed for
lack of a source.

---

## Step 5 — Annotate: mark what the letter relies on

Do **not** use yellow highlighting — the firm wants comments, so the note travels with
the passage and can be replied to or resolved.

Comment text format, uniform across both file types:

```
Petition letter, Criterion #5 (original contribution)-First — quoted: "<the letter's own words>"
```

Add `NOTE:` inside the comment where the evidence does not support the letter, or where
the exhibit carries something adverse on the same page. Those notes are the most valuable
output of this step. Real ones worth copying:

- `NOTE: the letter states 400 million users; the source supports 320 million.`
- `NOTE: the same article describes the raise as "tepid", 66% below target, following a
  52% reduction in deal size, and refers to a dispute with Boustead Securities.`
- `NOTE: Mr. August is the Petitioner's own Founder and CEO, not an independent third party.`

**.docx → real Word comments:**

```
scripts/wcomment.py     # annotate(path, [(substring, comment), …])
```
Paragraph-level anchoring (substring match anywhere in the paragraph comments the whole
paragraph) is more robust than run-level, because generated documents split runs
unpredictably. It also strips any pre-existing highlight.

⚠️ **Merge, don't overwrite.** If the file already has `word/comments.xml` (recommender
letters often carry drafting comments), read it, keep those comments, and give yours
fresh non-colliding `w:id`s. Overwriting destroys the firm's own review notes — this
happened once to `5-1 Charles Hu` and had to be recovered from the duplicate zip entry.

**.pdf → highlight plus popup:**

```
scripts/pdfann.py       # annotate_pdf(path, [(search_text, comment), …])
```
Searches for the phrase, highlights it, attaches the note as the annotation's content,
and falls back to a page-1 sticky note if the phrase cannot be located. Author is set to
`Lingtu Law Office` so the annotations can be found and cleared as a set.

`.pptx` cannot take either mechanism — note the relevant content in an accompanying
document instead.

---

## Step 6 — Sync and reconcile with Drive

Mirror the local tree to the case folder in Drive. Before overwriting, **diff both
directions** — the client edits Drive directly, and their version is often the newer,
better one:

```
scripts/drive_diff.py <EXHIBITS_ROOT> <DRIVE_FOLDER_ID>
```

What this has surfaced in practice: the client had already added the Blanket L I-797, the
executed offers, a Glassdoor capture and a replacement certified translation; and had
renumbered Exhibit 8 to match the letter while the local copy still had the old scheme.
Align to whichever side matches the current petition letter, and say which you chose.

### gws path and mimeType rules — both fail silently

**Every gws path must be inside the working directory, in both directions.** This governs
`--upload` *and* `-o/--out`. Run with `cwd=EXHIBITS_ROOT` and pass relative paths. An
absolute path outside cwd does not error usefully — it just writes nothing, and a bulk
sync reports every single file as failed while telling you nothing about why. That is
what a 41-file download failure looked like.

**Uploading a docx needs the mimeType in the same call**, or Drive records the file as
`multipart/related` and neither Google Docs nor Word will open it — the bytes are fine,
the file is simply unopenable, and the upload reports success:

```
gws drive files update \
  --params '{"fileId":"<ID>","supportsAllDrives":true,"uploadType":"multipart"}' \
  --json '{"mimeType":"application/vnd.openxmlformats-officedocument.wordprocessingml.document","name":"<exact name>"}' \
  --upload out.docx
```

`--upload-content-type` alone does not fix it, and neither does a metadata-only PATCH
afterwards. Verify after every upload: re-`get` with `fields=mimeType,size,version`, then
download with `alt=media` and open it. Pass `supportsAllDrives: true` on every call.

### Filenames must survive the USCIS upload portal

The portal accepts **English letters, numbers, `_`, `-`, `.`, `()` and spaces — nothing
else.** Rejected: commas, curly quotes (`’`), em dashes (`—`), `|`, `▷`, and any Chinese
characters. It rejects the whole file with "Your file has an invalid name."

Name files this way from the start; retrofitting a package means renaming a hundred files.
Check the set before handing anything over:

```python
re.match(r'^[A-Za-z0-9_\-.() ]+$', filename)
```

---

## Finish by reporting

- what was translated, and what was already covered
- every source-integrity defect found and how it was fixed
- **every mismatch between an exhibit and the petition letter** — this is the part the
  attorney needs
- what still has no translation certificate (all of them, until a translator signs)
