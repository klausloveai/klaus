---
name: case-artifact
description: >-
  Build or update the single-page CASE ARTIFACT for a 凌图律所 / Law Office of Shenqi Cai APC
  litigation case — a private claude.ai page that holds the whole file at a glance: docket
  block, where the case stands, what is blocked and on whom, the discovery matrix, parties
  and counsel, the incident, treatment, damages with the arithmetic shown, the Bates index,
  the watch list, the timeline, and where the documents live. Use whenever Klaus asks for a
  case page, a case dashboard, a case summary artifact, "案件底稿", "案件 artifact",
  "做一个 <客户名> 的 artifact", "给 <客户名> 建一页", or "/case-artifact <客户名>". Also use
  to UPDATE one: read the published page back and edit it, never rebuild from memory.
  READ-ONLY on the case record — it drafts nothing, serves nothing, and changes no Drive file.
---

# case-artifact — 一案一页

Goal: **一屏之内看懂这个案子现在卡在哪。** 不是档案清单，是工作底稿。
Klaus 不手动翻 Drive，他看这一页，所以页面错了等于他的判断就错了。

参照实现：**Yi Cong v. Rhea Edpao**（CIVSB2619725），2026-10-13 建。

## 死规矩 —— 先读这一段

1. **没核过的事实不写。** 宁可整节留白，也不要写一个"大概是这样"的数字。
   Yi Cong 那页就没写 CIV-050 上的 general damages、没写 Healthier Minds 第四次就诊的日期、
   没写事发时间 —— 因为都没核。页面的价值全在"上面写的每一条都能信"。
2. **每一个算式自己跑一遍。** 不要照抄文书里的结果就当它对。Yi Cong 的误工数跑出来是
   $21,084.08，送达文书写的是 $21,083.51 —— 差五十七分。**差额不改（那是已宣誓的数字），
   但要在页面上写明**，否则三个月后有人重算会以为账错了。
3. **负面结论要带前提。** 写"目前没有任何证据证明 X"之前，说清楚查了什么、查到哪天、
   盲区在哪。空搜索不等于不存在。
4. **当事人名、律所名、法院名一律英文**；正文中文；legal term 与法条判例保持英文。
5. **draft-only / read-only。** 这个 skill 只读案卷、只发 artifact。不改 Drive 文件、
   不起草文书、不发邮件。
6. **artifact 默认私有**，不要替 Klaus 分享。

## 数据源，按权威顺序

| 要什么 | 去哪拿 | 注意 |
|---|---|---|
| 案件在不在、stage、主办律师 | Tracking Sheet `0. Tracking Sheet` → **`All Cases`** 页 | 权威源。`#N/A` 行和 `Client Name` 模板行要剔掉 |
| 当事人、DOB、地址、保险、雇主 | 该案 intake sheet | |
| 本案流水 | 该案 **Case Log**（intake sheet row 30/31） | |
| 所内动作流水 | Tracking Sheet → `Activity Log`，按 Case 列筛 | 本 skill 自己也往这里写一行 |
| 已送达/已立案文书 | Drive case folder `4.1`–`4.6` | **文件名是人写的，只信内容**：开 PDF 核标记（Bates 末号、金额、签名页） |
| docket 实况 | 法院 portal | LASC 与 San Bernardino 的 **CAPTCHA 必须 Klaus 点**，见 `[[sb-court-access-portal]]` |
| 对方律师、送达名单 | 对方 POS 的 SERVICE LIST + 我方已发送达邮件的收件人 | 两边对一下 |
| 治疗与账单 | 案卷 medical 子夹 + lien 通知 | 金额要加总核对 |

## 工作流

0. **先定是新建还是更新。**
   - 更新：`Artifact` `action:"read"` 把已发布页面取回来（它就是源），剥掉发布骨架，改完再发。
     **绝不凭记忆重建** —— 会悄悄丢掉上一轮核实过的细节。
   - 新建：往下走。
