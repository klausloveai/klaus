#!/usr/bin/env python3
"""Read referral fields from a downloaded intake .xlsx (no deps).
Cells (new-case cell-map): C2=DOL C3=Time C4=Client C5=DOB C6=Phone C7=Address
C8=Email  F2=Accident Location  F4=Fact of Loss  F5=Point of Impact (=accident type).
Usage: python3 read_intake_referral.py <intake.xlsx>  -> JSON (blank -> null).
"""
import sys, json, zipfile
from xml.etree import ElementTree as ET
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
WANT = {"C2":"dol","C3":"time","C4":"client","C5":"dob","C6":"phone","C7":"address",
        "C8":"email","F2":"accident_location","F4":"fol","F5":"point_of_impact"}
def main():
    z=zipfile.ZipFile(sys.argv[1]); ss=[]
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS+"si"):
            ss.append("".join(n.text or "" for n in si.iter(NS+"t")))
    cells={}
    for c in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(NS+"c"):
        ref,typ=c.get("r"),c.get("t"); v,istr=c.find(NS+"v"),c.find(NS+"is"); val=None
        if v is not None: val=ss[int(v.text)] if typ=="s" else v.text
        elif istr is not None: val="".join(x.text or "" for x in istr.iter(NS+"t"))
        if val not in (None,""): cells[ref]=val.strip()
    print(json.dumps({k:cells.get(r) for r,k in WANT.items()}, ensure_ascii=False, indent=2))
if __name__=="__main__": main()
