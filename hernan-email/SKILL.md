---
name: hernan-email
description: >-
  Handle an email from attorney Hernán Simó end-to-end for Klaus: pull the latest thread
  from klaus@, produce a 中文 summary + numbered task breakdown (key legal wording kept in
  English), route each task to an existing skill/template (or flag it as first-time →
  template candidate), and draft the reply in Hernán's calibrated tone. Trigger on:
  "/hernan", "回 Hernán", "Hernán 的邮件", "处理 Hernán 邮件", "Hernán email", "翻译一下
  Hernán 这封", or when Klaus pastes/forwards a Hernán email. DRAFT-ONLY — Klaus sends every
  outbound email himself. Serves goal ② (litigation with Hernán → learn → systematize → scale).
---

# hernan-email — 处理 Hernán 的邮件 (understand → break down → route → draft reply)

Kills three manual steps Klaus does every time: copy-paste → translate → figure out the
tasks → hand-write the reply.

## Step 1 — Pull his latest email (no copy-paste needed)

Klaus's own account is the default `gws` config. Search klaus@:

```bash
gws gmail users messages list --params '{"userId":"me","q":"from:hernan.s@lingtulaw.com OR to:hernan.s@lingtulaw.com","maxResults":20}' --format json
gws gmail users messages get --params '{"userId":"me","id":"<MSG_ID>","format":"full"}' --format json
```

**GOTCHA (cost me a false "0 emails"):** `gws` prints `Using keyring backend: keyring` —
sometimes *after* the JSON. `json.loads(s[s.index('{'):])` then dies with "Extra data". Use
`json.JSONDecoder().raw_decode(...)` to parse only the first object. Body text is
base64url in `payload.parts[*].body.data` (mimeType `text/plain`); strip quoted history by
splitting on `\nOn .* wrote:` / `\nFrom: `.

If Klaus pastes the email instead, skip to Step 2.

## Step 2 — 中文摘要 + 任务拆解

Output, in this order:
1. **一句话中文摘要** — what he wants, overall.
2. **编号任务清单(中文)** — one line per task, with the **deadline** if any (he calendars
   things: e.g. Homeland/Amazon 90-day Proof of Loss; the Aug 30 2026 arbitration).
3. **关键法律措辞保留英文原文** — quote his exact English for anything legal/strategic
   (cause of action names, statutes, procedural terms). **Never let translation lose the
   original** — Klaus reads the English when it matters, so keep it beside the Chinese.
4. **他讲的 why** — he always explains reasoning; surface it, it's the teaching content
   Klaus is here to learn.

## Step 3 — Route each task

For every task, check whether Klaus already has a tool:
- 立案/filing package → `dogbite-file-complaint` · 送达 POS → `add-pos` · POE → the dog-bite
  POE workflow · LOR → `send-lor` / `draft-lor` · fax → `send-fax` · demand → `draft-demand`
- Discovery (FROG/SROG/POS/apportionment) → [[litigation-discovery-support]]
- **New / first-time task → flag it: `🆕 首次任务 — 建议跑完做成模版/skill`.** This is Klaus's
  standing rule ("做过一次反复出现的都做成模版和 Automation") and the engine of goal ②
  (learn → systematize → scale). Say what the template would cover.

## Step 4 — Draft the reply

### 先选型：他发来的是什么，决定回信是哪一种

| 他发来的 | 回哪一种 | 写在 |
|---|---|---|
| **提问 / 要分析、要事实** | **A. 引用—作答**（黑字照抄原文 + 红字答案） | 下一节 |
| **编号任务清单，我照做了** | **B. 编号状态回复**（三色，逐条对应） | 下下节 |
| **一条指示，做完了** | **C. 纯确认**（两句，只说这一件事） | [[feedback-email-reply-one-liner]] |
| **他没开口 —— 我备好文书请他签** | **D. 交件送签**（编号、全黑、附凭证、收尾时间线） | D 节 |

选错型比写得不好更糟：拿 A 去回任务清单，他得自己把我的散文跟他的编号对着读。

