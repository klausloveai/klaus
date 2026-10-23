---
name: new-case-all
description: |
  凌图律所 PI auto 新案「全套」一条龙：从企业微信收集表导出 intake → 跑完整 new-case 建档
  （Drive / intake sheet / tracking / Google Chat / Gmail label / DocuSign retainer）→ 企业微信建客户群
  → 个人微信给客户改备注、打标签、拉进群 → 群里依次发签约通知、@客户短句、案件须知。
  Use when Klaus says "/new-case-all", "全套建案", "建案+拉群", or asks for new-case PLUS the WeChat
  client group in one go. 只要 new-case 本身（不拉群）时仍用 `new-case`。暂不与 new-case 合并（Klaus 2026-10-17）。
---

# new-case-all — 新案全套（建档 + 企微客户群）

Klaus 2026-10-17 定：这套流程单独成一个 skill，**暂时不并进 `new-case`**。
建档部分以 `new-case` 为准，本 skill 只规定**前后多出来的阶段**和**这些阶段的规则**。

> 先读 `~/.claude/skills/new-case/SKILL.md`（Step 1–15），再按下面的阶段走。
> 企微/微信的点按操作见 `~/.claude/skills/wecom/SKILL.md`（本机修补版），坐标每次现取、每步截图核对。

## 阶段总览

| 阶段 | 做什么 | 停下来等 Klaus？ |
|---|---|---|
| A | 企业微信收集表导出 intake（若 Klaus 已给 zip 则跳过） | 否 |
| B | `new-case` Step 1–14（建档 + retainer） | 照 new-case 的闸门 |
| C | Google Chat：建群后**立刻** @ CM+CA+Amos | 否（笔记来了再补发） |
| D | 企业微信建客户外部群 | **先报方案再拉**（第一次/名单有变时） |
| E | 个人微信：客户改备注 + 打标签 + 拉进群 | 否 |
| F | 群里依次发 3 条消息 | Klaus 明确让发才发 |
| G | Activity Log + memory | 否 |

---

## 阶段 A — 从企业微信收集表导出 intake

Klaus 给的是截图/口述「文档里两位客户填写的信息」时：
1. 企业微信 → 文档 →「凌图律所-1.2车祸理赔案件信息收集表」(智能表格, Intake Form 视图)。
2. 右上「…」→ **导出** → **本地 Excel 表格和附件（.zip）**。
3. 保存框里**改文件名**（Downloads 常有同名旧 zip，别覆盖）：`<Client1>-<Client2> intake <M-D>.zip`。
4. 导出的是**整张表**里勾选/当前视图的记录——解压后核对 xlsx 里的行就是 Klaus 指的那几位客户，多出来的行不用。
5. 之后照 `new-case` Step 1 解压。

**DOL：用客户填的日期**（Klaus：「dol 输入用客户填写的不要搞错」）。导出的 Excel 每行日期常被 +1 天，
同一份表里两人日期可能不一样（例：司机 10/17、乘客 10/18）——以警察卡 / 客户实际填写为准，
不要直接抄 Excel。照 new-case Step 3 闸门处理。

## 阶段 B — new-case Step 1–14

完全照 `new-case`。补充：
- **Picase@ 已拆成三个 tab**：`Picase@(Amos)` / `Picase@(Jenkins)` / `Picase@(Eeve)`。Klaus 只说「picase」时
  **问他进哪个 tab**（AskUserQuestion）；`add_tracking_row.py --tab "Picase@(Jenkins)"`。
- Chat 群后缀按 tab 的 CM：Jenkins=(Z)、Eeve=(E)、Amos=(A)。
- **picase@ gws token 常过期** → Gmail label 建不了时照实报、给授权链接，别静默跳过。

## 阶段 C — Google Chat 立即 @

建完群、核完成员，**不等笔记，立刻发** `@CM @CA @Amos new case`
（Picase@(Jenkins) 案 = jenkins.l@ + tiana.d@ + amos.f@，**不 @ Eeve**）。
Klaus 笔记来了再**原话**补发一条（同样 @ 三人）。规则详见 memory `feedback_chat_mention_list_by_cm`。

## 阶段 D — 企业微信建客户外部群

**默认成员**（Klaus 2026-10-17）：

| 角色 | 企微里怎么搜 / 显示 |
|---|---|
| 蔡律师 Shenqi Cai | 搜「蔡沈祺」→ 显示「蔡沈祺 Cassie(Shenqi…)」 |
| Claire | 「Claire」→「Claire-法律助理」 |
| Amos | 搜「Hermès」→ 显示「Yu Feng(Hermès/冯经理…)」 |
| 该案 CM | Picase@(Jenkins) → Jenkins |
| 该案 CA | Picase@(Jenkins) → Tiana（显示名带「请假ing」也照拉） |
| ~~Eeve~~ | **已离职（2026-10-22），不再拉** |
| Klaus 个人微信 | 搜「Klaus Liu」→ 在「我的客户」下 |

