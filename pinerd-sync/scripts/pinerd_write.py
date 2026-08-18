#!/usr/bin/env python3
"""PI Nerd KB sync — STEP 2: write the summarized rows back into the Master Index.

Input: a JSON payload file
{
  "synced":"YYYY-MM-DD",
  "new":[ {"cat":"Providers & Referrals","title":"...","summary":"...","providers":"","phones":"",
           "warn":"⚠"|"","msgs":3,"tid":"120581402","url":"https://..."} ],
  "upd":{ "120258734": {"append":" ➕ [UPD 8/7/26] ...","extra_msgs":18} },
  "log":[ {"type":"🆕 新主题"|"♻️ 老主题更新","dates":"2026-08-03 → 2026-08-04","cat":"...",
           "title":"...","url":"...","what":"...","n":3} ],
  "providers_new":[ ["Name","Type","Area","Contact","Status","Notes","topic_slug/id"] ],
  "providers_upd":{ "Exact Provider cell text":" ➕[8/2026] ..." }
}
Behaviour: appends the new rows to Sheet1, applies the [UPD] appends in place,
re-sorts Sheet1 by (category order, topic) and renumbers, appends the Updates Log,
and appends/updates the Provider Database + Blacklist & Cautions. Append-only in
spirit: it never deletes a row and never overwrites a summary (it appends to it).

Usage: python3 pinerd_write.py payload.json
"""
import json,re,subprocess,sys

SID="1sbSGUq0Bu3khRoxKLk9wdi0CvDyaeJnF50EehvvS1p4"
CATORD=["Providers & Referrals","Liens & Reductions","Insurance Claims & Coverage",
        "Property Damage / Total Loss / DV","Litigation / Pre-Lit Escalation",
        "Case Screening / Intake / Retainer","Health Insurance & Billing",
        "Medical / Injury Knowledge","Practice Ops / Software / Vendors",
        "Community / Admin / Events","Misc / Other"]

def gws(args,params,body=None):
    cmd=["gws"]+args+["--params",json.dumps(params)]
    if body is not None: cmd+=["--json",json.dumps(body)]
    p=subprocess.run(cmd,capture_output=True,text=True)
    s=p.stdout; i=s.find("{")
    return (json.loads(s[i:]) if i>=0 else {}), p.stdout+p.stderr

def get(rng,fmt="FORMATTED_VALUE"):
    r,_=gws(["sheets","spreadsheets","values","get"],{"spreadsheetId":SID,"range":rng,"valueRenderOption":fmt})
    return r.get("values",[])

def put(rng,vals):
    r,raw=gws(["sheets","spreadsheets","values","update"],
              {"spreadsheetId":SID,"range":rng,"valueInputOption":"USER_ENTERED"},{"values":vals})
    ok="updatedCells" in r
    if not ok: print("  !! write failed",rng,raw[-300:])
    return ok

def esc(s): return str(s).replace('"','""')
def tid_of(r): 
    m=re.search(r'/(\d+)\s*$',str(r[8]) if len(r)>8 else '')
    return m.group(1) if m else ''

def main(path):
    P=json.load(open(path))
    synced=P.get("synced")
    rows=[(r+['']*9)[:9] for r in get("Sheet1!A2:I5000","FORMULA")]
    print("Sheet1 existing rows:",len(rows))
    # 1) in-place [UPD] appends
    n=0
    for r in rows:
        t=tid_of(r); u=P.get("upd",{}).get(t)
        if not u: continue
        if u["append"].strip()[:14] in r[3]: continue        # idempotent
        r[3]=str(r[3]).rstrip()+u["append"]
        try: r[7]=int(float(r[7]))+int(u.get("extra_msgs",0))
        except Exception: pass
        n+=1
    print("in-place updates:",n)
    # 2) new rows
    have={tid_of(r) for r in rows}; added=0
    for x in P.get("new",[]):
        if x["tid"] in have: print("  skip dup",x["tid"]); continue
        rows.append(["",x["cat"],f'=HYPERLINK("{x["url"]}","{esc(x["title"])}")',x["summary"],
                     x.get("providers",""),x.get("phones",""),x.get("warn",""),x.get("msgs",""),x["url"]])
        have.add(x["tid"]); added+=1
    print("new rows:",added)
    # 3) sort + renumber + write in chunks
    def key(r):
        c=r[1]; ci=CATORD.index(c) if c in CATORD else 99
        m=re.search(r'","(.*)"\)$',str(r[2]))
        return (ci,((m.group(1) if m else str(r[2])).replace('""','"')).lower())
    rows.sort(key=key)
    for i,r in enumerate(rows,1): r[0]=i
    for st in range(0,len(rows),200):
        ch=rows[st:st+200]
        put(f"Sheet1!A{st+2}:I{st+1+len(ch)}",ch)
    print("Sheet1 written:",len(rows),"rows")
    # 4) Updates Log (pure append)
    log=P.get("log",[])
    if log:
        start=len(get("'Updates Log'!A1:A5000"))+1
        put(f"'Updates Log'!A{start}:H{start+len(log)-1}",
            [[synced,x["type"],x["dates"],x.get("cat",""),
              f'=HYPERLINK("{x["url"]}","{esc(x["title"])}")' if x.get("url") else x["title"],
              x["what"],x.get("n",""),x.get("url","")] for x in log])
        print("Updates Log rows appended:",len(log),"at",start)
    # 5) Provider DB / Blacklist
    pu=P.get("providers_upd",{})
    if pu:
        for tab in ["Provider Database","Blacklist & Cautions"]:
            v=get(f"'{tab}'!A1:G500")
            for i,r in enumerate(v[1:],start=2):
                name=r[0] if r else ''
                if name in pu:
                    note=r[5] if len(r)>5 else ''
                    if pu[name].strip()[:12] in note: continue
                    put(f"'{tab}'!F{i}",[[note.rstrip()+pu[name]]]); print(f"  {tab} row {i}: {name}")
    pn=P.get("providers_new",[])
    if pn:
        rows2=[[a,b,c,d,e,f,f'=HYPERLINK("https://nerdgroup.co/g/Nerds/topic/{g}","source")'] for (a,b,c,d,e,f,g) in pn]
        st=len(get("'Provider Database'!A1:A500"))+1
        put(f"'Provider Database'!A{st}:G{st+len(rows2)-1}",rows2); print("Provider DB appended:",len(rows2))
        cau=[r for r in rows2 if r[4] in ("Caution","Blacklist","Note")]
        if cau:
            st2=len(get("'Blacklist & Cautions'!A1:A500"))+1
            put(f"'Blacklist & Cautions'!A{st2}:G{st2+len(cau)-1}",cau); print("Blacklist appended:",len(cau))
    print("DONE")

if __name__=="__main__": main(sys.argv[1])
