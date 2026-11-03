---
name: "skye-rfe"
description: "Draft an RFE or NOID response for a Lingtu Law / SIA 高徒 filing. Covers locating the client's case folder and RFE folder in Drive, page-mapping the notice, reading the firm's internal 解读+策略 analysis (produced by skye-readrfe) and the original petition letter, verifying the governing law fresh, building the two deliverables (the Response letter and a separate INDEX OF EXHIBIT), the firm's verified numbering scheme and typography, dense bolding of key facts, 蔡律师's language rules, continuing exhibit lettering from the original filing, mirroring exhibits as Drive folders, the ability-to-pay playbook, and the diff-before-write rule that keeps Skye's own Drive edits from being overwritten. Use whenever asked to respond to an RFE or NOID, to write or revise a Response, to build the exhibit package for one, or to act on review comments on one. Petition letters are drafted differently and have their own skills."
---

# RFE / NOID Response Drafting (Lingtu Law / SIA 高徒)

**Scope: responses to a Request for Evidence or Notice of Intent to Deny.** Petition
letters get `skye-petition` (O-1) or their own skill. A Response is *not* a rewritten
petition letter — see Step 4.

Two rules govern everything: **the letter answers the officer point by point, in his
order**, and **every assertion carries an exhibit number that says what the sentence
says**.

---

## ⛔⛔ Standing rule — never touch what Skye edited by hand

**This is the most important rule in this skill. She has had to say it three times.**

**Anything Skye has changed by hand in the Google Doc is final and is not to be modified,
reworded, reformatted, or reverted — ever, by any later action.** Not on the next
revision, not on a rebuild, not when a new instruction happens to land on the same
paragraph, and not because the original read better. Her edit is the baseline. Treat it
exactly as you would a reviewing attorney's tracked change: you may add around it, never
over it.

**Once a document has been through her hands, stop generating it wholesale.** Retire the
local builder for that document and make every subsequent change as a **targeted
paragraph edit** through the Docs API. On Xinyi Chen the generator reverted her header
block twice before it was retired; each rebuild silently undid work she had done minutes
earlier. A generator that is one edit out of date is a landmine, not a convenience — if
you keep one at all, sync her edits into it the moment you find them, and rename it
clearly when you stop trusting it.

The three ways this gets broken, all of which have already happened:

1. **Full-replace uploads.** A `.docx` or HTML upload overwrites the entire document and
   destroys her edits silently. Never upload without running the Step 9 diff first.
2. **Regenerating from the local builder.** The builder does not know about her edits.
   Prefer targeted edits; if you must rebuild, merge her edits into the source first.
3. **Editing a nearby paragraph.** When a new instruction lands on a paragraph she has
   already touched, **read that paragraph first**, keep her wording, and change only the
   specific thing the instruction asks for.

Match her characters **exactly**, including imperfect ones — a mismatched `("Ms. Chen”)`
quote pair, a `pp.` where you wrote `p.`, an italic fragment in a date, three asterisks
where you wrote one, a heading she unbolded. If something of hers looks wrong, **say so
and leave it**; never silently "fix" it.

If you cannot tell whether a passage is hers, **assume it is** and ask.

⛔ **Never full-overwrite a Drive document.** Skye and the reviewing attorney edit the
Drive copy directly. See Step 9 — read it before your first upload, not after.

---

## Step 0.0 — 每次动笔之前，先学一遍

**每次起草、每次大改都要重跑。** 两份东西，顺序不能反。

### 1. 读 `RFE Language` 库

Drive 文件夹 **`RFE Language`** — `1Ov6ceCqYvOHbZOFrCXvHbeDHR4zOkvef`
（在 `1. Training` → `Others` 下面）

所里按 criterion 攒下来的成文论证语言。**先看这次 RFE 打的是哪几条，把对应的那几份读掉**，
再去读 `Burden of proof` 那份 —— 它管所有条。

