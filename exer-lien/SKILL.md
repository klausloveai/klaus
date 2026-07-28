---
name: exer-lien
description: |
  Sign the Exer Urgent Care lien (DocuSign) for a Lingtu Law PI client and notify Exer,
  for 凌图律所 / Lingtu Law Office (Law Office of Shenqi Cai APC). Use this skill whenever
  any of the following are mentioned: Exer lien, Exer Urgent Care lien, "sign lien" for an
  Exer referral, refer a client to Exer on a lien, "/exer-lien" for a named client, or when
  an Exer Urgent Care booking screenshot is shared. Typical invocation: a client/driver name
  (+ optionally the clinic location and appointment date/time from a booking screenshot). The
  skill finds the case in Drive, determines the owning team/CM, reads the intake sheet, opens
  the Exer DocuSign PowerForm in the browser (Claude-in-Chrome), fills + signs the lien as the
  firm/attorney (PAUSES before the irreversible signature/Finish), drafts and (on approval)
  sends the Exer notification email (simple format, signed lien PDF attached) from the case team
  mailbox to personalinjury@exerurgentcare.com (no Cc) with Klaus's preset signature, labels the sent
  email with the case's Gmail label + blue-stars it + moves it to inbox, and posts a 【Claude】 note
  to the case Chat space. Always trigger for any "sign the Exer lien / refer to Exer on a lien"
  request, even a partial one.
---

# Exer Urgent Care Lien

End-to-end Exer lien: find the case → drive the Exer DocuSign PowerForm (firm signs first) →
notify Exer (email from the case team mailbox) → label the email → post to the case Chat space.

Background on Exer's referral program: see memory [[exer_urgent_care_lien_referral]]. Exer
auto-forwards medical records/bills back once set up. The CLIENT must still complete their OWN
DocuSign signature and present the signed lien + photo ID at the clinic to be seen as a lien
patient — remind the user of this at the end.

## Invocation inputs
- **Client** — the patient's name (find the Drive case folder + intake row).
- **Clinic + appointment** — from the booking screenshot if shared (clinic name/address +
  date/time). If not given, ask, or send the notice without them (less useful for Exer).

## Step 1 — Locate the case, team, and client data
1. Drive `search_files`: `fullText contains '<client>' or title contains '<client>'` → find the
   case folder + the `*Intake Sheet.xlsx`.
2. Determine the **owning team** from the **PI Master Sheet** (id
   `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`): which tab the client sits in —
   **Claims@ / Piteam@ / Picase@** → that team's mailbox is the case mailbox.
   - Read tab client column, e.g. `gws sheets +read --spreadsheet <id> --range "Piteam@!A1:B80"`.
3. Download + parse the intake .xlsx (Python `zipfile`/XML, sharedStrings) → for the client get:
   **First/Last name, DOB, Phone, Email, Date of accident (DOL)**. Driver is column C; passengers
   are the Pass1/Pass2/Pass3/Pass4 blocks (B/C and E/F column pairs).
4. CM for the team (for the firm phone field): Claims@→Amos Feng (626-598-1129),
   Piteam@→Jerry Piao (626-598-6352), Picase@→Ryan Wei. See [[firm_directory]].

## Step 2 — Open the Exer DocuSign PowerForm (Claude-in-Chrome)
- Navigate to:
  `https://na3.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=959cdf8a-8926-490b-9644-96237b31fd37&env=na3&acct=caae766f-b5a7-4dc6-8863-4d6af54b6dad&v=2`
  - This is the **updated PowerForm** (switched 7/2/2026): it **pre-fills the law-office "release to"
    block in Doc 2** (Law Firm / Address / Facsimile), so those fields are already populated — skip
    typing them; just confirm they're correct and fill only the remaining blanks (phone, email,
    patient info, radios). The old PowerForm (`9537805b-…`) required typing the whole firm block.
