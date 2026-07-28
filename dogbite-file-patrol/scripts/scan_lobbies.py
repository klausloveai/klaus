#!/usr/bin/env python3
"""Scan every Dog Bite case folder's LOBBY for loose (to-be-sorted) files.

Lobby norm (Klaus, 2026-07-02): a case folder's root should contain ONLY
  - `0. Case Intake.docx`  (and any other `0. ` file)
  - `<Client> - Intake Sheet`  (a Google Sheet)
  - the numbered subfolders `1. … 6. …`
Anything else loose in the root is a NEW file the client/Klaus dropped in and is
"to-be-sorted". This script lists those, per case, for the patrol to classify.

WHITELIST (never touched): folders, any name starting with "0.", and the intake
sheet (a Google Sheet). Everything else at root = a to-sort candidate.

Usage:  python3 scan_lobbies.py [DOG_BITE_CASES_ID]
Prints JSON: [{case, case_id, loose:[{id,name,mime}]}] — only cases with loose files.
"""
import sys, json
from gws_util import drive_children

DOG_BITE_CASES = "1ewaJIoeLHoc3lG3dIyDTfWwuSt6HYRVt"
FOLDER = "application/vnd.google-apps.folder"
SHEET = "application/vnd.google-apps.spreadsheet"


def is_whitelisted(f):
    name, mime = f["name"], f["mimeType"]
    if mime == FOLDER:
        return True
    if name.startswith("0."):
        return True
    if mime == SHEET and name.rstrip().endswith("Intake Sheet"):
        return True
    return False


# A case is "new template" only if it has these numbered subfolders. Legacy dog-bite
# cases use a different 4-folder layout and keep intake/POE/SCM loose in root ON PURPOSE
# — the patrol must SKIP them, never sort them.
REQUIRED_SUBFOLDERS = ["1. Incident & Liability", "3. Medical Record & Bill"]


def is_new_template(children):
    names = {c["name"] for c in children if c["mimeType"] == FOLDER}
    return all(req in names for req in REQUIRED_SUBFOLDERS)


def main():
    cases_id = sys.argv[1] if len(sys.argv) > 1 else DOG_BITE_CASES
    out, skipped = [], []
    for case in drive_children(cases_id):
        if case["mimeType"] != FOLDER:
            continue
        children = drive_children(case["id"])
        if not is_new_template(children):
            skipped.append(case["name"])          # legacy layout — leave alone
            continue
        loose = [{"id": f["id"], "name": f["name"], "mime": f["mimeType"]}
                 for f in children if not is_whitelisted(f)]
        if loose:
            out.append({"case": case["name"], "case_id": case["id"], "loose": loose})
    print(json.dumps({"to_sort": out, "skipped_legacy": skipped},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
