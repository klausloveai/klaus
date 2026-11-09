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
9a. **Lingtu Data 入档 —— 拿到编号**（查重 → 登记 → 挂案卷）。**没有编号不准进 Step 10**
10. Add the case to the tracking sheet, insert one row per client below the Example Row
11. Create the Google Chat case space, add the team, **promote Amos/Claire/CM to Manager**, ask user for case notes, post verbatim with the whole team's @mention list
12. Create the Gmail case label in the team mailbox (yellow)
13. Send the Docusign retainer — **ONLY if the prompt explicitly asks to send** (default = skip); when sending, `retainer type = new / standard` is a hard gate
14. **Output the client-facing signing message** (WeChat 文案 for Klaus to forward) — **always last, but only if Step 13 actually sent**
15. **完成闸门（Completion gate）** —— 逐项读回核对 Drive / Lingtu Data / Master / Chat / label 都真的建好了，再出最终回复。
16. **Final reply = `references/summary-format.md` only** — no analysis, no case-value opinions, no unsolicited to-dos

> The headings below (Step 1 – Step 14, plus Step 9a and the Completion gate) match this list exactly.

## Execution Mode

**Run all 14 steps end-to-end by default — do NOT pause for per-step confirmation.**
When the user has not said otherwise *in advance*, apply these defaults and keep going:
- Drive destination = **1. Pending**
- **Retainer = DO NOT send by default.** Steps 13 (Docusign retainer) and 14 (client signing
  message) are **skipped unless the prompt EXPLICITLY asks to send** — e.g. `new retainer`,
  `standard retainer`, or `send retainer`. If the prompt says nothing about the retainer, or says
  `retainer skip` / `retainer sent`, **skip both Step 13 and Step 14** (just note it in the summary).
  See the retainer gate below.
- CM assignment = **按信箱分，三个信箱轮转：`Claims@` / `Piteam@` / `Picase@`**（Klaus,
  2026-10-08）。**每一个新案都必须停下来跟 Klaus 确认 assign 给谁 —— 即使 prompt 里已经写了
  信箱或 CM 名字也要确认。** 确认时必须同时给出这三样：
  1. **上一次 assign 给了谁** —— 案件名 + 信箱 + 建档日期（从 Claims@ / Piteam@ / Picase@
     三个 tab 的最新行读，不要凭记忆）
  2. **上一案的人数构成** —— 几个成年人、几个 minor
  3. **本案的人数构成** —— 几个成年人、几个 minor
  4. **三个信箱当前的加权在手量** —— 见下方折算规则
  5. **Lingtu Data 登记字段**（Step 9a 要用，在这同一次确认里一起给 Klaus 看，不另停一次）：
     客户姓名、电话、`lead_source`（由 Referrer 推，见 Step 9a 对照表）、介绍人、`owner`，
     以及 `find` 查重结果（新客户 / 老客户 + 原编号 / 官网或总机已自动进库的线索）。
  6. **介绍人（Referrer）—— 必列，缺了就问**（Klaus 2026-11-08）：和 assign、合同类型、DOL 列在同一次确认里。
     取值顺序：Klaus 的 prompt → `find` 到的线索上已有的来源 / 介绍人 → intake。三处都没有 → **在这次确认里直接问 Klaus**，不猜、不留空往下走。
     客人是从登记链接 `lingtulaw.com/dengji?r=<码>` 进来的：`r` 码可以反解出介绍人（`@<数字>` 是合作方 ID，否则是人名）：
     `python3 -c "import base64,sys;c=sys.argv[1];b=base64.urlsafe_b64decode(c+'='*(-len(c)%4));k=b'lingtu-ref';print(bytes(x^k[i%len(k)] for i,x in enumerate(b)).decode())" <码>`
     反解出 `@<数字>` 时，把 ID 给 Klaus 看、问是哪家合作方，不自己对名字。
     确认后的介绍人同时用于：Master Referrer 列（`--referrer`）和 Lingtu Data `lead_source` / `referrer_name` / `source_detail`（Step 9a 对照表）。
  7. **修车行（车在哪修）—— 必列，缺了就问**（Klaus 2026-11-08）：intake 里有车行名 / 地址就照抄；没有 → 在这次确认里问 Klaus
     （Klaus 也可以回「还不知道」，就照写「未定」）。确认后写进 `log_lead` 的 `notes`，并列在最终回复里。
     介绍人就是修车行（如小朱修车）时，两项写同一个名字。

  > ⚠️ **2026-10-08 改口径**：以前是「只在 Jerry 和 Amos 之间轮」，现在 **Picase@ 回到轮转里**，
  > 三个信箱一起算。**少的那个就是 next assign**（Klaus 原话）；并列时规则选不出来，直接问 Klaus。

  **⚖️ 折算规则（Klaus 2026-09-22）：1 个 minor = 1/3 个成年人。**
  平衡看的是 **加权人头**，不是案件数、也不是原始人头：

  ```
  加权量 = 成年人数 + minor 数 ÷ 3
  ```

  > **为什么 minor 只算 1/3**：未成年人几乎总是跟着家长同车、同一场事故 —— 共用一份警察报告、
  > 一次责任调查、一套现场证据，增量工作主要只是多一份病历和多一次签署。所以「一家三口」
  > 远不等于「三个独立客户」的工作量。
  >
  > 反过来，**minor 案在结案端确实更重**（GAL 指定、Minor's Compromise 要过法院）—— 但那是
  > 几个月后的事，不在新案分配这个时点计入。分配看的是当下的建案与治疗跟进负荷。

  然后问："上一次是 [信箱]（[案名]，[N] 成年 / [M] minor）。三边当前加权：Claims@ [x.xx] /
  Piteam@ [y.yy] / Picase@ [z.zz]。这个案子（[N] 成年 / [M] minor，加权 [w.ww]）assign 给谁？"
  —— 等 Klaus 回答再往下走。绝不自动分配、绝不自己按轮转推断。
- Chat space "in charge" = the named CM (no default — must be either in the prompt or explicitly answered)

This Execution Mode overrides any "ask the user" / "Get user confirmation" wording in the
individual steps below (except the gates noted above). The user will state any deviation —
skip a step, hold the retainer as a draft, different retainer type/CM — up front.

**Retainer is DO-NOT-SEND by default (changed 8/11/2026).** Steps 13 + 14 run **only when the
prompt explicitly asks to send the retainer**. Decision tree:
- Prompt says nothing about retainer, or says `retainer skip` / `retainer sent` / `retainer already signed`
  → **skip Steps 13 + 14.** Do not ask about it. Just note "retainer skipped (not requested)" in the summary.
- Prompt explicitly asks to send AND names the fee type (`new retainer` / `standard retainer`)
  → run Steps 13 + 14 with that type.
- Prompt says to send but does NOT name the type (`send retainer` with no new/standard)
  → **this is the only case where you ask**: "这个案子用 new 还是 standard retainer？" — wait, then send.

