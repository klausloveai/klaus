---
name: it
description: Set up a new client case folder for SIA 高徒 / Lingtu Law Office in Google Drive — match the case type against the template library, mirror its subfolders, write the intake background doc, share "0. Shared Folder" with the client, keep a running Activity Log, and link the folder to the client's case in Lingtu Data (client code / matter code come from Lingtu Data first). Use whenever the user registers a new client and wants a case folder built — e.g. "帮XX客户建案件文件夹", "案件类型是XX，客户叫XX，建文件夹" (any case type) — or hands over a 客户跟进表 row/screenshot with 案件类型 + 客户名称. Also covers adding intake notes to an existing case, updating a client's tracking-sheet row (priority, notes, highlight, payment status), or reviewing/editing this workflow itself. Triggers without the word "skill" — any request to create/mirror a case folder or log a client into the tracking sheet counts.
---

# it — Case Folder Setup (SIA 高徒 / Lingtu Law Office)

Handles every case type the firm's template library has, not a fixed set —
match whatever 案件类型 the user gives against the templates and tracking-sheet
tabs live, rather than assuming which ones exist. Always use `gws` (CLI), never
click through the Drive/Sheets web UI — the API does in one call what clicking
takes a dozen steps for.

```bash
export PATH="$HOME/.local/bin:$PATH"   # gws lives here; run once per session
```
If any `gws` call 401s / `invalid_grant`: run `gws auth login -s drive`, paste
the printed URL to the user, ask them to approve it in their own browser. Never
touch their Google password/2FA.

**Every `gws drive files list` call must include** `supportsAllDrives`,
`includeItemsFromAllDrives`, `corpora: allDrives` in `--params` — omitting these
silently returns an empty list instead of an error, which reads as "folder is
empty" when it isn't.

## Known constants (don't re-discover these)

| What | Value |
|---|---|
| Template library root | `1acicNY34j3v9f15XqxiEd7StCz8-IEYB` ("0. Template") |
| Client destination root | `1RXWQsTkLdlIHUdbu2Rzs4HGH53tftzNm` ("0. Pending") |
| Case Tracking spreadsheet ID | `1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE` |
| — lives in shared drive | "SIA 高徒" (`0AE7q4ToQFsarUk9PVA`) |
| To Do List tab (universal, every case) | sheetId `228362949`, header row 2, data starts row 3 |
| Non-category tabs (skip when tab-matching) | `Dashboard`, `Helper`, anything titled "...No Longer Use" |

The spreadsheet also has one tab per case *category* (Family Based
Immigration, GC/Citizen, I-485 Package, Change of Status, EB23, BH, U/T,
SIJS, Other, H1B, ...) — which one a given 案件类型 belongs to is looked up,
not assumed; see Step 5's registry, which is the growing source of truth for
category-tab layouts. If the spreadsheet ID itself ever 404s, see
`references/tracking-sheet.md` before improvising.

## What you need from the user

- **案件类型** (case type), e.g. "131 回美证"
- **客户名称** (client name), e.g. "Zhehui Li"
- Whether it's a **multi-applicant case** (e.g. children filed together). If
  the intake info doesn't make this obvious, ask — don't guess.