| 文档 | 什么时候读 |
|---|---|
| `Burden of proof, More than likely not` | **每次都读**，证明标准是所有论证的地基 |
| `Leading role ` | RFE 质疑 lead / starring / critical role |
| `Distinguished productions` | RFE 质疑 production / event 的 distinguished reputation |
| `Distinguisehd Organization ` | RFE 质疑 organization / establishment 的 distinguished reputation |
| `Major Media ` | RFE 质疑 published material 是不是 major media |
| `Recommendation Letter` | RFE 质疑推荐信的分量或独立性 |
| `COMPARABLE EVIDENCE：individual or group` | 要用 comparable evidence 时 |

这些是**语言范本**，不是可以整段搬进信里的填空题。学它的论证动作和措辞，落到这个客户
自己的事实上重写。整段照搬会被退回来。

### 2. 读蔡律师的语言与论证规则

`references/cai-language.md` —— **从头读完再动笔。**

第一部分是硬性语言规则（Step 6 是它的摘要）；第二部分是她逐案的原话，按 criterion 分好了目录。
写哪条就把那条的语录段落再看一遍。

---

## Step 0 — Find the case folder, then the RFE folder

Work inside the client's existing case folder in the shared drive
(`0AIXy3tjXMf-MUk9PVA`). Locate it by name before creating anything:

```bash
gws drive files list --params '{"q":"name contains '"'"'<Client>'"'"' and mimeType='"'"'application/vnd.google-apps.folder'"'"' and trashed=false","supportsAllDrives":true,"includeItemsFromAllDrives":true,"fields":"files(id,name,parents)"}'
```

The RFE work lives in its own folder inside the case (for a Schedule A case, under the
`Schedule A` subfolder). Verified layouts — both shapes exist, do not "correct" one into
the other:

```
0. RFE/                                   ← Xinyi Chen shape (preferred)
  RFE.pdf                                 ← the notice as received
  <Client> RFE 解读+策略                    ← internal analysis + plan (Google Doc, from skye-readrfe)
  Response/
    Response—<Client>                     ← the letter
    INDEX OF EXHIBIT — <Client>           ← separate document, never appended
    Exhibit/
      Exhibit H <criterion label>/ …      ← one folder per exhibit letter
```

```
<Client> RFE/                             ← Junshun Zhang shape (flat)
  Exhibit/  Index (sheet)  Index of Exhibit  <Client> - RESPONSE  Translation Certificate
```

Fuller cases also carry `RFE Letter.pdf`, `<Client>补材料清单`, `Followup/`, `推荐信/`,
`材料翻译/`, per-criterion collection folders (`奖项`, `原创贡献`, `重要组织`, `工资证明`),
`00.打包/` for the assembled package, and a signed G-28.

**Create only what is missing.** If `Response/` already exists, use it. Add a
`Translate Certificate` doc only when foreign-language evidence is actually enclosed.

---

## Step 1 — Page-map the notice before writing a word

The house style cites `See RFE at p. N` throughout, so you need real page numbers. RFE
PDFs are **scanned images with no text layer** — the Drive reader OCRs them but discards
pagination.

```bash
# pull the notice
gws drive files download --params '{"fileId":"<id>"}' -o rfe.pdf   # or download_file_content
# extract one image per page (poppler/pdftotext are NOT installed on this Mac)
python3 -c "
import pypdf,os
r=pypdf.PdfReader('rfe.pdf'); os.makedirs('pg',exist_ok=True)
for i,p in enumerate(r.pages,1):
    for im in p.images: open(f'pg/p{i:02d}{os.path.splitext(im.name)[1]}','wb').write(im.data)
"
for f in pg/*.tiff; do sips -s format png "$f" --out "${f%.tiff}.png" >/dev/null; done
```

Then **Read the PNGs** and write down which section falls on which page. Record the map
before drafting; every `See RFE at p. N` depends on it. Xinyi Chen's 12-page notice mapped
as: p1 cover letter · p2 advanced degree · p3 Prong 1 · p4 Prong 2 + awards · p5 awards
asks + membership · **p6 published material = CRITERION MET** · p7 authorship + exhibition
heading · p8 exhibition + summary + ability to pay · p9 ability to pay · p10 coversheet.

**Read the whole notice, including the concessions.** What USCIS *granted* is the most
valuable thing in it and must be quoted back (Step 5).

