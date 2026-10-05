#!/usr/bin/env python3
"""
docx letter toolkit for case-substituted-out.

The firm's letter templates are .docx with a first-page letterhead header, a signature
image, and yellow-highlighted fill slots. This module edits word/document.xml directly:
python-docx is NOT used because it drops the header drawings. Same reason we never
round-trip these through openpyxl-style libraries. See [[gws_drive_binary_update]].

Hard rules encoded here:
  * only a YELLOW run is a fill slot -- a same-named plain run is the LABEL
  * filling a value strips its highlight; unknown values keep it so Klaus sees them
  * the date paragraph gets centered
  * word/header*.xml is NEVER touched, and w:top is never reduced below 1440

Usage as a library:

    from fill_letter import Letter
    L = Letter('tpl_3P.docx')
    L.fill('Carrier Name', 'Farmers Insurance')
    L.fill('Claim Number', '5044424448-1')
    L.fill('info@newfirm.com', '[CONFIRM EMAIL]', unknown=True)   # stays yellow
    L.center_date('October 6, 2026')
    L.save('out.docx'); L.render_pdf('out.docx')
"""
from __future__ import annotations

import io
import os
import re
import subprocess
import zipfile
from collections import defaultdict

PARA = re.compile(r'<w:p\b[^>]*>.*?</w:p>', re.S)
RUN = re.compile(r'<w:r\b[^>]*>.*?</w:r>', re.S)
TXT = re.compile(r'(<w:t[^>]*>)(.*?)(</w:t>)', re.S)
HL = re.compile(r'<w:highlight w:val="yellow"/>')

SOFFICE = '/Applications/LibreOffice.app/Contents/MacOS/soffice'


