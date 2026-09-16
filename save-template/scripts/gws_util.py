#!/usr/bin/env python3
"""Drive-agnostic gws-CLI helpers for the save-template skill (no third-party deps).

gws prints a "Using keyring backend ..." banner before its JSON, so every call
slices from the first '{' or '[' before json.loads. Every Drive call carries
supportsAllDrives/includeItemsFromAllDrives + corpora=allDrives so it works on
My Drive and on any shared drive without being told which one.
"""
import json, subprocess, sys

FOLDER_MIME = "application/vnd.google-apps.folder"


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


def drive_get(file_id, fields="id,name,mimeType,parents,driveId"):
    return gws(["drive", "files", "get"], params={
        "fileId": file_id, "supportsAllDrives": True, "fields": fields})


def drive_list(query, fields="files(id,name,mimeType)"):
    d = gws(["drive", "files", "list"], params={
        "q": query, "corpora": "allDrives",
        "includeItemsFromAllDrives": True, "supportsAllDrives": True,
        "fields": fields, "pageSize": 500})
    return (d or {}).get("files", [])


def drive_children(folder_id):
    return drive_list(f"'{folder_id}' in parents and trashed=false")


def find_child(parent_id, name):
    esc = name.replace("\\", "\\\\").replace("'", "\\'")
    hits = drive_list(f"'{parent_id}' in parents and name='{esc}' and trashed=false")
    return hits[0] if hits else None


def create_folder(name, parent_id):
    d = gws(["drive", "files", "create"], json_body={
        "name": name, "mimeType": FOLDER_MIME, "parents": [parent_id]},
        params={"supportsAllDrives": True, "fields": "id,name"})
    return d["id"]


def copy_file(file_id, new_name, parent_id):
    d = gws(["drive", "files", "copy"], params={
        "fileId": file_id, "supportsAllDrives": True, "fields": "id,name"},
        json_body={"name": new_name, "parents": [parent_id]})
    return d["id"]


def rename(file_id, new_name):
    return gws(["drive", "files", "update"], params={
        "fileId": file_id, "supportsAllDrives": True, "fields": "id,name"},
        json_body={"name": new_name})


def trash(file_id):
    return gws(["drive", "files", "update"], params={
        "fileId": file_id, "supportsAllDrives": True, "fields": "id,trashed"},
        json_body={"trashed": True})


def web_link(file_id):
    return f"https://drive.google.com/drive/folders/{file_id}"
