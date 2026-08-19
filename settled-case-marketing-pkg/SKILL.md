---
name: settled-case-marketing-pkg
description: >
  Post-settlement MARKETING material extraction for 凌图律所 / Law Office of Shenqi Cai APC
  PI-AUTO cases. When a settled case lands in the "8. Settled" lobby, this pulls the incoming
  settlement check out of the case's Folder 6 disbursement PDF, pulls the property-damage photos
  and videos out of Folder 2, packages them into "0. Marketing/人伤/<Clients>-<M-D-YY>/", then
  files the case folder into its DOL-year folder (2024/2025/2026). Use on: "整理素材", "做 marketing
  素材", "settled case marketing", "把 X 的素材抓出来", "分类 settled 案子", "/settled-case-marketing-pkg",
  or as Step 4d chained off `accounting-agent` once a case is disbursed. PI auto ONLY — never
  dog-bite / Hernán Simó litigation. Read-mostly + safe copies; it never deletes case files.
---

# Settled-Case Marketing Package (PI auto)

Marketing (车祸部) turns these into ad creatives. They get **only** the incoming settlement check
and the property-damage media — nothing else from the case file.

> **Scope:** PI auto only. Dog-bite / Hernán Simó litigation cases do NOT get marketing packages.
> **Consent:** Klaus confirmed (2026-08-18) client consent for marketing use is covered. Still stop
> and ask if a specific case has a known confidentiality clause in its settlement agreement.

---

## Verified IDs (PI Team Folder shared drive `0ADBH3EXeXKRBUk9PVA`)

| What | ID |
|---|---|
| `8. Settled` (the lobby) | `1P35bCgC82Lh6Xftpbt03TX1Cs20G6BoB` |
| `8. Settled / 0. Marketing` | `1-Z0pzfYR_EDeO6dWH6wlGbkOd-ZtKiZu` |
| `0. Marketing / 人伤` — **SHORTCUT** | `1YjOq97wy58uhV_5QMaoOIQ0te5oHShrj` |
| ↳ **人伤 real target folder — write HERE** | `1M1yRLjQyfHUnYlCOOCAD1kOzERJ9l9-W` |
| `0. Marketing / Dashcam素材` | `1RgaAc-DYQWfLMWIo3w8loQ4_Cem1CgU7` |
| DOL-year `2024` / `2025` / `2026` | `1qEIqVZEGtWdjLh6BbVBbnZOrlezj70iz` / `11sYsUiU9ufrnFQxjHGq-5t7cUiE6YniP` / `1SqMx1OMW0QfuofQbtgpZpNvwl9irxPVX` |
| shared-drive root (for `removeParents`) | `0ADBH3EXeXKRBUk9PVA` |

⚠️ `人伤` is a **shortcut**, not a folder. Resolve it first (`fields=shortcutDetails` → `targetId`)
and create inside the TARGET. Writing to the shortcut id fails.
⚠️ The `Dashcam素材` id contains a capital **I** (`...LMWIo3w8...`), not a lowercase `l` — a
transcribed `l` 404s. Everything in `8. Settled` lives in a **shared drive**: every call needs
`supportsAllDrives:true` (+ `includeItemsFromAllDrives:true`, `corpora:allDrives` on list).

---

## What the lobby is

`8. Settled` holds four fixed folders (`0. Marketing`, `2024`, `2025`, `2026`); **everything else at
that level is an unclassified case waiting for this workflow.** `accounting-agent` Step 4 drops each
newly-disbursed case there.

---

## Steps

### 1. Pick the case, derive the naming
From the case folder name get the client(s) and the **date of loss**. Two names, two formats:

