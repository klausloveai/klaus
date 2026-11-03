# NIW 表格材料信息模板（I-140 国家利益豁免）

本模板用于每个 NIW 案件，覆盖 **I-140 + ETA-9089（Appendix A / Appendix C / Final Determination）+ G-28（有代理时）+ I-907（加急时）+ G-1145（不加急时）+ G-1650（每笔费用一张）**。

Fixed = 律所固定信息，每案通用，不用重新收集。

Flexible = 客户信息，每案不同；每条后面标明具体填在哪份表格的第几页、第几 Part、第几 Item，方便直接照抄，不用重新去翻表格结构。

## 本文档存放在哪 / 填好的表放在哪

**每次填表都从 `0.testing` → `Test NIW` → `2. Form` 取本文档** —— 那一份是所有更正落地的地方，读它才能让上周修的东西真正用到这个案子上。

**填好的表格放到指令里指定的那个客户 Drive 文件夹**，不要放回测试文件夹。指令没说放哪就问。

客户信息填在**副本**上（可以复制一份到输出文件夹，命名 `NIW 填表指令 — 客户名`），**不要写进 `Test NIW` 里这一份** —— 它是后面每一次填表都要读的源，被某个客户的数据污染以后，下一个案子就会带着别人的信息起手。

## 三条 NIW 统一规则（每个 NIW 的 I-140 都适用）

### 规则一：Part 2 一律勾 1.h（NIW 那一栏），绝对不能勾 1.d

I-140 **Page 2, Part 2, Item 1.h**：「An alien applying for an NIW (who **IS** a member of the professions holding an advanced degree or an alien of exceptional ability)」。

**1.d 是坑。** 它的题干里同样写着「advanced degree / exceptional ability」，但后面跟着「who is **NOT** seeking a National Interest Waiver」。勾错了等于向移民局申请了另一个类别。

这一勾必须和 **I-907 Page 2, Part 2, Item 3** 写的 `EB-2 NIW` 对得上。

### 规则二：Part 4 Processing Information 一律 CP，Guangzhou，China

I-140 **Page 2, Part 4**：

- 勾 **1.a.**「Alien will apply for a visa abroad at a U.S. Embassy or U.S. Consulate at:」
- **1.b. City or Town** 填 `Guangzhou`
- **1.c. Country** 填 `China`
- **2.a.**（境内转换 / adjustment of status）**不勾**

即使受益人现在就在美国境内（比如持 H-1B），也按 CP 走。只有蔡律明确另行指示才改，改了要在交付说明里写清楚。

**三个框都要填。** 只勾 1.a、1.b / 1.c 空着（勾了领馆却没写是哪个领馆）已经在寄出去的表上出现过；整个 Item 1 全空也出现过。

**联动**：CP 案的随行家属在 **Part 7** 里，「applying for adjustment of status」= **No**，「applying for a visa abroad」= **Yes**。

### 规则三：Information About His or Her Last Arrival in the United States —— 照客户的 I-94 填，人不在境内就不填

Page 2 印的 10 到 11.c。表格自己写着：「If the person for whom you are filing is in the United States, provide the following information.」

| | 10. 最后入境日期 | 11.a. I-94 号码 | 11.b. 允许停留到期日 | 11.c. I-94 上的身份 |
|---|---|---|---|---|
| 人在美国境内 | 照 I-94 填 | 照 I-94 填 | 照 I-94 填 | 照 I-94 填 |
| 人不在美国境内 | 空 | 填 `Not in U.S.` | 空 | 空 |

三点由此而来：

- **F-1 / J-1 的 11.b 是 `D/S`。** duration-of-status 入境的 I-94 上印的本来就是 D/S，律所 NIW Checklist 第 6 条也写死了（「Page 2, Part 3, Q11b: If F1 or J1 status, write "D/S" instead of specific date」）。拿 I-20 的项目结束日或 OPT 结束日代替，是和记录打架。
- **11.a 那个值是 `Not in U.S.`，正好 11 个字符。** 11.a 是分格框（comb field），`MaxLen = 11`，在当期空表上核过。`not in the U.S.` 是 15 个字符：脚本只提示一行，值存进去了，但打印出来是 `n o t  i n  t h e`，后面的 `U.S.` 没了 —— 两种写法都渲染验证过。11 格是硬上限，要换措辞先数字符数。
- **12–15 题（护照号、旅行证件号、签发国、护照有效期）不属于这一块**，两种情况都要照护照填。Item 12 护照号是最容易漏的一格。

**人住在境外、以前来过一次但签证早过期的，属于「人不在境内」**：11.a 填 `Not in U.S.`，其余留空。拿一份已经过期的旧入境记录填满整块，已经在寄出去的表上出现过，那是错的。

## 关于地址：问的是申请人地址，就填申请人的地址

不是什么特别规则，但值得说一句，因为做 EB1A 容易养成另一种习惯：I-140 Part 1 Item 3、Part 3 Item 2，G-28 Item 13，I-907 印的 Item 8，题干问的都是**申请人自己的地址**，所以填申请人的地址。有没有律所代理，不改变这些题在问什么。

## 关于 Page 3, Part 4 的三块分工（出生国地址英文 / 中文姓名 / 国外地址中文）