**When sending, the FEE TYPE is still a hard gate** — never infer it from a template name or a
previous case; use exactly what the prompt says (or the answer to the question above).

| 类型 | 费用结构 | 典型适用 |
|---|---|---|
| **new** | **先付医疗费；扣除医疗费后剩余的金额，客户与律所各得一半（50%／50%）** | **小案子**：碰撞轻微、预计赔偿额低、治疗少或不治疗、走 early settlement。这类案子医疗费会吃掉赔偿的大部分，1/3 抽成对律所不划算。 |
| **standard** | **先扣律师费，再付医疗费，余额归客户。律师费分两档：诉讼前和解 = 赔偿总额的 1/3；进入诉讼 = 40%** | **常规案子**：正常伤情、要走完整治疗流程的。 |

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

> ⚠️ **超过 3 个客户（Klaus 2026-10-19）**：司机全名 + 其余客户首字母缩写，例
> `David Li Kwong-LZ-XZ-YM-BW-10-13-2026`（≤3 人仍用全名串）。Drive / intake 文件名 / Chat 群名 / 企微群名 /
> 签约文案标题用这串；Gmail label 用 `David Li Kwong/LZ/XZ/YM/BW`；tracking、DocuSign、intake 人名格子仍全名。

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
└── [CaseName]                    ← native Google Sheet in root (built locally as [CaseName].xlsx, converted on upload); name = DISK case name, nothing appended
```

> ⚠️ **Intake sheet filename (Klaus, 2026-09-24): `<DISK case name>.xlsx` — NO suffix.**
> `Mengmeng Wang-9-17-2026.xlsx` ✅ — not `Mengmeng Wang Intake Sheet.xlsx`,
> not `Mengmeng Wang-9-17-2026 Intake Sheet.xlsx`. The words "Intake Sheet" never appear
> in the filename. Same string as the case folder, dashes in the date. Local working copy is
> `.xlsx`; on Drive it is converted to a native Google Sheet with no extension (2026-11-03).
> (Older cases on Drive still carry the legacy ` Intake Sheet.xlsx` suffix — do not copy them.)

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
  -o "/Users/Klaus/work/[CaseName]/[CaseName].xlsx"
```

`[CaseName]` = the DISK case name (`Mengmeng Wang-9-17-2026`). The saved file is
`Mengmeng Wang-9-17-2026.xlsx` — **no ` Intake Sheet` suffix** (see Step 5).

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
  "<path>/<CaseName>.xlsx" --client-name "<Driver Name>"