- First page = "PowerForm Signer Information". Fill:
  - **Attorney or attorney representative** → Name `Shenqi Cai`, Email = **the case team mailbox**
    (e.g. `piteam@lingtulaw.com`) — this is the DocuSign signer-1 email where the completed copy lands.
  - **Client** → Name = client full name, Email = client's email from intake.
  - **Exer PI Manager** → **pre-filled (Virginia Hurtado / Virginia.Hurtado@exerurgentcare.com) — DO NOT change.**
- Click **Begin Signing**. The updated PowerForm goes **straight into the signing session — there is
  NO access-code page** (the old `9537805b` form asked for `092024`; the new one skips it). If an
  access-code page ever does appear, enter **`092024`** → Validate.
- "Review and continue" modal (message from Rosanna McCollough, Exer Urgent Care) → **Continue**.

## Step 3 — Fill + sign the documents (4 docs in the envelope)
Use the left **Start/Next** navigation; it jumps to required fields for the firm signer.
- **Doc 1 — Notice of Doctor's Lien:** Patient First/Last name, Patient DOB, Date of Accident
  (date field opens a calendar — it defaults to the current month, so click the prev-month `<` arrow
  to reach the DOL month, then the day). Then the **ATTORNEY SIGNATURE** (purple Sign box) —
  **Attorney Full Name = `Shenqi Cai` is now PRE-FILLED** on the new form (the old form needed it
  typed). DATED auto-stamps. Use the left **Next / Fill In** nav to reach the Sign box; if it keeps
  cycling through already-filled preset fields, just scroll up to Doc 1's signature box and click it
  directly.
- **Doc 2 — Authorization for Use/Disclosure:** patient **Name + DOB auto-carry from Doc 1** (no
  re-typing). The firm "release to" block is now **almost fully PRE-FILLED by the updated PowerForm**:
  - Attorney `Shenqi Cai` · Law Firm `Lingtu Law Firm` · Address `13191 Crossroads Parkway N, Suite 295`
    · City `City of Industry` · State `CA` · Zip `91746` · Facsimile `626-240-2046` — all **pre-filled**, confirm only.
  - **Phone — PRE-FILLED to `626-614-6666`, but OVERWRITE it** with the handling CM's direct line
    (NOT the 888 office line, and NOT the preset — see [[feedback_form_firm_phone_cm]]). Triple-click →
    `cmd+a` → Delete → type the CM line (e.g. Piteam@ = Jerry Piao `626-598-6352`).
  - **Email — PRE-FILLED to `piteam@lingtulaw.com`.** This is the records destination; if the case's
    owning team is NOT Piteam@ (i.e. Claims@ or Picase@), overwrite it with that team's mailbox.
  - **Patient Phone No.** = client's phone (this one is blank — type it).
  - **Records scope radio → Option 1** ("All health information … treatment received")
  - **PURPOSE radio → "Patient request"**
  - **Sensitive-info checkboxes (Mental health / HIV / Alcohol-drug) → leave BLANK** (unless told otherwise)
- **Doc 3** signature block is `(patient/legal representative)` → **leave blank** (the CLIENT signs it later).
- **Doc 4** = instructions only.

