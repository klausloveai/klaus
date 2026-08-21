#!/usr/bin/env python3
"""
make_doe_amendment.py — draft a CIV 105 (DOE amendment) + First Amended Summons
for a Lingtu Law / Law Office of Shenqi Cai (Hernán Simó) litigation case.

Usage:  python3 make_doe_amendment.py <config.json>

Produces two flattened, sign-ready PDFs in <output_dir>:
  - "<prefix> - CIV 105 Amendment to Complaint (DOE ... true name).pdf"
  - "<prefix> - First Amended Summons (DOE ... true name).pdf"

Draft/prep only. Leaves DATE + SIGNATURE blank for the attorney; leaves the
summons DATE/Clerk blank for the court to issue. Never files.

Why overlay instead of AcroForm fill: the CIV 105 and SUM-100 AcroForm fonts
mangle accents (é/ó -> ?) and drop checkbox marks when flattened by qpdf. So we
flatten a clean base first, then draw every value with an embedded Unicode TTF at
the exact field coordinates. Field rects for both forms are hard-coded below and
were mapped from the official/firm templates (identical SUM-100 layout).
"""
import sys, os, io, json, subprocess, tempfile
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, ArrayObject

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")

# Embed a Unicode font so accented names (Hernán S. Simó) always render.
_ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
_ARIALB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
pdfmetrics.registerFont(TTFont("Body", _ARIAL))
pdfmetrics.registerFont(TTFont("BodyB", _ARIALB))


def _qpdf(args):
    subprocess.run(["qpdf"] + args, check=True, capture_output=True)


def _wrap(text, font, size, max_w):
    """Greedy word-wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- CIV 105 ----
def make_civ105(cfg, out_path):
    at = cfg["attorney"]
    plaintiff = cfg["plaintiff"]
    branch = cfg.get("court_branch_note", "")
    courthouse_line = cfg["court_address"] + (f" — {branch} ({cfg['court_name']})" if branch else f" ({cfg['court_name']})")

    blank = os.path.join(ASSETS, "CIV105_blank.pdf")
    with tempfile.TemporaryDirectory() as td:
        flat = os.path.join(td, "civ_flat.pdf")
        _qpdf(["--flatten-annotations=all", blank, flat])

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(612, 792))

        def line(x, y, t, s=9, f="Body"):
            c.setFont(f, s); c.drawString(x, y, t)

        # A01 attorney name + address (multiline box y680.2..738.8, x36..288.5)
        addr = [at["name"], at["firm"], at["addr1"], at["addr2"]]
        yy = 728.8
        for l in addr:
            line(38, yy, l, 8.5); yy -= 11
        line(290, 714.5, at["sbn"], 9)                       # A02 State Bar No
        line(103, 670.5, at["tel"], 9)                       # A03 telephone
        line(311, 670.5, at.get("fax", ""), 9)               # A04 fax
        line(138, 661.0, at["email"], 9)                     # A05 email
        line(126, 651.5, "Plaintiff " + plaintiff, 9)        # A06 attorney for
        line(38, 609.0, courthouse_line, 8)                  # A07 courthouse addr
        line(38, 582.5, plaintiff, 9)                        # A08 plaintiff
        line(38, 555.6, cfg["complaint_defendant_caption"], 9)  # A09 defendant (pre-amendment)
        line(426, 526.0, cfg["case_number"], 9)              # A10 case number
        c.setFont("BodyB", 12); c.drawString(37.0, 505.2, "X")  # A11 FICTITIOUS box
        line(38, 450.5, cfg["doe_number"], 9)                # A12 fictitious name
        line(38, 404.0, cfg["true_name"], 9)                 # A13 true name
        line(139, 357.8, at["name"], 9)                      # A15 type/print name
        # DATE (A14) + SIGNATURE (A16) intentionally left blank for the attorney.
        c.showPage(); c.save(); buf.seek(0)

        base = PdfReader(flat); ov = PdfReader(buf)
        w = PdfWriter(); pg = base.pages[0]; pg.merge_page(ov.pages[0]); w.add_page(pg)
        with open(out_path, "wb") as fh:
            w.write(fh)


# ------------------------------------------------- First Amended Summons ----
# The SUM-100 "name and address of the court" block has only TWO usable line
# slots, and BOTH must stop before the CASE NUMBER box (its left edge is x=362.8
# on the template). Overflowing prints the court name straight through the case
# number — mapped from the issued Yi Cong summons, 2026-08-20.
COURT_SLOTS = [
    # (x, baseline_y, max_right)  — slot 1 sits beside the Spanish label
    (190.8, 292.0, 358.0),
    (36.1, 276.0, 358.0),
]
ATTY_SLOT = (36.5, 236.0, 570.0)   # attorney line may run the full box width


def extract_summons_court_block(pdf_path):
    """Read the court block + attorney line VERBATIM off an already-issued
    summons, so an amended summons repeats exactly what the court accepted.
    Returns {"court_lines": [...], "attorney_line": str or None}, or None if the
    file can't be parsed. Requires pdfplumber; degrades gracefully without it."""
    try:
        import pdfplumber
    except ImportError:
        return None
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            words = page.extract_words()
    except Exception:
        return None

    # Group words into visual lines by their baseline.
    rows = {}
    for w in words:
        rows.setdefault(round(w["bottom"]), []).append(w)

    court_lines, attorney_line = [], None
    for bottom in sorted(rows):
        ws = sorted(rows[bottom], key=lambda w: w["x0"])
        text = " ".join(w["text"] for w in ws)
        # Court slot 1: same row as the Spanish label, value starts after it.
        if "corte es)" in text:
            tail = [w["text"] for w in ws if w["x0"] > 188]
            if tail:
                court_lines.append(" ".join(tail))
        # Court slot 2: the row just below, left margin, left of the case-number box.
        elif 500 < bottom < 522 and ws[0]["x0"] < 60 and ws[-1]["x1"] < 362.8:
            court_lines.append(text)
        # Attorney line: the row below the plaintiff's-attorney label.
        elif 550 < bottom < 562 and ws[0]["x0"] < 60:
            attorney_line = text

    if not court_lines:
        return None
    return {"court_lines": court_lines[:2], "attorney_line": attorney_line}


