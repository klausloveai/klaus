# EB1A 表格材料信息模板（I-140 杰出人才）

本模板用于每个 EB1A 案件，覆盖 **I-140 + G-28（有代理时）+ I-907（加急时）+ G-1145 + G-1650（每笔费用一张）**。

Fixed = 律所固定信息，每案通用，不用重新收集。

Flexible = 客户信息，每案不同；每条后面标明具体填在哪份表格的第几页、第几 Part、第几 Item，方便直接照抄，不用重新去翻表格结构。

## 本文档存放在哪 / 填好的表放在哪

**每次填表都从 `0.testing` → `Test EB1A` → `2. Form` 取本文档** —— 那一份是所有更正落地的地方，读它才能让上周修的东西真正用到这个案子上。

**填好的表格放到指令里指定的那个客户 Drive 文件夹**，不要放回测试文件夹。指令没说放哪就问。

客户信息填在**副本**上（可以复制一份到输出文件夹，命名 `EB1A 填表指令 — 客户名`），**不要写进 `Test EB1A` 里这一份** —— 它是后面每一次填表都要读的源，被某个客户的数据污染以后，下一个案子就会带着别人的信息起手。

## 三条律所统一规则（每个 I-140 都适用，不逐案判断）

### 规则一：Part 4 Processing Information 一律 CP，Guangzhou，China

I-140 **Page 2, Part 4**：

- 勾 **1.a.**「Alien will apply for a visa abroad at a U.S. Embassy or U.S. Consulate at:」
- **1.b. City or Town** 填 `Guangzhou`
- **1.c. Country** 填 `China`
- **2.a.**（境内转换 / adjustment of status）**不勾**

即使受益人现在就在美国境内（比如持 F-1），也按 CP 走 —— 两个框互斥，律所统一填 CP。只有蔡律明确另行指示才改，改了要在交付说明里写清楚。

**联动**：CP 案的随行家属在 **Part 7** 里，「applying for adjustment of status」= **No**，「applying for a visa abroad」= **Yes**。两个都勾 Yes 是自相矛盾，也和同一份表的 Part 4 打架。

### 规则二：Page 2 的「Information About His or Her Last Arrival in the United States」只在人在境内时才填

表格自己写着：「If the person for whom you are filing is in the United States, provide the following information.」

| | 10. 最后入境日期 | 11.a. I-94 号码 | 11.b. 允许停留到期日 | 11.c. I-94 上的身份 |
|---|---|---|---|---|
| 人在美国境内 | 照 I-94 填 | 照 I-94 填 | 照 I-94 填 | 照 I-94 填 |
| 人不在美国境内 | 空 | 填 `Not in U.S.` | 空 | 空 |

**12–15 题（护照号、旅行证件号、签发国、护照有效期）不属于这一块，两种情况都要照护照填。**

**必须写成 `Not in U.S.`（正好 11 个字符）。** 11.a 是分格框（comb field），`MaxLen = 11`，写 `Not in the U.S.`（14 个字符）会被静默截断成 `Not in the`，脚本只在输出里提一行、很容易漏掉。已经渲染验证过：11 格里显示 `N o t   i n   U . S .`，读起来是完整的。要换措辞先数字符数。

人在境外时，这一块唯一要填的就是 11.a；整块留空（连 11.a 也空着）不算填完。

### 规则三：Page 3, Part 4 的三块分工（出生国地址英文 / 中文姓名 / 国外地址中文）

| 印的题号 | 填什么 |
|---|---|
| 2.b | 申请人出生国的国名（英文），如 `China` |
| 3.a – 3.f | 申请人在出生国的地址，英文 / 拼音（3.a 街道、3.b Apt、3.c 城市、3.d 省、3.e 邮编、3.f 国家） |
| 4.a – 4.c | 申请人的中文姓名（4.a 姓、4.b 名、4.c 中间名） |
| 5.a – 5.g | 申请人的国外地址中文版（5.b 街道、5.c Apt、5.d 城市、5.e 省、5.f 邮编、5.g 国家；5.a 是 In Care Of） |

即：同一个国外地址填两遍 —— **3.a–3.f 是英文版，5.a–5.g 是中文版**；中间夹的 4.a–4.c 是中文姓名。表格自己的题干说 4.a–5.g 是「母语文字姓名和地址」，中国申请人就是中文。

两个注意：

