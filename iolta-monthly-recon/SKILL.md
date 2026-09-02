---
name: iolta-monthly-recon
description: >
  Monthly bank reconciliation for the IOLTA #3618 trust account at 凌图律所 / Law Office of
  Shenqi Cai APC. Use on the 1st of the month, or whenever Klaus says: 月度对账 / 跑一下上月对账 /
  月结 / "对一下 X 月" / monthly reconciliation / month-end close / bank rec / "/iolta-monthly-recon",
  or simply drops a BoA statement CSV with no other words. Given one statement export it ties every
  bank line to a journal row, backfills the journal's `Cleared Date` / `Statement Month` columns,
  and outputs exactly two things: a WORKPAPER (what tied, what didn't, book-vs-bank proof) and a
  TODO LIST (what needs Klaus). Trust money: it NEVER plugs a difference, never invents a payee,
  never fills a balance to make it agree — anything that does not tie is reported and stops the sign-off.
  Sibling of `boa-reconcile` (which drives the BoA site to read individual check images and green the
  Disbursement Sheet); THIS skill is the statement-level month-end close and touches no browser.
  It does not sign the Reconciliation Form and does not disburse anything.
---

# IOLTA #3618 月度对账 — SOP

**一句话**：丢一份 statement 进来 → 出「工作底稿 + 待办清单」两样，账本自动打上 cleared 标记。
**红线**：信托账。**任何数字不许猜、不许填平。**对不上就列出来问 Klaus，宁可不签。

## 固定路径

| 什么 | 值 |
|---|---|
| 主账本 | `~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/Lingtu Law-Disbursement/IOLTA#3618/Account-Journal.xlsx`，工作表 `Account journal` |
| 表头 / 数据 | 表头第 **9** 行，数据第 **10** 行起。**第 1–9 行有合并单元格，openpyxl 从第 1 行扫会崩** —— 一律从第 10 行往后扫 |
| 列 | A 日期 · B Payor/Payee · C Method · D Check# · E Purpose · F Deposit · G Disbursement · H Running Balance · I Client · J Notes · K Reconciled to Ledgers? · L Reconciled to Bank Stmt? · **M Cleared Date** · **N Statement Month** |
| 备份 | 同目录 `Backups/`，命名 `Account-Journal_backup_<YYYY-MM-DD_HHMM>_<用途>.xlsx` |
| 底稿 | `IOLTA#3618/Monthly Reconciliations/Recon-3618-<YYYY>-<MM>-<Month>-WORKPAPER.md` |
| 对账表 | 同目录 `Recon-3618-<YYYY>-<MM>-<Month>.xlsx`（模版在 `IOLTA#3618/Templates/Reconciliation-Form.xlsx`）|
| 状态 | `IOLTA#3618/_STATE.md` |
| 旧账本 | `IOLTA #4854/Account#4854-Journal-Reconciled.xlsx`，工作表 `Acct 4854 (Jan-May 2026)`，表头第 6 行 |
| Activity Log | `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA` → `Activity Log!A:J`，Category「会计」Source「Manual」|
| 引擎 | `scripts/recon.py`（本 skill 目录内）|

## M / N 两列的读法（2026-09-02 建立）

| M Cleared Date | N Statement Month | 含义 |
|---|---|---|
| 有 | 有 | 已逐笔对到手上的对账单 —— 铁的 |
| 空 | 有 | 月份靠合计证明，具体哪天要等那个月的对账单 |
| 空 | 空 | 还没兑现，或兑现在我们手上没有的月份 |

这两列取代了账本里 `--- OUTSTANDING ---` / `--- JULY PENDING ---` 这类分隔行。以前 cleared/pending
的状态活在分隔行里，所以**每个月都得从零重新推一遍**；现在活在行上，月结变成勾对。

## 月度已确认的锚点（不要重推）

| 月末 | 银行余额 | 账本对应 | 状态 |
|---|---|---|---|
| 5/31/2026 | 780,092.77 | 行 10–82 | 逐笔对平，**零 outstanding、零在途** |
| 6/30/2026 | 1,049,028.91 | 行 10–180 | 合计对平到分（H 列公式也正好停在 181）|
| 7/31/2026 | 1,028,876.32 | — | ⚠️ 对账单缺，未回填 |
| 8/31/2026 | 1,208,565.16 | 见底稿 | 闭合，残差 197,531.32 已 100% 拆项 |

#4854 结转进 #3618 = **386,306.90**，三笔 FDES（5/4 的 250,000 + 112,726.90，5/13 的 23,580），
账本行 10 / 11 / 31。**别把它当两笔**——漏掉行 10 那笔 250,000 是已经踩过的坑。

## 流程

### 0. 拿对账单
BoA Business Advantage 360 导出 CSV → 默认落 `~/Downloads/stmt.csv`。
⚠️ **这个文件名每月被覆盖。** 拿到就先改名存档：
```bash
cp ~/Downloads/stmt.csv "<IOLTA#3618>/Monthly Reconciliations/stmt-3618-<YYYY-MM>.csv"
```
eStatement PDF 也行，先转文本：`pdftotext -layout eStmt.pdf out.txt`，脚本认 `.txt`。

### 1. 三行自检 —— 对账单先跟自己对平
期初 + 总贷 − 总借 = 期末。不平就停，重新导出。

### 2. 跑引擎（先 dry run）
```bash
python3 ~/.claude/skills/iolta-monthly-recon/scripts/recon.py \
  --stmt ~/Downloads/stmt.csv --month 2026-09 --bank-end <期末余额>
```
可重复跑，幂等。看清输出再加 `--write`（会自动先备份到 `Backups/`）。

匹配规则，按优先级：
1. **有号支票** = 支票号 + 金额都吻合，且该行没被别的月占用 → 唯一命中才算对上。多个候选时用行自身日期做 tie-break。
2. **银行没读出号的支票** = 按金额在未占用行里筛，并剔除**开票日晚于兑现日**的行（不可能）。剩唯一 → 按排除法认定，并在底稿写明是排除法。
3. **存款** = 把账本存款行按 A 列日期分组，跟当天银行贷记合计比。**整天对平才整组标记**；差一分钱就整组不标，逐行列出来。
   （A 列日期在存款行上就是银行入账日 —— 8 月六个存款日全部这样对平，且当月存款行一个不剩，是完整双射。）
4. **非支票借记**（transfer / sweep / fee）→ 引擎单独列出。**这些必须有自己的账本行**，不能当噪音跳过。

### 3. 把差额拆干净
```
Book(月末) − Bank(月末) = 在途存款 − 未兑现支票 + 银行有账本没有的借记 − 银行有账本没有的贷记
```
四项**每一项都要能列出具体行号或对账单行**。凑不上就是没做完 —— 不许写「大致是时间差」。

Book 要按**月末**算：账本里开票日晚于月末的支票要加回去（例：8 月要把 9 月开的 80372–80378 共 21,558.33 加回）。

在途存款怎么认：**没有任何银行侧证据的存款行** —— A 列没日期，Purpose/Notes 里也没有
"deposited x/x"。注意 `to deposit wk of 7/21` 这种是**计划不是事实**，算在途。

### 4. 写底稿
`Recon-3618-<YYYY>-<MM>-<Month>-WORKPAPER.md`，固定六节：
1. 对账单自身对平
2. 存款 —— 逐日对平表
3. 支票 —— 对上几张 / 号码歧义 / 金额不符 / **账本无此行**
4. 非支票借记
5. Book vs Bank —— 四项拆解，残差必须逐条列出
6. 合规发现（Rule 1.15 Standard (1)(b)：每行要有日期、金额、payor/payee、用途、当前余额）

改版时旧底稿改名加 `(SUPERSEDED <日期>)` 留着，别删。

### 5. 待办清单
只列**要 Klaus 动的**，每条带金额。典型四类：
- 账本无此行的支票 → 调支票影像（**正反面**：payee · memo · client · 签名 · 背书）
- 非支票借记缺账本行 → 要费用分摊才能入账
- 缺的对账单
- 客户归属对不上的存款

### 6. 收工
① `_STATE.md` 追加结论 ② Activity Log 追加一行（只 append，永不改写既有行；Ref/ID 抓全）：
```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA","range":"Activity Log!A:J","valueInputOption":"USER_ENTERED","insertDataOption":"INSERT_ROWS"}' \
  --json '{"values":[["MM/DD/YYYY","HH:MM","IOLTA #3618","会计","<X 月对账：结论一句>","Klaus","<关键号码>","Manual","manual:iolta-monthly-recon","<下一步>"]]}'
```

## 只在 Klaus 明确同意后才做
- 补任何账本行（改 book balance）
- 填 K / L 列
- 把 H 列 running balance 往下拉（目前只到 181 行）
- 填 / 签 Reconciliation Form 的 "agree = Yes"
- 停付、通知银行、对外任何动作

## 已知长期问题（每月扫一眼有没有变糟）
1. **223 行 A 列没日期** —— 日期埋在 Purpose 文本里（`Lien Payment (check 8/26/2026)`）。Standard (1)(b) 要求每行有日期。
2. **K / L 两列 437 行全空** —— 从来没填过。
3. **H 列 running balance 只到 181 行**，182–446 共 265 行没余额。Standard (1)(b) 要求每行有当前余额。
4. **支票号重号** —— 80275 用了两次（r292 Axis $705 / r314 Hong Li $3,210，银行两张都付了）。每月查一次重号。
5. **旧 #4854 800xxx 号段还有六个号在外**：800025 / 800079 / 800080 / 800092 / 800093 / 800094。
   #4854 账本里有一串标了 **Fraud** 的支票（80030–80049，payee 是 Tian Pan / Tian Fan /
   Minh Trang Nguyen / Renguang LLC），而 8 月兑现的六张 800xxx **全部落在 #4854 从没记过的号里**。
   这六个号一旦出现在对账单上，立刻报 Klaus，不要当普通漏记处理。

## 每月自查
- [ ] 对账单三行自检对平
- [ ] 每个存款日整天对平
- [ ] 每张有号支票号 + 金额都对上，或已列入待办
- [ ] 每笔非支票借记都有账本行，或已列入待办
- [ ] Book − Bank 四项拆到分，残差逐条可列
- [ ] 全表查一次重号支票
- [ ] 旧 800xxx 六个号没出现
- [ ] 写前备份到 `Backups/`
- [ ] 底稿 + 待办两样都产出
- [ ] `_STATE.md` + Activity Log 各追加一条
