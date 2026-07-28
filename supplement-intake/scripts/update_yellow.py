#!/usr/bin/env python3
"""
update_yellow.py — safe intake-sheet editor for native Google Sheets.

Accepts a GSheet spreadsheet ID (not a file path).  All intake sheets are
native Google Sheets since the new-case skill converts .xlsx → GSheet after
upload.  Drive version history is the backup mechanism.

Commands:
  list-yellow <spreadsheet_id>
      Print every yellow cell: coordinate, field label, current value.

  apply <spreadsheet_id> <edits.json | ->
      edits JSON:
        {"edits": [
            {"cell": "L5",  "value": "Farmers Insurance Exchange"},
            {"cell": "F5",  "value": "front-left; 3P rear", "keep_yellow": true},
            {"cell": "L13", "value": "213 E Dexter St, Covina CA 91723", "force": true}
        ]}

      Guards:
        - Only yellow (pending) cells are writable.
        - A non-yellow cell requires "force": true — use ONLY when a supplemental
          document clearly confirms a correction to an already-confirmed cell.
        - If any requested cell fails the guard, nothing is written.
      After writing, re-reads the sheet and verifies no unintended cell changed.
      Rollback: File > Version history > See version history in Google Sheets.
"""
import sys, json, subprocess, argparse


# ── GWS helper ───────────────────────────────────────────────────────────────

def gws_call(*args):
    r = subprocess.run(["gws"] + list(args), capture_output=True, text=True)
    lines = [l for l in r.stdout.split('\n') if not l.startswith('Using')]
    text = '\n'.join(lines).strip()
    if not text:
        raise RuntimeError(f"gws returned empty output.\nstderr: {r.stderr[:400]}")
    return json.loads(text)


# ── Coordinate helpers ────────────────────────────────────────────────────────

def col_to_idx(col):
    """'A' -> 0, 'Z' -> 25, 'AA' -> 26  (0-based)"""
    n = 0
    for ch in col.upper():
        n = n * 26 + (ord(ch) - 64)
    return n - 1

def idx_to_col(n):
    """0 -> 'A', 25 -> 'Z', 26 -> 'AA'  (0-based input)"""
    s = ''
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

def cell_to_rc(coord):
    """'C22' -> (row=21, col=2)  both 0-based"""
    col_s = ''.join(c for c in coord if c.isalpha())
    row_s = ''.join(c for c in coord if c.isdigit())
    return int(row_s) - 1, col_to_idx(col_s)

def rc_to_cell(r, c):
    return idx_to_col(c) + str(r + 1)


# ── Yellow detection ──────────────────────────────────────────────────────────

def is_yellow(bg):
    """
    Yellow = FFFF00 → {red:1.0, green:1.0, blue:0.0} in Sheets API.
    Threshold ±0.01 for float rounding.
    """
    if not bg:
        return False
    return (bg.get('red',   0) >= 0.99 and
            bg.get('green', 0) >= 0.99 and
            bg.get('blue',  0) <= 0.01)


# ── Sheet data fetch + parse ──────────────────────────────────────────────────

def fetch(spreadsheet_id):
    """Fetch full sheet data with formatting (includeGridData=true)."""
    return gws_call("sheets", "spreadsheets", "get",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id,
                                "includeGridData": True}))

def parse_cells(data):
    """Return dict: UPPERCASE_COORD -> {value, yellow, bg}"""
    result = {}
    rows = data["sheets"][0].get("data", [{}])[0].get("rowData", [])
    for r, row in enumerate(rows):
        for c, cell in enumerate(row.get("values", [])):
            uev = cell.get("userEnteredValue", {})
            v = (uev.get("stringValue")
                 or uev.get("formulaValue")
                 or (str(uev["numberValue"]) if "numberValue" in uev else "")
                 or ("TRUE" if uev.get("boolValue") else ""))
            bg  = cell.get("userEnteredFormat", {}).get("backgroundColor")
            coord = rc_to_cell(r, c)
            result[coord] = {"value": v or "", "yellow": is_yellow(bg), "bg": bg}
    return result

def get_sheet_id(data):
    return data["sheets"][0]["properties"]["sheetId"]

def row_label(data, row, col):
    """Nearest non-empty cell to the left — the human-readable field name."""
    rows = data["sheets"][0].get("data", [{}])[0].get("rowData", [])
    if row >= len(rows):
        return ""
    cells = rows[row].get("values", [])
    for cc in range(col - 1, -1, -1):
        if cc < len(cells):
            uev = cells[cc].get("userEnteredValue", {})
            v = uev.get("stringValue", "") or uev.get("formulaValue", "")
            if v.strip():
                return v.strip().split('\n')[0][:30]
    return ""


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_list_yellow(spreadsheet_id):
    data  = fetch(spreadsheet_id)
    cells = parse_cells(data)
    n = 0
    for coord in sorted(cells, key=lambda c: cell_to_rc(c)):
        info = cells[coord]
        if info["yellow"]:
            n += 1
            r, c = cell_to_rc(coord)
            label = row_label(data, r, c)
            print(f"  {coord:<5} [{label:30}] = {str(info['value'])[:50]!r}")
    print(f"\ntotal yellow (pending) cells: {n}")


