#!/usr/bin/env python3
"""Fill the Notice of Posting of Jury Fees template.

Usage: fill_jury_fee.py <template.docx> <output.docx> <fields.json>

fields.json: {"plaintiff": "...", "defendant": "...", "case_no": "...",
              "does_count": "50", "date": "August 21, 2026"}

Everything is done at the XML level, because the live Drive template's run
structure varies (Klaus edits it in the browser) and python-docx paragraph-level
edits either collapse runs or silently miss content inside table cells.

Three things this handles that a naive fill does not:

1. TOP ATTORNEY BLOCK LINE BREAK. Hernán's format rule (2026-07-29) puts the
   plaintiff's name on its OWN line directly beneath "Attorney for Plaintiff",
   in both the top attorney block and the signature block. The signature block
   carries its own break, but the top block in the current template is a single
   run — "Attorney for Plaintiff [PLAINTIFF NAME]" — so we re-insert a <w:br/>.

2. THE DATE IS A LIVE WORD FIELD. The template's "Dated:" line is a *complex*
   field (fldChar begin / instrText DATE / separate / cached value / end) sitting
   inside a table cell. It is NOT a fldSimple, so the old fldSimple-removal code
   never fired. Left alone, the date re-evaluates to whatever day the document is
   opened or printed — meaning a notice signed in November silently shows
   November. We replace the whole field with static text.

3. DOES COUNT GUARD. "1 through 50" is both the template default and a perfectly
   valid real value (Mudong Huang = 50). The guard only complains when the count
   we asked for is not what ended up in the document.
"""
import sys, json, re, zipfile, os


def main():
    if len(sys.argv) != 4:
        sys.exit("usage: fill_jury_fee.py <template.docx> <output.docx> <fields.json>")
    tpl, out, fields_path = sys.argv[1], sys.argv[2], sys.argv[3]
    f = json.load(open(fields_path))
    does = str(f.get('does_count', '50'))

    with zipfile.ZipFile(tpl) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    x = data['word/document.xml'].decode('utf-8')

    # 1. restore the name-below break in the top attorney block
    x = x.replace(
        '<w:t>Attorney for Plaintiff [PLAINTIFF NAME]</w:t>',
        '<w:t>Attorney for Plaintiff</w:t><w:br/>'
        '<w:t xml:space="preserve">[PLAINTIFF NAME]</w:t>')

    # 2. kill the live DATE field, substitute static text
    date_str = f.get('date')
    if date_str:
        static = ('<w:r><w:rPr><w:rFonts w:eastAsia="Times New Roman"/></w:rPr>'
                  '<w:t xml:space="preserve">%s</w:t></w:r>' % date_str)
        x, n = re.subn(
            r'<w:r[^>]*><w:fldChar w:fldCharType="begin"/></w:r>'
            r'.*?<w:fldChar w:fldCharType="end"/></w:r>',
            static, x, flags=re.S)
        if n == 0:
            # older template shape: a fldSimple wrapper
            x, n = re.subn(r'<w:fldSimple[^>]*>.*?</w:fldSimple>', static, x, flags=re.S)
        if n == 0:
            sys.exit('ERROR: could not find the DATE field to replace — inspect the template')

    # 3. tokens
    for k, v in {'[PLAINTIFF NAME]': f['plaintiff'],
                 '[DEFENDANT NAME]': f['defendant'],
                 '[CASE NO.]': f['case_no'],
                 '1 through 50': '1 through %s' % does}.items():
        x = x.replace(k, v)

    data['word/document.xml'] = x.encode('utf-8')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for n_ in names:
            z.writestr(n_, data[n_])

    # guards
    with zipfile.ZipFile(out) as z:
        body = re.sub(r'<[^>]+>', '', z.read('word/document.xml').decode('utf-8'))
    problems = []
    left = re.findall(r'\[[A-Z .]+\]', body)
    if left:
        problems.append('unfilled tokens %s' % left)
    if 'DOES 1 through %s' % does not in body:
        problems.append('DOES count did not take (wanted %s)' % does)
    if f['case_no'] not in body:
        problems.append('case number missing')
    if date_str and (date_str not in body or 'DATE \\@' in body):
        problems.append('date did not take / live DATE field survived')
    if problems:
        sys.exit('ERROR: ' + '; '.join(problems))
    print('OK ->', out)


if __name__ == '__main__':
    main()