| 印的题号 | 填什么 |
|---|---|
| 2.b | 申请人出生国的国名（英文），如 `China` |
| 3.a – 3.f | 申请人在出生国的地址，英文 / 拼音（3.a 街道、3.b Apt、3.c 城市、3.d 省、3.e 邮编、3.f 国家） |
| 4.a – 4.c | 申请人的中文姓名（4.a 姓、4.b 名、4.c 中间名） |
| 5.a – 5.g | 申请人的国外地址中文版（5.b 街道、5.c Apt、5.d 城市、5.e 省、5.f 邮编、5.g 国家；5.a 是 In Care Of） |

即：同一个国外地址填两遍 —— **3.a–3.f 是英文版，5.a–5.g 是中文版**；中间夹的 4.a–4.c 是中文姓名。

**5.a–5.g 这个中文块最容易只写一半** —— 寄出去的表上有过只填了街道和邮编、城市 / 省 / 国家全空的。要么整块填全，要么整块不填并在 Part 11 说明。**2.b 也是常漏的一格。**

**3.d/3.e 和 5.e/5.f 的字段名是对调的**（印的 Province 对应名字里带 Postal 的那个），按印在纸上的题号定位，不要照字段名填。

## 填表原则

1. **表格一律从官网现下载，不参考任何旧案子、旧模板、旧样本的 PDF。** 这一条在 NIW 上不是空话：**ETA-9089 Appendix A 换版时有 75 个字段名变了**（旧版名字里多一个 `Enter`），而律所之前填过的 9089 都是旧版。
2. **值只来自本文档第三、四节；位置只来自当期官网表格自己印的题号和说明。**
3. 下载后先核版次。USCIS 的五份对着各自的 USCIS 页面核（不是看 PDF 页脚的 Expires 日期，G-28 页脚写着 2021 年过期，但官网仍列 09/17/18 版为当前版）。**DOL 那三份核不了** —— dol.gov 对本机的 HTML 页面一律 403，脚本只能核「URL 里的到期日」和「文件里印的到期日」是否一致，所以要**人工打开 <https://www.dol.gov/agencies/eta/foreign-labor/forms> 看一眼**，确认三个链接还是 `Expires02-28-29`。
   **如果核出来的版次和本文档下面记的不一样，先停下来提示办案人，不要直接接着填。**
4. 勾选框的取值不能猜，也不能只看字段名 —— 要对着页面上印的选项位置（rect）确认。
5. **I-140 的字段名和印在纸上的题号系统性错位**（有的差 2、有的差 1、Province 和 Postal Code 整体对调、Page 6-8 的 Part 前缀比印的 Part 号小 1）。照本文档标的题号找位置，字段名交给技能里的 `references/i-140.md`。
6. **姓名顺序是 Last, First。** 律所 Checklist 每一份表的第一条都写这句 —— 寄出去的 G-28 上出现过姓名填反、而同一包里的 I-140 却是对的。每份表都要核，不能只核一份。

## 官方表格链接

I-140：<https://www.uscis.gov/sites/default/files/document/forms/i-140.pdf>

G-28：<https://www.uscis.gov/sites/default/files/document/forms/g-28.pdf>

I-907：<https://www.uscis.gov/sites/default/files/document/forms/i-907.pdf>

G-1650：<https://www.uscis.gov/sites/default/files/document/forms/g-1650.pdf>

G-1145：<https://www.uscis.gov/sites/default/files/document/forms/g-1145.pdf>

ETA-9089 Appendix A：<https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/ETA-9089-AppendixA-Expires02-28-29.pdf>

ETA-9089 Appendix C：<https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/ETA-9089-AppendixC-Expires02-28-29.pdf>

ETA-9089 Final Determination：<https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/ETA-9089-Final-Determination-Expires02-28-29.pdf>

（表格版本，2026-08-24 核：I-140 edition **06/07/24**，G-28 **09/17/18**，I-907 **04/01/24**，G-1650 **06/03/25**，G-1145 **09/26/14**，ETA-9089 三份均 **Expires 02/28/2029**。）

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
| I-140 / G-28 / I-907 邮寄地址 | 申请人自己的地址 | 申请人自己的地址 |
| I-907 Page 1 填谁 | 律师姓名 + 律所地址 | 客户本人姓名 + 地址 |
| I-907 Page 2, Part 1 Item 8 | 勾 b. for the petitioner | 勾 a. I am the petitioner |
| I-907 Page 3, Part 3 联系方式 | 律所电话 / 传真 / 邮箱 | 客户自己的电话 / 邮箱 |
| **ETA-9089 Final Determination Section C** | 律师姓名 + 律所名 | **整个 Section C 留空** |
| **G-1650 付款方式** | 律所 ACH 账户，整块填全 | **整块留空** —— 只填申请人姓名和金额，账户由客户自己补 |
| 补件 / 批准通知寄到 | 客户地址（表上填的就是客户地址） | 客户地址 |

判断依据是本案有没有签好的 G-28，不是上一个案子怎么做的。

## 2. 要不要加急（I-907）—— 顺带决定要不要 G-1145

NIW（E21 NIW）的加急费是 **$2,965**，和 EB-1 同一档，费用表把它们写在同一行，**没有 NIW 折扣**。

**G-1145 是同一个开关的另一面。** 律所 Checklist 第 5 条的标题就是「Form G-1145 (**No** Premium Processing)」—— 加急案十五天就有结果，不另外做电子通知表。所以：

- **加急** → 做 I-907，**不做 G-1145**，三张 G-1650
- **不加急** → 做 G-1145（**放在整包的第一页**），不做 I-907，两张 G-1650

律所之前的 NIW 案子都加急了，所以没有一份填好的 G-1145 可以照着抄。