---

## Step 2 — Read the record, in this order

1. **`<Client> RFE 解读+策略`** — the firm's internal analysis, produced by the `skye-readrfe`
   skill. Skye's plan for the case is here, and
   it often contains 蔡律师's directives for that specific case.
2. **The original petition letter** and its **INDEX OF EXHIBITS** — you must know the
   existing exhibit series (Step 8) and exactly what was already filed.
3. **The client's collection folders** — what is actually in hand versus what the 策略
   assumed.
4. **Apple Notes `蔡律师案子语录` and `KK案子语录`** — dictated drafting rules, and
   sometimes case-specific instructions. Read them with `osascript -e 'tell application
   "Notes" to get body of ...'` and strip the HTML.

⛔ **Do not read other clients' letters on your own initiative** beyond what this skill
already distils, unless Skye names one.

---

## Step 3 — Verify the governing law fresh

⚠️ **uscis.gov returns 403 to WebFetch.** Use the Browser pane
(`preview_start` with the URL, then `get_page_text`).

| Filing | Criteria live at |
|---|---|
| EB-1A | 8 C.F.R. § 204.5(h)(3) |
| EB-2 NIW | INA § 203(b)(2)(B); *Matter of Dhanasar*, 26 I&N Dec. 884 (AAO 2016) |
| **EB-2 Schedule A, Group II** | **20 C.F.R. § 656.15(d)(1)**; 20 C.F.R. § 656.5(b); **6 USCIS-PM E.7** |
| O-1A / O-1B | 8 C.F.R. § 214.2(o)(3)(iii)(B) / (iv)(B) / (v) |

### Schedule A, Group II — authorities worth their weight (verified 8/2026)

- **6 USCIS-PM E.7(G)(2)** — *"officers should take care not to erroneously apply the
  standard for the EB-1A category to a request for Schedule A, Group II designation."*
  Also locates the position's true minimum requirements in **Item H of ETA Form 9089**,
  which is how you answer a job-posting inference.
- **6 USCIS-PM E.7 n.49**, *Matter of Allied Concert Services, Inc.*, 88–INA–14 (BALCA
  1988) — the seven groups are *"suggested as possible methods of proof"*; the ultimate
  fact is exceptional ability *"as compared with others in the same field."*
- **6 USCIS-PM E.7 nn.47, 50**, *Matter of Chawathe*, 25 I&N Dec. 369, 376 (AAO 2010) —
  *"truth is to be determined not by the quantity of evidence alone but by its quality."*
- **6 USCIS-PM E.7(E)(2)**, *Love Korean Church v. Chertoff*, 549 F.3d 749, 758 (9th Cir.
  2008); *Kazarian v. INS*, 596 F.3d 1115, 1121 (9th Cir. 2010) — officers *"may not
  unilaterally impose novel substantive or evidentiary requirements beyond those set forth
  in the regulations."* Kills tier requirements and posting-notice inferences alike.
- **20 C.F.R. § 656.10(d)(3)** / **6 USCIS-PM E.7(D)(3)** — the Notice of Filing's required
  contents are job description, rate of pay, and the DOL Certifying Officer's address. It
  is a notice to employees, **not** a statement of what the work requires.
- Group II allows **no comparable evidence** (6 USCIS-PM E.7 n.61), and **no
  self-petition**. There is **no final-merits determination** for Group II — the Policy
  Manual describes none, so do not import the EB-1A framing.

For EB-1A final merits, the firm's full APA attack (*Kazarian* → *Mukherji v. Miller*, No.
4:24-cv-3170 (D. Neb. 2024) → 5 U.S.C. § 706(2)(A) → *State Farm*, 463 U.S. 29, 43) plus
the "*sustained* has no statutory duration" argument lives in the Junshun Zhang NOID
response. Always follow it with *"even assuming arguendo…"* and win on the record too.

---

## Step 4 — Two deliverables, and what a Response is

| Document | Notes |
|---|---|
| **The Response letter** | Answers the RFE point by point |
| **INDEX OF EXHIBIT** | **Its own document.** Never a section of the letter. |

