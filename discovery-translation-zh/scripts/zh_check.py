#!/usr/bin/env python3
"""zh_check.py — gate a Chinese client-verification translation.

    python3 zh_check.py --zh 中文译本.pdf --en 英文定稿.pdf \
        --kind FROG --names "YI CONG" "RHEA EDPAO" "KK NOW LA LLC"

Checks the things that make a translation useless or unsafe: a missing answer,
a name that got translated, a missing verification or translator declaration,
and glyphs that did not draw. Exit 1 on any failure.
"""
import argparse, re, subprocess, sys

KINDS = {"FROG": ("对表格式质询第", r"RESPONSE TO FORM INTERROGATORY NO\."),
         "SROG": ("对特别质询第",   r"RESPONSE TO SPECIAL INTERROGATORY NO\."),
         "RFP":  ("对文件出示请求第", r"RESPONSE TO REQUEST FOR PRODUCTION NO\."),
         "RFA":  ("对自认请求第",   r"RESPONSE TO REQUEST FOR ADMISSION NO\."),
         "INDEX": (None, None)}

def txt(p):
    return subprocess.run(["pdftotext", "-layout", p, "-"],
                          capture_output=True, text=True).stdout

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zh", required=True)
    ap.add_argument("--en", required=True)
    ap.add_argument("--kind", required=True, choices=KINDS)
    ap.add_argument("--names", nargs="*", default=[])
    ap.add_argument("--no-verification", action="store_true",
                    help="index and similar documents carry no verification page")
    a = ap.parse_args()

    z, e = txt(a.zh), txt(a.en)
    # pdftotext breaks Chinese mid-phrase; collapse whitespace before substring tests
    # ...and the pleading line numbers land inside the sentences, so drop digits too
    zc = re.sub(r"[\s\d]+", "", z)
    fails, warns = [], []

    zh_pat, en_pat = KINDS[a.kind]
    if zh_pat:
        nz, ne = z.count(zh_pat), len(re.findall(en_pat, e))
        print(f"answers: Chinese {nz} / English {ne}")
        if nz != ne:
            fails.append(f"answer count mismatch — Chinese {nz}, English {ne}. "
                         "Every numbered answer must be present and numbered identically.")

    for n in a.names:
        if n not in z:
            fails.append(f"name {n!r} does not appear in the Chinese — it must stay in "
                         "English so the client can match it to the English original")

    if "□" in z or "�" in z:
        fails.append("undrawn glyphs in the rendered PDF — check the eastAsia font")

    if not a.no_verification:
        if "宣誓认证" not in zc:
            fails.append("verification section missing")
        if "口译人声明" not in zc:
            fails.append("Declaration of Translator missing")
        if "已由英文口译为普通话" not in zc and "翻译" not in zc:
            fails.append("verification does not state the responses were translated to the client")

    if "致客户" not in zc:
        fails.append("client notice missing — the client must be told this is a "
                     "translation for checking and that opposing counsel gets the English")

    # Bates and citations should survive untranslated
    for pat, why in [(r'CONG\s?\d{6}', "Bates numbers"), (r'\d+\s+Cal\.\d', "case citations")]:
        if re.search(pat, e) and not re.search(pat, z):
            warns.append(f"{why} present in the English but not in the Chinese")

    for w in warns: print("  WARN ", w)
    for f in fails: print("  FAIL ", f)
    print(f"\n{len(fails)} failure(s), {len(warns)} warning(s)")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
