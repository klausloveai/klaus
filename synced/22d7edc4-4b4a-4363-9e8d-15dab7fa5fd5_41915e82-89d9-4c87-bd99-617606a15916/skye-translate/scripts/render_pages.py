#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render PDF pages (or a clip) to PNG so a broken text layer can be read visually.
Usage: render_pages.py <file.pdf> <out_dir> [--zoom 3.4] [--pages 1,2] [--clip x0,y0,x1,y1]"""
import sys,os,fitz
def main():
    src=sys.argv[1]; out=sys.argv[2]; a=sys.argv[3:]
    zoom=3.4; pages=None; clip=None
    for i,x in enumerate(a):
        if x=='--zoom': zoom=float(a[i+1])
        if x=='--pages': pages=[int(v)-1 for v in a[i+1].split(',')]
        if x=='--clip': clip=fitz.Rect(*[float(v) for v in a[i+1].split(',')])
    os.makedirs(out,exist_ok=True)
    d=fitz.open(src)
    for i in (pages if pages is not None else range(len(d))):
        pg=d[i]
        pix=pg.get_pixmap(matrix=fitz.Matrix(zoom,zoom),clip=clip)
        p=os.path.join(out,f'p{i+1}.png'); pix.save(p)
        print(p,pix.width,'x',pix.height)
if __name__=='__main__': main()
