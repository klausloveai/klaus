#!/usr/bin/env python3
"""Shrink a PDF by re-encoding its images, without making captures illegible.

    from slim import slim
    slim(doc, cap_dpi=300, quality=90)     # in-place on a fitz Document

Two independent wins:
  * lossless PNG screenshots re-encoded as JPEG - usually the bulk of the saving, and
    visually indistinguishable at q90
  * resolution capped relative to the size the image is actually PRINTED at, not its pixel
    count, so an image already at 90 DPI on the page is left alone

cap_dpi=300 / q90 is the default and is visually lossless for print. Only drop to 120 / q72
when a hard size cap cannot otherwise be met - at 120 DPI a full newspaper broadsheet's body
columns go soft, though phone screenshots and article text stay clean.
"""
import io

def slim(doc, cap_dpi=300, quality=90, min_bytes=40_000, verbose=False):
    from PIL import Image
    import fitz
    touched = saved = 0
    for i in range(doc.page_count):
        pg = doc[i]
        W, H = pg.rect.width / 72.0, pg.rect.height / 72.0
        # pages larger than Letter get scaled down when printed, so their effective DPI is
        # higher than the raw page geometry suggests
        pscale = min(8.5 / W, 11.0 / H, 1.0)
        for x in pg.get_images(full=True):
            xref = x[0]
            try:
                info = doc.extract_image(xref)
            except Exception:
                continue
            before = len(info["image"])
            if before < min_bytes:
                continue
            try:
                im = Image.open(io.BytesIO(info["image"])).convert("RGB")
            except Exception:
                continue
            rects = pg.get_image_rects(xref)
            if rects:
                r = max(rects, key=lambda z: z.width * z.height)
                win = max((r.width / 72.0) * pscale, 0.2)
                hin = max((r.height / 72.0) * pscale, 0.2)
                cap = (max(1, int(win * cap_dpi)), max(1, int(hin * cap_dpi)))
                if im.width > cap[0] or im.height > cap[1]:
                    im.thumbnail(cap, Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
            if len(buf.getvalue()) < before * 0.95:
                pg.replace_image(xref, stream=buf.getvalue())
                touched += 1
                saved += before - len(buf.getvalue())
    if verbose:
        print(f"re-encoded {touched} images, saved {saved/1e6:.0f} MB of image payload")
    return touched, saved
