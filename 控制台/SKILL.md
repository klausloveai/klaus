---
name: 控制台
description: >-
  Klaus's session-first DAILY CONTROL TOWER. Sweeps klaus@ Gmail inbox + Google
  Calendar (today/tomorrow) + Google Chat @mentions, classifies everything by
  urgency×importance, renders a single visual dashboard inline in the session,
  and pre-drafts replies for every email that maps to an existing skill — so
  Klaus reviews + hits send, never hunts. Trigger on: "/控制台", "控制台",
  "今日控制台", "daily control tower", "今天有什么", "帮我看今天的任务",
  "扫一下邮件日历", or the morning run. Scans FRESH from source every run (state
  lives in Gmail/Calendar, NOT the conversation) so a new session each day keeps
  tokens near zero. DRAFT-ONLY: never sends email, never posts to Chat, never
  files anything — every send / star / archive happens only on Klaus's explicit
  go. Heavy per-case work spins OUT to its own session via a copy-ready 开场
  prompt. Companion of [[case-brief]] (litigation-only) — this is the personal,
  everything-inbox tower.
---

# 控制台 — 每日任务控制台 (session-first)

Klaus 是所有信息的枢纽：客户、对方保险、诊所、团队、Hernán、法院都发到 **klaus@**，
外加 Calendar 的日程和 Chat 里 @他 的事。这个 skill 每天早上（或随时）把这三个源
**实时扫一遍**，收进一个可视化 dashboard，并把能对上 skill 的邮件**预先起草好回信**，
让 Klaus 只做"核对 + 点发送 + 分派"，不用不停刷邮箱被带走注意力。

**核心心法**：这是**每日一次性的调度台，不是常驻窗口**。
- 每次运行都从 Gmail/Calendar/Chat **重新扫**——真相在外部，不在对话历史里。
- 所以**每天开一个新 session** 敲 `/控制台` 即可，起步 token ≈ 0，永远不会满。
- 控制台只做「总览 + 起草 + 分派」；某件事要动手时，用它给的**开场 prompt 另开一个
  session** 去干（Klaus 本就爱并行开 2–3 个）。控制台这个 session 始终很轻。

## FIRST：拿到今天的真实日期 —— 绝不臆测
先跑 `date "+%m/%d/%Y (%A)"`，把结果当作 TODAY 用于：dashboard 抬头、Gmail 的
`newer_than` 窗口、日程的今天/明天判断、邮件"停留天数"计算、deadline 临近判断。
定时运行时你自己的日期感可能是错的，一律以 `date` 为准。

## 工具
所有 Gmail / Calendar / Chat 读取走本地 `gws` CLI（默认身份 **klaus@**；过滤
`Using keyring` 横幅）。语法是 Google API 资源路径：
- Gmail 列表：`gws gmail users messages list --params '{"userId":"me","q":"in:inbox is:unread newer_than:3d","maxResults":10}'`
- Gmail 详情：`gws gmail users messages get --params '{"userId":"me","id":"<id>","format":"metadata","metadataHeaders":["From","Subject","Date"]}'`（正文用 `format:"full"`）
- 日历：`gws calendar events list --params '{"calendarId":"primary","timeMin":"<今天0点-07:00>","timeMax":"<后天0点>","singleEvents":true,"orderBy":"startTime"}'`
- Chat：`gws chat spaces list`（**Chat 授权正常，实测可用**）、`gws chat spaces messages list`

**性能红线（实测）**：`gws` 每次调用走 keyring/auth，约 **20 秒/次**，串行拉 6 封就超时。
两条铁律：
1. **只对 `is:unread` 的邮件拉详情**，cap ~10 封。列表调用一次就够，别为每封都 list。
2. **并行抓取**——所有 `messages get` 用 `&` 同时发起、`wait` 收口，总耗时≈单封 20s：
   ```bash
   while read -r id; do [ -z "$id" ] && continue
     gws gmail users messages get --params "{\"userId\":\"me\",\"id\":\"$id\",\"format\":\"metadata\",\"metadataHeaders\":[\"From\",\"Subject\",\"Date\"]}" 2>/dev/null | grep -v "Using keyring" > "$S/_p_$id.json" &
   done < ids.txt; wait
   ```
   **不要用 `run_in_background`**（无 TTY 会卡 keyring 永不返回）；**不要 `for id in $ids`**
   （word-split 会把多个 id 连成一个 → "Invalid id value"），用 `while read` 逐行。