- **客户邮箱** (client email), if available — needed for Step 7 (sharing "0.
  Shared Folder" with the client). Not required to proceed: if it isn't
  available yet, do Steps 1-6 and 8-10 now and just skip Step 7, don't block
  on it or guess an address.

## Step 0 — 先在 Lingtu Data 里找到客户编号和案件编号（2026-11-02 起必做）

Lingtu Data（Supabase「凌图律所统一数据库」，连接器工具 `find` / `sign_lead` / `link_case_folder` / `log_event`）是案件的正本。建 Drive 案卷之前：

1. 用 `find` 按客户姓名、电话、微信或编号查客户，拿到 **客户编号**（5 位数）和 **案件编号**（如 `47765-IMM1`）。
2. 已经有在办案件：直接用这个案件编号，往下走。
3. 线索还没签约、没有案件：先签约。在工作台「客户跟进」里点「签约」，或者用 `sign_lead`。合同额、付款方式（一次付清 / 分几期）、主办、协办、合作方（没有就「无」）要先跟用户核对清楚，**不要猜**。签约后再建案卷。
4. 查不到这个客户：先用 `log_lead` 登记，再签约。不要在没有客户编号的情况下建案卷。

客户编号要带进 Step 2 的文件夹名，Step 5A 要把文件夹链接写回这个案件。

## Step 1 — Match the template folder

```bash
gws drive files list --params '{"q": "'"'"'1acicNY34j3v9f15XqxiEd7StCz8-IEYB'"'"' in parents and trashed=false", "fields": "files(id,name,mimeType)", "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives"}'
```
Match loosely: strip spaces, compare the leading case number. "131 回美证" ↔
"131回美证" counts as a match. Zero or multiple plausible matches → stop and
ask which template, don't guess (wrong template = wrong document checklist).

**SIJS has no folder here.** There's a *separate*, non-template "SIJS" Drive
folder (id `1xJxxRmAZdbgmd--jyofL2eGz98VNhMGg`, no discoverable parent —
found via a Drive-wide name search, not under this template root) holding
real client subfolders (Youyou Wang, Jingcheng Xu, Miaomiao Bai, Yuxin Zhang,
Ziyue Peng) plus a `0 SIJS - SAMPLE` sample subfolder (structure: `1`, `2`,
`Pleading`, `POS` — a state-court juvenile/probate layout, nothing like the
9-folder template pattern). Confirmed with the user 2026-08-10: SIJS cases
still go through the standard Step 1-10 flow under "0. Pending", borrowing
**I-485 Package**'s 9-folder structure as the closest stand-in (SIJS
petitions typically lead into I-360/I-485). If a future case needs the
court-pleading materials instead, point the user at that separate SIJS
folder — don't assume, ask which structure they want.

## Step 2 — Create the case root folder

Name: `{案件类型}-{客户姓名} - {客户编号}` — case-type text as it appears in the
template folder name, hyphen, name, then the 5-digit client code from Step 0.
E.g. `131回美证 -Zhehui Li - 47765`. (Folders made before 2026-11-02 have no
code; leave them as they are.)
Check the destination root doesn't already have this name (possible duplicate
registration — if it does, stop and ask) before creating:

```bash
gws drive files create --json '{"name": "<CASE ROOT NAME>", "mimeType": "application/vnd.google-apps.folder", "parents": ["1RXWQsTkLdlIHUdbu2Rzs4HGH53tftzNm"]}' --params '{"supportsAllDrives": true, "fields": "id,name,parents"}'
```

## Step 3 — Mirror the template's current subfolders

Read live every time — never hardcode a subfolder list, the firm edits
templates over time (last seen: `0. Intake`, `0. Shared Folder`, `1. Initial`,
`2. Form`, `3. Draft`, `4. Final`, `5. Scanned`, `6. I-797`, `7. Deleted` — 9
folders, treat only as a sanity check).

The template root may also contain **files** (not just subfolders) — in
particular an "Activity Log" template doc. Files at the template root level are
handled in Step 6, not here; skip them when creating subfolders.

```bash
gws drive files list --params '{"q": "'"'"'<TEMPLATE_FOLDER_ID>'"'"' in parents and trashed=false", "fields": "files(id,name,mimeType)", "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives", "orderBy": "name"}'
```
For each **folder** returned, create a same-named subfolder under the case root
and keep a name→id map (needed in Steps 4, 6, 7). Ignore any docs or files at
this level — they go to the case root in Step 6.

```bash
gws drive files create --json '{"name": "<SUBFOLDER_NAME>", "mimeType": "application/vnd.google-apps.folder", "parents": ["<CASE_ROOT_ID>"]}' --params '{"supportsAllDrives": true, "fields": "id,name"}'
```

## Step 4 — Intake background doc (in "0. Intake")

If the user gives intake context (tracking-sheet screenshot fields, or notes
like fees/biometrics/urgency), capture it as a Google Doc in "0. Intake" — this
is the client-facing record, distinct from Step 5's tracker row and Step 9's
internal Activity Log.

