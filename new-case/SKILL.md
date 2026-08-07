---
name: new-case
description: |
  Full end-to-end PI pre-litigation new-case setup for 凌图律所 (Lintu Law). Use this skill
  whenever a WeChat intake zip is uploaded and a case folder is requested, or when any of the
  following are mentioned: new case, create a case, intake zip, case folder, PI case, client
  intake, accident case, retainer, Docusign retainer, Google Drive upload for a case, add case
  to tracking sheet, create chat space for a case. This skill covers the complete workflow:
  read documents via vision → fill intake sheet → build folder structure → deliver zip → save
  intake responses zip to Folder 1 → upload to Google Drive → add case to the CM tracking
  sheet → create the Google Chat case space → create Gmail case label in team mailbox (yellow)
  → send Docusign retainer → output the client-facing signing message (last step).
  Always trigger this skill for any PI new-case / intake processing task, even if the request
  seems partial (e.g. "new case", "create a case", "process this zip", "send retainer").
---

# New Case — End-to-End PI Case Folder Skill

Full workflow for processing a WeChat PI intake export into a complete case folder,
uploading to Google Drive, tracking the case, opening the team chat space, and sending
the Docusign retainer as the final step.

## Overview of Steps

1. Extract the intake zip
2. Read ALL documents via vision (mandatory before filling any field)
3. Determine the Date of Loss (priority order)
4. Name the case folder (display + disk; driver first, then passengers)
5. Build the case folder structure (mirror the live template)
6. Fill the intake sheet from the Drive template
7. **Classify & place ALL documents into subfolders** (DL, AIC, Police Card, photos, videos)
8. Deliver the case folder zip + place "Intake Responses.zip" in 1#Legal Documents
9. Upload to Google Drive (default destination: 1. Pending)
10. Add the case to the tracking sheet, insert one row per client below the Example Row
11. Create the Google Chat case space, add the team, **promote Amos/Claire/May/CM to Manager**, ask user for case notes, post verbatim @Amos + CM
12. Create the Gmail case label in the team mailbox (yellow)
13. Send the Docusign retainer (recipients from intake; **retainer type = new / standard — mandatory gate, no default**)
14. **Output the client-facing signing message** (WeChat 文案 for Klaus to forward) — **always last**

> The 14 headings below (Step 1 – Step 14) match this list exactly.

## Execution Mode

**Run all 14 steps end-to-end by default — do NOT pause for per-step confirmation.**
When the user has not said otherwise *in advance*, apply these defaults and keep going:
- Drive destination = **1. Pending**
- Retainer = **send immediately**, recipient emails taken from the intake
- CM assignment = use the CM name given in the prompt. If **no CM name was given**,
  pause after Step 1 and ask: "这个案件 assign 给谁？（Jerry / Ryan / Amos）" — wait for
  the answer before proceeding. There is no auto-assignment.
- Chat space "in charge" = the named CM (no default — must be either in the prompt or explicitly answered)
- **Retainer type = NO DEFAULT — it is a mandatory gate. See below.**

This Execution Mode overrides any "ask the user" / "Get user confirmation" wording in the
individual steps below (except the gates noted above). The user will state any deviation —
skip a step, hold the retainer as a draft, different retainer type/CM — up front.

**Retainer FEE TYPE is a mandatory gate — ALWAYS confirm before Step 13.** There is NO default;
never infer it from a template name or from a previous case. If the prompt didn't say,
ask: "这个案子用 new 还是 standard retainer？"

| 类型 | 费用结构 | 典型适用 |
|---|---|---|
| **new** | **先付医疗费；扣除医疗费后剩余的金额，客户与律所各得一半（50%／50%）** | **小案子**：碰撞轻微、预计赔偿额低、治疗少或不治疗、走 early settlement。这类案子医疗费会吃掉赔偿的大部分，1/3 抽成对律所不划算。 |
| **standard** | **先扣律师费三分之一（1/3）**，剩余用于支付医疗费，之后余额归客户 | **常规案子**：正常伤情、要走完整治疗流程的。 |

