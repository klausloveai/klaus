#!/usr/bin/env python3
"""Gmail DRAFTS for lien-reduction emails (never sends).

Find candidate threads with a provider:
    python3 make_draft.py find --client "Zhiping Liu" --terms "TBI,Apogee" [--box claims]

Create a draft (reply in an existing thread, reply-all):
    python3 make_draft.py draft --kind lien --thread 1a0499... --to settle@x.com \
        --greeting "Hi Evelyn and Apogee team," --attach "/path/letter.pdf" --label "Zhiping Liu" [--dry-run]

    --kind w9  (no attachment)  asks the provider/billing company for a W-9.
    No --thread → new thread; then --subject and --to are required.
    --box claims|piteam|picase  works in that team mailbox (default: klaus@).
"""
import argparse, base64, json, os, subprocess, sys, tempfile
from email.message import EmailMessage
from email.utils import getaddresses

BODY = {
    "lien": "Lien reduction is attached. Please confirm receipt and let me know if there are any questions.",
    "w9": "{client}'s case has resolved. Please send us a W-9 for the payee on this account so we can "
          "prepare the lien reduction request.",
}
BOXES = {"claims": "~/.config/gws-claims", "piteam": "~/.config/gws-piteam", "picase": "~/.config/gws-picase"}


def gws(args, box=None, body=None, upload=None):
    env = dict(os.environ)
    if box:
        env["GOOGLE_WORKSPACE_CLI_CONFIG_DIR"] = os.path.expanduser(BOXES[box])
        env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"
    cmd = ["gws"] + args
    if body is not None:
        cmd += ["--json", json.dumps(body)]
    if upload:
        cmd += ["--upload", upload, "--upload-content-type", "message/rfc822"]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(f"gws failed ({' '.join(args[:4])}): {(r.stdout or r.stderr)[:300]}")
    if isinstance(d, dict) and d.get("error"):
        sys.exit(f"gws error {d['error'].get('code')}: {d['error'].get('message')} "
                 f"{'(re-auth this mailbox)' if d['error'].get('code') == 401 else ''}")
    return d


def hdr(m, k):
    return next((h["value"] for h in m["payload"]["headers"] if h["name"].lower() == k.lower()), "")


def me(box):
    return gws(["gmail", "users", "getProfile", "--params", json.dumps({"userId": "me"})], box)["emailAddress"].lower()


def cmd_find(a):
    """Provider threads only: match the provider's mail domains (best) or name terms, then drop
    threads where nobody outside the firm took part, and rank threads that include a provider-side
    address first."""
    parts = []
    doms = [d.strip().lstrip("@") for d in (a.domains or "").split(",") if d.strip()]
    for d in doms:
        parts += [f"from:{d}", f"to:{d}", f"cc:{d}"]
    parts += [f'"{t.strip()}"' for t in (a.terms or "").split(",") if t.strip()]
    if not parts:
        sys.exit("give --domains and/or --terms")
    q = f'"{a.client}" (' + " OR ".join(parts) + ")"
    d = gws(["gmail", "users", "threads", "list", "--params",
             json.dumps({"userId": "me", "q": q, "maxResults": 30})], a.box)
    keys = [x.lower() for x in doms] + [w.lower() for t in (a.terms or "").split(",") for w in t.split() if len(w) > 3]
    rows = []
    for t in d.get("threads", []):
        th = gws(["gmail", "users", "threads", "get", "--params", json.dumps(
            {"userId": "me", "id": t["id"], "format": "metadata",
             "metadataHeaders": ["From", "To", "Cc", "Subject", "Date"]})], a.box)
        msgs = [m for m in th["messages"] if "DRAFT" not in m.get("labelIds", [])]
        people = {x[1].lower() for m in msgs for k in ("From", "To", "Cc")
                  for x in getaddresses([hdr(m, k)]) if x[1]}
        outside = {p for p in people if not p.endswith("@lingtulaw.com")}
        if not outside:
            continue                                   # internal only — never the provider thread
        provider_side = {p for p in outside if any(k in p for k in keys)}
        rows.append((len(provider_side), t["id"], msgs, outside, provider_side))
    rows.sort(key=lambda r: (-r[0], r[1]), reverse=False)
    for score, tid, msgs, outside, prov in rows:
        last = msgs[-1]
        tag = "PROVIDER" if score else "external"
        print(f"[{tag}] {tid} | {len(msgs)} msgs | last {hdr(last, 'Date')[:22]} from {hdr(last, 'From')[:40]}\n"
              f"    subj: {hdr(last, 'Subject')[:90]}\n    outside: {', '.join(sorted(outside))[:200]}")
    if not rows:
        print("no provider thread found — a new thread is needed")


def label_id(name, box):
    labels = gws(["gmail", "users", "labels", "list", "--params", json.dumps({"userId": "me"})], box)["labels"]
    hits = [l for l in labels if name.lower() in l["name"].lower()]
    if len(hits) != 1:
        sys.exit(f"label {name!r}: {len(hits)} matches {[l['name'] for l in hits]} — ask Klaus, don't create one")
    return hits[0]["id"], hits[0]["name"]