I-907 规定不能由主表的受益人或共同申请人递交。NIW 自我申请里客户本人就是 petitioner，所以合规 —— 但交付说明里写一句，免得别人看着像填错了。

**I-907 上所有「公司」相关的题一律留空**：Page 1 Part 1 Item 4（Company or Organization Name）、Page 2 Part 2 Item 6（Name of Point of Contact for the Company or Organization，含 Position Title）、Item 7（公司 EIN）。

## 3. 谁是 Petitioner

NIW 一律是**本人自我申请**：I-140 **Page 3, Part 5 Item 1.b 勾 `Self`**。这一个勾决定后面一整片怎么填：

- **Part 1**（谁在递这份申请）填客户本人姓名和地址，Item 2 公司名留空、Item 4 EIN 留空
- **Part 5 Item 2–8**（业务类型、成立日期、员工数、收入、NAICS、劳工证）是公司专用；Item 2 填 `N/A`，其余留空
- **Part 5 Item 11、12**（Occupation、Annual Income）要填
- **Part 6**（拟任职位）NIW 客户一般有真实的美国工作，整块正常填全，不像 EB1A 的 CP 案那样写 `To be determined`
- **Page 1 Item 5**（是否非营利）= No；**Item 6**（美国全职等效员工是否 ≤25 人）= Yes
- **ETA-9089 Final Determination Section D** 由客户本人签，Title 写 **`Self-Petitioner`**

## 4. 是不是二次申请（re-file）？

**要问。** 律所接过第一次被拒之后再递的 NIW。二次申请的话，**I-140 Page 3 印的 Item 8**（是否曾有人为申请人递交过移民签证申请）要答 **Yes**，并在 Page 8 印的 Part 11 里写上一次的收据号、受理中心、决定日期和结果。这一题很容易顺手答成 No，而且没有填好 Yes 的样本可以照抄。

## 5. 受益人将在美国哪个州工作

**I-140 的寄件 lockbox 按「受益人将在哪个州工作」分，不是按申请人地址、也不是按律所地址。** 还没定工作地的，**问蔡律按哪个地址寄**，不要拿客户家庭住址推。

---

# 二、Fixed 律所固定信息（每案通用）

**2026-08-24 与律所确认过。旧的 NIW 表上的律所信息和下面这张表不一致，以本表为准。**

律师姓名：Shenqi Cai（Family Name: Cai / Given Name: Shenqi）

律所名称：Law Office of Shenqi Cai APC

律所地址：13191 Crossroads Parkway N, Ste 295, City of Industry, CA 91746, USA

律所电话（Daytime / Mobile 统一用此号，纯数字，不要括号和横杠）：4155479999

律所邮箱：cassie@lingtulaw.com

律所传真：6262402046

执业执照号 / 发照机构：348794 / the State Bar of California

律师 USCIS Online Account Number：063938833828

G-1650 ACH 扣款账户：Business Account / Checking / Bank of America / Routing 121000358 / Account 325210063004（开户人 Shenqi Cai，Business Name 填 Law Office of Shenqi Cai APC）

**旧表上出现、但已经停用、绝对不能抄进新表的：** 律所旧名、旧的 San Marino 地址、电话 `8186658535` 和 `7147171893`、`@lashinelaw.com` 邮箱。要写进表里的值如果是从上一份表上抄来的、不是从这张表上取的，先停下来核一遍。

这些信息填在（仅「有 G-28」时填律师那几处）：

  → I-140 Page 1 律师区块（勾 G-28 附件框、执照号、律师 USCIS 账号）

  → G-28 Page 1, Part 1（律师姓名 2a/2b、地址 Item 3、电话 Item 4、Item 6/7 见下方注意、传真 Item 7）

  → G-28 Page 1, Part 2（勾「我是有资格的律师」、发照机构 1a、执照号 1b、勾「不受任何限制执业的命令约束」、律所名 1d）

  → G-28 Page 3, Part 4 Item 1a（原件通知寄律师办公地址）

  → I-907 Page 1 律师区块 + Part 1 Item 3 / Item 5；I-907 Page 3, Part 3 Item 3/4/5/6

  → **ETA-9089 Final Determination Page 2, Section C**（律师姓 1、名 2、律所名 4）

  → G-1650 Bank Account Holder / Bank Account Information（勾 Business、开户人 Shenqi Cai、Business Name 律所名、勾 Checking、Bank Name / Routing / Account）

  → G-1145 Email + Mobile Phone（有 G-28 时用律所邮箱和电话）

  → I-140 Page 7（印的 Part 10，Preparer）：**填之前先问蔡律**

注意（都是核实过的、只看字段名会填错的地方）：

- **执照号是 `348794`。** 很容易手滑写成 `348749`（数字调序），每次都要逐位核。
- **G-28 Page 1 的 `Line6_EMail` 和 `Line7_MobileTelephoneNumber` 内部命名和视觉位置是反的** —— 电话填进名字叫 EMail 的框，邮箱填进名字叫 MobileTelephoneNumber 的框。
- **I-907 Page 3 的传真框是 `P3_Line5_MobileTelePhoneNumber` 的 `[1]`**。
- **G-1650 的 `CB_CreditCardType` 是 Checking / Savings 那一对**，不是信用卡类型；左边那个（`/V`）是 Checking。
- 所有 Apt / Ste / Flr 勾选框取值**自带前后空格**：`"/ APT "`、`"/ STE "`、`"/ FLR "`。
- **I-140 每个地址块里 Province 和 Postal Code 的字段名是对调的**。
- 所有 Yes/No 都是**两个独立勾选框**，不是一组单选；只勾你要的那一个（寄出去的 I-140/I-907 上有两处 Yes 和 No 同时勾上）。