```
It pairs every value with its label and asserts the value's TYPE matches the field
(Phone→phone number, Period→date range, Policyholder/Driver/Owner→person name, VIN→17 chars,
Email→has @, 1P Driver→must be our client), and flags values that smuggle in analysis.
**Exit code 2 = ERRORs present → fix and re-run before uploading to Drive.**
WARNs are advisory; review each one.

**Re-filling an existing case's sheet** (rules changed, or fixing an earlier fill): download the
live Drive copy first (`python3 scripts/intake_io.py fetch <id> live.xlsx` — works for both native
Sheets and legacy .xlsx) and diff it cell-by-cell against your new version before uploading. For a native
Sheet, write the changed cells back with `intake_io.py set`, never by re-uploading the xlsx.
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
python3 ~/.claude/skills/send-lor/scripts/match_carrier.py \
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

4. **Upload the intake sheet as a NATIVE Google Sheet** immediately — this gives you the `webViewLink` for Step 10:
   ```bash
   cd "/Users/Klaus/work/[CaseName]" && gws drive files create \
     --upload "[CaseName].xlsx" \
     --json '{"name":"[CaseName]","parents":["<CASE_FOLDER_ID>"],"mimeType":"application/vnd.google-apps.spreadsheet"}' \
     --params '{"supportsAllDrives":true,"uploadType":"multipart","fields":"id,name,mimeType,webViewLink"}'
   ```

   > ⚠️ **默认原生 Google Sheet（Klaus 2026-11-03：「我需要都默认 google sheet」）。** 推翻了
   > 2026-09-24「永远传 xlsx、不转换」的旧规则。本地仍用 openpyxl 填 `.xlsx` 并跑 `verify_intake.py`，
   > 上传时在 `--json` 里写 `"mimeType":"application/vnd.google-apps.spreadsheet"` 让 Drive 转换；
   > Drive 上的名字 = DISK case name，**不带 `.xlsx`**。转换实测无损（值 / 黄色高亮 / Nunito 字体全保留，
   > Jiuan Xiong 样本 round-trip 0 差异）。上传后核对返回的 `mimeType` 是
   > `application/vnd.google-apps.spreadsheet`，不是就删掉重传。
   > 原生 Sheet 才能挂 `Activity Log` subtab（案件 AL）。旧案的 `.xlsx` 不批量转换。
   >
   > **之后读写这张表**一律走 `scripts/intake_io.py`：`fetch` 两种格式都导出成本地 xlsx（只读）；
   > 写值用 `set`（Sheets API）。**绝不**把本地 xlsx `files update --upload` 覆盖回原生 Sheet ——
   > 那会把它变回 xlsx 文件。
   >
   > ⚠️ **`uploadType:multipart` + mimeType in `--json`.** Declaring `uploadType:media` while
   > sending a multipart body embeds the MIME headers INTO the file and silently corrupts it
   > (3 files corrupted 2026-09-17 → 09-23, one undetected for 6 days).

4a. **建案件 AL tab + 登记 registry**（Klaus 2026-11-03：「加上 al.py init」）。intake 一上传成原生 Sheet
   就建，不等第一次有人写：
   ```bash
   python3 ~/lingtu-cm-study/al/al.py init <INTAKE_SHEET_ID>
   ```
   - 用 Klaus@ 默认身份跑（al.py 拒绝 team 邮箱身份写 AL）；输出「已建「Activity Log」tab」或「已存在」都算过。
   - 然后在 `~/lingtu-cm-study/al/registry.json` 的 `cases` 里追加一条（同名同 DOL 已有就不加；同名不同 DOL 分开登记）：
     `{"case": "<司机姓名>", "dol": "MM/DD/YYYY", "sheet_id": "<INTAKE_SHEET_ID>", "type": "native", "al": true}`。
     一车多人：每人一条，`sheet_id` 相同。
   - 只建表头，**不写行**：建案本身记在 Lingtu Data（Step 9a）和中央 Activity Log，不在这里重复。
   - 上传回来的 `mimeType` 不是原生 Sheet（第 4 步要求删掉重传）时，先重传再 init，xlsx 上建不了 tab。

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

## Step 9a — Lingtu Data 入档（拿编号）

> **2026-11-02 起每个新案必做（Klaus：「有的时候还是会跳过入档，我放进 skill 里应该都可以确保
> 案件正确入档有编号」）。** 编号是系统生成的，照系统给的用，**绝不自己编、不手改**。
> 规则来源：`lingtu-data` skill（分流、来源、敏感信息）。这里只写 new-case 里怎么接。

**位置**：Step 9 上传 Drive 之后（要用案卷链接）、Step 10 写 Master 之前（Master A 列要用编号）。
**Step 10 的脚本 `--case-id` 是必填参数 —— 没有编号就写不了 Master 行，这一步跳不过去。**

0. **登记要的信息**（大部分从 intake 自己取，只有标 ★ 的要 Klaus 在开头一起给）：

   | 字段 | 从哪来 |
   |---|---|
   | 司机姓名、电话、email、所在城市、DOL、一句话案情、乘客姓名 | intake |
   | 案件类型（车祸 / 狗咬 …） | intake |
   | ★ 来源（怎么知道凌图的）+ 介绍人姓名 / 车行名 | Klaus；intake 的 Referrer 能对上就直接用 |
   | ★ 有没有先发登记链接给客人填过 | Klaus（说了就按下面第 1 步先找那条） |
   | 微信号（资料卡上的，不是昵称） | 可选，有就填 |

1. **查重（必做，客人可能已经自己填过登记链接）**：
   - `find` 依次查：**司机电话 → email → 微信号 → 英文名 → 中文名**。客人自己填表时常写中文名或别的拼法，
     所以**电话优先**，姓名只做补充。
   - `log_lead` 本身也会查重：返回「有相似客户」时**不写入**，把候选列给 Klaus 确认，再按下面规则重试。
   - 查到**客人自己填的登记表 / 官网 / 总机已自动进库**的线索 → 直接用它的编号，**不要再 `log_lead`**；
     intake 里有而线索上缺的（如来源、介绍人），只在它们是空的时候用 `update_lead` 补，先给 Klaus 看。
   - 查到**老客户**（电话对上）→ `log_lead` 带 `existing_client_code=<原编号>`、`lead_source=returning_client`。
   - 只是**重名、电话对不上** → 是另一个人，`log_lead` 带 `confirm_new_client=true`。重名不同人本来就该是不同编号。
   - 拿不准是不是同一个人 → 停下来问 Klaus。
2. **登记**（`log_lead`，字段已在开头的 assign 确认里给 Klaus 看过）：
   - `name` = 司机全名；`phone`、`email` 取 intake；`channel=staff_entry`
   - `case_type` = `car_accident`（狗咬 `dog_bite`，其他见 `options`）
   - `summary` = 一句话案情（DOL、事故类型、几位客户），**不写 SSN、DL#、DOB、地址**
   - `notes` = 同案乘客姓名、分派的信箱和 CM
   - `lead_source` 由 Master 的 Referrer 推：

     | Referrer 写的 | `lead_source` |
     |---|---|
     | `<名字>老客户介绍` / 朋友介绍 | `client_referral` + `referrer_name=<名字>` |
     | 老客户本人（「老客户（M/D/YYYY 案）」） | `returning_client` + `existing_client_code` |
     | `Klaus朋友圈` | `wechat_article` |
     | 修车行 / 车行（如「小朱修车」） | `partner` + `source_detail=<车行名>` |
     | `Cindy Intake` 或空白 / 对不上 | **问 Klaus**，不猜；客人确实不记得才用 `unknown_asked` |

   - `owner` 按 `lingtu-data` 分流：广告 / 官网 / 地图 / AI 搜索 / 社媒来的 → `Cindy`；
     朋友或老客户介绍、车行、到访、来源不明 → `Klaus Liu`。
3. **记下编号**：`log_lead` 返回客户编号（5 位）。PI 的案件编号（`12345-PI1`）要到 `sign_lead`
   才生成 —— retainer 发出后在 **Step 13b** 签（contingency 选项 Joe 已加好，2026-11-05 确认）。
   Step 10 时还没有案件编号，Master A 列先写**客户编号**，Step 13b 签约后换成案件编号。
   老客户第二个案子同理，签约后系统会排出 `-PI2`。retainer 不发（skip）的案子不签，A 列保持客户编号。
4. **挂案卷**：放到 Step 13b 签约之后做（没有案件挂不上）。retainer skip 的案子在最终回复里写明「案卷未挂，签约后补」。
5. **记一笔**：`log_event`（`action=note`，挂客户编号）
   「新案建档：Drive 案卷 1. Pending、Master <tab>、分派 <CM>」，`link` = Drive 案卷。
6. **读回核对**：再 `find` 一次，确认客户、线索、编号都在库里。**`find` 查不到就不算完成。**
7. **企微群认领口令**（Klaus 2026-11-08 定）：工作台「企微群」页每 5 分钟抓一次客户群；群里出现
   「本群客户编号 XXXXX」（签约后是「本群案件编号 XXXXX-PI1」）就自动把这个群认领到该编号，之后群消息和附件都归这个案子。
   最终回复 §8 在企微群名下面给出口令；**签约文案代码块最上面也要列出口令**（Klaus 2026-11-08：「这个客户签约文案也需要列出在最上面即可」，见 Step 14），
   旧做法「单独一行、单独一条消息发、不夹在签约文案里」作废
   （工作台能不能从长段落里认出编号，尚未确认）。拉群时多半还没签约 → 发客户编号；签约后系统自动转挂到案件，不用再发。
   已签约（13b 已跑）才拉群 → 直接发案件编号。一车多人：每个有编号的客户各一行；一个群能不能认领多个编号尚未确认，
   发完到工作台「企微群」→「已认领」核对，没认上的在「待认领」里点「选客户 / 案件」手动挂。

**同案多位客户**：一个案子登记一条线索（司机名下），乘客写进 `notes`，Master 里司机和乘客行用同一个编号
（库里已有的先例：48845-PI1 Kuang Yu Feng & Hui Lin Huang）。乘客本人以后自己再来办案，再单独登记。

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

### 🔧 Gate 3 — use the script, do NOT hand-roll the API calls

```bash
python3 ~/.claude/skills/new-case/scripts/add_tracking_row.py \
  --tab Piteam@ --dol 9/10/2026 --client "Xianyong Hou" \
  --sheet-id <intake sheet Drive file id> \
  --retainer "Standard 1/3" --retainer-sent 9/10 \
  --case-id <Step 9a 拿到的编号> \
  [--referrer "..."] [--passenger "Name"]...
