---
name: medical-records-sop
description: "Use this skill when processing incoming medical records/bills emails for Lingtu Law PI cases. Covers the full workflow: Gmail filtering → client identification → labeling → saving to Drive → renaming → draft reply → Google Chat Space summary → pin. Trigger on any task involving 'medical records', 'MRI', 'chiro', 'PM', 'neuro', 'medical bills', or 'client files' in the context of Lingtu Law."
author: Lingtu Law
---

# Lingtu Law — Medical Records & Bills Processing SOP

Complete workflow for handling incoming medical records and bills via email, from Gmail inbox to Google Chat Space.

**All steps use the `gws` CLI (Google Workspace CLI) only. Do NOT use MCP tools.**

### Account Usage Rules

Different steps use different gws accounts. The user will specify which email account to use for Gmail operations (piteam or claims). **Chat Space messages are ALWAYS sent via claire.f.**

| 操作 | 账号 | 环境变量前缀 |
|------|------|------------|
| Gmail (筛选/读取/label/draft) | 用户指定 piteam 或 claims | piteam: 无前缀 / claims: `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claims` |
| Drive (搜索/上传) | 同 Gmail 账号 | 同上 |
| **Chat Space (查询/发送)** | **始终 claire.f** | **`GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-personal`** |

> ⚠️ 默认 `gws`（无前缀）实际登录的是 **piteam@lingtulaw.com**，不是 claire.f！

---

## Step 1 — Filter Medical Emails from Gmail

Search Gmail for emails containing medical documents. **Add the correct env prefix based on the user's specified account.**

```bash
# For claims@lingtulaw.com:
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claims gws gmail +triage --query 'in:inbox' --max 30

# For piteam@lingtulaw.com (default):
gws gmail +triage --query 'in:inbox' --max 30
```

Or search for a specific client/unread emails:

```bash
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claims gws gmail +triage --query 'is:unread in:inbox [Client Name]' --max 10
```

---

## Step 2 — Read Email & Download Attachments

**Step 2a — Read the email to understand context:**
```bash
gws gmail +read --id MESSAGE_ID
```

**Step 2b — Get attachment IDs (need full message details):**
```bash
gws gmail users messages get --params '{"userId":"me","id":"MESSAGE_ID","format":"full"}' 2>/dev/null | python3 -c "
import sys, json
lines = sys.stdin.readlines()
json_start = next(i for i, l in enumerate(lines) if l.strip().startswith('{'))
data = json.loads(''.join(lines[json_start:]))
def find_parts(payload, results=None):
    if results is None: results = []
    fn = payload.get('filename', '')
    aid = payload.get('body', {}).get('attachmentId', '')
    if fn and aid:
        results.append((fn, aid))
    for p in payload.get('parts', []):
        find_parts(p, results)
    return results
for fn, aid in find_parts(data.get('payload', {})):
    print(f'{fn} -> {aid}')
"
```

> ⚠️ gws outputs a "Using keyring backend" line before JSON. Use `2>/dev/null` and find the JSON start position to avoid parse errors.

**Step 2c — Download attachment (returns base64, must decode):**
```bash
gws gmail users messages attachments get \
  --params '{"userId":"me","messageId":"MESSAGE_ID","id":"ATTACHMENT_ID"}' \
  2>&1 | python3 -c "
import sys, json, base64
lines = sys.stdin.readlines()
json_start = next(i for i, l in enumerate(lines) if l.strip().startswith('{'))
data = json.loads(''.join(lines[json_start:]))['data']
data = data.replace('-', '+').replace('_', '/')
padding = 4 - len(data) % 4
if padding != 4: data += '=' * padding
decoded = base64.b64decode(data)
with open('FILENAME.pdf', 'wb') as f:
    f.write(decoded)
print(f'Saved: {len(decoded)} bytes')
"
```

> ⚠️ The `-o` flag does NOT save binary files correctly. Always pipe through python3 to decode base64.

**Step 2d — Read the PDF locally** to identify the patient name and document content:
- Use the Read tool on the saved PDF file
- Check patient name, date of service, diagnoses, findings, bill amounts
- One email may contain records for only one client even if thread involves multiple

---

## Step 3 — Label Email in Gmail

