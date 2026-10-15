"""Thin wrapper around the gws CLI for klaus@ Gmail.

Every pitfall hit while building this skill is handled here, so the other
scripts never call gws directly:
  * gws prints "Using keyring backend: keyring" (sometimes after the JSON),
    so output is parsed with raw_decode from the first "{".
  * Request bodies (ids, addLabelIds, removeLabelIds) must go in --json;
    putting them in --params gives "400 Invalid ids value".
  * More than ~6 parallel calls trips the per-minute quota (403), so callers
    use WORKERS and every call retries on 403/429/5xx with backoff.
"""
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

GWS = "/Users/klaus/.local/bin/gws"
WORKERS = 5
_RETRY = (403, 429, 500, 502, 503)


def _parse(out):
    i = out.find("{")
    if i < 0:
        return {}
    obj, _ = json.JSONDecoder().raw_decode(out[i:])
    return obj


def call(*args, params=None, body=None, tries=5):
    cmd = [GWS, *args]
    if params is not None:
        cmd += ["--params", json.dumps(params, ensure_ascii=False)]
    if body is not None:
        cmd += ["--json", json.dumps(body, ensure_ascii=False)]
    for n in range(tries):
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
        d = _parse(out)
        code = (d.get("error") or {}).get("code")
        if code in _RETRY and n < tries - 1:
            time.sleep(2 ** n + 1)
            continue
        return d
    return d


def pmap(fn, items):
    with ThreadPoolExecutor(WORKERS) as ex:
        return list(ex.map(fn, items))


def labels():
    """{id: name} for user labels."""
    d = call("gmail", "users", "labels", "list", params={"userId": "me"})
    return {l["id"]: l["name"] for l in d.get("labels", []) if l.get("type") == "user"}


def list_threads(q=None, label_ids=None, cap=2000):
    out, tok = [], None
    while True:
        p = {"userId": "me", "maxResults": 500}
        if q:
            p["q"] = q
        if label_ids:
            p["labelIds"] = label_ids
        if tok:
            p["pageToken"] = tok
        d = call("gmail", "users", "threads", "list", params=p)
        out += [t["id"] for t in d.get("threads", [])]
        tok = d.get("nextPageToken")
        if not tok or len(out) >= cap:
            return out[:cap]


def get_thread(tid, fmt="full"):
    return call("gmail", "users", "threads", "get",
                params={"userId": "me", "id": tid, "format": fmt})


def modify_thread(tid, add=None, remove=None):
    body = {}
    if add:
        body["addLabelIds"] = add
    if remove:
        body["removeLabelIds"] = remove
    return call("gmail", "users", "threads", "modify",
                params={"userId": "me", "id": tid}, body=body)


def search_messages(q, cap=20):
    d = call("gmail", "users", "messages", "list",
             params={"userId": "me", "q": q, "maxResults": cap})
    return [m["id"] for m in d.get("messages", [])]


def get_message(mid, fmt="metadata"):
    p = {"userId": "me", "id": mid, "format": fmt}
    if fmt == "metadata":
        p["metadataHeaders"] = ["From", "To", "Cc", "Subject", "Date"]
    return call("gmail", "users", "messages", "get", params=p)
