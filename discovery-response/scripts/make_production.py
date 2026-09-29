# -*- coding: utf-8 -*-
"""Assemble and Bates-stamp Plaintiff YI CONG's document production, Set One.

Documents are produced AS RECEIVED (provider fax cover sheets included) so no
completeness objection can be made about cherry-picking pages.

Bates prefix: CONG 000001-. The one video is produced natively and carries a
Bates-style exhibit number rather than a stamp.

NOT produced, deliberately -- see the memo:
  * 4:12-5:12.pdf     -> photos of two PRE-incident prescriptions (3/13/2026
                          Amoxicillin, 4/3/2026 Mupirocin). Not treatment for
                          this incident; needs an attorney call, and it bears on
                          FROG 2.13 / 6.5 / 10.1 and RFP 4.
  * Treatment.jpg      -> client's WeChat message to this office (privileged).
  * 9-15-2026 lien form-> our own completed Machinify claim form (work product).
  * 7-29-2026 statement-> client statement taken by counsel (work product; see
                          RFP 13 response).
"""
import io, os, subprocess, sys
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
pdfmetrics.registerFont(TTFont("Body", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("BodyB", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))


# ---------------------------------------------------------------- per-case input
# Fill DOCS and NATIVE for the case, then run. Produce documents AS RECEIVED --
# provider fax covers included -- so no completeness objection can be made.
# (source file in src/, description for the index, "responsive to request nos.")
DOCS = [
    # ("driver-license.jpg", "California Driver License No. ...", "1"),
]
NATIVE = [
    # ("clip.mov", "Video of ... (produced in native format)", "12", "CONG-VIDEO-0001"),
]
PREFIX = "CONG "   # per-case Bates prefix


def img_to_pdf(path, out):
    """Wrap an image on a letter page, preserving aspect ratio."""
    img = ImageReader(path)
    iw, ih = img.getSize()
    PW, PH = 612.0, 792.0
    m = 36.0
    s = min((PW - 2 * m) / iw, (PH - 2 * m) / ih)
    w, h = iw * s, ih * s
    c = canvas.Canvas(out, pagesize=(PW, PH))
    c.drawImage(img, (PW - w) / 2, (PH - h) / 2, w, h, preserveAspectRatio=True)
    c.showPage(); c.save()
    return out


def stamp(page, label):
    """Bates stamp in a clear strip at the foot of the page.

    The page content is scaled 96% and pushed up first, so the stamp never sits
    on top of anything the producing party did not put there -- overlaying a
    knockout box was clipping the Ontario Fire report's own footer.
    """
    from pypdf import Transformation
    box = page.mediabox
    w = float(box.width); h = float(box.height)
    strip = 26.0
    s = (h - strip) / h
    page.add_transformation(Transformation().scale(s, s).translate(0, strip))

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    c.setFont("BodyB", 9)
    tw = c.stringWidth(label, "BodyB", 9)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(w - 24 - tw, 9, label)
    c.showPage(); c.save(); buf.seek(0)
    page.merge_page(PdfReader(buf).pages[0])
    return page


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(HERE, "tmp"); os.makedirs(tmp, exist_ok=True)

    writer = PdfWriter()
    n = 0
    index = []
    for fn, desc, resp in DOCS:
        path = os.path.join(SRC, fn)
        if not os.path.exists(path):
            sys.exit(f"MISSING SOURCE: {path}")
        if fn.lower().endswith((".jpg", ".jpeg", ".png")):
            path = img_to_pdf(path, os.path.join(tmp, fn + ".pdf"))
        rd = PdfReader(path)
        first = n + 1
        for pg in rd.pages:
            n += 1
            writer.add_page(stamp(pg, f"{PREFIX}{n:06d}"))
        index.append((f"{PREFIX}{first:06d} – {PREFIX}{n:06d}" if n > first
                      else f"{PREFIX}{first:06d}", desc, resp, n - first + 1))

    combined = os.path.join(out_dir, "Yi Cong - Production Set One (CONG 000001-%06d).pdf" % n)
    with open(combined, "wb") as fh:
        writer.write(fh)
    print("PRODUCTION:", combined, "—", n, "pages")
    return combined, index, n


if __name__ == "__main__":
    combined, index, n = main(sys.argv[1])
    import json
    json.dump({"index": index, "total": n, "native": NATIVE},
              open(os.path.join(HERE, "index.json"), "w"), ensure_ascii=False, indent=1)
    for b, d, r, c in index:
        print(f"  {b:28s} ({c:2d}p)  RFP {r:12s}  {d[:70]}")
