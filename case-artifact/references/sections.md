# 逐节的内容契约（shell 7.0：masthead + 十五节，顺序以 SKILL.md「页面结构」为准）

每节都标了：**放什么** · **数据来自哪** · **写坏了会怎样**。
节次固定；该案没有的节整节删掉，不要留空壳。

**每节固定包在 `<details class="sec">` 里，`<summary>` 包 `<h2>`**（见 SKILL.md 第 6 步）。

shell 里可用的组件：
`.card`（纸面卡片） · `.grid.g2/.g3`（卡片网格） · `.tw > table`（可横向滚动的表） ·
`.note`（金线旁注） · `.calc`（等宽算式块） · `.dls > .dl`（倒计时行） ·
`.bls > .it`（阻塞行；旧的 `.blockers > .bl` 卡片勿再新用） · `.tl`（时间线） · `.chip.done/.wait/.due`（状态标）
v7 新增：`.stats`（状态条，shell 自带） · `.road`（路线图） · `.it .meta`（待办出处行） ·
`.chk > li.miss/.got`（材料清单） · `[data-mail]`（寄件行，状态条据此计数） · `.bars`（周收入堆叠柱）

---

## 1. masthead —— **全英文**

`{{EYEBROW}}` 事务所 · 线 · 案由，例 `Lingtu Law APC · Litigation · Dog bite`
`{{CAPTION}}` `<Plaintiff> <i>v.</i> <Defendant>`，当事人名照起诉状
`{{SUBTITLE}}` 例 `Internal case record · Dog bite and premises liability`
`{{DOCKET}}` 六个 `<div><dt>…</dt><dd>…</dd></div>`：
Case number / Court / Department / Complaint filed / Date of loss / Attorney of record
`{{CHIPS}}` `.chip.plain`：案件性质、陪审费、`And related cross-action`、开庭日状态

`{{CHIPS}}` 末尾加一个 `<a class="chip plain" href="<case folder url>">Drive 案卷</a>`（没核到 folder url 就不加）

> 为什么全英文：这一块一一对应法院 caption，中英混排会让人核对时出错。
> 下面的状态条和路线图不属于 docket，用中文。

### 状态条 `{{STAGE}}` `{{DOL_ISO}}`

shell 自带五格。**只填两样**：`{{STAGE}}` 阶段（中文短语，与路线图「现在」那一步同名）、
`{{DOL_ISO}}` 事发日 `YYYY-MM-DD`。其余三格脚本数：待办 = `.bls .it` 条数；
寄件在途 = `[data-mail="pending|transit"]` 行数（页面没有寄件追踪节时这一格自动消失）；
下一期限 = 「关键期限」里最近的未来 `data-days`，并带出那一行的标题。
**所以这三格永远不要手写**，写了就会跟正文脱节。

### 路线图 `{{ROAD}}`

```html
<ol class="road" aria-label="案件进程">
  <li class="done"><span class="st">起诉立案</span><small>2026-06-02</small></li>
  <li class="now"><span class="here">现在</span><span class="st">送达</span><small>等 POS</small></li>
  <li><span class="st">Discovery</span></li>
  <li class="maybe"><span class="st">开庭</span></li>
</ol>
```

`done` 已完成（写完成日）· `now` 只有一个（写一句在等什么）· 无 class 为必经未到 ·
`maybe` 视情况才走（虚线圈）。最多 8 步，超出就合并。标准轨道：

- **诉讼**：起诉立案 · 送达 · 答辩 · Discovery · 调解 / MSC · 开庭 · 和解分配
- **诉前（狗咬 / PI）**：接案建档 · 调查保全 · 医疗账单 · 诉前索赔 · 起诉 · 诉讼程序 · 和解分配

**不写可能性百分比。** 分岔（被告有没有保险、对方会不会 cross-complain）写进「案件现状」，
每条写触发条件与依据，判断留给律师。

---

## 2. 案件现状

**放什么** 一段 `.lede` 讲清楚**这案子现在的胜负手在哪**，然后 `.deadlines` 倒计时卡片，
最后一条 `.note` 讲期限是怎么算出来的。

- lede 要有判断，不是复述。Yi Cong 那段写的是：对犬主的责任是法定的、硬；
  对物业全押在 notice 一个点上，而这个点零证据 —— 所以近期工作是防守性的。
- **倒计时独立成「关键期限」一节，一行一条，不要方框**（Klaus 2026-10-14 改定）。固定形状：

  ```html
  <ol class="dls">
    <li class="dl now">                      <!-- now 只给最紧的那一条 -->
      <div class="dl-head">
        <span class="dl-title">送达 X 并递交 POS-010</span>
        <span class="dl-when">2026-11-02<span class="count" data-days="2026-11-02"></span></span>
      </div>
      <p class="dl-desc">一两句：法条依据 + 为什么是这个日子 + 卡在谁身上。</p>
    </li>
  </ol>
  ```

  标题在左、日期与天数靠右，描述在下面一行。**按时间顺序排**，不按紧急度。
  `data-days` 的日期写死在 HTML 里，天数由 shell 的脚本实时算，过期自动变灰。
