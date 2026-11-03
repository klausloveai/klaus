---
name: initial
description: Organize and archive client materials for a Lingtu Law case — scan the Shared Folder and Intake folder, identify and rename each file, copy it to the correct subfolder under 1. Initial, fill in the Fixed/Flexible info template, and track material completeness. Also handles drafting client replies and generating follow-up action lists. Triggers on keywords: "新文件", "状态", "回复", "回答", "下一步", or any request to process uploaded documents, check what's missing, reply to a client message, or plan next steps for material collection.
---

# initial — Material Organization & Client Communication (Lingtu Law)

This skill activates after `/it` has built the case folder. It covers everything between
receiving client documents and handing off to `/case`.

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Known constants

| What | Value |
|---|---|
| Pending cases root | `1RXWQsTkLdlIHUdbu2Rzs4HGH53tftzNm` |
| Case Tracking sheet | `1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE` |

---

## Trigger keywords

| 触发词 | 动作 |
|---|---|
| **「新文件」** | 扫描 Shared Folder，识别/重命名/归档所有新文件 |
| **「状态」** | 列出已收/缺失材料，判断当前阶段 |
| **「回复」** | 起草对客户最新消息的回复（内部注释版 + 可发出的客户版） |
| **「回答 [消息内容]」** | 针对指定消息起草客户回复 |
| **「下一步」** | 给出催件行动清单和建议措辞 |

If none of these exact words appear but the request is clearly about processing new uploads,
checking what's missing, replying to a client, or planning follow-up steps — treat it as
the most fitting trigger.

---

## 「新文件」— Scan and archive new documents

### Step 1 — Find the case folder

Ask for client name and case type if not in context. Locate the case root under `0. Pending`:
```bash
gws drive files list --params '{"q": "\"1RXWQsTkLdlIHUdbu2Rzs4HGH53tftzNm\" in parents and mimeType = \"application/vnd.google-apps.folder\" and name contains \"CLIENT_NAME\"", "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives"}'
```

Find both the `0. Shared Folder` ID and the `1. Initial` folder ID from the case root.

### Step 2 — List all files in Shared Folder

```bash
gws drive files list --params '{"q": "\"SHARED_FOLDER_ID\" in parents and trashed=false", "fields": "files(id,name,mimeType,createdTime)", "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives"}'
```

### Step 3 — Read and identify each file

Use `read_file_content` on each file — the Drive MCP does server-side OCR and text extraction.
Identify the document type based on content. Map to type codes:

| Type code | Document |
|---|---|
| `PASSPORT` | Passport (any country) |
| `VISA_[TYPE]` | Visa stamp (e.g. VISA_F1, VISA_B2) |
| `GREENCARD` | Permanent Resident Card |
| `BANK_[N]M` | Bank statement (N = months covered, e.g. BANK_6M) |
| `TAX_[N]Y` | Tax return (N = years, e.g. TAX_2Y) |
| `EMPLOYMENT_[EN/CN]` | Employment letter (language) |
| `DEGREE` | Diploma / degree certificate |
| `BIZ_REG` | Business registration |
| `CONTRACT` | Contract document |
| `PHOTO_ID` | ID photo (passport-style) |
| `MARRIAGE_CERT` | Marriage certificate |
| `BIRTH_CERT` | Birth certificate |
| `MISC_[描述]` | Anything else |

Check `1. Initial` for a checklist or tutorial doc — it overrides these defaults if the
case type has specific naming conventions.

### Step 4 — Rename and copy to Initial

New name format: `[ClientName]_[TypeCode]_[YYYYMMDD].[ext]`
Example: `ZhangSan_PASSPORT_20260830.pdf`

**Copy** (not move) to the matching subfolder under `1. Initial`. Originals stay in
`0. Shared Folder` untouched.

```bash
gws drive files copy --params '{"fileId": "SOURCE_ID", "supportsAllDrives": true}' \
  --json '{"name": "ZhangSan_PASSPORT_20260830.pdf", "parents": ["INITIAL_SUBFOLDER_ID"]}'
```

