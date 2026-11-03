---
name: skye-initial
description: "Organize a 人才移民 client's uploaded materials for Lingtu Law / SIA 高徒, judge whether each one is actually usable, and keep that case's 材料清单 in step: read every file dropped in 0. Shared Folder or 1. Initial, rename it to the firm's convention, file it under 1. Initial by statutory criterion, write the first full 材料清单 and afterwards only append to it, mark each new file 能用 / 要重新提供 / 不算数 (truncated captures, missing source URLs), then draft the Chinese WeChat message telling the client what to redo and what is still missing. Also maintains the 材料进度 doc, sweeps Priority 1-3 cases daily, books an LA-Beijing meeting hour, and puts receipt numbers onto 案件总表. Use after a case Drive is built and every time the client uploads — 新文件 / 整理材料 / 写材料清单 / 材料进度 / 巡检 / 这些材料能不能用 / 给客户回个话 / 还缺什么材料."
---

# skye-initial — 材料归档与材料清单维护（O-1 / EB1A / NIW）

`skye-case-drive` 建完 case 之后接手。它交出来的是一个空壳：条件文件夹建好了，
案件根目录里有一份**空白的 `{客户姓名} 材料清单`**。这个 skill 把客户传进来的
材料变成归好档、改好名的卷宗，并把那份清单填起来、之后一直维护下去。

```bash
export PATH="$HOME/.local/bin:$PATH"   # gws 在这里，每个 session 跑一次
```

`gws` 报 401 或 `invalid_grant` 时，跑 `gws auth login -s drive`，把 URL 打给
用户让他自己在浏览器里授权。不要碰他的密码和 2FA。

**所有 `gws drive files list` 都要带 `supportsAllDrives`、
`includeItemsFromAllDrives`、`corpora: allDrives`。** 案件文件在共享盘里，
少了这几个参数 API 返回空列表而不是报错 —— 读起来就是「这个文件夹是空的」。
本 skill 的脚本已经带上了；手写调用别忘。

## 已知常量

| 什么 | ID |
|---|---|
| 人才移民 shared drive | `0AIXy3tjXMf-MUk9PVA` |
| O-1 客户文件夹 | `1-g_HDMHwSi7PtV5Nlyw1nUCwXGbQkwpS` |
| EB1A 客户文件夹 | `1rDPCJzYAiG13SzJjkrTqc9D7eUxU12xR` |
| NIW 客户文件夹 | `1D7hKuq2qi4daqIegvjM3YUiN3WKsawjy` |
| 案件总表 | `1hVkR6sLbQossobqyUA4bJ7Qg3P-mrYF2YupMJvdflEQ`，tab **法律** |

收件人和日历地址集中写在 `scripts/notify.py`，改在那里，不要散在各脚本里。
**Skye 的账号是 `skye.s@lingtulaw.com`** —— `skye@lingtulaw.com` 不存在，
拿它查日历会返回 `notFound`，而 `notFound` 的 busy 是空的，看起来像全天有空。
其余：`kk@`、`cathy.c@`、`cassie@`（蔡律师）、`karina.y@`。

材料清单**放在案件根目录**（主 Drive folder），不放在任何子文件夹里。全组每天
开的就是这一份，它必须和案件链接在同一层。

## 两种运行模式

脚本不区分，你区分 —— 判断依据是 `inventory` 报告里的 `initial_file_count`
和清单文档是不是空的。

| | 首次整理 | 增量更新 |
|---|---|---|
| 什么时候 | 刚建完 case，intake 材料已进来 | 客户后来又传了东西 |
| 清单 | `checklist.py init` 写整份 | `checklist.py insert` / `mark` 只加不改 |
| 归档 | 建条件文件夹 + 归档全部 | 只归档 `new_files` |

---

## Step 1 — 找到案子，盘点现状

没有上下文就先问客户姓名和案件类型。按姓名在对应案件类型的父文件夹下找案件根
目录，然后：

```bash
python3 <skill>/scripts/scan_materials.py inventory --case-root <CASE_ROOT_ID>
```

一次给出：`0. Shared Folder` / `0. Intake` / `1. Initial` 的 id、材料清单文档、
`new_files`（还没归档的上传）、`already_archived`、`loose_in_initial`（直接丢在
`1. Initial` 根上、需要改名归位的那批）、`generated_docs`（律所自己生成的
intake note 和上传指引，**不归档**）。

