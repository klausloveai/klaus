# Optional: marking what the petition letter relies on

Not part of every filing — do it when asked to highlight the evidence, or when the attorney
wants to see the letter tied to the exhibits. The firm's convention is a highlight **plus an
attached note**, so the note travels with the passage. All highlights are the same yellow
(`RGB 1.0 / 0.92 / 0.23`); author is `Lingtu Law Office` so the set can be found and cleared
together.

Three passes, each answering a different question:

1. **Asserted facts** — for each `Exhibit N` citation in the letter, highlight the passage in
   that exhibit which carries the assertion.
2. **Hard data points** — every figure the letter leans on: traffic, rankings, GMV, salary,
   award grade. These are what an adjudicator checks.
3. **Verbatim quotes** — passages the letter quotes word-for-word from a recommendation
   letter, so the reader can confirm the quote is real.

Note format:

```
Petition letter, Criterion #5 (original contribution) - Exhibit 5-1 - quoted: "<the letter's own words>"
```

Add a `NOTE:` line where the evidence does not actually support the letter, or where the same
page carries something adverse. Those notes are the most valuable output of the pass.

## What makes this work

**Scope every search to that exhibit's own page range.** A phrase like "TikTok Shop" appears
all over the package; unscoped search lands the highlight on an unrelated exhibit.

**Exclude cover pages from the search.** Cover text is the index wording, which is nearly
identical to the letter's wording, so cover pages win every match and the highlight lands on a
heading instead of the evidence. This is the single most common way this pass goes wrong.

**Take figure lists from a citation window, not a sentence.** Splitting the letter into
sentences on `.;:` truncates enumerated claims — `[Exhibit 4-2-2] Licensed News Credentials
and Readership:` becomes the whole "sentence" and every figure after the colon is lost. Take
the text from each citation up to the next one instead.

**Try the forms a source actually prints.** The letter formats figures its own way. Generate
variants: `US$43 billion` → `$43 billion` → `43 billion` → `43`; `34.4 million` → `34.4M`;
strip commas. Sources abbreviate where the letter spells out.

**Match quotes on word sequences, not raw string search.** Long quotes wrap across lines and
carry bracketed alterations like `complet[ed]`. Normalise to a word list, then find the
longest contiguous run on the page (≥75% of the quote's words) and build the highlight from
those words' rectangles.

**Leave contracts unmarked.** Executed agreements and award agreements are read as instruments;
highlighting inside them is not wanted.

Where an exhibit has no text layer — a scanned or image-only PDF — nothing can be highlighted.
Attach a page-level note instead, and flag the exhibit for OCR: an adjudicator cannot search
it either.
