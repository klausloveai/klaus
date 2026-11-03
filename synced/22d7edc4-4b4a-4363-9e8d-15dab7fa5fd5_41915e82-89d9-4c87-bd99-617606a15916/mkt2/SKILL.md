---
name: mkt2
description: Publish Lingtu Law / SIA 高徒 success cases to lingtulaw.com (Chinese, then the English version) once their row in 成功案例交接表 has the Approved box ticked. Phase 2 of the mkt pipeline, which `mkt` hands off to. Use when the scheduled task `mkt-approved-check` fires, or when the user says "/mkt2", "检查Approved", "把Approved的案例发官网", "发布成功案例到官网", "同步英文版". Writes straight to the Lovable database (no credits). Never ticks tracker checkboxes and never publishes a row whose Approved box is unticked.
---

# mkt2 — Publish approved success cases (Lingtu Law / SIA 高徒)

Phase 2 of the success-case pipeline. `mkt` writes the doc, files the folder
and adds a tracker row with 备注 `文案已定稿 · 等待Approved后发布官网`, then
stops. A lawyer at the firm reviews the doc and ticks **Approved**. This
skill picks those rows up, publishes the Chinese page, then the English page,
and records both URLs in the tracker.

**A ticked Approved box is the lawyer's sign-off** (Teresa, 2026-09-28).
Don't ask anyone to confirm again before publishing, and don't wait for a
reply in chat. Once the privacy check passes, write to the site, verify
both pages, and then update column I (备注) of that row. Every row that
went live must end with its 备注 changed to the published text in Step 4;
a published row whose 备注 still says 等待Approved would be published a
second time on the next run.

```bash
export PATH="$HOME/.local/bin:$PATH"   # gws lives here
```
Every gws drive call needs `"supportsAllDrives": true`.

## Known constants

| What | Value |
|---|---|
| Tracker spreadsheet | `1JebB6SkokvxnaMh83WiOgr53PoRj9XDAu3KKWwJ1mZ8` ("成功案例交接表") |
| Tabs to scan | `Sia`, `Skye`, `商业诉讼` (商业诉讼 got its Approved column on 2026-10-14) |
| Sia / Skye / 商业诉讼 header (2026-10-14) | A 序号 \| B 案件类型/案件名称 \| C 客户（真名） \| D 案件文件夹链接 \| E 完成日期 \| F Approved ☐ \| G Marketing图片完成 ☐ \| H 朋友圈发布 ☐ \| I 备注 |
| Column rule | Always read row 1 and map columns **by header name**, because they have moved before. ☐ cells take only `true`/`false`, never text. |
| Lovable project | `3beabb73-f7ca-4a0c-b860-6d92843f3046`, table `case_studies` |
| Site URLs | `https://www.lingtulaw.com/success-stories/<type>/<slug>` and `https://www.lingtulaw.com/en/success-stories/<type>/<slug>` |
| DB backup | `backup.case_studies_20260924` (taken before the translation work) |

**Write to the site only with `mcp__lovable__query_database`** (load it via
ToolSearch). Never use `send_message` or the Lovable agent: that spends
workspace credits and a direct SQL write doesn't (Teresa, 2026-09-24).

## Step 0 — Pick the rows

0. **Only one run writes at a time.** When this skill runs by hand (not from
   the scheduled task), first call `mcp__scheduled-tasks__list_task_runs`
   for `mkt-approved-check`. If a run has status `running`, don't write
   anything: tell the user it's running and review its results after it
   finishes. On 2026-09-28 a manual run and the 10:00 scheduled run picked
   the same rows at the same time. Only the slug unique index stopped a
   duplicate batch.
1. Read `Sia!A:I`, `Skye!A:I` and `商业诉讼!A:I`, and map each tab's columns
   by its own header row.
2. Skip rows with an empty 案件类型 cell and rows where Approved isn't TRUE.
   Of the rest, pick:
   - **A. Marked rows:** 备注 contains **等待Approved**. Always picked.
   - **B. Unmarked rows:** 备注 does *not* contain **官网已发布**. These are
     older rows made before the Approved gate existed (e.g. Skye rows 2, 3
     and 5 on 2026-09-28, which were approved but had never gone up). Before
     picking one, check whether it's already on the site: search `title_zh` /
     `body_md_zh` for the case's key terms (visa type, consulate, the
     distinctive difficulty). If a matching published row exists, don't
     republish it. Just write its URLs into 备注 (Step 4 success format) so
     it isn't checked again. Pick it only if nothing matches.
   Rows whose 备注 already says 官网已发布 are done and never touched.
3. No rows? Stop quietly and just say "no approved cases pending".
4. If the user named a specific case (e.g. "/mkt2 Jiaxin Zhang"), only handle
   that row, and still only if its Approved box is ticked. If it isn't, say
   so and stop. Don't tick the box for them.

