#!/usr/bin/env python3
"""case-transfer tools — inventory / audit / archive / index.

Usage:  python3 transfer_tools.py <step> <config.json> <workdir>
Steps:  inventory  — list threads (label + keywords), dedupe, participants, recent activity
        audit      — attachments vs Drive case folder by MD5 (zips opened member by member)
        archive    — file missing attachments, export threads to PDF, relabel, write index.json
        index      — build the "00 Email Index" Google Sheet from index.json
Config keys: label_id, label_name, keyword_query, case_folder_id, corr_folder_id,
             exclude_ids[], active_ids{thread_id: existing_pdf_id or ""}, notes{thread_id: text},
             case_title, dest_rules[{match:[substr..], folder_id, folder_name}], skip_rules[substr..],
             drafts_to_archive_attachments (default true)
All Gmail reads are klaus@ (default gws config). Read-only except `archive` and `index`.
"""
import json,subprocess,sys,time,re,html,os,base64,hashlib,zipfile
from email.utils import parsedate_to_datetime,getaddresses
D=json.JSONDecoder()
def call(a,tries=6):
    err=None
    for i in range(tries):
        r=subprocess.run(a,capture_output=True,text=True)
        try:
            o=D.raw_decode(r.stdout[r.stdout.index("{"):])[0]
            if "error" not in o: return o
            err=o["error"]
        except Exception as e: err=f"{e} {r.stderr[-200:]}"
        time.sleep(4*(i+1))
    print("FAIL",a[:5],str(err)[:200],flush=True); return {}
def log(*x): print(*x,flush=True)
def gm(method,params,body=None):
    a=["gws","gmail","users"]+method.split()+["--params",json.dumps(params),"--format","json"]
    if body is not None: a+=["--json",json.dumps(body)]
    return call(a)
def thread_ids(q):
    out=[];tok=None
    while True:
        p={"userId":"me","q":q,"maxResults":500}
        if tok:p["pageToken"]=tok
        o=gm("threads list",p); out+=[t["id"] for t in o.get("threads",[])]; tok=o.get("nextPageToken")
        if not tok: return out
def hdrs(m): return {x["name"]:x["value"] for x in m["payload"]["headers"]}
def day(s):
    try: return parsedate_to_datetime(s).strftime("%Y-%m-%d")
    except Exception: return ""
def drive_md5(folder,path="",acc=None):
    acc={} if acc is None else acc; tok=None
    while True:
        p={"q":f"'{folder}' in parents and trashed=false","fields":"nextPageToken,files(id,name,mimeType,md5Checksum)","pageSize":1000,"supportsAllDrives":True,"includeItemsFromAllDrives":True}
        if tok:p["pageToken"]=tok
        o=call(["gws","drive","files","list","--params",json.dumps(p),"--format","json"])
        for f in o.get("files",[]):
            if f["mimeType"]=="application/vnd.google-apps.folder": drive_md5(f["id"],path+"/"+f["name"],acc)
            elif f.get("md5Checksum"): acc[f["md5Checksum"]]=path+"/"+f["name"]
        tok=o.get("nextPageToken")
        if not tok: return acc

def inventory(C,W):
    lab=thread_ids(f'label:"{C["label_name"]}"')
    kw=thread_ids(f'({C["keyword_query"]}) -label:"{C["label_name"]}"')
    ids=[]; [ids.append(t) for t in lab+kw if t not in ids]
    rows=[]
    for t in ids:
        o=gm("threads get",{"userId":"me","id":t,"format":"metadata","metadataHeaders":["Subject","From","To","Cc","Date"]})
        ms=o.get("messages",[])
        if not ms: rows.append(dict(id=t,err=1)); continue
        parts=set(); last=hdrs(ms[-1])
        for m in ms:
            h=hdrs(m)
            for role in ("From","To","Cc"):
                for nm,ad in getaddresses([h.get(role,"")]):
                    if ad: parts.add((ad.lower(),nm))
        rows.append(dict(id=t,labeled=t in lab,n=len(ms),first=day(hdrs(ms[0]).get("Date","")),last=day(last.get("Date","")),
                         lastfrom=getaddresses([last.get("From","")])[0][1].lower(),subj=hdrs(ms[0]).get("Subject",""),
                         parts=sorted({a for a,_ in parts}),names={a:n for a,n in parts if n}))
        time.sleep(0.3)
    json.dump(rows,open(f"{W}/threads.json","w"),ensure_ascii=False,indent=1)
    log(f"threads: labeled {len(lab)}, keyword-only {len(kw)}, unique {len(ids)}")
    for r in sorted(rows,key=lambda x:x.get("last",""),reverse=True):
        if r.get("err"): log("ERR",r["id"]); continue
        tag="L" if r["labeled"] else "K"
        log(f'{tag} {r["id"]} {r["first"]}→{r["last"]} {r["n"]:>2}封 末:{r["lastfrom"][:26]:26} | {r["subj"][:70]}')
    ppl={}
    for r in rows:
        for a in r.get("parts",[]):
            p=ppl.setdefault(a,dict(n=0,names=set(),last=""))
            p["n"]+=1; p["last"]=max(p["last"],r["last"])
            if r["names"].get(a): p["names"].add(r["names"][a])
    log("\n=== participants (threads, last seen) ===")
    for a,p in sorted(ppl.items(),key=lambda x:-x[1]["n"]): log(f'{p["n"]:>3} {p["last"]} {a} | {"/".join(sorted(p["names"]))[:50]}')

