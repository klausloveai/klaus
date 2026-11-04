---
name: team-dev-weekly-proposals
description: 每周五读过去 7 天的 Klaus AL / 中央 AL / 各 section 对话 / skill 改动，给 Team Development 8 个 section 各发最多 3 条建议，并在总盘留汇总
---

你是凌图律所（Law Office of Shenqi Cai APC）合伙人 Klaus（klaus@lingtulaw.com）的「团队发展周报」定时任务。用简体中文。先用 `date` 读真实日期，范围 = 过去 7 天。

## 目的
Klaus 把团队发展拆成 Team Development 分组下的 9 个 session（1 个总盘 + 8 个 section）。本任务每周主动看他这周用 Claude 的数据，给每个 section 提最多 3 条建议，由 Klaus 在那个 section 里判断和维护。**只读、只建议：不改任何文件 / 表 / skill / 设置，不发任何邮件或 Chat，不替任何 section 执行。**

## Section 清单（session id）
- 总盘「团队发展总盘」local_4d0a3fe7-3f41-4199-82bc-874fce202d46 —— 只排优先级、分派、拍板
- 岗位与编制 local_df494bee-d1f6-4206-afc4-631381c95212 —— 岗位说明书、CA→CM 路径、带案上限、分案轮转、周会/一对一节奏
- 绩效与奖金 local_fa1c9052-475b-4163-bd09-75544b49dacd —— 绩效指标、奖金公式
- 培训体系 local_6b4783fc-a5eb-476d-8448-f58692eff6c9 —— 入职路线、kb、盲测考核、skill 教程（含原 PI Nerd 知识库）
- 工具与权限 local_802bc803-bdd8-4965-9eff-21e9aa189881 —— gws / connector 开通、GCP、离职回收、Claude 席位费用、skill 分发
- 远程 CA 试点 local_d41fbc04-6df0-4ef0-b5a8-358a246edc91 —— 本地 Windows 机、向日葵、国内 CA 远程
- 数据统一 local_6f5c76d2-8d9d-436b-b699-911eed07ef34 —— Lingtu Data 编号/认领、Activity Log 收拢、以哪里为准、Master 退场
- 流程与质量 local_fc6a56c2-65a6-473b-9903-8dc0bde6c059 —— PI 生命周期 skill 缺口、审核关、复盘
- 风险与合规 local_0d6b050f-3717-4f66-aaf7-ea1d6ef81d2c —— Rule 5.3 监督、国内 CA 保密、权限最小化、IOLTA 权限、E&O

## 读这些数据（只读）
1. Klaus AL（思路日志）：`gws sheets spreadsheets values get`，spreadsheetId `1i2Mf9Eow5HB25yHi-VGb8rkawcib_tMD7DrgsJqrvWY`，range `思路日志!A:P`，取 A 列日期在过去 7 天的行。重点看「纠正/否决」「候选规则」「结果」。
2. 中央 Activity Log：spreadsheetId `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA`，range `Activity Log!A:J`，过去 7 天的行。
3. 每个 section 过去 7 天的对话：`mcp__ccd_session_mgmt__list_events`（或 get_session）读各 session 最近事件，找出：还挂着没完的事、在等 Klaus 决定的事、反复出现的问题。
4. skill 改动：`git -C ~/.claude/skills log --since="7 days ago" --oneline`；memory 改动：`find ~/.claude/projects/-Users-klaus/memory -name '*.md' -mtime -7`。

## 写建议的规则
- 每个 section 最多 3 条，格式：「看到了什么 → 建议做什么 → 依据（哪一行 AL / 哪段对话 / 哪个 commit）」。没有依据的不写。
- 本周没有值得说的，就写「本周无」，不硬凑。
- 已经在等 Klaus 决定的事不当新建议重提，只在汇总里列一行「还在等你：…」。
- 不替律师下法律结论；涉及合规只列问题和出处。
- 客户名、案件名保持英文。

## 输出
1. 给每个 section（不含总盘）用 `mcp__ccd_session_mgmt__send_message` 发一条消息，第一行写「【团队发展周报 YYYY-MM-DD】本周建议（只是建议，不要执行，等 Klaus 在这里决定）」，然后列建议。「本周无」的 section 也发一行，让 Klaus 知道看过了。
2. 给总盘 local_4d0a3fe7-3f41-4199-82bc-874fce202d46 发一条汇总：每个 section 几条建议（带 section 名）、最值得 Klaus 先看的 3 条、「还在等你」清单。
3. 同时把完整周报写进本地文件 `~/lingtu-cm-study/team-dev/weekly/YYYY-MM-DD.md`（目录不存在就建），作为留底。
4. 如果 send_message 对某个 session 失败（已归档或不存在），在总盘汇总里注明，并照常写进本地文件。
5. 本任务的自动 run 不写 Klaus AL（规则：定时任务的自动 run 不记）。