---
name: skye-case-drive
description: "Build a new talent-immigration case folder in the 人才移民 Google shared drive for Lingtu Law / SIA 高徒: sort the intake into O-1 / EB1A / NIW, create the case Drive named 客户姓名+案件类型, lay out the standard subfolders (Intake, Shared Folder, Initial, Form, Petition Letter & Exhibits, RFE, Approval Letter, 弃用, plus NVC on EB1A/NIW), copy the PL template in, file the intake materials into 1. Initial renamed, add a blank 材料清单 and the intake note, share only 0. Shared Folder with the client, and log it into 案件总表 法律. Builds one subfolder per statutory criterion (EB1A 10, O-1A 8, O-1B 6, NIW 3 prongs, plus 工会信/offer/PS). Use on any intake hand-off for an O-1 / EB-1A / NIW client — 新客户建文件夹 / O1客户建case drive / 把这个intake建成案子 — and for later materials and criteria folders. For I-131 / I-485 / family-based / H1B use the it skill."
---

# EON Case Drive — 人才移民 case folder setup (O-1 / EB1A / NIW)

Intake hands over a client; this turns that into a working case Drive in a few
minutes with nothing typed twice. Everything happens through the `gws` CLI —
the Drive and Sheets web UI would take dozens of clicks for what the API does
in one call, and clicking leaves no record of what was actually created.

```bash
export PATH="$HOME/.local/bin:$PATH"   # gws lives here; run once per session
```

If a `gws` call 401s or says `invalid_grant`: run `gws auth login -s drive`,
print the URL for the user, and let them approve it in their own browser. Never
handle their Google password or 2FA.

**Every `gws drive files list` call needs `supportsAllDrives`,
`includeItemsFromAllDrives`, and `corpora: allDrives`.** These case files live
in a shared drive, and without those params the API returns an empty list
rather than an error — which reads as "the folder is empty" when it very much
isn't. The bundled script already sets them; if you hand-write a call, don't
forget.

## Known constants

| What | ID |
|---|---|
| 人才移民 shared drive | `0AIXy3tjXMf-MUk9PVA` |
| O-1 client folders | `1-g_HDMHwSi7PtV5Nlyw1nUCwXGbQkwpS` |
| EB1A client folders | `1rDPCJzYAiG13SzJjkrTqc9D7eUxU12xR` |
| NIW client folders | `1D7hKuq2qi4daqIegvjM3YUiN3WKsawjy` |
| O-1 PL template folder | `1KlSs38B0r4XWDSIJRw5m7puEZXttb4Qi` |
| EB1A PL template folder | `1NPZYMtv4fEQm9hNkd1o_ZZ0ndSLaoaYu` |
| NIW PL template folder | `1yTrJRlTCr9bpR_lSFdWqdRjBNVxtpKBi` |
| 案件总表 (tracking sheet) | `1hVkR6sLbQossobqyUA4bJ7Qg3P-mrYF2YupMJvdflEQ`, tab **法律** |

Each PL template folder is the `2. Cover/PL/Index` folder inside that case
type's `0 Sample` folder — that's where the firm keeps the live templates, so
re-reading it each run is what keeps a case current instead of frozen at
whatever the templates looked like when this skill was written.

**Only the PL template is copied automatically.** The `0 Sample` folders also
hold information-collection sheets, blank USCIS forms, signature guides,
checklists and LOI templates — those get picked and adjusted by hand per case,
so pulling them in automatically would just create files someone has to review
and delete. Don't "helpfully" copy them.

## What intake gives you

A name, an email, 申请种类, and an intake note. From that you need four things
before building:

- **Case type → which folder tree.** O-1 (any subtype), EB1A, or NIW.
- **O-1A vs O-1B**, if it's an O-1. Both live under the same `O-1` parent, but
  the subtype goes in the folder name and the tracking sheet: **O-1A** =
  sciences, business, education, athletics; **O-1B** = arts, film, TV. The
  intake note's field almost always settles it (a dancer is O-1B, a
  machine-learning researcher is O-1A) — take your best read and move on. If
  intake genuinely doesn't say, pass plain `O1` and note in your report that
  A/B is unset; the team fixes it by hand once the case starts. Don't stall the
  whole build on a letter that's one rename away.