```

It reads the LIVE header, inserts N rows below row 2, **copies the Example Row into them**, then
writes only the case fields (DOL / hyperlinked client name / retainer / referrer / status /
`Retainer sent M/D`), clearing the 1LOR–Property Damage block on passenger rows. `--dry-run`
prints the payload without touching the sheet.

> ⚠️ **Every hand-rolled attempt so far has produced a broken row.** Writing
> `insertDimension` + `values update` from memory skips the row-2 copy, so the row loses
> Property Damage `Ask Klaus` and the clinical defaults, and the Client Name lands as plain text
> with no link to the intake sheet — plus Note-Claims never gets the retainer date.
> (Zhe Ji 9/8, Xianyong Hou 9/10 — both had to be repaired by hand.) **Run the script.**
> The prose below documents what the script does and the column semantics; it is reference, not
> a set of steps to execute manually.

**Spreadsheet:** "PI Master Sheet" — ID `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`
**Tabs = the mailbox itself:** `Claims@` · `Piteam@` (sheetId `102974151`) · `Picase@` (sheetId `775230687`).
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

**Write the SAME value on EVERY client row — driver AND every passenger** (updated 8/19/2026).
All clients on one case sign the same retainer, so the column must read identically down the
whole case block; a blank passenger cell makes it look like that client never signed.

> ⚠️ **Changed 8/19/2026.** Previously this said "driver row only, leave passenger rows blank."
> That was wrong — Klaus corrected it. Passenger rows now carry the identical retainer label.

### Per-client row format

| Column | Driver row | Passenger row |
|---|---|---|
| DOL (A) | Date of Loss (M/D/YYYY) | leave blank |
| Client Name (B) | `=HYPERLINK("<intake sheet webViewLink>","Firstname Lastname")` — name only, no CM tag | plain text `"Firstname Lastname"` — **no hyperlink, no CM tag, no "(minor)" tag** |
| Retainer (C) | `Standard 1/3` or `New 50%` (per table above) | **same value as the driver — never blank** |
| Referrer (D) | 开头确认里定下的介绍人（第 6 项），用 `--referrer` 写；Klaus 没定就留空并在最终回复里标出 | leave blank |
| Case Status (E) | `✒️Signing`；Klaus 说 `retainer signed` → `⚠️Pending`（`--status`） | same as driver |
| Note-Claims (F) | `Retainer sent M/D` | same text + same blue formatting (keep from template copy; see background rule below) |
| 1LOR → Property Damage (G–M; **F–L on Claims@**) | keep Example Row values — do not override | **EMPTY + no color** — clear all 7 values *and* reset their background to white; one case only needs one primary record row |
| Ambulance → Health Ins Lien (cols N–T) | **keep Example Row template values (P / Pending) — do NOT pull from intake** | keep Example Row template values |
| Outstanding Balance → MRI (cols U–X) | keep Example Row values | keep Example Row values |

> ⚠️ **Policy (7/26/2026): do NOT populate the clinical/status columns from the intake.** When
> adding a new case, copy the template down from row 2 and leave **everything at default** except:
> DOL (A), Client Name (B), Retainer version (C), and Note-Claims (F) = `Retainer sent M/D`. The
> clinical/liability columns — 1LOR→Property Damage (G–M) and Ambulance→Health Ins Lien (N–T) —
> stay at their template `P`/`Pending` defaults; **the assigned CM follows up and confirms each
> later.** This replaces the earlier behavior of writing Ambulance/Emergency/Urgent Care/…/Health
> Ins from the intake sheet — no longer do that.

**Passenger row background rule — four zones, addressed BY HEADER NAME, not by letter:**

| Zone | Picase@ / Piteam@ | Claims@ | Action |
|---|---|---|---|
| `DOL` … `Case Status` | A–E | **A–D** | clear to **white** |
| `Note-Claims` | F | **E** | **untouched** (keep template blue) |
| `1LOR` … `Property Damage` | G–M | **F–L** | **values emptied AND background cleared to white** |
| `Ambulance` … end | N–X | **M–X** | **untouched** (keep template yellows) |

> ⚠️ **Claims@ has no `Retainer` column, so every block sits one column to the LEFT of
> Picase@/Piteam@.** Hardcoding `G–M` therefore leaves the passenger row's `1LOR`→`Property
> Damage` block orange on Claims@ while whitening a column that should have stayed yellow.
> Klaus caught exactly this on Shenglin Li / Perla Abigail Alvarado Vazquez (2026-09-16):
> "passenger的 F-L应该是empty no color". **Derive both zones from the LIVE header row** —
> `add_tracking_row.py` now does this automatically; never write the letters from memory.

**Emptying the value is not enough — the background must be cleared too.** A passenger row whose
`1LOR`→`Property Damage` cells are blank but still orange reads as "this row has an open LOR/PD
task", which is the opposite of the intent.

### Workflow

1. The assigned mailbox IS the tab: `Claims@` / `Piteam@` / `Picase@`.
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
   - **Passenger rows (row 4 onward):** plain text `"Firstname Lastname"` (col B — no hyperlink);
     **col C (Retainer) = the SAME label as the driver row** (`Standard 1/3` / `New 50%` — write it
     explicitly, do not leave blank); clear cols G–M (write 7 empty strings);
     cols N–T keep template values (already from copyPaste — do not overwrite); col F (Note) gets the
     same `Retainer sent M/D` text as the driver row (see step 7).
   - **Cols U–X (Outstanding Balance → MRI):** leave exactly as copied from Example Row.

   > ⚠️ **Case Status (col E) must NOT be written as empty string.** When building the values array
   > for the batchUpdate, omit column E entirely — or write `"✒️Signing"` explicitly. If you pass
   > `""` for E, it overwrites the template value that `copyPaste` set. The same applies to cols
   > N–X — never include them in the values write even as placeholders.
   >
   > Safest pattern: write only the columns you're actually changing (A, B, C for driver;
   > **B, C, G–M for passenger**). Do not write a full A–X row with empty strings for the untouched columns.
6. **Background rules for passenger rows — three zones:**
   **Resolve every index from the live header — Claims@ is shifted one column left (no Retainer column).**
   The letters below are the Picase@/Piteam@ case; on Claims@ they become A–D / E / F–L / M–X.
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

**Members = BASE (always, every case) + that case's TEAM ROSTER. Klaus is the creator and is
added automatically as owner — he is in every space.**

**BASE (all cases — 3 people):** `cassie@lingtulaw.com`, `claire.f@lingtulaw.com`, `amos.f@lingtulaw.com`

**Team roster — add ONLY the roster of the mailbox that owns the case. Never add another team's people.**

| Mailbox | Team roster to add | CM |
|---|---|---|
| **Claims@** | `taki.x@lingtulaw.com` *(Amos already in BASE)* | Amos |
| **Piteam@** | `jerry.p@lingtulaw.com` + `angelina.m@lingtulaw.com` + `kiko.w@lingtulaw.com` | Jerry |
| **Picase@** | `jenkins.l@lingtulaw.com` + `tiana.d@lingtulaw.com` *(eeve.l@ 已离职 2026-10-22)* | Jenkins |

> ⚠️ **Rewritten 2026-10-08 (Klaus) — this REPLACES the 9/18 roster.** Klaus's words:
> `claims@ = amos + taki + eeve` · `piteam@ = amos + jerry + angelina + kiko` ·
> `picase@ = amos + jenkins + tiana` · 所有都有 cassie and claire。
>
> Changes from 9/18:
> 1. **`may.z@`, `ryan.w@` and `lyne@` are GONE — all three have left the firm. Never add any of them to any space.**
> 2. **`amos.f@` is now in every team** (he was already BASE; Klaus now names him in all three).
> 3. **`taki.x@` moved Picase@ → Claims@**; **`eeve.l@` (Yulu) joined Claims@** —
>    ⚠️ **superseded 2026-10-12: `eeve.l@` moved Claims@ → Picase@**, learning CM alongside Jenkins.
> 4. **`jenkins.l@` replaced Ryan as the Picase@ CM.**
> 5. **The `Klaus@` row is deleted** — cases go to the three mailboxes only.
>
> `joe@lingtulaw.com` — removed from BASE 8/7/2026, still never added.
> `jessie.l@lingtulaw.com` — left the firm 8/18/2026, **never add her to any space.**
> `lyne@lingtulaw.com` — left the firm (confirmed 2026-10-08), **never add her to any space.**

**Suffix in space name:** Claims@ → `(A)`, Piteam@ → `(J)`, Picase@ → **`(Z)`**.

> ⚠️ **Corrected 2026-10-12.** The skill said Picase@ → `(R)`. It is **`(Z)`** — a live scan of all
> 618 Chat spaces found **87 `(Z)` spaces and ZERO `(R)` spaces**; every Picase@ case on the board
> (e.g. `Amanda Luo-Lucas Yu-8-28-2026(Z)`) carries `(Z)`. `(K)` is the retired Klaus@ line.

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
   for EMAIL in cassie@lingtulaw.com claire.f@lingtulaw.com amos.f@lingtulaw.com \
                <that mailbox's roster...>; do   # BASE 3 + the owning mailbox's roster
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
   **Expected totals (BASE 3 + that mailbox's roster + Klaus as owner) — updated 2026-10-08:**

   | Mailbox | Members in the space | Total |
   |---|---|---|
   | **Claims@** | Cassie · Claire · Amos · Taki · Klaus | **5** |
   | **Piteam@** | Cassie · Claire · Amos · Jerry · Angelina · Kiko · Klaus | **7** |
   | **Picase@** | Cassie · Claire · Amos · Jenkins · Tiana · Klaus | **6** |

   If the count is short, add the missing members with another `members create` call.

2b. **Set Klaus's notification for this space to "For you" — ALWAYS, right after creating it**
   (Klaus 2026-10-23: 「创建 chat 第一时间把 notification 调成 For you，only mention 我才能看到，所有新案子都这样」).
   This is Klaus@'s own per-user setting (`users/me`), so it does not affect anyone else in the space:
   ```bash
   gws chat users spaces spaceNotificationSetting patch \
     --params '{"name":"users/me/spaces/XXXX/spaceNotificationSetting","updateMask":"notification_setting"}' \
     --json '{"notificationSetting":"FOR_YOU"}'
   ```
   Verify with `... spaceNotificationSetting get` → `"notificationSetting": "FOR_YOU"`.
   Needs scope `chat.users.spacesettings` on Klaus@ (added 2026-10-23 via `bash ~/gws_chat_login.sh`).
   **If it returns 403 insufficient scopes → do it in the built-in browser in the same run. Reporting
   the 403 is NOT completing the step** (Klaus 2026-10-27: 「这个说过好几次了怎么没有履行」— three cases
   in a row were left on "Main conversations" because the 403 was only reported):
   navigate `https://chat.google.com/u/1/room/<SPACE_ID>` (klaus@ = `u/1`) → click the space name (≈ x300,y75)
   → menu item **Notifications** → radio **For you** → **Save** → reopen the menu and confirm the item reads
   `Notifications · For you`. ⚠️ The menu shifts after opening — screenshot before every click; **Mute** sits
   right above Notifications (mis-click once → hit Undo on the toast).

