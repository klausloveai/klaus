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

    # A statement line is "Check 80123", "Check Image 80325", or bare "Check" when the bank
    # could not read the number. The unnumbered ones are keyed by amount — the capture names
    # them the same way — so they are checked for coverage like any other.
    #
    # Key on number AND amount, never on the number alone: August re-used ck 80275 for two
    # different checks (8/03 $3,210.00 and 8/20 $705.00), and keying by number silently
    # dropped one of them from both the count and the total.
    stmt = {}
    with open(f"{MR}stmt-3618-{a.month}.csv") as fh:
        for row in csv.reader(fh):
            if len(row) >= 4 and re.match(r"^\d\d/\d\d/\d{4}$", row[0]) and row[2]:
                d = row[1].strip().strip('"')
                if not re.match(r"^Check\b", d, re.I): continue
                amt = abs(float(row[2].replace(",", "")))
                m = re.search(r"Check(?:\s+Image)?\s+(\d+)", d, re.I)
                num = m.group(1) if m else "NONUM" + f"{amt:.2f}".replace(".", "")
                k = f"{num}@{amt:.2f}"
                if k in stmt:
                    # Same number, same amount, twice. Only one image can carry that name,
                    # so coverage cannot be proven by filename — say so and move on.
                    print(f"!! two statement lines are both check {num} for {amt:,.2f} "
                          f"— verify this pair by eye")
                stmt[k] = (num, amt)

    imgs = {}
    for fn in os.listdir(a.src):
        m = re.match(r"^(\d{8})_ck(\d+|NONUM\d+)_([\d.]+)_(front|back)\.jpg$", fn)
        if m:
            k = f"{m.group(2)}@{float(m.group(3)):.2f}"
            imgs.setdefault(k, {})[m.group(4)] = (fn, float(m.group(3)))

    def label(k): return k.split("@")[0]

    missing   = sorted(label(k) for k in set(stmt) - set(imgs))
    extra     = sorted(label(k) for k in set(imgs) - set(stmt))
    oneside   = sorted(label(k) for k, s in imgs.items() if len(s) < 2)

    print(f"statement checks {len(stmt)}  ({sum(v[1] for v in stmt.values()):,.2f})")
    print(f"captured         {len(imgs)}  both sides {sum(1 for s in imgs.values() if len(s)==2)}")
    print(f"missing image    {len(missing)}  {missing if missing else ''}")
    print(f"one side only    {len(oneside)}  {oneside if oneside else ''}")
    print(f"not on statement {len(extra)}    {extra if extra else ''}")

    mismatch = []
    ok = not (missing or oneside or extra)
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
