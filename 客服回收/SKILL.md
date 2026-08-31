---
name: 客服回收
description: >
  客户满意度回收系统 for 凌图律所 / Law Office of Shenqi Cai APC (PI auto). Runs the
  post-settlement 口碑 recall loop: every disbursed client is invited to do **any one of
  Google Review / 小红书发帖 / 朋友圈推广** — any single one counts as 满意(达标); whoever does
  none of the three must have a RECORDED REASON. Also tracks the 三连 bonus program (GR free +
  $50 Zelle per XHS/PYQ, run by the case's Paralegal 好评负责人 → 内部 Form → Teresa 审核 →
  Joe 付款). Month-end reconciles the ledger against the firm's live Google page and the 好评返现
  Form responses, classifies each non-participant as 结构性 / 服务不满 / 待观察 / 未问, and hands
  Klaus a verdict to rule on. Trigger on: "/客服回收", 客服回收, 满意度, 客户满意度, 评论回收,
  好评回收, 好评返现, 三连, "登记一下 X 的好评", "X 不愿意评论", "跑月度满意度结算", "上月满意度",
  "Google 评论对账", or right after a case is disbursed. **Single source of truth = 市场部的
  好评返现 Google Form + its Responses sheet** (Klaus 2026-08-31: 市场部做的表足够了) — this skill
  keeps NO parallel ledger; it derives the 未做名单 by subtracting the Form's completions from the
  month's disbursed clients, collects the missing 「为什么」, and reports. It DRAFTS the monthly
  report only — never sends email, never posts to Chat, never pays anyone, never edits the
  marketing Form/SOP, and never rules on 达标 itself (Klaus rules).
---

# 客服回收 · 客户满意度回收系统

## 这个系统在解决什么
和解、支票交到客人手上那一刻,是满意度最高的时点。系统做两件事:
1. 把这一刻的口碑固定成**公开内容**(Google Review / 小红书 / 朋友圈);
2. 把**一个都没做**的客人变成一条**带原因的复盘线索**。

> **数量不是目的,拿到「为什么」才是。** 一个月人人都发了、但没有一条复盘线索 → 这个月只是运气好。

---

## 规则(Klaus 2026-08-31 定 · 规则只存在这里,不在表里)

### 达标(满意度指标)
- **三个渠道任意一个做了,就算这位客人满意 → 达标。**
  - `GR` Google Review · `XHS` 小红书发帖 · `PYQ` 朋友圈发推广文案
  - **GR 对客人最友好、最容易**,所以永远先请 GR;XHS / PYQ 有门槛,是加分不是主力。
- 计量单位 = **一位成年客户**。同事故司机 + 每位乘客各算一位;未成年由家长代领 → **家长算一位**,未成年本人不计。
- **当月和解客户里,三个都没做的人 —— 每一位都必须问出原因并记下细节。**
- **指标:未达标人数 ≤ 1 位。** 超过 1 位**不等于不达标** —— 但每位都要有原因细节,由 **Klaus 看原因裁定**。
- 系统只出四色初判,**裁定永远是 Klaus 填**(`月度结算` P 列)。

| 初判 | 触发 | 含义 |
|---|---|---|
| 🟩 达标 | 未达标 ≤ 1 位,且都有原因 | 过 |
| 🟨 待裁定 | 未达标 > 1 位,但全是结构性 / 待观察 | Klaus 看细节 |
| 🟧 需复盘 | 出现任何 D 类(服务不满) | 无论几位都复盘 |
| 🟥 流程失败 | 有客人没被邀请,或邀请了没记原因(U0) | **比不满更严重** —— 拿不到信息 |

### 加分项:三连(GR + XHS + PYQ)
- 目标是**每位结案客户都三连**。`GR` 白嫖(不返现),`XHS` / `PYQ` **每项 $50 Zelle**(市场部预算)。
- 三连满额 = **$100**(XHS $50 + PYQ $50)。台账 P 列自动算 `(XHS✅ + PYQ✅) × 50`。
- **三连是加分,不是达标条件** —— 只做了 GR 一样算达标。

> ⚠️ **和市场部现行 SOP 有冲突,未解决**:Drive「客户好评返现活动」里的《好评返现流程》和内部 Form
> 都写着 **Google Review 也返 $50**(7/31 已有一笔 GR+朋友圈 = $100 的实付记录)。Klaus 2026-08-31
> 的口径是 **GR 白嫖、只有 XHS/PYQ 返现**。本 skill 按 Klaus 的口径算钱。
> **建议维持 Klaus 口径**并让市场部改 Form + 海报:**付费换 Google 评论违反 Google 政策**,
> 评论会被清、Business Profile 有被罚风险。这件事需要 Klaus 拍板后同步给 Teresa / Joe。

