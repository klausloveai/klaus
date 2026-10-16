---
name: pm-recommendation
description: "Use this skill when processing incoming PM (Pain Management) recommendation or cost estimate emails for Lingtu Law PI cases. Covers: Gmail labeling + blue star → Drive upload to Referral folder → Chat notification → Sheet background color change. Trigger on any task involving 'PM recommendation', 'PM rec', 'cost estimate', or pain management recommendation documents."
author: Lingtu Law
---

# Lingtu Law — PM Recommendation Processing

Workflow for handling incoming PM (Pain Management) recommendation or cost estimate emails.

**All steps use the `gws` CLI only. Do NOT use MCP tools.**

### Account Usage Rules

| 操作 | 账号 | 环境变量前缀 |
|------|------|------------|
| Gmail (读取/label) | 用户指定 piteam 或 claims | piteam: 无前缀 / claims: `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claims` |
| Drive (搜索/上传) | 同 Gmail 账号 | 同上 |
| **Chat Space (查询/发送)** | **始终 claire.f** | **`GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-personal`** |

> ⚠️ 默认 `gws`（无前缀）实际登录的是 **piteam@lingtulaw.com**，不是 claire.f！

---

## Step 1 — Read Email & Download Attachments

**Step 1a — Read email:**
```bash
gws gmail +read --id MESSAGE_ID
```

**Step 1b — Get attachment IDs:**
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
hdrs = {h['name']:h['value'] for h in data['payload']['headers']}
print('---')
print('From:', hdrs.get('From',''))
print('Subject:', hdrs.get('Subject',''))
print('Message-Id:', hdrs.get('Message-Id',''))
print('ThreadId:', data.get('threadId',''))
"
```

**Step 1c — Download attachment:**
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

**Step 1d — Read PDF** using the Read tool to identify:
- Patient name
- Date of injury (DOI) / Date of examination (DOE)
- Recommended treatments (injections, referrals, diagnostics, conservative treatments)
- Medications
- Follow-up schedule

---

## Step 2 — Label Email & Add Blue Star

**Step 2a — Find the client's label:**
```bash
gws gmail users labels list --params '{"userId":"me"}' 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for l in data.get('labels', []):
    if 'CLIENT_NAME_KEYWORD' in l.get('name','').lower():
        print(f'{l[\"name\"]} -> {l[\"id\"]}')"
```

**If label not found, check Master Sheet before doing anything else** (search all 3 tabs — same as medical-records-sop Step 3b):
```bash
gws sheets +read --spreadsheet '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM' --range "'Claims@'!B1:B200"
gws sheets +read --spreadsheet '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM' --range "'Piteam@'!B1:B200"
gws sheets +read --spreadsheet '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM' --range "'Picase@'!B1:B200"
```

> ⚠️ **DO NOT** self-create a new label if the client isn't found in the current account. The client's case may actually be owned by a different mailbox.

If the client is in a **different tab** than the current email account, treat "forward to the owning account" and "label+blue-star the forwarded copy there" as **one atomic step** — do not stop after forwarding. **Blue star belongs ONLY on the owning-account copy, never on the current/receiving account's copy:**
1. Apply **only** the account ownership label (e.g., `PITeam` or `Claims`) to the message in the current account — `gws gmail users messages modify --json '{"addLabelIds":["OWNERSHIP_LABEL_ID"]}'`. Do **NOT** add `BLUE_STAR` here; skip Step 2b entirely for this message in the current account.
2. **Send** (not draft) forward to the owning account: `gws gmail +forward --message-id ID --to TARGET_EMAIL`
3. **In the owning account**, find the forwarded copy (`Fwd: ...` subject, from the sending account's address) and apply **both the client's case label AND `BLUE_STAR`** there in one call: `gws gmail users messages modify --json '{"addLabelIds":["LABEL_ID","BLUE_STAR"]}'`. Label alone isn't enough — blue star is what marks it as "待处理" (needs action) for whoever works that mailbox.
4. Continue with Steps 3–6 below (Drive upload, Chat notification, Sheet update) using the **owning account's** context. **Do not stop after Drive upload.** Caught in production on the sibling `referral` skill: a cross-account item got labeled, blue-starred, and uploaded to Drive, but Step 5's Chat notification to the client's own space was skipped entirely — only a separate internal rollup summary (from the calling automation, not this skill) went out, and nobody noticed until the client's Chat history was checked directly. The client-space Chat message in Step 5 is not optional and is not satisfied by any other summary elsewhere.

> Rule of thumb: blue star always lives with the client — one mailbox has the client label + blue star (the owning account), the other (if any) has only the routing/ownership label and no star at all.

If the client is in the **current tab**, proceed normally with the label found/created in the current account (this is the only case where Step 2b below applies to the current-account message).

**Step 2b — Apply label + blue star in one call (same-account case only — see above for cross-account):**
```bash
gws gmail users messages modify --params '{"userId":"me","id":"MESSAGE_ID"}' \
  --json '{"addLabelIds":["LABEL_ID","BLUE_STAR"]}'
