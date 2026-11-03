# Redaction (打码) — what to hide and how

Teresa's rule: **reveal as little as possible**. The post only needs to show which insurer paid, how much, and that it was paid to the firm.

## On the check — keep visible
- Insurer name / logo (e.g. "STATE FARM MUTUAL AUTOMOBILE INSURANCE COMPANY")
- Generic printed text (AUTO INJURY, "Pay to the Order of", "AUTHORIZED SIGNATURE", security-feature captions)
- The amount, words and numbers. **Reveal version only**; the cover version hides both.
- **The firm's own name**: "Lingtu Law", "Law Office of Shenqi Cai (APC)", "…, HIS/HER ATTORNEY". Never blur it.

## On the check — mosaic everything else
- Check / payment number (usually top-right), and the MICR line at the bottom if it's inside the crop
- Internal office / routing codes ("INJ E1 OFFICE PAGECNTQ.PZ6INJ", adjuster codes, "IP AND FEATURE" codes)
- Bank name, routing fraction (e.g. 56-1544/441), bank city
- Claim no., policy no., loss date, issue date
- Insured name(s), claimant name, **client name**. On the payee line blur only the client, keep "& LAW OFFICE OF SHENQI CAI APC"
- Signatures
- Tax ID, addresses (except the firm's), phone numbers, adjuster names

## Getting coordinates
1. `redact.py render check.pdf page.png`, then view `page.png`. Most PDFs are the whole letter page (stub + check). Pick the check itself as `crop` (the part with the insurer header, amount, "Pay to the order of" and signatures), usually the lower third.
2. Crop once with Pillow and **view the crop at full size** (Read the PNG). Coordinates in `pii` / `amount` / `amount_numeric` are relative to the crop. Read them off the full-size view; pad each box by ~5px.
3. Run `redact.py check`, then **view both outputs** and confirm nothing readable is left. If a box clipped a letter of client info, widen it and rerun. This self-check replaces asking Teresa.
4. If the check is only an image inside a scanned PDF page (GEICO "Detailed Payment Summary" style), apply the same rules to whatever is visible.

## Photos
- **License plates: always mosaic** (front, rear, reflections, other cars in the background).
- Faces, including people reflected in windows or paint.
- Anything with an ID number: CA Clean Air Vehicle decals, VIN plates, dealer plate frames with phone numbers, parking permits, street addresses on houses.
- Mosaic tile size scales with the box and the photo (`mosaic()` in `redact.py`), so plates in 4000px phone photos come out unreadable without resizing first. Still zoom into every plate box after redacting; a box that's too small or misplaced isn't fixed by bigger tiles.
- View each photo at full size before and after. Even a region outside Canva's visible crop gets redacted in the uploaded file, because the original goes into Canva's media library.
