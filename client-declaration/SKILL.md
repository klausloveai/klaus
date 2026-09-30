---
name: client-declaration
description: |
  Turn a client's factual account into ONE bilingual (English + 中文, side by side)
  Word document that the client can read, compare and SIGN — a statement plus a
  CCP § 2015.5 declaration, for 凌图律所 / Law Office of Shenqi Cai APC. Use whenever
  any of the following come up: client declaration, 客户声明, 客户陈述签字, declaration
  for the client to sign, 事实陈述书, statement for verification, 中英对照声明,
  "make this a declaration", "给客户签字确认", "/client-declaration". Typical
  invocation: an interview write-up, a recording, or an existing one-language client
  statement that now needs to be signed. It produces the timeline + narrative as
  two-language tables and a signature block per declarant, plus a Certificate of
  Translation for Mandarin-only clients. DRAFT-ONLY — never sent, never filed;
  Klaus reads the Chinese to the clients and they sign.
---

# client-declaration — bilingual client statement that can be signed

Born from Peiyun Zhou & Jian Wang (2026-09-30). Hernán had flagged two factual
conflicts in a client statement; correcting them turned the statement into something
the clients had to attest to, and the separate EN and CN files had to become one
signable document.

## What it produces

**One** `.docx` (+ PDF), never a pair of language files:

1. **I. TIMELINE / 一、时间轴** — 3 columns: `Time / 时间 | English | 中文`
2. **II. STATEMENT / 二、事实陈述** — 2 columns: `English | 中文`, paragraph for paragraph
3. **III. DECLARATION / 三、声明** — one block per declarant + Certificate of Translation

Build it with `scripts/build_declaration.py config.json`
(`references/example-config.json` is the Peiyun Zhou file, filled).

## The five rules (this is the skill; the formatting is just plumbing)

### 1. Personal knowledge only — strip everything else FIRST

A declaration carries only what the declarant saw, heard, did and felt. Before you
write a single row, delete:

- anything read off a **screenshot, file metadata or an app screen** ("the delivery
  screen still showed neither button pressed", "the metadata says 12:45")
- **agency record numbers, activity numbers, report numbers, filing dates** ("the
  Department opened Activity No. A26-677072 on August 19")
- anything the client learned **from us or from a document** rather than experienced

Every one of those lines draws the same deposition question — *how do you know that?* —
and the honest answer is *my lawyer told me*. That answer damages the whole document.
Those facts belong in the exhibits and in the attorney's letters, never in the
declarant's own words.

**Keep:** what they did, what they saw, what they were told at the scene, and **what
their own phone recorded in their presence** (a time shown in the Photos app is fine —
the client saw it; a time pulled out of the file's metadata by us is not).

Rewrite record-sourced sentences into the client's own experience where you can —
"Animal Services opened the file on August 19" becomes "Animal Services became involved
after a social worker at the hospital contacted the Department."

### 2. First person, in BOTH languages

Statements drafted for the attorney are often third person ("Zhou walked down to the
residence"). A signed declaration cannot be. If the English is third person and the
Chinese is first person, the signer is attesting to two different documents. Convert
both sides to first person before you add a signature block.

### 3. One document, side by side — never two files

The client compares the columns; the attorney reads one side; there is exactly one
thing to sign. Separate `(EN)` and `(CN)` files invite a client signing the language
they cannot read, and they drift apart on the next revision.

### 4. One block per declarant, scoped to what THAT person knows

The narrative is written in one person's voice. A second declarant does **not** sign a
first-person narrative belonging to someone else. Give them their own short block
naming the facts within their knowledge:

> *"The facts stated in it **that concern me** are within my own personal knowledge and
> are true and correct. In particular, I was driving on August 17, 2026; I went to my
> wife's aid; both dogs bit me; and I am the person who recorded the video."*

### 5. Certificate of Translation whenever the client does not read English

Mandarin-only clients signing a bilingual document will be asked whether they could
read what they signed. The certificate is signed by **whoever actually read the Chinese
aloud to them** — not automatically Klaus. Leave the name blank if that person isn't
settled yet. See [[discovery-translation-zh]], which carries the same requirement for
discovery verifications.

## House formatting

- **No colour coding, no highlighting, no internal annotations.** Working drafts may use
  shading to mark which facts are independently anchored; a signed declaration must not —
  opposing counsel will ask what the colours mean, and the answer implies some facts are
  better sourced than others. (Dropped from the Peiyun Zhou draft for exactly this reason.)
- **Chinese runs = SimSun (宋体)**, set on `w:ascii/hAnsi/eastAsia/cs`. The script does it.
- **Leave the date and the place of execution BLANK** — filled in at signing, in the
  client's own hand. Same for the case number if the complaint isn't filed yet.
- Perjury wording is fixed and must not be paraphrased:
  *"I declare under penalty of perjury under the laws of the State of California that the
  foregoing is true and correct."*
- Client and case names stay in English throughout ([[feedback-client-names-english]]);
  the Chinese column may carry the client's Chinese name where the client's own voice
  requires it.

## Before you hand it over

Read the finished tables against the source one more time and flag to Klaus anything the
client should be asked to confirm **out loud** before signing — numbers that came from two
different places (a route stop number vs. "the 75th delivery"), a start date that changed
between drafts, a provider name still missing. A declaration is the wrong place to discover
a discrepancy.

## Guardrails

- **DRAFT-ONLY.** Never email it, never file it, never attach it to anything. Klaus reads
  the Chinese to the clients; they sign; then it is archived and produced.
- **No fabrication.** If the client never said it, it does not go in — not even an obvious
  inference. Missing facts stay missing and get flagged.
- File the signed original to the case folder's `1. Incident & Liability`; mark superseded
  drafts `(SUPERSEDED)` rather than deleting them if a version was already sent out
  ([[feedback-always-file-to-case-folder]]).

Related: [[complaint-client-translation]] (the complaint itself, for client review before
filing) · [[discovery-response]] / [[discovery-translation-zh]] (the verification page)
· [[hernan-email]] (how the result is reported back to Hernán).