def _att_parts(payload):
    out=[]
    def w(p):
        if p.get("filename") and p.get("body",{}).get("attachmentId"):
            hd={x["name"].lower():x["value"] for x in p.get("headers",[])}
            inline=("inline" in hd.get("content-disposition","").lower() or "content-id" in hd) and p.get("mimeType","").startswith("image/")
            if not inline: out.append(p)
        for q in p.get("parts",[]) or []: w(q)
    w(payload); return out
def audit(C,W):
    rows=[r for r in json.load(open(f"{W}/threads.json")) if not r.get("err") and r["id"] not in set(C.get("exclude_ids",[]))]
    drive=drive_md5(C["case_folder_id"]); log("drive files with md5:",len(drive))
    seen={}; occ=0
    for r in rows:
        o=gm("threads get",{"userId":"me","id":r["id"],"format":"full"})
        for m in o.get("messages",[]):
            h=hdrs(m)
            for p in _att_parts(m["payload"]):
                occ+=1
                a=gm("messages attachments get",{"userId":"me","messageId":m["id"],"id":p["body"]["attachmentId"]})
                if "data" not in a: continue
                data=base64.urlsafe_b64decode(a["data"]); md=hashlib.md5(data).hexdigest()
                if md in seen: continue
                open(f"{W}/att_{md}","wb").write(data)
                seen[md]=dict(md5=md,fn=p["filename"],mime=p.get("mimeType"),size=len(data),date=day(h.get("Date","")),frm=h.get("From",""),tid=r["id"],subj=r["subj"])
        time.sleep(0.4)
    miss=[]
    for a in seen.values():
        if a["md5"] in drive: a["in_drive"]=drive[a["md5"]]; continue
        if a["fn"].lower().endswith(".zip"):
            try:
                z=zipfile.ZipFile(f'{W}/att_{a["md5"]}')
                mem=[i for i in z.infolist() if not i.is_dir() and "__MACOSX" not in i.filename]
                a["zip_missing"]=[i.filename for i in mem if hashlib.md5(z.read(i)).hexdigest() not in drive]
                if not a["zip_missing"]: a["in_drive"]="(all zip members already in Drive)"; continue
            except Exception as e: a["zip_err"]=str(e)
        miss.append(a)
    json.dump(dict(all=list(seen.values()),miss=miss),open(f"{W}/att.json","w"),ensure_ascii=False,indent=1)
    log(f"attachment occurrences {occ} | unique {len(seen)} | already in Drive {len(seen)-len(miss)} | missing {len(miss)}")
    for a in sorted(miss,key=lambda x:x["date"]): log(f'{a["date"]} {a["size"]//1024:>6}KB {a["fn"][:70]} | {a["frm"][:28]}')

CUT=[r'\nOn [^\n]{5,160}wrote:\s*\n',r'\n_{8,}\s*\nFrom:',r'\n-{2,}\s*Original Message',r'\nFrom: [^\n]+\nSent: ',r'NOTICE REGARDING SERVICE',r'Please be advised that I do not accept service',r'CONFIDENTIALITY NOTICE']
def body_text(p):
    pl,ht=[],[]
    def w(x):
        mt=x.get('mimeType',''); dt=x.get('body',{}).get('data')
        if dt and not x.get('filename'):
            t=base64.urlsafe_b64decode(dt+'==').decode('utf8','replace')
            (pl if mt=='text/plain' else ht if mt=='text/html' else []).append(t)
        for q in x.get('parts',[]) or []: w(q)
    w(p)
    if pl: t=pl[0]
    elif ht:
        t=re.sub(r'(?is)<(script|style).*?</\1>','',ht[0]); t=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>','\n',t); t=html.unescape(re.sub(r'<[^>]+>','',t))
    else: t=''
    for c in CUT:
        m=re.search(c,t)
        if m: t=t[:m.start()]
    return re.sub(r'\n{3,}','\n\n',t).strip()
