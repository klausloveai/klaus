# Intake Sheet Cell Map

## 填写总原则（2026-07-26 校准 — 覆盖以下所有字段）

**1. 照抄，不分析。** 这份 intake sheet 是**客户陈述的记录**，不是案件分析。除极少数明确允许的字段外，
一律**原封不动写客人填的内容**：不改写、不润色、不加"per client"、不加推荐动作、不加法律判断、
不加 ⚠️ 提示。判断性内容属于 Note / 案件报告，不属于 intake 字段。

**2. 黄色 = AI 抓取、待核实**（不再只表示"待补充"）。所有从材料抓取或客人自报的信息默认标黄；
CM/CA 在 welcome call 与客户确认后**去黄**；仍待定的**保持黄色**作为跟进提醒。

**3. 客人留空 ≠ 客人答"没有"。** 留空就留空（+黄），不要替客人写 `None` / `N/A - no passengers`。

**4. 不做法律定性、不做推断。** CVC code 一律不写（等警察报告，由律师加）；
不从间接线索推断事实（不用"身体甩向左"或照片猜撞击部位）——留空问客户。

**5. 证件优先于表格。** 客人可能填错自己的 DOB / 姓名 / 性别 —— 这些以**驾照为准**。

---

## Clients Index (col C = value column)

| 格 | 字段 | 规则 |
|---|---|---|
| C2 | DOL | MM/DD/YYYY（黄规则见 Step 3） |
| C3 | Time | **照抄客人填的**，不判断 AM/PM、不转 24h（客人填 `5:42` 就写 `5:42`） |
| C4 | Driver Name | **驾照为准** |
| C5 | DOB | **驾照为准**（客人常填错，以证件为准，不标黄） |
| C6 | Phone | **纯照抄**（客人填 `9493168463` 就写 `9493168463`，不加连字符） |
| C7 | Address | 见下方「地址格式」 |
| C8 | Email | 照抄 |
| C9 | Gender | **驾照为准** |
| C10 | Marital Status | **英文**：`Single` / `Married` / `Divorce` |
| C11 | Spouse Name | 客人不填 → `N/A` |
| C12 | Occupation | 极简：只填 Unsure → `Unsure`；Unsure+职位 → `[Job title], unsure loss of income` |
| C13 | SSN | **纯照抄**（不加连字符） |
| C14 | Medi-Cal | **`Pending` + 黄**（客人字段，表单更新前一律 Pending） |
| C15 | Medicare | **`Pending` + 黄**（同上） |
| C16 | Health Insurance | 有保险 → 直接写承保方，**无 "Yes – " 前缀**（e.g. `Kaiser Permanente (Southern California; MRN 32006874)`）；无保险 → `None` |
| C17 | Prior Accd & Injured | **详细记录客人填写的内容，不做任何判断**（不加 apportionment / 建议） |
| C18 | Ambulance | 客人否认 → `No`（不加解释） |
| C19 | Emergency | 客人否认 → `No` |
| C20 | Urgent Care | 客人否认 → `No`；我们安排的 → 诊所名 + 地址/时间 |
| C21 | Primary Doctor | 客人否认 → `No`；客人有自己的 PCP → PCP 姓名、地址、电话 |
| C22 | Injuries（**永远黄**） | **只记录客人填的伤 + 症状 + 疼痛等级**。不写事故力学（速度/气囊/撞击次数/力度/车身移动）、不写就诊情况（另有字段问）、不写既往伤分析 |

**地址格式（C7）** — 主存客人在 intake form 填的 **Current 地址**；其它材料上的地址简单标注来源：
```
5 Sage, Irvine, CA 92604(Current) 4327 Elmwood Ct, Riverside, CA 92506(Driver License)
```
客人填的地址残缺时（如 `5 sage irvine`），放进 Google Maps 补全成完整地址（含邮编）后再写入。

C45=Pass1 Injuries（**永远黄**）— 所有乘客伤情格同 C22 规则。

---

## Accident Information (col F = value column)

