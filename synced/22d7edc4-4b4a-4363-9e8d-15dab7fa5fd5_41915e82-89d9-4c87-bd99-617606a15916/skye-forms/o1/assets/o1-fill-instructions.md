# O-1 表格材料信息模板（O-1A / O-1B）

本模板用于每个 O-1 案件，覆盖 **I-129（含 O and P 附表）+ I-907 + G-1650 ×3 + G-28（如有）** 四类表格。

Fixed = 律所固定信息，每案通用，不用重新收集。

Flexible = 客户信息，每案不同；每条后面标明具体填在哪份表格的第几页、第几 Part、第几 Item，方便直接照抄，不用重新去翻表格结构。

## 本文档存放在哪 / 填好的表放在哪

**每次填表都从 `0.testing` → `Test O1B` → `2. Form` 取本文档** —— 那一份是所有更正落地的地方，读它才能让上周修的东西真正用到这个案子上。`0 Sample （O1）` → `3.Forms / Offer / Itinerary` 是同内容的镜像，改动要两边同步。

**填好的表格放到指令里指定的那个客户 Drive 文件夹**，不要放回测试文件夹。指令没说放哪就问。

客户信息填在**副本**上（可以复制一份到输出文件夹，命名 `O-1 填表指令 — 客户名`），**不要写进 `Test O1B` 里这一份** —— 它是后面每一次填表都要读的源，被某个客户的数据污染以后，下一个案子就会带着别人的信息起手。

## 填表原则

1. **表格一律从官网现下载，不参考任何旧案子、旧模板、旧样本的 PDF。** 旧文件的版次可能已过期（字段名会变），存久的副本 AcroForm 可能已损坏，而且会把旧的律所信息（旧电话、空着的执照号）一起带进来。
2. **值只来自本文档的第三节；位置只来自当期官网表格自己印的题号和说明。** 遇到本文档没写到的题，看表格自己的题干和 Instructions，不要去翻别的案子怎么填的。
3. 下载后先核 **Edition Date**：对着该表格自己的 USCIS 页面（那一页有个 Edition Date 折叠框）核，不是看 PDF 页脚的 Expires 日期。G-28 页脚写着 2021 年过期，但官网明确说 09/17/18 版仍可用。
   **如果核出来的版次和本文档下面记的不一样，先停下来提示办案人，不要直接接着填。** 换版意味着字段名和题号位置都可能动过，本文档标的 Page / Part / Item 会失效，要先重新核字段图谱、再更新本文档，然后才填。
4. 勾选框的取值不能猜，也不能只看字段名 —— 要对着页面上印的选项位置确认。本文档标出的每个勾选值都是这样核过的。

## 移民局固定表格链接

I-129：<https://www.uscis.gov/sites/default/files/document/forms/i-129.pdf>

I-907：<https://www.uscis.gov/sites/default/files/document/forms/i-907.pdf>

G-1650：<https://www.uscis.gov/sites/default/files/document/forms/g-1650.pdf>

G-28：<https://www.uscis.gov/sites/default/files/document/forms/g-28.pdf>

（表格版本，2026-08-20 核：I-129 edition 02/27/26，I-907 edition 04/01/24，G-1650 edition 06/03/25，G-28 edition 09/17/18。若 USCIS 更新了版本，先核 Edition Date，本文档标的页码和 Item 位置可能已变。）

费用表：<https://www.uscis.gov/sites/default/files/document/forms/g-1055.pdf>（I-129 看 Appendix A，加急费看 I-907 那一行）

寄件地址：<https://www.uscis.gov/i-129-addresses>

---

# 一、填表前必须先确认（本案参数）

**下面这些由指令给出或向办案人确认，定完再动表格。** 定错了整套要重填。

指令里应当带到的三样：**COS 还是 CP**、**通知哪个领馆**（Part 4 Item 1 的 b. 城市）、
**本案有没有 G-28**。缺哪样就问，不要推。担保形式和是否小雇主从客户材料里读。

