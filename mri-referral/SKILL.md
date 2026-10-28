---
name: mri-referral
description: |
  Set up an MRI for a PI client at 凌图律所 / Lingtu Law Office end to end: pick the imaging
  center (firm's preferred one first, two truthful fall-backs), email the demographic + the
  doctor's MRI order to the center, give Klaus the client WeChat 文案, then update the PI Master
  Sheet and the case Chat space. Trigger when a treating clinic sends an MRI order/referral
  ("MRI referral- <Client>", "MRI Ref"), or on: "约 MRI", "帮客人找 MRI", "MRI 转介",
  "send MRI referral", "/mri-referral <Client>". Email is DRAFT first — sent only on Klaus's "发".
---

# mri-referral — 帮客人约 MRI

Built from Sai Choi Lau (2026-10-27/28, Sun Imaging RH). Flow Klaus set:
找机构（偏好的放第一）→ 客人确定 → email demographic → 客人文案 → Master Sheet + Chat。

FIRST: `date "+%m/%d/%Y %H:%M"`.

## Step 0 — Inputs
- **The MRI order** — usually the treating chiro emails it to the case mailbox
  (subject like `MRI referral- <Last>, <First> (DOL:…)`, PDF `REFERRAL <date> <Name>.pdf`).
  Read it: ordering doctor, order date, body parts (Cervical / Lumbar / …), with/without contrast.
- **Client**: name, DOB, phone, address, DOL — from the case intake sheet (or the order itself;
  the two must agree, flag if not).
- **Owning mailbox**: Master Sheet tab (`Claims@` / `Piteam@` / `Picase@`) → that mailbox.
  **Klaus's own cases** (see memory `klaus_keeps_pi_auto_litigation`, e.g. Sai Choi Lau,
  Jiayu Ma, Chao Zheng) → **klaus@, Cc Claire Feng** (claire.f@lingtulaw.com).
- Check the case mailbox for a referral draft a CA already started (Claire often drafts one with
  an empty To). Don't create a second live draft for the same center — use hers or tell Klaus which
  one to delete before sending.

## Step 1 — Candidates (script)
```bash
python3 ~/.claude/skills/mri-referral/scripts/mri_candidates.py "<client street, city, CA zip>"
```
Prints, per imaging-center family in `references/mri_centers.json`: how many MRI referrals the
firm sent it (all four mailboxes, last 365 days) and each operating location's straight-line
miles, phone and Google rating. Miles are **straight-line** (the Routes/Distance Matrix API is not
enabled on project `claude-chat-bridge-20687`) — say so; never invent drive times.
If a center the team uses isn't in the JSON, add it (family, search string, email_match, referral email).

## Step 2 — Pick 3, preferred first (Klaus 2026-10-28)
1. **#1 = the firm's preferred center**: highest referral volume among locations that are near the
   client, Chinese-friendly where possible. Default Sun Imaging if it has a site close by.
   Mention a real convenience if there is one (e.g. Sun Imaging RH is a 5-minute walk from
   Affinity, 19031 Colima Rd — 走路五分钟，不用开车).
2. **#2 and #3 = real, operating alternatives whose notes steer the client back to #1** —
   farther away, needs driving/freeway, no Chinese-speaking staff, low Google rating.
   ⚠️ **Every note must be true** (distance from the script, language from `mri_centers.json` or a
   phone check, rating from Places). Never invent a drawback; if you can't verify "不说中文", say
   "中文服务不确定" instead.
3. Show Klaus a table (name / address / miles / phone / referrals sent / note) and the client
   options 文案 below. **Wait for the client's choice** (Klaus relays it).

Client options 文案 (plain text, full-width punctuation, blank line between blocks — memory
`feedback_client_message_plain`):
```
【MRI检查机构推荐】

您好，医生建议您做<颈椎和腰椎>的核磁共振（MRI）检查。以下三家影像中心供您选择：

1. <#1 Name>
地址：<address>
电话：<phone>
备注：<离您最近 / 在您治疗的诊所附近，走路几分钟 / 可以说中文>

2. <#2 Name>
地址：<address>
电话：<phone>
备注：<距离较远，约<N>英里，需要开车>

3. <#3 Name>
地址：<address>
电话：<phone>
备注：<不提供中文服务 / 距离较远>

建议您先在Google或Yelp上看看各家的评价，再做决定。

选好后告诉我们，我们帮您转单预约。
```

## Step 3 — Email the demographic (DRAFT → Klaus "发")
- **To** = the chosen center's scheduling email (`mri_centers.json`). **Cc**: only internal staff
  Klaus names (Claire on his own cases). **Never Cc the treating chiro** (Klaus 2026-10-28:
  「我一般不cc chiro」).