`missing_folders` 非空说明这个案子不是 skye-case-drive 建的（老案子结构不一样，
见 Qing Yang、Xuan Shen）。这时候停下来问用户要不要按新结构整理，别自己动手改
别人的老卷宗结构。

**先读 intake note。** DDL、加急与否、身份转换路径、案件背景都在里面，写清单
头部要用。它在 `generated_docs` 里。

## Step 2 — 读文件，认出它是什么

`new_files` 和 `loose_in_initial` 里每个文件都要读过再命名。用 Drive connector 的
`read_file_content`（服务端做 OCR 和文本抽取），扫描件和 PDF 都能读。

要认出三件事：**属于哪条标准、属于哪个条目、是哪一类证据**。
`references/naming.md` 有证据类型词表。

认不出来的不要猜。宁可在报告里列成「待确认」让同事看一眼，也不要把一份合同归进
「奖项」—— 归错的文件比没归档更难发现，因为文件夹看着是满的。

## Step 3 — 建条件文件夹

```bash
python3 <skill>/scripts/scan_materials.py layout \
  --initial-id <INITIAL_ID> --case-type EB1A
```

幂等，重跑只会报 `already_there`。O-1 必须指明 O1A 还是 O1B —— 两个子类的标准
几乎不重合，建错等于给案子搭了个错的骨架。案件类型还没定 A/B 的，先只归
`0. 个人信息` 和身份材料，把这件事在报告里说出来。

条目文件夹由 Step 4 的 plan 顺带建，**不要预先建空的**。

## Step 4 — 改名归档

写一个 plan 文件，一条一个文件：

```json
[
  {"src_id": "1abc...",
   "name": "奖状-iF Design 2026 Sofia.pdf",
   "path": ["1. Awards 奖项", "iF Design 2026 - Sofia"],
   "op": "copy"},
  {"src_id": "1def...",
   "name": "护照首页-Qing Yang.pdf",
   "path": ["0. 个人信息"],
   "op": "move"}
]
```

`op` 用 `copy`（来自 `0. Shared Folder` / `0. Intake`，客户原件留在原地）或
`move`（本来就在 `1. Initial` 里，只是改名归位）。命名规则见
`references/naming.md`。

```bash
python3 <skill>/scripts/scan_materials.py archive \
  --initial-id <INITIAL_ID> --plan /tmp/plan.json [--dry-run]
```

每个副本都会打上 `appProperties.eon_src` = 客户原件的 file id，这就是下次
`inventory` 判断「哪些是新的」的依据。重跑安全：已归档的直接跳过。

## Step 5 — 写 / 更新材料清单

格式规范在 `references/checklist-format.md`，**动手前先读**。版面是从五份真实
清单里量出来的（Times New Roman 12pt、标题加粗、章节行纯文本以「：」结尾、
正文 Tab 缩进圆点），不是可以自由发挥的部分。

### 首次：写整份

`assets/skeleton-{EB1A,O1A,O1B,NIW}.txt` 是四种案件类型的现成骨架，章节顺序和
固定措辞都对好了，`{...}` 是占位符。拷一份出来填，别从零拼章节。

客户已有的材料写成条目并标 `（已有）`/`✅`，该案件类型要求但还没有的，把骨架里
的空条目留着 —— 那是开会时逐条要问的清单。用不上的整节删掉（比如客户完全没有
展览）。

```bash
python3 <skill>/scripts/checklist.py init --doc-id <DOC_ID> --source /tmp/checklist.txt
```

清单文档不存在（老案子）就在**案件根目录**新建一个 `{客户姓名} 材料清单`：

```bash
gws drive files create --params '{"supportsAllDrives": true, "fields": "id,name"}' \
  --json '{"name": "Qing Yang 材料清单", "mimeType": "application/vnd.google-apps.document", "parents": ["<CASE_ROOT_ID>"]}'
```

### 之后：只加不改

```bash
python3 <skill>/scripts/checklist.py dump --doc-id <DOC_ID>          # 先看现在有什么
python3 <skill>/scripts/checklist.py insert --doc-id <DOC_ID> --section "奖项" --source /tmp/add.txt
python3 <skill>/scripts/checklist.py mark --doc-id <DOC_ID> --match "Orpetron" --marker " ✅"
```

