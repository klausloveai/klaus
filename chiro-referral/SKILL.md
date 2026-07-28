---
name: chiro-referral
description: |
  Email a medical REFERRAL to a treating clinic for 凌图律所 / Lingtu Law Office
  (Law Office of Shenqi Cai APC). Use this skill whenever any of the following are mentioned:
  send referral, refer client to clinic/chiro, chiro referral, 转介诊所, referral email,
  "refer 张三 to [clinic]", "/referral". The skill finds the case in Drive, reads the intake
  sheet, fills the firm's Referral email template with the client's info (accident type, DOL,
  name, DOB, phone, address), attaches the case's property-damage (PD) photos if any, shows it
  for approval, sends the email to the clinic (default FROM picase@), then labels the sent
  message by client name and posts "【Claude AI】 Chiro referral sent via email to <clinic>" to the case
  Chat space. Always trigger for any "send referral to clinic" request, even a partial one.
---

# Send Referral — email a client referral to a clinic

Mirrors `send-lop`/`lor-send`: find case → read intake → fill template → verify → send → label
+ post to case Chat. **Outbound to a clinic — mandatory approval before sending.**

## Invocation inputs
- **Case** — client/driver name (finds the Drive case folder).
- **Clinic** — name + **email** (required to send) + address/phone (for the record). The user
  provides these; verify them in Step 3.
- **Case manager** — signs the email (default: the case's tracking-tab owner; ask if unclear).
- Referral type — **generic Referral** for now (covers Chiro). Ortho/PM/MRI = future templates.

## Constants
- **Shared Drive "PI Team Folder":** driveId `0ADBH3EXeXKRBUk9PVA`. Case folder
  `Driver Name-M-D-YYYY` → intake `.xlsx` + subfolders incl. **`3#Property Damage Claim`** (PD photos).
- **Template + signature:** `references/referral-template.md` (subject/body + signature; fill
  CM ext/direct from `references/firm-directory.md`).
- **Intake reader:** `scripts/read_intake_referral.py` (C2 dol, C3 time, C4 client, C5 dob,
  C6 phone, C7 address, F5 point_of_impact = accident type).
- **Email builder:** `scripts/build_email.py` (`--to --from --subject --body-file --attach
  --attach-name --out`).
- **FROM account = the case's OWNING mailbox** (NOT klaus@, NOT hardcoded picase@).
  Resolve it from the **Master sheet** (`1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`):
  find the client's row in tab `Claims@` / `Piteam@` / `Picase@` — whichever tab the
  client is in = that mailbox. Match the FULL name (e.g. "Hai Liu" ≠ "Xianghai Liu").
  Send + label run through that mailbox's gws store (prefix gmail commands with
  `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-<store> GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-<store>/credentials.json`):
  picase@ → `gws-picase`, claims@ → `gws-claims`, piteam@ → `gws-piteam`.
  **Durable auth (一劳永逸):** each store holds a plain `credentials.json` (un-encrypted refresh
  token) — gws reads it directly, no keyring, survives across Cowork turns/sessions. **Do NOT set
  `GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file`** (the old encrypted `credentials.enc` broke every
  turn). If a store's `credentials.json` is missing/revoked, re-auth then re-export it (see the
  durable-auth note in [[gws-auth-scopes]] memory). klaus@ is only used on explicit
  instruction. Drive reads, case lookup, sheet update, and the Chat post use the
  **default** gws account.
- **SIGNATURE = the HANDLER (the person running this), NOT the FROM mailbox.** Fetch the
  handler's own configured Gmail signature (default gws account = klaus@) and append it
  verbatim — a referral sent FROM picase@ still carries klaus's signature when klaus runs it.
- Scratch dir: `~/referral_work` (`mkdir -p`; gws `-o`/`--upload` must be inside cwd — `cd` there).

---

## Step 1 — Find the case + key subfolders
Search the Shared Drive for the case folder by client name (same as lor-send Step 1). Capture
the case folder id, then list children for: the intake `.xlsx` id and the **`2#Accident Info`**
folder id (where vehicle-damage photos usually live) — also note `3#Property Damage Claim` as a
fallback location.

## Step 2 — Read the intake (referral fields)
```bash
mkdir -p ~/referral_work && cd ~/referral_work
gws drive files get --params '{"fileId":"<INTAKE_XLSX_ID>","alt":"media","supportsAllDrives":true}' -o intake.xlsx
python3 ~/.claude/skills/chiro-referral/scripts/read_intake_referral.py intake.xlsx
```
→ accident type (`point_of_impact`), `dol`, `time`, `client`, `dob`, `phone`, `address`.