蔡律师 on what a Response is: **对话/辩论，不是重写 PL** — "先说移民官指出什么，我们回答什么."
Do not drop in a template. If the RFE did not question something (benefit to the U.S., the
proposed endeavor, prevailing wage, Notice of Filing), **do not argue it** — 有点此地无银 —
just note the concession in the Summary and the Conclusion.

### Letter skeleton

```
<date>
USCIS/TSC · Attn: RFE/NOID/NOIR/NOIT · 6046 N Belt Line Rd. STE 140 · Irving, TX 75038-0014
***PREMIUM PROCESSING***
RE:                     Immigrant Petition for Alien Worker
Petitioner:             <name>
Beneficiary:            <name> (“Ms. <Surname>”)
Type of Petition:       I-140
Classification Sought:  <INA cite + classification>

Dear Officer:
<fixed opener: "On behalf of our client …, we hereby submit this Response to the USCIS
 Request for Evidence dated <date> (the “RFE”). Our Response to this RFE is being filed
 timely ahead of the deadline of <date>.">

SUMMARY OF THE RFE                      ← A. B. C. … list
<Policy Manual "not at issue" boilerplate>
THE APPLICABLE STANDARD                 ← only where the officer used the wrong yardstick
ANALYSIS OF THE <classification> EVIDENCE
  I. … II. … III. …                     ← one per requirement
     A. B. C.                           ← criteria / groups
CONCLUSION
Respectfully submitted, / Shenqi Cai, Esq. / Law Office of Shenqi Cai, APC
```

The **"not at issue" boilerplate**, verbatim, after the Summary:

> According to the USCIS Policy Manual (*Volume 1, Part E, Chapter 6, Section F,
> Subsection 3*), Requests for Evidence must "identify any missing evidence specifically
> required by the applicable statute, regulation, or form instructions" and "ask for all
> the evidence the officer anticipates needing to determine eligibility." **Based on this
> policy, elements not questioned in the RFE are considered sufficiently supported and
> thus not at issue.**

### Per-criterion shape

```
<criterion heading, restated with the beneficiary's name>      ← A. B. C.
The plain language of this criterion requires evidence (1) …, (2) …, (3) …, (4) ….
Here, Ms. X satisfies this criterion because ….
[Where the RFE conceded elements:] The RFE has resolved three of the four elements in the
Petitioner's favor: … The sole issue in concern is element (4), which the Petitioner
addresses below.

First, <sub-argument>.                                          ← bold plain paragraph
    <assertion>                                                 ← i. ii. iii.
        [Exhibit X] <source, date:> facts → closing clause      ← ○
    <quoted passage>                                            ← own indented italic para

Taken together, <recap with the hard numbers>.
In light of the above, <synthesis>. Therefore, Ms. X has satisfied the standard of <cite>.
```

Evidence bullets follow **`[Exhibit X] Source, Month Year:` → the facts → one closing
clause tying them to the claim**, using "demonstrating that" / "confirming that".

---

## Step 5 — The strategy that wins these

**Count first.** Before arguing anything, work out how many criteria the regulation
actually needs and how many the RFE already conceded. Xinyi Chen: Group II needs **two of
seven**, and the RFE said of published material *"Accordingly, this criterion has been
met."* → **only one more group was required.** Lead with the conceded group, then the
easiest remaining one, and treat the contested one as a bonus that cannot sink the case.
蔡律师: **RFE 认的东西，一定要清晰的点出来.**

**Reframe before you pile on evidence.** Each objection hides a definition the officer
invented. Recite the regulation's plain language first to take the yardstick back, *then*
put evidence against it.

**Be selective.** 奖项的论述，可以多方面，做取舍，没有的不用硬说. On Xinyi Chen the three
IAA awards (French Fashion, Muse, NY Product Design) were **cut** — same organizer, same
pay-to-enter model, so pushing them would have let the officer generalize the fee
objection back onto the A' Design Award that he had already conceded was internationally
recognized.

