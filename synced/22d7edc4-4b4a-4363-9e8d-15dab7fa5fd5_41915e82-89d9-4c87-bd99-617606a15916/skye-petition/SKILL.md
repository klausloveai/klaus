---
name: skye-petition
description: "Draft, revise and audit an O-1 petition letter for a Lingtu Law / SIA 高徒 filing. Covers pulling the firm's O-1 PL template from the shared drive, generating the letter skeleton, building each criterion section from the regulation outward, tying every assertion to a numbered exhibit, auditing the letter against the evidence package for unsupported figures and template leftovers, keeping exhibit numbering consistent across the letter, the INDEX OF EXHIBIT and the Drive folders, and processing a reviewing attorney's comments. Use whenever asked to write, restructure, condense, proofread, renumber or fact-check an O-1 petition letter, to add or rework a criterion argument, or to act on review comments on one. Routes any petition instruction by type first — O-1A, O-1B, EB-1A or NIW — to that type's own sample template and most recent filed case. The craft guidance is O-1 specific; EB-1A and NIW use different frameworks."
---

# O-1 Petition Letter Drafting (Lingtu Law / SIA 高徒)

**Scope.** The routing table in Step 0 covers all four petition types the firm files. The
craft guidance from Step 1 onward is **O-1 specific** — EB-1A and NIW are argued on
different frameworks, so route those to their own sample and their own recent-case
reference and argue on that framework, not on this one.

The letter is an argument built on a numbered evidence package. Two rules govern
everything below: **every assertion carries an exhibit number**, and **the exhibit must
actually say what the sentence says**. Most of the work is enforcing those two.

---

## Step 0.0 — 每次动笔之前，先学一遍

**这一步每次起草、每次大改都要重跑**，不是只在第一次接手这个案子的时候做。四步走完才进 Step 0。

### 1. 读所里的培训库

Drive 文件夹 **`1. Training`** — `1M3WZo48Q9JOeKVHnqznK1hnJQ1FWvB0b`

| 子文件夹 | 里面是什么 |
|---|---|
| `1. General 培训` | 通用培训 |
| `2. Legal Writing ` | `legal writing 2_7.pptx` + `Legal Writing.mp4` |
| `3. 如何使用GPT` | AI 工具的用法规范 |
| `4. 如何写新闻` | 媒体报道类证据怎么组织 |
| `5. 如何写推荐信` | 推荐信 |
| `6. 证据规范` | 证据本身的规范 |
| `7. Checklist` | `INDEX OF EXHIBITS.docx`、`Exhibit 0 AP_Translation certificate`、签名教程、两段 Checklist 录像 |
| `Exhibit （打包教程）` | exhibit 打包 |
| `Others` | 内含 `RFE Language`（那是 `skye-rfe` 的必读，写 PL 时也值得扫一眼） |
| `Training.docx` | 根目录那份总纲 |

**读得动的全读** —— Google Docs、`.docx`、`.pptx`、PDF。`.mp4` 是给人看的录像，跳过，
但在收尾报告里说明哪几份是视频没读，别让人以为你看过了。

一次没读完不要紧，但**至少要把这次要写的那条 criterion 相关的那几份读掉**。

### 2. 读蔡律师的语言与论证规则

`references/cai-language.md` —— **从头读完再动笔。** 她已经指出过的问题，不要让她第二次指出。

### 3. 把这个类型的法条现行原文调出来通读

条号见 Step 2 的对照表。**去读现行原文，不要凭记忆写** ——
`uscis.gov` 对 WebFetch 返回 403，用 Browser pane（`preview_start` 打开 URL，再 `get_page_text`）。

读法条是为了回答一个具体问题：**这一条到底要什么？** 先把它拆成要件，
再回头看客户的材料能对上哪几个要件。顺序反过来（先看材料再找法条）写出来的东西是凑的。

### 4. 下载对应的模板

见 Step 0 的路由表。

---

## Step 0 — Route by petition type before anything else

The first move on any petition instruction is to **establish which type it is** — from the
case folder name, the intake note, or the 方案 — and then go to that type's own sample
folder. Never start from a blank page, and never start from a neighbouring client's
letter picked at random.

Everything hangs off master shared drive `0AIXy3tjXMf-MUk9PVA`:

| Type | Sample folder → `2. Cover/PL/Index` | PL template |
|---|---|---|
| **O-1A / O-1B** | `O-1` `1-g_HDMHwSi7PtV5Nlyw1nUCwXGbQkwpS` → `0 Sample （O1）` `1u6SW71oWNmuJlVAAebi7NHzwz8J7U2cT` → `1KlSs38B0r4XWDSIJRw5m7puEZXttb4Qi` | **`3. PL Template`** `1aILAhBxmX7nkTLl62NK29bnGo0ywcg4quPohYiBxDTo` |
| **EB-1A** | `EB1A` `1rDPCJzYAiG13SzJjkrTqc9D7eUxU12xR` → `0 Sample （EB1A）` `1w3IBNQgOiFMXVJFAwKZ4SfwHkOWg5_t5` → `1NPZYMtv4fEQm9hNkd1o_ZZ0ndSLaoaYu` | **`PL_Template_EB1A`** `1xWnqIwQ_6a9Cd6xr2yoTNZ8DXm8hTTFnUkOV8vF-SO4` |
| **NIW** | `NIW` `1D7hKuq2qi4daqIegvjM3YUiN3WKsawjy` → `0 Sample （NIW）` `1tm3pxC3xZVQuRNmdNUjj6Wc8XY94J5lw` → `1yTrJRlTCr9bpR_lSFdWqdRjBNVxtpKBi` | **`PL Template`** `1VdL0qlVr37LTPvEQQbfB4I5GFRieS9LPmuGu5Sh9JiA` |

There is **no `0. Template` folder** in this Drive, whatever other skills say. The `O-1`
folder also holds loose `O1 Sample 1.docx` / `O1 Sample 2.docx` — finished letters, not
the template; open them only if told to.

The EB-1A and NIW `2. Cover/PL/Index` folders also carry a cover page and an
`INDEX OF EXHIBITS`; take those at the same time so all three documents share numbering
from the first draft. The EB-1A folder additionally holds
`RFE_Final Merits Determination` (`1BNkGq-Jj3LrUIahQ_7RPizZhsCeqzyfTrEPRxzaTETA`).

### Then read the three most recently filed cases of that same type

The template gives **structure**; recently filed cases of the same type give **the
argumentation preferences currently in use**. **Read three of them before drafting**, most
recent first — one case can be an outlier, three show you what the office is actually doing
right now, and where they disagree the newest one wins. This is a standing instruction, and
it is the exception to "don't go reading other clients' letters." Follow their structure and
legal moves, never their words (Step 7).

If fewer than three of that type have been filed, read what exists and **say so in the
report** — don't quietly pad the count with a neighbouring type.

| Type | Read | Document |
|---|---|---|
| **O-1B** | Ziqing Shi — short-form drama / film-TV, **approved** | `Ziqing Shi_ O1_PL` `1tQyeb8ESuRwPF___Fh6IqxvwGapy6Ayn1iV0cEpe9cc` |
| | Yixuan Wang — design / arts | `Yixuan Wang_PL.docx` `1Z7IjmrCVuS5oZzyA9tdkAzOmvZuwfSgA` |
| **O-1A** | Yuqian Tao | `Petition letter_v08226` `1Jaq2uUpF5pU1Uw-5yzV6S51-P22dmElC9WHkXKNDN74` |
| **NIW** | Yunyun Zhou — **approved** | `Yunyun Zhou_PL` `1RairGE8MnbsRwS7ckeInHFdXSJon_r8ikqAD8lmlYtk` |
| | Jiping Huang | `PL` `1g20epIYEV4nAMD9f2N59KiZ6GWU_CDNKQgLNIvjMalU` |
| | Wenqian Shao | `PL` folder `1ZhIEq5-gNOJ3rfVAJklHPtbxaYoSijrp` |
| **EB-1A** | the most recently filed case in the EB1A drive | `1rDPCJzYAiG13SzJjkrTqc9D7eUxU12xR` |

⛔ **Reading the reference case is not optional, and the skeleton in Step 1 does not
substitute for it.** The shape sketched in this file is a summary; the filed letter is the
authority. Drafting straight from Step 1 without opening the same-type case produces a
letter in roughly the right order with the wrong internal structure — the numbered layer
missing, headings phrased as regulation restatements, MAINTENANCE OF STATUS absent, no
verbatim quotation of the exhibits. That has happened. Open the case first.

⚠️ **This table goes stale by design.** It names the most recent case as of the time of
writing. Each time a newer case of that type is filed, **update the row to point at it**.
When the user names a specific case, theirs wins over the table.

Two spellings differ from how they are usually said aloud — in Drive they are
**`Yunyun Zhou`** (not Yuyun) and **`Wenqian Shao NIW`** (not Wenqiao).

For **NIW** there is standing permission to read across the whole NIW drive to build up
familiarity with how the firm argues those. That permission is NIW-specific.

**O-1B is the straightforward path** — apply the template and change the names.
**O-1A is not**: the regulation number changes and the criteria change with it (Step 2).
For **EB-1A**, first establish which criteria the client actually claims, then draft only
those.

---

## Step 0.1 — Start from the template, not from a blank page

Beyond the same-type reference case named in Step 0, **do not go browsing other clients'
letters on your own initiative.** If the user wants a particular letter studied, they
will name it. Absent that, the template + the same-type reference + the evidence package
are the whole input.

⛔ **Never modify the master template.** Read it, export a copy, work on the copy. The
master is shared across every O-1 case in the office.

### Two things about this template that will bite

1. **It is an O-1B template.** It quotes `8 CFR 214.2(o)(3)(v)` (motion picture and
   television) and its criteria are the O-1B six. For an **O-1A** case the entire
   regulatory frame has to be swapped — see Step 2 — not just the criterion text.