```bash
gws drive files create --json '{"name": "客户背景 - <客户姓名>", "mimeType": "application/vnd.google-apps.document", "parents": ["<0.INTAKE_SUBFOLDER_ID>"]}' --params '{"supportsAllDrives": true, "fields": "id,name,parents"}'
gws docs +write --document "<DOC_ID>" --text '客户背景

登记时间：<...>
客户名称：<...>
案件类型：<...>
备注：<screenshot 里的备注原文>
订单总价：<...>
成交日期：<...>
收款日期：<...>

Intake 备注
<用户额外给的备注，原文照抄>
'
```
If this case already has an intake doc from an earlier run, `+write`-append a
new dated block instead of creating a second doc.

## Step 5A — 把案卷链接写回 Lingtu Data（必做）

文件夹建好后，用 `link_case_folder` 把案卷根目录链接挂到 Step 0 的案件上（`matter_code` + `drive_folder_url`，有 Activity Log 就一起给 `activity_log_url`）。案件上已经挂了别的文件夹时，工具会拒绝，先问用户是不是重复建案卷，不要直接 `overwrite`。

挂好以后，工作台「合同管理」「我的案子」和客户全景页上，点进去就是这个案卷。

## Step 5 — Lingtu Case Tracking Sheet（2026-11-02 起停用，跳过）

Joe 11/2 定：今天起完全切换到 Lingtu Data，Tracking Sheet 已经设成只读（只有 Joe、Elena 能改）。**跳过整个 Step 5 和 Step 9 里写 Tracking Sheet 的部分**，案件信息只写 Lingtu Data（Step 0、5A）。下面的旧说明只留作查旧数据时参考。

Two separate writes: "To Do List" always (fixed tab, fixed columns, below),
and the case's *category* tab, which you identify fresh each time — the firm
adds case types faster than any hardcoded mapping could track, so don't guess
a tab from the case number alone.

### 5a. To Do List (fixed — every case goes here)

Header is row 2; data starts row 3. Full column layout (rows 1-2 verified 2026-08-14):

| Col | Field | Type |
|---|---|---|
| A | Client Name | text |
| B | Case Type | text |
| C | Priority | dropdown `0`-`4`, strict — default `0` if unspecified |
| D | Notes | text — put the **intake doc** link here (客户背景 Google Doc URL) |
| E | Assignee | dropdown [Lavender, Nancy, Li Zhang, Cassie, Christina] |
| F | $ | boolean checkbox — leave unset unless told |
| G | M | boolean checkbox — leave unset unless told |
| H | 📃 | boolean checkbox — leave unset unless told |
| I | PD | blank unless told |
| J | Due Date | blank unless told |
| K | Timeline | blank unless told |
| L | Mailing Status | blank unless told |
| M | Tracking Number | blank unless told |
| N | Case Status | blank unless told |
| O | Case# | blank unless told |
| P | Google Drive | text — put the **case root folder** link here (`https://drive.google.com/drive/folders/<CASE_ROOT_ID>`) |

New clients go right after the header, at **row 3**, not appended at the
bottom — this tab sorts newest-first.

### 5b. Category tab (auto-detect)

1. List every tab once:
   ```bash
   gws sheets spreadsheets get --params '{"spreadsheetId": "1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE", "fields": "sheets(properties(sheetId,title))"}'
   ```
   Drop `Dashboard`, `Helper`, and anything titled "...No Longer Use" — those
   aren't case-category tabs.
2. Check the **known-tabs registry** below first. If this 案件类型 (or an
   equivalent English case name, e.g. 131回美证 = "I-131 Application") is
   already mapped to a tab, use it directly — skip straight to writing.
3. Otherwise, search for it: read each remaining candidate tab's header row
   in one call (multiple ranges) to find which column holds "Case Type":
   ```bash
   gws sheets spreadsheets get --params '{"spreadsheetId": "1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE", "ranges": ["'"'"'Tab A'"'"'!1:1", "'"'"'Tab B'"'"'!1:1"], "includeGridData": true, "fields": "sheets(properties(title),data(rowData(values(formattedValue))))"}'
   ```
   then read each tab's Case Type column (another single multi-range call)
   and look for rows matching this 案件类型 loosely (shared case number or
   keyword — "131" / "回美证" / "I-131" are all the same case).