**Evidence the officer overlooked** — handle it **inside its own criterion, low-key**. No
standalone "record clarification" section: 挑衅意味太强. Write *"Evidence of the degree was
submitted with the initial petition as Exhibit G-1 … and is re-tabbed here for the
officer's convenience,"* or *"the Petitioner respectfully directs the officer to Exhibits
F-6 through F-8-2, submitted with the initial petition."* Wei Hu's letter has the sharpest
permissible register: *"much of the 'missing evidence' referenced in the RFE was already
provided, but may not have been fully considered."*

**Concede the irrelevant, hold the essential.** Wenrui Shi on an award won while a
student; Sara Hua conceding DOL has no matching SOC code and winning on the high benchmark
anyway; Wei Hu conceding a translation-certificate defect and curing the form.

**Read the officer's own document in full — the rebuttal is usually inside it.** When the
RFE quotes a document to make a point, pull that document and read the whole line, the
whole page. On Xinyi Chen the officer wrote *"the job posting shows that no work experience
is required. Therefore, it appears that the beneficiary's job does not require exceptional
ability."* The posted notice's requirement line actually reads **"At least a Master's degree
in Fashion Design … or related field. No work experience required."** — he quoted the second
sentence of two — and the same one-page notice lists nine job duties. The RFE even conceded
the document *"included details and information about the beneficiary's job opportunity."*
Do **not** argue that the officer's document is irrelevant when the document is on your
side; embrace it and read it back to him. Then look for a **second government document in
the same filing** that scored the same facts: here the ETA-9141 PWD put the position at
**OEWS wage level II, not level I**, and says on its face the wage "is based on the minimum
job requirements for the position" — DOL ran the officer's own premise and got the opposite
answer. Resubmit both under new exhibit letters so he physically has them.

**⛔ Read the current state of Drive before you write to it.** On Xinyi Chen the exhibit
folders were reported as "still empty" from a directory listing taken hours earlier — Skye
had since built them out, with subfolders and better filenames carrying `(previously
submitted as Exhibit F-6)` provenance. Thirteen duplicate files got copied in on top of her
structure, and an "delete the empty placeholder folders" step nearly took her originals with
them. Before any copy, rename, move or delete: **list the target folder and every subfolder,
and confirm what is actually there.** A folder that looks like an empty placeholder by its
name may be the real thing. This is the same rule as the one below, extended from citations
to file operations: never act on a remembered state, only on a state you just read.

**⛔ Never cite an exhibit you have not opened.** Twice on this case a document was described
in the letter before anyone confirmed it existed or said what was claimed. Before any
`[Exhibit X-N] …:` line ships, open the file and read the sentence you are about to quote.
Two specific traps: the **2023 ETA-9089 has no "Item H"** (the Policy Manual's phrasing is
written against the old form; job requirements now live in Appendix A, and Appendix A of a
Schedule A filing is the *beneficiary's* education, not the job's), and a **"Final
Determination" 9089 PDF is a blank signature form** with no job content at all. Quote the
Policy Manual's words if you need them; do not assert what the form says.

**Every number gets a benchmark and a multiple.** 裸数字不合格. Citations vs. the Clarivate
ESI field baseline; salary vs. BLS median, 90th percentile and DOL Level IV; selectivity as
a percentage ("top 10% to 20% of more than 91,743 submissions from over 180 nationalities").

---

## Step 6 — Language rules (蔡律师)

**完整版在 `references/cai-language.md`，Step 0.0 已经读过。**
下面是写的时候摆在手边的摘要。

- **Never attribute conclusiveness to the RFE.** No "determined", "concluded", "found
  evidence insufficient". Use **"suggested"**, "noted", "observed".
- **Never name a defect the RFE did not raise** — 不要自己给自己扣帽子.
- `etc` → **`among others`**; `documentary` → **`established`**; `expressed, documentary` →
  **`explicit, documented`**.
- Quote only the useful part of adverse material.
- Threshold-error opener where the RFE rests on a mischaracterisation: *"However, before
  addressing these specific concerns, we must first clarify the two fundamental
  mischaracterizations at the core of this RFE: (1) … (2) …"* → close with *"With these
  threshold mischaracterizations clarified, we now turn to …"*