2. **It already contains three different beneficiaries' names**: `Rui Qiu`, `Ms. Zhou`
   and `Ms. Jiarui Guo` appear in the same document, along with `one of the leading
   designers`, `the motion picture industry`, and `Sandra Ren Shan Chen` as petitioner.
   These leak into the draft. This is where `Ms. Rui Qiu` and `Ms. Jiarui Guo` came from
   in a completed O-1A letter. Sweep them explicitly — see Step 3.

### Then, in order

1. **Copy the template into the client's own PL folder** (`2. Cover/PL/Index` inside the
   client's case folder) and rename it for the client. That copy is now *the* letter —
   see Step 5.
2. **Generate the bare skeleton**: every section present, every placeholder still visibly
   a placeholder, the correct regulation cited, argument bodies empty.
3. **Only then map the evidence onto it.** Walk the exhibit package, decide which criteria
   the evidence can actually carry, and delete the sections it cannot. Choosing criteria
   before reading the evidence produces sections that later have to be torn out.
4. Take the **INDEX OF EXHIBITS** and cover-page templates from the same folder so all
   three documents share numbering from the first draft instead of being reconciled later.

---

## Step 0.5 — Where the evidence comes from

The letter cites `[Exhibit N]`. Those exhibits do not exist yet when you start. They come
from four places, and the order matters.

### 1. The client's own intake folders — read these first

A case folder is laid out one folder per topic, and the client uploads raw material into
them. Real layout of an O-1A case folder:

```
<CLIENT>_O1A/
  0.PL/                       ← the letter, EXHIBITS, INDEX live here (Step 5)
  01_身份证明 ID Documents
  02_未来工作Offer Future Job Offer
  03_工会信 Union Letter
  04_奖项 Awards
  05_协会会员 Memberships
  06_新闻 Press Coverage
  07_评委 Judge & Reviewer
  08_原创贡献 Original Contributions
  09_学术发表 Publications
  10_组织重要角色 Critical Role
  11_高薪 High Salary
  12_合同和付款 Contract & Payment
  13_表格 Forms (I-129)
  推荐信/                      ← recommendation letters
  翻译材料/                    ← Chinese originals awaiting translation
  L1 Maintenance of Status/
  <案件方案>.pdf · <材料清单> · <信息采集表>.xlsx · Resume · LinkedIn
```

The numbered folders map to criteria. **Walk every one before writing.** What is actually
in `08_原创贡献` decides whether there is an original-contribution section at all.

### 2. The intake documents — read these second

`方案` (case plan), `材料清单` (materials checklist), `信息采集表` (intake form), the resume
and the LinkedIn export. These tell you what the case was scoped to prove and what the
client was asked to supply. A criterion in the 方案 with an empty intake folder is a
missing-evidence problem to raise, not a section to invent.

### 3. What you research and capture yourself — this is drafting, not prep

Intake folders hold what the **beneficiary** has. They almost never hold what the argument
also needs. **Researching a criterion is part of writing it.** For each criterion you
intend to argue, work out what the *regulation* needs proved that the client cannot prove
about themselves, then go get it: **search → verify → capture → number into the exhibit
package → cite.** In that order — never a sentence first.

**Critical role / important organization.** The client proves the role; you must prove the
*organization*. Search across these dimensions and keep what lands: headcount and company
size, user or student scale, revenue, funding and valuation, industry rankings,
accreditation, awards and honours, notable counterparties, listing/financing records, and
independent news coverage. For a university: enrolment, accrediting body (e.g. NASM),
US News ranking, annual public events, alumni distinction.

**Published material / press.** Each article needs its outlet's standing proved separately
(the `Fourth` move in Step 1). The firm keeps a **media-authority pack** — per-outlet
traffic argumentation plus captured evidence — at `1. General 培训` → `1. EB1A` →
`3. 新闻报道` (`1CplV_BVFX4Xi8QOinpoiOTFVDwF3-lVp`):

- `1.中文媒体流量论述以及证据` (`1hm9o2Q7nXM_hwueYiQRtS4a5lAkNJsmo`) — one folder per outlet:
  China Daily, Sina, Phoenix New Media 凤凰, Sohu, Tencent, People's Daily, CCTV, 网易,
  环球网, 中国网, 北青网, 大众网, 雅昌, ELLE, BAZAAR, ETTV, plus 纸媒 and 专业组织
- `2. 英文媒体流量论述以及证据` (`17p_prIRnIXDHOX1-oL4xs5jm4EyLIy8F`) — The Hollywood
  Reporter, LA Weekly, ArtDaily, Broadway World, Aesthetica, Film Daily, Times Union,
  XinhuaNet, Medium
- `3. SimilarWeb Overview` (`1s21kWPYj6ESe95IVjZYQHScWd3Q6Nr2L`) — where the traffic
  figures come from, with a walkthrough
