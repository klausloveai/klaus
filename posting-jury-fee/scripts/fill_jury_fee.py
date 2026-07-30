#!/usr/bin/env python3
"""Fill the Notice of Posting of Jury Fees template.

Usage: fill_jury_fee.py <template.docx> <output.docx> <fields.json>

fields.json: {"plaintiff": "...", "defendant": "...", "case_no": "...",
              "does_count": "25", "date": "July 29, 2026"}

Fills tokens at the XML level so the "Attorney for Plaintiff" <w:br/> line break
(plaintiff name on its own line beneath) survives — a python-docx paragraph-level
replace would collapse the runs and destroy it. Then sets a static Dated line
(removing the Word DATE field) via python-docx. Aborts if any [TOKEN] is left.
"""
import sys, json, re, zipfile, os


def main():
    if len(sys.argv) != 4:
        sys.exit("usage: fill_jury_fee.py <template.docx> <output.docx> <fields.json>")
    tpl, out, fields_path = sys.argv[1], sys.argv[2], sys.argv[3]
    f = json.load(open(fields_path))

    # --- XML-level token fill (preserves <w:br/> in the attorney/signature blocks) ---
    with zipfile.ZipFile(tpl) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    x = data['word/document.xml'].decode('utf-8')
    repl = {
        '[PLAINTIFF NAME]': f['plaintiff'],
        '[DEFENDANT NAME]': f['defendant'],
        '[CASE NO.]': f['case_no'],
        '1 through 50': '1 through %s' % str(f.get('does_count', '50')),
    }
    for k, v in repl.items():
        x = x.replace(k, v)
    data['word/document.xml'] = x.encode('utf-8')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(n, data[n])

    # --- static date (remove the Word DATE field) ---
    date_str = f.get('date')
    if date_str:
        from docx import Document
        from docx.oxml.ns import qn
        d = Document(out)
        for p in d.paragraphs:
            if 'Dated' in ''.join(r.text for r in p.runs):
                for el in list(p._p):
                    if el.tag == qn('w:fldSimple'):
                        p._p.remove(el)
                if p.runs:
                    p.runs[0].text = 'Dated:   ' + date_str
                    for r in p.runs[1:]:
                        r._r.getparent().remove(r._r)
                break
        d.save(out)

    # --- guard: no leftover tokens ---
    with zipfile.ZipFile(out) as z:
        body = re.sub(r'<[^>]+>', '', z.read('word/document.xml').decode('utf-8'))
    left = re.findall(r'\[[A-Z .]+\]|1 through 50', body)
    if left:
        sys.exit('ERROR: unfilled tokens remain: %s' % left)
    print('OK ->', out)


if __name__ == '__main__':
    main()