3. **Promote to Manager — ALWAYS. Amos, Claire and the assigned CM get the Manager role.** (On a Claims@ case the CM *is* Amos, so the list is just Amos + Claire.)
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
   # promote list = amos.f + claire.f + the assigned CM (Claims@: amos.f + claire.f only)
   for EMAIL in amos.f@lingtulaw.com claire.f@lingtulaw.com <CM_EMAIL>; do
     MID=$(gws chat spaces members get --params "{\"name\":\"spaces/XXXX/members/$EMAIL\"}" 2>&1 \
       | grep -v '^Using' | python3 -c "import sys,json;print(json.load(sys.stdin)['member']['name'].split('/')[-1])")
     gws chat spaces members patch \
       --params "{\"name\":\"spaces/XXXX/members/$MID\",\"updateMask\":\"role\"}" \
       --json '{"role":"ROLE_ASSISTANT_MANAGER"}'
   done
   ```

   **Verify** by re-listing and confirming they show `ROLE_ASSISTANT_MANAGER`
   (Klaus will show `ROLE_MANAGER` as the space owner — that is correct, leave it):
   ```bash
   gws chat spaces members list --params '{"parent":"spaces/XXXX"}' 2>&1 | grep -v '^Using' | \
     python3 -c "
   import sys, json
   for m in json.load(sys.stdin).get('memberships', []):
       print(m.get('member',{}).get('name'), m.get('role'))
   "
   ```

4. **Resolve user IDs for the @mentions — @ EVERYONE in that mailbox's team (Klaus, 2026-10-08:
   「每次 at 就 at 组里的人」):**

   | Mailbox | @mention, in this order |
   |---|---|
   | **Claims@** | `amos.f@` + `taki.x@` |
   | **Piteam@** | `jerry.p@` + `angelina.m@` + `kiko.w@` + `amos.f@` |
   | **Picase@** | `jenkins.l@` + `tiana.d@` + `amos.f@` |

   > ⚠️ **Changed 2026-10-08.** Two changes from the 9/17 rule:
   > 1. **The whole group gets @'d, not one support person.** The old list named only one CA per
   >    team (May / Angelina / Tiana) and left Kiko / Taki out — that open item is now closed:
   >    **everyone in the mailbox's roster is mentioned.**
   > 2. `may.z@`, `ryan.w@` and `lyne@` are gone (left the firm); `taki.x@` is Claims@;
   >    `jenkins.l@` is the Picase@ CM.
   >
   > **Order:** the CM first, then that team's support people, and **`amos.f@` LAST on Piteam@ /
   > Picase@** — he is cc'd as supervisor, not the lead. On Claims@ Amos *is* the CM, so he leads.
   >
   > `cassie@` and `claire.f@` are space members but are **not** @mentioned.
   >
   > Everyone in the mention list is already a space member, so no extra `members create` call is
   > needed — but re-verify before posting; a mention of a non-member renders as plain text with no
   > notification.

   Resolve each one's numeric id:
   ```bash
   gws chat spaces members get --params '{"name":"spaces/<SPACE>/members/<email>"}'
   # -> member.name = users/<numericId>
   ```

> ⚠️ **2026-10-17 (Klaus)：@ 至少 CM + CA + CM supervisor Amos。** Picase 已拆成 Picase@(Amos)/(Jenkins)/(Eeve) 三个 tab，
> 按案子所在 tab 定 CM —— Picase@(Jenkins) 案 = `jenkins.l@` + `tiana.d@` + `amos.f@`（不 @ Eeve）。
> **没有 case notes 也要立刻发** `@CM @CA @Amos new case`，不能停着等 —— 群建好没人被 @ 就等于没分配。笔记来了再原话补发一条。

> ⚠️ **改派（Klaus 2026-10-19）：** 建完案后改 assign 到别的信箱/tab 时，重发新组的 `@CM @CA @Amos new case` 之后，
> **把之前 @ 错人的那条 new-case 消息删掉**（`gws chat spaces messages delete`，只删 Klaus@ 自己发的那条）。
> 全套挪动清单见 memory `feedback_case_reassign_checklist`。

5. **PAUSE — ask the user for their case notes.** After the space is created and all members are verified,
   stop and prompt the user:
   > "Chat 空间已建好，请留言你对这个案子了解的信息，我会原话复制粘贴 @ 给该案的 mention 名单。"
   Wait for the user's reply before posting anything.

6. **Post the user's text verbatim** — prepend the @mentions, then paste the user's exact words
   unchanged. Use Python `json.dumps()` to encode the message body:
   ```python
   import json, subprocess
   user_notes = "<user's verbatim reply — do NOT edit, translate, or reformat>"
   mentions = " ".join(f"<users/{i}>" for i in MENTION_IDS)   # order per the step-4 table
   status_line = "<retainer 状态句，见下表>"
   msg = {"text": f"{mentions} new case\n\n{user_notes}\n\n{status_line}"}
   subprocess.run(["gws", "chat", "spaces", "messages", "create",
     "--params", '{"parent":"spaces/XXXX"}',
     "--json", json.dumps(msg, ensure_ascii=False)])
   ```
   Verify the response `annotations` contain `USER_MENTION` entries for each @mentioned person.
   **Do NOT add, edit, translate, or reformat the user's text in any way.**

   **Retainer 状态句 —— 每条 new-case 消息末尾固定加一行（Klaus 2026-11-05：「发到 chat 里的内容之后都默认加一下」）：**

   | Klaus 的 prompt | 状态句（逐字，M/D 换成实际日期） | Master Case Status |
   |---|---|---|
   | 发合同（`new retainer` / `standard retainer`） | `M/D 合约已发出，等待客户签约后启动。` | `✒️Signing` |
   | `retainer signed` / `retainer signed, skip` | `客人已经签约，我们可以启动。` | **`⚠️Pending`**（`add_tracking_row.py --status "⚠️Pending"`） |
   | 只说 skip、没说签没签 | 不加状态句 | `✒️Signing` |

   M/D = Step 13 实际发出 retainer 的日期（Step 11 在 Step 13 之前跑时，按今天写；没发出就回头删掉这一句）。
   `retainer signed` 的案子同样走 Step 13b 签约挂 CM —— 合同类型从 DocuSign 已签的 envelope 主题 `(New)` / `(Standard)` 读，读不到就问。

   > 🔒 **The message body is a CLOSED SET: the step-4 @mention list + one case-name line + Klaus's notes verbatim + the retainer 状态句 above.
   > Nothing else may appear in it. Ever.** The following are all FORBIDDEN in the Chat message,
   > no matter how useful they look:
   > - **Drive folder link / intake-sheet link / any URL** (the team opens the case from Drive and
   >   the tracking sheet; a link here is noise and Klaus has said so explicitly, 2026-09-11)
   > - Facts extracted from the documents (insurer, policy#, VIN, plate, DL, adjuster, claim#)
   > - Injury / damage / treatment descriptions
   > - Liability analysis, coverage theories, respondeat superior, policy-limit estimates,
   >   case-value opinions, "这案子底子很硬"-type characterizations
   > - ⚠️/CRITICAL flags, to-do lists, next steps, "需要核实" items
   > - DOL / retainer type / CM restated as a header line beyond the plain case name
   >
   > **Everything in that forbidden list belongs in the Step 8 output summary to Klaus
   > (`references/summary-format.md`), NOT in Chat.** If you have found something urgent, it goes
   > in the summary under §6 Critical Flags and Klaus decides whether the team hears it.
   >
   > Violated twice (Ben Li 2026-08-03; Zhe Ji + Xianyong Hou 2026-09-10). Both times the cause was
   > running Step 11 from memory of earlier cases instead of re-reading this step. **Re-read this
   > block before composing the message, every case.**

7. **Set the ⚠️ `:warning:` space emoji avatar — MANUAL.** The Chat API Space resource has no
   avatar/emoji field, so this can't be set via API. Give the user the `spaceUri` and tell them
   to set it once in the UI (Space details → emoji → `:warning:`).
8. **Confirm:** report the space name, link (`spaceUri`), members added (verified count), and the posted mention.
9. **Self-check before moving on.** Re-read the message you just posted and confirm it contains
   ONLY: the @mentions, the case-name line, and Klaus's notes. If it contains a URL, a document
   fact, or any analysis, `gws chat spaces messages patch` it back down immediately —
   `--params '{"name":"<message name>","updateMask":"text"}'`.

### Auth note (Chat scopes)
All Chat calls use the **default `gws` (Klaus@ account)** — never picase@/piteam@ config dir.
Klaus@ needs `chat.spaces`, `chat.messages`, `chat.memberships`, `chat.users.spacesettings` (the last one for step 2b). **Use `bash ~/gws_chat_login.sh` — it carries the full current scope list and re-exports `credentials.json`.** The interactive
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

| Tab / mailbox | Team mailbox | gws config |
|---|---|---|
| `Claims@` (Amos) | claims@lingtulaw.com | `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-claims` |
| `Piteam@` (Jerry) | piteam@lingtulaw.com | `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-piteam` |
| `Picase@` (Jenkins) | picase@lingtulaw.com | `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-picase` |

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

> ⛔ **CONDITIONAL STEP — default is to SKIP.** Only run this step if the prompt explicitly asked to
> send the retainer (see the retainer gate in Execution Mode). If the prompt didn't ask, or said
> `retainer skip` / `retainer sent`, **do not run Step 13 or Step 14** — note "retainer skipped" and stop.

Send the retainer only after the tracking sheet, Chat space, and Gmail label
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

> 🛑 **Recipient roster is FIXED — 3 slots, nothing else (Klaus, 2026-09-11).**
>
> | Slot | Who | Type |
> |---|---|---|
> | Signer 1 | the client(s) — `Client1`, `Client2`… | signer |
> | Signer 2 | `Attorney` (Shenqi Cai) | signer |
> | CC | **exactly ONE** mailbox: the assigned CM's | carbon copy |
>
> **CC = the assigned mailbox itself:** `claims@lingtulaw.com` / `piteam@lingtulaw.com` /
> `picase@lingtulaw.com`. **Mailbox not decided → `klaus@lingtulaw.com` only.**
>
> **Delete every other recipient the template carries** — the other two team mailboxes, Klaus
> when a CM's mailbox is being kept, and any extra *signer* role the template picks up.
>
> ⚠️ The template gains and loses roles over time. On 2026-09-11 it briefly carried a
> **`Piteam@` SIGNER with 0 tabs at routing order 3** — a signer with no tabs blocks the
> envelope from ever reaching `completed`, even after the client signs. The pre-send gate
> (step 5b) catches this: **only `Client1…` and `Attorney` may be signers; everything else
> must be a carbon copy or be removed.**

> 🛑 **The client role is `Client1`. There is NO role named `Client`.**
> Passing `roleName: "Client"` does **not** match the template — Docusign silently appends a
> BRAND-NEW recipient with **zero tabs**, and the real client role `Client1` (which owns every
> signHere / fullName / dateSigned tab) is left empty. If you then remove `Client1` as an
> "unused slot", the client receives a contract **with no signature fields at all**. They can
> open it, click through, and Docusign marks it `completed` with nothing signed.
>
> **NEVER remove `Client1`.** Single client → `roleName: "Client1"`, remove Client2–5 only.
>
> Happened 2026-09-08 (Zhe Ji) and 2026-09-10 (Sai Choi Lau) — both went out unsignable and
> Klaus caught it, not us. Cause: running Step 13 from memory of "remove unused Client slots"
> instead of reading this section.
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
   **`Client1` (recipientId 1) is never empty and is never removed** — it holds every client tab.
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
5b. 🛑 **GATE — verify the client actually has signature fields BEFORE sending.**
   Call `listRecipients` with `include_tabs=true` and check the client signer:
   - `roleName` MUST be `Client1` (and `Client2`… for passengers) — never `Client`
   - `totalTabCount` MUST be **> 0** (a correct single-client envelope shows signHere +
     fullName + dateSigned on the client, and 3 tabs on the Attorney)
   - `recipientSuppliesTabs: "true"` together with `totalTabCount: "0"` is the exact
     signature of the broken envelope — **STOP, do not send.**
   - **The ONLY signers may be `Client1…` and `Attorney`.** Any other `recipientType: signer`
     (e.g. a `Piteam@` / `Picase@` / `Claims@` role) → remove it before sending; a 0-tab signer
     stalls the envelope forever.
   - **Exactly one carbonCopy may remain** — the assigned CM's mailbox (or klaus@ if no CM).
   - **That CC's display NAME must be the current CM** — the templates still carry `Ryan Wei` on
     picase@ (he has left; Klaus 2026-11-05: 「there is no more Ryan Wei, Picase only Jenkins Li」).
     Fix it with `updateEnvelopeRecipients` → `recipientsToUpdate.carbonCopies` before sending:
     claims@ = `Amos Feng` · piteam@ = `Jerry Piao` · picase@ = `Jenkins Li`.
     Remove the rest.

   If it is broken: delete the envelope and rebuild it with `roleName: "Client1"`. Do NOT send
   and fix later — once it goes out the client gets an unsignable contract.

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

**`PI Auto Retainer: [Driver Full Name] et al-M/D/YYYY(<Fee Type>)`** — updated 8/17/2026.

The trailing `(New)` / `(Standard)` is the **fee type actually sent** (the Step 13 gate), so the
subject alone tells you which version the client signed. It must match the template used:

| Fee type | Template | Subject suffix |
|---|---|---|
| **new** | PI Auto Retainer (New) / +Joint Conflict (New) | `(New)` |
| **standard** | PI Auto Retainer (Standard) / +Joint Conflict (Standard) | `(Standard)` |

Examples:
- Single client, new: `PI Auto Retainer: Jiajun He et al-8/15/2026(New)`
- Single client, standard: `PI Auto Retainer: Guanghua Li et al-5/30/2026(Standard)`
- Multi-client, new: `PI Auto Retainer: Hsuan-Yun Chang et al-5/24/2026(New)`

> Keep `et al` even for a single client — it is the firm's fixed subject shape, not a plural marker.

---

## Step 13b — Lingtu Data 签约 + 直接挂 CM（retainer 发出后立刻做）

> Klaus 2026-11-05：「最重要就是确保它后面是 assign 给的这个 case manager，然后它的凌图数据能直连到这个案子，
> 而不会出现延误，不会说需要它再主动去连接一下这个案子。」—— 所以 **DocuSign 一发出就签约**，不等客户签完，
> 也不让 CM 自己 `claim_my_case`。

**Step 13 真的发出 retainer，或 Klaus 说 `retainer signed` 时做。** 只说 skip、没说签了 → 跳过本步，A 列留客户编号。

1. **`sign_lead`**（每条线索签一次；一车多人每人各自的线索各签一次）：

   | 参数 | 值 |
   |---|---|
   | `lead_id` | Step 9a `log_lead` 返回的 |
   | `contract_kind` | new → `pi_new_50`；standard → `pi_standard_1_3`（与 Step 13 发出的模板一致） |
   | `client_minor` | 这位客户是 minor → `true` |
   | `lead_staff` | 按 tab 的 CM（下表） |
   | `assist_staff` | 按 tab 的 CA（下表） |
   | `partner` / `no_partner` | **开头闸门里 Klaus 说的**：车行 / 中介要付介绍费 → `partner`=合作方名单里的名字；没有 → `no_partner=true`。没说就问，不猜 |
   | `signed_on` | 今天（retainer 发出日） |
   | `attorney` | 不填（默认蔡律师） |

   | Tab | CM (`lead_staff`) | CA (`assist_staff`) |
   |---|---|---|
   | Claims@ | Amos Feng | Taki Xue |
   | Piteam@ | Jerry Piao | Angelina Meng |
   | Picase@(Jenkins) | Jenkins Li | Tiana Deng |
   | Picase@(Amos) | Amos Feng | 问 Klaus |

2. **挂案卷**：`link_case_folder`（`matter_code` = 返回的案件编号，`drive_folder_url` = Step 9 案卷，
   `activity_log_url` = intake sheet 链接）。
3. **Master A 列换号**：把 Step 10 写的客户编号换成案件编号（`84940` → `84940-PI1`），按客户名定位行。
4. **读回**：`find` 客户编号 → `cases[]` 里有这个案件编号，`lead` = 该 CM、`assist` = 该 CA、`linked` 有案卷。
   不对就停下报告，不算完成。

---

## Step 14 — Output the Client Signing Message (文案)

> ⛔ **CONDITIONAL — only if Step 13 actually sent a retainer.** If the retainer was skipped
> (the default), skip this step too — there is no signing message to produce.

**The last thing you output when a retainer was sent.** After the retainer is confirmed SENT, produce the
WeChat message Klaus forwards to the client asking them to sign. Klaus sends it himself —
this step GENERATES text only, it never sends anything.

> 🔒 **RE-READ THIS STEP AND COPY THE TEMPLATE VERBATIM — EVERY CASE. Do NOT compose from memory.**
>
> The template below is a **CLOSED SET**. The only things you may change are the fill-in values:
> client English name(s), client email(s), the fee block (`new` vs `standard`), and 您/两位/三位.
> **Every other character is fixed.** You may not add a block, drop a block, reorder blocks,
> reword a sentence, or "tighten" anything.
>
> **FORBIDDEN in the client message** (all of these were invented on 2026-09-24, Yang Yang +
> Mengmeng Wang, by writing the message from memory instead of opening this step):
> - **A 补充材料 / 待补文件 checklist** (驾照、保险卡、伤情、修车行地址…). Missing documents are a
>   **CM welcome-call** job and belong in the §7 summary to Klaus — never in the signing message.
> - **Medical advice or treatment offers** — `建议尽早就医`, `需要我们帮您安排看诊`. This is
>   attorney-driven solicitation and violates the firm's non-driven rule.
> - Case facts (车主姓名、对方保险、车牌、DOL), 索赔价值, 时间预期, or any 案情分析.
> - Paraphrasing the 费用说明 instead of pasting the exact block. Dropping
>   `以上为简要说明，具体条款以合同为准。`
> - Dropping the 服务内容 block, the 签约前提醒 block, or the `凌图律所` 落款.
>
> **Self-check before you output.** Diff what you wrote against the template: it must contain
> the `<DISK case name>⚠️` header line, a blank line, then exactly the five blocks in order
> (合同已发→服务内容→费用说明→签约前提醒→签署说明+落款), and nothing else. If a block is
> missing or an extra block appeared, rewrite from the template.
> Violated on the first two cases after this step was written — that is why this guard exists.

### Hard rules (firm's client-message style — see memory `feedback-client-message-plain`)

- **Plain text only.** No markdown, no bold, no bullets, no headers, no underline fill-lines.
- **Present it in a plain code block** so Klaus can copy it straight out.
- **First line INSIDE the code block = the case header `<DISK case name>⚠️`, then a blank line**
  (Klaus, 2026-09-28: "我好直接复制" — it must come out with one copy, so it lives inside the
  block, not as a caption above it). Example first two lines:
  ```
  Yutao Ma-9-28-2026⚠️

  Yutao 您好，我们已经把委托合同…
  ```
  Disk case name = same string as the case folder (dashes in the date), then the ⚠️ emoji,
  no space before it.
- **Claim-phrase lines go ABOVE the case header** (Klaus 2026-11-08): the very first line(s) of the
  code block = `本群案件编号 <matter code>`, one line per client with a code (unsigned → `本群客户编号 <5-digit>`),
  then a blank line, then the `<DISK case name>⚠️` header. Lets the workbench claim the WeCom group from the
  same paste. These lines + the header are the ONLY additions permitted to the closed set below.
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

**`standard` 版（先扣律师费，诉前 1/3 / 诉后 40%）：**

```
费用说明：
一、我们采用风险代理方式，签约时不需要您支付任何前期费用。
二、案子拿到赔偿后，先扣除律师费。如果案子在提起诉讼之前和解，律师费为赔偿金的三分之一；如果案子需要提起诉讼，律师费为赔偿金的百分之四十。
三、扣除律师费之后的金额，用来支付您的医疗费用，付完之后剩余的部分全部归您。
四、以上为简要说明，具体条款以合同为准。
```

> ⚠️ **两档费率是 2026-09-10 Klaus 校准的**：standard 不是单一的 1/3 —— 诉讼前和解 1/3，
> 进入诉讼 40%，**两档必须都写出来**。只写 1/3 是错的。

Multi-client: swap 您 → 两位／三位 to match the client count.

### Single-client template

```
[CaseName]⚠️

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
[CaseName]⚠️

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

