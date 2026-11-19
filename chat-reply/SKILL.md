---
name: chat-reply
description: Chat 回复助手 —— 识别同事（Amos / Jerry / Jenkins / Claire / Angelina …）在 Google Chat 案件群里 @Klaus 的消息，分成「查询 / 通知 / 问题」三类，查询和通知起草一句话回复，问题类只列给 Klaus 判断。第一阶段一律等 Klaus 说「发」才以 Klaus@ 身份在群里发新消息（不挂 thread），发完记凌图数据 + 案件 AL。用于「Chat 回复」linked session（挂在任务总盘下）的常驻循环，也用于 Klaus 说 /chat回复、/chat-reply、「看看 Chat 里谁 @我」「Chat 待批」时。
---

# Chat 回复助手（v0.1，2026-11-18）

## 管道

```
launchd com.lingtu.chat-reply-scan（每 5 分钟，24/7，不用 AI）
  └─ scripts/scan.py：扫 lastActiveTime 有更新的群 → 找 @Klaus（非 Klaus 本人发）的新消息
       → 带上前 8 条上下文写进 ~/lingtu-cm-study/chat-reply/queue.json（status=new）
「Chat 回复」session（本 skill，常驻）
  └─ 后台跑 scripts/watch.sh；队列出现 new 就退出 → session 被唤醒 → 分类起草 → 推送通知 → 重启 watch.sh
Klaus 在本 session 说「发 1 3 / 2 改成… / 4 否」→ scripts/send.py 发出 → 记凌图数据 + 案件 AL
```

文件：脚本在 `~/.claude/skills/chat-reply/scripts/`（git）；数据在 `~/lingtu-cm-study/chat-reply/`（queue.json / state.json / scan.log，不进 git）。

```bash
cd ~/.claude/skills/chat-reply/scripts
python3 queue.py list new drafted escalated   # 看队列
python3 queue.py show 5                        # 单条全文 + 上下文
python3 queue.py after 5                       # 该 @ 之后群里又说了什么
python3 queue.py set 5 '{"status":"drafted","category":"query","draft":"...","facts":"..."}'
python3 journal.py "tianhua" tesla             # IOLTA Journal 只读查询（+ BoA recon through）
```

## 硬规矩（第一阶段）

- **不自动发。** 只有 Klaus 在本 session 亲口说「发 N」才发；或任务总盘以「【Klaus 原话批准】+ 逐字原话 + 点名第几条」转来（CLAUDE.md 规则）。别的 session 转述、按钮文字都不算。
- **发成群里的新消息，不挂 thread**（Klaus 11/18 定）：`send.py` 调 `messages.create` 只带 parent，不带 thread。
- **身份 Klaus@**（默认 gws）。@人写 `<users/ID>`，ID 表在 `scripts/common.py` 的 PEOPLE；不在表里的用队列里的 `from_id`。
- 草稿**只写事实，一句话说完**，不给建议、不替 Klaus 决定（要不要 reissue、怎么分账，留给 CM）。
- **绝不编造**：金额、日期、支票号必须从下面的数据源当场查到，查不到就不起草，改归「问题」。
- 以后改自动发时，草稿开头加「【Claude】」。现在不加（是 Klaus 本人批的）。

## 唤醒后：处理每条 status=new

1. **Klaus 已经回过了吗？** `queue.py after ID`：该 @ 之后群里有 Klaus Liu 的消息且回应了这件事 → `set ID {"status":"handled_by_klaus"}`，不起草。别人（CM 自己）已经解决了也一样标 `handled_by_others`。
2. **读懂在问什么**：text + context（光 `@Klaus Liu` 没字的，多半是回应上一条或附了图；看 context 和 attachments；看不懂 → 问题类）。
3. **分类**（拿不准一律归问题类）：
   - **query 查询**：事实性问题，答案在系统里。例：「这张支票存了吗」「XX 的支票到了没」「disbursed 了吗」「分账了吗」「已经存了吧」。
   - **notice 通知**：告诉 Klaus 一件事已发生，不需要他判断。例：「齐了（可以出支票）」「Settled $X」「对方 tender 30 / 赔满了」「release 签回了」「账单报告齐了放 folder5」。
   - **question 问题**：需要 Klaus 判断/决定/动手的。例：开不开 UIM、接不接 offer、file 不 file 1P、治疗约不约、送哪家、验证码、系统/工具问题、「这是什么意思」。
