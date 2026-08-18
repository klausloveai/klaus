---
name: pinerd-sync
description: Sync new Pre-Litigation Nerd (nerdgroup.co) listserv activity into Klaus's "PI Nerd" knowledge base in Google Drive — pull the new threads out of klaus@ Gmail, summarize each, and write them into the Master Index sheet (Sheet1 + Updates Log + Provider Database + Webinar Library). Use whenever any of these are mentioned: PI Nerd 更新, 同步 PI Nerd, nerdgroup 更新, listserv 更新, 更新知识库, "PI Nerd sync", "/pinerd-sync", or when the weekly scheduled routine fires. Also handles the webinar library refresh (Box) when asked. It only writes to Klaus's own private KB — it never posts to the listserv, never emails, never redistributes member content.
---

# PI Nerd 知识库同步

Klaus 是 **Pre-Litigation Nerd**（Groups.io，`nerdgroup.co/g/Nerds`，Lydia Santiago 主持，
Carpenter & Zuckerman 深度参与）的付费会员。内容按 Terms §6a 属 **member-confidential** ——
**备份保持私有，绝不转发、绝不外传**。

## 资源 id（写死，别猜）

| 资源 | id |
|---|---|
| Drive 文件夹 "PI Nerd"（Shared Drive） | `1LbrJWKmFX1bSVAYRwTXb3j3W7cy1RCxg` |
| **Master Index**（本 skill 的唯一写入目标） | `1sbSGUq0Bu3khRoxKLk9wdi0CvDyaeJnF50EehvvS1p4` |
| Master TOC (Doc) | `1VN8uuIsONzhO-D7_v7Hex6hLLBS698j0meeeidefJt4` |
| START HERE (Doc) | `1OJd8P5_T4UQUeEVvLbHMYzzukw0Zmpwe9zv5OELe6OY` |
| RAW backup JSON（首轮 1,125 帖全文） | `1EIEggu_iRb0THMRV8W-DUQPukGqirfgk` |
| Box「02. Webinars」（录像库，需登录 nerdgroup.co → Files） | `https://app.box.com/s/2t4828l1ztr0sh9ewqxjsafc6a0s4hbs` |

Master Index 的 tab：
- **Sheet1** — 主表，一帖一行：`# / Category / Topic(HYPERLINK) / Summary / Providers mentioned / Phone(s) / ⚠ / Msgs / Source URL`，按 Category 分组、组内按主题名字母排序。
- **Webinar Library** — 历届 webinar + Box 录像直链 + 学习优先级 + 「已看」勾选栏。
- **Updates Log** — 只 append 的同步流水（每次 sync 的新帖/新回复一行）。**下次 sync 的起始日期就从这张表 A 列的最大值推出来。**
- **Provider Database** / **Blacklist & Cautions** — 供应商库（`Provider/Type/Area/Contact/Status/Notes/source`）。

## 为什么走 Gmail，不爬网站

Klaus 的订阅是 **Individual Messages，投递到 klaus@lingtulaw.com**（已于 2026-08-18 核实），
所以每一条群消息都在 klaus@ 里；且每封 Groups.io 邮件的页脚都带
`Mute This Topic: https://nerdgroup.co/mt/<topicId>/<subId>` —— 从这里拿 topic id，
拼出 `https://nerdgroup.co/g/Nerds/topic/<slug>/<topicId>`（Groups.io 只认 id，slug 随意）。
**因此常规同步完全不需要登录、不需要浏览器。** 只有刷新 webinar 录像库才要开浏览器进 Box。

## 流程

### 1. 拉取
```bash
python3 ~/.claude/skills/pinerd-sync/scripts/pinerd_pull.py --workdir <scratchpad>/pinerd
```
不带 `--since` 就自动从 Updates Log 续跑（可用 `--since YYYY/MM/DD` 覆盖）。
产出 `threads.json` + `digest.txt`，并已按 Sheet1 的 Source URL 去重，标好每帖是
`NEW`（新主题）还是 `UPD`（老主题有新回复）。**若 0 条，就报"本周无新内容"收工，不要写表。**

### 2. 读 digest，逐帖写摘要
读 `digest.txt` 全文（通常 20–100KB）。每帖产出：

