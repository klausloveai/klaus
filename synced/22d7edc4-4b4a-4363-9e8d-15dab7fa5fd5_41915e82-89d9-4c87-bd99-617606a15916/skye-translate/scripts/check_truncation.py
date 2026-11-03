#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flag PDFs whose captured page lost its left margin (body lines start mid-word).
Usage: check_truncation.py <file.pdf> [more.pdf ...]"""
import sys,re,pypdf
# characters that legitimately begin a Chinese sentence/clause
OK_START=set('“「（(【0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
SUSPECT=re.compile(r'^[，。、；：？！）」”】%]')
def check(p):
    r=pypdf.PdfReader(p); bad=[]
    for i,pg in enumerate(r.pages):
        for line in (pg.extract_text() or '').split('\n'):
            s=line.strip()
            if len(s)<12: continue
            if SUSPECT.match(s): bad.append((i+1,s[:60]))
    print(f'\n### {p}  [{len(r.pages)}p]')
    if bad:
        print('  ⚠ 可能左侧截断 / 断句:')
        for pn,s in bad[:8]: print(f'    p{pn}: {s}')
    else:
        print('  未发现明显断句 — 仍需人工核对开头几行是否完整')
if __name__=='__main__':
    for f in sys.argv[1:]: check(f)
