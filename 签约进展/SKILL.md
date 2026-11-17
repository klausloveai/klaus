---
name: 签约进展
description: 随时查 DocuSign 签约进展（凌图 PI / DV retainer）：一次扫完，新签好的立刻处理（Master 改 ⚠️Pending + 案件 Chat @CM + 凌图数据记录），再给 Klaus 一张「已签 / 没签」清单。Klaus 说「/签约进展」「查签约」「签约进展」「谁签了谁没签」「跑一下签约检查」时用。等于手动把每小时任务 docusign-signed-hourly 和每天 11am 的 docusign-unsigned-daily 合起来跑一次。不催客人、不发 DocuSign 提醒、不 void、不改信封。
---

# /签约进展

Klaus 2026-11-16：「做一个 /签约进展 skill」——平时靠两个定时任务（每小时 :20 处理新签约、每天 11am 未签清单），
这个 skill 让他**随时手动触发同样的事**，不用等下一次定时。

**规则以两个定时任务的 SKILL.md 为唯一来源，这里不重复抄细节：**
- 处理新签约：`~/.claude/skills/scheduled-tasks/docusign-signed-hourly/SKILL.md`（第 0–6 步：状态文件、拉信封、判断全签/部分签、找 Chat 群和 CM、改 Master、逐字发 Chat、记录）
- 未签清单：`~/.claude/scheduled-tasks/docusign-unsigned-daily/SKILL.md`（第 1、3 步：筛选范围、未签分组）

开始前两份都读一遍，照做。回复用简体中文，客户名保持英文。

## 步骤

1. `date` 读真实时间。
2. **拉信封一次，两部分共用**：DocuSign `getEnvelopes`，accountId `e78a2bb2-9440-4ca6-8dff-deded2f8766c`，
   from_date = 今天往前 30 天，status `sent,delivered,completed`，include `recipients`，count 40，order_by sent desc；
   结果存成文件时用 python 读完整，`totalSetSize` 比拿到的多就用 `start_position` 翻页，直到读完。
   mcpSessionId 沿用本对话里已有的（没有就省略）。
3. **A. 新签好的 → 立刻处理**：完全按 hourly 第 0–6 步（cutoff、`state=full` 跳过、partial 只在有新签时处理、
   找不到群/行进 unresolved、Chat 文案逐字）。Klaus 已长期授权，不用再问。
   ⚠️ 处理前**重新读一遍 notified.json**——每小时任务可能刚处理过同一封，已是 full 的不重复发 Chat。
4. **B. 没签的 → 列清单**：按 daily 第 1 步筛范围（PI / DV / 和解相关，排除移民和诉讼收费协议），第 3 步分组
   （客户未签 / 只差律师签 / Cindy intake 发、未分配）。
5. **凌图数据缺口（顺带核）**：已签齐的客户 `find` 一下，没有 `-PI1` 案件编号的列出来，并写原因
   （通常是介绍人没设介绍费比例 → 等财务；其他原因写明）。只报告，不自己 sign_lead——要 Klaus 说再做。

## 回复格式（结论先行，短）

第一行：「刚扫完：本次新处理 N 封；还没签 M 封；最久没签的是 X（Y 天）」

**🆕 本次新处理**（没有就写「本次没有新签约」）
| 案件 | 全签/部分签 | Master 改了哪行 | Chat @谁 |

**✅ 近 7 天已签齐**：一行列名字（信箱），不展开。

**⏳ 还没签**（按已等天数从长到短）
| 客户 | 谁没签 | 状态（未打开 / 已打开未签 / 自动回复） | 发出日 | 已等天数 |
另起小组：「只差律师签」「Cindy intake 发、未分配」（有才写）。

**🔢 凌图数据还没案件编号**：客户 — 原因（一行一个，有才写）。

**⚠️ 要你看**：unresolved 新增项（没找到群 / Master 没找到行），有才写。

不写催签文案、不甩交付清单。

## 不做的事
- 不给客人发任何东西，不发 DocuSign 提醒（催签要 Klaus 说了才走 `feedback_docusign_chase_workflow` 那套）。
- 不 void、不改信封、不改未签客户的 Master 行。
- 不 sign_lead、不改凌图数据阶段（只报缺口）。
- Cindy intake 发的信封不发 Chat（要 Klaus 先定 assign）。
