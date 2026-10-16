---
name: 团队复盘
description: >-
  Weekend DEPARTMENT retrospective for 凌图律所 / Lingtu Law PI team — analyze the week's
  collected case-chat data and produce material for the Monday team meeting. Trigger on:
  团队复盘, 周会复盘, 跑团队复盘, 周末复盘, "/团队复盘", or when Klaus wants to 复盘 the team's
  weekly case work before Monday's meeting. It reads the 每周数据收集 sheet
  (Claims@/Piteam@/Picase@ tabs, one row per week), extracts FAQ-worthy Q&A + good client
  scripts, runs a RED-LINE compliance check + RISK scan against the handbook and case
  decision tree, flags data-hygiene issues and recurring systemic blind spots, and outputs
  a Monday-meeting brief. NOT the same as the `weekly-review` skill (that one reviews
  Klaus's own Claude setup/memory). v1 — several steps still TBD, see 待补充.
---

# 团队复盘 · Weekly Team Retrospective

## 这个 skill 干什么
每周末,把案件助理收集上来的一周案件群对话数据,做一次**部门复盘**:提炼知识、扫风险、查合规、发现系统性问题,产出**周一团队会议要用的材料**。Klaus 周末跑一次 → 周一开会用。

## ⚠️ 和 `weekly-review` 的区别(别混)
- `weekly-review` = 复盘 **Klaus 自己的 Claude 设置**(memory / skill / 指令)。
- 本 skill `团队复盘` = 复盘 **团队的案件工作数据**(客户群对话)。两个是不同的东西。

## 输入(数据源)
- **每周数据收集 Sheet** id `1pr9QbFx8FinCb4-rTU1LRLDYiWVYlnAXpLhDoIrQOHE`,三个 tab:`Claims@`(Amos)/`Piteam@`(Jerry)/`Picase@`(Ryan)。每 tab **最新一行(第 4 行,最新永远在最上面)= 本周数据**;『AI 汇总正文』列是案件助理用企微收集的整份总结。
- 数据是怎么来的:见同文件夹《怎么做 · 每周数据收集 SOP》。
- 若某 tab 本周没数据 → 该团队跳过,报告里注明"XX 团队本周未提交数据"。

## 参照标准(判断依据)
- **合规红线**:入职手册 Part 1 的 9 条红线,doc `17waC5NuHkdUPlMojh0G2HwuQGvsV_4RrqmN1vm2_RjM` —— 用它当尺子查不规范回答。
- **风险模式 + 分支规则**:案件决策树,doc `1o7HHK0Qzm3nH-lqIqQdt6yHTrGia7EtnHjf52ExayhE` —— 尤其反复出现的盲区:非机动车受害人必查家庭 UM、gig 案 app 状态/注册车、多人案先问 policy limits、UM 四铁律、DUI 加速定责、intake 错档。
- **知识库 FAQ**,sheet `12SFVJM_4bQYbceWfPRA0QCIcTTMKtB_d3nSicwA8rSI`(当前为部分版):入库前先搜一遍,避免重复。

## 步骤
1. 读三个 tab 的本周行,拿到各团队『AI 汇总正文』。
2. 逐团队分析:
   a. **提炼 FAQ**:客户反复问的问题 + 我方回答**原话** → 候选 FAQ(问题 / 答案原话 / 来源群 / 日期)。
   b. **合规检查**:逐条对我方回答扫 9 红线 —— 承诺金额或结果 / 引导夸大伤情 / 给法律意见(该律师答的) / attorney-driven 措辞 / 敏感问题草答(精神健康史、既往伤、录音陈述、责任归属)。有则列『群+日期+原话+红线编号』;拿不准的进"待人工复核"。
   c. **风险扫描**:客户不满 / 催进度 / 响应慢 / 回国出国 / 拒赔或争议责任或保险直接联系客户 / 头部伤·住院·伤情加重 / 想放弃或换律师 / 治疗中断或未开始 / 未成年 / gig 或工作中受伤 / 非机动车受害人→查家庭 UM / intake 或 Master 数据错。
   d. **好话术**:特别规范、可当范本的对客解释 → 候选『话术模板』(正面教材,点名表扬)。
   e. **系统性盲区**:同类问题/漏判本周出现 ≥2 次,或与历史反复呼应 → 标为"该补进 SOP / 决策树的盲区"。
3. 产出**复盘报告**(见下方输出格式)。
4. 收尾(当前半自动,待系统建成后自动化):把"建议入库清单"里 Klaus 勾选确认的,写进知识库 FAQ / 话术库;把本周新增写进"每周更新"文档。

## 输出格式(周一会议材料)
一份 Doc(或聊天消息),固定结构:
- **① 部门速览** — 三团队本周动态、活跃群数、整体状态一句话。
- **② 🚨 风险清单**(按严重度排)— 群 + 一句话 + 建议动作 + 谁跟进。
- **③ 📋 合规提醒** — 不规范回答(对事不对人,引原话)+ 正确应该怎么说;无则写"本周合规"。
- **④ 💎 本周金句** — 最好的对客话术(点名表扬 + 收进话术库)。
- **⑤ 🔁 系统性盲区** — 反复出现、该补进 SOP / 决策树的。
- **⑥ 📌 周一会议要点** — 给团队讲的 3-5 条(表扬 + 提醒 + 新规则)。
- **⑦ 📥 建议入库清单** — 待 Klaus 审批后写进知识库的 FAQ / 话术。

## 注意
- 合规判断会有误报 → 标"待人工复核",别直接拿去批评人。表扬可点名,批评对事不对人。
- 报告是给管理层(Klaus / Amos / Claire)看的内部材料,含真实客户案例,不外传;入库时剥客户 PII。
- 只读收集来的文字数据,**不碰客户 / adjuster 通话录音**(加州双方同意法)。

## 待补充(v1 占位,Klaus 后续定)
- [ ] **复盘报告存哪**:建一个"复盘归档"文件夹按周存?还是每次发 Chat?
- [ ] **知识库 + 每周更新系统建成后**,把步骤 4 的"人工审后入库"升级成半自动(黄→橙→无色更新机制)。
- [ ] **周一会议模板**:时长、谁主持、固定议程。
- [ ] 每个团队单独出一份报告 vs 三团队合并一份?
- [ ] 触发方式:纯手动跑,还是每周日晚定时任务自动跑好、周一 Klaus 直接看?
- [ ] 是否把"决策树盲区"的更新也纳入本流程(反复漏的自动提议补进决策树 Doc)。
