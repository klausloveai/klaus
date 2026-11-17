# new-case 事故复盘记录

每次建案出错、被 Klaus / CM 发现，在这里追加一节：发生了什么 → 根因 → 为什么没拦住 → 改了什么 → 怎么验证。

---

## 2026-11-16 · Xinchen Hou intake 客户本人资料整块空白

**发现**：Klaus 打开 Xinchen Hou-11-14-2026 intake，C5–C21（DOB、电话、地址、邮箱、婚姻、职业、SSN、
健保、既往车祸、就医）全空且无色；C2–C4、C22 正常。CM（Jerry / Angelina）已接手。

**影响面**：扫最近 25 张 intake，三张中招，都是 11/16 同一 session 建的：
- Xinchen Hou：资料被乘客栏 N/A 覆盖丢失 → 已按企微表单原值回填 C5–C21（黄）。
- Weiguo Mao：同样丢失（原值多为 Pending + 邮箱）→ Klaus 定：留给 Angelina 手填，补充材料只补黄格。
- Yi Li：驾照/官网登记的 5 格错写在乘客 1 栏 C28–C32（Klaus 有意不让客人填企微表、等网页版 intake）→ 待 Klaus 定是否挪回。

**根因**：建案第 6 步每次现写 inline openpyxl，按 B 列标签建 `label → cell` 字典并扫到第 45 行。
模板里客户区（B5–B21）与乘客区（B28 起，另有 E28、B53、E53）标签大量重名：
Date Birth / Phone / Address / Email / Gender / Marital Status / Spouse Name / Occupation / SSN /
Medi-Cal? / Medicare? / Health Insurance / Prior Accd & Injured? / Ambulance? / Emergency? /
UrgentCare? / Primary Doctor Visited?。字典「后写覆盖先写」→ `B('Date Birth')` 实际写到 C28。
随后脚本把乘客区整块填 N/A / Pending，把客户资料盖掉。不重名的字段（Date of Loss、Driver Name、
Initial Injuries?）不受影响，所以表看起来「填了一部分」，不显眼。
（1P / 3P 区也有同类隐患：Adjuster / Phone / Email 各出现两次。）

**为什么没拦住**：
1. `verify_intake.py` 只检查「有值的格子类型对不对」，空格跳过 —— 整块空白零报错。
2. 完成闸门只核 Drive / Lingtu Data / Master / Chat / label 建没建，不读回 intake 内容。
3. SKILL.md Gate 1 示例代码本身就是「扫到第 75 行的字典推导式」，等于教了错误写法。
4. 每案现写脚本，没有共享、经过测试的填表工具。

**改了什么**（skills 私库 commit b8e8a0e / ee6138d / 本次）：
1. 新增 `scripts/fill_intake.py`：区块行范围写死、区内重名自动编号、未知标签报错不保存、
   自动黄色格式；保存前自检客户核心格非空 + 客户 DOB/电话/邮箱不得出现在乘客区块。
   SKILL.md Gate 1 改为**只准用这个脚本**，禁止 inline 手写。
2. `verify_intake.py`：C5–C8 空 = ERROR，提示先查 C28–C32。
3. 完成闸门第 9 项：从线上 Google Sheet 读回 C2:C22 与 C24:C32，对照表单。

**验证**：
- 拿当时出错的 Xinchen Hou 建案稿跑 verify_intake → 报「客户本人资料 C5–C8 空」。
- 空模板跑 fill_intake：客户值落在 C5/C6/C8，乘客区为 N/A，I16/I17 = 第一个 Adjuster 块；
  传未知标签 → 报错、文件未保存。

**教训 / 规则**：
- 按标签定位必须限定区块；任何「字典推导式扫整列」都视为 bug。
- 检查要覆盖「该有值却空着」，不能只查「有值的对不对」。
- 团队已接手的表，修自己的错也先问 Klaus 修哪几张。