**How to use the 典型适用 column:** reference ONLY — never an auto-rule. **Klaus judges the fee
type case by case and will state it in the prompt.** Take what he says. If he didn't say, ask
(you may attach a one-line suggestion, e.g. "撞击很轻 + 客户不打算治疗 → 建议 new，确认吗？"），
then wait. Never send on your own read alone — the fee is his business call, and similar-looking
cases can legitimately get different types.

The fee type drives BOTH the Docusign template (Step 13) AND the 费用说明 paragraph in the
client message (Step 14). They must always match — never send a `new` template with `standard`
fee wording or vice versa.

**Client count is NOT a gate — you determine it yourself** from the intake, and it selects the
Joint-Conflict vs plain variant (see the 2×2 matrix in Step 13). 1 client → plain; 2+ → Joint Conflict.

**Step 3 has a mandatory DOL confirmation gate:** after reading all documents and determining
the best-evidence Date of Loss, STOP and confirm the DOL with the user BEFORE naming the folder
(Step 4) or filling the intake sheet (Step 6). Show what the documents/form say and your proposed
DOL, then ask e.g. "这个案子的 DOL 我定为 [DATE]（依据：[police card / form-stated / …]），确认吗？".
Wait for the user's confirmation (or correction) before proceeding. This applies to EVERY case,
even when a document seems to confirm the date — the DOL drives the folder name, intake sheet,
tracking row, Chat space name, and the retainer date, so a wrong DOL is expensive to unwind.
(Rationale: WeChat→Excel exports have shifted the form-stated date by a day; the client's actual
answer is authoritative.)

**Step 11 has a mandatory pause:** after the Chat space is created and members are verified,
STOP and ask the user for their case notes before posting to Chat. The user's reply is required
input — the Chat message cannot be generated without it.

---

## Step 1 — Extract Intake Zip

```bash
unzip "/mnt/user-data/uploads/<filename>.zip" -d /home/claude/work/intake_raw/
```

Read the Excel form:
```bash
extract-text 凌图律所-车祸理赔案件信息收集表.xlsx
```

Identify all clients (driver + passengers) and their roles from the form.

> macOS note: WeChat zips have CJK filenames that `unzip` rejects ("Illegal byte sequence").
> Extract with Python `zipfile`. **Always check `info.flag_bits & 0x800` first** — if the
> UTF-8 bit is SET, use `info.filename` as-is (already UTF-8). Only when the bit is NOT set
> do the cp437 re-encode: `info.filename.encode('cp437').decode('utf-8', errors='replace')`
> (fall back to `gbk`). Calling `.encode('cp437')` on an already-UTF-8 string crashes with
> `UnicodeEncodeError` — this is the most common extraction failure.
>
> Correct extraction pattern:
> ```python
> for info in zf.infolist():
>     if info.flag_bits & 0x800:
>         name = info.filename          # already UTF-8
>     else:
>         raw = info.filename.encode('cp437')
>         try:    name = raw.decode('utf-8')
>         except: name = raw.decode('gbk', errors='replace')
>     # skip resource forks
>     if name.startswith('__MACOSX') or os.path.basename(name).startswith('._'):
>         continue
>     ...
> ```
>
> System python3 may need `python3 -m pip install --user openpyxl pillow`.

---

## Step 2 — Read All Documents (MANDATORY FIRST)

Before filling any intake sheet field, read every uploaded document image using vision.
Priority order when data conflicts: Document image → Form text → Yellow-highlight

Documents to read:
- Our Client Driver License(s) → name, DOB, address, DL#, expiry, gender, LIMITED-TERM flag
- Our Client Auto Insurance Card(s) → insurer, policy#, policyholder, vehicle, VIN, LP, period
- Other Party Driver License → name, DOB, address, DL#
- Other Party Auto Insurance → insurer, policy#, policyholder, vehicle, VIN, period, eff date
- Our Client License Plate → 1P LP#
- Other Party License Plate → 3P LP#
- Police Card → officer, badge, agency, report#, crash date/time, NCIC#
- Health Insurance Card(s) → carrier, member ID (→ Folder 4, not Folder 2)
- Scene Photos / Videos → check for phone clock visible, dashcam metadata
- PD Photos → vehicle damage

See `references/document-rules.md` for full document-specific extraction rules.

### ⚠️ Form submitter ≠ client (most common name error)

WeChat intake forms are often submitted by **someone other than the client** — the attorney,
a family member, or a paralegal using their WeChat account. The form's "Full Legal Name" field
may contain the submitter's name, NOT the client's name.

**Rule:** The DL name is authoritative for C4. If DL name ≠ form name:
- Write the DL name into C4 **without yellow** (the DL confirms it).
- Flag the discrepancy prominently in the Day 1 SOP Chat message and case report.
- Do NOT use the form name anywhere in the case folder, intake sheet, or Chat space name.
- Example: form said "Shenqi Cai" (the attorney's name) but DL/AIC/health card/registration
  all showed "Andrew Yi Chen Lin" — use the document name throughout.

### ⚠️ "Other Party License Plate" folder may contain scene photos

Clients frequently upload **scene photos** (wide-angle shots of the accident scene, the other
vehicle from a distance, or road context) into the "Other Party License Plate" folder instead
of a close-up of the actual plate.

**Rule:** Always inspect the actual image BEFORE assuming it contains a readable plate number.
- If the image clearly shows a readable plate → extract LP#, file as `3P-License Plate.jpg`
- If the image is a scene photo or the plate is not readable → classify as scene photo
  (→ `Scene Photos.pdf`), leave L17 as Pending+YELLOW
- Never fill L17 from a blurry, distant, or partially-visible plate

---

## Step 3 — Date of Loss

Priority:
1. Police card crash date
2. Medical record date of initial encounter
3. Dashcam iPhone metadata (com.apple.quicktime.creationdate)
4. TeslaCam timestamp on screen
5. Form-stated DOL (last resort — client self-reported only)

Supplementary (not standalone): WeChat filename timestamp, phone clock in scene photo.
Form submission timestamp is NEVER a valid DOL source.

### Yellow C2 rules (stricter than other fields)

- **Priority 1–4 confirms DOL, and it matches the form** → C2 **no yellow** (fully confirmed)
- **Priority 1–4 confirms DOL, but it differs from the form** → C2 **yellow** (corrected by document)
- **No Priority 1–4 evidence — using form-stated DOL (Priority 5)** → C2 **always yellow**, no exception.
  Client self-reported dates are unverified and are frequently wrong.

### Submission-date trap (most common DOL error)

Clients often fill out the form the day AFTER the accident and accidentally type today's
date (the submission date) rather than the actual accident date.

**Detection:** Note the WeChat zip filename — it contains the upload timestamp (e.g.
`凌图律所-车祸理赔案件信息收集表_20260616_143022.zip` → submitted 2026-06-16). If the
form-stated DOL matches or is 0–1 days after the zip filename date AND no Priority 1–4
document confirms it:

1. Flag C2 yellow with note: `"⚠️ Form states [DATE] — matches/near submission date [ZIP DATE]. Verify with client: was the accident the previous day?"`
2. Write the form-stated date into C2 (best available), but keep it yellow.
3. In the case assessment (Step 12 Chat message) call this out explicitly.

**Do NOT silently accept a form-stated DOL that equals the submission date as confirmed.**

---

## Step 4 — Case Folder Naming

**Display name:** `Firstname Lastname-M/D/YYYY`
**Disk name:** `Firstname Lastname-M-D-YYYY`
**Multi-client:** Driver first, then all passengers in order.

Examples:
- `Hsuan-Yun Chang-5-24-2026`
- `Hsuan-Yun Chang-Ting-Wei Chien-5-24-2026`

---

## Step 5 — Build Folder Structure

**PI Folder Template** (single source of truth for both folder structure AND intake sheet):
- **Folder:** https://drive.google.com/drive/folders/1TxojpCUHlIaO6m4m3jRjYqYDYakmunze (ID: `1TxojpCUHlIaO6m4m3jRjYqYDYakmunze`)

At the start of each case, **list the template folder to get the current subfolder structure** — do not hardcode folder names, as the template may be updated:

```bash
gws drive files list --params '{
  "q": "'"'"'1TxojpCUHlIaO6m4m3jRjYqYDYakmunze'"'"' in parents and trashed=false and mimeType='"'"'application/vnd.google-apps.folder'"'"'",
  "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives",
  "fields": "files(id,name)", "orderBy": "name"}'
```

Build the local case folder mirroring whatever subfolders the template currently contains. Also recursively list each top-level subfolder to pick up nested subfolders (e.g. `Loss of Wage Documents` and `Referral` inside `4#Bodily Injury Claim`).

**As of last check, the template contains:**
```
[Case Folder Root]/
├── 1#Legal Documents/       (template id: 1-47IZ4NRsv_suEMkrtkgD_H_WOV51-L5)
│     └── Intake Responses.zip   ← renamed original intake zip, ALWAYS present
├── 2#Accident Info/         (template id: 1oTEG5FyA6JS34iBcsQ9b10f4PZ2tqQFt)
├── 3#Property Damage Claim/ (template id: 1oWbooyhHzrrpeQJ9W94Iik9iJerQ15Lp)
├── 4#Bodily Injury Claim/   (template id: 1zBVBNg5Ayu2SmZkgBjKhyEQXw5ESUUMp)
│     ├── [Client Name]/          ← per-client subfolder (multi-client only, NOT in template)
│     ├── Loss of Wage Documents/ (template id: 1-ITJJ628o9UM3lwfggPPYCQXfVCyFlSZ)
│     └── Referral/               (template id: 1fZ1giwvsg_W6FPmzREbAXT1JDZAmLjF0)
├── 5#Demand Package/        (template id: 1I4DRX7DVTfPq_sfLcPV0cynTVxxevEFb)
├── 6#Settlement Documents/  (template id: 1SWMMs0Qsy_wz2GwldlaO9JNng-Gj-gUU)
└── [Intake Sheet].xlsx           ← in root
```

If the live query returns a different set of folders, use the live set — the template IDs above are cached references only.

**Intake Responses.zip rule:** Copy the original WeChat export zip, rename it
"Intake Responses.zip", and place it in `1#Legal Documents` for every case.

See `references/document-placement.md` for full file naming and placement rules.

---

## Step 6 — Fill Intake Sheet

**Always download a fresh copy of the template from Google Drive — never use a local cache.**
The canonical template is a Google Sheets file in the PI Folder Template folder:

- **Template folder:** https://drive.google.com/drive/folders/1TxojpCUHlIaO6m4m3jRjYqYDYakmunze
- **Template file ID:** `1Lnp8oMj3D3k9rKAYPCSIGCndBKR1ztt3-u8Qe53QKMM` (Google Sheets — "Intake Sheet Template")

Export as xlsx at the start of each case:
```bash
gws drive files export \
  --params '{"fileId":"1Lnp8oMj3D3k9rKAYPCSIGCndBKR1ztt3-u8Qe53QKMM","mimeType":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}' \
  -o "/Users/Klaus/work/[CaseName] Intake Sheet.xlsx"
```

Open the exported file with `openpyxl(data_only=False)`. **Write only to VALUE cells — never overwrite labels or change the template structure/formatting.**

**Global write rules:**
- Font: Nunito, size 10, not bold
- Alignment: left, no wrap
- Values in English, EXCEPT where cell-map says to keep the client's original wording (e.g. F11 Purpose of Trip)
- Yellow: `PatternFill("solid", fgColor="FFFF00")`
- After saving: verify yellow by checking `fgColor.rgb` in `("FFFF00", "00FFFF00")`

See `references/cell-map.md` for the complete value cell map and yellow rules.
**Read the 「填写总原则」 section at the top of cell-map.md before writing anything** — the sheet
records the CLIENT'S STATEMENT verbatim, not case analysis. No rewriting, no recommendations,
no legal characterization, no ⚠️ flags inside cells.

### ⚠️ Two mandatory gates — 防止「值填错栏」

This has caused real errors (I7 Policyholder ← policy period; I8 Driver ← named insured;
L12 Driver Phone ← address; F12 Child Seat ← the "did you see it coming" answer). The root
cause was writing a hardcoded list of cell addresses from memory of the template layout,
without ever comparing the intended field against that cell's actual label.

**Gate 1 — address cells BY LABEL, not by remembered row number.**
Before writing, read the label column (B / E / H / K / X / AA) and build a `label → cell` map,
then write by field name:
```python
labels = {str(ws[f"B{r}"].value).split("\n")[0].strip(): f"C{r}"
          for r in range(1, 75) if ws[f"B{r}"].value}
def put(field, value, yellow=False):
    cell = labels[field]           # KeyError if the label doesn't exist → fails loudly
    ...
put("Policyholder", "Yujing Zhou")
put("Policy Period", "03/22/2026-09/22/2026")
```
A shifted row or a template revision then raises instead of silently writing into the
neighbouring field.

**Gate 2 — run the type self-check after saving. REQUIRED, not optional.**
```bash
python3 ~/.claude/skills/new-case/scripts/verify_intake.py \
  "<path>/<Case> Intake Sheet.xlsx" --client-name "<Driver Name>"
```
It pairs every value with its label and asserts the value's TYPE matches the field
(Phone→phone number, Period→date range, Policyholder/Driver/Owner→person name, VIN→17 chars,
Email→has @, 1P Driver→must be our client), and flags values that smuggle in analysis.
**Exit code 2 = ERRORs present → fix and re-run before uploading to Drive.**
WARNs are advisory; review each one.

**Re-filling an existing case's sheet** (rules changed, or fixing an earlier fill): download the
live Drive copy first and diff it cell-by-cell against your new version before uploading.
Other skills write real progress into this sheet after intake (e.g. `exer-lien` fills C20
UrgentCare with the booked appointment) — never let an initial-fill default overwrite a fact
that already happened. See 「既成事实不被初填规则覆盖」 in cell-map.md.

### Sub-step 6a — Insurance Directory Lookup

Run this **after** writing I5 (1P insurer) and L5 (3P insurer) to the sheet.
Full rules in `references/insurance-directory.md`.

```bash
# 1. Fetch insurance list once (cache for both 1P + 3P)
gws sheets +read \
  --spreadsheet "1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM" \
  --range "insurance list!A1:D200" \
  --format json > /tmp/insurance_list.json

# 2. Match each insurer
python3 ~/.claude/skills/lor-send/scripts/match_carrier.py \
  "<1P insurer name>" /tmp/insurance_list.json
# → {"matched": "...", "fax": "+1XXXXXXXXXX", "email": "..."}
```

**If matched — fill these cells (no yellow):**

| 1P cell | 3P cell | Value |
|---|---|---|
| I17 | L21 | Phone Number from directory |
| I18 | L22 | Email from directory (see Mercury below) |
| I22 | *(none)* | LOR Fax Number from directory |

**Mercury Insurance special case (detected when `matched` contains "mercury"):**
- Phone/fax fill normally.
- Email → check I15 (1P) or L19 (3P) for claim#:
  - Claim# known → `MyClaim+CAPA-XXXXXXXX@mercuryinsurance.com` (no yellow)
  - Claim# "Pending" → `MyClaim+[CLAIM#]@mercuryinsurance.com` + **yellow**

**If no match or directory read fails:**
- I17 / I18 / L21 / L22 → leave as `"Pending"+yellow` (unchanged — adjuster contact is truly pending)
- **I22 (1P fax) → leave BLANK, no yellow** — there is no "pending fax" state; if we don't have a
  directory fax number, the cell should be empty, not pending. LOR fax is only filled when we have
  a confirmed number from the directory.
- Note in output summary: "no directory match for [insurer name] — add to insurance list."

---

## Step 7 — Classify & Place Documents into Subfolders

**MANDATORY — do not skip.** Every document extracted from the intake zip must be classified
and copied/renamed into the correct case subfolder before packaging or uploading. Failing to
do this step means the case folder is empty and unusable for the CM.

See `references/document-placement.md` for the full naming and placement rules. Summary:

### Destination: `2#Accident Info/`
| Source | Saved as |
|---|---|
| Client Driver License image | `Firstname Lastname-Driver License.ext` |
| Client Auto Insurance Card image | `Firstname Lastname-Auto Insurance Card.ext` |
| Police Card image | `Police Card.ext` (no client name prefix) |
| All PD (vehicle damage) photos | Combined → `Vehicle Damage Photos.pdf` |
| All on-scene/context photos | Combined → `Scene Photos.pdf` |
| Videos | `Scene Video 1.mp4`, `Scene Video 2.mp4`, … (copy as-is) |
| 3P DL image | `3P-Driver License.ext` |
| 3P AIC image | `3P-Auto Insurance Card.ext` |
| License plate photos (1P/3P) | `1P-License Plate.ext` / `3P-License Plate.ext` |

### Destination: `4#Bodily Injury Claim/`
| Source | Saved as |
|---|---|
| Health Insurance Card | `Firstname Lastname-Health Insurance Card.ext` |

### Destination: `1#Legal Documents/`
| Source | Saved as |
|---|---|
| Original intake zip | `Intake Responses.zip` |

### DNG raw photo conversion (iPhone Pro / iOS 16+)

iPhones in Pro RAW mode save `.dng` files. Pillow cannot open DNG directly — it will raise
`UnidentifiedImageError`. Convert to JPEG first using macOS's `sips` (always available, no install):

```bash
sips -s format jpeg "input.dng" --out "output.jpg"
```

Batch-convert all DNG files before building PDFs:
```python
import subprocess, os
for f in photo_files[:]:
    if f.lower().endswith('.dng'):
        jpg = f[:-4] + '.jpg'
        subprocess.run(['sips', '-s', 'format', 'jpeg', f, '--out', jpg], check=True)
        photo_files[photo_files.index(f)] = jpg
```

### Combining images into PDF
Use Python Pillow (`PIL.Image`) to combine multiple photos into a single PDF:
```python
from PIL import Image
imgs = [Image.open(f).convert('RGB') for f in photo_files]
imgs[0].save("Vehicle Damage Photos.pdf", save_all=True, append_images=imgs[1:])
```

**Key rules:**
- Always exclude macOS resource fork files (`._*`) when listing files — filter with
  `not f.startswith('._')` before processing.
- PD photos (close-up damage) → `Vehicle Damage Photos.pdf`
- Scene photos (context, location, police on-scene, tow trucks) → `Scene Photos.pdf`
- Videos are scene videos unless timestamps/metadata confirm dashcam → `Dashcam Video N.mp4`
- If a photo could be either PD or scene, prefer putting full-scene context shots in
  `Scene Photos.pdf` and close-up damage shots in `Vehicle Damage Photos.pdf`
- Do NOT label damage photos "1P-Vehicle Photo" — just `Vehicle Damage Photos.pdf`
- Check for duplicate files (identical content) before combining — skip duplicates
- Any unidentifiable document → place in case folder root

---

## Step 8 — Deliver Zip + Intake Responses

```bash
# Copy intake zip into Folder 1 renamed
cp "/mnt/user-data/uploads/<original>.zip" \
   "/home/claude/work/[CaseName]/1#Legal Documents/Intake Responses.zip"

# Package case folder
cd /home/claude/work
zip -r "/mnt/user-data/outputs/[CaseName].zip" "[CaseName]/"
```

Present the zip. Then provide the output summary (see `references/summary-format.md`).

---

## Step 9 — Google Drive Upload

**Default destination: always the "1. Pending" folder** — a new case always goes to Pending.
Do NOT ask; upload there automatically and tell the user where it went. Only use a different
folder if the user explicitly names one.

**PI Team Folder Shared Drive:** driveId `0ADBH3EXeXKRBUk9PVA`
**"1. Pending" folder ID:** `1PDbkMUmeNBBZ338kolSM-UggkmTqUFcQ`
**PI Folder Template:** `1TxojpCUHlIaO6m4m3jRjYqYDYakmunze` (use to replicate structure in Drive)

### Preferred method — copy via mounted Drive + immediate API parallel

The piteam@ Shared Drive is mounted locally, but the **mount path has a timestamp suffix** that
changes each session (e.g. `GoogleDrive-piteam@lingtulaw.com - (6-20-26 1:49 AM)`). The suffix
also contains a Unicode narrow no-break space (` `). **Never hardcode the path** — use glob:

```python
import glob, os
mounts = glob.glob(os.path.expanduser(
    '~/Library/CloudStorage/GoogleDrive-piteam*'))
# mounts[0] is the actual path; then append the rest:
pending = os.path.join(mounts[0], 'Shared drives/PI Team Folder/0. PI Cases/1. Pending/')
```

Copy the local case folder to the mount for background sync. **At the same time**, immediately
create the case folder and all subfolders via the Drive API — do NOT wait for the mount to sync.
This is necessary because mount sync of large files (DNG photos, videos, or large ZIPs >50MB)
can take 5–30+ minutes before the Drive API sees them, and subsequent steps need the folder IDs.

**Parallel strategy (always use this for new cases):**

1. **Copy to mount** (background sync; gets files into Drive eventually):
   ```bash
   cp -R "/Users/Klaus/work/[CaseName]" "$PENDING_MOUNT/"
   ```

2. **Immediately create case folder via API** (no waiting; gives instant folder ID):
   ```bash
   gws drive files create \
     --json '{"name":"[CaseName]","mimeType":"application/vnd.google-apps.folder","parents":["1PDbkMUmeNBBZ338kolSM-UggkmTqUFcQ"]}' \
     --params '{"supportsAllDrives":true,"fields":"id,name,webViewLink"}'
   ```
   Capture `id` as `CASE_FOLDER_ID`.

3. **Create subfolders via API** (one call per subfolder, using `CASE_FOLDER_ID` as parent):
   Replicate the same subfolder structure built locally. Capture each subfolder ID.

4. **Upload intake sheet `.xlsx` via API** immediately — this gives you the `webViewLink` for Step 10:
   ```bash
   gws drive files create \
     --upload "/Users/Klaus/work/[CaseName]/[CaseName] Intake Sheet.xlsx" \
     --upload-content-type "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
     --json '{"name":"[CaseName] Intake Sheet.xlsx","parents":["<CASE_FOLDER_ID>"]}' \
     --params '{"supportsAllDrives":true,"fields":"id,name,webViewLink"}'
   ```

5. **Upload all other files to their respective API-created subfolders** (small files sequentially;
   large files — ZIPs, DNG, videos >20MB — in parallel background processes):
   ```bash
   # Large files in parallel
   gws drive files create --upload "file1.zip" ... & \
   gws drive files create --upload "video.mov" ... & \
   wait
   ```

6. **Delete the mount copy** once API uploads are confirmed complete (prevents duplicates):
   ```bash
   rm -rf "$PENDING_MOUNT/[CaseName]"
   ```

**Fallback — if mount not found at all:**
Skip steps 1 and 6; proceed directly with API-only upload (steps 2–5).

**NEVER use `gws drive +upload`** — the `+upload` helper does NOT pass `supportsAllDrives`,
so it returns HTTP 404 on Shared Drives. Always use `files create` with `supportsAllDrives:true`.

**Capture the intake sheet `webViewLink`** from step 4 — this URL is used in Step 10
for the tracking-sheet `=HYPERLINK(...)` formula.

---

## Step 10 — Add Case to Tracking Sheet

After the Drive upload (Step 9), add the case to the **PI Master Sheet** tracking Google Sheet.
Insert one row per client (driver first, then passengers) directly below the Example Row (row 2).

> 🔒 **Row 1 (header) and Row 2 (Example Row) are PERMANENT, FIXED TEMPLATES — never move, overwrite,
> or write into them.** Every new case ALWAYS goes to **row 3 and below**. The mechanic is fixed:
> **insert N blank rows immediately below row 2 → copy row 2 down into them → fill the NEW rows starting
> at row 3.** The driver goes to **row 3**, passengers to rows 4, 5, … So `insertDimension` uses
> `startIndex: 2` (0-based index 2 = spreadsheet row 3, which keeps rows 1–2 above it untouched), and
> the value-writes target **A3/B3/C3…**, NEVER A2/B2. If you ever find yourself writing to row 2, STOP —
> that is the Example Row and you are corrupting the template (this has caused real breakage on
> multi-client cases where the driver was written to row 2 and pushed the Example Row down).

**Spreadsheet:** "PI Master Sheet" — ID `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`
**CM tabs:** Jerry → `Piteam@` (sheetId `102974151`), Ryan → `Picase@` (sheetId `775230687`), Amos → `Claims(Amos)`.
Always read the live header row (row 1) to map columns — never hardcode the order.

**Picase@ confirmed column layout (A–X):** DOL · Client Name · **Retainer** · Referrer · Case Status · Note-Claims · 1LOR · 1Coverage · 1Liability · 3LOR · 3Coverage · 3Liability · Property Damage · Ambulance · Emergency · Urgent Care · Primary Doctor · Medi-Cal · Medicare · Health Ins Lien · Outstanding Balance · Note-Treatment · Chiropractic · MRI

> ⚠️ **Layout changed 7/25/2026** — a **Retainer** column was inserted at **C**, shifting every
> later column one to the right (Referrer C→D, Case Status D→E, Note E→F, the 1LOR→Property-Damage
> block F–L→G–M, the clinical block M–S→N–T). The clinical tail was also renamed/extended
> (…Medicare(S) · Health Ins Lien(T) · Outstanding Balance(U) · Note-Treatment(V) · Chiropractic(W) · MRI(X)).
> **Always read the live header row (row 1) and map by column NAME, not by a memorized letter** — the
> layout may shift again. The letters below are the current (post-7/25) mapping.

### Retainer column (C) — NEW

Record the retainer version the client signed. Klaus states the fee type up front (the Step 13
gate), so map it directly:

| Step 13 fee type | Write in col C |
|---|---|
| **standard** (先扣 1/3 律师费) | `Standard 1/3` |
| **new** (先付医疗费 → 剩余 50/50) | `New 50%` |

Driver row only (it's the case's primary record row). Leave passenger rows blank — one retainer
entry per case.

### Per-client row format

| Column | Driver row | Passenger row |
|---|---|---|
| DOL (A) | Date of Loss (M/D/YYYY) | leave blank |
| Client Name (B) | `=HYPERLINK("<intake sheet webViewLink>","Firstname Lastname")` — name only, no CM tag | plain text `"Firstname Lastname"` — **no hyperlink, no CM tag, no "(minor)" tag** |
| Retainer (C) | `Standard 1/3` or `New 50%` (per table above) | leave blank |
| Referrer (D) | leave blank (Klaus fills manually) | leave blank |
| Case Status (E) | `✒️Signing` (from template) | `✒️Signing` (from template) |
| Note-Claims (F) | `Retainer sent M/D` | same text + same blue formatting (keep from template copy; see background rule below) |
| 1LOR → Property Damage (cols G–M) | keep Example Row values — do not override | **EMPTY** — clear all 7 cells; one case only needs one primary record row |
| Ambulance → Health Ins Lien (cols N–T) | **keep Example Row template values (P / Pending) — do NOT pull from intake** | keep Example Row template values |
| Outstanding Balance → MRI (cols U–X) | keep Example Row values | keep Example Row values |

> ⚠️ **Policy (7/26/2026): do NOT populate the clinical/status columns from the intake.** When
> adding a new case, copy the template down from row 2 and leave **everything at default** except:
> DOL (A), Client Name (B), Retainer version (C), and Note-Claims (F) = `Retainer sent M/D`. The
> clinical/liability columns — 1LOR→Property Damage (G–M) and Ambulance→Health Ins Lien (N–T) —
> stay at their template `P`/`Pending` defaults; **the assigned CM follows up and confirms each
> later.** This replaces the earlier behavior of writing Ambulance/Emergency/Urgent Care/…/Health
> Ins from the intake sheet — no longer do that.

**Passenger row background rule — three zones:** A–E clear to white; F (Note-Claims) untouched (keep template blue); G–M clear to white (empty cells, no color); N–X untouched (keep template yellows). See step 6 below for the exact `repeatCell` calls.

### Workflow

1. Match CM to tab: Jerry → `Piteam@`, Ryan → `Picase@`, Amos → `Claims(Amos)`.
2. **Read header row (row 1) and Example Row (row 2)** from the CM tab. Confirm client not already present (avoid duplicates).
3. **Insert N blank rows immediately below the Example Row** using `insertDimension` with
   `inheritFromBefore: true`. `startIndex: 2` is a 0-based index = spreadsheet **row 3**, so rows 1
   (header) and 2 (Example Row) stay put and the N new rows appear at rows 3 … 2+N:
   ```json
   {"insertDimension": {
     "range": {"sheetId": <id>, "dimension": "ROWS", "startIndex": 2, "endIndex": 2+N},
     "inheritFromBefore": true
   }}
   ```
4. **Copy Example Row (row 2) into every new row** using `copyPaste PASTE_NORMAL` from `A2:X2`
   (24 columns, index 0–23 — re-check the live header width, the table now runs A–X):
   ```json
   {"copyPaste": {
     "source":      {"sheetId": <id>, "startRowIndex": 1, "endRowIndex": 2, "startColumnIndex": 0, "endColumnIndex": 24},
     "destination": {"sheetId": <id>, "startRowIndex": 2, "endRowIndex": 2+N, "startColumnIndex": 0, "endColumnIndex": 24},
     "pasteType": "PASTE_NORMAL"
   }}
   ```
5. **Write case-specific values** (`valueInputOption: USER_ENTERED`) — **the first new row is ROW 3.
   Driver → row 3; passengers → rows 4, 5, … Never write to row 1 or row 2.** (For a single-client
   case that means everything goes to row 3; for a 3-client case, rows 3, 4, 5.)
   - **Driver row (row 3):** DOL (col A → `A3`), `=HYPERLINK(url,"Firstname Lastname")` (col B → `B3`),
     Retainer label (col C → `C3` — `Standard 1/3` or `New 50%`). **Do NOT write the clinical columns N–T** —
     they stay at the template `P`/`Pending` defaults for the CM to confirm later. (Note-Claims col F is set to
     `Retainer sent M/D` in step 7, after the retainer is confirmed sent.)
   - **Passenger rows (row 4 onward):** plain text `"Firstname Lastname"` (col B — no hyperlink); clear cols G–M (write 7 empty strings);
     cols N–T keep template values (already from copyPaste — do not overwrite); col C (Retainer) and col F (Note) keep as-is from copyPaste.
   - **Cols U–X (Outstanding Balance → MRI):** leave exactly as copied from Example Row.

   > ⚠️ **Case Status (col E) must NOT be written as empty string.** When building the values array
   > for the batchUpdate, omit column E entirely — or write `"✒️Signing"` explicitly. If you pass
   > `""` for E, it overwrites the template value that `copyPaste` set. The same applies to cols
   > N–X — never include them in the values write even as placeholders.
   >
   > Safest pattern: write only the columns you're actually changing (A, B, C for driver;
   > B, G–M for passenger). Do not write a full A–X row with empty strings for the untouched columns.
6. **Background rules for passenger rows — three zones:**
   - **A–E (indices 0–5): clear to white** — removes any inherited driver-row highlight (DOL, Client, Retainer, Referrer, Case Status)
   - **F (index 5): do NOT touch** — Note-Claims column blue must be preserved from template copy
   - **G–M (indices 6–12): clear to white** — these cells are empty (no values, no color)
   - **N–X (indices 13–23): do NOT touch** — keep template yellows exactly

   Issue two separate `repeatCell` requests:
   ```json
   {"repeatCell": {
     "range": {"sheetId": <id>, "startRowIndex": 3, "endRowIndex": 2+N, "startColumnIndex": 0, "endColumnIndex": 5},
     "cell": {"userEnteredFormat": {"backgroundColor": {"red": 1, "green": 1, "blue": 1}}},
     "fields": "userEnteredFormat.backgroundColor"
   }},
   {"repeatCell": {
     "range": {"sheetId": <id>, "startRowIndex": 3, "endRowIndex": 2+N, "startColumnIndex": 6, "endColumnIndex": 13},
     "cell": {"userEnteredFormat": {"backgroundColor": {"red": 1, "green": 1, "blue": 1}}},
     "fields": "userEnteredFormat.backgroundColor"
   }}
   ```
7. **After Step 13 (retainer confirmed sent):** update the Note-Claims column (**col F**) for all client rows to `"Retainer sent M/D"`.
8. **Confirm:** report the row values and verify the Client Name formula links to the intake sheet.

---

## Step 11 — Create the Google Chat Case Space

After the case is on the tracking sheet (Step 10), open the team chat space for the case.

> **Auth: ALWAYS use the default `gws` command (Klaus@ account) for ALL Chat API calls in this step.**
> Never pass `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` or any picase@/piteam@ config override here.
> Klaus@ is the space creator/owner; other team mailboxes are added as members, not as callers.

**Naming:** space `displayName` = **case name + `(<CM initial>)` suffix**, e.g.
`Qingshun Liu-5-25-2026(A)`. The CM is already known by this point — it's a mandatory gate at
Step 1 (see Execution Mode), so **do NOT ask "who is in charge" here**; just use the assigned CM.

**Members = BASE (always, every case) + CM-specific additions. Calling user (Klaus) added automatically as owner.**

**BASE (all cases — 5 people):** `cassie@lingtulaw.com`, `amos.f@lingtulaw.com`, `claire.f@lingtulaw.com`, `may.z@lingtulaw.com`, `jessie.l@lingtulaw.com`

> `joe@lingtulaw.com` was removed from BASE on 8/7/2026 — no longer added to any new-case space.

> `jessie.l@` is in BASE for **every** case (added 7/23/2026) — she is on all case spaces so she
> ramps up faster. She is a plain **Member**, not a Manager.

**CM-specific additions:**
- **Ryan cases (Picase@):** + `ryan.w@lingtulaw.com`, `tiana.d@lingtulaw.com`, `angelina.m@lingtulaw.com`
- **Jerry cases (Piteam@):** + `jerry.p@lingtulaw.com`, `tiana.d@lingtulaw.com`, `angelina.m@lingtulaw.com`
  (i.e. SAME full member set as a Ryan case — just swap `jerry.p@` in for `ryan.w@`; everyone else identical)
- **Amos cases (Claims@):** no additions (Amos already in BASE)
- **Klaus cases (Claims@):** no additions

**CM suffix in space name:** Jerry → `(J)`, Ryan → `(R)`, Klaus → `(K)`, Amos → `(A)`.

### Workflow

0. **Check for an existing space first (duplicate prevention).** Before creating, list spaces
   and filter by displayName to avoid building a second space on retry:
   ```
   gws chat spaces list --params '{"pageSize":100}' 2>&1 | \
     python3 -c "
   import sys, json
   data = '\n'.join(l for l in sys.stdin if not l.startswith('Using'))
   spaces = json.loads(data).get('spaces', [])
   target = '<CASE_DISPLAY_NAME>'
   match = next((s for s in spaces if s.get('displayName','').strip() == target), None)
   print(match['name'] if match else 'NOT_FOUND')
   "
   ```
   - If result is `NOT_FOUND` → proceed to create below.
   - If result is `spaces/XXXX` → **skip creation**, use that existing space. Add any missing
     members individually with `gws chat spaces members create` (the API silently ignores
     members already present), then post the opening message. Do not create a second space.

1. **Create the space** with `spaces create`, then **add each member individually** with separate
   `spaces members create` calls. Do NOT use `spaces setup` — it fails silently and leaves members
   missing without any error.

   ```bash
   # Step 1a: create the space
   gws chat spaces create \
     --params '{"requestId":"<case-slug-for-idempotency>"}' \
     --json '{"displayName":"<case name>(CM_INITIAL>","spaceType":"SPACE"}'
   # Capture: spaces/XXXX and spaceUri

   # Step 1b: add each member individually (run in parallel or sequentially)
   for EMAIL in cassie@lingtulaw.com amos.f@lingtulaw.com \
                claire.f@lingtulaw.com may.z@lingtulaw.com jessie.l@lingtulaw.com; do   # + CM additions
     gws chat spaces members create \
       --params '{"parent":"spaces/XXXX"}' \
       --json "{\"member\":{\"name\":\"users/$EMAIL\",\"type\":\"HUMAN\"}}"
   done
   ```

2. **Verify member count after adding.** List the space members and confirm all expected
   members are present. If any are missing (due to silent API failure), add them again:
   ```bash
   gws chat spaces members list --params '{"parent":"spaces/XXXX"}' 2>&1 | \
     python3 -c "
   import sys, json
   data = '\n'.join(l for l in sys.stdin if not l.startswith('Using'))
   members = json.loads(data).get('memberships', [])
   print(f'Members: {len(members)}')
   for m in members:
       print(' -', m.get('member',{}).get('name','?'))
   "
   ```
   **Expected totals (BASE 5 + CM additions + Klaus as owner):**

   | Case | Members added | Total incl. Klaus |
   |---|---|---|
   | **Ryan** | BASE 5 + ryan.w + tiana.d + angelina.m | **9** |
   | **Jerry** | BASE 5 + jerry.p + tiana.d + angelina.m | **9** |
   | **Amos** | BASE 5 (Amos already in BASE) | **6** |
   | **Klaus** | BASE 5 | **6** |

   If the count is short, add the missing members with another `members create` call.

3. **Promote to Manager — ALWAYS. Amos, Claire, May, and the assigned CM get the Manager role.**
   Everyone else stays a plain Member. Do this after the members are verified, before posting.

   > ⚠️ **API role names do NOT match the UI labels:**
   > | Chat UI | API `role` |
   > |---|---|
   > | Owner | `ROLE_MANAGER` |
   > | **Manager** | **`ROLE_ASSISTANT_MANAGER`** ← this is the one to set |
   > | Member | `ROLE_MEMBER` |
   >
   > Setting `ROLE_MANAGER` would make them a co-OWNER — wrong. Always use
   > `ROLE_ASSISTANT_MANAGER`.

   Patch each one by their numeric member id (from the `members list` in step 2, or a
   `members get` by email). The call is idempotent — safe to re-run.

   ```bash
   # promote list = amos.f + claire.f + may.z + the assigned CM (skip duplicates when CM is Amos)
   for EMAIL in amos.f@lingtulaw.com claire.f@lingtulaw.com may.z@lingtulaw.com <CM_EMAIL>; do
     MID=$(gws chat spaces members get --params "{\"name\":\"spaces/XXXX/members/$EMAIL\"}" 2>&1 \
       | grep -v '^Using' | python3 -c "import sys,json;print(json.load(sys.stdin)['member']['name'].split('/')[-1])")
     gws chat spaces members patch \
       --params "{\"name\":\"spaces/XXXX/members/$MID\",\"updateMask\":\"role\"}" \
       --json '{"role":"ROLE_ASSISTANT_MANAGER"}'
   done
   ```

   **Verify** by re-listing and confirming the four show `ROLE_ASSISTANT_MANAGER`
   (Klaus will show `ROLE_MANAGER` as the space owner — that is correct, leave it):
   ```bash
   gws chat spaces members list --params '{"parent":"spaces/XXXX"}' 2>&1 | grep -v '^Using' | \
     python3 -c "
   import sys, json
   for m in json.load(sys.stdin).get('memberships', []):
       print(m.get('member',{}).get('name'), m.get('role'))
   "
   ```

4. **Resolve user IDs for the @mentions — always two lookups:**
   - **Amos** (always, supervisor): `gws chat spaces members get --params '{"name":"spaces/<SPACE>/members/amos.f@lingtulaw.com"}'`
   - **Assigned CM** (if different from Amos): same call with the CM's email.
   Both return `member.name` = `users/<numericId>`.

5. **PAUSE — ask the user for their case notes.** After the space is created and all members are verified,
   stop and prompt the user:
   > "Chat 空间已建好，请留言你对这个案子了解的信息，我会原话复制粘贴 @Amos + @CM。"
   Wait for the user's reply before posting anything.

6. **Post the user's text verbatim** — prepend the @mentions, then paste the user's exact words
   unchanged. Use Python `json.dumps()` to encode the message body:
   ```python
   import json, subprocess
   user_notes = "<user's verbatim reply — do NOT edit, translate, or reformat>"
   msg = {"text": f"<users/AMOS_ID> <users/CM_ID> new case\n\n{user_notes}"}
   subprocess.run(["gws", "chat", "spaces", "messages", "create",
     "--params", '{"parent":"spaces/XXXX"}',
     "--json", json.dumps(msg, ensure_ascii=False)])
   ```
   Verify the response `annotations` contain `USER_MENTION` entries for each @mentioned person.
   **Do NOT add, edit, translate, or reformat the user's text in any way.**

7. **Set the ⚠️ `:warning:` space emoji avatar — MANUAL.** The Chat API Space resource has no
   avatar/emoji field, so this can't be set via API. Give the user the `spaceUri` and tell them
   to set it once in the UI (Space details → emoji → `:warning:`).
8. **Confirm:** report the space name, link (`spaceUri`), members added (verified count), and the posted mention.

### Auth note (Chat scopes)
All Chat calls use the **default `gws` (Klaus@ account)** — never picase@/piteam@ config dir.
Klaus@ needs `chat.spaces`, `chat.messages`, `chat.memberships`. The interactive
`gws auth login` scope **picker omits Chat**, and `--full` / `--services` do not include it.
Re-authenticate with explicit scope URLs (which bypass the picker), e.g. run a small script:
```
gws auth login --scopes \
https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/spreadsheets,\
https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/calendar,\
https://www.googleapis.com/auth/documents,https://www.googleapis.com/auth/presentations,\
https://www.googleapis.com/auth/tasks,https://www.googleapis.com/auth/chat.spaces,\
https://www.googleapis.com/auth/chat.messages,https://www.googleapis.com/auth/chat.memberships
```
Then open the printed URL in a browser and complete sign-in. (Note: `gws auth login` REPLACES
the granted scope set, so always include Drive/Sheets/etc. alongside the Chat scopes.)

---

## Step 12 — Create Gmail Case Label (Yellow)

After the Chat space is created, create a case label in the **team mailbox that owns the case**
and color it the firm's standard yellow (#fbe983).

### Label name

Use the **client name(s) only — no date.** Driver first, then passengers, separated by `/`:
- Single client: `Mingshan Ji`
- Multi-client: `Fan Bi/Yilin Yuan`

Per convention, one label per case — never separate labels per client. Before creating, list
existing labels and reuse if found (same name, possibly wrong color → patch the color).

### Color

Gmail's "banana yellow": `backgroundColor = #fbe983`, `textColor = #594c05`.
This matches Gmail's built-in yellow preset (RGB 251, 233, 131) visible in the label-color picker.

### Mailbox → gws config mapping

| CM tab | Team mailbox | gws config |
|---|---|---|
| `Piteam@` (Jerry) | piteam@lingtulaw.com | `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-piteam` |
| `Picase@` (Ryan) | picase@lingtulaw.com | `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-picase` |
| `Claims@` (Amos/Klaus) | claims@lingtulaw.com | `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claims` |

All three config dirs exist and are authenticated. If a future mailbox is added without
credentials, note it to the user and skip — do not create the label in the wrong mailbox.

Required gws scope for this step: `gmail.labels` (+ `gmail.modify` also accepted).
If auth is missing, run: `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-<mailbox> gws auth login --scopes https://www.googleapis.com/auth/gmail.labels,https://www.googleapis.com/auth/gmail.modify`

### Workflow

```bash
# 1. Set config dir for the team mailbox
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claims   # adjust per CM

# 2. List existing labels — check for duplicate
# NOTE: userId must be passed via --params, not --user-id flag
gws gmail users labels list --params '{"userId":"me"}' 2>&1 | \
  python3 -c "
import sys, json
lines = [l for l in sys.stdin if not l.startswith('Using')]
labels = json.loads('\n'.join(lines)).get('labels', [])
target = '<CASE LABEL NAME>'
match = next((l for l in labels if l.get('name','') == target), None)
print(match['id'] if match else 'NOT_FOUND')
"

# 3a. If NOT_FOUND — create:
gws gmail users labels create \
  --params '{"userId":"me"}' \
  --json '{"name":"<CASE LABEL NAME>","color":{"backgroundColor":"#fbe983","textColor":"#594c05"}}'

# 3b. If found but needs color patch — update:
gws gmail users labels update \
  --params '{"userId":"me","id":"<LABEL_ID>"}' \
  --json '{"color":{"backgroundColor":"#fbe983","textColor":"#594c05"}}'
```

**Confirm:** report the label name, mailbox, and whether it was created or already existed.

---

## Step 13 — Docusign Retainer

The final step — send the retainer only after the tracking sheet, Chat space, and Gmail label
are all done. After confirming sent, update the tracking sheet Note cells to `"Retainer sent M/D"`.

### Template Selection — a 2×2 matrix (fee type × client count)

Pick on TWO axes. **Axis 1 (fee) is Klaus's call — the mandatory gate. Axis 2 (client count)
you determine yourself from the intake.**

| | **1 client** (no joint conflict) | **2+ clients** (joint conflict required) |
|---|---|---|
| **new**<br>先付医疗费 → 剩余 50/50 | **PI Auto Retainer (New)**<br>`dc04f4a3-7e97-4bd6-89e2-f9269d188707` · 9 pages | **PI Auto Retainer+Joint Conflict (New)**<br>`5e019e33-f526-4160-8794-f8c3b738f600` · 12 pages |
| **standard**<br>先扣 1/3 律师费 | **PI Auto Retainer (Standard)**<br>`3211f105-bd8a-4bde-aad1-044d19ed05c4` · 8 pages | **PI Auto Retainer+Joint Conflict (Standard)**<br>`8db4e784-8eb6-4692-9f47-f0c60785832f` · 11 pages |

**Why the joint-conflict axis is mechanical (do NOT ask Klaus about it):** the joint-conflict
disclosure exists because the firm is representing co-clients in one matter — co-clients can
have competing interests (e.g. splitting a limited policy, or the passenger having a claim
against the driver). **1 client → never use a Joint Conflict template** (the client would get
pages of waiver text irrelevant to them). **2+ clients → always use one.**

**All four templates share the same structure:**
- Roles = `Client1` … `Client5` + `Attorney` (Shenqi Cai, pre-filled) + `Case Manager` CC
  (Klaus, pre-filled). Map **Client1 = driver**, Client2 = first passenger, Client3… = rest.
- **Always remove unused Client slots** via `updateEnvelopeRecipients` → `recipientsToRemove`
  before sending (single client → remove Client2–5; two → remove Client3–5).
- **Prefill date tab count/pages differ per template — never assume.** Always call
  `listEnvelopeDocuments` with `include_tabs=true` on the actual envelope and fill every
  returned prefill tab with the DOL. (Known: the 12-page Joint/New one has 4 tabs on pages
  1, 8, 11, 12 — but re-read every time; page counts differ across the four.)

> Note: `5e019e33…` was originally named "PI Auto Retainer（New）" and was renamed to
> "+Joint Conflict (New)" on 7/18/2026. Match on templateId, not on remembered names.

**Legacy templates** — superseded by the four above; use ONLY if Klaus explicitly names one:
`PI Retainer(1/3)` `6ea947db-…` · `PI Retainer + Joint Waiver` `3210bb03-…` ·
`PI Retainer(50%)` `6179267f-…` (these use the old `Driver`/`Passenger1-4` role names).

### Minor client rule

When any client/passenger is a minor (under 18), a parent or legal guardian must sign on their
behalf. Set the minor's Docusign recipient as follows:
- **Name:** `[Parent Name], Parent of [Minor Name]` (e.g. "Bohao Huang, Parent of Lucas Huang")
- **Email:** parent's email address
- The parent signs twice in the same session — once for themselves (if also a client) and once
  for the minor.

### Retainer Workflow

1. **Get account ID:** call `Docusign:getUserInfo` → `e78a2bb2-9440-4ca6-8dff-deded2f8766c`
2. **Create draft** with the DEFAULT template (`PI Auto Retainer（New）`,
   `5e019e33-f526-4160-8794-f8c3b738f600`): `createEnvelope` with `status="created"` and
   `templateRoles` populated **in client order**:
   - `Client1` → driver name/email
   - `Client2` → first passenger (or, if minor, parent name + parent email)
   - `Client3`/`Client4`/`Client5` → additional passengers, else omit
   - Do NOT populate Attorney / Case Manager — template defaults apply.
3. **Remove unused Client slots:** call `listRecipients` first to get the live recipientIds,
   then `updateEnvelopeRecipients` with `recipientsToRemove` containing ONLY the empty ones.
   On this template the ids come back as: Client1=1, Client2=2, Client3=3, Client4=4,
   Client5=5, Attorney=6, Case Manager(CC)=7 — but ALWAYS confirm from `listRecipients`.
   ```
   // two clients → remove the three empty slots
   recipientsToRemove: { signers: [ {recipientId:"3"}, {recipientId:"4"}, {recipientId:"5"} ] }
   ```
   Keep Attorney and Case Manager.
4. **Discover prefill tabs:** call `listEnvelopeDocuments` with `include_tabs=true`
5. **Fill required prefill tabs:** call `updateEnvelopeTabs` with the DOL. Tab IDs must come
   from step 4 — never fabricate.
   - If `updateEnvelopeTabs` is unavailable (it has intermittently dropped off the MCP
     server): leave the envelope as a DRAFT and tell the user the client email, the DOL,
     and which pages need the date — do NOT try to send with empty required tabs.
6. **Send:** `updateEnvelope` with `status="sent"`
7. **After confirmed sent:** write `"Retainer sent M/D"` into the **Note-Claims column (col F)** for
   **all** client rows in the tracking sheet. Also confirm the **Retainer column (col C)** on the
   driver row holds the signed version (`Standard 1/3` or `New 50%`) matching the template you sent.

### Known Prefill Tab Locations

| Template | Prefill date tabs |
|---|---|
| **PI Auto Retainer（New）** ← default | **4 tabs — pages 1, 8, 11, 12** |
| PI Retainer(1/3) / PI Retainer(50%) (legacy) | 3 tabs — pages 1, 5, 6 |
| PI Retainer + Joint Client Waiver (legacy) | 4 tabs — pages 1, 5, 6, 7 |

Fill every tab with the DOL in MM/DD/YYYY format.

### Email Subject Format (max 100 chars)
`PI Retainer: [Driver Full Name] et al-M/D/YYYY`

Examples:
- Single client: `PI Retainer: Guanghua Li et al-5/30/2026`
- Multi-client: `PI Retainer: Hsuan-Yun Chang et al-5/24/2026`

---

## Step 14 — Output the Client Signing Message (文案)

**Always the last thing you output.** After the retainer is confirmed SENT, produce the
WeChat message Klaus forwards to the client asking them to sign. Klaus sends it himself —
this step GENERATES text only, it never sends anything.

### Hard rules (firm's client-message style — see memory `feedback-client-message-plain`)

- **Plain text only.** No markdown, no bold, no bullets, no headers, no underline fill-lines.
- **Present it in a plain code block** so Klaus can copy it straight out.
- **中文（简体）+ 全角标点**（，。：？！）
- **CLIENT NAMES ALWAYS IN ENGLISH — exactly as they appear on the ID.** Never write a
  client's Chinese name in the message, even though the rest of the text is 中文, and even
  when the intake form or WeChat shows a Chinese name. Use the DL / passport spelling in
  `Firstname Lastname` order (DL prints `LN CHEN / FN XIONGLING` → write **Xiongling Chen**).
  Rationale: the name must match what DocuSign shows the signer, so the client can tell at a
  glance which envelope is theirs. Same rule for the minor and the signing parent
  (e.g. `Yujie Hu（代 Louis Chen 签署）`).
- **Fill in every value** — never leave `____` or placeholders. If a value is genuinely
  unknown, ask Klaus instead of shipping a blank.
- **Non-driven / State-Bar-safe.** No promises about outcome, value, or timeline. Do not
  imply the firm arranged anything the client didn't ask for.
- Sign off with `凌图律所`.

### Structure (all versions)

Every version has the same four blocks, in this order:
1. 合同已发到哪个邮箱
2. **服务内容**（我们会做什么）
3. **费用说明**（见下方 fee rules — NEVER invent this)
4. **签约前提醒**（以合同为准 / 先读懂再签 / 有问题先问）
5. 签署操作说明 + 落款