**Step 3a — List existing labels to find the client label:**
```bash
gws gmail users labels list --params '{"userId":"me"}'
```

**Step 3b — If label NOT found, check Master Sheet before creating:**

> ⚠️ **DO NOT** create a new label if the client is not found. The client may belong to a different email account. Always verify in the Master Sheet first.

```bash
# Search all 3 tabs for the client name
gws sheets +read --spreadsheet '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM' --range "'Claims@'!B1:B200"
gws sheets +read --spreadsheet '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM' --range "'Piteam@'!B1:B200"
gws sheets +read --spreadsheet '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM' --range "'Picase@'!B1:B200"
```

- If client is in a **different tab** than the current email account, treat "forward" and "label the forward" as **one atomic step** — a forward that lands unlabeled in the destination mailbox is invisible to that mailbox's normal label-based workflow, so never stop after step 2 below:
  1. Apply the account ownership label (e.g., `PITeam` or `Claims`) to the message in the current account
  2. **Send** (not draft) forward to the owning account: `gws gmail +forward --message-id ID --to TARGET_EMAIL`
  3. **In the owning account**, find the forwarded email (`Fwd: ...` subject) and apply the client's case label there with `gws gmail users messages modify --params '{"userId":"me","id":"FWD_MESSAGE_ID"}' --json '{"addLabelIds":["CLIENT_LABEL_ID"]}'` — do this immediately, don't defer it
  4. Back in the current account, create a **draft reply** to the clinic: `gws gmail +reply --message-id ID --body 'Received, thank you!' --draft`
- If client is in the **current tab** → create the label

**Step 3c — Create label (only after Master Sheet verification):**
```bash
gws gmail users labels create --params '{"userId":"me"}' \
  --json '{"name":"Tingting Yang"}'
```

**Step 3d — Apply label to the message:**
```bash
gws gmail users messages modify --params '{"userId":"me","id":"MESSAGE_ID"}' \
  --json '{"addLabelIds":["LABEL_ID"]}'
```

- Label format: **First name Last name** (e.g., `Tingting Yang`)
- Check if label already exists before creating

### Known account ownership labels in claims@lingtulaw.com
- `PITeam` → Label_1667880425376635053

---

## Step 4 — Upload Attachments to Google Drive Folder 4

**Drive folder structure:**
```
[Client Name] [DOL]
└── 4#Bodily Injury Claim                          ← single client
    or
└── 4#Folder-Bodily Injury Claim(...)              ← multi-client
```

**DOL format in folder name:** MM:DD:YYYY (e.g., `02:27:2026`)

**Step 4a — Find the client folder (shared drive — must use `corpora: allDrives`):**
```bash
gws drive files list --params '{
  "q":"name contains '\''ClientName'\'' and mimeType='\''application/vnd.google-apps.folder'\''",
  "fields":"files(id,name,parents)",
  "supportsAllDrives":true,
  "includeItemsFromAllDrives":true,
  "corpora":"allDrives"
}'
```

**Step 4b — Find Folder 4 inside the client folder:**
```bash
gws drive files list --params '{
  "q":"name contains '\''4#'\'' and parentId='\''CLIENT_FOLDER_ID'\'' and mimeType='\''application/vnd.google-apps.folder'\''",
  "fields":"files(id,name)",
  "supportsAllDrives":true,
  "includeItemsFromAllDrives":true,
  "corpora":"allDrives"
}'
```

**Step 4c — Upload to shared drive (use `files create`, NOT `+upload`):**
```bash
gws drive files create \
  --params '{"supportsAllDrives":true}' \
  --json '{"name":"Neuro R","parents":["FOLDER_4_ID"]}' \
  --upload ./filename.pdf \
  --upload-content-type application/pdf
```

> ⚠️ `gws drive +upload` does NOT support shared drives. Always use `gws drive files create` with `supportsAllDrives:true`.
> ⚠️ `--upload` requires the file to be inside the current working directory. If files are in `/tmp`, first `cp` them to the current directory, then use `./filename.pdf`.

**Step 4d — Clean up local temp files after upload.**

---

## Step 5 — File Naming Convention

Files are named during upload in Step 4c via the `"name"` field.

