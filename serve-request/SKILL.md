---
name: serve-request
description: >
  THE entry point for "Hernán sent signed documents to serve" at 凌图律所 / Law Office of
  Shenqi Cai APC. **Trigger it whenever Hernán Simó emails signed discovery or pleadings with
  instructions to fill in the proof of service, serve them, calendar the response deadline and
  file them** — his standing email shape is "Please find attached, for the case of <Client>,
  Plaintiff's written discovery, Set One, to Defendants X and Y … Please complete the following
  tasks: 1) Fill in the service date … 2) Serve … 3) Sign each proof of service and save …
  4) Calendar the response deadline." Also on: "/serve-request", "送达这批", "serve discovery",
  "e-serve these", "帮我送达", "这批文书要送出去", or Klaus forwarding such an email with no
  instruction. It orchestrates the whole chain in one pass — label the thread with the case's Gmail label → decide the POS branch → fill or
  append the POS → client folder in Downloads → Gmail DRAFT per defendant (**HARD GATE: stop
  and wait for "发"**) → send → verify the sent attachments → calendar 30 days + 2 court days
  and invite Hernán + Cassie → archive the served copies to the Drive case folder → star the
  sent threads ORANGE_CIRCLE → draft the numbered status reply to Hernán (**also draft-only**)
  → Activity Log + dashboard. POS mechanics live in `add-pos`; reply format lives in
  `hernan-email`; **this skill owns the ORDER, the two STOP gates, and the verification.**
  Serves goal ② (litigation with Hernán → do it right → systematize → scale).
---

# serve-request — 从 Hernán 交件到收尾，一条龙

Hernán 这类信的形状是固定的：**签好的文书 + 四条任务**（填 POS 日期 / 送达 / 签 POS 并归档 /
记期限）。2026-09-29 Bo Tao v. Beas 那次，前半段 `add-pos` 做了，后半段五步是 Klaus 一条条口述
才做的 —— 这个 skill 把整条链固化成 11 步，让它不用再口述第二次。

**他的四条任务 → 这 11 步的对应：**

| Hernán 说的 | 这里 |
|---|---|
| Fill in the service date on each proof of service | Step 1–2 |
| Serve all documents by email on the same day | Step 4（草稿）→ Step 5（发） |
| Sign each proof of service and save the served copies | Step 2 签 · Step 8 归档 |
| Calendar the response deadline | Step 7 |

Step 0、3、6、9、10 是他没说但每次都要做的：打 case label、客户文件夹、核对发出去的件、
回他的信、打星 + 台账 + dashboard。

**两个 STOP gate，其余自动：**
- **Gate 1（第 4 步）** —— 送达邮件永远只是 Gmail 草稿，Klaus 说 "发" 才发。
- **Gate 2（第 9 步）** —— 给 Hernán 的回信也只是草稿，Klaus 自己发。

其余八步在 gate 之间自动跑完，不要逐步征求同意。

---

## Step 0 — 这封邮件打上 case label 了吗？没有就打

每案一个 Gmail label（[[feedback-case-label-one-per-case]]）。Hernán 交件的信是这个案子
往后三个月最常被回头搜的一封 —— **先贴标签，再动文书**。

```bash
# 1) 这条 thread 现在有哪些 label
gws gmail users threads get --params '{"userId":"me","id":"<THREAD_ID>","format":"minimal"}'

# 2) 全部 label 里找这个案子的（name 通常就是客户名）
gws gmail users labels list --params '{"userId":"me"}'

# 3) 没有就建；已有就跳过建这一步
gws gmail users labels create --params '{"userId":"me"}' \
  --json '{"name":"<Client Name>","labelListVisibility":"labelShow","messageListVisibility":"show"}'

# 4) 贴到整条 thread 上（★ thread 级，不要 messages.modify）
gws gmail users threads modify --params '{"userId":"me","id":"<THREAD_ID>"}' \
  --json '{"addLabelIds":["<LABEL_ID>"]}'
```

⚠️ **labelIds 是 `Label_xxxxxxxx` 这种不透明 id，不是 label 名字** —— 必须先 `labels list`
换成 id 再用。第 10 步给送达邮件打星时同理，也顺手把 case label 贴到那两条 sent thread 上。

⚠️ **别新建重名 label。** 先在 `labels list` 里按客户名搜一遍；同一个案子出现两个 label
比没有 label 更难搜。查到名字不完全一致（`Yi Cong` vs `Yi Cong - Camden`）就**用已有那个**，
不要自作主张改名。

