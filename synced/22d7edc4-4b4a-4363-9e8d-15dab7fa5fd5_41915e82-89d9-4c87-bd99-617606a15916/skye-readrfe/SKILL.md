---
name: skye-readrfe
description: "End-to-end handling of a USCIS Request for Evidence or NOID for a Lingtu Law / SIA 高徒 case: pick the scan up from Gmail (the office scanner mails them as MX-M476WH_*.pdf), identify whose case it is, file it into that client's Drive folder, page-map the notice so `See RFE at p. N` cites are real, and write the firm's internal 解读+策略 analysis as a Google Doc — quoting the officer verbatim with the operative holding in red, counting criteria required against criteria the RFE conceded, giving each objection a numbered 解读 with a parallel-numbered 应对. Then it emails Skye, watches for her 'done' comment, finds an hour both Skye and Cassie are free, and drafts the Chinese meeting invitation. Use whenever an RFE or NOID needs reading, analyzing, translating or filing — 解读RFE / RFE分析 / 看一下这个补件 / 补件策略 / 收到RFE了. The Response letter itself belongs to skye-rfe."
---

# RFE 解读+策略 (Lingtu Law / SIA 高徒)

**Scope: from the scanned notice arriving in Skye's inbox through to a meeting booked with
the client.** Drafting the Response letter is a different job with its own skill
(`skye-rfe`), which takes the 解读 document produced here as its starting point.

The 解读 has two readers with different needs, and the format exists to serve both at once:
**the attorney**, who needs to know within a day whether the case is still winnable and what
has to be collected, and **the client**, who needs to understand what the government actually
said about them. That is why the officer's English is quoted verbatim and then translated
rather than paraphrased — the client is entitled to see the real words, and the attorney needs
the exact language to argue against later.

Three phases: **intake** (Steps 1–3), **analysis** (Steps 4–11), **hand-off** (Steps 12–14).

---

# Phase 1 — Intake

## Step 1 — Find the scan in Gmail

The office scanner mails notices to `skye.s@lingtulaw.com`. They arrive from
**`Lingtu Law <joe@lingtulaw.com>`**, subject **`Scanned image from Lingtu Law`**, with a
PDF attachment named **`MX-M476WH_<yyyymmdd>_<hhmmss>.pdf`**.

```bash
gws gmail users messages list --params '{"userId":"me","q":"from:joe@lingtulaw.com has:attachment newer_than:30d","maxResults":20}'
gws gmail users messages get --params '{"userId":"me","id":"<msgId>","format":"full"}'
gws gmail users messages attachments get --params '{"userId":"me","messageId":"<msgId>","id":"<attachmentId>"}'
```

The attachment comes back as base64url in a `data` field — decode it with
`base64.urlsafe_b64decode` and write the bytes yourself. **Attachment ids run to ~400
characters**; truncating one for display and then reusing the truncated value returns
`Invalid attachment token`, so carry the full string through.

The scanner mails everything, not just RFEs — approvals, receipts, denials, client mail. So
open the PDF before assuming. If the user pointed at a specific message, use that one; if they
just said a scan came in, list recent ones and say which you are working on.

## Step 2 — Read it and identify the case

Read page 1. It gives you everything you need to route the document: the **beneficiary's
name**, the **receipt number**, the **notice type** (REQUEST FOR EVIDENCE / NOTICE OF INTENT
TO DENY / approval / receipt), the **form** (I-140, I-129), the **date**, and the
**response deadline**.

If it is not an RFE or NOID, stop and say so — this skill does not cover approvals or receipts.

## Step 3 — File it into the client's case folder

Find the client's case folder in the shared drive (`0AIXy3tjXMf-MUk9PVA`) by the beneficiary
name you just read:

```bash
gws drive files list --params '{"q":"name contains '"'"'<Client>'"'"' and mimeType='"'"'application/vnd.google-apps.folder'"'"' and trashed=false","supportsAllDrives":true,"includeItemsFromAllDrives":true,"fields":"files(id,name,parents)"}'
```

**Look for an existing RFE folder before creating one.** Cases already carry these under
various names — `0. RFE/`, `RFE/`, `<Client> RFE/`, sometimes nested under a `Schedule A/`
subfolder. Put the scan in the one that exists rather than creating a second folder that
splits the case in two. Only when there is genuinely no RFE folder, create one named `RFE`
in the case's main folder:

