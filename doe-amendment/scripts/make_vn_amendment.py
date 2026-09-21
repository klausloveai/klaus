#!/usr/bin/env python3
"""
make_vn_amendment.py — Ventura County DOE amendment package:
  * VN004 "Amendment to Complaint" (FICTITIOUS NAME — no order required)  +
  * First Amended Summons (SUM-100) with the CCP §474 fictitious-name endorsement

Ventura County Superior Court uses its own local optional form **VN004** for a
Doe/fictitious-name amendment — not the LA CIV 105 (make_doe_amendment.py) and not
San Bernardino's SB-16778 (make_sb_amendment.py). Use this for Ventura cases; the
case-number prefix looks like `2026CUPO069898` (CUPO = Civil Unlimited PersOnal injury).

VN004 carries BOTH halves on one page: the top FICTITIOUS NAME block (no order) and a
bottom INCORRECT NAME block plus an ORDER for a judge. A Doe amendment uses the TOP
block only; the bottom block and the ORDER are left completely blank.

TEMPLATE SOURCE: pulled fresh at run time from the court's own site so a form revision
flows through automatically —
    https://ventura.courts.ca.gov/system/files/vn004.pdf
falling back to the bundled cache assets/VN004_blank.pdf.

Draft-only: the "Attorney(s) for Plaintiff(s)" signature line is left BLANK (Hernán
signs), and the summons DATE / Clerk / Deputy are left blank (the clerk issues it).
Never e-files, never serves.

Usage:  python3 make_vn_amendment.py <config.json>

Config schema — `defendants` is a LIST so one run can add several Does:
{
  "output_dir": "/Users/klaus/Downloads/Bo Tao - DOE Amendment",
  "file_prefix": "Bo Tao",
  "case_number": "2026CUPO069898",
  "plaintiff": "BO TAO",
  "attorney": {
    "name": "Hernán S. Simó", "sbn": "354175",
    "firm": "Law Office of Shenqi Cai APC",
    "addr1": "13191 Crossroads Pkwy N, Suite 295",
    "addr2": "City of Industry, CA 91746",
    "tel": "(626) 479-2207", "fax": "(626) 479-2207",
    "email": "hernan.s@lingtulaw.com"
  },
  "court_name": "Ventura County Superior Court",
  "court_address": "800 S. Victoria Ave., Ventura, CA 93009",
  "complaint_defendant_caption": "EUTIMEO BEAS; RACHEL R. BEAS; BECKY BEAS; and DOES 1 through 20, inclusive",
  "summons_defendant_caption": "EUTIMEO BEAS; RACHEL R. BEAS; BECKY BEAS; RALPH BEAS; and DOES 1 through 20, inclusive",
  "issued_summons_pdf": "/path/to/1. Summons  on Complaint.pdf",
  "limited_civil": false,
  "defendants": [{"doe_number": "DOE 1", "true_name": "RALPH BEAS"}]
}

Note `limited_civil`: VN004 has a "Limited Civil Case" checkbox next to the court name.
Leave it false for an unlimited case (CUPO). Only tick it for a limited civil matter.
"""
import sys, os, io, json, subprocess, tempfile, urllib.request
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, HERE)
import make_doe_amendment as mda          # reuse the tested First Amended Summons generator

