---
name: mkt
description: Turn a real client's case folder in Google Drive into an anonymized marketing success-story doc for Lingtu Law / SIA 高徒's "成功案例" (Success Cases) library. Use whenever the user says things like "学我的成功案例", "把这个案子做成案例分享", "写一个成功案例放到成功案例文件夹", or points at a client's case folder and a success-case library folder and asks to turn one into the other. Also covers touching up an already-generated case-study doc (e.g. "职业写得太精准了，模糊一下"). Triggers on requests to extract/summarize/anonymize a client case into shareable marketing copy — not on requests to just read or organize case files (that's the `it` skill), and not on drafting official USCIS filing content (that's the `case` skill).
---

# mkt — Success-Case Marketing Doc Generator (Lingtu Law / SIA 高徒)

Takes one real client's working case folder (full of PII — approval notices,
SSNs, USCIS account passwords, home addresses) and produces a short, punchy
Chinese case-study write-up safe to share on WeChat/social, filed into the
firm's "成功案例" library and handed to the tracker for review. This skill
stops there. Publishing to lingtulaw.com is the separate **`mkt2`** skill,
which runs once the tracker row's Approved box is ticked. The only required
input is the source case folder, or just a client name to search Drive for.
The destination is the matching category folder inside 成功案例 (see Step 4). Everything else is inferred from
the case content or confirmed with the user along the way.

```bash
export PATH="$HOME/.local/bin:$PATH"   # gws lives here; run once per session
```

**Every `gws drive files create/update` call on this firm's Drive must
include `supportsAllDrives: true`** in `--params` — the library and case
folders live in a Shared Drive, and omitting this makes Drive return a plain
404 "file not found" instead of a helpful error.

## Known constants (don't re-discover these)

| What | Value |
|---|---|
| "成功案例" library root | `1qMHVfmX0eFNfuTpZhe5ObMdOyPl7YPj6` |
| Marketing handoff tracker spreadsheet | `1JebB6SkokvxnaMh83WiOgr53PoRj9XDAu3KKWwJ1mZ8` ("成功案例交接表", lives in the library root) |
| — tabs | `Sia` (sheetId `0`), `Skye` (sheetId `153994123`), `商业诉讼` (sheetId `1972172249`) |
| — header row, `Sia` / `Skye` / `商业诉讼` (商业诉讼 matched the others on 2026-10-14) | A 序号 \| B 案件类型/案件名称 \| C 客户（真名） \| D 案件文件夹链接 \| E 完成日期 \| F **Approved** ☐ \| G Marketing图片完成 ☐ \| H 朋友圈发布 ☐ \| I 备注 |
| — rule | Columns have moved before. **Always read row 1 first and map columns by header name**, never by fixed letter. ☐ = checkbox cell: write only `true`/`false` there, never text. |

If the destination folder the user points at is this same library, skip
straight to using these IDs instead of searching for them again.

## Step 1 — Read the case

List and read what's in the source folder to learn the case, rather than
asking the user to re-type facts that are already sitting in the approval
notices and intake forms:

```bash
gws drive files list --params '{"q": "'"'"'<SOURCE_FOLDER_ID>'"'"' in parents and trashed=false", "fields": "files(id,name,mimeType)", "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives"}'
```

Read the approval/receipt notices and any intake docs to extract:
- **Case type / transition** — e.g. "L-1A转F1", "STEM OPT申请", "H-1B Transfer". If the case bundles several people (e.g. a principal applicant plus F2/H4 dependents), note that — it's often the most interesting part of the story.
- **Core difficulty** — whatever made this case non-routine: a tight deadline, a status gap, an unusual employer/occupation combination, a prior RFE, an out-of-status period, etc. This is what makes the case worth writing up; a case with no real difficulty barely makes a story.
- **What the firm actually did** — the concrete actions taken (材料梳理, 加急审理, 补充说明信, 论证雇佣关系, etc.), not generic filler.
- **Timeline** — received date, key milestones (RFE,加急启动), approval/notice date.

If any of these four are genuinely unclear from the source files, ask the
user rather than inventing a difficulty or strategy that didn't happen —
fabricated specifics are the one thing that would make this backfire if a
client ever recognized their own (mis-told) story.

## Step 2 — Draft the write-up

Match the house style already established in the firm's own social posts
(a STEM OPT case poster and a "H1B Approval Notice" collection of case
blurbs were the references this skill was built from) — short sections,
punchy hook, no filler:

```
<一句话吸睛标题，带感叹号或强对比，如"L-1A转F1，全家三口零RFE一次性获批！">

客户背景：
<一到两句，身份/背景，见下方匿名与模糊规则>

核心难点：
<编号列出，一条一句>

我们的策略：
①②③ <编号列出，每条对应一个难点>

案件时间线：
<日期  节点>（2-4行即可，不用逐日流水账）

结语：
<一到两句总结，呼应难点与结果>
```

### Anonymize the client

Body text never carries the client's real name — use surname-initial +
honorific instead (e.g. "F女士", "C同学", "Z先生"), matching every existing
entry in the firm's library. The real name is still useful, just not here —
see Step 4 for where it belongs instead.