---

# 三、Flexible 客户信息（逐项标明填在哪）

NIW 自我申请里，**申请人（Petitioner）和受益人（Beneficiary）是同一个人**，所以下面同一条信息经常要在同一份表里填两遍。**别以为重复就是抄错了。**

本节的问法对齐律所自己的 `1. Personal Information.docx`，直接照那张表抄。

## 【客户姓名】

姓（Family Name）：＿＿＿
名（Given Name）：＿＿＿
中间名（如有）：＿＿＿

  → I-140 Page 1, Part 1 Item 1.a / 1.b / 1.c（谁在递这份申请）

  → I-140 Page 2, Part 3 Item 1.a / 1.b / 1.c（申请对象）

  → I-140 Page 6，印的 Part 8 Item 1.a / 1.b（签字人姓名）

  → I-140 Page 8，印的 Part 11 页头（姓名 + A-Number，**全套里最常漏的一处**）

  → G-28 Page 2, Part 3 印的 Item 6（姓 6.a / 名 6.b）；G-28 Page 4 再写一遍

  → I-907 Page 2, Part 2 Item 4（petitioner）+ Item 5（beneficiary）；Page 1 Part 1 Item 3（无 G-28 时）；Page 7 再写一遍

  → **ETA-9089 Appendix A Section A Item 1 / 2 / 3**

  → **ETA-9089 Final Determination Page 2, Section D Item 1 / 2 / 3**

  → G-1650 每张的 Applicant/Petitioner Information

  → G-1145 LastName / FirstName（不加急时才做）

## 【中文姓名（母语文字）】

姓：＿＿＿　名：＿＿＿　中间名：＿＿＿

  → I-140 Page 3, Part 4 Item 4.a / 4.b / 4.c

**这一格和下面的中文地址，`NIW个人信息表` 里没有对应的问题** —— 那张表只问了拼音姓名和拼音地址。所以每个案子这两项都会是空的，很容易顺手记成「客户没提供」然后把 Page 3 交出去。**中国籍申请人这一块不是选填**：题干写的是「If the person's native alphabet is other than Roman letters」，中文就是。

**先在案卷里现有的中文材料里找**，按这个顺序：

1. **软著**文件夹 —— 常常直接以著作权人的名字命名，里面的申请表 / 登记证书也有
2. **新闻**文件夹里的中文报道 —— 署名报道会写中文全名，而且是第三方公开来源
3. 签署过的**中文合同 / 谅解备忘录 / 采购订单** —— 法定代表人、授权代表那几栏
4. 国内发的**证书 / 奖状**
5. 护照扫描件上的中文姓名行（如果案卷里有）

**要两个互相独立的来源才动手写。** 一个文件夹名只是线索，不算来源；文件夹名 + 一篇署名报道够了；一份材料 + 自己猜不算。

**绝对不要拿拼音倒推汉字。** `Su` 可以是 苏 / 素 / 塑 / 速 / 粟；`Jingnansan Rd` 可以是 京南三路 也可以是 经南三路。同音字太多，猜错就是把错的法定姓名或错的地址写在联邦申请上。地址里一部分有据、一部分没据的，**有据的填上，没据的那格留空，并在交付说明里点名要确认哪个字** —— 留一个说明清楚的空格是诚实的，编一个不是。

**案卷里找不到就去问客户**，并且把这两项加进要客户补的材料清单，不要留空交出去。

## 【出生日期 DOB (mm/dd/yyyy)】：＿＿＿

  → I-140 Page 2, Part 3 **印的 Item 3**　→ ETA-9089 Appendix A Item 11

## 【出生地】

出生城市 / 城镇：＿＿＿（`1. Personal Information` 里的「出生地（城市，省份）」拆开填）
出生省份：＿＿＿
出生国家：＿＿＿

  → I-140 Page 2, Part 3 印的 Item 4（城市）/ Item 5（省份）/ Item 6（国家）

  → ETA-9089 Appendix A Item 14（出生国家）

## 【国籍 / Citizenship】：＿＿＿

  → I-140 Page 2, Part 3 印的 Item 7　→ ETA-9089 Appendix A Item 15

## 【A-Number（如有，纯数字不含 "A-" 前缀）】：＿＿＿

  → I-140 Page 2, Part 3 印的 Item 8；Page 8 Part 11 页头；G-28 Page 2 Item 9；ETA-9089 Appendix A Item 13

## 【美国 SSN（如有，9 位纯数字无横杠）】：＿＿＿

  → I-140 Page 1, Part 1 印的 Item 7；Page 2, Part 3 印的 Item 9

## 【USCIS Online Account Number（如有）】：＿＿＿

  → I-140 Page 1, Part 1 印的 Item 8；G-28 Page 2 Item 8

## 【客户是否在美国境内？】是 / 否

**这一格决定规则三怎么走。** 是 → 下面 I-94 四项按规则三填；否 → 11.a 填 `Not in U.S.`，10 / 11.b / 11.c 留空。

在境内的话，以下四项**只能从 I-94 读**（不能拿 I-20 的 OPT 结束日期代替）：

最后入境日期（Admission Date, mm/dd/yyyy）：＿＿＿　→ I-140 Page 2 印的 Item 10

I-94 号码（11 位）：＿＿＿　→ I-140 Page 2 印的 Item 11.a

