---
name: supplement-intake
description: |
  Process CLIENT-SUPPLEMENTED materials for an EXISTING 凌图律所 / Lingtu Law PI case — file the
  new images into the case folder AND fill in only the still-pending (yellow) cells of the existing
  intake sheet. Use this skill whenever a client sends follow-up / additional materials after the
  case was already set up, or when any of the following are mentioned: 补充材料, 客户补发的图,
  客人后面发的照片/证件/保险卡, supplement intake, supplemental documents, "add these to the case
  folder and update the intake sheet", "客户又发了...更新一下", "把这些补充进 [case] 的 intake".
  Typical invocation: a case name + a zip/folder of images. The skill locates the existing case
  folder + intake sheet, reads the new images, archives them into the right subfolders, and updates
  ONLY the yellow (pending) intake-sheet cells the images actually support — leaving every
  un-highlighted cell untouched, then posts a short summary to the case's Chat space. It does NOT
  send an LOR, file a claim, or touch the tracking sheet (use new-case / lor-send / file-claim for
  those). Always trigger for any "client sent more docs, update the case" request, even a partial one.
---

# Supplement Intake — Add Client Follow-up Materials to an Existing Case

A PI case rarely arrives complete. Clients drip-feed materials: the police report next week,
the other party's insurance card after they finally exchange it, scene photos once they calm
down. This skill captures the repeatable workflow for **adding those late materials to an
already-built case** without disturbing the work already done.

Two rules define the whole skill, so internalize them before anything else:

1. **Archive the new documents** into the existing case folder (same naming/placement as new-case).
2. **Resolve pending (yellow) cells, and correct confirmed-but-wrong ones.** Yellow = "still
   pending / needs attention" — fill these when the new images answer them. Un-highlighted cells
   are already human-confirmed, so you don't *speculatively* touch them — but when a supplemental
   **document clearly confirms a correction** to a non-yellow cell (e.g. the 3P driver's own DL
   shows a different address than the owner's address entered earlier), fix it (the script needs
   `"force": true`) and flag the change in your report. The bar for touching a non-yellow cell is
   *document-confirmed*, not inference.

This skill does **not** send LORs, file claims, or update the Master tracking sheet. Those are
separate, outbound, or human-gated actions — keep this skill read-mostly and safe so it can run
often and unattended. Its one hand-off is a short **note to the case's internal Chat space** on
completion (Step 7), so the team sees what was filed and where.

## Reused references (single source of truth — do not duplicate)

This skill deliberately shares the `new-case` skill's reference docs so the firm's conventions
stay in one place. Read them as needed:

- Per-document extraction rules: `~/.claude/skills/new-case/references/document-rules.md`
- File naming & folder placement: `~/.claude/skills/new-case/references/document-placement.md`
- Intake sheet value-cell map + yellow rules: `~/.claude/skills/new-case/references/cell-map.md`
- Insurance directory lookup: `~/.claude/skills/new-case/references/insurance-directory.md`
- Carrier matcher script: `~/.claude/skills/lor-send/scripts/match_carrier.py`