**GOTCHA — after clicking the Sign box the view auto-jumps to Doc 2**, so the `Attorney Full Name`
box right under the signature on Doc 1 is easy to miss. After signing, scroll back to Doc 1 and
confirm `Shenqi Cai` actually landed in that box (Doc 2's `(Attorney)` field auto-fills FROM it —
if Doc 2 `(Attorney)` is empty/highlighted, the Doc 1 name didn't take; fill it).

**APPROVAL GATE:** the attorney e-signature is an irreversible legal act. Before clicking the
Sign box / **Finish**, confirm with the user (unless they've already said "sign it / go all the
way"). On first use DocuSign adopts a `Shenqi Cai` signature style (accept default). After Finish,
the "Your document has been signed" dialog → **Close**. The envelope auto-routes to the client to
e-sign; Exer (Virginia) is a recipient and gets the completed copy automatically. Record the
**Envelope ID** (shown at top of each doc).

## Step 4 — Notify Exer (email)
Send FROM the **case team mailbox** with **Klaus's preset Gmail signature** (Exer is Klaus's
program — see [[feedback_email_signature_sender]]). The team mailbox must be reachable by `gws`
via its own config dir (see [[gws_auth_scopes]]; piteam@ store = `~/.config/gws-piteam`).
- Fetch Klaus's preset signature (Gmail API does NOT auto-append it):
  `gws gmail users settings sendAs get --params '{"userId":"me","sendAsEmail":"klaus@lingtulaw.com"}'`
  → take `.signature` (HTML) and embed it in an **HTML** body.
- **To:** `personalinjury@exerurgentcare.com` — **To ONLY, no Cc** (Klaus dropped the Rosanna Cc;
  personalinjury@ is the PI-team distro).
- **Subject:** `New Lien Patient - <Client> | Exer Urgent Care - <clinic>`
- **Attach the signed COMBO FORM lien PDF** (multipart/mixed; base64) — the *Notice of Doctor's Lien +
  Authorization for Use or Disclosure*, filename e.g. `Lien Authorization for Disclosure.pdf`. (Attach
  the DocuSign-executed copy when available; for a same-day walk-in where the client signs at the front
  desk, attach the blank/standard form.)
- **Body** (HTML) — **Klaus's calibrated SIMPLE format** (keep it short; client-as-actor, non
  attorney-driven — see [[feedback_no_attorney_driven_language]]). Fill `<he/she>` by gender:
  ```
  Hi Exer Urgent Care PI Team,

  Our client(s) sustained injuries in an auto accident, and <he/she> has signed the lien.

  DOL-<DOL>
  <Client Name>
  DOB <DOB>
  P-<Phone>

  Appointment/Walk in info:

  <date>
  Exer Urgent Care - <clinic>

  Let me know if you have any questions.
  ```
  (Render as COMPACT HTML — Klaus calibrated 7/3: do NOT wrap every line in its own `<p>` (Gmail adds
  big gaps and the email looks stretched). Use ONE `<div>` with single `<br>` between lines and `<br><br>`
  only between paragraphs — e.g.
  `Hi …,<br><br>Our client … lien.<br><br>DOL-…<br><Name><br>DOB …<br>P-…<br><br>Appointment/Walk in info:<br><date><br>Exer Urgent Care - <clinic><br><br>Let me know …<br><br>` + Klaus's preset
  signature. The DOL/name/DOB/phone block and the date/clinic block are tight single-spaced lines. Do NOT
  add an Envelope ID line or a long "we executed the lien" paragraph — the simple block above replaces
  the old verbose body.)
- Build raw MIME (multipart/mixed with the PDF part) + create the draft in the team mailbox:
  `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-<team> gws gmail users drafts create --params '{"userId":"me"}' --json '{"message":{"raw":"<b64url>"}}'`
- Show the draft for review. **On the user's OK, send** (outbound gate):
  `… gws gmail users drafts send --params '{"userId":"me"}' --json '{"id":"<draftId>"}'` (the
  `--params {"userId":"me"}` is REQUIRED or send silently no-ops). Capture the sent message id.

## Step 5 — Label + blue-star + move to inbox
Find the **existing combined case label** in the team mailbox (one label per case, driver first —
[[feedback_case_label_one_per_case]]): `… gws gmail users labels list` → match the case name.
**If no case label exists** (brand-new case), create one (yellow, per new-case convention):
`… gws gmail users labels create --params '{"userId":"me"}' --json '{"name":"<Client>","labelListVisibility":"labelShow","messageListVisibility":"show","color":{"backgroundColor":"#fbe983","textColor":"#594c05"}}'`
Then apply **case label + `BLUE_STAR` + `INBOX`** to the sent message (blue star + move to inbox — same
convention as the referral skills; Gmail auto-adds `STARRED` alongside `BLUE_STAR`):
`… gws gmail users messages modify --params '{"userId":"me","id":"<sentMsgId>"}' --json '{"addLabelIds":["<labelId>","BLUE_STAR","INBOX"]}'`