- **2.b 印的题干是「现居国 / 来美前最后长期居住国」。** 出生国和现居国一致（绝大多数中国申请人）时按出生国填没问题；**两者不一致时（比如出生中国、现居加拿大）按题干填现居国，并跟蔡律确认**，不要机械套本规则。
- **3.d/3.e 和 5.e/5.f 的字段名是对调的**（印的 Province 对应名字里带 Postal 的那个，反之亦然），按印在纸上的题号定位，不要照字段名填。

## 填表原则

1. **表格一律从官网现下载，不参考任何旧案子、旧模板、旧样本的 PDF。** 旧文件的版次可能已过期（字段名会变），存久的副本 AcroForm 可能已损坏，而且会把旧的律所信息一起带进来。
2. **值只来自本文档第三节；位置只来自当期官网表格自己印的题号和说明。** 遇到本文档没写到的题，看表格自己的题干和 Instructions，不要去翻别的案子怎么填的。
3. 下载后先核 **Edition Date**：对着该表格自己的 USCIS 页面核，不是看 PDF 页脚的 Expires 日期。G-28 页脚写着 2021 年过期，但官网仍列 09/17/18 版为当前版。
   **如果核出来的版次和本文档下面记的不一样，先停下来提示办案人，不要直接接着填。** 换版意味着字段名和题号位置都可能动过，本文档标的 Page / Part / Item 会失效。
4. 勾选框的取值不能猜，也不能只看字段名 —— 要对着页面上印的选项位置（rect）确认。
5. **I-140 的字段名和印在纸上的题号系统性错位**（有的差 2、有的差 1、Province 和 Postal Code 整体对调、Page 6-8 的 Part 前缀比印的 Part 号小 1）。照本文档标的题号找位置，字段名交给技能里的 `references/i-140.md`。

## 移民局固定表格链接

I-140：<https://www.uscis.gov/sites/default/files/document/forms/i-140.pdf>

G-28：<https://www.uscis.gov/sites/default/files/document/forms/g-28.pdf>

I-907：<https://www.uscis.gov/sites/default/files/document/forms/i-907.pdf>

G-1650：<https://www.uscis.gov/sites/default/files/document/forms/g-1650.pdf>

G-1145：<https://www.uscis.gov/sites/default/files/document/forms/g-1145.pdf>

（表格版本，2026-08-20 核：I-140 edition **06/07/24**，G-28 **09/17/18**，I-907 **04/01/24**，G-1650 **06/03/25**，G-1145 **09/26/14**。）

费用表：<https://www.uscis.gov/sites/default/files/document/forms/g-1055.pdf>（I-140 那一行 + 下一页的 Additional Fees，加急看 I-907 那一行）

寄件地址：<https://www.uscis.gov/i-140-addresses>

---

# 一、填表前必须先确认（本案参数）

**下面这些由指令给出或向办案人确认，定完再动表格。** 定错了整套要重填。

指令里应当带到的三样：**有没有 G-28**、**要不要加急（I-907）**、**受益人将在美国哪个州工作**（决定寄哪个 lockbox）。缺哪样就问，不要推。

## 1. 有 G-28 还是无 G-28

| | 有 G-28（律所代理） | 无 G-28（客户自己递） |
|---|---|---|
| G-28 | 要做，Part 3 Item 5 勾 Petitioner | 不做 |
| I-140 Page 1 律师区块 | 勾「G-28 is attached」+ 执照号 `348794` + 律师 USCIS 账号 `063938833828` | 整块留空 |
| I-140 邮寄地址（Part 1 Item 3、Part 3 Item 2） | 律所地址（通知走律所） | 客户自己的美国地址 |
| I-907 Page 1 填谁 | 律师姓名 + 律所地址 | 客户本人姓名 + 地址 |
| I-907 Page 2, Part 1 Item 8 | 勾 b. for the petitioner | 勾 a. I am the petitioner |
| I-907 Page 3, Part 3 联系方式 | 律所电话 / 传真 / 邮箱 | 客户自己的电话 / 邮箱 |
| G-1145 | 律所邮箱 `cassie@lingtulaw.com` + 律所电话 | 先问要不要做、用谁的邮箱和电话 |
| G-1650 扣款账户 | 律所 ACH 账户，整块填全 | **只填金额那一个数字**（715 / 300 / 2965），姓名、账户类型、银行名、Routing、Account 和签字都留给客户自己填 |
| 补件 / 批准通知寄到 | 律所地址 | 客户地址（要提前跟客户讲清楚，通知不经过律所） |