## 1. COS 还是 CP

**指令里会给，不要自己推。**

| | 含义 | I-129 Page 2, Part 2 Item 4 |
|---|---|---|
| **CP**（Consular Processing，领馆签证） | 受益人在境外，或要出境去领馆签 O-1 签证 | 勾 **a.**「Notify the office in Part 4. so each beneficiary can obtain a visa or be admitted」 |
| **COS**（Change of Status，境内转换身份） | 受益人已在美国境内，直接转成 O-1 身份 | 勾 **b.**「Change the status and extend the stay of each beneficiary...」 |

只能勾一个。相关联动：

- 表格自己写明 b. 仅在 Part 2 Item 2 勾了「New employment」时可用 —— O-1 初次申请正是 New employment，所以没冲突。
- **CP 和 COS 都要填 I-129 Page 3, Part 4 Item 1**（领馆类型 Consulate / 城市 / 国家）。COS 案子也填，作为万一境内转换不批时的退路 —— 表格 Item 1 的题干本身就是这个意思（"或者境内转换/延期不能批准时"）。
- COS 的话，受益人当前身份和身份到期日（Page 3, Part 3 Item 6）必须填全，否则审案官无法确认境内转换资格。

## 2. 有 G-28 还是无 G-28

| | 有 G-28（律所代理） | 无 G-28（担保人自己递） |
|---|---|---|
| G-28 | 要做 | 不做 |
| I-907 Page 1 填谁 | 律师姓名 + 律所地址 | 担保人姓名 + 担保人地址 |
| I-907 Page 1 律师区块 | 勾「Form G-28 is attached」+ 填执照号 + 律师 USCIS 账号 | 整块留空 |
| I-907 Page 2, Part 1 Item 8 | 勾 **b.**「I am the attorney or accredited representative **for the petitioner**」 | 勾 **a.**「I am the **petitioner**」 |
| I-907 Page 3, Part 3 联系方式 | 律所电话 / 传真 / 邮箱 | 担保人自己的电话 / 邮箱 |
| I-129 | **I-129 全表没有任何 G-28 字段**，只有 Page 7, Part 8（Preparer）受影响 | Part 8 一般留空 |
| 补件 / 批准通知寄到 | 律所地址 | 担保人地址（要提前跟担保人讲清楚，通知不经过律所） |

## 3. 担保形式 + 是否小雇主

**担保形式：公司担保 还是 个人担保（Agent）**

| | 公司担保 | 个人担保 / Agent |
|---|---|---|
| I-129 Page 1, Part 1 | 只填 **Item 2 公司名**，Item 1 留空 | 只填 **Item 1 个人姓名**，Item 2 留空 |
| I-129 Page 1, Part 1 Item 5 FEIN | 公司 FEIN，写成 `XX-XXXXXXX` | 无 FEIN 填 `N/A` |
| I-129 Page 6, Part 5 Item 12 | 公司主营业务 | `Agent` |
| I-129 Page 6, Part 5 Item 13/14/16/17 | 成立年份 / 人数 / 税前 / 税后收入 | 多数填 `N/A` |
| I-907 Page 2, Part 2 Item 4 | 公司名写进 **Family Name** 框 | 个人姓 / 名分开填 |
| I-129 Page 28, O 附表 Item 1 | 公司名 | 个人姓名 |
| G-28 Page 2, Part 3 | Item 5a/5b 填**代表公司签字的那个人**；Item 7a 填公司名、7b 填他的头衔 | Item 5a/5b 填担保人本人；Item 7a/7b 留空 |

Part 1 的 Item 1 和 Item 2 **互斥**，两个都填会让审案官搞不清谁是 petitioner。

**是否小雇主**：担保方在美国全职等效员工是否 ≤ 25 人（含关联公司、子公司）？→ I-129 Page 6, Part 5 Item 15

- 是 → I-129 费 $530 + Asylum Program Fee $300
- 否 → I-129 费 $1,055 + Asylum Program Fee $600
- 非营利 → I-129 费 $530 + Asylum Program Fee $0

