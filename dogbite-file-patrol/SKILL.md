---
name: dogbite-file-patrol
description: |
  Daily maintenance patrol that keeps every DOG BITE case folder tidy for Hernán Simó /
  凌图律所 (Law Office of Shenqi Cai APC) in the "Hernan Simo Cases" shared drive. Use this
  skill on a daily schedule, or on demand when asked to "整理 dog bite 文件 / tidy the dog
  bite cases / run the dog bite file patrol / sort the lobby files". It scans every
  new-template case folder's LOBBY (root) for loose files the client/Klaus dropped in,
  classifies each (by learned rules → filename → Claude vision of the content) into the
  right numbered subfolder per the firm's four routing rules, MOVES them (within the same
  case; never deletes, never crosses cases), leaves anything it is unsure about in the
  lobby, and posts a summary to the "Dog Bite Cases" Google Chat space. Files Klaus
  manually resolves are learned into routing_memory.json so the same kind auto-sorts next
  time. Legacy (non-6-folder) cases are detected and skipped. Read-mostly + safe moves only.
---

# Dog Bite File Patrol — daily lobby tidy

Keeps dog-bite case folders organized as new files arrive. The **lobby norm**: a case
folder's root holds ONLY `0. Case Intake.docx`, `0. Intake Sheet`, and the six numbered
subfolders. Anything else loose in the root is a new file to sort.

**Safety contract:** only MOVES files within the same case (loose root → a subfolder).
Never deletes, never renames destructively, never touches another case, never touches the
whitelist, never touches legacy-layout cases. Unsure → leave in place + report.

## Constants
- Shared drive **Hernan Simo Cases** `driveId 0APtYw9adyTl8Uk9PVA`;
  **`1. Dog Bite Cases`** = `1ewaJIoeLHoc3lG3dIyDTfWwuSt6HYRVt`.
- Summary Chat space **"Dog Bite Cases"** = `spaces/AAQAJFB3j-o` (members: Klaus + claude@).
- Post as **claude@** via `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claude`. If that
  store is not authenticated, fall back to default `gws` (Klaus@) and note it.
- Scratch: `~/dogpatrol_work` (`mkdir -p`; absolute `$HOME/...` paths only).

Scripts (`scripts/`, import `gws_util.py`):
- `scan_lobbies.py` — list loose lobby files per **new-template** case (skips legacy).
- `apply_moves.py` — execute the moves from a decisions.json (safe: move-only).
References:
- `references/routing_memory.json` — learned filename→subfolder rules (checked first).

## The four routing rules (source of truth — same as new-dogbite-case)
| File | → subfolder |
|---|---|
| Driver license / ID; scene / address / dog / liability photos & videos; property deed | `1. Incident & Liability` |
| Retainer, POE, LOR, other legal correspondence | `2. Legal Documents` |
| **Injury photos**, ER / medical records & bills | `3. Medical Record & Bill` |
| Summons / complaint / CMC / court & litigation docs | `4. Litigation` |
| Invoices / receipts / costs | `5. Cost & Receipt` |
| Settlement / disbursement docs | `6. Settlement & Disbursement` |
> Injury photos (client's wounds) = **medical → 3**. Scene/liability photos = **1**.

---

## Step 1 — Scan all lobbies
```bash
mkdir -p ~/dogpatrol_work
python3 ~/.claude/skills/dogbite-file-patrol/scripts/scan_lobbies.py > ~/dogpatrol_work/scan.json
cat ~/dogpatrol_work/scan.json
```
Returns `{to_sort:[{case,case_id,loose:[{id,name,mime}]}], skipped_legacy:[...]}`. If
`to_sort` is empty, post a short "nothing to sort today" summary and stop.

## Step 2 — Classify each loose file (learned rules → filename → vision)
Load `references/routing_memory.json`. For every loose file, decide its target subfolder:

1. **Learned rules first.** If the filename matches any `name_contains` rule → that target.
2. **Descriptive filename.** If the name clearly says what it is (e.g. `ER Records`,
   `Injury`, `Deed`, `Summons`) → apply the four rules.
3. **Vision / content.** If the name is meaningless (`IMG_1234.jpg`, `scan_0001.pdf`),
   inspect the content: download it (`gws drive files get … alt=media`) and **read it**
   — for images use the `Read` tool (vision); for PDFs read the text, and if there is no
   text layer (scanned) render page 1 and read it. Then classify:
   - wound / injury close-up → `3. Medical Record & Bill`
   - accident scene / house / gate / street / dog → `1. Incident & Liability`
   - an ID / driver license → `1. Incident & Liability`
   - a medical record or bill → `3. Medical Record & Bill`
   - a court/litigation doc → `4. Litigation`
4. **Unsure?** Do NOT guess. Leave the file in the lobby and add it to the summary's
   "待你人工定" list.

Map each chosen subfolder name to its **id** from the case's children (list the case
folder; match by exact subfolder name). Build `~/dogpatrol_work/decisions.json`:
```json
{"moves": [
  {"file_id":"…","case":"Bo Tao-062726","from_parent":"<case_id>",
   "to_parent":"<subfolder_id>","subfolder":"1. Incident & Liability",
   "old_name":"IMG_9001.jpg"}
]}
```
Add `"new_name"` only if a rename clearly helps (e.g. `IMG_9001.jpg` →
`Incident Scene Photo.jpg`); otherwise keep the original name.

## Step 3 — Apply the moves
```bash
python3 ~/.claude/skills/dogbite-file-patrol/scripts/apply_moves.py ~/dogpatrol_work/decisions.json
```

## Step 4 — Post the summary to the Dog Bite Cases space (as claude@)
```bash
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claude
gws chat spaces messages create --params '{"parent":"spaces/AAQAJFB3j-o"}' \
  --json "$(python3 -c 'import json;print(json.dumps({"text":"<summary>"},ensure_ascii=False))')"
```
Summary format (skip the "nothing" line if all clear):
```
🐕 【Claude】Dog Bite 文件巡检 — <today>
已归类 N 个文件:
 • <Case>: <file> → <subfolder>
 …
待你人工定(留在 lobby):
 • <Case>: <file> — <why unsure>
跳过旧结构案: <list>   (仅首次或有变化时提一句)
```

## Step 5 — Learn from Klaus's manual placements
When Klaus resolves a "待你人工定" file himself (or tells you where it goes), **append a
rule to `references/routing_memory.json`** (`name_contains` or a content hint → target)
so the same kind auto-sorts next time. This is the patrol's memory — keep it growing.

## Notes
- **Never touch legacy cases** — `scan_lobbies.py` already filters to new-template cases
  (those with `1. Incident & Liability` + `3. Medical Record & Bill`). Legacy cases keep
  their intake/POE/SCM loose on purpose.
- The two `0.` files and the Intake Sheet are whitelisted — never swept.
- Moves are reversible (a move, not a delete). If a classification is later found wrong,
  it can be moved back; still, prefer leaving unsure files in the lobby over guessing.
- On demand: the same skill runs when Klaus says "整理 Bo Tao / tidy the dog bite cases".
