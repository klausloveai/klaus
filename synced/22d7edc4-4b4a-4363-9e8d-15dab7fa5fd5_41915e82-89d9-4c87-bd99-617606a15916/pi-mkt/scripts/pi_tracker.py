#!/usr/bin/env python3
"""Write one case into the PI tab of 成功案例交接表, never touching columns G (Approved) or H (朋友圈发布).

Usage:
  pi_tracker.py --type 车祸 --client "Lianhai Mu" \
      --folder https://drive.google.com/drive/folders/<id> \
      --canva https://www.canva.com/design/<designId>/edit \
      --note "State Farm $7,500 · #LT-2026-0916 · 侧面碰撞 · 37天" [--date 2026-09-25] [--dry-run]

If a row for the same folder link (or, failing that, the same client name) already
exists, that row's A–F and I are updated in place; otherwise the next empty row is
used and 序号 = previous max + 1. Prints the row number written.
Requires the `gws` CLI (~/.local/bin/gws) with Google auth already set up.
"""
import argparse
import datetime
import json
import os
import subprocess

SHEET_ID = "1JebB6SkokvxnaMh83WiOgr53PoRj9XDAu3KKWwJ1mZ8"
TAB = "PI"
GWS = os.path.expanduser("~/.local/bin/gws")


def gws(*args, body=None):
    cmd = [GWS, *args]
    if body is not None:
        cmd += ["--json", json.dumps(body, ensure_ascii=False)]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    start = out.find("{")  # gws prints a "Using keyring backend" line first
    return json.loads(out[start:]) if start >= 0 else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, help="案件类型: 车祸 / 卡车 / 摩托车 / 自行车 / 行人 / 狗咬 / 滑倒 …")
    ap.add_argument("--client", required=True)
    ap.add_argument("--folder", required=True)
    ap.add_argument("--canva", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    rows = gws("sheets", "spreadsheets", "values", "get",
               "--params", json.dumps({"spreadsheetId": SHEET_ID, "range": f"{TAB}!A1:I1000"})).get("values", [])

    target, max_no = None, 0
    for i, r in enumerate(rows[1:], start=2):
        r = r + [""] * (9 - len(r))
        if r[0].strip().isdigit():
            max_no = max(max_no, int(r[0]))
        if target is None and a.folder and r[3].strip() == a.folder:
            target = (i, r[0])
    if target is None:
        for i, r in enumerate(rows[1:], start=2):
            r = r + [""] * (9 - len(r))
            if r[2].strip().lower() == a.client.strip().lower():
                target = (i, r[0])
                break
    if target is None:
        last = max((i for i, r in enumerate(rows[1:], start=2) if any(c.strip() for c in r[:6] + r[8:9])), default=1)
        target = (last + 1, str(max_no + 1))
    row, seq = target
    seq = seq or str(max_no + 1)

    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"{TAB}!A{row}:F{row}", "values": [[seq, a.type, a.client, a.folder, a.canva, a.date]]},
            {"range": f"{TAB}!I{row}", "values": [[a.note]]},
        ],
    }
    if a.dry_run:
        print(json.dumps({"row": row, "body": body}, ensure_ascii=False, indent=2))
        return
    gws("sheets", "spreadsheets", "values", "batchUpdate",
        "--params", json.dumps({"spreadsheetId": SHEET_ID}), body=body)
    print(json.dumps({"row": row, "序号": seq}, ensure_ascii=False))


if __name__ == "__main__":
    main()