判断依据是本案有没有签好的 G-28，不是上一个案子怎么做的。

## 2. 要不要加急（I-907）

加急适用于 E11 类别，费用 **$2,965**。加急意味着：多一份 I-907、多一张 G-1650、**而且寄件地址不一样**。

- 加急费必须和其他费用**分开支付**，所以单独一张 G-1650。
- I-907 规定不能由主表的受益人或共同申请人递交。EB1A 自我申请里客户本人就是 petitioner，所以合规 —— 但交付说明里写一句，免得别人看着像填错了。
- **I-907 上所有「公司」相关的题一律留空**：Page 1 Part 1 Item 4（Company or Organization Name）、Page 2 Part 2 **Item 6（Name of Point of Contact for the Company or Organization，含 Position Title）**、Item 7（公司 EIN）。EB1A 自我申请没有公司，就没有公司联系人 —— 把客户自己的名字填进 Item 6 等于凭空声明了一个公司关系。

## 3. 谁是 Petitioner

EB1A 基本都是**本人自我申请**：I-140 **Page 3, Part 5 Item 1.b 勾 `Self`**。这一个勾决定后面一整片怎么填：

- **Part 1**（谁在递这份申请）填客户本人姓名和地址，Item 2 公司名留空、Item 4 EIN 留空
- **Part 5 Item 2–8**（业务类型、成立日期、员工数、收入、NAICS、劳工证）是公司专用；Item 2 填 `N.A.`，其余留空
- **Part 5 Item 11、12**（Occupation、Annual Income）要填 —— 那是「如果是个人递交」的那一块
- **Part 6**（拟任职位）描述客户来美后的工作；CP 案往往还没定，9.a 写 `To be determined`，并在 Part 11 说明。**Part 6 整块留空会招 RFE。**
- **Page 1 Item 5**（是否非营利）= No；**Item 6**（美国全职等效员工是否 ≤25 人）= Yes

雇主担保的 EB1A（Part 5 Item 1.a `Employer`）少见；如果真是那种，Asylum Program Fee 的金额会变，见第四节。

## 4. 受益人将在美国哪个州工作

**I-140 的寄件 lockbox 按「受益人将在哪个州工作」分，不是按申请人地址、也不是按律所地址。** 这跟 I-129 的习惯相反。CP 案还没定工作地的，**问蔡律按哪个地址寄**，不要拿客户家庭住址推。

---

# 二、Fixed 律所固定信息（每案通用）

律师姓名：Shenqi Cai（Family Name: Cai / Given Name: Shenqi）

律所名称：Law Office of Shenqi Cai APC

律所地址：13191 Crossroads Parkway N, Ste 295, City of Industry, CA 91746, USA

律所电话（Daytime / Mobile 统一用此号，纯数字，不要括号和横杠）：4155479999

律所邮箱：cassie@lingtulaw.com

律所传真：6262402046

执业执照号 / 发照机构：348794 / the State Bar of California

律师 USCIS Online Account Number：063938833828

G-1650 ACH 扣款账户：Business Account / Checking / Bank of America / Routing 121000358 / Account 325210063004（开户人 Shenqi Cai，Business Name 填 Law Office of Shenqi Cai APC）

这些信息填在（仅「有 G-28」时填律师那几处）：

  → I-140 Page 1 律师区块（勾 G-28 附件框、执照号、律师 USCIS 账号）

  → I-140 Page 1 Part 1 Item 3 + Page 2 Part 3 Item 2（有 G-28 时邮寄地址用律所地址；In Care Of 写 `Law Office of Shenqi Cai APC`）

  → G-28 Page 1, Part 1（律师姓名 2a/2b、地址 Item 3、电话 Item 4、Item 6/7 见下方注意、传真 Item 7）

  → G-28 Page 1, Part 2（勾「我是有资格的律师」、执照号 1b、发照机构 1a、勾「不受任何限制执业的命令约束」、律所名 1d）

  → G-28 Page 3, Part 4 Item 1a（原件通知寄律所地址）

  → I-907 Page 1 律师区块 + Part 1 Item 3/Item 5；I-907 Page 3, Part 3 Item 3/4/5/6

  → G-1650 Bank Account Holder / Bank Account Information（勾 Business、开户人 Shenqi Cai、Business Name 律所名、勾 Checking、Bank Name / Routing / Account）

  → G-1145 Email + Mobile Phone（有 G-28 时用律所邮箱和电话）

  → I-140 Page 7（印的 Part 10，Preparer）：**填之前先问蔡律**