```bash
gws drive files create --params '{"supportsAllDrives":true}' \
  --json '{"name":"RFE","mimeType":"application/vnd.google-apps.folder","parents":["<case folder id>"]}'
gws drive files create --params '{"uploadType":"multipart","supportsAllDrives":true}' \
  --json '{"name":"<Client> RFE <yyyy-mm-dd>.pdf","parents":["<RFE folder id>"]}' \
  --upload rfe.pdf --upload-content-type application/pdf
```

Rename the scanner filename to something a human can read. Keep the name portal-safe:
letters, digits, spaces, `_ - . ( )` only.

Note `gws` takes the request body in `--json` and query parameters in `--params`, and prints
a `Using keyring backend:` line before its JSON — strip everything before the first `{`.

---

# Phase 2 — Analysis

## Step 4 — Ask about the translation before drafting

**Confirm with the user, every single time, whether this client needs the Chinese
translation.** Domestic clients whose English is weak get the RFE quoted and then translated
paragraph by paragraph. US-based clients who read English do not, and padding their document
with translation makes it harder to use.

Do not infer this from the client's name or from where the case was filed. Ask:

> 这个客户需要中文翻译吗？（国内客户一般需要，在美客户一般不用）

Record the answer as `translate: true|false`; it feeds straight into the builder script. Ask
at the same time whether an analysis document already exists that you should be updating
rather than creating — and check the folder yourself either way.

## Step 5 — Read the whole notice, and page-map it

Read it end to end before forming a view. Two things are easy to miss and both matter more
than anything else in the document:

- **What the officer conceded.** Buried in the middle of eight pages of objections there is
  often a single sentence like *"The evidence you submitted does meet the 'plain language' of
  this criterion."* That sentence is the most valuable thing in the notice and it decides the
  strategy.
- **What the officer got wrong about the case.** Officers sometimes mischaracterize the field
  of endeavor, the job, or the classification sought, and then tailor every subsequent
  objection to that mistake. When that happens, the mistake *is* the case — arguing individual
  criteria without fixing it first is wasted work.

`read_file_content` on the Drive file gives you the OCR'd text quickly, which is enough to
read. But the OCR discards pagination and the Response will need real `See RFE at p. N` cites
throughout, so build the page map now:

```bash
python3 <skill>/scripts/rfe_pages.py rfe.pdf sheets
```

This writes contact sheets with the page number stamped on each page. Read them and write down
which section falls on which page. A typical 16-page EB-1A notice maps as: p1 cover and
deadline · p2 Part 6 + field of endeavor · p3 continuing to work + substantial benefit ·
p4–5 first criterion · p6–7 second criterion · p8 **criterion MET** · p9–13 remaining criteria
· p14 final merits · p15 coversheet.

### Verify the notice is one document before saying anything about it

Scans get combined, and two clients' notices can end up in one PDF. But a claim that a client's
file is contaminated is expensive — it sends someone hunting for a filing accident, and can get
a good file deleted and re-uploaded. **This has been fabricated before.** So when the pages
look inconsistent, check three things against each other and report only what they show:

1. the **footer barcode string** (e.g. `NSCI140NSCI14000038976847`), which is per-notice;
2. the **`N of M` page counter** in the footer, which should run unbroken 1..M;
3. the **coversheet** at the end — beneficiary name and receipt number.

If all three agree, it is one document; say nothing about contamination. If they genuinely
disagree, say exactly which pages carry which barcode and which name, so the claim can be
checked. Never assert a filing problem from an impression of the content alone.

## Step 6 — Count before you analyze

Before writing a word of analysis, work out three numbers and put the answer at the top:

1. **How many criteria does the regulation require?** EB-1A: three of ten. O-1A: three of
   eight. Schedule A Group II: **two of seven** — and Group II has **no final-merits
   determination**, so do not import the EB-1A framework into it. NIW has prongs, not criteria.
2. **How many did the RFE concede?** Quote the concession exactly.
3. **How many are therefore still needed?**

This reframes the whole exercise. A notice objecting to six criteria looks devastating until
you notice it conceded one and only needs two more.

List separately any threshold issues that are not criteria at all — a blank form part, a
mischaracterized field of endeavor, ability to pay, a missing statement of intent. They are
usually cheap to fix and expensive to miss.

## Step 7 — Break each objection down, point by point

This is the substance. Work through the notice **in the officer's own order**, one section per
criterion, producing four things for each:

**我们交的** — what we actually filed under this criterion, in one line. Skip where the RFE
already recites the list.

**RFE 原文** — the officer's words, quoted. Quote enough that the reasoning is visible; cut the
boilerplate "to assist in determining…" lists, which say nothing about this case. Mark the
**operative sentence in red bold** — the one clause that actually decides the objection. There
is usually exactly one per objection, and finding it is most of the work.

