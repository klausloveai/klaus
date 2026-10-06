# -*- coding: utf-8 -*-
"""Table renderer + letterhead docx packager for client discovery questionnaires."""
import zipfile, os, re
from xml.sax.saxutils import escape

TNR = ('<w:rFonts w:ascii="Times New Roman" w:eastAsia="SimSun" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:hint="eastAsia"/>')
W_TOTAL, W_LABEL, W_ANS = 9360, 4320, 5040      # 6.5" = 3.0" + 3.5"

def rpr(sz=24, bold=False, color=None, hl=None):
    s = '<w:rPr>' + TNR
    if bold: s += '<w:b/><w:bCs/>'
    s += '<w:noProof/>'
    if color: s += f'<w:color w:val="{color}"/>'
    s += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    if hl: s += f'<w:highlight w:val="{hl}"/>'
    s += '</w:rPr>'
    return s

def run(t, sz=24, bold=False, color=None, hl=None):
    return f'<w:r>{rpr(sz,bold,color,hl)}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'

def para(t="", sz=24, bold=False, center=False, brk=False, color=None, hl=None,
         after=0, before=0, line=240, keep=False):
    p = '<w:pPr>'
    if brk: p += '<w:pageBreakBefore/>'
    if keep: p += '<w:keepNext/>'
    p += f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
    if center: p += '<w:jc w:val="center"/>'
    p += rpr(sz, bold, color) + '</w:pPr>'
    return f'<w:p>{p}{run(t,sz,bold,color,hl) if t else ""}</w:p>'

def blank(sz=24): return para("", sz=sz)

# ---------- table primitives ----------
BORDER = '<w:{0} w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>'
def _borders():
    return '<w:tblBorders>' + ''.join(BORDER.format(k) for k in
        ("top","left","bottom","right","insideH","insideV")) + '</w:tblBorders>'

def tbl_open(c1=W_LABEL, c2=W_ANS):
    return ('<w:tbl><w:tblPr>'
            f'<w:tblW w:w="{W_TOTAL}" w:type="dxa"/>'
            '<w:tblLayout w:type="fixed"/>'
            + _borders() +
            '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
            '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar>'
            '</w:tblPr>'
            f'<w:tblGrid><w:gridCol w:w="{c1}"/><w:gridCol w:w="{c2}"/></w:tblGrid>')

def tbl_close(): return '</w:tbl>'

def tc(width, body, span=1, shade=None):
    pr = f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>'
    if span > 1: pr += f'<w:gridSpan w:val="{span}"/>'
    if shade: pr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
    pr += '<w:vAlign w:val="top"/></w:tcPr>'
    return f'<w:tc>{pr}{body or para()}</w:tc>'

def tr(cells, height=0, split=False):
    pr = '<w:trPr>'
    if not split: pr += '<w:cantSplit/>'
    if height: pr += f'<w:trHeight w:val="{height}" w:hRule="atLeast"/>'
    pr += '</w:trPr>'
    return f'<w:tr>{pr}{"".join(cells)}</w:tr>'

def row_full(body, shade=None, height=0, split=False):
    return tr([tc(W_TOTAL, body, span=2, shade=shade)], height, split)

def row_label(en, cn, height=400):
    body = para(en, after=0) + (para(cn, after=0) if cn else "")
    return tr([tc(W_LABEL, body, shade="FAFAFA"), tc(W_ANS, para())], height)

def row_box(height):
    return tr([tc(W_TOTAL, para(), span=2)], height, split=True)

# ---------------- package assembly ----------------

NS = ('xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
      'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
      'xmlns:o="urn:schemas-microsoft-com:office:office" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
      'xmlns:v="urn:schemas-microsoft-com:vml" '
      'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:w10="urn:schemas-microsoft-com:office:word" '
      'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
      'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
      'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
      'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
      'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
      'mc:Ignorable="w14 wp14"')