1. **在 `All Cases` 里确认这个案子存在**，取 stage、attorney、date。查不到就停下问 Klaus。
2. **把案卷读一遍**，按上表。读的时候同时记下"哪些字段没核到" —— 那是最后要留白的地方。
3. **跑算术**：医疗费分项加总 = SOD 医疗费？误工算式复算一遍？specials 合计对不对？
   对不上就把差额写进页面，别抹平。
4. **列 blocker**：每一条都要能回答"卡在谁身上"。分三栏：等律师 / 等客户 / 等所内。
   没有 blocker 的案子，这一节写"当前无阻塞"，不要硬凑。
5. **按 `references/sections.md` 逐节写。** 节次固定，内容按案子裁剪；
   该案没有的节（比如还没 discovery）整节删掉，不要留空壳。
6. **套 `assets/shell.html`**，替换 `{{TITLE}}` `{{CAPTION}}` `{{EYEBROW}}` `{{SUBTITLE}}`
   `{{DOCKET}}` `{{CHIPS}}` `{{ATTORNEY}}` `{{SECTIONS}}`。CSS、配色、字体、倒计时脚本都在 shell 里，不要改。
7. **发布前自检**（照做，不要跳）：
   ```
   node --check <(sed -n '/^<script>/,/^<\/script>/p' page.html | sed '1d;$d')
   grep -nE '#[0-9A-Fa-f]{6}' page.html | grep -v '\-\-'      # 正文里不该有写死的颜色
   ```
   再人眼过一遍：有没有 emoji（design system 禁用）、有没有没填的占位符。
8. **发布**：`Artifact` publish，`icon:"folder"`，一句话 `description`。更新时带 `url`。
9. **记台账**：Activity Log 一行，`Category` = 起草，`Ref/ID` 里放 **artifact 的 url**，
   这样三个月后搜得到。

## 页面结构

十一节，顺序固定。详见 `references/sections.md`。

1. **masthead** —— docket 块，**全英文**（它对应法院 caption）
2. **案件现状** —— 分析，不是罗列；配倒计时卡片
3. **待办与阻塞** —— 按"卡在谁身上"分三栏
4. **Discovery 进度** —— 矩阵 + 对方这套到底问了什么
5. **当事人与律师** —— 含送达地址
6. **事发经过** —— 事实 + 机关记录 + 责任基础
7. **伤情与治疗** —— 机构 / 诊治 / 日期 / 金额
8. **损害赔偿** —— SOD 分项 + 算式摊开
9. **文书产出** —— Bates 索引
10. **风险点** —— 每条写清"会怎么咬到我们"
11. **关键日期** —— 时间线，含未来
12. **文件位置** —— Drive 文件夹对照

## 设计

凌图 design system v1 的 token 原值照用（shell 里已写死，附来源注释）：
ink `#1C1917` / parchment `#F2EDE2` / paper `#FFFDF8` / gold `#C0A260` /
deep gold `#A8862F` / hairline `#E6DFD1` / row tint `#FAF6EC`。

- 中文标题宋体、正文黑体、拉丁字 Raleway、案号与 Bates 走 JetBrains Mono
- 金色只做 1px 细线、眉标、数字 —— **绝不填面**
- 边框一律 1px（规格里 2px 只留给"选中的列表行"）
- **不用 emoji**，一个都不行
- deep gold `#A8862F` 在羊皮纸底上是 2.94:1，低于 4.5。这是 design system 自己的 token，
  Klaus 2026-10-13 明确要求以品牌为准 —— 照用，不要自作主张压深

## 跨案导航

试过在页顶加全部案件的 tag 条，**Klaus 2026-10-13 让撤掉了**，不要再加。
真要做跨案跳转，问清楚再动：artifact 之间不能共享文件也 fetch 不到彼此，
每加一个案子就要把其余所有页面 republish 一遍，必须由脚本从 `All Cases` 生成，不能手写。
