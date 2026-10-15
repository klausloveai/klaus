# SUM-100 的两条铁律 —— 每份 summons 都必须过这两关

Klaus 2026-10-14 定（Chao Zheng v. Jasa Transportation，连改三版才对）。

> **1. 和起诉状一模一样。** caption 里的当事人块逐字照抄 complaint，不改写、不简称、
>    不用 "et al."。
> **2. 所有内容都要落在 caption 格子里。** 不许因为太长被 FOR COURT USE 框压掉、
>    或者被切在半句话中间。

两条都失守过，各自的坑不一样，下面分开说。

---

## 铁律一：逐字照抄 complaint

送达的被告名必须和起诉状 caption 完全一致 —— 这是送达是否有效、默认判决是否站得住的
基础。**不要**缩写成 `JASA TRANSPORTATION INC, et al.`：summons 是给被告看的，
每一名被告都要在上面看到自己。

照抄的范围包括身份后缀和 DOE 区间：

```
JASA TRANSPORTATION INC, a California corporation; JOSHUA OLVERA, an individual;
and DOES 1 through 50, inclusive
```

原告块同理，未成年人的 GAL 写法（`MUDONG HUANG, a minor, by and through his Guardian
Ad Litem, BAIYUN JIANG; and BAIYUN JIANG, individually`）连大小写都照抄。

> ⚠️ Certificate of Assignment（圣贝纳迪诺 13-16503-360）那张**可以**用
> `JASA TRANSPORTATION INC, et al.` —— 它的 caption 格子只有一行 221pt，塞不下全名，
> 而它不是送达文书。**只有 summons 不许简称。**

---

## 铁律二：全部落进格子

### 坑在哪

SUM-100 的 `FillText25`（NOTICE TO DEFENDANT）和 `FillText180`（YOU ARE BEING SUED
BY PLAINTIFF）：

| | 值 |
|---|---|
| 字段 rect | x 36.0 → 431.3（宽 **395.3pt**） |
| 字段 `/DA` | `/ArialMT 9 Tf 0 g` |
| FOR COURT USE 框左边 | 约 x **383pt** |
| 实际可用宽度 | **≈ 330pt** |

两件事叠在一起就出事：

1. **字段声明的宽度比肉眼可用的宽度大。** 按 395pt 去 wrap，文字会一路排到 x≈425，
   正好钻进 FOR COURT USE 框底下。
2. **字号会在阅读器里变大。** 剥掉 XFA 之后 `/ArialMT` 常常解析不到，阅读器回退并
   按大一号重排 —— 9pt 下 379.6pt 的一行，到 10pt 就是 421.8pt，必溢出。
   （`pypdf` 生成外观流时也会打印 `Font dictionary for /ArialMT not found`。）

所以**包裹宽度必须写死 330pt、并按 9pt 计算**，留出被放大到 10pt 的余量。

### 怎么断行

**在当事人边界（分号）断，不要按宽度硬切。** 按宽度切会断出
`JOSHUA OLVERA, an / individual;` 这种半句，像排版事故，律师会退回来。

`scripts/fill_forms.py` 里的 `caption_wrap()` 就是干这个的：按 `'; '` 切成若干段，
每段保持完整，再贪心装行到 330pt 为止。正确输出：

```
JASA TRANSPORTATION INC, a California corporation;
JOSHUA OLVERA, an individual; and DOES 1 through 50, inclusive
```

一名被告本身就超过 330pt（很长的公司名）时，`caption_wrap()` 退回逐词换行 ——
这种情况把该段单独列一行，必要时手工核一眼渲染稿。

### 怎么验

**不要靠 pypdf 读字段值就算完** —— 字段里有值不代表看得见。两步：

```bash
# 1) 展平，让文字烧进页面内容层
qpdf --flatten-annotations=all "1 - Summons.pdf" out.pdf && mv out.pdf "1 - Summons.pdf"

# 2) 读回来看断行，再渲染出来看位置
pdftotext -layout "1 - Summons.pdf" - | sed -n '6,12p'
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r110 -dFirstPage=1 -dLastPage=1 \
   -sOutputFile=chk.png "1 - Summons.pdf"
```

`pdftoppm` 渲染这类 Judicial Council 表单会糊，**用 gs**。

---

## 展平是收尾动作，不是可选项

SUM-100 / CM-010 / CIV-050 / CIV 109 全是 XFA 混合表单。剥掉 XFA 层之后，值只活在
AcroForm 字段里，而**不是每个 widget 都有外观流** —— Chao Zheng 的 CIV-050 是
52 个文本 widget 只有 15 个有。结果是 Ghostscript 渲染满满当当，Klaus 在 Preview /
快速查看里看到的却是**一张空表**。

所以交付前一律 `qpdf --flatten-annotations=all`：字段归零、文字进页面内容层，
任何阅读器、打印机、One Legal 预览看到的都一样。展平后 `pdftotext` 能读到正文就是
通过。

需要留可编辑版的，按 Weihong Wang 那个案子的惯例，旁边放一份
`<N> - <文书名> (fillable).pdf`。

---

## 交付前自检清单

- [ ] 被告块和 complaint caption 逐字一致（含 `, an individual` 等后缀与 DOE 区间）
- [ ] 原告块同样逐字一致
- [ ] 断行在分号处，没有半句被切开
- [ ] gs 渲染出来，两行都在 FOR COURT USE 框左边
- [ ] 已 `qpdf --flatten-annotations=all`，`pdftotext` 读得到当事人名
- [ ] 案号、DATE、Clerk by 三处留空（立案时才填）
