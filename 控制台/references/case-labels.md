# Hernán 案件标签树（klaus@，Klaus 手动维护）

Klaus **手动**把案件邮件归到这些嵌套标签；控制台按标签把已 label 的邮件捞进来
（**不做自动打标签**——模拟过，纯发件人/主题判案子对 Bo Tao「转发无名」、Jiayu Ma「只有 claim#」
会误判，故弃用，改由 Klaus 自己标）。

## 标签树（2026-08 实测）
母标签 `⚖️Hernan Cases`（id `Label_2462494372802428188`）**本身挂 0 封邮件**；
邮件只挂在 **case leaf** 上，分类中间层也不挂。**扫描按 leaf id，别查母标签**（会捞不到）。
**动态发现**：`labels list` 取 name 以 `⚖️Hernan Cases/` 开头且最深层者即案件标签，新案自动纳入。

| Case (leaf) | Label id | 类别 |
|---|---|---|
| CL-Brian Wu v. Azucanela LLC | Label_2581322858093206735 | Civil Limited |
| DB-Bo Tao-062726 | Label_7788628222844443496 | Dog Bite |
| DB-Guolin Zhao-062126 | Label_1845552354652370299 | Dog Bite |
| DB-Lina Lu-070926 | Label_5980763080143242915 | Dog Bite |
| DB-Mudong Huang-062926 | Label_1856079116373276236 | Dog Bite |
| DB-Weicong Lin-070926 | Label_2 | Dog Bite |
| DB-Yi Cong-041226 | Label_6510174514892044222 | Dog Bite |
| LB-Hansen Li v. Aligcus, Inc | Label_8866899269630938126 | Labor |
| LB-Saihui Tan/CB Kitchen and Bathroom | Label_3403499162978877023 | Labor |
| Jiayu Ma | Label_4186601605671161245 | PI Auto |
| Zhiping Liu | Label_4960110660159648009 | PI Auto |

**不要硬编码这张表**——每次动态发现；此表仅供参考 + 记 id。
`LB-Saihui Tan/CB Kitchen…` 名字里带 `/`，Gmail 当层级 → 多嵌套一层；用 id 操作，别用名字拼 `label:`。

## 已知缺口
**Brian Wu（Civil Limited）有标签、但不在 Tracking Sheet**（表无 Civil Limited tab，
见 [[limited_civil_commercial_cases]]）。→ 邮件能扫到，但诉讼进度 status/日期拿不到；
待 Klaus 在表里加 Civil Limited tab/行，或指明进度来源。