| 格 | 字段 | 规则 |
|---|---|---|
| F2 | Accident Location | **纯照抄客人填的原文，不加任何括号说明**（客人填 `不清楚` 就写 `不清楚`，不写 `不清楚 (unclear per client)`）；黄色高亮已表示"待核实" |
| F3 | Accd Diagram | **默认 `Pending`，不标黄**（跳过，不是客人字段） |
| F4 | Fact of Loss（**永远黄**） | **固定模板**，见下 |
| F5 | Point of Impact（**永远黄**） | **固定模板**，见下 |
| F6 | Vehicle Status | **完全照抄**客人所选，不改写（不加 but / per client）；没填 → 空 + 黄 |
| F7 | Vehicle Location | 照抄；表单无此栏或客人没填 → **空 + 黄** |
| F8 | Vehicle Owner | 可带**基于 facts 的简单标注**，不过度分析（e.g. `Yujing Zhou (client's mother)`） |
| F9 | Vehicle Mileage | **原封不动**（客人填 `150000` 就写 `150000`，不加 "Approx." / "miles"） |
| F10 | Weather | 翻译原文即可（`晴天` → `Clear`） |
| F11 | Purpose of Trip | **按客人原文，中文也照出**（`去上班`）；没填 → 空 |
| F12 | Child Seat | `Yes` / `No` |
| F13 | Airbag Deploy | `Yes` / `No` |
| F14 | Dashcam | `Yes` / `No` |
| F15 | Independent Witness | `Yes` / `No`，客人没填 → 空 |
| F16 | Passenger Info | 有乘客且填了姓名/电话 → **照抄**；没有乘客 → `No`；有乘客但没填信息 → `Yes` |
| F17 | Police Report | `Yes` / `No`，或空；可加**简单**判断 |
| F18 | Crash Date | **只填警察卡/报告上的**。客人答"没有警察报告" → `No` |
| F19–F22 | Crash Time / NCIC# / Officer ID / Report# | 无警察报告 → **留空，不标黄** |

> ⚠️ **F18–F22 只看警察卡或报告**，不用客人自报的日期时间 —— 两者可能不一致。

### F4 Fact of Loss — 两行格式（客人原文 + 模板）

**第一行照抄客人在表单「简述事发经过（What Happened?）」栏填的原文**（一字不改，中文照出，
作为 CM 打 welcome call 时的参考）；**第二行是待填模板**：

```
<客人自述原文，一字不改>
Client First Name was on [street name] and the other vehicle was on [street name]
when the other vehicle [what happened], colliding with Client First Name's vehicle.
```

Qianxu Jin 案示例：
```
她的，我正常行驶，她从plaza出来撞的我
Qianxu was on [street name] and the other vehicle was on [street name]
when the other vehicle [what happened], colliding with Qianxu's vehicle.
```

- 客人没填自述 → 第一行留空，只放模板
- 模板里**只预填客人名字**（我们一定知道）；其余 `[]` 保留、黄标，welcome call 逐项确认后去黄
- 对方司机姓名确认后可把 `the other vehicle` 替换成姓名
- **街名一律留空** —— accident location 只说明事故大概在哪，不代表客人当时走的是那条街
- 客人原文只作参考，**不据此推断街名、动作或撞击部位**；不引 CVC code，不写责任判断

### F5 Point of Impact — 固定模板
```
Client First Name's vehicle [point of impact], other vehicle [point of impact].
```
板件名词汇（CM 填空时统一用词）：`front bumper` / `front end` /
`driver's side front corner` / `driver's side front fender` / `driver's side front door` /
`driver's side rear door` / `driver's side rear quarter panel` / `rear bumper`
（乘客侧把 `driver's` 换成 `passenger's`）

---

## 1P Insurance (col I = value column) — 按标签核对每一行

| 格 | 字段 | 规则 |
|---|---|---|
| I2 / I3 | Coverage / Liability Status | `Pending`，不标黄 |
| I5 | Insurer | 保单卡全称 |
| I6 | Policy# | 照抄 |
| **I7** | **Policyholder** | **保单持有人姓名**（e.g. `Yujing Zhou`）—— 不是保单期间 |
| **I8** | **Driver** | **实际开车的人**（= 我方客户，e.g. `Qianxu Jin`）—— 不是 named insured |
| I9 | Driver License | **只填驾照号**（`Y9416226`）。非加州驾照 → 用简单字母标注州（e.g. `D1234567 (NV)`）。class/exp/restrictions 等放 Additional Details，不塞进本格 |
| I11 / I12 / I13 | Vehicle / VIN / LP | 保单+照片抓取 |
| I15 / I16 | Claim# / PD Adjuster | `Pending` + 黄 |
| I17 / I18 / I22 | Phone / Email / Fax | 保险目录带入 → 不黄；无匹配 → `Pending` + 黄（I22 无匹配则留空不黄） |
| I19–I21 | BI Adjuster 组 | 留空，不黄 |
| I24–I28 | Dec Page / Collision Ded / Rental / Med Pay / UM-UIM | `Pending` + 黄 |
| **I30** | **Policy Period** | 保单期间（e.g. `03/22/2026-09/22/2026`） |
| **I31** | **SR-1 Status** | **默认 `Pending` + 黄，不做任何判断**（不写"建议报"、不算截止日） |

---

## 3P Insurance (col L = value column)