⚠️ **范围 = Klaus 指的那一封，不并其他信的事项**（Klaus 2026-10-19，Chunpeng Wu 当场纠正）。
他说「回复 Hernán 的更新」并截图了 10/19 那封的 `Tasks for you: 1–4`，我却把 10/15 的五项和
10/12 的误工问题一起并进了一封长信 —— 他回：**「你搞错了，我要你回的是这段」**，然后自己发了一句：
`Hi Hernán, 1-4 completed, and waiting client's response.`

两条规则：
1. **只回他指的那封信的编号。** 其他信里悬着的事项另开一封、回在它自己的 thread 上，
   或者在 chat 里提醒 Klaus 还有哪些没回 —— 不要自作主张合并。
2. **他列的每一项都已做完或都在等别人 → 走 C 型一句话**，像上面那句。
   B 型的逐条三色只用在**有实质内容要逐条交代**的时候（凭证号、日期、要他拍板的选择）。
   "已办 / 在等客户"不是实质内容，不值得展开成七段。

⚠️ **每一项默认一到两句**（Klaus 2026-10-19 再次强调：「draft 回复的时候 keep it simple，
不要说那么多复杂的内容，就是一句话两句话」）。同一封 Chunpeng Wu 回信，他把我每项三四句的版本
压成每项一两句；第 3 项只要「我按你的意思改了，附上，你看行不行，然后转给 Cassie」——
**不复述改了哪几个字、不解释改动的法律效果**，附件里他自己看得到。

---


### A. 引用—作答 —— 他提问、我作答（Klaus 2026-08-17 亲手改定，取代 08-14 版）

他的信常有 8–12 项编号交办，每项一大段。Klaus 要的是**他扫一眼就知道每段在答哪一句**，
不用回头翻自己的信。所以每一项写成**两层**：

```html
<!-- 1) 他那一项的原文，一字不改，黑字整段加粗 -->
<p><b>First, please pull the tracking record for the duplicate letter we sent the same day,
July 20, 2026, to GOFO's registered agent, Corporate Creations Network Inc., at 7801 Folsom
Blvd, Sacramento, California 95826, and confirm whether that copy was delivered and signed
for.</b></p>

<!-- 2) 答案紧接在下面，红字 = 要发出去的答案 -->
<p><span style="color:#ff0000">The registered-agent copy went out under certified mail number
<b>9589 0710 5270 2931 6710 42</b>, postmarked Bassett, CA 91746 on July 21, 2026. The Chino
copy that came back is <b>9589 0710 5270 2931 6710 35</b>, postmarked the same day.</span></p>
```

1. **黑字 = 他那一项的原文，整段照抄一字不改。** 他用编号或散文段落（`First, …` /
   `Second, …`）就整段 `<b>` 加粗；他用带标签的小节（`Amazon Logistics:` /
   `Public Records Act requests:`）就只把标签 `<u>` 下划线、正文不加粗。
   黑字用 Times New Roman 12pt。
2. **红字 = 答案**，紧接在黑字下面，Arial small。**答案要短** —— 能一句就一句：
   `Done.` / `Yes, attached for your review.` / 只给硬事实与编号（certified #、order #、
   日期，编号在红字里再 `<b>` 一次）。见 [[feedback_drafts_keep_simple]]。
3. **某项还没有答案 → 只留黑字原文，下面空着。** 让它显眼地悬着，不要写废话填充，
   也不要为了"每项都有回复"而编。

**顺序严格照他的**，不合并、不重排、不跳项 —— 漏掉一项他会以为我们没看见。

**不再使用**旧版的「灰色斜体缩进引最硬的一句」—— 改成整段照抄原文。

### 🔴 红字语义已反转（务必看清）

**回 Hernán 时，红字 = 要发给他的答案**，不是给 Klaus 的备注。这与
[[hourly-email-agent]] 的通用红字规则相反，Hernán 这条线以本节为准。