4. Exactly one tab has matches → that's the target. Zero matches (first case
   of this type ever) or matches split across tabs → stop and ask the user
   which tab it belongs to, don't guess.
5. Once confirmed, read one existing data row there with `includeGridData` to
   learn its column types (dropdown/checkbox/formula — see "formatting"
   below), then **add it to the registry** (tab name, sheetId, header row,
   Case Type column, and its full column map) so future cases of this type
   skip steps 1-3 entirely.

#### Known-tabs registry (check first, extend as you learn more)

| Tab | sheetId | Header row | Case Type col | Column map |
|---|---|---|---|---|
| Family Based Immigration | `368386619` | 1 | E | see below |
| GC/Citizen | `1981020956` | 1 | E | see below |
| SIJS | `788341383` | 1 | E | see below |
| Change of Status | `235755894` | 1 | E | see below |
| Other | `268172406` | 1 | E | see below |
| EB23 | `1386162211` | 1 | F | see below |

**Family Based Immigration columns** (data starts row 2, append after the last used row —
sequential, not newest-first; covers 婚绿, Marriage/GC, I-130, I-751, etc.):

| Col | Field | Type |
|---|---|---|
| A | No | formula `=row()-1`, don't hand-type |
| B | Year | number |
| C | Month | text, full month names |
| D | Client Name | text |
| E | Case Type | text, e.g. "婚绿", "Marriage/GC/US", "I-130 Intent to Deny" |
| F | Priority | number/dropdown `1`-`4` — default `1` if unspecified |
| G | Assignee | text, blank ok |
| H | Other Notes | text — put doc links and notes here |
| I | Service Fee | number (formatted as $) |
| J | Already Paid | number |
| K | Pending Payment | formula `=I<row>-J<row>` |
| L | Service Fee Paid | boolean checkbox, set directly — recent rows (61+) hold plain TRUE/FALSE, not a formula (verified 2026-10-06) |
| M | USCIS Fee | text, uses `$` prefix — `"$<amount> Paid"` or `"Unpaid"` |
| N | USCIS Paid | boolean checkbox |
| O-Q | PP Date / Steps / Due Date | blank unless told |
| R | Shipping Status | dropdown (`Printed` / `Shipped` / `Delievered`) |
| S | Shipping# | text |
| T | Case Status | text/dropdown (`Received` / `Approved` / etc.) |
| U | Case# | text |
| V | Notes | text |
| W | I-485 Package | text (trailing space in header — leave blank unless told) |

Template folder for this tab's cases is `Family Base` (`1SPnOvXTWhoHOAU7HWHTMmf1dLwUiUALN`); 亲属移民 / 婚绿 both use it. Case root names in "0. Pending" use the user's Chinese case type, not the template name (e.g. `婚绿 -Jingbo Zhang`, `亲属移民 -Hua Li`).

**GC/Citizen columns** (data starts row 2, append after the last used row —
this tab is sequential, not newest-first):

