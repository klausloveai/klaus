#!/usr/bin/env python3
"""
fill_inplace_pos.py — Complete a POS that is ALREADY EMBEDDED in an attorney-drafted
pleading, instead of appending the firm template POS.

Usage:
    python3 fill_inplace_pos.py <outdir> <file.pdf> [file2.pdf ...]

Use this when Hernán (or any attorney) drafted the Proof of Service INTO the pleading
with the blanks left open, e.g.:

    On ______________________, 2026, I served the foregoing document described as ...
    Executed on ______________________, 2026, at City of Industry, California.
    ______________________________          <- declarant signature rule
    Name: ______________________

Appending the firm template POS to such a document would give it TWO proofs of service,
and would also discard any case-specific recital the attorney wrote into his own POS
(e.g. "pursuant to the Consent to Electronic Service ... served by Defendant on
August 31, 2026" — CRC 2.251(b)(1)(B)). Fill in place instead.

What it fills, per document:
  * both date blanks  -> today, as "Month D" (the ", 2026" is already in the template text)
  * Name: blank       -> the declarant
  * signature rule    -> Klaus's signature PNG, taken from the firm POS template in Drive

The signature lives inside the firm POS template as word/media/image1.png
(template file id 1yHMojbfNpE_C6aeZ30Td7qXypwLp0sok). This script extracts it on the fly,
so there is one source of truth for the signature and it stays in step with the template.

Judicial Council forms (DISC-001, DISC-002, ...) cannot take an appended page. Their POS
belongs in the companion attachment document, and that POS must name the form by its full
title in the "documents served" recital. Do not try to stamp the form itself.

Requires: pymupdf, python-docx-free (zipfile only), gws on PATH.
"""
import fitz, sys, os, io, json, zipfile, subprocess, datetime

TEMPLATE_ID = "1yHMojbfNpE_C6aeZ30Td7qXypwLp0sok"
DECLARANT   = "Klaus Liu"
FONT, SIZE  = "tiro", 12          # Times — matches firm pleading paper
SIG_W       = 115.0               # pt on the page

DATE_PATTERNS = ("On ______________________, 2026, I served",
                 "Executed on ______________________, 2026")
NAME_PATTERN  = "Name: ______________________"
RULE_PATTERN  = "______________________________"


def signature_png(workdir):
    """Pull the firm POS template from Drive and extract the embedded signature."""
    docx = os.path.join(workdir, "_pos_template.docx")
    subprocess.run(["gws", "drive", "files", "get", "--params",
                    json.dumps({"fileId": TEMPLATE_ID, "alt": "media",
                                "supportsAllDrives": True}), "-o", docx],
                   capture_output=True, cwd=workdir)
    if not os.path.exists(docx):
        raise SystemExit("could not fetch the POS template from Drive — check the file id")
    with zipfile.ZipFile(docx) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
        if not media:
            raise SystemExit("no signature image in the POS template — ask Klaus to add it")
        png = os.path.join(workdir, "_sig.png")
        with open(png, "wb") as fh:
            fh.write(z.read(media[0]))
    os.remove(docx)
    return png


def fill(path, outdir, sig_png, date_str, declarant=DECLARANT):
    d = fitz.open(path)
    filled = signed = 0
    with fitz.open(sig_png) as s:
        aspect = s[0].rect.height / s[0].rect.width
    for pg in d:
        for pat, val in [(p, date_str) for p in DATE_PATTERNS] + [(NAME_PATTERN, declarant)]:
            for r in pg.search_for(pat):
                clip = fitz.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2)
                for u in pg.search_for("______________________", clip=clip):
                    w = fitz.get_text_length(val, fontname=FONT, fontsize=SIZE)
                    x = u.x0 + max(2, ((u.x1 - u.x0) - w) / 2)
                    pg.insert_text((x, u.y1 - 3.2), val, fontname=FONT,
                                   fontsize=SIZE, color=(0, 0, 0))
                    filled += 1
        # the signature rule is the long underscore run sitting just ABOVE a "Name:" line
        for nm in pg.search_for(NAME_PATTERN):
            for rule in pg.search_for(RULE_PATTERN):
                if 8 < (nm.y0 - rule.y0) < 40:
                    h = SIG_W * aspect
                    box = fitz.Rect(rule.x0 + 18, rule.y1 - 2 - h,
                                    rule.x0 + 18 + SIG_W, rule.y1 - 2)
                    pg.insert_image(box, filename=sig_png, overlay=True)
                    signed += 1
    out = os.path.join(outdir, os.path.basename(path))
    d.save(out)
    d.close()
    return out, filled, signed


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    outdir, srcs = sys.argv[1], sys.argv[2:]
    os.makedirs(outdir, exist_ok=True)
    sig = signature_png(outdir)
    date_str = datetime.date.today().strftime("%B %-d")
    for src in srcs:
        out, n, s = fill(src, outdir, sig, date_str)
        tag = f"filled {n}, signed {s}" if n else "no embedded POS — skipped"
        print(f"  {tag:28s} {os.path.basename(out)}")
    os.remove(sig)
    print(f"\nServe date used: {date_str}, {datetime.date.today().year}")
    print("Spot-check one signature page before serving.")


if __name__ == "__main__":
    main()
