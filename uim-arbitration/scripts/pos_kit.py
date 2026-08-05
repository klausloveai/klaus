# -*- coding: utf-8 -*-
# POS builder for UIM/UM arbitration service. 3 modes: 'opc' | 'tesla' | 'both'.
# Firm POS template (Drive id) is downloaded + extracted on first use into TPL_DIR.
# Set SERVE_DATE to the ACTUAL mailing/e-service date before building (it prints on
# every POS as a penalty-of-perjury declaration date, so it MUST match reality).
import re, os, shutil, zipfile, subprocess
TPL_DIR=os.environ.get('POS_TPL_DIR','/tmp/postpl_clean')
POS_TEMPLATE_DRIVE_ID='1yHMojbfNpE_C6aeZ30Td7qXypwLp0sok'  # "Proof of Service - TEMPLATE (fillable, highlighted).docx"
SERVE_DATE=os.environ.get('SERVE_DATE','')  # e.g. 'August 5, 2026' — REQUIRED, set before use

def ensure_template():
    """Download + extract the firm POS template into TPL_DIR if missing."""
    if os.path.exists(TPL_DIR+'/word/document.xml'): return
    os.makedirs(TPL_DIR, exist_ok=True)
    docx='/tmp/_pos_template.docx'
    subprocess.run(['gws','drive','files','get','--params',
        '{"fileId":"%s","alt":"media","supportsAllDrives":true}'%POS_TEMPLATE_DRIVE_ID,
        '-o',docx], check=True, capture_output=True)
    with zipfile.ZipFile(docx) as z: z.extractall(TPL_DIR)
    # shorten the 28-underscore signature line so it doesn't wrap in narrow pleading margins
    xp=TPL_DIR+'/word/document.xml'; t=open(xp,encoding='utf-8').read()
    t=t.replace('____________________________','________________________')
    open(xp,'w',encoding='utf-8').write(t)
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
OUTSIDE={
 '{{DECLARANT NAME}}':'Klaus Liu',
 '{{CASE NAME}}':'Jiayu Ma v. Tesla Insurance Company',
 '{{COURT &amp; CASE NO. (or: In the Matter of the Arbitration... Claim No. ___)}}':
   'In the Matter of the Arbitration Pursuant to California Insurance Code § 11580.2(f); Claim No. CL-70-93NTRL-1',
}
def _P(runs): return ('<w:p><w:pPr><w:pStyle w:val="Normal"/><w:spacing w:lineRule="auto" w:line="240"/><w:ind w:end="90"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr>'+runs+'</w:p>')
def _R(text,b=False,i=False):
    rpr='<w:rPr>'+('<w:b/>' if b else '')+('<w:i/>' if i else '')+'<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>'
    return '<w:r>'+rpr+'<w:t xml:space="preserve">'+esc(text)+'</w:t></w:r>'
_BRD='<w:tcBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:start w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:end w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders>'
LB='<w:tcPr><w:tcW w:w="5504" w:type="dxa"/>'+_BRD+'</w:tcPr>'
RB='<w:tcPr><w:tcW w:w="3972" w:type="dxa"/>'+_BRD+'</w:tcPr>'
def _row(left,right): return '<w:tr><w:trPr><w:trHeight w:val="1000" w:hRule="atLeast"/></w:trPr><w:tc>'+LB+left+'</w:tc><w:tc>'+RB+right+'</w:tc></w:tr>'
def service_rows(mode):
    cl=(_P(_R('Daniel A. Everakes, Esq.'))+_P(_R('Colman Perkins Law Group',b=True))
        +_P(_R('500 North Brand Boulevard, Suite 2200'))+_P(_R('Glendale, California 91203'))
        +_P(_R('Telephone: (818) 546-8686'))+_P(_R('Facsimile: N/A'))
        +_P(_R('E-service Address: deverakes@colmanlawgroup.com; trouhani@colmanlawgroup.com')))
    cr=_P(_R('Attorneys for Respondent:',i=True))+_P(_R('Tesla Insurance Company',i=True))
    tl=(_P(_R('Tesla Insurance Company',b=True))+_P(_R('45500 Fremont Blvd'))+_P(_R('Fremont, CA 94538'))
        +_P(_R('Attn: Zamira Sandoval, Claims Adjuster'))
        +_P(_R('Telephone: 801-998-9283'))
        +_P(_R('E-service Address: claims@reply.teslainsuranceservices.com'))
        +_P(_R('(Served by certified mail, return receipt requested, and e-mail)',i=True)))
    tr=_P(_R('Respondent (Insurer)',i=True))
    if mode=='opc': return _row(cl,cr)
    if mode=='tesla': return _row(tl,tr)
    return _row(cl,cr)+_row(tl,tr)