def folder(name,parent):
    o=call(["gws","drive","files","list","--params",json.dumps({"q":f"'{parent}' in parents and name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false","fields":"files(id)","supportsAllDrives":True,"includeItemsFromAllDrives":True}),"--format","json"])
    if o.get("files"): return o["files"][0]["id"]
    return call(["gws","drive","files","create","--json",json.dumps({"name":name,"mimeType":"application/vnd.google-apps.folder","parents":[parent]}),"--params",json.dumps({"supportsAllDrives":True,"fields":"id"}),"--format","json"])["id"]
def upload(path,name,parent,mime):
    tmp="_ct_up"+os.path.splitext(name)[1]; open(tmp,"wb").write(open(path,"rb").read())
    o=call(["gws","drive","files","create","--upload",tmp,"--upload-content-type",mime or "application/octet-stream","--json",json.dumps({"name":name,"parents":[parent]}),"--params",json.dumps({"supportsAllDrives":True,"fields":"id,md5Checksum"}),"--format","json"])
    ok=o.get("md5Checksum")==hashlib.md5(open(tmp,"rb").read()).hexdigest(); os.remove(tmp); return o.get("id"),ok
def archive(C,W):
    os.chdir(os.path.expanduser("~"))
    ARCH=folder("Email Archive",C["corr_folder_id"]); ATT=folder("Attachments",ARCH); log("Email Archive",ARCH,"Attachments",ATT)
    A=json.load(open(f"{W}/att.json"))
    for a in A["miss"]:
        fn=a["fn"]; low=fn.lower()
        if any(s.lower() in low for s in C.get("skip_rules",[".ics","letter header"])) or (low.endswith(".zip") and not a.get("zip_missing")): log("SKIP",fn); continue
        tgt,tname=ATT,"Email Archive/Attachments"
        for r in C.get("dest_rules",[]):
            if any(k.lower() in low for k in r["match"]): tgt,tname=r["folder_id"],r["folder_name"]; break
        base,ext=os.path.splitext(fn)
        name=f'{a["date"]} - {fn}' if tgt==ATT else f'{base} (from email {a["date"]}){ext}'
        fid,ok=upload(f'{W}/att_{a["md5"]}',name,tgt,a.get("mime")); log("ATT","✓" if ok else "✗ MD5",tname,"|",name[:80]); time.sleep(0.5)
    rows=[r for r in json.load(open(f"{W}/threads.json")) if not r.get("err") and r["id"] not in set(C.get("exclude_ids",[]))]
    active=C.get("active_ids",{}); existing=C.get("existing_pdfs",{})
    for fid in [v for v in list(active.values())+list(existing.values()) if v]:
        call(["gws","drive","files","update","--params",json.dumps({"fileId":fid,"addParents":ARCH,"supportsAllDrives":True,"fields":"id"}),"--json","{}","--format","json"])
    index=[]
    for r in rows:
        tid=r["id"]; time.sleep(0.6)
        o=gm("threads get",{"userId":"me","id":tid,"format":"full"}); ms=o.get("messages",[])
        if not ms: index.append(dict(id=tid,subj=r["subj"],err=1)); continue
        gm("threads modify",{"userId":"me","id":tid},{"addLabelIds":[C["label_id"]]})
        parts=[];atts=[];ext=set()
        for i,m in enumerate(ms,1):
            h=hdrs(m)
            for role in ("From","To","Cc"):
                for _,ad in getaddresses([h.get(role,"")]):
                    if ad and not ad.lower().endswith(C.get("firm_domain","lingtulaw.com")): ext.add(ad.lower())
            al=[p["filename"] for p in _att_parts(m["payload"])]; atts+=al
            hd=''.join(f'<tr><td class=k>{k}</td><td>{html.escape(h.get(k,""))}</td></tr>' for k in ('Date','From','To','Cc','Subject') if h.get(k))
            if al: hd+=f'<tr><td class=k>Attachments</td><td>{html.escape("; ".join(al))}</td></tr>'
            parts.append(f'<div class=msg><div class=n>Message {i} of {len(ms)}</div><table>{hd}</table><pre>{html.escape(body_text(m["payload"]))}</pre></div>')
        d0=day(hdrs(ms[0]).get("Date","")) or "0000-00-00"; dl=day(hdrs(ms[-1]).get("Date",""))
        subj=hdrs(ms[0]).get("Subject","(no subject)")
        pdf=active.get(tid) or existing.get(tid) or ""
        if not pdf:
            name=f"{d0} - {re.sub(r'[\\\\/:*?\"<>|]+','-',subj)[:90].strip()}.pdf"
            doc=f'''<!doctype html><meta charset=utf-8><style>@page{{size:letter;margin:.7in}}body{{font-family:Arial,sans-serif;font-size:10pt}}h1{{font-size:13pt;margin:0 0 2px}}.sub{{font-size:9pt;color:#444;margin-bottom:12px}}.msg{{border-top:2px solid #000;padding-top:6px;margin-top:14px}}.n{{font-size:8.5pt;color:#555}}table{{border-collapse:collapse;font-size:9pt;margin-bottom:6px}}td{{padding:1px 6px 1px 0;vertical-align:top}}.k{{font-weight:bold;width:80px}}pre{{white-space:pre-wrap;font-family:Arial,sans-serif;font-size:10pt;margin:0}}</style><h1>{html.escape(subj)}</h1><div class=sub>{html.escape(C["case_title"])} · Exported from klaus@lingtulaw.com, Gmail thread {tid}, on {time.strftime("%m/%d/%Y")} · {len(ms)} message(s) · quoted history and footer notices trimmed</div>{"".join(parts)}'''
            hp=f"{W}/x_{tid}.html"; pp=f"{W}/x_{tid}.pdf"; open(hp,"w").write(doc)
            for _try in range(3):  # Chrome headless can hang on a single page; never block the run
                try:
                    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome","--headless=new" if _try else "--headless","--disable-gpu","--no-pdf-header-footer",f"--print-to-pdf={pp}","file://"+hp],capture_output=True,timeout=90)
                    if os.path.exists(pp) and os.path.getsize(pp)>0: break
                except subprocess.TimeoutExpired:
                    subprocess.run(["pkill","-f",f"print-to-pdf={pp}"]); log("PDF render timeout, retry",_try+1,tid)
            pdf,ok=upload(pp,name,ARCH,"application/pdf"); log("PDF","✓" if ok else "✗ MD5",name[:90])
        index.append(dict(id=tid,first=d0,last=dl,subj=subj,n=len(ms),ext=sorted(ext),atts=sorted(set(atts)),status="Active" if tid in active else "History",pdf=pdf))
    json.dump(dict(arch=ARCH,att=ATT,index=index),open(f"{W}/index.json","w"),ensure_ascii=False,indent=1)
    log("DONE threads",len(index),"errors",[i["id"] for i in index if i.get("err")])