### 谁做什么(沿用市场部《好评返现流程》角色分工)
- **Paralegal(该案好评负责人)**:① 在客户群发「好评返现指导图片」② 回答客户关于发布方式 / 截图 /
  返现金额的问题 ③ 收集完成截图 + Zelle 账号(**尽量一次性收完,不要后续补充**)
  ④ 填内部 Google Form ⑤ 填完在内部群 **@Teresa 和 @Joe**。
- **Teresa**:看内部群通知 + Form,资料不全 → 催对应 Paralegal。
- **Joe**:按 Form 资料 Zelle 付款,付完在表里打勾 / 群里留言,留付款凭证。
- **审核要点**(Paralegal 提交前自查):截图清晰可辨平台 · 小红书内容含案件类型 + 对团队正面评价 ·
  GR 是给 Lingtu Law APC 的五星 · **朋友圈必须「所有人可见」** · Zelle 账号无输入错误 · 金额 = 每项 $50。

---

## 固定 ID
| 什么 | ID / URL |
|---|---|
| **⚠️ 旧「满意度回收系统」Sheet — 已停用** | `1-i0Dw-cccJOFIxNM-6tsBd2SefNCN5KezuoVCwLLguE`(只留 2026-08 的 26 位基线数据 + `话术`/`原因码` 两个 tab 还有用;是否删由 Klaus 定。**不要再往里写数据**) |
| Completed Disbursed Sheet(结案客户名单来源) | `1EvsbLjAuRdTTfH3uyEmV3qFjmAtKCdfBPByVCMAF1kA` → `🔍 Search`: Date of Disburse \| Client \| DOL \| Tab |
| PI Master Sheet(查团队 / CM) | `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`(tab = 所属邮箱) |
| Drive「客户好评返现活动」 | folder `10Jwhvfyr0GAKiCcI9Vl-KBVrzLOp0SA5`(shared drive `0ADGjWMsKp6m6Uk9PVA`) |
| ↳ **诉讼人伤好评返现指导图片.png**(PI 用这张,不是移民那张) | `1JsOqrr3bm4duOQPPSEWjSGYPhea_s-m_` |
| ↳ 朋友圈文案 doc / 朋友圈海报 1 / 海报 2 | `1KTYnwAi9v_9TTifhzqLBGqd5-tBQdp-8Lr7Ph-6nojA` / `10ULPZ80RYZ1FeRqaZgMQ0BZgXFkcgH7K` / `1D8tPnrXaYvtbi8DEU_JA87a12NKzBhBA` |
| ↳ 《好评返现流程》SOP doc | `1ND2L7JPfJwKj16d61CFs9w3BuRUHKDjDeJMgmZIYfrw` |
| **内部好评返现 Form** | https://forms.gle/wMo6mZHMhxTmBKQw5 |
| ↳ **Form Responses sheet**(对账用) | `1JBJSJWbf_U9N94Vt1fzR8ZDrTv48AAkUlLuJ698OHEg` — 两个 tab,现行是 **`Form Responses 2`**(有 `Joe已付款` 列);列 = Timestamp \| Paralegal \| 客户姓名-案件类别 \| 完成的平台(多选) \| 截图链接 \| Zelle \| 应付金额 \| 备注 \| Joe已付款 |
| 律所 Google 页面 | https://maps.app.goo.gl/5KHw5NWWcEDYUWGu8 |
| 一键好评工具(发客人,自动生成文案) | https://lingtu-review-tool-925809628668.us-west1.run.app |
| Activity Log | `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA` → `Activity Log!A:J` |

**回收台账列位**(A..Y):
`A` 结算月份(公式) `B` Disburse日期 `C` Client `D` DOL `E` 团队邮箱 `F` 经办CM `G` 好评负责人
`H` 支票交付方式 `I` 邀请日期 `J` **GR** `K` **XHS** `L` **PYQ** `M` 完成日期
`N` 达标(公式) `O` 三连(公式) `P` 应返现$(公式) `Q` 返现Form提交日 `R` 返现状态 `S` Joe已付款
`T` 已@Teresa/@Joe `U` 未做原因码 `V` 原因细节(必填) `W` 归因(公式) `X` Klaus裁定 `Y` 复盘/备注

渠道列取值:`✅已发` / `⏳邀请中` / `❌没发` / `🚫不宜` / `❓未问`(只有 `✅已发` 计入达标)。
**Zelle 账号只存在 Form 里,台账不留** —— 别把客户收款信息抄进第二个地方。

