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

Use the **4-beat recipe in [[hernan-email-tone]]** — read it, don't improvise:
1. Specific thanks (name the thing) · 2. Answer his list **1:1 in his order**, CAPS labels,
short · 3. **A thought or a question** (share experience → *"That said… I'll follow your
lead"*, or ask *"the reason behind"*) — never skip · 4. Claim next step + invite correction.

Never dry (`"I will work on it."`); never pure apology → extract the lesson instead.
Open `Hi Hernán,`, close `Best,` + Klaus's preset signature (fetch via
`gws gmail users settings sendAs get`, per [[feedback-email-signature-sender]]).

## Step 5 — Deliver

Show Klaus: 中文摘要 + 任务清单(标好路由/🆕)+ the drafted reply in a copy-paste block.

## Guardrails
- **DRAFT ONLY — never send.** Klaus sends every outbound email himself ([[hernan-email-tone]]).
- **No fabrication.** Don't invent deadlines, case facts, or what he "meant" — quote him.
- Any document drafted off the back of this passes [[draft-check-skill]] first (litigation
  docs: Klaus's `626-479-2207` as **both** phone and fax).
- Klaus stays in the paralegal/CM lane — never draft him overruling the attorney.
