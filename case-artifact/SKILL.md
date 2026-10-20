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

> **PI 车祸案（诉前）不走本 skill** —— 用 `pi-case-artifact`，模板与登记表完全分开（Klaus 2026-10-20）。

Goal: **一屏之内看懂这个案子现在卡在哪。** 不是档案清单，是工作底稿。
Klaus 不手动翻 Drive，他看这一页，所以页面错了等于他的判断就错了。

参照实现：**Yi Cong v. Rhea Edpao**（CIVSB2619725），2026-10-13 建。v7 组件的假数据样张：`assets/sample-7.0.html`（只看版式，别抄内容）。

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
   `{{DOCKET}}` `{{CHIPS}}` `{{STAGE}}` `{{DOL_ISO}}` `{{ROAD}}` `{{ATTORNEY}}` `{{SECTIONS}}`。
   CSS、配色、字体、倒计时与状态条脚本都在 shell 里，不要改。
   **状态条只填「阶段」和事发日**；距事发天数、待办条数、寄件在途、下一期限全由脚本从正文数出来 ——
   不手写数字，所以正文一改条子自动跟着对。
   **每一节都写成可折叠**（Klaus 2026-10-14 要求），固定形状：

   ```html
   <section>
     <div class="rule"></div>
     <details class="sec" open>          <!-- open 只给默认展开的那两节 -->
       <summary><h2>标题<small>English</small></h2></summary>
       ...内容...
     </details>
   </section>
   ```

   **默认展开：关键期限 + 待办与阻塞；其余全部收起。** 一开页面就是「一屏看完卡在哪」，
   其余按需点开。用原生 `<details>`，不加 JS —— 倒计时脚本在页面加载时就把收起的节也算好了。
8. **发布前自检**（照做，不要跳）：
   ```
   node --check <(sed -n '/^<script>/,/^<\/script>/p' page.html | sed '1d;$d')
   grep -nE '#[0-9A-Fa-f]{6}' page.html | grep -v '\-\-'      # 正文里不该有写死的颜色
   ```
   再人眼过一遍：有没有 emoji（design system 禁用）、有没有没填的占位符。
9. **发布**：`Artifact` publish，`icon:"folder"`，一句话 `description`。更新时带 `url`。
10. **不记 Activity Log。**（2026-10-19 起，见 CLAUDE.md「收工留痕」）artifact 的建立与更新自带版本历史，
   页面 url 由 `assets/applied.json` 登记；台账只记别处没有痕迹的事。这一步原先要求「记一行、Ref 放 url」，已作废。

## 收工增量同步（默认，不等 Klaus 开口）

Klaus 2026-10-15 定：**每个 session 里做完的案件动作，凡记进 Activity Log 的，同一收尾里同步到该案 artifact。**
（规则本体在 `~/.claude/CLAUDE.md`「收工同步 Case Artifact」。）

1. `assets/applied.json` 查案名 → url；没有就 `Artifact list` 按标题找，找到补登记。该案没页面 → 跳过，不新建。
2. `Artifact read` 带 `path:"index.html"` 存盘 —— **用线上最新版，不用本地旧稿**（别的 session 可能改过，例如加了折叠）。
3. 只做定点替换（Python 每处 `assert count==1` 再替换），只碰受影响的节：期限、待办与阻塞、时间线、文件位置、风险点。不重排、不重写其他节。
4. publish 回同一个 url（`label` 写一句改了什么），更新 `applied.json` 的 `updated`。
5. 收尾一句话报告改了哪几节。未核实的金额/专科/结论不写。

## 版本与同步 —— 模板怎么迭代

**shell 是唯一标准。** 在某个案子页面上试出来的改动，**回写进 `assets/shell.html`
（样式）或 `references/sections.md`（结构）之前，等于没发生** —— 下一个新案子不会有它。
2026-10-14 的待办编号就是这么差点丢掉的。

```
在某个案子页面上试改 → 满意了回写 shell / sections.md，版本号 +1
                   → 其他案子下次打开时刷过去
```

### 版本号

`shell.html` 的 `<div class="wrap" data-shell="X.Y">`，每个生成的页面都带着它当时的版本。

- **小版本（Y）= 只动样式**（CSS、脚本、默认折叠状态）→ `scripts/reskin.py` 全自动
- **大版本（X）= 动了正文结构**（节的顺序、新增节、编号规则）→ 脚本刷不了，要逐页人工改

`assets/applied.json` 记每个案子页面刷到了哪一版。**查它不用打开任何页面。**

### 刷新一个页面

```bash
# 1) 把页面存到磁盘 —— Artifact read 带 path（action:"read", url, path:"index.html",
#    out_dir:<scratch>），40 KB 的 HTML 不会进对话，只回一行
# 2) 看要不要刷
python3 scripts/reskin.py --check <scratch>/index.html
# 3) 刷（只换 <style>/<script>/版本戳，正文不动）
python3 scripts/reskin.py <scratch>/index.html
# 4) publish 回同一个 url，更新 applied.json
```

存盘那一步是省 token 的关键。所以刷十个案子和刷一个案子，成本差别很小。

### 什么时候刷

**默认懒加载 —— 不要主动全量刷。** 下次打开某个案子要动它的页面时先 `--check`，
旧了就顺手刷掉再干活；没碰到的案子放着不管。Klaus 明确要全量时才一次扫完。

**注意**：从服务端取回的页面带着一层发布骨架（到 `<title>` 为止，约 530 字节）。
publish 之前切掉，从 `<title>` 开始，否则会套两层。

## 页面结构