### Blur anything that narrows down to one person

A job title alone is usually fine ("IT项目经理"); a job title *plus* a
specific employer or narrow industry is what makes someone identifiable
("在一家精密零件制造公司担任IT Project Manager" — a search away from a real
LinkedIn profile). Default to keeping only the immigration-relevant fact and
dropping the rest: prefer "F女士原持L-1A工作签证在美从事全职工作" over naming
the industry or role. If the case's whole hook *is* an unusual job/industry
combination (e.g. "跨行业H-1B" cases in the reference library, where the
mismatch between background and employer is the story), keep the category
level detail ("金融背景" + "非传统咨询公司") but still drop the specific
employer name and exact title. When in doubt, blur more rather than less —
it's easy for the user to ask for a specific detail back in, harder to
un-leak one.

Never include SSN, USCIS account passwords, passport/A-numbers, exact home
addresses, or phone numbers in the doc — these routinely appear in the
source intake forms and must not make it into the draft at all, not even
partially redacted.

## Step 3 — Create the doc

```bash
gws docs documents create --json '{"title": "<hook headline>"}'
```
Then write the body with a `batchUpdate` `insertText` request (or
`gws docs +write` if only appending). If you need to fix a specific phrase
after the fact — e.g. the user says a detail is still too identifying —
use `replaceAllText`, not delete-and-recreate:

```bash
gws docs documents batchUpdate --params '{"documentId": "<DOC_ID>"}' --json '{
  "requests": [
    {"replaceAllText": {"containsText": {"text": "<exact old phrase>", "matchCase": true}, "replaceText": "<new vaguer phrase>"}}
  ]
}'
```
(There is no direct "edit content" call on the Drive MCP connector if you're
using it instead of `gws` for this — only `create_file`, which makes a new
file, and `copy_file`. `gws docs documents batchUpdate` is the reliable way
to edit an existing doc in place.)

## Step 4 — File it in the library

File the case folder **inside the matching category folder** of the
"成功案例" library. Teresa reversed the flat-folder rule on 2026-09-25:
"文件夹还是分类到相关内容下面吧". Never create case folders in the library
root. Category folders (IDs as of 2026-09-25; list 移民 again if one is missing):

| Case | Parent folder | ID |
|---|---|---|
| **Any visa interview at a consulate outside the US** (immigrant or nonimmigrant: EB-1A/E11, F-1, O-1, H-1B, family-based, 221(g) stuck at a consulate…) | 移民 / 领馆面签 | `1Q0otWkrwpvREgYQaa3D7DUUGrztZ5fc5` |
| E-2 | 移民 / E2 | `1jix9Q6YvwLEttBlhjZ4pJwzykEjow4bY` |
| EB-1A petition (I-140, no interview) | 移民 / EB1A | `1Ndfbrz1MAufs72HtA7rYEmBmc-eNnX_y` |
| H-1B (petition, amendment, transfer) | 移民 / H1B | `1gStdebnPUauvuhiFpIDGXQdCbqDK9lEX` |
| L-1A/L-1B/L-2, EB-1C | 移民 / L1/EB1C | `1Iji-9JJQ7o6SANjECB6XSZYGXBbBp2My` |
| NIW | 移民 / NIW | `1RYrfoAun_q_Z9Fk0Hh2p4qmBCJoYptKr` |
| O-1 petition (no interview) | 移民 / O1 | `1Blyx7cQ-JkWcPDbqabOaCsK5sPSgVa8D` |
| RFE / NOID reversals | 移民 / RFE/NOID | `1x904vtw3ibxmpFttfaaZkAosGb5VK7T_` |
| SIJS | 移民 / SIJS | `16oJnI14EdBOW7YptOc03IE0C8YG6woKK` |
| Family-based (I-130, I-485 marriage/parents, naturalization) | 移民 / 亲属移民 | `1nNJAuaPmv_2MpnUFqp8SlsvXwSeQcs8K` |
| Change / extension / reinstatement of status inside the US (F-1, B-2, OPT, H-4…) | 移民 / 非移民身份转换 | `1Q29yevRJnr8UjvNyHCxkbs0kikCJC2_b` |
| Personal injury / 车祸 | 人伤 | `1M1yRLjQyfHUnYlCOOCAD1kOzERJ9l9-W` |
| Business / civil litigation (contract, debt collection, fraud, employment defense, small claims, vacating a default judgment…) | 商业诉讼 (library root, added 2026-10-14) | `1PlCmEHBGGUjBWFnhc4YLq6rErR5LHyXP` |

A 商业诉讼 case goes in the `商业诉讼` tracker tab in Step 5, and `mkt2`
publishes it under website type `litigation`.

The **领馆面签 rule wins**: if the case story is a consular interview outside
the US, it goes there whatever the visa type. Otherwise pick by the case's
main outcome. If two categories fit equally (e.g. RFE on an H-1B), or none
fits, ask the user rather than creating a new category folder.
Don't touch the loose files already sitting in 移民 (已打码_… etc.).

This Drive folder choice is separate from the website `type` that `mkt2` picks. A
consular F-1 case lives in 领馆面签 on Drive but can still be `status-change`
on the site.