| 格 | 字段 | 规则 |
|---|---|---|
| L2 / L3 | Coverage / Liability | `Pending`，不黄 |
| L5 / L6 / L7 | Insurer / Policy# / Period | 照抄保单卡 |
| L8 | Policyholder | 保单 named insured |
| **L9** | **Driver** | **直接写姓名**（`Arshia Amod Deshpande`）—— minor / 临时驾照等标注放 Note，不塞进本格 |
| L10 / L11 | Driver DOB / DL# | 驾照抓取 |
| **L12** | **Driver Phone** | **电话**。未知 → 空 + 黄（不要填地址） |
| L13 | Driver Address | 驾照地址 |
| L15–L17 | Vehicle / VIN / LP | 保单+照片 |
| L19 / L20 | Claim# / PD Adj | `Pending` + 黄 |
| L21 / L22 | Phone / Email | 目录带入 → 不黄；无匹配 → `Pending` + 黄 |
| L23–L25 | BI Adj 组 | 留空，不黄 |
| L27 | Policy Limits | `Pending` + 黄 |

---

## Treatment (col R=driver, S=pass1, T=pass2…)
**R3/S3/T3 一律 `Pending` + 黄**，不做任何逻辑推导（不判断是否已签约）。
子行留空。MRI / Pain Mgmt 留空。

---

## Note 栏
**不填任何信息，保持空模板。** 判断性标注（SR-1 依据、对方司机是 minor、责任风险等）
在表单正式加入 Note 区之前不写入 intake sheet。

---

## Passenger 1 (col C, rows 24–45)
C24=Name C25=Seat C26=Guardian(N/A if adult) C27=Relationship C28=DOB C29=Phone
C30=Address C31=Email C32=Gender C33=Marital C34=Spouse C35=Occupation C36=SSN
C37=Medi-Cal C38=Medicare C39=HI C40=Prior C41=Ambulance C42=Emergency C43=Urgent
C44=Primary C45=Injuries
（各字段规则同 Clients Index 对应项）

## Passenger 2 (col F, rows 24–45) | Pass3 (col C, rows 49–70) | Pass4 (col F, rows 49–70)

## No Passengers Rule
Fill C24:C45, F24:F45, C49:C70, F49:F70 all = `N/A`. NO yellow.

---

## Other Party Insurance (col X 标签, col Y 值) 及 Vehicle (col AA 标签, col AB 值)

**这两个区块一律：不填任何信息、不标黄，保留空模板。**

- **col Y** — 记录"第三方受害者"（3+ 车事故中另一台同样无责的车），普通两车事故留空
- **col AB** — 原为 3P 信息镜像区，现**不再镜像填入**，保留空模板

**3+ 方无位置时**：在右侧下一组可用列创建新的 Other Party Insurance 区（同结构），同样不标黄。

---

## Yellow Rules Summary

### 默认：抓取来的一律标黄
**凡是从客人表格或证件材料抓取、填进格子的值，一律标黄** —— 包括驾照直读的姓名 / DOB / 性别、
保单号、VIN、车牌，也包括客人答的 `No`。黄色在这里的意思是「**待 welcome call 与客户核对**」，
不是「有问题」。CM/CA 逐格确认后去黄，仍待定的保持黄色作为跟进提醒。

一个典型两车无乘客案子（Qianxu Jin）填完约 **68 个黄格** —— 这是预期结果，等于给 CM 的核对清单。

### NEVER yellow（唯一的例外清单）
| 项 | 原因 |
|---|---|
| I2 / I3 / L2 / L3 Coverage & Liability Status | 结构性 `Pending`，不是客人可确认的信息 |
| **F3** Accd Diagram | 非客人字段 |
| **F18–F22**（无警察报告时） | 没有警察卡/报告可核，留空即可 |
| C11 Spouse = `N/A`（Single/Divorced） | 无内容可核 |
| I17 / I18 / I22 / L21 / L22 | 保险目录带入的联系方式（无匹配时才 `Pending`+黄） |
| I19–I21、L23–L25 BI adjuster 组 | 留空 |
| **col Y / col AB** | 空模板区，永不填、永不黄 |
| 无乘客时的 C24:C45 / F24:F45 / C49:C70 / F49:F70 = `N/A` | 结构性占位 |
| **后续 workflow 写入的既成事实** | 见下 |

### 既成事实不被初填规则覆盖
本 sheet 是活文档 —— 建案后其它 skill 会继续写入真实进展（例如 `exer-lien` 把 C20 UrgentCare
写成 `Exer Urgent Care - Irvine, 7/26 2:00 PM` 并去黄）。**重填 / 补填 intake 时，不要用初填
默认值覆盖这些已发生的事实**（不要把上例改回 `No`）。重填前先下载线上版本做差异对比，
确认哪些是进展数据、哪些是待修正的旧填法。

### Mercury 特例
I18 / L22 若为 Mercury：`MyClaim+[CLAIM#]@mercuryinsurance.com` → **黄**，直到拿到真实 CAPA#。