**不要默认勾「是」。** 这一格必须和 Item 14（人数）以及两张 G-1650 的金额一致，对不上就是少交钱，直接退件。

---

# 二、Fixed 律所固定信息（每案通用）

律师姓名：Shenqi Cai（Family Name: Cai / Given Name: Shenqi）

律所名称：Law Office of Shenqi Cai APC

律所地址：13191 Crossroads Pkwy N, Ste 295, City of Industry, CA 91746, USA

律所电话（Daytime / Mobile 统一用此号，纯数字，不要括号和横杠）：4155479999

律所邮箱：cassie@lingtulaw.com

律所传真：6262402046

执业执照号 / 发照机构：348794 / the State Bar of California

律师 USCIS Online Account Number：063938833828

G-1650 ACH 扣款账户：Business Account / Checking / Bank of America / Routing 121000358 / Account 325210063004（开户人 Shenqi Cai，Business Name 填 Law Office of Shenqi Cai APC）

这些信息填在（仅「有 G-28」时填 G-28 那几处）：

  → G-28 Page 1, Part 1（律师姓名 Item 2a/2b、地址 Item 3、电话 Item 4、Item 6/7 见下方注意、传真 Item 7、USCIS 账号 Item 1）

  → G-28 Page 1, Part 2（Eligibility：勾「我是有资格的律师」、执照号 Item 1b、发照机构 Item 1a、勾「不受任何限制执业的命令约束」、律所名 Item 1d）

  → G-28 Page 3, Part 4 Item 1a（原件通知寄律所地址）

  → I-907 Page 1 律师区块（勾 G-28 附件框 + 执照号 + 律师 USCIS 账号）

  → I-907 Page 1, Part 1 Item 3 + Item 5（有 G-28 时，填表人写律师姓名 + 律所地址）

  → I-907 Page 3, Part 3 Item 3/4/5/6（有 G-28 时的 Daytime / Mobile / Fax / Email）

  → G-1650 Bank Account Holder Information + Bank Account Information（勾 Business Account、开户人 Shenqi Cai、Business Name 律所名、勾 Checking Account、Bank Name / Routing / Account）

  → I-129 Page 7, Part 8（Preparer）：两份存档案例都留空，**填之前先问蔡律**，不要自己决定填还是不填

注意（都是核实过的、只看字段名会填错的地方）：

- **G-28 Page 1 的 "Line6_EMail" 和 "Line7_MobileTelephoneNumber" 内部命名和视觉位置是反的** —— 电话号码要填进名字叫 "EMail" 的那个框（视觉上是 Mobile Phone 位置），邮箱要填进名字叫 "MobileTelephoneNumber" 的那个框（视觉上是 Email 位置）。
- **G-28 Part 2 Item 1b 执照号是最容易漏的一格**，旧样本文件那一格是空的。每次都要填 `348794`。
- **I-907 Page 3 的传真框，字段名是 "P3_Line5_MobileTelePhoneNumber" 的 `[1]` 号** —— 手机字段的第二个实例其实是 Fax 框。
- **G-1650 的 "CB_CreditCardType" 是 Checking / Savings 那一对勾选框**，不是信用卡类型；左边那个（`/V`）是 Checking。
- 所有 Apt / Ste / Flr 勾选框的取值**自带前后空格**：`"/ APT "`、`"/ STE "`、`"/ FLR "`。
- **律所电话用 4155479999。** 旧文件里出现的 `8186658535` 是旧号，不要从旧案子抄。

---

# 三、Flexible 客户信息（逐项标明填在哪）

以下"客户"分两个角色，填之前先分清：**受益人 = O-1 申请人本人**；**担保人 / Petitioner = 递交申请的雇主或 agent**。O-1 的 G-28 客户是**担保人**，不是受益人。

## 【受益人姓名】

