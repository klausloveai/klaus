#!/usr/bin/env python3
"""Propose ad / blank / site-furniture pages for removal from a web-capture PDF.

    python junk_pages.py <PDF> [--show]

Prints a keep/drop proposal. This is a PROPOSAL: --show prints the full body text of every
page it wants to drop so you can confirm none is article body before removing anything.
Attribution pages (Written by, 记者, 编辑, 来源) are always kept - they are provenance.
"""
import sys, re

ATTR = re.compile(r'Written by|Published in|More from|followers'
                  r'|Editor|编辑|记者|作者|来源[:：]', re.I)

def body_text(pg):
    """Page text minus the print header/footer bands, which every page repeats."""
    import fitz
    r = pg.rect
    t = pg.get_textbox(fitz.Rect(0, 30, r.width, r.height - 26))
    t = re.sub(r'\d{1,2}/\d{1,2}/\d{2},?\s*\d{1,2}:\d{2}\s*[AP]M.*?(?=\n|$)', '', t)
    t = re.sub(r'https?://\S+', '', t)
    return re.sub(r'\s+', ' ', t).strip()

def classify(path):
    import fitz
    d = fitz.open(path)
    rows = []
    for i in range(d.page_count):
        pg = d[i]
        t = body_text(pg)
        nch = len(re.sub(r'\s+', '', t))
        img = sum(len(d.extract_image(x[0])["image"]) for x in pg.get_images(full=True)) / 1e6
        if nch >= 300:      keep, why = True,  "text"
        elif img >= 0.35:   keep, why = True,  "image"
        elif ATTR.search(t) and nch >= 30:
                            keep, why = True,  "attribution"
        else:               keep, why = False, "ad / footer / blank"
        rows.append((i + 1, keep, why, nch, img, t))
    d.close()
    return rows

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    rows = classify(sys.argv[1])
    show = "--show" in sys.argv
    keep = [p for p, k, *_ in rows if k]
    print(f"{'pg':>3} {'chars':>6} {'imgMB':>6}  verdict")
    for p, k, why, nch, img, _ in rows:
        print(f"{p:3} {nch:6} {img:6.2f}  {'KEEP  ' if k else 'drop  '}({why})")
    print(f"\nkeep {len(keep)}/{len(rows)}: {keep}")
    if show:
        print("\n=== full body text of pages proposed for removal ===")
        for p, k, why, nch, img, t in rows:
            if not k:
                print(f"\n--- p{p} ---\n{t[:600]}")
