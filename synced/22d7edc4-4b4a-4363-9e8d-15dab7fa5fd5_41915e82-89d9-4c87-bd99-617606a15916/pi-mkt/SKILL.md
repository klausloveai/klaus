---
name: pi-mkt
description: Build Lingtu Law's 人伤 "猜猜赔多少系列" (guess-the-settlement) social posts in Canva from a client's folder in the Drive 人伤 folder. Reads and redacts (打码) the insurer's settlement check, adds accident photos, auto-picks 事故类型 / 受伤详情 / 结案天数, fills a copy of Canva template DAHG9rQstfw (cover + matching insurer reveal page), saves it, and logs the case in the PI tab of 成功案例交接表 for Teresa to review at the end. Then publishes the case to lingtulaw.com/success-stories/auto (zh + en) via the Lovable database; PI cases need no Approved tick. The daily scheduled task mkt-approved-check also runs the publish step for any PI row still marked 待发布官网. Use whenever the user says "/pi-mkt", "猜猜赔多少", "猜猜看", "做赔偿帖", "做个人伤案例图", "把XX的支票做成猜猜赔多少", "/pi-mkt 发布", "把车祸案例发官网", "人伤案例上网站", names a client folder from 人伤 and wants a Canva post, or asks to do the next / all un-done 人伤 cases, even without the word "skill". Not for immigration success stories (mkt / mkt2).
---

# pi-mkt — 猜猜赔多少系列 Canva posts