---

## Step 1 — 先分型：文书里已经有 POS 了吗？

这一步决定后面所有事，先做，不要跳。

```bash
cd ~/Downloads/"<Client Name>"
for f in *.pdf; do
  n=$(pdfinfo "$f" | awk '/^Pages/{print $2}')
  pos=$(pdftotext -layout "$f" - | grep -ciE "proof of (electronic )?service")
  blank=$(pdftotext -layout "$f" - | grep -cE "_{6,}")
  printf "%-64s %3sp  POS:%-3s blanks:%s\n" "${f:0:62}" "$n" "$pos" "$blank"
done
```

⚠️ grep 必须写成 `proof of (electronic )?service` —— 只搜 `proof of service` 会把标题是
**PROOF OF ELECTRONIC SERVICE** 的那份漏掉，报成"没有 POS"（2026-09-29 踩过）。

| 结果 | 走哪条 |
|---|---|
| `POS:≥1` 且有下划线空格 → **律师自己写的 POS，留了空** | **A. 就地填**，绝不另附模版 |
| `POS:0` | **B. 拉 Drive 模版，每份文书尾部各接一份** |

**A 优先。** 律师自己写的 POS 常带通用模版没有的案件专属 recital，替换掉是降级。例如
Yi Cong 2026-09-28 那八份：

> …pursuant to the **Notice of E-Service** served by Defendants Camden Landmark, LLC and
> Camden Development, Inc. on **September 24, 2026**, and pursuant to the **Consent to
> Electronic Service and Notice of Electronic Service Address** served by Defendant Rhea
> Edpao on **August 31, 2026**…

另外：混合情况（部分有、部分没有）按**每份文书各自**判断，不要一刀切。

---

## Step 2 — 填 / 加 POS

**A. 就地填**（文书自带 POS）：

```bash
python3 ~/.claude/skills/add-pos/scripts/fill_inplace_pos.py \
  ~/Downloads/"<Client Name>" <signed pdf> [<signed pdf> ...]
```

填两处日期（= 送达日 = 今天）、declarant 姓名，并把 Klaus 的签名盖在签名横线上。
**律师自己的签名和日期一律不动** —— 他签的是文书，我签的是 POS。

**B. 模版**（文书没有 POS）：完整做法见 `add-pos` SKILL.md，要点：

- 从 Drive 拉 `Proof of Service - TEMPLATE (fillable, highlighted).docx`
  （id `1yHMojbfNpE_C6aeZ30Td7qXypwLp0sok`），**绝不本地重建**
- **每份文书尾部各接一份 POS**，页码接续正文（start = 该文书页数 + 1），页脚换成该文书自己的
  caption 标题 —— Klaus 原话「主要不要重叠页码」
- Hernán 若另给了**一份独立 POS 涵盖全部文书**，这时它不再送达（会重复）。
  在第 9 步的回信里**以红字项**提一句，由 Klaus 决定留删
- Judicial Council 表格（DISC-001 等）：**绝不在表格页面上盖任何东西**，但在后面接 POS 页是对的，
  表格自带的 `Page 8 of 8` 保持原样，POS 从 9 接下去，不会重号

**Service list 取自已立案的 Answer 的 caption block，不取对方邮件签名档。**
2026-09-29 Bo Tao：签名档只给 `Christine Hanna, Esq.` + 手机 (818) 966-5390；
Answer 上是 **SBN 349900** + **(213) 615-2500**。Answer 同时证明被告确已 appeared
（POS 勾选项 "represented by counsel and has appeared" 的前提）。
对方签名档里"la.legal@ is our designated email"是**每封都有的固定文字**，不是事件 —— 别拿某封
邮件的日期当"指定日"。

---

## Step 3 — 客户文件夹

输出一律进 `~/Downloads/<Client Name>/`，不散在 Downloads 里。
附件名里若带真换行符（`Camden Development^J Inc.pdf`），**在这一步就改成正常名字**，
别带到对外邮件上。

---

## Step 4 — 建 Gmail 草稿 🛑 GATE 1

### 一名被告一封邮件

不同被告收到不同附件 → **分开发**，即使两名被告共用同一律师、同一送达地址。
每封的主题点名该被告。（Bo Tao：两封都发到同一个 `la.legal@farmersinsurance.com`，
一封 Rachel R. Beas、一封 Becky Beas。）

**例外：他明确要求一封发全部时，问 Klaus 一句再定** —— 别自己替他选。

### 同日送达约束

