#!/usr/bin/env python3
"""Post an APPROVED reply as a NEW top-level message in the case space, as Klaus@ (no thread).
Usage (text in a plain heredoc so the approval prompt shows it):
  python3 send.py ID <<'EOF'
  <users/100654574587915125622> 特斯拉这张 $10,000 ...
  EOF"""
import json, sys, datetime as dt
from common import gws, read_queue, locked_queue

qid = int(sys.argv[1])
text = sys.stdin.read().strip()
it = next(i for i in read_queue() if i["id"] == qid)
if it["status"] == "sent":
    sys.exit(f"#{qid} already sent: {it.get('sent_msg')}")
if not text: sys.exit("empty text")
# messages.create with NO thread -> new top-level message in the space
r = gws("chat", "spaces", "messages", "create", "--params", json.dumps({"parent": it["space"]}),
        "--json", json.dumps({"text": text}, ensure_ascii=False))
with locked_queue() as q:
    x = next(i for i in q if i["id"] == qid)
    x.update(status="sent", sent_msg=r.get("name"), sent_text=text,
             sent_at=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
print("sent", it["space_name"], r.get("name"), "thread:", r.get("thread", {}).get("name"))