### ⚠️ Fee-section rules (read before writing 费用说明)

- The fee paragraph is a **representation the client relies on** — getting it wrong is a
  real harm and a Bar problem. **Never invent or infer fee/cost mechanics.**
- **The 费用说明 MUST match the retainer type actually sent in Step 13.** Never pair a `new`
  template with `standard` wording or vice versa.
- Use the exact wording below for each type — do **not** paraphrase or add mechanics that
  aren't there (e.g. don't claim the firm advances case costs unless Klaus has confirmed it).
- Always close the fee block with `以上为简要说明，具体条款以合同为准。`
- Never promise outcome, amount, or timeline.

**`new` 版（先付医疗费 → 剩余 50/50）：**

```
费用说明：
一、我们采用风险代理方式，签约时不需要您支付任何前期费用。
二、案子拿到赔偿后，先用赔偿金支付您的医疗费用。
三、扣除医疗费用之后剩余的金额，由您和律所各得一半（各 50%）。
四、以上为简要说明，具体条款以合同为准。
```

**`standard` 版（先扣 1/3 律师费）：**

```
费用说明：
一、我们采用风险代理方式，签约时不需要您支付任何前期费用。
二、案子拿到赔偿后，先按赔偿总额的三分之一（1/3）支付律师费。
三、剩余的金额用于支付您的医疗费用，之后的余额归您。
四、以上为简要说明，具体条款以合同为准。
```

