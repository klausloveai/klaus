# fill_disc001.py — fill the Judicial Council Form Interrogatories DISC-001 (static XFA form).
# Method: update the XFA `datasets` packet (what Adobe reads) + set AcroForm checkbox /AS+/V
# as a backstop, keeping XFA. Do NOT drop XFA + NeedAppearances (renders as tofu in poppler).
# PER CASE, edit:
#   - SRC / OUT paths
#   - CB{}: KEEP only the checkboxes the attorney's Sec. 4(a)(2) attachment lists (the CB map
#     below is the full DISC-001 field->onstate reference; comment out boxes not being checked).
#   - TX{}: header/caption values (court line = "IN THE MATTER OF THE ARBITRATION BETWEEN",
#     short title "<Last> v. <Insurer short>", CASE NUMBER blank, Set No. ONE, party names).
#   - Definitions field -> '2' (custom INCIDENT per the attachment).
# The CB map's field names are universal to DISC-001; the on-state per box (Yes/1/2) is fixed.
# Verify after: the datasets values are set; open in Adobe to confirm rendering (poppler tofus this form).

# -*- coding: utf-8 -*-
import re
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject, TextStringObject, DictionaryObject
import xml.etree.ElementTree as ET

SRC="/Users/klaus/Downloads/Jiayu Ma-Request/FROG (fill in Adobe)/DISC-001 Form Interrogatories - BLANK fillable.pdf"
OUT="/Users/klaus/Downloads/Jiayu Ma-Request/FROG (fill in Adobe)/Jiayu Ma - DISC-001 Form Interrogatories (FILLED).pdf"