- `4.案例` (`1xye_5M1bezEj0ess5trv1oR-Q8aQbdKM`) — worked exhibit examples

**Check the pack before researching an outlet from scratch** — if it is covered, reuse it.
Three rules apply to anything taken from it:

1. **Re-verify the evidence is real** and still says what the pack says it says.
2. **Read for adverse material on the same page** before citing (Step 4).
3. **Refresh the traffic numbers.** Rank and visit figures age; pull current SimilarWeb
   data rather than shipping a stale figure.

**Original contributions — the "widely adopted" half.** Originality is provable from the
work itself; *influence* is not, and the client's own materials never establish it. Go find
it across dimensions: third-party citations, independent adoption at other institutions,
invitations that followed publication, curricula or products implementing the method, and
practitioners with no relationship to the beneficiary doing the same thing. Evidence
already used to prove authorship **cannot** also prove adoption — Shenqi Cai's
不要再重复用上面的材料了 (Step 7).

**High salary.** ZipRecruiter, Indeed, Glassdoor for the exact title and metro, converted
to a single unit before comparing.

**Recommender credentials.** A conference programme or independent report naming their
title — a recommender's own letter cannot establish its author's standing.

**NIW — proposed endeavor.** The national-importance prong is carried almost entirely by
research you supply, not by the client: US government and agency reports, national policy
and strategy documents, industry and market reports, and federal funding priorities that
align with the specific endeavor. Build it outward from the endeavor.

⚠️ **When you are unsure whether a criterion needs outside research, ask mid-run** rather
than guessing either way. Silently skipping it produces a thin section; silently doing it
can burn hours on a criterion already covered.

Capture what you find as PDFs and number them into the package. Capture wide
(`--window-size=1600,2400`) or web pages lose their left margin; verify the capture is not
truncated before relying on it. The `skye-translate` skill carries the capture and
integrity-check procedure.

### 4. What the user hands you mid-conversation

URLs and files pasted into the chat while drafting. Treat these as first-class evidence:
capture, number, file and cite them like anything else — and check them for the same
defects (self-published PR, platform-authored content, adverse material on the same page).

### The order

0. Route by type; pull that type's template and its most recent same-type case (Step 0).
1. Read intake folders and intake documents.
2. Decide which criteria the evidence can actually carry. Drop the others.
3. List, per criterion, what the argument needs that the package does not have — and
   check the media-authority pack before researching any outlet from scratch.
4. Research it, verify it, capture it, number it into the exhibit folder.
5. Only then write.

Keep a `00 - SOURCES.md` per exhibit group recording, for each fact the letter asserts:
the fact, the file that proves it, and status ✓ / ○ / ✗ — plus every deliberate exclusion
and **why**, so nobody reinstates a claim that was removed for want of a source.

⛔ **Never write a sentence first and look for the exhibit afterwards.** Every claim that
went into a draft ahead of its evidence in this office later had to be removed: the
"62 Amazon's Choice products", the eMarketer attribution, the secondary-transaction
valuations. If the evidence is not in hand, the sentence does not go in.

---

## Step 1 — The skeleton

### Document level

```
<date>
USCIS / Attn: Premium I-129 O / P.O. Box 660090 / Dallas, TX 75265-0090

RE:          Petition for Non-immigrant Worker, O-1A Classification
PETITIONER:  <name>
BENEFICIARY: <name> (“Ms. <Surname>”)
FIELD:       <field>

Dear U.S.C.I.S. Officer in Charge:

<one sentence: what this letter supports and whose services are sought>
<ONE dense paragraph of achievements, with the numbers, ending “Collectively, …”>
<“With her distinguished track record …, Ms. X is recognized as one of the leading …”>

MAINTENANCE OF STATUS                       [Exhibit 1]
PROPOSED U.S. EMPLOYMENT / CONTRACT         [Exhibit 2]
CONSULTATION                                [Exhibit 3]
ANALYSIS OF THE O-1A EVIDENCE
    <quote the regulation, then: “Ms. X qualifies for O-1 classification under …”>
    Criterion #N …  (repeat; criterion exhibits start at Exhibit 4)
FINAL MERITS DETERMINATION
CONCLUSION
Sincerely, / Shenqi Cai, Esq.
<footnotes — used for source citations of outside facts>
```

⚠️ **The master template omits MAINTENANCE OF STATUS.** Real filed letters carry it, right
after the opening, and on a transfer / change-of-status case it is one of the most
important sections in the letter. Add it; do not wait for the template to remind you.

**The achievements paragraph is one paragraph, not three.** It names the original
contribution, the biggest numbers, the organizations, the media, and the authorship in a
single dense block, then closes “Collectively, …”.

### Criterion level