Multi-client: swap 您 → 两位／三位 to match the client count.

### Single-client template

```
您好，我们已经把委托合同通过 DocuSign 发送到您的邮箱：[客户邮箱]

签之前，先跟您简单说明一下我们会做什么、以及费用怎么算。

我们的服务内容：
一、代表您处理这次事故的人身伤害索赔，与对方保险公司和您自己的保险公司沟通，由我们出面，您不需要自己跟保险公司对接。
二、调取并整理案件材料，包括警察报告、医疗记录和账单、车损与现场证据。
三、协助处理医疗账单和治疗机构的费用问题。
四、协助处理车辆维修、租车等财产损失相关事宜。
五、代表您与保险公司谈判赔偿方案，任何和解方案都需要经过您同意才会接受。

费用说明：
[按上方 fee-section rules，整段套用 new 版或 standard 版 — 必须与 Step 13 实际发出的模板一致]

签约前请您注意：
一、合同里写的内容以合同为准，这段文字只是方便理解的简要说明。
二、请您在签名前完整阅读一遍合同，特别是费用和成本的部分。
三、如果有任何不明白的地方，签之前随时问我，我们解释清楚再签，不用着急。

麻烦您查收后，点击邮件里的链接完成电子签名。如果收件箱里没有看到，请检查一下垃圾邮件文件夹，发件人显示为 DocuSign。

签署完成后系统会自动回传给我们，我们就可以正式开始处理您的案子。

凌图律所
```

