#!/usr/bin/env python3
"""Fill a copied Dog Bite "Intake Sheet" Google Sheet and yellow-highlight blanks.

Layout (discovered from the template): the sheet is a set of label/value column
pairs. The VALUE cell is always the column immediately to the RIGHT of its label.
Data sections we auto-fill + highlight:
    Client            labels in col B  -> values in col C
    Incident          labels in col E  -> values in col F
    Dog & Resp Party  labels in col H  -> values in col I
    HO/Renter/CGL Ins labels in col K  -> values in col L
We locate value cells by SCANNING the label columns for non-empty labels (robust
to row drift / template revisions), rather than hard-coding rows.

SOP (N/O), Treatments (Q-V), Other Party Insurance (X/Y) and Vehicle (AA/AB) are
left untouched in v1 (SOP is a live checklist; the last two are vestigial from the
auto template and are N/A for dog-bite).

fields.json is a flat map of VALUE-cell A1 -> string, e.g. {"C2":"06/27/2026", ...}.
Any data value cell that ends up empty is filled with a yellow background
(#FFE599, the firm's "pending" highlight); filled cells are set white.

Usage:  python3 fill_intake_sheet.py <SPREADSHEET_ID> <fields.json>
"""
import sys, json, string
from gws_util import gws

LABEL_COLS = {"B": "C", "E": "F", "H": "I", "K": "L"}  # label col -> value col
YELLOW = {"red": 1.0, "green": 0.898, "blue": 0.6}     # #FFE599
WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}


def col_to_idx(col):  # "C" -> 2
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def idx_to_col(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def main():
    ssid, fields_path = sys.argv[1], sys.argv[2]
    fields = json.load(open(fields_path))

    meta = gws(["sheets", "spreadsheets", "get"], params={
        "spreadsheetId": ssid,
        "fields": "sheets(properties(sheetId,title,gridProperties))"})
    prop = meta["sheets"][0]["properties"]
    sheet_id = prop["sheetId"]

    grid = gws(["sheets", "spreadsheets", "values", "get"], params={
        "spreadsheetId": ssid, "range": f"{prop['title']}!A1:AC60"})
    rows = grid.get("values", [])

    def cell(colletter, r0):  # r0 is 0-indexed row
        ci = col_to_idx(colletter)
        if r0 < len(rows) and ci < len(rows[r0]):
            return (rows[r0][ci] or "").strip()
        return ""

    # Discover every data value cell by scanning the label columns.
    value_cells = []  # list of (col, row0) for value cells
    for lab_col, val_col in LABEL_COLS.items():
        for r0 in range(0, 60):
            if cell(lab_col, r0):            # label present in this row
                value_cells.append((val_col, r0))

    requests = []
    for (val_col, r0) in value_cells:
        a1 = f"{val_col}{r0 + 1}"
        supplied = str(fields.get(a1, "")).strip()
        existing = cell(val_col, r0)          # e.g. pre-filled "Pending"
        col_i = col_to_idx(val_col)
        base = {"start": {"sheetId": sheet_id, "rowIndex": r0, "columnIndex": col_i}}
        if supplied:
            requests.append({"updateCells": {
                "rows": [{"values": [{
                    "userEnteredValue": {"stringValue": supplied},
                    "userEnteredFormat": {"backgroundColor": WHITE,
                                          "wrapStrategy": "WRAP",
                                          "verticalAlignment": "TOP",
                                          "textFormat": {"bold": False}}}]}],
                # values are NON-bold — only the question labels (col B/E/H/K) stay bold
                "fields": "userEnteredValue,userEnteredFormat.backgroundColor,"
                          "userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment,"
                          "userEnteredFormat.textFormat.bold",
                **base}})
        elif existing:
            pass  # keep template value (e.g. "Pending"); no highlight
        else:
            requests.append({"repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": r0, "endRowIndex": r0 + 1,
                          "startColumnIndex": col_i, "endColumnIndex": col_i + 1},
                "cell": {"userEnteredFormat": {"backgroundColor": YELLOW}},
                "fields": "userEnteredFormat.backgroundColor"}})

    gws(["sheets", "spreadsheets", "batchUpdate"], params={"spreadsheetId": ssid},
        json_body={"requests": requests})

    filled = sum(1 for (vc, r0) in value_cells if str(fields.get(f"{vc}{r0+1}", "")).strip())
    yellow = sum(1 for r in requests if "repeatCell" in r)
    print(json.dumps({"value_cells": len(value_cells), "filled": filled,
                      "yellowed_blank": yellow}, indent=2))


if __name__ == "__main__":
    main()
