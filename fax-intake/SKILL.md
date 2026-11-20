---
name: fax-intake
description: RingCentral 收传真巡查：抓 Klaus 分机 101 收件箱里新进的入站传真（(626) 323-8181、888 总机、626-479-2207 都落这里），逐份识别是哪个案子，存进该案 Drive 案卷，把原件发到案件 Chat 群并 @负责人（通知里写存到哪），记案件 Activity Log + 凌图数据，每次跑完给 Klaus 一份汇报。定时任务 fax-intake-hourly 每小时跑；Klaus 说「查传真」「跑一下传真巡查」「/fax-intake」时手动跑。不回传真、不发外部消息、不改 RingCentral 设置。
---

# 收传真巡查（fax-intake）

Klaus 11/20 定的流程（原话要点）：下载 → 分析是哪个案子 → 找到该案的 Chat 群，把文件发进去并通知负责人 → 知道该存哪就直接存，并在通知里写明存到哪 → 每次跑完给 Klaus 汇报。内部「收到传真」通知 Klaus 已授权自动发。

## 1. 拉新传真
```
python3 ~/.claude/skills/fax-intake/scripts/rc_inbox.py new --days 14 --out <scratchpad>/fax-run
```
返回未处理的入站传真（message_id、收到时间、页数、来电号码/名字、PDF 和每页 PNG 路径）。已处理的记录在 `~/.claude/automation/fax-intake/state/processed.json`（不入库）。没有新传真 → 结束，不汇报。

## 2. 逐份识别（读每页 PNG）
- 抽出：发件机构、收件人、客户名、DOB、DOL、claim # / 参考号、文件类型（病历 · 账单 · lien · 保险信 · 律师信 · 法院文书 · 其他）、要点（金额、期限、要我们做什么）。
- 对案子：凌图数据 `find` 客户名（必要时用 claim #、DOB 核对）。**只有唯一匹配且至少两项信息对得上（姓名 + DOL / claim # / DOB / 机构与案情相符）才算对上。**
- 对不上、同名多案、没客户名 → **待认领**（见第 5 步），不存案卷、不发群。
- 被 RingCentral 标成 spam 且内容里没有任何我们客户的名字 → 跳过（`mark … skipped_spam`），汇报里列一句。
- 收件人明显不是我们（如写着别家律所的人、客户名在凌图数据查不到） → `mark … misdirected`，不存不发，汇报里列一句。

## 3. 存案卷（出手即归档）
- 案卷 = `find` 返回的 `drive_folder_url`。先列子文件夹，按文件类型放：lien / 医保 subrogation → 跟该机构以前的 lien 放一起（搜 Drive 同机构文件所在文件夹）；病历账单 → 4#（Bodily Injury / Medical）对应诊所子文件夹；保险信 → 3#/4# 对应 claim；律师信 / 转所 / 法院 → 1#Legal Documents。拿不准 → 放案卷根目录，并在通知里写明。
- 命名：`<客户名> - <机构> <文件类型/要点> (fax M-D-YYYY).pdf`。
- 上传前在案卷里搜同一份：Drive `md5Checksum` 对本地 `md5`，相同就不再上传（`mark … duplicate`）。上传后核 MD5。

## 4. 发 Chat + 通知负责人（默认 gws = Klaus@）
- 找群：`gws chat spaces list --params '{"pageSize":1000}'` 翻页读完，displayName 以「<客户全名>-」开头、含 DOL「M-D-YYYY」的群；同车多人群名可能是「A-B-DOL(X)」。必须正好一个，否则当待认领。
- 负责人：群名结尾 `(A)`=Amos、`(J)`=Jerry、`(Z)`=Jenkins、`(K)`=Klaus；从 `gws chat spaces members list` 取对应 `users/<数字id>`。没有后缀 → 用凌图数据 `lead`。
- 附件：`gws chat media upload --params '{"parent":"spaces/<id>"}' --json '{"filename":"<文件名>"}' --upload <pdf> --upload-content-type application/pdf` 取 `attachmentDataRef`。
- 消息（新消息、不挂 thread；格式：第一行只 @，第二行说事）：
```
<users/数字id>
M/D 收到 <机构> 传真：<客户名> 的 <文件类型>，<要点：金额 / 期限 / 对方要什么>（N 页，原件见附件）。已存到案卷 <子文件夹路径>。<要不要处理：下一步一句话，或「无需处理」>
```
- `messages create` body = `{"text":…, "attachment":[{"attachmentDataRef":…}]}`；确认返回有 USER_MENTION 和 1 个 attachment。
- 只发所内案件群；不发客户群、不发外部、不发别的群。

## 5. 记录
- 案件 Activity Log subtab：`python3 ~/lingtu-cm-study/al/al.py read <intake id>` → `append <id> <ROWS> '<13 值>' s:<key>`（Category 按内容：理赔 / 记录申请 / 供应商 / 律师指示；Source=Fax；Ref = `RC fax <message_id> · Drive <file id>`；Actor = 发件机构）。intake id 来自 `find` 的 intake 链接或 `~/lingtu-cm-study/al/registry.json`。
- 凌图数据 `log_event`（document_received，channel=other，挂 matter_code，link=Drive 文件，source_id=`rcfax-<message_id>`，summary 末尾带 `[s:<key>]`）。
- 有新期限才 `sync_case_status`（`hard` 按通知是否硬期限）；Klaus 自己的案子（`(K)`）顺手更新 next_step。
- 待认领：PDF 放 `~/Downloads/传真待认领/`，命名 `<收到日期> <机构> - <类型>（<猜测/缺什么>）.pdf`；中央 Activity Log 追加一行，Next Step 以「Klaus：认领传真 …」开头（会上 Task To-do 面板），写上你的猜测。
- 每份处理完：`rc_inbox.py mark <message_id> <filed|unclaimed|skipped_spam|misdirected|duplicate> <一句话>`。

## 6. 汇报 Klaus（每次有新传真就发）
发到 Google Chat「Klaus-Claude Agent Notice Group」（`spaces/AAQA-WwExfU`），新消息，纯文本：
```
【传真巡查 M/D HH:MM】新传真 N 份
1. <机构> → <客户>（<案号>）· <类型/要点> · 已存 <路径> · 已 @<CM>
2. …（待认领 / 跳过 / 发错的也逐条列，写原因）
```
没有新传真不汇报。

## 不做
- 不回传真、不发邮件、不往客户群或外部发消息、不改 RingCentral 路由 / 已读状态。
- 不编造：读不清的字写「读不清」，不猜金额、不猜案号。
- 凭据（`~/.ringcentral.env`）不进 git、不进 Drive。