注意（都是核实过的、只看字段名会填错的地方）：

- **执照号是 `348794`。** 很容易手滑写成 `348749`（数字调序），每次都要逐位核。
- **G-28 Page 1 的 "Line6_EMail" 和 "Line7_MobileTelephoneNumber" 内部命名和视觉位置是反的** —— 电话填进名字叫 EMail 的框，邮箱填进名字叫 MobileTelephoneNumber 的框。
- **I-907 Page 3 的传真框是 `P3_Line5_MobileTelePhoneNumber` 的 `[1]`**。
- **G-1650 的 "CB_CreditCardType" 是 Checking / Savings 那一对**，不是信用卡类型；左边那个（`/V`）是 Checking。
- 所有 Apt / Ste / Flr 勾选框取值**自带前后空格**：`"/ APT "`、`"/ STE "`、`"/ FLR "`。
- **I-140 每个地址块里 Province 和 Postal Code 的字段名是对调的**（印的 3.g Province 对应字段 `Line6h_Province`）。
- 所有 Yes/No 都是**两个独立勾选框**，不是一组单选；只勾你要的那一个。

---

# 三、Flexible 客户信息（逐项标明填在哪）

EB1A 自我申请里，**申请人（Petitioner）和受益人（Beneficiary）是同一个人**，所以下面同一条信息经常要在同一份表里填两遍（Part 1 和 Part 3）。**别以为重复就是抄错了。**

本节的问法对齐律所自己的 `个人信息 / Personal Information_EB1A.docx`，直接照那张表抄。

## 【客户姓名】

姓（Family Name）：＿＿＿
名（Given Name）：＿＿＿
中间名（如有）：＿＿＿

  → I-140 Page 1, Part 1 Item 1.a / 1.b / 1.c（谁在递这份申请）

  → I-140 Page 2, Part 3 Item 1.a / 1.b / 1.c（申请对象）

  → I-140 Page 6，印的 Part 8 Item 1.a / 1.b（签字人姓名）

  → I-140 Page 8，印的 Part 11 页头（姓名 + A-Number，**很容易漏**）

  → G-28 Page 2, Part 3 Item 5.a / 5.b；G-28 Page 4 再写一遍（`[1]`）

  → I-907 Page 2, Part 2 Item 4（petitioner）+ Item 5（beneficiary）+ Item 6（联系人）；Page 1 Part 1 Item 3（无 G-28 时）；Page 7 再写一遍

  → G-1650 每张的 Applicant/Petitioner Information

  → G-1145 LastName / FirstName

## 【中文姓名（母语文字）】

姓：＿＿＿　名：＿＿＿　中间名：＿＿＿

  → I-140 Page 3, Part 4 Item 4.a / 4.b / 4.c（见规则三；中国申请人填中文）

## 【出生日期 DOB (mm/dd/yyyy)】：＿＿＿

  → I-140 Page 2, Part 3 **印的 Item 3**

## 【出生地】

出生城市 / 城镇：＿＿＿（`个人信息` 里的「出生地（城市，省份）」拆开填）
出生省份：＿＿＿
出生国家：＿＿＿

  → I-140 Page 2, Part 3 印的 Item 4（城市）/ Item 5（省份）/ Item 6（国家）

## 【国籍 / Citizenship】：＿＿＿

  → I-140 Page 2, Part 3 印的 Item 7

## 【A-Number（如有，纯数字不含 "A-" 前缀）】：＿＿＿

  → I-140 Page 2, Part 3 印的 Item 8；Page 8 Part 11 页头；G-28 Page 2 Item 9

## 【美国 SSN（如有，9 位纯数字无横杠）】：＿＿＿

  → I-140 Page 1, Part 1 印的 Item 7；Page 2, Part 3 印的 Item 9

## 【USCIS Online Account Number（如有）】：＿＿＿

  → I-140 Page 1, Part 1 印的 Item 8

## 【客户是否在美国境内？】是 / 否