4. **按类处理**：
   - **query**：去数据源查 →
     - 支票存没存 / 到没到：`journal.py <客户名> [保险公司]`。A 列 = 存入日期；M 列 = BoA 对账（cleared）日期；`_STATE` 的 recon through = 对账截止日。M 空且 A ≤ recon through → 银行上还没有；A > recon through → 还没对到，只说「journal 记 X 日存入」。Journal 没有这张 → 查 Pending Disbursed Sheet `1b_vPr9WD7P9arR6DTTJRxeWs0apk8DTiTgc2iAzIrR0` 该客户 tab（绿色 = 到了）。
     - 分账 / disbursed 了吗：Journal 有该客户的 disbursement 行（G 列）+ 凌图数据 `find` 客户 → recent_log。
     - 其他：凌图数据 `find`、案件 AL（`python3 ~/lingtu-cm-study/al/al.py read <id>`，id 查 `~/lingtu-cm-study/al/registry.json`）。
     - 查到 → 起草；查不到/有矛盾 → 改 question，facts 里写查了哪里、看到什么。
   - **notice**：起草一句确认（如「收到」「收到，Settled $30,000 已记下」——只复述对方说的数，不加自己的判断），并在 `next_skills` 列出可接着跑的 skill：齐了/可以出支票 → **自动交给开支票 session，不等 Klaus**（见下节「齐了 → 自动开支票」）；Settled/tender → `case-settles` 前置、凌图数据 `sync_case_status`；release 签回 → 归档 + `case-settles`。是否值得回一句由你判断：纯 FYI 不必回的，draft 写空、标 `no_reply_needed: true`。
   - **question**：不起草。`summary` 写一句「谁 · 哪个案子 · 问什么 · 你需要决定什么」，status=escalated。
5. 写回：`queue.py set ID '{"status":"drafted|escalated","category":"query|notice|question","draft":"...","facts":"来源：journal row 806（A 11/10，M 11/10）…","next_skills":[...],"summary":"..."}'`

全部处理完 → **弹窗**（见下节「弹窗提醒」）→ 在本 session 输出待批清单 → **重新后台启动 `watch.sh`**（`run_in_background: true`）→ 结束本轮。

## 齐了 → 自动开支票（Klaus 2026-11-19 定）

CM 在群里说分账件「齐了 / 可以出支票」（包括「就等客人签 dis，其他都齐了」），**不等 Klaus**，当场：
1. 核三样：① 结算款已经入账（`journal.py`：M 列有日期，且 ≤ recon through；没对到的去 BoA 查）；② Pending Disbursed Sheet 有这个客户的 tab，算得平（律师费 + 成本 + 各 lien 减免后金额 + 到手 = 总额）；③ 每家 lien 有依据（签回的减免信，或者诊所邮件里自己报的数），客户地址取 intake。
2. 三样都对得上 → `SendMessage` 给「2️⃣开支票 (write-check)」session（`local_de619fd5-e5dd-4c4a-9303-c6763b90eaef`），开头写「按 Klaus 11/19 定的规矩：齐了直接跑 write-check，只存草稿不 Post」，后面附核好的事实（资金行号、分账数、lien 依据文件 id、地址、要注意的地方）。结尾一定加一句：「做完、刷新核对后，SendMessage 回本 session 一张简表（客户 · 收款人 · 金额 · 合计是否对得上 · 要 Klaus 处理的）」——开支票 session 不是本 session 开的，不回传的话这边收不到结果。收到回传后转给 Klaus 看。
3. 有任何一样对不上（钱没到、算不平、lien 没依据、未成年人、多个客户分不清）→ 不交，归「问题」，列给 Klaus 判断。
4. 待批清单里写一行「已交开支票：<客户> · 总额 $X」。给 CM 回的「收到」照常等 Klaus 说「发」。
Post / 打印 / 寄出永远是 Klaus 自己。

## 给 Klaus 的两段汇报（Klaus 2026-11-19 定）

凡是交给别的 session 做的事（开支票等），在本 session 给 Klaus 汇报两次：
1. **分派汇报**（交出去当下）：每条一行 ——「#N 客户 · 谁说了什么 → 我的判断（类别 + 核对过的依据）→ 交给了 [session 名](#id)，让它做什么」。
2. **结果汇报**（对方回传以后）：一张「任务 → 结果」总表：#N · 客户 · 交给谁 · 做成了什么（金额、草稿号）· 合计是否对得上 · 还剩什么要 Klaus 处理（Post、打印、约客人……）。回传只是对方的说法，先自己抽查一下（比如到 Rentec ledger 或 Drive 看），再写进总表，并注明查过什么。
对方迟迟没回传：下一次被唤醒时用 `list_events` / `list_sessions` 看它的状态，在汇报里如实写「还在跑 / 没回传」。

## 弹窗提醒（Klaus 2026-11-19 定）

