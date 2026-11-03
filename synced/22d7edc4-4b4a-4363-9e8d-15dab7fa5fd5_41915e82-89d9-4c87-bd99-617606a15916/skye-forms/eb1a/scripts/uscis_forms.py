#!/usr/bin/env python3
"""USCIS AcroForm toolkit for skye-forms (EB-1A).

Four subcommands, in the order a filing actually needs them:

    fetch    download blank forms from USCIS.gov + report edition date and
             AcroForm integrity (never fill a firm-stored copy)
    dump     list every widget on a PDF: dotted field name, page, type, rect,
             checkbox on-state, current value. Works on blank templates AND on
             filled precedents (that is how the field maps were derived).
    fill     apply a JSON {field_name: value} map, page by page
    render   rasterize pages to JPEG so the filled form can be read back by eye

Run it with the venv that has pypdf + cryptography:

    ~/.local/opt/pdfvenv/bin/python scripts/uscis_forms.py <cmd> ...

cryptography is not optional. USCIS PDFs ship AES-encrypted with an empty
password, so plain pypdf raises DependencyError on the very first page access.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

FORM_URL = "https://www.uscis.gov/sites/default/files/document/forms/{form}.pdf"
PAGE_URL = "https://www.uscis.gov/{form}"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

# pdftoppm ships with the codex runtime on this Mac; poppler is not installed globally.
PDFTOPPM_CANDIDATES = [
    "pdftoppm",
    os.path.expanduser(
        "~/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/pdftoppm"
    ),
]


def _reader(path):
    from pypdf import PdfReader

    return PdfReader(path)


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def _fq(annot):
    """Resolve a widget's /Parent chain into its dotted AcroForm field name."""
    from pypdf.generic import IndirectObject

    parts, cur, guard = [], annot, 0
    while cur is not None and guard < 30:
        t = cur.get("/T")
        if t is not None:
            parts.append(str(t))
        cur = cur.get("/Parent")
        if isinstance(cur, IndirectObject):
            cur = cur.get_object()
        guard += 1
    return ".".join(reversed(parts))


def _annots(page):
    a = page.get("/Annots")
    return list(a.get_object()) if a else []


def _widgets(reader):
    """Yield (page_number_1based, annot_dict) for every widget in the document."""
    for i, page in enumerate(reader.pages, 1):
        for ref in _annots(page):
            an = ref.get_object()
            if an.get("/Subtype") == "/Widget":
                yield i, an


def _onstates(annot):
    """Checkbox/radio export values, e.g. ['/Y'] or ['/CON'].

    Never guess a checkbox value from the label you see in a PDF viewer — write
    the export value this returns, or the tick silently lands nowhere.
    """
    from pypdf.generic import IndirectObject

    if _fieldtype(annot) != "/Btn":
        # A text field's /AP /N is a single appearance stream, not a state map;
        # reading its keys would report /Type, /BBox... as if they were choices.
        return []
    ap = annot.get("/AP")
    if not ap:
        return []
    n = ap.get("/N")
    if isinstance(n, IndirectObject):
        n = n.get_object()
    try:
        return [k for k in n.keys() if k != "/Off"]
    except Exception:
        return []


def _value(annot):
    from pypdf.generic import IndirectObject

    v = annot.get("/V")
    if v is None:
        par = annot.get("/Parent")
        if isinstance(par, IndirectObject):
            par = par.get_object()
        if par is not None:
            v = par.get("/V")
    return v


def _fieldtype(annot):
    from pypdf.generic import IndirectObject

    ft = annot.get("/FT")
    if ft is None:
        par = annot.get("/Parent")
        if isinstance(par, IndirectObject):
            par = par.get_object()
        if par is not None:
            ft = par.get("/FT")
    return str(ft) if ft else "?"


def _edition(reader):
    """The edition date printed in the form's own footer."""
    seen = []
    for page in reader.pages:
        for m in re.findall(
            r"Form\s+([IG]-\d+[A-Z]?)\s+(?:Edition\s+)?(\d{2}/\d{2}/\d{2})",
            page.extract_text() or "",
        ):
            if m not in seen:
                seen.append(m)
    return seen


def cmd_fetch(args):
    """Download blank forms and report edition + AcroForm health."""
    os.makedirs(args.out, exist_ok=True)
    problems = []
    for form in args.forms:
        path = os.path.join(args.out, f"{form}.pdf")
        with open(path, "wb") as fh:
            fh.write(_get(FORM_URL.format(form=form)))

        r = _reader(path)
        fields = r.get_fields() or {}
        widgets = sum(len(_annots(p)) for p in r.pages)
        footer = _edition(r)
        printed = footer[0][1] if footer else "?"

        # The authority on whether an edition is current is the form's own USCIS
        # page, not the footer — USCIS routinely keeps an edition valid long past
        # the "Expires" date printed on it (G-28 is the standing example).
        live = "?"
        try:
            html = _get(PAGE_URL.format(form=form)).decode("utf-8", "ignore")
            html = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
            i = html.find("Edition Date")
            if i >= 0:
                m = re.search(r"(\d{2}/\d{2}/\d{2})", re.sub(r"<[^>]+>", " ", html[i : i + 400]))
                if m:
                    live = m.group(1)
        except Exception as e:  # network/policy hiccup is not fatal — just report it
            live = f"lookup failed ({e.__class__.__name__})"

        ok_form = len(fields) >= widgets * 0.9
        match = "OK" if live == printed else "*** MISMATCH ***"
        print(
            f"{form}: pages={len(r.pages)} fields={len(fields)} widgets={widgets} "
            f"acroform={'intact' if ok_form else 'BROKEN — re-download'} "
            f"footer_edition={printed} uscis_page_edition={live} {match}"
        )
        if not ok_form:
            problems.append(f"{form}: AcroForm damaged ({len(fields)} fields vs {widgets} widgets)")
        if live != printed and not live.startswith("lookup failed"):
            problems.append(f"{form}: downloaded {printed} but USCIS lists {live}")

    if problems:
        print("\nSTOP AND RESOLVE BEFORE FILLING:")
        for p in problems:
            print("  -", p)
        return 1
    return 0