若 FROG 17.1 引用了同批的 RFA（Hernán 会在信里点明），**那一被告的四份必须同一天送出**。
分两天送会给对方拿捏的口实。

### 收件人

**只发给 POS 里列的送达地址。** 对方的"correspondence only"邮箱可以放 Cc 作礼貌，
**绝不写进 POS 的 Service List**。Hernán 通常要求抄送他自己。

### 正文 —— 三块，别的都不要

```
Dear Counsel,

Please find attached, for service on Defendant <Name>, Plaintiff's written discovery, Set One:

1. Plaintiff <CLIENT>'s Form Interrogatories—General (Judicial Council form DISC-001), Set One, to Defendant <NAME>;
2. ... ;
3. ... ; and
4. ... .

Kindly confirm receipt, thank you,

<the real Gmail signature>
```

HTML 形状：`<p>greeting</p><p>lead-in</p><ol><li>…</li></ol><p>closing</p>` + 签名。
清单是真 `<ol>`，标点 `;` … `; and` … `.`

**删掉、且永远保持删掉的：**
- ❌ "A Proof of Electronic Service is attached to the end of each document." —— POS 就绑在附件里，
  说一遍是在告诉对方他们自己看得见的东西
- ❌ 指定送达地址的出处、引用 Answer 日期之类的**法律陈述** —— POS 自己做 §1010.6 的活，
  正文重复一遍只是多一句可能写错的话
- ❌ 单独一行 `Thank you,` —— 并进 `Kindly confirm receipt, thank you,`

**签名从 `gws gmail users settings sendAs get` 取，绝不手打、绝不从旧邮件抽 HTML。**
`build_pos.py` 的 `gmail_signature()` 已经这么做了。

### 🛑 停

把草稿（收件人 / 抄送 / 主题 / 正文 / 附件清单）摆给 Klaus，**等他说"发"**。
不要顺手发，不要"我先发了再说"。

---

## Step 5 — 发送（Klaus 放行后）

```bash
gws gmail users drafts send --params '{"userId":"me","id":"<DRAFT_ID>"}'
```

---

## Step 6 — 核对**实际发出去的**附件

从 Sent 里把附件**下载回来**验，不要验本地副本 —— 本地对不代表发出去的对。

```bash
# 逐份检查：POS 份数 / 两处日期 / 签名图 / 勾选框 / 服务清单 / 页码接续
for f in *.pdf; do
  n=$(pdfinfo "$f" | awk '/^Pages/{print $2}'); t=$(pdftotext -layout "$f" -)
  printf "%-56s %3sp POS:%s date:%s/%s sig:%s\n" "${f:0:54}" "$n" \
    "$(echo "$t"|grep -ciE 'proof of (electronic )?service')" \
    "$(echo "$t"|grep -c "On $(date '+%B %-d, %Y'), I served")" \
    "$(echo "$t"|grep -c "Executed on $(date '+%B %-d, %Y')")" \
    "$(pdfimages -list -f $((n-2)) -l $n "$f" 2>/dev/null | tail -n +3 | wc -l|tr -d ' ')"
done
```

⚠️ 用正则抓页码会抓到 pleading 的**行号**（1–28），看着像 MISMATCH 其实没错。
拿不准就 `pdftoppm` 渲染那几页用眼睛看一次。

---

## Step 7 — 日历期限，invite Hernán + Cassie

**我方送达的 discovery：送达日 + 30 天 + 2 court days**（CCP §1010.6(a)(4)(B)，电子送达）。
遇周末 / 法定假日顺延，顺延了要在报告里点出来。

标题：`<Case>: <被告> — Discovery Responses Due (Set One)`
描述里写清：送达了什么、送到哪个地址、逾期后果、归档位置。逾期后果照抄这三条 ——
objections waived（CCP §§2030.290 / 2031.300）、RFA 可动议 deemed admitted（§2033.280）、
先 meet and confer。

```bash
gws calendar events insert --params '{"calendarId":"primary","sendUpdates":"all"}' \
  --json '{"summary":"...","description":"...","start":{"date":"YYYY-MM-DD"},"end":{"date":"YYYY-MM-DD"},
           "attendees":[{"email":"hernan.s@lingtulaw.com"},{"email":"cassie@lingtulaw.com"}],
           "reminders":{"useDefault":false,"overrides":[{"method":"popup","minutes":1440}]}}'
```

多名被告同日送达 → 期限相同，**一条日历写全**即可，别开两条。

---

## Step 8 — 归档进 Drive case folder

