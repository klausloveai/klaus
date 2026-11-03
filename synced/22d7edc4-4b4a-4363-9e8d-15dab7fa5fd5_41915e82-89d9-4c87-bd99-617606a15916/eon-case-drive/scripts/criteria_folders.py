#!/usr/bin/env python3
"""The subfolders that go inside "3. Petition Letter & Exhibits".

One folder per statutory criterion, plus the case type's non-criterion pieces
(工会信, offer, Personal Statement...). They're created for **every** criterion
the law lists, not just the ones the case will claim — at build time nobody
knows yet which three-or-more will carry the case. Staff prune and rename them
by hand once the background materials are in, which is faster than creating
folders one at a time later.

No A/B/C exhibit letters here on purpose: staff delete the criteria that don't
apply, and letters would go out of sequence the moment they did. NIW is the
exception — its four folders are lettered because the prongs are a fixed set
that never gets pruned.

Sources, verified against the USCIS Policy Manual:
  EB-1A  Vol 6 Part F Ch 2  (8 CFR 204.5(h)(3)(i)-(x))       — 10 criteria
  O-1A   Vol 2 Part M Ch 4  (8 CFR 214.2(o)(3)(iii)(B))      —  8 criteria
  O-1B   Vol 2 Part M Ch 4  (8 CFR 214.2(o)(3)(iv)(B))       —  6 criteria
  NIW    Matter of Dhanasar                                  —  3 prongs

Importable (`folders_for()` — used by build_case_drive.py) and runnable to add
them to a case that already exists:

  python3 criteria_folders.py --case-type EB1A --list
  python3 criteria_folders.py --folder-id <PL_AND_EXHIBITS_ID> --case-type O1B
"""

import argparse
import json
import subprocess
import sys

FOLDER_MIME = "application/vnd.google-apps.folder"

# (name, is_statutory_criterion). Order = statutory order, with the case type's
# non-criterion folders sitting where the firm expects them.
LAYOUTS = {
    "EB1A": [
        ("Awards 奖项", True),
        ("Memberships 协会会员", True),
        ("Published Material 媒体报道", True),
        ("Judging 评审", True),
        ("Original Contributions 原创性重大贡献", True),
        ("Scholarly Articles 学术发表", True),
        ("Exhibitions 展览展示", True),
        ("Leading or Critical Role 重要机构关键角色", True),
        ("High Salary 高薪", True),
        ("Commercial Success 商业成就", True),
        ("Final Merits 推荐信", False),
        ("Personal Statement", False),
    ],
    "O1A": [
        ("Waiver 工会信", False),
        ("未来计划 Offer", False),
        ("Awards 奖项", True),
        ("Memberships 协会会员", True),
        ("Published Material 媒体报道", True),
        ("Judging 评审", True),
        ("Original Contributions 原创性重大贡献", True),
        ("Scholarly Articles 学术发表", True),
        ("Critical or Essential Capacity 关键岗位", True),
        ("High Salary 高薪", True),
    ],
    "O1B": [
        ("工会信", False),
        ("未来工作 Offer", False),
        ("Lead or Starring Role in Productions 重要作品主演主创", True),
        ("National or International Recognition 国家级国际级认可", True),
        ("Lead or Critical Role for Distinguished Organizations 知名机构主要角色", True),
        ("Major Commercial or Critical Success 商业或口碑成就", True),
        ("Significant Recognition from Experts 业内专家认可", True),
        ("High Salary 高薪", True),
    ],
    # NIW keeps its letters — the three Dhanasar prongs plus the endeavor are a
    # fixed set, so nothing gets pruned and the lettering stays in sequence.
    "NIW": [
        ("A. Endeavor", False),
        ("B. Prong 1", True),
        ("C. Prong 2", True),
        ("D. Prong 3", True),
    ],
}


def folders_for(case_type, numbered=False):
    """Folder names for a case type, in the order they should be created.

    Returns [] for a plain "O1" with no A/B — the two subtypes share almost no
    criteria, so guessing one would scaffold the wrong case.
    """
    key = case_type.strip().upper().replace("-", "").replace(" ", "")
    layout = LAYOUTS.get(key)
    if not layout:
        return []
    if not numbered or key == "NIW":
        return [name for name, _ in layout]
    out, n = [], 0
    for name, is_criterion in layout:
        if is_criterion:
            n += 1
            out.append(f"{n}. {name}")
        else:
            out.append(name)
    return out


def gws(args, params=None, body=None):
    cmd = ["gws"] + args
    if params is not None:
        cmd += ["--params", json.dumps(params, ensure_ascii=False)]
    if body is not None:
        cmd += ["--json", json.dumps(body, ensure_ascii=False)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"gws {' '.join(args[:3])} failed: {(proc.stderr or proc.stdout).strip()}")
    out = proc.stdout.strip()
    data = json.loads(out) if out else {}
    if isinstance(data, dict) and "error" in data:
        sys.exit(json.dumps(data["error"], ensure_ascii=False))
    return data


def create_in(folder_id, names):
    """Create each name under folder_id, skipping ones already there."""
    existing = {f["name"] for f in gws(
        ["drive", "files", "list"],
        params={"q": f"'{folder_id}' in parents and trashed=false",
                "fields": "files(id,name)", "supportsAllDrives": True,
                "includeItemsFromAllDrives": True, "corpora": "allDrives",
                "pageSize": 200}).get("files", [])}
    result = []
    for name in names:
        if name in existing:
            result.append({"name": name, "status": "already there"})
            continue
        made = gws(["drive", "files", "create"],
                   params={"supportsAllDrives": True, "fields": "id,name"},
                   body={"name": name, "mimeType": FOLDER_MIME, "parents": [folder_id]})
        result.append({"name": name, "id": made["id"], "status": "created"})
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case-type", required=True, help="EB1A | O1A | O1B | NIW")
    ap.add_argument("--folder-id", help='The case\'s "3. Petition Letter & Exhibits" folder')
    ap.add_argument("--numbered", action="store_true",
                    help="Prefix each statutory criterion with its number from the regulation")
    ap.add_argument("--list", action="store_true", help="Print the folder names and exit")
    args = ap.parse_args()

    names = folders_for(args.case_type, numbered=args.numbered)
    if not names:
        key = args.case_type.strip().upper().replace("-", "")
        if key == "O1":
            sys.exit("O-1 needs the subtype: pass O1A or O1B — their criteria barely overlap")
        sys.exit(f"unknown case type {args.case_type!r}; expected EB1A / O1A / O1B / NIW")

    if args.list or not args.folder_id:
        print("\n".join(names))
        if not args.list:
            sys.exit("(nothing created — pass --folder-id to actually build them)")
        return

    print(json.dumps({"case_type": args.case_type, "folders": create_in(args.folder_id, names)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
