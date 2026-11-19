#!/usr/bin/env python3
"""Queue ops.  queue.py list [status...]   |  queue.py show ID  |  queue.py set ID '<json patch>'
             queue.py count new            |  queue.py after ID   (messages in the space after the mention)"""
import json, sys
from common import read_queue, locked_queue, gws, who

def short(it):
    return (f"#{it['id']} [{it['status']}{'/'+it['category'] if it.get('category') else ''}] "
            f"{it['time'][:16]} {it['from']} @ {it['space_name']}: {it['text'][:120]!r}")

cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
if cmd == "list":
    want = set(sys.argv[2:])
    for it in read_queue():
        if not want or it["status"] in want: print(short(it))
elif cmd == "count":
    print(sum(1 for it in read_queue() if it["status"] in set(sys.argv[2:] or ["new"])))
elif cmd == "show":
    it = next(i for i in read_queue() if i["id"] == int(sys.argv[2]))
    print(json.dumps(it, ensure_ascii=False, indent=1))
elif cmd == "set":
    patch = json.loads(sys.argv[3])
    with locked_queue() as q:
        it = next(i for i in q if i["id"] == int(sys.argv[2]))
        it.update(patch)
    print("ok", sys.argv[2], list(patch))
elif cmd == "after":
    it = next(i for i in read_queue() if i["id"] == int(sys.argv[2]))
    d = gws("chat", "spaces", "messages", "list", "--params",
            json.dumps({"parent": it["space"], "pageSize": 50,
                        "filter": f'createTime > "{it["time"]}"'}))
    for m in d.get("messages", []):
        print(m["createTime"][:19], who(m.get("sender")), "|", m.get("text", "")[:300].replace("\n", " "))
