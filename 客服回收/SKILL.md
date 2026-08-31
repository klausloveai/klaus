---
name: 客服回收
description: >
  客户满意度回收系统 for 凌图律所 / Law Office of Shenqi Cai APC (PI auto). Runs the
  post-settlement Google-review recall loop: every disbursed client gets asked for a Google
  review at check pickup; whoever does not review must have a RECORDED REASON; month-end
  reconciles the ledger against the firm's live Google page, classifies each non-reviewer as
  结构性 / 服务不满 / 待观察 / 未问, and hands Klaus a verdict to rule on. Trigger on:
  "/客服回收", 客服回收, 满意度, 客户满意度, 评论回收, 好评回收, "登记一下 X 的评论",
  "X 不愿意评论", "跑月度满意度结算", "上月满意度", "Google 评论对账", or right after a case
  is disbursed (chained from `case-settles` Phase 7). Three modes: ①登记 ②回填 ③月度结算.
  It WRITES to the satisfaction ledger (append/update only) and DRAFTS the monthly report —
  it never sends email, never posts to Chat, and never rules on 达标 itself (Klaus rules).
---

# 客服回收 · 客户满意度回收系统

## 这个系统在解决什么
和解、支票交到客人手上那一刻,是满意度最高的时点。系统做两件事:
1. 把这一刻的口碑固定成 **Google 评论**(新客户来源);
2. 把**不愿意评论**的客人变成一条**带原因的复盘线索**。

> **评论数不是目的,拿到「为什么」才是。** 一个月没人不评论但也没人复盘 → 系统没在工作。

## 达标规则(Klaus 2026-08-31 定 · 不用百分比)
- 计量单位 = **一位成年客户**。同事故的司机 + 每位乘客各算一位;未成年人由家长代领 → **家长算一位**,未成年本人不计。
- **默认每月允许 1 位客人不评论**,但**必须知道细节原因**。
- **超过 1 位不评论 ≠ 不达标** —— 但每一位都必须有原因细节,由 **Klaus 看原因裁定**。
- 系统只给事实 + 初判四色,**裁定永远是 Klaus 填**(月度结算 K 列)。

| 初判 | 触发 | 含义 |
|---|---|---|
| 🟩 达标 | 未评论 ≤ 1 位,且都有原因 | 过 |
| 🟨 待裁定 | 未评论 > 1 位,但全是结构性/待观察 | Klaus 看细节 |
| 🟧 需复盘 | 出现任何 D 类(服务不满) | 无论几位都复盘 |
| 🟥 流程失败 | 有客人没被问,或问了没记原因(U0) | **比不满更严重** —— 拿不到信息 |

## 固定 ID
| 什么 | ID / URL |
|---|---|
| **满意度回收系统 Sheet** | `1-i0Dw-cccJOFIxNM-6tsBd2SefNCN5KezuoVCwLLguE` (klaus@ My Drive) |
| ↳ tabs | `规则`(847866788) `回收台账`(251393844) `月度结算`(348568453) `原因码`(1772388048) `Google评论对账`(599287952) `话术`(902706954) |
| Completed Disbursed Sheet(结案客户名单来源) | `1EvsbLjAuRdTTfH3uyEmV3qFjmAtKCdfBPByVCMAF1kA` → `🔍 Search` tab: Date of Disburse \| Client \| DOL \| Tab |
| PI Master Sheet(查团队/CM) | `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`(tab = 所属邮箱) |
| 律所 Google 页面 | https://maps.app.goo.gl/5KHw5NWWcEDYUWGu8 |
| 一键好评工具(发客人) | https://lingtu-review-tool-925809628668.us-west1.run.app |
| Activity Log | `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA` → `Activity Log!A:J` |

**回收台账列位**:A 结算月份(公式) B Disburse日期 C Client D DOL E 团队邮箱 F 经办CM
G 支票交付方式 H 是否已请评论 I 请求日期 J 请求方式 K 评论状态 L 评论日期 M Google显示名
N 星级 O 原因码 P 原因细节 Q 归因(公式) R Klaus裁定 S 复盘/备注

