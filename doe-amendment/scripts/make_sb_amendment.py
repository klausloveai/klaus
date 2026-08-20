#!/usr/bin/env python3
"""
make_sb_amendment.py — San Bernardino DOE amendment package:
  * SB-16778 "Amendment to Complaint" (Fictitious Name, No order required)  +
  * First Amended Summons (SUM-100) with the §474 fictitious-name endorsement
for each newly-identified DOE defendant.

San Bernardino Superior Court uses local form SB-16778 for a Doe/fictitious-name
amendment — NOT the LA CIV 105 (that path lives in make_doe_amendment.py). Use
this script for San Bernardino cases (case no. prefix CIVSB...).

TEMPLATE SOURCE (Klaus's standing instruction, 2026-08-20): the SB-16778 blank is
pulled fresh at run time from Klaus's Drive file so that if he revises the firm's
template, the change flows through automatically:
    Drive file "Amendent to Complaint.pdf"  id = 184p3wdnweubmMwkuU4sB8EJQ5cUgMDgj
If the Drive pull fails (offline / gws down), it falls back to the bundled cache
assets/SB-16778_blank.pdf (byte-identical to the official court blank as of 8/20/26).

Draft-only: Declarant DATE + SIGNATURE (SB-16778) and summons DATE/Clerk/Deputy are
left blank; INCORRECT NAME + ORDER sections stay blank. Never e-files, never serves.

Usage:  python3 make_sb_amendment.py <config.json>

Config schema (see make_doe_amendment.py for attorney/court fields; here `defendants`
is a LIST so one run can add several Does at once):
{
  "output_dir": "/Users/klaus/Downloads/Yi Cong - DOE Amendments",
  "file_prefix": "Yi Cong",
  "case_number": "CIVSB2619725",
  "plaintiff": "YI CONG",
  "attorney": { ...same shape as make_doe_amendment... },
  "court_name": "Superior Court of California, County of San Bernardino",
  "court_address": "247 West 3rd Street, San Bernardino, CA 92415-0210",
  "court_branch_note": "San Bernardino District — San Bernardino Justice Center",
  "complaint_defendant_caption": "RHEA EDPAO; and DOES 1 through 20, inclusive",
  "summons_defendant_caption": "RHEA EDPAO; CAMDEN LANDMARK, LLC; CAMDEN DEVELOPMENT, INC.; and DOES 1 through 20, inclusive",
  "defendants": [
    {"doe_number": "DOE 11", "true_name": "CAMDEN LANDMARK, LLC"},
    {"doe_number": "DOE 12", "true_name": "CAMDEN DEVELOPMENT, INC."}
  ]
}
"""
import sys, os, io, json, subprocess, tempfile
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, HERE)
import make_doe_amendment as mda  # reuse the tested First Amended Summons generator

pdfmetrics.registerFont(TTFont("Body", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("BodyB", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

SB16778_DRIVE_ID = "184p3wdnweubmMwkuU4sB8EJQ5cUgMDgj"   # Klaus's canonical template
SB16778_CACHE = os.path.join(ASSETS, "SB-16778_blank.pdf")


def fetch_sb16778_blank(dest):
    """Pull the SB-16778 blank fresh from Klaus's Drive; fall back to the cache."""
    try:
        # gws forbids --output paths outside the cwd, so run inside dest's dir
        # with a relative filename.
        ddir, dname = os.path.dirname(dest), os.path.basename(dest)
        r = subprocess.run(
            ["gws", "drive", "files", "get",
             "--params", json.dumps({"fileId": SB16778_DRIVE_ID, "alt": "media",
                                     "supportsAllDrives": True}),
             "--output", dname],
            cwd=ddir, capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 1000:
            # refresh the cache too
            try:
                import shutil; shutil.copyfile(dest, SB16778_CACHE)
            except Exception:
                pass
            return "drive"
    except Exception:
        pass
    import shutil; shutil.copyfile(SB16778_CACHE, dest)
    return "cache"


def make_sb16778(cfg, doe_number, true_name, blank, out_path):
    at = cfg["attorney"]
    branch = cfg.get("court_branch_note", "")
    with tempfile.TemporaryDirectory() as td:
        flat = os.path.join(td, "flat.pdf")
        subprocess.run(["qpdf", "--flatten-annotations=all", blank, flat],
                       check=True, capture_output=True)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(612, 792))

        def L(x, y, t, s=8.5, f="Body"):
            c.setFont(f, s); c.drawString(x, y, t)

        def C(x, y, t, s=11, f="Body"):
            c.setFont(f, s); c.drawCentredString(x, y, t)

        # Attorney box (top-left caption)
        L(42, 746, f"{at['name']} (SBN {at['sbn']})")
        L(42, 736, at["firm"])
        L(42, 726, f"{at['addr1']}, {at['addr2']}", 7.5)
        L(100, 708, at["tel"])                                   # Telephone No.
        L(305, 708, at.get("fax", ""))                           # Fax No.
        L(132, 694, f"Plaintiff, {cfg['plaintiff']}")            # Attorney For (Name)
        L(288, 694, at["sbn"])                                   # Bar No.
        # Court block (SB pre-printed "COUNTY OF SAN BERNARDINO")
        street = cfg["court_address"].split(",")[0].strip()
        cityzip = ",".join(cfg["court_address"].split(",")[1:]).strip()
        L(125, 662, street)                                      # street address
        L(125, 647, street)                                      # mailing address
        L(130, 631, cityzip)                                     # city/zip
        L(110, 616, branch, 7.5)                                 # branch name
        # Parties
        L(185, 597, cfg["plaintiff"])                            # plaintiff
        L(195, 571, cfg["complaint_defendant_caption"])          # defendant (pre-amendment)
        L(463, 524, cfg["case_number"], 9)                       # case number
        # FICTITIOUS NAME (No order required)
        C(298, 459, doe_number, 11)                              # fictitious name of: DOE N
        C(298, 425, true_name, 11)                               # true name to be: entity
        # Date + Declarant's Signature intentionally BLANK (attorney signs)
        # INCORRECT NAME + ORDER sections intentionally BLANK
        c.showPage(); c.save(); buf.seek(0)

        base = PdfReader(flat); ov = PdfReader(buf)
        w = PdfWriter(); pg = base.pages[0]; pg.merge_page(ov.pages[0]); w.add_page(pg)
        with open(out_path, "wb") as fh:
            w.write(fh)


def main():
    if len(sys.argv) != 2:
        print("usage: make_sb_amendment.py <config.json>", file=sys.stderr); sys.exit(2)
    cfg = json.load(open(sys.argv[1]))
    out_dir = os.path.expanduser(cfg["output_dir"]); os.makedirs(out_dir, exist_ok=True)
    prefix = cfg["file_prefix"]

    with tempfile.TemporaryDirectory() as td:
        blank = os.path.join(td, "sb16778.pdf")
        src = fetch_sb16778_blank(blank)
        print(f"SB-16778 blank source: {src}")
        for d in cfg["defendants"]:
            tag = f"{d['doe_number']} {d['true_name']}"
            sb = os.path.join(out_dir, f"{prefix} - SB-16778 Amendment to Complaint ({tag}).pdf")
            su = os.path.join(out_dir, f"{prefix} - First Amended Summons ({tag}).pdf")
            make_sb16778(cfg, d["doe_number"], d["true_name"], blank, sb)
            scfg = dict(cfg); scfg["doe_number"] = d["doe_number"]; scfg["true_name"] = d["true_name"]
            mda.make_fa_summons(scfg, su)
            print("SB16778 :", sb)
            print("SUMMONS :", su)
    print("DONE")


if __name__ == "__main__":
    main()