### Multi-client template

Each client signs on their OWN email — say so explicitly, and list every client + email.
Swap 您 → 两位／三位 etc. to match the client count.

```
您好，我们已经把委托合同通过 DocuSign 分别发送到两位的邮箱：

[客户1英文名]：[客户1邮箱]
[客户2英文名]：[客户2邮箱]

签之前，先跟两位简单说明一下我们会做什么、以及费用怎么算。

我们的服务内容：
一、代表两位处理这次事故的人身伤害索赔，与对方保险公司和您自己的保险公司沟通，由我们出面，两位不需要自己跟保险公司对接。
二、调取并整理案件材料，包括警察报告、医疗记录和账单、车损与现场证据。
三、协助处理医疗账单和治疗机构的费用问题。
四、协助处理车辆维修、租车等财产损失相关事宜。
五、代表两位与保险公司谈判赔偿方案，任何和解方案都需要经过两位同意才会接受。

费用说明：
[按上方 fee-section rules，整段套用 new 版或 standard 版 — 必须与 Step 13 实际发出的模板一致]

签约前请两位注意：
一、合同里写的内容以合同为准，这段文字只是方便理解的简要说明。
二、请两位在签名前完整阅读一遍合同，特别是费用和成本的部分。
三、如果有任何不明白的地方，签之前随时问我，我们解释清楚再签，不用着急。

两位都需要在各自的邮箱里点击链接完成电子签名，缺一份合同都无法生效。如果收件箱里没有看到，请检查一下垃圾邮件文件夹，发件人显示为 DocuSign。

两位都签署完成后系统会自动回传给我们，我们就可以正式开始处理这个案子。

凌图律所
```