允许停留到期日：＿＿＿　→ I-140 Page 2 印的 Item 11.b（**F-1 / J-1 写 `D/S`**）

I-94 上的身份 / Class of Admission（如 `H1B`、`F1`、`B2`）：＿＿＿　→ I-140 Page 2 印的 Item 11.c，**并且同一个值要填进 ETA-9089 Appendix A Item 12**

案卷里没有 I-94、或存的那份超过一年，要去 <https://i94.cbp.dhs.gov/search/recent-search> 重新拉一份存进案卷。**网站的 Terms of Service 弹窗要客户/办案人自己点同意**，不能由 AI 代点（那份条款本身禁止自动化访问）。拉取需要：姓、名、出生日期、护照号、护照签发国 —— 护照号要用**当时入境时用的那本**，不一定是现在这本。

## 【护照信息】（不论人在境内境外都要填）

护照号：＿＿＿　→ I-140 Page 2 印的 Item 12

旅行证件号（一般空）：＿＿＿　→ 印的 Item 13

签发国：＿＿＿　→ 印的 Item 14

护照有效期至（mm/dd/yyyy）：＿＿＿　→ 印的 Item 15

## 【美国邮寄地址】（申请人自己的地址）

街道 / Apt / 城市 / 州 / ZIP / 国家：＿＿＿

  → I-140 Page 1, Part 1 Item 3.a–3.i

  → I-140 Page 2, Part 3 Item 2.a–2.i（同一个地址，两处都填）

  → G-28 Page 2, Part 3 Item 13

  → I-907 Page 3 印的 Item 8（related case 里 petitioner 的地址）；无 G-28 时另填 I-907 Page 1 Part 1 Item 5

  → **ETA-9089 Appendix A Item 4–9**（Item 7 State 是**纯文本框不是下拉**，写 `CA` 不写 `California`）

## 【出生国国名（英文）】：＿＿＿

  → I-140 Page 3, Part 4 Item 2.b（**常漏的一格**）

## 【境外地址（含邮编）】

**出生国地址 —— 英文 / 拼音版**：街道 ＿＿＿ Apt ＿＿＿ 城市 ＿＿＿ 省 ＿＿＿ 邮编 ＿＿＿ 国家 ＿＿＿

  → I-140 Page 3, Part 4 Item 3.a–3.f（3.a 有 `MaxLen 34`，长街道会被静默截断）

**同一地址 —— 中文版**：＿＿＿

  → I-140 Page 3, Part 4 Item 5.a–5.g

**这一块要分两批填**：Apt/Ste/Flr 的勾、门牌号、邮编是 ASCII 和数字，走 `forms.py fill`；**汉字走 `cjk_stamp.py` 第二遍**，而且走了 stamp 的格子不能再让 fill 写一次，否则会在汉字上面盖一层 `?`。

**汉字是画在页面上的，不是表单值** —— Acrobat 里那一格看着是空的，`dump --filled-only` 也看不到它。**盖失败和忘了填长得一模一样，只有渲染出来看才能发现。** 来源见上面【中文姓名】那一节，同样不能拿拼音倒推。

**人住在境外的**，这个地址同时是 I-907 Page 2 Part 1 Item 7 的 physical address（Item 6 答 No），也是 ETA-9089 Appendix A Item 4 的 current address（那时用 Item 10 Province，不用 Item 7 State）。

**长地址填不进框**：框里填短的，完整地址写到 **I-140 Page 8 印的 Part 11**，并标明 Page / Part / Item。

## 【电话 / 邮箱】

美国电话（纯数字）：＿＿＿　中国电话：＿＿＿　邮箱：＿＿＿

  → I-140 Page 6，印的 Part 8 Item 3（Daytime）/ Item 4（Mobile）/ Item 5（Email）—— 这三格填**客户自己的**

  → G-28 Page 2, Part 3 印的 Item 10 / 11 / 12（客户自己的）

  → I-907 Page 3, Part 3 Item 3/4/5/6（有 G-28 时填律所的）

## 【职业与收入】

当前职业 Occupation：＿＿＿　→ I-140 Page 4, Part 5 印的 Item 11

年收入（美元，只写数字和逗号，不写 `$`）：＿＿＿　→ I-140 Page 4, Part 5 印的 Item 12

**这个年收入和下面 Part 6 Item 8 的工资要对得上**，对不上就说明有一处抄错了。寄出去的表上有过两处互相一致、但和 intake 表不一致的情况 —— 数字要从工资单据上取，不要从同一张表的另一格上抄。

## 【拟任职位（Part 6）】

职位名称 Job Title：＿＿＿　→ I-140 Page 4, Part 6 Item 1

SOC Code（前 2 位 + 后 4 位分两格）：＿＿＿ - ＿＿＿　→ Item 2（按职位对应的 SOC 码填）

职位描述：统一写 `Please see attached letter of support.`　→ Item 3

是否全职 full-time：是 / 否　→ Item 4（否的话 Item 5 填每周小时数）

是否永久职位 permanent：是 / 否　→ Item 6

是否新设职位 new position：是 / 否　→ Item 7

工资（数字 + 单位写全词 `year`）：＿＿＿ / ＿＿＿　→ Item 8

工作地点（与 Part 1 地址不同才填）：街道 / Apt / 城市 / 州 / ZIP　→ Item 9.a–9.e