```
人伤 subfolder :  <Clients>-<M-D-YY>       e.g.  Chih-Ming Huang-12-2-25
merged PDF     :  <Clients>-<M:D:YYYY>.pdf e.g.  Chih-Ming Huang-12:2:2025.pdf
```
**Multi-client:** join the names with `-`, driver first — `Jiwen Zhang-Changming Dong-6-23-2026`.
(Drive allows `:` and `/` in names; don't "sanitize" them.)

### 2. Folder 6 → pull the SETTLEMENT CHECK page(s)
Open `6#Folder-…Checks&Invoice&Disbursements` → `<Client>-Disbursements.pdf`. It is a scanned
image-only PDF (no extractable text) — **you must look at the pages**.

Take **only the incoming settlement check**: drawn by the **insurance carrier**, payee =
`<LAW OFFICE OF SHENQI CAI APC> & <client>`. Usually page 1, sometimes pages 1–2 with its
remittance stub.

**Never include** (all of these are elsewhere in that same PDF):
- the **client-recovery check** — it prints the client's **home address**
- the disbursement letter — attorney fee / lien / net-to-client breakdown
- lien-reduction letters and provider checks — clinic names and settled lien amounts

### 3. Folder 2 → pull PD photos and videos
`2#Folder-All Photos and Videos&Police Report&Dec Page` is the **only** source for media.
Do NOT take from Folder 3 even though it is named "Property Damage Claim".

Take: vehicle-damage photos (often bundled as a `pd.pdf`) and **every video**.
Skip: `1P DL` / `2P DL` (driver licenses), `police card`, `policy dec`, insurance cards,
3P license-plate docs, message screenshots.

### 4. Build the merged PDF
`settlement check page(s)` first, then every PD photo page, in order.
```python
from pypdf import PdfReader, PdfWriter
w = PdfWriter()
w.add_page(PdfReader("disb.pdf").pages[0])        # the carrier's settlement check
for p in PdfReader("pd.pdf").pages: w.add_page(p) # PD photos
w.write("<Clients>-<M:D:YYYY>.pdf")
```
Reference for the expected result: `人伤/Cheng Peng-2-5-26/Cheng Peng-2:5:2026.pdf` (3 pages:
check + 2 damage photos).

### 5. Create the 人伤 subfolder and upload
Dedup first — list the 人伤 target and confirm no folder of that name exists; if it does, ask Klaus
before making a second one.

```bash
gws drive files create --params '{"supportsAllDrives":true}' \
  --json '{"name":"<Clients>-<M-D-YY>","mimeType":"application/vnd.google-apps.folder","parents":["<人伤 TARGET id>"]}'
```

⚠️ **Upload takes two calls.** `files create --upload` stringifies `parents`, so the file lands in
the shared-drive ROOT named "Untitled". Upload, then rename + reparent:
```bash
gws drive files create --params '{"supportsAllDrives":true}' --upload "<file>.pdf" --upload-content-type application/pdf
gws drive files update --params '{"fileId":"<id>","addParents":"<subfolder>","removeParents":"0ADBH3EXeXKRBUk9PVA","supportsAllDrives":true}' \
  --json '{"name":"<Clients>-<M:D:YYYY>.pdf"}'
```

### 6. Copy every video in
**Any** video from Folder 2 goes into the same 人伤 subfolder, as separate files alongside the PDF
(video cannot be merged into the PDF). They are already in Drive — use `files copy`
(`--json '{"name":…,"parents":[…]}'`), not a re-upload.

### 7. File the case folder into its DOL year
Material extraction done → move the case folder out of the lobby into the year matching its **date
of loss** (DOL 12/2/2025 → `2025`):
```bash
gws drive files update --params '{"fileId":"<case folder>","addParents":"<year folder>","removeParents":"1P35bCgC82Lh6Xftpbt03TX1Cs20G6BoB","supportsAllDrives":true}'
```

### 8. Verify, then log
Read back: the 人伤 subfolder holds the PDF (+ videos), the PDF page count is right, the case folder's
parent is the year folder, and **no stray "Untitled" is left in the shared-drive root**. Then append
one Activity Log row (Category `起草`/`客户`, Source `Drive`, Ref = the 人伤 folder link).

---

## Rules of thumb
- **Every** settled PI-auto case gets a package — no settlement-amount threshold.
- Never delete or move anything out of the case's own subfolders; this workflow only **copies** out.
- If Folder 6 has no disbursement PDF, or Folder 2 has no PD media, stop and tell Klaus — do not
  ship a half package.
- Marketing reaches the folder by a Drive link pasted into 车祸部-Marketing on WeChat (manual, by
  Klaus). Access is by **named account** on the shared drive — a marketing teammate who is not a
  member will get a 403 on the link.
