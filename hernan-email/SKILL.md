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
  POE workflow · LOR → `lor-send` / `draft-lor` · fax → `send-fax` · demand → `draft-demand`
- Discovery (FROG/SROG/POS/apportionment) → [[litigation-discovery-support]]
- **New / first-time task → flag it: `🆕 首次任务 — 建议跑完做成模版/skill`.** This is Klaus's
  standing rule ("做过一次反复出现的都做成模版和 Automation") and the engine of goal ②
  (learn → systematize → scale). Say what the template would cover.

## Step 4 — Draft the reply

### 结构：引用—作答（Klaus 2026-08-14 定为**所有**回 Hernán 邮件的标准格式）

他的信常有 8–12 项编号交办，每项一大段。Klaus 要的是**他扫一眼就知道每段在答哪一句**，
不用回头翻自己的信。所以每一项写成三层：

```html
<p><b>1. Confirm the preservation letter to Benjamin Velazquez Lopez was actually mailed. This is the most urgent item.</b></p>
<p style="margin:4px 0 8px 28px;color:#666666;font-style:italic;">“Please confirm with Claire today, tell me the exact date it was mailed and the address used…”</p>
<p>Mailed. <span style="color:#CC0000">[Klaus: fill in the exact date, address and certified mail number from Claire.]</span></p>
```

1. **标题 = 他那一项的原句**，一字不改（`1. Confirm the preservation letter…`）。他没编号的
   段落（`Item 1:` / `Calendaring.` / `Appointments.`）就用他自己的那个词做标题。
2. **灰色斜体缩进引他那一项里最硬的一句**（`#666666` + italic + `margin-left:28px`）——
   **只引一句**，挑要求最具体、将来会拿来对账的那句。引多了信就臃肿。
3. **回复接在下面**，一两段，直给。

**顺序严格照他的**，不合并、不重排、不跳项——哪怕某项只能答「still open」也要出现，
漏掉一项他会以为我们没看见。

### 🔴 红字 = 写给 Klaus 自己的，不是写给 Hernán 的
凡是**我查不到、或需要 Klaus 拍板**的，就地插一段
`<span style="color:#CC0000">[Klaus: …]</span>`，写清**他要填什么或要决定什么**。
规则同 [[hourly-email-agent]]：**红字必须可整段删除，删完黑字仍通顺**。
Klaus 删光红字 = 一封干净可发的信。别把红字塞进黑字句子中间。

### 语气（在上述结构之内）
[[hernan-email-tone]] 的 4-beat 仍然适用，但**压到最短**：具体的一句谢 → 逐项作答 →
**一个想法或一个问题**（分享经验后 *"That said… I'll follow your lead"*，或问
*"the reason behind"*）——这条别省，是学习点 → 认领下一步。
放在开头一句和结尾一句即可，不要每一项都来一遍。

Never dry (`"I will work on it."`); never pure apology → extract the lesson instead.
Open `Hi Hernán,`, close `Best,` + Klaus's preset signature (fetch via
`gws gmail users settings sendAs get`, per [[feedback-email-signature-sender]]).
**Reply All**，收件人照他原信的分发（通常 Cc cassie / cindy.z / claire.f / joe），
并回在**线程里最新那封**上，不要回到更早的一封。

## Step 5 — Deliver

Show Klaus: 中文摘要 + 任务清单(标好路由/🆕)+ the drafted reply in a copy-paste block.

## Guardrails
- **DRAFT ONLY — never send.** Klaus sends every outbound email himself ([[hernan-email-tone]]).
- **No fabrication.** Don't invent deadlines, case facts, or what he "meant" — quote him.
- Any document drafted off the back of this passes [[draft-check-skill]] first (litigation
  docs: Klaus's `626-479-2207` as **both** phone and fax).
- Klaus stays in the paralegal/CM lane — never draft him overruling the attorney.
