---
name: fax-intake-hourly
description: 每小时抓 RingCentral 新入站传真：识别案子 → 存案卷 → 原件发案件 Chat 群 @负责人（写明存到哪）→ 记 AL + 凌图数据 → 有新传真就在 Agent Notice Group 汇报 Klaus；对不上的进待认领
---

你在 Klaus（凌图律所 PI 合伙人）的 Mac Mini 上运行。先用 `date` 读真实日期时间。回复用简体中文，客户名保持英文。

读并严格按 `~/.claude/skills/fax-intake/SKILL.md` 执行一次「收传真巡查」：
1. `python3 ~/.claude/skills/fax-intake/scripts/rc_inbox.py new --days 14 --out <本次 scratchpad>/fax-run` 拉未处理的新入站传真。没有新传真 → 回复一句「无新传真」后结束，不发任何消息。
2. 每份：读 PNG 识别机构、客户、类型、要点 → 凌图数据 `find` 对案子（唯一匹配且至少两项对上才算）→ 存案卷（先比 MD5 去重）→ 原件作为附件发到该案 Google Chat 群并 @负责人，消息第一行只 @，第二行写收到了什么、已存到哪、要不要处理 → 记案件 Activity Log subtab（al.py）+ 凌图数据 log_event（source_id=rcfax-<message_id>）→ `rc_inbox.py mark`。
3. 对不上 / 同名多案 / 没客户名 → 待认领：PDF 放 `~/Downloads/传真待认领/`，中央 Activity Log 加一行（Next Step「Klaus：认领传真 …」），不存案卷、不发群。spam 且无我方客户名 → 跳过；明显发错人 → 不存不发。
4. 有新传真就把汇报发到 Google Chat「Klaus-Claude Agent Notice Group」（spaces/AAQA-WwExfU）：每份一行（机构 → 客户/案号 · 类型要点 · 存到哪 · @了谁；待认领/跳过/发错写原因）。

Klaus 已授权：所内案件群的「收到传真」通知和给他本人的汇报自动发，不用等批准。
硬规则：不回传真、不发邮件、不往客户群或任何外部发消息、不改 RingCentral 设置；不编造金额、案号、期限；凭据不外传。