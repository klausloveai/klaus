#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fill a LA County PI complaint filing package (SUM-100, CM-010, CIV 109)
from the firm's Drive templates. Config-driven; see SKILL.md.

Usage:
    python3 fill_forms.py config.json

The config JSON schema is documented in SKILL.md ("Build the config"). The
script strips the XFA layer (so every PDF viewer / e-filing portal renders the
AcroForm values), generates real appearance streams for the fields it fills,
and PRESERVES any field the template already had filled (e.g. the accented
attorney block) by never forcing global NeedAppearances.

Verify every output by rendering with Ghostscript before trusting it:
    gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r120 -dFirstPage=1 -dLastPage=1 \
       -sOutputFile=chk.png "1 - Summons.pdf"
(poppler/pdftoppm mangles these Judicial Council fonts — use gs, not pdftoppm.)
"""
import io, json, sys, subprocess, tempfile, os, re
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

# CIV 109 Column B checkboxes on pages 1-2 are NOT AcroForm fields — they are
# static '☐' glyphs. locate_civ109_boxes() finds each box by scanning the glyphs
# (reliable at x≈203) and pairs them with the 4-digit action codes by reading
# order (the codes and boxes appear in the same top-down sequence). This is robust
# across form revisions, so there are no fragile hard-coded coordinates.
import re


def locate_civ109_boxes(reader):
    """Return {action_code: (page_index, box_x, box_y)} for the Column B checkboxes."""
    found = {}
    for pi in range(min(2, len(reader.pages))):  # action table is on pages 1-2
        boxes, codes = [], []

        def v(text, cm, tm, fd, fs, boxes=boxes, codes=codes):
            ex = cm[0] * tm[4] + cm[2] * tm[5] + cm[4]
            ey = cm[1] * tm[4] + cm[3] * tm[5] + cm[5]
            if '☐' in text:            # ☐
                boxes.append((round(ex, 1), round(ey, 1)))
            m = re.match(r'^\s*(\d{4})\b', text)
            if m:
                codes.append(m.group(1))
        reader.pages[pi].extract_text(visitor_text=v)
        boxes.sort(key=lambda b: -b[1])     # top-to-bottom
        for i, code in enumerate(codes):    # pair by order
            if i < len(boxes) and code not in found:
                found[code] = (pi, boxes[i][0], boxes[i][1])
    return found


def fqname(o):
    parts, cur = [], o
    while cur is not None:
        t = cur.get('/T')
        if t:
            parts.append(str(t))
        p = cur.get('/Parent')
        cur = p.get_object() if p is not None else None
    return '.'.join(reversed(parts))


def strip_xfa(writer):
    """Remove XFA so viewers use the AcroForm values. Do NOT set NeedAppearances
    globally — that would force pre-filled fields (attorney block) to regenerate."""
    acro = writer._root_object.get('/AcroForm')
    if acro is not None:
        acro = acro.get_object()
        if '/XFA' in acro:
            del acro[NameObject('/XFA')]


def widget_on_state(o):
    """Return a checkbox/radio widget's 'on' state name (the /AP/N key != /Off)."""
    ap = o.get('/AP')
    if ap and '/N' in ap:
        for k in ap['/N'].keys():
            if k != '/Off':
                return k
    return '/Yes'


def collect_widgets(writer):
    out = []
    for pi, page in enumerate(writer.pages):
        for a in (page.get('/Annots') or []):
            o = a.get_object()
            if o.get('/Subtype') == '/Widget':
                out.append((pi, page, o))
    return out


def set_text(writer, matches):
    """matches: dict {predicate(fqname,TU) -> value}. Fills by fully-qualified name
    and lets pypdf build appearance streams (auto_regenerate=False => no global NA)."""
    resolved = {}  # fqname -> value
    for pi, page, o in collect_widgets(writer):
        if o.get('/FT') != '/Tx':
            continue
        nm = fqname(o)
        tu = str(o.get('/TU') or '')
        for pred, val in matches.items():
            if pred(nm, tu):
                resolved[nm] = val
    for page in writer.pages:
        try:
            writer.update_page_form_field_values(page, resolved, auto_regenerate=False)
        except Exception as e:
            print('  [warn] text fill:', e)
    return set(resolved)


def set_button(writer, predicate):
    """Check the first button widget matching predicate(fqname,TU). Uses the
    widget's own on-state and sets /V up the ancestor chain (radio-group value)."""
    for pi, page, o in collect_widgets(writer):
        if o.get('/FT') != '/Btn':
            continue
        nm = fqname(o); tu = str(o.get('/TU') or '')
        if predicate(nm, tu):
            on = widget_on_state(o)
            o[NameObject('/AS')] = NameObject(on)
            o[NameObject('/V')] = NameObject(on)
            par = o.get('/Parent')
            while par is not None:
                po = par.get_object(); po[NameObject('/V')] = NameObject(on)
                par = po.get('/Parent')
            return True
    print('  [warn] no button matched predicate')
    return False


