#!/usr/bin/env python3
"""Propose a case label for every fetched thread that has none yet.

Order of evidence, strongest first:
  1. references/aliases.json  (claim #, order names, reversed names ...)
  2. client names taken from the label names themselves (word-boundary match)
  3. --history: pull reference numbers out of the mail (claim #, report #,
     order #) and see which case label earlier mail with that number carries

Never guesses: a thread with no evidence, or evidence pointing at two
different clients, lands in "unresolved" with the reason.

  match.py --in inbox.json --out plan.json [--no-history]
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
import gmail  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALIASES = os.path.join(HERE, "references", "aliases.json")

# Words in label paths that are containers, firm names or people on every
# email signature -- never client names.
STOP = {"shenqi cai", "lingtu law", "case referral", "pi auto", "hernan cases",
        "hernan & joe cases", "lingtu cases", "firm billing", "962 house",
        "hernán simó", "hernan simo", "klaus liu", "joe wu", "cassie cai"}
PARK = "待归档"  # "please tell me which case" -- not a case label
LIT_WORDS = re.compile(r"complaint|discovery|interrogator|request for production|CMC|"
                       r"case management|court|e-?fil|summons|served|service of process|"
                       r"deposition|motion|hearing|case no", re.I)
# Signature / disclaimer boilerplate: cut before pulling reference numbers.
# (Hernán's footer cites "18 U.S.C. §§ 2510-2523", which once matched a case.)
BOILER = re.compile(r"CONFIDENTIALITY NOTICE|Please be advised that I do not accept|"
                    r"NOTICE REGARDING SERVICE|Sincerely,|Best regards,|Thank you,\s*$", re.I)
NOT_REF = re.compile(r"\d{1,5}|\d{3}-\d{3}-\d{4}|\d{5}(-\d{4})?|\d{4}-\d{4}|"
                     r"\(?\d{3}\)?-?\d{3}-?\d{4}")
MIN_HISTORY_HITS = 2
REF_TOKEN = re.compile(r"(?<![\w-])(?=[\w-]*\d)[A-Z0-9][A-Z0-9-]{5,}(?![\w-])", re.I)


def clean_part(p):
    p = re.sub(r"^[^\w]+", "", p.strip())                        # leading emoji
    p = re.sub(r"^(DB|CL|CV|LB|PI|WC|WC&EL|FL|Auto|PI\(AZ\))-", "", p)
    p = re.sub(r"-\d{6}$", "", p)                                  # -MMDDYY
    p = re.sub(r"-\d{2}[A-Z]{2,}\d+$", "", p)                      # -26NNCV05107
    p = re.sub(r"\(\d+/\d+\)$", "", p).strip()
    p = re.sub(r"\s+v\.?\s+.*$", "", p, flags=re.I).strip()       # caption -> plaintiff
    p = re.sub(r"\s*-\s*PI$|\d+$", "", p).strip()
    return p


def name_index(labels):
    """[(name, label_id)] longest first; one label can own several names."""
    idx = set()
    for lid, full in labels.items():
        if full == PARK:
            continue
        for part in full.split("/"):
            for piece in re.split(r"\s*&\s*|\s+/\s+", part):
                n = clean_part(piece)
                if not n or n.lower() in STOP:
                    continue
                if len([t for t in n.split() if len(t) >= 2]) < 2:
                    continue
                idx.add((n, lid))
    return sorted(idx, key=lambda x: -len(x[0]))


def leafmost(lids, labels):
    """Drop a label when one of its own sub-labels also matched."""
    return {l for l in lids
            if not any(labels[o].startswith(labels[l] + "/") for o in lids if o != l)}


def is_lit(name):
    return name.startswith(("⚖️", "👥"))


def decide(lids, text, labels):
    """Return (label_id, None) or (None, reason)."""
    lids = leafmost(set(lids), labels)
    if len(lids) == 1:
        return next(iter(lids)), None
    if len(lids) >= 3:
        return None, "多案汇总邮件（命中 %d 个案子），不挂单案 label" % len(lids)
    a, b = sorted(lids, key=lambda l: labels[l])
    # Same client with a pre-lit and a litigation label: pick by content.
    if is_lit(labels[a]) != is_lit(labels[b]):
        lit = a if is_lit(labels[a]) else b
        pre = b if lit == a else a
        return (lit, None) if LIT_WORDS.search(text) else (pre, None)
    return None, "命中两个案子：%s / %s" % (labels[a], labels[b])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-history", action="store_true")
    a = ap.parse_args()

    data = json.load(open(a.inp))
    labels = gmail.labels()  # fresh: Klaus renames labels by hand
    park_id = next((i for i, n in labels.items() if n == PARK), None)
    idx = name_index(labels)
    aliases = json.load(open(ALIASES)) if os.path.exists(ALIASES) else []

    todo = [t for t in data["threads"] if "error" not in t
            and not [l for l in t["label_ids"] if l in labels and l != park_id]]
    proposals, unresolved = [], []

    def history(tokens):
        votes = Counter()
        for tok in tokens[:4]:
            for mid in gmail.search_messages(f'"{tok}" -in:inbox', cap=8):
                m = gmail.get_message(mid, fmt="minimal")
                for l in m.get("labelIds", []):
                    if l in labels and l != park_id:
                        votes[(tok, l)] += 1
        return votes

    for t in todo:
        text = t["match_text"]
        low = text.lower()
        hits, why = set(), []
        for al in aliases:
            if al["label_id"] in labels and re.search(al["pattern"], text, re.I):
                hits.add(al["label_id"])
                why.append("别名表:" + al.get("note", al["pattern"]))
        if not hits:
            found = [(n, lid) for n, lid in idx
                     if re.search(r"(?<![a-z])" + re.escape(n.lower()) + r"(?![a-z])", low)]
            # a short name inside a longer matched name is not a second client
            found = [(n, lid) for n, lid in found
                     if not any(n.lower() in m.lower() and n != m for m, _ in found)]
            for n, lid in found:
                hits.add(lid)
                why.append("客户名:" + n)
        lid, reason = decide(hits, text, labels) if hits else (None, None)
        if not lid and len(hits) >= 2:
            # The subject names exactly one of them -> that is the thread's case.
            subj = t["subject"].lower()
            in_subj = leafmost({l for n, l in idx if l in hits and re.search(
                r"(?<![a-z])" + re.escape(n.lower()) + r"(?![a-z])", subj)}, labels)
            if len(in_subj) == 1:
                lid, reason = next(iter(in_subj)), None
                why.append("主题只点了这一个案子")
        if lid:
            proposals.append({"no": t["no"], "tid": t["tid"], "subject": t["subject"],
                              "label_id": lid, "label": labels[lid], "why": "；".join(why)})
            continue
        body = BOILER.split(t["last_text"])[0]
        tokens = sorted(set(REF_TOKEN.findall(t["subject"] + " " + body)), key=len, reverse=True)
        tokens = [x for x in tokens if not NOT_REF.fullmatch(x)]
        if reason is None and tokens and not a.no_history:
            votes = history(tokens)
            per_case = Counter()
            for (_, l), n in votes.items():
                per_case[l] += n
            cases = leafmost({l for l, n in per_case.items() if n >= MIN_HISTORY_HITS}, labels)
            if len(cases) == 1:
                l = next(iter(cases))
                tok = next(tk for (tk, ll) in votes if ll == l)
                proposals.append({"no": t["no"], "tid": t["tid"], "subject": t["subject"],
                                  "label_id": l, "label": labels[l],
                                  "why": f"历史邮件:「{tok}」以前出现在这个案子里"})
                continue
            if len(cases) > 1:
                reason = "编号在多个案子里出现过：" + " / ".join(labels[c] for c in cases)
        unresolved.append({"no": t["no"], "tid": t["tid"], "subject": t["subject"],
                           "from": t["last_from"], "ref_tokens": tokens[:5],
                           "why": reason or ("有编号但历史里查不到" if tokens else "没有客户名也没有编号")})

    plan = {"park_label_id": park_id, "label": proposals, "unresolved": unresolved,
            "already_labelled": len(data["threads"]) - len(todo)}
    json.dump(plan, open(a.out, "w"), ensure_ascii=False, indent=1)

    print(f"已有 case label：{plan['already_labelled']}   建议打 label：{len(proposals)}   归不了：{len(unresolved)}\n")
    for p in proposals:
        print(f"{p['no']:>3}  → {p['label']}\n       {p['subject'][:70]}\n       依据：{p['why']}")
    if unresolved:
        print("\n— 归不了 —")
        for u in unresolved:
            print(f"{u['no']:>3}  {u['subject'][:70]}\n       {u['why']}  {u['ref_tokens'] or ''}")



if __name__ == "__main__":
    main()