| Document Type | Report | Bill |
|---|---|---|
| MRI — Brain | `Brain MRI R` | `MRI B` |
| MRI — Cervical | `C MRI R` | `MRI B` |
| MRI — Lumbar | `L MRI R` | `MRI B` |
| MRI — Thoracic | `T MRI R` | `MRI B` |
| Chiropractic | `Chiro R` | `Chiro B` |
| Pain Management | `PM R` | `PM B` |
| Pain Management — Surgery Center (injection/procedure performed at an ambulatory surgery center, not the PM office itself) | `PM SE R` | `PM SE B` |
| Neurology | `Neuro R` | `Neuro B` |
| Physical Therapy | `PT R` | `PT B` |
| Orthopedic | `Ortho R` | `Ortho B` |
| Psychology | `Psych R` | `Psych B` |

> A PM report/bill package sometimes bundles a **Surgery Center** report+bill for the actual injection/procedure (separate from the PM office visit). Name those `PM SE R` / `PM SE B` — don't fold them into plain `PM R` / `PM B`, since they're billed by a different facility and need to be distinguishable on the Sheet and in Drive.

**Duplicate handling:** Add date to distinguish (e.g., `PM R 5-11`, `PM R 6-3`)

If renaming is needed after upload:
```bash
gws drive files update \
  --params '{"fileId":"FILE_ID","supportsAllDrives":true}' \
  --json '{"name":"Neuro R"}'
```

---

## Step 6 — Draft Reply in Gmail

**Do NOT use `+reply`** — it auto-includes quoted original text. Instead, construct a MIME draft directly so the reply body is clean (only "Received, thank you!" with no quoted text below).

**Step 6a — Get the original message headers for threading:**
```bash
gws gmail users messages get --params '{"userId":"me","id":"MESSAGE_ID","format":"metadata","metadataHeaders":["Subject","Message-Id","References"]}' 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
hdrs = {h['name']:h['value'] for h in data['payload']['headers']}
print('Subject:', hdrs.get('Subject',''))
print('Message-Id:', hdrs.get('Message-Id',''))
print('ThreadId:', data.get('threadId',''))
"
```

**Step 6b — Create the draft with clean body (no quoted text):**

> ⚠️ **必须用 `multipart/alternative` 格式**（同时包含 plain text 和 HTML）。单独用 `MIMEText html` 或纯文本都不行，Gmail 无法正常加载签名图片。

```bash
gws gmail users drafts create --params '{"userId":"me"}' --json "$(python3 -c "
import base64, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
msg = MIMEMultipart('alternative')
msg['To'] = 'SENDER_EMAIL'
msg['Subject'] = 'Re: ORIGINAL_SUBJECT'
msg['In-Reply-To'] = 'ORIGINAL_MESSAGE_ID_HEADER'
msg['References'] = 'ORIGINAL_MESSAGE_ID_HEADER'
msg.attach(MIMEText('Received, thank you!', 'plain', 'utf-8'))
msg.attach(MIMEText('<div dir=\"ltr\">Received, thank you!</div>', 'html', 'utf-8'))
raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
print(json.dumps({'message': {'raw': raw, 'threadId': 'THREAD_ID'}}))
")" 2>/dev/null
```

> ⚠️ After creating the draft, **open it in Gmail and select the preset signature "Claire"** before sending. The CLI cannot set Gmail signatures programmatically.
> ⚠️ Body must be ONLY `Received, thank you!` — no extra text, no signature block, no greeting.

---

## Step 7 — Find Client's Google Chat Space

**Always use claire.f (gws-personal) for Chat operations.**

> ⚠️ **不要用 grep + regex proximity 提取 space ID！** 会匹配到相邻 space 的 ID。必须用完整 JSON 对象解析。

```bash
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-personal gws chat spaces list --page-all --format json 2>/dev/null | python3 -c "
import sys, json, re
text = sys.stdin.read()
for m in re.finditer(r'\"displayName\":\"([^\"]*CLIENT_KEYWORD[^\"]*)\"', text):
    start = m.start()
    brace_start = text.rfind('{', max(0, start-500), start)
    depth = 0
    for i in range(brace_start, min(len(text), start+1000)):
        if text[i] == '{': depth += 1
        elif text[i] == '}': depth -= 1
        if depth == 0:
            obj = json.loads(text[brace_start:i+1])
            print(json.dumps(obj, indent=2))
            break
"
```