def set_action_radio(writer, code):
    """Rev-04/26+ CIV 109 makes Column B 'Type of Action' a real radio (field '03')
    whose kid widgets carry on-states like '/2301 Premise Liability'. Select the kid
    whose on-state begins with the 4-digit action code. Returns True if matched
    (older revisions have only static glyphs → False, caller falls back to stamping)."""
    code = str(code)
    for pi, page, o in collect_widgets(writer):
        ft = o.get('/FT')
        if ft and ft != '/Btn':          # kids inherit FT from parent → ft is None
            continue
        on = widget_on_state(o)          # e.g. '/2301 Premise Liability'
        if on and on.lstrip('/').strip().startswith(code):
            o[NameObject('/AS')] = NameObject(on)
            o[NameObject('/V')] = NameObject(on)
            par = o.get('/Parent')
            while par is not None:
                po = par.get_object(); po[NameObject('/V')] = NameObject(on)
                par = po.get('/Parent')
            return True
    return False


def field_geom(writer, suffix):
    """Return (usable_width_pt, font_size_pt) for the text field whose fqname ends
    with `suffix`. Reads width from /Rect and size from the /DA (0/absent → 9pt)."""
    for pi, page, o in collect_widgets(writer):
        if fqname(o).endswith(suffix):
            rect = [float(x) for x in o['/Rect']]
            m = re.search(r'([\d.]+)\s+Tf', str(o.get('/DA') or ''))
            size = float(m.group(1)) if m else 9.0
            return (rect[2] - rect[0], size or 9.0)
    return (395.0, 9.0)


def wrap_text(text, max_w, size, font='Helvetica'):
    """Word-wrap `text` to `max_w` points at `size` (Helvetica≈ArialMT metrics),
    honoring any pre-existing '\\n'. SUM-100 caption fields are multiline but pypdf
    does NOT auto-wrap, so we insert the breaks ourselves. Long single tokens are
    left intact (never mid-word split)."""
    lines = []
    for para in text.split('\n'):
        line = ''
        for word in para.split(' '):
            trial = f'{line} {word}'.strip()
            if line and stringWidth(trial, font, size) > max_w:
                lines.append(line); line = word
            else:
                line = trial
        lines.append(line)
    return '\n'.join(lines)


def overlay(writer, page_index, draw_fn):
    """Stamp reportlab drawing onto a page (letter, 612x792)."""
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(612, 792))
    draw_fn(c); c.save(); buf.seek(0)
    writer.pages[page_index].merge_page(PdfReader(buf).pages[0])


# --------------------------------------------------------------------------- #
def fill_sum100(cfg, tmpl, out):
    r = PdfReader(tmpl); w = PdfWriter(); w.append(r); strip_xfa(w)
    line2 = f"{cfg['courthouse_street']}, {cfg['courthouse_city_zip']}"
    # NOTICE-TO-DEFENDANT / SUED-BY-PLAINTIFF boxes are multiline but don't auto-wrap;
    # wrap to the field width so long captions (multi-defendant, minor-by-GAL) don't
    # overflow into the FOR-COURT-USE box. Feed these the VERBATIM complaint caption.
    dw, ds = field_geom(w, 'FillText25[0]')
    pw, ps = field_geom(w, 'FillText180[0]')
    defendant = wrap_text(cfg['defendant_block'], dw - 6, ds)
    plaintiff = wrap_text(cfg['plaintiff'], pw - 6, ps)
    set_text(w, {
        (lambda nm, tu: nm.endswith('FillText25[0]')): defendant,
        (lambda nm, tu: nm.endswith('FillText180[0]')): plaintiff,
        (lambda nm, tu: nm.endswith('FillText3[0]')): cfg['courthouse_name'],
        (lambda nm, tu: nm.endswith('FillText2[0]')): line2,
    })
    # FillText30 (attorney) is left as-is from the template (pre-filled, accented)
    # unless the config overrides it — use `attorney_line` when the template's
    # pre-filled block needs correcting for a given filing.
    if cfg.get('attorney_line'):
        set_text(w, {(lambda nm, tu: nm.endswith('FillText30[0]')): cfg['attorney_line']})
    with open(out, 'wb') as fh: w.write(fh)
    print('wrote', out)


