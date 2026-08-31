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
  "Google 评论对账", or right after a case is disbursed (chained from `case-settles` Step 36).
  Three modes: ①登记 ②回填 ③月度结算. It WRITES to the satisfaction ledger (append/update only)
  and DRAFTS the monthly report — it never sends email, never posts to Chat, never pays anyone,
  and never rules on 达标 itself (Klaus rules).
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
| **满意度回收系统 Sheet** | `1-i0Dw-cccJOFIxNM-6tsBd2SefNCN5KezuoVCwLLguE`(klaus@ My Drive) |
| ↳ tabs | `回收台账`(251393844) `月度结算`(348568453) `原因码`(1772388048) `Google评论对账`(599287952) `话术`(902706954) |
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

## Mode ① 登记 — 支票交付当天
触发:`case-settles` 跑完 / Klaus 说「X 的支票给了 / 寄了」。

1. 从 Completed Disbursed / disbursement PDF 拿 **Client(英文原名,永不翻中文)、DOL、disburse 日期**。
2. 多客户案(司机+乘客)→ **一人一行**。未成年不建行,家长那行备注「代 <Minor> 领」。
3. PI Master Sheet 查所属 tab = 团队邮箱 → 经办 CM;`G` 好评负责人 = 该案 Paralegal(不确定就留空并问)。
4. 写 `B:M`:B–H 基础信息,I 邀请日期,J/K/L 三个渠道先给 `⏳邀请中` 或 `❓未问`。
   - 当面交付且当场邀请过 → I=当天,J=`⏳邀请中`(先请 GR),K/L 按有没有讲返现给 `⏳邀请中` / `❓未问`
   - **邮寄** → H=邮寄,**当天必须微信补邀请**(话术 5)+ 发「诉讼人伤好评返现指导图片」;没补 → J/K/L=`❓未问`,U=`S4`
5. 把 `话术` tab 对应场景原文贴给 Paralegal / 贴回 session,让他照读。

## Mode ② 回填 — 客人做了 / 没做
**按 Client 名字现搜行号,不要用缓存行号**(表会被排序)。

- **做了**:对应渠道列填 `✅已发`,M=完成日期。N 自动变 `✅达标`。
  - XHS / PYQ 有 ✅ → P 自动算出应返现 → 走返现闭环:Paralegal 收截图 + Zelle → 填 Form(Q 记提交日)
    → 内部群 @Teresa @Joe(T=是)→ Joe 付款(S=是,R=已发)。P>0 而 R≠已发 的格子会自动标黄。
- **一个都没做**:U 选原因码,V **必填客人原话**。
  - 「客人不愿意」这类空话不接受 → 退回问。V 空着时该格自动标红。
  - 客人明确不愿意 → 先用**话术 4(探因)**问一句,原话写进 V。
- **口头答应没发**:第 3 天(话术 6)、第 7 天(话术 7)各跟一次 → 仍没发 → U=`W1`(待观察);
  第 3 次还没发 → 改 U=`D0`(服务不满),由好评负责人电话探因。
- **🚫不宜**(失联 / 回国 / 未成年独立 / 律所自己人)→ 三个渠道填 `🚫不宜`,U=`S5`,V 写清情况。

## Mode ③ 月度结算 — 每月 1 号跑上个月
1. **`date` 读真实日期**,算出目标月 `YYYY-MM`(默认上一个自然月)。
2. **结案客户名单**:读 Completed Disbursed `🔍 Search`,筛 Date of Disburse 落在目标月 →
   展开成客户级名单(tab 名里 `/` 分隔 = 同案多客户,**每位都算一位**;剥掉 `✅` 前缀)。
   **去重坑**:中间名(`Yuran Zhou` vs `Yuran N Zhou`)会打断精确匹配 → 模糊比对。
3. **对账台账**:名单里在 `回收台账` 找不到行的客户 → **漏登记**,算 U0(未问),点名负责人。
4. **对账 GR**(公开页,不用登录;浏览器打开 Google 页面 → 按最新排序 → 读评论人 / 星级 / 日期 / 正文):
   - 数出目标月新增评论数、累计数、平均星级 → 写一行进 `Google评论对账`。
   - Google 上有、台账没记 → 回填 `✅已发`(客人自己发的照样算)。台账记了 ✅、Google 上找不到 →
     让负责人拿截图,否则改回 `⏳邀请中`。
   - ⚠️ Google 显示名常和案件英文名不一样(昵称 / 拼音 / 中文名),对不上的进「待确认」,别硬猜。
5. **对账 XHS / PYQ + 返现**:读 Form Responses sheet(`Form Responses 2`),筛目标月 Timestamp →
   按客户名匹配台账:完成的平台 → 回填 K/L `✅已发`;Q=Timestamp 日期;`Joe已付款`=TRUE → S=是,R=已发。
   Form 里有、台账没有的客户 → 补登记。**台账应返现总额 与 Form 应付金额合不上就报出来**
   (最常见原因就是上面那条 GR 是否返现的口径冲突)。
6. **算数**(`月度结算` 目标月行 B–O 是公式;缺行就补一行,A 列 RAW 写月份)。
7. **产出中文报告**(见下),Klaus 看完在 P 列写裁定。
8. **复盘条目**:每个 D 类 + 每个 U0 各生成一条(客人 / 负责人 / 原话 / 卡在哪个环节 / 建议动作),
   D3(沟通不到位)按红线级处理。可直接喂 `团队复盘` 当周一材料。
9. 收工:Activity Log append 一行 —— Category `客户`,Source `Manual`,`manual:客服回收`,
   Ref = `<YYYY-MM> 满意度结算`。

### 月度报告格式
```
📊 <YYYY-MM> 客户满意度回收

结案客户 N 位 · 达标 X 位(做了至少一项)· 未达标 Y 位   [指标 ≤1]
渠道:GR a · XHS b · PYQ c · 🏆三连 d 位
返现:应付 $e(Form 已提交 f 笔 / Joe 已付 g 笔)
Google 页面:本月新增 h 条 · 累计 T 条 · 平均 R★
系统初判:<🟩/🟨/🟧/🟥 + 一句话>

未达标名单(一个渠道都没做)
1. <Client> · <负责人> · <原因码 说明>
   客人原话:「……」
2. …

⚠️ 需要复盘(D 类 / U0)
· <Client> — <卡在哪个环节> → <建议动作>

💰 返现待办
· <Client> $<金额> — 卡在 <Form 未填 / 未 @Teresa @Joe / Joe 未付>

📋 等 Klaus 裁定
· <这个月判 达标 / 达标(有观察项) / 不达标>,写进 月度结算!P<行>
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
- `2026-08` 已回填 **26 位** disburse 客户(来自 Completed Disbursed `🔍 Search`),三个渠道全 `❓未问`
  → 初判 🟥。**8 月是上线基线月,不作为考核月**(写在 `月度结算!Q2`)。
- 其中 **8/20 之后交付的 12 位仍可追补邀请**(台账 Y 列标了 `🔔 可追补`)。
- `Dacheng Xu`(8/20) 在 Master 的 Claims@ 和 Piteam@ **都有**,团队 = `待确认`,等 Klaus 定。
- `G` 好评负责人全列空白 —— 需要 Klaus / 市场部给出每个案子的 Paralegal 对应关系。
- **GR 是否返现的口径冲突未解决**(见上)。
- **2026-09 起正式跑**。表还没共享给团队 —— 共享范围由 Klaus 定。

## 相关
`case-settles`(Step 36 建行)· `团队复盘`(D 类进周一材料)· `bonus_records_system`(结案月同一数据源)
