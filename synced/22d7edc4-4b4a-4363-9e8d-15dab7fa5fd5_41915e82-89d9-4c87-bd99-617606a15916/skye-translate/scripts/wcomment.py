# -*- coding: utf-8 -*-
import zipfile, os, re
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
AUTHOR='Lingtu Law Office'; INITIALS='LL'; DATE='2026-08-19T00:00:00Z'
def _mk(tag,**a):
    el=OxmlElement(tag)
    for k,v in a.items(): el.set(qn(k),v)
    return el
def annotate(path, rules):
    """rules: list of (substring, comment). Comments whole matching paragraph.
       Also strips any yellow highlight in the file."""
    d=Document(path)
    def allp(doc):
        o=list(doc.paragraphs)
        for tb in doc.tables:
            for r in tb.rows:
                for c in r.cells: o+=list(c.paragraphs)
        return o
    paras=allp(d)
    for p in paras:                      # remove existing highlights
        for r in p.runs: r.font.highlight_color=None
    comments=[]; cid=0; used=set()
    for sub,note in rules:
        for p in paras:
            if id(p._p) in used: continue
            if sub.lower() in p.text.lower() and p.runs:
                first=p.runs[0]._element; last=p.runs[-1]._element
                first.addprevious(_mk('w:commentRangeStart',**{'w:id':str(cid)}))
                end=_mk('w:commentRangeEnd',**{'w:id':str(cid)}); last.addnext(end)
                ref=OxmlElement('w:r'); rpr=OxmlElement('w:rPr')
                rpr.append(_mk('w:rStyle',**{'w:val':'CommentReference'})); ref.append(rpr)
                ref.append(_mk('w:commentReference',**{'w:id':str(cid)}))
                end.addnext(ref)
                comments.append((cid,note)); used.add(id(p._p)); cid+=1
                break
    d.save(path)
    if not comments: return 0
    # ---- merge with any pre-existing comments part (never overwrite) ----
    z=zipfile.ZipFile(path,'r')
    existing=None
    if 'word/comments.xml' in z.namelist():
        existing=z.read('word/comments.xml').decode('utf8',errors='ignore')
    doc=z.read('word/document.xml').decode('utf8',errors='ignore')
    base=0
    if existing:
        ids=[int(x) for x in re.findall(r'<w:comment [^>]*w:id="(\d+)"',existing)]
        base=(max(ids)+1) if ids else 0
    if base:                       # shift our ids so they don't collide
        for cid,_ in reversed(comments):
            for tag in ('commentRangeStart','commentRangeEnd','commentReference'):
                doc=doc.replace(f'<w:{tag} w:id="{cid}"/>', f'<w:{tag} w:id="{cid+base}"/>')
    mine=[]
    for cid,txt in comments:
        s2=txt.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        mine.append(f'<w:comment w:id="{cid+base}" w:author="{AUTHOR}" w:initials="{INITIALS}" '
                    f'w:date="{DATE}"><w:p><w:r><w:t xml:space="preserve">{s2}</w:t></w:r></w:p></w:comment>')
    if existing:
        merged=existing.replace('</w:comments>',''.join(mine)+'</w:comments>')
    else:
        merged=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<w:comments xmlns:w="{W}">'+''.join(mine)+'</w:comments>')
    tmp=path+'.tmp'; zo=zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED); seen=set()
    for it in z.infolist():
        if it.filename in seen: continue
        seen.add(it.filename)
        if it.filename=='word/comments.xml':      data=merged.encode('utf8')
        elif it.filename=='word/document.xml':    data=doc.encode('utf8')
        elif it.filename=='[Content_Types].xml':
            t=z.read(it).decode('utf8')
            if 'comments+xml' not in t:
                t=t.replace('</Types>','<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/></Types>')
            data=t.encode('utf8')
        elif it.filename=='word/_rels/document.xml.rels':
            t=z.read(it).decode('utf8')
            if 'comments.xml' not in t:
                t=t.replace('</Relationships>','<Relationship Id="rIdCmtX" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/></Relationships>')
            data=t.encode('utf8')
        else: data=z.read(it)
        zo.writestr(it,data)
    if 'word/comments.xml' not in seen: zo.writestr('word/comments.xml',merged)
    z.close(); zo.close(); os.replace(tmp,path)
    return len(comments)
