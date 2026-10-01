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
import sys, os, io, json, re, subprocess, tempfile
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

    # Drop the e-filing stamp. Courts print a vertical "transmitted through
    # eFiling" band OUTSIDE the form's left margin (SUM-100 body starts at
    # x=36.0); pdfplumber reads it as one-or-two-character words at x0~24 that
    # otherwise land inside the court-block row window and win over the real
    # value. Ventura's copy produced court_lines == ["S", "a"] this way.
    words = [w for w in words if w["x0"] >= 34]

    # Group words into visual lines by their baseline.
    rows = {}
    for w in words:
        rows.setdefault(round(w["bottom"]), []).append(w)

    def row_text(bottom):
        return " ".join(w["text"] for w in sorted(rows[bottom], key=lambda w: w["x0"]))

    # Anchor on the two labels rather than on absolute y windows: the forms are
    # the same but each court's e-filed copy shifts the values by a few points.
    court_label = next((b for b in sorted(rows) if "corte es)" in row_text(b)), None)
    atty_label = next((b for b in sorted(rows)
                       if "abogado del demandante" in row_text(b)), None)
    if court_label is None:
        return None
    # Boundary = the END OF THE LABEL TEXT, not the end of the row. When a court
    # sets the value on the label's own baseline (San Bernardino), the value
    # words are in this row too, and taking max(x1) would swallow them.
    label_right = max(
        [w["x1"] for w in rows[court_label] if "es)" in w["text"]]
        or [max(w["x1"] for w in rows[court_label])]
    )

    # Court slot 1 = the value to the RIGHT of the label. Some courts set it on
    # the label's own baseline (San Bernardino), others a couple of points
    # below it (Ventura: label 501, value 503) — accept either.
    slot1 = []
    for b in sorted(rows):
        if abs(b - court_label) <= 6:
            slot1 += [w for w in sorted(rows[b], key=lambda w: w["x0"])
                      if w["x0"] > label_right]
    # Court slot 2 = the next left-margin row below, stopping before the
    # CASE NUMBER box (x=362.8).
    slot2 = None
    for b in sorted(rows):
        if court_label + 6 < b <= court_label + 30:
            ws = sorted(rows[b], key=lambda w: w["x0"])
            if ws[0]["x0"] < 60 and ws[-1]["x1"] < 362.8:
                slot2 = " ".join(w["text"] for w in ws)
                break

    court_lines = []
    if slot1:
        court_lines.append(" ".join(w["text"] for w in slot1))
    if slot2:
        court_lines.append(slot2)

    # Attorney line = the first left-margin row below its Spanish label.
    attorney_line = None
    if atty_label is not None:
        for b in sorted(rows):
            if atty_label < b <= atty_label + 20:
                ws = sorted(rows[b], key=lambda w: w["x0"])
                if ws[0]["x0"] < 60:
                    attorney_line = " ".join(w["text"] for w in ws)
                    break

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


# ---- Summons ordinal -------------------------------------------------------
# The ordinal tracks the SUMMONS, not the amendment. Original summons issued
# with the complaint; the first Doe amendment gets a FIRST Amended Summons; the
# second Doe amendment gets a SECOND Amended Summons, and so on. (The CIV 105 /
# SB-16778 / VN004 amendment itself carries NO ordinal — each is standalone.)
#
# Hernán's template has "FIRST AMENDED SUMMONS" as STATIC page content, so any
# other ordinal must be painted over. Measured off the template (2026-09-30):
# heading occupies PDF y 736.3..746.4, x 92.6..284.2 -> centre x 188.4,
# baseline 736.3, Arial-Bold 14 (width 192.1 vs the template's 191.5).
# Hernán added "FIRST AMENDED" to the template as a SEPARATE text block drawn
# with the embedded CID font /C2_0 at 14pt, `91.637 736.237 Td`, in the LAST
# content stream — the form's own `(SUMMONS  )Tj` sits at x=212.42 on the same
# baseline. So the heading is really two pieces: Hernán's "FIRST AMENDED" plus
# the stock "SUMMONS".
#
# Do NOT paint over it: a white rectangle hides it visually but leaves "FIRST
# AMENDED" in the text layer, so pdftotext (and the court's own extraction)
# still reads FIRST on a SECOND amended summons. Delete the block instead, then
# redraw the ordinal right-aligned against the stock SUMMONS.
HEADING_BASELINE = 736.237
HEADING_SIZE = 14
HEADING_RIGHT = 209.5          # end "<ORD> AMENDED" just left of SUMMONS (x=212.42)

