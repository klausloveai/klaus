#!/usr/bin/env python3
"""Audit exhibit PDFs for source-URL footers and AI-tool markers.

    python audit_footers.py <EXHIBITS_ROOT>

Classifies each PDF as a web capture (with or without a footer) or a non-web document, and
flags any captured URL carrying an AI-tool referrer. Judgement notes are in
references/preflight.md - a downloaded report legitimately has no footer.
"""
import sys, os, re, glob, urllib.parse

STAMP = re.compile(r'\d{1,2}/\d{1,2}/\d{2},?\s*\d{1,2}:\d{2}\s*[AP]M')
URL   = re.compile(r'https?://[^\s)\]"]{10,}')
AI    = re.compile(r'(?:utm_)?source=(?:chatgpt|openai|perplexity|copilot|claude|gemini)'
                   r'|utm_source=chatgpt\.com|ref=(?:claude|chatgpt)|[?&]oai_', re.I)

def main(root):
    try:
        import fitz
    except ImportError:
        sys.exit("needs PyMuPDF:  pip install pymupdf")
    web_ok, web_no, other, ai_hits = [], [], [], []
    for p in sorted(glob.glob(os.path.join(root, "**", "*.pdf"), recursive=True)):
        try:
            d = fitz.open(p)
        except Exception:
            continue
        text = "".join(pg.get_text() for pg in d)
        w, h = round(d[0].rect.width), round(d[0].rect.height)
        links = sum(len(d[i].get_links()) for i in range(d.page_count))
        d.close()
        stamp = bool(STAMP.search(text))
        found = URL.search(text)
        footer = stamp and bool(found)
        # a browser print is Letter-sized and carries many outbound links
        webish = footer or (w == 612 and links >= 8)
        rel = os.path.relpath(p, root)
        row = (rel, w, h, links, found.group(0)[:90] if found else "")
        (web_ok if footer else web_no if webish else other).append(row)
        seen_u=set()
        for u in URL.findall(text):
            if AI.search(urllib.parse.unquote(u)) and u not in seen_u:
                seen_u.add(u); ai_hits.append((rel, u[:130]))

    print(f"web captures WITH footer   : {len(web_ok)}")
    print(f"web captures WITHOUT footer: {len(web_no)}")
    print(f"non-web documents          : {len(other)}   (letters, agreements, report PDFs)")

    if web_no:
        print("\n=== MISSING FOOTER - recover the URL and re-capture ===")
        for rel, w, h, links, _ in web_no:
            print(f"  {w}x{h} links={links:3}  {rel}")
    if ai_hits:
        print("\n=== AI-TOOL MARKER IN A CAPTURED URL - must be re-captured clean ===")
        for rel, u in ai_hits:
            print(f"  {rel}\n      {u}")
    else:
        print("\nno AI-tool markers found in any captured URL")
    return 1 if (web_no or ai_hits) else 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
