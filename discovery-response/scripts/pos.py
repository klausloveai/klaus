# -*- coding: utf-8 -*-
"""House proof-of-service block, built to POS-TEMPLATE-format-fixed (2026-10-12).

Klaus's standing template. Three parts, in this order:
  page 1  PROOF OF SERVICE heading, employment recital, documents served, and the
          service methods -- ONLY the methods used, each marked X (Klaus 2026-10-26; was all five).
  page 2  declaration under penalty of perjury, ///, execution line, signature,
          and the bracketed [Service List on following page.] line.
  page 3  SERVICE LIST: case name, court and case number, then a BORDERED
          two-column table, counsel on the left and the party served on the right.

The engine in common.py sets bold per paragraph, so this module carries its own
run splitter: **double asterisks** mark a bold span inside an otherwise plain
paragraph (the method names and the two dates need it).
"""
import copy
import re
from docx.enum.text import WD_ALIGN_PARAGRAPH as A
from docx.oxml.ns import qn
from docx.shared import Pt

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
MARK = re.compile(r"\*\*(.+?)\*\*|//(.+?)//", re.S)

METHODS = [
    ("personal", "By personal service.",
     " I personally delivered the documents to the persons at the addresses listed in the "
     "Service List. (1) For a party represented by an attorney, delivery was made (a) to the "
     "attorney personally; or (b) by leaving the documents at the attorney's office, in an "
     "envelope or package clearly labeled to identify the attorney being served, with a "
     "receptionist or an individual in charge of the office; or (c) if there was no person in "
     "the office with whom the notice or papers could be left, by leaving them in a conspicuous "
     "place in the office between the hours of nine in the morning and five in the morning and "
     "five in the evening. (2) For a party, delivery was made to the party or by leaving the "
     "documents at the party's residence with some person not younger than 18 years of age "
     "between the hours of eight in the morning and eight in the evening."),
    ("mail", "By United States mail.",
     " I enclosed the documents in a sealed envelope or package addressed to the person(s) at "
     "the address(es) in the Service List and placed the envelope for collection and mailing, "
     "following our ordinary business practices. I am readily familiar with this firm's practice "
     "for collecting and processing correspondence for mailing. On the same day that "
     "correspondence is placed for collection and mailing, it is deposited in the ordinary course "
     "of business with the United States Postal Service, in a sealed envelope with postage fully "
     "prepaid."),
    ("overnight", "By overnight delivery:",
     " I enclosed the documents in an envelope or package provided by an overnight delivery "
     "carrier and addressed to the persons at the addresses in the Service List. I placed the "
     "envelope or package for collection and overnight delivery at an office or a regularly "
     "utilized drop box of the overnight delivery carrier."),
    ("fax", "By fax transmission.",
     " Based on an agreement of the parties to accept service by fax transmission, I faxed the "
     "documents to the persons at the fax numbers listed in the Service List. No error was "
     "reported by the fax machine that I used. A copy of the record of the fax transmission, "
     "which I printed out, is attached."),
    ("email", "By electronic mail (e-mail):",
     " The party served is represented by counsel and has appeared in the action or proceeding. "
     "Before first serving the represented party electronically, I confirmed by telephone or "
     "email the appropriate electronic service address for counsel being served, in accordance "
     "with Code of Civil Procedure section 1010.6(e)(1)."),
]


def _runs(p):
    return p._p.findall(W + "r")


def rich(p, text, align=None):
    """Re-text a cloned paragraph, honouring **bold** spans and \\t tabs."""
    rs = _runs(p)
    proto = rs[0]
    for r in rs[1:]:
        r.getparent().remove(r)
    for tag in ("t", "tab", "br"):
        for el in proto.findall(W + tag):
            proto.remove(el)

    segs, pos = [], 0
    for m in MARK.finditer(text):
        if m.start() > pos:
            segs.append((text[pos:m.start()], None))
        segs.append((m.group(1), "b") if m.group(1) is not None else (m.group(2), "i"))
        pos = m.end()
    if pos < len(text) or not segs:
        segs.append((text[pos:], None))

    def fill(r, s):
        for chunk in re.split(r"(\t)", s):
            if chunk == "\t":
                r.append(r.makeelement(W + "tab", {}))
            elif chunk:
                t = r.makeelement(W + "t", {})
                t.text = chunk
                t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                r.append(t)

    def style(r, kind):
        """Add bold/italic for a marked span. Never strip what the prototype carries --
        the Heading 1 prototype is bold, and clearing it silently un-bolded PROOF OF
        SERVICE, STATE OF CALIFORNIA and SERVICE LIST (caught 2026-10-12)."""
        if not kind:
            return
        rPr = r.find(W + "rPr")
        if rPr is None:
            rPr = r.makeelement(W + "rPr", {}); r.insert(0, rPr)
        tag = "b" if kind == "b" else "i"
        if rPr.find(W + tag) is None:
            rPr.insert(0, rPr.makeelement(W + tag, {}))

    anchor = proto
    for i, (s, b) in enumerate(segs):
        if i == 0:
            fill(proto, s); style(proto, b)
        else:
            r = copy.deepcopy(proto)
            for tag in ("t", "tab", "br"):
                for el in r.findall(W + tag):
                    r.remove(el)
            fill(r, s); style(r, b)
            anchor.addnext(r); anchor = r
    if align is not None:
        p.alignment = align
    return p