**永远不要整篇重写这份文档。** 每一份真实清单上都挂着 Google Docs 评论串和同事
手改的内容，整篇替换会把评论变成孤儿、把手改内容默默吞掉。新材料对应的条目
已经在清单里，就 `mark`；是全新条目，就 `insert` 到对应章节末尾。

`insert` 之前先 `dump` 一次确认章节名 —— 每份清单的章节措辞略有出入
（「评审」/「评委」、「原创贡献」/「原创性重大贡献」），按文档里已有的写法来，
不要按你以为的标准名去插，那会插不进或者插错地方。

## Step 6 — 报告

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 本次归档：N 件
   奖项 → iF Design 2026 - Sofia：奖状、获奖页面
   评审 → Orpetron：邀请函、打分表 sample
❓ 待确认：xxx.pdf（读出来像合同，不确定归哪条）
📋 材料清单已更新：[链接]
   新增条目：Muse Design 2026
   标记完成：Orpetron ✅
⏳ 仍缺（按重要程度）：
   1. 红点 2026 奖状 —— 10/15 官网公布后客户上传
   2. 推荐人 2 位的 legal name/title/linkedin
   3. 最近三个月 paystub
👉 建议下一步：[具体行动，谁做]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

「仍缺」按对案子的重要程度排，不按章节顺序 —— 这一段是直接拿去催件的。
每条要写清是客户做还是律所做。

---

## Step 7 — 判断材料能不能用，然后写给客户的话术

归档完不等于收到了。**每一份新材料都要过一遍「能不能用」**，再把结论写成客户看得懂的话。

### 7a. 逐份判断

三个结论，只能选一个：

| 判定 | 意思 |
|---|---|
| ✅ **能用** | 归档，材料清单上标完成 |
| ⚠️ **要重新提供** | 收到了，但这一份递不出去 —— 说清楚为什么、以及具体怎么重弄 |
| ❌ **不算数** | 跟这条 criterion 对不上，或者根本不构成证据 —— 归到 `弃用`，并说明还需要什么 |

判「要重新提供」的常见情形（这几条后面 `skye-submission` 递交前还会再审一次，
在这里拦住比在递交前拦住便宜得多）：

- 网页 PDF **抓截断了** —— 少页、正文被切掉、只抓到首屏
- 网页抓取件**页脚没有来源 URL**，或者 URL 里带 `source=chatgpt` 之类的 AI 工具标记
- 截图**代替原件** —— 奖状、合同、paystub 要原件或官方 PDF
- **糊到看不清**关键字段：姓名、日期、金额、签章
- 缺**署名 / 日期 / 出处**，无法证明是谁在什么时候发布的
- 中文件本身没问题，但**要走翻译**（交给 `skye-translate`，不算「不能用」）

⛔ **不要替客户估计「大概能用吧」。** 拿不准的标成 ⚠️ 并写清楚疑点，让律师定。

### 7b. 生成给客户的话术

判完直接出一段可以粘进微信 / 邮件的中文，**给用户过目后再发，不要自己发出去**。

结构固定三段，缺哪段就省掉哪段：

```
{客户称呼}您好，材料我们收到并整理好了，跟您同步一下：

✅ 已收妥
   · {材料名}
   · {材料名}

⚠️ 这几份需要麻烦您重新提供一下
   · {材料名} —— {为什么不能用，一句话}
     怎么弄：{具体到可以照做的动作}

📋 还差这些
   · {材料名} —— {谁做、什么时候之前}

有任何不清楚的地方随时问我。
```

写话术的三条规则：

1. **只写动作，不写分析。** 不写「这条 criterion 比较弱」「可能会被 RFE」——
   风险和策略单独在聊天里给律师，不进客户消息。这跟材料清单是同一条规矩。
2. **「怎么弄」要具体到能照做。** 不写「请重新提供清晰版本」，写「请用手机横屏拍原件全页，
   确保四个角都在画面里，不要用截图」。网页类写「请把这个链接发给我们，我们来抓取」。
3. **不催没到期的东西。** 有明确时间点的（比如奖项官网 10/15 才公布）写清楚时间点，
   不要放进「还差这些」里制造焦虑。

### 7c. 报给律师的那一份另外写

⚠️ 和 ❌ 的技术原因、对案子的影响、哪条 criterion 现在悬着 —— 这些写在给用户的报告里
（Step 6 的格式），不进客户话术。

---

# 自动化任务