**只读扫描**——本 skill 不 label、不 move、不 send、不 post。所有会改变外部状态的动作
（发送邮件、加/换星标、归档、发 Chat）都要 Klaus 明确说了才做，且大多分流到各自的 skill 去执行。

---

## 运行步骤

### 1. 扫三个源（只读，窗口 = 最近 3 天 + 未读优先）
- **Gmail inbox**：**只扫 klaus@ 这一个邮箱**（枢纽箱）；团队邮箱
  claims@/piteam@/picase@ 不纳入（发送时各 skill 按案件归属处理，
  [[feedback_send_from_case_mailbox]]）。取 `is:unread newer_than:3d`，并行抓。
  **案件中心过滤（Klaus 明确要求，最关键）**：dashboard **只显示与花名册这些在办案子
  【相关】的邮件**。匹配依据：客户/案名、案件 Gmail 标签（`DB-*` / `LB-*` /
  `✅Case/<name>` / 以案名建的 label，见 [[feedback_case_label_one_per_case]]）、或已知
  对方/诊所/合办所/法院（如 Hernán、LaShine Law、对方律师、Animal Control）。
  **匹配不上任何在办案子的邮件一律不显示**——推广、PI Nerd 论坛帖、newsletter、通用通知、
  以及与这些案子无关的邮件，全部不上 dashboard，也**不做批处理栏**。这是刻意的聚焦。
- **Google Calendar**：klaus@ 今天 + 明天的 event，标出带 deadline / 客户电话 / 例会的。
  （个人重要紧急日程在 Apple Calendar，工作在 Google Calendar —— 见 [[calendar_routing]]。）
- **Google Chat**：最近 24h 内 @klaus 的消息（案件群等），抓空间名 + 谁 @ + 一句诉求。
- **诉讼案件进度**（Klaus 亲自负责的诉讼 —— **权威名单 = 这张 Tracking Sheet**
  `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA`，"Hernan Simo Cases" 共享盘。
  Klaus 确认：**表上的案子都是他负责的；以后加新案 = 他在对应 tab 加一行**，本 skill 无需
  另建花名册）：
  - 读 **3 个案件 tab**（一次 `values batchGet` 读完，别逐案读）：
    - `Dog Bite Cases` → **狗咬案**（dashboard **折叠**，一行一件）。
    - `Labor Cases` → **其他诉讼**（**展开**卡片）。role 看 `Case Status`
      🗡️Defender/⚖️Plaintiff。
    - `PI Auto Cases` → **其他诉讼**（**展开**卡片）。这些是他亲办的 PI/仲裁案
      （如 Jiayu Ma=💉EUO Claim、Zhiping Liu=🗡️UIM Claim/合办 LaShine）。
  - **跳过** `Animal Control` 和 `Sheet5`——它们是 provider/联系方式目录，**不是案子**。
  - 每案进度小结从这几列派生：`Case Status` + 关键日期列（Labor: 1st POS / 1st Def
    Answer / CMC / TSC / Discovery；Dog Bite: Complaint 立案日 / POE / Animal Control
    索证；PI Auto: Objection / Def Answer / CMC）+ `Note`。数据薄时补 [[case_log_and_brief]]
    的 Case Log / 邮件里的最新一封。
  - 空行 / "Example Row" 跳过。行数变化自动适应（新案自动出现）。

### 2. 分类 + 排序（两轴 → 六桶）
- **紧迫度**：court/SOL deadline、今日日程、邮件停留天数。
- **重要度**：诉讼(Hernán) > 客户/对方保险 > 涉钱(disbursement/claim/settlement) > 内部杂事。
- 落桶（**全部限定在花名册案件范围内**）：
  - 🎯 **今日焦点**（最多 3 件，逼聚焦）——今天最该推进的案件动作。
  - ⚖️ **诉讼案件进度**——见上（Labor + PI Auto 展开、狗咬折叠）。这是核心。
  - 🔴 **案件待办邮件**——需我回、且属于某在办案子的邮件（附草稿）。
  - 🔵 **等待中**——已回、等对方（某在办案子）；超阈值（默认 4 天）顶红并备催函。
  - 💬 **Chat @我**——案件群里 @我 的，摘要 + 备草稿。
  - 📅 **案件 deadline**——这些案子今天/临近的截止与开庭。
  - **不设「可批量处理」，非案件内容不显示**。

