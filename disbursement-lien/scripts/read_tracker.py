#!/usr/bin/env python3
"""Read one client tab of the Pending Disbursed Sheet (values + Reduced-cell colors) and print a
case JSON skeleton for disb.py. Remit-to fields (payee/addr1/csz) are left empty on purpose:
fill them only from a W-9, the provider's own bill, or the provider's own email.

    python3 read_tracker.py "Zhiping Liu" [--letter-date "October 21, 2026"] > case.json
"""
import argparse, datetime, json, re, subprocess, sys

SHEET = "1b_vPr9WD7P9arR6DTTJRxeWs0apk8DTiTgc2iAzIrR0"   # Pending Disbursed Sheet


def num(s):
    s = (s or "").replace("$", "").replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def color(cell):
    c = (cell.get("effectiveFormat") or {}).get("backgroundColor") or {}
    rgb = tuple(round(c.get(k, 0), 2) for k in ("red", "green", "blue"))
    return {(1, 1, 1): "white", (0, 1, 0): "green", (1, 1, 0): "yellow", (0, 0, 0): "white"}.get(rgb, str(rgb))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tab")
    ap.add_argument("--client", help="which client block, for tabs holding several clients")
    ap.add_argument("--letter-date", default=datetime.date.today().strftime("%B %-d, %Y"))
    a = ap.parse_args()
    meta = json.loads(subprocess.run(["gws", "sheets", "spreadsheets", "get", "--params", json.dumps({
        "spreadsheetId": SHEET, "fields": "sheets.properties(sheetId,title)"})],
        capture_output=True, text=True).stdout)
    sid = next((s["properties"]["sheetId"] for s in meta["sheets"]
                if s["properties"]["title"].strip().lower() == a.tab.strip().lower()), None)
    if sid is None:
        sys.exit(f"no tab named {a.tab!r} in Pending Disbursed Sheet")
    r = subprocess.run(["gws", "sheets", "spreadsheets", "getByDataFilter",
                        "--params", json.dumps({"spreadsheetId": SHEET}),
                        "--json", json.dumps({"includeGridData": True, "dataFilters": [{"gridRange": {
                            "sheetId": sid, "startRowIndex": 0, "endRowIndex": 80,
                            "startColumnIndex": 0, "endColumnIndex": 5}}]})],
                       capture_output=True, text=True)
    d = json.loads(r.stdout)
    if "sheets" not in d:
        sys.exit(f"cannot read tab {a.tab!r}: {d.get('error', {}).get('message', r.stderr[:200])}")
    rows = d["sheets"][0]["data"][0].get("rowData", [])
    cells = [[v.get("formattedValue", "") for v in rw.get("values", [])] for rw in rows]
    colors = [[color(v) for v in rw.get("values", [])] for rw in rows]

    # a tab can hold several client blocks; each starts with "<Name> | <DOL>" in row A/B
    start = 0
    if a.client:
        start = next((i for i, rw in enumerate(cells) if rw and rw[0].strip().lower() == a.client.strip().lower()), None)
        if start is None:
            sys.exit(f"client block {a.client!r} not found in tab {a.tab!r}")
    cells, colors = cells[start:], colors[start:]
    c = {"client": cells[0][0], "dol": cells[0][1] if len(cells[0]) > 1 else "",
         "tracker_note": " | ".join(x for x in cells[0][2:] if x), "letter_date": a.letter_date,
         "sources": {}, "case_cost": 0, "providers": [], "guardian": None}
    in_prov = False
    for i, rw in enumerate(cells):
        if not rw or not rw[0].strip():
            continue
        lab = rw[0].strip(); val = num(rw[1]) if len(rw) > 1 else None
        low = lab.lower()
        if low.startswith("provider name"):
            in_prov = True; continue
        if not in_prov:
            if low.startswith("3p settlement") and val: c["sources"]["3P"] = val
            elif "um/uim" in low and val: c["sources"]["UIM"] = val
            elif "medical payment" in low and val: c["sources"]["Med Pay"] = val
            elif low.startswith("total settlement"): c["total"] = val
            elif low.startswith("case cost"): c["case_cost"] = val or 0
            elif low.startswith("attorney fee"):
                c["fee"] = val
                m = re.search(r"\(([^)]*)\)", lab)
                lbl = (m.group(1) if m else "1/3").replace(" of net", "")
                c["fee_label"] = lbl
            elif low.startswith("client recovery"): c["net"] = val
            continue
        if low == "total":
            c["tracker_total_lien"] = val
            c["tracker_total_reduced"] = num(rw[2]) if len(rw) > 2 else None
            break
        red = num(rw[2]) if len(rw) > 2 else None
        p = {"name": re.sub(r"\s*\(\d+\)\s*$", "", lab), "lien": val, "reduced": red,
             "reduced_color": colors[i][2] if len(colors[i]) > 2 else "",
             "payee": "", "addr1": "", "csz": ""}
        if red is None:
            p["exclude_from_dis"] = True
            p["skip_lien"] = "no reduced amount on tracker (e.g. client out-of-pocket) — ask Klaus"
        c["providers"].append(p)
    json.dump(c, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
