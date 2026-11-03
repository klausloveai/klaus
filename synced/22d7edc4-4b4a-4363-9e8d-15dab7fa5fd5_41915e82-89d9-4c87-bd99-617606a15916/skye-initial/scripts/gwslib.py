#!/usr/bin/env python3
"""Thin shared wrapper around the `gws` CLI for the skye-initial scripts.

Kept as its own module because both scripts need the same three things and
getting any of them subtly wrong fails silently rather than loudly:

  * every Drive call carries the allDrives params (a shared-drive list without
    them returns an empty `files` array, not an error — which reads as "the
    folder is empty" when it very much isn't),
  * `gws` prints a JSON error object with exit code 0 in some paths, so the
    return value has to be inspected rather than just the return code,
  * listing has to follow nextPageToken; a case with 200+ evidence files is
    normal here and a single page would quietly drop the tail.
"""

import json
import subprocess

FOLDER_MIME = "application/vnd.google-apps.folder"
DOC_MIME = "application/vnd.google-apps.document"

ALL_DRIVES = {
    "supportsAllDrives": True,
    "includeItemsFromAllDrives": True,
    "corpora": "allDrives",
}


class GwsError(RuntimeError):
    pass


def gws(args, params=None, body=None):
    cmd = ["gws"] + args
    if params is not None:
        cmd += ["--params", json.dumps(params, ensure_ascii=False)]
    if body is not None:
        cmd += ["--json", json.dumps(body, ensure_ascii=False)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise GwsError(f"{' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    out = proc.stdout.strip()
    if not out:
        return {}
    # gws prints a keyring banner on stderr, but some builds leak it to stdout;
    # take the JSON document that starts at the first brace.
    brace = out.find("{")
    if brace > 0:
        out = out[brace:]
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        raise GwsError(f"{' '.join(args)} returned non-JSON: {out[:400]}")
    if isinstance(data, dict) and "error" in data:
        raise GwsError(f"{' '.join(args)}: {json.dumps(data['error'], ensure_ascii=False)}")
    return data


def list_children(folder_id, fields="files(id,name,mimeType,size,createdTime,appProperties,lastModifyingUser(emailAddress))"):
    """Every child of a folder, following pagination."""
    files, token = [], None
    while True:
        params = dict(ALL_DRIVES)
        params.update({
            "q": f"'{folder_id}' in parents and trashed=false",
            "fields": f"nextPageToken,{fields}",
            "orderBy": "folder,name",
            "pageSize": 200,
        })
        if token:
            params["pageToken"] = token
        page = gws(["drive", "files", "list"], params=params)
        files.extend(page.get("files", []))
        token = page.get("nextPageToken")
        if not token:
            return files


def walk(folder_id, prefix=""):
    """Depth-first walk. Yields (file_dict, path) for files only, folders recursed."""
    for f in list_children(folder_id):
        path = f"{prefix}/{f['name']}" if prefix else f["name"]
        if f["mimeType"] == FOLDER_MIME:
            yield from walk(f["id"], path)
        else:
            yield f, path


def find_child(folder_id, name, folders_only=True):
    """First child matching `name` exactly, then by prefix. None if absent.

    Prefix matching is not laziness: staff mark a finished folder by prepending
    or appending a tick ("✅ 奖项", "个人信息 ✅"), so an exact-match-only lookup
    stops finding the folder the moment someone marks it done.
    """
    kids = list_children(folder_id, fields="files(id,name,mimeType)")
    if folders_only:
        kids = [k for k in kids if k["mimeType"] == FOLDER_MIME]
    for k in kids:
        if k["name"] == name:
            return k
    stripped = name.strip()
    for k in kids:
        kn = k["name"].replace("✅", "").strip()
        if kn == stripped or kn.startswith(stripped) or stripped.startswith(kn):
            return k
    return None


def create_folder(name, parent):
    return gws(
        ["drive", "files", "create"],
        params={"supportsAllDrives": True, "fields": "id,name"},
        body={"name": name, "mimeType": FOLDER_MIME, "parents": [parent]},
    )


def ensure_folder(name, parent, cache=None):
    """Idempotent folder creation. Returns (id, created_bool)."""
    key = (parent, name)
    if cache is not None and key in cache:
        return cache[key], False
    existing = find_child(parent, name)
    if existing:
        if cache is not None:
            cache[key] = existing["id"]
        return existing["id"], False
    made = create_folder(name, parent)
    if cache is not None:
        cache[key] = made["id"]
    return made["id"], True


def folder_link(fid):
    return f"https://drive.google.com/drive/folders/{fid}"


def file_link(fid):
    return f"https://drive.google.com/file/d/{fid}/view"
