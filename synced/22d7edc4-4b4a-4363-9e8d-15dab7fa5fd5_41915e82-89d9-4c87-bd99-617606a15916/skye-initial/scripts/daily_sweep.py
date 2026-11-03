#!/usr/bin/env python3
"""Daily check of the Priority 1-3 cases for new client uploads.

Reads the 法律 tab of 案件总表, takes every row whose Priority is 1, 2 or 3,
opens that case's folder, and reports uploads sitting in 0. Shared Folder /
0. Intake that haven't been archived into 1. Initial yet. If anything is new
since the last run, it mails the digest to the 新材料 list in notify.py.

Usage:
  python3 daily_sweep.py                    # check, mail if there's news
  python3 daily_sweep.py --dry-run          # check, print the mail instead
  python3 daily_sweep.py --no-send          # check, print nothing but JSON
  python3 daily_sweep.py --priorities 1,2   # narrow the sweep

## Why there's a state file

"New material" has to mean new *since we last looked*, not "not yet archived".
A file nobody has had time to file yet is still unarchived tomorrow, and a
digest that re-reports it every morning is a digest people stop opening after
four days. State lives in ~/.local/state/skye-initial/sweep_state.json (override
with EON_STATE_DIR) and records the file ids already reported per case. The
digest still carries a 累计待归档 count so a growing backlog stays visible
without shouting about the same files.

A missing or deleted state file is not an error — the next run simply treats
everything currently unarchived as new. That's the safe direction to fail: it
over-reports once instead of going quiet.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notify  # noqa: E402
from gwslib import GwsError, gws  # noqa: E402
from scan_materials import inventory  # noqa: E402

TRACKING_SHEET = "1hVkR6sLbQossobqyUA4bJ7Qg3P-mrYF2YupMJvdflEQ"
TAB = "法律"
DATA_RANGE = f"{TAB}!A3:V400"

COL = {"name": 0, "priority": 1, "assignee": 2, "case_type": 3,
       "status": 4, "note": 5, "deadline": 6, "folder": 7}

# Cases in these states don't need a materials sweep — the filing is out of our
# hands or the case is over. Sweeping them just pads the digest.
DONE_STATES = {"submitted", "approved", "denied", "terminated"}

FOLDER_ID = re.compile(r"/folders/([A-Za-z0-9_-]+)")


def state_path():
    base = os.environ.get("EON_STATE_DIR",
                          os.path.expanduser("~/.local/state/skye-initial"))
    return os.path.join(base, "sweep_state.json")


def load_state():
    try:
        with open(state_path(), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {"cases": {}}


def save_state(state):
    path = state_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    state["last_run"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)


def cell(row, key):
    idx = COL[key]
    return row[idx].strip() if len(row) > idx and row[idx] else ""


def read_cases(priorities):
    data = gws(["sheets", "+read", "--spreadsheet", TRACKING_SHEET,
                "--range", DATA_RANGE])
    cases, skipped = [], []
    for offset, row in enumerate(data.get("values", [])):
        name = cell(row, "name")
        if not name:
            continue
        prio = cell(row, "priority")
        if prio not in priorities:
            continue
        if cell(row, "status").strip().lower() in DONE_STATES:
            continue
        link = cell(row, "folder")
        hit = FOLDER_ID.search(link)
        entry = {"row": offset + 3, "name": name, "priority": prio,
                 "assignee": cell(row, "assignee"), "case_type": cell(row, "case_type"),
                 "status": cell(row, "status"), "deadline": cell(row, "deadline"),
                 "folder_link": link}
        if not hit:
            # No folder URL means there's nothing to look in. Say so rather than
            # dropping the row — a Priority 1 case with no folder link is itself
            # worth someone's attention.
            entry["problem"] = "案件总表 H 列没有可用的文件夹链接"
            skipped.append(entry)
            continue
        entry["case_root"] = hit.group(1)
        cases.append(entry)
    return cases, skipped


def sweep(priorities):
    cases, skipped = read_cases(priorities)
    state = load_state()
    results = []
    for case in cases:
        row = dict(case)
        try:
            inv = inventory(case["case_root"])
        except GwsError as exc:
            row["problem"] = f"读取文件夹失败：{exc}"
            skipped.append(row)
            continue
        seen = set(state["cases"].get(case["case_root"], {}).get("reported", []))
        pending = inv.get("new_files", [])
        fresh = [f for f in pending if f["id"] not in seen]
        row.update({
            "shared_folder_id": inv.get("shared_folder_id"),
            "checklist_doc": inv.get("checklist_doc"),
            "pending_count": len(pending),
            "fresh": [{"name": f["name"], "source": f["source"],
                       "createdTime": f.get("createdTime"), "link": f["link"]}
                      for f in fresh],
        })
        results.append(row)
        state["cases"].setdefault(case["case_root"], {})["reported"] = sorted(
            seen | {f["id"] for f in pending})
        state["cases"][case["case_root"]]["name"] = case["name"]
    return results, skipped, state


def digest(results, skipped):
    withnews = [r for r in results if r["fresh"]]
    lines = [f"【材料巡检】{datetime.now().strftime('%Y-%m-%d')} "
             f"— Priority 1-3 共 {len(results)} 个案子，{len(withnews)} 个有新材料", ""]
    for r in withnews:
        lines.append(f"■ {r['name']}（{r['case_type']} / P{r['priority']}"
                     + (f" / {r['assignee']}" if r["assignee"] else "") + "）")
        for f in r["fresh"]:
            when = (f.get("createdTime") or "")[:10]
            lines.append(f"    · {f['name']}  [{f['source']}{' ' + when if when else ''}]")
        if r["pending_count"] > len(r["fresh"]):
            lines.append(f"    （该案累计待归档 {r['pending_count']} 件）")
        if r.get("deadline"):
            lines.append(f"    DDL：{r['deadline']}")
        lines.append(f"    {r['folder_link']}")
        lines.append("")
    backlog = [r for r in results if r["pending_count"] and not r["fresh"]]
    if backlog:
        lines.append("— 以下案子有旧的待归档材料，本次无新增：")
        for r in backlog:
            lines.append(f"    {r['name']}：{r['pending_count']} 件待归档")
        lines.append("")
    if skipped:
        lines.append("— 没查成的：")
        for r in skipped:
            lines.append(f"    {r['name']}：{r.get('problem')}")
        lines.append("")
    lines.append("归档和更新材料清单：对 Claude 说「{客户姓名} 有新文件」")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--priorities", default="1,2,3")
    ap.add_argument("--dry-run", action="store_true", help="print the mail, don't send")
    ap.add_argument("--no-send", action="store_true", help="JSON only, no mail at all")
    # Neither --dry-run nor --no-send writes state: a run nobody was told about
    # must not consume tomorrow's alert.
    ap.add_argument("--always-send", action="store_true",
                    help="mail even when there is no new material")
    ap.add_argument("--no-state", action="store_true",
                    help="ignore and don't write the state file (report everything pending)")
    args = ap.parse_args()

    priorities = {p.strip() for p in args.priorities.split(",") if p.strip()}
    if args.no_state:
        globals()["load_state"] = lambda: {"cases": {}}

    try:
        results, skipped, state = sweep(priorities)
    except GwsError as exc:
        sys.exit(f"gws error: {exc}")

    has_news = any(r["fresh"] for r in results)
    body = digest(results, skipped)
    out = {"checked": len(results), "with_new_material": sum(1 for r in results if r["fresh"]),
           "skipped": skipped, "cases": results}

    if not args.no_send and (has_news or args.always_send):
        subject = (f"[材料巡检] {datetime.now().strftime('%m/%d')} "
                   f"{sum(1 for r in results if r['fresh'])} 个案子有新材料")
        out["mail"] = notify.send("new-materials", subject, body, dry_run=args.dry_run)
    else:
        out["mail"] = {"status": "not sent (无新材料)" if not has_news else "not sent (--no-send)"}
        out["digest_preview"] = body

    # State is only recorded when the digest actually went out. A run that
    # sent nothing has not told anybody anything, so marking those files as
    # "reported" would swallow the next real alert — which is exactly what
    # happened the first time --no-send was used to test this.
    if out["mail"].get("status") == "sent" and not args.no_state:
        save_state(state)
    out["state_written"] = out["mail"].get("status") == "sent" and not args.no_state

    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
