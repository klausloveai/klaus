#!/usr/bin/env python3
"""Render an RFE PDF into contact sheets so the notice can be page-mapped.

Usage:  python3 rfe_pages.py rfe.pdf [outdir] [--per N]

RFE notices arrive as scans with no text layer, so `See RFE at p. N` citations
can only be written after looking at the pages. This renders 4 pages per sheet
with the page number stamped on each, which is legible enough to spot section
headings. Read the sheets, write down which section starts on which page, and
keep that map beside you for the rest of the job.

Requires PyMuPDF and Pillow (both already present on the firm Mac).
"""
import sys, os
import fitz
from PIL import Image, ImageDraw

def main():
    pdf = sys.argv[1]
    args = [a for a in sys.argv[2:] if not a.startswith('--')]
    outdir = args[0] if args else 'rfe_sheets'
    per = 4
    if '--per' in sys.argv:
        per = int(sys.argv[sys.argv.index('--per') + 1])
    cols = 2 if per <= 4 else 5
    rows = (per + cols - 1) // cols
    TH = (760, 1000) if per <= 4 else (420, 545)

    os.makedirs(outdir, exist_ok=True)
    doc = fitz.open(pdf)
    print('pages:', doc.page_count)
    made = []
    for start in range(0, doc.page_count, per):
        chunk = range(start, min(start + per, doc.page_count))
        sheet = Image.new('RGB', (cols * TH[0], rows * TH[1]), 'white')
        dr = ImageDraw.Draw(sheet)
        for k, pno in enumerate(chunk):
            pm = doc[pno].get_pixmap(dpi=110)
            im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
            im.thumbnail(TH)
            x, y = (k % cols) * TH[0], (k // cols) * TH[1]
            sheet.paste(im, (x, y))
            dr.rectangle([x, y, x + TH[0] - 2, y + TH[1] - 2], outline='red', width=3)
            dr.text((x + 10, y + 6), 'PAGE %d' % (pno + 1), fill='red')
        fn = os.path.join(outdir, 'sheet_%02d-%02d.png' % (start + 1, list(chunk)[-1] + 1))
        sheet.save(fn)
        made.append(fn)
        print(' ', fn)
    print('\nNow read each sheet and write down the page map before drafting.')
    return made

if __name__ == '__main__':
    main()
