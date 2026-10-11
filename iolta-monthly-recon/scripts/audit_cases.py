#!/usr/bin/env python3
"""Per-matter audit for one month: does the Disbursement Sheet hang together, and do the
checks actually written agree with it. The three-way tie cannot see either of these."""
import sys, datetime, json, subprocess, argparse
sys.path.insert(0,'/Users/klaus/.claude/skills/iolta-monthly-recon/scripts')
from build_package import load_journal, num, f, norm, DISB_ID
from collections import defaultdict

ap=argparse.ArgumentParser(); ap.add_argument('--month',required=True); a=ap.parse_args()
out=subprocess.run(["gws","sheets","spreadsheets","values","get","--params",
  json.dumps({"spreadsheetId":DISB_ID,"range":"Internal !A1:R400","valueRenderOption":"UNFORMATTED_VALUE"})],
  capture_output=True,text=True).stdout
j=json.loads(out[out.index("{"):])
ser=lambda s:(datetime.date(1899,12,30)+datetime.timedelta(days=int(s))) if isinstance(s,(int,float)) and s>1000 else None
N=lambda v: float(v) if isinstance(v,(int,float)) else 0.0
sheet={}
for r in j["values"][2:]:
    r=list(r)+['']*18; nm=norm(str(r[1]).strip()); dt=ser(r[0])
    if not nm or nm=='Template' or not dt or dt.strftime('%Y-%m')!=a.month: continue
    sheet[nm]=dict(I=N(r[8]),J=N(r[9]),K=N(r[10]),L=N(r[11]),M=N(r[12]))

print(f'### {a.month} 逐案复核  ({len(sheet)} 案)\n')
print('【A】Disbursement Sheet 自身：结算 I = 客户 J + 费 K + cost L + liens M')
bad=[]
for nm in sorted(sheet):
    s=sheet[nm]; d=round(s['I']-(s['J']+s['K']+s['L']+s['M']),2)
    if abs(d)>=0.005: bad.append((nm,d)); print(f'  ⚠️ {nm:<26} 差 {d:+,.2f}')
print(f'  {"全部自洽 ✓" if not bad else f"{len(bad)} 案不自洽"}')

ws,last=load_journal()
# classify each check: client money / provider lien / MedPay returned to carrier (not a lien)
CLIENT=('Client Recovery','Case Settlement','Client Compensation')
pay=defaultdict(lambda: {'client':0.0,'lien':0.0,'mp':0.0,'rows':[]})
for r in range(10,last+1):
    s=num(ws.cell(r,7).value)
    if not s: continue
    cl=norm(str(ws.cell(r,9).value or ''))
    if cl not in sheet: continue
    purp=f(ws.cell(r,5).value); payee=f(ws.cell(r,2).value); note=f(ws.cell(r,10).value)
    blob=(purp+' '+note).lower()
    if any(k.lower() in purp.lower() for k in CLIENT): kind='client'
    elif 'medpay' in blob.replace(' ','') or 'med pay' in blob or 'subrogation' in blob or 'return' in blob: kind='mp'
    else: kind='lien'
    pay[cl][kind]+=s; pay[cl]['rows'].append((f(ws.cell(r,4).value),s,kind,payee[:30]))

print('\n【B】Sheet 应付 vs Journal 实开支票')
print(f'{"客户":<24}{"客户款表":>11}{"实开":>11}{"差":>8}  {"liens表":>10}{"实开":>10}{"差":>8}  {"MP退还":>9}')
prob=[]
for nm in sorted(sheet):
    s=sheet[nm]; p=pay[nm]
    dc=round(p['client']-s['J'],2); dl=round(p['lien']-s['M'],2)
    flag=''
    if abs(dc)>=0.005 or abs(dl)>=0.005: flag='  ⚠️'; prob.append(nm)
    print(f'{nm[:24]:<24}{s["J"]:>11,.2f}{p["client"]:>11,.2f}{dc:>8,.2f}  {s["M"]:>10,.2f}{p["lien"]:>10,.2f}{dl:>8,.2f}  {p["mp"]:>9,.2f}{flag}')
print()
if prob:
    for nm in prob:
        s=sheet[nm]; p=pay[nm]
        print(f'⚠️ {nm}  结算 {s["I"]:,.2f}  客户款差 {p["client"]-s["J"]:+,.2f}  liens 差 {p["lien"]-s["M"]:+,.2f}')
        for ck,amt,kind,payee in sorted(p['rows'],key=lambda x:-x[1]):
            print(f'     ck {ck:<9}{amt:>11,.2f}  {kind:<7}{payee}')
else:
    print('✓ 全部一致 —— 实开支票与 Disbursement Sheet 分毫不差')
