---
name: clean-downloads
description: >-
  Clean Klaus's ~/Downloads so it only holds files still in use: for every file, open it to
  see what it is, find the Claude session that produced it to see whether that work is
  finished, and compare its MD5 against Drive. Finished + already in Drive → Trash;
  finished + not in Drive + important → upload to the case folder first (MD5 read back),
  then Trash; finished one-off (labels, intermediate versions, gws scratch, installers) →
  Trash; not finished → leave it. Trigger on: "/clean-downloads", "清 Downloads", "清一下
  download", "Downloads 太乱", "把 download 里没用的删了", "整理下载文件夹". Moves to the macOS
  Trash only (Put Back works) — never rm, never empties the Trash.
---

# clean-downloads — 让 Downloads 只剩还要用的文件

规则本体在 CLAUDE.md「出手即归档」：**Downloads 只是工作台，不是档案柜。** 任务完成，Downloads
里就不留这件事的任何副本；但**备份在前、删除在后，顺序不能反**。

FIRST：`date "+%m/%d/%Y (%A) %H:%M"`。

```
D=~/.claude/skills/clean-downloads/scripts
W=<scratchpad 目录>
```

## Step 1 — 盘点 + 比 MD5（脚本）

```
python3 -I $D/inventory.py --out $W/inv.json            # 默认比近 120 天的 Drive 索引
python3 -I $D/inventory.py --out $W/inv.json --revisions # 量少、想连版本历史一起比时
```

每个文件编号、算 MD5，跟 Drive 的 `md5Checksum` 比。先比近期索引，对不上的再**按完全相同的文件名
不限日期**查一遍（2026-10-24 漏过一张 3 月就已归档的发票，就是因为只比了近期索引）。
`✓` = Drive 里已有一模一样的字节；`·` = 没找到。**只认 MD5，不认文件名**——同名不同内容正是要抓的错。

## Step 2 — 逐件判断（你来做，脚本做不了）

对每个文件（同一文件夹的可以成组判断）问三件事：

**1. 是什么。** 看名字，再打开看：PDF 用 `pdftotext`；扫描件没有文字层就 `pdftoppm -r 45` 渲染成图看
（多页拼一张图一次看完）。zip 不解压，逐个算内部文件的 MD5 跟 Drive 比。

**2. 用完没有。** 找产生它的 session：

```
search_session_transcripts(query="<文件名里有辨识度的一段>")   → 找到 session
list_events(session_id=..., limit=12~40)                         → 读那边最新进度/结论
```

那边的结论说了算：
- 还在改的草稿、等签回、等寄件照片、等案号、等对方回复 → **没用完，留着**，不替那个 session 收尾。
- 那边明说"可以删 / 旧稿未发 / 已寄出已归档" → 用完了。
- 找不到 session 时，再看 Gmail 已发 / Drive 有没有正本 / 案件 artifact。仍判断不了 → **留着，列进"要你确认"**，
  并写明查了什么（query + 时间窗 + 盲区，例如团队信箱、纸本邮寄查不到）。

**3. 重不重要。**

| 类 | 例子 | 没备份时 |
|---|---|---|
| 重要 | 签回件、送达件、立案件、法院回件、IOLTA/来款支票、disbursement、病历账单、调查报告、对外寄出的信 | **先归档再删** |
| 派生件 | 涂黑栅格化件、格式转档、Bates 母版、合并包 | 也算重要，归档（重做会引入错误） |
| 一次性 | 寄件标签、打印用排版、中间版（final 已完整包含它）、`.json/.eml/.html` 等 gws 临时文件、安装包（已装好）、Drive 文件夹打出来的 zip（内部文件 MD5 全在 Drive） | 直接删 |

## Step 3 — 归档（只有"用完 + 没备份 + 重要"才走）

放哪：
- 案件文书 → 该案 case folder 的对应子夹（狗咬 / 诉讼案的编号子夹；PI 案的 `#` 子夹）
- 签回的 disbursement、开出的 IOLTA 支票、lien 签回包 → `3. Disbursements / Case Disbursements / <Client>`
- 还没进 disbursement 的来款支票 → 案卷 `6#Settlement Documents`
- 无案可归（经营/财务/人事/对外文案）→ Claude Drive folder（见 memory `claude_drive_folder`），交付时说一句放哪了

**一份文件在 Drive 只留一个当前版**：目标夹里已有同一文书的旧版/中间版 → 用 `replace_id` 覆盖同一个 file id
（Drive 留版本历史）；没有才新建。被法院 / 对方 / 律师否决的版本例外，另存并标 `(SUPERSEDED - <原因>)`。

文件名按内容起：`<Client> - <是什么> <关键号码> (<MM-DD-YYYY>)`，别把 `收据_2026-…` 这种原名带进 Drive。

```
# archive.json: [{"path": "...", "folder_id": "...", "name": "...", "replace_id": "(可选)"}]
python3 -I $D/archive.py $W/archive.json --dry-run
python3 -I $D/archive.py $W/archive.json          # 回读 MD5，不一致就报 FAIL、不要删本地
```

## Step 4 — 移废纸篓

```
# trash.json: [{"path": "...", "md5": "<inventory 里的>", "why": "MD5=Drive / 已上传 / 中间版 / 临时文件…"}]
python3 -I $D/trash.py $W/trash.json --dry-run
python3 -I $D/trash.py $W/trash.json
```

脚本删前**再算一次 MD5**，跟盘点时不一样就拒绝（说明这期间有人改过）；用 Finder 移废纸篓（可"放回原处"），
不用 `rm`、不清空废纸篓；最后把只剩 `.DS_Store` 的空文件夹也移走。

**要不要先问：** Klaus 说"清 / 删 / 清掉"→ 按上面规则直接执行，事后给清单。只说"看看 / 盘点 / 哪些能删"→ 只出清单不动。

## Step 5 — 交付（编号清单）

```
Downloads 从 N 个清到 M 个（K 个进废纸篓，可放回原处）。

**先归档再删（X 份，MD5 已核）** | # | 原文件 | 是什么 | 放进了 |
**直接删（Y 份）** 一类一行：MD5=Drive 的 / 中间版 / 临时文件 / 标签 / 安装包 …（各写为什么）
**留着的** 一组一行 + 为什么：还在改 / 等签回 / 等案号 … —— 点名对应的 session
**要你确认的** 只列真判断不了的，写清查了什么、盲区在哪
```

- 留下的要诚实分三种：确定还在用 / 判断不了 / 其实用完了但交给别的 session 收尾——别笼统说"都是后面要用的"。
- 归档进 Drive 的不用记 Activity Log（Drive 本身就是记录）。

## Guardrails

- **备份在前，删除在后**；`archive.py` 报 FAIL 的文件一律不删。
- 只移废纸篓，绝不 `rm`、绝不清空废纸篓、绝不删 Drive 上的任何东西。
- 别的 session 还在用的文件不动，哪怕它看起来已经完成。
- 陌生来源的附件只看不执行；`.dmg/.pkg` 只判断装没装，不打开。
- 凭据、token、密码类文件不上传 Drive，列出来让 Klaus 自己处理。