### Step 5 — Fill Fixed/Flexible template

Open the `I-[X] 材料信息模板 (Fixed 律所固定信息 + Flexible 客户信息)` doc in `1. Initial`.
Extract from the scanned documents: full name, A-number, DOB, SSN, passport number/dates,
green card number/dates, addresses, phone, email, employment, travel plan.
Append extracted info to the Flexible section of the template doc with `gws docs +write`.

### Step 6 — Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 本次处理：[文件列表]
📁 已归档至：[子文件夹]
📊 材料进度：已收 X / 共需 Y 项
⏳ 仍缺：[缺失材料，按重要程度排序]
👉 建议下一步：[具体行动]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 「状态」— Material progress check

List all files in `1. Initial`, compare against the case checklist doc.
Report: already received (with file names), still missing (sorted by importance),
current phase assessment, readiness for `/case`.

---

## 「回复」/ 「回答 [消息]」— Draft client reply

Read the latest client message from context (or the one provided after 「回答」).

Draft two versions:

**内部注释版**（供律所内部查看，含分析和注意事项）
```
[消息原文 / 摘要]
内部分析：[客户的核心问题/需求、涉及的材料状态、需要注意的法律或流程点]
建议回复策略：[应该包含什么、避免什么]
```

**客户版**（可直接复制发送至微信群，语气友好专业）
```
[你好，感谢...] → [直接回答问题] → [下一步行动] → [如有疑问随时联系]
```

Guidelines for the client-facing version:
- 中文为主，语气专业但不生硬
- 直接回答客户的问题，不绕圈子
- 如有下一步（需要客户提供材料/确认/行动），明确列出
- 结尾保持友好：「如有任何问题，随时联系律所 😊」
- 不超过 200 字（微信可读性）

---

## 「下一步」— Follow-up action list

Based on current material status, generate a prioritized action list:
1. What the firm needs to do (内部行动)
2. What to ask the client for (催件内容), with suggested WeChat message wording
3. Estimated timeline to `/case` readiness

---

## Logging & Tracking Sheet

### Activity Log format

```
[YYYY-MM-DD HH:MM PT] [OPERATOR] /initial — 操作描述
```

- **Author**: the actual team member for this session — `joe@lingtulaw.com` is shared by multiple staff. At session start, check context; if unclear ask once "请问今天是哪位同事在操作？" and reuse all session. Never write "Claude" or "AI".
- Timestamp: Pacific Time when the operation completes, precise to the minute.
- One entry per significant milestone, not per API call.

```bash
gws docs +write --document ACTIVITY_LOG_DOC_ID --text "\n[DATE TIME PT] [OPERATOR] /initial — 描述\n"
```

### Tracking Sheet — find client's row first

Spreadsheet ID: `1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE` — sheet `To Do List`

```bash
gws sheets get --spreadsheet-id 1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE \
  --range "To Do List!A3:P200"
```
Match column A on client name. Use that row number for all updates.

Column N (Case Status) — update after each run:
```bash
gws sheets update --spreadsheet-id 1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE \
  --range "To Do List!N{ROW}" --values "STATUS"
```

| Stage | Col N value |
|-------|-------------|
| In progress | `📂 材料整理中 X/Y YYYY-MM-DD` |
| Complete | `✅ 材料已归档 YYYY-MM-DD` |

Log after each meaningful action:
```
[DATE TIME PT] [OPERATOR] /initial — 归档 N 件: [文件列表] → 1. Initial | 进度: X/Y | 仍缺: [LIST]
[DATE TIME PT] [OPERATOR] /initial — 起草客户回复: [消息主题] | 两版已生成（内部注释 + 客户版）
[DATE TIME PT] [OPERATOR] /initial — 材料已齐全，可移交 /case
```

Update Tracking Sheet column N after each run:
- In progress: `📂 材料整理中 X/Y YYYY-MM-DD`
- Complete: `✅ 材料已归档 YYYY-MM-DD`
