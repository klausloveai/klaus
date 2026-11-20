---
name: weekly-meeting-wecom
description: 车祸部门周二周会的企业微信会议流程：会前确认会议在、会后从企微取智能纪要+逐字稿，整理成周会记录，并按案件拆出待办，在 Klaus 确认后记进凌图数据、案件 Activity Log 和工作台。Klaus 说「收周会纪要」「取这周的周会纪要」「周会开完了」「/weekly-meeting-wecom」时用；会前出稿仍是「跑这周的周会」（weekly_partner_meeting 规格）。只在装了 wecom-cli 且已授权的 Mac Mini 上可用。不往企微群发消息、不以 Klaus 身份发任何消息、不建定时任务。
---

# 车祸部门周会 × 企业微信会议

**状态：草稿（2026-11-20）。wecom-cli 授权和三项实测完成前，第 2、3 步的命令和字段以实测为准。**

周会：每周二 11:30–12:30 PT（11/20 起；企微周期会议「车祸部门周会」已由机器人建好，52 场），Klaus 主持，Cassie、Joe 出席。周会内容只报三项：本周新案数、结案数、要处理的案子（见 memory `weekly_partner_meeting.md`）。本技能归「岗位编制 · Roles」section（local_df494bee）触发。

## 0. 前置检查（每次先做）

1. `wecom-cli auth show` 必须是 authorized。不是 → 停下，告诉 Klaus 要扫码：Klaus 在场时才运行 `wecom-cli auth init --noninteractive --no-browser --output-qrcode <scratchpad>/wecom_qr.png`（后台跑），二维码**生成后立刻** SendUserFile 给他，5 分钟过期。
2. 先读 `wecomcli-shared` 和 `wecomcli-meeting` 技能（官方要求，命令参数以它们的 references 为准）。

## 1. 会议本身（一次性设置，之后每周自动有）

- 周会从 Zoom 改用企微会议（Klaus 11/20 定）。建成一个**每周二的周期腾讯会议**（企微会议），参会人 Klaus、Cassie、Joe。**只建一次。**
- 谁建：Klaus 在企微客户端自己建；或 Klaus 点头后由 Claude 用 `wecomcli-meeting` 的 create（recurrence weekly、TU）建。**建会会给参会人发邀请，必须先问 Klaus。**
- 当面开会也要开这场线上会议：Klaus 用一台设备（电脑或手机）入会，放在会议桌上收音。**没有入会，就没有纪要和逐字稿**，CLI 只能读线上会议的。

## 2. 开会时（Klaus 做，10 秒）

1. 准时入会（会议发起人最好是 Klaus：CLI 只能读自己发起或参加的会）。
2. 会议里打开「转写」和「智能纪要」（腾讯会议工具栏 → 转写 / AI 小助手；具体按钮名以实测为准）。
3. 会议结束后等几分钟，让企微生成纪要。

## 3. 会后取纪要（Klaus 在岗位编制 section 说「收周会纪要」）

1. **定位**：`meeting list` 拉今天的会（**CLI 时间按北京时间**：PT 周二 11:30 = 北京周三 03:30，时间窗要换算）（周期会议要拿当场的 `sub_meeting_id`），按主题和时间核对是这次周会。找不到 → 说明查询范围，不猜。
2. **取纪要**：`meeting get` → `notes[].note_content`（纪要）、`notes[].todo_content`（待办）；`has_note_permission=false` 或为空 → 说明，改用逐字稿。
3. **取逐字稿**：`meeting original get`，翻页到 `has_more=false`，按顺序拼接。
4. **存档**：逐字稿原文 + 智能纪要原文存成 `<M-D-YYYY> 车祸部门周会 逐字稿.md`，上传到周会笔记 Doc（`1tQ7Pk7lNWLPsoOtXvAyPp1TnFry5_F2tKBkTyzJdXlQ`）所在的 Drive 文件夹下的「逐字稿」子文件夹（没有就建）。本地副本放 `~/Downloads/任务总盘/周会/`，上传后比 MD5、移废纸篓。
5. **整理周会记录**（交 Klaus，不直接写 Doc）：纯文本、对齐缩进、不用 markdown 表格，标题 `M/D/YYYY`，出席 Cassie、Joe，Klaus 主持。三块：新案 · 结案 · 要处理的案子；再加一块「会上决定 / 待办」（谁 · 做什么 · 期限）。**人名、金额、日期一律以逐字稿为准**，AI 纪要和逐字稿不一致的地方标出来。
6. **按案件拆待办**：每条待办先 `find` 客户名拿 `matter_code`（同名或多案按 DOL 列给 Klaus 选）。列一张表给 Klaus：案件 · 编号 · 待办 · 负责人 · 期限 · 要写到哪（凌图数据 / 案件 AL / 工作台 next_step / 日历）。

## 4. Klaus 确认后再写

Klaus 说「写」或逐条勾选后，对每个案子：
- 凌图数据 `log_event`（类型 note 或 律师指示，摘要带 `[s:<session前8位>-<序号>]`）；
- 案件 intake 表的 `Activity Log` subtab（`al.py read` → `al.py append`，按 CLAUDE.md 案件 AL 规则）；
- `sync_case_status`：更新 `next_step` / `next_step_owner` / `deadlines`（我们自己定的跟进日 `hard=false`）；
- 有日期的期限 → 按日历规则建带时间的事件（9:30 + popup，Free）。
- 周会记录文本交给 Klaus 贴进 Doc；他说「写 Doc」才由 Claude 写。

收尾报告：周会记录已交 · 案件 AL +N 行 · 凌图数据 +N 条 · 工作台改了哪几张卡 · 日历 +N · 逐字稿存在哪。

## 不做

- 不往企微群 / 客户群发任何消息（CLI 的 message 能力不用）。
- 不以 Klaus 身份发邮件或企微消息；要通知同事，起草给 Klaus 看。
- 会后取纪要不建定时任务（说「收周会纪要」才跑）；会前大纲由定时任务 `weekly-meeting-agenda`（周一 15:00，Klaus 11/20 定）自动出。
- 不把纪要里没有核实的数字写进系统。