- `.now` 只上金色字（标题与天数），**绝不给行加金色边框** —— 金色只做 1px 细线与数字。
- `.note` 必须把法定期限**算给人看**：送达方式 → 起算 → 顺延 → 加几天。
  再写一句逾期的代价（waive objection / RFA 被视为承认）。

**写坏了会怎样** 期限算错 = 丢全部 objection。这一节是整页风险最高的地方。

---

## 3. 待办与阻塞 —— **排在 masthead 之后的第一节**

> **行式，不要方框。** 用 `.bls`：组标题 `<div class="grp">等 Hernán</div>`，
> 每条 `<div class="it"><span class="n">7</span><div class="tx">…</div></div>`。
> 旧的 `.blockers > .bl` 三个卡片盒子是 v5 及以前的写法，Klaus 2026-10-14 让换掉了。
>
> **编号：三栏共用一套连续编号**，从 1 开始，跨栏不重复
> （等律师 1-3 → 等客户 4-6 → 等所内 7-13…）。写法
> `<li><span class="n">7</span><b>事项。</b>说明…</li>`。
> Klaus 靠号码点事（「办 9」「7 和 8 一起」），所以**同一页内绝不重号**。
> 删掉一条之后后面的号会前移 —— 他知道，暂时接受；要改成固定号再说。

**放什么** `.blockers` 三栏：**等律师 / 等客户 / 等所内**。每条 `<b>` 起头点名事项，
后面一句说清为什么卡着、以及定了之后会牵动什么。

- 分栏依据是"**卡在谁身上**"，不是事项类别。Klaus 看这一节是为了知道该去催谁。
- 开头一句点题，例：「这案子现在没有一件事卡在起草上，全部卡在人身上。」
- 真的没有阻塞，就写「当前无阻塞」，不要为了填满而列伪待办。
- **v7：每条末尾一行出处** `<span class="meta">来源 Hernán 2026-10-12 邮件第 3 项 · 负责 Klaus · 期限 2026-10-20</span>`。
  来源写到能搜回原件为止（邮件日期 + 第几项 / 法条 / 客户微信日期）；负责人与期限没有就省掉那一段，
  不要编。期限若够硬，同时进「关键期限」。

---

## 3b. 案件现状 · 分岔口（v7）

lede 之后，路线图上每个 `maybe` 一张 `.card`：标题写分岔本身（「被告是否有 homeowner's 保险」），
正文写**触发条件 / 两条路各意味着什么 / 我们现在知道什么、从哪知道**。不写百分比。

---

## 4. Discovery 进度

**放什么** 一张矩阵表（哪一套 / 方向 / 送达日 / 到期日 / 状态），
后面 `.grid.g3` 三张卡拆解"对方这套到底问了什么"。

- 状态用 `.chip`：`done` 已送达 · `wait` 等对方 · `due` 迫近
- 方向写「对方 → 我方」「我方 → 对方」，别用缩写
- 拆解卡要给**可移植率**：多少题能从已送达的那套逐字沿用、哪几题必须改。
  Yi Cong 是 49 题里 42 题可沿用，改了 7 题并逐条点名 —— 律师据此只看那 7 题。
- 对方模版里的硬伤（问"原告的狗"、INCIDENT 定义写成车祸）写进来，这是留痕

---

## 4b. 寄件追踪（v7）

**放什么** 一张表：收件人 / 内容 / 寄出 / 追踪号 / 状态 / 回复期限。每行 `<tr data-mail="…">`，
值只有四个：`pending` 待入网 · `transit` 运输中 · `delivered` 已签收 · `returned` 退回。
状态 chip 对应 `plain` / `wait` / `done` / `due`；签收的写日期（`已签收 10-04`）。

- 追踪号 mono，链到 `https://tools.usps.com/go/TrackConfirmAction?tLabels=<号码>`
- 签收后回复期限算出来写进本表，**同时进「关键期限」**，`.note` 写算法
- 签收截图存 Drive，`.note` 写路径；页面上不贴图
- 一个收件人一行（一个收件人一套挂号，律所规矩）

## 4c. 客户材料（v7）

`.grid.g2` 两张卡：**待补** `li.miss`、**已收** `li.got`（右侧 mono 收到日期）。
待补项已在「待办与阻塞 · 等客户」里的，只写「见待办 N」，别把说明抄两遍。
清单依据写一句 `.note`（按哪类案子的材料清单 / 哪封律师邮件要的）。

---

## 5. 当事人与律师

**放什么** 一张表：当事人 / 身份 / 代理律师 / 送达地址（mono）。

- 身份用 `Plaintiff` `Defendant` `Cross-defendant` `Cross-complainant`，英文
- **谁是 attorney of record 必须明确标出**。换了律师但 substitution 没入案的，
  旧律师仍是 record counsel —— 这决定送达义务，错了就是送达瑕疵
