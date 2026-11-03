# 解读+策略 formatting conventions

Read off the Jian Wang analysis (run-level inspection of the exported .docx, Sept 2026).
`scripts/build_jiedu.py` implements all of this; this file explains what it does and why,
so you can tell whether a document came out right.

Base font is **Arial 11** (Google Docs default) — this is an internal working document, not
a filing, so it does not use the firm's Times New Roman letter typography.

## Colors carry meaning — use them sparingly or they stop working

| Formatting | Markup | Used for |
|---|---|---|
| **Black bold** | (automatic on labels) | Document title, criterion headings, the field labels `我们交的：` `RFE 原文：` `翻译：` `解读：` `应对：` `⚠️ 待核实：` |
| **Red bold** | `**text**` | The single operative sentence in each RFE quote — the clause that actually decides the objection. Also `File Date` and `DDL` at the top. |
| Red plain | `~~text~~` | Secondary emphasis: the specific words being complained about, and action verbs in 应对 (e.g. `改business Plan`) |
| Blue | `<<url>>` | Drive links to evidence folders |
| Plain black | — | The bulk of the quote, the whole translation, and the 解读 / 应对 prose |

In the Jian Wang document there were **12 red-bold runs across a 16-page notice** — roughly
one per objection. That ratio is the point. Red bold is how the attorney finds, in five
seconds, the sentence she has to beat. If half the quote is red, none of it is.

## Structure

```
<Client> RFE 解读+策略          ← black bold
File Date：MM/DD/YYYY            ← red bold
DDL：MM/DD/YYYY                  ← red bold
(blank)
评审认可✅                        ← black bold; the concession, at the top where it is seen

<Criterion heading>              ← black bold; use the RFE's own section name
我们交的：…                       ← optional, one line
RFE 原文：<quote, operative sentence in red bold>
翻译：<Chinese, paragraph by paragraph, interleaved with the quotes>
解读：1）…；2）…；3）…             ← one paragraph, numbered inline
应对：                            ← label alone on its line
1）…                             ← separate paragraphs, numbered in parallel with 解读
2）…
⚠️ 待核实：                       ← only when something could not be confirmed
- …

需客户提供                        ← black bold; once, at the very end of the document
● <what is needed>　——　<which objection it answers>（<who produces it>）
```

Where the RFE recites what was filed as a bulleted list ("You have provided: …"), keep it
as a bulleted list — a `{"list": [...]}` block.

Where a quote runs long and is broken into several paragraphs, alternate quote-paragraph
then translation-paragraph rather than stacking all the English and then all the Chinese.
The client reads them as pairs. Set `"continued": true` on follow-on blocks so the builder
does not repeat the `翻译：` label.

## Why 解读 and 应对 are numbered in parallel

`解读 1）` states an objection; `应对 1）` answers it. Same for 2）, 3）, and so on.

This is the load-bearing property of the format. It makes an unanswered objection visible
at a glance, and when the Response is drafted later each numbered pair converts directly
into a sub-argument. Breaking the correspondence — three 解读 points and five unnumbered
应对 paragraphs — costs the reader the ability to check coverage, which is most of what the
document is for.

## Naming

File name and document title both read `<Client> RFE 解读+策略`, placed in the case's RFE
folder. Older cases may use `<Client> RFE 分析解读`; if a document already exists, keep its
name rather than renaming it out from under whoever is working in it.