姓（Family Name）：___
名（Given Name）：___
中间名（如有）：___

  → I-129 Page 2, Part 3 Item 3（受益人姓名）

  → I-129 Page 28, O 附表 Section 1 Item 2.a（Name of the Beneficiary —— 一个整行框，姓名写在一起，不分姓名格）

  → I-907 Page 2, Part 2 Item 5（Beneficiary in the Related Case）

  → G-1650 ×3 每张的 Applicant's/Petitioner's/Requester's Information（Given Name / Family Name）

## 【受益人出生日期 DOB (mm/dd/yyyy)】：___

  → I-129 Page 3, Part 3 Item 5

## 【受益人性别 Sex】：Male / Female

  → I-129 Page 3, Part 3 Item 5（勾对应框）

## 【受益人出生国家】：___

## 【受益人出生省份】：___

## 【受益人国籍 / Citizenship】：___

  → I-129 Page 3, Part 3 Item 5（三项同在 Other Information 区块。出生省份那一格的字段名叫 `Part4Line3_DProvince`，名字里带 Part4 但实际在 Part 3）

## 【受益人 A-Number（如有，纯数字不含 "A-" 前缀）】：___

## 【受益人 SSN（如有，9 位纯数字无横杠）】：___

  → I-129 Page 3, Part 3 Item 5

## 【受益人当前在美国境内？】是 / 否

若在境内，以下整组都要填（**COS 案子必填**）：

最近入境日期：___
I-94 号码：___
护照号：___
护照签发国：___
护照签发日期：___
护照到期日期：___
当前非移民身份：___（如 `F1`、`L1A`）
身份到期日：___（日期，或 `D/S`）

  → I-129 Page 3, Part 3 Item 6

  **这两格一律从 I-94 抓，不从 I-20、签证页或聊天记录推。** I-94 上的
  `Class of Admission` 就是「当前非移民身份」，`Admit Until Date` 就是「身份到期日」
  （常见是 `D/S`，照抄 `D/S`，不要换算成日期）。

  **案卷里没有 I-94（或那份已经一年以上）的话，去官网现取。** 用浏览器工具驱动
  Chrome 完成（`gws` 是 Google Workspace 的 CLI，控制不了浏览器，别用它）：

  1. 在浏览器里打开 <https://i94.cbp.dhs.gov/search/recent-search>，进
     「Get Most Recent I-94/I-95」，把页面开到查询表单。
  2. **页面会弹一个必须滚动读完才能同意的 Terms of Service，这一下由办案人自己点**，
     不要让自动化代点 —— 那份条款本身就禁止用自动化访问该站，机器代勾等于声明遵守一
     个自己不满足的条件。这不是 cookie 横幅，是把律所绑进条款的那道门。
  3. 把五项值备好给办案人粘贴：**Last/Surname、First (Given) Name、Date of Birth、
     Passport Number、Passport Country of Issuance**。这五项在本节里本来就要收集。
  4. 结果页存成 PDF，**放进本案表格文件夹**，命名 `I-94 客户姓名.pdf`。
  5. 再回填「当前非移民身份」和「身份到期日」两格。

  **用哪本护照的号**：用受益人**最后一次入境时用的那本**，不一定是现用护照。入境之后
  换过护照的，要用旧号；提交前先拿入境日期对一下护照签发日。

  存档不是流程装饰：I-94 是这两格取值的唯一出处凭证，审案官或同事复核时要看得到。

  **边界**：一次只查一条、只查本所在办案件的客户本人、只为这次填表用。CBP 站点条款
  禁止的是批量抓取 / 数据挖掘，不是律所替自己客户做单条查询；但也正因为如此，不要拿它
  批量跑名单，也不要把结果留在案件文件夹以外的地方。姓名或护照号有任何不确定，先跟
  客户核实再查，不要用几种拼法反复试。

  注意 I-94 只反映**最近一次入境**。换学校、转 CPT/OPT 不会产生新的 I-94，所以
  `Class of Admission` 仍是入境时的那个身份。如果案卷里的 I-94 是一年以上的旧件，
  重新取一份确认没有新入境记录，比直接用旧件稳。

  注意两处：**护照签发日和到期日两个框紧挨着**，字段名 `Line11e_ExpDate[0]` 是**到期**、`[1]` 是**签发**，填反了肉眼看不出来但记录是错的；**当前非移民身份是 151 项下拉框**，只认代码（`L1A`、`F1`），打描述会被丢掉。

