---
name: owed-to-opposing
description: |
  Find and close out everything 凌图律所 / Law Office of Shenqi Cai APC still owes the
  OTHER SIDE in a litigation case — documents opposing counsel or a self-represented
  defendant asked for, or that we promised, but which could not be sent at the time
  because the thing did not exist yet (a court-returned conformed copy, a stipulation
  still to be drafted, a record still to be pulled). Use whenever any of these come up:
  "对方要的东西给了吗", "还欠对方什么", "盖章件回来了吗", "conformed copy", "file-stamped
  copy", "拉 conformed 件", "把盖章版发给对方", "stipulation 发了没", "/owed-to-opposing"
  for a named case, or right after an e-filing is accepted. Also run it as a sweep across
  all of Hernán's cases when asked "还有什么挂着的". It READS Gmail + Activity Log + Case
  Log + Drive, reports what is now deliverable, pulls or prepares the missing artifact,
  and DRAFTS the transmittal. DRAFT-ONLY — never sends to the opposing side.
---

# Owed to the other side

## The lesson that created this skill

**Brian Wu v. Azucanela LLC, 2026-09-26 → 2026-10-21 (25 days).** Robert Kennedy Leiva,
self-represented, asked in writing for two things: a **file-stamped copy of his Proof of
Service**, and the **written extension stipulation**. Both were reasonable, both were
owed, neither could be sent that day — the conformed POS had not come back from the court
yet, and the stipulation had not been drafted.

Hernán replied on 9/28 with the *submitted* POS (`FOR COURT USE ONLY` box blank) and a
one-line email confirming the extension. Both items were written into the Case Log as
outstanding. Claude raised them twice and both times **ended on a question** — "要我现在去
One Legal 把 conformed 件下下来吗？" — the thread moved on, nobody answered, and the items
sat for 25 days while Leiva's response deadline (11/17/2026) came closer.

Three failures, all structural:

1. **The obligation was recorded, not scheduled.** The Case Log is a ledger. It does not
   fire when the blocking condition clears.
2. **The trigger signal was already in the system and nothing read it.** One Legal's
   `eFiling accepted for <case>` emails were ingested into the Activity Log on 9/23 and
   9/30 by [[hourly-email-agent]]. The conformed copy was available from that moment.
   Nothing connected "accepted" to "someone is waiting for this".
3. **Claude ended on a question instead of an owner.** A question is not a handoff. This
   skill never ends on "要我…吗？" — it ends on a drafted deliverable or a named owner
   with a date.

## The task shape this skill exists for

Two-stage obligations:

```
对方 request（或我方承诺）  →  [条件未成就]  →  动作
     9/26 Leiva asks            court has not         send the
     for file-stamped POS       returned it yet       conformed copy
```

The gap is always between the second and third box. Anything that can be done the same
day gets done; what cannot gets written down and then orphaned.

Where this shape recurs:

- **Conformed / file-stamped copies after any e-filing** — POS, complaint, amended
  pleadings, Doe amendments, CIV 105, stipulations, jury fee notices
- **Stipulations** the attorney agreed to in correspondence but never papered
- **Discovery** — supplemental responses promised in a meet-and-confer
- **Exhibits, records, policy pages** offered to the other side
- **Court orders** that must be served on the opposing party once issued

## Do NOT create a tracking table

Per [[case_data_architecture]] the firm has three layers already and a fourth one will
rot. This skill **reads** existing sources and reports. It stores nothing of its own.

| Source | What it gives |
|---|---|
| Gmail, opposing-party thread | the request itself, in their words — quote it verbatim |
| Gmail, our sent mail | what we promised, and what we actually attached |
| Activity Log | `eFiling accepted for <case>` rows → the One Legal order numbers |
| Case Log | items a prior session already flagged as outstanding |
| Drive case folder | whether a CONFORMED copy already exists |

## Workflow

### 1. Identify the other side and pull their thread

Opposing counsel, or a self-represented party. Search klaus@ on their **domain or
address**, not on a name — a name search misses messages that do not contain it:

```bash
gws gmail users messages list --params '{"userId":"me","q":"(<their-domain> OR <their-address>) newer_than:120d","maxResults":30}' --format json
```

Read the thread **to the end** ([[feedback_read_thread_to_end]]). Then list, verbatim:

- every sentence in which they **ask** for something (`Please send…`, `Please provide…`)
- every sentence in which **we** said we would send something (`I will send you…`,
  `once it is available`, `Please find attached`)

