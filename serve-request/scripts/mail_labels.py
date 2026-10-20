#!/usr/bin/env python3
"""
mail_labels.py — two-up half-sheet address labels (8.5 x 5.5 in each, two per Letter sheet)
for first-class mailed service. Approved by Klaus 2026-10-20 (Lina Lu): bold firm name + return
address top-left, recipient 20pt centred-left, "FIRST-CLASS MAIL" bottom-left. Print at 100%
(Actual size). Odd number of recipients -> the last sheet's bottom half is left blank.

Usage:
    python3 mail_labels.py OUT.pdf "Name|Street|City, State ZIP" ["Name|Street|City, State ZIP" ...]
           [--from "Lingtu Law Office|13191 Crossroads Parkway North, Suite 295|City of Industry, California 91746"]
           [--class "FIRST-CLASS MAIL"]
Addresses are written out in full (Road, California), per the firm house style.
"""
import fitz, sys, argparse
R = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
B = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("to", nargs="+")
ap.add_argument("--from", dest="frm", default="Lingtu Law Office|13191 Crossroads Parkway North, Suite 295|City of Industry, California 91746")
ap.add_argument("--class", dest="cls", default="FIRST-CLASS MAIL")
a = ap.parse_args()
d = fitz.open(); frm = a.frm.split("|")
for n, to in enumerate(a.to):
    if n % 2 == 0:
        pg = d.new_page(width=612, height=792)
        pg.insert_font(fontname="R", fontfile=R); pg.insert_font(fontname="B", fontfile=B)
    y0 = (n % 2) * 396
    for k, l in enumerate(frm):
        pg.insert_text((36, y0 + 48 + k * 15), l, fontname="B" if k == 0 else "R", fontsize=11)
    for k, l in enumerate(to.split("|")):
        pg.insert_text((200, y0 + 200 + k * 26), l, fontname="B" if k == 0 else "R", fontsize=20)
    if a.cls:
        pg.insert_text((36, y0 + 370), a.cls, fontname="B", fontsize=10)
d.save(a.out); print(a.out, d.page_count, "page(s)")