def cmd_apply(spreadsheet_id, edits_arg):
    raw   = sys.stdin.read() if edits_arg == "-" else edits_arg
    edits = json.loads(raw).get("edits", [])
    if not edits:
        sys.exit("no edits provided")

    data     = fetch(spreadsheet_id)
    before   = parse_cells(data)
    sheet_id = get_sheet_id(data)

    intended, refused, forced = [], [], []
    requests = []

    for e in edits:
        coord = e["cell"].upper()
        cur   = before.get(coord, {"value": "", "yellow": False, "bg": None})

        if not cur["yellow"] and not e.get("force"):
            refused.append(coord)
            continue
        if not cur["yellow"]:
            forced.append((coord, cur["value"], e["value"]))
        intended.append(coord)

        r, c = cell_to_rc(coord)
        # keep_yellow → FFFF00; otherwise → white (un-highlighted)
        bg = ({"red": 1.0, "green": 1.0, "blue": 0.0}
              if e.get("keep_yellow")
              else {"red": 1.0, "green": 1.0, "blue": 1.0})

        requests.append({"updateCells": {
            "range": {"sheetId": sheet_id,
                      "startRowIndex": r, "endRowIndex": r + 1,
                      "startColumnIndex": c, "endColumnIndex": c + 1},
            "rows": [{"values": [{
                "userEnteredValue": {"stringValue": str(e["value"])},
                "userEnteredFormat": {
                    "backgroundColor": bg,
                    "textFormat": {"fontFamily": "Nunito", "fontSize": 10, "bold": False},
                    "horizontalAlignment": "LEFT"
                }
            }]}],
            "fields": ("userEnteredValue,"
                       "userEnteredFormat.backgroundColor,"
                       "userEnteredFormat.textFormat,"
                       "userEnteredFormat.horizontalAlignment")
        }})

    if refused:
        sys.exit(
            f"REFUSED (not yellow; add \"force\": true only for a document-confirmed "
            f"correction): {', '.join(refused)}\n"
            f"No changes written.")

    if not requests:
        sys.exit("No valid edits — nothing to apply.")

    gws_call("sheets", "spreadsheets", "batchUpdate",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id}),
        "--json",   json.dumps({"requests": requests}))

    # ── Verify: re-read and check only intended cells changed ──────────────
    after       = parse_cells(fetch(spreadsheet_id))
    intended_set = set(intended)
    all_coords   = set(before) | set(after)

    collateral = [
        coord for coord in all_coords
        if coord not in intended_set
        and (before.get(coord, {}).get("value")  != after.get(coord, {}).get("value") or
             before.get(coord, {}).get("yellow") != after.get(coord, {}).get("yellow"))
    ]

    # ── Report ─────────────────────────────────────────────────────────────
    print(f"applied {len(intended)} cell(s): {', '.join(intended)}")
    forced_set = {c for c, _, _ in forced}
    cleared = [e["cell"] for e in edits
               if not e.get("keep_yellow") and e["cell"].upper() not in forced_set]
    kept    = [e["cell"] for e in edits if e.get("keep_yellow")]
    print(f"  un-highlighted (confirmed): {', '.join(cleared) or '(none)'}")
    print(f"  filled but kept yellow:     {', '.join(kept) or '(none)'}")
    for coord, old, new in forced:
        print(f"  FORCED correction: {coord}: {old!r} -> {new!r}")
    if collateral:
        print(f"  WARNING: unexpected cells changed: {', '.join(sorted(collateral))}")
        print(f"  Rollback: open the sheet → File → Version history → See version history")
    else:
        print(f"  verified: no unintended cell changed.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    ap  = argparse.ArgumentParser(description="Safe yellow-only GSheet intake editor")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("list-yellow")
    p1.add_argument("sheet_id", help="GSheet spreadsheet ID")

    p2 = sub.add_parser("apply")
    p2.add_argument("sheet_id", help="GSheet spreadsheet ID")
    p2.add_argument("edits",    help="JSON edits string or '-' to read from stdin")

    a = ap.parse_args()
    if a.cmd == "list-yellow":
        cmd_list_yellow(a.sheet_id)
    elif a.cmd == "apply":
        cmd_apply(a.sheet_id, a.edits)


if __name__ == "__main__":
    main()
