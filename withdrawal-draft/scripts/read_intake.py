#!/usr/bin/env python3
"""Read withdrawal-letter fields from a downloaded intake-sheet .xlsx (no deps).

The intake sheet is an .xlsx (not a Google Sheet), so we parse the OOXML
directly. Values live in fixed cells (see new-case references/cell-map.md):
  Clients (col C):  C2=DOL(MM/DD/YYYY)  C4=Driver Name
  Accident (col F): F2=Accident Location  (used to determine the governing state/SOL)

The withdrawal template has NO recipient address block, so the client's mailing
address is not read. For a multi-client case (driver + passenger[s]), the
passenger names live in C24 (Pass1), F24 (Pass2), C49 (Pass3), F49 (Pass4) — the
skill joins the relevant client names with "/" itself.

Usage:  python3 read_intake.py <intake.xlsx>
Prints a JSON object of the cells above (missing/blank -> null).
"""
import sys, json, zipfile
from xml.etree import ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
WANT = {
    "C2": "dol", "C4": "client",
    "F2": "accident_location",
}

def main():
    z = zipfile.ZipFile(sys.argv[1])
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si"):
            ss.append("".join(n.text or "" for n in si.iter(NS + "t")))
    cells = {}
    for c in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(NS + "c"):
        ref, typ = c.get("r"), c.get("t")
        v, istr = c.find(NS + "v"), c.find(NS + "is")
        val = None
        if v is not None:
            val = ss[int(v.text)] if typ == "s" else v.text
        elif istr is not None:
            val = "".join(x.text or "" for x in istr.iter(NS + "t"))
        if val not in (None, ""):
            cells[ref] = val.strip()
    out = {key: cells.get(ref) for ref, key in WANT.items()}
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