For each picked row, run Steps 1-4.

## Step 1 — Read the doc

List the row's folder (from 案件文件夹链接) and read the Google Doc in it with
`gws docs documents get`. The doc is the source of truth, because the reviewer
may have edited it before ticking Approved. No doc in the folder, or more
than one candidate? Mark the row as failed (Step 4) and move on.

- **The link cell sometimes holds a folder name, not a URL** (Sia row 4 had
  `OPT NOID+Shuo Chen`). Search Drive for a folder with exactly that name
  (`name = '…' and mimeType = 'application/vnd.google-apps.folder'`,
  `corpora: allDrives`). Use it only if exactly one folder matches.
- Plain text is easiest to work with:
  `gws drive files export --params '{"fileId":"<id>","mimeType":"text/plain"}' -o <name>.txt`.
  The `-o` path must be relative to the current directory, so `cd` into the
  output folder first. An absolute path silently writes nothing.

## Step 2 — Publish the Chinese page

1. **Privacy check on the doc body (required before any insert).** Search for
   every fragment of the client's real name (English given name and surname,
   plus any Chinese name) and for SSN / A-number / receipt-number
   (`[A-Z]{3}\d{10}`) / phone patterns. If anything matches, **don't publish and don't edit the doc**. The
   reviewer approved the doc as it stands, so mark the row as failed (Step 4)
   with the matched fragment's type (not its value), and let a person fix it.
   客户（真名） can hold several parties separated by `、`, including
   companies (商业诉讼 row 5: `Nova Space Inc.、Sha Wang`). Check every
   party, and for a company check its distinctive word(s) too (`Nova Space`,
   `CB Kitchen`), not only the full legal name.
2. **Pick `type`.** Every row from the `商业诉讼` tab is `litigation`, no
   matter what the case is about (Teresa, 2026-10-14). For Sia / Skye rows: It must be one of the types the site knows: eb1a, niw,
   o1, h1b, l1 (also EB-1C), eb5, family (婚姻绿卡/亲属/入籍), status-change
   (F-1/B-2 转身份/E-2/身份恢复), personal-injury, auto (车祸),
   litigation, **consular** (领馆面签，非移民和移民都放这里；用 `大类` 区分：
   `NIC 非移民签证面签` 放 H-1B/L-1/O-1 等，`NVC 移民签证面签` 放 EB-1A 等),
   **rfe-noid** (RFE/NOID 逆转，OPT 执法记录类也归这里).
   Interview cases that were overseas consular visas go to `consular`, not
   status-change. The site's consular page already shows both NIC and NVC. Go by what the case *ended with*, not by where its Drive
   folder came from. Example: an O-1 holder who got an F-1 visa goes under
   status-change. A new type needs a code change in Lovable first.
3. **Pick the group (分类).** Reuse an existing group name exactly instead of
   inventing a near-duplicate. Litigation groups as of 2026-10-14 (zh / en):
   雇佣纠纷 / Employment Disputes, 合同纠纷 / Contract Disputes,
   租务纠纷 / Landlord–Tenant, 股权纠纷 / Shareholder Disputes,
   欠款追收 / Debt Collection, 场所责任 / Premises Liability,
   产权纠纷 / Property Disputes. If a litigation case fits none of them, don't
   invent one in an unattended run: mark the row failed with
   `分类待定` and let Teresa pick the group. Re-run the query to see the
   current list:
   ```sql
   select type, substring(body_md_zh from '\*\*分类：\*\*\s*([^\n]+)') grp, count(*)
   from case_studies group by 1,2 order by 1,3 desc;
   ```
   Also get the English group name that rows in that group already use
   (`**Category:** …` in body_md_en). The /en list page groups cards by that
   exact string, so it has to match.
