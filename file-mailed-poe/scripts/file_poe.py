#!/usr/bin/env python3
"""Plan and apply the filing of mailed letters / certified receipts / returned mail
into a Lingtu case's "2. Legal Documents/Mailed POE" folder.

Dry-run by default: prints the rename+move plan. Pass --apply to execute.

House naming (items 5+ of the Weicong Lin folder are the current standard):
    <N>. <Client> - <Document Name>.pdf                 the letter that was mailed
    <N>. <Client> - <Document Name> - Receipt.pdf       its USPS certified-mail receipt
    <N>. <Client> - <Document Name> - Return.<ext>      the envelope if it came back

A receipt/return REUSES the N of the letter it belongs to; only a new letter takes
the next free number.
"""
import argparse, json, os, re, shutil, sys, unicodedata

DRIVE = os.path.expanduser(
    "~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/Shared drives")
DOGBITE = os.path.join(DRIVE, "Hernan Simo Cases/1. Cases/Dog Bite Cases")
SUBFOLDER_NAMES = ["Mailed POE", "POE"]          # existing variants seen in the wild


def norm(s):
    return unicodedata.normalize("NFC", s)


def find_case_folder(case_hint):
    """Return the case folder path whose name starts with the client name."""
    hits = []
    for root in (DOGBITE,):
        if not os.path.isdir(root):
            continue
        for name in os.listdir(root):
            if name.lower().startswith(case_hint.lower()):
                hits.append(os.path.join(root, name))
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"case folder: {len(hits)} match(es) for {case_hint!r}: {hits}")


def find_poe_folder(case_dir, create=False):
    legal = os.path.join(case_dir, "2. Legal Documents")
    for n in SUBFOLDER_NAMES:
        p = os.path.join(legal, n)
        if os.path.isdir(p):
            return p
    p = os.path.join(legal, SUBFOLDER_NAMES[0])
    if create:
        os.makedirs(p, exist_ok=True)
        return p
    raise SystemExit(f"no POE subfolder under {legal!r} (pass --create-folder)")


NUM_RE = re.compile(r"^\s*(\d+)\.\s*(.+)$")


def scan(poe_dir):
    """-> {n: {'letter': fn, 'receipt': fn, 'return': fn, 'stem': str}}"""
    groups = {}
    for fn in os.listdir(poe_dir):
        if fn.startswith("."):
            continue
        m = NUM_RE.match(fn)
        if not m:
            continue
        n, rest = int(m.group(1)), m.group(2)
        stem = os.path.splitext(rest)[0]
        g = groups.setdefault(n, {"letter": None, "receipt": None, "return": None,
                                  "stem": None})
        low = stem.lower()
        if low.endswith("- receipt") or low.startswith("poe receipt"):
            g["receipt"] = fn
        elif low.endswith("- return") or "- return" in low or ")- return" in low:
            g["return"] = fn
        else:
            g["letter"] = fn
            g["stem"] = stem
    return groups


def next_number(groups):
    return (max(groups) + 1) if groups else 1


def classify(path):
    """letter | receipt | return, guessed from the filename."""
    b = os.path.basename(path).lower()
    if "return" in b or b.endswith(".heic"):
        return "return"
    if "receipt" in b or "certified" in b or "3800" in b:
        return "receipt"
    return "letter"


def doc_stem(path, client):
    """Best-effort document name from a dropped file, minus client prefix/suffixes."""
    stem = os.path.splitext(os.path.basename(path))[0]
    stem = re.sub(r"^\s*\d+\.\s*", "", stem)
    stem = re.sub(rf"^{re.escape(client)}\s*-\s*", "", stem, flags=re.I)
    stem = re.sub(r"\s*-\s*(receipt|return)\s*$", "", stem, flags=re.I)
    return stem.strip()


def plan(case, files, attach_to=None, name_override=None, create_folder=False):
    case_dir = find_case_folder(case)
    client = os.path.basename(case_dir).rsplit("-", 1)[0].strip()
    poe = find_poe_folder(case_dir, create=create_folder)
    groups = scan(poe)
    actions, taken = [], next_number(groups)

    for f in files:
        if not os.path.exists(f):
            raise SystemExit(f"missing input file: {f}")
        kind = classify(f)
        ext = os.path.splitext(f)[1]
        if kind == "letter":
            n = taken
            taken += 1
            stem = name_override or doc_stem(f, client)
            new = f"{n}. {client} - {stem}{ext}"
        else:
            if attach_to is not None:
                n = int(attach_to)
            else:
                # match a receipt/return to an existing letter by fuzzy stem overlap
                want = (name_override or doc_stem(f, client)).lower()
                best, score = None, 0
                for gn, g in groups.items():
                    if not g["stem"]:
                        continue
                    a = set(re.findall(r"[a-z0-9]+", g["stem"].lower()))
                    b = set(re.findall(r"[a-z0-9]+", want))
                    s = len(a & b)
                    if s > score:
                        best, score = gn, s
                if best is None or score < 2:
                    raise SystemExit(
                        f"cannot match {os.path.basename(f)!r} to a letter — "
                        f"pass --attach-to <N>")
                n = best
            letter_stem = groups.get(n, {}).get("stem")
            if letter_stem:
                # scanned stems still carry the "<Client> - " prefix; drop it
                letter_stem = re.sub(rf"^{re.escape(client)}\s*-\s*", "",
                                     letter_stem, flags=re.I).strip()
            stem = name_override or letter_stem or doc_stem(f, client)
            suffix = "Receipt" if kind == "receipt" else "Return"
            new = f"{n}. {client} - {stem} - {suffix}{ext}"
        dest = os.path.join(poe, new)
        actions.append({"src": f, "dest": dest, "kind": kind, "n": n,
                        "exists": os.path.exists(dest)})
    return {"case_dir": case_dir, "client": client, "poe": poe,
            "existing_max": max(groups) if groups else 0, "actions": actions}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True, help="client name, e.g. 'Weicong Lin'")
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--attach-to", help="force receipt/return onto this letter number")
    ap.add_argument("--name", dest="name_override",
                    help="document name to use (without client prefix / number)")
    ap.add_argument("--create-folder", action="store_true")
    ap.add_argument("--apply", action="store_true", help="execute (default: dry run)")
    ap.add_argument("--move", action="store_true",
                    help="move instead of copy (default: copy, original untouched)")
    a = ap.parse_args()

    p = plan(a.case, a.files, a.attach_to, a.name_override, a.create_folder)
    print(f"case   : {p['case_dir']}")
    print(f"folder : {p['poe']}")
    print(f"highest existing number: {p['existing_max']}\n")
    for act in p["actions"]:
        flag = "  ⚠️ DEST EXISTS — skipped" if act["exists"] else ""
        print(f"  [{act['kind']:<7}] #{act['n']}")
        print(f"      from: {os.path.basename(act['src'])}")
        print(f"      to  : {os.path.basename(act['dest'])}{flag}")
    if not a.apply:
        print("\n(dry run — pass --apply to execute)")
        return
    for act in p["actions"]:
        if act["exists"]:
            print("skip (exists):", os.path.basename(act["dest"]))
            continue
        (shutil.move if a.move else shutil.copy2)(act["src"], act["dest"])
        print("filed:", os.path.basename(act["dest"]))


if __name__ == "__main__":
    main()
