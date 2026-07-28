#!/usr/bin/env python3
"""Apply the patrol's classification decisions: MOVE loose lobby files into subfolders.

Takes a decisions.json the patrol builds after classifying each loose file:
  {
    "moves": [
      {"file_id": "...", "case": "Bo Tao-062726",
       "from_parent": "<case_folder_id>", "to_parent": "<subfolder_id>",
       "subfolder": "1. Incident & Liability",
       "new_name": "Incident Scene Photo.jpg",   # optional; omit to keep name
       "old_name": "IMG_9001.jpg"}
    ]
  }

SAFETY: only MOVES within the same case (addParents=subfolder, removeParents=case
root). Never deletes, never crosses cases. Files the patrol was UNSURE about are
simply omitted from "moves" (they stay in the lobby and are reported to Klaus).

Usage:  python3 apply_moves.py <decisions.json>
Prints a JSON report of what moved.
"""
import sys, json, os

sys.path.insert(0, os.path.dirname(__file__))
from gws_util import gws


def main():
    plan = json.load(open(sys.argv[1]))
    report = []
    for m in plan.get("moves", []):
        params = {"fileId": m["file_id"], "addParents": m["to_parent"],
                  "removeParents": m["from_parent"], "supportsAllDrives": True,
                  "fields": "id,name,parents"}
        body = {"name": m["new_name"]} if m.get("new_name") else None
        try:
            r = gws(["drive", "files", "update"], params=params, json_body=body)
            report.append({"case": m.get("case"), "file": r.get("name"),
                           "moved_to": m.get("subfolder"), "ok": True})
        except SystemExit:
            report.append({"case": m.get("case"), "file": m.get("old_name"),
                           "moved_to": m.get("subfolder"), "ok": False})
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