- **Category** — 只能用 Sheet1 已有的 11 个值：`Providers & Referrals` / `Liens & Reductions` /
  `Insurance Claims & Coverage` / `Property Damage / Total Loss / DV` / `Litigation / Pre-Lit Escalation` /
  `Case Screening / Intake / Retainer` / `Health Insurance & Billing` / `Medical / Injury Knowledge` /
  `Practice Ops / Software / Vendors` / `Community / Admin / Events` / `Misc / Other`。
- **Summary** — 英文，**可执行的知识**而不是"某人问了个问题"。规矩：
  - 结论先行，把**法条 / 法规引用原样保留**（`Ins. Code §11580.2`、`10 CCR §2695.7(b)`、`Veh. Code §21703`…）。
  - **金额、日期、电话、地址、诊所名、律师名一律照抄，不许编。** 没人回答就写
    `No recommendation posted as of <today>.` —— 空着比猜准。
  - 自己的补充要显式标 `[KB note: …]`，不要伪装成帖子里说过的话。
  - Lydia / Paul Zuckerman / Ivy Callahan / Michael Geragos 的回答点名署上（社群里这几位=权威）。
- **Providers mentioned / Phone(s)** — 只放**真正有用的**联系人和号码，不要把签名档的电话当数据。
- **⚠** — 有 blacklist/caution/踩坑/合规红线时填 `⚠`。
- **Msgs** — `n_emails`。
- `UPD` 帖不新建行：写成 `upd` 里的一段 `➕ [UPD M/D–M/D/YY] …` 追加到原摘要末尾，
  并把 `extra_msgs` 加到原 Msgs 上。**永不改写既有摘要文字，只在后面追加。**

### 3. 顺手抽供应商
帖子里出现新的诊所 / 医生 / 影像中心 / lien 网络 / 调查公司 / 记录检索 / 外州转介律师 /
车行 / DV 估价 / 仲裁员 / 软件供应商 → 进 `providers_new`
（`[Name, Type, Area, Contact, Status, Notes, "<slug>/<topicId>"]`，Status =
`Recommended` / `Caution` / `Blacklist` / `Note`）。
**先读一遍 Provider Database 的 A 列**，已存在的写进 `providers_upd`（追加 ` ➕[M/YYYY] …`），别建重复行。
Status 为 `Caution/Blacklist/Note` 的会自动同时进 Blacklist & Cautions。

### 4. 回写
把 payload 存成 JSON（格式见 `scripts/pinerd_write.py` 顶部 docstring），然后：
```bash
python3 ~/.claude/skills/pinerd-sync/scripts/pinerd_write.py payload.json
```
脚本负责：追加新行 → 应用 `[UPD]` 追加 → Sheet1 重排序重编号 → append Updates Log →
append/更新 Provider DB 与 Blacklist。**幂等**：同一 topic id 不会重复入表，同一段 `[UPD]` 不会重复追加。

### 5. Webinar Library（**只在被要求刷新、或有新录像公告时才做**）
digest 里出现 `Replay Now Available` / `Webinar Notes` / `Event: ... Webinar` 时：
开浏览器（Claude-in-Chrome，已登录）→ `nerdgroup.co/g/Nerds/files` → Webinars（跳 Box）→
逐个子夹（Medical / Structure / Liens & Health Insurance / Pre-Litigation / Litigation）
读 `a[href*="/file/"]` 拿到文件名 + 直链，把新录像补进 **Webinar Library** tab
（`录像` 列 = `=HYPERLINK("<box>/file/<id>","▶ 看录像 (Box)")`）。
给 Klaus 的学习优先级按北极星排：**诉讼线（complaint / discovery / depo）与团队规模化 = ★★★**。

### 6. 汇报
简体中文，短：新增 N 帖 / M 帖有新回复；挑 3–5 条**对凌图当下真正有用**的（dog bite、lien 减免、
UM/UIM、carrier 期限、demand 升级、诉讼流程）；列 Klaus 自己发的帖有没有人回；
新增/更新了哪些供应商；有无新 webinar 录像。**别复述整张表。**

## 硬边界

- **只读 klaus@ 的邮件、只写 Klaus 自己的 KB。** 不发帖、不回帖、不发邮件、不外传成员内容。
- 想改订阅设置（投递方式等）→ 先问 Klaus，别自己动。
- 每次 sync 后如果发现了长期有用的新事实，才更新 memory；日常流水不进 memory。