**翻译** — the Chinese translation, paragraph by paragraph, interleaved with the quotes it
translates rather than collected at the end. Omit entirely when `translate: false`.

**解读** — what the officer is actually saying, as **numbered points, one per distinct
objection**, in a single paragraph: `1）…；2）…；3）…`. Be concrete. "认为奖项不够" is useless;
"认为竞赛面向全国开放不等于奖项本身获得全国认可" tells the reader what has to be rebutted.

**应对** — our strategy, as separate paragraphs, **numbered in parallel with 解读**: 应对 1）
answers 解读 1）, and so on. This one-to-one correspondence is the single most useful property
of the format: it makes an unanswered objection visible at a glance, and each numbered pair
later converts into a sub-argument in the Response. If an objection has no good answer, say so
in that slot rather than silently dropping it — a known weak point is worth more to the
attorney than a gap.

Paste Drive links to the relevant evidence folders directly into the 应对 points. Two habits
worth carrying through:

- **Where the officer overlooked evidence already in the record, say where it is.** A large
  share of objections are not "you have no evidence" but "I did not see your evidence." The
  answer is a pinpoint cite, not new collection.
- **Where the officer invented a requirement, name the real standard first.** Objections often
  smuggle in a test the regulation does not contain. Reciting the plain language, or the
  officer's own quoted definition, takes the yardstick back before any evidence is discussed.

## Step 8 — Light record check, and flag what you could not confirm

The 解读 is written fast, from the notice. But every 应对 point makes an implicit promise about
what the evidence says, and those promises get relied on for months — they flow into the
Response, into the client's collection list, and into what the attorney tells the client is
winnable.

So before publishing, spot-check the evidence each 应对 point leans on. Not an exhaustive audit
— open the exhibit or the index, confirm it says what the point assumes, move on. What this
catches, from real cases: evidence assumed to be filed that never was; a credential described
one way in the petition letter and differently on the certificate; a contract said to name the
beneficiary — check which page and in what capacity; a source said to be available that is not.

Anything you cannot confirm goes in a **⚠️ 待核实** block under that section, stating what was
assumed, what you actually found, and what would settle it. Do not quietly fix it and do not
quietly drop it. The attorney decides; your job is to make sure she knows.

Contradictions between documents already filed — two figures for the same contract, two
accounts of the same credential — belong here too, with both versions quoted. Internal
contradictions in a filed record are exactly what a skeptical officer looks for.

## Step 9 — Close with what the client has to produce

Every 应对 point that depends on evidence we do not yet hold creates a collection task, and
those are the long pole: a signed expert letter or a re-issued certificate takes weeks, and the
deadline does not move. Collect them into a **需客户提供** section at the end.

One line per item: **what is needed**, **why** (which objection it answers), and **who has to
produce it** — client, employer, recommender, or the firm. The "who" matters because items
needing a third party's signature must start first.

Keep it to what is actually missing. Evidence already in the record that the officer overlooked
belongs in 应对 as a pinpoint cite; putting it on the client's list sends them hunting for
something we already have.

## Step 10 — Build the document

Write a JSON spec and run the builder, which handles the colors and label formatting:

```bash
python3 <skill>/scripts/build_jiedu.py spec.json jiedu.docx
```

See `references/spec_example.json` for the shape and `references/format.md` for the formatting
conventions and why each exists. Upload into the RFE folder, converting to a Google Doc, named
`<Client> RFE 解读+策略`:

```bash
gws drive files create --params '{"uploadType":"multipart","supportsAllDrives":true}' \
  --json '{"name":"<Client> RFE 解读+策略","mimeType":"application/vnd.google-apps.document","parents":["<RFE folder id>"]}' \
  --upload jiedu.docx \
  --upload-content-type application/vnd.openxmlformats-officedocument.wordprocessingml.document
```

**If an analysis document already exists, do not overwrite it.** Skye and the reviewing attorney
edit these directly and their copy is the live one. Read it, diff it against what you would
write, merge their edits into your spec, keep their filename, and update in place by file id
with `gws drive files update` (same params, plus `"fileId"`). Leave their open comments alone.

## Step 11 — Tell Skye it is ready

Email `skye.s@lingtulaw.com` — and only her. This notification is internal; nothing in this
skill ever emails the client.

```
Subject: <Client> RFE 解读+分析策略已完成
```

Body: the document link, the deadline, the count (required / conceded / still needed), and the
one or two things she has to decide. Keep it to a few lines — the detail is in the document.

