"""Exhibit cover-page generator.
Style reverse-engineered from 'Qing Yang - Exhibits (2nd Submission).pdf':
  US Letter 612x792pt; Times New Roman Bold 22pt; left margin 72pt;
  wrap width 468pt; first line bbox-top y=320.4 (baseline 340.0); line pitch 36pt.
"""
import fitz
FONTFILE="/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
PAGE_W, PAGE_H = 612.0, 792.0
MARGIN_L = 72.0
WRAP_W   = 468.0
SIZE     = 22.0
PITCH    = 36.0
FIRST_BASELINE = 340.0          # = 320.4 + ascender(0.891*22)
_font = fitz.Font(fontfile=FONTFILE)

def wrap(text, size=SIZE, width=WRAP_W):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = w if not cur else cur+" "+w
        if _font.text_length(trial, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def make_cover(text, doc=None):
    """Append one cover page carrying `text` to `doc` (or a new doc)."""
    doc = fitz.open() if doc is None else doc   # NB: an empty Document is falsy
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_font(fontname="TNRB", fontfile=FONTFILE)
    y = FIRST_BASELINE
    for line in wrap(text):
        page.insert_text((MARGIN_L, y), line, fontname="TNRB", fontsize=SIZE)
        y += PITCH
    return doc