```
Criterion #N.  <DECLARATIVE sentence: “Ms. X has <done the thing the criterion names>”>

The plain language of this criterion requires evidence (1) …, (2) …, and (3) ….
[+ where the criterion has a known gloss: “Relevant factors for element N include …”]

Here, the Beneficiary satisfies this criterion because ….  Specifically,

First, <sub-argument>.                        ← plain lead paragraph
    1. <assertion sentence>                    ← numbered layer
        * [Exhibit X] <evidence>               ← bulleted exhibit layer

Second, <sub-argument>.
Third, <sub-argument>.

[In light of the above, <synthesis>.]          ← used on some criteria, not all
Therefore, Ms. <Name> has satisfied the requirements of 8 CFR 214.2(o)(3)(iii)(B)(N).
```

⚠️ **The heading is declarative, not a restatement of the regulation's words.** Write
`Criterion #7. Ms. Tao has been employed in a critical or essential capacity for
organizations and establishments that have a distinguished reputation.` — never
`Documentation of the alien's employment in …`.

**Three layers, and the middle one is easy to lose.** Lead sentence → **numbered**
assertions → **bulleted** exhibit citations. Writing a bold lead sentence followed
directly by a flat bullet list drops the numbered layer and does not match the house
format. Where an entity or outlet is being argued, it gets its own plain sub-heading
(`ByteDance Ltd.`, `Major Media #1 Entrepreneur Daily`) above its First/Second.

**Quote the exhibit.** The house style proves the “because” by reproducing the source’s
own words — `The original text states:` followed by the quotation — rather than
paraphrasing it. This is what makes the section auditable.

**List levels: the document you are editing governs.** Read its numbering definition and
follow it; never fake a level by typing "1." into a plain paragraph. For reference, the
filed Yuqian Tao O-1A letter renders as arabic `1. 2. 3.` at the numbered layer with `*`
bullets beneath, indents `left=720/1440`, hanging `360`; the `3. PL Template` master uses
`●` (numId 1, 3) and `-` (numId 2) at level 0 with `○` beneath.

### Exhibit numbering follows the sections, three levels deep

`Exhibit 1` status · `Exhibit 2` employment · `Exhibit 3` consultation · criterion
evidence from `Exhibit 4`. Within a criterion, each item is `N-M` and each item's own
supporting evidence is `N-M-K` — e.g. `5-1` the article, `5-1-1` the outlet's readership,
`5-1-2` its licence, `5-1-3` its awards.

### Published-material sections have their own inner template

Criterion #3 argues **one outlet at a time**. Each gets a plain sub-heading
`Major Media #N <Outlet>` and then a **numbered list of exactly four moves**:

```
Major Media #1 <Outlet>

1. First, the article is published in <outlet>, <one clause on what the outlet is>.
   See full article at Exhibit 5-1.
2. Second, the format of this article has all required elements: <Outlet>, “<Title>”,
   Author <Name>, <Date>[, Page N]. <Translation + translator’s certificate of accuracy
   is enclosed immediately before the original article.> Available at: <URL>
3. Third, the material is about the beneficiary and relates to her work in the <field>
   field, because:
       <what it reports about her>
       The original text states:
       “<verbatim quotation>”
       <one sentence tying the quotation back to her work>
4. Fourth, the published material qualifies as <a professional publication / major
   media>, because:
       * [Exhibit 5-1-1] <Label>: <readership / intended audience>
       * [Exhibit 5-1-2] <Label>: <licence, registration, institutional standing>
       * [Exhibit 5-1-3] <Label>: <awards, rankings, circulation>
```

Every item in move 2 must actually appear on the exhibit — **title, date and author are
what the regulation asks for by name.** If the page names only a 责任编辑 (responsible
editor) or a content supplier, say so accurately and flag that no author exists; do not
promote an editor into the author slot.

Outlets beyond the main three go into a **collection exhibit** introduced as “In addition
to the coverage in … discussed above, several other media outlets enclosed in Exhibit 5-4
have reported on Ms. X …”, then a numbered list, each entry carrying outlet, title,
`Author: <name>`, date and URL.

Criterion #3 in the filed Tao letter goes **straight from the last outlet to “Therefore”**
with no “In light of the above” paragraph.

---

## Step 2 — Cite the right regulation

| Filing | Criteria live at |
|---|---|
| **O-1A** (sciences, education, business, athletics) | 8 CFR **214.2(o)(3)(iii)(B)(1)–(8)** |
| **O-1B** (arts) | 8 CFR 214.2(o)(3)(iv)(B) |
| **O-1B** (motion picture / TV) | 8 CFR 214.2(o)(3)(v) — **what the template ships with** |

⚠️ **The commonest citation error in this office is leaving the template's O-1B citation
in an O-1A letter.** The template quotes `(o)(3)(v)` and closes every section with
`…(v)(B)(n)`. A completed O-1A letter in this office cited `(iv)(B)` eight times before it
was caught. When converting, change:

- the block quote under `ANALYSIS OF THE O-1 EVIDENCE`
- every `Therefore, … has satisfied the requirements of …` line
- the criteria themselves — the O-1B six are not the O-1A eight

Check every `Therefore` line before delivering.

---

## Step 3 — How I write these letters