- **Client's English full name**, as it should appear on the folder.
- **Client email**, for the shared folder. If intake didn't include one, build
  everything else and skip the sharing step rather than blocking — just flag it
  as pending in your report.

A note that mentions two tracks ("NIW 先，O1 后", "EB1A+O1") means two cases.
Ask which one to build now rather than guessing; the firm does file both, but
they're separate folders under separate parents.

Two things you might be tempted to ask about and shouldn't: **whether the case
files a G-28**, and **whether it goes premium processing (I-907)**. Both are
decided in the meeting with the client, and the form-filling workflow carries
its own instructions for them. If the intake note happens to state one, record
it in the intake doc — but never hold up the build waiting for an answer, and
never guess one into the tracking sheet.

## Step 1 — Build the folder tree

```bash
python3 <skill>/scripts/build_case_drive.py \
  --case-type EB1A --client-name "Xuan Shen" \
  --client-email xuan@example.com \
  --intake-note-file /tmp/intake.txt
```

Write the intake note to a file first rather than passing it inline — intake
notes are long, contain newlines and quotes, and shell-escaping them by hand is
how they end up truncated in the doc.

One run does all of this:

1. Checks the case type's parent folder for a same-named case root. **A match
   stops the run** (exit 2) rather than creating a twin — two folders for one
   client is worse than no folder, because they drift apart silently and half
   the team ends up working in the stale one. Report the existing folder and
   ask before re-running with `--force`.

   It also reports `possible_existing_cases` — folders that merely *start* with
   the client's name. Older cases here carry no case type at all (`Qing Yang`,
   `Cheng Chen`) and finished ones pick up suffixes (`Yizhen Zhang EB1A 摄影师`),
   so an exact-name check alone would miss them. This one doesn't stop the
   build — the same client legitimately files more than one case — but **say it
   out loud in your report** so a human can rule out a duplicate.
2. Creates the case root, named `{客户姓名} {案件类型}` — `Xuan Shen EB1A`,
   `Yuxin Tan O1B`, `Tian Ye NIW`. O-1 cases keep the A/B in the name so the
   folder matches the tracking sheet at a glance; `--case-type O1` (no letter)
   gives a plain `... O1` for cases where A/B isn't settled yet. Pass
   `--folder-name` to override entirely (e.g. `Yizhen Zhang EB1A 摄影师`).
3. Creates the standard subfolders:

   | Folder | What lives here |
   |---|---|
   | `0. Intake` | intake team's notes — internal, never shared out |
   | `0. Shared Folder` | **the only folder the client ever sees.** Their own upload space, plus finished work product copied in when it's ready to show them. Starts empty |
   | `1. Initial` | the firm's copy of the record: intake materials (renamed — see Step 1b) and the open-source research built from them |
   | `2. Form` | every USCIS form for the case, flat in one place — I-140 / I-129 / I-907 / G-28 / G-1145, signed and unsigned alike |
   | `3. Petition Letter & Exhibits` | the letter and its exhibits together — PL template lands here, `Exhibit A/B/C...` folders and the Index of Exhibits join it later |
   | `4. Final Scanned` | the final signed/scanned package as filed |
   | `5. RFE` | created empty; the RFE letter, the 解读+策略 doc, and the response go here if one arrives |
   | `6. Approval Letter` | I-797 and approval correspondence |
   | `7. NVC Letter` | NVC-stage correspondence — **EB1A and NIW only** |
   | `8. 弃用` (`7.` on O-1) | superseded drafts and replaced evidence — **moved here, not deleted**, so an earlier version is always recoverable |

   **O-1A and O-1B get no `7. NVC Letter`.** O-1 is a nonimmigrant visa, so the
   case never reaches the National Visa Center — that folder would sit empty
   forever and make people wonder what they forgot to file in it. EB1A and NIW
   are immigrant petitions and do get one. 弃用 takes the next free number
   either way (`7.` on O-1, `8.` on EB1A/NIW) so the sequence has no gap.

