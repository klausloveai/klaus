---
name: onboard-team-member
description: |
  Onboard a NEW PI-team hire at 凌图律所 / Lingtu Law Office (Law Office of Shenqi Cai APC) —
  add them to their team's Google Chat case spaces, grant Google Drive access, and draft the
  Chinese onboarding email that hands them the whole training curriculum. Use whenever any of
  these come up: 新人入职, 新同学, 带新人, onboard a new member, "把 X 加到所有 claims@/piteam@/picase@
  相关的 chat 里", "share 整个 case folder 给 X", 新人培训邮件, 入职指引, welcome email for a new hire,
  new CA / new case assistant / new case manager, "/onboard-team-member". Typical invocation: a
  name + work email + which team (Claims@/Piteam@/Picase@) + who is 带教 them. The skill resolves
  their Chat user id, classifies every case space by the room-name suffix (A/J/R/K) cross-checked
  against the PI Master Sheet, bulk-adds them to their team's ACTIVE case rooms plus the shared
  ops rooms, grants fileOrganizer on the "PI Team Folder" shared drive, and creates a Gmail DRAFT
  of the onboarding email with every training-doc link. Three approval gates (room scope, Drive
  scope, send) — it NEVER sends the email; Klaus sends it himself. Always trigger for any
  "新人入职 / 加群 / 开权限 / 入职邮件" request, even a partial one.
---

# Onboard a New Team Member

Four things happen, in this order — **the order matters**: rooms → Drive → email draft → Klaus sends.
The email is full of Drive links; if Drive access isn't granted first, every link 404s for them.

Serves north-star goal ① 团队规模化. Precedents: Taki + Kiko (2026-08-31, intern CAs),
**Lyne (2026-09-18, CA on Claims@ — the run this skill was written from)**.
Related memory: [[onboarding_lyne]] · [[feedback_chat_space_members]] · [[firm_directory]] ·
[[onboarding_welcome_letter]] (the curriculum) · [[onboarding_cindy]] (the SOP/Work Log/装机清单).

## Invocation inputs

| 必填 | 说明 |
|---|---|
| 姓名 + 工作邮箱 | e.g. `lyne@lingtulaw.com` |
| 所属组 | **Claims@**(Amos) / **Piteam@**(Jerry) / **Picase@**(Ryan) |
| 带教人 | e.g. May（组长）— 决定邮件里"有问题找谁" |
| **岗位轨** | **CA (Case Assistant)** 还是 **CM (Case Manager)** — 见 GATE 1 |

## GATE 1 — 岗位轨（必须先问清，决定邮件内容）

**CA 和 CM 的入职内容不一样，不要猜：**
- **CA** → 邮件指向 00 欢迎信第三节的 **CA 四类职责**。
  **⚠️ CA 不使用 Claude / Cowork** — Day 1 装机清单最后一项（Cowork + Lingtu PI 插件）对 CA 不适用。
  邮件里要**明写让他跳过这一项**（不要去改那份 Doc，它对 CM 仍然有效）。DocuSign 也不给 CA。
- **CM** → 指向 **CM 10 条职责**，装机清单全项照做，含 Cowork/Claude。

现有对应关系（[[firm_directory]]）：CM 配 CA —— Jerry+Angelina、Ryan+Tiana、Amos+Claire；
CA组长 May；实习 CA Taki（跟 Tiana）、Kiko（跟 Angelina）、Lyne（跟 May）。

## Step 1 — 解析他的 Chat user id

Chat API 的 `memberships.create` **接受 email 别名**，直接拿第一次真实添加的返回值当 id：

```bash
gws chat spaces members create --params '{"parent":"spaces/AAQAYUyVfMg"}' \
  --json '{"member":{"name":"users/<new>@lingtulaw.com","type":"HUMAN"}}'
```
返回的 `member.name` 就是永久 user id（例：Lyne = `users/100251725481766007390`）。
`spaces/AAQAYUyVfMg` = **PI Team Chat**，本来就要加，拿它当探针不浪费。