- Three-layer rebuttal: no industry discrimination → industry reports that the role/field
  matters → the client's own documentary evidence.
- Award field is not set by its title — examine entry eligibility, evaluation criteria,
  past winners.
- Exhibition criterion always centres on the **exhibition**; the venue is supporting
  weight only. Define both.
- Recent achievements are not absent acclaim — reaching this level so soon proves the
  ability; compare against same-age, same-tenure peers.
- **No Chinese characters in the letter.** Romanise every name; one romanisation per
  person; one name for the field throughout.

---

## Step 7 — Format: numbering, bolding, typography

### Numbering — read it out of a real letter, never invent it

⚠️ Exporting a firm letter to Markdown **flattens every numbered heading to "1."**, which
makes the scheme look flat. It is not. Export to `.docx` and read `word/numbering.xml`:

```bash
gws drive files export --params '{"fileId":"<example letter>","mimeType":"application/vnd.openxmlformats-officedocument.wordprocessingml.document"}' -o example.docx
```

Verified scheme (Wenrui Shi, 8/2026). **`ilvl 0` all sits at `left=720`; the tier is
signalled by the numbering format, not by deeper indentation:**

| Tier | numFmt | ind |
|---|---|---|
| RFE summary items | `upperLetter` A. B. C. | left 720, hanging 360 |
| Major section heading | `upperRoman` I. II. III. | left 720, hanging 360 |
| Criterion heading | `upperLetter` A. B. C. | left 720, hanging 360 |
| Assertion | `lowerRoman` i. ii. iii. | left 720, hanging 360 |
| `[Exhibit X]` evidence | bullet `○` | left 1440, hanging 360 |
| Standalone evidence list | bullet `●` | left 720, hanging 360 |
| Sub-evidence | bullet `■` | left 2160, hanging 360 |

Reusable abstractNumIds in that file: **21** upperRoman/upperLetter/decimal · **24** and
**31** upperLetter/○/■ · **13** lowerRoman/○/■ · **11** lowerRoman/●/■ · **3** ●/○/■.

**Build the letter as a `.docx` using an example letter as the template**, copying its
`numbering.xml` and adding fresh `<w:num>` entries pointing at those abstract ids (one per
list instance that must restart). The Google Docs API cannot express level-0 `lowerRoman`
— its `createParagraphBullets` presets do not include it — so HTML upload and batchUpdate
both approximate. Strip the template body, keep `sectPr`, write your paragraphs, upload the
`.docx` to the existing doc id and let Drive convert.

⚠️ If you ever do go through HTML: multiple `<p>` inside one `<li>` are **silently
collapsed** (heading merges into body, intervening paragraphs vanish), and nesting `<ol>`
inside `<li>` pushes evidence to level 2–3. Verify with the Docs API afterwards and print
each paragraph's `bullet.nestingLevel`.

### Bolding — dense, not decorative

40% of runs bold is the house register. Bold **every** hard number, name, institution,
date, statutory cite, the operative clause inside each quotation, and every `Therefore …`
conclusion. Exhibit labels are bold through the colon:
`**[Exhibit J-1-4] Awards and Industry Leadership:**`. Italics for case names, journal
titles, work titles and quoted passages.

### Typography

