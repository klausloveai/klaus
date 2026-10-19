#!/usr/bin/env python3
"""
fill_inplace_pos.py — Date and sign the blanks an attorney left in his own signed
document: the embedded Proof of Service, and (opt-in) the Declaration of Translator.

Usage:
    python3 fill_inplace_pos.py <outdir> <file.pdf> [file2.pdf ...]
        [--inplace]                 overwrite the source files instead of writing to <outdir>
        [--date "October 16"]       default: today, as "Month D" (", 2026" is already printed)
        [--city "City of Industry"] city written into an "at ____, California" blank
        [--declarant "Klaus Liu"]   who signs the POS
        [--translator "Klaus Liu"]  ALSO date + sign the Declaration of Translator

    Pass "-" as <outdir> together with --inplace.

Use this when Hernán (or any attorney) drafted the Proof of Service INTO the pleading with
the blanks left open. Appending the firm template POS to such a document would give it
TWO proofs of service and would discard any case-specific recital he wrote. Fill in place.

What it fills — and nothing else:
  POS region (from the "PROOF OF SERVICE" heading to the end of the document, so a POS
  that runs onto a second page is covered):
    * "On ____, 2026, I served ..."              -> date
    * "Executed on ____, 2026[,] at ____, ..."   -> date (and city, if that blank exists)
    * "Name: ____"                               -> declarant
    * the signature rule directly above the declarant's name, or above "Name:",
      or a "By: ____" line followed by the declarant's name -> signature
  Translator region (only with --translator; from "DECLARATION OF TRANSLATOR" to the next
  heading or page end). Two layouts are recognised -- the firm template's, and Hernan's
  ("I, ____, declare:" ... "Printed name: ____", first met on Yi Cong 2026-10-16, where the
  old patterns silently filled nothing):
    * "On ____, 2026, I translated ..."          -> date
    * "Executed on ____, 2026, at ____, ..."     -> date + city
    * rule above "Signature of Translator"       -> signature
    * rule above "Printed Name of Translator"    -> translator's name

Never touched: the client's VERIFICATION (the client signs it), the attorney's "Dated:" and
"By:" lines (the attorney signs them), and anything outside the two regions above.

Fill method: the value is written ON the existing underscores, centred, slightly above the
baseline, so it reads as a hand-filled blank. The underscores are never removed — removing
them leaves a gap the rest of the line cannot close up (tried 2026-10-16, Jiayu Ma).

The signature lives inside the firm POS template as word/media/image1.png
(template file id 1yHMojbfNpE_C6aeZ30Td7qXypwLp0sok). This script extracts it on the fly,
so there is one source of truth for the signature.

Judicial Council forms (DISC-001, DISC-002, ...) are never stamped. Their POS belongs in the
companion attachment document, which must name the form by its full title.

Requires: pymupdf, gws on PATH.
"""
import fitz, sys, os, json, zipfile, subprocess, datetime, argparse, shutil

TEMPLATE_ID = "1yHMojbfNpE_C6aeZ30Td7qXypwLp0sok"
TNR = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
SIZE = 12
SIG_W = 115.0          # pt on the page


def signature_png(workdir):
    """Pull the firm POS template from Drive and extract the embedded signature."""
    docx = os.path.join(workdir, "_pos_template.docx")
    subprocess.run(["gws", "drive", "files", "get", "--params",
                    json.dumps({"fileId": TEMPLATE_ID, "alt": "media",
                                "supportsAllDrives": True}), "-o", docx],
                   capture_output=True, cwd=workdir)
    if not os.path.exists(docx):
        raise SystemExit("could not fetch the POS template from Drive — check the file id")
    with zipfile.ZipFile(docx) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
        if not media:
            raise SystemExit("no signature image in the POS template — ask Klaus to add it")
        png = os.path.join(workdir, "_sig.png")
        with open(png, "wb") as fh:
            fh.write(z.read(media[0]))
    os.remove(docx)
    return png


# ---------------------------------------------------------------- page geometry
def lines(pg):
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            txt = "".join(s["text"] for s in l["spans"])
            if txt.strip():
                out.append({"rect": fitz.Rect(l["bbox"]), "text": txt.strip(),
                            "base": l["spans"][0]["origin"][1]})
    return sorted(out, key=lambda x: (round(x["rect"].y0), x["rect"].x0))


def runs(pg, rect):
    """Underscore runs on one line, left to right, merged into contiguous blanks."""
    hits = sorted((r for r in pg.search_for("___") if r.intersects(rect)), key=lambda r: r.x0)
    out = []
    for r in hits:
        if out and r.x0 - out[-1].x1 < 3:
            out[-1] |= r
        else:
            out.append(fitz.Rect(r))
    return out


def write_on(pg, run, base, text):
    font = fitz.Font(fontfile=TNR)
    w = font.text_length(text, SIZE)
    x = run.x0 + max(2, (run.width - w) / 2)
    pg.insert_font(fontname="TNR", fontfile=TNR)
    pg.insert_text((x, base - 1.5), text, fontname="TNR", fontsize=SIZE, color=(0, 0, 0))


def sign_on(pg, run, sig_png, aspect):
    h = SIG_W * aspect
    pg.insert_image(fitz.Rect(run.x0 + 8, run.y1 - 1 - h, run.x0 + 8 + SIG_W, run.y1 - 1),
                    filename=sig_png, overlay=True)