```bash
gws gmail users messages send --params '{"userId":"me"}' --json '{"raw":"<base64url-encoded RFC822 message>"}'
```

Build the raw message with Python (`email.message.EmailMessage`, then
`base64.urlsafe_b64encode`) so the Chinese subject and body encode correctly.

---

# Phase 3 — Hand-off

## Step 12 — Watch for Skye's `done`

Skye reviews the document and leaves a comment reading **`done`** when she is satisfied. That
comment is the signal to start scheduling.

```bash
gws drive comments list --params '{"fileId":"<doc id>","fields":"comments(id,author(displayName),content,resolved,createdTime,replies(content))","includeDeleted":false}'
```

Match on the comment content being `done` (case-insensitive, possibly with punctuation) from
Skye. Note the API returns `author.displayName` reliably but often not an email address, so
match on the name.

**Be honest about what this step can and cannot do.** You cannot watch a document
continuously; you check when you are run. So either check now and report what you find, or —
if the user wants it to happen without them asking again — set up a recurring check with the
`/loop` skill (e.g. every 30 minutes) rather than implying you are watching. If the comment is
not there yet, say so and stop; do not schedule anything.

## Step 13 — Find an hour both attorneys are free

The meeting is Skye, Cassie and the client, one hour, in the firm's zone: **Los Angeles
(`America/Los_Angeles`)**.

```bash
gws calendar freebusy query --json '{"timeMin":"<ISO with -07:00>","timeMax":"<ISO>","timeZone":"America/Los_Angeles","items":[{"id":"skye.s@lingtulaw.com"},{"id":"cassie@lingtulaw.com"}]}'
```

Search the next five business days. Propose two or three candidate slots rather than one, so
Skye has something to choose from, and prefer times that are civil at **both** ends.

Two practical traps in the free/busy data. **All-day events come back as a `00:00`-to-`00:00`
pair on the same date** — a naive overlap test treats them as zero-length and they stop
blocking anything, so expand any same-instant pair to cover the whole day before testing.
And **skip US public holidays**: the calendar will happily show both attorneys free on
Thanksgiving or Labor Day.

For a **China-based** client, Beijing is `Asia/Shanghai`, **UTC+8, no daylight saving** — so it
is LA+15 during Pacific Daylight Time and LA+16 during Pacific Standard Time. Compute it from
the actual dates rather than from memory of the offset.

The workable band is narrower than it first looks, and there is no slot that is convenient at
both ends. Only two windows are usable at all:

| LA (firm) | Beijing (client) | Reads as |
|---|---|---|
| **17:00–19:00** | **08:00–10:00 next day** | LA evening ↔ Beijing morning — usually the best compromise |
| 06:00–08:00 | 21:00–23:00 same day | LA early morning ↔ Beijing evening — use if the attorneys prefer it |

Do not search LA afternoon: **LA 15:00 is Beijing 06:00 the next day**, which is too early to
offer a client. Searching a comfortable-looking LA window and reporting whatever it maps to is
the easy mistake here — start from the hour that works for the **client** and check whether the
attorneys are free then, not the reverse.

Say the date on both sides explicitly, because for a Beijing client it is nearly always a
different calendar day.

For a **US-based** client, use their actual local zone — Eastern, Central, Mountain, Pacific —
not an assumption.

## Step 14 — Confirm with Skye, then write the client script

**Do not write the client-facing script until two things are settled with Skye: which time
zone the client is actually in, and which slot she wants.** Getting the zone wrong produces an
invitation that reads as careless to the client, and the case folder does not always say where
someone currently lives.

Ask her both together:

> 这个客户是国内（北京时间）还是在美国？如果在美国，哪个时区？
> 会议时间我找到这几个两位律师都有空的一小时：<候选时段，两地时间都写>。您定哪个？

Once she has confirmed, produce the script for her to send — **you generate it, she sends it.**
Template:

> xx/xx/xxxx 洛杉矶时间 x 点，客户当地时间 x 点，您是否有空，我们约个会议，讨论一下您的 RFE。

Spell out both dates when they differ, and keep the register the firm uses with clients. Hand
Skye the text; do not message the client yourself.

---

## Finish by reporting

The document is for the file; the message is for the attorney. Lead with the decision she has
to make, not a description of what you wrote:

- the count — required / conceded / still needed
- any threshold mischaracterization, because it reframes everything else
- the criteria most likely to carry the case, and the ones not worth pushing
- every **⚠️ 待核实** item, and what would settle it
- what has to be collected, and who has to produce it
- the response deadline, and where in the process this now sits