This is my own established form for O-1 petition letters. It is not any one reviewer's
preference; apply it by default, and let a named reviewer's instruction override it.

### Bullet form

1. A **plain lead sentence** naming what is being shown — no bold group headers.
2. Each bullet: **`[Exhibit X] Source, Month Year:` → the facts → one closing sentence
   that ties them back to the claim**, using "demonstrates" / "confirming that".
3. A **one-sentence bridge** between groups of bullets, not a heading.
4. A **"Taken together"** paragraph before the section's "In light of the above".

State facts directly rather than naming the reporting outlet in-line ("JD.com's holiday
program brought together…", not "Cover News reported that…"). Keep quoted matter to short
phrases. Prune secondary examples rather than listing everything found. Prefer
"internationally" to enumerating countries in a conclusion.

### Ordering evidence within a sub-argument

Put the **general proposition first and the instances second** when both are available —
industry research states the pattern, campaigns instantiate it. Do not run two parallel
lists organised on different axes (one about *reach*, one about *the nature of the
practice*); the seam is visible and gets called out as 割裂. Where an arc is wanted,
`trend → scaled practice → international spread` works.

### Vocabulary discipline

Define the beneficiary's contribution **once**, in one taxonomy, and reuse those exact
words in the originality argument, in the adoption argument and in the conclusion. One
letter defined the same model three ways — four *actors*, three *departures*, four
*components* — and nothing downstream could echo the definition because there wasn't one.
Pick the version with verbatim source support and hold it.

### Condense

Draft long, then cut. Recurring instruction: 太长了 / 这里重点就几点. Say the thing once, in
the shortest form that keeps the exhibit citation. No meta-commentary about the argument
being made.

### Hard content rules

- **No Chinese characters anywhere in the letter.** Romanize every name, brand and outlet
  (康泽宇 → Kang Zeyu; 韩束 → Kans; 好欢螺 → HaoHuanLuo). Use a subject's published English
  name where one exists (Christy Chung, Michelle Yeoh, Jay Chou, Chris Lee).
- **One exchange rate, stated once, applied everywhere.**
- **One name for the field**, everywhere.
- **One romanization per person.** A source writing 童偉 surname-first as "Tong Wei" and a
  letter writing "Wei Tong" reads as two people to an officer.
- **Sweep the template's own leftovers before delivering.** Grep for `Rui Qiu`, `Zhou`,
  `Jiarui Guo`, `Sandra Ren Shan Chen`, `designer`, `motion picture`, `he/his`, and any
  `[bracketed placeholder]` still in the file.

---

## Step 4 — Audit the letter against the package

This is where the real errors are, and the client will find them if you don't.

### Every figure must trace to an exhibit

Read the exhibit, don't trust the draft. Real corrections from a completed O-1A:

| Draft said | Source actually said |
|---|---|
| "62 products 'Amazon's Choice' and five '#1 Best Seller'" | "numerous products" — **no counts exist** in any SEC filing |
| mobile matrix "400 million users", "100 million daily visits" | **320 million** users; **no** daily-visit figure |
| Glassdoor 90th percentile presented as met | 90th percentile is **above** the contracted rate |
| "exceeds the highest figure published by every source" | one source's 90th percentile exceeded it |
| `RMB 120,822,140  044` | **RMB 113,031,044** (2,208,904 + 822,140 + 110,000,000) |
| a figure attributed to eMarketer / SCMP / Statista | never captured; the figure is **TIME's** |

**Verify before declaring a gap, too.** Twice a "no source exists" call was wrong — the
client had the source in Drive. Search the package before saying something is unsupported.

### Claims that fail on their face

- **Entity names the evidence does not carry.** A letter said "ByteDance Ltd." five times;
  **no exhibit used any suffix** — the official site, CNBC, Reuters, S&P, TIME and HBR all
  write plain "ByteDance", and the appointment letter named no legal entity at all.
  Government filings distinguish **ByteDance Ltd.** (Cayman parent) from **ByteDance Inc.**
  (Delaware, US subsidiary); a beneficiary paid in RMB with PRC social insurance worked for
  neither. Use the name the evidence uses.
- **Self-referential evidence.** For "others in the field emulate her," letters written by
  her colleagues, articles *about her*, and interviews *with her* prove nothing. You need
  third parties with no relationship to her doing the same thing.
- **The petitioner's own officer is not an independent expert.** The petitioner's CEO under
  a heading "Experts in the field confirm…" is an RFE magnet.
- **Sources that are the subject's own PR.** A trade body republishing a company's press
  release is self-description. Platform-authored case studies republished by a research
  house are the platform's marketing — name the author in the letter rather than passing it
  off as independent research.

### Adverse material on the cited page

Read the whole page, not just the sentence you want. The article supporting "+15% first-day
close" also called the raise "**tepid**", "**66% below** target", after a "**52%
reduction**" in deal size, and disclosed a dispute that "could lead to litigation." That is
not a reason to drop the exhibit — it is a reason to **tell the attorney**, and to keep a
fallback ready (there: rest on the SEC filings alone).

Record every such finding in the exhibit's notes file, never silently.

---

## Step 5 — One document, in Drive, edited in place

### There is exactly one letter, and it lives in the client's PL folder

Create **one** document in the client's PL folder and write into it. From then on **edit
that document** — download, change, upload back to the same file id. Never `-72`, `-82`,
`-83-3`, `-84-3`, `out2.docx`, `out5.docx`. One case accumulated dozens of local drafts
while the only version that mattered was the one in Drive; the local pile created nothing
but chances to overwrite the client's work.

- **Download immediately before every edit.** The client and the reviewing attorney edit
  Drive directly; their copy is the live one.
- Keep at most **one** local working file, overwritten each round, purely as the staging
  buffer for the upload. It is a temp file, not a draft.
- Upload back to the **same file id**, with the mimeType in the same call.
- After uploading, re-download and verify: paragraph count, sections intact, comments
  survived, no Chinese characters.

### Two editing modes, and the trigger between them

| Phase | How to edit |
|---|---|
| **Before the reviewing attorney has seen it** | Edit the text **directly**. No tracked changes. It is still a draft; suggestion markup only makes it unreadable for review. |
| **After the reviewing attorney has reviewed it** | **Suggest mode (tracked changes) only.** Never overwrite reviewed text silently. |

The trigger is the first review, not the calendar. Once the reviewer has been in the
document, every later change is a suggestion until told otherwise.

**Set the revision author to the user's own name** (`Skye Sun`), not the firm's — a
suggestion signed "Lingtu Law Office" tells the reviewer nothing about who to ask.

### Mechanics that bite

- A new paragraph must mark **both** its runs (`w:ins`) **and its paragraph mark**
  (`w:pPr/w:rPr/w:ins`), or the change is half-tracked.
- A deletion converts `w:t` → `w:delText` inside `w:del`, and marks the paragraph mark
  `w:pPr/w:rPr/w:del`.
- **`paragraph.text` in python-docx ignores runs inside `w:ins`.** Verifying with it makes
  correct insertions look empty and once caused a rollback that deleted a whole paragraph.
  Walk `w:t` nodes directly:
  ```python
  ''.join(t.text or '' for t in p._p.iter(W+'t'))          # accepted view
  ''.join(t.text or '' for t in p._p.iter(W+'delText'))    # deleted view
  ```
- **Google Docs suggestions export as `w:sdt` content controls** tagged `goog_rdk_N`,
  wrapping `w:ins`/`w:del`. Comment anchors are wrapped the same way. Accepting means
  unwrapping the **`w:sdt` shell**, not just the `w:ins` — and a `w:sdt` holding neither is
  a comment anchor that must be preserved.
- Never delete a paragraph carrying `commentRangeStart` / `commentReference`.
- Upload with the mimeType in the same call or Drive stores it as `multipart/related` and
  nobody can open the file — see the `skye-translate` skill for the exact command.

---

## Step 6 — Numbering is a four-place change

Exhibit numbers follow the **order of first citation in the letter**. When a number moves,
four things change together, and missing one is what the client notices:

1. the **letter** (every `[Exhibit X]` and `[See Exhibit X]`)
2. the **INDEX OF EXHIBIT** docx
3. the **folder and file names**, local **and** in Drive
4. the **translation certificate**'s list of numbers

Renumbering is usually a permutation — stage through a temp directory so two folders never
collide. Afterwards, re-scan the letter for stale numbers and confirm every cited number
resolves to a real folder.

Filenames must survive the USCIS upload portal: **letters, digits, `_`, `-`, `.`, `()`,
spaces only**. No commas, curly quotes, em dashes, or Chinese.

---

## Step 7 — Processing a reviewing attorney's review

1. **Read the full comment text** out of `word/comments.xml` — the UI truncates, and the
   instruction is usually in the truncated half.
2. **Accept the wording edits first**, in one pass, and study them.
3. **Separate wording from argumentation.** A comment saying 这里换成客观的事实，不要再重复
   用上面的材料了 is an instruction to **replace** a bullet list, not to append to it.
4. When the reviewer writes **参考** and pastes a passage from another client's letter,
   follow its **structure and legal move**, not its words. Copying it verbatim gets sent
   back.
5. Rework, then report what changed and what you deliberately did not.

### Shenqi Cai's documented preferences

Taken from her actual tracked edits, not from impression. Apply these before she has to
make them again.

**Precision of legal relationship.** She tightens loose prepositions describing employment:
`during her … of <company>` → `during her **employment with** <company>` / `**at**
<company>`. Name the relationship, do not gesture at it.

**Exact referents, not vague quantifiers.** Where the facts name exactly two companies,
`each additional company` → `**the other** company`.

**Parallel series must actually be parallel.** In `…establish the baseline, identify the
departures, record her implementation, and characteriz**ed** the result` she deleted the
`-ed`.

**Track the governing language.** She inserted `mimicked` and `and similarly` so the
sub-heading reads `is being **mimicked and similarly implemented by others** throughout the
industry` — the phrasing USCIS uses for original contributions. Where a criterion has
standard language, use it rather than a paraphrase.

**Claim only the prong you are arguing.** When past salary was dropped from Criterion #8,
she cut `has commanded a high salary and` from the heading, leaving `Ms. Tao **will**
command a high salary or other remuneration for her services.`

**Leverage a prior USCIS adjudication as an admission — then prove it anyway.** Her largest
insertion, and the most transferable technique in the file:

> The fact that Ms. Tao's employment at iPower Inc. was authorized under L-1A inherently
> establishes USCIS' recognition of her as a member of executive or managerial capacity at
> the employer. Nevertheless, we provide below analysis and evidence in support of her role
> at the company, for the officer's convenience of reviewing this petition.

Whenever the beneficiary holds a status the agency already granted on findings that overlap
a criterion — L-1A manager for critical role, an approved O-1 in the same field — open the
sub-argument by saying so, then say `Nevertheless, we provide below…`. Assert the
admission; never rest on it.

**Cite the enabling provision with its mechanism, not just its number.** For a gap in
employment she wanted `8 C.F.R. § 214.1(l)(2)`, the 60-day period, `or until the end of her
authorized validity period, **whichever is shorter**`, the computed end date, and the
statement that the petition is filed within it.

**Say it positively.** Not `Ms. Tao is not considered to have failed to maintain her L-1A
status`, but `Ms. Tao has maintained valid L-1A status throughout this period`. Do not
stack negatives, and do not recite the regulation at length once cited.

**Objective facts over recycled ones.** `不要再重复用上面的材料了` — evidence already used to
prove authorship cannot also prove that unrelated parties adopted the work.

---

## Step 8 — FINAL MERITS DETERMINATION and CONCLUSION

### In an O-1 letter this is a short passage, not a section

O-1 has no formal *Kazarian* two-step, so there is no free-standing final-merits analysis
to write. It is a handful of tight paragraphs that stand the whole record up at once and
land on **top of the field**. Do not re-argue the criteria here and do not re-cite every
exhibit — the reader has just read them.

### Shape

```
FINAL MERITS DETERMINATION

<Totality sentence>   The totality of the evidence demonstrates that Ms. <Name>
                      possesses extraordinary ability in <field>, with sustained
                      national and international acclaim.

<Duration + the one original thing>   one sentence of span, then the contribution and
                      its number.

<Critical roles>      the organizations and what she delivered there.

<Everything else, in one sentence>    media recognition, authorship, salary — named,
                      not itemized.

<Top-of-the-field close>   an independent voice concluding she belongs among the small
                      percentage at the top of the field.

CONCLUSION

The information above and the documentation herein clearly establish Ms. <Name>'s
qualification for a grant of O-1 visa status as an "Alien of Extraordinary Ability".
Thank you for your anticipated attention and consideration in this matter.

Sincerely,
```

The opening and closing sentences are template boilerplate — keep them. The template also
offers `…meeting the standard of extraordinary ability under INA §101(a)(15)(O)(i) and
8 CFR §214.2(o)` as the close; use it when no independent voice is available to close
instead.

### Rules learned writing this passage

- **The activity span is one sentence, not a timeline.** Compute it from the earliest
  record in the package and state it once: `For more than six years, Ms. Tao has produced
  distinguished results across China and the United States.` Do not list the years, and do
  not walk through each engagement — that instruction came back twice as
  还是太长了 / 一句话说她持续在领域里优秀 x 年就可以了.
- **One number, the biggest one, already proven above.** The final merits carries the
  headline figure (`more than RMB 113 million (approximately US$16.87 million)`), not the
  breakdown.
- **Name the criteria in a single clause.** `Her achievements have received substantial
  media recognition; she has authored three peer-reviewed articles; and her prospective
  compensation is significantly higher than that of comparable professionals.` One
  sentence for three criteria.
- **Give the top-of-field conclusion to someone else.** Close on a recommender who says
  it, rather than asserting it in the firm's own voice — the letter used
  `Its CEO, William August (See Exhibit 9), concludes that she belongs among the small
  percentage of professionals at the top of the field.`
- ⚠️ **If that voice is the petitioner's own officer, say whose it is.** The example above
  is the petitioner's founder and CEO, which is exactly the reliance an officer discounts.
  Where an unconnected expert letter exists, close on that one instead; where it does not,
  fall back to the template's INA/CFR close rather than dressing up an interested party as
  independent.
- **No new evidence appears here.** Anything cited in final merits must already have been
  argued and cited above; `See Exhibit N` is a back-reference, never a first appearance.

---

## Finish by reporting

- what changed, section by section, and what is still pending in suggest mode
- **every figure that did not match its exhibit** — the attorney needs these most
- every claim removed for lack of a source, and why, so nobody reinstates it
- what is cited but missing from the package, and what is in the package but uncited
- open questions that need the client's decision, each with your recommendation
