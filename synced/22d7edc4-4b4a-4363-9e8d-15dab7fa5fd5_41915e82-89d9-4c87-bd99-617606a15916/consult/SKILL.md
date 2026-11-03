---
name: consult
description: Archive client consultations for Lingtu Law / SIA 高徒 into Google Drive. Use this skill whenever someone wants to file, archive, or log a client consultation ($100/$250/$500), create a doc or folder for a new or returning consultation client, rename an existing consultation folder/doc to add a follow-up date, or upload materials for a consultation. Triggers on Chinese or English phrasing — "归档咨询", "咨询归档", "新咨询", "建咨询文件夹", "上传咨询材料", "archive consultation", "log consultation", "consultation folder" — even if the user doesn't say "skill".
---

# consult — Client Consultation Archiver

Archives client consultation records into Google Drive, matched against Cassie's calendar.

```bash
export PATH="$HOME/.local/bin:$PATH"   # gws lives here; run once per session
```

If any `gws` call 401s / `invalid_grant`: run `gws auth login -s drive`, paste the URL to the user.

**Every `gws drive files list` call must include** `supportsAllDrives`, `includeItemsFromAllDrives`, `corpora: allDrives` — omitting these returns an empty list silently.

## Known constants

| What | ID / Value |
|---|---|
| `评估` main folder (holds all $250/$500 folders and the $100 subfolder) | `1Njsfhvq3qsH9B3EpldO9_L7TbElPnBbn` |
| `$100` subfolder (holds docs for $100 consultations with special notes) | `1yaeJ_CuuiB6PSFl_peUdWMDX85zEBzp0` |
| Cassie's calendar | `cassie@lingtulaw.com` |
| Date format (new records) | `MM.DD.YYYY` e.g. `08.18.2026` |

## Step 1 — Gather info

Collect from the user (or infer from context):

| Field | Notes |
|---|---|
| Client name | Exactly as it should appear in the file/folder name |
| Consultation date | Default: today |
| Type | `$100`, `$250`, or `$500` |
| Topic | e.g. O1, H1B, NIW, EB1A, 婚绿, 身份规划 … |
| Special notes | Any written notes to put in the doc body (for $100 only) |
| Materials to upload | File paths or user-uploaded files |

**If name or date is unclear**, pull today's appointments from Cassie's calendar and ask the user to confirm which one:

```bash
gws calendar events list --calendar cassie@lingtulaw.com \
  --params '{"timeMin":"<today>T00:00:00Z","timeMax":"<today>T23:59:59Z","singleEvents":true,"orderBy":"startTime"}'
```

## Step 2 — Check for existing records

Search BOTH locations for the client's name before creating anything — the person may have consulted before.

**Search in `$100` folder (docs):**
```bash
gws drive files list --params '{
  "q": "'\''1yaeJ_CuuiB6PSFl_peUdWMDX85zEBzp0'\'' in parents and name contains '\''<FirstName>'\''",
  "fields": "files(id,name,mimeType)",
  "supportsAllDrives": true,
  "includeItemsFromAllDrives": true,
  "corpora": "allDrives"
}'
```

**Search in `评估` main folder (for $250/$500 folders):**
```bash
gws drive files list --params '{
  "q": "'\''1Njsfhvq3qsH9B3EpldO9_L7TbElPnBbn'\'' in parents and name contains '\''<FirstName>'\'' and mimeType = '\''application/vnd.google-apps.folder'\''",
  "fields": "files(id,name,mimeType)",
  "supportsAllDrives": true,
  "includeItemsFromAllDrives": true,
  "corpora": "allDrives"
}'
```

If you find a match, confirm with the user: "I found [Name] from [prior date] — is this the same person?" before renaming.

## Step 3 — Create or update

### $100 consultations

**No special notes → no action.** Tell the user: "普通 $100 咨询无需提前建档，当场处理即可。"

**Has special notes or materials:**

- **New client** → Create a Google Doc in the `$100` folder:
  ```bash
  gws drive files create --params '{
    "name": "<Name> <Topic> <MM.DD.YYYY>",
    "mimeType": "application/vnd.google-apps.document",
    "parents": ["1yaeJ_CuuiB6PSFl_peUdWMDX85zEBzp0"]
  }' --supports-all-drives
  ```
  Then add the notes to the doc body using `gws docs documents batchUpdate` or similar.

- **Returning client** → Rename the existing doc by appending the new date:
  ```bash
  gws drive files update --file-id "<existing-doc-id>" \
    --params '{"name": "<Name> <Topic> <OriginalDate>/<NewDate>"}' --supports-all-drives
  ```

### $250 / $500 consultations (评估)

- **New client** → Create a folder in the `评估` main folder:
  ```bash
  gws drive files create --params '{
    "name": "<Name> <Topic> <MM.DD.YYYY>",
    "mimeType": "application/vnd.google-apps.folder",
    "parents": ["1Njsfhvq3qsH9B3EpldO9_L7TbElPnBbn"]
  }' --supports-all-drives
  ```

- **Returning client** → Rename the existing folder by appending the new date:
  ```bash
  gws drive files update --file-id "<existing-folder-id>" \
    --params '{"name": "<Name> <Topic> <OriginalDate>/<NewDate>"}' --supports-all-drives
  ```

## Step 4 — Upload materials (if any)

macOS screenshot filenames contain a Unicode narrow no-break space (U+202F) before AM/PM, which breaks shell quoting. Always copy to a safe filename first, upload, then delete:

```bash
python3 -c "
import os, shutil, glob
# find the file the user specified, e.g. most-recent Desktop screenshot
src = '<full path to file>'   # or use glob to find it
dst = os.path.expanduser('~/Desktop/_upload_tmp.png')
shutil.copy(src, dst)
"
cd ~/Desktop
gws drive files create \
  --upload _upload_tmp.png \
  --json '{"name": "<display name>", "parents": ["<target-folder-id>"]}' \
  --params '{"supportsAllDrives": true, "fields": "id,name"}'
rm ~/Desktop/_upload_tmp.png
```

For non-screenshot files (PDFs, docx, etc.) with normal filenames, you can skip the copy step and pass the path directly to `--upload` from the file's directory.

**Do NOT upload payment screenshots** — the team confirms payment manually. If the user asks to upload a payment screenshot, skip it and remind them.

## Naming rules

Format: `Name Topic MM.DD.YYYY`

| Scenario | Example |
|---|---|
| First consultation | `Zhang San H1B 08.18.2026` |
| Follow-up (same topic) | `Zhang San H1B 08.18.2026/10.05.2026` |
| Follow-up (new topic) | `Zhang San H1B 08.18.2026/NIW 10.05.2026` (add new topic before date) |

When searching for existing records, be flexible — older entries may use 2-digit years (`8.18.26`) or missing leading zeros. Match on the name, not the full string.

## Confirmation before acting

Always state what you're about to do before running write commands:
- "Creating Google Doc '张三 H1B 08.18.2026' in the $100 folder."
- "Renaming folder 'Zhang San NIW 06.16.2026' → 'Zhang San NIW 06.16.2026/08.18.2026'."

Then proceed immediately — don't ask for a second confirmation unless something is ambiguous.
