#!/usr/bin/env python3
"""Scan Google Chat spaces for new messages that @mention Klaus; append to queue as status=new.
No AI. Run by launchd every 5 minutes. Usage: scan.py [--since ISO]"""
import json, sys, datetime as dt
from common import gws, who, KLAUS, STATE, DATA, locked_queue

def iso(t): return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def main():
    now = dt.datetime.now(dt.timezone.utc)
    DATA.mkdir(parents=True, exist_ok=True)
    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    if "--since" in sys.argv:
        since = sys.argv[sys.argv.index("--since") + 1]
    else:
        since = st.get("last_scan") or iso(now)          # first run: no backfill
    since_dt = dt.datetime.fromisoformat(since.replace("Z", "+00:00")) - dt.timedelta(minutes=3)
    since_q = iso(since_dt)

    spaces, tok = [], None
    while True:
        p = {"pageSize": 1000}
        if tok: p["pageToken"] = tok
        d = gws("chat", "spaces", "list", "--params", json.dumps(p))
        spaces += d.get("spaces", [])
        tok = d.get("nextPageToken")
        if not tok: break
    active = [s for s in spaces if s.get("spaceType") != "DIRECT_MESSAGE"
              and s.get("lastActiveTime", "") > since_q]

    found = []
    for s in active:
        try:
            d = gws("chat", "spaces", "messages", "list", "--params",
                    json.dumps({"parent": s["name"], "pageSize": 500,
                                "filter": f'createTime > "{since_q}"'}))
        except Exception as e:
            print("WARN", s["name"], e, file=sys.stderr); continue
        for m in d.get("messages", []):
            if m.get("sender", {}).get("name") == KLAUS: continue
            if not any(a.get("userMention", {}).get("user", {}).get("name") == KLAUS
                       for a in m.get("annotations", [])): continue
            found.append((s, m))

    added = 0
    if found:
        with locked_queue() as q:
            seen = {it["msg"] for it in q}
            nid = max([it["id"] for it in q], default=0)
            for s, m in found:
                if m["name"] in seen: continue
                ctx = context(s["name"], m["createTime"])
                nid += 1; added += 1
                q.append({
                    "id": nid, "status": "new", "msg": m["name"], "space": s["name"],
                    "space_name": s.get("displayName", ""), "thread": m.get("thread", {}).get("name"),
                    "time": m["createTime"], "from": who(m.get("sender")),
                    "from_id": m.get("sender", {}).get("name"),
                    "text": m.get("text", ""),
                    "attachments": [a.get("contentName") for a in m.get("attachment", [])],
                    "context": ctx, "scanned_at": iso(now),
                })
    st["last_scan"] = iso(now); st["last_added"] = added; st["spaces_checked"] = len(active)
    STATE.write_text(json.dumps(st, indent=1))
    print(f"{iso(now)} checked {len(active)} spaces, +{added} mentions")

def context(space, t, n=8):
    """Previous n messages in the space before t (oldest first)."""
    try:
        d = gws("chat", "spaces", "messages", "list", "--params",
                json.dumps({"parent": space, "pageSize": n, "orderBy": "createTime desc",
                            "filter": f'createTime < "{t}"'}))
    except Exception as e:
        return [{"err": str(e)[:200]}]
    out = []
    for m in reversed(d.get("messages", [])):
        out.append({"time": m["createTime"], "from": who(m.get("sender")),
                    "text": m.get("text", "")[:600],
                    "attachments": [a.get("contentName") for a in m.get("attachment", [])]})
    return out

if __name__ == "__main__":
    main()