4. **Check for duplicates and get the slug.** Search `title_zh` /
   `body_md_zh` for the case's key terms. If the case is already on the site
   (some went up before the Approved gate existed), `update` that row from
   the doc instead of inserting a second one, and keep its slug. Otherwise
   slug = `<type>-<max existing number + 1>`. Take the max numerically, only
   over slugs shaped `<type>-<digits>` (`legacy-o1-…` doesn't count), and
   right before the insert, not at the start of the run. If the insert
   fails with a duplicate slug, **don't just bump the number.** Re-query the
   rows created in the last hour: a duplicate slug usually means another run
   is publishing the same cases.
5. **Insert** with dollar-quoted strings (`$b$…$b$`) so Chinese quotes and
   newlines need no escaping. Columns:
   - **Internal notes never go on the site.** Leave out any 【营销重点】 /
     营销说明 / 截图素材 / 私信话术 block, and anything addressed to the
     firm rather than the reader (Skye rows 2 and 3 have one).
   - **Relative dates** like 本周四 or 今天 read wrong on a web page. Use the
     real date if the doc or the tracker's 完成日期 pins it down. If not,
     use a neutral label (面试当天), and mention the change in the summary.
   - **Non-standard headings:** map 这个案例有什么不一样 → 难点 and
     我们做了什么 → 策略. An extra section such as 顺带科普 goes at the end
     of 结语 as a bold lead-in line plus its paragraphs, so the house
     section order stays the same.
   - `title_zh`: the doc's headline (its first line). If the body starts
     straight at 客户背景 with no headline, use the Doc's file name with
     the leading ✔ and any trailing `+X女士/+客户名` removed. `summary_zh`: a short card line such as
     "当天通过 · 已获批I-140仍拿下F-1". `result_zh` is not a column; use
     `result`, which holds the outcome sentence.
   - `body_md_zh` in house format: `**分类：**<组名>`, then `### 背景`,
     `### 难点`, `### 策略`, `### 案件时间线`, `### 结语`, `### 结果`.
     ①②③ and numbered items become `- ` bullets. The timeline is a table:
     `| 时间 | 进展 |` / `| --- | --- |` / one row per event.
   - Leave the `_en` columns empty in this insert; Step 3 below fills them.
   - Leave `timeline` (jsonb) null because no rows use it. `status` defaults to
     `'published'`. Approved already happened, so publish directly.
   - List pages sort each type by `published_at desc`, and the h1b /
     family / status-change rows carry the real case date there (back to
     2023). Set `published_at` to the date of the case's last timeline event
     (e.g. `'2026-08-05'`), not `now()`, so the newest case sorts first.
     If the doc only gives month/day, take the year from the tracker's
     完成日期.
   - End the statement with `returning id, slug, status` to confirm.
6. **Verify in the browser, not with curl.** The site renders on the client,
   so the HTML has no case text even for pages that are live. Open the URL
   with the built-in browser (`navigate` + `get_page_text`) and confirm the
   title, the sections and the timeline table.

### Adapted cases (改编案例)

A row whose 备注 contains **改编案例** is a case rewritten from a real matter
with changed details and an assumed outcome (商业诉讼 rows 2–7 on
2026-10-14). Publish it exactly like any other case: no disclaimer line in
the body, no prefix on the summary. The litigation list page carries one
page-wide note that some cases are adapted (Teresa, 2026-10-14), so nothing
per case is needed.

## Step 3 — Sync the English version

Once the Chinese page checks out, translate the case and write it into the
same row: `update case_studies set title_en=…, summary_en=…, body_md_en=…,
result_en=… where slug='<slug>'`.

- `body_md_en` starts with `**Category:** <English group>`. Copy that string
  exactly from an existing row in the same group, because the /en list page
  groups cards by it. Then use
  `### Background / Challenges / Strategy / Case Timeline / Closing Note / Outcome`,
  with the timeline as `| Date | Milestone |`.
- Keep the anonymized form ("Ms. Z", "Mr. C"), translate "BH" as
  "asylum (BH)", and run the same real-name / number-pattern check on the
  English text.
- Verify `https://www.lingtulaw.com/en/success-stories/<type>/<slug>` in the
  browser the same way.

## Step 4 — Update the tracker and report

- Success: right after both pages verify, set only that row's 备注 cell
  (column I today, but use the column the header map found; explicit
  single-cell range such as `Sia!I16`, `values update`) to
  `文案已定稿 · 官网已发布 <中文URL> · EN <英文URL>` (adapted cases too; the
  改编案例 prefix doesn't need to stay). Read the cell back to
  confirm the write landed. This step is not optional: a published case is
  not done until its 备注 is updated.
- Failure at any point (the privacy check hits, no doc, an unclear type, a DB
  error, a page that doesn't render): don't publish, or if the Chinese row is
  already in, set it back to `status='draft'`. Set 备注 to
  `等待Approved · 发布失败：<简短原因>` so the next scheduled run retries it and
  the reason is visible.
- Never touch the Approved / Marketing图片完成 / 朋友圈发布 checkboxes.
- End with a short Chinese summary: which cases went live (both URLs) and
  which failed and why.

Wording fixes after publishing: update the Doc first, then
`update case_studies set … where slug='<slug>'` for both languages. To take a
case down: `update case_studies set status='draft' where slug='<slug>'`.

## Scheduled task `mkt-approved-check`

This skill normally runs from the standing scheduled task
`mkt-approved-check`. Its schedule is whatever is set on the task; on
2026-09-25 Teresa changed it to daily at 10:00 (`0 10 * * *`, local time), so
keep that unless she asks otherwise. It runs only while the Claude app is open
and catches up on the next launch. If the task is
missing, recreate it with `mcp__scheduled-tasks__create_scheduled_task`
(taskId `mkt-approved-check`, notifyOnCompletion false) and a prompt that
tells the run to follow this file:
`~/.claude/skills/mkt2/SKILL.md`.