## 【受益人美国现住址】（不能填邮政信箱）：___

  → I-129 Page 3, Part 3 Item 7

## 【受益人境外地址（含邮编）】：___

  → I-129 Page 4, Part 4（地址区块）

  → 地址太长装不下时接到 I-129 Part 9 Additional Information 续页，标注「Page 4 / Part 4 / Item d」

## 【受益人电话 / 邮箱】

美国电话：___
境外电话：___
邮箱：___

  → G-28 Page 2, Part 3 Item 9/10/11（Daytime Phone / Mobile / Email）—— 仅「有 G-28」且客户联系方式指的是担保人时；受益人自己的联系方式不填在 G-28 上

  注：I-129 上没有单独的受益人联系方式栏，Part 7 填的是担保方签字人的联系方式。

## 【Part 4 Item 1 —— 通知哪个领馆】

**a. Type of Office：固定勾 `Consulate`**（不用 Pre-flight inspection，也不用 Port of Entry）

**b. Office Address (City)：___** ← **填表时由指令给出是哪个领馆**（北京 / 上海 / 广州 / 沈阳……）。
指令里没给就问，不要按客户籍贯或护照签发地猜。

**c. U.S. State or Foreign Country：固定填 `China`**

  → I-129 Page 3, Part 4 Item 1

CP 和 COS **都要填这一组**。COS 案子填它是作为境内转换不获批时的退路 —— Item 1 的题干
本身就是这个意思。三格里只有 b. 是每案不同的。

## 【担保人 / Petitioner 基本信息】

个人担保 —— 姓 / 名 / 中间名：___
公司担保 —— 公司名：___
邮寄地址（In Care of Name / 街道 / 单元 / 城市 / 州 / 邮编 / 国家）：___
电话（Daytime / Mobile）：___
邮箱：___
FEIN（公司担保，写成 `XX-XXXXXXX`）：___

  → I-129 Page 1, Part 1 Item 1（个人）**或** Item 2（公司）、Item 3 地址、Item 4 联系方式、Item 5 FEIN

  → I-129 Page 28, O 附表 Section 1 Item 1（Name of the Petitioner，整行框）

  → I-129 Page 30, O 附表 Section 2 Item 1（这里姓 / 名 / 中间名分三格）+ Item 3 联系方式

  → I-907 Page 2, Part 2 Item 4（Petitioner or Applicant in the Related Case；公司名写进 Family Name 框）

  → I-907 Page 3, Part 2 Item 8（担保方 / 公司地址）

  → G-28 Page 2, Part 3 Item 5a/5b 姓名、Item 7a 公司名 + 7b 头衔、Item 8 客户 USCIS 账号（如有）、Item 9/10/11 联系方式、Item 13 邮寄地址

  → 无 G-28 时另外还要填：I-907 Page 1, Part 1 Item 3 姓名 + Item 4 公司名 + Item 5 邮寄地址 + Item 2 客户 USCIS 账号（如有）

## 【担保方是否非营利组织 / 政府研究机构】：是 / 否

  → I-129 Page 1, Part 1 Item 6（一般勾 No）

## 【授权签字人】

姓名：___
头衔 Title：___
电话：___
邮箱：___

  → I-129 Page 6-7, Part 7 Item 1（姓名 + 头衔，头衔在姓名下面那一格）、Item 3（电话 + 邮箱）

  → I-907 Page 2, Part 2 Item 6（Name of Point of Contact + Position Title）

  → G-28 Page 2, Part 3 Item 7b（公司担保时的头衔）

  签名和签名日期一律留空。

## 【公司担保 —— 公司经营信息】

