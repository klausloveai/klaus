#!/usr/bin/env python3
"""Gate 3 — add a case to the PI Master Sheet tracking tab.

Copies the Example Row (row 2) down into the new row(s) FIRST — so the row keeps every
template default (Case Status, Property Damage "Ask Klaus", the clinical block, formatting,
data validation) — and only then writes the case-specific fields.

Never hand-roll insertDimension + values.update for the tracking sheet: that produces a row
missing the template columns. This has happened (Zhe Ji 9/8, Xianyong Hou 9/10).

Columns are resolved by reading the LIVE header row, never by hardcoded letters — the tabs
have different layouts (Claims@ has no Retainer column).

Usage:
  add_tracking_row.py --tab Piteam@ --dol 9/10/2026 \
      --client "Xianyong Hou" --sheet-id 1oukBsI... \
      --retainer "Standard 1/3" --retainer-sent 9/10 \
      [--passenger "Guihong Li" ...] [--referrer "..."] [--status "✒️Signing"] [--dry-run]
"""
import argparse, json, subprocess, sys

SPREADSHEET = "1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM"
# 2026-10-16: Picase@ was split into three tabs (one per CM). The old name 'Picase@' no longer
# exists — Picase@(Jenkins) is the original tab renamed (same sheetId). Klaus names the tab per case.
TAB_SHEET_IDS = {"Piteam@": 102974151, "Claims@": 86730608, "Klaus@": 1401961516,
                 "Picase@(Amos)": 948247733, "Picase@(Jenkins)": 775230687,
                 "Picase@(Eeve)": 1835238126}


def a1(tab, ref):  # quote the tab name: 'Picase@(Jenkins)' has parentheses
    return "'" + tab.replace("'", "''") + "'!" + ref


def gws(*args, params=None, body=None):
    cmd = ["gws", *args]
    if params:
        cmd += ["--params", json.dumps(params, ensure_ascii=False)]
    if body:
        cmd += ["--json", json.dumps(body, ensure_ascii=False)]
    out = subprocess.run(cmd, capture_output=True, text=True)
    raw = out.stdout
    i = raw.find("{")
    if i < 0:
        sys.exit(f"gws failed: {out.stdout}\n{out.stderr}")
    return json.JSONDecoder().raw_decode(raw[i:])[0]


