#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit an exhibit tree for Chinese-language files lacking an English counterpart.
Usage: audit_translations.py <EXHIBITS_ROOT>"""
import os,re,sys,hashlib
IMG=('.png','.jpg','.jpeg','.gif','.webp')
TR=re.compile(r'English Translation|Certified Translation|\(English\)',re.I)
def text(p):
    try:
        if p.lower().endswith('.pdf'):
            import pypdf
            return "".join((x.extract_text() or '') for x in pypdf.PdfReader(p).pages[:10])
        if p.lower().endswith('.docx'):
            from docx import Document
            d=Document(p); t="\n".join(x.text for x in d.paragraphs)
            for tb in d.tables:
                for r in tb.rows: t+=" ".join(c.text for c in r.cells)
            return t
        if p.lower().endswith('.pptx'):
            from pptx import Presentation
            t=''
            for s in Presentation(p).slides:
                for sh in s.shapes:
                    if sh.has_text_frame: t+=sh.text_frame.text+'\n'
            return t
    except Exception: pass
    return ''
def main(root):
    need=[]; imgs=[]; dups={}
    for dp,dns,fns in os.walk(root):
        dns[:]=sorted(x for x in dns if not x.startswith('_'))
        if '/_' in dp: continue
        files=[f for f in sorted(fns) if f!='.DS_Store' and not f.endswith('.md')]
        has=[f for f in files if TR.search(f)]
        for f in files:
            p=os.path.join(dp,f); rel=os.path.relpath(p,root)
            if f.lower().endswith(IMG):
                imgs.append((rel,bool(has)))
                dups.setdefault(hashlib.md5(open(p,'rb').read()).hexdigest(),[]).append(rel)
                continue
            if TR.search(f): continue
            t=text(p); zh=len(re.findall(r'[一-鿿]',t)); en=len(re.findall(r'[A-Za-z]',t))
            if zh>40 and zh/(zh+en+1)>0.25: need.append((rel,zh,bool(has)))
    print('=== 含中文、需确认译文 ===')
    for rel,zh,has in need: print(f'  {"✓" if has else "✗ 缺译文"}  [{zh:>5} 字] {rel}')
    print('\n=== 图片类（需人工打开确认是否含中文） ===')
    for rel,has in imgs: print(f'  {"✓" if has else "?"}  {rel}')
    d=[v for v in dups.values() if len(v)>1]
    if d:
        print('\n=== 重复文件（MD5 相同） ===')
        for g in d:
            for x in g: print('   ',x)
            print('   ---')
    print(f'\n缺译文: {sum(1 for _,_,h in need if not h)} / {len(need)}')
if __name__=='__main__': main(sys.argv[1])
