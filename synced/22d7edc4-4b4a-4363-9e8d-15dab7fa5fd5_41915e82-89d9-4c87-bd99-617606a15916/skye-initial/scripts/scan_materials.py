#!/usr/bin/env python3
"""Inventory a 人才移民 case's client materials, and file them into 1. Initial.

Three subcommands, meant to be run in this order:

  inventory  — what's in 0. Shared Folder / 0. Intake / 1. Initial right now,
               and which of those uploads have already been archived
  layout     — create the criterion subfolders inside 1. Initial (idempotent)
  archive    — execute a rename/file plan you wrote after reading the files

The split exists because only one of these steps needs judgement. Deciding
that a PDF is "Orpetron 的评审邀请函" requires reading it; creating a folder and
copying a file does not. So the scripts do the Drive mechanics and the model
does the identification, which is also why `archive` takes a plan file instead
of guessing from filenames — the filenames are exactly the thing being fixed.

## Already-archived detection

Every archived copy carries `appProperties.eon_src` = the id of the client's
original upload. That's what makes the second and every later run cheap: the
inventory subtracts the set of `eon_src` values found under 1. Initial from the
files sitting in 0. Shared Folder, and what's left is genuinely new. Matching
on filename instead would break on the very first run, since renaming the file
is the whole point.

Usage:
  python3 scan_materials.py inventory --case-root <ID>
  python3 scan_materials.py layout --initial-id <ID> --case-type EB1A
  python3 scan_materials.py archive --initial-id <ID> --plan plan.json [--dry-run]

Plan file — a JSON list, one entry per file:
  [
    {"src_id": "1abc...",
     "name":   "奖状-iF Design 2026 Sofia.pdf",
     "path":   ["1. Awards 奖项", "iF Design 2026 - Sofia"],
     "op":     "copy"},
    ...
  ]
`op` is "copy" for anything coming from 0. Shared Folder or 0. Intake (the
client's original stays where they put it) and "move" for a file that is
already somewhere under 1. Initial and only needs renaming/refiling.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gwslib import (  # noqa: E402
    ALL_DRIVES, FOLDER_MIME, GwsError, ensure_folder, file_link, find_child,
    folder_link, gws, list_children, walk,
)

# Criterion subfolders for 1. Initial. Names mirror skye-case-drive's
# criteria_folders.py exactly so the raw-material tree and the exhibit tree
# line up folder-for-folder — when it's time to build exhibits, "which folder
# does this criterion's evidence come from" is answered by reading the name,
# not by remembering a mapping. If that skill's layout changes, change this to
# match.
#
# Numbered here even though the exhibit folders aren't: those get pruned and
# re-lettered as the case narrows, while this tree keeps the full statutory set
# as a collection checklist, and Drive's alphabetical sort would otherwise put
# 高薪 before 奖项 and make the folder list unreadable against the 材料清单.
LAYOUTS = {
    "EB1A": [
        "0. 个人信息",
        "1. Awards 奖项",
        "2. Memberships 协会会员",
        "3. Published Material 媒体报道",
        "4. Judging 评审",
        "5. Original Contributions 原创性重大贡献",
        "6. Scholarly Articles 学术发表",
        "7. Exhibitions 展览展示",
        "8. Leading or Critical Role 重要机构关键角色",
        "9. High Salary 高薪",
        "10. Commercial Success 商业成就",
        "11. Final Merits 推荐信",
        "12. Personal Statement",
    ],
    "O1A": [
        "0. 个人信息",
        "1. Maintenance of Status 身份材料",
        "2. Waiver 工会信",
        "3. 未来计划 Offer",
        "4. Awards 奖项",
        "5. Memberships 协会会员",
        "6. Published Material 媒体报道",
        "7. Judging 评审",
        "8. Original Contributions 原创性重大贡献",
        "9. Scholarly Articles 学术发表",
        "10. Critical or Essential Capacity 关键岗位",
        "11. High Salary 高薪",
    ],
    "O1B": [
        "0. 个人信息",
        "1. Maintenance of Status 身份材料",
        "2. 工会信",
        "3. 未来工作 Offer",
        "4. Lead or Starring Role in Productions 重要作品主演主创",
        "5. National or International Recognition 国家级国际级认可",
        "6. Lead or Critical Role for Distinguished Organizations 知名机构主要角色",
        "7. Major Commercial or Critical Success 商业或口碑成就",
        "8. Significant Recognition from Experts 业内专家认可",
        "9. High Salary 高薪",
    ],
    "NIW": [
        "0. 个人信息",
        "1. A. Endeavor",
        "2. B. Prong 1",
        "3. C. Prong 2",
        "4. D. Prong 3",
        "5. 推荐信",
    ],
}

# Folder names inside the case root, as skye-case-drive creates them.
SHARED = "0. Shared Folder"
INTAKE = "0. Intake"
INITIAL = "1. Initial"


# Docs this workflow's sibling skill writes into the case folder. They live
# alongside the client's uploads but are firm-internal, so they never get filed
# as evidence.
GENERATED_PREFIXES = ("Intake Note", "材料上传指引邮件", "Document Upload Instructions")

FIRM_DOMAIN = "@lingtulaw.com"


def is_generated(f):
    """True for anything the firm put in the folder rather than the client.

    Two tests, because neither alone is enough. The name check catches the docs
    this skill and skye-case-drive create. The uploader check catches everything
    else staff drop into 0. Shared Folder for the client to see — the finished
    材料清单, a 方案, an information form — which carry no predictable name but
    are emphatically not new client material. Without it the daily digest
    announces the firm's own work back to the firm.
    """
    name = f["name"] if isinstance(f, dict) else f
    if any(name.startswith(p) for p in GENERATED_PREFIXES):
        return True
    if isinstance(f, dict):
        who = (f.get("lastModifyingUser") or {}).get("emailAddress", "")
        if who.lower().endswith(FIRM_DOMAIN):
            return True
    return False


def norm_case_type(raw):
    given = raw.strip().upper().replace("-", "").replace(" ", "")
    if given not in LAYOUTS:
        sys.exit(f"unknown case type {raw!r}; expected EB1A / O1A / O1B / NIW")
    return given


# --------------------------------------------------------------------------- #
# inventory
# --------------------------------------------------------------------------- #

def cmd_inventory(args):
    json.dump(inventory(args.case_root), sys.stdout, ensure_ascii=False, indent=2)
    print()


def inventory(case_root):
    """The full picture of one case's materials. Importable — daily_sweep.py and
    progress.py both need it, and shelling out to this script just to re-parse
    its own JSON would be silly."""
    root_kids = list_children(case_root, fields="files(id,name,mimeType)")
    by_name = {k["name"]: k for k in root_kids}

    def locate(label):
        hit = by_name.get(label)
        if hit:
            return hit["id"]
        hit = find_child(case_root, label)
        return hit["id"] if hit else None

    shared_id = locate(SHARED)
    intake_id = locate(INTAKE)
    initial_id = locate(INITIAL)

    report = {
        "case_root": case_root,
        "case_root_link": folder_link(case_root),
        "shared_folder_id": shared_id,
        "intake_folder_id": intake_id,
        "initial_folder_id": initial_id,
        "missing_folders": [n for n, i in
                            ((SHARED, shared_id), (INTAKE, intake_id), (INITIAL, initial_id))
                            if not i],
    }

    # The 材料清单 lives in the case root — that's the one doc the whole team
    # opens, so it stays one click from the case link rather than buried.
    checklist = next((k for k in root_kids
                      if "材料清单" in k["name"] or "会议清单" in k["name"]), None)
    report["checklist_doc"] = ({"id": checklist["id"], "name": checklist["name"],
                                "link": f"https://docs.google.com/document/d/{checklist['id']}/edit"}
                               if checklist else None)

    archived_src = {}
    initial_files = []
    if initial_id:
        for f, path in walk(initial_id):
            initial_files.append({"id": f["id"], "name": f["name"], "path": path,
                                  "mimeType": f["mimeType"]})
            src = (f.get("appProperties") or {}).get("eon_src")
            if src:
                archived_src[src] = path
    report["initial_file_count"] = len(initial_files)
    report["initial_files"] = initial_files

    # Files sitting loose directly in 1. Initial (not in a criterion subfolder)
    # are the case-creation drop: someone uploaded straight into Initial. They
    # need refiling with op "move", not "copy".
    loose = []
    if initial_id:
        for f in list_children(initial_id):
            if f["mimeType"] != FOLDER_MIME:
                loose.append({"id": f["id"], "name": f["name"], "mimeType": f["mimeType"],
                              "size": f.get("size"), "createdTime": f.get("createdTime"),
                              "link": file_link(f["id"]),
                              "archived": bool((f.get("appProperties") or {}).get("eon_src"))})
    report["loose_in_initial"] = loose

    new_files, done_files, generated = [], [], []
    for label, fid in ((SHARED, shared_id), (INTAKE, intake_id)):
        if not fid:
            continue
        for f, path in walk(fid):
            entry = {"id": f["id"], "name": f["name"], "mimeType": f["mimeType"],
                     "size": f.get("size"), "createdTime": f.get("createdTime"),
                     "source": label, "path": path, "link": file_link(f["id"]),
                     "uploaded_by": (f.get("lastModifyingUser") or {}).get("emailAddress")}
            if is_generated(f):
                # Firm-side files: the intake note, the upload-instructions
                # email, and anything staff uploaded for the client to see.
                # Listed separately — read the intake note, don't archive it,
                # and don't announce our own documents as new material.
                entry["uploaded_by"] = (f.get("lastModifyingUser") or {}).get("emailAddress")
                generated.append(entry)
                continue
            if f["id"] in archived_src:
                entry["archived_as"] = archived_src[f["id"]]
                done_files.append(entry)
            else:
                new_files.append(entry)
    new_files.sort(key=lambda e: e.get("createdTime") or "")
    report["new_files"] = new_files
    report["new_file_count"] = len(new_files)
    report["already_archived"] = done_files
    report["already_archived_count"] = len(done_files)
    report["generated_docs"] = generated
    return report


# --------------------------------------------------------------------------- #
# layout
# --------------------------------------------------------------------------- #

def cmd_layout(args):
    case_type = norm_case_type(args.case_type)
    made, existed = [], []
    for name in LAYOUTS[case_type]:
        if args.dry_run:
            made.append(name)
            continue
        fid, created = ensure_folder(name, args.initial_id)
        (made if created else existed).append({"name": name, "id": fid,
                                               "link": folder_link(fid)})
    json.dump({"case_type": case_type, "initial_folder_id": args.initial_id,
               "created": made, "already_there": existed,
               "dry_run": args.dry_run},
              sys.stdout, ensure_ascii=False, indent=2)
    print()


# --------------------------------------------------------------------------- #
# archive
# --------------------------------------------------------------------------- #

def resolve_path(initial_id, path, cache, dry_run):
    """Walk/create a folder path under 1. Initial. Returns the leaf id."""
    parent = initial_id
    for segment in path:
        if dry_run:
            parent = f"<{segment}>"
            continue
        parent, _ = ensure_folder(segment, parent, cache)
    return parent


def cmd_archive(args):
    with open(args.plan, encoding="utf-8") as fh:
        plan = json.load(fh)
    if not isinstance(plan, list):
        sys.exit("plan file must be a JSON list of entries")

    # Anything already archived is skipped rather than duplicated — re-running
    # after a partial failure is the normal case, not the exception.
    already = set()
    if not args.dry_run:
        for f, _ in walk(args.initial_id):
            src = (f.get("appProperties") or {}).get("eon_src")
            if src:
                already.add(src)

    cache, results = {}, []
    for entry in plan:
        src_id = entry["src_id"]
        name = entry["name"]
        path = entry.get("path") or []
        op = entry.get("op", "copy")
        row = {"src_id": src_id, "name": name, "path": path, "op": op}
        if src_id in already and op == "copy":
            row["status"] = "skipped (already archived)"
            results.append(row)
            continue
        try:
            target = resolve_path(args.initial_id, path, cache, args.dry_run)
            row["target_folder_id"] = target
            if args.dry_run:
                row["status"] = "would " + op
            elif op == "move":
                current = gws(["drive", "files", "get"],
                              params={"fileId": src_id, "supportsAllDrives": True,
                                      "fields": "parents"})
                params = {"fileId": src_id, "supportsAllDrives": True,
                          "addParents": target, "fields": "id,name"}
                parents = current.get("parents") or []
                if parents:
                    params["removeParents"] = ",".join(parents)
                out = gws(["drive", "files", "update"], params=params,
                          body={"name": name, "appProperties": {"eon_src": src_id}})
                row["file_id"] = out.get("id", src_id)
                row["status"] = "moved"
            else:
                out = gws(["drive", "files", "copy"],
                          params={"fileId": src_id, "supportsAllDrives": True,
                                  "fields": "id,name"},
                          body={"name": name, "parents": [target],
                                "appProperties": {"eon_src": src_id}})
                row["file_id"] = out["id"]
                row["status"] = "copied"
            if row.get("file_id"):
                row["link"] = file_link(row["file_id"])
        except GwsError as exc:
            row["status"] = "FAILED"
            row["error"] = str(exc)
        results.append(row)

    summary = {}
    for r in results:
        summary[r["status"]] = summary.get(r["status"], 0) + 1
    json.dump({"initial_folder_id": args.initial_id, "dry_run": args.dry_run,
               "summary": summary, "results": results},
              sys.stdout, ensure_ascii=False, indent=2)
    print()
    if any(r["status"] == "FAILED" for r in results):
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("inventory", help="what's uploaded, what's archived, what's new")
    p.add_argument("--case-root", required=True)
    p.set_defaults(func=cmd_inventory)

    p = sub.add_parser("layout", help="create the criterion subfolders in 1. Initial")
    p.add_argument("--initial-id", required=True)
    p.add_argument("--case-type", required=True, help="EB1A | O1A | O1B | NIW")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_layout)

    p = sub.add_parser("archive", help="execute a rename/file plan")
    p.add_argument("--initial-id", required=True)
    p.add_argument("--plan", required=True, help="JSON plan file")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_archive)

    args = ap.parse_args()
    try:
        args.func(args)
    except GwsError as exc:
        sys.exit(f"gws error: {exc}")


if __name__ == "__main__":
    main()