def fill_cm010(cfg, tmpl, out):
    r = PdfReader(tmpl); w = PdfWriter(); w.append(r); strip_xfa(w)
    # Firm standing rule (Klaus, 2026-07-09): ALL litigation documents use phone AND
    # fax = (626) 479-2207. Override the template's attorney phone/fax accordingly.
    set_text(w, {
        (lambda nm, tu: nm.endswith('Phone[0]') or tu.strip() == 'TELEPHONE NUMBER:'): cfg.get('firm_phone', '(626) 479-2207'),
        (lambda nm, tu: nm.endswith('Fax[0]') or tu.strip() == 'FAX NUMBER:'): cfg.get('firm_fax', '(626) 479-2207'),
        (lambda nm, tu: nm.endswith('AttyFor[0]')): cfg['plaintiff_for'],
        (lambda nm, tu: tu == 'SUPERIOR COURT OF CALIFORNIA, COUNTY OF' or nm.endswith('CrtCounty[0]')): cfg['county'],
        (lambda nm, tu: nm.endswith('CrtStreet[0]')): cfg['courthouse_street'],
        (lambda nm, tu: nm.endswith('CrtMailingAdd[0]')): cfg['courthouse_street'],
        (lambda nm, tu: nm.endswith('CrtCityZip[0]')): cfg['courthouse_city_zip'],
        (lambda nm, tu: nm.endswith('CrtBranch[0]')): cfg['courthouse_name'],
        (lambda nm, tu: nm.endswith('Party1[0]')): cfg['case_name'],
        (lambda nm, tu: nm.endswith('FillText1[0]')): cfg['num_causes'],
        (lambda nm, tu: nm.endswith('SigName[0]')): cfg['attorney_print_name'],
    })
    # Amount: Unlimited / Limited (radio 'limited1'); on-state read from widget.
    unlimited = cfg.get('amount', 'unlimited').lower().startswith('un')
    set_button(w, lambda nm, tu: nm.endswith('limited1[0]') if unlimited else nm.endswith('limited1[1]'))
    # Item 1 case type — detect by tooltip so it works across form revisions
    # (older rev names it CheckBox23, newer Item1Check[5]; both TU='Other PI/PD/WD (23)').
    ct_tu = cfg.get('case_type_tooltip', 'Other PI/PD/WD (23)')
    set_button(w, lambda nm, tu: tu.strip() == ct_tu)
    # Item 2 complex? No | Item 3 monetary | Item 5 class action? No
    set_button(w, lambda nm, tu: nm.endswith('is1[1]'))   # complex = No
    # Item 3 remedies — "check all that apply". Default monetary; add 'punitive'
    # whenever the complaint's prayer seeks exemplary damages (Civ. Code § 3294),
    # and 'nonmonetary' for declaratory/injunctive relief.
    REMEDY_FIELD = {'monetary': 'Ch1[0]', 'nonmonetary': 'Ch2[0]', 'punitive': 'Ch3[0]'}
    for remedy in cfg.get('remedies', ['monetary']):
        fld = REMEDY_FIELD[remedy]
        set_button(w, lambda nm, tu, f=fld: nm.endswith(f))
    set_button(w, lambda nm, tu: nm.endswith('is[1]'))    # class action = No
    with open(out, 'wb') as fh: w.write(fh)
    print('wrote', out)


def fill_civ109(cfg, tmpl, out):
    r = PdfReader(tmpl); w = PdfWriter(); w.append(r); strip_xfa(w)
    reason = str(cfg['civ109_reason'])
    set_text(w, {
        (lambda nm, tu: tu == 'CITY'): cfg['incident_city'],
        (lambda nm, tu: tu == 'STATE'): cfg['incident_state'],
        (lambda nm, tu: tu == 'ZIP CODE'): cfg['incident_zip'],
        (lambda nm, tu: tu == 'ADDRESS'): cfg['incident_address'],
        (lambda nm, tu: tu.startswith('I certify that this case is properly filed')): cfg['district'],
    })
    # Reason radios have TU == the plain number ('1'..'11')
    set_button(w, lambda nm, tu: tu.strip() == reason)
    # Column B action selection. Newer (Rev 04/26+) forms expose it as a real radio
    # ('03' Type of Action) → set it directly. Older forms have only static '☐'
    # glyphs → fall back to stamping an X at the located box.
    code = str(cfg['civ109_action_code'])
    short = cfg['case_short_title']
    radio_set = set_action_radio(w, code)
    loc = None if radio_set else locate_civ109_boxes(PdfReader(tmpl)).get(code)
    for pi in range(len(w.pages)):
        def draw(c, pi=pi):
            c.setFont('Helvetica', 9); c.drawString(48, 741, short)
            if loc and loc[0] == pi:
                # the '☐' glyph origin sits near the box TOP, so drop the X ~2.5pt
                # below it to center it inside the box.
                c.setFont('Helvetica-Bold', 10); c.drawString(loc[1] + 0.8, loc[2] - 2.5, 'X')
        overlay(w, pi, draw)
    if not radio_set and not loc:
        print('  [warn] could not locate CIV109 action for code', code, '- check by hand')
    with open(out, 'wb') as fh: w.write(fh)
    print('wrote', out)


def main():
    cfg = json.load(open(sys.argv[1], encoding='utf-8'))
    t = cfg['templates']; outd = cfg['out_dir']
    os.makedirs(outd, exist_ok=True)
    fill_sum100(cfg, t['sum100'], os.path.join(outd, '1 - Summons.pdf'))
    fill_cm010(cfg, t['cm010'], os.path.join(outd, '3 - Civil Case Cover Sheet.pdf'))
    fill_civ109(cfg, t['civ109'], os.path.join(outd, '4 - Civil Case Cover Sheet Addendum and Statement of Location.pdf'))
    print('DONE ->', outd)


if __name__ == '__main__':
    main()