> ⚠️ 本账号**没有 Directory / People 的 scope**（`admin` 不是 gws 已知服务，
> `people.searchDirectoryPeople` 返回 403）。不要浪费时间去查目录。

## Step 2 — 判定要加哪些案件群

**⚠️ 铁律：用房间名后缀判组，绝不用"CM 是不是群成员"判。**
Amos 出现在 557 个空间里的 507 个、May 359 个 —— 按人筛会全错（[[feedback_chat_space_members]] 里
8/31 那次也踩过：Ryan 在 23 个非 (R) 房、Jerry 在 94 个非 (J) 房）。

| 后缀 | 组 | CM |
|---|---|---|
| `(A)` | Claims@ | Amos |
| `(J)` | Piteam@ | Jerry |
| `(R)` | Picase@ | Ryan |
| `(K)` | Picase@ | Klaus |

1. 全量拉空间（**必须 page-all 或 pageSize 1000**，单页静默截断在 ~100）：
   ```bash
   gws chat spaces list --params '{"pageSize":1000,"filter":"spaceType = \"SPACE\""}' > spaces.json
   ```
2. `scripts/sweep_spaces.py` → 并发拉每个空间的成员，出 `members.json`（557 个约 1 分钟）。
3. `scripts/classify_spaces.py <TEAM_TAB> <SUFFIX>` → 用 **PI Master Sheet**
   (`1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`) 对应 tab 的 **B 列客户名 + D 列 Case Status**
   交叉验证后缀，输出 `a_split.json`（active / closed / unmatched）。
   - **先验证再批量**：抽几个该 tab 的客户名，确认确实落在该后缀的房间里。
   - 匹配不上的（老房间、改过名）归 `unmatched`，**默认算在办**一起加 —— 宁可多给不要漏。

**结案状态词**（`Case Status` D 列）：`✅Completed` / `❌Withdrawn` / `💼Substituted` = 已结。
其余（`📧Negotiating` `🧑‍⚕️Reduction` `💉Treating` `⚠️Pending` `🔔Collecting` `✍️Drafting`
`📧UIM Demand` `⚖️Litigation` `⚖️Small Claim`）= 在办。

### 固定加的共享群（三个，所有新人都加）
| 群 | space id |
|---|---|
| PI Team Chat | `spaces/AAQAYUyVfMg` |
| Treatment Team | `spaces/AAQABniKvxc` |
| Treatment Notice | `spaces/AAQARYNZEFo` |

**不要自作主张加**个人工作群（`May 工作群` / `Amos 工作群` / `Case Manager 培训群` / `核心群 KCA`）
—— Lyne 那次 Klaus 明确没选。要加就问。

## GATE 2 — 案件群范围（问 Klaus，报数字）

报三个选项 + **实际算出来的数量**，不要抽象地问：
1. **只加在办**（推荐）= active + unmatched
2. 全部该后缀房间（含已结）
3. 再加 legacy 无后缀老房间（约 110 个，多数已结，Amos 在里面）

Lyne 2026-09-18 选的是 ①：**107 个**（88 active + 19 unmatched）+ 3 个共享群 = **110**。

## Step 3 — 批量加 + 全量复核

`scripts/bulk_add.py` —— 6 并发，逐个打印 OK/ERROR，写 `add_result.json`，
**然后把每个目标房间重新拉一遍成员确认 `PRESENT`**。
不要只信 create 的返回值；报给 Klaus 的数字必须是复核过的数字。

角色一律 **`ROLE_MEMBER`**（默认）。`ROLE_ASSISTANT_MANAGER` 只给 Amos / Claire / May / 该案 CM。

## GATE 3 + Step 4 — Drive 授权

案件文件夹全在一个共享云端硬盘里，**不是逐个案子分享**：
**`PI Team Folder`** — driveId **`0ADBH3EXeXKRBUk9PVA`**，案件在
`0. PI Cases`（`1JwQtWURVoHxzYOLnOXvljc8ayBJTPRpp`）下按状态分 18 个文件夹。

