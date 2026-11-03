#!/usr/bin/env python3
"""Find USCIS receipt numbers in the mailbox and put them on 案件总表.

  scan   — search the signed-in mailbox for receipt numbers
  apply  — append one to that client's 重要笔记 (column F) and print the
           wording to send the client

Usage:
  python3 case_number.py scan [--days 90] [--client "Dechao You"]
  python3 case_number.py apply --client "Dechao You" --case-number IOE1234567890 [--dry-run]

## Whose mailbox

Whichever account `gws` is authenticated as — KK's on KK's machine, Skye's
once this skill is installed on hers. The scan says which mailbox it actually
read, and finding nothing is reported as "没找到", never as "there is no
receipt number": the notice may simply have gone to a colleague's inbox.

## Column F, appended not overwritten

案件总表 has no receipt-number column, so the number goes into F 重要笔记
alongside the intake gist that is already there. F is written by hand and read
at a glance, so this appends to whatever it holds and refuses to write a
number that is already in the cell. Overwriting F would silently delete a
colleague's note — the sort of loss nobody notices until the note is needed.
"""

import argparse
import base64
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gwslib import GwsError, gws  # noqa: E402

TRACKING_SHEET = "1hVkR6sLbQossobqyUA4bJ7Qg3P-mrYF2YupMJvdflEQ"
TAB = "法律"
STATUS_URL = "https://egov.uscis.gov/"

# USCIS receipt numbers are a three-letter service-center prefix plus ten
# digits (IOE8342503951, WAC2190123456...). Matching the shape rather than a
# fixed prefix list means a centre we haven't seen before still gets caught;
# the prefix is reported so a human can sanity-check it.
RECEIPT = re.compile(r"\b([A-Z]{3}\d{10})\b")

SEARCH_TERMS = ('("receipt number" OR "Receipt Number" OR I-797 OR USCIS '
                'OR "case number" OR 收据 OR uscis.gov)')


def whoami():
    try:
        prof = gws(["gmail", "users", "getProfile"], params={"userId": "me"})
        return prof.get("emailAddress", "unknown")
    except GwsError:
        return "unknown"


def decode_parts(payload, out):
    data = (payload.get("body") or {}).get("data")
    if data:
        try:
            out.append(base64.urlsafe_b64decode(data + "==").decode("utf-8", "replace"))
        except Exception:
            pass
    for part in payload.get("parts", []) or []:
        decode_parts(part, out)


def cmd_scan(args):
    mailbox = whoami()
    q = f"newer_than:{args.days}d {SEARCH_TERMS}"
    if args.client:
        q += f' "{args.client}"'
    listing = gws(["gmail", "users", "messages", "list"],
                  params={"userId": "me", "q": q, "maxResults": args.max_results})
    ids = [m["id"] for m in listing.get("messages", [])]

    found = {}
    for mid in ids:
        msg = gws(["gmail", "users", "messages", "get"],
                  params={"userId": "me", "id": mid, "format": "full"})
        headers = {h["name"].lower(): h["value"]
                   for h in (msg.get("payload", {}).get("headers") or [])}
        chunks = [headers.get("subject", ""), msg.get("snippet", "")]
        decode_parts(msg.get("payload", {}), chunks)
        text = "\n".join(chunks)
        for number in set(RECEIPT.findall(text)):
            rec = found.setdefault(number, {
                "case_number": number, "prefix": number[:3], "messages": []})
            rec["messages"].append({
                "subject": headers.get("subject", ""),
                "from": headers.get("from", ""),
                "date": headers.get("date", ""),
                "link": f"https://mail.google.com/mail/u/0/#inbox/{mid}",
            })

    json.dump({"mailbox_searched": mailbox, "query": q,
               "messages_examined": len(ids),
               "found_count": len(found),
               "found": sorted(found.values(), key=lambda r: r["case_number"]),
               "note": ("没找到不等于没有收据号 —— 通知可能只发到了同事的信箱。"
                        if not found else "")},
              sys.stdout, ensure_ascii=False, indent=2)
    print()


def find_row(client):
    data = gws(["sheets", "+read", "--spreadsheet", TRACKING_SHEET,
                "--range", f"{TAB}!A3:F400"])
    rows = data.get("values", [])
    exact, loose = [], []
    for i, row in enumerate(rows):
        name = (row[0].strip() if row and row[0] else "")
        if not name:
            continue
        entry = {"row": i + 3, "name": name,
                 "note": row[5].strip() if len(row) > 5 and row[5] else ""}
        if name.lower() == client.strip().lower():
            exact.append(entry)
        elif client.strip().lower() in name.lower():
            loose.append(entry)
    return exact or loose


def cmd_apply(args):
    number = args.case_number.strip().upper()
    if not RECEIPT.fullmatch(number):
        sys.exit(f"{number!r} 不像 USCIS 收据号（三位字母 + 十位数字）。确认后再写入表。")

    matches = find_row(args.client)
    if not matches:
        sys.exit(f"案件总表 法律 tab 里找不到客户 {args.client!r}。")
    if len(matches) > 1:
        listing = "\n".join(f"  行 {m['row']}: {m['name']}" for m in matches)
        sys.exit(f"{args.client!r} 匹配到多行，缩小名字再试：\n{listing}")
    row = matches[0]

    if number in row["note"]:
        print(json.dumps({"status": "already there", "row": row["row"],
                          "note": row["note"], "client_message": message(number)},
                         ensure_ascii=False, indent=2))
        return

    addition = f"Case No. {number}（{date.today().isoformat()}）"
    merged = f"{row['note']} | {addition}" if row["note"] else addition
    target = f"{TAB}!F{row['row']}"

    if not args.dry_run:
        gws(["sheets", "spreadsheets", "values", "update"],
            params={"spreadsheetId": TRACKING_SHEET, "range": target,
                    "valueInputOption": "USER_ENTERED"},
            body={"values": [[merged]]})

    print(json.dumps({"status": "dry-run" if args.dry_run else "updated",
                      "row": row["row"], "client": row["name"], "cell": target,
                      "was": row["note"], "now": merged,
                      "client_message": message(number)},
                     ensure_ascii=False, indent=2))


def message(number):
    return f"您的Case number：{number}\n查案子网站：{STATUS_URL}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("scan", help="search the signed-in mailbox")
    p.add_argument("--days", type=int, default=90)
    p.add_argument("--client", help="narrow the search to one client's name")
    p.add_argument("--max-results", type=int, default=40)
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser("apply", help="append the number to 案件总表 F 列")
    p.add_argument("--client", required=True)
    p.add_argument("--case-number", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_apply)

    args = ap.parse_args()
    try:
        args.func(args)
    except GwsError as exc:
        sys.exit(f"gws error: {exc}")


if __name__ == "__main__":
    main()