def _emit(doc, protos, kind, text, align=None, indent=None):
    from docx.text.paragraph import Paragraph
    new = copy.deepcopy(protos[kind])
    if indent is not None:
        pPr = new.find(W + "pPr")
        for i in pPr.findall(W + "ind"):
            pPr.remove(i)
        pPr.append(pPr.makeelement(W + "ind", {W + "start": str(indent),
                                               W + "left": str(indent),
                                               W + "firstLine": "0"}))
    body = doc.element.body
    sect = body.find(W + "sectPr")
    (sect.addprevious(new) if sect is not None else body.append(new))
    return rich(Paragraph(new, doc._body), text, align)


def _bordered(table):
    tblPr = table._tbl.tblPr
    borders = tblPr.makeelement(qn("w:tblBorders"), {})
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = borders.makeelement(qn("w:" + edge), {})
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "6")
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000")
        borders.append(e)
    tblPr.append(borders)


ADDRESS = ("13191 Crossroads Parkway North, Suite 295, City of Industry, California 91746")


def build(doc, protos, *, served, date="____________, 2026", method="email",
          declarant="Klaus Liu", case_name, court_line, counsel=None, party_role=None,
          party_name=None, page_break, parties=None, address=ADDRESS):
    """Append the three-part proof of service.

    `method` is one key or a tuple of keys (mixed service, e.g. ("mail", "email") when
    in pro per parties are mailed and counsel is e-served). `parties` is a list of
    (left_lines, right_lines) rows for the service list; when omitted, one row is built
    from `counsel` / `party_role` / `party_name` as before."""
    used = {method} if isinstance(method, str) else set(method)
    page_break(doc, protos)
    _emit(doc, protos, "head", "PROOF OF SERVICE")
    _emit(doc, protos, "head", "STATE OF CALIFORNIA, COUNTY OF LOS ANGELES")
    _emit(doc, protos, "body",
          "\tI am employed in the County of Los Angeles, State of California. At the time of "
          "service, I was over the age of 18 and not a party to this action; my business address "
          "is %s." % address)
    _emit(doc, protos, "body", "\tOn **%s**, I served the following documents:" % date)
    _emit(doc, protos, "body", "\t**%s**" % served)
    _emit(doc, protos, "body",
          "\tI served the documents on the person(s) in the Service List below, as follows:")
    # Klaus 2026-10-26: list only the methods actually used (all X); unchecked methods are dropped.
    for key, name, text in METHODS:
        if key in used:
            _emit(doc, protos, "sub", "▪\t   X   **%s**%s" % (name, text))

    _emit(doc, protos, "body", "")
    _emit(doc, protos, "body",
          "\tI declare under penalty of perjury under the laws of the State of California that "
          "the above is true and correct.")
    _emit(doc, protos, "body", "///", align=A.LEFT)
    _emit(doc, protos, "body",
          "\tExecuted on **%s** in City of Industry, California." % date)
    _emit(doc, protos, "body", "______________________", align=A.LEFT, indent=5760)
    _emit(doc, protos, "body", declarant, align=A.LEFT, indent=5760)
    _emit(doc, protos, "body", "[Service List on following page.]", align=A.CENTER)

    _emit(doc, protos, "head", "SERVICE LIST")
    _emit(doc, protos, "body", case_name, align=A.CENTER)
    _emit(doc, protos, "body", court_line, align=A.CENTER)

    if parties is None:
        parties = [(counsel, ["//Attorneys for %s://" % party_role, "", "**%s**" % party_name])]
    t = doc.add_table(rows=len(parties), cols=2)
    _bordered(t)
    sect = doc.element.body.find(W + "sectPr")
    sect.addprevious(t._tbl)
    proto = copy.deepcopy(protos["body"])

    from docx.text.paragraph import Paragraph

    def fill_cell(cell, lines):
        for p in list(cell.paragraphs):
            cell._tc.remove(p._p)
        for txt in lines:
            el = copy.deepcopy(proto)
            for jc in el.findall(W + "pPr/" + W + "jc"):
                el.find(W + "pPr").remove(jc)
            cell._tc.append(el)
            rich(Paragraph(el, cell), txt)
    for row, (lcol, rcol) in zip(t.rows, parties):
        fill_cell(row.cells[0], lcol)
        fill_cell(row.cells[1], rcol)