- 送达地址列全（七个 g3pmlaw 那种就写"另六个个人邮箱"，不要漏说数量）
- 底下 `.note` 写送达名单的现状与依据，包括查 docket 的日期
- **v7**：保险公司（claim # mono）、房东 / 物业、政府机构（报告号）也各占一行；
  身份没核实的（只知道 DoorDash 账号名、只知道车牌）在身份列加 `<span class="chip due">身份未明</span>`

---

## 6. 事发经过

**放什么** `.lede` 一段经过，`.grid.g2` 四张卡（合法在场的依据 / 机关记录 ×2 / 关键证据），
再一张责任基础表（依据 / 针对谁 / 命题），最后视情况一条 `.note`。

- 卡片要挑**能堵住抗辩的那几件事**，不是流水账。
  Yi Cong 第一张卡讲的是包裹收件人就是被告本人 —— 这一条直接堵死 §3342 的"非法进入"抗辩
- 机关记录写全编号：报告号、活动号、警号、出勤号
- 不在我方手上的关键证据（对方的 Ring 录像）要单列一卡，写明已在哪几处文书里留痕
- 引错过的法条要写进 `.note` 并说明为什么错 —— 防止下次再引

---

## 7. 伤情与治疗

**放什么** 一张表（机构 / 诊治内容 / 就诊日 / 金额），`tfoot` 放合计；
后面 `.grid.g2` 放诊断码和悬而未决的问题。

- 金额右对齐、tabular-nums；合计必须等于 SOD 里的医疗费，**对不上就在页面上说明**
- 已结束的治疗要写**结束原因**（Yi Cong 是排班与派送路线冲突，不是症状好转）——
  这一句决定对方怎么解读治疗中断
- 还没开始的转介（签了 lien、尚未就诊）单列一行，金额留 `—`
- 与病历矛盾的客户陈述（处方日期早于事发）写进卡片，并说明目前怎么处理

---

## 8. 损害赔偿

**放什么** SOD 分项表 + `.calc` 算式块 + 若干 `.note`。

- `.calc` 把算式一步步摊开，每一步标出它对应哪个 interrogatory
- **自己复算**。对不上就加一条 `.note` 写明差额、为什么不改、以及记在这里的原因
- 取数窗口的讲究要写（"at the time of the INCIDENT" 取事发前四周，不是停工后的平均）
- 口径要写（gross receipts / Form 1099 / 未扣业务支出 / 保留改按 net）
- **尚未主张但已浮现的损失**单独一条 `.note`，写清不披露的后果
- **v7 误工案：每周收入堆叠柱**，事发前后各取够看出断崖的周数：

  ```html
  <figure class="bars">
    <div class="bars-legend"><span style="--c:var(--s1)">Uber</span><span style="--c:var(--s2)">Lyft</span></div>
    <div class="bars-scroll"><div class="bars-plot" style="--max:1200">
      <div class="col hit" tabindex="0" title="05-04 周 · Uber $420 · Lyft $180">
        <div class="bar"><i style="--v:420;--c:var(--s1)"></i><i style="--v:180;--c:var(--s2)"></i></div>
        <span class="x">05-04</span></div>
    </div></div>
    <figcaption>数据来源 + 口径（gross / 1099）。明细见下表。</figcaption>
  </figure>
  ```

  `--max` 取最高那周向上取整；`<i>` 从底往上写；**值为 0 的段不写**（否则留一道 2px 缝）；
  事发那周 `col hit`。平台按 `--s1`…`--s4` **固定顺序**分配，不轮换（已过 dataviz 校验）。
  **图下必须跟一张明细表**（周 / 各平台 / 合计），图只是看形状，数以表为准；表的合计要跟 `.calc` 对得上。

---

## 9. 文书产出

**放什么** Bates 区间对文件名的一张表，外加一句 production 的范围与送达方式。

- 区间写法 `000002–000006`，mono
- 页数有变动的，写明哪一版送到哪一号
- 视频等原生格式单列

---

## 10. 风险点

**放什么** `.grid.g2` 卡片，每张一个风险。标题是结论句，不是名词。

- 标题要能单独读懂：「送达的 Index 只列到 CONG 000105」好过「索引问题」
- 每张卡要讲**会怎么咬到我们**，以及现在的处置
- 已经发生但无害的（产出完整、只是清单漏行）要明说无害，不要制造假警报
- **v7 定级**：卡片第一行 `<p><span class="chip due">要处理</span></p>` / `chip wait 留意` / `chip done 已解决`，
  按「要处理 → 留意 → 已解决」排。已解决的留着 —— 它说明这个坑查过了

---

## 11. 关键日期 / 12. 文件位置

**关键日期** `.tl` 时间线，已发生 + 未来都要有。重要节点加 `class="mark"`（金点），
未来加 `class="future"`（空心点）。日期 mono，`YYYY-MM-DD`。

**文件位置** Drive 文件夹对照表。末尾 `.note` 写旧版的标注约定
（`SUPERSEDED` / `SERVED`），并点名本案有哪几份容易认错的。

---

## 页脚

固定两行：免责声明（中文）+ 落款（事务所 · 整理人 · 主办律师 · 数据截至日）。
截至日由 shell 的脚本自动填，不要手写。
