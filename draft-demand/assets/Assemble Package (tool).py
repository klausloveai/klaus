#!/usr/bin/env python3
"""
Assemble a ready-to-send demand package into ONE bookmarked PDF.

Usage:
    python3 "Assemble Package (tool).py" "/path/to/<Client> - Demand Package"

It looks in that folder for:
  • the demand letter  -> any PDF whose name contains "Demand Letter" (or "Demand")
  • exhibits           -> PDFs named "Exhibit N - <description>.pdf"
…then builds:  Demand Letter  +  (divider page + exhibit) for each exhibit, in order,
with PDF bookmarks (Demand Letter, Exhibit 1, Exhibit 2, …), saved as
"<Client> - Demand Package (MERGED).pdf" in the same folder.
"""
import re, sys, os, tempfile
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit

def make_divider(n, desc, path):
    c = canvas.Canvas(path, pagesize=letter)
    w, h = letter
    c.setFont("Helvetica-Bold", 54); c.drawCentredString(w/2, h/2 + 50, f"EXHIBIT {n}")
    c.setLineWidth(1.2); c.line(w/2 - 130, h/2 + 30, w/2 + 130, h/2 + 30)
    c.setFont("Helvetica", 22)
    y = h/2 - 10
    for line in simpleSplit(desc, "Helvetica", 22, w - 200):
        c.drawCentredString(w/2, y, line); y -= 28
    c.setFont("Helvetica-Oblique", 10); c.drawCentredString(w/2, 54, "Lingtu Law Office")
    c.showPage(); c.save()

def main(folder):
    folder = os.path.abspath(folder)
    pdfs = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")
            and "(MERGED)" not in f and "(PREVIEW)" not in f]
    demand = next((f for f in pdfs if "demand letter" in f.lower()), None) \
        or next((f for f in pdfs if "demand" in f.lower() and not f.lower().startswith("exhibit")), None)
    if not demand:
        sys.exit("No demand-letter PDF found (need a PDF with 'Demand Letter' in the name).")
    exh = []
    for f in pdfs:
        m = re.match(r"Exhibit\s+(\d+)\s*-\s*(.+)\.pdf$", f, re.I)
        if m: exh.append((int(m.group(1)), m.group(2).strip(), f))
    exh.sort(key=lambda x: x[0])

    client = re.split(r"\s*-\s*", demand)[0].strip()
    out = os.path.join(folder, f"{client} - Demand Package (MERGED).pdf")

    writer = PdfWriter(); tmp = []
    start = len(writer.pages); writer.append(os.path.join(folder, demand), import_outline=False)
    writer.add_outline_item("Demand Letter", start)
    for n, desc, f in exh:
        dpath = os.path.join(tempfile.gettempdir(), f"_div{n}.pdf"); make_divider(n, desc, dpath); tmp.append(dpath)
        dstart = len(writer.pages); writer.append(dpath, import_outline=False)
        node = writer.add_outline_item(f"Exhibit {n} - {desc}", dstart)
        writer.append(os.path.join(folder, f), import_outline=False)
    with open(out, "wb") as fh: writer.write(fh)
    for t in tmp:
        try: os.remove(t)
        except OSError: pass
    print(f"Demand letter : {demand}")
    print("Exhibits      : " + (", ".join(f"Ex {n} ({desc})" for n, desc, _ in exh) or "none"))
    print(f"Pages         : {len(writer.pages)}")
    print(f"Saved         : {out}")

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit('Usage: python3 "Assemble Package (tool).py" "/path/to/<Client> - Demand Package"')
    main(sys.argv[1])