# ---- checkbox targets: widget fullname -> on-value (no slash) ----
CB={
 r'DISC-001[0].Page2[0].Page2[0].List1\.0[0].item1\.0[0].Identity[0]':'1',
 r'DISC-001[0].Page3[0].Set1[0].List3\.1[0].GenBkgrdBiz[0]':'Yes',
 r'DISC-001[0].Page3[0].Set1[0].List3\.2[0].GenBkgrdBiz2[0]':'Yes',
 r'DISC-001[0].Page3[0].Set1[0].List3\.3[0].GenBkgrdBiz3[0]':'Yes',
 r'DISC-001[0].Page3[0].List3\.4[0].GenBkgrdBiz4[0]':'Yes',
 r'DISC-001[0].Page3[0].List3\.5[0].GenBkgrdBiz5[0]':'Yes',
 r'DISC-001[0].Page3[0].List3\.6[0].GenBkgrdBiz6[0]':'Yes',
 r'DISC-001[0].Page3[0].List3\.7[0].GenBkgrdBiz7[0]':'Yes',
 r'DISC-001[0].Page3[0].List4\.1[0].Insurance[0]':'Yes',
 r'DISC-001[0].Page3[0].List4\.2[0].item4\.2[0].Insurance2[0]':'Yes',
 r'DISC-001[0].Page5[0].List12\.1[0].InvestigatGen[0]':'Yes',
 r'DISC-001[0].Page5[0].List12\.2[0].InvestigatGen2[0]':'Yes',
 r'DISC-001[0].Page5[0].List12\.3[0].InvestigatGen3[0]':'Yes',
 r'DISC-001[0].Page6[0].Set1[0].List12\.4[0].InvestigatGen[0]':'1',
 r'DISC-001[0].Page6[0].Set1[0].List12\.5[0].CheckBox34[0]':'1',
 r'DISC-001[0].Page6[0].Set1[0].List12\.6[0].CheckBox35[0]':'1',
 r'DISC-001[0].Page6[0].Set1[0].List12\.7[0].CheckBox36[0]':'1',
 r'DISC-001[0].Page6[0].Set1[0].List13\.1[0].CheckBox37[0]':'1',
 r'DISC-001[0].Page6[0].List13\.2[0].CheckBox38[0]':'1',
 r'DISC-001[0].Page6[0].List14\.1[0].item14\.1[0].StatRegViolation[0]':'Yes',
 r'DISC-001[0].Page6[0].List14\.2[0].StatRegViolation2[0]':'Yes',
 r'DISC-001[0].Page6[0].List15\.1[0].DSADefenses[0]':'Yes',
 r'DISC-001[0].Page6[0].List16\.1[0].DefContend[0]':'Yes',
 r'DISC-001[0].Page6[0].List16\.2[0].DefContend2[0]':'Yes',
 r'DISC-001[0].Page7[0].Set1[0].List16\.3[0].DefContend3[0]':'Yes',
 r'DISC-001[0].Page7[0].Set1[0].List16\.4[0].DefContend4[0]':'Yes',
 r'DISC-001[0].Page7[0].Set1[0].List16\.5[0].DefContend5[0]':'Yes',
 r'DISC-001[0].Page7[0].Set1[0].List16\.6[0].DefContend6[0]':'Yes',
 r'DISC-001[0].Page7[0].Set1[0].List16\.7[0].DefContend7[0]':'Yes',
 r'DISC-001[0].Page7[0].List16\.8[0].DefContend8[0]':'Yes',
 r'DISC-001[0].Page7[0].List16\.9[0].DefContend9[0]':'Yes',
 r'DISC-001[0].Page7[0].List16\.10[0].DefContend10[0]':'Yes',
 r'DISC-001[0].Page7[0].List17\.1[0].RespReqAd[0]':'Yes',
 r'DISC-001[0].Page2[0].Page2[0].Set1[0].List4[0].Lia[0].Definitions[0]':'2',
}
# ---- text targets: widget fullname -> value ----
TX={
 r'DISC-001[0].Page1[0].Table[0].Info2[0].TextField4[0]':'IN THE MATTER OF THE ARBITRATION BETWEEN',
 r'DISC-001[0].Page1[0].Table[0].TextField8[0]':'Ma v. Tesla Ins. Co.',
 r'DISC-001[0].Page1[0].Table[0].Info3[0].TextField5[0]':'Claimant Jiayu Ma',
 r'DISC-001[0].Page1[0].Table[0].Info3[0].TextField6[0]':'Respondent Tesla Insurance Company',
 r'DISC-001[0].Page1[0].Table[0].Info3[0].TextField7[0]':'ONE',
 r'DISC-001[0].Page1[0].Table[0].Cell[0].CaseNumber[0]':'',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].AttyBarNo[0]':'354175',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].Name[0]':'Hernán S. Simó',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].AttyFirm[0]':'LAW OFFICE OF SHENQI CAI APC',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].Street[0]':'13191 Crossroads Pkwy N, Suite 295',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].City[0]':'City of Industry',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].State[0]':'CA',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].Zip[0]':'91746',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].Phone[0]':'(626) 479-2207',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].Fax[0]':'(626) 479-2207',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].Email[0]':'hernan.s@lingtulaw.com; klaus@lingtulaw.com',
 r'DISC-001[0].Page1[0].Table[0].AttyPartyInfo[0].AttyFor[0]':'Claimant, Jiayu Ma',
 r'DISC-001[0].Page2[0].Page2[0].Set1[0].List4[0].Lia[0].FillText36[0]':
   "See the attachment labeled “Sec. 4(a)(2)” served herewith, which defines INCIDENT and states the substitutions required because this matter is an arbitration under Insurance Code section 11580.2(f).",
}

def to_path(fullname):
    # split on dots not preceded by backslash; drop [0]; unescape \.
    toks=re.split(r'(?<!\\)\.', fullname)
    toks=[t.replace('[0]','').replace('\\.', '.') for t in toks]
    return toks  # includes leading 'DISC-001'

r=PdfReader(SRC)
acro=r.trailer['/Root']['/AcroForm']
xfa=acro['/XFA']
packets={}; order=[]
for i in range(0,len(xfa),2):
    nm=str(xfa[i]); order.append(nm); packets[nm]=xfa[i+1]
