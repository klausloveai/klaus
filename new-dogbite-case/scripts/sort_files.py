#!/usr/bin/env python3
"""Upload the intake zip's files, renamed, into the right case subfolders.

Takes a routing.json produced by the skill after reading the zip:
  {
    "subfolders": { "1. Incident & Liability": "<id>", ... },   # from build_case.py
    "files": [
      {"src": "/abs/path/ER Medical Records.pdf",
       "subfolder": "3. Medical Record & Bill",
       "newname": "Bo Tao - ER Records (Community Memorial) 6-27-26.pdf"},
      ...
    ]
  }

Skips macOS junk (.DS_Store, ._*). Prints a JSON report of uploads.
"""
import sys, json, os

sys.path.insert(0, os.path.dirname(__file__))
from gws_util import upload_file

CT = {".pdf": "application/pdf", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
      ".png": "image/png", ".mov": "video/quicktime", ".mp4": "video/mp4",
      ".heic": "image/heic", ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      ".doc": "application/msword", ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}


def main():
    plan = json.load(open(sys.argv[1]))
    subs = plan["subfolders"]
    report = []
    for f in plan["files"]:
        src, sub, newname = f["src"], f["subfolder"], f["newname"]
        base = os.path.basename(src)
        if base == ".DS_Store" or base.startswith("._"):
            continue
        if sub not in subs:
            report.append({"file": newname, "error": f"unknown subfolder {sub!r}"})
            continue
        ct = CT.get(os.path.splitext(base)[1].lower(), "application/octet-stream")
        res = upload_file(src, newname, subs[sub], ct)
        report.append({"file": newname, "subfolder": sub, "id": res.get("id")})
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