4. Copies that case type's petition-letter templates into
   `3. Petition Letter & Exhibits`, reading the template folder live. RFE-specific
   templates are skipped by default — an RFE template in a brand-new case
   folder reads as "this case already got an RFE", which is alarming and wrong.
   Pass `--include-rfe` when the case actually is an RFE response.
5. Builds one subfolder per **statutory criterion** inside
   `3. Petition Letter & Exhibits`, plus that case type's non-criterion pieces
   (工会信, offer, Personal Statement...). See Step 4 for what each type gets
   and why they're not lettered.
6. Creates a **blank** `{客户姓名} 材料清单` doc in the case root. Blank on
   purpose — it gets filled in live during the meeting with the client,
   criterion by criterion, and a pre-filled template is just text someone has
   to clear out first. `--no-checklist` skips it.
7. Writes the client's upload-instructions email into a Google Doc
   `材料上传指引邮件 - {name}` (or `Document Upload Instructions - {name}` in
   English) in the **case root** — 收件人 / 主题 / 正文,
   ready to copy and send. Chinese by default; `--lang en` for
   English-speaking clients (judge from the intake note — if the client
   corresponded in English, use English). `--no-email-doc` skips it.
8. Writes the intake note into a Google Doc `Intake Note - {name}` inside
   `0. Intake`, with the name / case type / email / date header on top.

The script prints JSON with every folder id and link — keep it, the next steps
use `shared_folder_id` and `root_folder_link`.

Adding a note to an **existing** case instead? Don't re-run the builder. Find
the case's `0. Intake`, look for an existing `Intake Note - {name}` doc, and
append a dated block with `gws docs +write` rather than creating a second doc.

## Step 1b — Intake materials into "1. Initial", renamed

Whatever intake hands over — a Drive folder from the intake staffer, files from
a chat thread, screenshots of tax records — goes into **`1. Initial`**, not
`0. Shared Folder`. The shared folder is the client's own upload space; putting
the firm's intake pile in there mixes "what we already have" with "what they
still need to send," and the client can't tell which is which.

```bash
# a whole Drive folder from the intake staffer, structure preserved
python3 <skill>/scripts/import_materials.py --dest <1.INITIAL_ID> --src-folder <SRC_FOLDER_ID>

# individually named files (Drive ids and/or local paths)
python3 <skill>/scripts/import_materials.py --dest <1.INITIAL_ID> --map files.json
```

`files.json` is a list of `{"src": <drive id or local path>, "name": "<新名字>",
"subfolder": "<可选>"}`.

**Rename as you import.** Intake material arrives named `img01507.pdf`,
`扫描全能王 2026-06-01 22.04.pdf`, `WeChatWorkScreenshot_ab79.png` — names that
force whoever picks the case up to open every file to find anything. Give each
one a name that says what it is: who, what document, which year — e.g.
`尤德超 简历 2025-11.pdf`, `2023年个税收入纳税明细.png`,
`北京市科学技术奖 科学技术进步奖二等奖 证书.jpg`. Where the material already sorts
into evidence categories, use `subfolder` — `奖项`, `高薪`, `评审`, `媒体报道`,
`身份材料` — so `1. Initial` doesn't become one flat pile of forty files.

Copies, never moves: the intake staffer's original folder stays untouched, so a
mistake here costs nothing.

Materials that exist only as images in a chat and not as files on disk? Don't
guess which cached screenshot is which — a wrong guess files another client's
document into this case. Transcribe what they say into the intake note (the
numbers are the point, not the pixels) and ask for the files.

## Step 2 — Share "0. Shared Folder" with the client

Only this folder, ever. **A client gets exactly one folder permission for the
whole life of the case** — the shared folder. Sharing the case root would hand
them the draft petition letter, internal research, RFE strategy and intake
notes, which is the failure this whole layout exists to prevent. Check the id
you're about to share is the one the script reported as `shared_folder_id`, not
the root.