HDR_RID   = "rId6"        # letterhead header already in the package
FOOT_RID  = "rId900"
BLANK_RID = "rId901"

RPR = ('<w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="SimSun" w:hAnsi="Times New Roman" '
       'w:cs="Times New Roman"/><w:noProof/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>')

FOOTER_TEXT = ["Law Office of Shenqi Cai APC  |  Form Interrogatories\u2014General (DISC-001) Questionnaire  |  Page "]

def footer_xml():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
  f'<w:ftr {NS}><w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
  f'<w:jc w:val="center"/>{RPR}</w:pPr>'
  f'<w:r>{RPR}<w:t xml:space="preserve">{FOOTER_TEXT[0]}</w:t></w:r>'
  f'<w:fldSimple w:instr=" PAGE "><w:r>{RPR}<w:t>1</w:t></w:r></w:fldSimple>'
  '</w:p></w:ftr>')

BLANK_HDR_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
  f'<w:hdr {NS}><w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
  f'{RPR}</w:pPr></w:p></w:hdr>')

def sectpr(top, header=None, footer=None, blank_header=False, final=True):
    s = '<w:sectPr>'
    if header:       s += f'<w:headerReference w:type="default" r:id="{header}"/>'
    if blank_header: s += f'<w:headerReference w:type="default" r:id="{BLANK_RID}"/>'
    if footer:       s += f'<w:footerReference w:type="default" r:id="{footer}"/>'
    s += ('<w:pgSz w:w="12240" w:h="15840"/>'
          f'<w:pgMar w:top="{top}" w:right="1440" w:bottom="1440" w:left="1440" '
          'w:header="720" w:footer="576" w:gutter="0"/>'
          '<w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr>')
    return s

def section_break_para(sp):
    """A paragraph whose only job is to carry a section break."""
    return f'<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>{sp}</w:pPr></w:p>'

def build(body_xml, out_path, base="hdr.docx", fix_fax=True):
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           f'<w:document {NS}><w:body>{body_xml}</w:body></w:document>')
    zin = zipfile.ZipFile(base, 'r')
    names = set(zin.namelist())
    if os.path.exists(out_path): os.remove(out_path)
    zout = zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED)

    for item in zin.infolist():
        n, data = item.filename, zin.read(item.filename)
        if n == 'word/document.xml':
            data = doc.encode('utf8')
        elif n == 'word/header1.xml' and fix_fax:
            t = data.decode('utf8')
            before = t.count('626-240-2046')
            t = t.replace('626-240-2046', '626-323-8181')
            print(f"   header1.xml: replaced {before} fax occurrence(s) -> 626-323-8181")
            data = t.encode('utf8')
        elif n == 'word/_rels/document.xml.rels':
            t = data.decode('utf8')
            add = (f'<Relationship Id="{FOOT_RID}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer900.xml"/>'
                   f'<Relationship Id="{BLANK_RID}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header901.xml"/>')
            t = t.replace('</Relationships>', add + '</Relationships>')
            data = t.encode('utf8')
        elif n == '[Content_Types].xml':
            t = data.decode('utf8')
            add = ('<Override PartName="/word/footer900.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
                   '<Override PartName="/word/header901.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>')
            t = t.replace('</Types>', add + '</Types>')
            data = t.encode('utf8')
        elif n == 'word/settings.xml':
            t = data.decode('utf8')
            if 'hideSpellingErrors' not in t:
                t = re.sub(r'(<w:settings[^>]*>)', r'\1<w:hideSpellingErrors/><w:hideGrammaticalErrors/>', t, count=1)
            data = t.encode('utf8')
        zout.writestr(item, data)

    zout.writestr('word/footer900.xml', footer_xml().encode('utf8'))
    zout.writestr('word/header901.xml', BLANK_HDR_XML.encode('utf8'))
    zin.close(); zout.close()
    print("   package parts added: footer900.xml, header901.xml")
