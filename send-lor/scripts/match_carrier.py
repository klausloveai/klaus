#!/usr/bin/env python3
"""Match an insurer name (from the intake sheet) to the firm's "insurance list"
carrier directory and return the LOR fax number + claims email.

Usage:
    match_carrier.py "<insurer name>" <insurance_list_values.json>

`insurance_list_values.json` = the `gws sheets ... values get` JSON for
`insurance list!A1:Z200` (a {"values":[[...]]} object). The leading
`Using keyring backend` banner is fine — we slice from the first '{'.

Columns are read by header name: "Insurance Name", "LOR Fax Number", "Email".

Prints JSON: {"matched": <dir name|null>, "fax": <E.164|null>, "email": <str|null>}
Fax is normalized to +1XXXXXXXXXX when it has 10/11 digits.
"""
import sys, json, re

STOP = {"insurance","company","indemnity","group","co","the","of","llc","inc",
 "mutual","casualty","general","assurance","national","protection","automobile",
 "auto","northbrook","fire","american","america","corporation","corp","ins",
 "underwriters","services","exchange","county","and"}

def toks(s):
    s = re.sub(r"\(.*?\)", "", s or "")          # drop "(NAIC ...)"
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return {t for t in s.split() if len(t) >= 3 and t not in STOP}

def e164(fax):
    d = re.sub(r"\D", "", fax or "")
    if len(d) == 10: return "+1" + d
    if len(d) == 11 and d[0] == "1": return "+" + d
    return (fax or None)

def main():
    name = sys.argv[1]
    raw = open(sys.argv[2], encoding="utf-8").read()
    raw = raw[raw.index("{"):]
    rows = json.loads(raw).get("values", [])
    out = {"matched": None, "fax": None, "email": None}
    if not rows:
        print(json.dumps(out)); return
    hdr = [h.strip().lower() for h in rows[0]]
    def col(key):
        for i, h in enumerate(hdr):
            if key in h: return i
        return None
    ci_name, ci_fax, ci_email = col("insurance name"), col("lor fax"), col("email")
    want = toks(name)
    best, best_score = None, 0
    for r in rows[1:]:
        if ci_name is None or len(r) <= ci_name: continue
        score = len(want & toks(r[ci_name]))
        if score > best_score:
            best, best_score = r, score
    if best:
        fax = best[ci_fax] if ci_fax is not None and len(best) > ci_fax else None
        email = best[ci_email] if ci_email is not None and len(best) > ci_email else None
        email = email.strip() if email else None
        out = {"matched": best[ci_name], "fax": e164(fax), "email": (email or None)}
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
