---
name: boa-reconcile
description: >
  BoA IOLTA #3618 bank-side reconciliation sweep for 凌图律所 / Law Office of Shenqi Cai APC.
  Use whenever Klaus says: 对账 / 对一下账目 / reconcile BoA / 银行对账 / "登录 BoA 对账" /
  "把 X 月的过一遍" / "抓取 counter credit" / "/boa-reconcile". Works the BoA Business Advantage 360
  site inside Klaus's ALREADY-LOGGED-IN Chrome (Claude-in-Chrome). Two lanes:
  ① OUTGOING checks — read each check image (payee+memo), cross-check the Rentec IOLTA ledger,
  flip the matching YELLOW cell GREEN on the 2026-Disbursement Sheet `Internal ` tab, then tick
  BoA Reconcile (rule from Klaus 2026-08-28: 对上且标绿 → 勾; 对不上 → 不勾并报告).
  ② DEPOSITS (Counter Credit / Mobile) — open each deposit's thumbnails, read every component
  check image, 3-way match (check# + amount + client) against Account-Journal JULY/AUG PENDING
  pre-logged rows, fill cleared dates + add missing rows (backup xlsx first), green the Pending
  Disbursed Sheet settlement cells / create missing tabs, then tick Reconcile when the components
  sum EXACTLY to the deposit. Never touches transfers/fee sweeps without explicit instruction.
  NEVER types passwords — if BoA is logged out, STOP and ask Klaus to log in.
---

# BoA IOLTA Reconcile — 完整作业手册

## 固定 ID / 路径
| 什么 | 值 |
|---|---|
| BoA 账户 | Public Service Trust - **3618**（Business Advantage 360）|
| Rentec IOLTA ledger | `https://secure.rentecdirect.com/owners/bank_account.php?bank_id=111793` |
| 2026-Disbursement Sheet | gsheet `1Av8_fj3MAekCM6RujmGWuFsYRnSG6MMbAskvPkFcs2U` tab **`Internal `**(尾空格) sheetId `1554087303` |
| Pending Disbursed Sheet | `1b_vPr9WD7P9arR6DTTJRxeWs0apk8DTiTgc2iAzIrR0`（Template of 1/3 = sheetId 0）|
| Completed Disbursed Sheet | `1EvsbLjAuRdTTfH3uyEmV3qFjmAtKCdfBPByVCMAF1kA`（对账不用它——搬案时全绿，看不出兑现）|
| Account Journal | `~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/Lingtu Law-Disbursement/IOLTA#3618/Account-Journal.xlsx`，写前必备份到同目录 `Backups/` |
| Activity Log | `1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA` → `Activity Log!A:J` |

颜色：绿 = `{red:0,green:1,blue:0}`(#00ff00)，黄 = `{red:1,green:1,blue:0}`。非零才涂，$0 留白。

## 铁律
1. **绝不新开 `secure.bankofamerica.com` tab** —— 触发 re-auth 把 Klaus 挤下线（踩过）。只用他已开的 tab。
2. **绝不代输密码**。登录页/登出页 → 停，请 Klaus 登录。会话闲置 2 分钟会弹超时框（点 OK 续命）；
   我方长时间做 sheet 工作时 BoA 会静默登出——回来发现登出就再请 Klaus。
3. **View/Edit 是 modal**，关 modal 回列表；**绝不按浏览器后退**（跳 signIn 页）。
4. Klaus 的勾选规则（2026-08-28 口谕）：**disbursement sheet 找到对应金额且标绿 → 勾 Reconcile；
   对不上（无行/差额/无记录）→ 不勾，报告**。差 1 分钱也不勾（例：80277 差 $0.09）。
5. 存款(CC/Mobile) 勾选前提：**组成加总与存款额精确相等** 且全部完成 journal 三重匹配。
6. Transfer / fee sweep(如 to CHK 2995) 一律不动，除非 Klaus 明说。
7. Internal 表**行号天天漂移**（新案插行）——每次改色前按客户名 fresh lookup，绝不用旧行号。
8. 改色三段式：pre-flight(确认全黄) → batchUpdate repeatCell → re-check(确认全绿)。
9. 只 append Activity Log，收工一行(Category 会计, manual:iolta-<mon>-reconcile, Ref 带支票号段)。

## BoA 操作(全部 javascript_tool 驱动，tabId=已开 BoA tab)
- **设 filter**: `#search-filters-link`.click → setSel('search-filter-timeframe-select','month') →
  等 800ms → setSel('search-filter-month-select','MM YYYY') → setSel('reconcile-select','N') →
  `#apply-search-filters`.click。setSel 必须用原型 setter + input/change 事件:
  ```js
  function setSel(id,val){const s=document.getElementById(id);
    const st=Object.getOwnPropertyDescriptor(window.HTMLSelectElement.prototype,'value').set;
    st.call(s,val);s.dispatchEvent(new Event('input',{bubbles:true}));s.dispatchEvent(new Event('change',{bubbles:true}));}
  ```
- **交易表**: `#txn-activity-table`，rows[0]=表头 rows[1]=banner，数据行 `cells.length>4`。
  列: 0=Posting date 1=Description(含 View/Edit) 3=Amount 5=Reconcile checkbox
  (`input[name=reconcile-checkbox]`)。**一页 50 行**，"View more" 加载更多（会产生重复行，按
  date|desc|amt 去重；有时点击后 filter 失效混入已勾行——重新设 filter）。
- **看支票影像**: 行内 `a[id^=view-txn-details]`.click → 等 2.8s → `#checks-accordionPanel0 img`
  scrollIntoView → 用 computer zoom 截 region（region = rect × 1568/window.innerWidth ± 6px）。
  读 PAY TO THE ORDER OF + MEMO + 票面日期 + 支票号。关 modal: `button[aria-label="close Dialog"]`。
- **看存款组成**: 打开 deposit 的 modal 后有 `[id^=deposit-slip-thumbnail]` 缩略图排
  （-1=Deposit Slip，-2 起=每张组成支票按金额标注）。逐个 click → 同法 zoom 读。
  Mobile Deposit 用描述里的确认号定位行。
- **勾 Reconcile**: checkbox.click → 等 ≥900ms（服务器保存）→ **一批勾完必须重设 filter 复查**：
  Non-reconciled 视图有快照延迟，**以 Reconciled 视图（reconcile-select='Y'）出现为准**。
  一次 js call 里连点多个易超时(45s CDP 限)——每 call ≤4 个勾，或单勾单 call。
- **Reconciled 视图顺带扫一遍**：能发现被勾过但 journal 没日期的存款（踩过：Jianjun Li 14k、
  Zhiping Liu 57.8k 早已入账，Non-reconciled 扫不到）。

## Rentec 反查(免登录信息源，tab 已常开)
ledger 页 body.innerText 按行 split，支票号所在行 i 的 [i-4..i+1] = 日期|payee|科目|memo|支票号|金额。
科目: `7000 Provider Reimbursement`=诊所 lien(→provider 列)、`7010 Client Compensation`=客户
recovery(→J 列)、`7020 Medical Payment Return`=MedPay 还保险(→U-Z 保险公司列，不是 M!)。
memo 格式 `<Client>, DOL-MM/DD/YYYY`。页面是懒加载——bodyLen<1000 就等几秒重读。

## Internal 表匹配
读 `Internal !A1:EK<末行>` 带 backgroundColor，按客户名建行索引(一名多行都收)，在该客户行里扫
D..EK 找金额==支票额的格。歧义时以**支票收款人**定列(如同额 Exer vs Shin Imaging)。
客户 recovery 必须落 J 列。找不到行/金额 → 不动不勾，报告（常见原因：案子没录 Internal——
Xiaohua Yu 型;或差额——80277 型）。列结构见 accounting-agent skill(U-Z=保险公司,AA+=providers)。

## Journal 更新(openpyxl)
表头 row9: Date|Payor/Payee|Method|Check#|Purpose|Deposit|Disbursement|RunningBal|Client。
JULY/AUGUST PENDING 区的预登 deposit 行 Date 为空；对上银行后填 `datetime(Y,M,D)` +
number_format='M/D/YYYY'。写前 assert：client 列匹配、Date 原本为空。缺的组成支票 → 在
PENDING 区末尾空行 append 完整行(标注 "ADDED from bank check image")。**改前 shutil.copy 备份**。

## Pending Disbursed Sheet 更新
- 收到支票的案子：该客户块的 settlement 格(3P=B2 / UM-UIM=B3；多客户块纵向堆叠，第2块≈row19)
  涂绿。先读宽范围(A1:C40)确认块位置，别只读 9 行(踩过：以为块缺失差点重复建)。
- 无 tab 且未结案：duplicateSheet(sourceSheetId 0) 建 tab，填 8 行块(名字/DOL/金额/1/3 fee)，
  绿 settlement 格。多人同案一个 tab 纵向多块。UIM/MedPay 未结的案子**不建**(Klaus 规则)。
- 写值前 values.batchGet 确认目标区为空。

## 流程顺序(每月/每次)
1. `date` 读真实日期。BoA 设 filter(目标月+Non-reconciled) → 列全量(View more 到底,去重)。
2. 支票 lane：Rentec 反查全部支票号 → 逐张 View/Edit 读影像核 payee/memo → Internal fresh
   lookup 匹配 → pre-flight → 改绿 → 复查 → BoA 勾 → 重设 filter 服务器端确认。
3. 存款 lane：逐笔开 thumbnails 读组成 → journal 三重匹配(check#+金额+client) → 差异报告
   (缺行即补,金额不符只报不改) → journal 填日期/补行 → Pending sheet 绿/建 tab → 组成精确
   加总后 BoA 勾 → Reconciled 视图复查。
4. Reconciled 视图扫漏网(被勾过但 journal 无日期的存款)。
5. Activity Log 一行收工；差异清单(不勾的+原因)必须完整报给 Klaus。

## 已知悬案速查(报告时别当新发现)
- 80277 Yan Li→Kaisheng Yang $3,570.70 vs 表 $3,570.79：等 Klaus 的 $0.09 补票。
- Junke Li $1,000 MedPay：1P 直付、subrogation waived、**永不入账**(Chat 8/6 确认)；trust 按
  $4,500 分了 $3,500 的钱——处理方向等 Klaus 裁定。
- Xiaohua Yu UIM $10,000 (AIG 1646181779)：journal 预登未清；她的 disbursement 未录 Internal。
- Xiuying Wang(tab, DOL 2/12) vs Xueying Wang(Hudson 支票, DOL 6/2)：拼写疑点待 Klaus。
- 80275 重号两张(Hong Li $3,210 + Axis $705)——月结对 Journal 时别绊住。

## 相关
[[accounting-agent]](per-case 记账+月结 mirror 的 SOP 本体) · [[write-check]](Rentec 开票) ·
memory `iolta_disbursement_workflow`。
