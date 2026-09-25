#!/usr/bin/env python3
"""
make_cm110.py — draft a CM-110 Case Management Statement for a
凌图律所 / Law Office of Shenqi Cai (Hernán Simó) litigation case.

Usage:  python3 make_cm110.py <config.json>

Writes one flattened, signature-ready 5-page PDF to <output_dir>.
Draft/prep only: DATE + SIGNATURE are left blank for the attorney. Never files.

WHY OVERLAY, NOT ACROFORM TEXT (learned the hard way on Guolin Zhao, 2026-09-23):
  * qpdf --generate-appearances does NOT word-wrap multiline fields — it renders
    one line and silently clips the rest (item 4b lost 3/4 of the case summary).
  * Single-line fields clip too (item 3b(1)/(2) ran off the page).
  * Leaving /NeedAppearances true makes some renderers draw a value TWICE.
  So: set CHECKBOXES on the AcroForm, flatten, then draw every TEXT value with
  reportlab at the real field rect — wrapping and auto-shrinking to fit the box.
  Checkbox marks survive this order (flatten first, never overlay-then-flatten).

Verify output with ghostscript, not pdftoppm: the Judicial Council forms use
non-embedded Arial and poppler renders tofu.
"""
import sys, os, io, json, subprocess, tempfile
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
BLANK = os.path.join(ASSETS, "CM110_blank.pdf")

pdfmetrics.registerFont(TTFont("Body", "/System/Library/Fonts/Supplemental/Arial.ttf"))

P = "CM-110[0]."


# ---------------------------------------------------------------- helpers ----
def _fullname(o):
    parts, cur = [], o
    while cur is not None:
        t = cur.get("/T")
        if t:
            parts.append(str(t))
        p = cur.get("/Parent")
        cur = p.get_object() if p else None
    return ".".join(reversed(parts))


def _walk(objs):
    for f in objs:
        o = f.get_object()
        yield o
        k = o.get("/Kids")
        if k:
            yield from _walk(k)


def field_rects(pdf_path):
    """{full field name: {page, rect, multiline}} for every /Tx widget."""
    r = PdfReader(pdf_path)
    out = {}
    for pi, pg in enumerate(r.pages):
        for a in (pg.get("/Annots") or []):
            o = a.get_object()
            if o.get("/Subtype") != "/Widget":
                continue
            parent = o.get("/Parent")
            ft = o.get("/FT") or (parent.get_object().get("/FT") if parent else None)
            if str(ft) != "/Tx":
                continue
            ff = o.get("/Ff") or (parent.get_object().get("/Ff") if parent else None)
            ff = int(ff) if ff else 0
            out[_fullname(o)] = {
                "page": pi,
                "rect": [float(x) for x in o.get("/Rect")],
                "multiline": bool(ff & 4096),
            }
    return out


def wrap(text, font, size, maxw):
    lines = []
    for para in str(text).split("\n"):
        cur = ""
        for wd in para.split():
            t = (cur + " " + wd).strip()
            if pdfmetrics.stringWidth(t, font, size) <= maxw:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        lines.append(cur)
    return lines


