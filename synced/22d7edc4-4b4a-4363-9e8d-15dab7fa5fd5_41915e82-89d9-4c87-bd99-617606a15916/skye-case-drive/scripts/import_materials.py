#!/usr/bin/env python3
"""Copy intake materials into a case's "1. Initial" folder, renamed.

Intake materials go to 1. Initial, not 0. Shared Folder. 0. Shared Folder is the
client's own upload space — dropping the firm's intake pile in there mixes "what
we already have" with "what they still need to send," and the client can't tell
which is which. 1. Initial is where the firm's copy of the record lives.

Renaming matters as much as the copying. Intake material arrives as
`扫描全能王 2026-06-01 22.04.pdf`, `img01507.pdf`, `WeChatWorkScreenshot_ab79.png` —
names that tell the next person nothing, so every file gets opened one by one.
Give each file a name that says what it is.

Two ways to call it:

  # a Drive folder, copied recursively, names kept
  python3 import_materials.py --dest <1.INITIAL_ID> --src-folder <DRIVE_FOLDER_ID>

  # explicit per-file names (Drive ids and/or local paths)
  python3 import_materials.py --dest <1.INITIAL_ID> --map files.json

files.json is a list of {"src": <drive id or local path>, "name": "<new name>"},
optionally with "subfolder": "奖项" to file it under a subfolder of 1. Initial.
"""

import argparse
import json
import mimetypes
import os
import subprocess
import sys
import time

FOLDER = "application/vnd.google-apps.folder"
ALL = {"includeItemsFromAllDrives": True, "supportsAllDrives": True, "corpora": "allDrives"}


def gws(args, params=None, body=None, upload=None, tries=3, cwd=None):
    cmd = ["gws"] + args
    if params is not None: cmd += ["--params", json.dumps(params, ensure_ascii=False)]
    if body is not None: cmd += ["--json", json.dumps(body, ensure_ascii=False)]
    if upload is not None: cmd += ["--upload", upload]
    last = ""
    for attempt in range(tries):
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
        out = p.stdout.strip()
        if p.returncode == 0 and out:
            try:
                d = json.loads(out)
            except json.JSONDecodeError:
                last = out[:200]; time.sleep(1.5 * (attempt + 1)); continue
            if isinstance(d, dict) and "error" in d:
                last = json.dumps(d["error"], ensure_ascii=False)
                time.sleep(1.5 * (attempt + 1)); continue
            return d
        last = (p.stderr or out)[:200]
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(last)


def ls(fid):
    p = dict(ALL); p.update({"q": f"'{fid}' in parents and trashed=false",
                             "fields": "files(id,name,mimeType)", "orderBy": "name", "pageSize": 500})
    return gws(["drive", "files", "list"], params=p).get("files", [])


def mkdir(name, parent):
    for f in ls(parent):
        if f["name"] == name and f["mimeType"] == FOLDER:
            return f["id"]
    return gws(["drive", "files", "create"],
               params={"supportsAllDrives": True, "fields": "id"},
               body={"name": name, "mimeType": FOLDER, "parents": [parent]})["id"]


def copy_drive_file(fid, name, parent):
    return gws(["drive", "files", "copy"],
               params={"fileId": fid, "supportsAllDrives": True, "fields": "id,name"},
               body={"name": name, "parents": [parent]})


def upload_local(path, name, parent):
    # gws refuses an --upload path outside its working directory, so run it from
    # the file's own directory and hand it the bare filename.
    path = os.path.abspath(path)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return gws(["drive", "files", "create"],
               params={"uploadType": "multipart", "supportsAllDrives": True, "fields": "id,name"},
               body={"name": name, "parents": [parent], "mimeType": mime},
               upload=os.path.basename(path), cwd=os.path.dirname(path))


def copy_tree(src, dest, stats):
    existing = {f["name"] for f in ls(dest)}
    for f in ls(src):
        if f["mimeType"] == FOLDER:
            copy_tree(f["id"], mkdir(f["name"], dest), stats)
        elif f["name"] in existing:
            stats["skipped"] += 1
        else:
            copy_drive_file(f["id"], f["name"], dest)
            stats["files"] += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", required=True, help='The case\'s "1. Initial" folder id')
    ap.add_argument("--src-folder", help="Drive folder to copy recursively")
    ap.add_argument("--map", help="JSON list of {src, name, subfolder?} for per-file renaming")
    args = ap.parse_args()

    stats = {"files": 0, "skipped": 0, "failed": []}
    done = []

    if args.src_folder:
        copy_tree(args.src_folder, args.dest, stats)

    if args.map:
        with open(args.map, encoding="utf-8") as fh:
            items = json.load(fh)
        for it in items:
            src, name = it["src"], it["name"]
            parent = mkdir(it["subfolder"], args.dest) if it.get("subfolder") else args.dest
            try:
                made = (upload_local(src, name, parent) if os.path.exists(src)
                        else copy_drive_file(src, name, parent))
                done.append({"name": made.get("name", name), "id": made["id"],
                             "subfolder": it.get("subfolder", "")})
                stats["files"] += 1
            except (RuntimeError, OSError) as e:
                stats["failed"].append({"src": src, "name": name, "error": str(e)})

    print(json.dumps({"stats": stats, "imported": done}, ensure_ascii=False, indent=2))
    if stats["failed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