> ⚠️ If Chat returns 403 "insufficient scopes", delete the token cache and retry:
> `rm ~/.config/gws-personal/token_cache.json`

**Space naming format:** `[Client Name]-[DOL](J)`
- Example: `Zhixing Piao-2/27/2026(J)`

Extract the `name` field (e.g., `spaces/AAQAgR6pbNU`) for use in Step 8.

---

## Step 8 — Send Summary Message to Chat Space

**Always use claire.f (gws-personal) to send Chat messages:**

```bash
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-personal gws chat +send --space 'spaces/SPACE_ID' --text 'MESSAGE_TEXT'
```

### Message Template (中文)

```
📋 [科室]报告 ([date]):
诊断:
[诊断1]
[诊断2]
...

*建议治疗:*
[治疗项目1]
[治疗项目2]
...

💰 [科室] Bill ([provider]): $[总金额]

[Client Name] 的 [document types] 已保存至 [Client Name] [DOL] > 4#Folder

文件链接:
[File Name 1]: https://drive.google.com/file/d/FILE_ID_1/view
[File Name 2]: https://drive.google.com/file/d/FILE_ID_2/view
```

**Format rules:**
- `*建议治疗:*` 必须加粗（用 `*` 包围）
- 存储路径信息放在消息**最后一行之前**，文件链接放在**最后**
- 用简体中文
- 文件链接使用上传时返回的 Drive file ID 构建 `https://drive.google.com/file/d/FILE_ID/view`，Chat 会自动渲染为 rich link 预览卡片

### What to include by document type

| Type | What to summarize |
|---|---|
| Neuro / PM / 骨科 / 心理科 | 诊断 + 建议治疗计划（分段列出） |
| MRI | 简要诊断结果（不需要逐级复阅细节） |
| Chiro / PT | 就诊次数 + 总账单金额 |
| Bills | 只需总金额，不需要逐项列出 |

### Emoji guide

| Emoji | Use for |
|---|---|
| 📋 | General report / summary |
| 💰 | Bill / invoice |

> Note: 不需要为每个 MRI 部位使用不同 emoji，统一用 📋 即可。

---

## Step 8.1 — Draft MRI Reports to Chiro Clinic

**Only when MRI reports are received.** Draft a reply to the chiro clinic with the MRI report PDFs attached.

**Step 8.1a — Find the chiro referral email:**

在**客户所属账号**（owning account）中搜索原始 referral 邮件。命名规则：
- `Referral_Lingtu Law_[Client Name]` → **chiro clinic** (no prefix)
- `MRI_Referral_Lingtu Law_[Client Name]` → MRI facility (has `MRI_` prefix)

> ⚠️ 搜索 `Referral_Lingtu Law_客户名`，排除 `MRI_` 前缀和 `Fwd:` 转发的邮件。必须在 owning account 中找，不是收件账号。

```bash
gws gmail +triage --query 'subject:"Referral_Lingtu Law_CLIENT_NAME"' --max 20
```

Read the email to confirm: the `To` address is the chiro clinic. Note the `threadId` and `Message-Id` header.

**Step 8.1b — Download the MRI report files from Drive:**
```bash
gws drive files get --params '{"fileId":"FILE_ID","supportsAllDrives":true,"alt":"media"}' -o ./filename.pdf
```

**Step 8.1c — Create a draft reply with attachments:**

> ⚠️ 带附件的 draft JSON 很大（~400KB+），**不能用 shell `$(...)` 传参**，会静默失败。必须用 python `subprocess` 直接调用 gws，通过命令行参数传递完整 JSON。

