# Hernán 案件标签树 + 自动打标签设计

## 标签树（klaus@，2026-08 实测）
母标签 `⚖️Hernan Cases`（id `Label_2462494372802428188`）**本身挂 0 封邮件**；
邮件只挂在 **case leaf** 上。分类中间层也不直接挂案件邮件。

| Case (leaf) | Label id | 类别 |
|---|---|---|
| CL-Brian Wu v. Azucanela LLC | Label_2581322858093206735 | Civil Limited |
| DB-Bo Tao-062726 | Label_7788628222844443496 | Dog Bite |
| DB-Guolin Zhao-062126 | Label_1845552354652370299 | Dog Bite |
| DB-Lina Lu-070926 | Label_5980763080143242915 | Dog Bite |
| DB-Mudong Huang-062926 | Label_1856079116373276236 | Dog Bite |
| DB-Weicong Lin-070926 | Label_2 | Dog Bite |
| DB-Yi Cong-041226 | Label_6510174514892044222 | Dog Bite |
| LB-Hansen Li v. Aligcus, Inc | Label_8866899269630938126 | Labor |
| LB-Saihui Tan/CB Kitchen and Bathroom | Label_3403499162978877023 | Labor |
| Jiayu Ma | Label_4186601605671161245 | PI Auto |
| Zhiping Liu | Label_4960110660159648009 | PI Auto |

**不要硬编码这张表**——每次运行动态发现（见 SKILL 扫描步骤）。此表仅供参考 + 记 id。
注意 `LB-Saihui Tan/CB Kitchen…` 名字里带 `/`，Gmail 会当层级 → 该 label 实际多嵌套一层；
用 id 操作即可，别用名字拼 `label:` 查询。

## 自动打标签：为什么"只凭发件人/主题"会翻车（模拟结论）
拉每案最近一封收到邮件模拟，只用 From/Subject 判案子，结果：

| 案子 | 信号 | 能否自动判对 |
|---|---|---|
| Brian Wu / Guolin Zhao / Lina Lu / Mudong Huang / Weicong Lin / Yi Cong / Hansen Li | 主题里有客户名 | ✅ 主题名匹配 |
| Zhiping Liu | 主题是「刘女士」无全名，但发件 `zhipingliu2001@gmail.com` | ⚠️ 要靠**发件地址**，不能只看主题 |
| LB-Saihui Tan | 主题是「CB Kitchen」（雇主名），无客户名 | ⚠️ 要维护**别名/雇主→案子**映射 |
| **DB-Bo Tao** | Hernán 转发「New Message for Order # 28815490」——无名无案号 | ❌ 纯 From/Subject **判不出** |
| **Jiayu Ma** | 主题只有「Claim No.: CL-70-93NTRL-1 / TESLA」 | ❌ 无名，要靠**claim# 映射** |

**根因**：案件邮件的发件人多是内部同事（Claire/Cindy）、Hernán（在所有案子上）、claims@ 转发——
**发件人本身不指向具体案子**；只能靠主题/正文里的名字/案号，而这对 Bo Tao、Jiayu Ma 这类失效。

## 推荐设计（三层，低置信度必须人工确认）
1. **线程继承（最强，先做）**：新邮件先看 `threadId`——若该 thread 里已有邮件挂了某 case leaf，
   新邮件就打同一个 leaf。解决 Bo Tao 转发、Jiayu Ma claim# 回复这类（多为已标记 thread 的续聊）。
   Gmail 原生 filter 做不到线程匹配，但本 skill / routine 能（拉 thread 其它邮件的 labelIds）。
2. **确定性规则**：
   - 主题/正文含客户全名 → 对应 leaf。
   - 唯一发件地址 → leaf（如 `zhipingliu2001@gmail.com`→Zhiping Liu；对方 adjuster 专属地址）。
   - claim# / 案号 映射（如 `CL-70-93NTRL-1`→Jiayu Ma）——维护一张 alias/claim# 映射（可放本文件或小表）。
   - 别名/雇主（`CB Kitchen`→Saihui Tan）。
   高置信可用 **Gmail filter**（服务端即时）承接；new-case / new-dogbite-case 建案时顺手建该案 filter。
3. **低置信 → 不自动打，进 dashboard「待归类」让 Klaus 一键确认**。**绝不瞎标**——错标比漏标更烦。

## 已知缺口
- **Brian Wu（Civil Limited）在标签树里、但不在 Tracking Sheet**（那张表无 Civil Limited tab，
  见 [[limited_civil_commercial_cases]]）。→ 诉讼进度区块拿不到它的 status/日期；需 Klaus 在表里加
  Civil Limited tab/行，或指明它的进度来源。邮件侧（label）不受影响。