## Step 6 — Post to the case Chat space
Find the case Chat space (`gws chat spaces list` → display name = case folder name) and post
(see [[feedback_exer_lien_chat_format]]). Two accepted formats:
- **Walk-in / simple notify** (current default): one line stating the plan —
  ```
  gws chat spaces messages create --params '{"parent":"spaces/<id>"}' --json '{"text":"【Claude】\n<Client> will go to Exer Urgent Care - <clinic> on <date> on lien basis."}'
  ```
  (e.g. `Baolian Kuang will go to Exer Urgent Care - Glendora on 7/1/2026 on lien basis.`)
- **Full sign+notify (DocuSign) flow**: the two-line ✅ format —
  ```
  gws chat spaces messages create --params '{"parent":"spaces/<id>"}' --json '{"text":"【Claude】\nExer Urgent Care Lien Signed✅\nEmail sent to confirm appointment: <clinic>, <date> <time>✅"}'
  ```
  (e.g. `Email sent to confirm appointment: Exer Urgent Care - Montebello, 6/21 4:00 PM✅`)
**Run Chat with the DEFAULT gws config (klaus@) — NOT the team config dir** (the team mailbox
e.g. piteam@ may not be a Chat-space member / lack chat scope, so it silently no-ops). So do NOT
prefix this command with `GOOGLE_WORKSPACE_CLI_CONFIG_DIR`.