### 3. 对能映射到 skill 的邮件，预先起草（DRAFT-ONLY）
按下方【常用 skill 路由表】判断每封待回邮件对应哪个 skill，**把回信/动作草稿先备好**
（能自动起草的就草，草稿只预览不发送）；对不上任何 skill 的，只给摘要 + 建议动作。
**绝不自动发送**——Klaus 核对后自己点发。

### 4. 渲染 dashboard（内嵌在 session 里）
用 `mcp__visualize__show_widget` 渲染，widget_code 取
`references/dashboard-widget.html`，把 `{{...}}` 占位换成本次真实扫描数据。
标题 `klaus_control_tower_<MMDD>`。这是【已锁定的 UI】——布局不要改，只填数据；
后续按 Klaus 的使用反馈再更新模板。

**诉讼区块的行模板**（填 `{{LITIG_EXPANDED_CARDS}}` 和 `{{DOGBITE_ROWS}}`）：
- 每个展开案卡（Labor 及其他亲办诉讼），role badge 用 `#efa027`(Defender) / `var(--text-accent)`(Plaintiff)：
  ```html
  <div style="padding:9px 0;border-top:0.5px solid var(--border);">
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
      <span style="font-size:11px;font-weight:500;padding:2px 8px;border-radius:6px;color:#8a5a10;background:var(--bg-warning);">Defender</span>
      <span style="font-size:14px;font-weight:500;flex:1;">{{CASE_NAME}}</span>
      <span style="font-size:12px;color:var(--text-danger);">{{NEXT_DEADLINE}}</span>
    </div>
    <div style="font-size:13px;color:var(--text-secondary);margin-top:5px;line-height:1.5;">{{PROGRESS_SUMMARY}}</div>
  </div>
  ```
- 每个折叠狗咬案行（一行一件）：
  ```html
  <div style="display:flex;align-items:baseline;gap:10px;font-size:13px;">
    <span style="font-weight:500;min-width:150px;">{{NAME}}</span>
    <span style="font-size:11px;font-weight:500;padding:2px 8px;border-radius:20px;color:#185fa5;background:var(--bg-accent);">{{STAGE}}</span>
    <span style="color:var(--text-secondary);">{{NEXT_STEP}}</span>
  </div>
  ```

### 5. 给出文字调度摘要
widget 之后，用简体中文给一段短摘要：
- 今日焦点 3 件，每件附一条**可直接复制的开场 prompt**（自然语言，见下方规则），
  Klaus 复制到新 session 即开工。
- 待回邮件哪些草稿已备好、等他核对发送。
- 等待中有没有超时该催的。
一句话收尾即可，不要罗列"要不要我帮你①②③④"。

**⚠️ 开场 prompt 的写法（实测踩坑，务必遵守）**：
- **用自然语言，不要用未注册的斜杠命令**。`sendPrompt`/复制出去后若以 `/xxx` 开头，
  harness 会当斜杠命令解析；**只有等于 skill 目录全名的才有效**，别的一律
  `Unknown command`。例如 **`/hernan` 不存在**（skill 叫 `hernan-email`）。
- 正确形式 = 「案件 + 要做什么 + 用哪个/哪些 skill」的自然句，例如：
  `处理 Mudong Huang 案（狗咬·未成年·Hernán）：确认 GAL(CIV-010+011) 还缺什么、客户签字声明是否已提供，起草给 Hernán 的回复。用 gal-appointment 和 hernan-email。`
  模型收到会自己经 Skill 工具路由，无需斜杠。
- 一件事可跨多个 skill（如上：GAL + 回信），在 prompt 里都点名。
- 填进 widget `onclick="sendPrompt('...')"` 时，prompt 文本内**不要出现英文单引号**
  （会截断字符串）；用中文引号或去掉。
- `sendPrompt` 是发到**当前 session**；重活建议 Klaus 复制到**新 session** 跑，保持控制台轻量。

---

## 星标状态机（Klaus 的既有习惯 —— 只在他 go 之后执行）
```
新任务邮件 ─▶ 🔴 红叹号 (待我回复，草稿已备)
                │ 我点发送后
                ▼
           🔵 蓝星 (已回，等对方) ─▶ 对方再回 → 自动回到 🔴
                │ 阶段性完成、无需再回但重要（后续可能调信息）
                ▼
           🟡 黄星 (存档参考)
                │ 彻底结束
                ▼
          无星 + 移出 inbox (归档)
```
**技术备注（实测结论）**：Gmail API 只能设「加星 / 不加星」(`STARRED`)，**无法通过 API
指定彩色星标的颜色**（superstar 颜色是客户端按用户设置轮换渲染的，没有 API）。所以状态机
用**同色系自定义 label 镜像**：`⟳待回复`(红) / `⟳等对方`(蓝) / `⟳存档`(黄) —— 一眼可筛、
可用规则批管，思路同 [[intake_sheet_highlight_convention]]。Klaus 现有 113 个 label 里
**没有**这三个状态标签，首次执行发送/归档动作时按需 `gws gmail users labels create` 建好
（配色 red/blue/yellow），之后 `messages modify` 加减。案件归属仍用他既有的 `✅Case/<name>`
标签（[[feedback_case_label_one_per_case]]），状态标签与案件标签叠加、不互斥。