def transform(t,title,set_no,mode):
    t=re.sub(r'<w:r><w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>.*?<w:fldChar w:fldCharType="end"/></w:r>',
             '<w:r><w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:t>'+SERVE_DATE+'</w:t></w:r>',t,flags=re.DOTALL)
    key='By United States mail. '; i=t.find(key)
    ps=max(t.rfind('<w:p>',0,i),t.rfind('<w:p ',0,i)); pe=t.find('</w:p>',i)+len('</w:p>'); para=t[ps:pe]
    para=para.replace('<w:r><w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:u w:val="single"/></w:rPr><w:tab/></w:r>',
                      '<w:r><w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:u w:val="single"/></w:rPr><w:t>X</w:t><w:tab/></w:r>',1)
    para=para.replace('By United States mail. ','By United States mail, certified mail, return receipt requested. ',1)
    t=t[:ps]+para+t[pe:]
    t=re.sub(r',\s*<w:r>[^<]*<w:rPr>[^<]*<w:highlight w:val="yellow"/>[^<]*</w:rPr><w:t>\{\{SET NO\.\}\}</w:t></w:r>',(', '+esc(set_no)) if set_no else '',t)
    t=t.replace('{{SET NO.}}',esc(set_no)).replace('{{TITLE(S) OF DOCUMENT(S) SERVED}}',esc(title))
    for k,v in OUTSIDE.items(): t=t.replace(k,esc(v))
    ti=t.find('<w:tbl>'); tr0=t.find('<w:tr>',ti); tre=t.find('</w:tr>',tr0)+len('</w:tr>')
    t=t[:tr0]+service_rows(mode)+t[tre:]
    return t.replace('<w:highlight w:val="yellow"/>','')
def transform_footer(f,title):
    f=f.replace('{{TITLE(S) OF DOCUMENT(S) SERVED}}',esc(title)).replace('{{SET NO.}}','').replace('<w:highlight w:val="yellow"/>','')
    return f.replace('<w:t xml:space="preserve"> [</w:t>','<w:t xml:space="preserve"></w:t>').replace('<w:t>]</w:t>','<w:t></w:t>')
def _fresh():
    assert SERVE_DATE, "Set SERVE_DATE (env or module var) to the actual service date first."
    ensure_template()
    d='/tmp/_pb2'
    if os.path.exists(d): shutil.rmtree(d)
    shutil.copytree(TPL_DIR,d); return d
def _zip(d,docx):
    if os.path.exists(docx): os.remove(docx)
    with zipfile.ZipFile(docx,'w',zipfile.ZIP_DEFLATED) as z:
        for root,_,files in os.walk(d):
            for fn in files: fp=os.path.join(root,fn); z.write(fp,os.path.relpath(fp,d))
def _pdf(docx,outpdf):
    os.system(f'soffice --headless --convert-to pdf --outdir /tmp "{docx}" >/dev/null 2>&1')
    shutil.move(docx.replace('.docx','.pdf'),outpdf)
def build_standalone_pdf(outpdf,title,set_no,mode):
    d=_fresh()
    xp=d+'/word/document.xml'; _t=open(xp,encoding='utf-8').read(); open(xp,'w',encoding='utf-8').write(transform(_t,title,set_no,mode))
    fp=d+'/word/footer1.xml'; _f=open(fp,encoding='utf-8').read(); open(fp,'w',encoding='utf-8').write(transform_footer(_f,title))
    _zip(d,'/tmp/_sa.docx'); _pdf('/tmp/_sa.docx',outpdf); return outpdf
def build_block(title,set_no,mode):
    d=_fresh(); t=transform(open(d+'/word/document.xml',encoding='utf-8').read(),title,set_no,mode)
    b0=t.find('<w:body>')+len('<w:body>'); s=t.find('<w:sectPr'); return t[b0:s]
def splice(src_docx,outpdf,title,set_no,mode,page_break=False,fix_dated=False):
    block=build_block(title,set_no,mode)
    if page_break: block='<w:p><w:r><w:br w:type="page"/></w:r></w:p>'+block
    d='/tmp/_sp2'
    if os.path.exists(d): shutil.rmtree(d)
    os.makedirs(d)
    with zipfile.ZipFile(src_docx) as z: z.extractall(d)
    xp=d+'/word/document.xml'; t=open(xp,encoding='utf-8').read()
    pi=t.find('PROOF OF SERVICE'); ps=max(t.rfind('<w:p>',0,pi),t.rfind('<w:p ',0,pi)); sect=t.find('<w:sectPr')
    new=t[:ps]+block+t[sect:]
    if fix_dated:
        new=re.sub(r'<w:r\b[^>]*><w:fldChar w:fldCharType="begin"/></w:r>.*?<w:fldChar w:fldCharType="end"/></w:r>',
                   '<w:r><w:t xml:space="preserve">'+SERVE_DATE+'</w:t></w:r>',new,flags=re.DOTALL)
    open(xp,'w',encoding='utf-8').write(new)
    _zip(d,'/tmp/_sp.docx'); _pdf('/tmp/_sp.docx',outpdf); return outpdf
print('pos_kit2 ready')