**这一格决定规则二怎么走。** 是 → 下面 I-94 四项全填；否 → 11.a 填 `Not in U.S.`，10 / 11.b / 11.c 留空。

在境内的话，以下四项**只能从 I-94 读**（不能拿 I-20 的 OPT 结束日期代替）：

最后入境日期（Admission Date, mm/dd/yyyy）：＿＿＿　→ I-140 Page 2 印的 Item 10

I-94 号码（11 位）：＿＿＿　→ I-140 Page 2 印的 Item 11.a

允许停留到期日（Admit Until Date）：＿＿＿　→ I-140 Page 2 印的 Item 11.b

I-94 上的身份 / Class of Admission（如 `F1`）：＿＿＿　→ I-140 Page 2 印的 Item 11.c

案卷里没有 I-94、或存的那份超过一年，要去 <https://i94.cbp.dhs.gov/search/recent-search> 重新拉一份存进案卷。**网站的 Terms of Service 弹窗要客户/办案人自己点同意**，不能由 AI 代点（那份条款本身禁止自动化访问）。拉取需要：姓、名、出生日期、护照号、护照签发国 —— 护照号要用**当时入境时用的那本**，不一定是现在这本。

## 【护照信息】（不论人在境内境外都要填）

护照号：＿＿＿　→ I-140 Page 2 印的 Item 12

旅行证件号（一般空）：＿＿＿　→ 印的 Item 13

签发国：＿＿＿　→ 印的 Item 14

护照有效期至（mm/dd/yyyy）：＿＿＿　→ 印的 Item 15

## 【美国邮寄地址】（无 G-28 时用客户自己的；有 G-28 时用律所地址）

街道 / Apt / 城市 / 州 / ZIP / 国家：＿＿＿

  → I-140 Page 1, Part 1 Item 3.a–3.i

  → I-140 Page 2, Part 3 Item 2.a–2.i（同一个地址，两处都填）

  → I-907 Page 1, Part 1 Item 5；I-907 Page 3 印的 Item 8（related case 里 petitioner 的地址）

  → G-28 Page 2, Part 3 Item 13（客户邮寄地址；客户在境外、没有美国地址时填哪个地址**先问蔡律**）

## 【出生国国名（英文）】：＿＿＿

  → I-140 Page 3, Part 4 Item 2.b（见规则三：一般填出生国；出生国与现居国不一致时按题干填现居国，并跟蔡律确认）

## 【境外地址（含邮编）】

**出生国地址 —— 英文 / 拼音版**：街道 ＿＿＿ Apt ＿＿＿ 城市 ＿＿＿ 省 ＿＿＿ 邮编 ＿＿＿ 国家 ＿＿＿

  → I-140 Page 3, Part 4 Item 3.a–3.f（见规则三）

**同一地址 —— 中文版**：＿＿＿

  → I-140 Page 3, Part 4 Item 5.a–5.g（见规则三）

**长地址填不进 5.b 的框**：框里填短的，完整地址写到 **Page 8 印的 Part 11**，并标明 Page / Part / Item。

## 【电话 / 邮箱】

美国电话（纯数字）：＿＿＿　中国电话：＿＿＿　邮箱：＿＿＿

  → I-140 Page 6，印的 Part 8 Item 3（Daytime）/ Item 4（Mobile）/ Item 5（Email）—— 这三格填**客户自己的**电话和邮箱

  → G-28 Page 2, Part 3 Item 9 / 10 / 11（客户自己的）

  → I-907 Page 3, Part 3 Item 3/4/5/6（有 G-28 时填律所的）

## 【职业与收入】

当前职业 Occupation：＿＿＿　→ I-140 Page 4, Part 5 印的 Item 11

年收入（美元，只写数字和逗号，不写 `$`）：＿＿＿　→ I-140 Page 4, Part 5 印的 Item 12

## 【拟任职位（Part 6）】

职位名称 Job Title：＿＿＿　→ I-140 Page 4, Part 6 Item 1

SOC Code（前 2 位 + 后 4 位分两格）：＿＿＿ - ＿＿＿　→ Item 2（按职位对应的 SOC 码填，设计类是 `27` + `1020`）

职位描述：统一写 `Please see attached letter of support.`　→ Item 3

是否全职 full-time：是 / 否　→ Item 4（否的话 Item 5 填每周小时数）

是否永久职位 permanent：是 / 否　→ Item 6

是否新设职位 new position：是 / 否　→ Item 7

