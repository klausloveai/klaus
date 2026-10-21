"""match_internal.py <internal.json> <items.json>
items: [{"ck":"80501","client":"Name","amt":123.45,"kind":"C"|"P"}]  kind C = client recovery (J col only).
Prints every cell in that client's rows whose amount == check amount, with its color.
NOTE: Sheets API omits zero channels, so colors default to 0 (green = {green:1})."""
import json,sys
d=json.load(open(sys.argv[1])); rd=d['sheets'][0]['data'][0]['rowData']
def cell(r,c):
    vs=(rd[r] if r<len(rd) else {}).get('values',[]); return vs[c] if c<len(vs) else {}
def fv(r,c): return (cell(r,c).get('formattedValue') or '').strip()
def bg(r,c):
    b=cell(r,c).get('effectiveFormat',{}).get('backgroundColor',{})
    return (round(b.get('red',0),2),round(b.get('green',0),2),round(b.get('blue',0),2))
NC=len(rd[0]['values']); hdr=[fv(0,c) for c in range(NC)]
def cn(n):
    s=''; n+=1
    while n: n,r=divmod(n-1,26); s=chr(65+r)+s
    return s
def amt(s):
    s=s.replace('$','').replace(',','').strip()
    if s.startswith('(') and s.endswith(')'): s='-'+s[1:-1]
    try: return round(float(s),2)
    except: return None
clients={}
for r in range(1,len(rd)):
    n=fv(r,1)
    if n: clients.setdefault(n.lower(),[]).append(r)
for it in json.load(open(sys.argv[2])):
    name=it['client'].lower(); tgt=it['amt']; kind=it.get('kind','P')
    rows=clients.get(name) or [r for k,v in clients.items() if name in k or k in name for r in v]
    if not rows: print(f"{it['ck']:>7} {it['client']:<20} ${tgt:>10,.2f}  NO-CLIENT-ROW"); continue
    hits=[(r,c) for r in rows for c in (range(9,10) if kind=='C' else range(3,NC)) if amt(fv(r,c))==tgt]
    if not hits: print(f"{it['ck']:>7} {it['client']:<20} ${tgt:>10,.2f}  NO-AMOUNT-MATCH rows={[r+1 for r in rows]}")
    for r,c in hits:
        b=bg(r,c); col={(0.0,1.0,0.0):'GREEN',(1.0,1.0,0.0):'YELLOW',(1.0,1.0,1.0):'WHITE'}.get(b,str(b))
        print(f"{it['ck']:>7} {it['client']:<20} ${tgt:>10,.2f}  {cn(c)}{r+1} [{hdr[c][:30]}] {col}")