### Minor-client variant

When a client is a minor, the parent/guardian signs. Adjust that client's line to name the
parent and their email, e.g. `[家长英文名]（代 [小孩英文名] 签署）：[家长邮箱]`, and add this line
to the 签署操作说明 block:
`未成年人的合同需要由家长在同一封邮件里签署两次，一次代表本人，一次代表孩子。`

---

## Critical Flags to Always Check

> ⚠️ **These are reported to the user in the case summary / Chat message — they do NOT get
> written into intake-sheet cells.** The sheet records the client's statement verbatim
> (see 「填写总原则」 in cell-map.md). Never put a flag, a ⚠️, a recommendation, or a legal
> characterization inside a cell.

- **3P AIC effective date = DOL** → CRITICAL same-day coverage flag
- **Expired AIC (1P or 3P)** → CRITICAL
- **CAARP temp card** → compute 60-day expiry, flag if expired at DOL
- **Instruction permit (not DL)** → CRITICAL, policy rescission risk
- **State ID uploaded instead of DL** → verify client has valid DL
- **LIMITED-TERM DL** → note in summary (DACA/visa, no coverage impact)
- **Named insured ≠ driver** → report in summary. (I7 = Policyholder, I8 = the person actually
  driving = our client. Do NOT write the named insured into I8.)
- **Vehicle not on AIC** → yellow I11/I12/I13, CRITICAL
- **Minor client or passenger** → guardian auth required; report in summary (L9 keeps just the
  name — minor/provisional-licence notes go in the summary, not the cell)
- **Active gig/TNC work** → yellow I5/I6/I11, note platform and Period
- **No police report** → report in summary. (I31 SR-1 Status stays `Pending`+yellow — no
  judgment, no computed deadline, in the cell.)
- **Prior accident still open** → report in summary; C17 keeps the client's answer verbatim

---

## Reference Files

- `references/cell-map.md` — 填写总原则 + complete value cell map and yellow rules (**read first**)
- `references/document-rules.md` — Per-document extraction rules (DL, AIC, police card, etc.)
- `references/document-placement.md` — File naming conventions and folder placement
- `references/summary-format.md` — Output summary format
- `scripts/verify_intake.py` — **Gate 2**: post-write type self-check (catches values written
  into the wrong field). Mandatory after filling the intake sheet, before Drive upload.
