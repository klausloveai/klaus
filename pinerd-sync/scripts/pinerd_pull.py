#!/usr/bin/env python3
"""PI Nerd KB sync — STEP 1: pull new listserv activity out of klaus@ Gmail.

Reads nothing from the nerdgroup.co website (no login needed): every group message
is delivered to klaus@lingtulaw.com as an individual email, and each Groups.io
footer carries `Mute This Topic: https://nerdgroup.co/mt/<topicId>/<subId>`, which
gives us the canonical topic id.

Writes into the work dir:
  threads.json  - one record per thread (topic id, url, dates, msg count, body)
  digest.txt    - human/AI-readable digest to summarize from

Usage:  python3 pinerd_pull.py [--since YYYY/MM/DD] [--workdir DIR]
Without --since it resumes from the newest date in the sheet's "Updates Log" tab.
"""
import argparse,base64,collections,datetime,html,json,os,re,subprocess,sys
import concurrent.futures as cf

SID="1sbSGUq0Bu3khRoxKLk9wdi0CvDyaeJnF50EehvvS1p4"   # PI Nerd — Knowledge Base (Master Index)

def gws(args, params, body=None):
    cmd=["gws"]+args+["--params",json.dumps(params)]
    if body is not None: cmd+=["--json",json.dumps(body)]
    p=subprocess.run(cmd,capture_output=True,text=True)
    s=p.stdout; i=s.find("{")
    if i<0: return {}
    try: return json.loads(s[i:])
    except Exception: return {}

def sheet_get(rng,fmt="FORMATTED_VALUE"):
    return gws(["sheets","spreadsheets","values","get"],
               {"spreadsheetId":SID,"range":rng,"valueRenderOption":fmt}).get("values",[])

def last_sync_date():
    v=sheet_get("'Updates Log'!A2:A5000")
    ds=[r[0] for r in v if r and re.match(r'^\d{4}-\d{2}-\d{2}$',str(r[0]).strip())]
    if not ds: return None
    d=datetime.date.fromisoformat(max(ds))
    return d.strftime("%Y/%m/%d")          # inclusive — re-reading a day is harmless (we dedupe)

def known_topic_ids():
    ids=set()
    for r in sheet_get("'Sheet1'!I2:I5000"):
        if r:
            m=re.search(r'/(\d+)\s*$',str(r[0]))
            if m: ids.add(m.group(1))
    return ids

# ---------- Gmail ----------
def list_msgs(q):
    out=[];tok=None
    while True:
        par={"userId":"me","q":q,"maxResults":500}
        if tok: par["pageToken"]=tok
        r=gws(["gmail","users","messages","list"],par)
        out+=r.get("messages",[]); tok=r.get("nextPageToken")
        if not tok: break
    return out

def _walk(p,acc):
    if p.get("mimeType","").startswith("text/") and p.get("body",{}).get("data"):
        acc.append((p["mimeType"],p["body"]["data"]))
    for x in p.get("parts") or []: _walk(x,acc)

def _strip_html(s):
    s=re.sub(r'(?is)<(script|style).*?</\1>','',s)
    s=re.sub(r'(?i)<br\s*/?>','\n',s); s=re.sub(r'(?i)</p>','\n\n',s)
    return re.sub(r'\n{3,}','\n\n',html.unescape(re.sub(r'<[^>]+>','',s)))

CUT=re.compile(r'(-=-=-=|Links: You receive|CONFIDENTIALITY|NOTICE:|Disclaimer:|This e-?mail (transmission|and any files)|IRS Circular)',re.I)
SIGN=re.compile(r'(?im)^\s*(thank you|thanks so much|thanks|best regards|best,|best\b|regards|sincerely|warm regards|cheers|much appreciated|appreciate it)\s*[,!.]?\s*$')

def clean(t):
    t='\n'.join(l for l in t.split('\n') if not l.strip().startswith('>'))
    m=CUT.search(t)
    if m: t=t[:m.start()]
    m=SIGN.search(t)
    if m and m.start()>60: t=t[:m.start()]
    t=re.sub(r'(?im)^\s*(sent from my \w+.*|On \w{3},? \w{3} \d+, 20\d\d at .*wrote:.*)$','',t)
    return re.sub(r'\n{3,}','\n\n',t).strip()