### 三个已踩过的坑(2026-08-31 建表时踩的,别再踩)
1. **A 和 Q 是 ARRAYFORMULA,锚点只在第 2 行** —— 写新行**只写 B:P(+S)**,永不往 A / Q 写值。
   而且 **`append` 不要带 `insertDataOption=INSERT_ROWS`** —— 插行会把 A2/Q2 的 ARRAYFORMULA 挤掉、
   新行也不继承格式和数据验证。正确做法:先读到最后一个有 C 值的行号,再用 `values.update`
   写 `B<n+1>:P<n+1>`(或 append 但用默认 OVERWRITE)。写完顺手 verify A 列出来的是 `2026-09` 这种月份。
2. **日期一律写 ISO `YYYY-MM-DD`** —— 表刚建时 locale 是 `zh_CN`,`8/3/2026` 被当成「3 月 8 日」写进去了
   (locale 已改成 `en_US`,但 ISO 无论 locale 都对)。写完抽查 B/D 列。
3. **月份匹配靠文本** `YYYY-MM`。`月度结算!A` 列写入必须 `valueInputOption=RAW`,否则被解析成日期 →
   COUNTIF 全部对不上(和奖金表同一个坑)。台账 A 列的数字格式已设成 TEXT。
   附带坑:`TEXT()` 作用在文本上会原样返回 —— 所以 B 列一定要是**真日期**,不能是文本串,否则 A 列会漏出整个日期。

---

## Mode ① 登记 — 支票交付当天
触发:`case-settles` 跑完 / Klaus 说「X 的支票给了 / 寄了」。

1. 从 Completed Disbursed / disbursement PDF 拿 **Client(英文原名,永不翻中文)、DOL、disburse 日期**。
2. 多客户案(司机+乘客)→ **一人一行**。未成年人不建行,家长那行备注「代 <Minor> 领」。
3. PI Master Sheet 查所属 tab = 团队邮箱 → 经办 CM。
4. `values.append` 到 `回收台账!B:P`,写 B–J,K 先给 `⏳已答应待发` 或 `❓未问`:
   - 当面交付且已当场请求 → H=是,I=当天,J=当面扫码/当面引导操作,K=⏳已答应待发
   - **邮寄** → G=邮寄,并**当天必须微信补请求**(话术 4);没补 → K=❓未问,O=S4
5. 把「话术」tab 对应场景的原文贴给 CM(或贴回 session),让他照读。

## Mode ② 回填 — 客人发了 / 不发
**按 Client 名字现搜行号,不要用缓存行号**(表会被排序)。

- **发了**:K=✅已评论,L=评论日期,M=Google 上的显示名(用来月度对账),N=星级。O/P 留空。
- **不发**:O 选原因码(见 `原因码` tab),P **必填客人原话**。
  - 「客人不愿意」这类空话不接受 → 退回 CM 重问。P 空着时该格会自动标红。
  - 客人明确不愿意 → 必须先用**话术 3(探因)**问一句,把原话写进 P。
- **口头答应没发**:第 3 天(话术 5)、第 7 天(话术 6)各跟一次 → 仍没发 → O=W1(待观察);
  第 3 次还没发 → 改 O=D0(服务不满),由 CM 电话探因。
- **🚫不宜请求**(失联/回国/未成年独立/律所自己人)→ K=🚫不宜请求,O=S5,P 写清情况。**不计入不满,但要有行**。

## Mode ③ 月度结算 — 每月 1 号跑上个月
1. **`date` 读真实日期**,算出目标月 `YYYY-MM`(默认上一个自然月)。
2. **结案客户名单**:读 Completed Disbursed `🔍 Search`,筛 Date of Disburse 落在目标月的行 →
   展开成客户级名单(tab 名里 `/` 分隔的是同案多客户,**每个都算一位**;`✅` 前缀要剥掉)。
   **去重坑**:中间名(`Yuran Zhou` vs `Yuran N Zhou`)会打断精确匹配 → 模糊比对。