**草稿里不放任何给 Klaus 的备注，也不能有一个中文字。**（Klaus 2026-10-19 Gaoyang Qin，
取代此前的「蓝字【Claude 备注 — 发送前删除】」做法：「为什么还有中文？它不应该出现中文…
你缺什么信息，先告诉我呀，然后我提供给你」。）
- 查不到的事实 → **起草前先在 chat 里问 Klaus**，拿到再写。
- 已经起草、仍有个别空格 → 草稿里只留英文占位 `[DATE]` / `[CERTIFIED NO.]`，亮黄高亮
  （见 [[feedback-highlight-missing-fields]]），解释放在 chat 里。
- 建草稿前对 HTML 正文跑一遍 CJK 扫描，有中文字就不建。

### B. 编号状态回复 —— 他给任务清单、我报进度（Klaus 2026-09-29 定稿，Bo Tao）

他常一封信给 4–8 条编号任务。做完之后**照他的编号逐条回**，每条一句，上色。
这是 Klaus 亲手发出的版本，逐字照抄结构：

```html
<div dir="ltr">
<p>Hi Hernan,</p>
<p>Below is where each of your four items stands. (Blue is confirm, yellow is pending, red is question.)</p>
<p><font color="#0000ff">1. The Proof of Electronic Service is completed and signed.</font></p>
<p><font color="#0000ff">2. Both sets were e-served on September 29, 2026 to la.legal@farmersinsurance.com, with a copy to Christine Hanna, and you are copied on both.</font></p>
<p><font color="#0000ff">3. Defendants&rsquo; responses are calendared for November 2, 2026, which is thirty (30) days plus two (2) court days from the date of service. You and Cassie have the invitation.</font></p>
<p><font color="#0000ff">4. The served documents are saved in the case folder under 4. Litigation &gt; 4.5 Discovery - To Defense.</font></p>
<!-- 签名紧接在最后一项后面 -->
</div>
```

**硬规则：**

1. **不写颜色说明那一行。**（Klaus 2026-10-14 当场删除，取代此前规则。）
   过去的写法是开头加一句 `Below is where each of your <N> items stands.
   (Blue is confirm, yellow is pending, red is question.)` —— **不要再写了**，
   `Hi Hernan,` 之后直接进第 1 项。

   **为什么取消**：这句话是个持续出问题的可删层引用。2026-09-29 Yi Cong 我写成
   `…, with one point at the end.`，Klaus 删了末尾那条红字，于是它空指；
   2026-10-12 Lina Lu 我给了两条红字，Klaus 两条都删，`red is question` 留在信里，
   发出去的版本承诺了一个不存在的颜色。颜色本身不需要解释 —— 取消这行，
   整类错误随之消失。

   **三色照用不变**（见下条）。编号、分段、无结尾句也都不变。

2. **三色，实现方式各不相同**（照他 9/28、9/29 两封发出稿）：

   | 色 | 含义 | markup |
   |---|---|---|
   | 蓝 | confirm 已完成 | `<font color="#0000ff">` **字色** |
   | 黄 | pending 未落定 | `<span style="background-color:#fff2cc">` **底色高亮**，柔黄 |
   | 红 | question 我在问他 | `<font color="#ff0000">` **字色** |

   蓝红是字色、只有黄是高亮，别统一。

   ⚠️ **黄色是 `#fff2cc`（Gmail 调色盘最浅的那一格黄），不是纯黄 `#ffff00`。**
   Klaus 2026-09-30 亲手改的：整段高亮用纯黄太刺眼，一封信里三四条 pending 会盖过蓝字。
   看到脏色（粘贴带进来的 `rgb(255,217,102)`、或旧稿的纯黄）**改成 `#fff2cc`，不要退回无色**。
3. **每一项各自一个 `<p>`**，不要 `<br>` 连排成一段 —— Klaus 两次改过这个（"换行 in between"）。
4. **编号严格用他的编号**，一项一句。他一条里含两问（`… and whether she ever …`）就答两句，
   仍归在他那个号下。
