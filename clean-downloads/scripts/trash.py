#!/usr/bin/env python3
"""Move Downloads files to the macOS Trash (Finder delete -> "Put Back" works),
never rm. Each file's MD5 is re-checked against the inventory first, so a file
that changed after the inventory is refused. Then empty folders (only
.DS_Store left) are trashed too, innermost first, repeated until none remain.

Plan file (JSON list): [{"path": "...", "md5": "...", "why": "..."}]

  trash.py plan.json [--dry-run]
"""
import argparse, hashlib, json, os, subprocess, sys

ROOT = os.path.expanduser("~/Downloads")


def finder_delete(paths):
    if not paths:
        return
    esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
    items = ", ".join(f'POSIX file "{esc(p)}"' for p in paths)
    r = subprocess.run(["osascript", "-e", f"tell application \"Finder\" to delete {{{items}}}"],
                       capture_output=True, text=True)
    if r.returncode:
        print("osascript error:", r.stderr[:300])


def empty_dirs():
    out = []
    for dp, dn, fn in os.walk(ROOT, topdown=False):
        if dp == ROOT:
            continue
        if not [f for f in fn if f != ".DS_Store"] and not [d for d in dn if os.path.exists(os.path.join(dp, d))]:
            out.append(dp)
    return [d for d in out if not any(d != e and d.startswith(e + "/") for e in out)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    go, refused = [], []
    for it in json.load(open(a.plan)):
        p = os.path.join(ROOT, it["path"])
        if not os.path.exists(p):
            refused.append((it["path"], "已不在"))
            continue
        if hashlib.md5(open(p, "rb").read()).hexdigest() != it["md5"]:
            refused.append((it["path"], "盘点后内容变了"))
            continue
        go.append(p)
        print(f"{'DRY ' if a.dry_run else 'TRASH'} {it['path']}  — {it.get('why', '')}")
    for p, why in refused:
        print(f"REFUSED {p}: {why}")
    if a.dry_run:
        print(f"\n将移废纸篓 {len(go)} 个，拒绝 {len(refused)} 个（dry run，未改动）")
        return
    finder_delete(go)
    left = [p for p in go if os.path.exists(p)]
    rounds = 0
    while (dirs := empty_dirs()) and rounds < 5:
        finder_delete(dirs)
        print("空文件夹移走:", [os.path.relpath(d, ROOT) for d in dirs])
        rounds += 1
    print(f"\n移废纸篓 {len(go) - len(left)} 个，失败 {len(left)} 个，拒绝 {len(refused)} 个")
    for p in left:
        print("  仍在原处:", p)
    sys.exit(1 if left else 0)


if __name__ == "__main__":
    main()
