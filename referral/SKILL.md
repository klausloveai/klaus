---
name: referral
description: "Use this skill when processing incoming medical referral (转诊单) emails for Lingtu Law PI cases. Covers: Gmail labeling + blue star → Drive upload to Referral folder → Chat notification → Sheet update with date+specialty+Ref and bright yellow background. Trigger on any task involving 'referral', '转诊', 'Ref' in the context of medical specialty referrals (acupuncture, neurology, orthopedic, PT, PM, etc.)."
author: Lingtu Law
---

# Lingtu Law — Referral Processing

Workflow for handling incoming medical referral (转诊单) emails.

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
- Patient name(s) — one email may have referrals for multiple clients
- Referring provider and specialty
- Target specialty (e.g., acupuncture, neurology, orthopedic)
- Reason for referral (symptoms/complaints)

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

If the client is in a **different tab** than the current email account, treat "forward to the owning account" and "label the forwarded copy there" as **one atomic step** — do not stop after forwarding. **Blue star belongs ONLY on the owning-account copy, never on the current/receiving account's copy:**
1. Apply **only** the account ownership label (e.g., `PITeam` or `Claims`) to the message in the current account — `gws gmail users messages modify --json '{"addLabelIds":["OWNERSHIP_LABEL_ID"]}'`. Do **NOT** add `BLUE_STAR` here; skip Step 2b entirely for this message in the current account.
2. **Send** (not draft) forward to the owning account: `gws gmail +forward --message-id ID --to TARGET_EMAIL`
3. **In the owning account**, find the forwarded copy (`Fwd: ...` subject, from the sending account's address) and apply **both the client's case label AND `BLUE_STAR`** there in one call: `gws gmail users messages modify --json '{"addLabelIds":["LABEL_ID","BLUE_STAR"]}'`. Label alone isn't enough — blue star is what marks it as "待处理" (needs action) for whoever works that mailbox. A forward that isn't labeled+blue-starred in the destination mailbox is effectively invisible to that mailbox's normal workflow — do not skip this.
4. Continue with Steps 3–6 below (Drive upload, Chat notification, Sheet update) using the **owning account's** context. **Do not stop after Drive upload.** Caught in production: a cross-account referral got labeled, blue-starred, and uploaded to Drive, but Step 5's Chat notification to the client's own space was skipped entirely — only a separate internal rollup summary (from the calling automation, not this skill) went out, and nobody noticed until the client's Chat history was checked directly. The client-space Chat message in Step 5 is not optional and is not satisfied by any other summary elsewhere.

> Rule of thumb: blue star always lives with the client — one mailbox has the client label + blue star (the owning account), the other (if any) has only the routing/ownership label and no star at all.

If the client is in the **current tab**, proceed normally with the label found/created in the current account (this is the only case where Step 2b below applies to the current-account message).

**Step 2b — Apply label + blue star in one call (same-account case only — see above for cross-account):**
```bash
gws gmail users messages modify --params '{"userId":"me","id":"MESSAGE_ID"}' \
  --json '{"addLabelIds":["LABEL_ID","BLUE_STAR"]}'
```

> ⚠️ 蓝星的 label ID 是 `BLUE_STAR`，不是 `STARRED`（那是黄星）。

---

## Step 3 — Upload to Drive Folder 4 > Referral

Referrals go into the **Referral** subfolder inside Folder 4.

**Step 3a — Find client folder → Folder 4 → Referral subfolder** (same flow as pm-recommendation Step 3a-3c).

If no Referral subfolder exists, create one:
```bash
gws drive files create \
  --params '{"supportsAllDrives":true}' \
  --json '{"name":"Referral","mimeType":"application/vnd.google-apps.folder","parents":["FOLDER_4_ID"]}'
```

**Step 3b — Upload file:**
```bash
cp /tmp/filename.pdf ./filename.pdf
gws drive files create \
  --params '{"supportsAllDrives":true}' \
  --json '{"name":"FILE_NAME","parents":["REFERRAL_FOLDER_ID"]}' \
  --upload ./filename.pdf \
  --upload-content-type application/pdf
rm ./filename.pdf /tmp/filename.pdf
```

**File naming:** `[Specialty] Ref - [Client Name]`
- Examples: `PM Ref - Jing Wang`, `Acu Ref - Ran An`, `Neuro Ref - John Doe`
- For multi-client referrals in one email, upload each as a separate file

---

## Step 4 — NO Draft Reply

> ⚠️ Referral 邮件**不需要** draft reply。Referral 是我们发出去请诊所转诊的，诊所回复附上 referral 单是正常流程，不需要再回复。

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

**Step 5b — Send message:**
```bash
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-personal gws chat +send --space 'spaces/SPACE_ID' --text 'MESSAGE'
```

### Chat Message Template

```
📋 [Specialty] Referral ([Referring Provider]):

[Client Name 1] — [symptoms] → 建议[specialty]治疗
[Client Name 2] — [symptoms] → 建议[specialty]治疗

[Client Names] 的 [Specialty] Referral 已保存至 [Folder Name] > 4#Folder > Referral

文件链接:
[File Name 1]: https://drive.google.com/file/d/FILE_ID_1/view
[File Name 2]: https://drive.google.com/file/d/FILE_ID_2/view
```

**Format rules:**
- 存储路径信息放在消息**最后一行之前**，文件链接放在**最后**
- 用简体中文
- 每个客户单独一行，列出症状和建议
- 文件链接使用上传时返回的 Drive file ID 构建 `https://drive.google.com/file/d/FILE_ID/view`，Chat 会自动渲染为 rich link 预览卡片

---

## Step 6 — Update Master Sheet

**Spreadsheet ID:** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`

### ⚠️ IMPORTANT: Check before updating

Before writing to the Sheet, check if the client already has treatment data in the target specialty column. If the column already has content (client is already treating in that specialty), the referral may be a late-arriving document — **DO NOT update the Sheet**, ask the user how to handle it.

### Step 6a — Find client row:
```bash
gws sheets +read --spreadsheet '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM' --range 'TAB!A1:B200'
```

### Step 6b — Find available column:
Read the client's row to find the next empty column. If all standard columns (J-M for Claims, M-P for Piteam) are used, continue to the next available column (N, O, P, etc.).

### Step 6c — Write referral info:
Format: `DATE [Specialty abbreviation] Ref`
- Examples: `6/10 Acu Ref`, `6/10 Neuro Ref`, `6/10 Ortho Ref`, `6/10 PT Ref`

Specialty abbreviations:
| Specialty | Abbreviation |
|-----------|-------------|
| Acupuncture | Acu |
| Neurology | Neuro |
| Orthopedic | Ortho |
| Physical Therapy | PT |
| Pain Management | PM |
| Chiropractic | Chiro |
| Psychology | Psych |
| Spine Specialist | Spine |

```bash
gws sheets spreadsheets values update \
  --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM","range":"TAB!CELL","valueInputOption":"RAW"}' \
  --json '{"values":[["DATE SPEC Ref"]]}'
```

### Step 6d — Set background to bright yellow:
```bash
gws sheets spreadsheets batchUpdate \
  --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM"}' \
  --json '{"requests":[{"repeatCell":{"range":{"sheetId":SHEET_GID,"startRowIndex":ROW_0BASED,"endRowIndex":ROW_0BASED+1,"startColumnIndex":COL_0BASED,"endColumnIndex":COL_0BASED+1},"cell":{"userEnteredFormat":{"backgroundColor":{"red":1,"green":1,"blue":0}}},"fields":"userEnteredFormat.backgroundColor"}}]}'
```

### Background Color Reference

| Color | RGB | Meaning |
|-------|-----|---------|
| Bright Yellow | R=1 G=1 B=0 | Referral received |
| Light Blue | R=0.76 G=0.91 B=1.0 | PM Recommendation received |
| Orange | R=0.98 G=0.74 B=0.02 | Treating / waiting for report |
| Green | R=0.83 G=0.93 B=0.74 | R/B received |

---

## Step 7 — Mark the Email as Read

```bash
gws gmail users messages modify --params '{"userId":"me","id":"MESSAGE_ID"}' \
  --json '{"removeLabelIds":["UNREAD"]}'
```

> ⚠️ This is separate from `BLUE_STAR` and must not be skipped. `UNREAD` is what triage/automation uses to decide "still needs looking at" — `BLUE_STAR` is the human-facing "待处理" signal. Once you've applied the label, uploaded to Drive, sent the Chat notification, and updated (or deliberately skipped) the Sheet, the email is fully handled and must not stay `UNREAD`, or the next triage pass will rediscover and reprocess it (duplicate Drive upload, duplicate Chat message). If you forwarded to a different owning account (Step 2a), mark **both** the original and the forwarded copy as read — they're separate messages with separate `UNREAD` state.

---

## Step 8 — Pin the Message

> Pinning is NOT supported via `gws` CLI. Inform the user to manually pin the message in Google Chat.

---

## Key Differences from Other SOPs

| Item | Medical Records/Bills | PM Recommendation | Referral |
|------|----------------------|-------------------|----------|
| Draft reply | ✅ "Received, thank you!" | ❌ No reply | ❌ No reply |
| Upload location | Folder 4 > client subfolder | Folder 4 > Referral | Folder 4 > Referral |
| Blue star | No | ✅ Yes | ✅ Yes |
| Sheet update | date + R/B + provider, green bg | Only change bg to light blue | date + specialty Ref, bright yellow bg |
| Sheet check | N/A | N/A | ⚠️ Check if already treating first |