The client's side of the work is simple: they upload materials into this
folder. When something the firm wrote is ready for them to see, it gets copied
*into* the shared folder — never by widening their access to anything else.

Echo the exact email address back to the user before running this. A typo here
gives a stranger write access to real case files, and an apology afterwards
doesn't take it back.

```bash
gws drive permissions create \
  --params '{"fileId": "<SHARED_FOLDER_ID>", "supportsAllDrives": true, "sendNotificationEmail": true, "fields": "id"}' \
  --json '{"role": "writer", "type": "user", "emailAddress": "<CLIENT_EMAIL>"}'
```

`writer` is intentional — the client has to upload into it. `sendNotificationEmail`
is **on**: Google's share notice reaching the client first is fine, and it's
also required for clients whose email isn't a Google account (QQ, 163,
Outlook...). With it off, Drive rejects those addresses outright —
`invalidSharingRequest`, "there is no Google account associated with this email
address" — so turning it off to control first contact only works for Gmail
clients and silently breaks for everyone else.

## Step 3 — The client's upload email (already written in Step 1)

Step 1 puts the email in the **case root** as `材料上传指引邮件 - {name}`
(`Document Upload Instructions - {name}` when `--lang en`) — a doc, not a Gmail
draft, because whoever ends up emailing the client isn't necessarily whoever
built the folder. A draft sits in one person's mailbox; a doc in the case folder
is there for whoever picks the case up.

It stays out of `0. Shared Folder` on purpose. That folder is the client's own
upload space, and a staff-facing "copy this and send it" doc doesn't belong
where they're working. Tell the user where the doc is and let them (or intake,
or the assigned attorney) send it.

Rewriting it later — reworded copy, switching to English, or a case whose
folder already exists:

```bash
python3 <skill>/scripts/upload_email.py \
  --folder-id <CASE_ROOT_ID> --client-name "Xuan Shen" --case-type EB1A \
  --shared-folder-link "<SHARED_FOLDER_LINK>" --to <CLIENT_EMAIL> [--lang en]
```

`--print-only` shows the wording without creating anything; `--body-file`
swaps in custom wording. Note this creates a *new* doc each run — delete or
rename the old one so the folder doesn't end up with two versions.

## Step 4 — The criteria folders (Step 1 already made them)

`3. Petition Letter & Exhibits` gets one folder per criterion the regulation
lists — **all of them**, not just the ones this case will claim. Which three-or-
more actually carry the case isn't known at intake; it's settled later against
the background materials. Scaffolding the full statutory list means staff prune
and rename, which is faster and less error-prone than looking the regulation
back up to add one.

| Case type | Folders | Source |
|---|---|---|
| **EB1A** | 10 criteria + `Final Merits 推荐信` + `Personal Statement` | Policy Manual Vol 6 Part F Ch 2 — 8 CFR 204.5(h)(3) |
| **O-1A** | `Waiver 工会信` + `未来计划 Offer` + 8 criteria | Vol 2 Part M Ch 4 — 8 CFR 214.2(o)(3)(iii)(B) |
| **O-1B** | `工会信` + `未来工作 Offer` + 6 criteria | Vol 2 Part M Ch 4 — 8 CFR 214.2(o)(3)(iv)(B) |
| **NIW** | `A. Endeavor` / `B. Prong 1` / `C. Prong 2` / `D. Prong 3` | Matter of Dhanasar |

`criteria_folders.py --case-type EB1A --list` prints any of these without
touching Drive.

**No exhibit letters.** Staff delete the criteria that don't apply, and an
`Exhibit A/B/C` scheme would go out of sequence the moment they did — the
letters get assigned later, when the Index of Exhibits is written and the set
is final. NIW is the exception: its four folders are a fixed set that never
gets pruned, so they carry A–D.

One consequence to know: with no prefix, Drive sorts these folders
alphabetically rather than in statutory order. If someone wants the scaffold to
read in the order of the regulation, `--numbered-criteria` prefixes each
criterion with its number (`1. Awards 奖项` … `10. Commercial Success 商业成就`);
non-criterion folders stay unprefixed and NIW is unaffected. Off by default.