我方送出的 discovery 进 `<Case folder> / 4. Litigation / 4.5 Discovery - To Defense`
（对方送来的在 `4.4 Discovery - From Defense`，别放错方向）。

命名对齐该 case folder 里**已有**的语法，别自己发明。Bo Tao 实例：

```
9-29-2026 Form Interrogatories-General Set 1(to Rachel R. Beas) - with POS.pdf
9-29-2026 Special Interrogatories Set 1(to Rachel R. Beas) - with POS.pdf
```

⚠️ `gws drive files create --upload` **必须 `cd` 进目录用 basename**，绝对路径会失败。

---

## Step 9 — 回 Hernán 原任务邮件 🛑 GATE 2

**先 `Skill(hernan-email)`,按里面的 B 型（编号状态回复）写，不要凭记忆。** 要点：

- 回在**他那封原任务邮件**的 thread 上，不是另起一封
- 开头一句注明颜色：`Below is where each of your <N> items stands.
  (Blue is confirm, yellow is pending, red is question.)`
- **严格照他的编号**，一项一句，**每项各自一个 `<p>`**
- 三色实现不同：蓝 `<font color="#0000ff">` 字色 · 黄 `background-color:rgb(255,255,0)` 高亮 ·
  红 `<font color="#ff0000">` 字色
- **没有结尾句**，最后一项写完直接接签名
- Cc：他原信抄送所内多人 → 只保留 **Cassie + Joe**；只发给 Klaus 一人 → 不加 Cc
- 打招呼 `Hi Hernan,`（不带重音）

**红字 = 提议层，宁可多给。** 凡是 Hernán 能答的问题就写出来（例如"你那份独立 POS 这次没用上，
以后要不要改回合并式"），**去留交给 Klaus**。他删掉要 1 秒；我不写他根本不知道有这个选项。
形式硬要求：红字独立成段，整条删掉后全文仍通顺。

### 🛑 停 —— 回信也是草稿，Klaus 自己发。

---

## Step 10 — 打星 + Activity Log + Dashboard

**打星**（送达那几条 sent thread）：`ORANGE_CIRCLE` 🟠⭕ = 等外部回音、到期要催。
Klaus 自己去挂 snooze。**一切走 `threads.modify`，且重标前先清掉全部 12 个 superstar**
（见 [[gmail-star-status-convention]]）。

**Activity Log**（只 append，永不改写既有行）：

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA","range":"Activity Log!A:J","valueInputOption":"USER_ENTERED","insertDataOption":"INSERT_ROWS"}' \
  --json '{"values":[["MM/DD/YYYY","HH:MM","<Case>","起草","<送达了什么、给谁、怎么送>","Klaus","<Ref/ID>","Local","manual:<slug>","<Next Step>"]]}'
```

`Ref/ID` 必须抓全：**案号 + 每封送达邮件的 gmail message id + 日历 event id**。
`Next Step` 写答复到期日和逾期后果。

**Dashboard**：

```bash
cd ~/lingtu-cms && ./.venv/bin/python sync/scan_litigation.py <case_id>   # 整数 id，不是 Drive id
./.venv/bin/python board/export.py
cd board && ../.venv/bin/python build.py                                   # 必须在 board/ 里跑
```

然后把 `~/lingtu-cms/board/picase-board.html` 发布到固定 URL
`https://claude.ai/artifact/FnTCxBaNVDHbDVgaN9jcxg`（发布前先 `action:"read"` 读一次）。
case_id 在 `board/data.json` 里查，别猜。

---

## 交付给 Klaus

一次报完，别逐步汇报。按这 11 步给状态，**✅ 已完成 / ⚠️ 等你决定 / 🛑 卡在 gate**。
⚠️ 项必须 self-contained —— 他不该为了看懂而回翻上文。

## Guardrails

- **两个 gate 都是硬的**：送达邮件和给 Hernán 的回信都只是草稿，Klaus 说发才发。
- **绝不编造**：日期、地址、SBN、编号一律从文书或 Drive 核实，查不到就标出来问。
- **对方律师信息以已立案文书为准**，邮件签名档只作参考。
- 附件对外**不带内部版本标签**（`VERSION A` 之类），收件人只该看到文书本身的名字。
- Klaus 始终在 paralegal / CM 的位置上 —— 绝不起草他推翻律师判断的话。
- 相关：`add-pos`（POS 机制细节）· `hernan-email`（回信格式）·
  `discovery-response`（反方向：我方答复）· `discovery-translation-zh`（客户核对中译本）
