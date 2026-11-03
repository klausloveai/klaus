---
name: skye-forms
description: "Auto-fill the USCIS and DOL forms for any 人才移民 petition at Lingtu Law, routing by case type first — O-1A/O-1B (I-129 with the O and P supplement, I-907, three G-1650s), EB-1A (I-140, G-1145) and EB-2 NIW (I-140 plus ETA-9089 Appendix A, Appendix C and Final Determination) — with G-28 when the firm is attorney of record, I-907 when premium processing is requested, and one G-1650 per fee. Each run reads that case's 填表指令 doc and writes the filled forms into the client Drive folder the user names. Blank forms are always downloaded fresh from uscis.gov and dol.gov and each edition date checked first. Use whenever forms need filling, checking or regenerating: 填表, 填O1表格, 填EB1A表格, 填NIW表格, 填140, 帮XX客户填表, 有G28还是无G28, 9089怎么填, 加急要不要交907, 几张1650, 核对表格版本, 换新版表格重填. Also for a single form and for current editions or fees."
---

# 人才移民填表 (Lingtu Law · O-1 / EB-1A / NIW)

一次填表是四到七张表、横跨一到两个机构、两到三笔付款，而且**几乎每种错都是不出声的** ——
checkbox 的 export value 对不上、新版里字段名挪了位、上个季度还对的费用。所以流程的形状是固定的：
先认案件类型，从写好的填表指令 doc 出发，现下空表，从客户自己的案件文件夹里学事实，
走真实 AcroForm 字段填，最后用眼睛把每一页读回来。

三种案件类型合在这一个 skill 里，因为 Step 0–7 的骨架是同一套；不同的只有表单集、
参数和几条写死的规则。**类型专属的完整 playbook 在 `<type>/playbook.md`，路由进去之后从头读完。**

```bash
export PATH="$HOME/.local/bin:$PATH"   # gws 在这里，每个 session 跑一次
```

---

## ⛔ 三种类型共用的一条铁律

**只用现下的空表填。** 不许从旧案 PDF、库存样本或所里 `0 Sample` 的副本上改。那些是过期版本
（字段名会挪位）、AcroForm 可能是坏的，还会把作废的所内数据带进新案子 —— 已经退役的
`8186658535` 电话、空白的律师执照号。

**数值来自那个案子的填表指令 doc；位置来自现行表格自己印的条目号。** 各类型 references 里的
字段映射是导航用的，不是照抄旧案答案的许可。

这条在 NIW 上不是理论风险：**上一个版本边界上 ETA-9089 Appendix A 有 75 个字段名变了**，
而库里那两份 9089 先例用的都是旧版。

---

## Step 1 — 先认案件类型，别的都靠后

从案件文件夹名、填表指令 doc 的标题、或者用户的说法里判断类型。判断不了就问，不要猜。

| 类型 | 表单集 | 填表指令 doc 在哪 | 路由到 |
|---|---|---|---|
| **O-1A / O-1B** | I-129 + O and P Supplement · I-907 · G-1650 × 3 · G-28（做 attorney of record 时） | `0.testing` → `Test O1B` → `2. Form` | `o1/playbook.md` |
| **EB-1A** | I-140 · G-28 · I-907（加急）· G-1145 · G-1650 每笔费用一张 | `0.testing` → `Test EB1A` → `2. Form` | `eb1a/playbook.md` |
| **EB-2 NIW** | I-140 · ETA-9089 Appendix A + Appendix C + Final Determination · G-28 · I-907（加急）· G-1145（不加急）· G-1650 每笔费用一张 | `0.testing` → `Test NIW` → `2. Form` | `niw/playbook.md` |

**G-1145 不属于 O-1 这个包。** 库里有它的样本，但 O-1 不交。

路由之后，那个类型目录下的文件这样用：

| 文件 | 什么时候读 |
|---|---|
| `<type>/playbook.md` | **进来先读完这一份**，它是该类型的全流程 |
| `<type>/references/…` | 动某一张表之前读那张表的字段映射 |
| `<type>/assets/…-fill-instructions.md` | 填表指令 doc 的本地范本 |
| `<type>/scripts/…` | 下表、填表、CJK 盖字用的脚本 |