**O-1 without an A/B subtype gets no criteria folders at all** — the two
subtypes share almost nothing, so scaffolding one would build the wrong case.
The build says so in `criteria_folders_skipped`; once the subtype is settled,
fill them in:

```bash
python3 <skill>/scripts/criteria_folders.py \
  --folder-id <PL_AND_EXHIBITS_FOLDER_ID> --case-type O1B
```

Re-running is safe — existing folders come back as `already there`.

The petition letter is written criterion by criterion alongside these folders
and the index, not drafted whole and then chopped up. That's why the letter and
the criteria share one folder.

## Step 5 — Log the case into 案件总表

Add one row at the **top** of the **法律** tab of
`1hVkR6sLbQossobqyUA4bJ7Qg3P-mrYF2YupMJvdflEQ` — insert a blank row 3
(`insertDimension`, `inheritFromBefore: false`), then write into `A3:V3`. The
team reads this tab newest-first, so a new case appended at the bottom is a
case nobody sees. Read `references/tracking-sheet.md` for the full column map,
the dropdown vocabulary, and the exact two calls — it's a 22-column row, and
skipping the insert means overwriting a live client instead of pushing them
down.

The short version: column A client name, B priority (`4` unless told
otherwise), C assignee (blank if unassigned — don't invent one), D case type
(`O1A`/`O1B`/`EB1A`/`NIW`), E status (`To be assigned`, or `In progress` if
someone owns it), F a one-line gist of the intake note, H the case root URL,
P/Q `FALSE`. Leave the per-stage progress columns empty; a new case genuinely
hasn't started any of them.

## Step 6 — Report back

Verify what actually exists before reporting it:

```bash
gws drive files list --params '{"q": "'"'"'<CASE_ROOT_ID>'"'"' in parents and trashed=false", "fields": "files(id,name)", "orderBy": "name", "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives"}'
```

Then give the user, in Chinese: the case root link, the shared folder link, which
PL templates got copied (and any skipped), what went into `1. Initial` and under
what names, the blank 材料清单 link, whether the
intake doc was written, whether sharing succeeded and to which address, the link
to the upload-email doc (and that someone still needs to send it), the
tracking-sheet row that was added, and any `possible_existing_cases` the
duplicate check turned up. If anything was skipped — no email
yet, no PL template in that folder — say so plainly instead of letting it look
complete.

## What happens after this skill

This skill stops at "the folder exists and the client knows where to upload".
**The next step is always `skye-initial`** — say so in the report, and hand it the
case folder link. Everything after that has its own skill; pointing the user at it
beats half-doing it here:

| Next | Skill |
|---|---|
| 材料归档、写第一份材料清单、判断材料能不能用、给客户的话术 | **`skye-initial`** ← 建完就走这个 |
| 填 `2. Form` 里的 USCIS / DOL 表格（I-129 / I-140 / ETA-9089 / G-28 / I-907 / G-1650） | `skye-forms` |
| `3. Petition Letter & Exhibits` 里的申请信、逐条 criterion 论证、Index of Exhibits | `skye-petition` |
| 中文证据翻译、翻译认证、标注申请信依据 | `skye-translate` |
| 定稿后合并拆分成电子提交那一套 | `skye-submission` |
| 收到 RFE / NOID | `skye-readrfe` → `skye-rfe` |

Don't improvise form-filling, drafting or splitting inside this skill.

## When to just do it vs. stop and ask

Once you have case type, subtype (for O-1), name, and email, run Steps 1–3 and 5–6
straight through. This is routine, reversible work and pausing at each step
wastes the user's time. Two exceptions worth a beat:

- **Before sharing (Step 2)** — echo the email address back.
- **A duplicate folder already exists** — the script stops on its own; surface
  the existing folder and let the user decide.

Otherwise stop and ask only when the intake mentions two tracks ("EB1A+O1",
"NIW 先，O1 后") and you can't tell which to build now — those are two separate
cases under two separate parents. An unclear O-1 A/B is *not* a reason to
stop: build with plain `O1` and flag it, since renaming is a two-second fix and
a blocked build isn't.