## Step 7 — Update the UrgentCare field on the intake + Master sheet
Record the Exer visit on both sheets, using the **same `<clinic>, <date> <time>` string** as the
Chat line (e.g. `Exer Urgent Care - Montebello, 6/21 4:00 PM`). Look up the Exer clinic's street
address (web search) for the email in Step 4, but the sheet value is just the clinic+appt string.
Use Sheets API `batchUpdate`→`updateCells` with
`fields:"userEnteredValue,userEnteredFormat.backgroundColor"` (preserves other formatting); get each
tab's `sheetId` via `spreadsheets.get`.
- **Intake sheet** (the case's `*Intake Sheet`): the **UrgentCare?** row's label is in col B, the
  VALUE is in col **C** (e.g. C20). Set C-value = the clinic+appt string AND **remove the highlight**.
  First check the file's `mimeType` (some intakes are native gsheet, some are still raw `.xlsx`):
  - **native gsheet** (`…spreadsheet`): Sheets API `batchUpdate`→`updateCells` on C-cell with
    `backgroundColor {red:1,green:1,blue:1}` (white = un-pending; cf. [[intake_sheet_highlight_convention]]).
  - **raw .xlsx** (`…spreadsheetml.sheet` — Sheets API does NOT work on it): download via Drive, do a
    **surgical XML edit** of `xl/worksheets/sheet1.xml` (find `<c r="C20" s="N" t="s"><v>idx</v></c>`,
    replace with `<c r="C20" s="N" t="inlineStr"><is><t>…</t></is></c>` — KEEP the `s` style attr,
    repackage the zip member-by-member so nothing else changes), then `gws drive files update --params
    '{"fileId":…,"supportsAllDrives":true}' --upload <new.xlsx>`. Only swap the style if the cell is
    actually yellow (s=9→s=8); if it's already a normal style (e.g. UrgentCare was answered "No"),
    leave `s` as-is. Verify by re-reading the cell after upload. (Surgical XML, NOT an openpyxl
    round-trip, which can drop data-validations/conditional formatting on a live intake.)
- **Master sheet** (`1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`) — always a native gsheet, use Sheets
  API `updateCells` (`fields:"userEnteredValue,userEnteredFormat.backgroundColor"`); the client's tab
  (Claims@/Piteam@/Picase@) **DRIVER row**: column **"Urgent Care"** (= col **P** for Picase@ gid
  775230687 AND Piteam@ gid 102974151 as of 7/25/2026 — a **Retainer** column was inserted at C,
  shifting Urgent Care from O→P. **Always map by the header NAME, not a fixed letter** — read row 1
  and `spreadsheets.get` first; the layout may shift again).
  Set = the clinic+appt string AND **highlight blue = "in progress"** → `#c2e7ff` =
  `backgroundColor {red:0.7608,green:0.9059,blue:1.0}`. Only the driver/main row gets a background —
  passenger rows stay uncolored ([[feedback_tracking_sheet_passenger_rows]]).
- Master has an intake→master live sync on cols M–S, but a direct master edit **locks** the cell
  ([[intake_master_sync]]); set the intake first, then master, so the master value/color sticks.

## Step 8 — Remind the user + output the client message
Tell the user to have the **client complete their own DocuSign e-signature** (sent to the client's
email) and bring **photo ID + the signed lien** to register at the clinic. If the visit is a pre-op,
Exer also needs the pre-op order form. If the client visited Exer WITHOUT a lien, request records via
Chartswap.com instead.

Then **output a ready-to-send Chinese client message** (Exer clients are Chinese-speaking — keep it
中文). It is a copy-paste deliverable for the CM to forward (WeChat/text); the skill does NOT send it.
Fill the tokens from the case data. If it's a walk-in with no fixed time, write `<date>(周X)walk-in
随到随诊`. **No greeting line and no signature/落款** (Klaus's calibrated format — the CM adds those if
needed). Opening uses the **client-as-actor** phrasing "您将以 lien 方式到 Exer 就诊" (NOT "我们已为您安排",
per [[feedback_no_attorney_driven_language]]).

**Variant A — clinic confirmed** (you know which Exer + address/time):
```
您将以 lien(留置权)方式到 Exer Urgent Care 就诊——先治疗,医疗费用日后从案件赔偿中结算,您现在无需自付。请按以下三步操作:

1️⃣ 签文件:您会收到一封 DocuSign 邮件(发件方 Exer Urgent Care / 律所),请点开完成电子签名 ✍️

2️⃣ 就诊当天带两样:
您的带照片证件(驾照/护照/ID);
告诉前台你是 lien 病人,给他们看你签好的 lien 文件

3️⃣ 就诊信息:
📍 诊所:{{诊所名称}}
🏠 地址:{{诊所地址}}
🕒 时间:{{日期时间 / walk-in 随到随诊}}

就诊后诊所会把病历和账单直接发给我们,您无需操心。任何疑问请联系您的案件经理 {{CM 姓名}}({{CM 电话}})。
```

**Variant B — clinic NOT confirmed** (client picks the nearest open Exer themselves — Exer is a chain):
```
您将以 lien(留置权)方式到 Exer Urgent Care 就诊——先治疗,医疗费用日后从案件赔偿中结算,您现在无需自付。请按以下三步操作:

1️⃣ 签文件:您会收到一封 DocuSign 邮件(发件方 Exer Urgent Care / 律所),请点开完成电子签名 ✍️

2️⃣ 就诊当天带两样:
您的带照片证件(驾照/护照/ID);
告诉前台你是 lien 病人,给他们看你签好的 lien 文件

3️⃣ 就诊信息:
Exer Urgent Care 是连锁诊所。您可在 Google Maps 搜索 "Exer Urgent Care",就近选一家显示"营业中 / Open"的直接 walk-in 即可。正常营业时间 早 8:00–晚 8:00;个别节假日可能提前关门(如下午 5:00),以 Google Maps 实时显示为准。

就诊后诊所会把病历和账单直接发给我们,您无需操心。任何疑问请联系您的案件经理 {{CM 姓名}}({{CM 电话}})。
```

## Notes / gotchas
- Multi-client case: run once per client; each is a separate envelope. Use the per-client intake block.
- Records-scope / Purpose / sensitive boxes are the firm signer's required fields (not the client's).
- The firm-signed-only PDF is NOT the executed copy; the completed PDF arrives at the team mailbox +
  Exer once the client signs — no need to attach a half-signed copy.
- Reuses conventions from [[exer_urgent_care_lien_referral]], [[feedback_form_firm_phone_cm]],
  [[feedback_email_signature_sender]], [[feedback_send_from_case_mailbox]], [[firm_directory]],
  [[feedback_exer_lien_chat_format]], [[intake_master_sync]], [[intake_sheet_highlight_convention]],
  [[feedback_tracking_sheet_passenger_rows]].