**远程 / hybrid 的人，工作地点是他自己住的地方**，不是公司办公室所在城市 —— 这不是格式问题，**lockbox 就是按受益人工作的州分的**，写成公司城市会寄错地方。intake 表里「工作地址」一栏答成「hybrid，公司在某两个城市有办公室」的，那不是一个工作地点，要另外问。

**Item 1 的职位名和 Item 2 的 SOC 码，必须和 ETA-9089 Appendix A Section E 的 1g、以及 Final Determination 的 8/9/10 题一致** —— 它们装在同一个信封里。

## 【随行家属（配偶 + 21 岁以下子女）】

每人：姓 / 名 / 中间名 / 出生日期 / 出生国家 / 与申请人关系

  → I-140 Page 4, Part 7：第一人 Item 1.a–4，第二人 Item 7.a–10

  → 第三至第六人在 Page 5（**那一页的字段编号和姓名编号不对应，要重新按 rect 核**）

每人两问，**CP 案统一**：

- 「Is he or she applying for adjustment of status?」→ **No**
- 「Is he or she applying for a visa abroad?」→ **Yes**

**没有家属的，那几格要确认是干净的** —— 寄出去的表上有过：「第二人」栏里没有姓名，却留着一个孤零零的 No。

## 【Part 4 案件历史（逐题确认，不要默认全 No）】

第 6.a 题　是否与本 I-140 同时递交其他申请？是 / 否　→ Page 3 印的 Item 6.a；是的话在 6.b 勾 I-485 / I-131 / I-765 / Other

第 7 题　申请人是否处于遣返程序中？是 / 否　→ 印的 Item 7

第 8 题　是否曾有人为申请人递交过移民签证申请？是 / 否　→ 印的 Item 8（**二次申请必须答 Yes，见第一节第 4 条**）

第 9 题　是否因原劳工证已随另一份 I-140 递交而未附原件？→ NIW 一律 No

第 10 题　是否请 USCIS 向 DOL 索取劳工证副本？→ NIW 一律 No

**第 9、10 题答 No 是有原因的，不是默认值**：NIW 豁免的正是雇主 offer 和劳工证，所以根本没有一份被认证过的劳工证；包里那份 ETA-9089 是**未经认证**的。不要因为文件夹里躺着一份 9089 就答成 Yes。

答 Yes 的题要在 Page 8 印的 Part 11 里写案号、办理机构、决定日期和结果。

---

# 四、ETA-9089 三份（Appendix A / Appendix C / Final Determination）

这三份是**劳工部（DOL）**的表，不是移民局的。NIW 豁免的是雇主 offer 和劳工证，所以**没有 PERM 案号、没有认证**，这三份是**未经认证**地随 I-140 一起交给移民局。

**Final Determination 的第 1 页整页是 DOL 专用，全部留空** —— 案号、Case Status、雇主 FEIN、各种日期、OFLC 电子签名，一个都不填，也不要编。只填第 2 页。

## Appendix A —— Section A 联系信息（第 1 页 1–15 题）

姓 / 名 / 中间名、现住地址（Address 1 / Address 2 / City / State / Postal Code / Country / Province）、出生日期、**Class of Admission**、A-Number、出生国、国籍。

值全部来自第三节，不用重新收集。三点注意：

- **Item 12 Class of Admission 必须和 I-140 Page 2 Item 11.c 一模一样。**
- **Item 7 State 是纯文本框**，不是下拉，写两位州码。
- 人住境外的，Item 4 填境外地址，那时用 **Item 10 Province**、不用 Item 7 State。

## Appendix A —— Section B 学历（五个块，第 1–2 页）

每个块：学位等级勾选框 + 1a 其他学位说明 + 1b 专业 + 1c 学校 + 1d 学校所在国 + 1e 取得年月(mm/yyyy)。

**每个学位一个块，从最高往下填，每个块都对着它自己那张学位证。** `1. Personal Information.docx` 只问了最高学位，其余学位要从学位证和成绩单上读 —— 这正是下面几个块容易照抄上面那个块的原因。

寄出去的表上出现过的错法：本科块把硕士块的学校名和取得年月照抄了下来，只有国家改成了本科那个 —— 结果那一块描述的是一个不存在的学位。

用不到的块，**每一个文本格都填 `N/A`** —— 这是律所的习惯，好处是「故意留空」和「漏填」能分得开。

## Appendix A —— Section C 培训 / 证书（三个块，第 2–3 页），Section D 技能（两个块，第 3–4 页）

没有的填 `N/A`。Section C 第一个块的 1b 在第 3 页、1 和 1a 在第 2 页，跨页。

## Appendix A —— Section E 工作经历（第 4–5 页）

**Appendix A 上只有一份工作经历的位置**（1 公司名、1a/1b 地址、1c 城市、1d 邮编、1e 国家、1f 州/省、1g 职位、1h 起、1i 止、1j 是否在职、1k 每周小时数、1l 工作职责）。

**律所 intake 表收五份。第二份起全部写到 Appendix C。** 这是整套 9089 的结构关键。

工作经历（照 `1. Personal Information.docx` 的五个块抄）：

| # | 公司名称 | 公司地址 | 职位 | 起 (mm/yyyy) | 止 (mm/yyyy) | 每周小时 | 工作职责 |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

第 1 份 → Appendix A Section E；第 2 份起 → Appendix C。

## Appendix C —— 溢出页（一页两条，可以多做几张）

每条三格：Section and Item Number / Section Name or Category / Supplemental Information（1500 字符上限）。

**律所已经定型的写法**：