# ------------------------------------------------------------ field values ---
def build_values(cfg):
    at, ct, cmc = cfg["attorney"], cfg["court"], cfg["cmc"]
    plaintiff = cfg["plaintiff"]
    defcap = cfg["defendant_caption"]
    case_no = cfg["case_number"]
    svc = cfg.get("service", {})
    adr = cfg.get("adr", {})

    T = {
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].AttyBarNo[0]": at["sbn"],
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].Name[0]": at["name"],
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].AttyFirm[0]": at["firm"],
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].Street[0]": at["street"],
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].City[0]": at["city"],
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].State[0]": at.get("state", "CA"),
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].Zip[0]": at["zip"],
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].Phone[0]": at["phone"],
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].Fax[0]": at.get("fax", ""),
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].Email[0]": at["email"],
        P+"Page1[0].P1Caption[0].AttyPartyInfo[0].AttyFor[0]": at.get("atty_for", "Plaintiff " + plaintiff),
        P+"Page1[0].P1Caption[0].CourtInfo[0].CrtCounty[0]": ct["county"],
        P+"Page1[0].P1Caption[0].CourtInfo[0].CrtStreet[0]": ct["street"],
        P+"Page1[0].P1Caption[0].CourtInfo[0].CrtCityZip[0]": ct["city_zip"],
        P+"Page1[0].P1Caption[0].CourtInfo[0].CrtBranch[0]": ct["branch"],
        P+"Page1[0].Note[0].Date1[0]": cmc["date"],
        P+"Page1[0].Note[0].Time1[0]": cmc["time"],
        P+"Page1[0].Note[0].Dept1[0]": cmc.get("dept", ""),
        P+"Page1[0].List1[0].Lia[0].TextField2[0]": cfg.get("filing_party", plaintiff),
        P+"Page1[0].List2[0].Lia[0].Date3[0]": cfg["complaint_filed"],
        P+"Page1[0].List4[0].Lia[0].FillText11[0]": cfg["case_type"],
        P+"Page2[0].List4[0].Lib[0].FillText13[0]": cfg["case_statement"],
        P+"Page2[0].List7[0].Lia[0].specify[0]": str(cfg.get("trial_days", "5")),
        P+"Page5[0].List20[0].NumberOfPages[0].Numbers[0]": str(cfg.get("pages_attached", "0")),
        P+"Page5[0].Sign[0].SigName1[0]": at["name"],
    }
    # caption repeats on pages 2-5
    for pg in ("Page2", "Page3", "Page4", "Page5"):
        T[P+f"{pg}[0].PxCaption[0].TitlePartyName[0].Party1[0]"] = plaintiff
        T[P+f"{pg}[0].PxCaption[0].TitlePartyName[0].Party2[0]"] = defcap
        T[P+f"{pg}[0].PxCaption[0].CaseNumber[0].caseNumber[0]"] = case_no
    T[P+"Page1[0].P1Caption[0].TitlePartyName[0].Party1[0]"] = plaintiff
    T[P+"Page1[0].P1Caption[0].TitlePartyName[0].Party2[0]"] = defcap
    T[P+"Page1[0].P1Caption[0].captionSub[0].CaseNumber[0].caseNumber[0]"] = case_no

    # item 3 service
    if svc.get("not_served"):
        T[P+"Page1[0].List3[0].lib[0].sublist[0].Lii1[0].TextField4[0]"] = svc["not_served"]
    if svc.get("served_not_appeared"):
        T[P+"Page1[0].List3[0].lib[0].sublist[0].Lii2[0].TextField5[0]"] = svc["served_not_appeared"]
    if svc.get("default_entered"):
        T[P+"Page1[0].List3[0].lib[0].sublist[0].li3[0].TextField7[0]"] = svc["default_entered"]

    # item 16b discovery table (up to 5 rows)
    slots = [("ft1", "ft2", "ft3"), ("ft4", "ft5", "ft6"), ("ft7", "ft8", "ft9"),
             ("ft10", "ft11", "ft12"), ("ft13", "ft", "ft")]
    for i, row in enumerate(cfg.get("discovery", [])[:5]):
        a, b, c = slots[i]
        base = P+"Page4[0].List16[0].Lib[0].Table[0]."
        T[base+f"AdmProceedingTitle_{a}[0]"] = row[0]
        T[base+f"AdmProceedingTitle_{b}[0]"] = row[1]
        T[base+f"AdmProceedingDate_{c}[0]"] = row[2]

    # item 19a explanation (left UNCHECKED when parties have not met and conferred)
    if cfg.get("meet_confer_explain"):
        T[P+"Page5[0].List19[0].Lia[0].Field43[0]"] = cfg["meet_confer_explain"]

    # ---------------- checkboxes ----------------
    C = {
        P+"Page1[0].P1Caption[0].FormTitle[0].limit12[0]": "/1" if cfg.get("unlimited", True) else None,
        P+"Page1[0].P1Caption[0].FormTitle[0].limit12[1]": None if cfg.get("unlimited", True) else "/2",
        P+"Page1[0].List1[0].Lia[0].partystatement1[0]": "/1",     # 1a submitted by party
        P+"Page1[0].List4[0].Lia[0].Ch10[0]": "/Yes",              # 4a complaint
        P+"Page2[0].List8[0].Ch25[0]": "/Yes",                     # 8 attorney in caption
        # --- Hernán's standing ADR answers (confirmed 2026-09-25) ---
        P+"Page2[0].List10[0].Lia[0].SubLista[0].Lii1[0].counsel1[0]": "/1",   # 10a(1) counsel HAS
        P+"Page2[0].List10[0].Lia[0].SubLista[0].Lii2[0].partya1[0]": "/1",    # 10a(2) party HAS
    }
    # item 3: all served? else 3b + sub-boxes
    if svc.get("all_served"):
        C[P+"Page1[0].List3[0].Lia[0].limitedee[0]"] = "/1"
    else:
        C[P+"Page1[0].List3[0].lib[0].Ch5[0]"] = "/2"
        if svc.get("not_served"):
            C[P+"Page1[0].List3[0].lib[0].sublist[0].Lii1[0].Ch6[0]"] = "/1"
        if svc.get("served_not_appeared"):
            C[P+"Page1[0].List3[0].lib[0].sublist[0].Lii2[0].Ch7[0]"] = "/1"
        if svc.get("default_entered"):
            C[P+"Page1[0].List3[0].lib[0].sublist[0].li3[0].Ch8[0]"] = "/1"
    # item 5 jury
    if cfg.get("jury", True):
        C[P+"Page2[0].List5[0].item5[0].jurytrial1[0]"] = "/1"
    else:
        C[P+"Page2[0].List5[0].item5[0].jurytrial1[1]"] = "/2"
    # item 6b no trial date set  (NOTE: the form pre-prints "within 12 months";
    # FillText8 is the "(if not, explain)" blank — leave it empty)
    if not cfg.get("trial_date"):
        C[P+"Page2[0].List6[0].Lib[0].Ch20[0]"] = "/2"
    else:
        C[P+"Page2[0].List6[0].Lia[0].Ch20[0]"] = "/1"
        T[P+"Page2[0].List6[0].Lia[0].Date7[0]"] = cfg["trial_date"]
    # item 7a days
    C[P+"Page2[0].List7[0].Lia[0].estimation1[0]"] = "/1"
    # item 16b anticipated discovery
    if cfg.get("discovery"):
        C[P+"Page4[0].List16[0].Lib[0].disco1[0]"] = "/2"
    # item 10c ADR matrix — Mediation + Settlement conference, "not yet scheduled"
    t1 = P+"Page3[0].List10[0].Lic[0].Table1[0]."
    if adr.get("mediation", True):
        C[t1+"Row1[0].sub1[0].limitedch[0]"] = "/1"
        C[t1+"Row1[0].sub2[0].partystatement10[0]"] = "/1"
    if adr.get("settlement_conference", True):
        C[t1+"Row2[0].sub3[0].limitedch1[0]"] = "/1"
        C[t1+"Row2[0].sub4[0].partystatement5[0]"] = "/1"

    C = {k: v for k, v in C.items() if v}
    T = {k: v for k, v in T.items() if str(v).strip()}
    return T, C