5. **没有结尾句。** 最后一项写完直接接签名 —— Klaus 把我写的
   `Let me know if you need anything else.` 删了。（那句属于 C 型纯确认回信，不属于这里。）

   ⚠️ **"简单一点" ≠ 丢掉编号和颜色。** 2026-09-29 Yi Cong,Klaus 说我那版七条太长，我改成
   四段散文 —— 他回：**「改短的是对的，1、2、3、蓝色 confirm rules」**。
   **编号和三色是固定骨架，压缩的是每条的字数，不是结构。** 三条也要编号、也要上色、
   也要留颜色说明那一行。散文段落只用在 C 型纯确认（一件事、两句话、无清单）。

   条目数可以少于他的任务数 —— 把同类合并成一条（例如"SOD 已附 + production 在链接"合成一条），
   但**合并后仍然是编号项**。
6. **红字 = 提议层，宁可多给，不要少给。** 2026-09-29 我在 Bo Tao 那封里加了一条红字
   （我改成一被告一封邮件、每份文书各绑 POS、没用他那份独立 POS，问他要不要改回去），
   Klaus 删掉了 —— 但他当场说明：**"我删红字是因为我觉得没必要，但是你给我提供更多选择是好的，
   我会决定是否删掉"**。所以判据不是"他会不会想要"，而是**这条是不是 Hernán 能答的问题**。
   是 → 写出来，由 Klaus 决定去留。**我替他预判而不写，他连删的机会都没有。**

   代价是不对称的：多写一条他划掉要 1 秒；少写一条他根本不知道有这个选项。

   **但形式必须对 —— 红字独立成一段（或独立一个编号项），整条删掉后剩下的全文仍然通顺。**
   绝不把提议揉进某句话中间，那样他删起来要重写句子。这与
   [[feedback-drafts-keep-simple]]「分析别写进正文」不冲突：那条禁的是**把分析揉进叙述里**，
   红字是可整段摘除的分离层，跟本节蓝字备注同一个机制。

   ⚠️ **口径收紧（Klaus 2026-10-14，Chunpeng Wu）：红字只留「他不拍板就推进不下去」的那种。**
   我给了三条，Klaus 只留一条、删两条：
   - **留下的**：车损照片与 medpay 凭证要不要由他去向 Tesla 索取（我方已在对该保险公司仲裁）。
     —— 不定这件事，谁都不能动手，所以必须问。
   - **删掉的 ①**：问他 causation report 要 Dr. Chiu 还是换医生。**当天我们已经按 Chiu 发信问费用了**，
     问题已被事实回答 —— 变成噪音。
   - **删掉的 ②**：我发现 2/9 病历原句比他引的更有利、且前次事故只涉下背不涉颈椎，
     问他要不要把颈椎腰椎分开论证。**那是在替律师想打法。**

   所以「宁可多给」给的是**选择题**，不是我的观察和建议。判据从"他能不能答"收紧为
   **"不答这条，事情就卡住吗"**。事实发现（例如病历原文比他引的更有利）照样要告诉他，
   但走 chat 跟 Klaus 说，由 Klaus 决定要不要转达 —— 见 [[feedback_drafts_keep_simple]]。

   ⚠️ **送他审阅/签字的文书附 `.docx`，不附 `.pdf`**（Klaus 2026-10-14 当场换掉）。
   理由就一句：他要能直接改。定稿、要签字、或对外送达的那一版才用 PDF。
7. **Cc：他群发给所内多人时，回信只 Cc Cassie + Joe —— 不加 Allison、Cindy、Claire。**
   （Klaus 2026-10-19 Jiayu Ma 明确：「service list 不要加 Allison，也不要 Cindy，也不要 Claire」；
   与 9/29 Bo Tao、10/16 Jiayu Ma demand thread 他亲手裁的结果一致，三次同一结论，定为默认。）
   他只发给我一人 → 不加 Cc。下面是此前的旧口径，仅留作背景：
   ~~**Cc：默认 reply-all 照他的原收件人名单，不要自己裁。**~~
   两次实测不一致 —— Bo Tao（9/29）Klaus 裁到 Cassie + Joe；Yi Cong（同日）**四人全留**
   （Cassie / Cindy / Claire / Joe）。**没有固定规则，要看案子谁在跟。**
   所以照抄他的名单，裁减交给 Klaus —— 跟红字同一个不对称逻辑：多留一个他删掉要 1 秒，
   少留一个就是有人该知道却没收到。他原信只发给我一人 → 回信也不加 Cc（见下一节）。