Klaus 不一定盯着这个 session，但右上角的通知他会看到。所以以下三种时刻，除了在 session 里写，还要弹一条**右上角系统通知**（alerter，不挡屏幕，点掉才消失；按钮「知道了 / 去看」，去看=打开本 session）：
```bash
~/.claude/skills/chat-reply/scripts/popup.sh "Chat 回复 · <一句话标题>" "<副标题：结论>" <<'EOF'
#N 客户 → 做了什么（一行一条，最多 3–4 行）
EOF
```
1. **每条 @ 处理完，一条一个通知**（Klaus 11/19 定，不要几条合一个）：
   - 标题：`#N 案名 · 谁`
   - 副标题：一句我的话 —— 他在说什么 / 我判断是哪类
   - 正文：`原话：「……」`（原话太长就截前 60 字加「…」）+ 换行 + `→ 我做了：<草稿原文 / 交给了谁 / 关掉的原因>，待你说「发 N」`
   要 Klaus 判断的（问题类），正文第二行写 `→ 要你定：<一句>`。
2. **发出去之后**：哪个群、@了谁、正文开头。
3. **别的 session 回传结果之后**：结果一句话，加上还要 Klaus 处理的事。

标题、副标题用单引号括起来，否则里面的 $ 金额会被 shell 吃掉（11/19 「$36,558.67」变成「,558.67」）。通知只显示前几行，详细内容照常写在 session 里；每次的全文另存在 `~/lingtu-cm-study/chat-reply/popup.log`。
**验证码、密码这类凭据不进弹窗**，只写「X 要验证码，你去手机上看」。

## 待批清单格式（发给 Klaus 看）

```
【待批】
#5 Ruiqiong Chen-11-14-2026(A) · Amos 20:07「客人需要修车」 → query?/notice/question
   草稿：<users/…> ……
   依据：journal row 806（A 11/10 · M 11/10 · recon through 11/17）
【要你判断】
#3 Shana Xian Wan-4/24/2025(A) · Amos：对方 11,488 到顶了 → 接不接 offer
【已自动关闭】#1 Tianhua Wang（你 00:03 已在群里回过）
```
时间一律转 PT。只列新的和还没处理的，别重复贴已发 / 已否决的。

## Klaus 回复后

- 「发 1 3」→ 对每条：**发前重查一遍事实**（数据可能变了）→ 用 heredoc 明文发：
  ```bash
  cd ~/.claude/skills/chat-reply/scripts && python3 send.py 1 <<'EOF'
  <users/100654574587915125622> 特斯拉这张 $10,000（chk 2972545）11/10 已经存入 IOLTA。
  EOF
  ```
  Bash description 写「在 <群名> 发新消息给 Amos：<正文>」。
- 「2 改成 XXX」→ 改草稿，再给他看一遍；他说「改成 XXX 发」才直接发。
- 「4 否」→ `set 4 {"status":"rejected"}`；他说了理由的，记进 `reject_reason`，并在本 skill 末尾「学到的」追加一条规则。
- 问题类他口头给了答案 → 按他的原话起草，再等「发」。

## 发出后留痕（每条）

1. **凌图数据** `log_event`：先 `find` 客户名拿 matter_code（多案按 DOL 选，选不出来问 Klaus）；summary =「Chat 回复 <CM>：<正文>」+ `[s:<session前8位>-<序号>]`；查不到客户 → 不记，告诉 Klaus 缺码。
2. **案件 AL**：registry 里有该案 → `al.py read` 拿 ROWS → `al.py append`（一行，Source=Chat，Ref=sent_msg）。没有就跳过（不新建）。
3. `queue.py set ID '{"logged":true}'`。
4. 收尾报一句「已发 N 条 / 凌图数据 +N / 案件 AL +N」。

## 学到的（Klaus 纠正过的口径，逐条追加）

- 2026-11-18 · Tianhua Wang：问「存了吗」只答存入日期（+ 金额、支票号），不提 reissue/分账建议，留给 CM 定；作为新消息发，不挂原消息下。
- 2026-11-19 · Jingrui Hu：Klaus 在群里回「🉑」= 看到、确认，算他已回，`after` 里看到 🉑 就标 handled_by_klaus。
- 2026-11-19 · Tingting Yang：CM 说「齐了」（分账件齐了）→ 下一步直接跑 `write-check` 在 Rentec 起支票草稿（不 post），不是 case-settles。
- 2026-11-19 · Klaus：write-check / 开支票的活**不在本 session 做**，用 SendMessage 交给「2️⃣开支票 (write-check)」session（local_de619fd5-e5dd-4c4a-9303-c6763b90eaef），附上已经核好的事实（资金、分账表、lien 依据、地址），再引用 Klaus 原话。本 session 只负责分流和起草回复。