playbook 和 references 里写的 `references/…`、`scripts/…`、`assets/…` 都相对于
`<skill>/<type>/`，不是相对于 skill 根目录。

---

## Step 0–7 — 共用骨架

这是三种类型都走的这一条线。每一步的类型专属细节在该类型的 playbook 里。

### Step 0 — 把这个案子的填表指令 doc 摆在面前

Fixed / Flexible 那份指令表，说清楚这个案子需要哪些数据、每个事实填到哪。
**没有它就不要开始填** —— 找不到就停下来问，不要从别的案子的 doc 推。

### Step 1 — 定这个案子的参数

三种类型都要定的：

- **有 G-28 还是无 G-28** —— 所里做不做 attorney of record
- **加不加急** —— 决定交不交 I-907
- **petitioner 是谁**

类型专属的还有：O-1 要定 COS 还是 CP、公司担保还是 individual agent、是不是 small employer；
EB-1A 是自我申请（I-140 上几乎每个 petitioner 栏都指回受益人本人）；
NIW 要定加急与否连带的 G-1145 收不收、以及是不是重递。细节看各自 playbook。

### Step 2 — 从客户自己的案件文件夹里读事实

**I-94 不是可选项。** 受益人人在美国时，最后入境栏从 I-94 上读；人不在美国，
按各类型 playbook 里写的方式标注（EB-1A / NIW 在 I-140 item 11.a 写 `Not in U.S.`）。

### Step 3 — 现下空表，逐张核对版本

从 `uscis.gov`（NIW 还要 `dol.gov`）现下，对着每张表自己那个官方页面核 edition date。
按 Step 1 定下的参数摘表：无 G-28 摘 G-28；不加急摘 I-907；NIW 加急则摘 G-1145。

### Step 4 — 走真实 AcroForm 字段填

不要靠坐标盖字。**中文字段要跑第二遍**（EB-1A 上是必须，NIW 上是强制项），
用 `<type>/scripts/cjk_stamp.py`。

### Step 5 — 每一页都用眼睛读回来

填完不等于填对。checkbox 的 export value、串行的字段、被截断的长地址，
只有把渲染出来的页面看一遍才会暴露。

### Step 6 — 把要客户签字的页抽出来

单独成文件，命名让人一眼知道是等签字的。

### Step 7 — 传回用户指定的 Drive 文件夹并记日志

传完核对文件名和字节数 —— 传了一半在 Drive UI 里跟传完了长得一样。

---

## 写死在类型里的规则（不要现场重新判断）

### EB-1A —— 三条全所默认

1. **Part 4 Processing Information 一律 CP / Guangzhou / China。**
2. **第 2 页最后入境栏只在受益人人在美国时填**；不在的话 item 11.a 写 `Not in U.S.`。
3. **第 3 页 Part 4 分三块**：`3.a-3.f` 出生国地址（英文）· `4.a-4.c` 中文姓名 ·
   `5.a-5.g` 同一个地址的中文写法。

### NIW —— 三条专属规则

1. **I-140 Part 2 勾 `1.h`，那个 NIW 框 —— 绝不是 `1.d`。**
2. **Part 4 Processing Information 一律 CP / Guangzhou / China。**
3. **最后入境栏读客户的 I-94，且只在人在美国时填**；F-1 或 J-1 的 `D/S` 写在 item 11.b，
   人不在美国就在 item 11.a 写 `Not in U.S.`。

另外：**ETA-9089 不认证提交** —— NIW 没有 PERM 案子，所以 Final Determination 第 1 页留空。

### O-1

Part 4 之类的处理信息按填表指令 doc 走，不套 EB-1A / NIW 的 CP 默认。
三张 G-1650 对应三笔费用，费用金额每次都去 `o1/references/fees-and-filing.md` 核。

---

## 只问一件小事的时候

用户只要一张表、或者只想知道现在哪个 edition、这笔费用多少 —— 直接答，不用把全流程跑一遍。
但**版本和费用一律去官方页面现查**，不要凭记忆答。

## 收尾报告

报告：填了哪几张表、每张的 edition date、按什么参数摘了哪些表、签字页抽了哪几页、
传到哪个 Drive 文件夹、以及有没有哪一处是你拿不准而按填表指令 doc 原样照填的。
