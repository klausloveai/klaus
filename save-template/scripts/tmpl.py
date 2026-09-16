#!/usr/bin/env python3
"""One-click template versioning for Lingtu Law templates living in Google Drive.

The LIVE template is always the working copy everyone edits and every new case
duplicates. Each `save` freezes a full copy into a sibling `_Template Archive/`
folder named "<Template> v1.1", so every past version stays openable.

  python3 tmpl.py list
  python3 tmpl.py register --key dogbite-case --name "Dog Bite Case Template" \
                           --file-id <driveId> [--note "baseline"]
  python3 tmpl.py show    <key>
  python3 tmpl.py save    <key> [--minor|--major|--replace] [--note "..."] [--force]
  python3 tmpl.py use     <key> [version]        # id/link to duplicate FROM
  python3 tmpl.py restore <key> <version> --yes  # make an old version live again

Registry: ../templates.json (git-backed with the skill).
"""
import argparse, hashlib, json, os, sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gws_util import (FOLDER_MIME, drive_get, drive_children, find_child,
                      create_folder, copy_file, trash, web_link)

REGISTRY = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "templates.json")
ARCHIVE_NAME = "_Template Archive"


# ---------- registry ----------

def load():
    if not os.path.exists(REGISTRY):
        return {"templates": {}}
    with open(REGISTRY, encoding="utf-8") as f:
        return json.load(f)


def store(reg):
    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")


def entry(reg, key):
    t = reg["templates"].get(key)
    if not t:
        sys.exit(f"unknown template key '{key}'. Known: {', '.join(reg['templates']) or '(none)'}")
    return t


# ---------- version math ----------

def parse(v):
    a, b = v.split(".")
    return int(a), int(b)


def bump(v, kind):
    a, b = parse(v)
    return f"{a+1}.0" if kind == "major" else f"{a}.{b+1}"


def vname(t, v):
    return f"{t['name']} v{v}"


# ---------- Drive tree ----------

def walk(folder_id, prefix=""):
    """Yield (relpath, mimeType, id) for every node under folder_id, depth-first."""
    for c in sorted(drive_children(folder_id), key=lambda x: x["name"]):
        rel = f"{prefix}/{c['name']}" if prefix else c["name"]
        yield rel, c["mimeType"], c["id"]
        if c["mimeType"] == FOLDER_MIME:
            yield from walk(c["id"], rel)


def fingerprint(t):
    """Signature of the live template: names + structure + order-prefixes."""
    if t["kind"] == "file":
        f = drive_get(t["file_id"], fields="id,name,mimeType,modifiedTime")
        raw = f"{f['name']}|{f['mimeType']}|{f.get('modifiedTime','')}"
    else:
        raw = "\n".join(f"{rel}|{mime}" for rel, mime, _ in walk(t["file_id"]))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def copy_tree(src_id, dst_id):
    for c in drive_children(src_id):
        if c["mimeType"] == FOLDER_MIME:
            copy_tree(c["id"], create_folder(c["name"], dst_id))
        else:
            copy_file(c["id"], c["name"], dst_id)


def archive_folder(t):
    """Find or create the `_Template Archive` sibling of the live template."""
    if t.get("archive_id"):
        return t["archive_id"]
    parent = drive_get(t["file_id"])["parents"][0]
    hit = find_child(parent, ARCHIVE_NAME)
    t["archive_id"] = hit["id"] if hit else create_folder(ARCHIVE_NAME, parent)
    return t["archive_id"]


def snapshot(t, version):
    """Freeze the live template into the archive as "<Name> v<version>"."""
    arc = archive_folder(t)
    name = vname(t, version)
    if t["kind"] == "file":
        return copy_file(t["file_id"], name, arc)
    new_id = create_folder(name, arc)
    copy_tree(t["file_id"], new_id)
    return new_id


# ---------- commands ----------

def cmd_list(reg, _a):
    if not reg["templates"]:
        print("(registry empty — run `tmpl.py register` first)")
        return
    for k, t in reg["templates"].items():
        print(f"{k:22} v{t['current']:6} {t['kind']:6} {t['name']}")
        print(f"{'':22} live  {web_link(t['file_id'])}")


def cmd_register(reg, a):
    if a.key in reg["templates"] and not a.force:
        sys.exit(f"'{a.key}' already registered (use --force to re-register)")
    meta = drive_get(a.file_id)
    kind = "folder" if meta["mimeType"] == FOLDER_MIME else "file"
    t = {"name": a.name or meta["name"], "kind": kind, "file_id": a.file_id,
         "archive_id": None, "current": "1.0", "versions": []}
    fp = fingerprint(t)
    snap = snapshot(t, "1.0")
    t["versions"].append({"v": "1.0", "date": str(date.today()), "archive_id": snap,
                          "fingerprint": fp, "note": a.note or "baseline"})
    reg["templates"][a.key] = t
    store(reg)
    print(f"registered '{a.key}' → {t['name']} ({kind}) @ v1.0")
    print(f"  live    {web_link(a.file_id)}")
    print(f"  v1.0    {web_link(snap)}")


