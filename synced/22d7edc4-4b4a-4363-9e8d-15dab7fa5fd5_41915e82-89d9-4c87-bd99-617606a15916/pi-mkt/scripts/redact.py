#!/usr/bin/env python3
"""Mosaic-redact a check (or any image) and emit the cover/reveal pair.

Usage:
  redact.py check  <page.pdf|image> <boxes.json> <out_dir>
  redact.py photo  <image> <boxes.json> <out_path>
  redact.py render <page.pdf> <out.png>          # PDF page 1 -> PNG at 200 dpi

boxes.json for `check`:
{
  "crop":   [x0, y0, x1, y1],          # the check itself, in rendered-page pixels (optional)
  "pii":    [[x0,y0,x1,y1], ...],      # blurred on BOTH versions (coords relative to the crop)
  "amount": [[x0,y0,x1,y1], ...],      # blurred on the COVER version only (words + numeric amount)
  "amount_numeric": [x0,y0,x1,y1]      # the "$****7,500.00" box, used to compute the magnifier crop
}
boxes.json for `photo`: {"pii": [[x0,y0,x1,y1], ...]}   (plates, faces, decals)

`check` writes check_crop.png, check_cover.png, check_reveal.png and prints the
Canva crop_media values that centre `amount_numeric` in the 266px magnifier.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

MAGNIFIER_D = 266.16614305931216  # diameter of the magnifier circle element in the template


def mosaic(im, box, block=14):
    """Pixelate `box`. `block` is a minimum: tiles grow with the box and the image,
    so a plate in a 4000px phone photo gets ~5 tiles across its height instead of
    a dozen legible ones (a fixed 14–20px tile left such plates readable)."""
    box = tuple(int(v) for v in box)
    r = im.crop(box)
    w, h = r.size
    block = max(block, min(w, h) // 5, max(im.size) // 200)
    r = r.filter(ImageFilter.GaussianBlur(max(6, block // 2)))
    r = r.resize((max(1, w // block), max(1, h // block)), Image.BILINEAR)
    r = r.resize((w, h), Image.NEAREST)
    im.paste(r, box)


def render(pdf, out_png, dpi=200):
    import pymupdf
    doc = pymupdf.open(pdf)
    doc[0].get_pixmap(dpi=dpi).save(out_png)
    return out_png


def load(path):
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        png = p.with_suffix(".rendered.png")
        render(p, png)
        p = png
    return ImageOps.exif_transpose(Image.open(p)).convert("RGB")


def magnifier_crop(img_w, img_h, amt):
    x0, y0, x1, y1 = amt
    scale = 0.82 * MAGNIFIER_D / (x1 - x0)  # amount fills ~82% of the circle
    scale = max(scale, MAGNIFIER_D / img_h)  # image must still cover the circle vertically
    cx, cy = (x0 + x1) / 2 * scale, (y0 + y1) / 2 * scale
    return {
        "width": round(img_w * scale, 1),
        "height": round(img_h * scale, 1),
        "left": round(MAGNIFIER_D / 2 - cx, 1),
        "top": round(MAGNIFIER_D / 2 - cy, 1),
    }


def cmd_check(src, boxes_path, out_dir):
    boxes = json.loads(Path(boxes_path).read_text())
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    im = load(src)
    if boxes.get("crop"):
        im = im.crop(tuple(boxes["crop"]))
    im.save(out / "check_crop.png")
    reveal = im.copy()
    for b in boxes.get("pii", []):
        mosaic(reveal, b)
    reveal.save(out / "check_reveal.png")
    cover = reveal.copy()
    for b in boxes.get("amount", []):
        mosaic(cover, b, 18)
    cover.save(out / "check_cover.png")
    result = {"size": im.size, "files": [str(out / n) for n in ("check_cover.png", "check_reveal.png")]}
    if boxes.get("amount_numeric"):
        result["magnifier_crop_media"] = magnifier_crop(*im.size, boxes["amount_numeric"])
    print(json.dumps(result, indent=2))


def cmd_photo(src, boxes_path, out_path):
    boxes = json.loads(Path(boxes_path).read_text()) if boxes_path != "-" else {"pii": []}
    im = load(src)
    for b in boxes.get("pii", []):
        mosaic(im, b, 20)
    im.save(out_path, quality=92)
    print(json.dumps({"size": im.size, "file": out_path}))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    mode = sys.argv[1]
    if mode == "check":
        cmd_check(*sys.argv[2:5])
    elif mode == "photo":
        cmd_photo(*sys.argv[2:5])
    elif mode == "render":
        render(sys.argv[2], sys.argv[3])
        print(sys.argv[3])
    else:
        sys.exit(__doc__)
