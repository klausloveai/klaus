---
name: case-brief
description: >-
  Daily litigation case brief for Klaus: sweep klaus@ for new email on the Hernán /
  litigation cases, append the new events to the "Case Log" Sheet (中文 + English tabs),
  and output a todo digest — 你要做的 / 等别人的 / 临近 deadline. Trigger on: "/案件简报",
  "案件简报", "待办", "todo", "案件进度", "case brief", "跑案件简报", or the daily 11am
  reminder. READ-ONLY against email (never labels, moves, or deletes anything); the only
  write is appending rows to the Case Log, and only after Klaus approves. NOT a 复盘 —
  siblings are /设置复盘 (Claude config) and /项目复盘 (project portfolio).
---

# case-brief — 每日案件简报 (litigation)

Klaus is the hub: Hernán, the courts, One Legal, adjusters, providers and clients all
email **klaus@**. This turns that inbox into (1) an append to the case log and (2) a
"what do I owe / who owes me" digest. Scope = **litigation cases only** — the auto-PI
book is tracked by the Master sheet + the CMs.

## The Tracking Sheet

Sheet **"Tracking Sheet"**, id `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA` — lives in the
**"Hernan Simo Cases" shared drive** (so Hernán/the team can see it; keep entries factual,
not internal musing). Klaus combined it 2026-07 — **three tabs**:
- **Master Sheet** (`2022430354`) — the firm's standard PI tracking grid (DOL · Client Name ·
  Referrer · Case Status · 1LOR/1Coverage/1Liability · 3LOR/3Coverage/3Liability · Property
  Damage · Ambulance/Emergency/Urgent Care/Family Doctor · Medi-Cal/Medicare/Health Insurance
  Lien · Outstanding Balance · Chiropractic/MRI/PM/Other). **This is the primary view — case
  PROGRESS.** Cell colors follow [[master-sheet-recording-colors]]. Don't restructure it.
- **中文 Log** (`0`) — `日期 | 案件 | 事项 | 状态` · statuses `待办 / 进行中 / 完成`
- **English Log** (`583147617`) — `Date | Case | Entry | Status` · `To-do / In progress / Done`

The **Logs are the chronological narrative**; the **Master Sheet is the current-state grid**.
`/案件简报` appends to both Log tabs; if an email also changes a Master Sheet field (e.g. an
LOR went out, a status moved), propose that cell update too — same approval gate.

**Newest date on top.** Colors are conditional-format rules keyed off the status column,
using the firm's standard palette ([[master-sheet-recording-colors]]):
🟨 `#ffe49f` 待办/To-do · 🟦 `#c2e7ff` 进行中/In progress · 🟩 `#d4edbd` 完成/Done.
Write **both Log tabs every time** so they never drift.

Active cases (as of 2026-07): Yi Cong · Guolin Zhao · Mudong Huang · Bo Tao · Weicong Lin
· Lina Lu · Zhiping Liu · Jiayu Ma · CB Kitchen.

## Steps

1. **Sweep klaus@** for email since the last logged date (default: yesterday → today).
   ```bash
   gws gmail users messages list --params '{"userId":"me","q":"newer_than:2d","maxResults":60}' --format json
   gws gmail users messages get --params '{"userId":"me","id":"<ID>","format":"full"}' --format json
   ```
   **GOTCHA:** `gws` prints `Using keyring backend: keyring` — sometimes *after* the JSON,
   so `json.loads(s[s.index('{'):])` dies with "Extra data". Use
   `json.JSONDecoder().raw_decode()`. Bodies are base64url in `payload.parts[*].body.data`
   (`text/plain`); strip quoted history by splitting on `\nOn .* wrote:` / `\nFrom: `.
2. **Match each email to a case by subject** — Klaus's subject hygiene is good
   (`Bo Tao - Complaint`, `Zhiping Liu v. State Farm - …`, `Mudong Huang, Homesite claim #…`,
   `eFiling accepted for CONG-v- EDPAO`). Ignore anything not litigation.
3. **Turn real events into log rows** — one row per *thing that happened*, short. Skip pure
   acks ("Thank you!", 👍 reactions) unless they carry an instruction or a decision. Set the
   status: 完成 (it happened) / 进行中 (running, e.g. clerk review, service en route) /
   待办 (Klaus or someone must act).
4. **Read the log back first** so you don't duplicate rows already there.
5. **Present the digest + the proposed rows** — numbered, `批准 / 跳过`:
   - 🔴 **今天必须动** — overdue / imminent deadlines
   - ⏰ **你的待办** — extracted from Hernán's asks, court notices, adjuster requests
   - ⏳ **等别人的** — blocked on Hernán's signature / Claire's records / the process server
     / the clerk (**this section is the point** — litigation's biggest leak is forgetting
     who you're waiting on and for how long)
   - 📅 **Deadlines** — days remaining
6. **On approval, append to BOTH tabs**, then confirm with the Sheet link.

## Guardrails
- **Read-only against Gmail.** Never label, move, archive or delete — Klaus rejected label
  automation as too error-prone (2026-07); a digest is safe precisely because it only reads.
- **Approval-gated writes.** Propose rows first; only append after Klaus says which.
- **No fabrication.** Every row must trace to an actual email. If a deadline isn't stated,
  don't invent one — flag it as "to confirm".
- **Deadlines → the calendar goes through [[hernan-email-skill]]'s propose→approve→invite
  flow** (Klaus does NOT want auto-created events). Default invitees follow Hernán's own
  pattern: Klaus · Joe Wu · Shenqi Cai · Cindy Zhang. Reminder tiers 提前3天/1天/当天.
- The log is **shared-drive visible** — keep entries factual and neutral.

## Cadence
Daily **11:00 AM** email reminder (rides the same calendar events as `/项目复盘`). Klaus
triggers it; the analysis is interactive. Once its output proves reliable for a few days it
can be promoted to a headless LaunchAgent that delivers the digest each morning — Gmail is
server-side, so unlike the 复盘 skills this one *can* eventually run unattended.
