#!/usr/bin/env python3
"""preflight.py — gate a discovery response package before the attorney sees it.

Every check here exists because the mistake was actually made once. See
references/hernan-standard.md. Exit code 1 if anything fails.

usage:  python3 preflight.py <responses.docx> [more.docx ...] [--production <pdf>]
"""
import sys, re, os, subprocess

CJK   = re.compile(r'[　-〿㐀-鿿＀-￯]')
NUMDATE = re.compile(r'\b\d{2}/\d{2}/(?:\d{2}|\d{4})\b')
ABBREV = re.compile(r'\b(Blvd|Ste|Pkwy|Ave|St|Dr|Rd)\b\.?(?=[ ,])|,\s(CA)\s\d{5}')
BAD_CITES = {
    "Catholic Mut": "reinsurance case — does not support health-insurance discovery",
    "30801": "Food & Agric. 30801 authorizes county ordinances; it binds no owner",
    "not waived by": "Webb/Schnabel do not say the taxpayer privilege is unwaivable",
}
WITHHOLD = "No responsive document is being withheld"

def paras(path):
    from docx import Document
    from docx.enum.text import WD_COLOR_INDEX
    d = Document(path)
    out = []
    for p in d.paragraphs:
        hl = any(r.font.highlight_color == WD_COLOR_INDEX.YELLOW
                 for r in p.runs if r.text.strip())
        out.append((p.text, hl))
    return out

def check(path):
    fails, warns = [], []
    ps = paras(path)
    text = "\n".join(t for t, _ in ps)

    for t, hl in ps:
        if CJK.search(t):
            fails.append(f"Chinese characters in a served document: {t.strip()[:70]}")
        if hl:
            tag = "REMOVE BEFORE SERVICE" in t
            (warns if tag else fails).append(
                ("attorney-decision flag still present (clear before service): "
                 if tag else "unexplained highlight: ") + t.strip()[:70])

    for m in NUMDATE.finditer(text):
        warns.append(f"numeric date {m.group(0)} — house style writes dates out")
    for m in ABBREV.finditer(text):
        warns.append(f"abbreviated address {m.group(0)!r} — spell it out")
    for frag, why in BAD_CITES.items():
        if frag in text:
            fails.append(f"suspect authority {frag!r}: {why}")
    if ", Esq." in text.split("VERIFICATION")[0][-600:]:
        warns.append("signature block carries ', Esq.' — house style omits it")

    # objection + full production must carry the withholding sentence
    blocks = re.split(r'RESPONSE TO [A-Z ]+NO\. [0-9.]+:', text)
    for b in blocks[1:]:
        if "objects to this" in b and "will comply with this request in whole" in b \
           and WITHHOLD not in b:
            fails.append("objection + full production without the "
                         f"'{WITHHOLD}...' sentence: {b.strip()[:60]}")

    # verification must not claim he read English if 2.9/2.10 say otherwise
    if re.search(r'NO\. 2\.(9|10):\s*No\.', text) or "does not read English" in text:
        v = text.split("VERIFICATION")[-1]
        if "I have read the foregoing" in v and "translated" not in v:
            fails.append("verification says the client READ the responses, but 2.9/2.10 "
                         "say he does not read English — must say translated, and add a "
                         "Declaration of Translator")
        if "DECLARATION OF TRANSLATOR" not in v.upper():
            fails.append("Declaration of Translator missing from the verification page")
    return fails, warns

def bates_check(docs, production):
    """Every CONG cite in the responses must fall inside the production."""
    pages = int(subprocess.run(["pdfinfo", production], capture_output=True, text=True)
                .stdout.split("Pages:")[1].split()[0])
    cited = set()
    for d in docs:
        for t, _ in paras(d):
            cited.update(int(n) for n in re.findall(r'CONG 0*(\d+)', t))
    over = sorted(n for n in cited if n > pages)
    return pages, (["Bates cited beyond the production (%d pages): %s"
                    % (pages, ", ".join("CONG %06d" % n for n in over))] if over else [])

def main():
    args = sys.argv[1:]
    production = None
    if "--production" in args:
        i = args.index("--production"); production = args[i+1]; args = args[:i] + args[i+2:]
    if not args:
        print(__doc__); sys.exit(2)

    all_fail, all_warn = [], []
    for p in args:
        f, w = check(p)
        label = os.path.basename(p)
        all_fail += [f"[{label}] {x}" for x in f]
        all_warn += [f"[{label}] {x}" for x in w]
    if production:
        pages, f = bates_check(args, production)
        print(f"production: {pages} pages")
        all_fail += f

    for x in dict.fromkeys(all_warn): print("  WARN ", x)
    for x in dict.fromkeys(all_fail): print("  FAIL ", x)
    print(f"\n{len(set(all_fail))} failure(s), {len(set(all_warn))} warning(s)")
    sys.exit(1 if all_fail else 0)

if __name__ == "__main__":
    main()