**角色照抄同组**：Tiana / Angelina / Taki / Kiko / Lyne 全是 **`fileOrganizer`**（内容管理者）。
- `organizer` 只有 Klaus 一人，别给。
- `writer` 不能移动文件夹，跟案件按状态归档的流程冲突。

```bash
gws drive permissions create \
  --params '{"fileId":"0ADBH3EXeXKRBUk9PVA","supportsAllDrives":true,"sendNotificationEmail":false,"fields":"id,role,emailAddress"}' \
  --json '{"type":"user","role":"fileOrganizer","emailAddress":"<new>@lingtulaw.com"}'
```
`sendNotificationEmail:false` —— 不发 Google 自动通知，由入职邮件统一告知。

复核：
```bash
gws drive permissions list --params '{"fileId":"0ADBH3EXeXKRBUk9PVA","supportsAllDrives":true,"pageSize":100,"fields":"permissions(emailAddress,role)"}'
```

**必须向 Klaus 说明的暴露面**：共享盘整盘继承，`3. Disbursements`（分款）、`Account Information`、
`Business Development`、`DashCams`、`1. Templates` 都**没有独立权限**，加进来就都看得到。
收窄方案 = 只单独共享 `0. PI Cases`，代价是拿不到 Templates。

**不给**：`Hernan Simo Cases`(`0APtYw9adyTl8Uk9PVA`) / `Lashinelaw`(`0AFATGWjQ_6NsUk9PVA`) /
`Kaisheng Yang Cases`(`0ACp1kTfnh7wJUk9PVA`) —— 三个独立盘，与 PI 新人无关。

## Step 5 — 起草入职邮件（**DRAFT ONLY**）

从 **klaus@** 发（内部管理邮件，不走 case mailbox）。
**Cc = 该组的人**：Claims@ → `amos.f@` + `may.z@` + `claire.f@`。是否加 `cassie@` 要问。
标题：`欢迎加入凌图律所 · 入职指引（<Team>@ 组）`

签名**必须取邮箱预设**，不要手打（[[feedback_email_signature_sender]]）：
```bash
gws gmail users settings sendAs list --params '{"userId":"me"}'   # 取 isDefault 的 signature，原样拼在正文末尾
```
建草稿：`gws gmail users drafts create --params '{"userId":"me"}' --json '{"message":{"raw":"<base64url>"}}'`
（Python `MIMEText(body,'html','utf-8')` + `base64.urlsafe_b64encode`）

### 邮件七块（顺序固定）