def cmd_show(reg, a):
    t = entry(reg, a.key)
    print(f"{t['name']}  ({t['kind']})   current v{t['current']}")
    print(f"live  {web_link(t['file_id'])}")
    live_fp = fingerprint(t)
    top = t["versions"][-1]
    print(f"live vs v{top['v']}: {'UNCHANGED' if live_fp == top['fingerprint'] else 'MODIFIED (unsaved edits)'}")
    print("\nversions:")
    for v in t["versions"]:
        print(f"  v{v['v']:6} {v['date']}  {v['note']}")
        print(f"{'':10} {web_link(v['archive_id'])}")


def cmd_save(reg, a):
    t = entry(reg, a.key)
    live_fp = fingerprint(t)
    top = t["versions"][-1]
    if live_fp == top["fingerprint"] and not a.force:
        print(f"no changes since v{top['v']} — nothing saved (use --force to snapshot anyway)")
        return
    if a.replace:
        version = top["v"]
        trash(top["archive_id"])
        t["versions"].pop()
    else:
        version = bump(t["current"], "major" if a.major else "minor")
    snap = snapshot(t, version)
    t["versions"].append({"v": version, "date": str(date.today()), "archive_id": snap,
                          "fingerprint": live_fp, "note": a.note or ""})
    t["current"] = version
    store(reg)
    verb = "replaced" if a.replace else "saved"
    print(f"{verb} {t['name']} → v{version}")
    print(f"  snapshot {web_link(snap)}")
    print(f"  live     {web_link(t['file_id'])}  (still what new cases duplicate)")


def cmd_use(reg, a):
    t = entry(reg, a.key)
    if not a.version or a.version.lstrip("v") == t["current"]:
        print(json.dumps({"template": t["name"], "version": t["current"], "source": "live",
                          "file_id": t["file_id"], "link": web_link(t["file_id"])},
                         ensure_ascii=False, indent=2))
        return
    want = a.version.lstrip("v")
    for v in t["versions"]:
        if v["v"] == want:
            print(json.dumps({"template": t["name"], "version": want, "source": "archive",
                              "file_id": v["archive_id"], "link": web_link(v["archive_id"])},
                             ensure_ascii=False, indent=2))
            return
    sys.exit(f"v{want} not found. Have: {', '.join('v'+v['v'] for v in t['versions'])}")


def cmd_restore(reg, a):
    t = entry(reg, a.key)
    want = a.version.lstrip("v")
    src = next((v for v in t["versions"] if v["v"] == want), None)
    if not src:
        sys.exit(f"v{want} not found. Have: {', '.join('v'+v['v'] for v in t['versions'])}")
    if t["kind"] != "folder":
        sys.exit("restore only supports folder templates — a file template's id would change, "
                 "breaking skills that hard-code it. Use `use` to duplicate the old version instead.")
    if not a.yes:
        sys.exit("restore REPLACES the live template's contents. Re-run with --yes to confirm.")
    # 1. never lose the current live state
    live_fp = fingerprint(t)
    if live_fp != t["versions"][-1]["fingerprint"]:
        auto = bump(t["current"], "minor")
        snap = snapshot(t, auto)
        t["versions"].append({"v": auto, "date": str(date.today()), "archive_id": snap,
                              "fingerprint": live_fp, "note": "auto-saved before restore"})
        t["current"] = auto
        store(reg)
        print(f"auto-saved live state as v{auto} before restoring")
    # 2. clear live, refill from the archived version (folder id is preserved)
    for c in drive_children(t["file_id"]):
        trash(c["id"])
    copy_tree(src["archive_id"], t["file_id"])
    # 3. record the restore as the new head version
    new_v = bump(t["current"], "minor")
    snap = snapshot(t, new_v)
    t["versions"].append({"v": new_v, "date": str(date.today()), "archive_id": snap,
                          "fingerprint": fingerprint(t), "note": f"restored from v{want}"})
    t["current"] = new_v
    store(reg)
    print(f"live template restored to the contents of v{want}, recorded as v{new_v}")
    print(f"  live {web_link(t['file_id'])}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list").set_defaults(fn=cmd_list)

    r = sub.add_parser("register"); r.set_defaults(fn=cmd_register)
    r.add_argument("--key", required=True)
    r.add_argument("--file-id", required=True)
    r.add_argument("--name")
    r.add_argument("--note")
    r.add_argument("--force", action="store_true")

    s = sub.add_parser("show"); s.set_defaults(fn=cmd_show); s.add_argument("key")

    v = sub.add_parser("save"); v.set_defaults(fn=cmd_save)
    v.add_argument("key")
    g = v.add_mutually_exclusive_group()
    g.add_argument("--minor", action="store_true", help="default: v1.1 → v1.2")
    g.add_argument("--major", action="store_true", help="structural overhaul: v1.2 → v2.0")
    g.add_argument("--replace", action="store_true", help="overwrite the current version's snapshot")
    v.add_argument("--note", default="")
    v.add_argument("--force", action="store_true", help="snapshot even if nothing changed")

    u = sub.add_parser("use"); u.set_defaults(fn=cmd_use)
    u.add_argument("key"); u.add_argument("version", nargs="?")

    x = sub.add_parser("restore"); x.set_defaults(fn=cmd_restore)
    x.add_argument("key"); x.add_argument("version"); x.add_argument("--yes", action="store_true")

    a = p.parse_args()
    a.fn(load(), a)


if __name__ == "__main__":
    main()