### 四个已踩过的坑
1. **A / N / O / P / W 是 ARRAYFORMULA,锚点只在第 2 行** —— 写新行**只写 B:M + Q:V + Y**,永不往
   A/N/O/P/W 写值。而且 **`append` 不要带 `insertDataOption=INSERT_ROWS`** —— 插行会挤掉锚点公式,
   新行也不继承格式和数据验证。正确做法:读到最后一个有 C 值的行号,再 `values.update` 写下一行。
2. **日期一律写 ISO `YYYY-MM-DD`** —— 表建时 locale 曾是 `zh_CN`,`8/3/2026` 被当成 3 月 8 日写进去过
   (已改 `en_US`,但 ISO 无论 locale 都对)。
3. **月份匹配靠文本** `YYYY-MM`;`月度结算!A` 列必须 `valueInputOption=RAW`,否则被解析成日期 →
   COUNTIF 全部对不上。附带坑:`TEXT()` 作用在文本上原样返回 → B 列必须是**真日期**。
4. **Form 的「客户姓名-案件类别」字段填得很脏**(见过整格只写 `PI Auto`)→ 按客户名对账会漏。
   对不上的列进「待确认」交 Paralegal 补,**不要硬猜**。

---

## 记录在哪(2026-08-31 定)
- **完成记录 = 市场部的内部好评返现 Form**(Paralegal 填)→ Responses sheet `Form Responses 2`。**不另建表。**
- **未做名单 = 差集算出来的**:当月 Completed Disbursed 的客户 − Form 里有完成记录的客户。
- **「为什么」不进表** —— 月度结算时向该案好评负责人问一遍,原话写进**月度报告** + Activity Log 一行。
  这条是这套系统的命门:Form 只记做了的人,没人替我们记没做的人。**报告里每个未做的客人必须带一句客人原话**,
  写不出来的就是 U0(没问),点名负责人。
- 原因分类沿用旧表 `原因码` tab(S1–S6 结构性 / W1 待观察 / D0–D6 服务不满 / U0 未问),只当分类词典用。

## Mode ① 交付当天(不写表,只发东西)
1. 支票交付(当面或寄出)当天,该案好评负责人在客户群:
   - 先请 **GR** —— 发一键好评工具链接(自动生成文案,客人看一遍发出去)。
   - 再发**诉讼人伤好评返现指导图片**(`1JsOqrr3bm4duOQPPSEWjSGYPhea_s-m_`,PI 用这张,别用移民那张)
     + 朋友圈文案 / 海报,讲清 XHS $50 / PYQ $50。
2. 邮寄件**当天必须微信补邀请**(话术 5)—— 这是最常见的漏口。
3. 把 `话术` tab 对应场景原文贴给负责人。多客户案(司机+乘客)每位都要单独邀请。

## Mode ② 跟进 / 收材料(负责人自己跑,Claude 只提供话术)
- 客人做了 → 收截图 + Zelle(**一次性收齐**)→ 填 Form → 群里 @Teresa @Joe → Joe 付款。
- 口头答应没发 → 第 3 天(话术 6)、第 7 天(话术 7)各跟一次;第 3 次还没发 → 电话探因,记原话。
- 客人明确不愿意 → 先用**话术 4(探因)**问一句,原话记下来 —— 这句话比那条评论值钱。
- 提交前自查:截图清晰可辨平台 · XHS 内容含案件类型 + 对团队正面评价 · GR 是给 Lingtu Law APC 的五星 ·
  **PYQ 必须「所有人可见」** · Zelle 无输入错误 · 金额 = 每项 $50。

## Mode ③ 月度结算 — 每月 1 号跑上个月
1. **`date` 读真实日期**,算出目标月 `YYYY-MM`(默认上一个自然月)。
2. **结案客户名单**:读 Completed Disbursed `🔍 Search`,筛 Date of Disburse 落在目标月 → 展开成客户级名单
   (tab 名里 `/` 分隔 = 同案多客户,每位算一位;剥掉 `✅` 前缀)。**去重坑**:中间名(`Yuran Zhou` vs
   `Yuran N Zhou`)打断精确匹配 → 模糊比对。
3. **读 Form Responses**(`Form Responses 2`),筛目标月 Timestamp → 拿到「完成了什么平台 / 应付金额 /
   Joe已付款」。⚠️ Form 的「客户姓名-案件类别」字段填得脏(见过整格只写 `PI Auto`)→ 对不上的进「待确认」,
   交负责人补,**不要硬猜**。