---

## 常用 skill 路由表（任务类型 → skill → 使用效果）
控制台据此把每件事路由到对应 skill，并生成开场 prompt。"使用效果"= Klaus 点进去会得到什么。

| 触发信号（邮件/日程/Chat 里出现） | 路由到 skill | 使用效果（产出） |
|---|---|---|
| 新 WeChat intake zip / "开个新案" | `new-case` | 建案卷+intake表+Drive+tracking+Chat空间+Gmail标签+Docusign retainer，末尾给客户签署文案 |
| 狗咬新案（Hernán） | `new-dogbite-case` | 复制模板案卷 `<Client>-<MMDDYY DOL>`，vision 读证件自动填 intake |
| 客户补发照片/证件 | `supplement-intake` | 归档新图 + 只补 intake 表里还黄的待填格 |
| 要网上报案 / claim | `file-claim` | 走碰运营商门户报案，提交前 gate，回写 claim# 到 intake+tracking |
| 发/寄 LOR 给保险 | `lor-send` | 从模板起草 LOR → PDF → email+fax 双通道发carrier → 归档 + tracking 记录 |
| 新案要 claim + LOR 一条龙 | `file-claim-lor` | file-claim → 取email/un-highlight → lor-send → Master log，两处 gate |
| 转介诊所治疗 | `chiro-referral` / `referral` | 填转介模板+附PD照片 → 直接发诊所 → 蓝星+归档+Chat通知 |
| Exer lien 转介/签署 | `exer-lien` | DocuSign 签 Exer lien（签名前 gate）+ 通知 Exer + 标签 + Chat |
| MRI / PM 专科转介 | `mri-referral` / `pm-referral` / `pm-recommendation` | 生成对应专科转介/建议 |
| 治疗结束、要 demand | `draft-demand` | 读病历账单警报 → 选 3P/UM/UIM/Early 模板 → 建损害表 → demand包PDF（draft-only） |
| Hernán 来邮件 | `hernan-email` | 中文摘要+任务拆解+路由+按他语气起草回复（draft-only） |
| 结算/给诊所或客户开支票 | `write-check` | Rentec 里每个payee建vendor+填Post Expense存草稿（提交前必 gate，信托钱） |
| settled 案要做分账 | `accounting-agent` | 核对+更新Disbursement Sheet+记账+归档+案子转Completed |
| 客户伤情/进度公告 | `injury-update` | 从 intake 生成「💉受伤更新」中文群公告 |
| 要发传真 | `send-fax` | RingCentral 起草 cover page + 附件发传真，回执确认 |
| 撤案/退案 | `withdrawal-draft` | 算SOL填模板→去黄→PDF存Downloads+案卷（draft-only） |
| Hernán 周更新 | `weekly-case-update` | 给Hernán英文 + 给Klaus中文，两份 Gmail 草稿（draft-only） |
| 起草任何文件后自检 | `draft-check` | 按house style逐条核对（日期居中/letterhead/bold RE/非driven/无捏造） |

对不上表里任何一项 = 新型任务：只摘要 + 建议，并在摘要里标记「**这是新型任务，可考虑做成
template/skill**」（服务 Klaus 的系统化目标 [[north_star_goals]]）。

---

## 边界（红线）
- **只读扫描**；发送 / 星标 / 归档 / 发 Chat 一律 Klaus 明确 go 之后再做。
- **绝不捏造**邮件内容或案情；草稿基于真实 thread + 案卷。
- 客户/案件名一律**英文**，不翻中文（[[feedback_client_names_english]]）。
- 外发邮件走 house 格式（[[feedback_email_list_formatting]]）+ 从案件所属邮箱发
  （[[feedback_send_from_case_mailbox]]）——但这些都在被路由到的 skill 里发生，本 skill 不发。
- 每次运行重新扫，不依赖上次对话；控制台 session 保持轻量。