3. **对账台账**:名单里在 `回收台账` 找不到行的客户 → **漏登记**,直接算 U0(未问),点名 CM。
4. **读 Google 页面**(公开页,不用登录;用浏览器工具打开 Google 页面 → 按最新排序 → 读出
   评论人显示名 / 星级 / 日期 / 正文):
   - 数出**目标月新增评论数**、累计数、平均星级。
   - 逐条比对台账 M 列显示名 → 匹配上的确认 K=✅已评论;**Google 上有、台账没记** → 回填台账
     (客人自己发的,照样算数);**台账记了✅、Google 上找不到** → 标疑问,让 CM 拿截图,
     否则改回 ⏳(客人可能删了或没真发)。
   - 一行写进 `Google评论对账` tab。
   - ⚠️ Google 显示名常和案件英文名不一样(昵称/拼音/中文名)→ 匹配靠 CM 当场记的 M 列,
     实在对不上的列进「待确认」,不要硬猜。
5. **算数**(`月度结算` 目标月行 B–J 是公式,自动出;缺行就补一行,A 列 RAW 写月份)。
6. **产出中文报告**(见下),Klaus 看完在 K 列写裁定。
7. **复盘条目**:每个 D 类 + 每个 U0 各生成一条复盘项(客人 / CM / 原话 / 卡在哪个环节 /
   建议动作),D3(沟通不到位)按红线级处理。可直接喂给 `团队复盘` 当周一材料。
8. 收工:Activity Log append 一行 —— Category `客户`,Source `Manual`,
   `manual:客服回收`,Ref = `<YYYY-MM> 满意度结算`。

### 月度报告格式
```
📊 <YYYY-MM> 客户满意度回收

结案客户 N 位 · 已评论 X 位 · 未评论 Y 位
Google 页面:本月新增 Z 条 · 累计 T 条 · 平均 R★
系统初判:<🟩/🟨/🟧/🟥 + 一句话>

未评论名单
1. <Client> · <CM> · <原因码 说明>
   客人原话:「……」
2. …

⚠️ 需要复盘(D 类 / U0)
· <Client> — <卡在哪个环节> → <建议动作>

📋 等 Klaus 裁定
· <这个月判 达标 / 达标(有观察项) / 不达标>,写进 月度结算!K<行>
```

---

## 红线(照抄给团队,`话术` tab 最后一行)
1. **不许用钱、礼品、减费、折扣换评论** —— 违反 Google 政策,页面可能被下架。
2. **不许代客人发布**、不许用律所手机或帐号发 —— 必须客人本人发布。好评工具只生成文案。
3. **不许只挑满意的客人请求**(review gating)—— 每个结案客人都要请;不满意的照样请,不发就记原因。
4. **不许在评论里出现赔偿金额、保险公司名、伤情细节** —— 客人自己愿意写是他的事,我们不引导。
5. 客人说不满意时**不许辩解、不许当场解释** —— 只记原话,交给 Klaus。

## 边界
- 只 **append / 更新**台账,**永不删行**;写错了在 S 列写更正说明。
- **不裁定达标**、**不动奖金表** —— 奖金联动由 Klaus 拍板,系统只提供事实和原因。
- 不发邮件、不发 Chat、不改 Google 页面。报告出在 session 里。
- 客户名一律英文原名。

## 当前状态(2026-08-31 建成)
- `2026-08` 已回填 **26 位** disburse 客户(来自 Completed Disbursed `🔍 Search`),全部 K=`❓未问` →
  初判 🟥。**8 月是上线基线月,不作为考核月**(已写在 月度结算!L2)。
- 其中 **8/20 之后交付的 12 位仍可追补请求**(台账 S 列标了 `🔔 可追补`)。
- `Dacheng Xu`(8/20)在 Master 的 Claims@ 和 Piteam@ **都有**,团队=`待确认`,要 Klaus 定。
- **2026-09 起正式跑**。表还没共享给团队 —— 共享范围由 Klaus 定。

## 相关
`case-settles`(Phase 7 建行)· `团队复盘`(D 类进周一材料)· `bonus-records-system`(结案月同一数据源)
