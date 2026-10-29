# San Bernardino County —— 立案包怎么做

LA 用 **CIV 109**（Civil Case Cover Sheet Addendum and Statement of Location）。
圣贝纳迪诺不用 CIV 109，用 **Certificate of Assignment，表格号 13-16503-360
（Rev. June 2019，Mandatory Use）**。其余（SUM-100、CM-010）两个县一样。

本页分两类信息：**✅ 已被法院受理验证过的**，和 **🔎 查来的、尚未经一次立案验证的**。
别把两类混着用。

---

## ✅ Yi Cong 的实证（2026-06-30 立案，已受理，案号 CIVSB2619725）

| 项目 | 实际填／选的值 |
|---|---|
| 事发地点 | 950 N Duesenberg Dr. Apt. 6210, **Ontario, CA 91764** |
| One Legal → Court Name | `San Bernardino County, Superior Court of California` |
| One Legal → Court Branch | **`San Bernardino-Justice`** |
| Certificate of Assignment 的 district 行 | **`Civil Division of the San Bernardino`** |
| One Legal order # | 28636644 |

> **Ontario 的 unlimited civil 走 San Bernardino 区。** 这一条有判决性分量，因为直觉会
> 指向别处 —— 见下面「Ontario 为什么不是 Fontana」。

district 那一行要填 **`Civil Division of the San Bernardino`**，不是光写
`San Bernardino`。表格预印的是「…is filed for proceedings in the ＿＿＿ District of
the Superior Court under Rule 131…」，照 Yi Cong 已受理的写法抄。

立案包命名照 Yi Cong（Chao Zheng 沿用，一致）：

```
1 - Summons.pdf
2 - Complaint.pdf
3 - Civil Case Cover Sheet.pdf
4 - Certificate of Assignment.pdf
```

---

## 🔎 Ontario 为什么不是 Fontana、也不是 Rancho Cucamonga

三个来源会把人带偏，先写清楚：

- **CHP 报告的 Judicial District 栏会写 `FONTANA COURTHOUSE`**（Chao Zheng 那份就是）。
  那是 CHP 自己的归属，**不是民事立案区**。Fontana 地理上确实管 Ontario，但
  **不收 unlimited civil**。
- **Rancho Cucamonga（West Valley）听起来最像**，但法院「Where can I file」页的
  城市清单里**没有 Ontario**。
- 法院自己的页面把 Ontario 列在 **Civil Division of the San Bernardino District**
  名下，该区收 unlimited civil。现行站与旧站（old.sb-court.org）说法一致。

法院地址（填进 SUM-100 与 CM-010）：

```
San Bernardino Justice Center
247 West 3rd Street
San Bernardino, CA 92415-0210
```

> 其它城市（Victorville、Barstow、Joshua Tree、Big Bear 等）**没验过**，不要照搬。
> 每换一个城市，去 One Legal 的 branch 下拉框确认一次，然后把结果补进上面那张表。

---

## 模版在哪

`Hernan Simo Cases/2. Template/1. Pleadings & Court Forms/San Bernardino County/`

- `Certificate of Assignment (SB, blank).pdf`
- `ADR Package (SB).pdf` —— 随传票一起送达
- `Amendment to Complaint (SB, blank).pdf`

SUM-100 / CM-010 仍用 `Judicial Council forms (Hernán pre-filled)/` 里那两份。

---

## Certificate of Assignment 的字段地图

这张表的字段名是自动生成的 `undefined_N`，**不能按名字猜**，照这张表填：

| 内容 | 字段名 | 备注 |
|---|---|---|
| 原告 | `undefined` | y≈697.7 |
| 被告 | `vs 1` | **只有 221pt 宽** —— 用 `JASA TRANSPORTATION INC, et al.`；这张不是送达文书，可以简称 |
| 区 | `District of the Superior Court under Rule131 and General Order` | 填 `Civil Division of the San Bernardino`；**`/DA` 必须 7pt** —— 默认字号会切成 `San Bernard`（Chao Zheng 2026-10-15 律师已签的那份就是被切的，只能重签） |
| 案由勾选 第 N 行 | `undefined_(N+1)` | 填 `X`。**Personal Injury 是第 11 行 → `undefined_12`** |
| 资格事由名称 | `NAME  INDICATE TITLE OR OTHER QUALIFYING FACTOR` | 人伤写 `Place of injury` |
| 地址 | `ADDRESS` | **只有约 179pt** —— 长地址要把 `/DA` 调到 6pt，否则会被切掉 |
| 城市 / 州 / 邮编 | `CITY` / `STATE` / `ZIP CODE` | |
| 宣誓地点 | `undefined_23` | 填 `City of Industry` |
| 宣誓日期 | `executed on` | **留空**，律师签字当天填 |

**用 `fill_forms.py` 的 `fill_sb_coa(cfg, tmpl, out)` 填，然后 `flatten(out)`** —— 字号、勾选框定位都在里面，别再手写一次性脚本。
交给律师签之前**渲染一遍看 district 行和地址行**，pdftotext 读得出全文不代表画面上没被切。

勾选框不要按行号硬算 —— `fill_forms.py` 的做法是**先在页面上找到 "Personal Injury"
那行文字的 y 坐标，再取最近的那个窄方框**，表格改版也不会错位。

两处 caption 的宽度差别要记住：**summons 必须写全名不许简称**（见
`summons-caption.md`），**Certificate of Assignment 必须简称**，因为格子只有一行。

---

## 别忘了

- 交付前一律 `qpdf --flatten-annotations=all`，理由见 `summons-caption.md`。
- Statement of Damages（CIV-050）**不随起诉状立案**，只送达；只有申请缺席判决时才连同
  送达证明交进法院。人伤案必须送，因为 CCP §425.10(b) 不许在起诉状里写金额，
  §580(a) 的上限就靠它。对未应诉的被告，§425.11(d)(1) 要求**按送达传票的方式送达** ——
  所以和传票起诉状捆在一起送，省一趟人工送达费。
- 查 docket：`cap.sb-court.org`，按案号免登录，但 **reCAPTCHA 必须 Klaus 点**，
  内置浏览器加载不出，要走 Claude in Chrome。见 `[[sb-court-access-portal]]`。
- 案号前缀 `CIVSB`。

---

## ⚠️ 2026-10-28 更正：Ontario 的 PI 案被法院改派到 Rancho Cucamonga 区

Chao Zheng（I-10 / Ontario 事发）按上文填 CoA = `Civil Division of the San Bernardino`、One Legal branch = `San Bernardino-Justice`，
**书记员受理时改派 Rancho Cucamonga District**：案号 **CIVRS2609730**（前缀 `CIVRS`），
conformed 盖章「Rancho Cucamonga District」，传票法院地址被改成 **8303 Haven Avenue, Rancho Cucamonga, CA 91730**。
同为 Ontario 的 Yi Cong（狗咬）当初是 `CIVSB2619725`（San Bernardino 区）—— **同城不同结果，区由书记员定，不是我们定。**

**怎么用：** 立案后以法院盖章版的区名/地址为准，后续 subsequent filing（jury fee、POS 等）在 One Legal 选对应分院；
送达用的就是法院签发、地址已改的那份传票。下次 Ontario 案可考虑直接填 Rancho Cucamonga 区 —— 先问 Klaus。