- Section and Item Number 写 **`E(b)`**、**`E(c)`**、**`E(d)`**…（接着 Appendix A 占掉的 `a` 往下排）
- Section Name or Category 写 `Foreign Worker Work Experience`
- Supplemental Information 里把 Appendix A 自己的题号原样重排一遍：

```
Work Experience 2
1. Employer Name: ...
1a. Address 1: ...      1b. Address 2: ...
1c. City or Town: ...   1d. Postal Code: ...
1e. Country: ...        1f. State, Territory, or Province: ...
1g. Job Title: ...
1h. Start Date: ...     1i. End Date: ...
1j. Present: No         1k. Hours Worked Per Week: 40
1l: Job Duties: ...
```

**1500 字符是硬上限，脚本不会拦你** —— 超了就静默溢出框外。宁可把 Job Duties 写短，也不要漏掉某一格。经历多的就多做几张 Appendix C，不要压缩。

其他 section 溢出（第六个学位、第四段培训）也用同样的 `Section(字母)` 写法。

## Final Determination 第 2 页 —— 三个声明块

| 块 | 谁 | 填什么 |
|---|---|---|
| **B. Foreign Worker Declaration** | 客户 | **签名和日期都留空，客户手签** |
| **C. Attorney or Agent Declaration** | 律师 | 姓 `Cai` / 名 `Shenqi` / 律所名 `Law Office of Shenqi Cai APC`；签名日期留空。**无 G-28 的案子整块留空** |
| **D. Employer Declaration** | 客户 | 客户姓 / 名 / 中间名首字母，**Title 写 `Self-Petitioner`**；签名日期留空 |

D 块印的抬头是「Employer Declaration」，NIW 里没有雇主指定代理人，所以由申请人自己以 `Self-Petitioner` 的身份站在那个位置上签。

**B 块的客户签名是必须抽出来给客户签的页**，律所 Checklist 点名：「ETA-9089 Final Determination - Compliant: Page 2 Client Signature: Clear, handwritten (not electronic), and dated.」

---

# 五、费用与 G-1650（G-1055 版本 05/29/26，2026-08-24 核）

| # | 费用 | 金额 | G-1650 文件名 |
|---|---|---|---|
| 1 | I-140 纸质申请费 | $715 | `g-1650-715.pdf` |
| 2 | Asylum Program Fee（self-petitioner 档） | $300 | `g-1650-300.pdf` |
| 3 | I-907 加急费（EB-2 / E21 NIW）—— 只在加急时 | $2,965 | `g-1650-2965.pdf` |

- **加急费和 EB-1 同一档，费用表把它们写在同一行，没有 NIW 折扣。**
- **律所 NIW Checklist 上写的 $2,805 已经过期**，那是上一版费率。Checklist 其他部分都好用，这一行不能用。每次对着当期 G-1055 现核。
- **$300 是「small employer 或 self-petitioner」档**，不是按员工数算出来的，而且要和 I-140 Page 1 Item 5 / 6 的答案对得上。
- **一笔费用一张 G-1650，不能合并**；加急费必须单独交。
- 金额栏只写数字（`715`，不写 `$715.00`，表格自己印了 `.00`）。
- **付款方式按有没有 G-28 分叉（2026-08-25 确认）**：
    - **有 G-28** → 律所付，ACH 块整块填全（勾 Business + Checking，开户人 Shenqi Cai，Business Name 律所名，Bank of America / Routing 121000358 / Account 325210063004）。
    - **无 G-28** → **付款方式整块留空**，只填申请人姓名和金额。账户类型、开户人姓名、Business Name、Checking/Savings、银行名、Routing、Account 全部空着，由客户按自己的账户填。律所不是本案的代理，账户不该出现在客户自己递的表上。
    - 无 G-28 的 G-1650 **是故意以未填完的状态交出去的**，这不是缺陷；但交付说明里必须写明，否则看着就像漏填。移民局扣不到款会整包退件，所以三张都要客户补完才能寄。
- 律所之前的 NIW 案子都是客户 Zelle 给律所、律所开支票，所以没有一张填好的 G-1650 可以照着抄。个案要改回支票的话，要确认并写进交付说明。
- **银行块空着的 G-1650 是不能寄的状态** —— 移民局扣不到款，整包退件。

---

# 六、签字页与寄送

## 签字

**所有签名栏和签名日期一律留空**，由本人手签。填完把要客户签的页单独抽出来成一份 PDF，命名成一眼能看出状态的样子，例如 `i-140-waiting signature.pdf`。

标准包里客户要签的：

- I-140 印的 Part 8（Page 6）
- G-28 Part 4（Page 3）
- **ETA-9089 Final Determination Page 2, Section B** —— 这一处最容易漏
- I-907 Part 3 —— **只在无 G-28 时**；有 G-28 时 requestor 是律师，客户不签

签名页要靠表格自己印的「Signature of...」区块认，不要靠记住的页码 —— 换版会移位。

**律所 Checklist 的签名标准：Clear, handwritten (not electronic), and dated.** 每一份表都写了这一句，电子签不接受。

**填好但没签的包不能寄。** 交付说明里要明写「待签字」，不要让「填好了」被读成「可以寄了」。

## 寄送地址（2026-08-24 核，页面最后更新 04/08/2025）

**按「受益人将在美国哪个州工作」分，不是按申请人地址。**

