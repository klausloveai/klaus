#!/usr/bin/env python3
"""Set one cell in an intake .xlsx to a text value, dependency-free.

openpyxl is NOT installed in this environment, so we edit xl/worksheets/sheet1.xml
directly: replace the target cell with an inlineStr, preserving its style (s="..").
Claim numbers are 16 digits — they MUST be stored as text (inlineStr), not numeric,
or precision is lost.

Usage:  python3 set_intake_cell.py <in.xlsx> <out.xlsx> <CELLREF> <VALUE>
  e.g.  python3 set_intake_cell.py intake.xlsx intake_new.xlsx L19 8844066210000001

Handles: (a) cell already present -> replace its content (keep style);
         (b) cell absent but its <row> exists -> insert the cell into the row;
         (c) row absent -> error (intake rows always exist for L19/I15).
Prints the resulting cell XML on success.
"""
import sys, re, zipfile
from xml.sax.saxutils import escape

def col_to_num(col):
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n

def main():
    src, dst, ref, value = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    col = re.match(r"[A-Z]+", ref).group(0)
    zin = zipfile.ZipFile(src, "r")
    sheet = "xl/worksheets/sheet1.xml"
    xml = zin.read(sheet).decode("utf-8")
    val = escape(str(value))

    cell_re = re.compile(r'<c r="%s"( s="\d+")?[^>]*>.*?</c>|<c r="%s"( s="\d+")?[^>]*/>' % (ref, ref))
    m = cell_re.search(xml)
    if m:
        style = (m.group(1) or m.group(2) or "")
        new_cell = '<c r="%s"%s t="inlineStr"><is><t>%s</t></is></c>' % (ref, style, val)
        xml2 = xml[:m.start()] + new_cell + xml[m.end():]
    else:
        # insert into the existing row, in column order
        rownum = re.match(r"[A-Z]+(\d+)", ref).group(1)
        rowm = re.search(r'(<row r="%s"[^>]*>)(.*?)(</row>)' % rownum, xml, re.S)
        if not rowm:
            sys.exit("ERROR: row %s not found; cannot insert %s" % (rownum, ref))
        new_cell = '<c r="%s" t="inlineStr"><is><t>%s</t></is></c>' % (ref, val)
        body = rowm.group(2)
        cells = re.findall(r'<c r="([A-Z]+)\d+"[^>]*?(?:/>|>.*?</c>)', body, re.S)
        # find insert position by column number
        target = col_to_num(col)
        insert_at = len(body)
        for cm in re.finditer(r'<c r="([A-Z]+)\d+"', body):
            if col_to_num(cm.group(1)) > target:
                insert_at = cm.start(); break
        newbody = body[:insert_at] + new_cell + body[insert_at:]
        xml2 = xml[:rowm.start(2)] + newbody + xml[rowm.end(2):]

    if xml2 == xml or val not in xml2:
        sys.exit("ERROR: edit did not apply")

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = xml2.encode("utf-8") if item.filename == sheet else zin.read(item.filename)
            zout.writestr(item, data)
    zin.close()
    print(re.search(r'<c r="%s"[^>]*>.*?</c>' % ref,
                    zipfile.ZipFile(dst).read(sheet).decode("utf-8")).group(0))

if __name__ == "__main__":
    main()
