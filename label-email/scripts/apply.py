#!/usr/bin/env python3
"""Apply a triage plan to Gmail, then read every thread back to prove it.

Plan file (JSON):
  {"label":   [{"tid": "...", "label_id": "Label_x"}, ...],
   "archive": [{"tid": "...", "no": "M1", "why": "..."}, ...]}

Hard guards (not overridable from the plan):
  * archive = remove INBOX only. Never touches UNREAD, stars or labels.
  * a thread with any star is refused for archive (star = to-do).
  * a label id that does not exist is refused (Klaus renames/deletes labels).
  * --dry-run prints what would happen and changes nothing.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import gmail  # noqa: E402

STAR_SUFFIX = ("_STAR", "_CIRCLE", "_BANG", "_GUILLEMET", "_INFO", "_QUESTION")


def starred(d):
    return any(l == "STARRED" or l.endswith(STAR_SUFFIX)
               for m in d.get("messages", []) for l in m.get("labelIds", []))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    plan = json.load(open(a.plan))
    labels = gmail.labels()

    def do_label(item):
        tid, lid = item["tid"], item["label_id"]
        if lid not in labels:
            return f"REFUSED {tid}: label {lid} 不存在"
        if a.dry_run:
            return f"DRY     {tid} + {labels[lid]}"
        d = gmail.modify_thread(tid, add=[lid])
        ok = d.get("messages") and all(lid in m.get("labelIds", []) for m in d["messages"])
        return f"{'OK     ' if ok else 'FAIL   '}{tid} + {labels[lid]}"

    def do_archive(item):
        tid = item["tid"]
        cur = gmail.get_thread(tid, fmt="minimal")
        tag = f"{item.get('no', '')} {tid}".strip()
        if "messages" not in cur:
            return f"FAIL    {tag}: 读不到对话"
        if starred(cur):
            return f"REFUSED {tag}: 带星（星=待办），不移出"
        if a.dry_run:
            return f"DRY     {tag} 移出 inbox"
        d = gmail.modify_thread(tid, remove=["INBOX"])
        ok = d.get("messages") and all("INBOX" not in m.get("labelIds", []) for m in d["messages"])
        return f"{'OK     ' if ok else 'FAIL   '}{tag} 移出 inbox"

    out = gmail.pmap(do_label, plan.get("label", [])) + gmail.pmap(do_archive, plan.get("archive", []))
    for line in out:
        print(line)
    bad = [l for l in out if l.startswith(("FAIL", "REFUSED"))]
    print(f"\n共 {len(out)} 项，问题 {len(bad)} 项" + ("（dry run，未改动）" if a.dry_run else ""))
    sys.exit(1 if any(l.startswith("FAIL") for l in out) else 0)


if __name__ == "__main__":
    main()
