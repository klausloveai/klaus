#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build reusable FILLABLE templates civ010(Hernan).pdf and civ011(Hernan).pdf with
ONLY the fixed attorney block pre-filled (Hernán S. Simó / Law Office of Shenqi
Cai APC). Everything case-specific (court, caption, minor, applicant, DOB,
checkboxes) is left BLANK and editable. NeedAppearances is set so the pre-filled
values display; the forms remain fillable in Adobe Acrobat.

Usage:
    python3 make_hernan_template.py <out_dir>

Matches the firm's Drive "Litigation Forms" template convention (sum100(Hernan),
cm010(Hernan), ...). Upload the two outputs into that template folder.
"""
import sys, os
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'file-complaint', 'scripts'))
from fill_forms import strip_xfa, set_text   # noqa: E402

def ew(s): return (lambda nm, tu, s=s: nm.endswith(s))

ATTY = {  # the fixed block — identical on every Hernán GAL case
    'sbn': '354175', 'name': 'Hernán S. Simó', 'firm': 'Law Office of Shenqi Cai APC',
    'street': '13191 Crossroads Pkwy N, Suite 295', 'city': 'City of Industry',
    'state': 'CA', 'zip': '91746', 'phone': '(626) 479-2207', 'fax': '(626) 479-2207',
    'email': 'hernan.s@lingtulaw.com',
}

def need_appearances(w):
    acro = w._root_object.get('/AcroForm')
    if acro is not None:
        acro.get_object()[NameObject('/NeedAppearances')] = BooleanObject(True)

def build(src, atty_prefix, out):
    r = PdfReader(os.path.join(ASSETS, src)); w = PdfWriter(); w.append(r); strip_xfa(w)
    set_text(w, {
        ew(atty_prefix + 'AttyBarNo[0]'): ATTY['sbn'],
        ew('AttyPartyInfo[0].Name[0]'): ATTY['name'],
        ew(atty_prefix + 'AttyFirm[0]'): ATTY['firm'],
        ew('AttyPartyInfo[0].Street[0]'): ATTY['street'],
        ew('AttyPartyInfo[0].City[0]'): ATTY['city'],
        ew('AttyPartyInfo[0].State[0]'): ATTY['state'],
        ew('AttyPartyInfo[0].Zip[0]'): ATTY['zip'],
        ew('AttyPartyInfo[0].Phone[0]'): ATTY['phone'],
        ew('AttyPartyInfo[0].Fax[0]'): ATTY['fax'],
        ew('AttyPartyInfo[0].Email[0]'): ATTY['email'],
    })
    need_appearances(w)
    with open(out, 'wb') as fh:
        w.write(fh)
    return out

def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out_dir, exist_ok=True)
    # CIV-010 uses AttyBarNo[0] / AttyFirm[0] directly under the caption block;
    # CIV-011 nests them under AttyPartyInfo[0].
    o10 = build('civ010.pdf', '', os.path.join(out_dir, 'civ010(Hernan).pdf'))
    o11 = build('civ011.pdf', 'AttyPartyInfo[0].', os.path.join(out_dir, 'civ011(Hernan).pdf'))
    print('template ->', o10)
    print('template ->', o11)

if __name__ == '__main__':
    main()