主营业务 Type of Business：___
成立年份：___
当前美国员工人数：___
是否 ≤25 人（见第一节第 3 项）：是 / 否
税前年收入 Gross Annual Income：___
税后年收入 Net Annual Income：___

  → I-129 Page 6, Part 5 Item 12 / 13 / 14 / 15 / 16 / 17

## 【职位与雇佣条件】

职位名称 Job Title：___
薪酬金额 + 单位：___（单位写 `hour` / `week` / `month` / `year`，不要只写一个字母）
其他报酬说明（如有）：___

  **多个 offer、时薪不一样的情况**：材料里出现两份以上 offer 且薪酬不同（例如
  A 公司 $65/hour、B 公司 $100/hour），第 9 题填**本次 petition 对应那份 offer** 的
  金额，然后**第 10 题 Other Compensation 必须加一句说明**：

  > Different wage for different project.

  不加这句的话，第 9 题的单一数字会和附件里几份不同金额的 offer 互相矛盾，审案官看到
  的就是"记录内部不一致"—— 这正是拒信里最常被抓的那类问题。第 10 题写清楚，就变成
  一个已解释的事实。
是否全职：是 / 否；非全职则每周小时数：___
雇佣起止日期（初次 O-1 最长 3 年）：___ 至 ___
  ← **From / To 两个日期都取自客户的 offer / 雇佣合同里写的 O-1 起止时间**，不要自己拟。
  合同上的起始日已经过去的话，那份合同就不能用了，要先让担保人出一份日期前瞻的新 offer；
  日期没定之前这两格留空，不要拿旧日期凑。
是否随本次递交行程表 itinerary：是 / 否
是否会在其他公司场地工作（off-site）：是 / 否
是否只在北马里亚纳群岛 CNMI 工作：是 / 否（一般 No）

  → I-129 Page 5, Part 5 Item 1 职位、Item 2 LCA（O-1 填 `N/A`）、Item 4 行程表、Item 5 off-site、Item 6 CNMI、Item 7 全职、Item 8 周工时、Item 9 薪酬、Item 10 其他报酬、Item 11 起止日期

  → 每周工时不固定的，Item 8 留空并在 Part 9 续页写说明，标注「Page 5 / Part 5 / Item 8」

## 【工作地点】（与 Part 1 地址不同时才填）

地点 1：街道 / 单元 / 城市 / 州 / 邮编：___
地点 1 是否第三方场所：是 / 否；是则填第三方机构名称：___
地点 2（如有）：同上
地点 2 是否第三方场所：是 / 否；机构名称：___

  → I-129 Page 5, Part 5 Item 3（两组地址）

  注意：那两个「是否第三方场所」勾选框的取值是 **`/1`（是）和 `/0`（否）**，不是 `/Y`/`/N`；超过两个地点接到 Part 9 续页。

## 【O 类别与活动内容】

类别：O-1A（科学 / 教育 / 商业 / 体育）/ O-1B（艺术、影视）
活动性质（Explain the nature of the event）：___
职责描述（Describe the duties）：___（1–2 行 + "See details in attached documents." 之类的指向附件）

  → I-129 Page 2, Part 2 Item 1（Classification Symbol，写 `O-1A` / `O-1B`，带横杠）

  → I-129 Page 28, O 附表 Section 1 Item 3（勾 a. O-1A 或 b. O-1B，只能勾一个）、Item 4 活动性质、Item 5 职责

  → I-907 Page 2, Part 2 Item 2（Classification or Eligibility Requested，写 `O-1A` / `O-1B`）

  注意：O 附表 Item 6 只对 O-2 和 P 类支持人员，**O-1 留空**。

## 【受益人是否持有担保方股权】：是 / 否

  → I-129 Page 28, O 附表 Section 1 Item 7.a

  → 勾 Yes 的话，Page 29 Item 7.b 要写说明（例："The beneficiary owns the petitioning company."）。受益人通过自己名下公司担保的案子就是这一种。

## 【咨询意见 / 工会信】