以下四件事和上面的手工整理共用同一套脚本，但触发方式不同：前面是「客户传了东西
就跑一次」，这四件是按时间或按信号跑。

## A. 每日巡检 Priority 1-3

```bash
python3 <skill>/scripts/daily_sweep.py            # 有新材料才发信
python3 <skill>/scripts/daily_sweep.py --dry-run  # 打印邮件不发
```

读案件总表法律 tab，取 Priority 为 1/2/3 且状态不是
Submitted/Approved/Denied/TERMINATED 的案子，逐个看 `0. Shared Folder` 和
`0. Intake` 里有没有还没归档的上传，有新增就把摘要发给 kk / cathy.c / skye.s。

两个设计点值得知道：

- **只报「上次看过之后」的新增。** 状态存在
  `~/.local/state/skye-initial/sweep_state.json`（`EON_STATE_DIR` 可改）。没这个
  的话，一份还没来得及归档的文件会连续四天出现在摘要里，然后所有人就不看摘要了。
  摘要里另有「累计待归档 N 件」，积压依然可见。状态文件丢了不算错，下一次会把
  当前所有待归档的当成新的报一遍 —— 宁可多报一次。
- **律所自己放进 shared folder 的文件不算新材料。** 判断依据是
  `lastModifyingUser` 是不是 `@lingtulaw.com`。少了这一条，摘要会把律所写完
  拿给客户看的材料清单、方案当成「客户传了新东西」报回给律所自己。

没有新材料就不发信 —— 每天一封「今天没事」的邮件等于训练大家忽略这个发件人。
要日报就加 `--always-send`。

**这个脚本自己不会每天跑。** 需要在跑它的那台机器上挂一个定时任务
（scheduled task / cron），见 `references/automation.md`。

## B. 材料进度 doc

内部文档，叫 `{客户姓名} 材料进度`，和材料清单一起放在案件根目录。
清单是给客户和会上用的，进度表是律所自己的跟踪视图 —— 两份文档，不要合并。

```bash
python3 <skill>/scripts/progress.py ensure  --case-root <ID> --client-name "Dechao You"
python3 <skill>/scripts/progress.py collect --case-root <ID>
```

`collect` 一次给出：材料清单里的条目（连同 ✅/（已有）标记）、`1. Initial` 下
实际归了什么（条件 → 条目 → 文件数）、还没归档的上传、以及**旧进度表里的时间线**。

需求这一侧是从材料清单读回来的，不是按案件类型重新推的 —— 开会时同事会删掉用不上
的条目、加上新的，进度表要跟的是这个案子真正需要什么，不是模板说它需要什么。

写入用 `checklist.py init --doc-id <进度表ID> --force`。这份文档是机器生成的，
整篇重写是安全的（正因如此它开头要写「本文档自动生成，请勿手改，讨论写在材料清单里」）。
唯一必须跨次保留的是时间线，所以把 `previous_timeline` 原样重新写进去，再追加今天这条。

正文用 `☑`/`☐`，和材料清单的 `✅` 区分开，两份文档不会看混。

写完把汇总发给 kk / cathy.c：

```bash
python3 <skill>/scripts/notify.py --audience progress --subject "..." --body-file /tmp/summary.txt
```

## C. 定稿后排会议

信号：案件文件夹里出现文件名带「定稿」或 Final 的材料清单。

```bash
python3 <skill>/scripts/meeting.py detect --case-root <ID>
python3 <skill>/scripts/meeting.py slots --days 10 --duration 60
```

`slots` 查 Skye 和蔡律师的 free/busy，给出**同时**落在律所和客户可接受时段内的
整段空闲。默认律所 **09:00–17:30**（美西，律所实际能约会的时间），客户
08:00–22:00（北京）。

**一年里有半年这两个窗口没有重合区间**，这不是日历排满了，是时区算术：

| | 洛杉矶 09:00–17:30 对应北京 | 一小时的会 |
|---|---|---|
| 夏令时 PDT（3 月–11 月） | 次日 00:00–08:30 | **排不出来** |
| 冬令时 PST（11 月–3 月） | 次日 01:00–09:30 | LA 16:00–17:00 = 北京次日 08:00–09:00 ✅ |

所以脚本在一个时段都找不到时，不会只说「没空」—— 它会带着几种放宽方式各重跑一遍，
告诉你哪一种能开出时段、能开几个：

