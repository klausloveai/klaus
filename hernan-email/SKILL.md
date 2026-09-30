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

选错型比写得不好更糟：拿 A 去回任务清单，他得自己把我的散文跟他的编号对着读。

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

Claude 自己的备注（查不到的、要 Klaus 拍板的）改用**蓝字**，并以标记开头：

```html
<p><span style="color:#1155CC">【Claude 备注 — 发送前删除】原信写 5:19 p.m.，但 17:19:37
是送达签收时间，与起诉状 ¶12 的 1:14:57 p.m. 不符 —— 要不要提，你定。</span></p>
```

规则不变：**蓝字必须可整段删除，删完黑字＋红字仍通顺**，不要塞进句子中间。
Klaus 删光蓝字 = 一封干净可发的信。

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

1. **开头一句注明颜色含义**，原话：`Below is where each of your <N> items stands.
   (Blue is confirm, yellow is pending, red is question.)` —— `<N>` 用英文数词（four / six）。
2. **三色，实现方式各不相同**（照他 9/28、9/29 两封发出稿）：

   | 色 | 含义 | markup |
   |---|---|---|
   | 蓝 | confirm 已完成 | `<font color="#0000ff">` **字色** |
   | 黄 | pending 未落定 | `<span style="background-color:rgb(255,255,0)">` **底色高亮**，纯黄 |
   | 红 | question 我在问他 | `<font color="#ff0000">` **字色** |

   蓝红是字色、只有黄是高亮，别统一。看到脏色（粘贴带进来的 `rgb(255,217,102)` 之类）
   **改成对的色，不要退回无色**。
3. **每一项各自一个 `<p>`**，不要 `<br>` 连排成一段 —— Klaus 两次改过这个（"换行 in between"）。
4. **编号严格用他的编号**，一项一句。他一条里含两问（`… and whether she ever …`）就答两句，
   仍归在他那个号下。
5. **没有结尾句。** 最后一项写完直接接签名 —— Klaus 把我写的
   `Let me know if you need anything else.` 删了。（那句属于 C 型纯确认回信，不属于这里。）
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
7. **Cc**：他原信若抄送了所内多人，回信**只保留 Cassie + Joe**（诉讼线固定二人），
   Cindy / Claire 去掉。他原信只发给我一人 → 回信也不加 Cc（见下一节）。
8. 收尾签名一律从 `gws gmail users settings sendAs get` 取，**绝不手打、绝不从旧邮件抽**
   （见 [[gmail-signature-source]]）。
9. 他打招呼用 **`Hi Hernan,`**（不带重音）。

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
