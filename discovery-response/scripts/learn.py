#!/usr/bin/env python3
"""learn.py — diff our draft against the attorney's returned version.

Run this the moment a review comes back. It produces the raw change list that
feeds a revisions/ entry; you still have to read the attorney's covering email
for the *reason*, which is the part that becomes a rule.

    python3 learn.py --mine draft.docx --theirs returned.pdf --kind FROG
    python3 learn.py --mine draft.docx --theirs returned.pdf --kind RFP

Both .docx and .pdf are accepted on either side. Cosmetic-only changes (dates
written out, addresses spelled out, pin cites) are separated from substantive
ones so the substantive list stays short enough to actually read.
"""
import argparse, difflib, os, re, subprocess, sys, tempfile

KINDS = {"FROG": "FORM INTERROGATORY", "SROG": "SPECIAL INTERROGATORY",
         "RFP": "REQUEST FOR PRODUCTION", "RFA": "REQUEST FOR ADMISSION"}

MONTHS = [None, "January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
ABBREV = [("Pkwy", "Parkway"), ("Blvd", "Boulevard"), ("Ste", "Suite"),
          ("Ave", "Avenue"), ("Dr", "Drive"), ("Rd", "Road"), ("St", "Street"),
          ("N", "North"), ("S", "South"), ("E", "East"), ("W", "West"),
          ("CA", "California"), ("Esq", ""), ("Inc", "Incorporated"),
          ("MRI", "magnetic resonance imaging"), ("CT", "computed tomography")]
NOISE = re.compile(r'^[\d\s_]*$')          # stray pleading line numbers, rules

def norm(s):
    """Collapse the differences that are pure house style, so what survives is meaning."""
    s = re.sub(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',
               lambda m: "%s %d, %s" % (MONTHS[int(m.group(1))], int(m.group(2)), m.group(3)), s)
    for a, b in ABBREV:
        s = re.sub(r'\b' + re.escape(a) + r'\b\.?', b, s)
    s = re.sub(r'\b\d{3}(-\d{3})?\b', 'PIN', s)     # pin cites
    s = re.sub(r'[^A-Za-z0-9]+', ' ', s).lower()
    return re.sub(r'\s+', ' ', s).strip()

def text_of(path):
    if path.lower().endswith(".pdf"):
        t = subprocess.run(["pdftotext", "-layout", path, "-"],
                           capture_output=True, text=True).stdout
    else:
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", path,
                            "--outdir", td], capture_output=True)
            pdf = os.path.join(td, os.path.splitext(os.path.basename(path))[0] + ".pdf")
            t = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                               capture_output=True, text=True).stdout
    t = re.sub(r'\n\s*\d+\s+', ' ', t)                 # pleading line numbers
    t = re.sub(r'PLAINTIFF .*?SET ONE', '', t, flags=re.S)   # running footer
    return t

def answers(path, kind):
    t = text_of(path)
    parts = re.split(r'RESPONSE TO %s NO\. ([0-9.]+):' % KINDS[kind], t)
    out = {}
    for n, body in zip(parts[1::2], parts[2::2]):
        out.setdefault(n, re.sub(r'\s+', ' ', body).strip())
    return out

def classify(mine, theirs):
    """noise = pleading-line artefacts; cosmetic = identical once house style is
    normalised away; everything else is substantive and needs a human reason."""
    if NOISE.match(mine) and NOISE.match(theirs):
        return "noise"
    if norm(mine) == norm(theirs):
        return "cosmetic"
    return "substantive"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mine", required=True)
    ap.add_argument("--theirs", required=True)
    ap.add_argument("--kind", required=True, choices=KINDS)
    a = ap.parse_args()

    A, B = answers(a.mine, a.kind), answers(a.theirs, a.kind)
    keys = sorted(set(A) | set(B), key=lambda s: [int(x) for x in s.split('.')])

    subs, cos, noise, gone = [], [], [], []
    for k in keys:
        if k not in A: gone.append(f"{k}: ADDED by attorney"); continue
        if k not in B: gone.append(f"{k}: REMOVED by attorney"); continue
        if A[k] == B[k]: continue
        sm = difflib.SequenceMatcher(None, A[k].split(), B[k].split())
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal": continue
            m = " ".join(A[k].split()[i1:i2]); t = " ".join(B[k].split()[j1:j2])
            c = classify(m, t)
            {"cosmetic": cos, "substantive": subs, "noise": noise}[c].append((k, m, t))

    print(f"# {a.kind}: {len(A)} ours / {len(B)} theirs")
    if gone:
        print("\n## structural"); [print("  ", g) for g in gone]
    print(f"\n## SUBSTANTIVE ({len(subs)}) — read the covering email for the reason, "
          "then decide: LAW / PROCEDURE / CASE-SPECIFIC")
    for k, m, t in subs:
        print(f"\n  [{k}]")
        print(f"    ours  : {m[:260] or '(nothing)'}")
        print(f"    theirs: {t[:260] or '(deleted)'}")
    print(f"\n## cosmetic ({len(cos)}) — fold into preflight as WARN, do not write prose rules")
    seen = set()
    for k, m, t in cos:
        key = (m[:40], t[:40])
        if key in seen: continue
        seen.add(key); print(f"    {k}: {m[:60]!r} -> {t[:60]!r}")
    print(f"\n(suppressed {len(noise)} line-number artefacts)")

if __name__ == "__main__":
    main()
