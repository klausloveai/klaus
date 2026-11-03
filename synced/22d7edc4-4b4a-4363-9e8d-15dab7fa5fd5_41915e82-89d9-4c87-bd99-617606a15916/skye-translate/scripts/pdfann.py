# -*- coding: utf-8 -*-
import fitz, os
AUTHOR='Lingtu Law Office'
def annotate_pdf(path, rules, maxpages=None):
    """rules: list of (search_text, comment). Highlights first match of each and attaches a popup note.
       Falls back to a page-level sticky note if the text can't be located."""
    d=fitz.open(path); added=0; missed=[]
    npages=len(d) if maxpages is None else min(maxpages,len(d))
    for needle,note in rules:
        hit=False
        for pno in range(npages):
            pg=d[pno]
            rects=pg.search_for(needle, quads=False)
            if not rects: continue
            a=pg.add_highlight_annot(rects[:6])
            a.set_info(title=AUTHOR, content=note)
            a.set_colors(stroke=(1,0.92,0.23)); a.update()
            added+=1; hit=True; break
        if not hit:
            pg=d[0]
            a=pg.add_text_annot(fitz.Point(36,36+18*added), note, icon='Comment')
            a.set_info(title=AUTHOR, content=note); a.update()
            added+=1; missed.append(needle[:40])
    d.saveIncr() if d.can_save_incrementally() else d.save(path+'.tmp')
    if not d.can_save_incrementally():
        d.close(); os.replace(path+'.tmp',path)
    else: d.close()
    return added, missed