Each post is a 2-page Canva design: a **cover** (accident photos, a check with the amount hidden, "左滑解锁赔偿金额", 事故类型, 受伤详情) and a **reveal** page (the same check with the amount under a magnifier, the insurer's logo on an envelope, "N天高效结案").

Teresa wants to step in as little as possible and check everything at the end. Run the whole pipeline without questions, commit the Canva edits, and hand her one report with previews and links. Ask only if something makes the post impossible (no check in the folder, an unreadable check). Everything else has a default below.

## Constants
- Drive 人伤 folder: `1M1yRLjQyfHUnYlCOOCAD1kOzERJ9l9-W`. One subfolder per client, named `Name-M-D-YY` (the loss date). `✅` prefix = post done, `❌` = don't make one, no prefix = candidate.
- Canva template: `DAHG9rQstfw`. Page map, element roles and gotchas are in `references/template.md`. Read it before touching Canva.
- Helpers in `scripts/`: `setup_env.sh` (prints a python with PyMuPDF+Pillow), `redact.py` (render / check / photo), `canva_upload.sh`.
- Work in the session scratchpad directory, one subfolder per client.
- `used_photos.json` in this skill folder logs which Drive photos have already appeared in a post.
- Tracker: 成功案例交接表 `1JebB6SkokvxnaMh83WiOgr53PoRj9XDAu3KKWwJ1mZ8`, tab PI, written with `scripts/pi_tracker.py` (needs the `gws` CLI at `~/.local/bin/gws`, already authenticated on Teresa's Mac).

## Workflow (per case)

### 1. Pick the case
- User named a client → find that subfolder (`search_files` with `parentId = '<人伤 id>'`, match on name).
- "next" / "做一个" / no name → list the unmarked subfolders, newest `createdTime` first, and skip any that already have a row in the PI tracker tab or a Canva design (`search-designs` query = client name; titles look like `Name-M:D:YYYY`). Take the newest one. "全部" / "all" → do them all in that order, one after another.
- Skip `❌` folders unless the user explicitly names one.

### 2. Read the check
- List the folder. The check is usually a PDF named after the client. Download it (`download_file_content`; the output is big, so it gets saved to a file: `jq -r .content <file> | base64 -d > check.pdf`).
- `PY=$(scripts/setup_env.sh)`; `$PY scripts/redact.py render check.pdf page.png`, then look at it.
- Record: payer insurer, amount, **issue date** (the date on the check), payee line.
- Several checks in the folder (BI + UIM, several payees…) → put the **largest** one on the post.
- No check or unreadable → skip this case, note it in the final report, and move on to the next case if there is one.
- **The damage has to match the amount** (Teresa, 2026-10-08). Readers guess the payout from the photos, so a wrecked car next to a small check makes the result look weak. Once you've looked at the photos (step 4): heavy damage (crumpled body panels, crushed door or pillar, airbags out, towed/totaled) and a check **under $10,000** → hold the case (no Canva, no tracker row), list it in the report as 「照片撞得重、金额小，暂缓」, and take the next folder instead. Heavy-damage cases with big checks are the ones worth doing first. Light damage (scrapes, small dents, scuffed bumper) is fine with any amount.

### 3. Redact the check
Follow `references/redaction.md`. In short: keep the insurer name, amount, generic printed text and **the firm's name (Lingtu Law / Law Office of Shenqi Cai)**. Mosaic every other number, code, date, name, bank detail and signature. Write `boxes.json`, run `$PY scripts/redact.py check page.png boxes.json out/`, then **look at both output images** yourself. The script prints the `crop_media` values for the magnifier. Keep them.

### 4. Photos
- Use the folder's own photos (jpg/png/heic, or a "Vehicle Damage Photos.pdf": render its pages). Two are needed. Pick two that show damage and differ (two angles / two cars).
- None in the folder → borrow from another 人伤 subfolder. Prefer photos not already in `used_photos.json`, and never reuse the photos of the case you're borrowing *for*. Videos don't count.
- Redact per `references/redaction.md` (plates always, faces/reflections, ID decals): `$PY scripts/redact.py photo in.jpg boxes.json out.jpg` (`-` for no boxes). View before and after.
- Append what you used to `used_photos.json`: `{"file_id", "folder", "used_for", "date"}`.

### 5. Text
From `references/content_rules.md`:
- 案件编号 `#LT-YYYY-MMDD` from the check issue date; if the PI tab already has that number, add `-2`, `-3`… (see content_rules.md)
- 事故类型: pick from the table to fit the photos
- 受伤详情: three short phrases from the word lists, ≤15 characters
- 结案天数: random 30–60
- Title: `Name-M:D:YYYY` from the folder's loss date

### 6. Build in Canva
Details and element recognition: `references/template.md`.
1. `copy-design` DAHG9rQstfw with `page_numbers: [1, <insurer page>]`. If the insurer isn't in the template, follow "Insurer not in template".
2. Upload the 4 images (cover check, reveal check, photo 1, photo 2): one `create-upload-url` per file, then `scripts/canva_upload.sh <file> <url>` → mediaId.
3. `read-design` with `open_transaction: true` and `design_content` to get the locator IDs.
4. Page 1: fill both photos + cover check, replace the case number, 事故类型 and 受伤详情, then re-position the two value lines to left≈179.85.
5. Page 2: fill check + magnifier with the reveal check, `crop_media` the magnifier with the printed values, replace the case number and days.
6. `update_title`.
7. Look at the thumbnails `edit-design` returns and fix anything off: text wrapping, magnifier not centred on the amount, a photo cropped so the damage is out of frame (`crop_media` the photo). Save the last page-1 and page-2 thumbnails (`curl` them) as the preview.
8. `finalize: commit`. Teresa has pre-approved committing; she reviews at the end.
9. Verify the commit per template.md "Verifying after commit" (the API thumbnails go stale after a commit).

### 7. Log it in the tracker (成功案例交接表 → PI tab)
Spreadsheet `1JebB6SkokvxnaMh83WiOgr53PoRj9XDAu3KKWwJ1mZ8`, tab **PI** (gid 598651). Columns: A 序号 · B 案件类型 · C 客户（真名） · D 案件文件夹链接 · E Canva链接 · F 完成日期 · **G Approved · H 朋友圈发布** · I 备注.

**Columns G and H belong to Teresa. Never write to them**, not even to clear them; she ticks them herself after review. `scripts/pi_tracker.py` writes only A–F and I (two explicit ranges), updates the existing row if the folder/client is already listed, and otherwise appends with the next 序号:

```bash
scripts/pi_tracker.py --type 车祸 --client "Lianhai Mu" \
  --folder "https://drive.google.com/drive/folders/<folderId>" \
  --canva "https://www.canva.com/design/<designId>/edit" \
  --note "State Farm \$7,500 · #LT-2026-0916 · 侧面碰撞 · 37天；事故照片借用 Zongwei Chen 文件夹 · 待发布官网"
```
- **案件类型 (B)** is a broad category judged from the photos (and the check/folder if the photos are ambiguous): 车祸 (ordinary car-vs-car, the default), 卡车 (a truck/semi/commercial vehicle is involved), 摩托车, 自行车, 行人, 网约车 (Uber/Lyft markings), 狗咬 (dog-bite injury photos), 滑倒摔伤 (slip/trip and fall), or another plain 2–4 character label if none fits. It's coarser than the Canva 事故类型: side impact and rear-end are both 车祸.
- **Canva链接 (E)**: use the stable form `https://www.canva.com/design/<designId>/edit`, not the short `canva.com/d/…` links (those rotate on every API call).
- **完成日期 (F)**: today, `YYYY-MM-DD`.
- **备注 (I)**: `<保险公司> $<金额> · #LT-… · <事故类型简称> · <N>天`, plus anything Teresa should know (borrowed photos and from whom, swapped-in logo, odd check layout), and **always end with ` · 待发布官网`**. That marker is what the publish step looks for; step 8 replaces it once the case is live.
- A case skipped for lack of a check doesn't get a row.

### 8. Publish to the website
Right after the tracker row is written, publish the case per "Publishing" below. **PI cases don't wait for the Approved box** (Teresa, 2026-09-28): ignore column G entirely. A publish failure doesn't undo the Canva post or the tracker row; it just leaves the marker for the scheduled task to retry.

### 9. Report (once, at the end)
Send the saved previews with `SendUserFile` (all cases in one call), then a short report in Chinese per case:
- Canva link (`https://www.canva.com/design/<designId>/edit`), the tracker row number, and the website URLs (zh + en) or why publishing failed
- 保险公司 / 金额 / 编号 / 事故类型 / 受伤详情 / 天数
- Where the photos came from (own folder or borrowed from whom)
- Anything that should get a look: swapped-in logo, borrowed photos, an unusual check layout, skipped cases and why
- Remind her: if the Canva link still shows old images, refresh the page (thumbnail cache)

Don't rename Drive folders (no ✅), don't touch the template, and don't write tracker columns G/H. Teresa does those herself.

## Publishing (step 8, "/pi-mkt 发布", and the scheduled task)
Same model as the `mkt2` skill; field mapping, SQL and verification are in `references/website.md`.

1. Read `PI!A:I` with gws, mapping columns by the header row. Pick rows whose 备注 contains **待发布官网** (in step 8 that's just the row you wrote). **Don't look at Approved (G)**: PI publishing doesn't depend on it. No rows → say "没有待发布的人伤案例" and stop.
2. Build the card from facts only: amount and issue year (from 备注 / the check), "和解结案", and the 案件类型 label. **Don't carry the Canva post's randomized 事故类型 / 受伤详情 / 结案天数 onto the site**, since those aren't verified case facts.
3. Duplicate check → slug `auto-<next>` → privacy check → insert zh + en with `mcp__lovable__query_database` (never the Lovable agent, which costs credits).
4. Verify the zh and en detail pages and the zh list page in the built-in browser (not curl).
5. Replace `待发布官网` in that row's 备注 cell with `官网已发布 <中文URL> · EN <英文URL>` and read it back. On failure, set the row back to draft if inserted, and write `… · 待发布官网 · 发布失败：<原因>` so the next run retries.
6. Never write columns G/H. Report in Chinese: which cases went live (both URLs), which failed and why.

## Scheduled task
The PI publish step also runs daily inside the existing task `mkt-approved-check` (Part 2 of its prompt, after mkt2's Sia/Skye part), at whatever time that task is set to (10:00 local as of 2026-09-28). It catches any PI row still marked 待发布官网, e.g. a publish that failed mid-run. If the task is missing, recreate it with `mcp__scheduled-tasks__create_scheduled_task` (taskId `mkt-approved-check`) with both parts in the prompt; don't create a separate PI task.