是否存在对应的工会 / peer group：是 / 否
咨询意见书（advisory opinion）是否随本次递交：是 / 否 - 已附申请副本 / N/A
若另寄：收件机构名称 / 地址 / 寄出日期 / 电话：___

  → I-129 Page 29, O 附表 Section 1 Item 8（是否存在工会）

  → I-129 Page 29, O 附表 Section 1 Item 9（咨询意见是否随交，三个选项：Yes / No - copy of request attached / N/A）

  → I-129 Page 29, O 附表 Item 10（O-1A 的 peer group）、Item 11（O-1B 影视的工会）、Item 12（O-1B 影视的管理方组织）—— 只有另寄了副本才需要填这几组

  注意：Item 8 勾 No 的话，**必须**去 Part 9 续页写说明，标注「Page 29 / Part 8」，不能只勾框。

## 【Part 4 案件历史（逐题确认，不要默认全 No）】

每人是否持有有效护照：是 / 否
是否与本申请同时递交其他 petition：是 / 否（几份）
是否同时申请补发 I-94：是 / 否
是否同时为家属递交申请：是 / 否
受益人是否在遣返程序中：是 / 否
是否曾为本案任何受益人递交过移民申请（immigrant petition）：是 / 否
过去 7 年内是否曾获批本类别：是 / 否
过去 7 年内是否曾被拒本类别：是 / 否
是否曾为本受益人递交过非移民 petition：是 / 否
（娱乐团体）是否有成员入团不满一年：是 / 否
受益人是否曾是 J-1 / J-2：是 / 否；若是，填维持该身份的起止日期

  → I-129 Page 4, Part 4 Item 2 至 Item 11b

  凡是答 Yes 的，按题干指示去 Part 9 续页写说明。

## 【O-1A 专属：受控技术声明】

是否需要美国商务部 / 国务院出口许可才能向受益人开放相关技术：否 / 是

  → I-129 Page 6, Part 6 Item 1（不需要许可）**或** Item 2（需要许可并承诺在取得许可前不开放）

  **只有 O-1A 要填这一栏，O-1B 整栏留空** —— 表格 Part 6 的题头自己写明了适用范围。两题不能都勾。

## 【费用】

I-129 申请费：___
Asylum Program Fee：___
I-907 加急费：___

  → 三张 G-1650 各自的 Bank Account Information → Authorized Payment Amount（纯数字，如 `530`，表格自己会印 `.00`）

  **金额务必上 G-1055 官网核当期数字，不要套用旧案例。** 详见第四节。

---

# 四、费用与三张 G-1650

O-1 加急递交是**三笔独立付款，所以三张 G-1650，绝不能合成一张** —— USCIS 明确要求加急费与其他费用分开缴。

| # | 用途 | 常规雇主 | 小雇主（≤25 人） | 非营利 |
|---|---|---|---|---|
| 1 | I-129 O 类申请费（纸质） | $1,055 | $530 | $530 |
| 2 | Asylum Program Fee | $600 | $300 | $0 |
| 3 | I-907 加急费（O 类） | $2,965 | $2,965 | $2,965 |

（2026-08-20 核对于 G-1055 费用表 05/29/26 版。加急费不分雇主规模。）

三张每张都要填全：Applicant 姓名（受益人）、勾 Business Account、开户人 Shenqi Cai、Business Name、勾 Checking Account、Bank Name、Routing、Account、金额。**缺了银行栏 USCIS 扣不到款，整个案子退回。**

文件命名按金额：`g-1650-530.pdf` / `g-1650-300.pdf` / `g-1650-2965.pdf`，一眼能看出金额对不对。

递交前对账：I-129 Page 6 Part 5 Item 14（人数）↔ Item 15（≤25 人？）↔ 第 1、2 张 G-1650 的金额，三者必须一致。

---

# 五、签字页与寄送

