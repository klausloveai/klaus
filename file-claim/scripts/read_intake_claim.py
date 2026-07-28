#!/usr/bin/env python3
"""Read claim-filing fields from a downloaded intake-sheet .xlsx (no dependencies).

Superset of lor-send's read_intake.py — adds the vehicle / accident / FOL cells
the carrier online-claim forms need. Cell refs follow new-case cell-map.md.

  Clients (col C):   C2=DOL  C3=Time  C4=Driver/Client Name  C7=Client Home Address
  Accident (col F):  F2=Accident Location  F4=Fact of Loss
  1P (col I) = OUR client's own carrier + OUR vehicle:
     I5=Insurer I6=Policy# I7=Policyholder I8=Driver I11=Vehicle I12=VIN I13=LP
     I15=Claim# I16=PD Adjuster I18=Adj Email I30=Policy Period
  3P (col L) = AT-FAULT carrier + AT-FAULT vehicle:
     L5=Insurer L6=Policy# L8=Policyholder(Insured) L9=Driver L11=DL#
     L13=Address L15=Vehicle L16=VIN L17=LP
     L19=Claim# L20=PD Adj L22=Adj Email L27=Policy Limits

Usage:  python3 read_intake_claim.py <intake.xlsx>
Prints a JSON object (missing/blank -> null).
"""
import sys, json, zipfile
from xml.etree import ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
WANT = {
    "C2": "dol", "C3": "time", "C4": "client", "C7": "client_address",
    "F2": "accident_location", "F4": "fol",
    # 1P = our client's own carrier and OUR vehicle
    "I5": "p1_insurer", "I6": "p1_policy", "I7": "p1_policyholder", "I8": "p1_driver",
    "I11": "our_vehicle", "I12": "our_vin", "I13": "our_lp",
    "I15": "p1_claim", "I16": "p1_adjuster", "I18": "p1_adjuster_email", "I30": "p1_period",
    # 3P = at-fault carrier and AT-FAULT vehicle
    "L5": "p3_insurer", "L6": "p3_policy", "L8": "p3_insured", "L9": "p3_driver",
    "L11": "p3_dl", "L13": "p3_address", "L15": "p3_vehicle", "L16": "p3_vin", "L17": "p3_lp",
    "L19": "p3_claim", "L20": "p3_adjuster", "L22": "p3_adjuster_email", "L27": "p3_limits",
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
