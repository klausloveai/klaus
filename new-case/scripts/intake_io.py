#!/usr/bin/env python3
"""
intake_io.py — 读写案件 intake sheet，自动兼容两种存储格式。

2026-11-03 起新案的 intake 一律是 **原生 Google Sheet**（Klaus：「我需要都默认 google sheet」）；
之前的旧案大多是 Drive 上的 `.xlsx` 文件。下游 skill 不要再直接 `alt=media` 下载 ——
原生 Google Sheet 用 alt=media 会报 "Only files with binary content can be downloaded"。

用法：
    python3 intake_io.py mime  <fileId>                    # 打印 gsheet / xlsx
    python3 intake_io.py fetch <fileId> <out.xlsx>         # 两种格式都落成本地 xlsx（只读用）
    python3 intake_io.py set   <fileId> <CELL> <VALUE> [<CELL> <VALUE> ...]
                                                           # 只对原生 Google Sheet：写值（RAW，长数字按文本存）
fetch 出来的 xlsx 只用来读；写回原生 Google Sheet 一律走 `set`（或 Sheets API），
绝不能把本地 xlsx `files update --upload` 覆盖回原生 Sheet（会变回 xlsx 文件）。
"""
import json
import os
import subprocess
import sys

GSHEET = "application/vnd.google-apps.spreadsheet"
XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def gws(args, cwd=None):
    # gws 拒绝 cwd 之外的 -o / --upload 路径，所以落盘时切到目标目录、传相对文件名
    r = subprocess.run(["gws"] + args, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        sys.exit(f"gws {' '.join(args[:3])} failed: {r.stderr[-400:]}{r.stdout[-400:]}")
    i = r.stdout.find("{")
    return json.loads(r.stdout[i:]) if i >= 0 else {}


def mime(fid):
    m = gws(["drive", "files", "get", "--params",
             json.dumps({"fileId": fid, "fields": "mimeType,name", "supportsAllDrives": True})])
    return m["mimeType"]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, fid = sys.argv[1], sys.argv[2]
    mt = mime(fid)
    kind = "gsheet" if mt == GSHEET else "xlsx" if mt == XLSX else mt
    if cmd == "mime":
        print(kind)
    elif cmd == "fetch":
        out = os.path.abspath(sys.argv[3])
        d, base = os.path.dirname(out), os.path.basename(out)
        if kind == "gsheet":
            gws(["drive", "files", "export", "--params",
                 json.dumps({"fileId": fid, "mimeType": XLSX}), "-o", base], cwd=d)
        else:
            gws(["drive", "files", "get", "--params",
                 json.dumps({"fileId": fid, "alt": "media", "supportsAllDrives": True}), "-o", base], cwd=d)
        print(f"{kind} -> {out}")
    elif cmd == "set":
        if kind != "gsheet":
            sys.exit("这是 .xlsx intake —— 按该 skill 原有的 xlsx 编辑路径改，不走 set")
        pairs = sys.argv[3:]
        if not pairs or len(pairs) % 2:
            sys.exit("set 需要成对的 <CELL> <VALUE>")
        tab = gws(["sheets", "spreadsheets", "get", "--params",
                   json.dumps({"spreadsheetId": fid, "fields": "sheets.properties.title"})]
                  )["sheets"][0]["properties"]["title"]
        data = [{"range": f"'{tab}'!{pairs[i]}", "values": [[pairs[i + 1]]]}
                for i in range(0, len(pairs), 2)]
        gws(["sheets", "spreadsheets", "values", "batchUpdate",
             "--params", json.dumps({"spreadsheetId": fid}),
             "--json", json.dumps({"valueInputOption": "RAW", "data": data})])
        print(f"set {len(data)} cell(s) on '{tab}'")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