# ------------------------------------------------------------------ build ----
def build(cfg, out_path):
    RECTS = field_rects(BLANK)
    TEXT, CHECK = build_values(cfg)

    with tempfile.TemporaryDirectory() as td:
        # 1) checkboxes on the AcroForm, then flatten
        reader = PdfReader(BLANK)
        w = PdfWriter(); w.append(reader)
        acro = w._root_object["/AcroForm"]
        hits = set()
        for o in _walk(acro["/Fields"]):
            nm = _fullname(o)
            if nm in CHECK:
                on = CHECK[nm]
                o[NameObject("/V")] = NameObject(on)
                o[NameObject("/AS")] = NameObject(on)
                hits.add(nm)
        acro[NameObject("/NeedAppearances")] = BooleanObject(False)
        cb = os.path.join(td, "cb.pdf")
        with open(cb, "wb") as fh:
            w.write(fh)
        missing_c = set(CHECK) - hits
        flat = os.path.join(td, "flat.pdf")
        subprocess.run(["qpdf", "--flatten-annotations=all", cb, flat],
                       check=True, capture_output=True)

        # 2) overlay every text value at its real rect
        base = PdfReader(flat)
        per_page, missing_t = {}, []
        for nm, val in TEXT.items():
            if nm not in RECTS:
                missing_t.append(nm); continue
            per_page.setdefault(RECTS[nm]["page"], []).append((nm, val))

        out = PdfWriter()
        for pi in range(len(base.pages)):
            buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(612, 792))
            for nm, val in per_page.get(pi, []):
                x0, y0, x1, y1 = RECTS[nm]["rect"]
                ml = RECTS[nm]["multiline"]
                boxw, boxh = x1 - x0 - 4, y1 - y0
                size = 9.0
                if ml:
                    while size > 5.5:
                        if len(wrap(val, "Body", size, boxw)) * (size + 1.6) <= boxh + 1.0:
                            break
                        size -= 0.25
                    c.setFont("Body", size)
                    yy = y1 - size - 0.5
                    for ln in wrap(val, "Body", size, boxw):
                        c.drawString(x0 + 2, yy, ln); yy -= (size + 1.6)
                else:
                    while size > 5.5 and pdfmetrics.stringWidth(str(val), "Body", size) > boxw:
                        size -= 0.25
                    c.setFont("Body", size)
                    c.drawString(x0 + 2, y0 + (boxh - size) / 2 + 1.0, str(val))
            c.showPage(); c.save(); buf.seek(0)
            pg = base.pages[pi]; pg.merge_page(PdfReader(buf).pages[0]); out.add_page(pg)
        with open(out_path, "wb") as fh:
            out.write(fh)
    return len(TEXT), len(CHECK), missing_t, missing_c


def main():
    if len(sys.argv) != 2:
        print("usage: make_cm110.py <config.json>", file=sys.stderr); sys.exit(2)
    cfg = json.load(open(sys.argv[1]))
    out_dir = os.path.expanduser(cfg.get("output_dir", "~/Downloads"))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{cfg['file_prefix']} - CM-110 Case Management Statement.pdf")
    nt, nc, mt, mc = build(cfg, out)
    print(f"text fields: {nt}   checkboxes: {nc}")
    for m in mt: print("  MISS-TEXT:", m.replace(P, ""))
    for m in mc: print("  MISS-CHECK:", m.replace(P, ""))
    print("wrote:", out)
    print("verify with:  gs -o /tmp/cm_%d.png -sDEVICE=png16m -r110 '" + out + "'")


if __name__ == "__main__":
    main()