| Col | Field | Type |
|---|---|---|
| A | No | formula `=row()-1`, don't hand-type |
| B | Year | number |
| C | Month | dropdown, full month names ("Feburary" is misspelled in the list — use it as-is) |
| D | Client Name | text |
| E | Case Type | text, e.g. "I-131 Application" |
| F | Priority | dropdown `1`-`4` (no `0`!) — default `1` if unspecified |
| G | Assignee | text, blank ok |
| H | Service Fee | number |
| I | Already Paid | number |
| J | Pending Payment | formula `=H<row>-I<row>` |
| K | Service Fee Paid | formula `=IF(J<row>=0, TRUE, FALSE)` (checkbox display, don't hand-type) |
| L | USCIS Fee | **text**, not a bare number — `"<amount> Paid"` (e.g. `"630 Paid"`, no `$`) if paid, `"Unpaid"` if not. Multiple applicants sharing one fee: `"630*2 Paid"`; a surcharge on top: `"630 + $60"`. Older rows in the sheet just have a bare number here — that's legacy, not the convention to copy. |
| M | USCIS Paid | boolean checkbox, set directly — keep consistent with L (`TRUE` for "...Paid", `FALSE` for "Unpaid") |
| N-T | PP Date/Progress/Due Date/Shipping.../Case#/... | leave blank unless told |
| U | Other Notes | text (put doc links here) |

**SIJS columns** (data starts row 2, append after the last used row —
sequential, not newest-first, same as GC/Citizen):

| Col | Field | Type |
|---|---|---|
| A | No | formula `=row()-1`, don't hand-type |
| B | Year | number |
| C | Month | dropdown, full month names (same list as GC/Citizen, "January " has a trailing space, "Feburary" misspelled — use as-is) |
| D | Client Name | text — convention here is the **minor/beneficiary's name**, not a co-registering guardian/sponsor (e.g. "Youyou Wang", "Yuxin Zhang"); put the guardian/contact in Note instead |
| E | Case Type | text, "SIJS" |
| F | Priority | dropdown `1`-`4` (no `0`!) |
| G | DDL | text — SIJS-specific: the age-out deadline (e.g. "满21岁" cutoff), free text, no format enforced |
| H | Assignee | blank ok |
| I | Service Fee | **text**, not a bare number — total plus the installment breakdown, e.g. `"10000(分期7000+3000)"`, `"9500(分期6500+3000)"`, `"1400+1400"` |
| J | Already Paid | number, blank ok |
| K | Pending Payment | **plain, not a formula** on this tab (unlike GC/Citizen) — Service Fee is often non-numeric text, so leave blank rather than writing `=I-J` |
| L | Service Fee Paid | boolean checkbox, set directly (not formula-driven here) |
| M | USCIS Fee | text — same convention as GC/Citizen: `"Unpaid"` if owed but not yet collected, `"<amount> Paid"` once collected. Don't assume a fee is waived/not-charged without the user saying so explicitly — a first pass on this tab wrongly wrote "不收取" from an ambiguous "政府费用没收" note that actually meant "owed, not yet collected"; when in doubt ask or default to "Unpaid" and flag the assumption |
| N | USCIS Paid | boolean checkbox |
| O | Google Drive | dropdown (`Contract Unsigned` / `Materials Missing` / `WE NEED TO TAKE ACTION`) — despite the header name this is a status flag, not a link; leave blank unless told |
| P | Due Date | blank unless told |
| Q | Result | blank unless told |
| R | Note | text — put guardian/contact info, language/translation notes, communication preference, and doc links here |

**Change of Status columns** (data starts row 2, append after the last used
row — sequential, not newest-first, same as GC/Citizen; covers I-539 COS
cases, e.g. "H1B转B1/2"):

| Col | Field | Type |
|---|---|---|
| A | No (header "COS") | formula `=row()-1`, don't hand-type |
| B | Year | number |
| C | Month | dropdown, full month names (same list as GC/Citizen — "Feburary" misspelled — use as-is) |
| D | Client Name | text |
| E | Case Type | text, e.g. "B2 Extension", "H1B转B1/2 COS" |
| F | Priority | dropdown `1`-`4` (no `0`!) — default `1` if unspecified |
| G | Due Date | blank unless told |
| H | Assignee | text, blank ok |
| I | Service Fee | number |
| J | Already Paid | number |
| K | Pending Payment | formula `=I<row>-J<row>` |
| L | Service Fee Paid | boolean checkbox, set directly (not formula-driven here) |
| M | USCIS Fee | text, with a `$` prefix on this tab (unlike GC/Citizen) — `"$<amount> Paid"` / `"$<amount> Unpaid"`, multiple fees concatenated with `+` (e.g. `"$420 Paid+ $350 Paid +$1965 Paid"`); free-form Chinese notes also appear (`"政府规费Unpaid"`, `"暂未支付"`) — match the existing style, don't force English |
| N | USCIS Paid | boolean checkbox |
| O | PP Date | blank unless told |
| P | Steps | blank unless told |
| Q | Shipping Status | dropdown (`Printed` / `Shipped` / `Delievered`) |
| R | Shipping# | text |
| S | Case Status | dropdown (`Received` / `RFE` / `Denied` / `NOID/NOIR` / `Approved` / `Withdrawn`) |
| T | Case# | text |
| U | Other Notes | text (put doc links here) |

**EB23 columns** (data starts row 2, append after the last used row —
sequential, not newest-first; covers EB2/EB3 PERM + I-140 cases, e.g.
"EB2/3 - PERM", "EB3 - PERM"):

| Col | Field | Type |
|---|---|---|
| A | No | formula `=row()-1`, don't hand-type |
| B | Year | number |
| C | Month | text, full month names |
| D | Client Name | text — the **employee/beneficiary** |
| E | Employer Name | text, e.g. "Education Tomorrow Inc." |
| F | Case Type | text, e.g. "EB2/3 - PERM" |
| G | Priority | blank ok (existing rows mostly blank) |
| H | Assignee | blank ok |
| I | Status | text, e.g. "Ads", "EAT-9141" |
| J | Service Fee | number |
| K | Already Paid | number |
| L | Pending Payment | formula `=J<row>-K<row>` |
| M | Service Fee Paid | formula `=IF(L<row>=0, TRUE, FALSE)` |
| N | Google Drive | text — case root folder link |
| O | Due Date | blank unless told |
| P | ETA 9141 | boolean checkbox |
| Q | Determination Date | date/text |
| R | ETA 9089 | text (case no.) |
| S | ETA 9089 Approval Date | date |
| T | I-140 | boolean checkbox |
| U-W | I-140 Submission Date / Status / PP Date | blank unless told |
| X | I-485 Package | boolean checkbox |
| Y-Z | I-485 Shipping Status / Shipping# | blank unless told |
| AA | Case Status | blank unless told |
| AB | Approval Notice | boolean checkbox |
| AC | Case# | text |
| AD | Other Notes | text — put doc links / G-28 note / fee notes here |

**Other columns** (data starts row 2, append after the last used row —
sequential, not newest-first; catches misc cases like I-824, NOID, lawsuits,
OPT reviews, etc.):

| Col | Field | Type |
|---|---|---|
| A | No | formula `=row()-1`, don't hand-type |
| B | Year | number |
| C | Month | text/dropdown, full month names |
| D | Client Name | text |
| E | Case Type | text, e.g. "I-824", "OPT NOID", "起诉移民局" |
| F | Priority | number `1`-`4` — default `1` if unspecified |
| G | DDL | text, blank ok |
| H | Assignee | text, blank ok |
| I | Service Fee | number |
| J | Already Paid | number |
| K | Pending Payment | formula `=I<row>-J<row>` |
| L | Service Fee Paid | formula `=IF(K<row>=0, TRUE, FALSE)` (checkbox display, don't hand-type) |
| M | USCIS Fee | number (bare number ok on this tab — existing rows use bare numbers, not "Paid" suffix) |
| N | USCIS Paid | boolean checkbox |
| O | (blank/status) | leave blank unless told |
| P | Due Date | blank unless told |
| Q | Result/Notes | text, shipping tracking, mailing dates, etc. |
| R | Note | text — put doc links and other notes here |

For any tab not yet in the registry, find its last used row the same way as
GC/Citizen unless its own header implies otherwise (e.g. a newest-first sort
like To Do List's) — read column A fully (`majorDimension: COLUMNS`); trailing
blanks are trimmed from the response, so `len(values) + 1` is the next free
row.

**Formula and dropdown columns must stay formulas/dropdowns, not text** — a
blank/new row has no validation on it until you copy it over from an adjacent
data row (`copyPaste` with `PASTE_FORMAT` + `PASTE_DATA_VALIDATION`, or
`insertDimension` with `inheritFromBefore` pointed at a real data-row
neighbor) — see the reference file for the exact request shapes. Write actual
formula strings (e.g. `"=H28-I28"`) with `valueInputOption: USER_ENTERED`, not
frozen numbers.

```bash
gws sheets spreadsheets values update --params '{"spreadsheetId": "1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE", "range": "'"'"'<TAB>'"'"'!A<ROW>:<LASTCOL><ROW>", "valueInputOption": "USER_ENTERED"}' --json '{"values": [[...]]}'
```

Only fill columns you actually have data for. If a fact reads as ambiguous for
a paid/unpaid field (e.g. "客户已交律师费500，移民局费用630" could mean both
paid, or just state the second amount) — make your best reading, fill it in,
but say the assumption out loud when you report back; never silently guess on
money. Highlighting a cell (e.g. "client name 高光红色") is a background-color
`repeatCell` request, not a value — see the reference file.

## Uploading local files into a case folder

`gws drive +upload` does **not** pass `supportsAllDrives` and 404s on shared-drive
folders. Use the raw API instead:

```bash
gws drive files create --upload "<LOCAL_PATH>" --upload-content-type "<MIME>" --json '{"name": "<NAME>", "parents": ["<FOLDER_ID>"]}' --params '{"supportsAllDrives": true, "fields": "id,name,size"}'
```

## Step 6 — Copy template files into matching new subfolders

For each template subfolder with files (e.g. "回美证所需信息及文件" under
"0. Shared Folder", "Final Checklist" under "4. Final"), copy into the
corresponding new subfolder; leave empty ones empty.

```bash
gws drive files copy --params '{"fileId": "<TEMPLATE_FILE_ID>", "supportsAllDrives": true, "fields": "id,name,parents"}' --json '{"parents": ["<NEW_SUBFOLDER_ID>"]}'
gws drive files update --params '{"fileId": "<NEW_FILE_ID>", "supportsAllDrives": true, "fields": "id,name"}' --json '{"name": "<ORIGINAL_NAME>"}'   # drop the auto "Copy of " prefix
```

### Activity Log template (template root-level doc → case root)

If the template listing from Step 3 returned a file named "Activity Log" (or
similar — mimeType `application/vnd.google-apps.document`), copy it directly
into the **case root** (not a subfolder), remove the "Copy of " prefix, then
fill in the placeholders using `replaceAllText`:

```bash
# 1. Copy to case root
gws drive files copy --params '{"fileId": "<ACTIVITY_LOG_TEMPLATE_ID>", "supportsAllDrives": true, "fields": "id,name,parents"}' --json '{"parents": ["<CASE_ROOT_ID>"]}'
# 2. Rename to remove "Copy of"
gws drive files update --params '{"fileId": "<NEW_DOC_ID>", "supportsAllDrives": true, "fields": "id,name"}' --json '{"name": "Activity Log"}'
# 3. Fill in placeholders
gws docs documents batchUpdate --params '{"documentId": "<NEW_DOC_ID>"}' --json '{
  "requests": [
    {"replaceAllText": {"containsText": {"text": "CLIENT_NAME", "matchCase": true}, "replaceText": "<客户名称>"}},
    {"replaceAllText": {"containsText": {"text": "CASE_TYPE",   "matchCase": true}, "replaceText": "<案件类型>"}},
    {"replaceAllText": {"containsText": {"text": "ROOT_FOLDER_LINK", "matchCase": true}, "replaceText": "https://drive.google.com/drive/folders/<CASE_ROOT_ID>"}}
  ]
}'
```

The template block looks like:
```
LINGTU LAW · 案件初始化
客户名：CLIENT_NAME
案件类型：CASE_TYPE
案件文件夹：ROOT_FOLDER_LINK
```
Replace each placeholder with the real value for this case. Do this **before**
appending the dated entry in Step 9 — the header should be at the top of the
doc, not after the log entries.

## Step 7 — Share "0. Shared Folder" with the client (only if you have their email)

Once it's populated (after Step 6), share the case's "0. Shared Folder"
subfolder with the client so they can see/download what's in it. Default
permission is **Editor** (`writer`) — that's the firm's chosen default here,
not the generally-safer choice, so don't downgrade it to viewer on your own
judgment. Always echo the exact email address back before sharing — a typo
here hands a stranger access to real case files, and that's not something a
later apology fixes:

```bash
gws drive permissions create --params '{"fileId": "<0.SHAREDFOLDER_SUBFOLDER_ID>", "supportsAllDrives": true, "sendNotificationEmail": true, "fields": "id"}' --json '{"role": "writer", "type": "user", "emailAddress": "<CLIENT_EMAIL>"}'
```

No email on hand yet → skip this step entirely (don't guess or fabricate one)
and mention in your Step 9/10 report that sharing is still pending an email
address.

## Step 8 — Multi-applicant cases (only if flagged upfront)

If several people are filed together (e.g. children in one case), the folder
structure stays shared except these four, which get one subfolder per
applicant name inside them: `2. Form`, `1. Initial`, `6. I-797`, `4. Final`.
Everything else (`0. Intake`, `0. Shared Folder`, `3. Draft`, `5. Scanned`,
`7. Deleted`) stays shared. If unsure whether a case is multi-applicant, ask
before building — redoing this later means redoing Steps 3-6.

## Step 9 — Activity Log entry + Tracking Sheet status

**Activity Log** — one running Google Doc in the case root (not "0. Intake").
If the template already had an Activity Log, it was copied in Step 6 — just append.
If not, find or create it first:

```bash
gws drive files list --params '{"q": "'"'"'<CASE_ROOT_ID>'"'"' in parents and name='"'"'Activity Log'"'"' and trashed=false", "fields": "files(id,name)", "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives"}'
# if still none:
gws drive files create --json '{"name": "Activity Log", "mimeType": "application/vnd.google-apps.document", "parents": ["<CASE_ROOT_ID>"]}' --params '{"supportsAllDrives": true, "fields": "id,name,parents"}'
```

Format: `[YYYY-MM-DD HH:MM PT] [OPERATOR] /it — 操作描述`

- **Author**: the actual team member for this session — `joe@lingtulaw.com` is shared by multiple staff. At session start, check context; if unclear ask once "请问今天是哪位同事在操作？" and reuse all session. Never write "Claude" or "AI".
- Timestamp: Pacific Time when the operation completes, precise to the minute.

```bash
gws docs +write --document "<ACTIVITY_LOG_DOC_ID>" --text "\n[YYYY-MM-DD HH:MM PT] [OPERATOR] /it — 案件已建立: [CASE_TYPE] - [CLIENT_NAME] | 根目录: [CASE_ROOT_URL] | 子文件夹: 9个 | 追踪表: To Do List 行已写入 + [CATEGORY_TAB] 行已写入 | Shared Folder: [已分享至 CLIENT_EMAIL / 待分享]\n"
```

**Lingtu Data 工作日志** — 再用 `log_event`（action=note，带 `matter_code` 和案卷链接）记一笔「建了 Drive 案卷」。`link_case_folder` 已经自动记过一笔的话就不用重复。

**Tracking Sheet**（已停用，跳过）— 旧做法是 after the row is created in Step 5, also write column N:

```bash
gws sheets update --spreadsheet-id 1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE \
  --range "To Do List!N3" --values "📁 案件已建立 YYYY-MM-DD"
```

(Use the actual row number from Step 5, not always row 3.)

## Step 10 — Confirm

```bash
gws drive files list --params '{"q": "'"'"'<CASE_ROOT_ID>'"'"' in parents and trashed=false", "fields": "files(id,name)", "orderBy": "name", "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives"}'
```
Report the client code and matter code, the case root link (and that it is linked in Lingtu Data), subfolder list, which got template files, the
multi-applicant split if any, and whether
"0. Shared Folder" was shared with the client (or is still pending an email).

## When to just do it vs. stop and ask

Everything here is routine and reversible — once you have 案件类型 + 客户名称
and know if it's multi-applicant, run Steps 1-10 without pausing for
confirmation each step, **except Step 7**: always echo the client's email
back before granting them Editor access to real case files — that one's worth
a beat, since a wrong address hands a stranger access, not just a wrong cell
value. Otherwise stop and ask only when:
- the case-type text doesn't clearly match exactly one template folder,
- multi-applicant status is unclear and the intake info doesn't say,
- a folder with the exact target name already exists at the destination,
- you can't tell which category tab (beyond "To Do List") a case belongs to.

Financial payment-status assumptions (Step 5) are the one exception to "just
proceed silently" — fill them in, but always state the assumption in your
final report.