| 组合 | 地址 |
|---|---|
| 只寄 I-140 | 西部/南部各州 → Dallas lockbox（Attn: I-140, P.O. Box 660128, Dallas TX 75266-0128）；东北/中西部各州（含 NJ / NY / IL）→ Chicago lockbox（Attn: I-140, P.O. Box 88774, Chicago IL 60680-1774） |
| **I-140 + I-907**（NIW 常见） | CA / AZ / TX / WA 等 → Phoenix（Attn: Premium I-140, P.O. Box 21500, Phoenix AZ 85036-1500）；NJ / NY / IL / FL 等 → Elgin（Attn: Premium I-140, P.O. Box 4008, Carol Stream IL 60197-4008） |
| I-140 + I-485 | 任何州 → Dallas，Attn: NFB, P.O. Box 660867, Dallas TX 75266-0867 |
| I-140 + I-485 + I-907 | 也是 Phoenix / Elgin，但分州名单和上面那行不一样，要现查 |

快递（FedEx / UPS / DHL）用另一套街道地址，现查页面。**没定工作州的，问蔡律按哪个寄。**

---

# 七、填表后自查（每次都做，不能只看脚本没报错）

脚本跑通只证明值写进去了，不证明写对了。逐条核：

1. **Page 2 Part 2** 勾的是 **1.h**（不是 1.d），并且 I-907 Part 2 Item 3 写的是 `EB-2 NIW`。
2. **Page 2 Part 4** 是不是 1.a + `Guangzhou` + `China` 三格都填了，2.a 没勾。
3. **Page 2 最后入境那一块**：人在境内的四项是不是都照 I-94 填了（F-1 / J-1 的 11.b 是 `D/S`）；人在境外的 11.a 是不是 `Not in U.S.`（渲染出来 11 格显示完整）、10 / 11.b / 11.c 是不是空的。
4. **12–15 题**是不是都照护照填了（两种情况都要填，护照号最容易漏）。
5. **Page 3 Part 4**：2.b 国名、3.a–3.f 英文地址、4.a–4.c 中文姓名、5.a–5.g 中文地址，四块有没有各就各位。**4.a–4.c 和 5.a–5.g 必须真的显示出汉字** —— 空着是错的，显示 `?` 也是错的；`dump` 查不出来，只能靠渲染。另外看一眼别把中文地址填进了 3.a–3.f。
6. **Part 5 Item 1.b `Self`** 有没有勾；Item 11 / 12 有没有填；Item 2 是 `N/A`、3–8 空。
7. **Part 6** 不是整块空的；工资单位写的是 `year`；工作地点是受益人真正工作的地方。
8. **Part 7** 家属两问是不是 No（AOS）/ Yes（visa abroad）；没有家属的栏位是不是干净的。
9. **姓名顺序**每份表都是 Last / First，没有填反。
10. **ZIP、护照号、I-94 号、出生日期、执照号**逐位对着原件核一遍。
11. **Page 8 Part 11 的页头**（姓名 + A-Number）有没有填；G-28 Page 4、I-907 Page 7 的姓名重复处有没有填。
12. **ETA-9089**：Appendix A Item 12 和 I-140 Item 11.c 一致；职位名和 SOC 码在 I-140 Part 6、Appendix A 1g、Final Determination 8–10 三处一致；用不到的块填了 `N/A`；工作经历 2 起在 Appendix C 上、编号是 `E(b)` `E(c)`…；Final Determination 第 1 页整页空白；Section D 的 Title 是 `Self-Petitioner`。
13. **所有签名栏是空的。**
14. **G-1650 张数和金额**跟本案是否加急对得上。**有 G-28** 的：银行块该填的都填了；**无 G-28** 的：银行块是不是整块空的（只有姓名和金额），并且交付说明里写了要客户补。加急案**没有** G-1145；不加急案**有** G-1145 且排在整包第一页。
15. **每一页都渲染出来用眼睛看过**（`forms.py render` + 逐页看图）。

---

# 八、材料清单核对（从 `0. Intake` / `0. Shared Folder` 提取后打勾）

- [ ] `1. Personal Information.docx`（姓名、出生日期、出生地、最高学位与学校、职业、收入、中美地址、电话、邮箱、家属信息、**五段工作经历**）
- [ ] **中文姓名**（信息表不问，Page 3 Item 4.a–4.c 必需；先翻案卷里的中文材料，找不到就问客户）
- [ ] **国内地址的中文写法**（信息表只给拼音，Page 3 Item 5.a–5.g 必需；不能拿拼音倒推汉字）
- [ ] 护照信息页扫描件（护照号、签发国、有效期）
- [ ] 最近赴美签证页（如有）
- [ ] I-94（**仅人在美国境内时必需**；超过一年要重新拉）
- [ ] 现阶段在美合法身份证明（H-1B / F-1 / J-1 等）
- [ ] **各阶段学位证书和成绩单**（Appendix A Section B 每个学位一个块，intake 表只问了最高学位）
- [ ] 专业资格证书 / 培训证书（Appendix A Section C）
- [ ] 家属护照页 + 身份关系文件（结婚证、出生证明）
- [ ] 个人简历 CV（Part 6 职位、SOC code、工作经历交叉核对）
- [ ] SOC code 已确定
- [ ] 签好的 G-28（如律所代理）
- [ ] 加急与否的指示（决定 I-907 / G-1145 / G-1650 张数 / lockbox）
- [ ] 付款方式确认（有 G-28 → 律所 ACH 填全；无 G-28 → 付款方式留空，客户自己补）
- [ ] 受益人将在哪个州工作（决定 lockbox）
- [ ] **是否二次申请**（决定 Page 3 Item 8 答 Yes 还是 No）
