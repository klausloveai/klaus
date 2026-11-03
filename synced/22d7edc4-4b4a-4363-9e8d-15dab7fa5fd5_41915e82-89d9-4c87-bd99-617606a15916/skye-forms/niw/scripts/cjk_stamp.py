#!/usr/bin/env python3
"""Stamp Chinese (CJK) text into USCIS AcroForm boxes.

Why this exists: the I-140's text fields carry a Helvetica /DA, which has no CJK
glyphs. Writing 杨 through `forms.py fill` stores the right value but the
generated appearance stream renders every character as `?` — verified by render.
Acrobat would regenerate the appearance with a substituted font, but Preview.app
and poppler (what we use to read the form back) will not, so what the user prints
is `?`.

So for the fields that must hold Chinese — I-140 page 3, printed items 4.a–4.c
(native-alphabet name) and 5.a–5.g (native-alphabet address) — we draw the text
onto the page instead, positioned on the field's own rect, using reportlab's
built-in `STSong-Light` CID font (no font file needed).

    $PY scripts/cjk_stamp.py out/i-140.pdf cjk-values.json --out out/i-140.pdf

`cjk-values.json` is the same {field_name: text} shape `fill` takes. Run it
AFTER `fill`, on the filled PDF.

Two consequences to know and to report:

- The stamped text is page content, not a form value. The field itself is left
  empty on purpose — setting it too would draw `?` on top of the stamp.
- It is therefore not editable in Acrobat like the other answers. If a value
  needs changing, re-run fill + stamp rather than typing over it.

Everything that is not Chinese belongs in `forms.py fill`, not here.
"""

import argparse
import json
import os
import sys


# The glyphs have to be EMBEDDED. reportlab's built-in STSong-Light CID font
# produces a PDF that references a non-embedded CJK font: Acrobat substitutes and
# it looks fine, but poppler (our read-back renderer) draws nothing at all — an
# invisible answer that reads as a blank box. So embed a real TrueType instead.
# Verified: Songti.ttc renders correctly through pdftoppm.
CJK_FONTS = [
    ("/System/Library/Fonts/Supplemental/Songti.ttc", 0),
    ("/System/Library/Fonts/STHeiti Light.ttc", 0),
    ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
    ("/Library/Fonts/Arial Unicode.ttf", 0),
]


def _register_font(pdfmetrics, TTFont):
    for path, idx in CJK_FONTS:
        if not os.path.exists(path):
            continue
        try:
            pdfmetrics.registerFont(TTFont("CJK", path, subfontIndex=idx))
            print(f"embedding {os.path.basename(path)}")
            return "CJK"
        except Exception as e:
            print(f"  skipped {path}: {e.__class__.__name__}")
    raise SystemExit(
        "No embeddable CJK font found. Do NOT fall back to a non-embedded CID font —\n"
        "it renders blank in poppler and cannot be read back."
    )


def _fq(annot):
    from pypdf.generic import IndirectObject

    parts, cur, guard = [], annot, 0
    while cur is not None and guard < 30:
        t = cur.get("/T")
        if t is not None:
            parts.append(str(t))
        cur = cur.get("/Parent")
        if isinstance(cur, IndirectObject):
            cur = cur.get_object()
        guard += 1
    return ".".join(reversed(parts))


def _annots(page):
    a = page.get("/Annots")
    return list(a.get_object()) if a else []


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf")
    ap.add_argument("values", help="JSON {field_name: chinese_text}")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=float, default=10.0, help="max font size (pt)")
    args = ap.parse_args()

    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas

    with open(args.values) as fh:
        values = {k: v for k, v in json.load(fh).items() if str(v).strip()}

    reader = PdfReader(args.pdf)
    writer = PdfWriter(clone_from=reader)

    # Locate each target field by name and remember page + rect.
    targets = {}   # page_index -> [(rect, text)]
    found = set()
    for i, page in enumerate(writer.pages):
        for ref in _annots(page):
            an = ref.get_object()
            if an.get("/Subtype") != "/Widget":
                continue
            name = _fq(an)
            if name in values:
                rect = [float(x) for x in an.get("/Rect")]
                targets.setdefault(i, []).append((rect, str(values[name])))
                found.add(name)
                # Clear the field so pypdf's `?` appearance never competes with
                # the stamp. An empty field under stamped text is deliberate.
                for key in ("/V", "/AP"):
                    if key in an:
                        del an[key]

    missing = [k for k in values if k not in found]

    font = _register_font(pdfmetrics, TTFont)
    tmp = args.out + ".overlay.pdf"
    first = writer.pages[0]
    W = float(first.mediabox.width)
    H = float(first.mediabox.height)
    c = canvas.Canvas(tmp, pagesize=(W, H))
    for i in range(len(writer.pages)):
        for rect, text in targets.get(i, []):
            x0, y0, x1, y1 = rect
            box_w = (x1 - x0) - 4
            size = args.size
            while size > 5 and pdfmetrics.stringWidth(text, font, size) > box_w:
                size -= 0.5
            c.setFont(font, size)
            # Baseline: centre the glyph box vertically in the field rect.
            c.drawString(x0 + 2, y0 + ((y1 - y0) - size) / 2 + size * 0.22, text)
        c.showPage()
    c.save()

    overlay = PdfReader(tmp)
    for i, page in enumerate(writer.pages):
        if targets.get(i):
            page.merge_page(overlay.pages[i])

    with open(args.out, "wb") as fh:
        writer.write(fh)
    os.remove(tmp)

    print(f"stamped {len(found)} of {len(values)} fields into {args.out}")
    if missing:
        print("\nNOT STAMPED — no widget carries these names on any page:")
        for k in missing:
            print("  -", k)
        return 1
    print("Now render those pages and read the characters back — a wrong glyph is silent.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
