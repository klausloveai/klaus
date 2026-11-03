"""Place each image on US-Letter page(s), 0.5in margins, centered.
Very tall captures (ar > 2.5) are sliced into full-width segments so they stay legible."""
import fitz, os, math, io
from PIL import Image
PW,PH=612.0,792.0
M=36.0
UW,UH=PW-2*M, PH-2*M
PAGE_AR=UH/UW
def _bytes(im):
    b=io.BytesIO()
    if im.mode in ("RGBA","P","LA"): im=im.convert("RGB")
    im.save(b, format="JPEG", quality=88, optimize=True)
    return b.getvalue()
def image_pages(path, doc):
    im=Image.open(path); im.load()
    w,h=im.size; ar=h/w
    n=math.ceil(ar/PAGE_AR) if ar>2.5 else 1
    seg=h/n
    for i in range(n):
        page=doc.new_page(width=PW,height=PH)
        top=int(i*seg); bot=int(min(h,(i+1)*seg))
        part = im if n==1 else im.crop((0,top,w,bot))
        sw,sh=part.size
        sc=min(UW/sw, UH/sh); dw,dh=sw*sc, sh*sc
        x=(PW-dw)/2; y=(PH-dh)/2
        page.insert_image(fitz.Rect(x,y,x+dw,y+dh), stream=_bytes(part))
    return n
