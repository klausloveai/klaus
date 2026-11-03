#!/usr/bin/env python3
"""Split a merged filing into upload files under a byte cap, breaking only at cover pages.

    python split_package.py <merged.pdf> <outdir> [--limit 11920000] [--front front.pdf]
                            [--max-files 15] [--client "Yuqian Tao"]

Why it measures instead of estimating: a size model built from per-page image bytes runs
about 10% low on image-heavy sections, which is exactly where the cap bites. So this proposes
boundaries from the model, then MEASURES every candidate file and repairs the ones that came
out over - handing the worst offender's tail block to its neighbour and re-measuring until
everything fits.

Structural rules it enforces, because breaking them reads as a missing exhibit:
  * a file never ENDS on a cover page (a cover orphaned from its evidence)
  * a file is never made up only of cover pages
"""
import sys, os, re, argparse

def clean_name(s):
    """USCIS accepts only letters, digits, space and _ - . ( ) in filenames."""
    return re.sub(r'\s+', ' ', re.sub(r'[^A-Za-z0-9 _\-.()]', '', s)).strip()

def main():
    import fitz
    ap = argparse.ArgumentParser()
    ap.add_argument("merged"); ap.add_argument("outdir")
    ap.add_argument("--limit", type=int, default=11_920_000)
    ap.add_argument("--front", default=None, help="PDF to lead file 1 (petition letter + index)")
    ap.add_argument("--max-files", type=int, default=15)
    ap.add_argument("--client", default="Client")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    m = fitz.open(a.merged)
    toc = m.get_toc()
    if not toc:
        sys.exit("merged PDF has no outline; cover pages must be bookmarked to split on them")
    starts = {p: (lvl, t) for lvl, t, p in toc}
    covers = sorted(starts)
    front = fitz.open(a.front) if a.front else None
    frontbytes = os.path.getsize(a.front) if a.front else 0

    def emit(rng, path):
        d = fitz.open()
        if front is not None and rng[0] == 1:
            d.insert_pdf(front)
        off = front.page_count if (front is not None and rng[0] == 1) else 0
        d.insert_pdf(m, from_page=rng[0]-1, to_page=rng[1]-1)
        sub = []
        if off:
            sub.append([1, "Petition Letter and Index of Exhibit", 1])
        for p in range(rng[0], rng[1]+1):
            if p in starts:
                lvl, t = starts[p]
                sub.append([min(lvl + (1 if off else 0), 3), t[:170], p - rng[0] + 1 + off])
        if sub:
            base = min(x[0] for x in sub); prev = 0
            for x in sub:
                x[0] = min(x[0] - base + 1, prev + 1); prev = x[0]
            d.set_toc(sub)
        d.save(path, deflate=True, garbage=4); n = d.page_count; d.close()
        return n

    def measure(rng):
        t = os.path.join(a.outdir, "_probe.pdf")
        emit(rng, t); v = os.path.getsize(t); os.remove(t); return v

    # cost model: image payload plus a flat text allowance, scaled to the real file size
    real = os.path.getsize(a.merged)
    cost = [sum(len(m.extract_image(x[0])["image"]) for x in m[i].get_images(full=True)) + 3000
            for i in range(m.page_count)]
    sc = real / max(1, sum(cost)); cost = [c * sc for c in cost]

    bnds = [c for c in covers if c > 1] + [m.page_count + 1]
    blocks = []; st = 1
    for c in bnds:
        if c > st:
            blocks.append((st, c - 1, sum(cost[st-1:c-1]))); st = c

    def pack(cap):
        out = []; s = blocks[0][0]; run = frontbytes
        for bs, be, bc in blocks:
            if run + bc > cap and bs > s:
                out.append((s, bs - 1)); s = bs; run = bc
            else:
                run += bc
        out.append((s, blocks[-1][1])); return out

    lo = int(max(b[2] for b in blocks)) + frontbytes; hi = int(real + frontbytes); best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        r = pack(mid)
        if len(r) <= a.max_files: best = (mid, r); hi = mid - 1
        else: lo = mid + 1
    ranges = best[1]

    # repair with real measurements: shrink the worst offender, hand its tail block onward
    bstart = {b[0] for b in blocks}
    for _ in range(60):
        sizes = [measure(r) for r in ranges]
        bad = [i for i, v in enumerate(sizes) if v > a.limit]
        if not bad:
            break
        i = max(bad, key=lambda k: sizes[k])
        s0, e0 = ranges[i]
        cuts = [c for c in sorted(bstart) if s0 < c <= e0]
        if not cuts:
            print(f"part {i+1} cannot be split further ({sizes[i]/1e6:.2f} MB) - "
                  f"compress harder or raise the file count", file=sys.stderr)
            break
        if i + 1 < len(ranges):
            ranges[i] = (s0, cuts[-1] - 1); ranges[i+1] = (cuts[-1], ranges[i+1][1])
        elif i > 0:
            ranges[i] = (cuts[0], e0); ranges[i-1] = (ranges[i-1][0], cuts[0] - 1)
        else:
            break

    # a cover-only part folds into the next; a part must not end on a cover
    coverset = set(covers)
    merged = True
    while merged and len(ranges) > 1:
        merged = False
        for i in range(len(ranges) - 1):
            s0, e0 = ranges[i]
            if all(p in coverset for p in range(s0, e0 + 1)):
                ranges[i:i+2] = [(s0, ranges[i+1][1])]; merged = True; break
            t = e0
            while t > s0 and t in coverset:
                t -= 1
            if t < e0:
                ranges[i] = (s0, t); ranges[i+1] = (t + 1, ranges[i+1][1]); merged = True; break

    N = len(ranges); over = 0
    for i, (s0, e0) in enumerate(ranges, 1):
        labs = []
        for p in range(s0, e0 + 1):
            if p in starts:
                mm = re.match(r'Exhibit\s+(\d+(?:-\d+)*)', starts[p][1])
                if mm: labs.append("Exhibit " + mm.group(1))
                elif "Translation Certificate" in starts[p][1]: labs.append("Translation Certificate")
        lbl = (labs[0] if len(labs) == 1 else f"{labs[0]} to {labs[-1]}") if labs else "continued"
        if i == 1 and a.front: lbl = "Petition Letter and Index of Exhibit, " + lbl
        name = clean_name(f"{a.client} - Exhibits {i} of {N} ({lbl})") + ".pdf"
        path = os.path.join(a.outdir, name)
        n = emit((s0, e0), path)
        b = os.path.getsize(path); over += b > a.limit
        print(f"  {i}/{N}  {b:>11,} B  {b/1e6:6.2f} MB  {n:4} pages  {name}")
    print(f"\nfiles: {N} | over limit: {over} | cap {a.limit:,} bytes")
    if over:
        sys.exit("some files are still over the cap - compress harder or allow more files")

if __name__ == "__main__":
    main()