def signature(box):
    for s in gws(["gmail", "users", "settings", "sendAs", "list", "--params", json.dumps({"userId": "me"})], box)["sendAs"]:
        if s.get("isDefault"):
            return s["sendAsEmail"], s.get("displayName", ""), s.get("signature", "")
    sys.exit("no default sendAs")


def cmd_draft(a):
    my = me(a.box)
    sender, display, sig = signature(a.box)
    msg = EmailMessage()
    msg["From"] = f"{display} <{sender}>" if display else sender
    if a.thread:
        th = gws(["gmail", "users", "threads", "get", "--params", json.dumps(
            {"userId": "me", "id": a.thread, "format": "metadata",
             "metadataHeaders": ["Message-ID", "From", "To", "Cc", "Subject"]})], a.box)
        msgs = [m for m in th["messages"] if "DRAFT" not in m.get("labelIds", [])]
        mids = [hdr(m, "Message-ID") for m in msgs if hdr(m, "Message-ID")]
        people = []
        for m in msgs[-1:]:                              # reply-all = the LAST real message's From/To/Cc (as Gmail does)
            for k in ("From", "To", "Cc"):
                for n, ad in getaddresses([hdr(m, k)]):
                    ad = ad.lower()
                    if ad and ad != my and ad not in [p[1] for p in people]:
                        people.append((n, ad))
        to = [x.strip().lower() for x in (a.to or "").split(",") if x.strip()] or [people[0][1]]
        extra_cc = [x.strip().lower() for x in (a.cc or "").split(",") if x.strip()]
        fmt = lambda xs: ", ".join(f'"{n}" <{ad}>' if n else ad for n, ad in xs)
        to_list = [p for p in people if p[1] in to] + [("", t) for t in to if t not in [p[1] for p in people]]
        cc_list = [p for p in people if p[1] not in to] + [("", c) for c in extra_cc if c not in [p[1] for p in people]]
        subj = hdr(msgs[-1], "Subject")
        msg["To"] = fmt(to_list)
        if cc_list:
            msg["Cc"] = fmt(cc_list)
        msg["Subject"] = subj if subj.lower().startswith("re:") else "Re: " + subj
        msg["In-Reply-To"] = mids[-1]
        msg["References"] = " ".join(mids)
    else:
        if not (a.to and a.subject):
            sys.exit("new thread needs --to and --subject")
        msg["To"] = a.to
        if a.cc:
            msg["Cc"] = a.cc
        msg["Subject"] = a.subject
    text = BODY[a.kind].format(client=a.client or "The client")
    html = f"<div>{a.greeting}</div><br><div>{text}</div><br><div>{sig}</div>"
    msg.set_content(f"{a.greeting}\n\n{text}\n")
    msg.add_alternative(f"<html><body>{html}</body></html>", subtype="html")
    if a.kind == "lien":
        if not a.attach:
            sys.exit("lien email needs --attach")
        msg.add_attachment(open(a.attach, "rb").read(), maintype="application", subtype="pdf",
                           filename=os.path.basename(a.attach))
    lid, lname = label_id(a.label, a.box) if a.label else (None, None)
    print(f"FROM:  {msg['From']}\nTO:    {msg['To']}\nCC:    {msg.get('Cc', '')}\nSUBJ:  {msg['Subject']}\n"
          f"THREAD: {a.thread or '(new)'}\nLABEL: {lname}\nATTACH: {os.path.basename(a.attach) if a.attach else '-'}\n"
          f"BODY:\n  {a.greeting}\n  {text}")
    if a.dry_run:
        print("DRY RUN — nothing written to Gmail"); return
    with tempfile.NamedTemporaryFile(suffix=".eml", delete=False) as f:
        f.write(bytes(msg)); eml = f.name
    body = {"message": {"threadId": a.thread}} if a.thread else {}
    args = ["gmail", "users", "drafts"] + (["update", "--params", json.dumps({"userId": "me", "id": a.update})]
                                           if a.update else ["create", "--params", json.dumps({"userId": "me"})])
    d = gws(args, a.box, body=body, upload=eml)
    os.unlink(eml)
    tid = d["message"]["threadId"]
    if a.thread and tid != a.thread:
        print(f"WARNING: draft landed in thread {tid}, expected {a.thread}")
    if lid:
        gws(["gmail", "users", "threads", "modify", "--params", json.dumps({"userId": "me", "id": tid})],
            a.box, body={"addLabelIds": [lid]})
    print(f"DRAFT {d['id']} in thread {tid} (labeled: {lname})")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    f = sp.add_parser("find"); f.add_argument("--client", required=True); f.add_argument("--terms"); f.add_argument("--domains")
    f.add_argument("--box", choices=list(BOXES))
    d = sp.add_parser("draft")
    d.add_argument("--kind", choices=["lien", "w9"], required=True)
    d.add_argument("--thread"); d.add_argument("--to"); d.add_argument("--cc"); d.add_argument("--subject")
    d.add_argument("--greeting", default="Hi Doctor Office,"); d.add_argument("--attach")
    d.add_argument("--client"); d.add_argument("--label"); d.add_argument("--update", help="existing draft id to replace")
    d.add_argument("--box", choices=list(BOXES)); d.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    {"find": cmd_find, "draft": cmd_draft}[a.cmd](a)


if __name__ == "__main__":
    main()
