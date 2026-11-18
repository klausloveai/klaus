#!/usr/bin/env python3
"""Inventory ~/Downloads and say, per file, whether Drive already holds the
same bytes. Output is numbered so Klaus can call files by number.

Drive matching, in order (each is a real MD5 match, never a name match):
  1. index of Drive files modified since --since (default 120 days back)
  2. exact-file-name lookup with no date limit -- catches files archived long
     ago (2026-10-24: a March invoice was missed by a date-limited index)
  3. --revisions: revision history of same-name Drive files (slow; optional)

  inventory.py --out inv.json [--since 2026-06-01] [--revisions]
"""
import argparse, datetime, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import gws  # noqa: E402

ROOT = os.path.expanduser("~/Downloads")
SKIP = {".DS_Store", ".localized"}
SKIP_EXT = (".gdoc", ".gsheet", ".gslides", ".gform", ".gdraw", ".gmap", ".gsite")  # Drive pointers, not files
# Since 2026-11-18 ~/Downloads is a symlink INTO Google Drive (My Drive/Download-Drive,
# shared by Mac Mini + MacBook). Every local file therefore also exists in Drive inside this
# folder tree -- those self-matches must NOT count as "already archived in Drive".
DL_FOLDER_ID = os.environ.get("CLEAN_DOWNLOADS_DRIVE_ID", "1i9hUQBNYBOpHt_V_MyXNuhoOwPoU8nW-")


def downloads_tree():
    """Folder ids of the Drive Downloads folder and every subfolder (BFS)."""
    seen, todo = {DL_FOLDER_ID}, [DL_FOLDER_ID]
    while todo:
        fid = todo.pop()
        tok = None
        while True:
            p = {"q": f"'{fid}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed=false",
                 "pageSize": 1000, "fields": "nextPageToken,files(id)"}
            if tok:
                p["pageToken"] = tok
            d = gws.call("drive", "files", "list", params=p)
            for f in d.get("files", []):
                if f["id"] not in seen:
                    seen.add(f["id"]); todo.append(f["id"])
            tok = d.get("nextPageToken")
            if not tok:
                break
    return seen


def outside(files, tree):
    """Drop Drive hits that are just the synced copy living in the Downloads folder itself."""
    return [f for f in files if not set(f.get("parents", [])) & tree]


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def drive_index(since):
    files, tok = [], None
    while True:
        p = {"q": f"trashed=false and modifiedTime > '{since}T00:00:00' and mimeType != 'application/vnd.google-apps.folder'",
             "corpora": "allDrives", "includeItemsFromAllDrives": True, "supportsAllDrives": True,
             "pageSize": 1000, "fields": "nextPageToken,files(id,name,md5Checksum,parents)"}
        if tok:
            p["pageToken"] = tok
        d = gws.call("drive", "files", "list", params=p)
        files += d.get("files", [])
        tok = d.get("nextPageToken")
        if not tok:
            return files


def by_name(name):
    q = name.replace("\\", "\\\\").replace("'", "\\'")
    d = gws.call("drive", "files", "list", params={
        "q": f"name = '{q}' and trashed=false", "corpora": "allDrives",
        "includeItemsFromAllDrives": True, "supportsAllDrives": True,
        "fields": "files(id,name,md5Checksum,parents)"})
    return d.get("files", [])


def revisions_md5(fid):
    d = gws.call("drive", "revisions", "list", params={"fileId": fid, "fields": "revisions(md5Checksum)", "pageSize": 200})
    return {r.get("md5Checksum") for r in d.get("revisions", [])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--since", default=(datetime.date.today() - datetime.timedelta(days=120)).isoformat())
    ap.add_argument("--revisions", action="store_true")
    a = ap.parse_args()

    loc = []
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if f in SKIP or f.endswith(SKIP_EXT):
                continue
            p = os.path.join(dp, f)
            st = os.stat(p)
            loc.append({"path": os.path.relpath(p, ROOT), "md5": md5(p), "size": st.st_size,
                        "mtime": datetime.datetime.fromtimestamp(st.st_mtime).strftime("%m-%d %H:%M")})
    loc.sort(key=lambda x: x["path"])

    tree = downloads_tree()
    idx = {}
    for f in outside(drive_index(a.since), tree):
        if f.get("md5Checksum"):
            idx.setdefault(f["md5Checksum"], []).append(f)
    for o in loc:
        o["drive"] = [{"id": f["id"], "name": f["name"], "how": "index"} for f in idx.get(o["md5"], [])]

    todo = [o for o in loc if not o["drive"]]
    for o, hits in zip(todo, gws.pmap(lambda o: outside(by_name(os.path.basename(o["path"])), tree), todo)):
        same = [f for f in hits if f.get("md5Checksum") == o["md5"]]
        o["drive"] = [{"id": f["id"], "name": f["name"], "how": "name"} for f in same]
        o["_samename"] = [f["id"] for f in hits if f not in same]
    if a.revisions:
        for o in loc:
            if o["drive"]:
                continue
            for fid in o.get("_samename", []):
                if o["md5"] in revisions_md5(fid):
                    o["drive"] = [{"id": fid, "name": os.path.basename(o["path"]), "how": "revision"}]
                    break
    for i, o in enumerate(loc, 1):
        o["no"] = i
        o.pop("_samename", None)

    json.dump(loc, open(a.out, "w"), ensure_ascii=False, indent=1)
    hit = sum(1 for o in loc if o["drive"])
    print(f"Downloads 文件 {len(loc)}   Drive 已有同一份（MD5）{hit}   未对上 {len(loc) - hit}\n")
    for o in loc:
        mark = "✓" if o["drive"] else "·"
        tail = f"  ⇒ {o['drive'][0]['name'][:55]} [{o['drive'][0]['how']}]" if o["drive"] else ""
        print(f"{o['no']:>3} {mark} {o['mtime']} {o['size'] / 1024:>8.0f}K  {o['path'][:95]}{tail}")


if __name__ == "__main__":
    main()