工资（数字 + 单位写全词 `year`，不要只写 `p`）：＿＿＿ / ＿＿＿　→ Item 8

工作地点（与 Part 1 地址不同才填）：街道 / Apt / 城市 / 州 / ZIP　→ Item 9.a–9.e

**CP 案还没定美国工作的**：9.a 写 `To be determined`，并在 Part 11 里对 Page 4 / Part 6 / Item 1 和 9 作说明。

## 【随行家属（配偶 + 21 岁以下子女）】

每人：姓 / 名 / 中间名 / 出生日期 / 出生国家 / 与申请人关系

  → I-140 Page 4, Part 7：第一人 Item 1.a–4，第二人 Item 7.a–10

  → 第三至第六人在 Page 5（**那一页的字段编号和姓名编号不对应，要重新按 rect 核**）

每人两问，**CP 案统一**：

- 「Is he or she applying for adjustment of status?」→ **No**
- 「Is he or she applying for a visa abroad?」→ **Yes**

（两个都勾 Yes 是错的。）

## 【Part 4 案件历史（逐题确认，不要默认全 No）】

第 6.a 题　是否与本 I-140 同时递交其他申请？是 / 否　→ Page 3 印的 Item 6.a；是的话在 6.b 勾 I-485 / I-131 / I-765 / Other

第 7 题　申请人是否处于遣返程序中？是 / 否　→ 印的 Item 7

第 8 题　是否曾有人为申请人递交过移民签证申请？是 / 否　→ 印的 Item 8（**这题是真问题，要问客户，不能默认 No**）

第 9 题　是否因原劳工证已随另一份 I-140 递交而未附原件？→ EB1A 一律 No

第 10 题　是否请 USCIS 向 DOL 索取劳工证副本？→ EB1A 一律 No

答 Yes 的题要在 Page 8 印的 Part 11 里写案号、办理机构、决定日期和结果。

## 【Part 2 类别】

EB1A 固定勾 **Page 1, Part 2 Item 1.a「An alien of extraordinary ability」**。2.a（修改此前递交的申请）/ 2.b（Schedule A）一般留空。

---

# 四、费用与 G-1650（G-1055 版本 05/29/26，2026-08-20 核）

| # | 费用 | 金额 | G-1650 文件名 |
|---|---|---|---|
| 1 | I-140 纸质申请费 | $715 | `g-1650-715.pdf` |
| 2 | Asylum Program Fee（self-petitioner 档） | $300 | `g-1650-300.pdf` |
| 3 | I-907 加急费（EB-1 / E11）—— 只在加急时 | $2,965 | `g-1650-2965.pdf` |

- **$300 是「small employer 或 self-petitioner」档**，不是按员工数算出来的。如果本案是**雇主担保**的 EB1A，这笔变成 $600（≤25 人的雇主 $300，非营利 $0），而且要和 I-140 Page 1 Item 5 / 6 的答案对得上。
- **一笔费用一张 G-1650，不能合并**；加急费必须单独交。
- 金额每次都对着当期 G-1055 现核，不要信本文档这张表。
- 金额栏只写数字（`715`，不写 `$715.00`，表格自己印了 `.00`）。
- **谁付钱决定填多少**，按有没有 G-28 分：
  - **有 G-28（律所付）**：整张填全 —— 申请人姓名、勾 Business、开户人 Shenqi Cai、Business Name 律所名、勾 Checking、Bank of America / Routing / Account、金额。
  - **无 G-28（客户自付）**：**只填金额那一个数字**，其余（姓名、账户类型、银行名、Routing、Account、签字）留给客户自己填。客户的银行信息不该由我们代填，而且这张表是由开户人本人签的。
- **只填了金额的 G-1650 还不能寄** —— 交付时要跟客户讲清楚：银行块不补全，移民局扣不到款，整包退件。

---

# 五、签字页与寄送

## 签字

**所有签名栏和签名日期一律留空**，由本人手签或电子签。填完把要客户签的页单独抽出来成一份 PDF，命名成一眼能看出状态的样子，例如 `i-140-waiting signature.pdf` / `g-28-waiting signature.pdf`。

标准包里客户要签的是：I-140 印的 Part 8（Page 6）、I-907 Part 3、G-28 Part 4。签名页要靠表格自己印的「Signature of...」区块认，不要靠记住的页码 —— 换版会移位。