def col_letter(idx):  # 0-based -> A, B, ... AA
    s = ""
    idx += 1
    while idx:
        idx, r = divmod(idx - 1, 26)
        s = chr(65 + r) + s
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tab", required=True, choices=sorted(TAB_SHEET_IDS))
    ap.add_argument("--dol", required=True, help="M/D/YYYY")
    ap.add_argument("--client", required=True, help="driver, exactly as in the case name")
    ap.add_argument("--sheet-id", required=True, help="Drive file id of the intake sheet")
    ap.add_argument("--retainer", default="", help="'Standard 1/3' or 'New 50%%' (blank on Claims@)")
    ap.add_argument("--retainer-sent", default="", help="M/D the retainer went out")
    ap.add_argument("--referrer", default="")
    ap.add_argument("--status", default="✒️Signing")
    ap.add_argument("--passenger", action="append", default=[])
    # 2026-11-02: every new case must carry its Lingtu Data code (Step 9a). Required on purpose —
    # no code, no tracking row. Same code on the driver and every passenger row.
    ap.add_argument("--case-id", required=True,
                    help="Lingtu Data code from Step 9a: matter code (12345-PI1) or, before signing, client code (12345)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    sheet_id = TAB_SHEET_IDS[a.tab]
    n = 1 + len(a.passenger)

    hdr = gws("sheets", "spreadsheets", "values", "get",
              params={"spreadsheetId": SPREADSHEET, "range": a1(a.tab, "1:1")}).get("values", [[]])[0]
    col = {h.strip(): i for i, h in enumerate(hdr) if h and h.strip()}

    # Some tabs spell the DOL header "Date of Loss" (Picase@) instead of "DOL".
    if "DOL" not in col and "Date of Loss" in col:
        col["DOL"] = col["Date of Loss"]
        print(f"note: {a.tab} spells the DOL header 'Date of Loss' -> using that column")

    # Claims@ leaves column A's header blank even though A holds the DOL.
    # Only accept that specific shape, and say so out loud — never guess any other column.
    if "DOL" not in col and hdr and not str(hdr[0]).strip():
        col["DOL"] = 0
        print(f"note: {a.tab} has no 'DOL' header; column A is blank -> treating A as DOL")

    # After the Case ID column was added at A (2026-11), some tabs left B's header blank while B holds the DOL.
    if "DOL" not in col and len(hdr) > 1 and str(hdr[0]).strip() == "Case ID" and not str(hdr[1]).strip():
        col["DOL"] = 1
        print(f"note: {a.tab} has 'Case ID' in A and a blank B header -> treating B as DOL")

    def need(name):
        if name not in col:
            sys.exit(f"column {name!r} not found in {a.tab} header: {hdr}")
        return col[name]

    # 1. insert N blank rows below the Example Row, then COPY row 2 into them
    reqs = [
        {"insertDimension": {"range": {"sheetId": sheet_id, "dimension": "ROWS",
                                       "startIndex": 2, "endIndex": 2 + n},
                             "inheritFromBefore": False}},
        {"copyPaste": {
            "source": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 2,
                       "startColumnIndex": 0, "endColumnIndex": len(hdr)},
            "destination": {"sheetId": sheet_id, "startRowIndex": 2, "endRowIndex": 2 + n,
                            "startColumnIndex": 0, "endColumnIndex": len(hdr)},
            "pasteType": "PASTE_NORMAL"}},
    ]

    # 1b. passenger rows: clear the backgrounds the copyPaste dragged down.
    #     Zones are derived from the LIVE header, never a hardcoded column letter —
    #     Claims@ has no Retainer column, so its blocks sit one column left of
    #     Picase@/Piteam@ (F-L there vs G-M here).
    #       A .. Case Status          -> white
    #       Note-Claims               -> UNTOUCHED (keep template blue)
    #       1LOR .. Property Damage   -> white (values are cleared too, below)
    #       Ambulance .. end          -> UNTOUCHED (keep template yellows)
    if a.passenger:
        white = {"userEnteredFormat": {"backgroundColor": {"red": 1, "green": 1, "blue": 1}}}
        block = [col[h] for h in ("1LOR", "1Coverage", "1Liability", "3LOR",
                                  "3Coverage", "3Liability", "Property Damage") if h in col]
        zones = [(0, need("Note-Claims"))]
        if block:
            zones.append((min(block), max(block) + 1))
        for c0, c1 in zones:
            if c1 > c0:
                reqs.append({"repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": 3, "endRowIndex": 2 + n,
                              "startColumnIndex": c0, "endColumnIndex": c1},
                    "cell": white, "fields": "userEnteredFormat.backgroundColor"}})

    # 2. per-row field writes (driver row 3, passengers 4..)
    link = f"https://docs.google.com/spreadsheets/d/{a.sheet_id}/edit"
    data = []

    def put(row, header, value):
        data.append({"range": a1(a.tab, f"{col_letter(need(header))}{row}"), "values": [[value]]})

    import re
    if not re.fullmatch(r"\d{5}(-PI\d+)?", a.case_id):
        sys.exit(f"--case-id {a.case_id!r} is not a Lingtu Data code (12345 or 12345-PI1)")
    put(3, "Case ID", a.case_id)
    put(3, "DOL", a.dol)
    put(3, "Client Name", f'=HYPERLINK("{link}","{a.client}")')
    if a.referrer:
        put(3, "Referrer", a.referrer)
    # Klaus 2026-11-05: cases referred by 小朱修车 send the car to that shop, so Property Damage
    # starts at "小朱修车 Ref" instead of the Example Row's "Ask Klaus".
    if a.referrer.strip() == "小朱修车":
        put(3, "Property Damage", "小朱修车 Ref")
    put(3, "Case Status", a.status)
    if a.retainer_sent:
        put(3, "Note-Claims", f"Retainer sent {a.retainer_sent}")
    if a.retainer and "Retainer" in col:
        put(3, "Retainer", a.retainer)

    for k, name in enumerate(a.passenger):
        r = 4 + k
        put(r, "Case ID", a.case_id)      # passengers share the driver's code
        put(r, "DOL", "")                 # passengers: DOL blank
        put(r, "Client Name", name)       # plain text, no hyperlink
        put(r, "Case Status", a.status)
        if a.retainer and "Retainer" in col:
            put(r, "Retainer", a.retainer)   # same label as driver, never blank
        if a.retainer_sent:
            put(r, "Note-Claims", f"Retainer sent {a.retainer_sent}")
        # 1LOR..Property Damage stay as copied from the Example Row for the DRIVER row only;
        # clear them on passenger rows — one case needs one primary record row
        for h in ("1LOR", "1Coverage", "1Liability", "3LOR", "3Coverage", "3Liability",
                  "Property Damage"):
            if h in col:
                put(r, h, "")

    if a.dry_run:
        print(json.dumps({"requests": reqs, "data": data}, ensure_ascii=False, indent=2))
        return

    gws("sheets", "spreadsheets", "batchUpdate",
        params={"spreadsheetId": SPREADSHEET}, body={"requests": reqs})
    gws("sheets", "spreadsheets", "values", "batchUpdate",
        params={"spreadsheetId": SPREADSHEET},
        body={"valueInputOption": "USER_ENTERED", "data": data})

    rng = a1(a.tab, f"A3:{col_letter(len(hdr)-1)}{2+n}")
    got = gws("sheets", "spreadsheets", "values", "get",
              params={"spreadsheetId": SPREADSHEET, "range": rng,
                      "valueRenderOption": "FORMULA"}).get("values", [])
    print(f"wrote {n} row(s) to {a.tab}:")
    for r in got:
        print("  ", r)


if __name__ == "__main__":
    main()
