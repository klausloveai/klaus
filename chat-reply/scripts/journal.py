#!/usr/bin/env python3
"""IOLTA Account Journal lookup (read-only).  journal.py <client substring> [more terms...]
Prints matching rows: row#, date(A), payor/payee, method, check#, deposit, disbursement, client, cleared(M), stmt month(N)
plus the 'BoA recon through' line from _STATE.md."""
import sys, openpyxl
from pathlib import Path
D = Path.home() / "Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/Documents/Lingtu Law-Disbursement/IOLTA#3618"
terms = [t.lower() for t in sys.argv[1:]]
ws = openpyxl.load_workbook(D / "Account-Journal.xlsx", read_only=True, data_only=True)["Account journal"]
f = lambda v: v.strftime("%m/%d/%Y") if hasattr(v, "strftime") else ("" if v is None else str(v))
for i, r in enumerate(ws.iter_rows(min_row=10, values_only=True), 10):
    blob = " ".join(str(x) for x in r[:14] if x is not None).lower()
    if all(t in blob for t in terms):
        print(f"row {i} | A {f(r[0])} | {f(r[1])} | {f(r[2])} | chk {f(r[3])} | dep {f(r[5])} | disb {f(r[6])} "
              f"| client {f(r[8])} | M cleared {f(r[12]) or '(空)'} | N {f(r[13])} | {f(r[4])[:140]}")
print("_STATE:", (D / "_STATE.md").read_text().splitlines()[2])