- **所有签名框和签名日期一律留空**，等真人手签或电子签。
- 需要**担保方本人**签的页：I-129 Page 7 Part 7、I-129 Page 30 O 附表 Section 2、I-907 Part 3；有 G-28 版另加 G-28 Page 3 Part 4。抽成一个 PDF 发出去签。
- 签字状态写进文件名（`i-129 waiting signature.pdf` / `i-907 signed.pdf`）。**填好 ≠ 能寄**，签名没回来就不是可寄状态。
- 签名教程见 `0 Sample （O1）` → `5. Signature Guidance and Page`。
- **寄件地址每次上 <https://www.uscis.gov/i-129-addresses> 查**：看**担保方主要办公所在州**，而且「与 I-907 同封」和「不同封」是两张不同的表、box 号不同、州的划分也略有差别。

  加州 + 同封加急（2026-08-20 查）：
  USPS：`USCIS, Attn: Premium I-129 O, P.O. Box 660090, Dallas, TX 75265-0090`
  FedEx / UPS / DHL：`USCIS, Attn: Premium I-129 O (Box 660090), 2501 S. State Highway 121 Business, Suite 400, Lewisville, TX 75067-8003`

---

# 六、填表后自查

- [ ] 表格是刚从官网下的，Edition Date 对着官网页面核过了
- [ ] 四张表的 Edition Date 都和本文档记的一致；**不一致的话已经提示过办案人，没有硬填**
- [ ] COS / CP 按指令勾对了（Page 2 Part 2 Item 4：CP = a.，COS = b.）
- [ ] Page 3 Part 4 Item 1 三格：a. 勾了 Consulate、b. 填了指令给的领馆城市、c. 填了 China
- [ ] Page 3 Part 3 Item 6 的「当前非移民身份 / 身份到期日」是从 I-94 抄的；案卷没有 I-94 的话，已从官网取了一份并存进本案文件夹
- [ ] Page 5 Item 11 的雇佣起止日期取自 offer，且起始日在未来
- [ ] Part 1 Item 1 和 Item 2 只填了一个
- [ ] Part 5 Item 15 按真实人数勾（不默认「是」），且与两张 G-1650 金额一致
- [ ] 加急费按当期 G-1055 核过
- [ ] O-1A 填了 Page 6 Part 6（两题只勾一个）；O-1B 整栏留空
- [ ] O 附表 Item 3 类别只勾了一个
- [ ] O 附表 Item 8 勾 No 的话，Part 9 里写了说明
- [ ] 有 G-28：Part 2 Item 1b 执照号 `348794` 填了；I-907 Part 1 Item 8 勾的是 b.
- [ ] 无 G-28：I-907 Part 1 Item 8 勾的是 a.，律师区块整块留空
- [ ] 律所电话是 `4155479999`
- [ ] 电话全是纯数字，州名全是两位代码
- [ ] Apt/Ste/Flr 勾选用了带空格的取值
- [ ] 续页上重复的姓名字段填了（G-28 Page 4、I-907 Page 7）
- [ ] 所有签名和签名日期留空
- [ ] **每一页都渲染成图片用眼睛回读过** —— 脚本报成功只证明值写进去了，不证明写对了。性别没勾、签发/到期日填反、文字溢出框，只有看图才发现

---

# 七、材料清单核对（从 0. Intake / 0. Shared Folder 提取后打勾）

- [ ] 受益人护照扫描件（信息页 + 最近赴美签证页）
- [ ] I-94 记录（cbp.gov/i94 下载）
- [ ] 当前身份证明（I-20 / EAD / 前一份 I-797 批准通知）
- [ ] 担保方营业登记 / 公司注册文件、FEIN 证明
- [ ] 担保方财务材料（税前 / 税后年收入、员工人数佐证）
- [ ] 雇佣合同 / offer letter
- [ ] 行程表 itinerary
- [ ] 咨询意见书 / 工会信（advisory opinion）
- [ ] 受益人个人简历
- [ ] 授权签字人身份与头衔证明
- [ ] 跟进表登记信息（订单总价、成交 / 收款日期、备注）
