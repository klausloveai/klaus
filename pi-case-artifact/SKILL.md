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
- 页面是**视图**：待办由底层推出，每条写「怎么关掉」（改 Master / Chat 里说 / 文件进 Drive）。页面上不能改。
- 数据源：Master Sheet 该行（按表头名取列）· intake（含 Treatment Cost）· 案件 Chat 全部消息 · Drive 案卷树。
- 没核过的不写；负面结论写明查了什么、没查什么（邮箱默认未读要写出来）。
- 金额每一笔自己复算；跨源对不上的写进待办或风险点。
- 顶栏 docket：Client · DOL · Tortfeasor · 1P/3P Claim # · **Team** · **负责人**；眉标「凌图律所 · PI Case」。
- 不放 SSN / 驾照号。

## 节次（2026-10-20 版）
关键期限 → 关键日期（时间线，默认展开）→ **任务**（默认展开，三块）→ 案件现状 → 治疗与账单 → Lien 与自付 → 保险与理赔 → 事发经过与财产损失 → 当事人与团队 → 文件位置 → 这一页怎么来的。

**任务节三块**（Klaus 2026-10-20 定，取代旧的「待办与阻塞」+「风险点」）：
1. **已完成**：表格 日期 · 完成了什么 · 谁 · 详情/凭据（从 Chat 与 Drive 抽，按日期升序）。
2. **待办**：每条一个 `<details class="todo">`，标题行写事项 + 负责人 · 时限；点开是「为什么 → 怎么做（编号步骤）→ 关掉条件」，相关的官方教程附链接（如 PI Master Sheet 记录教程 Doc `1X0Q0IR…`）。编号连续，供「办 N」点名。
3. **预防**：`<details class="todo prev">`，编号 P1…，写「会怎么出事 → 现在先做什么」。不计入状态条的待办数。

模板结构仍在迭代中（以 Andrew 页为准），定稿后再把节次规范写进 `references/`。