## Step 3 — Verify clinic + client fields (auto-proceed if clean)
Show the user a compact table of (a) the **clinic**: name + **email** (+ address/phone), and
(b) every **client value** that will go in the email body (accident type, DOL, time, name,
DOB, phone, address). **Do NOT wait for approval — if the data is clean, continue straight to
building + sending.** ONLY pause and ask the user when something is actually wrong: a required
field is blank, the clinic email is missing/malformed, a value looks inconsistent (e.g. the
intake address ≠ the driver-license address, two conflicting DOBs), or you'd otherwise be
guessing. The table is for transparency + catching errors, not a routine gate.

## Step 4 — Collect the vehicle-damage photos (attach if any)
Vehicle-damage (PD) photos usually live in **`2#Accident Info`** (fall back to `3#Property
Damage Claim` if not there). **Attach ONLY the vehicle-damage file(s)** — typically one named
like `Vehicle Damage Photos.pdf` / `PD Photos` / `*damage*`. **NEVER attach** the other
contents of `2#Accident Info` — driver licenses, insurance cards, license plates, scene
videos, police reports — those are client/3P PII and irrelevant to a clinic referral. When
unsure which file is the damage photos, ask the user rather than guessing. Mind Gmail's 25 MB
cap (scene `.mov` videos are huge — never attach them).
```bash
gws drive files list --params '{"q":"'\''<ACCIDENT_INFO_FOLDER_ID>'\'' in parents and trashed=false","supportsAllDrives":true,"includeItemsFromAllDrives":true,"fields":"files(id,name,mimeType,size)"}' --format json
# pick ONLY the vehicle-damage file(s) by name, then:
# gws drive files get --params '{"fileId":"<id>","alt":"media","supportsAllDrives":true}' -o "<name>"
```

## Step 5 — Build the email (HTML; signature pulled from Gmail, NOT composed)
Subject: `<Type>_Referral_Lingtu Law_<Client>` (e.g. `MRI_Referral_Lingtu Law_Chunming Zhang`)
or `Referral_Lingtu Law_<Client>` for a generic/chiro referral.