⚠️ `Please find attached` is not proof the right thing was attached. On Brian Wu, Hernán
wrote "Please also find attached the filed POS" and the attachment was the submitted copy.
**Open the attachment and check it** (step 3).

### 2. For each item, state the blocking condition and whether it has cleared

Write one line each: *what was asked · who asked · the date · what it is waiting on ·
cleared yes/no · where the artifact is now*.

### 3. Verify a conformed copy by RENDERING it, never by text

**Court file stamps on LASC PDFs are images.** `extract_text()` and `pdftotext` do not see
them, and an unstamped PDF looks identical in a text dump to a stamped one. Same rule as
[[feedback_signature_check_render]].

```bash
gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r200 -dFirstPage=1 -dLastPage=1 \
   -sOutputFile=p1.png <file>.pdf
```

Then crop the upper-right `FOR COURT USE ONLY` box and look at it. Blank box = submitted
copy. A conformed copy carries the stamp, and usually the clerk name and a Deputy line.

### 4. Pull the conformed copy

Two routes. Both need Klaus to click — do not pretend otherwise.

**One Legal** (preferred, free, already paid for): each e-filing has an order number. Get
it from the Activity Log row or the One Legal confirmation email, then
**order → View court-returned documents**. Requires login.

**LASC Court Access Portal** `cap.lacourt.ca.gov` ([[lasc_public_case_documents]]): the
register is free and needs no attorney number, but downloads are **$1/page** and the
**CAPTCHA must be clicked by Klaus**.

Brian Wu order numbers, as a worked example: Leiva's POS `29345090`, Azucanela LLC's POS
`29402432`.

### 5. File it, replacing the submitted version

Per [[feedback_always_file_to_case_folder]]: one current version per document.

- The conformed copy **replaces** the submitted copy — `files.update` into the **same
  Drive file id**, renamed `… - CONFORMED.pdf`. Drive keeps the old version in history.
- **Exception, and it is a real one:** a copy that was *actually sent to the other side*
  is a separate record of what they received, not a duplicate. Keep it, named so it says
  so — e.g. `POS - Robert Kennedy Leiva (copy emailed to Leiva 09.28.2026 - SUBMITTED,
  court stamp box blank).pdf`. Compare MD5 before assuming the emailed copy is the same
  file as the one already in Drive; on Brian Wu it was not.

### 6. Draft the transmittal — and nothing else

Cover email to the opposing side: **only the owed items**. Do not raise strategy,
settlement, mediation, or the merits. A self-represented defendant reads every line
looking for something to use.

Draft on klaus@ as a Gmail draft, label the thread with the case label immediately
([[feedback_draft_case_label]]), and **stop**. Klaus sends.

If the attorney has not seen the item, route it through him first — use
`Skill(hernan-email)`, type **D (交件送签)**: what is attached, which blanks are left for
whom, each judgment he might question as its own numbered item, and the proposed cover
email to the other side quoted inline for his approval.

### 7. End on an owner, never on a question

The report closes with one of:

- ✅ drafted — draft id, which thread, what is attached
- 📋 blocked on a named person and a date — "Klaus to pull order 29345090 from One Legal;
  needed before 11/17"

**Never** "要我去拉吗？" as the final line. That is the exact failure this skill was built
to stop. If it genuinely needs Klaus's decision, state the recommendation first, then ask.

## Run it automatically at these moments

- Right after an **e-filing is accepted** — the conformed copy exists from that moment
- When drafting any **weekly case update** ([[weekly-case-update]]) — stale owed items are
  exactly what a weekly update should surface
- Before any **response deadline, default request, or hearing** — unmet obligations to the
  other side get raised at the worst time
- When the other side **follows up** — by then it is already late

## Guardrails

- **DRAFT-ONLY.** Never send to the opposing party. Klaus sends every outbound himself.
- **Quote, never paraphrase, what they asked for.** Their words decide whether we complied.
- **No fabrication.** If the conformed copy has not been pulled, say it has not been
  pulled. Do not write "attached is the file-stamped copy" into a draft before the file
  is in hand — that is how the 9/28 email became a problem.
- Negative claims need a premise ([[feedback_negative_claims_need_premise]]): report the
  query, the time window, and the blind spot. **Hernán's own mailbox is not visible from
  klaus@** — if he wrote to the other side directly without copying Klaus, this skill
  cannot see it, and the report must say so.