def _draw_fitted(c, x, y, text, max_right, size=9, font="Body", min_size=6.5):
    """Draw text at (x, y), shrinking the font until it ends before max_right.
    Returns the size actually used. Never lets a value run into the next box."""
    avail = max_right - x
    s = size
    while s > min_size and pdfmetrics.stringWidth(text, font, s) > avail:
        s -= 0.25
    c.setFont(font, s)
    c.drawString(x, y, text)
    return s


def _layout_court_lines(cfg):
    """Decide the court block's lines, in priority order:
    1. cfg['court_lines'] — explicit verbatim override
    2. cfg['issued_summons_pdf'] — scraped verbatim off the issued summons
    3. cfg['court_name'] / cfg['court_address'] — composed, then width-wrapped
    Klaus's rule (2026-08-20): if the case already has an issued summons, repeat
    its court block verbatim; otherwise keep it inside the box and wrap."""
    if cfg.get("court_lines"):
        return list(cfg["court_lines"])[:2], "config"

    issued = cfg.get("issued_summons_pdf")
    if issued and os.path.exists(os.path.expanduser(issued)):
        got = extract_summons_court_block(os.path.expanduser(issued))
        if got and got["court_lines"]:
            return got["court_lines"], "issued summons"

    # Fallback: fill slot 1 then slot 2, wrapping on word boundaries.
    full = f"{cfg['court_name']}, {cfg['court_address']}"
    words, lines, cur = full.split(), [], ""
    slot = 0
    for wd in words:
        trial = (cur + " " + wd).strip()
        x, _, right = COURT_SLOTS[min(slot, len(COURT_SLOTS) - 1)]
        if pdfmetrics.stringWidth(trial, "Body", 9) <= (right - x) or not cur:
            cur = trial
        else:
            lines.append(cur); cur = wd; slot += 1
            if slot >= len(COURT_SLOTS):
                break
    if cur:
        lines.append(cur)
    return lines[:2], "composed"


