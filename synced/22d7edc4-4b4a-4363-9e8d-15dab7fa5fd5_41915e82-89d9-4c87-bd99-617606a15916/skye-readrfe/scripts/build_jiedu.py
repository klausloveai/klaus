#!/usr/bin/env python3
"""Build the RFE 解读+策略 document (.docx) from a JSON spec.

Usage:  python3 build_jiedu.py spec.json out.docx

The .docx is an intermediate: upload it to Drive converting to a Google Doc, e.g.
  gws drive files create --params '{"uploadType":"multipart","supportsAllDrives":true}' \
    --json '{"name":"<Client> RFE 解读+策略","mimeType":"application/vnd.google-apps.document","parents":["<RFE folder id>"]}' \
    --upload out.docx \
    --upload-content-type application/vnd.openxmlformats-officedocument.wordprocessingml.document

Inline markup, usable in any text field:
    **text**   -> RED BOLD   (the officer's operative holding — the sentence that decides the objection)
    ~~text~~   -> red plain  (secondary emphasis: the specific words being complained about)
    [[text]]   -> black bold (structural emphasis inside prose; rarely needed)
    <<text>>   -> hyperlink-blue (paste Drive URLs here so they read as links)

Spec shape — see references/spec_example.json for a filled-in example.
"""
import json, re, sys, zipfile

NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
RED, BLUE, DARK = 'ff0000', '1155cc', '0b0b0b'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def runs(text, base_bold=False, base_color=None):
    """Turn marked-up text into a run sequence."""
    out = []
    for tok in re.split(r'(\*\*.+?\*\*|~~.+?~~|\[\[.+?\]\]|<<.+?>>)', text or ''):
        if not tok:
            continue
        bold, color = base_bold, base_color
        if tok.startswith('**') and tok.endswith('**'):
            tok, bold, color = tok[2:-2], True, RED
        elif tok.startswith('~~') and tok.endswith('~~'):
            tok, color = tok[2:-2], RED
        elif tok.startswith('[[') and tok.endswith(']]'):
            tok, bold = tok[2:-2], True
        elif tok.startswith('<<') and tok.endswith('>>'):
            tok, color = tok[2:-2], BLUE
        props = ''
        if bold:
            props += '<w:b/>'
        if color:
            props += '<w:color w:val="%s"/>' % color
        rpr = '<w:rPr>%s</w:rPr>' % props if props else ''
        inner = ''
        for k, seg in enumerate(tok.split('\t')):
            if k:
                inner += '<w:tab/>'
            if seg:
                inner += '<w:t xml:space="preserve">%s</w:t>' % esc(seg)
        out.append('<w:r>%s%s</w:r>' % (rpr, inner))
    return ''.join(out) or '<w:r><w:t/></w:r>'


def para(text='', bold=False, color=None, bullet=False, label=None):
    """One paragraph. `label` is emitted first in black bold (e.g. 'RFE 原文：')."""
    ppr = '<w:pPr>'
    if bullet:
        ppr += '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
    ppr += '<w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>'
    body = ''
    if label:
        body += runs(label, base_bold=True)
    body += runs(text, base_bold=bold, base_color=color)
    return '<w:p>%s%s</w:p>' % (ppr, body)


NUMBERING = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering %s>'
             '<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="singleLevel"/>'
             '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/>'
             '<w:lvlText w:val="&#9679;"/><w:lvlJc w:val="left"/>'
             '<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
             '<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr>'
             '</w:lvl></w:abstractNum>'
             '<w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num></w:numbering>') % NS

STYLES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles %s><w:docDefaults>'
          '<w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Arial"/>'
          '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault>'
          '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>'
          '</w:pPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
          '</w:style></w:styles>') % NS

CT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
      '<Default Extension="xml" ContentType="application/xml"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
      '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
      '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
      '</Types>')

RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')

DRELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
         '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
         '</Relationships>')


def build(spec):
    translate = spec.get('translate', True)
    p = []
    p.append(para('%s RFE 解读+策略' % spec['client'], bold=True))
    p.append(para('File Date：%s' % spec['file_date'], bold=True, color=RED))
    p.append(para('DDL：%s' % spec['ddl'], bold=True, color=RED))
    p.append(para(''))
    for note in spec.get('top_notes', []):
        p.append(para(note, bold=True))

    for sec in spec['sections']:
        p.append(para(sec['heading'], bold=True))
        if sec.get('filed'):
            p.append(para(sec['filed'], label='我们交的：'))
        first_quote = True
        for blk in sec.get('blocks', []):
            if 'list' in blk:
                for item in blk['list']:
                    p.append(para(item, bullet=True))
                continue
            p.append(para(blk.get('en', ''), label='RFE 原文：' if first_quote else None))
            first_quote = False
            if translate and blk.get('zh'):
                p.append(para(blk['zh'], label='翻译：' if not blk.get('continued') else None))
        if sec.get('jiedu'):
            p.append(para(sec['jiedu'], label='解读：'))
        if sec.get('yingdui'):
            p.append(para('', label='应对：'))
            for item in sec['yingdui']:
                p.append(para(item))
        if sec.get('audit'):
            p.append(para('', label='⚠️ 待核实：'))
            for item in sec['audit']:
                p.append(para(item))
        p.append(para(''))

    asks = spec.get('client_asks') or []
    if asks:
        p.append(para('需客户提供', bold=True))
        for item in asks:
            if isinstance(item, dict):
                line = item['item']
                if item.get('why'):
                    line += '　——　' + item['why']
                if item.get('who'):
                    line += '（' + item['who'] + '）'
            else:
                line = item
            p.append(para(line, bullet=True))
    return ''.join(p)


def main():
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2] if len(sys.argv) > 2 else 'jiedu.docx'
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document %s><w:body>%s'
           '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
           '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>'
           '</w:sectPr></w:body></w:document>') % (NS, build(spec))
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CT)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/document.xml', doc)
        z.writestr('word/_rels/document.xml.rels', DRELS)
        z.writestr('word/styles.xml', STYLES)
        z.writestr('word/numbering.xml', NUMBERING)
    print('wrote', out)


if __name__ == '__main__':
    main()