**填好但没签的包不能寄。** 交付说明里要明写「待签字」，不要让「填好了」被读成「可以寄了」。

签字页随包附一份签名教程给客户；签回来的扫描件放案卷的 `signed & scanned` 子文件夹。

## 寄送地址（2026-08-20 核，页面最后更新 04/08/2025）

**按「受益人将在美国哪个州工作」分，不是按申请人地址。**

| 组合 | 地址 |
|---|---|
| 只寄 I-140 | 西部/南部各州 → Dallas lockbox（Attn: I-140, P.O. Box 660128, Dallas TX 75266-0128）；东北/中西部各州（含 NJ / NY / IL）→ Chicago lockbox（Attn: I-140, P.O. Box 88774, Chicago IL 60680-1774） |
| I-140 + I-907 | CA / AZ / TX / WA 等 → Phoenix（Attn: Premium I-140, P.O. Box 21500, Phoenix AZ 85036-1500）；NJ / NY / IL / FL 等 → Elgin（Attn: Premium I-140, P.O. Box 4008, Carol Stream IL 60197-4008） |
| I-140 + I-485 | 任何州 → Dallas，Attn: NFB, P.O. Box 660867, Dallas TX 75266-0867 |
| I-140 + I-485 + I-907 | 也是 Phoenix / Elgin，但分州名单和上面那行不一样，要现查 |

快递（FedEx / UPS / DHL）用另一套街道地址，现查页面。**CP 案没定工作州的，问蔡律按哪个寄。**

---

# 六、填表后自查（每次都做，不能只看脚本没报错）

脚本跑通只证明值写进去了，不证明写对了。逐条核：

1. **Page 2 Part 4** 是不是 1.a + Guangzhou + China，2.a 没勾。
2. **Page 2 最后入境那一块**：人在境外的，11.a 是不是 `Not in U.S.`（渲染出来 11 格显示完整），10 / 11.b / 11.c 是不是空的；人在境内的，四项是不是都照 I-94 填了。
3. **12–15 题**是不是都照护照填了（两种情况都要填）。
4. **Page 3 Part 4**：2.b 国名、3.a–3.f 英文地址、4.a–4.c 中文姓名、5.a–5.g 中文地址，四块有没有各就各位（最常见的错是把中文地址填进 3.a–3.f）。
5. **Part 2** 是不是勾了 1.a extraordinary ability。
6. **Part 5 Item 1.b `Self`** 有没有勾；Item 11 / 12 有没有填。
7. **Part 6** 不是整块空的；工资单位写的是 `year` 不是 `p`。
8. **Part 7** 家属两问是不是 No（AOS）/ Yes（visa abroad），没有两个都勾。
9. **ZIP、护照号、I-94 号、出生日期**逐位对着原件核一遍 —— ZIP 和执照号的数字调序是最常犯的错。
10. **Page 8 Part 11 的页头**（姓名 + A-Number）有没有填；G-28 Page 4、I-907 Page 7 的姓名重复处有没有填。
11. **所有签名栏是空的**。
12. **G-1650 张数和金额**跟本案是否加急、谁付钱对得上；银行块该填的都填了。
13. **每一页都渲染出来用眼睛看过**（`uscis_forms.py render` + 逐页看图）。

---

# 七、材料清单核对（从 `0. Intake` / `0. Shared Folder` 提取后打勾）

- [ ] `个人信息 / Personal Information_EB1A.docx`（姓名、出生日期、出生地、职业、收入、中美地址、电话、邮箱、家属信息）
- [ ] 护照信息页扫描件（护照号、签发国、有效期）
- [ ] 最近赴美签证页（如有）
- [ ] I-94（**仅人在美国境内时必需**；超过一年要重新拉）
- [ ] I-20 / EAD / 其他身份文件（如有，用于交叉核对，不作为 I-94 的替代）
- [ ] 家属护照页 + 身份关系文件（结婚证、出生证明）
- [ ] 个人简历 CV（Part 6 职位、SOC code 参考）
- [ ] 美国工作意向 / offer（Part 6；没有就按 `To be determined` 处理并在 Part 11 说明）
- [ ] 签好的 G-28（如律所代理）
- [ ] 付款方式确认（律所 ACH 还是客户自付）
- [ ] 加急与否的指示
- [ ] 受益人将在哪个州工作（决定 lockbox）
