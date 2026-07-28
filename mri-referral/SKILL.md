---
name: mri-referral
description: |
  Email an MRI / imaging REFERRAL to an imaging center for 凌图律所 / Lingtu Law Office
  (Law Office of Shenqi Cai APC). Use this skill whenever any of the following are mentioned:
  MRI referral, refer client for MRI, send MRI referral, imaging referral, 转介做核磁/MRI,
  "refer 张三 for MRI to [center]", "/mri-referral". The skill finds the case in Drive, reads
  the intake sheet (client info + injury regions), fills the firm's MRI Referral email template
  with the client's info (study/region to image, accident type, DOL, name, DOB, phone, address),
  shows it for approval, sends the email to the imaging center (FROM the case's owning mailbox),
  then labels the sent message by case name + blue-stars it, posts "【Claude AI】 MRI referral
  sent via email to <center>" to the case Chat space, and records the MRI center on the Master
  + intake sheets. Always trigger for any "send MRI referral" request, even a partial one.
---

# Send MRI Referral — email an imaging referral to an MRI center

Mirrors `chiro-referral`: find case → read intake → fill MRI template → verify → send → label
+ post to case Chat → record on sheets. **Outbound to an imaging center — auto-send when clean,
pause only on a real data problem or an explicit "draft it".**

> An MRI is a one-time **imaging study**, not ongoing treatment. The two MRI-specific differences
> from chiro-referral are: (1) the body **must name the study / region(s) to image** (confirm it
> in Step 3), and (2) the client WeChat message is an **imaging-appointment** message, not a
> course-of-treatment message (no "缺席治疗"/"假条" language). Everything else is the same.

## Invocation inputs
- **Case** — client/driver name (finds the Drive case folder).
- **Imaging center** — name + **email** (required to send) + address/phone (for the record).
- **Study / region(s)** — what to image (e.g. "MRI cervical spine", "C-spine + L-spine"). If the
  user didn't say, propose one from the intake injury regions and **confirm in Step 3**.
- **Case manager** — signs the email (default: the case's tracking-tab owner; ask if unclear).

## Constants
- **Shared Drive "PI Team Folder":** driveId `0ADBH3EXeXKRBUk9PVA`. Case folder
  `Driver Name-M-D-YYYY` → intake `.xlsx` + subfolders.
- **Template + signature:** `references/referral-template.md` (subject/body + signature; fill
  CM ext/direct from `references/firm-directory.md`).
- **Intake reader:** `scripts/read_intake_referral.py` (C2 dol, C3 time, C4 client, C5 dob,
  C6 phone, C7 address, F5 point_of_impact = accident type). Read injury regions directly from
  the intake (driver `Initial Injuries` ~C22 + pain scale; each passenger's block) to propose
  the study region.
- **FROM account = the case's OWNING mailbox** (NOT klaus@). Resolve it from the **Master sheet**
  (`1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`): find the client's row in tab `Claims@` /
  `Piteam@` / `Picase@` — whichever tab the client is in = that mailbox. Match the FULL name.
  Send + label run through that mailbox's gws store (prefix gmail commands with
  `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-<store> GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-<store>/credentials.json`):
  picase@ → `gws-picase`, claims@ → `gws-claims`, piteam@ → `gws-piteam`.
  **Durable auth:** each store holds a plain `credentials.json` (un-encrypted refresh token) —
  gws reads it directly, no keyring. **Do NOT set `GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file`.**
  If a store's `credentials.json` is missing/revoked, re-auth then re-export it (see
  [[gws-auth-scopes]]). klaus@ is only used on explicit instruction. Drive reads, case lookup,
  sheet update, and the Chat post use the **default** gws account.
- **SIGNATURE = the HANDLER (the person running this), NOT the FROM mailbox.** Fetch the handler's
  own configured Gmail signature (default gws account = klaus@) and append it verbatim.
- Scratch dir: `~/referral_work` (`mkdir -p`; gws `-o`/`--upload` must be inside cwd — `cd` there).

---

## Step 1 — Find the case + intake
Search the Shared Drive for the case folder by client name. Capture the case folder id, then
list children for the intake `.xlsx` id. (Unlike chiro-referral, an MRI referral does **not**
attach PD photos — imaging centers don't need them.)

## Step 2 — Read the intake (referral fields + injury regions)
```bash
mkdir -p ~/referral_work && cd ~/referral_work
gws drive files get --params '{"fileId":"<INTAKE_XLSX_ID>","alt":"media","supportsAllDrives":true}' -o intake.xlsx
python3 ~/.claude/skills/mri-referral/scripts/read_intake_referral.py intake.xlsx
```
→ accident type (`point_of_impact`), `dol`, `time`, `client`, `dob`, `phone`, `address`. Also
open the intake injury fields to read the injured **regions** (to propose the MRI study).

## Step 3 — Verify center + client fields + STUDY (auto-proceed if clean)
Show the user a compact table of (a) the **imaging center**: name + **email** (+ address/phone);
(b) the **study / region(s) to image** (the value you'll put on the first body line — REQUIRED);
and (c) every **client value** in the email body (accident type, DOL, time, name, DOB, phone,
address). **Do NOT wait for approval — if the data is clean, continue to building + sending.**
ONLY pause and ask when something is actually wrong: a required field (incl. the **study/region**
or the center email) is blank/malformed, or a value looks inconsistent. The table is for
transparency + catching errors, not a routine gate.

## Step 4 — (no attachments)
MRI referrals are sent **without attachments**. Skip straight to Step 5.

## Step 5 — Build the email (HTML; signature pulled from Gmail, NOT composed)
Subject: `MRI_Referral_Lingtu Law_<Client>` (e.g. `MRI_Referral_Lingtu Law_Chunming Zhang`).

Body = compose the content lines — **the study/region line FIRST**, then intro + client values —
then **append the FROM account's configured Gmail signature verbatim** (do NOT write a signature).
The signature is HTML (logo + footer), so build an **HTML** message:
```bash
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-picase GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-picase/credentials.json \
  gws gmail users settings sendAs list --params '{"userId":"me"}' --format json
```
Then build a `multipart/mixed` message inline (Python `email.mime`): a `text/html` part =
`<div dir="ltr">` + one `<div>` per content line (`<div><br></div>` for blanks) + the fetched
signature HTML; base64url-encode → `{"raw": ...}`. (build_email.py is plain-text only — don't use
it here.) Client values come from intake verbatim (no fabrication); the study/region is the
value confirmed in Step 3.

## Step 6 — Show content, then SEND by default (no approval wait)
**List the final content** in Claude — recipient + subject + body lines (incl. the study line) +
which signature — for transparency, **then send immediately. Default = SEND.** Two exceptions:
(a) Step 3 surfaced a real problem → pause and ask; (b) the user **explicitly** said "draft it"
this run → make a draft in the FROM mailbox and STOP.
```bash
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-<store>
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-<store>/credentials.json
```
- **Draft** (only on explicit "draft it"):
  `gws gmail users drafts create --params '{"userId":"me"}' --json '{"message":{"raw":"<RAW>"}}' --format json` → STOP.
- **Send** (default, no attachment): `{"raw": "<base64url>"}` inline is fine.
Capture the returned message `id`.

## Step 7 — Label + blue-star + move to inbox + post to case Chat
> ⚠️ Don't use `eval $PFX ...` — eval mangles JSON quotes. `export` the two env vars once, then
> run plain `gws` commands.
1. **Label by CASE name (ONE label) + BLUE-STAR + move to INBOX** (in the FROM mailbox's store).
   ONE label for the whole case — for a multi-client case a **single combined label, driver first
   then passenger(s)** (e.g. `Xingwen Bai/Hongmei Zhang`). **NEVER one label per client.** First
   list labels and **reuse the existing case label** if present; only create if missing, color
   yellow `#fbe983` (text `#594c05`). Then add three labels in one `modify`: the **case label**,
   **`BLUE_STAR`** (referral-sent / awaiting marker), and **`INBOX`** (keeps it visible).
   ```bash
   export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-<store>
   export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-<store>/credentials.json
   gws gmail users labels create --params '{"userId":"me"}' \
     --json '{"name":"<Case Label>","color":{"backgroundColor":"#fbe983","textColor":"#594c05"},"labelListVisibility":"labelShow","messageListVisibility":"show"}' --format json   # skip if exists
   gws gmail users messages modify --params '{"userId":"me","id":"<MSG_ID>"}' --json '{"addLabelIds":["<LABEL_ID>","BLUE_STAR","INBOX"]}' --format json
   ```
   (`BLUE_STAR` implies `STARRED`; don't also add `STARRED`. Verify the account has superstars —
   `BLUE_STAR` must exist in `labels list`.)
2. **Post to the case Google Chat space** (default gws account — member of case spaces): find the
   space by client name (`gws chat spaces list`), then post a **multi-line** message — the
   headline `to✅` line, then the center's **name / address / phone / email** each on its own line:
   ```
   【Claude AI】 MRI referral sent via email to✅
   <Imaging Center Name>
   <Center Address>
   <Center Phone>
   <Center Email>
   ```
   ```bash
   gws chat spaces messages create --params '{"parent":"spaces/<ID>"}' \
     --json '{"text":"【Claude AI】 MRI referral sent via email to✅\n<Center Name>\n<Address>\n<Phone>\n<Email>"}'
   ```

## Step 8 — Update the Master sheet (MRI specialty column)
Master sheet `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`, the same tab where the client was
found. For each referred client, write `M/D <Center Name>` (e.g. `6/24 RadNet Imaging`) into the
**MRI** specialty column of that client's row, **bright-yellow** background (R=1 G=1 B=0).

**Do NOT hardcode the column letter — the layout drifts.** Read the live **header row (row 1)** of
the CM tab and match the **MRI** header to find the column index (the old fixed-letter mappings are
stale). **Pull the Master grid FRESH every run** — rows AND columns drift (new cases insert at top;
columns get inserted) and stale indices silently clobber the wrong cell.
- **Locate** by pulling grid data with **no A1 ranges**, scanning in code:
  ```bash
  gws sheets spreadsheets get --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM","includeGridData":true,"fields":"sheets(properties(title,sheetId),data(rowData(values(formattedValue))))"}' --format json
  ```
  Find the tab by title, the **MRI** column by header text, the client's row by name (0-based).
- **Write** with a **gid-based `updateCells`** (value + yellow in one request):
  ```bash
  gws sheets spreadsheets batchUpdate --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM"}' --json '{"requests":[{"updateCells":{"range":{"sheetId":<GID>,"startRowIndex":<R0>,"endRowIndex":<R0+1>,"startColumnIndex":<C0>,"endColumnIndex":<C0+1>},"rows":[{"values":[{"userEnteredValue":{"stringValue":"M/D Center Name"},"userEnteredFormat":{"backgroundColor":{"red":1,"green":1,"blue":0}}}]}],"fields":"userEnteredValue,userEnteredFormat.backgroundColor"}}]}'
  ```
> Tab sheetIds (gids stable): Picase@ `775230687`, Claims@ `86730608`, Piteam@ `102974151`.
> If the MRI column already has content, DON'T overwrite — flag it to the user.

## Step 8b — Update the case INTAKE sheet (MRI Treatments block)
Also record the center in the **case intake `.xlsx`** (case-folder root), in its **Treatments**
section's **MRI** block, so the case file shows where the client was imaged. Edit the mounted
`.xlsx` with openpyxl (back it up first to `~/.supplement-intake-backups/`; the mount syncs to Drive).

Layout (read it live — don't assume): col **Q** holds Treatments labels; each client has a value
column — **R = Driver, S = Pass1, T = Pass2 …**. Each specialty is a small block: the specialty
row takes the **center name**, then `Address` / `Phone` / `Email` rows below it. **Find the MRI
block** (match the `MRI` label in col Q — it's a separate block lower than Chiropractic) and write
into the referred client's column:
```
<MRI row>      = <Center Name>
<+1 Address>   = <Center Address>
<+2 Phone>     = <Center Phone>
<+3 Email>     = <Center Email>
```
Write the referred client's column only (driver → R, passenger → S/T). Font Nunito 10, left,
no-wrap. Don't clobber a different center already in the block — flag it instead.

**Un-highlight the MRI specialty-name cell.** That cell starts **yellow** (the "pending" marker);
once you fill it with the center name, set its fill to no-fill (same convention as
[[intake-sheet-highlight-convention]]). The Address/Phone/Email rows aren't highlighted.

## Step 9 — Log run + confirm
Report: client, imaging center + email, study/region sent, fields sent, the Gmail message id, the
label applied (+ color), the **blue star + moved-to-inbox** state, the Chat post, and the
Master + intake cells updated. Clean up: `rm -rf ~/referral_work`.

## Step 10 — Output the WeChat (企业微信) client message (copy-paste, in Claude)
After everything is done, **print a ready-to-copy Chinese message in the Claude chat** (do NOT send
it anywhere — Klaus pastes it into the 企业微信 group himself). Single plain-text block (no markdown
tables). Two sections:

**1) 🏥MRI检查安排** — imaging-appointment template (NOT a course-of-treatment message); fill the
center **name / address / phone** (no email) + the **检查部位 (region)**:
```
🏥MRI 核磁共振检查安排

🔔您好，我们已为您安排好 MRI（核磁共振）检查，检查中心会打电话联系您预约具体时间！

检查部位：<Region(s) in Chinese, e.g. 颈椎 / 腰椎>

检查中心信息⬇️
<Center Name>
<Center Address>
<Center Phone (digits only)>

🕒 确认时间：约好后请在群里告知我们您的检查日期和时间，谢谢！

🆔 携带证件：无需支付任何费用，带上您的 ID 或驾照即可，按时到场即可完成检查。

⚠️ 如需改期，请务必提前在群里报备，不要无故缺席。
```

**2) 💉受伤更新** — per **referred** client, summarize injuries + pain level **in Chinese**, pulled
from the intake injury fields (driver: `Initial Injuries` + pain-scale; each passenger's block).
One line per client: `<Client>-<症状，顿号分隔>；疼痛程度 <X>/10`. Translate intake symptoms to
Chinese (Neck pain→颈部疼痛, back pain→背部疼痛, headache→头痛, dizziness→头晕, nausea→恶心,
vomiting→呕吐, difficulty sleeping→睡眠困难). Do NOT invent symptoms — only what the intake lists.
```
💉受伤更新

您好，这是基于您之前告诉我们，关于您当前受伤与症状的文字总结：

🤕您目前的症状包括：

<Client 1>-<症状>；疼痛程度 <X>/10。
（…one line per referred client…）

‼️做检查时如有医生/技师询问，请如实完整告知您的受伤部位与症状。

🚩 信息核对：如果以上描述有任何遗漏或变化，请务必现在就在群里告知我们，以便及时更新备案。
```
(For a single-client referral, the 受伤更新 section has just one symptom line. Render both sections.)

## Notes & gotchas
- **MRI = imaging study, not treatment.** Always include the **study/region** on the first body
  line, and use the imaging-appointment WeChat wording (Step 10) — never the "缺席治疗/假条"
  course-of-treatment language from chiro-referral.
- **No attachments.** Unlike chiro-referral, do not attach PD photos to an MRI referral.
- **Auto-send is the default** (show content → send). Pause only on a real Step-3 problem
  (blank/inconsistent field incl. missing study/region, bad center email) or an explicit "draft it".
- FROM = the case's owning mailbox (resolved from the Master-sheet tab), NOT klaus@ unless told.
  Signature = the handler/invoker (klaus when klaus runs it).
- Accident type = intake **F5 Point of Impact**, rendered as a SHORT phrase (e.g. `Rear-end`).
- Don't fabricate any client field — copy from intake; if blank, drop that line and flag it.
- See [[feedback-send-from-case-mailbox]], [[feedback-case-label-one-per-case]],
  [[feedback-send-referral-autosend]] (same conventions as chiro-referral).