4. **对账 GR**(公开页,不用登录;浏览器打开 Google 页面 → 按最新排序 → 读评论人 / 星级 / 日期 / 正文):
   数出本月新增评论数、累计数、平均星级。Google 上有、Form 里没有 → 客人自己发的,**照样算达标**,
   在报告里补上。Google 显示名常和案件英文名不一样(昵称 / 拼音 / 中文名),对不上的进「待确认」。
5. **差集 → 未做名单**,逐个向负责人要原因 + 客人原话,按 `原因码` 归类。
6. **算数**:结案客户 N · 达标 X(至少一项)· 未达标 Y · GR/XHS/PYQ 各几位 · 🏆三连几位 ·
   应返现 $ / 已付 $ · 未做里结构性 / 服务不满 / 待观察 / 未问 各几位。
7. **四色初判**:未问>0 → 🟥流程失败;有 D 类 → 🟧需复盘;未达标 ≤1 → 🟩达标;否则 🟨待裁定。
   **裁定永远是 Klaus 的** —— 报告末尾把裁定选项摆出来,不要自己判。
8. **复盘条目**:每个 D 类 + 每个 U0 各一条(客人 / 负责人 / 原话 / 卡在哪个环节 / 建议动作),
   D3(沟通不到位)按红线级处理。可直接喂 `团队复盘` 当周一材料。
9. 收工:Activity Log append 一行 —— Category `客户`,Source `Manual`,`manual:客服回收`,
   Ref = `<YYYY-MM> 满意度结算`,备注里带上未达标名单和原因(这就是「为什么」的留痕)。

### 月度报告格式
```
📊 <YYYY-MM> 客户满意度回收

结案客户 N 位 · 达标 X 位(做了至少一项)· 未达标 Y 位   [指标 ≤1]
渠道:GR a · XHS b · PYQ c · 🏆三连 d 位
返现:应付 $e · Joe 已付 $f · 待付 <名单>
Google 页面:本月新增 h 条 · 累计 T 条 · 平均 R★
系统初判:<🟩/🟨/🟧/🟥 + 一句话>

未达标名单(三个渠道一个都没做)
1. <Client> · <好评负责人> · <原因码 说明>
   客人原话:「……」
2. …

⚠️ 需要复盘(D 类 / U0)
· <Client> — <卡在哪个环节> → <建议动作>

💰 返现待办
· <Client> $<金额> — 卡在 <Form 未填 / 未 @Teresa @Joe / Joe 未付>

📋 等 Klaus 裁定
· 这个月判 达标 / 达标(有观察项) / 不达标
```

---

## 红线(照抄给团队,也在 `话术` tab 最后一行)
1. **Google 评价绝对不许用钱、礼品、减费换** —— 违反 Google 政策,页面可能被下架。返现只针对 XHS / PYQ。
2. **不许代客人发布**、不许用律所手机或帐号发 —— 必须客人本人发。工具只生成文案。
3. **不许只挑满意的客人邀请**(review gating)—— 每个结案客人都要邀请;不满意的照样邀请,不做就记原因。
4. **不许在内容里出现赔偿金额、保险公司名、伤情细节** —— 客人自己愿意写是他的事,我们不引导。
5. 客人说不满意时**不许辩解、不许当场解释** —— 只记原话,交给 Klaus。
6. **返现一律走登记流程**(截图 + Zelle + 内部 Form + @Teresa @Joe + Joe 付款),不许私下答应金额、不许先转后补。

## 边界
- 只 **append / 更新**台账,**永不删行**;写错了在 Y 列写更正说明。
- **不裁定达标**、**不动奖金表**、**不付返现** —— 钱由 Joe 走 Zelle,系统只记账和催。
- 不发邮件、不发 Chat、不改 Google 页面、不改市场部 Form / SOP。报告出在 session 里。
- 客户名一律英文原名。

## 当前状态(2026-08-31)
- **规则文字已定稿**(见上「规则」段),团队版纯文本在 `~/.claude/skills/客服回收/规则文字.txt`。
- **不建平行台账** —— 记录走市场部 Form。旧 Sheet `1-i0Dw…` 停用,只留 8 月基线 + `话术`/`原因码`,
  是否删由 Klaus 定。
- **GR 是否返现的口径冲突未解决**:市场部 Form / SOP / 海报写着 GR 也返 $50(7/31 有实付记录),
  Klaus 口径是 GR 白嫖。规则文字按 Klaus 口径写 —— **发给团队前必须先改 Form,否则两边对不上**。
- **2026-09 起正式跑**;2026-08 是上线前,不考核。

## 相关
`case-settles`(Step 36 建行)· `团队复盘`(D 类进周一材料)· `bonus_records_system`(结案月同一数据源)
