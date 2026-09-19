#!/usr/bin/env python3
"""Combine scene / vehicle-damage photos into ONE pdf for a case referral.

Usage: python3 combine_photos.py "Scene Photos.pdf" img1.jpg img2.jpg ...
Downscales to keep the packet small; Gmail caps at 25 MB total.
"""
import sys
from PIL import Image

out, srcs = sys.argv[1], sys.argv[2:]
if not srcs:
    sys.exit("no images given")
ims = []
for s in srcs:
    im = Image.open(s).convert("RGB")
    if max(im.size) > 1600:
        f = 1600 / max(im.size)
        im = im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS)
    ims.append(im)
ims[0].save(out, save_all=True, append_images=ims[1:], resolution=150.0)
print("saved", out, len(ims), "pages")