Name the folder
`<案件类型/hook>+<客户真名>` — note this is the **real** name, unlike the
doc's body text. The folder name is for the firm's own internal
findability; the anonymization from Step 2 only applies to content someone
outside the firm might read.

```bash
gws drive files create --params '{"supportsAllDrives": true}' --json '{"name": "<CASE TYPE>+<REAL NAME>", "mimeType": "application/vnd.google-apps.folder", "parents": ["<CATEGORY_FOLDER_ID>"]}'
```

Move the doc into it (Drive files don't have a single "move" call — it's an
add/remove on parents):

```bash
gws drive files update --params '{"fileId": "<DOC_ID>", "addParents": "<NEW_SUBFOLDER_ID>", "removeParents": "<DOC_CURRENT_PARENT_ID>", "supportsAllDrives": true}' --json '{}'
```

## Step 5 — Tracker row, then wait for Approved

This is the execution team's handoff signal to marketing: every case this
skill produces gets a row here, every time. **This is where `mkt` ends.**
The website step is `mkt2`, and it only runs once the row's Approved box is
ticked.

1. Ask which tab (`Sia` / `Skye` / `商业诉讼`) the case belongs to if it isn't
   obvious from context already established this session. These are fixed
   team/category buckets, so don't guess between them.
2. Read row 1 of that tab and map the columns by header (see Known constants).
   Then read the tab and find the last row with a 序号.
3. Write the row **by explicit range** (`<TAB>!A<n>:I<n>`) with `values update`.
   Don't use `append`: the tabs have pre-filled blank checkbox rows, and
   append lands below them. Fill in:
   - 序号 (last + 1), 案件类型/案件名称 (same headline as the folder),
     客户（真名）, 案件文件夹链接 (the Step 4 folder URL), 完成日期 (today)
   - **Approved = `false`**. Someone at the firm ticks it after reviewing the
     doc; this skill never does.
   - Marketing图片完成 = `false`, 朋友圈发布 = `false`. These are marketing's
     boxes, not this skill's.
   - 备注 = `文案已定稿 · 等待Approved后发布官网`. `mkt2` looks for exactly
     the words **等待Approved**, so keep them.
   ```bash
   gws sheets spreadsheets values update --params '{"spreadsheetId": "1JebB6SkokvxnaMh83WiOgr53PoRj9XDAu3KKWwJ1mZ8", "range": "<TAB>!A<n>:I<n>", "valueInputOption": "USER_ENTERED"}' --json '{"values": [["<N>", "<案件类型/案件名称>", "<客户真名>", "<文件夹链接>", "<YYYY-MM-DD>", false, false, false, "文案已定稿 · 等待Approved后发布官网"]]}'
   ```
4. Read the row back. Checkbox columns must hold `TRUE`/`FALSE`, and 备注 must
   be the note text.
5. **Report to the user now, and stop here:** doc link, folder link, tab +
   row number, one line on what was blurred or omitted for privacy, and a
   note that the website goes up automatically once Approved is ticked.
6. **Make sure the scheduled Approved check exists.** It's one standing
   scheduled task, `mkt-approved-check`, that runs `mkt2` on a schedule
   (daily at 10:00 since 2026-09-25) across all rows, so there's no per-case task to create. Look for it with
   `mcp__scheduled-tasks__list_scheduled_tasks`. If it's missing, tell the
   user, and offer to recreate it using the setup in the `mkt2` skill.

The 商业诉讼 tab has the same Approved gate as Sia / Skye since 2026-10-14,
so its rows get the same values. For an adapted case (details rewritten,
outcome assumed), start 备注 with `改编案例（细节已改写，结果为假设）· ` so
`mkt2` adds the adapted-case disclaimer on the site.

If a case gets revised later, update that row's 备注 in place rather than
adding a duplicate row.

## When to just do it vs. stop and ask

The first time this runs for an unfamiliar case, pause once before writing
anything to confirm two things the user may have a house style for beyond
what's above:
- whether they want the synthesized write-up (default, and the whole point
  of this skill) or literally think they want raw files copied — if they
  ask for the latter, flag that raw source files carry SSN/passwords/exact
  addresses and shouldn't go into a sharing-facing library as-is,
- the anonymization form for the client name in the body text (default:
  surname-initial + honorific, as above).

Once those are settled for a session, later cases in the same session don't
need to re-ask — proceed straight through Steps 1-5. Still stop and ask
(don't guess) if:
- the case's core difficulty or strategy genuinely isn't recoverable from
  the source folder's contents,
- blurring a detail would strip the case of the thing that makes it a story
  worth telling (e.g. an "unusual industry" case with the industry blurred
  away) — surface the tension to the user instead of silently picking a
  side,
- a folder with the same target name already exists in the destination
  library (possible duplicate write-up).

## Report back

After Step 5, give the user the doc link, the case-folder link, the tracker
tab + row number, one line on what got blurred or omitted for privacy, and a
note that the website goes up via `mkt2` once someone ticks Approved (checked
daily at 10:00 by the scheduled task, or right away with `/mkt2`). Then stop. Don't publish anything to the website from this skill.