```python
python3 << 'PYEOF'
import base64, json, subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

msg = MIMEMultipart('mixed')
msg['To'] = 'CLINIC_EMAIL'
msg['Subject'] = 'Re: Referral_Lingtu Law_CLIENT_NAME'

body_alt = MIMEMultipart('alternative')
body_alt.attach(MIMEText('Hi,\n\nPlease find attached the MRI reports for CLIENT_NAME.\n\nThank you.', 'plain', 'utf-8'))
body_alt.attach(MIMEText('<div dir="ltr">Hi,<br><br>Please find attached the MRI reports for CLIENT_NAME.<br><br>Thank you.</div>', 'html', 'utf-8'))
msg.attach(body_alt)

for fname, display in [('./c_mri_r.pdf', 'Client Name - C MRI Report.pdf'),
                        ('./l_mri_r.pdf', 'Client Name - L MRI Report.pdf')]:
    with open(fname, 'rb') as f:
        att = MIMEApplication(f.read(), _subtype='pdf')
        att.add_header('Content-Disposition', 'attachment', filename=display)
        msg.attach(att)

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
payload = json.dumps({'message': {'raw': raw, 'threadId': 'THREAD_ID'}})

result = subprocess.run(
    ['gws', 'gmail', 'users', 'drafts', 'create', '--params', '{"userId":"me"}', '--json', payload],
    capture_output=True, text=True
)
print(result.stdout)
if result.returncode != 0:
    print("ERROR:", result.stderr)
PYEOF
```

