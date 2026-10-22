---
name: disbursement-lien-email
description: |
  The `disbursement-lien` run PLUS Gmail drafts for 凌图律所 / Lingtu Law PI settlements: lien
  reduction letters and the disbursement letter as PDFs, then a reply-all draft to each provider
  with its lien reduction attached, and a W-9 request draft for any provider whose W-9 is missing.
  Use for "/disbursement-lien-email", "lien redu and draft the emails", "发 lien 邮件",
  "lien reduction 起草邮件", or `/disbursement-lien ... -email`. DRAFT-ONLY: never sends.
---

# /disbursement-lien-email

`/disbursement-lien-email <client> [lien [providers]] [dis] [--detail | --formal] [--en]`

## Step 1 · Run `disbursement-lien` first

Follow `~/.claude/skills/disbursement-lien/SKILL.md` Steps 1–7 exactly (anchor → reconcile →
remit-to → PDFs → verify → client message). This skill only adds the email step. Emails cover
the **lien letters and W-9 requests**; the dis goes to the client through DocuSign, which Klaus
sends himself.

## Step 2 · Find the thread for each provider

```bash
python3 scripts/make_draft.py find --client "<Client>" --domains "<provider.com>,<billing.com>,<funder.com>" [--box claims|piteam|picase]
```

- Search by the provider side's **mail domains** (from the bill, W-9 cover email, or a past thread),
  not by keywords: keyword search returns the internal and opposing-counsel threads that merely
  mention the provider. The script drops threads with no outside participant and tags provider threads.
- Search the case's owning mailbox (PI Master Sheet tab). Old LaShine cases: klaus@ (default box).
- Pick the thread **most on point and most recent**: the billing company's own balance/lien thread,
  or the funder's own lien-notice thread, beats an older scheduling or records thread. Open a new
  thread only when none exists.
- Read the chosen thread to its **last message** before drafting: it may already answer the question
  (e.g. a confirmed balance, an attached W-9) or name a new contact address.
- If a funder owns the receivable, the lien email goes in the funder's thread, To its settlement
  address. Don't copy the original provider unless Klaus says so (funders ask for exclusive contact).
- If a mailbox returns 401, its gws login has expired: tell Klaus, don't fall back silently.

## Step 3 · Draft

Lien letter (attach the matching PDF):
```bash
python3 scripts/make_draft.py draft --kind lien --thread <id> --to <addr> \
  --greeting "Hi Doctor Office," --attach "<pdf>" --label "<Client>" [--box ...] [--dry-run]
```
Missing W-9 (no attachment):
```bash
python3 scripts/make_draft.py draft --kind w9 --thread <id> --to <billing addr> \
  --greeting "Hi <Billing Co> team," --client "Ms. <Client>" --label "<Client>"
```

**Body is fixed. Add nothing.**

```
Hi Doctor Office,

Lien reduction is attached. Please confirm receipt and let me know if there are any questions.
```

- Greeting: `Hi Doctor Office,` by default; a named contact by name instead
  (e.g. `Hi Evelyn and Apogee team,`).
- Don't explain the case, amounts, or payee; the PDF carries them.
- Reply-all = the recipients of the thread's **last** message (as Gmail does); `--to` picks who goes
  in To, the rest go to Cc, `--cc` adds. Klaus removes people himself.
- Signature = the mailbox's own Gmail sendAs signature (the script fetches it).
- The script puts the draft inside the thread (`threadId` in the request body), and labels the
  thread with the case label. If no unique case label exists, it stops: ask Klaus, don't create one.
- To replace a draft (e.g. after fixing a PDF), pass `--update <draft id>` so there is still one draft.

Run with `--dry-run` first when testing; it prints headers and body and writes nothing.

## Step 4 · Report

One short list per provider: PDF path, draft id + thread subject, To/Cc, or STOP (no W-9, W-9
request drafted). Then the client message from `disbursement-lien`.

## Never

Send any email. Klaus reviews every draft and sends it himself.