8. 收尾签名一律从 `gws gmail users settings sendAs get` 取，**绝不手打、绝不从旧邮件抽**
   （见 [[gmail-signature-source]]）。
9. 他打招呼用 **`Hi Hernan,`**（不带重音）。
10. **一个 thread 只回这个 thread 的事 —— 蓝/黄/红三色都一样。**（Klaus 2026-10-19，Jiayu Ma）
    同一个案子常有几条并行 thread（discovery 一条、demand/998 一条、调卷一条）。
    我在 discovery thread 的回信里放了一条红字，问 998 的接受期限是 11/18 还是 11/23
    —— 那是 demand thread 的事，Klaus 当场拿掉，并要求「不是这个 email 的事就不要在这个 email 里问」；
    挂号信已寄出那条也一样，回到 demand thread 去说。
    判据：**这条内容的「出处」在哪条 thread（他在哪封信里交办的、对方文书是在哪封信里送的），就回在哪条。**
    他在 A thread 顺口提到 B 的事，确认可以在 A 里写一句蓝字，但要问的问题和要交的附件仍回 B。
    一次起草两封时，交付时分别报两个草稿号和各自 thread。见 memory `feedback_reply_routing_and_followup.md` ③。

---

### D. 交件送签 —— 我备好文书、请他签字（Klaus 2026-10-01 定稿，Guolin Zhao）

前三型都是**他先开口、我回**。这一型是**我先开口**：文书已经做好，需要他签名/审核，
顺带把他可能会追问的依据一次交代完。Bo Tao / Guolin Zhao 的 CIV 105、SUM-100、CIV-120
一类送签件都走这个形状。

- **Subject**：`<Client> — <文书名> for your signature | Case No. <案号>`
  —— 客户名在前、要他做的动作在中、案号收尾。他按案号归档。
- **颜色：全黑，不上色。** 三色是 B 型「逐条对应他的编号」才用的。这一型没有他的编号可对，
  上色反而制造"哪条要我答"的假信号。真有要他定夺的，就写成一个独立编号项，照样黑字。
- **Cc：固定 Cassie + Joe，不多加。**（Guolin Zhao / Bo Tao / Yi Cong 三次实测一致。）
  2026-10-19 Yi Cong subpoena 那封，我照 Hernán 近期来信的名单加了 Cindy / Claire / Allison，
  Klaus 发前全部删掉，只留 Cassie + Joe。**我先开口的信不抄他的群发名单** —— 那份名单是他回信时的范围，
  不是我主动交件的范围。（上面 B 型「reply-all 照他原名单」只适用于回他的信。）

**骨架（照 Klaus 发出稿的顺序）：**

1. **第 1 项 = 附了什么 + 哪些空白留给谁。** 原话：
   `Attached are the CIV 105 Amendment to Complaint and the Second Amended Summons adding
   DOE 21 as ON GRAND AVE, LLC. The CIV 105 DATE and signature are left for you; the summons
   DATE and Clerk line are left for the court.` —— 他最关心"要我签哪里"，放第一条。
2. **中间各项 = 每一个他可能质疑的判断，各占一条，自足成段。** Guolin Zhao 这封是：
   DOE 号为什么是 21（引 complaint ¶6/¶7 的 Doe 分块）→ 产权记录怎么把 LLC 绑到事发地址
   （录件号 + APN + "Also Known as" 原文）→ SOS 状态与送达代理人 → 实体送达的法条依据
   （CCP §416.10 + Corp. Code §17701.16(b)）。
3. **最后一项 = 这次动作会不会碰坏已经在跑的事，以及为什么不会。** 他这封写的是
   Jorge Velazquez 的 default 仍在法院 review，并说明 §474 加新当事人不重开已 default
   一方的期间。**这一条是自己想到的，不是他问的** —— 价值最高的一条。
