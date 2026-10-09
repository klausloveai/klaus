#!/usr/bin/env python3
"""Move captured BoA check images into the month's package and verify coverage
against that month's bank statement. Reports any check with no image, any image
with no statement line, and any amount that disagrees."""
import csv, json, os, re, shutil, sys, argparse

MR = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/"
                        "Lingtu Law-Disbursement/IOLTA#3618/Monthly Reconciliations/")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True)          # 2026-06
    ap.add_argument("--src", default=os.path.expanduser("~/Downloads"))
    ap.add_argument("--move", action="store_true")
    a = ap.parse_args()

    stmt = {}
    with open(f"{MR}stmt-3618-{a.month}.csv") as fh:
        for row in csv.reader(fh):
            if len(row) >= 4 and re.match(r"^\d\d/\d\d/\d{4}$", row[0]):
                m = re.search(r"Check (\d+)", row[1])
                if m: stmt[m.group(1)] = abs(float(row[2].replace(",", "")))

    imgs = {}
    for fn in os.listdir(a.src):
        m = re.match(r"^(\d{8})_ck(\d+)_([\d.]+)_(front|back)\.jpg$", fn)
        if m:
            imgs.setdefault(m.group(2), {})[m.group(4)] = (fn, float(m.group(3)))

    missing   = sorted(set(stmt) - set(imgs))
    extra     = sorted(set(imgs) - set(stmt))
    oneside   = sorted(c for c, s in imgs.items() if len(s) < 2)
    mismatch  = [(c, stmt[c], list(imgs[c].values())[0][1])
                 for c in sorted(set(stmt) & set(imgs))
                 if abs(stmt[c] - list(imgs[c].values())[0][1]) > 0.005]

    print(f"statement checks {len(stmt)}  ({sum(stmt.values()):,.2f})")
    print(f"captured         {len(imgs)}  both sides {sum(1 for s in imgs.values() if len(s)==2)}")
    print(f"missing image    {len(missing)}  {missing if missing else ''}")
    print(f"one side only    {len(oneside)}  {oneside if oneside else ''}")
    print(f"not on statement {len(extra)}    {extra if extra else ''}")
    print(f"amount mismatch  {len(mismatch)} {mismatch if mismatch else ''}")

    ok = not (missing or oneside or extra or mismatch)
    if a.move:
        if not ok:
            sys.exit("\nnot complete — nothing moved. Capture the rest first.")
        dst = f"{MR}{a.month} State Bar Package/3 - Check Images/"
        os.makedirs(dst, exist_ok=True)
        n = 0
        for c, sides in imgs.items():
            for side, (fn, _) in sides.items():
                shutil.move(os.path.join(a.src, fn), dst + fn); n += 1
        print(f"\nmoved {n} files -> {dst}")
    elif ok:
        print("\nCOMPLETE — re-run with --move to file them")

if __name__ == "__main__":
    main()