```
  把客户窗口放宽到 07:00 起          2 个 | 例：09/14 16:00–17:00 LA = 09/15 07:00–08:00 CN
  律所延到 18:00                    1 个 | 例：09/14 17:00–18:00 LA = 09/15 08:00–09:00 CN
  律所延到 19:00                    5 个
  律所提前到 07:00（客户当晚 22 点后） 4 个
```

放宽顺序是先动客户那边 —— 请北京客户 07:30 开会，比请两位律师留到 17:30 之后
是更小的人情。选定后用 `--la-window` / `--cn-window` 重跑。

- **任何一个日历读不到，脚本直接拒绝出方案**（退出码 2）。freebusy 对读不到的
  日历返回空 busy，跟「全天有空」长得一模一样，据此排会是在猜。
- 时段是按「整段会议同时落在两个窗口内」筛的，不是写死某个钟点，夏令时切换时
  窗口自己跟着挪。

选好时段后，先发给 Skye 确认（抄送蔡律师）：

```bash
python3 <skill>/scripts/notify.py --audience meeting --subject "..." --body-file /tmp/ask.txt
```

Skye 确认后，把 `slots` 输出里的 `phrasing` 给用户，由人发给客户。
时间带上午/下午和分钟，**两地日期都写全**：

```
09/14/2026 洛杉矶时间下午4点，客户当地时间09/15/2026（次日） 上午7点，您是否有空，我们约个会议，对一下材料；
```

**不要自动发给客户。** 这条话术是给人复制的。

## D. Case number 回填

```bash
python3 <skill>/scripts/case_number.py scan --days 90 [--client "Dechao You"]
python3 <skill>/scripts/case_number.py apply --client "Dechao You" --case-number IOE8342503951 [--dry-run]
```

`scan` 搜**当前登录的那个信箱** —— 在 KK 电脑上是 kk@，装到 Skye 电脑上就是
skye.s@。收据号按「三位字母 + 十位数字」识别。搜不到只报「没找到」，不报「没有
收据号」：通知可能只进了同事的信箱。三个人的信箱要一次查全，得三台机器各跑一次，
或者按 karina.y 那套给每个账号单独授权。

`apply` 把号码**追加**到案件总表 F 列重要笔记（法律 tab 没有收据号那一列）。
F 是人手写的，所以只追加、不覆盖，已经在格子里的号码不会重复写。覆盖 F 会悄悄
删掉同事的笔记，那种损失要等到需要那条笔记时才会被发现。

然后把话术给用户：

```
您的Case number：IOE8342503951
查案子网站：https://egov.uscis.gov/
```

同样**不自动发给客户**。

## 自动发信的边界

`notify.py` 里三个收件人组全部是 `@lingtulaw.com`，非律所地址会被硬拒。
客户话术一律只打印不发送 —— 会自己给客户发信的自动化，早晚会就着错的案子发给
错的人，而那件事没法道歉回来。

## 案件总表

**默认不动。** 法律 tab 的 I–O 是起草阶段的进度列（框架/PL/Exhibit/Form），
材料收集没有对应列，硬填进去等于给别人的进度列写假数据。

用户明确要求时才写，而且只写 F（重要笔记）或 G（Deadline）。列位见
skye-case-drive 的 `references/tracking-sheet.md`。

例外是 case number：`case_number.py apply` 会往 F 列**追加**收据号，这是上面
D 节明确要做的事。追加不覆盖。

需要留时间线的话，往 `0. Intake` 里已有的 `Intake Note - {name}` 文档追加一段
带日期的记录（`gws docs +write`），不要在材料清单里加「更新记录」章节 ——
那份文档是给客户看和开会用的。

## 什么时候直接做，什么时候停下来问

案子找到了、案件类型确定了，Step 1–6 一路做完。归档是复制，清单是追加，都可以
回退，逐步确认只是浪费用户时间。

三种情况停下来：

- **`missing_folders` 非空** —— 老结构的案子，问清楚要不要改结构。
- **O-1 没定 A/B** —— 条件文件夹建错等于骨架错了。先归个人信息和身份材料，
  把这件事说出来。
- **一份文件认不出归属** —— 报告里列出来，不要猜着归。

客户材料里出现护照号、SSN、W-2 这类信息是正常的，读它们、按它们命名和归档就是
这个 skill 的工作；但不要把这些数字抄进材料清单正文 —— 那份文档是要发给客户和
在会上投屏的。
