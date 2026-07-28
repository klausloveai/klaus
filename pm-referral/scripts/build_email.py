#!/usr/bin/env python3
"""Build a base64url RFC822 message with a PDF attachment for the Gmail raw API.

Writes a JSON file {"raw": "..."} that is passed to:
    gws gmail users messages send --params '{"userId":"me"}' --json "$(cat out.json)"

Usage:
    python3 build_email.py --to <addr[,addr]> --from <addr> --subject <s> \
        --body-file <path> --attach <file.pdf> --attach-name <display.pdf> \
        --out <out.json> [--cc <addr>]

--body-file holds the plain-text email body. Multiple --attach/--attach-name
pairs may be repeated to attach more than one PDF (e.g. 1P + 3P in one email).
"""
import sys, json, base64, argparse, mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--to", required=True)
    p.add_argument("--from", dest="frm", required=True)
    p.add_argument("--cc")
    p.add_argument("--subject", required=True)
    p.add_argument("--body-file", required=True)
    p.add_argument("--attach", action="append", default=[])
    p.add_argument("--attach-name", action="append", default=[])
    p.add_argument("--out", required=True)
    a = p.parse_args()

    msg = MIMEMultipart()
    msg["To"] = a.to
    msg["From"] = a.frm
    if a.cc:
        msg["Cc"] = a.cc
    msg["Subject"] = a.subject
    msg.attach(MIMEText(open(a.body_file, encoding="utf-8").read(), "plain"))

    names = a.attach_name + [None] * (len(a.attach) - len(a.attach_name))
    for path, name in zip(a.attach, names):
        with open(path, "rb") as f:
            sub = (mimetypes.guess_type(path)[0] or "application/pdf").split("/")[-1]
            part = MIMEApplication(f.read(), _subtype=sub)
        part.add_header("Content-Disposition", "attachment",
                        filename=name or path.split("/")[-1])
        msg.attach(part)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    json.dump({"raw": raw}, open(a.out, "w"))
    print("OK: wrote", a.out)

if __name__ == "__main__":
    main()
