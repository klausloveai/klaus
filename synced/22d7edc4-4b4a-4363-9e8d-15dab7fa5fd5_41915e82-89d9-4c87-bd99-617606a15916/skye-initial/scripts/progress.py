#!/usr/bin/env python3
"""The internal 材料进度 doc: what's required, what came in, what's still missing.

Lives in the case root next to the 材料清单 and is **firm-internal** — the
清单 is the document the client and the meeting work from; this one is the
tracking view, and the two are deliberately different documents rather than
one with a status column bolted on.

  collect  — gather everything needed to write the doc (requirements from the
             材料清单, actual files from 1. Initial, the previous timeline)
  ensure   — find or create "{客户姓名} 材料进度" in the case root

Writing is done with `checklist.py init --force`, which is safe here precisely
because this doc is machine-owned: it carries a "请勿手改" header, discussion
belongs in the 材料清单, and nothing is lost by regenerating it. The one part
that must survive a regeneration is the timeline, so `collect` reads the old
one back out and hands it to you to re-emit.

Usage:
  python3 progress.py collect --case-root <ID>
  python3 progress.py ensure  --case-root <ID> --client-name "Dechao You"
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checklist as cl  # noqa: E402
from gwslib import (  # noqa: E402
    DOC_MIME, FOLDER_MIME, GwsError, gws, list_children,
)
from scan_materials import inventory  # noqa: E402

PROGRESS_SUFFIX = "材料进度"
TIMELINE_HEADER = "时间线："


def find_progress_doc(case_root):
    for f in list_children(case_root, fields="files(id,name,mimeType)"):
        if f["mimeType"] == DOC_MIME and PROGRESS_SUFFIX in f["name"]:
            return f
    return None


def read_timeline(doc_id):
    """The timeline bullets from the existing progress doc, oldest first."""
    if not doc_id:
        return []
    paras = cl.paragraphs(cl.get_doc(doc_id))
    out, inside = [], False
    for p in paras:
        text = p["text"].strip()
        if not p["bullet"] and text:
            inside = text.startswith(TIMELINE_HEADER.rstrip("："))
            continue
        if inside and text:
            out.append(text)
    return out


def archive_tree(initial_id):
    """criterion folder -> item folder -> [file names]. Loose files under a key of ''."""
    tree = {}
    if not initial_id:
        return tree
    for crit in list_children(initial_id, fields="files(id,name,mimeType)"):
        if crit["mimeType"] != FOLDER_MIME:
            continue
        items = {}
        for child in list_children(crit["id"], fields="files(id,name,mimeType)"):
            if child["mimeType"] == FOLDER_MIME:
                items[child["name"]] = [
                    g["name"] for g in list_children(child["id"], fields="files(id,name,mimeType)")
                    if g["mimeType"] != FOLDER_MIME]
            else:
                items.setdefault("", []).append(child["name"])
        tree[crit["name"]] = items
    return tree


def checklist_outline(doc_id):
    """The 材料清单 as sections -> bullet lines, with their status markers.

    This is the requirements side of the progress doc. Reading it back rather
    than re-deriving requirements from the case type matters: staff prune and
    add items during the client meeting, and the progress doc has to track what
    this case actually needs, not what the template said it would.
    """
    if not doc_id:
        return []
    paras = cl.paragraphs(cl.get_doc(doc_id))
    sections, current = [], None
    for p in paras:
        text = p["text"].rstrip()
        if not text.strip():
            continue
        if not p["bullet"]:
            if text.strip() == "________________":
                continue
            current = {"section": text.strip(), "items": []}
            sections.append(current)
            continue
        if current is None:
            continue
        current["items"].append({
            "text": text.strip(),
            "level": p["level"],
            "done": ("✅" in text) or ("（已有）" in text) or ("(已有)" in text),
        })
    # Everything before the first section header is the title/meta block.
    return [s for s in sections if s["items"]]


def cmd_collect(args):
    inv = inventory(args.case_root)
    checklist = inv.get("checklist_doc")
    progress = find_progress_doc(args.case_root)
    out = {
        "case_root": args.case_root,
        "case_root_link": inv["case_root_link"],
        "checklist_doc": checklist,
        "progress_doc": ({"id": progress["id"], "name": progress["name"],
                          "link": f"https://docs.google.com/document/d/{progress['id']}/edit"}
                         if progress else None),
        "previous_timeline": read_timeline(progress["id"] if progress else None),
        "checklist": checklist_outline(checklist["id"] if checklist else None),
        "archived": archive_tree(inv.get("initial_folder_id")),
        "pending_uploads": [{"name": f["name"], "source": f["source"],
                             "createdTime": f.get("createdTime")}
                            for f in inv.get("new_files", [])],
        "archived_file_count": inv.get("initial_file_count", 0),
    }
    done = sum(1 for s in out["checklist"] for i in s["items"]
               if i["level"] == 0 and i["done"])
    total = sum(1 for s in out["checklist"] for i in s["items"] if i["level"] == 0)
    out["headline"] = {"top_level_items": total, "marked_done": done}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()


def cmd_ensure(args):
    existing = find_progress_doc(args.case_root)
    if existing:
        print(json.dumps({"status": "already there", "id": existing["id"],
                          "name": existing["name"],
                          "link": f"https://docs.google.com/document/d/{existing['id']}/edit"},
                         ensure_ascii=False))
        return
    name = f"{args.client_name} {PROGRESS_SUFFIX}"
    made = gws(["drive", "files", "create"],
               params={"supportsAllDrives": True, "fields": "id,name"},
               body={"name": name, "mimeType": DOC_MIME, "parents": [args.case_root]})
    print(json.dumps({"status": "created", "id": made["id"], "name": made.get("name", name),
                      "link": f"https://docs.google.com/document/d/{made['id']}/edit"},
                     ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("collect", help="requirements + archived files + old timeline")
    p.add_argument("--case-root", required=True)
    p.set_defaults(func=cmd_collect)

    p = sub.add_parser("ensure", help="find or create the 材料进度 doc")
    p.add_argument("--case-root", required=True)
    p.add_argument("--client-name", required=True)
    p.set_defaults(func=cmd_ensure)

    args = ap.parse_args()
    try:
        args.func(args)
    except GwsError as exc:
        sys.exit(f"gws error: {exc}")


if __name__ == "__main__":
    main()
