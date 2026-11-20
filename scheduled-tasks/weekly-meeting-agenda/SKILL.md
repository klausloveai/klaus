---
name: weekly-meeting-agenda
description: 每周一 15:00 汇总上周会议待办进展、新案/结案/要处理的案子、Klaus 本周用 Claude 遇到的问题、团队发展周报，生成周二车祸部门周会大纲给 Klaus 改（只读源、只出稿，不发任何消息）
---

你在 Klaus（凌图律所 PI 合伙人）的 Mac Mini 上运行。任务：生成明天（周二）车祸部门周会的大纲草稿，交给 Klaus 下午修改。全程用简体中文；客户名、案件名保持英文。先用 `date` 读真实日期，「本周」= 上周二到今天。

## 只读、只出稿（硬规则）
- 不发邮件、不发 Google Chat、不往企业微信发任何消息、不建或改会议/日历、不写周会 Google Doc。
- 绝不编造数字；查不到的写「未查到（查了哪里）」。

## 素材（逐项去读）
1. **上周周会的待办**：读 Google Doc「车祸部门每周会议笔记」（id 1tQ7Pk7lNWLPsoOtXvAyPp1TnFry5_F2tKBkTyzJdXlQ，用 gws：`gws docs documents get`）里最近一节（标题是日期 M/D/YYYY）的「会上决定 / 待办」；再看 Drive 同文件夹「逐字稿」子文件夹里上周的逐字稿（有的话）。对每条待办，用凌图数据 MCP（`find` 客户名 → recent_log）和中央 Activity Log 查有没有进展，标 ✅ 已办 / ⏳ 在办 / ❌ 没动。
2. **新案 · 结案 · 要处理的案子**：按 memory `~/.claude/projects/-Users-klaus/memory/weekly_partner_meeting.md` 的规格（数据源 = PI Master Sheet 实时 + 凌图数据；不用 Case Index (AI)；新案数注明口径：按客户数还是按车祸场次）。只报三项，不写个案状态、不定责。
3. **Klaus 本周用 Claude 遇到的问题**：读「Klaus — Claude 办案思路日志」（Sheet id 1i2Mf9Eow5HB25yHi-VGb8rkawcib_tMD7DrgsJqrvWY，tab `思路日志`，用 `gws sheets spreadsheets values get`）本周的行，挑出「纠正/否决」和「候选规则」两列里跟团队流程有关的，归成 3–6 个议题（每个写：问题一句话 · 影响谁 · 建议在会上定什么）。纯个人工具配置类的不放。
4. **团队发展周报**：读团队发展总盘 session（local_4d0a3fe7-3f41-4199-82bc-874fce202d46）上周五「团队发展周报」的汇总（用 ccd_session_mgmt 的 list_events / search_session_transcripts 找），挑跟 PI 车祸团队有关、需要在周会上拍板的建议。
5. **memory 里交代过的待讨论议题**：`weekly_partner_meeting.md` 的「待讨论议题」一节里，日期是本周二的条目原样放进大纲。

## 输出格式
纯文本、对齐缩进、不用 markdown 表格（要能直接贴进 Google Doc）。结构：

```
M/D/YYYY 车祸部门周会大纲（草稿）
出席：Cassie、Joe；Klaus 主持
一、上周待办跟进
二、本周数字：新案 N（口径）· 结案 N
三、要处理的案子
四、流程 / Claude 使用问题（要定的事）
五、团队发展提议
六、其他议题
```
每条后面括号写来源（例：〔思路日志 11/18〕〔凌图数据 18703-PI1〕）。

## 交付
1. 存成 `~/Downloads/周会大纲 <M-D-YYYY>.md`（日期用明天周二）。
2. 中央 Activity Log 追加一行（只 append）：
```
gws sheets spreadsheets values append --params '{"spreadsheetId":"1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA","range":"Activity Log!A:J","valueInputOption":"USER_ENTERED","insertDataOption":"INSERT_ROWS"}' --json '{"values":[["<MM/DD/YYYY>","<HH:MM>","车祸部门周会","起草","周会大纲草稿已生成：~/Downloads/周会大纲 <M-D-YYYY>.md","Claude","weekly-meeting-agenda","Local","manual:weekly-meeting-agenda","Klaus：改周会大纲（周二开会前）"]]}'
```
3. 在本次运行的回复里贴出大纲全文，结尾一句：「改完直接用；会上记得开企微会议的转写和智能纪要，会后在岗位编制 section 说『收周会纪要』。」