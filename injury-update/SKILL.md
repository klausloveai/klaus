---
name: injury-update
description: |
  Generate a client-facing 「💉受伤更新」 (Injury Update) WeChat bulletin for 凌图律所 /
  Lingtu Law Office (Law Office of Shenqi Cai APC). Use this skill whenever any of the
  following are mentioned: 受伤更新, 受伤总结, injury update, injury summary, symptom summary,
  "生成受伤更新", "出一个受伤更新", "受伤 bulletin", "/injury-update" for a named client,
  or any request to summarize a PI client's injuries/symptoms into a group message. Typical
  invocation: just a client/driver name (e.g. "给 Baolian Kuang 出一个受伤更新"). The skill
  finds the case in Drive, reads the intake sheet, extracts the ENGLISH injuries/symptoms
  field for the driver and every passenger, translates them into Chinese, fills the fixed
  「受伤更新」 template (one paragraph per client — driver first, then each passenger), and
  outputs the finished, WeChat-ready text (plain text + emoji, no markdown bold). It
  DRAFTS ONLY — it does not send, email, label, or write to any sheet. Always trigger for
  any "make an injury update / 受伤总结" request, even a partial one.
---

# Injury Update — 「💉受伤更新」 client bulletin (generate only)

Produce the fixed 「受伤更新」 WeChat message for a case, with the injuries auto-pulled from
the intake sheet's English fields and translated to Chinese. **Generate only — never send,
email, label, or update any sheet.** Output plain text ready to paste into the case WeChat
group (no markdown `**bold**` — WeChat shows the stars literally).

Follows the firm's client-bulletin house style and non-driven ethics — see
`~/.claude/projects/-Users-klaus/memory/client_bulletin_house_style.md` and
`feedback_no_attorney_driven_language.md`.

## Inputs
- **Client** — the client/driver name (required; used to find the case + intake sheet).

## Steps

### 1. Find the case intake sheet
Use the Google Drive tools to locate the case's intake `.xlsx`:
- `search_files` with `title contains '<name>' and title contains 'Intake'` (or `fullText contains '<name>'`).
- The intake file is named like `<Driver Name>-<M-D-YYYY> Intake Sheet.xlsx`.
- If several match, pick the one whose title/folder matches the client and confirm with the user if ambiguous.

### 2. Read the intake and extract injuries (ENGLISH, verbatim)
Call `read_file_content` on the intake fileId. Extract the raw English value of:
- **Driver**: the field labeled `Initial Injuries? Short, comma-separated, from high to low, ...`
  — the value immediately after this label (e.g. `Neck pain; right upper back pain; ... Pain level: 6–7/10.`).
- **Passenger 1–4**: the field labeled `Injuries? Short, comma-separated, ...` inside each
  passenger's block. Only include a passenger if their name AND injuries fields are non-empty.

Also grab each person's **name** (Driver Name; Pass1 Name … Pass4 Name).

If the driver's injuries cell is empty, tell the user it's blank in intake and stop (don't invent injuries).

### 3. Translate to Chinese
Translate the extracted injuries into natural, client-friendly Chinese, **semicolon-separated**,
ending with the pain level as `疼痛程度 X/10`. Keep the high→low order from intake. Do NOT add
or drop symptoms — translate exactly what's recorded.

Common glossary (extend as needed):
- Neck pain → 颈部疼痛 · upper back pain → 上背部疼痛 · lower back pain → 下背部(腰部)疼痛
- shoulder pain → 肩部疼痛 · knee pain → 膝盖疼痛 · chest pain → 胸部疼痛
- pain and numbness → 疼痛及麻木 · tingling → 刺痛/发麻 · stiffness → 僵硬
- headache → 头痛 · dizziness → 头晕 · nausea → 恶心 · vomiting → 呕吐 · insomnia → 失眠
- left/right → 左侧/右侧 · Pain level 6–7/10 → 疼痛程度 6-7/10
Keep side qualifiers (right/left) attached to the body part, e.g. `right upper back pain` → `右侧上背部疼痛`.

### 4. Fill the template (one paragraph per client)
Use this EXACT template. The only generated part is each `<Name>-您目前的症状包括:<translated; semicolon-separated>。`
line. **Multi-client**: repeat ONLY that symptom line for each client — driver first, then each
passenger — stacking them right after the "文字总结:" opener. Everything else stays verbatim.

```
💉受伤更新

您好,这是基于您之前告诉我们,关于您当前受伤与症状的文字总结:

<Name>-您目前的症状包括:<中文症状;分号连排>;疼痛程度 X/10。
<（多位客人则每人再加一行同样格式）>

‼️见医生时,请务必将您的受伤情况完整告知,以便获得更精准的治疗方案。

‼️如果此时此刻您还有额外的受伤部位或症状,请立即告知我们进行更新。

⚠️ 温馨提醒:

🔍 别漏掉任何不适:有些车祸伤在当下并不明显,可能过几天才逐渐出现。请留意自己从头到脚的状况,任何真实的不适(即使轻微)都如实告诉医生,由医生评估处理。

✅ 如实且完整:请把身体所有不舒服的地方如实、完整地告诉医生,包括事故后才慢慢出现的症状。完整的就诊记录既有助于医生对症治疗,也让您的伤情有客观、连续的记录。若这份总结与您的实际感受有出入,请以您的真实感受为准,并在群里告诉我们更新。

🚩 及时核对信息:如果以上描述有任何遗漏或变化,请现在就在群里告诉我们,以便我们及时为您更新备案。
```

Notes:
- Name = the client's English name exactly as in intake (e.g. `Baolian Kuang`).
- If a client has no recorded pain level, omit the `;疼痛程度 X/10` tail for that line.

### 5. Output
Print the finished message in a copy-ready block. **Do not send or file anything.** If the user
then wants it posted to the case Chat space, that's a separate manual step.

## Guardrails
- Never invent or embellish symptoms — translate only what intake records.
- No `**markdown bold**` in the output (WeChat renders the stars).
- Generate only: no send / email / label / sheet write.