def rule_above(L, i):
    for j in range(i - 1, max(-1, i - 3), -1):
        if "___" in L[j]["text"] and (L[i]["rect"].y0 - L[j]["rect"].y0) < 40:
            return L[j]
    return None


def is_heading(t):
    t = t.strip()
    return t.isupper() and len(t) > 6 and "___" not in t and not t.startswith("BY ")


# ---------------------------------------------------------------- filling
def fill_doc(d, sig_png, date, city, declarant, translator):
    with fitz.open(sig_png) as s:
        aspect = s[0].rect.height / s[0].rect.width
    log = []
    in_pos = False
    for pg in d:
        L = lines(pg)
        in_tr = False
        for i, ln in enumerate(L):
            t = ln["text"]
            if t == "PROOF OF SERVICE":
                in_pos, in_tr = True, False
                continue
            if t.startswith("DECLARATION OF TRANSLATOR"):
                in_tr = translator is not None
                continue
            if in_tr and is_heading(t):
                in_tr = False

            if in_tr:
                rs = runs(pg, ln["rect"])
                # Hernan's layout (Yi Cong, 2026-10-16): "I, ____, declare: I am fluent ..."
                # -- the translator's name sits in the first blank of the opening line.
                if t.startswith("I,") and "declare" in t and rs:
                    write_on(pg, rs[0], ln["base"], translator); log.append("translator name")
                    rs = rs[1:]
                # The date blank is on whichever line carries "I translated" -- the opening
                # line in the older layout, the next line ("Chinese. On ____, 2026, I
                # translated ...") in Hernan's. Match the phrase, not the line's first word.
                if "I translated" in t and rs:
                    write_on(pg, rs[0], ln["base"], date); log.append("translator date")
                elif t.startswith("I am fluent") and rs:
                    write_on(pg, rs[0], ln["base"], date); log.append("translator date")
                # "Executed on" can open the line or follow "foregoing is true and correct."
                elif "Executed on" in t and rs:
                    write_on(pg, rs[0], ln["base"], date)
                    if len(rs) > 1:
                        write_on(pg, rs[1], ln["base"], city)
                    log.append("translator executed")
                # Hernan's Bo Tao layout (2026-10-19): bare rule, then the translator's name
                # printed under it ("Klaus Liu") -- sign on that rule.
                elif t.strip().lower() == translator.lower():
                    r = rule_above(L, i)
                    if r: sign_on(pg, runs(pg, r["rect"])[0], sig_png, aspect); log.append("translator signature")
                elif t == "Signature of Translator":
                    r = rule_above(L, i)
                    if r: sign_on(pg, runs(pg, r["rect"])[0], sig_png, aspect); log.append("translator signature")
                elif t == "Printed Name of Translator":
                    r = rule_above(L, i)
                    if r: write_on(pg, runs(pg, r["rect"])[0], r["base"] - 1.5, translator); log.append("translator name")
                # Hernan's layout: "Printed name: ____" carries its own blank; the signature
                # goes on the bare rule directly above it (a line of underscores and nothing else).
                elif t.lower().startswith("printed name") and rs:
                    write_on(pg, rs[0], ln["base"], translator); log.append("translator printed name")
                    r = rule_above(L, i)
                    if r and r["text"].strip("_ ") == "":
                        sign_on(pg, runs(pg, r["rect"])[0], sig_png, aspect); log.append("translator signature")
                continue

            if not in_pos:
                continue
            rs = runs(pg, ln["rect"])
            if t.startswith("On ") and "served" in t and rs:
                write_on(pg, rs[0], ln["base"], date); log.append("POS served date")
            elif t.startswith("Executed on") and rs:
                write_on(pg, rs[0], ln["base"], date)
                if len(rs) > 1:
                    write_on(pg, rs[1], ln["base"], city)
                log.append("POS executed date")
            elif t.startswith("Name:") and rs:
                write_on(pg, rs[0], ln["base"], declarant); log.append("POS name")
                r = rule_above(L, i)
                if r: sign_on(pg, runs(pg, r["rect"])[0], sig_png, aspect); log.append("POS signature")
            elif t == declarant:
                r = rule_above(L, i)
                if r: sign_on(pg, runs(pg, r["rect"])[-1], sig_png, aspect); log.append("POS signature")
    return log


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--inplace", action="store_true")
    ap.add_argument("--date", default=datetime.date.today().strftime("%B %-d"))
    ap.add_argument("--city", default="City of Industry")
    ap.add_argument("--declarant", default="Klaus Liu")
    ap.add_argument("--translator", default=None)
    a = ap.parse_args()

    work = os.path.dirname(os.path.abspath(a.files[0]))
    sig = signature_png(work)
    for src in a.files:
        d = fitz.open(src)
        log = fill_doc(d, sig, a.date, a.city, a.declarant, a.translator)
        if a.inplace:
            tmp = src + ".tmp.pdf"; d.save(tmp, garbage=3, deflate=True); d.close()
            shutil.move(tmp, src); out = src
        else:
            os.makedirs(a.outdir, exist_ok=True)
            out = os.path.join(a.outdir, os.path.basename(src)); d.save(out, garbage=3, deflate=True); d.close()
        tag = ", ".join(log) if log else "no embedded POS / translator blank — skipped"
        print(f"  {os.path.basename(out)}\n      {tag}")
    os.remove(sig)
    print(f"\nDate used: {a.date}, {datetime.date.today().year} · city: {a.city}"
          + (f" · translator: {a.translator}" if a.translator else ""))
    print("Render and look at every signature page before serving.")


if __name__ == "__main__":
    main()
