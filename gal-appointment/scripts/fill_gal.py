#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fill CIV-010 (Application for Appointment of Guardian ad Litem) AND
CIV-011 (Order Appointing Guardian ad Litem) from a config.json.

Both forms are produced and FLATTENED (so values render in every viewer incl.
macOS Preview). Signatures, dates, and the case number are left BLANK.

Usage:
    python3 fill_gal.py config.json

Requires: pypdf and the `qpdf` CLI (brew install qpdf). Reuses the fill
primitives from the sibling file-complaint skill.

Caption: use the SHORT form on these small JC caption boxes — e.g.
plaintiff "NAME, a minor, etc., et al." / defendant "NAME, et al." (Hernán's
preference; the full defendant list overflows the box onto the Other Parent row).
The SUMMONS (SUM-100) still names every defendant for service — that's a
different form; see file-complaint.

Verify every output by RENDERING with Ghostscript (poppler mangles JC fonts):
    gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r140 -sOutputFile=chk_%d.png OUT.pdf
"""
import json, sys, os, subprocess, tempfile
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'file-complaint', 'scripts'))
from fill_forms import strip_xfa, set_text, set_button   # noqa: E402

def ew(s):   return (lambda nm, tu, s=s: nm.endswith(s))
def tueq(t): return (lambda nm, tu, t=t: tu.strip() == t.strip())


def _flatten(inp, out):
    subprocess.run(['qpdf', '--generate-appearances', '--flatten-annotations=all', inp, out], check=True)


def fill_civ010(cfg, scratch):
    a, ct, m, ap, cap = cfg['attorney'], cfg['court'], cfg['minor'], cfg['applicant'], cfg['caption']
    r = PdfReader(os.path.join(ASSETS, 'civ010.pdf'))
    w = PdfWriter(); w.append(r); strip_xfa(w)
    set_text(w, {
        ew('AttyBarNo[0]'): a['sbn'], ew('AttyPartyInfo[0].Name[0]'): a['name'],
        ew('AttyFirm[0]'): a['firm'], ew('AttyPartyInfo[0].Street[0]'): a['street'],
        ew('AttyPartyInfo[0].City[0]'): a['city'], ew('AttyPartyInfo[0].State[0]'): a['state'],
        ew('AttyPartyInfo[0].Zip[0]'): a['zip'], ew('AttyPartyInfo[0].Phone[0]'): a['phone'],
        ew('AttyPartyInfo[0].Fax[0]'): a['fax'], ew('AttyPartyInfo[0].Email[0]'): a['email'],
        ew('AttyFor[0]'): cfg['attorney_for'],
        ew('CrtCounty[0]'): ct['county'], ew('CourtInfo[0].CrtStreet[0]'): ct['street'],
        ew('CrtMailingAdd[0]'): ct['mailing'], ew('CrtCityZip[0]'): ct['city_zip'],
        ew('CrtBranch[0]'): ct['branch'],
        ew('TitlePartyName[0].Party1_ft[0]'): cap['plaintiff'],   # both pages
        ew('TitlePartyName[0].Party2_ft[0]'): cap['defendant'],
        ew('ApplicantName_ft[0]'): ap['name'], ew('Item1a[0].ParentName_ft[0]'): m['name'],
        ew('GALInfo_ft[0]'): ap['gal_info'], ew('PersonRepInfo_ft[0]'): ap['rep_info'],
        ew('Item4a[0].MinorDOB_ft[0]'): m['dob'], ew('Item8b[0].SpecifyFamRel_ft[0]'): ap['relationship'],
        ew('Page2[0].AttName_ft[0]'): a['name'], ew('PoPDecl[0].ApplName_ft[0]'): ap['name'],
        ew('Page2[0].GALName_ft[0]'): ap['name'],
    })
    preds = [tueq('the parent of'),               # item 1a
             tueq('a party to the suit.'),        # item 1d  (parent is ALSO a plaintiff)
             ew('Item4a[0].Minor_cb[0]'),         # item 4a
             tueq('The person named in item 3 is a minor and is (check one):'),  # item 5 header
             tueq('has no guardian or conservator of the estate.'),  # item 6c
             tueq('A familial relationship'),      # item 8b
             tueq('not aware of any actual or potential conflicts of interest that would or might arise from the appointment.')]  # 9a
    if cfg.get('ex_parte', True):
        preds.insert(0, tueq('EX PARTE'))
    preds.append(tueq('a plaintiff or petitioner in this action and the summons has not been issued.')
                 if not cfg.get('summons_issued', False)
                 else tueq('a defendant or respondent in this action. More than 10 days have passed since service of the summons, and no one has applied for the appointment of a guardian ad litem.'))
    for p in preds:
        set_button(w, p)
    tmp = os.path.join(scratch, 'civ010_filled.pdf')
    with open(tmp, 'wb') as fh:
        w.write(fh)
    out = os.path.join(cfg['out_dir'], cfg.get('civ010_name', 'CIV-010 (GAL Application) for signature.pdf'))
    _flatten(tmp, out)
    return out


def fill_civ011(cfg, scratch):
    a, ct, m, ap, cap = cfg['attorney'], cfg['court'], cfg['minor'], cfg['applicant'], cfg['caption']
    r = PdfReader(os.path.join(ASSETS, 'civ011.pdf'))
    w = PdfWriter(); w.append(r); strip_xfa(w)
    set_text(w, {
        ew('AttyPartyInfo[0].AttyBarNo[0]'): a['sbn'], ew('AttyPartyInfo[0].Name[0]'): a['name'],
        ew('AttyPartyInfo[0].AttyFirm[0]'): a['firm'], ew('AttyPartyInfo[0].Street[0]'): a['street'],
        ew('AttyPartyInfo[0].City[0]'): a['city'], ew('AttyPartyInfo[0].State[0]'): a['state'],
        ew('AttyPartyInfo[0].Zip[0]'): a['zip'], ew('AttyPartyInfo[0].Phone[0]'): a['phone'],
        ew('AttyPartyInfo[0].Fax[0]'): a['fax'], ew('AttyPartyInfo[0].Email[0]'): a['email'],
        ew('AttyPartyInfo[0].AttyFor[0]'): cfg['attorney_for'],
        ew('CourtInfo[0].CrtCounty[0]'): ct['county'], ew('CourtInfo[0].Street_ft[0]'): ct['street'],
        ew('CourtInfo[0].MailingAdd_ft[0]'): ct['mailing'], ew('CourtInfo[0].CityZip_ft[0]'): ct['city_zip'],
        ew('CourtInfo[0].Branch_ft[0]'): ct['branch'],
        ew('TitlePartyName[0].Party1_ft[0]'): cap['plaintiff'],   # both pages
        ew('TitlePartyName[0].Party2_ft[0]'): cap['defendant'],
        ew('li1[0].ApplicantNm_ft[0]'): ap['name'],
        ew('li1[0].RepPersonNm_ft[0]'): m['name'],      # page1 "seeks..." + page2 "is appointed..."
        ew('li1[0].GALName_ft[0]'): ap['name'],         # page2 item 6 GAL name
        ew('Item4a[0].DOB_ft[0]'): m['dob'],
    })
    preds = [tueq('All notices required by law have been given.'),   # item 3 (minor plaintiff, summons not issued -> no notice required, finding proper)
             ew('Item4a[0].Minor_cb[0]'),                            # item 4a
             tueq('The person for whom a guardian ad litem is to be appointed'),  # item 5 header
             tueq('does not have a guardian or conservator of the estate.'),      # item 5c
             tueq('is not')]                                         # item 7: GAL is NOT authorized to waive substantive rights (protective; expected for a minor)
    if cfg.get('ex_parte', True):
        preds.insert(0, tueq('EX PARTE'))
    for p in preds:
        set_button(w, p)
    tmp = os.path.join(scratch, 'civ011_filled.pdf')
    with open(tmp, 'wb') as fh:
        w.write(fh)
    out = os.path.join(cfg['out_dir'], cfg.get('civ011_name', 'CIV-011 (Proposed Order Appointing GAL).pdf'))
    _flatten(tmp, out)
    return out


def main():
    cfg = json.load(open(sys.argv[1]))
    os.makedirs(cfg['out_dir'], exist_ok=True)
    with tempfile.TemporaryDirectory() as scratch:
        o10 = fill_civ010(cfg, scratch)
        o11 = fill_civ011(cfg, scratch)
    print('CIV-010 ->', o10)
    print('CIV-011 ->', o11)


if __name__ == '__main__':
    main()
