#!/usr/bin/env python3
"""Fill the Dog Owner POE (spoliation) template for a dog-bite case.

Replaces the template's [bracket] tokens with THIS case's collected info, YELLOW-
HIGHLIGHTS the variables Hernán must confirm (owner name, address, city, dog breed),
and sets the letter [Date] as a Word auto-date field (format "July 15, 2026" =
`DATE \\@ "MMMM d, yyyy"`). Output = a filled .docx (convert to PDF separately).

Only pass values this case's own materials establish — never copy from another case.
Leave a variable as a highlighted "[… — confirm]" placeholder when unknown.

Usage: python3 fill_poe.py <template.docx> <fields.json> <out.docx>
  fields.json keys: owner_name, address, city_zip, client_name, date_of_incident,
                    location, dog_breed, county, delivery_clause (optional)
  highlight: list of token-labels to highlight yellow (default: owner/address/city/breed)
"""
import sys, json, copy
from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TOKENS = {  # template token -> fields.json key
    "[Dog Owner / Resident Name]": "owner_name",
    "[Address]": "address",
    "[City, State ZIP]": "city_zip",
    "[Client Name]": "client_name",
    "[Date of Incident]": "date_of_incident",
    "[Location]": "location",
    "[dog breed]": "dog_breed",
    "[County]": "county",
    "[to complete a commercial delivery]": "delivery_clause",
}
HIGHLIGHT_KEYS = {"owner_name", "address", "city_zip", "dog_breed"}


def set_date_field(run):
    """Turn a run into a Word DATE field formatted 'Month D, YYYY'."""
    r = run._r
    for ch in list(r):
        if ch.tag == qn('w:t'):
            r.remove(ch)
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), r'DATE \@ "MMMM d, yyyy"')
    t = OxmlElement('w:t'); t.text = "July 15, 2026"
    sub = OxmlElement('w:r'); sub.append(t); fld.append(sub)
    r.addnext(fld)


def main():
    tmpl, fields_path, out = sys.argv[1:4]
    f = json.load(open(fields_path))
    doc = Document(tmpl)
    for p in doc.paragraphs:
        for run in p.runs:
            txt = run.text
            if not txt:
                continue
            if "[Date]" in txt and txt.strip() == "[Date]":
                run.text = ""
                set_date_field(run)
                continue
            for token, key in TOKENS.items():
                if token in txt:
                    val = str(f.get(key, "")).strip()
                    if key == "delivery_clause":
                        val = val or "to complete a commercial delivery"
                    txt = txt.replace(token, val)
                    if key in HIGHLIGHT_KEYS:
                        run.font.highlight_color = WD_COLOR_INDEX.YELLOW
            run.text = txt
    doc.save(out)
    print("POE written:", out)


if __name__ == "__main__":
    main()