def cmd_dump(args):
    r = _reader(args.pdf)
    pages = {int(x) for x in args.pages.split(",")} if args.pages else None
    pat = re.compile(args.grep) if args.grep else None
    rows = []
    for pg, an in _widgets(r):
        if pages and pg not in pages:
            continue
        name = _fq(an)
        if "BarCode" in name:
            continue
        if pat and not pat.search(name):
            continue
        val = _value(an)
        if args.filled_only and val in (None, "", "/Off"):
            continue
        rect = [round(float(x)) for x in (an.get("/Rect") or [0, 0, 0, 0])]
        rows.append(
            {
                "page": pg,
                "name": name,
                "type": _fieldtype(an),
                "rect": rect,
                "on_states": _onstates(an),
                "value": None if val is None else str(val),
            }
        )
    # Reading order (top-to-bottom, then left-to-right) is what lets you match a
    # field to the label printed beside it. Field *names* lie; geometry does not.
    rows.sort(key=lambda r_: (r_["page"], -r_["rect"][1], r_["rect"][0]))
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        for r_ in rows:
            extra = f" on={','.join(r_['on_states'])}" if r_["on_states"] else ""
            val = f"  = {r_['value']!r}" if r_["value"] not in (None, "") else ""
            print(f"p{r_['page']:>2} {r_['name']} [{r_['type']}] {r_['rect']}{extra}{val}")
    return 0


def cmd_fill(args):
    """Apply {field_name: value} through each field's own appearance stream.

    Going through update_page_form_field_values (rather than stamping text with
    reportlab) is what makes narrow boxes, comb SSN fields and single-digit boxes
    come out centred and correctly clipped.
    """
    from pypdf import PdfReader, PdfWriter

    with open(args.values) as fh:
        values = json.load(fh)

    reader = PdfReader(args.pdf)
    writer = PdfWriter(clone_from=reader)
    # Without NeedAppearances some viewers show blank boxes even though the
    # values are in the file.
    writer.set_need_appearances_writer(True)

    remaining = dict(values)
    applied = {}
    for page in writer.pages:
        names = {_fq(ref.get_object()) for ref in _annots(page)}
        chunk = {k: v for k, v in remaining.items() if k in names}
        if not chunk:
            continue
        writer.update_page_form_field_values(page, chunk, auto_regenerate=False)
        applied.update(chunk)
        for k in chunk:
            remaining.pop(k, None)

    with open(args.out, "wb") as fh:
        writer.write(fh)

    print(f"wrote {args.out}: {len(applied)} of {len(values)} fields applied")
    if remaining:
        print("\nNOT APPLIED — these names do not exist on any page:")
        for k in remaining:
            print("  -", k)
        print(
            "\nA silently-unapplied field is the main failure mode here. Most often it is a\n"
            "stale name from an older edition, or a checkbox whose export value differs from\n"
            "what you passed. Re-derive with `dump` against THIS pdf."
        )
        return 1
    return 0


def cmd_render(args):
    exe = next((c for c in PDFTOPPM_CANDIDATES if shutil.which(c) or os.path.exists(c)), None)
    if not exe:
        print("pdftoppm not found; cannot render for visual read-back", file=sys.stderr)
        return 1
    os.makedirs(args.out, exist_ok=True)
    cmd = [exe, "-jpeg", "-r", str(args.dpi)]
    if args.pages:
        lo, hi = (args.pages.split("-") + [args.pages.split("-")[0]])[:2]
        cmd += ["-f", lo, "-l", hi]
    cmd += [args.pdf, os.path.join(args.out, "page")]
    subprocess.run(cmd, check=True)
    print("rendered to", args.out)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="download blank forms + verify edition/AcroForm")
    f.add_argument("forms", nargs="+", help="e.g. i-140 g-28 i-907 g-1650 g-1145")
    f.add_argument("--out", default="forms")
    f.set_defaults(func=cmd_fetch)

    d = sub.add_parser("dump", help="list widgets: name, page, type, rect, on-states, value")
    d.add_argument("pdf")
    d.add_argument("--pages", help="comma-separated page numbers, 1-based")
    d.add_argument("--grep", help="regex filter on field name")
    d.add_argument("--filled-only", action="store_true", help="only widgets with a value")
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_dump)

    fl = sub.add_parser("fill", help="apply a JSON value map")
    fl.add_argument("pdf")
    fl.add_argument("values", help="JSON file of {field_name: value}")
    fl.add_argument("--out", required=True)
    fl.set_defaults(func=cmd_fill)

    r = sub.add_parser("render", help="rasterize pages for visual read-back")
    r.add_argument("pdf")
    r.add_argument("--out", default="render")
    r.add_argument("--pages", help="e.g. 1-8")
    r.add_argument("--dpi", type=int, default=150)
    r.set_defaults(func=cmd_render)

    args = ap.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