def build_index(C,W):
    J=json.load(open(f"{W}/index.json")); ix=J["index"]; notes=C.get("notes",{})
    rows=[["Status","First date","Last date","Subject","Messages","External parties","Attachments","PDF","Note","Gmail thread id (klaus@)"]]
    for i in sorted([x for x in ix if not x.get("err")],key=lambda x:(x["status"]!="Active",x["first"])):
        link=f'=HYPERLINK("https://drive.google.com/file/d/{i["pdf"]}/view","PDF")' if i.get("pdf") else "live in Gmail only"
        rows.append([i["status"],i["first"],i["last"],i["subj"],i["n"],", ".join(i["ext"]),"; ".join(i["atts"])[:500],link,notes.get(i["id"],""),i["id"]])
    o=call(["gws","sheets","spreadsheets","create","--json",json.dumps({"properties":{"title":f'00 Email Index — {C["case_title"]}'},"sheets":[{"properties":{"title":"Index","gridProperties":{"frozenRowCount":1}}}]}),"--format","json"])
    sid=o["spreadsheetId"]; gid=o["sheets"][0]["properties"]["sheetId"]
    f=call(["gws","drive","files","get","--params",json.dumps({"fileId":sid,"fields":"parents","supportsAllDrives":True}),"--format","json"])
    call(["gws","drive","files","update","--params",json.dumps({"fileId":sid,"addParents":J["arch"],"removeParents":",".join(f.get("parents",[])),"supportsAllDrives":True,"fields":"id"}),"--json","{}","--format","json"])
    call(["gws","sheets","spreadsheets","values","update","--params",json.dumps({"spreadsheetId":sid,"range":"Index!A1","valueInputOption":"USER_ENTERED"}),"--json",json.dumps({"values":rows}),"--format","json"])
    call(["gws","sheets","spreadsheets","batchUpdate","--params",json.dumps({"spreadsheetId":sid}),"--json",json.dumps({"requests":[{"repeatCell":{"range":{"sheetId":gid,"startRowIndex":0,"endRowIndex":1},"cell":{"userEnteredFormat":{"textFormat":{"bold":True},"backgroundColor":{"red":0.9,"green":0.9,"blue":0.9}}},"fields":"userEnteredFormat(textFormat,backgroundColor)"}}]}),"--format","json"])
    log("Email Index",sid)

if __name__=="__main__":
    step,cfg,W=sys.argv[1],os.path.abspath(sys.argv[2]),os.path.abspath(sys.argv[3]); os.makedirs(W,exist_ok=True); C=json.load(open(cfg))
    {"inventory":inventory,"audit":audit,"archive":archive,"index":build_index}[step](C,W)