> ⚠️ This draft is created in the **owning account** (the account where the client's label exists), not necessarily claims. Add env prefix if needed.
> ⚠️ Only attach **report** PDFs, not bills.
> ⚠️ Body 用 `multipart/alternative`（text + html），与 Step 6b 保持一致，确保 Gmail 能正常显示签名图片。

---

## Step 8.5 — Update Master Sheet Treatment Column

After sending the Chat summary, update the client's treatment column in the PI Master Sheet.

**Spreadsheet ID:** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`

### Tab → Treatment Column Mapping

| Tab | Chiro | MRI | PM | Other |
|-----|-------|-----|-----|-------|
| Claims@ sheetId=86730608 | J | K | L | M |
| Piteam@ sheetId=102974151 | M | N | O | P |
| Picase@ sheetId=775230687 | (check header) | | | |

### Step 8.5a — Find the client row:
```bash
gws sheets +read --spreadsheet '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM' --range 'TAB_NAME!A1:B200'
```
Match client name in Column B to get the row number.

### Step 8.5b — Update cell value:

**Determine what was received and update accordingly:**

| Received | Cell update | Background color |
|----------|------------|-----------------|
| Report + Bill (R/B) | Add `R/B` to entry | Change to **green** (see multi-visit rule below) |
| Bill only | Add `B` to existing entry | **Do NOT change** background color |
| Report only | Add `R` to existing entry | **Do NOT change** background color |

**Multi-visit R/B tracking rule:**
When a treatment entry has multiple visits (indicated by a number in parentheses and multiple dates, e.g., `5/15(2)-6/5 Vanguard`), R/B must be marked per individual visit date, not for the whole entry.

- Example: `5/15(2)-6/5 Vanguard` means 2 visits on 5/15 and 6/5
- Received 5/15's R/B → update to `5/15R/B(2)-6/5 Vanguard` (mark R/B after the specific date)
- Background stays **orange** — do NOT change to green yet
- Only change to **green** when ALL visit dates have R/B marked (e.g., `5/15R/B(2)-6/5R/B Vanguard`)

```bash
gws sheets spreadsheets values update \
  --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM","range":"TAB!CELL","valueInputOption":"RAW"}' \
  --json '{"values":[["NEW_VALUE"]]}'
```

Format: `DATE(TYPE)R/B PROVIDER` — e.g., `6/1(C)R/B Sun Imaging`
- (C)=Cervical, (L)=Lumbar, (T)=Thoracic, (Brain)=Brain MRI
- If bill only: append `B` to existing entry (e.g., `1/12(3)-6/18 Vanguard` → `1/12(3R/B-💉1)-6/18 Vanguard` when R/B both received; or just add `B` marker if only bill)

### Step 8.5c — Change background color to green (ONLY when both R and B are received):
```bash
gws sheets spreadsheets batchUpdate \
  --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM"}' \
  --json '{"requests":[{"repeatCell":{"range":{"sheetId":SHEET_GID,"startRowIndex":ROW_0BASED,"endRowIndex":ROW_0BASED+1,"startColumnIndex":COL_0BASED,"endColumnIndex":COL_0BASED+1},"cell":{"userEnteredFormat":{"backgroundColor":{"red":0.83137256,"green":0.92941177,"blue":0.7411765}}},"fields":"userEnteredFormat.backgroundColor"}}]}'
```

### Background Color Reference

| Color | RGB | Meaning |
|-------|-----|---------|
| Orange | R=0.98 G=0.74 B=0.02 | Treating / waiting for report |
| Green | R=0.83 G=0.93 B=0.74 | R/B **both** received (not bill-only or report-only) |
| Bright Yellow | R=1 G=1 B=0 | Referral received |
| Light Blue | R=0.76 G=0.91 B=1.0 | PM Recommendation received |

---

## Step 9 — Pin the Message

> Pinning is NOT supported via `gws` CLI. Inform the user to manually pin the message in Google Chat.

---

## Step 10 — Mark the Email as Read

```bash
gws gmail users messages modify --params '{"userId":"me","id":"MESSAGE_ID"}' \
  --json '{"removeLabelIds":["UNREAD"]}'
```

> ⚠️ Must not be skipped. `UNREAD` is what triage/automation uses to decide "still needs looking at" — it's a separate signal from the client label and from any downstream 待确认 flag left for a human. Once you've labeled, uploaded to Drive, sent the draft reply, and posted the Chat summary (Step 8.5's Sheet update, or a documented reason it was skipped, included), the email is fully handled and must not stay `UNREAD` — otherwise the next triage pass rediscovers it and reprocesses it from scratch (duplicate Drive upload, duplicate draft, duplicate Chat message). If you forwarded to a different owning account (Step 3b), mark **both** the original and the forwarded copy as read — they're separate messages with separate `UNREAD` state.

---

## Troubleshooting

### gws 403 "serviceUsageConsumer" error
The Google Cloud project needs the `Service Usage Consumer` role for the user.
Fix: Project Owner goes to `https://console.cloud.google.com/iam-admin/iam?project=PROJECT_ID` → Grant Access → add user email → role: Service Usage Consumer.

### gws Chat "insufficient scopes"
Run: `gws auth login --scopes "https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/documents,https://www.googleapis.com/auth/presentations,https://www.googleapis.com/auth/tasks,https://www.googleapis.com/auth/chat.spaces.readonly,https://www.googleapis.com/auth/chat.messages.create,https://www.googleapis.com/auth/chat.messages,https://www.googleapis.com/auth/chat.messages.readonly,https://www.googleapis.com/auth/chat.memberships.readonly"`

> ⚠️ Do NOT use `--services chat` alone — it replaces all other scopes. Always include all needed scopes together.

### gws Chat "app not found"
Need to configure Chat App in Google Cloud Console:
1. Go to `https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat?project=PROJECT_ID`
2. Disable "Enable Interactive features" toggle
3. Save

### Shared Drive files not found
Always include these params for shared drive operations:
```json
{"supportsAllDrives":true,"includeItemsFromAllDrives":true,"corpora":"allDrives"}
```

---

## Capabilities Summary

| Task | Method | Notes |
|---|---|---|
| Gmail search | `gws gmail +triage --query "..."` | ✅ |
| Gmail read | `gws gmail +read --id MSG_ID` | ✅ |
| Gmail attachment IDs | `gws gmail users messages get` | ✅ Parse JSON for parts |
| Gmail download attachment | `gws gmail users messages attachments get` | ✅ Pipe through python3 to decode base64 |
| Gmail labeling | `gws gmail users labels list/create` + `messages modify` | ✅ |
| Gmail draft reply | `gws gmail +reply --message-id ID --body TEXT --draft` | ✅ |
| Drive search (shared) | `gws drive files list` with `corpora:allDrives` | ✅ |
| Drive upload (shared) | `gws drive files create --upload FILE` with `supportsAllDrives` | ✅ Do NOT use `+upload` |
| Drive rename | `gws drive files update` with `supportsAllDrives` | ✅ |
| Chat find space | `gws chat spaces list --page-all` | ✅ Needs Chat scope |
| Chat send message | `gws chat +send --space SPACE --text TEXT` | ✅ Needs Chat scope |
| Chat pin message | Manual only | ❌ No CLI support |
