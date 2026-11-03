import zipfile, re, html
def docx_text(p):
    try:
        z=zipfile.ZipFile(p); x=z.read('word/document.xml').decode('utf8','ignore')
    except Exception: return ""
    x=re.sub(r'</w:p>','\n',x)
    t=re.sub(r'<[^>]+>','',x)
    return re.sub(r'\s+',' ',html.unescape(t)).strip()