Times New Roman · 12 pt · line spacing **1.15** · **space after paragraph** (6 pt / 120
twips), **no blank paragraphs between paragraphs** · body flush left, no first-line indent
and no leading spaces · headings indented by tier · block quotations on their own
paragraph, whole paragraph indented one tab (720 twips / 0.5") and italic.

Also set `docDefaults` and the `Normal` style to Times New Roman 12 — the firm's template
ships **Arial 11**, so paragraph marks and anything typed later inherit the wrong font.

---

## Step 8 — Exhibit lettering, the index, and Drive folders

**Continue the letter series from the original filing.** Xinyi Chen's petition used A–G, so
the response starts at **H**. **`I` is not skipped** — Sara Hua's response uses
`Exhibit I`.

**One letter per criterion, not per document type.** The letter-group header restates the
criterion as a sentence naming the beneficiary; sub-items run `-1, -2, -3 …` continuously
within the letter even across several awards; sub-item labels read
`<object>: <what it proves>`.

```
Exhibit H.  Ms. Chen is a member of the professions holding an advanced degree
H-1  Proof of Advanced Degree: Diploma, …
H-2  Official Academic Record: Transcript, …

Exhibit J.  Ms. Chen’s receipt of internationally recognized prizes or awards for excellence …
J-1  A’ Design Award: Criteria of Excellence — <article>, Design Studies, Vol. 45 (2016)
```

Re-tabbing previously submitted evidence under a new letter is accepted practice — note the
old number in parentheses (`previously submitted as Exhibit F-6`). In the letter body, cite
record evidence as **`[See Exhibit X, previously submitted]`**.

**Mirror the letters as Drive folders** inside `Response/Exhibit/`, named
`Exhibit <letter> <short criterion label>` (space, no dash — `Exhibit 53 future Work`,
`Exhibit L Ability to Pay`). Filenames must survive the USCIS upload portal: **letters,
digits, `_`, `-`, `.`, `()`, spaces only** — no commas, em dashes, curly quotes or Chinese.

**Renumbering is a four-place change**: the letter, the INDEX document, the Drive folder and
file names, and the translation certificate's list. Afterwards, re-scan the letter for stale
numbers and cross-check every cited number against the index:

```python
cited  = set(re.findall(r"Exhibit[s]?\s+([A-Z]-[0-9]+(?:-[0-9]+)?)", letter_text))
listed = set(re.findall(r"\b([H-Z]-[0-9]+)\b", index_text))
# report cited-but-unlisted and listed-but-uncited
```

---

## Step 9 — ⛔ Diff before every write

Skye and the reviewing attorney edit the Drive copy directly; **their copy is the live
one.** A full-replace upload destroys their work silently. This happened on Xinyi Chen and
had to be caught after the fact — she had rewritten the whole `RE:` header block into the
petition-letter form, and a rebuild put the old block back.

**Before every upload:** pull the head, extract paragraph text, diff against the local
build, and treat any HEAD line you did not author as her edit. **Merge it into the
generator source first**, then rebuild, then diff again — the second diff should show only
the changes you intended. If the diff is empty, **do not upload at all.**

This is the mechanism that enforces the standing rule at the top of this skill. Run it
even for a one-line change: the diff is cheap and the failure is silent.

```python
# gws docs documents get -> paragraph text ; local .docx -> w:t AND w:tab
# (omit w:tab and tabs show up as phantom diffs)
sm = difflib.SequenceMatcher(None, local_paras, head_paras)
ops = [o for o in sm.get_opcodes() if o[0] != "equal"]   # non-empty => stop and review
```

Match their characters **exactly**, even imperfect ones (a mismatched `("Ms. Chen”)` quote
pair stays), and flag the imperfection rather than silently "fixing" it.

Recovering a lost edit: `gws drive revisions list --params '{"fileId":"…"}'` then
`gws drive revisions get` with `fields=exportLinks` — native Docs revisions are not
downloadable as media, so the export link needs the account's own token.

**Editing modes.** Before the reviewing attorney has seen the letter, edit text directly.
**After her first review, suggestions only** — never overwrite reviewed text — with the
revision author set to `Skye Sun`.

---

## Step 10 — Ability to pay (I-140 with a job offer)

**8 C.F.R. § 204.5(g)(2)** — ability to pay **as of the priority date** and **continuing
until permanent residence**, evidenced *"either in the form of copies of annual reports,
federal tax returns, or audited financial statements."*

Two openings the RFE hands you, both used on Xinyi Chen:

1. **The financial-officer option is capped.** It is available only where the petitioner
   *"employ[s] 100 or more workers."* Count the payroll register — Fore Collection had
   **37** — and say so; the tax return then becomes the only proper primary route, not a
   convenient one.
2. **A current-year return cannot exist.** USCIS routinely demands "2025 and 2026" returns
   mid-2026. Say plainly that the tax year has not closed and cite **8 C.F.R.
   § 103.2(b)(2)(i)** — secondary evidence is permitted where primary evidence does not
   exist or cannot be obtained. The P&L and payroll register are then submitted *"not in
   place of available primary evidence, but because primary evidence for 2026 cannot yet
   exist."* The RFE itself invites profit/loss statements and payroll records.

Then build it: **First**, the prior-year federal return (primary). **Second**, the
current-year P&L and whole-company payroll — check that the period **spans the priority
date**. **Third**, wages actually paid to the beneficiary through and past the priority
date, the annualised rate derived from the register (hours ÷ amount, cross-checked against
the employment verification letter), and the **differential** between actual and proffered
wage. Express net income as a multiple of both the proffered wage and the differential.
Close on totality under *Matter of Sonegawa*, 12 I&N Dec. 612 (Reg'l Comm'r 1967).

⚠️ A P&L is **cash basis and unaudited** — never call it primary evidence.

---

## Step 11 — Criterion playbooks

**Design awards.** Recite the four plain-language elements, then per award: **First**
receipt · **Second** in the field (category, judging criteria verbatim, media
confirmation, submission volume + nationalities + juror count, previous winners in the
sub-field) · **Third** internationally recognised (history and founder; global media
**broken out by country**; granting organisation and named jurors with institutions;
corporate winners announcing it themselves, top design schools citing their ranking,
governments listing it for high-level-talent status) · **Fourth** excellence was the basis.

**Beating a tier attack** ("your level says *A good design*, not *superior design*"): the
regulation requires an award *for excellence*, not the **highest** award, and does not rank
multi-tier schemes — reading in a top-tier requirement is exactly what *Love Korean
Church* forbids. Show the absurd consequence (every Bronze and Silver award, including
those held by listed companies, would fail). Then move off the label onto the **mechanism**:
selection threshold, pool size and nationality spread, jury size and named academics, and
peer-reviewed design scholarship establishing that the award's published criteria *are* the
field's dimensions of excellence — Self, *Mind the Gap*, Int'l J. of Design 8:3 (2014);
*Dimensions of Creative Evaluation*, Design Studies 45 (2016); *Assessing Design
Creativity*, Design Studies 32 (2011).

**Beating a pay-to-enter attack.** The regulation contains no fee exclusion; an entry fee
is ordinary across Red Dot and iF; requiring a submission is inherent in a competition.
What matters is independent conferral — the beneficiary did not create the award, appoint
its jurors, set its criteria, score her entry or confer it on herself. **Payment purchased
consideration of the work, not the outcome.**

**Beating a benchmark mismatch.** Concede the taxonomy gap and own it — *"DOL does not
maintain a discrete '<X>' category, so the closest standardized SOC comparator is <Y>"* —
win on that high benchmark anyway, offer a broader SOC as an alternative, add
seniority-matched third-party comparators each as its own small table with a
"% Difference from Beneficiary's …" column, and exclude whatever the RFE said not to count
while noting the exclusion.

**Beating a job-posting inference** (Prong 2 / Schedule A). Three moves: the Notice of
Filing's contents are fixed by 20 C.F.R. § 656.10(d)(3) and none concerns the ability the
work demands; a minimum entry requirement is the floor to *apply*, not a description of the
work, and 6 USCIS-PM E.7(G)(2) locates the true requirements in **ETA Form 9089 Item H**;
and the regulation asks what the work **requires**. ⚠️ 蔡律师's correction: quote the
employer on **what the job requires**, not on how good the beneficiary is — 这个 prong 2 要说
work "Require" exceptional ability，不是 "demonstrate" her exceptional ability.

**Curing a translation defect.** Standalone **Translation Statement** section: have the
original translator reissue a certification itemising every document and exhibit, then
*"this represents a formal improvement in compliance … and does not affect the probative
value of the underlying evidence or the merits of the case."*

---

## Finish by reporting

- what each section argues and which authority carries it
- **every figure that did not match its exhibit** — the attorney needs these most
- every claim removed for want of a source, and why, so nobody reinstates it
- exhibits cited but missing from the package, and exhibits in the package but uncited
- anything of Skye's you matched rather than corrected, and why
- open questions needing a decision, each with your recommendation