1. **定位** —— 组 / 岗位（CA 或 CM）/ 带教人 / 案件主管 / 法助主管 / 部长 Klaus / 律师 Cassie。
2. **Day 1 装机（先做这个，别先读书）** ——
   [新人装机与设置 · Day 1 安装清单](https://docs.google.com/document/d/1P0f5q_3ZNlAV6TbHE8sYa4H4gbCMEPH4HJgcywDqmFk/edit)
   ＋ [RingCentral JWT 教程](https://docs.google.com/document/d/1dZeAodD-udvSWFN_C2Ypr9uVCSksq--y4H7vFkBrh_4/edit)。
   **CA 要明写跳过 Cowork/Claude 那项。** 分机 / 直线 / 签名档写成"带教人带你设"，**绝不编号码**。
3. **第一周按序读 00–10**（Drive `Claude培训` 文件夹 `1q3aD0M-_cffvlGFraLoX9yFQEfwh5PIn`）：

   | # | Doc id | 备注 |
   |---|---|---|
   | 00 从这里开始·欢迎加入 | `1r3vnpDV_BCEwQl0qo9UvseB4HHUTMSo8xJNPqQszFbE` | **先读这份**；CA 看第三节 CA 四类职责 |
   | 01 新人教学 PPT | `1AsZKUPztA3Ig0rf88MgLAnQTIo-IHhHDGFJ7dKOYONU` | presentation |
   | 02 第一课·认识 PI | `1DGES91t9EbvSMcuIQBzXUbreWHgNjQ7KgHavWMZY7uU` | |
   | 03 第一课小测 | `15og6I8JulmuiawZYT7dVRXwJ4nzXCnJv5jq9WiPOhuY` | form；**标成第一周第一个交付** |
   | 04 入职手册 Part 1 | `17waC5NuHkdUPlMojh0G2HwuQGvsV_4RrqmN1vm2_RjM` | 红线必读 |
   | 05 PI 知识库 FAQ | `12SFVJM_4bQYbceWfPRA0QCIcTTMKtB_d3nSicwA8rSI` | sheet；查用不必通读 |
   | 06 案件决策树 | `1o7HHK0Qzm3nH-lqIqQdt6yHTrGia7EtnHjf52ExayhE` | 连带 07 思维导图 / 08 闪卡 |
   | 09 工具设置与使用 | `1xuX_J2--39KNnDl7fQczoe4PwON87H689-e2Iq4kHyE` | ⚠️建设中，只有 Master Sheet/Chat/RC 三节 |
   | 10 任务卡总册 | `1ZvsNn1OcC16Ac1ZXRp6TQoamHD9fGoLaaDbY8TkJhMM` | ⚠️框架版 v0.2 |

   **⚠️ 绝不放进邮件**：`95 · 培训体系总纲` 和两份 `90 ·`（Skills Matrix / SOP 流程图）——
   内部蓝图，只给主管 / Claire。
4. **怎么干活** —— [团队工作模式 SOP](https://docs.google.com/document/d/1D4rQtYPAeO9EihafTCBgBrW5zYuicv2XubEDK_SOkLY/edit)
   ＋ [团队工作日志 Work Log](https://docs.google.com/spreadsheets/d/1IUwxdIvTTP1wlQOccSC85vLFUjVIG_1Q0IUaIxoKu2A/edit)
   ＋ 硬规矩 **完成报「三件套」**：做了什么 / 产出在哪 / 有无异常。
5. **业务主表** —— PI Master Sheet `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`，**看他自己组的 tab**；
   配 [记录教程](https://docs.google.com/document/d/1X0Q0IR_gX0sFITD-KbM1HOL9_Me5PrjFV-TedBvCZvk/edit)
   ＋ [记录准则](https://docs.google.com/document/d/1qPy0yUBfMFqEJvc-V15jYv4hLdu5X4k5GKFLajPjhKU/edit)
   ＋ [Treatment 教材第一章](https://docs.google.com/document/d/1DmOXQXew4rHAFIQYi8fPzkg5cb2iQDR89NkjN3iHoTg/edit)。
6. **已经开好的** —— 报 Chat 群数量 + Drive，并叮嘱 **第一周消息很多，先看不急着回**。
7. **找谁** —— 日常找带教人，案件判断找 CM/主管，**卡住超过半小时就问；问问题不扣分，闷着才扣分**。

格式：HTML 流动段落，多项清单才一项一行（[[feedback_email_list_formatting.md]]）；中文；
客户名 / 案件名保持英文。

## GATE 4 — 发送

**建好草稿就停。** 渲染一份 preview HTML 落 `~/Downloads/<Name>-Onboarding-Email-Preview.html`
给 Klaus 看，然后**等他明确说发**。Klaus 经常自己发 —— 发完他会告诉你。
发之前提醒他两件事：**Cc 名单对不对**、**他的入职日期对不对**（邮件通篇写"第一周"）。

## Step 6 — 收尾

1. 写 memory `onboarding_<name>.md`（type: project）：user id、组、带教人、
   加了哪些群（数量 + 范围口径）、Drive 角色与范围、邮件草稿 id。MEMORY.md 加一行索引。
2. **不写 Activity Log** —— 那是案件台账，人员入职不是案件动作。
3. **⚠️ 每次都要提醒的已知缺口**：`new-case` skill Step 11 的建群成员名单
   （`~/.claude/skills/new-case/SKILL.md`）**没有 Taki / Kiko / Lyne** —— 8/31 起就挂着。
   今后新开的案件群不会自动带上新人，要么手动补，要么让 Klaus 拍板改名单。
   同理 [[feedback_chat_mention_list_by_cm]] 的 @ 名单也没加新人 —— **Klaus 没发话不要自己改**。