ds_bytes=packets['datasets'].get_object().get_data()
ds_text=ds_bytes.decode('utf-8')

# --- edit datasets XML ---
ET.register_namespace('xfa','http://www.xfa.org/schema/xfa-data/1.0/')
root=ET.fromstring(ds_text)
XFA_NS='{http://www.xfa.org/schema/xfa-data/1.0/}'
data_el=root.find(XFA_NS+'data')
disc=data_el.find('DISC-001')

def navigate(root_el, toks):
    cur=root_el
    for t in toks[1:]:  # skip 'DISC-001'
        nxt=None
        for ch in list(cur):
            if ch.tag==t: nxt=ch; break
        if nxt is None: return None
        cur=nxt
    return cur

miss=[]
for fn,val in {**CB, **TX}.items():
    el=navigate(disc, to_path(fn))
    if el is None: miss.append(fn); continue
    el.text=val
print('datasets set:', len(CB)+len(TX)-len(miss), '| missing:', len(miss))
for m in miss: print('  MISS',m)

# fix: Definitions radio binds directly under DISC-001 (value 2 = INCIDENT 4(a)(2))
_dfn=disc.find('Definitions')
if _dfn is not None:
    _dfn.text='2'; print('Definitions set to 2 (datasets)')
else:
    print('Definitions element NOT found under DISC-001')
new_ds=ET.tostring(root, encoding='utf-8', xml_declaration=False)
# write back into the datasets stream object
packets['datasets'].get_object().set_data(new_ds)

# --- also set AcroForm field values (belt & suspenders) ---
def fullname(o):
    parts=[]; name=o.get('/T')
    if name: parts=[str(name)]
    p=o.get('/Parent')
    while p:
        po=p.get_object(); t=po.get('/T')
        if t: parts.insert(0,str(t))
        p=po.get('/Parent')
    return '.'.join(parts)

w=PdfWriter(); w.append(r)
# re-embed edited XFA datasets into writer's acroform
wacro=w._root_object['/AcroForm']
wxfa=wacro['/XFA']
for i in range(0,len(wxfa),2):
    if str(wxfa[i])=='datasets':
        wxfa[i+1].get_object().set_data(new_ds)

cb_on={fn:('/'+v) for fn,v in CB.items()}
setcb=0; settx=0
for page in w.pages:
    an=page.get('/Annots')
    if not an: continue
    for a in an:
        o=a.get_object()
        if o.get('/Subtype')!='/Widget': continue
        fn=fullname(o)
        if fn in cb_on:
            on=cb_on[fn]
            o[NameObject('/AS')]=NameObject(on); o[NameObject('/V')]=NameObject(on)
            par=o.get('/Parent')
            if par: par.get_object()[NameObject('/V')]=NameObject(on)
            setcb+=1
        elif fn in TX:
            o[NameObject('/V')]=TextStringObject(TX[fn])
            par=o.get('/Parent')
            if par: par.get_object()[NameObject('/V')]=TextStringObject(TX[fn])
            settx+=1
print('AcroForm checkboxes set:',setcb,'text set:',settx)
wacro[NameObject('/NeedAppearances')]=BooleanObject(True)

with open(OUT,'wb') as fh: w.write(fh)
print('WROTE', OUT)

# --- verify: re-read datasets from output ---
r2=PdfReader(OUT)
x2=r2.trailer['/Root']['/AcroForm']['/XFA']
for i in range(0,len(x2),2):
    if str(x2[i])=='datasets':
        d2=x2[i+1].get_object().get_data().decode('utf-8')
root2=ET.fromstring(d2); disc2=root2.find(XFA_NS+'data').find('DISC-001')
ok=0
for fn,val in {**CB,**TX}.items():
    el=navigate(disc2,to_path(fn))
    if el is not None and (el.text or '')==val: ok+=1
print('VERIFY datasets in output: matched', ok, 'of', len(CB)+len(TX))
