# -*- coding: utf-8 -*-
"""compare_sets.py -- answer-by-answer diff of a NEW response set against one we
already served in the same case.

Why this exists (Klaus, 2026-10-12): when a second defendant propounds the same
form interrogatories, the answers SHOULD be near-identical -- the facts do not
change with who is asking, and answering the same question two ways is handed
straight back at deposition. So the review question is not "is this copy-paste?"
but "is every DIFFERENCE justified, and is every thing that CHANGED since the
first verification actually updated?" This prints exactly three lists:

  * asked by one side but not the other  -> questions dropped or newly live
  * IDENTICAL                            -> intentionally ported, no review needed
  * CHANGED                              -> read every one; each needs a reason

A difference is legitimate only if it is (a) a fact that changed since the first
set was verified, (b) a party reference that must now be disambiguated, or
(c) an answer to a question the first set never asked. Anything else is drift.

usage: python3 compare_sets.py <served.pdf> <new_draft.docx>

GOTCHA: pleading line numbers sit in the PDF text with ~7 leading spaces. An
anchor of \\s{0,6} silently leaves them inside every answer and then NOTHING
compares equal -- the first run of this reported "IDENTICAL (0)". Use \\s*.
"""
import re, sys, difflib
from docx import Document

def norm(t):
    t = t.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    t = t.replace('–','-').replace('—','-')
    return re.sub(r'\s+', ' ', t).strip()

def from_pdf(path):
    import subprocess
    raw = subprocess.run(["pdftotext","-layout",path,"-"],capture_output=True,text=True).stdout
    lines=[]
    for ln in raw.split('\n'):
        s=re.sub(r'^\s*\d{1,2}\s{3,}','',ln).strip()
        if not s: continue
        if s.startswith('Docusign Envelope ID'): continue
        if re.fullmatch(r'\d{1,3}', s): continue
        if 'PLAINTIFF YI CONG' in s and 'RESPONSES' in s: continue
        if s == 'SET ONE': continue
        lines.append(s.strip())
    txt='\n'.join(lines)
    out={}
    for m in re.finditer(r'RESPONSE TO FORM INTERROGATORY NO\. ([\d.]+):\s*(.*?)(?=RESPONSE TO FORM INTERROGATORY NO\.|VERIFICATION|\Z)', txt, re.S):
        out[m.group(1)] = norm(m.group(2))
    return out

def from_docx(path):
    d=Document(path); out={}; cur=None; buf=[]
    for p in d.paragraphs:
        t=p.text
        m=re.match(r'RESPONSE TO FORM INTERROGATORY NO\. ([\d.]+):', t.strip())
        if m:
            if cur: out[cur]=norm(' '.join(buf))
            cur=m.group(1); buf=[]
        elif cur:
            if t.strip().upper()=='VERIFICATION': out[cur]=norm(' '.join(buf)); cur=None; continue
            buf.append(t)
    if cur: out[cur]=norm(' '.join(buf))
    return out

served = from_pdf(sys.argv[1])
camden = from_docx(sys.argv[2])
print("served Edpao items:", len(served), "| Camden draft items:", len(camden))
print()
only_served = [k for k in served if k not in camden]
only_camden = [k for k in camden if k not in served]
print("asked by Edpao but NOT by Camden:", ", ".join(only_served) or "none")
print("asked by Camden but NOT by Edpao:", ", ".join(only_camden) or "none")
print()
same=[]; diff=[]
def order(k): return tuple(int(x) for x in k.split('.'))
for k in sorted(set(served) & set(camden), key=order):
    a,b = served[k], camden[k]
    a2 = re.sub(r'«.*?»','',b)  # strip highlight markers if any
    if a == b: same.append(k)
    else: diff.append((k,a,b))
print("IDENTICAL (%d):" % len(same), ", ".join(same))
print()
print("CHANGED (%d):" % len(diff))
for k,a,b in diff:
    sm=difflib.SequenceMatcher(None,a,b)
    print("\n--- NO. %s   (similarity %.3f)" % (k, sm.ratio()))
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': continue
        if max(i2-i1,j2-j1) < 1: continue
        print("    EDPAO : " + (a[i1:i2][:200] or "(nothing)"))
        print("    CAMDEN: " + (b[j1:j2][:200] or "(nothing)"))
