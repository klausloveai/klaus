#!/usr/bin/env python3
"""Read LOR fields from a downloaded intake-sheet .xlsx (no dependencies).

The intake sheet is an .xlsx (not a Google Sheet), so we parse the OOXML
directly. Values live in fixed cells (see new-case references/cell-map.md):
  Clients:  C2=DOL  C4=Driver Name
  1P (col I): I5=Insurer I6=Policy# I7=Policyholder I15=Claim# I16=PD Adj I18=Adj Email
  3P (col L): L5=Insurer L6=Policy# L8=Policyholder(Insured) L9=Driver
              L19=Claim# L20=PD Adj L22=Adj Email

Usage:  python3 read_intake.py <intake.xlsx>
Prints a JSON object of the cells above (missing/blank -> null).
"""
import sys, json, zipfile
from xml.etree import ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
WANT = {
    "C2": "dol", "C4": "client",
    "I5": "p1_insurer", "I6": "p1_policy", "I7": "p1_policyholder",
    "I15": "p1_claim", "I16": "p1_adjuster", "I18": "p1_adjuster_email",
    "L5": "p3_insurer", "L6": "p3_policy", "L8": "p3_insured", "L9": "p3_driver",
    "L19": "p3_claim", "L20": "p3_adjuster", "L22": "p3_adjuster_email",
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