```

---

## Step 3 — Upload to Drive Folder 4 > Referral

PM Recommendations go into the **Referral** subfolder inside Folder 4, NOT the root of Folder 4.

**Step 3a — Find client folder:**
```bash
gws drive files list --params '{
  "q":"name contains '\''ClientName'\'' and mimeType='\''application/vnd.google-apps.folder'\''",
  "fields":"files(id,name,parents)",
  "supportsAllDrives":true,
  "includeItemsFromAllDrives":true,
  "corpora":"allDrives"
}'
```

**Step 3b — Find Folder 4:**
```bash
gws drive files list --params '{
  "q":"name contains '\''4#'\'' and '\''CLIENT_FOLDER_ID'\'' in parents and mimeType='\''application/vnd.google-apps.folder'\''",
  "fields":"files(id,name)",
  "supportsAllDrives":true,
  "includeItemsFromAllDrives":true,
  "corpora":"allDrives"
}'
```

**Step 3c — Find Referral subfolder inside Folder 4:**
```bash
gws drive files list --params '{
  "q":"name='\''Referral'\'' and '\''FOLDER_4_ID'\'' in parents and mimeType='\''application/vnd.google-apps.folder'\''",
  "fields":"files(id,name)",
  "supportsAllDrives":true,
  "includeItemsFromAllDrives":true,
  "corpora":"allDrives"
}'
```

If no Referral subfolder exists, create one:
```bash
gws drive files create \
  --params '{"supportsAllDrives":true}' \
  --json '{"name":"Referral","mimeType":"application/vnd.google-apps.folder","parents":["FOLDER_4_ID"]}'
```

**Step 3d — Upload file:**
```bash
cp /tmp/filename.pdf ./filename.pdf
gws drive files create \
  --params '{"supportsAllDrives":true}' \
  --json '{"name":"PM Rec - Client Name","parents":["REFERRAL_FOLDER_ID"]}' \
  --upload ./filename.pdf \
  --upload-content-type application/pdf
rm ./filename.pdf /tmp/filename.pdf
```

**File naming:** `PM Rec - [Client Name]` (add date if duplicate, e.g., `PM Rec - Jing Wang 6-5`)

---

## Step 4 — NO Draft Reply

> ⚠️ PM Recommendation 邮件**不需要** draft reply。不要创建 "Received, thank you!" 草稿。

---

## Step 5 — Send Chat Space Notification

**Step 5a — Find Chat Space (必须用 claire.f 账号):**

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

**Step 5b — Send message with correct format:**

```bash
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-personal gws chat +send --space 'spaces/SPACE_ID' --text 'MESSAGE'
```

### Chat Message Template

```
📋 PM Recommendation (DATE, PROVIDER):

*建议治疗:*
[治疗项目1]
[治疗项目2]
...

💊 Medications: [药物列表]