Body = compose the content lines (intro + client values + any study/order details), then
**append the FROM account's configured Gmail signature verbatim** — do NOT write a signature.
The signature is HTML (logo + footer), so build an **HTML** message:
```bash
# fetch the configured signature for the FROM account (picase store):
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-picase GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-picase/credentials.json \
  gws gmail users settings sendAs list --params '{"userId":"me"}' --format json
```
Then build a `multipart/mixed` MIME inline (Python `email.mime`): a `text/html` part =
`<div dir="ltr">` + one `<div>` per content line (`<div><br></div>` for blanks) + the fetched
signature HTML; plus each attachment; base64url-encode → `{"raw": ...}`. (build_email.py is
plain-text only — don't use it here.) Compose only the content; client values come from intake
/ the source doc verbatim (no fabrication).

## Step 6 — Show content, then SEND by default (no approval wait)
**List the final content** in Claude — recipient + subject + body lines + attachment list +
which signature — for transparency, **then send immediately. Default = SEND; do NOT wait for
approval.** (Standing instruction from Klaus 2026-06-20: Step 3 clean → just send.) Only two
exceptions divert from auto-send: (a) Step 3 surfaced a real problem (blank/inconsistent field,
bad clinic email) → pause and ask; (b) the user **explicitly** said "draft it" this run → make a
draft instead and STOP.
- **Draft** (only when the user explicitly asks `"draft it"`): create a draft in the FROM mailbox
  for the user to review/send from Gmail — then STOP (skip Step 7's send-only bits, but you may
  still note it):
  ```bash
  GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-picase GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-picase/credentials.json \
    gws gmail users drafts create --params '{"userId":"me"}' --json '{"message":{"raw":"<RAW>"}}' --format json
  ```
- **Send** (default): send + then do Step 7 (label + blue-star + move to inbox + Chat).
  ```bash
  export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-<store>
  export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-<store>/credentials.json
  ```
  - **No attachment (small):** `{"raw": "<base64url>"}` inline is fine, OR send the approved
    draft: `gws gmail users drafts send --params '{"userId":"me"}' --json '{"id":"<DRAFT_ID>"}'`.
  - **WITH attachment (e.g. PD photos):** the base64 raw is too big for the command line
    (`Argument list too long`). Write the MIME to a file and **media-upload** it instead:
    ```bash
    # build the message with email.mime (text/html + MIMEApplication pdf), write m.as_bytes() → message.eml
    gws gmail users messages send --params '{"userId":"me"}' \
      --upload message.eml --upload-content-type message/rfc822 --format json
    ```
Capture the returned message `id`.

## Step 7 — Label + blue-star + move to inbox + post to case Chat
> ⚠️ Don't use `eval $PFX ...` — eval mangles the JSON quotes. `export` the two env vars
> once, then run plain `gws` commands.
1. **Label by CASE name (ONE label) + BLUE-STAR + move to INBOX** (in the FROM mailbox's store).
   The label is the **whole case**, not per-client: for a multi-client case use a **single combined
   label, driver first then passenger(s)** (e.g. `Xingwen Bai/Hongmei Zhang`). **NEVER create one
   label per client** (don't make separate `Xingwen Bai` + `Hongmei Zhang` labels — that was a past
   mistake). **First list labels and reuse the existing case label if it's already there** (case
   setup usually created it, matching the Drive folder / Chat-space case name); only create it if
   missing. Set color to **yellow `#fbe983`** (RGB 251,233,131 — Gmail palette yellow, text
   `#594c05`). Then on the sent message add three labels in one `modify`:
   - the **case label** (id from above),
   - **`BLUE_STAR`** — the blue superstar (Gmail auto-adds `STARRED` alongside it, so the star shows
     up blue, not yellow). This is the firm's "referral sent, awaiting clinic" marker.
   - **`INBOX`** — moves the sent referral into the inbox so it stays visible as a follow-up
     (instead of Snooze, which the Gmail API can't do).

   Note: a `/` in a Gmail label name nests it (the firm uses `/` for some multi-client case
   labels) — that's fine; the point is ONE case label, not a label per person.
   ```bash
   export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-<store>
   export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-<store>/credentials.json
   # list labels → find or create one named "<Client>" → get its id
   gws gmail users labels create --params '{"userId":"me"}' \
     --json '{"name":"<Client>","color":{"backgroundColor":"#fbe983","textColor":"#594c05"},"labelListVisibility":"labelShow","messageListVisibility":"show"}' --format json   # skip create if it exists
   # if it already existed, patch its color: gws gmail users labels patch --params '{"userId":"me","id":"<LABEL_ID>"}' --json '{"color":{"backgroundColor":"#fbe983","textColor":"#594c05"}}'
   gws gmail users messages modify --params '{"userId":"me","id":"<MSG_ID>"}' --json '{"addLabelIds":["<LABEL_ID>","BLUE_STAR","INBOX"]}' --format json
   ```
   (Gmail only accepts label colors from its fixed palette — `#fbe983`/`#594c05` is the yellow pair
   for the case **label**. The message **star** is the superstar `BLUE_STAR`; verify the account has
   superstars enabled — the `BLUE_STAR` system label must exist in `labels list`. `BLUE_STAR`
   implies `STARRED`, so don't also add `STARRED`.)
2. **Post to the case Google Chat space** (default gws account — it's the member of case
   spaces): find the space by client name (`gws chat spaces list`), then post a **multi-line**
   message — the headline `to✅` line, then the clinic's **name / address / phone / email** each
   on its own line (so the team sees exactly where the client was referred):
   ```
   【Claude AI】 Chiro referral sent via email to✅
   <Clinic Name>
   <Clinic Address>
   <Clinic Phone>
   <Clinic Email>
   ```
   ```bash
   gws chat spaces messages create --params '{"parent":"spaces/<ID>"}' \
     --json '{"text":"【Claude AI】 Chiro referral sent via email to✅\n<Clinic Name>\n<Address>\n<Phone>\n<Email>"}'
   ```
   (Headline ends with `to✅` — no clinic name on that line; the details follow on separate lines.
   Use the actual referral type word if not chiro.)

## Step 8 — Update the Master sheet (treatment column)
Master sheet `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`, the same tab where the client
was found (Step "Constants"). For each referred client, write `M/D Clinic Name`
(e.g. `6/15 Accident & Wellness Group`) into the **specialty column** of that client's row,
with a **bright-yellow** background (R=1 G=1 B=0).

**Do NOT hardcode the column letter — the layout drifts.** Read the live **header row (row 1)**
of the CM tab and match the specialty name to find the column index. (As of 2026-06 on `Picase@`,
Chiropractic is **col S (idx 18)**, not M — M is now `EMS`. MRI/PM/etc. likewise shifted. The
old "Chiropractic = col M" mapping is stale.) For a multi-client referral, update **every**
referred client's row.

**Read + write without A1 ranges (robust against renamed/parenthesized tabs).** Plain
`Sheetname!A1` range reads can fail with `Unable to parse range` when a tab was renamed (the CM
tabs lost their `(Name)` suffixes — now just `Picase@` / `Claims@` / `Piteam@`). Avoid that:
- **Pull the Master grid FRESH every run — never reuse a cached snapshot from an earlier step/case.**
  Both **rows and columns drift**: new cases insert at the top (so row indices shift down) and columns
  get inserted (e.g. Chiropractic moved from idx 18 → **idx 19** when a `Health Insurance` column was
  added on `Picase@`). Writing to stale indices silently clobbers the wrong cell (a real bug we hit:
  clinic names landed in the `Health Insurance` column of two *other* clients). Always re-pull, then
  locate the client's row **by name** and the specialty column **by header text** in that fresh data.
- **Locate the client + header** by pulling grid data with **no ranges**, then scanning in code:
  ```bash
  gws sheets spreadsheets get --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM","includeGridData":true,"fields":"sheets(properties(title,sheetId),data(rowData(values(formattedValue))))"}' --format json
  ```
  Find the tab by title, the specialty column by header text, and the client's row by name (0-based row index).
- **Write** with a **gid-based `updateCells`** (no A1 parsing) — value + yellow in one request:
  ```bash
  gws sheets spreadsheets batchUpdate --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM"}' --json '{"requests":[{"updateCells":{"range":{"sheetId":<GID>,"startRowIndex":<R0>,"endRowIndex":<R0+1>,"startColumnIndex":<C0>,"endColumnIndex":<C0+1>},"rows":[{"values":[{"userEnteredValue":{"stringValue":"M/D Clinic Name"},"userEnteredFormat":{"backgroundColor":{"red":1,"green":1,"blue":0}}}]}],"fields":"userEnteredValue,userEnteredFormat.backgroundColor"}}]}'
  ```
> Tab sheetIds (names may change, gids are stable): Picase@ `775230687`, Claims@ `86730608`, Piteam@ `102974151`.
> If the target column already has content, DON'T overwrite — flag it to the user.

## Step 8b — Update the case INTAKE sheet (Treatments block)
Also record the clinic in the **case intake `.xlsx`** (the one in the case-folder root), in its
**Treatments** section, so the case file itself shows where the client is treating. Edit the
mounted `.xlsx` with openpyxl (back it up first to `~/.supplement-intake-backups/`; the mount
syncs to Drive).

Layout (read it live — don't assume): col **Q** holds the Treatments labels, and each client has a
value column — **R = Driver, S = Pass1, T = Pass2 …** (row 2 of cols R/S/T are the headers
`Driver`/`Pass1`/…). Each specialty is a small block: the **specialty row** (e.g. `Chiropracitc`)
takes the **clinic name**, then the next rows `Address` / `Phone` / `Email` take the clinic's
contact info. For a chiro referral, find the `Chiropracitc` block (typically Q3=Chiropracitc,
Q4=Address, Q5=Phone, Q6=Email) and write into the referred client's column:
```
R3 = <Clinic Name>            # e.g. "Optimum Health Rehab (Suwanee)"
R4 = <Clinic Address>
R5 = <Clinic Phone>
R6 = <Clinic Email>
```
(MRI/PM blocks are the same shape lower down — match the specialty label.) Write the referred
client's column only (driver → R, passenger → S/T). Font Nunito 10, left, no-wrap. For a
multi-client referral, fill each referred client's column. Don't clobber a different clinic
already in the block — flag it instead.

**Un-highlight the specialty-name cell.** The specialty row (e.g. the `Chiropracitc` cell, R3/S3/T3)
starts **yellow** (the "treatment pending" marker). Once you fill it with the clinic name, that
item is no longer pending → **remove the yellow highlight on that cell** (set fill to no-fill), the
same un-highlight convention as supplement-intake. (The Address/Phone/Email rows below it are not
highlighted, so just write their values.)

## Step 9 — Log run + confirm
Report: client, clinic + email, fields sent, # PD photos attached, the Gmail message id, the
label applied (+ color), the **blue star + moved-to-inbox** state, the Chat post, and the
Master-sheet cell updated. Clean up: `rm -rf ~/referral_work`.

## Step 10 — Output the WeChat (企业微信) client message (copy-paste, in Claude)
After everything is done, **print a ready-to-copy Chinese message in the Claude chat** (do NOT
send it anywhere — Klaus pastes it into the case's 企业微信 group himself). Output it as a single
plain-text block (no markdown tables) so it copies clean. It has **two sections**:

**1) 🏥诊所更新** — fixed template, fill in the clinic **name / address / phone** (no email here):
```
🏥诊所更新

🔔您好，我们已为您联系好诊所，医生会打电话联系您预约第一次治疗！

诊所信息⬇️
<Clinic Name>
<Clinic Address>
<Clinic Phone (digits only)>

🕒 确认时间：约好后请在群里告知我们您的预约日期和时间，谢谢！

📄 医生假条：若因伤无法工作/上学，请务必找医生开具至少一周的假条 (Doctor Excuse)。拿到后请拍照发给我们，这是为您申请误工费 (Loss of Earnings) 的核心凭证。

⚠️ 保持沟通：请勿擅自缺席治疗。如需改期，请务必提前在群里报备。

🆔 携带证件：无需支付任何费用，带上您的 ID 或驾照即可。
```

**2) 💉受伤更新** — per **referred** client, summarize their injuries + pain level **in Chinese**,
pulled from the intake's injury fields (driver: `Initial Injuries` C22 + the pain-scale value;
each passenger: their block's `Initial Injuries` + pain scale). One line per client in the form
`<Client>-<症状，顿号分隔>；疼痛程度 <X>/10`. Translate the English intake symptoms to Chinese
(e.g. Neck pain→颈部疼痛, back pain→背部疼痛, headache→头痛, dizziness→头晕, nausea→恶心,
vomiting→呕吐, difficulty sleeping→睡眠困难). Do NOT invent symptoms — only what the intake lists.
```
💉受伤更新

您好，这是基于您之前告诉我们，关于您当前受伤与症状的文字总结：

🤕您目前的症状包括：

<Client 1>-<症状>；疼痛程度 <X>/10。

<Client 2>-<症状>；疼痛程度 <X>/10。
（…one line per referred client…）

‼️见医生时，请务必将您的受伤情况完整告知，以便获得更精准的治疗方案。

‼️如果此时此刻您还有额外的受伤部位或症状，请立即告知我们进行更新。

⚠️ 温馨提醒:

🔍 别漏掉任何不适:有些车祸伤在当下并不明显,可能过几天才逐渐出现。请留意自己从头到脚的状况,任何真实的不适(即使轻微)都如实告诉医生,由医生评估处理。

✅ 如实且完整:请把身体所有不舒服的地方如实、完整地告诉医生,包括事故后才慢慢出现的症状。完整的就诊记录既有助于医生对症治疗,也让您的伤情有客观、连续的记录。若这份总结与您的实际感受有出入,请以您的真实感受为准,并在群里告诉我们更新。

🚩 及时核对信息:如果以上描述有任何遗漏或变化,请现在就在群里告诉我们,以便我们及时为您更新备案。
```
(For a single-client referral, the 受伤更新 section has just one symptom line. Always render the
two sections so Klaus can copy both at once.)

> When this skill is added to the plugin, append the standard run-log final step
> (`tools/log_run.py --skill chiro-referral --outcome ... --case "<client>" --carrier "<clinic>"`).

## Notes & gotchas
- **Auto-send is the default** (Step 6, per Klaus 2026-06-20): show the content, then send — no
  approval wait. Still **pause and ask** only when Step 3 finds a real problem (blank/inconsistent
  field, bad clinic email) or the user explicitly said "draft it". Outbound to a clinic carries
  client PII, so the content table + the data-sanity check (Step 3) are the safeguards now.
- FROM = the case's owning mailbox (resolved from the Master-sheet tab; see Constants), NOT
  klaus@ unless explicitly told. Signature = the handler/invoker (klaus when klaus runs it).
- Accident type = intake **F5 Point of Impact**, but render it as a SHORT phrase
  (e.g. `Sideswipe`, `T-bone`, `Rear-end`) — don't copy the full intake sentence. Verify in Step 3.
- v1 body is plain-text (no logo). The firm signature/footer text lives in the template ref.
- Don't fabricate any client field — copy from intake; if a value is blank, drop that line and
  flag it rather than inventing one.
