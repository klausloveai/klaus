#!/usr/bin/env python3
"""Duplicate the Dog Bite Case Template into a new case folder (recursive).

Drive's files.copy copies single files only, not folders, so we recreate the
folder tree and copy each contained file. The template's "0. Intake Sheet"
Google Sheet is copied (renamed to "<Case> - Intake Sheet"); the six numbered
subfolders are recreated (they are empty placeholders, but we recurse in case
the firm adds seed files later).

Usage:
  python3 build_case.py <TEMPLATE_FOLDER_ID> <DOG_BITE_CASES_ID> "<Case Name-DOL>" "<Client>"

Prints JSON: {"case_folder_id", "subfolders": {name:id}, "intake_sheet_id"}.
"""
import sys, json
from gws_util import drive_children, create_folder, copy_file

INTAKE_SHEET_MIME = "application/vnd.google-apps.spreadsheet"
FOLDER_MIME = "application/vnd.google-apps.folder"


def copy_tree(src_folder_id, dst_folder_id, client, out):
    for child in drive_children(src_folder_id):
        name, mime, cid = child["name"], child["mimeType"], child["id"]
        if mime == FOLDER_MIME:
            new_id = create_folder(name, dst_folder_id)
            out["subfolders"][name] = new_id
            copy_tree(cid, new_id, client, out)  # recurse (usually empty)
        elif mime == INTAKE_SHEET_MIME:
            new_name = f"{client} - Intake Sheet"
            out["intake_sheet_id"] = copy_file(cid, new_name, dst_folder_id)
            out["intake_sheet_name"] = new_name
        else:
            out["other_files"][name] = copy_file(cid, name, dst_folder_id)


def main():
    tmpl_id, cases_id, case_name, client = sys.argv[1:5]
    case_folder_id = create_folder(case_name, cases_id)
    out = {"case_folder_id": case_folder_id, "case_name": case_name,
           "subfolders": {}, "intake_sheet_id": None, "other_files": {}}
    copy_tree(tmpl_id, case_folder_id, client, out)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
