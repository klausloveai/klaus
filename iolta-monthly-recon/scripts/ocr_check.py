#!/usr/bin/env python3
"""Read the MICR line at the bottom of each captured check front and compare it with
the file name. The grabber names a file from the table row, but if the modal was still
showing the previous check the image and the name disagree — this catches that."""
import os, re, subprocess, sys, tempfile
from PIL import Image

D = sys.argv[1]
bad, ok, unread = [], 0, []
for fn in sorted(os.listdir(D)):
    m = re.match(r"^(\d{8})_ck(\d+)_([\d.]+)_front\.jpg$", fn)
    if not m: continue
    want_ck, want_amt = m.group(2), m.group(3)
    im = Image.open(os.path.join(D, fn)); w, h = im.size
    # top-right corner carries the printed check number
    crop = im.crop((int(w*0.72), 0, w, int(h*0.18))).resize((int(w*0.28*3), int(h*0.18*3)))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        crop.save(t.name)
        txt = subprocess.run(["tesseract", t.name, "-", "--psm", "6",
                              "-c", "tessedit_char_whitelist=0123456789"],
                             capture_output=True, text=True).stdout
    os.unlink(t.name)
    nums = re.findall(r"\d{5,6}", txt)
    if not nums:
        unread.append(fn); continue
    if want_ck in nums: ok += 1
    else: bad.append((fn, want_ck, nums))

print(f"front images checked: {ok+len(bad)+len(unread)}")
print(f"  number matches file name : {ok}")
print(f"  MISMATCH                 : {len(bad)}")
for fn, want, got in bad: print(f"      {fn}  -> image shows {got}")
print(f"  could not read           : {len(unread)}")
for fn in unread: print(f"      {fn}")