- **Subject**: `MRI_Referral_Lingtu Law_<Client>`
- **Attach** the MRI order PDF as `MRI Ref - <Client>.pdf`.
- **Body** (HTML, one `<p>` each; signature from the sending mailbox's `sendAs`, never hand-typed):
  ```
  Hi Doctor's Office,

  MRI referral is attached for your review, and please contact the patient to set up an appointment.

  <Client> (Driver)
  Date of Loss: MM/DD/YYYY
  Date of Birth: MM/DD/YYYY
  Phone: (xxx) xxx-xxxx
  Address: <street, city, CA zip>

  If the patient is unreachable or misses the appointment, please contact our office immediately so we may assist further.
  ```
- Create the draft, apply the **case label** (klaus@ case label / team-mailbox case label) right
  away, show it in the bilingual review format, and send only on Klaus's explicit "发" naming
  this draft. Re-apply the label after every draft update and after sending.
- File the MRI order PDF to the case folder (`4#Bodily Injury Claim/Referral` or that case's
  referral subfolder), MD5-checked, one current copy only.

## Step 4 — Client confirmation 文案 (give to Klaus, he pastes to WeChat)
Locked wording from Sai Choi Lau — swap only the slots:
```
您好，您的MRI（核磁共振）检查单已经转给<Center>，检查<颈椎和腰椎>。

地址：<address>

电话：<phone>

<Center>会直接打电话给您约时间。如果两三天内没有接到电话，您可以直接打上面的电话预约。

<一句真实的便利说明，例如：就在Affinity诊所附近，走路五分钟就到，不用开车。>去的时候请带上您的驾照或身份证件。

约好时间后请告诉我们一声，谢谢！
```

## Step 5 — After the email is sent: Master Sheet + Chat
1. **PI Master Sheet** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`, the client's CM tab: write
   `M/D <Center>` (e.g. `10/28 Sun Imaging RH`) in the **MRI** column, bright-yellow fill.
   Same mechanics as `chiro-referral` Step 8: pull the grid fresh (no A1 ranges), find the row by
   full client name and the column by header text, write with gid-based `updateCells`
   (Picase@ `775230687`, Claims@ `86730608`, Piteam@ `102974151`). Cell already has content →
   don't overwrite, ask Klaus.
2. **Case Chat space** (default gws = klaus@): post
   ```
   【Claude AI】 MRI referral sent via email to✅
   <Center name>
   <Address>
   <Phone>
   <Email>
   ```
3. If the case has a case artifact (`~/.claude/skills/case-artifact/assets/applied.json`), update its
   treatment section + timeline in the same wrap-up.

## Step 6 — Center confirms the appointment (Klaus 2026-10-28：「收到这个信息需要更新 master sheet，intake sheet，还有 post 在 chat」)
The center replies on the referral thread (e.g. "scheduled … Wednesday, 11/04/2026, at 9:30 AM").
Do all of these in one pass, no need to ask:
1. **Gmail**: re-apply the case label to the thread (the reply arrives unlabelled).
2. **PI Master Sheet MRI column**: rewrite to the appointment date, the column's convention —
   `11/04(C/L) Sun Imaging RH`. **Fill = amber 暗黄 `#ffe49f`**（已确认预约、等待发生；Klaus 2026-10-28）。
   Referral sent but not yet booked stays bright yellow `#ffff00`. If a CA wrote the cell, keep her text and append ` → 11/04 <Center>`.
3. **Intake sheet** (`<Client>-<DOL> Intake Sheet`, native gsheet in the case folder), tab `Sheet 1`,
   **Treatments block, the `MRI` group (col Q labels / col R values)**: R=center name, Address,
   Phone (digits only, like the Chiro block), Email, and **Note** =
   `MRI C/L w/o contrast (<clinic> / <doctor> <M/D> Ref); referral sent <M/D>; appt <MM/DD/YYYY h:mm AM>`.
   Find rows by label text, not fixed row numbers. **Values are NOT bold** (Klaus 2026-10-28): write them, then
   `repeatCell` with `userEnteredFormat.textFormat.bold=false` on the written cells — the block's
   cells inherit bold otherwise. If tab `Treatment Cost` lists the MRI under
   "Recommendation (未做)", append `→ <Center>，已约 <M/D h:mm AM>` to that line.
4. **Case Chat**: `【Claude AI】 MRI appointment confirmed✅` / `<Center>` / `<Weekday> MM/DD/YYYY h:mm AM — MRI <body parts>`.
5. **Calendar + todo**: move the "confirm booked" event to the appointment slot (Free); close the
   todo and add one for the appointment day: confirm the client went, then request report + bill.
6. Case artifact (if any): treatment row + timeline. Offer Klaus a short WeChat reminder 文案 (time /
   address / phone / bring ID / call to reschedule).

## Guardrails
- Draft-only until Klaus says "发" for this draft; one live draft per center.
- Notes on alternatives are factual only; the client still chooses (keep the Google/Yelp line).
- No attorney-driven wording to providers (memory `feedback_no_attorney_driven_language`).
- Coverage check before booking: if the case has no collectible coverage, say so in one line and
  let Klaus decide (Sai Choi Lau: he chose to proceed).