def _esc(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;')


def _ptext(p: str) -> str:
    return ''.join(t for _, t, _ in TXT.findall(p))


class Letter:
    def __init__(self, src: str):
        self.src = src
        self.xml = zipfile.ZipFile(src).read('word/document.xml').decode('utf8')
        self._queue: dict[str, list] = defaultdict(list)

    # ---------- filling ----------

    def fill(self, placeholder: str, value: str, unknown: bool = False) -> 'Letter':
        """Queue one fill. Repeat the same placeholder to fill successive slots in
        document order (e.g. two `Claim Number` slots -> 1P then 3P)."""
        self._queue[placeholder].append((value, unknown))
        return self

    def apply(self) -> 'Letter':
        q = self._queue

        def sub(m):
            run = m.group(0)
            tm = TXT.search(run)
            if not tm:
                return run
            text = tm.group(2).strip()
            if not HL.search(run):
                return run  # plain run == label, never a fill slot
            for ph in list(q):
                if text == ph and q[ph]:
                    value, unknown = q[ph].pop(0)
                    new = run[:tm.start(2)] + _esc(value) + run[tm.end(2):]
                    return new if unknown else HL.sub('', new)
            return run

        self.xml = RUN.sub(sub, self.xml)
        left = {k: [v[0] for v in vs] for k, vs in q.items() if vs}
        if left:
            raise AssertionError(f'unconsumed fills (placeholder not found or not yellow): {left}')
        self._queue = defaultdict(list)
        return self

    def set_run(self, old_text: str, new_text: str) -> 'Letter':
        """Replace EVERY run whose text == old_text (labels included). Used for header
        lines like 'Attn: ...' that are not highlighted slots."""
        hits = [0]

        def sub(m):
            run = m.group(0)
            tm = TXT.search(run)
            if not tm or tm.group(2).strip() != old_text:
                return run
            hits[0] += 1
            new = run[:tm.start(2)] + _esc(new_text) + run[tm.end(2):]
            return HL.sub('', new)

        self.xml = RUN.sub(sub, self.xml)
        assert hits[0], f'set_run: not found {old_text!r}'
        return self

    # ---------- paragraph surgery ----------

    def set_para(self, marker: str, text: str) -> 'Letter':
        """Collapse the paragraph containing `marker` into a single run of `text`,
        keeping the first run's formatting. Use to merge body paragraphs."""
        hits = [0]

        def sub(m):
            p = m.group(0)
            if marker not in _ptext(p):
                return p
            runs = RUN.findall(p)
            if not runs:
                return p
            base = runs[0]
            tm = TXT.search(base)
            if not tm:
                return p
            new = base[:tm.start(2)] + _esc(text) + base[tm.end(2):]
            new = HL.sub('', new)
            hits[0] += 1
            return p[:p.index(runs[0])] + new + p[p.rindex(runs[-1]) + len(runs[-1]):]

        self.xml = PARA.sub(sub, self.xml)
        assert hits[0], f'set_para: not found {marker!r}'
        return self

    def drop_para(self, marker: str) -> 'Letter':
        """Delete every paragraph containing `marker` (e.g. the 1P row when there is
        no 1P claim, or the optional misrouting sentence)."""
        n = [0]

        def sub(m):
            if marker in _ptext(m.group(0)):
                n[0] += 1
                return ''
            return m.group(0)

        self.xml = PARA.sub(sub, self.xml)
        assert n[0], f'drop_para: not found {marker!r}'
        return self

    def drop_blank(self, marker: str, where: str = 'before', count: int = 1) -> 'Letter':
        """Remove blank paragraphs adjacent to the paragraph containing `marker`.
        Page-shrink lever #4. Never remove the blank that holds the signature image."""
        spans = [m.span() for m in PARA.finditer(self.xml)]
        texts = [_ptext(self.xml[a:b]).strip() for a, b in spans]
        i = next((k for k, t in enumerate(texts) if marker in t), None)
        assert i is not None, f'drop_blank: anchor not found {marker!r}'
        cuts, removed = [], 0
        rng = range(i - 1, -1, -1) if where == 'before' else range(i + 1, len(texts))
        for k in rng:
            if texts[k] == '' and removed < count:
                cuts.append(spans[k]); removed += 1
            elif texts[k] != '':
                break
        assert removed, f'drop_blank: no blank {where} {marker!r}'
        for a, b in sorted(cuts, reverse=True):
            self.xml = self.xml[:a] + self.xml[b:]
        return self

    # ---------- layout ----------

    def center_date(self, date_text: str | None = None) -> 'Letter':
        """Center the first paragraph (the date line). House rule, every document."""
        m = PARA.search(self.xml)
        assert m, 'empty document'
        p = m.group(0)
        if date_text:
            assert date_text in _ptext(p), (
                f'first paragraph is not the date line (got {_ptext(p)!r})')
        if '<w:jc ' in p:
            p2 = re.sub(r'<w:jc w:val="[^"]*"/>', '<w:jc w:val="center"/>', p)
        elif '<w:pPr>' in p:
            p2 = p.replace('<w:pPr>', '<w:pPr><w:jc w:val="center"/>', 1)
        else:
            p2 = re.sub(r'(<w:p\b[^>]*>)', r'\1<w:pPr><w:jc w:val="center"/></w:pPr>',
                        p, count=1)
        self.xml = self.xml[:m.start()] + p2 + self.xml[m.end():]
        return self

    def tighten(self, bottom: int = 540, after: int | None = 80) -> 'Letter':
        """Page-shrink levers 2 and 3. `bottom` in twips, floor 360 (0.25in).
        w:top is deliberately NOT exposed -- reducing it breaks the letterhead."""
        assert bottom >= 360, 'bottom margin below 360 twips looks broken'
        self.xml = re.sub(r'(<w:pgMar[^>]*?)w:bottom="\d+"',
                          lambda m: m.group(1) + f'w:bottom="{bottom}"', self.xml)
        if after is not None:
            self.xml = re.sub(r'w:after="(\d+)"',
                              lambda m: f'w:after="{min(int(m.group(1)), after)}"', self.xml)
        return self

    # ---------- io ----------

    def save(self, dst: str) -> str:
        zin = zipfile.ZipFile(self.src)
        buf = io.BytesIO()
        zo = zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED)
        for it in zin.infolist():
            data = (self.xml.encode('utf8') if it.filename == 'word/document.xml'
                    else zin.read(it.filename))     # header*.xml copied untouched
            zo.writestr(it, data)
        zo.close(); zin.close()
        with open(dst, 'wb') as f:
            f.write(buf.getvalue())
        return dst

    @staticmethod
    def render_pdf(docx_path: str, outdir: str | None = None) -> str:
        outdir = outdir or os.path.dirname(os.path.abspath(docx_path)) or '.'
        subprocess.run([SOFFICE, '--headless', '--convert-to', 'pdf',
                        docx_path, '--outdir', outdir],
                       capture_output=True, check=True)
        return os.path.join(outdir,
                            os.path.splitext(os.path.basename(docx_path))[0] + '.pdf')

    @staticmethod
    def page_count(pdf_path: str) -> int:
        out = subprocess.run(['pdfinfo', pdf_path], capture_output=True, text=True).stdout
        m = re.search(r'^Pages:\s+(\d+)', out, re.M)
        return int(m.group(1)) if m else -1

    @staticmethod
    def overflow(pdf_path: str) -> list[str]:
        """Lines that spilled past page 1 -- tells you exactly how much to trim."""
        out = subprocess.run(['pdftotext', '-layout', '-f', '2', pdf_path, '-'],
                             capture_output=True, text=True).stdout
        return [ln for ln in out.splitlines() if ln.strip()]

    @staticmethod
    def leftover_placeholders(pdf_path: str) -> list[str]:
        """Catch anything unfilled before showing Klaus.

        The RE block renders as `Policy Number : 189661039`, so the bare words
        `Policy Number` are legitimate LABELS. Only flag a slot word when it sits
        on the VALUE side of the colon."""
        out = subprocess.run(['pdftotext', '-layout', pdf_path, '-'],
                             capture_output=True, text=True).stdout
        slot = (r'Carrier Name|Adjuster Name|Client Name|Insured Name|Claim Number'
                r'|Policy Number|MM/DD/YYYY|Carrier')
        value_side = re.compile(r':\s*(?:' + slot + r')\s*$')
        anywhere = re.compile(r'Month Day, Year|New Firm|\(###\)|teamemail@|Mr\./Ms\.'
                              r'|1P Carrier|3P Carrier|CONFIRM|Optional —'
                              r'|info@newfirm\.com|adjuster@carrier\.com')
        bad = []
        for ln in out.splitlines():
            s = ln.strip()
            if not s:
                continue
            if value_side.search(s) or anywhere.search(s):
                bad.append(s)
        return bad


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        pdf = sys.argv[1]
        print('pages     :', Letter.page_count(pdf))
        print('overflow  :', Letter.overflow(pdf) or 'none')
        print('leftovers :', Letter.leftover_placeholders(pdf) or 'none')
