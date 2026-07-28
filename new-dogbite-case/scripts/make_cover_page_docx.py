#!/usr/bin/env python3
"""Editable Word (.docx) tri-fold mailing COVER PAGE for a #10 double-window envelope.

Same geometry as make_cover_page.py (the exact PDF generator), but as an EDITABLE Word
template: each address sits in a page-anchored, borderless TEXT BOX, so retyping the
address never shifts its position. Two solid fold guides at 3.667" and 7.333".

USPS: the address blocks hold ONLY the deliverable address — never a "To:" / "From:" label.

Usage:
  python3 make_cover_page_docx.py <out.docx>                       # template (placeholders)
  python3 make_cover_page_docx.py <out.docx> "line1" "line2" ...   # filled recipient
"""
import sys
from docx import Document
from docx.shared import Inches
from docx.oxml import parse_xml

IN = 72.0  # pt per inch
RET_TOP, RET_LEFT, RET_W, RET_SIZE = 0.50, 0.90, 3.30, 10
TO_TOP,  TO_LEFT,  TO_W,  TO_SIZE = 2.05, 1.10, 4.00, 11
FOLD1, FOLD2, PAGE_W = 3.667, 7.333, 8.5

RETURN_ADDRESS = ["Lingtu Law Office",
                  "13191 Crossroads Pkwy N, Suite 295",
                  "City of Industry, CA 91746"]
TEMPLATE_RECIPIENT = ["[Recipient Name] and Any/All Residents,",
                      "Occupants, or Dog Owners",
                      "[Street Address]",
                      "[City, State ZIP]"]

NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:v="urn:schemas-microsoft-com:vml" '
      'xmlns:o="urn:schemas-microsoft-com:office:office" '
      'xmlns:w10="urn:schemas-microsoft-com:office:word"')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def textbox(lines, left_in, top_in, width_in, size_pt):
    body = "".join(
        f'<w:p><w:pPr><w:spacing w:after="0" w:line="{int(size_pt*20*1.3)}" '
        f'w:lineRule="exact"/></w:pPr><w:r><w:rPr>'
        f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:sz w:val="{int(size_pt*2)}"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(l)}</w:t></w:r></w:p>' for l in lines)
    style = (f"position:absolute;margin-left:{left_in*IN}pt;margin-top:{top_in*IN}pt;"
             f"width:{width_in*IN}pt;height:{(len(lines)*size_pt*1.4)+6}pt;z-index:1;"
             "mso-position-horizontal-relative:page;mso-position-vertical-relative:page")
    return parse_xml(
        f'<w:p {NS}><w:r><w:pict>'
        f'<v:shape type="#_x0000_t202" style="{style}" stroked="f" filled="f">'
        f'<v:textbox inset="0,0,0,0"><w:txbxContent>{body}</w:txbxContent></v:textbox>'
        f'</v:shape></w:pict></w:r></w:p>')


def foldline(top_in):
    style = (f"position:absolute;z-index:2;"
             "mso-position-horizontal-relative:page;mso-position-vertical-relative:page")
    return parse_xml(
        f'<w:p {NS}><w:r><w:pict>'
        f'<v:line style="{style}" from="0,{top_in*IN}pt" to="{PAGE_W*IN}pt,{top_in*IN}pt" '
        f'strokecolor="#000000" strokeweight="0.75pt"/>'
        f'</w:pict></w:r></w:p>')


def build(out, recipient):
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Inches(8.5), Inches(11)
    for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(s, m, Inches(0.3))
    b = doc.element.body
    b.append(textbox(RETURN_ADDRESS, RET_LEFT, RET_TOP, RET_W, RET_SIZE))
    b.append(textbox(recipient, TO_LEFT, TO_TOP, TO_W, TO_SIZE))
    b.append(foldline(FOLD1))
    b.append(foldline(FOLD2))
    doc.save(out)
    print("cover page (docx):", out)


if __name__ == "__main__":
    a = sys.argv[1:]
    build(a[0], a[1:] if len(a) > 1 else TEMPLATE_RECIPIENT)