shell 7.0（2026-10-15）起：masthead + 十五节，顺序固定。详见 `references/sections.md`。
**每节都包在 `<details class="sec">` 里。**

1. **masthead** —— docket 块，**全英文**（它对应法院 caption）；chips 里放一个 `Drive 案卷` 链接；
   其下 **状态条**（阶段 / 距事发 / 待办 / 寄件在途 / 下一期限）+ **路线图**（一行轨道，标「现在」）
2. **待办与阻塞** —— 按"卡在谁身上"分三栏，**三栏共用一套连续编号**（Klaus 用号码点事：
   「办 9」）· *默认展开* · **排在最前面**：他打开页面第一眼要看的是现在卡在谁身上，
   不是案情叙述。v7 起每条带一行 `.meta` **出处**：来源（哪封邮件第几项 / 哪条法条 / 客户哪天微信）·
   负责人 · 期限 —— 三个月后能追回这件事是谁、凭什么布置的
3. **关键期限** —— 倒计时，**一行一条**（`.dls`），不要方框卡片 · *默认展开*
4. **案件现状** —— 分析，不是罗列；v7 起加 **分岔口**（路线图上标虚线的那几步，各自的触发条件与依据）· *默认折叠*
5. **Discovery 进度** —— 矩阵 + 对方这套到底问了什么
6. **寄件追踪** —— *v7 新增*：USPS Certified Mail 一封一行，状态 chip，签收后算回复期限并进「关键期限」
7. **客户材料** —— *v7 新增*：待补 / 已收两栏；待补项若已列进待办，写「见待办 N」，不重复展开
8. **当事人与律师** —— 含送达地址；v7 起保险、房东、政府机构也列；**身份未核实的一律 `.chip.due 身份未明`**
9. **事发经过** —— 事实 + 机关记录 + 责任基础
10. **伤情与治疗** —— 机构 / 诊治 / 日期 / 金额
11. **损害赔偿** —— SOD 分项 + 算式摊开；**误工案加每周收入堆叠柱 `.bars`**（必须配明细表）
12. **文书产出** —— Bates 索引
13. **供应商订单史** —— One Legal 全部订单：order / 递交 / 内容 / 结果 + court transaction #
14. **风险点** —— 每条写清"会怎么咬到我们"；v7 起卡片顶上一个 chip 定级：要处理 / 留意 / 已解决，按此顺序排
15. **关键日期** —— 时间线，含未来
16. **文件位置** —— Drive 文件夹对照

该案没有的节整节删掉，不要留空壳。

## 设计

**三级表面，别弄混**（Klaus 2026-10-14 定）：

| 层 | 颜色 | 用在哪 |
|---|---|---|
| 底 | `--ground` `#F2EDE2` | 页面背景 |
| 面板 | `--paper-tint` `#FAF6EC` | 每一节 `.sec`，让正文不直接压在底色上 |
| 卡片 | `--paper` `#FFFDF8` | 面板内的 `.card`、`.tw` 表格、`.bls .it` 待办行、`.dls .dl` 期限行、`.note`、`.calc` |

新加任何块状元素，先想它属于哪一层 —— 同层叠同层就会糊成一片。

凌图 design system v1 的 token 原值照用（shell 里已写死，附来源注释）：
ink `#1C1917` / parchment `#F2EDE2` / paper `#FFFDF8` / gold `#C0A260` /
deep gold `#A8862F` / hairline `#E6DFD1` / row tint `#FAF6EC`。

- 中文标题宋体、正文黑体、拉丁字 Raleway、案号与 Bates 走 JetBrains Mono
- 金色只做 1px 细线、眉标、数字 —— **绝不填面**
- 边框一律 1px（规格里 2px 只留给"选中的列表行"）
- **不用 emoji**，一个都不行
- deep gold `#A8862F` 在羊皮纸底上是 2.94:1，低于 4.5。这是 design system 自己的 token，
  Klaus 2026-10-13 明确要求以品牌为准 —— 照用，不要自作主张压深

## v7 的来历 —— 哪些从 Joe 教程拿、哪些故意没拿

2026-10-15 Joe 群发《Claude 案件页制作指南》（artifact `V7H5i4wpvjv4vPUdCJkRD6`）。
两边合并取长，结果就是 shell 7.0：

- **拿了**：状态条（距事发 / 待办 / 在途 / 下一期限）· 路线图「现在」标记 + 分岔口 ·
  待办的出处行 · 寄件追踪 · 客户材料清单 · 风险三级定级 · 当事人身份未明标红 ·
  误工周收入堆叠图 · masthead 的 Drive 案卷链接
- **没拿，别再加回来**：
  - **页面数据库（artifact-capabilities db）**。本 skill 的更新流程是「read 回页面 → 定点替换 → publish」，
    加上 `applied.json` 版本登记与 `reskin.py`；数据进了 db 这三样全失效。真要改，先问 Klaus
  - **路线图的百分比可能性**。死规矩 1：没核过的不写；走向是律师判断，只写分岔口的触发条件与依据
  - **深色封面**、"我的风格"式自由生成 —— shell 是唯一标准
  - **每日 USPS 无人值守定时任务**默认不建；Klaus 要时再建，且只读不发

## 跨案导航

试过在页顶加全部案件的 tag 条，**Klaus 2026-10-13 让撤掉了**，不要再加。
真要做跨案跳转，问清楚再动：artifact 之间不能共享文件也 fetch 不到彼此，
每加一个案子就要把其余所有页面 republish 一遍，必须由脚本从 `All Cases` 生成，不能手写。