[Client Name] 的 PM Recommendation 已保存至 [Client Name] [DOL] > 4#Folder > Referral

文件链接:
[File Name]: https://drive.google.com/file/d/FILE_ID/view
```

**Format rules:**
- `*建议治疗:*` 必须加粗（用 `*` 包围）
- 存储路径信息放在消息**最后一行之前**，文件链接放在**最后**
- 用简体中文
- 列出所有建议的治疗、诊断、转诊项目
- Medications 单独一行
- 文件链接使用上传时返回的 Drive file ID 构建 `https://drive.google.com/file/d/FILE_ID/view`，Chat 会自动渲染为 rich link 预览卡片
- ⚠️ 若邮件本身没有附件（纯文字follow-up，Drive中无新文件），**省略"已保存至"和"文件链接"两行**，不要编造不存在的存储路径

---

## Step 6 — Update Master Sheet

PM Recommendation 收到后，**不修改 Sheet 中的文字内容**，只将 PM 列的背景色改为**浅蓝色**。

**Spreadsheet ID:** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`

### Tab → PM Column Mapping

| Tab | PM Column | sheetId |
|-----|-----------|---------|
| Claims@ | L | 86730608 |
| Piteam@ | O | 102974151 |
| Picase@ | (check header) | 775230687 |

**Step 6a — Find client row:**
```bash
gws sheets +read --spreadsheet '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM' --range 'TAB!A1:B200'
```

**Step 6b — Change background to light blue (DO NOT modify text):**
```bash
gws sheets spreadsheets batchUpdate \
  --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM"}' \
  --json '{"requests":[{"repeatCell":{"range":{"sheetId":SHEET_GID,"startRowIndex":ROW_0BASED,"endRowIndex":ROW_0BASED+1,"startColumnIndex":COL_0BASED,"endColumnIndex":COL_0BASED+1},"cell":{"userEnteredFormat":{"backgroundColor":{"red":0.7607843,"green":0.90588236,"blue":1}}},"fields":"userEnteredFormat.backgroundColor"}}]}'
```

### Background Color Reference

| Color | RGB | Meaning |
|-------|-----|---------|
| Light Blue | R=0.76 G=0.91 B=1.0 | PM Recommendation received |
| Orange | R=0.98 G=0.74 B=0.02 | Treating / waiting for report |
| Green | R=0.83 G=0.93 B=0.74 | R/B received |
| Bright Yellow | R=1 G=1 B=0 | Referral received |

---

## Step 7 — Pin the Message

> Pinning is NOT supported via `gws` CLI. Inform the user to manually pin the message in Google Chat.

---

## Step 8 — Mark the Email as Read

```bash
gws gmail users messages modify --params '{"userId":"me","id":"MESSAGE_ID"}' \
  --json '{"removeLabelIds":["UNREAD"]}'
```

> ⚠️ This is separate from `BLUE_STAR` and must not be skipped. `UNREAD` is what triage/automation uses to decide "still needs looking at" — `BLUE_STAR` is the human-facing "待处理" signal. Once you've applied the label, uploaded to Drive, sent the Chat notification, and updated the Sheet background, the email is fully handled and must not stay `UNREAD`, or the next triage pass will rediscover and reprocess it (duplicate Drive upload, duplicate Chat message). If you forwarded to a different owning account (Step 2a), mark **both** the original and the forwarded copy as read — they're separate messages with separate `UNREAD` state.

---

## Key Differences from Medical Records SOP

| Item | Medical Records/Bills | PM Recommendation |
|------|----------------------|-------------------|
| Draft reply | ✅ "Received, thank you!" | ❌ No reply |
| Upload location | Folder 4 > client subfolder | Folder 4 > **Referral** subfolder |
| File name | `PM R` / `PM B` | `PM Rec - [Client Name]` |
| Blue star | No | ✅ Yes |
| Sheet update | Write date + R/B + provider, green bg | **Only change bg to light blue**, no text change |
| Chat format | Same template | Same template with `*建议治疗:*` bold |