_ORDINALS = {1: "FIRST", 2: "SECOND", 3: "THIRD", 4: "FOURTH", 5: "FIFTH",
             6: "SIXTH", 7: "SEVENTH", 8: "EIGHTH", 9: "NINTH", 10: "TENTH"}


def summons_ordinal(cfg):
    """Return the ordinal word for this summons, upper-case. Accepts
    summons_ordinal as a word ("SECOND") or a number (2). Defaults to FIRST."""
    raw = cfg.get("summons_ordinal", "FIRST")
    if isinstance(raw, int):
        return _ORDINALS.get(raw, _ORDINALS[1])
    raw = str(raw).strip().upper()
    if raw.isdigit():
        return _ORDINALS.get(int(raw), _ORDINALS[1])
    return raw or "FIRST"


def _drop_template_heading(pdf_path):
    """Delete Hernán's 'FIRST AMENDED' text block from the page content so it
    cannot survive in the text layer. Matches the BT..ET block that uses the
    /C2_0 CID font on the heading baseline. Returns True if something was cut."""
    r = PdfReader(pdf_path); w = PdfWriter(); w.append(r)
    pg = w.pages[0]
    arr = pg.get("/Contents")
    streams = arr if isinstance(arr, ArrayObject) else [arr]
    cut = False
    for ref in streams:
        obj = ref.get_object()
        data = obj.get_data().decode("latin-1")
        out, pos = [], 0
        for m in re.finditer(r"BT\b.*?\bET", data, re.S):
            blk = m.group(0)
            if "/C2_0" not in blk:
                continue
            td = re.search(r"([-\d.]+)\s+([-\d.]+)\s+T[dDm]", blk)
            if td and 730.0 <= float(td.group(2)) <= 742.0:
                out.append(data[pos:m.start()]); pos = m.end(); cut = True
        if cut and pos:
            out.append(data[pos:])
            obj.set_data("".join(out).encode("latin-1"))
            break
    if cut:
        with open(pdf_path, "wb") as fh:
            w.write(fh)
    return cut


def _redraw_heading(c, ordinal):
    """Set '<ORDINAL> AMENDED' right-aligned so it reads straight into the
    template's own 'SUMMONS'. The old block is deleted, not covered."""
    c.setFillColorRGB(0, 0, 0)
    c.setFont("BodyB", HEADING_SIZE)
    c.drawRightString(HEADING_RIGHT, HEADING_BASELINE, f"{ordinal} AMENDED")


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
        if summons_ordinal(cfg) != "FIRST":
            if not _drop_template_heading(stripped):
                print("  !! template 'FIRST AMENDED' block not found — check the heading")
        _qpdf(["--flatten-annotations=all", stripped, flat])

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(612, 792))

        def line(x, y, t, s=9, f="Body"):
            c.setFont(f, s); c.drawString(x, y, t)

        # Heading — the template says FIRST; repaint it for any other ordinal.
        ordinal = summons_ordinal(cfg)
        if ordinal != "FIRST":
            _redraw_heading(c, ordinal)
            print(f"  heading repainted: {ordinal} AMENDED SUMMONS")

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
        # Item 3 — only when the Doe is an ENTITY. A natural person is served as
        # himself, so item 2 alone says everything; an LLC or corporation is served
        # THROUGH someone, and §474's fictitious-name endorsement does not by itself
        # tell the process server (or a later default court) under which subdivision
        # the entity was reached. Leave it off for a human.
        #   An LLC goes under CCP 416.10: Corp. Code §17701.16(b) routes service on a
        #   limited liability company to that section.
        ent = cfg.get("entity_service")
        if ent:
            CCP_SLOTS = {"416.10": (218.2, 110.3), "416.20": (218.2, 97.6),
                         "416.40": (218.2, 84.9),  "416.60": (414.9, 110.3),
                         "416.70": (414.9, 97.6),  "416.90": (414.9, 84.9)}
            c.setFont("BodyB", 11); c.drawString(190.2, 126.2, "X")   # item 3 checkbox
            line(298, 128.0, ent["name"], 10)                          # item 3 specify
            slot = CCP_SLOTS.get(str(ent.get("ccp", "")).strip())
            if slot:
                c.setFont("BodyB", 11); c.drawString(slot[0], slot[1], "X")
            else:
                print(f"  !! unknown CCP section {ent.get('ccp')!r} — no box marked")
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
    ordinal = summons_ordinal(cfg).title()
    summ = os.path.join(out_dir, f"{prefix} - {ordinal} Amended Summons ({tag}).pdf")
    make_civ105(cfg, civ)
    make_fa_summons(cfg, summ)
    print("CIV105:", civ)
    print("SUMMONS:", summ)


if __name__ == "__main__":
    main()