pdfmetrics.registerFont(TTFont("Body", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("BodyB", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

VN004_URL = "https://ventura.courts.ca.gov/system/files/vn004.pdf"
VN004_CACHE = os.path.join(ASSETS, "VN004_blank.pdf")


def fetch_vn004_blank(dest):
    """Court site first so form revisions flow through; bundled cache as fallback."""
    try:
        req = urllib.request.Request(VN004_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        if data[:4] != b"%PDF":
            raise ValueError("not a PDF")
        with open(dest, "wb") as fh:
            fh.write(data)
        return f"court site ({VN004_URL})"
    except Exception as e:
        if not os.path.exists(VN004_CACHE):
            raise SystemExit(f"could not fetch VN004 ({e}) and no cache at {VN004_CACHE}")
        with open(VN004_CACHE, "rb") as s, open(dest, "wb") as fh:
            fh.write(s.read())
        return f"bundled cache (court site failed: {e})"


def _draw_caption(c, x, y_single, y1, y2, right, text, size=8.0, font="Body"):
    """Draw a defendant caption inside a one-or-two-line form cell.
    Keeps the single-line baseline when the caption fits there; otherwise wraps
    onto the two baselines, preferring a break after one of the caption's own
    semicolons, and only shrinks the type if no break works."""
    avail = right - x
    if pdfmetrics.stringWidth(text, font, size) <= avail:
        c.setFont(font, size); c.drawString(x, y_single, text); return size

    def split(sz):
        semis = [i + 1 for i, ch in enumerate(text) if ch == ";"]
        spaces = [i for i, ch in enumerate(text) if ch == " "]
        for pts in (semis, spaces):
            best = None
            for i in pts:
                a, b = text[:i].strip(), text[i:].strip()
                if (pdfmetrics.stringWidth(a, font, sz) <= avail
                        and pdfmetrics.stringWidth(b, font, sz) <= avail):
                    best = (a, b)      # last workable break → fullest line 1
            if best:
                return best
        return None

    sz = size
    while sz > 5.5:
        got = split(sz)
        if got:
            c.setFont(font, sz)
            c.drawString(x, y1, got[0]); c.drawString(x, y2, got[1])
            return sz
        sz -= 0.25
    # Last resort: one shrunken line beats a caption running out of the box.
    return mda._draw_fitted(c, x, y_single, text, right, size=size, min_size=5.0)


def make_vn004(cfg, doe_number, true_name, blank, out_path):
    """Overlay values onto a flattened VN004. Coordinates are reportlab (origin
    bottom-left); they were measured off the form's own ruled blanks, so the values
    sit ON the lines rather than floating."""
    at = cfg["attorney"]
    with tempfile.TemporaryDirectory() as td:
        flat = os.path.join(td, "flat.pdf")
        subprocess.run(["qpdf", "--flatten-annotations=all", blank, flat],
                       check=True, capture_output=True)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(612, 792))

        def L(x, y, t, s=8.5, f="Body"):
            c.setFont(f, s); c.drawString(x, y, t)

        # ── Attorney / party box (top-left) ──────────────────────────────────
        L(38, 734, f"{at['name']} (SBN {at['sbn']})")
        L(38, 724, at["firm"])
        L(38, 714, at["addr1"], 8)
        L(38, 704, at["addr2"], 8)
        L(38, 694, f"Email: {at['email']}", 7.5)
        L(320, 734, at["tel"])                                   # Telephone Number
        L(320, 724, f"Fax: {at['fax']}", 7.5)
        # ── Attorney For (Name) ──────────────────────────────────────────────
        L(115, 676, f"Plaintiff {cfg['plaintiff']}")
        # ── Courthouse location checkbox — MUST be marked ───────────────────
        # The blank's own widget is named "800 SOUTH VICTORIA AVE VENTURA CA
        # 93009": it is Ventura's location selector, not decoration. Drawn box
        # measures [55.4, 145.6, 65.9, 156.0] top-down; centre the X in it.
        c.setFont("BodyB", 8); c.drawString(57.8, 638.5, "X")
        # ── Limited Civil Case checkbox (leave clear for unlimited) ──────────
        if cfg.get("limited_civil"):
            # Drawn box [310.5, 126.1, 318.6, 134.2] top-down.
            c.setFont("BodyB", 8); c.drawString(311.6, 660.0, "X")
        # ── Parties ──────────────────────────────────────────────────────────
        L(148, 610, cfg["plaintiff"], 9)                         # PLAINTIFF/PETITIONER
        # DEFENDANT/RESPONDENT: the cell is only ~231pt wide (x 162 → the
        # vertical rule at 396.2). A full dog-bite caption needs 5.5pt to fit
        # on one line, which prints unreadably; wrap onto the cell's two
        # baselines instead (rule below sits at y=209.9 top-down).
        _draw_caption(c, 162, 590, 594.5, 585.5, 393,
                      cfg["complaint_defendant_caption"])
        # ── Case number (inside the ruled cell y552..582, x396..581) ─────────
        L(405, 556, cfg["case_number"], 9.5)
        # ── FICTITIOUS NAME block — the only part a Doe amendment fills ──────
        L(270, 484, doe_number, 10)                              # fictitious name of:
        L(274, 449, true_name, 10)                               # true name to be:
        # Attorney(s) for Plaintiff(s) signature line: intentionally BLANK
        # INCORRECT NAME block + ORDER: intentionally BLANK
        c.showPage(); c.save(); buf.seek(0)

        base = PdfReader(flat); ov = PdfReader(buf)
        w = PdfWriter(); pg = base.pages[0]; pg.merge_page(ov.pages[0]); w.add_page(pg)
        with open(out_path, "wb") as fh:
            w.write(fh)


def main():
    if len(sys.argv) != 2:
        print("usage: make_vn_amendment.py <config.json>", file=sys.stderr); sys.exit(2)
    cfg = json.load(open(sys.argv[1]))
    out_dir = os.path.expanduser(cfg["output_dir"]); os.makedirs(out_dir, exist_ok=True)
    prefix = cfg["file_prefix"]

    with tempfile.TemporaryDirectory() as td:
        blank = os.path.join(td, "vn004.pdf")
        print(f"VN004 blank source: {fetch_vn004_blank(blank)}")
        for d in cfg["defendants"]:
            tag = f"{d['doe_number']} {d['true_name']}"
            vn = os.path.join(out_dir, f"{prefix} - VN004 Amendment to Complaint ({tag}).pdf")
            su = os.path.join(out_dir, f"{prefix} - First Amended Summons ({tag}).pdf")
            make_vn004(cfg, d["doe_number"], d["true_name"], blank, vn)
            scfg = dict(cfg); scfg["doe_number"] = d["doe_number"]; scfg["true_name"] = d["true_name"]
            mda.make_fa_summons(scfg, su)
            print("VN004   :", vn)
            print("SUMMONS :", su)
    print("DONE")


if __name__ == "__main__":
    main()
