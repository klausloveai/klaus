#!/usr/bin/env python3
"""Fill an LOR .docx template by direct XML replacement (no dependencies).

Replaces [Bracketed] placeholder tokens with provided values and removes the
yellow placeholder highlight so the finished letter looks clean. Preserves the
letterhead, logo, fonts, and all other formatting exactly.

Usage:
    python3 fill_lor.py <template.docx> <out.docx> <fields.json>

fields.json is a flat object mapping the EXACT token (including brackets) to its
value, e.g. {"[Client Name(s)]": "Jane Doe", "[Date of Loss]": "March 1, 2026"}

Any tokens not present in the chosen template are simply ignored. After filling,
the script verifies no "[...]" placeholder tokens remain and exits non-zero if
any are left unfilled (so the skill never sends a half-filled letter).
"""
import sys, json, re, html, zipfile, datetime


def stamp_today(xml):
    """Set the letter's Word DATE field to today (the conversion to PDF keeps the
    field's last-cached value otherwise, so the letter would show a stale date)."""
    today = datetime.date.today().strftime("%B %-d, %Y")
    pat = re.compile(
        r'(<w:instrText[^>]*>\s*DATE[^<]*</w:instrText>.*?'
        r'<w:fldChar[^>]*w:fldCharType="separate"[^>]*/>)(.*?)'
        r'(<w:fldChar[^>]*w:fldCharType="end"[^>]*/>)', re.S)
    def repl(m):
        mid = re.sub(r'(<w:t[^>]*>)[^<]*(</w:t>)',
                     lambda t: t.group(1) + html.escape(today) + t.group(2),
                     m.group(2), count=1)
        return m.group(1) + mid + m.group(3)
    return pat.sub(repl, xml, count=1)

def main():
    if len(sys.argv) != 4:
        sys.exit("usage: fill_lor.py <template.docx> <out.docx> <fields.json>")
    src, out, fields_path = sys.argv[1], sys.argv[2], sys.argv[3]
    fields = json.load(open(fields_path, encoding="utf-8"))

    zin = zipfile.ZipFile(src)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                x = data.decode("utf-8")
                for token, value in fields.items():
                    x = x.replace(token, html.escape(str(value)))
                # Strip the yellow highlight used to mark placeholders.
                x = re.sub(r'<w:highlight w:val="yellow"\s*/>', "", x)
                # Stamp the letter date to today (PDF conversion keeps stale cache).
                x = stamp_today(x)
                data = x.encode("utf-8")
            zout.writestr(item, data)

    # Verify nothing was left unfilled. Read back the visible text only.
    body = zipfile.ZipFile(out).read("word/document.xml").decode("utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", "", body))
    leftover = sorted(set(re.findall(r"\[[^\[\]\n]{1,40}\]", text)))
    if leftover:
        sys.exit("ERROR: unfilled placeholders remain: " + ", ".join(leftover))
    print("OK: filled ->", out)

if __name__ == "__main__":
    main()
