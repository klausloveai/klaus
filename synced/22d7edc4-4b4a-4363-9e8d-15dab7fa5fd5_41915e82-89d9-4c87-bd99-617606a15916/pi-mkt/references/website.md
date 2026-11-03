# Publishing a PI case to lingtulaw.com/success-stories/auto

Modelled on the `mkt2` skill (`~/.claude/skills/mkt2/SKILL.md`): same Lovable project, same table, same "write via SQL, never via the Lovable agent" rule. **Unlike mkt2 there is no Approved gate**: PI cases publish as soon as they are made (Teresa, 2026-09-28). Column G is ignored.

| What | Value |
|---|---|
| Lovable project | `3beabb73-f7ca-4a0c-b860-6d92843f3046`, table `case_studies` |
| Tool | `mcp__lovable__query_database` only (load via ToolSearch). Never `send_message`, which spends credits. |
| List pages | `https://www.lingtulaw.com/success-stories/auto` · `https://www.lingtulaw.com/en/success-stories/auto` |
| Detail pages | `https://www.lingtulaw.com/success-stories/auto/<slug>` · `https://www.lingtulaw.com/en/success-stories/auto/<slug>` |
| DB backup | `backup.case_studies_20260924` |

## How the site renders an auto card (from `src/components/db-content-pages.tsx`)
- Sorted by `published_at` desc, so a fresh insert (default `now()`) lands on top. That satisfies the newest-first rule automatically.
- **Label chip** = `title_zh` text before the first `：`/`:`.
- **Bold headline / subline** = `summary_zh` split on ` · ` (first part bold, rest underneath).
- **案件说明** = `body_md_zh` (markdown). Existing auto rows have no `**分类：**` line, so they all sit in the default group "车祸索赔". **Don't add a 分类 line**, or the new card would start its own group at the top of the page.
- `result` is stored but not displayed. Still fill it, because other code reads it.

## What goes on the site (facts only)
The Canva post's 事故类型 (often chosen from borrowed photos), 受伤详情 and 结案天数 are marketing placeholders. **Don't publish them as case facts.** The card uses only what the check and tracker prove: the amount, the year the check was issued, that it settled, and the tracker's 案件类型. Keep the tone of the existing cards: one or two plain sentences, no insurer name, no client detail.

| Field | Pattern | Example ($50,000, 2026, 车祸) |
|---|---|---|
| `title_zh` | `<标签>：<金额>，<副标题>` | `车祸受伤：5 万美金，保险公司足额赔付` |
| `summary_zh` | `<金额> · <副标题>` | `5 万美金 · 保险公司足额赔付` |
| `body_md_zh` | `<一两句说明>\n\n_<YYYY> · 和解结案_` | `客户驾车途中遭对方车辆撞击受伤，我们整理事故与就医材料向对方保险公司索赔，最终足额和解。\n\n_2026 · 和解结案_` |
| `result` | `<YYYY> · 和解结案` | `2026 · 和解结案` |
| `title_en` | `<Label>: <Amount> <Subtitle>` | `Car Accident Injury: $50,000 Paid in Full by the Insurer` |
| `summary_en` | `<Amount> · <Subtitle>` | `$50,000 · Paid in full by the insurer` |
| `body_md_en` | same sentence(s) in English + `\n\n_<YYYY> · Settled_` | … `_2026 · Settled_` |
| `result_en` | `<YYYY> · Settled` | `2026 · Settled` |
| `type` | `auto` (use `personal-injury` only for non-vehicle cases like 狗咬/滑倒) | |
| `status` | default `'published'` | |

Labels by tracker 案件类型: 车祸 → 车祸受伤 / Car Accident Injury (rotate with 车辆碰撞 / Vehicle Collision, 车辆事故 / Vehicle Accident), 卡车 → 商用货车事故 / Commercial Truck Collision, 网约车 → 网约车事故 / Rideshare Accident, 摩托车 → 摩托车事故 / Motorcycle Accident, 自行车 → 自行车事故 / Bicycle Accident, 行人 → 行人被撞 / Pedestrian Struck.
Vary the subtitle and body sentence between cases (保险公司足额赔付 / 保险公司和解 / 责任明确顺利和解 …) so the page doesn't read as copies.

**Amount format** (match the existing cards):
- ≥ $10,000: amount ÷ 10,000 with trailing zeros dropped + ` 万美金` (50,000 → `5 万美金`, 23,500 → `2.35 万美金`, 75,000 → `7.5 万美金`).
- < $10,000: thousands separator + ` 美金` (7,500 → `7,500 美金`).
- English: `$50,000`, `$7,500`.

## Steps
1. **Duplicate check**: `select slug,title_zh,summary_zh,status from case_studies where type in ('auto','personal-injury') and (summary_zh like '<金额> ·%' or summary_zh like '$<金额> ·%' or summary_en like '$<英文金额> ·%');`. Match the whole amount at the start of the summary. A loose `%5 万美金%` also hits 2.35 万 / 3.5 万 / 85 万. The same amount already live probably means the case went up before the tracker existed. Compare, and if it's the same case, `update` that row instead and keep its slug.
2. **Slug**: `select max((regexp_match(slug,'^auto-(\d+)$'))[1]::int) from case_studies;` → `auto-<max+1>` zero-padded to 3 digits (drafts count too; auto-018 is a draft).
3. **Privacy check** on every zh/en string: no fragment of the client's name, no claim/policy/check numbers, no insurer adjuster names, no phone numbers.
4. **Insert** both languages in one statement with dollar quoting:
   ```sql
   insert into case_studies (slug,type,title_zh,summary_zh,body_md_zh,result,title_en,summary_en,body_md_en,result_en)
   values ('auto-019','auto',$t$…$t$,$s$…$s$,$b$…$b$,$r$…$r$,$te$…$te$,$se$…$se$,$be$…$be$,$re$…$re$)
   returning id, slug, status, published_at;
   ```
5. **Verify in the built-in browser** (the site renders client-side, so curl shows nothing): `navigate` + `get_page_text` on the zh detail page, the en detail page, and the zh list page. Confirm the new card is first and the text is right.
6. **Tracker**: set only that row's 备注 cell (e.g. `PI!I3`, `values update`) by replacing `待发布官网` with `官网已发布 <中文详情URL> · EN <英文详情URL>`, keeping the rest of the note. Read it back. On failure set status back to `'draft'` if the row was inserted, and set 备注 to `… · 待发布官网 · 发布失败：<原因>` so the next run retries it.
7. Never write the Approved (G) / 朋友圈发布 (H) cells, and never read G as a condition.

Take a card down: `update case_studies set status='draft' where slug='<slug>'`. Fix wording: `update … where slug='<slug>'` for both languages.
