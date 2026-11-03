# Preflight audit

Four checks, all run before anything is merged. Each one exists because skipping it has cost a
rebuild of the whole package.

---

## 1. Checklist

Fetch the case type's checklist (IDs in SKILL.md Step 0) and work through it. The O-1
checklist is a filing-review document, not just a document list — it covers fees, then each
form with named field checks (G-1650, G-28, I-907, G-1145, I-129 with per-page questions),
then package-level items: passport/visa/I-94/consultation letter present, index of exhibits
checked, translation certificate checked, correct pronoun, correct name, media articles having
a named author rather than "editor".

Separately, walk the petition letter's own criterion arguments. The letter is the real
specification: if it argues five criteria, all five need exhibits, and every exhibit number it
cites must exist. Extract citations directly:

```python
re.findall(r'Exhibit\s+(\d+(?:-\d+)*)', petition_letter_text)
```

An exhibit cited by the letter but absent from the index is the highest-severity finding —
it means the letter promises evidence the adjudicator will not find. Report the exhibit
number, where the letter cites it, and what the folder actually holds.

---

## 2. Translations

Chinese-language evidence needs an English rendering, and the Translation Certificate must
list every translated item. Run `scripts/audit_translations.py <EXHIBITS_ROOT>`, which flags:

- exhibits whose only content is CJK with no English sibling
- translations present in the folder but absent from the certificate's numbered list
- certificate items describing material no longer in the package (over-description is as
  much a defect as omission — the translator is attesting to documents that are not there)

Two things the text scan alone will miss:

- **Image-only exhibits.** A screenshot carries Chinese no text extraction will find.
  Enumerate `.png/.jpg/.jpeg` separately and look at them.
- **Natively-English sources that look untranslated** — e.g. a government registry page with
  an official English version. That is not a translation and belongs in a different
  certificate note.

---

## 3. Footers (角标)

A web-sourced exhibit should carry the browser's print header/footer: capture timestamp, page
title, source URL, page N of M. That footer is the provenance — without it there is nothing
tying the pages to a URL the adjudicator can check.

```
scripts/audit_footers.py <EXHIBITS_ROOT>
```

It classifies each PDF and reports which web captures lack a stamp or URL. Interpreting the
output takes judgement:

- **Letters, agreements, forms, signed recommendations** — never have footers. Correct as-is.
- **Downloaded report / white-paper PDFs** (often slide-shaped, e.g. 720×540) — distributed as
  files, not captured from a page. No footer expected; publisher branding on the document is
  the provenance.
- **Browser prints** (US Letter with many outbound links) — these *should* have a footer. A
  missing one means the capture was made with headers/footers switched off.

To fix, re-capture from the canonical URL:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --window-size=1600,2400 --virtual-time-budget=40000 \
  --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36" \
  --print-to-pdf=out.pdf "<URL>"
```

Chrome's default header/footer matches the firm's existing captures (date + title on top, URL
at the bottom), so re-captures sit consistently beside older exhibits.

**Recovering the URL** when the exhibit does not show one, in order of reliability:

1. The **English translation** of that exhibit — the firm's translations preserve the capture
   stamp and URL, so the URL is usually sitting right there.
2. **Share links inside the PDF's own annotations** — QZone/Weibo share buttons embed the
   canonical article URL as a `url=` parameter. Unquote and extract it.
3. The client's `材料清单`, which records source links for press and publication exhibits.
4. Web search on the exact headline. Verify the returned page carries the same load-bearing
   figures as the exhibit before trusting it.

**Verify before swapping.** Compare the new capture against the old one on the facts that
matter — the headline, the byline, and the specific figures the petition letter cites — not on
whole-page text overlap. Ad blocks, view counters and related-news rails change constantly, so
a genuine re-capture of the same article can score under 40% whole-page similarity while being
word-for-word identical in the body. Judge on the facts, then swap.

Two failure modes worth knowing:

- Some sites set `@page { margin: 0 }` in print CSS, which suppresses Chrome's header/footer
  entirely. Stamping the footer yourself is defensible **only** with the real capture time and
  the verified URL, in the same visual style — and say so in the report, because it differs
  from a browser-generated footer.
- Lazy-loaded page tails come out blank. If the article body is short of the original, raise
  `--virtual-time-budget` and re-capture before concluding the content is gone.

Re-capturing sometimes recovers content the original capture truncated. Compare page counts
both ways and mention any exhibit that gained body pages — an article filed at 4 pages that is
really 10 was missing most of its substance.

---

## 4. AI markers

A URL captured after following an AI-generated link keeps the referrer parameter, and it is
visible in the footer of the filed exhibit. Filing evidence stamped `source=chatgpt` tells the
adjudicator how the research was done.

`scripts/audit_footers.py` flags: `source=chatgpt`, `utm_source=chatgpt.com`,
`utm_source=openai`, `source=perplexity`, `ref=claude`, `utm_source=copilot`, `oai_`,
and any `utm_*` naming an AI product.

The fix is not to edit the footer text — that leaves a URL that no longer matches what was
captured. Strip the parameters from the URL, re-capture from the clean canonical address, and
verify the content matches.

---

## Junk pages

Web captures drag in material that is not evidence. Run `scripts/junk_pages.py <PDF>` and
review what it proposes; it classifies on body text (excluding the footer band), image
payload, and ink coverage.

Safe to remove — none of it is evidence:

- related-news and recommended-story rails, whose items are unrelated to the exhibit
- site footers, nav columns, cookie notices, newsletter and contest promos
- blank pages left by lazy-loaded content
- advertising blocks and trending-ticker strips

**Keep** anything carrying provenance or substance:

- author and editor attribution, publication cards, "Written by", 记者/编辑/来源 lines —
  the user specifically wants these preserved
- the closing paragraph of an article, which often sits on a page that is mostly comments
- data figures, even when the page is otherwise sparse

The classifier is a proposal, not a decision. Print the full body text of every page it wants
to drop and confirm none is article body before removing anything.