## Completion gate — 读回核对，全部过了才准写最终回复

> 2026-11-02 加（Klaus：有时会跳过入档）。**不凭记忆说"做完了"，逐项用工具读回来。**
> 任何一项不过 → 回去补那一步；补不了的，写进最终回复 §8 的「未完成」，**不准当成完成**。

| # | 核对 | 怎么读回 |
|---|---|---|
| 1 | Drive 案卷在 `1. Pending`，内有 intake sheet 和 `Intake Responses.zip` | `gws drive files list`（parent = 案卷 id） |
| 2 | Lingtu Data 有这个客户和编号 | `find` 司机电话或姓名 |
| 3 | Master 对应 tab 有这几行，**A 列 = 编号**、Client Name 带 intake 链接 | 读 `'<tab>'!A3:F<3+N-1>` |
| 4 | Chat 群已建、成员齐、CM 和 Amos/Claire 是 Manager | `gws chat spaces members list` |
| 5 | 团队信箱的 Gmail case label 已建且是黄色 | `labels list` |
| 6 | retainer 发了：Lingtu Data 有案件编号、CM/CA 已挂、案卷已挂、Master A 列已换成案件编号；retainer skip：注明「签约后补」 | Step 13b 第 4 步的 `find` |
| 7 | retainer：送了就有 envelope id；没要求就写「未发（未要求）」 | Step 13 的结果 |
| 8 | intake 表有 `Activity Log` tab，registry.json 已登记这个案子 | `al.py init <id>` 再跑一次应回「已存在」；`grep <sheet_id> registry.json` |

