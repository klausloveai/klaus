#!/usr/bin/env python3
"""
RingCentral Fax sender — dependency-free (stdlib only).

Auth: JWT bearer flow. Reads credentials from ~/.ringcentral.env:
  RC_CLIENT_ID, RC_CLIENT_SECRET, RC_JWT, RC_SERVER (default production)

Usage:
  rc_fax.py --to +16262402046 --subject "Claim# 8812..." \
            [--note "Hi Adjuster, ..."] \
            [--attach "/path/a.pdf" --attach "/path/b.pdf"] \
            [--cover Classic] [--no-poll]

Cover page: defaults to "Classic". The subject + note are placed in the cover
page text (coverPageText). With --cover None (index 0) and no attachments you
get nothing useful, so a cover or an attachment is expected.

Prints a JSON result to stdout: {ok, id, status, pages, to, error}.
Exit code 0 on a submitted+non-failed fax, 1 otherwise.
"""
import argparse, base64, json, os, ssl, sys, time, urllib.parse, urllib.request, uuid

COVERS = {  # from GET /restapi/v1.0/dictionary/fax-cover-page
    "none": 0, "ancient": 1, "birthday": 2, "blank": 3, "clasmod": 4,
    "classic": 5, "confidential": 6, "contempo": 7, "elegant": 8,
    "express": 9, "formal": 10, "jazzy": 11, "modern": 12, "urgent": 13,
}


def load_env(path):
    env = {}
    with open(os.path.expanduser(path)) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def get_token(env):
    server = env.get("RC_SERVER", "https://platform.ringcentral.com")
    basic = base64.b64encode(f"{env['RC_CLIENT_ID']}:{env['RC_CLIENT_SECRET']}".encode()).decode()
    body = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": env["RC_JWT"],
    }).encode()
    st, txt = http(server + "/restapi/oauth/token", data=body, headers={
        "Authorization": "Basic " + basic,
        "Content-Type": "application/x-www-form-urlencoded",
    }, method="POST")
    d = json.loads(txt)
    if st != 200 or "access_token" not in d:
        raise SystemExit(json.dumps({"ok": False, "error": f"auth failed ({st})", "detail": d}))
    return server, d["access_token"]


def build_multipart(meta, attachments):
    boundary = "----rcfax" + uuid.uuid4().hex
    crlf = b"\r\n"
    buf = b""
    buf += b"--" + boundary.encode() + crlf
    buf += b'Content-Disposition: form-data; name="json"' + crlf
    buf += b"Content-Type: application/json" + crlf + crlf
    buf += json.dumps(meta).encode() + crlf
    for path in attachments:
        fn = os.path.basename(path)
        with open(path, "rb") as f:
            data = f.read()
        ctype = "application/pdf" if fn.lower().endswith(".pdf") else "application/octet-stream"
        buf += b"--" + boundary.encode() + crlf
        buf += f'Content-Disposition: form-data; name="attachment"; filename="{fn}"'.encode() + crlf
        buf += f"Content-Type: {ctype}".encode() + crlf + crlf
        buf += data + crlf
    buf += b"--" + boundary.encode() + b"--" + crlf
    return boundary, buf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True, help="destination fax number, E.164 (+1...)")
    ap.add_argument("--subject", required=True, help="cover subject (usually claim#)")
    ap.add_argument("--note", default="", help="optional cover note")
    ap.add_argument("--attach", action="append", default=[], help="file to attach (repeatable)")
    ap.add_argument("--cover", default="Classic", help="cover page name (default Classic)")
    ap.add_argument("--to-name", default="", help="optional recipient name for the cover")
    ap.add_argument("--env", default="~/.ringcentral.env")
    ap.add_argument("--no-poll", action="store_true")
    ap.add_argument("--resolution", default="High", choices=["High", "Low"])
    args = ap.parse_args()

    for p in args.attach:
        if not os.path.isfile(p):
            raise SystemExit(json.dumps({"ok": False, "error": f"attachment not found: {p}"}))

    env = load_env(args.env)
    cover_idx = COVERS.get(args.cover.strip().lower())
    if cover_idx is None:
        raise SystemExit(json.dumps({"ok": False, "error": f"unknown cover '{args.cover}'", "valid": list(COVERS)}))

    cover_text = ("Re: " + args.subject) if args.subject else ""
    if args.note:
        cover_text = (cover_text + "\n\n" + args.note) if cover_text else args.note

    to_obj = {"phoneNumber": args.to}
    if args.to_name:
        to_obj["name"] = args.to_name
    meta = {"to": [to_obj], "faxResolution": args.resolution, "coverIndex": cover_idx}
    if cover_text:
        meta["coverPageText"] = cover_text

    server, token = get_token(env)
    boundary, body = build_multipart(meta, args.attach)
    st, txt = http(
        server + "/restapi/v1.0/account/~/extension/~/fax",
        data=body,
        headers={"Authorization": "Bearer " + token,
                 "Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    d = json.loads(txt)
    mid = d.get("id")
    if not mid:
        print(json.dumps({"ok": False, "error": f"send failed ({st})", "detail": d}, indent=2))
        sys.exit(1)

    result = {"ok": True, "id": mid, "status": d.get("messageStatus"),
              "to": args.to, "cover": args.cover, "attachments": [os.path.basename(p) for p in args.attach]}

    if not args.no_poll:
        for _ in range(18):  # ~3 min max
            time.sleep(10)
            st, txt = http(server + f"/restapi/v1.0/account/~/extension/~/message-store/{mid}",
                           headers={"Authorization": "Bearer " + token})
            m = json.loads(txt)
            status = m.get("messageStatus")
            result["status"] = status
            result["pages"] = m.get("faxPageCount")
            err = (m.get("to") or [{}])[0].get("faxErrorCode")
            if err and err != "0":
                result["faxErrorCode"] = err
            if status in ("Sent", "Delivered", "SendingFailed", "DeliveryFailed", "Error"):
                break
        result["ok"] = result["status"] in ("Sent", "Delivered")

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
