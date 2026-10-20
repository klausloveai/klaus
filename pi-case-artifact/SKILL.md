---
name: pi-case-artifact
description: >-
  Build or update the read-only CASE PAGE for a 凌图律所 PI auto (车祸, pre-litigation) case — a private
  claude.ai artifact derived from the PI Master Sheet row, the case intake sheet (incl. Treatment Cost tab),
  the case Google Chat space, and the Drive case folder. Use for "PI 案件页", "车祸案 artifact",
  "给 <客户名> 做 PI 案件页", "/pi-case-artifact <客户名>". NOT for dog-bite / Hernán litigation cases —
  those use `case-artifact`. READ-ONLY: drafts nothing, sends nothing, changes no source.
---

# pi-case-artifact — 车祸案一页

**与 `case-artifact`（狗咬 / 诉讼）完全分开**（Klaus 2026-10-20 定）：模板、登记表、版本号各管各的。
那边的 shell 改动或 `reskin.py` 不得碰本目录登记的页面，本目录的改动也不回写那边。

- 模板：`assets/shell.html`（版本 `data-shell="PI-1.0"`，2026-10-20 从 case-artifact shell 7.0 分叉）
- 样板：`assets/sample-andrew-yi-chen-lin.html`（Andrew Yi Chen Lin-6-27-2026，唯一基准案；
  Ruijie Yan / Weicheng Hu 两版已弃用，不再维护）
- 登记：`assets/applied.json`（案名 → url）

## 页面原则
- **事故经过以警方报告为准**（Drive 2# 的 police report，扫描件要渲染成图片读 Narrative 页），intake 的 Fact of Loss 只作参考；两者不一致时页面按报告写，并生成「改 intake」待办。Andrew 案就是 intake 写右转、报告写左转（CVC 22107）。
- **期限节与时间线节底部各放一行 `.src` 来源说明**：期限 = Chat 里的预约与 snooze + DOL 推算的法定时效（Master/intake 目前没有期限栏）；时间线 = 警方报告 + Chat 消息日期 + Master 治疗列 + Drive 上传时间。
- 页面是**视图**：待办由底层推出，每条写「怎么关掉」（改 Master / Chat 里说 / 文件进 Drive）。页面上不能改。
- 数据源：Master Sheet 该行（按表头名取列）· intake（含 Treatment Cost）· 案件 Chat 全部消息 · Drive 案卷树。
- 没核过的不写；负面结论写明查了什么、没查什么（邮箱默认未读要写出来）。
- 金额每一笔自己复算；跨源对不上的写进待办或风险点。
- 顶栏 docket：Client · DOL · Tortfeasor · 1P/3P Claim # · **Team** · **负责人**；眉标「凌图律所 · PI Case」。
- 不放 SSN / 驾照号。

## 顶栏联系卡（Klaus 2026-10-20 定）
masthead 里 chips 下方、状态条上方，`{{CONTACTS}}`：左 1P、右 3P 各一张卡，每张是 `<details class="ct" open>`，点卡头可收起。**卡下不放角色图例**，角色只标在 adjuster 姓名后。卡头 = 保险公司 + Claim #；
每位 adjuster 一行：姓名 + **角色标签**（BI / PD / Med Pay / Total Loss / Subrogation / Supervisor，未标的用红色「角色未标」）
+ Phone（含分机）· Email（总邮箱注明「总邮箱」）· Fax（没有写「无记录」）。电话邮箱用纯文本（可全选复制），不用 tel:/mailto:。
数据取 intake 1st/3rd Party 栏；角色只认 intake 括号里写明的（如 (T/L) (B/I)），不推测。缺的就生成一条「补齐 adjuster 角色/传真/supervisor」待办。

卡内保单栏照 intake 架构：1P = Policy # · Period · Coverage · Liability · UM/UIM · Med Pay · Collision Ded · Rental；
3P = Policy # · Insured · Driver · Period · Coverage · Liability · Limits · PD。limits、UM/UIM 这类**只属于一方的事实放进该方卡里，不放顶部 chips**。

**状态字段照 Master 走**（Klaus 2026-10-20）：1P 卡放 G 1LOR · H 1Coverage · I 1Liability；3P 卡放 J 3LOR · K 3Coverage · L 3Liability；
M Property Damage 放进实际理赔的那一方（Andrew 案 = 3P）。每格显示「Master 原值 + 色块（`.ms.y/.dy/.b/.g/.o/.gr`，照抄 Master 底色）+ 教程里的含义」，
读取时用 Sheets API 取 `effectiveFormat.backgroundColor`，含义查《PI Master Sheet 记录教程》（Doc `1X0Q0IR…`，第三节逐列表格）。卡片下方一行 `.src` 注明来源。

## 字体（Klaus 2026-10-20 选 B）
拉丁字与数字 **Source Sans 3**（与思源黑体同族，等高数字），等宽 **Source Code Pro**，中文正文 Noto Sans SC、中文标题 Noto Serif SC 不变。
不用 Raleway（老式高低数字）和 Cormorant 斜体。所有数字列加 `lining-nums tabular-nums`。

## 顶部 chips
**只放四个链接，顺序固定：Master Sheet · Chat 群 · Drive 案卷 · Retainer**（Retainer 链到 Drive 1# 已签合同 PDF）。Liability、PD 等状态不放顶部，进 1P/3P 卡。**Retainer 着色：Standard = 橙（`.chip.ret-std`）、New = 蓝（`.chip.ret-new`）。**

## 节次（2026-10-20 版）
**期限与时间线**（一节两栏：左关键期限精简行+较多 memo，右时间线新的在上、限高滚动）→ **任务**（默认展开，三块）→ 案件现状 → 治疗与账单 → Lien 与自付 → 保险与理赔 → 事发经过与财产损失 → 当事人与团队 → 文件位置 → 这一页怎么来的。

**任务节三块**（Klaus 2026-10-20 定，取代旧的「待办与阻塞」+「风险点」）：
1. **已完成**：表格 日期 · 完成了什么 · 谁 · 详情/凭据（从 Chat 与 Drive 抽，**新的在上**）。表上方 `[data-tally]` 由脚本按「谁」列计数（共 N 件 · 每人几件 · 未注明几件），供以后统计贡献。
2. **待办**：双栏网格；每条标题下写「起于 <日期+起因> · N 天前」（`data-opened`，脚本算天数），久拖的标红「拖得久」，可能已经办掉的标绿「可能已办」并在展开内写「判断：…」。每条一个 `<details class="todo">`，标题行写事项 + 负责人 · 时限；点开是「为什么 → 怎么做（编号步骤）→ 关掉条件」，相关的官方教程附链接（如 PI Master Sheet 记录教程 Doc `1X0Q0IR…`）。编号连续，供「办 N」点名。
   「谁」= Chat 里报告该动作的发言人；【Claude AI】通知记转发人；Chat 没写就标「—」，不按角色推测。表下放一行 `.src` 说明。
   **所内同事一律只写 first name**（Tiana、Claire、Amos…），律师写全称 Shenqi Cai, Esq.，外部 adjuster 写全名。
3. **预防**：`<details class="todo prev">`，编号 P1…，写「依据（触发它的本案数据 + 通用规则）→ 会怎么出事 → 现在先做什么」。生成法：拿本案数据对照对方常用的压价理由清单（影像与治疗不相称、既往伤、限额、治疗空档、身份错误、材料缺失、lien 未定、比较过失），有事实触发才列。不计入状态条的待办数。

模板结构仍在迭代中（以 Andrew 页为准），定稿后再把节次规范写进 `references/`。
