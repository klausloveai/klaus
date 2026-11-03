#!/usr/bin/env python3
"""Who gets told what, in one place.

Every automatic message this skill sends goes to firm addresses only. Nothing
here can reach a client: the client-facing wording produced by meeting.py and
case_number.py is printed for a person to read, adjust and send. That split is
deliberate — an automation that mails clients on its own will eventually mail
the wrong one about the wrong case, and no apology takes that back.

Sender is whichever account gws is authenticated as. On KK's machine that's
kk@; installed on Skye's it's skye@. The recipient lists below stay the same
either way, so a digest sent from Skye's machine still reaches KK.
"""

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gwslib import GwsError  # noqa: E402

# Firm recipients. Change here, not in the individual scripts.
NEW_MATERIALS = ["kk@lingtulaw.com", "cathy.c@lingtulaw.com", "skye.s@lingtulaw.com"]
PROGRESS_REPORT = ["kk@lingtulaw.com", "cathy.c@lingtulaw.com"]
MEETING_CONFIRM = ["skye.s@lingtulaw.com"]
MEETING_CONFIRM_CC = ["cassie@lingtulaw.com"]

AUDIENCES = {
    "new-materials": (NEW_MATERIALS, []),
    "progress": (PROGRESS_REPORT, []),
    "meeting": (MEETING_CONFIRM, MEETING_CONFIRM_CC),
}


def send(audience, subject, body, dry_run=False):
    """Send to a named internal audience. Returns a result dict."""
    if audience not in AUDIENCES:
        raise ValueError(f"unknown audience {audience!r}; expected one of {list(AUDIENCES)}")
    to, cc = AUDIENCES[audience]
    for addr in to + cc:
        if not addr.endswith("@lingtulaw.com"):
            # The one hard stop. Everything this module sends is internal.
            raise GwsError(f"refusing to send to non-firm address {addr!r}")
    cmd = ["gws", "gmail", "+send", "--to", ",".join(to),
           "--subject", subject, "--body", body]
    if cc:
        cmd += ["--cc", ",".join(cc)]
    if dry_run:
        return {"status": "dry-run", "to": to, "cc": cc,
                "subject": subject, "body": body}
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise GwsError(f"send failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return {"status": "sent", "to": to, "cc": cc, "subject": subject}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audience", required=True, choices=sorted(AUDIENCES))
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    body = open(args.body_file, encoding="utf-8").read()
    try:
        print(json.dumps(send(args.audience, args.subject, body, args.dry_run),
                         ensure_ascii=False))
    except (GwsError, ValueError) as exc:
        sys.exit(str(exc))


if __name__ == "__main__":
    main()
