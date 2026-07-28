#!/usr/bin/env python3
"""Generate a tri-fold mailing COVER PAGE for a #10 double-window envelope.

The page carries ONLY two things (nothing else):
  • firm return address  — aligns with the TOP window
  • recipient address    — aligns with the BOTTOM window
plus two solid tri-fold guide lines at 3.667" and 7.333" from the page top.

Rendered at exact coordinates via headless Chrome (absolute-positioned HTML), because
window alignment is measured in fractions of an inch — Word paragraph spacing is not
reliable enough for this.

USPS note: the address blocks contain ONLY the deliverable address — never add a
"To:" / "From:" label. The postal OCR reads these blocks through the windows.

Usage:
  python3 make_cover_page.py <out.pdf> "<recipient line 1>" ["<line 2>" ...]
  python3 make_cover_page.py --template <out.pdf>     # placeholder version

Tune POS_* below if a test print shows the addresses off-window.
"""
import sys, subprocess, tempfile, os

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# --- position knobs (inches from page top/left) — adjust after a test print ---
RET_TOP, RET_LEFT, RET_SIZE = 0.50, 0.90, 10
TO_TOP,  TO_LEFT,  TO_SIZE  = 2.05, 1.10, 11
FOLD1, FOLD2 = 3.667, 7.333

RETURN_ADDRESS = ["Lingtu Law Office",
                  "13191 Crossroads Pkwy N, Suite 295",
                  "City of Industry, CA 91746"]

TEMPLATE_RECIPIENT = ["[Recipient Name] and Any/All Residents,",
                      "Occupants, or Dog Owners",
                      "[Street Address]",
                      "[City, State ZIP]"]

HTML = """<meta charset="utf-8">
<style>
  @page {{ size: 8.5in 11in; margin: 0; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ width: 8.5in; height: 11in; position: relative;
         font-family: "Times New Roman", Times, serif; }}
  .ret  {{ position: absolute; left: {rl}in; top: {rt}in; font-size: {rs}pt; line-height: 1.25; }}
  .to   {{ position: absolute; left: {tl}in; top: {tt}in; font-size: {ts}pt; line-height: 1.30; }}
  .fold {{ position: absolute; left: 0; width: 8.5in; border-top: 0.75pt solid #000; }}
  .f1   {{ top: {f1}in; }}
  .f2   {{ top: {f2}in; }}
</style>
<div class="ret">{ret}</div>
<div class="to">{to}</div>
<div class="fold f1"></div>
<div class="fold f2"></div>
"""


def build(out_pdf, recipient_lines):
    html = HTML.format(
        rl=RET_LEFT, rt=RET_TOP, rs=RET_SIZE,
        tl=TO_LEFT, tt=TO_TOP, ts=TO_SIZE, f1=FOLD1, f2=FOLD2,
        ret="<br>\n".join(RETURN_ADDRESS), to="<br>\n".join(recipient_lines))
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html); tmp = f.name
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", tmp],
                   capture_output=True)
    os.unlink(tmp)
    print("cover page:", out_pdf)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--template":
        build(a[1], TEMPLATE_RECIPIENT)
    else:
        build(a[0], a[1:])
