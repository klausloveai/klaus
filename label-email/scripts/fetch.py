#!/usr/bin/env python3
"""Pull the threads to triage and write one JSON row per thread, numbered in
Gmail display order (newest first), so Klaus can call them by number.

Default scope is Klaus's "inbox": unread conversations in the Primary and
Updates tabs (Updates added 2026-10-26 at his request). Pass --query for
anything else.

  fetch.py --out /path/inbox.json
  fetch.py --query 'in:inbox newer_than:7d' --out ...
"""
import argparse
import base64
import datetime
import html
import json
import re
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
import gmail  # noqa: E402

DEFAULT_Q = "in:inbox is:unread (category:primary OR category:updates)"
STAR_SUFFIX = ("_STAR", "_CIRCLE", "_BANG", "_GUILLEMET", "_INFO", "_QUESTION")
QUOTE_CUT = re.compile(r"\n(On .{5,120}wrote:|From: |-----Original|_{8,}|发件人[:：])")


def _decode(data):
    return base64.urlsafe_b64decode(data).decode("utf-8", "ignore")


def _body(p):
    if p.get("mimeType") == "text/plain" and p.get("body", {}).get("data"):
        return _decode(p["body"]["data"])
    for c in p.get("parts") or []:
        r = _body(c)
        if r:
            return r
    if p.get("mimeType") == "text/html" and p.get("body", {}).get("data"):
        return html.unescape(re.sub(r"<[^>]+>", " ", _decode(p["body"]["data"])))
    return ""


def _files(p, out):
    if p.get("filename"):
        out.append(p["filename"])
    for c in p.get("parts") or []:
        _files(c, out)
    return out


def _own_text(msg):
    b = QUOTE_CUT.split(_body(msg["payload"]))[0]
    b = re.sub(r"<https?://[^>]+>|\[https?://[^\]]+\]", "", b)
    return re.sub(r"\s+", " ", b).strip()


def row(tid, names):
    d = gmail.get_thread(tid)
    if "messages" not in d:
        return {"tid": tid, "error": str(d)[:200]}
    ms = d["messages"]
    last = ms[-1]
    h = {x["name"]: x["value"] for x in last["payload"]["headers"]}
    h0 = {x["name"]: x["value"] for x in ms[0]["payload"]["headers"]}
    all_l = {l for m in ms for l in m.get("labelIds", [])}
    text = _own_text(last)
    to, cc = h.get("To", ""), h.get("Cc", "")
    return {
        "tid": tid,
        "n_msgs": len(ms),
        "date": datetime.datetime.fromtimestamp(int(last["internalDate"]) / 1000).strftime("%m/%d %H:%M"),
        "subject": h0.get("Subject", ""),
        "last_from": h.get("From", ""),
        "last_to": to,
        "last_cc": cc,
        "klaus_in": "TO" if "klaus@" in to.lower() else ("CC" if "klaus@" in cc.lower() else "-"),
        "klaus_named": bool(re.search(r"\bKlaus\b", text)),
        "starred": sorted(l for l in all_l if l == "STARRED" or l.endswith(STAR_SUFFIX)),
        "unread": "UNREAD" in last.get("labelIds", []),
        "label_ids": sorted(l for l in all_l if l.startswith("Label_")),
        "labels": sorted(names.get(l, l) for l in all_l if l.startswith("Label_")),
        "attachments": _files(last["payload"], []),
        # matching text: subject + every message's snippet + last message's own text
        "match_text": " ".join([h0.get("Subject", "")] + [m.get("snippet", "") for m in ms] + [text]),
        "last_text": text[:700],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default=DEFAULT_Q)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cap", type=int, default=500)
    a = ap.parse_args()

    names = gmail.labels()
    tids = gmail.list_threads(q=a.query, cap=a.cap)
    rows = gmail.pmap(lambda t: row(t, names), tids)
    for i, r in enumerate(rows, 1):
        r["no"] = i
    bad = [r for r in rows if "error" in r]
    json.dump({"query": a.query, "labels": names, "threads": rows},
              open(a.out, "w"), ensure_ascii=False, indent=1)

    print(f"query: {a.query}\nthreads: {len(rows)}  (fetch errors: {len(bad)})\n")
    for r in rows:
        if "error" in r:
            print(f"{r['no']:>3}  !! {r['tid']} {r['error']}")
            continue
        star = "⭐" if r["starred"] else "  "
        lab = "; ".join(r["labels"]) or "—"
        print(f"{r['no']:>3} {star} {r['date']}  {r['subject'][:70]}\n"
              f"        last: {r['last_from'][:40]} | Klaus {r['klaus_in']}"
              f"{' · 点名' if r['klaus_named'] else ''} | 🏷 {lab}")


if __name__ == "__main__":
    main()