Bundled here:
- `scripts/update_yellow.py` — the safe intake-sheet editor (guarded-write → un-highlight policy →
  diff-verify). **⚠️ Current version talks to the Google Sheets API and only works on a NATIVE
  Google Sheet (spreadsheet ID).** Many case intakes are still **.xlsx files** (if `gws drive files
  get … alt=media` downloads it, it's an .xlsx, not a native Sheet) — on those the script throws
  `KeyError: 'sheets'`. For an .xlsx intake, use the **openpyxl safe-edit path in Step 5** instead
  (same guarantees: backup → only-named-cells → full-sheet diff). Don't free-hand openpyxl without
  the backup+diff — that guard is what makes this skill safe to run often.

## Environment notes (Cowork / macOS)

- The PI Team Folder Shared Drive is mounted locally; case folders live under:
  `~/Library/CloudStorage/GoogleDrive-<ACCOUNT>@lingtulaw.com/Shared drives/PI Team Folder/0. PI Cases/`
  — but **`<ACCOUNT>` may be `piteam@` OR `klaus@`** (the same shared drive can be mounted under
  either account's CloudStorage path). Don't hard-code one; **locate the real mount** with
  `find ~/Library/CloudStorage -maxdepth 6 -type d -iname "<Case Folder Name>"`. Editing a file in
  the mount syncs to Drive automatically — no upload step needed.
- **Mount can serve a TRUNCATED stub** (local bytes < real bytes → openpyxl `BadZipFile` / no
  End-of-Central-Directory). Verify the mounted .xlsx opens (`openpyxl.load_workbook`) before
  editing; if it fails, download full bytes via API (`xattr -p com.google.drivefs.item-id#S <file>`
  → `gws drive files get --params '{"fileId":"…","alt":"media","supportsAllDrives":true}' -o copy.xlsx`),
  edit the copy, and push it back via the Drive API rather than trusting the broken mount.
- Python deps are light: `python3 -m pip install --user --break-system-packages openpyxl pillow pypdf`
  (only install if an import fails; the Bash tool PATH is snapshotted at session start).
- `gws` is the Google Workspace CLI used for the insurance-directory sheet read.

---

## Step 1 — Locate the case folder + intake sheet (GSheet ID)

Search every case-stage subfolder (Pending / Treating / Collecting / …), not just Pending:

```bash
BASE=~/Library/CloudStorage/GoogleDrive-piteam@lingtulaw.com/"Shared drives/PI Team Folder/0. PI Cases"
find "$BASE" -maxdepth 2 -type d -iname "*<client or distinctive name>*"
```

**If zero or more than one folder matches, STOP and ask the user which case** — never guess across
cases. (Repeat clients have multiple cases with different dates of loss; the wrong folder corrupts
the wrong file.)

Once the case folder path is confirmed, get the **GSheet spreadsheet ID** via Drive API
(intake sheets are native Google Sheets, not .xlsx files):

```python
import subprocess, json

def gws(args):
    r = subprocess.run(["gws"] + args, capture_output=True, text=True)
    lines = [l for l in r.stdout.split('\n') if not l.startswith('Using')]
    return json.loads('\n'.join(lines).strip())

# Step A: find the case folder's Drive ID
case_name = "Jiachen Li-6-18-2026"   # replace with actual name
folders = gws(["drive", "files", "list", "--params", json.dumps({
    "q": f"name='{case_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
    "supportsAllDrives": True, "includeItemsFromAllDrives": True, "corpora": "allDrives",
    "fields": "files(id,name)"
})]).get("files", [])
folder_id = folders[0]["id"]   # confirm it's the right one

# Step B: find the native GSheet intake sheet in that folder
sheets = gws(["drive", "files", "list", "--params", json.dumps({
    "q": (f"'{folder_id}' in parents and name contains 'Intake Sheet' "
          f"and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"),
    "supportsAllDrives": True, "includeItemsFromAllDrives": True,
    "fields": "files(id,name,webViewLink)"
})]).get("files", [])
spreadsheet_id = sheets[0]["id"]
```

Use `spreadsheet_id` for all `update_yellow.py` calls in Step 5.

## Step 2 — Get the supplemental images

If given a zip, extract with Python `zipfile` (WeChat zips have CJK filenames that macOS `unzip`
rejects). Recover names with `raw.encode('cp437').decode('utf-8')`, falling back to `gbk`, when the
UTF-8 flag bit (`info.flag_bits & 0x800`) is unset. Skip `__MACOSX`. A plain folder of images works
too — just read them in place.

## Step 3 — Read ALL images first (vision is mandatory)

Identify every image before writing anything. Follow `document-rules.md` for per-document fields
(driver license, auto insurance card, registration, license plate, police card, health insurance,
scene/PD photos).

**Date-vs-DOL guard (critical):** check each photo's capture date (filename timestamp / EXIF) against
the case's Date of Loss (intake cell C2). When a photo was taken *after* the DOL — common, since
clients photograph things days later — its **scene location and weather are NOT accident-day evidence
and must not be written** to F2/F7/F10. Damage close-ups, IDs, registrations, and insurance cards stay
valid regardless of when they were photographed (the damage and the documents don't change).

Decide which party each document belongs to. The other party's DL + their car's insurance/registration
= **3P**; our client's own card/plate = **1P**. When the at-fault driver ≠ the registered owner / named
insured, record the driver and the policyholder separately and flag it (see cell-map).

## Step 4 — Archive into the case folder

Place files per `document-placement.md`. Combine related images into single PDFs (auto-rotate IDs and
cards upright; phone scene/damage shots are usually already upright):

- `2#Accident Info/Scene Photos.pdf` — overall scene / positions
- `2#Accident Info/Vehicle Damage Photos.pdf` — all vehicles' damage close-ups
- `2#Accident Info/3P-Driver License.pdf`, `3P-Auto Insurance Card.pdf`, `Vehicle Registration.pdf`
- `2#Accident Info/Police Card.ext` (no client-name prefix)
- Health insurance cards → `4#Bodily Injury Claim/[Client Name]/` (per-client subfolder for multi-client)

**md5-dedupe before adding** — compare new images against files already in the case folder so a client
re-sending the same photo doesn't create duplicates. If a true duplicate, skip it (or prefix
`[DUPLICATE]` only if the user wants both kept).

**Tidy naming by default.** Earlier intake passes sometimes leave documents under meaningless
auto-generated hash names (e.g. `2d70cdec….jpg`). When a new batch lets you positively identify such
a file (its md5 matches a document you just read, or you can see what it is), rename/replace it with
the convention name — and prefer a proper upright PDF over a sideways jpg. Keeping the folder
self-describing is part of the job; do it without being asked.

A small Pillow helper builds the PDFs; rotate held documents to upright (a CA DL/insurance card/
registration photographed sideways usually needs `Image.rotate(90, expand=True)` — verify by reading
the generated page, and fall back to `-90` if it comes out upside down).

## Step 5 — Update the intake sheet (only yellow cells)

This is the heart of the skill. **First decide which editor applies — native Google Sheet vs .xlsx:**

- **Native Google Sheet** (a `gws drive files get … alt=media` would fail / the file is
  `application/vnd.google-apps.spreadsheet`): use **`scripts/update_yellow.py`** (Sheets API) below.
- **`.xlsx` file** (`alt=media` downloads a real zip / mime `…spreadsheetml.sheet`): the script
  throws `KeyError: 'sheets'` — use the **openpyxl safe-edit path** further down. Most pre-litigation
  case intakes are still .xlsx, so this is the common path.

Either way the rules are identical (only yellow cells, un-highlight on confirm, full-sheet diff).

### 5a — Native Google Sheet (update_yellow.py)
First see what's pending (pass the GSheet spreadsheet ID from Step 1):

```bash
python3 ~/.claude/skills/supplement-intake/scripts/update_yellow.py list-yellow "<spreadsheet_id>"
```

This prints each yellow cell with its row label and current value. Match the new image data against
these pending cells. Run the carrier directory lookup for any newly-known insurer to fill phone /
email / fax (and the Mercury email-template special case) per `insurance-directory.md`:

```bash
gws sheets +read --spreadsheet "1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM" \
  --range "insurance list!A1:D200" --format json > /tmp/insurance_list.json
python3 ~/.claude/skills/lor-send/scripts/match_carrier.py "<insurer>" /tmp/insurance_list.json
```

Then apply edits with a JSON edit list:

```bash
python3 ~/.claude/skills/supplement-intake/scripts/update_yellow.py apply "<spreadsheet_id>" '{
  "edits": [
    {"cell":"L5","value":"Farmers Insurance Exchange"},
    {"cell":"L11","value":"B9749712"},
    {"cell":"F5","value":"Client front-left; 3P rear","keep_yellow":true}
  ]
}'
```

Rollback (if needed): open the GSheet → **File → Version history → See version history**.

### 5b — .xlsx intake (openpyxl safe-edit path)
`update_yellow.py` does NOT work here (Sheets API ≠ xlsx). Edit the **mounted** .xlsx directly
(it syncs to Drive) with the same guard the script gives — backup, named-cells-only, full diff:

1. **Locate + sanity-check** the mount (see Environment notes — account may be `klaus@` or `piteam@`;
   confirm `openpyxl.load_workbook(MNT)` succeeds, else use the API-download fallback).
2. **Detect yellow on EVERY cell, including blanks.** Yellow = `cell.fill.fgColor.rgb[-6:].upper()
   == "FFFF00"`. **A blank cell can be yellow (still-pending).** Don't only test cells that have a
   value — that was the 2026-06 miss (blank `L12`/`L16` were yellow-pending but read as "empty,
   non-yellow"). List *all* pending = blank-or-not but yellow.
3. **Back up first:** `cp` the mounted file to `~/.supplement-intake-backups/<case>-<YYYYMMDD-HHMMSS>.xlsx`.
4. **Write ONLY the named cells.** For each: `c.value=…`; `c.font=Font(name="Nunito",size=10,bold=False)`;
   `c.alignment=Alignment(horizontal="left",wrap_text=False)`. Highlight policy (same as 5a):
   - filled a **yellow pending** cell → **un-highlight** (`c.fill=PatternFill(fill_type=None)`);
   - **always-yellow review** field (F4/F5/C22/I15-16/L19-20/I24–28 …) → keep yellow
     (`PatternFill("solid", fgColor="FFFF00")`);
   - **document-confirmed** correction/fill of a **non-yellow** cell → write, leave fill as-is, and
     report it (this is the `"force"` case — bar is document-confirmed, not inference).
5. `wb.save(MNT)`.
6. **Verify = full-sheet diff vs the backup**: re-open both, assert ONLY your named cells changed
   (value *and* yellow). If any other cell drifted, restore it from the backup and re-verify. If a
   blank-yellow cell you filled is still yellow, you forgot to un-highlight it (step 4) — fix it.

A self-contained Python block doing backup→edit→diff is the right shape (see the Hong Wang
2026-06 run). Honor a **dry-run** request: do steps 1–2 and print the proposed `coord → value`
table, write nothing.

### What to fill, and the highlight policy

- **Only fill a yellow cell when the new images clearly support the value.** Leave a yellow cell
  untouched if nothing in this batch answers it — it stays pending for the next supplement.
- **Confirmed data fields → un-highlight** (the script removes the fill). These are the factual
  insurance / vehicle / driver / plate / address fields. Resolving them is the whole point of yellow.
- **Always-yellow review fields → fill but KEEP yellow** (`"keep_yellow": true`). Per cell-map these
  are judgment/tracking fields a human always re-checks: **F4** Fact of Loss, **F5** Point of Impact,
  **C22** Injuries (and passenger injury cells), **I15/I16** Claim#/PD-Adjuster, **L19/L20**
  Claim#/PD-Adjuster, and the **I24–I28** dec-page block (Dec Page / Collision Ded / Rental / Med Pay /
  UM-UIM). The directory-filled phone/email/fax (I17/I18/I22, L21/L22) un-highlight normally.
- **Inferred values → fill, but flag "inferred — confirm"** in your report. Example: reading the 1P
  license plate (I13) off the client's own scene photo when no plate document was sent. It's useful to
  capture, but the human should confirm it, so call it out rather than presenting it as documented.
- Values are English, font Nunito size 10 (not bold), left-aligned, no wrap — the script applies this.

### Critical flags to surface (from cell-map / new-case)

Same red flags apply when the new docs reveal them: 3P AIC effective date = DOL, expired AIC, named
insured ≠ driver, vehicle not on the AIC, minor client/passenger, instruction permit instead of DL,
no police report (recommend SR-1). Note them in the report — don't silently fill around them.

## Step 6 — Safety verify (mandatory)

The full-sheet diff is non-negotiable on **both** paths:
- **5a (GSheet):** `apply` re-reads the sheet and diffs against the pre-write snapshot automatically.
- **5b (.xlsx):** YOU run the diff (Step 5b.6) — re-open saved file + backup, assert only the named
  cells changed in value and yellow; restore any drifted cell from the backup.

The assertion is the same: **only the intended cells changed** (value *and* highlight). If anything
else drifted (we've seen openpyxl/Drive-sync touch an unrelated cell), restore it from the backup and
re-verify. This guarantee is why the skill is safe to run repeatedly on live case files. If the diff
is unrecoverable, stop and show the user.

## Step 7 — Post an update to the case Chat space

So the team sees the supplement was processed, post a short note to the case's Google Chat space.
**Always do this on completion** (it's the firm's expected hand-off). Use the **default** gws account
(klaus@) — it's the member of the case spaces; the piteam@ config only sees its own DM, not the named
case spaces. Find the space by matching the case folder name against each space's `displayName`, then
post the summary:

```bash
unset GOOGLE_WORKSPACE_CLI_CONFIG_DIR   # use klaus@ default; piteam@ can't see named spaces
SPACE=$(gws chat spaces list --page-all --page-limit 30 --format json | python3 -c "
import sys,json
key='<distinctive client surname, e.g. Deng>'
for line in sys.stdin:
    line=line.strip()
    if not line.startswith('{'): continue
    for s in json.loads(line).get('spaces',[]):
        if key in (s.get('displayName') or ''): print(s['name']); break
" | head -1)
gws chat +send --space "$SPACE" --text '【Claude】补充材料已归档 — <client>
• 内容：<what was filed, e.g. ER 病历 / 保险卡 / 身份证>
• 存放：<subfolder>/<filename>
• 说明：<intake 更新的关键字段 or「无待填黄格，未改动」>; <any ⚠️ flag>'
```

Keep it concise but informative — what was filed, where it's stored (subfolder + filename), the key
intake fields updated (or "no yellow cells answered"), and surface any **critical flag** (e.g.
"⚠️ minor passenger — guardian authorization needed"; "⚠️ Medi-Cal lien"). Start with `【Claude】`.
Notes:
- `gws chat +send` is the working helper — the older `gws chat spaces messages create` / `--params
  filter` syntax does **not** exist in this CLI.
- This is the skill's one outbound action; it posts only to the internal team Chat space (low risk),
  never to the client or a carrier.
- If no Chat space matches the case (new case not fully set up), skip and note it in the report —
  don't create one here.

## Step 8 — Report

Tell the user, concisely:
- **Which case** (full folder path) you updated.
- **Files archived** and where (subfolder + filename).
- **Yellow cells updated** — split into *resolved (un-highlighted)* vs *filled-but-kept-yellow*.
- **Still-pending yellow cells** that this batch couldn't answer (so the user knows what's outstanding).
- **Flags / inferred / conflicts** — anything that needs human confirmation, plus any critical flag.

Offer obvious follow-ups (e.g. "send the 3P LOR now that we have the carrier" → `lor-send`) but do not
perform them in this skill.

---

## Yellow detection note (why the script, not ad-hoc openpyxl)

Intake sheets exported from Google Sheets store the yellow highlight as ARGB **`FFFFFF00`** (alpha +
`FFFF00`), while locally-authored sheets may use `FFFF00` or `00FFFF00`. A naive `== "FFFF00"` check
silently misses the Google-exported cells and the guard fails open. `update_yellow.py` detects yellow
robustly via `rgb[-6:].upper() == "FFFF00"`, and "un-highlight" means setting the fill back to *no
fill* (which is how confirmed cells already look in these sheets). Always go through the script so this
stays correct.