4. **收尾时间线**（签名之前）：斜体一行 `Quick timeline update for your reference.`
   然后**倒序**几条「日期 + 一句话」，各自一个 `<p>`：
   `9/28/2026 filed CMC statement.` / `9/22/2026 placed process of service and still attempting.`
   / `9/21/2026 filed request for default for Jorge and still under court review.`

**★ 最硬的一条：凡是正文里作为事实陈述的东西，把原始凭证一起附上。**
Guolin Zhao 这封除了两份待签文书，Klaus 还附了 **SOS Initial Filing (9/1/2023)、
两份 SOI (9/22/2023、9/17/2025)、以及完整 title report (`3827 TR.pdf`, 2.7 MB)** ——
正文第 3、4 项的每一句都有对应附件可查。
**不要只写"我查了 SOS，状态 ACTIVE"就算完**；他要能自己点开核对，而不是回信问我要。
大附件走 `--upload`（见 [[gws-large-attachments]]）。

**不写的东西**：没有结尾句（最后一项或时间线写完直接接签名）、不写 "Let me know if you
need anything else."、不预告"我接下来会…"。签名照旧从 `sendAs` 取。

---

### 语气（在上述结构之内）
[[hernan-email-tone]] 的 4-beat **压到只剩第 1 拍**：开头一句**具体的**致谢，点出那件事本身
（"reading the envelope as confirmation of an active location rather than a bad address is the
part I had backwards"），不要写 "Taking your four items in order." 这种套话。

⚠️ **第 3 拍「一个想法或一个问题」不写进邮件正文。** Klaus 2026-08-17 把我主动指出旧信两处
事实错误的那整段删掉了 —— 分析、建议、风险提示一律**放在 chat 里对 Klaus 说**，由他决定要不要
跟 Hernán 提。见 [[feedback_drafts_keep_simple]]。

Never dry (`"I will work on it."`); never pure apology → extract the lesson instead.
Open `Hi Hernán,`; `Best,` 可有可无（两份范本一份有一份没有），之后接 Klaus's preset signature (fetch via
`gws gmail users settings sendAs get`, per [[feedback-email-signature-sender]]).
**Cc 跟着他的原信走，且要裁剪：**
- 他只发给我一人 → 回信不加任何 Cc（Klaus 2026-08-17 删掉了我自己加的 cassie / claire）。
  ⚠️ **2026-10-19 Chunpeng Wu 反例**：他 10/15 那封只发给 Klaus，我照这条没加 Cc，Klaus 当场要求
  **Cc Cassie + Joe，不要 Cindy、Claire、Allison**（这封附了 retainer 补充协议，Cassie 要看）。
  所以「只发给我一人就不加 Cc」不是铁律：**回信涉及律所层面的事（收费、retainer、要 Cassie 拍板的）
  就抄 Cassie + Joe**；Cindy / Claire / Allison 在 Hernán 线一律不主动加。拿不准就默认 Cassie + Joe，交 Klaus 删。
- 他原信抄送了所内多人 → 回信**只保留 Cassie + Joe**，Cindy / Claire 去掉
  （Klaus 2026-09-29 Bo Tao 那封就是这样裁的）。
- 他在信里明确点名要抄谁 → 照他说的。

绝不无脑 reply-all。回在**线程里最新那封**上，不要回到更早的一封（[[feedback-read-thread-to-end]]）。

## Step 5 — Deliver

Show Klaus: 中文摘要 + 任务清单(标好路由/🆕)+ the drafted reply in a copy-paste block.

## Guardrails
- **DRAFT ONLY — never send.** Klaus sends every outbound email himself ([[hernan-email-tone]]).
- **No fabrication.** Don't invent deadlines, case facts, or what he "meant" — quote him.
- Any document drafted off the back of this passes [[draft-check-skill]] first (litigation
  docs: Klaus's `626-479-2207` as **both** phone and fax).
- Klaus stays in the paralegal/CM lane — never draft him overruling the attorney.