def _strip_fa_template(src, dst):
    """Remove widget annotations + AcroForm so the firm template's pre-filled
    values (court/attorney from a prior case) drop away, keeping the static
    'FIRST AMENDED SUMMONS' heading + all printed labels/borders."""
    r = PdfReader(src); w = PdfWriter(); w.append(r)
    pg = w.pages[0]
    annots = pg.get("/Annots")
    if annots:
        keep = [a for a in annots if a.get_object().get("/Subtype") != "/Widget"]
        pg[NameObject("/Annots")] = ArrayObject(keep)
    if "/AcroForm" in w._root_object:
        del w._root_object["/AcroForm"]
    with open(dst, "wb") as f:
        w.write(f)


def make_fa_summons(cfg, out_path):
    at = cfg["attorney"]
    tmpl = os.path.join(ASSETS, "FA-Summons-template.pdf")
    court_lines, court_src = _layout_court_lines(cfg)
    # Attorney line: verbatim off the issued summons when we have one, so the
    # amended summons matches what the court already accepted.
    attorney_line = cfg.get("summons_attorney_line")
    if not attorney_line and cfg.get("issued_summons_pdf"):
        got = extract_summons_court_block(os.path.expanduser(cfg["issued_summons_pdf"]))
        if got and got.get("attorney_line"):
            attorney_line = got["attorney_line"]
    if not attorney_line:
        attorney_line = (
            f"{at['name']} (SBN {at['sbn']}), {at['firm']}, {at['addr1']}, {at['addr2']}, {at['tel']}"
        )
    print(f"  court block ({court_src}): " + " | ".join(court_lines))
    with tempfile.TemporaryDirectory() as td:
        stripped = os.path.join(td, "fa_stripped.pdf")
        flat = os.path.join(td, "fa_flat.pdf")
        _strip_fa_template(tmpl, stripped)
        _qpdf(["--flatten-annotations=all", stripped, flat])

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(612, 792))

        def line(x, y, t, s=9, f="Body"):
            c.setFont(f, s); c.drawString(x, y, t)

        # NOTICE TO DEFENDANT (FillText25 box y651.7..673.6, x36..431 -> usable ~388w)
        deflines = _wrap(cfg["summons_defendant_caption"], "Body", 9, 388)
        if len(deflines) == 1:
            line(41, 660, deflines[0], 9)
        else:
            y = 665
            for l in deflines[:2]:
                line(41, y, l, 9); y -= 11
        line(41, 604, cfg["plaintiff"], 10)                  # FillText180 plaintiff
        # Court block — each line width-guarded so it can never bleed into the
        # CASE NUMBER box at x=362.8.
        for text, (cx, cy, cright) in zip(court_lines, COURT_SLOTS):
            _draw_fitted(c, cx, cy, text, cright, size=9)
        line(369, 288, cfg["case_number"], 10)               # CaseNumber
        ax, ay, aright = ATTY_SLOT
        _draw_fitted(c, ax, ay, attorney_line, aright, size=8)   # FillText30 attorney
        c.setFont("BodyB", 11); c.drawString(190.2, 150.0, "X")  # item 2 checkbox
        line(212, 140.0, cfg["doe_number"], 10)              # item 2 specify (fictitious name)
        # DATE / Clerk / Deputy left blank -> court issues.
        c.showPage(); c.save(); buf.seek(0)

        base = PdfReader(flat); ov = PdfReader(buf)
        w = PdfWriter(); pg = base.pages[0]; pg.merge_page(ov.pages[0]); w.add_page(pg)
        with open(out_path, "wb") as fh:
            w.write(fh)


def main():
    if len(sys.argv) != 2:
        print("usage: make_doe_amendment.py <config.json>", file=sys.stderr); sys.exit(2)
    cfg = json.load(open(sys.argv[1]))
    out_dir = os.path.expanduser(cfg["output_dir"])
    os.makedirs(out_dir, exist_ok=True)
    prefix = cfg["file_prefix"]
    tag = f"{cfg['doe_number']} {cfg['true_name']}"

    civ = os.path.join(out_dir, f"{prefix} - CIV 105 Amendment to Complaint ({tag}).pdf")
    summ = os.path.join(out_dir, f"{prefix} - First Amended Summons ({tag}).pdf")
    make_civ105(cfg, civ)
    make_fa_summons(cfg, summ)
    print("CIV105:", civ)
    print("SUMMONS:", summ)


if __name__ == "__main__":
    main()