不拉 Taki / Joe（老群残留）。群主 = Klaus（企微）。

**操作**（`scripts/wecom_picker_search.sh` 负责搜索+截图）：
1. 企微 → 消息 → 右上「＋」直接弹「发起群聊」选人框。
2. 逐个 `wecom_picker_search.sh "<名字>" out.png` → 看截图确认第一条就是本人 → 点勾 → 右栏核对「已选择 N 个」。
3. 全部勾完、右栏人数对上，点「完成」。
4. **改群名**：右上「…」→ 群聊名称 → 弹框里全选粘贴 `<DISK 案名>⚠️` → 确定。
   （聊天区中间「填写群名称」那行字点不动；弹框有时同时弹出某人名片挡住按钮，先点空白处关掉。）
5. 截图核对群名 + 人数。**改名后会话列表会重排，别按旧坐标点会话**——会误开别的群、把未读标成已读。

**客户此时拉不进**：客户几乎都不是 Klaus 企微的外部联系人，走阶段 E。

## 阶段 E — 个人微信：改备注 + 打标签 + 拉进群

客户通常已在 Klaus 个人微信里（常见来源：Klaus 之前拉的「医疗理赔 …」小群）。

1. `scripts/wechat_search.sh "<客户中文名/拼音/微信昵称>" out.png` 找到人；核 **WeChat ID** 与表单信息对得上再动。
2. 打开客户资料卡 → 右上「…」→ **设置备注和标签**：
   - 备注名：`<English Name>-PI`（例：`Zhaoxing Gu-PI`、`Liyang Shen-PI`）
   - 标签：已有的 **🈲PI客户**（**不要新建同名标签**）。标签弹层会飘到窗口左外侧；**先在弹层搜索框粘贴「PI客户」再点结果**，
     直接点列表项常常只高亮不勾选。看到标签栏出现「🈲PI客户」再点「完成」。
3. 再开资料卡核对：备注、标签都对。
4. 个人微信里打开新建的企微群（搜群名）→ 右上「…」→ 成员区「添加」→ 按备注搜 → 勾选所有客户 → 「添加」。
   客户直接入群，不需要对方确认。截图核对人数（例：8 → 10）。

## 阶段 F — 群里发三条（顺序固定，Klaus 2026-10-17 定稿）

**只有 Klaus 明确说「发」才发**；发之前贴好、截图核对输入框，再回车。全部从 **Klaus 个人微信**发。

1. **签约通知** —— `new-case` Step 14 的签约文案（多人/单人、new/standard 套对），
   **不带** `<案名>⚠️` 标题行，**不 @ 人**。
2. **@ 所有客户 + 短句**：
   - 多位客户：`大家好，这是案件群，合约发送至邮箱了，请仔细阅读后电子签即可谢谢～`
   - 单个客户：`您好，这是案件群，合约发送至邮箱了，请仔细阅读后电子签即可谢谢～`
3. **案件须知全文** —— `references/client_group_welcome_bulletin.txt`，一字不改（Klaus 微信收藏 8/27 那几条的合并版）。
   结尾要求客户回「已阅读理解」。文中邮箱写死 claims@ —— Piteam@/Picase@ 案要不要换由 Klaus 定，别擅改。

**输入技巧**：
- 多行文本：文件 → `pbcopy` → ⌘V；去掉末尾多余换行（贴完按一次 Delete）再回车。
- @：粘贴 `@` 再粘贴英文名（如 `Zhaoxing`）→ 弹出成员 → 回车选中；重复下一位。
  **不要直接键入字母**——中文输入法会把 `Zhaoxing` 变成候选词。@ 出来显示的是客户**微信昵称**，不是备注，正常。
- 回车 = 发送。每条发完截图确认气泡出现。
- 剪贴板用完还原。

## 阶段 G — 收尾

- Activity Log 每个对外动作各一行（建企微群 / 拉客户 / 发三条），Ref 写群名和人数。
- 本次学到的新坑写进 memory `feedback_wecom_case_group`。
- 最终回复：new-case 的 7 节 summary（照 new-case Step 15）+ 一段企微群状态（群名、成员、已发哪几条、客户有没有回）。

## 不做的事

- 不在任何客户群发测试文字；不替 Klaus 回客户私聊（只报告有未读）。
- 不点「创建新的群聊」以外的群（搜索结果第一条常是别的客户群，先截图核对）。
- 不新建微信标签、不删联系人、不碰「加入黑名单 / 删除联系人」菜单项。
- 凭据、客户证件号不写进任何群消息或记录。