def fetch(m):
    r=gws(["gmail","users","messages","get"],{"userId":"me","id":m["id"],"format":"full"})
    h={x["name"]:x["value"] for x in r.get("payload",{}).get("headers",[])}
    acc=[];_walk(r.get("payload",{}),acc)
    raw_plain=raw_html=""
    for mt,data in acc:
        try: raw=base64.urlsafe_b64decode(data+"==").decode("utf-8","replace")
        except Exception: continue
        if mt=="text/plain" and len(raw)>len(raw_plain): raw_plain=raw
        elif mt=="text/html" and not raw_html: raw_html=raw
    full=raw_plain or _strip_html(raw_html)
    tm=re.search(r'nerdgroup\.co/mt/(\d+)/',full)
    return {"id":m["id"],"topic":tm.group(1) if tm else "",
            "date":datetime.datetime.fromtimestamp(int(r.get("internalDate","0"))/1000).isoformat(timespec="minutes"),
            "from":re.sub(r'\s*via nerdgroup\.co.*','',h.get("From","").split('<')[0].strip().strip('"')),
            "subject":h.get("Subject",""),"txt":clean(full)[:12000]}

def slugify(subj):
    s=re.sub(r'^(Re|RE|Fwd|FW):\s*','',subj.strip())
    s=re.sub(r'[^A-Za-z0-9]+','_',s).strip('_').lower()
    return (s[:30].rstrip('_') or 'topic')

def norm(s):
    s=re.sub(r'^(Re|RE|Fwd|FW):\s*','',s.strip())
    return re.sub(r'[^a-z0-9]+','',s.lower())[:60]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--since"); ap.add_argument("--workdir",default=".")
    a=ap.parse_args()
    os.makedirs(a.workdir,exist_ok=True)
    since=a.since or last_sync_date() or (datetime.date.today()-datetime.timedelta(days=14)).strftime("%Y/%m/%d")
    q=f"from:nerdgroup.co after:{since}"
    print("query:",q,flush=True)
    msgs=list_msgs(q); print("emails:",len(msgs),flush=True)
    if not msgs:
        json.dump([],open(os.path.join(a.workdir,"threads.json"),"w")); open(os.path.join(a.workdir,"digest.txt"),"w").write("")
        print("nothing new"); return
    with cf.ThreadPoolExecutor(8) as ex: rows=list(ex.map(fetch,msgs))
    known=known_topic_ids()
    groups=collections.defaultdict(list)
    for m in rows: groups[m["topic"] or norm(m["subject"])].append(m)
    out=[]
    for k,ms in groups.items():
        ms.sort(key=lambda x:x["date"])
        subj=re.sub(r'^(Re|RE|Fwd|FW):\s*','',ms[0]["subject"]).strip()
        tid=next((m["topic"] for m in ms if m["topic"]),"")
        seen=set();parts=[]
        for m in ms:
            key=re.sub(r'\W','',m["txt"])[:80]
            if not m["txt"] or key in seen: continue
            seen.add(key); parts.append(f"[{m['from']}] {m['txt'][:1100]}")
        out.append({"tid":tid,"subj":subj,"is_new":bool(tid) and tid not in known,
                    "url":f"https://nerdgroup.co/g/Nerds/topic/{slugify(subj)}/{tid}" if tid else "",
                    "first":ms[0]["date"][:16],"last":ms[-1]["date"][:16],
                    "n_emails":len(ms),"body":"\n".join(parts)[:2600]})
    out.sort(key=lambda x:x["first"])
    json.dump(out,open(os.path.join(a.workdir,"threads.json"),"w"),indent=0)
    with open(os.path.join(a.workdir,"digest.txt"),"w") as f:
        for x in out:
            f.write("="*80+f"\n[{'NEW' if x['is_new'] else 'UPD'}] {x['tid']} | {x['subj']} | {x['first']}→{x['last']} | {x['n_emails']}msgs\n{x['body']}\n")
    print(f"threads: {len(out)}  (new {sum(1 for x in out if x['is_new'])}, existing-with-replies {sum(1 for x in out if not x['is_new'])})")
    print("digest chars:",sum(len(x['body']) for x in out))

if __name__=="__main__": main()
