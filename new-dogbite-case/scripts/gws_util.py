#!/usr/bin/env python3
"""Shared gws-CLI helpers for the new-dogbite-case skill (no third-party deps).

gws prints a "Using keyring backend ..." banner before its JSON, so every
call slices from the first '{' or '[' before json.loads. All Drive calls carry
supportsAllDrives/includeItemsFromAllDrives so they work on the Hernan Simo
Cases *shared drive*.
"""
import json, subprocess, sys

HERNAN_DRIVE_ID = "0APtYw9adyTl8Uk9PVA"  # "Hernan Simo Cases" shared drive


def gws(args, params=None, json_body=None, upload=None, upload_ct=None, out=None):
    """Run a gws command, return parsed JSON (or None for -o downloads)."""
    cmd = ["gws"] + args
    if params is not None:
        cmd += ["--params", json.dumps(params)]
    if json_body is not None:
        cmd += ["--json", json.dumps(json_body)]
    if upload is not None:
        cmd += ["--upload", upload]
    if upload_ct is not None:
        cmd += ["--upload-content-type", upload_ct]
    if out is not None:
        cmd += ["-o", out]
    cmd += ["--format", "json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(f"gws failed: {' '.join(args)}\n{r.stderr}\n")
        raise SystemExit(1)
    s = r.stdout
    i = min([x for x in (s.find("{"), s.find("[")) if x != -1] or [-1])
    if i == -1:
        return None
    return json.loads(s[i:])


def drive_list(query, fields="files(id,name,mimeType)"):
    d = gws(["drive", "files", "list"], params={
        "q": query, "corpora": "drive", "driveId": HERNAN_DRIVE_ID,
        "includeItemsFromAllDrives": True, "supportsAllDrives": True,
        "fields": fields, "pageSize": 500})
    return (d or {}).get("files", [])


def drive_children(folder_id):
    return drive_list(f"'{folder_id}' in parents and trashed=false")


def create_folder(name, parent_id):
    d = gws(["drive", "files", "create"], json_body={
        "name": name, "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id]},
        params={"supportsAllDrives": True, "fields": "id,name"})
    return d["id"]


def copy_file(file_id, new_name, parent_id):
    d = gws(["drive", "files", "copy"], params={
        "fileId": file_id, "supportsAllDrives": True, "fields": "id,name"},
        json_body={"name": new_name, "parents": [parent_id]})
    return d["id"]


def upload_file(local_path, name, parent_id, content_type):
    d = gws(["drive", "files", "create"], upload=local_path, upload_ct=content_type,
            json_body={"name": name, "parents": [parent_id]},
            params={"supportsAllDrives": True, "fields": "id,name,webViewLink"})
    return d
