#!/usr/bin/env python3
"""Upload Downloads files into Drive case folders, then read back the MD5.

Plan file (JSON list):
  [{"path": "<relative to ~/Downloads>", "folder_id": "...", "name": "<Drive name>",
    "replace_id": "<optional: existing Drive file to replace in place>"}]

  * new file  -> files.create into folder_id
  * replace_id -> files.update on that id (Drive keeps the old one in version
    history) -- use when the folder already holds an older version of the SAME
    document: one current version per document in Drive.
Always uploadType=multipart (media corrupts the file -- see memory
gws_drive_binary_update). Exits non-zero if any MD5 does not match.

  archive.py plan.json [--dry-run]
"""
import argparse, hashlib, json, mimetypes, os, subprocess, sys

GWS = "/Users/klaus/.local/bin/gws"
ROOT = os.path.expanduser("~/Downloads")


def parse(out):
    i = out.find("{")
    return json.JSONDecoder().raw_decode(out[i:])[0] if i >= 0 else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    bad = 0
    for it in json.load(open(a.plan)):
        p = os.path.join(ROOT, it["path"])
        local = hashlib.md5(open(p, "rb").read()).hexdigest()
        ctype = mimetypes.guess_type(p)[0] or "application/octet-stream"
        if a.dry_run:
            print(f"DRY  {it['path']} → {it['name']} ({'replace ' + it['replace_id'] if it.get('replace_id') else 'new in ' + it['folder_id']})")
            continue
        fields = "id,name,md5Checksum,mimeType,parents"
        if it.get("replace_id"):
            cmd = [GWS, "drive", "files", "update", "--params", json.dumps(
                {"fileId": it["replace_id"], "supportsAllDrives": True, "uploadType": "multipart", "fields": fields}),
                "--json", json.dumps({"name": it["name"]})]
        else:
            cmd = [GWS, "drive", "files", "create", "--params", json.dumps(
                {"supportsAllDrives": True, "uploadType": "multipart", "fields": fields}),
                "--json", json.dumps({"name": it["name"], "parents": [it["folder_id"]]})]
        cmd += ["--upload", p, "--upload-content-type", ctype]
        d = parse(subprocess.run(cmd, capture_output=True, text=True).stdout)
        ok = d.get("md5Checksum") == local and not d.get("mimeType", "").startswith("multipart/")
        bad += not ok
        print(f"{'OK  ' if ok else 'FAIL'} {it['path']} → {d.get('name')} id={d.get('id')} md5 {local} / {d.get('md5Checksum')}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