---

## Step 15 — Final Reply to Klaus (HARD STOP)

**The last thing you say after the 14 steps is the output summary from
`references/summary-format.md` — its 8 sections, in order, and NOTHING else.**

Forbidden in the final reply (all of these were written 2026-09-10 and Klaus called them out):
- Liability analysis, respondeat superior / corporate-defendant theories, policy-limit estimates,
  case-value or case-strength characterizations ("底子很硬", "不是一个量级")
- Treatment advice, urgency coaching, "gap 越久越伤案子"-type commentary
- Unsolicited next-step / to-do lists beyond §6 Critical Flags
- Re-explaining what the documents said beyond §2

§6 Critical Flags is the ONLY place judgment belongs, and each item is **one line**, prefixed
`⚠️ CRITICAL:`. If something genuinely needs a decision from Klaus, state it in one sentence and
stop — do not build the argument for him.

> The pipeline ends at "here is what I built and what is still open." Klaus asks for analysis
> when he wants analysis.

---

## Reference Files

- `references/cell-map.md` — 填写总原则 + complete value cell map and yellow rules (**read first**)
- `references/document-rules.md` — Per-document extraction rules (DL, AIC, police card, etc.)
- `references/document-placement.md` — File naming conventions and folder placement
- `references/summary-format.md` — Output summary format
- `scripts/verify_intake.py` — **Gate 2**: post-write type self-check (catches values written
  into the wrong field). Mandatory after filling the intake sheet, before Drive upload.
- `scripts/add_tracking_row.py` — **Gate 3**: builds the Step 10 tracking row by copying the
  Example Row (row 2) and then setting only the case fields. Mandatory — never hand-roll
  `insertDimension` + `values update` for the tracking sheet.
