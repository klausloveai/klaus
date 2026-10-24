---
name: case-transfer
description: |
  Hand a litigation or pre-litigation case from one handler to another at 凌图律所 / Law Office
  of Shenqi Cai APC so the receiver — and the receiver's Claude — has the whole file without
  reading the sender's mailbox. Use for "case transfer", "交接案子", "把 <案名> 转给 <人>",
  "handoff to Allison", "完整交接", "/case-transfer <案名> <接手人>". It inventories every email
  thread and attachment, files what was never filed (MD5-checked), exports closed threads to PDF
  with an index, builds a Parties & Service List, brings the receiver into only the threads that
  are still active, writes an English Case Transfer Memo, and drafts one transfer-complete email
  to the receiver copying the team. Version 1.0, built from Brian Wu v. Azucanela (2026-10-21/23).
  DRAFT-ONLY for every email; Klaus approves each send.
---

# case-transfer 1.0

**Built from:** Brian C. Wu v. Azucanela LLC, Klaus → Allison Pan, 2026-10-21 to 10-23.
The worked example's real IDs are in `assets/config.example.brian-wu.json`.
Refine this file after every transfer: add what went wrong to **Lessons** and bump the version.

## What "done" means

The receiver can run the case from Drive alone:
1. Every case email thread is either **active** (receiver is on it) or **archived** (PDF + index).
2. Every email attachment is in the case folder (MD5-verified), in a sensible subfolder.
3. One **Case Transfer Memo** (English) says where the case stands, what happens next and
   when, what is risky, and where everything lives.
4. One **Parties & Service List** says who is who.
5. The team got **one** transfer-complete email. Nobody got a pile of forwards.

## Order of work — inventory first, email last

Brian Wu did it backwards: a handoff email went out on day 1, the archive was built on day 3,
and the day-1 email's to-do list (an extension stipulation) was already obsolete. It took a
second "transfer complete" email to fix. **Do not send anything to the receiver until Phase 5.**

### Phase 0 — Inputs (ask Klaus only for what you cannot find)
Case name · receiver (name + email) · attorney of record · Drive case folder id · Gmail case
label name + id · Case Log sheet id · `5. Correspondence & Demand` folder id.
Copy `assets/config.example.brian-wu.json` to the scratchpad and fill it in.

### Phase 1 — Inventory (read-only)
```bash
python3 ~/.claude/skills/case-transfer/scripts/transfer_tools.py inventory <config> <workdir>
```
- Threads = case label **plus** a keyword query (case number, party names, client emails),
  **deduped by thread id**. Brian Wu: two searches overlapped — 79 was reported, 58 was real.
- Classify each thread **include / exclude**. Exclude: other cases' threads, HR/compensation,
  multi-case memos and meeting notes, One Legal monthly statements, calendar notifications.
  Put excluded ids and reasons in the config.
- Mark **active** threads — ones that will have a follow-up: a pending instruction from the
  attorney, a client question awaiting reply, an expected payment. Usually 1–3. Everything else
  is history. **Klaus decides** which active threads get touched (Brian Wu: he chose not to
  reply on the 10/9 client thread).
- Read the active threads **to the last message**. Facts come from the last one.

**Gate 1 → show Klaus:** thread counts, the exclude list with reasons, the proposed active list.

### Phase 2 — Attachments (read-only audit, then file)
```bash
python3 .../transfer_tools.py audit <config> <workdir>
```
- Every attachment is compared to the case folder by **MD5**, not by name. Zips are opened and
  compared member by member. Skip calendar invites and firm templates (letterhead).
- Brian Wu: 81 unique attachments, 27 already filed, **42 never filed** — including five client
  evidence documents, one of them the invoice behind the $7,344 commission claim.
- Destinations: client evidence → `4. Contract & Evidence`; One Legal receipts/invoices →
  `Receipts`; letters actually sent → `5. Correspondence & Demand`; vendor quotes →
  `0. Attorney Work Product`; **drafts and intermediate versions → `Email Archive/Attachments`**
  dated, never into `2. Pleadings` where they could be mistaken for the filed version.
  Encode as `dest_rules` in the config.

### Phase 3 — Archive and index (writes to Drive)
```bash
python3 .../transfer_tools.py archive <config> <workdir>   # long — run in background
python3 .../transfer_tools.py index   <config> <workdir>
```
- One PDF per thread in `5. Correspondence & Demand / Email Archive/`, named `YYYY-MM-DD - subject`.
  Quoted history and footer notices trimmed; each message once in full; attachments listed.
- Every included thread gets the case label (all messages).
- `00 Email Index` sheet: status, dates, subject, message count, external parties,
  attachments, PDF link, note, thread id. **Active rows first, with a note saying what is pending.**
- Gmail quota: the script sleeps and retries. If a run dies, re-run the step; it is idempotent
  except for uploads, so check the archive folder before re-running `archive`.

### Phase 4 — Knowledge the receiver cannot get from documents
- **Parties & Service List** (sheet, case folder root). Columns: group, name, role, email, phone,
  address, notes. Include: client and every client representative; each defendant and whether
  represented; **opposing counsel, or an explicit "None" row**; firm people; court/dept/judge;
  vendors; mediator. Note anything only the sender knows:
  - a contact saved under the wrong name (Brian Wu: `401efoothill@` saved as "Rich" — it is Brian);
  - an address that is **correspondence-only, not an agreed e-service address**;
  - who actually answers (Wilson Chen, not Rich).
- **Verify facts at the source before writing them down.** Brian Wu caught: Dept 26 vs 25;
  September 26 (UTC) vs September 25 (Pacific); a deadline we computed vs one agreed in writing.
  Label every date **computed** or **confirmed**.
- Update the internal case brief (or create one) on the **same Drive file id**.

### Phase 5 — Bring the receiver in (drafts; Klaus approves each)
**Cc alone does not give the receiver anything that came before.** A Cc'd person receives only
the new message. To put the receiver on an active thread:
- reply in that thread, **quote the last message in full** below your text, and
  **re-attach its attachments**;
- To = the person who sent the last message; Cc = receiver + the people that thread's rules
  require (Hernán threads: Cassie + Joe).
- Keep it to two sentences: the case has been transferred to <receiver>; <receiver>, please
  follow the steps below.

**Internal approval of a client reply:** reply **inside the client's thread but addressed only
to the attorney** (Cc receiver + partners; client not on it). The attorney sees the client's
email below and the proposed reply in a quote box. Send to the client only after approval.

**Client introduction:** only if Klaus wants it, and only on a thread the client is already
writing on. One message, reply-all plus the receiver.

### Phase 6 — Transfer memo and the one transfer-complete email
- **Case Transfer Memo**, English, PDF, case folder root, ~4 pages, `INTERNAL — ATTORNEY WORK
  PRODUCT` banner. Sections (template: `assets/memo_template.html`):
  1 Case at a glance · 2 Where the case stands · 3 Next steps and dates (table; mark anything
  superseded) · 4 Email threads still active · 5 Issues that matter · 6 Other open items ·
  7 Where everything is (folder-by-folder, with links) · 8 Working notes (contact traps,
  attorney's preferred channel, e-service limits).
- **Email**: To receiver, Cc attorney + Cassie + Joe (ask Klaus about others). Short: transfer
  complete; the memo is the one reference; **the three most immediate items**; anything in an
  earlier email that is now obsolete; "nothing else is active." Attach the memo.

**Gate 3 → bilingual preview** (`~/.claude/draft-review-format.md`), then wait for "发".

### Phase 7 — Wrap
- Case Log: one row — transferred to whom, effective date, what was archived, active threads,
  receiver's next steps, all message ids and sheet ids.
- Activity Log: one row (conclusion + counts + ids). Errors found later → **append a correction
  row**, never edit.
- **Relabel every touched thread and count**: messages carrying the label = messages in thread.
- Downloads: compare by MD5 against Drive, move matches to Trash.
- Tell Klaus what only he can do (add receiver to the WeCom group, account settings such as
  One Legal, anything needing his login or CAPTCHA). **Calendar belongs to the receiver** —
  do not create events for the sender.

## Rules that bit us (Lessons — add to this list every time)

| # | Lesson | Since |
|---|---|---|
| 1 | Inventory before emailing; one complete transfer email at the end. | Brian Wu |
| 2 | Cc ≠ history. Quote the last message and re-attach its files. | Brian Wu |
| 3 | Only active threads get the receiver added; everything else → PDF + index. | Brian Wu |
| 4 | Receiver's Claude cannot read the sender's mailbox — everything lands in Drive; link, don't attach, so there is one current version. | Brian Wu |
| 5 | Attachments by MD5, zips member by member; drafts go to `Email Archive/Attachments`. | Brian Wu |
| 6 | Dedupe thread ids before counting or reporting. | Brian Wu |
| 7 | Overwriting a draft (`drafts.update` with new raw) **drops its label** — relabel after every update and after send; verify per message. | Brian Wu |
| 8 | Shell `$` expansion silently ate dollar amounts (`$759.44` → `.44`). Build bodies in quoted heredocs (`<<'PY'`); read amounts back before showing Klaus. | Brian Wu |
| 9 | After splicing HTML, read the whole body back — one splice used stale offsets and left a fragment. | Brian Wu |
| 10 | Draft text for Klaus to paste only when he is editing in the Gmail UI; otherwise rebuild the API draft — never both at once. | Brian Wu |
| 11 | Who-said-what from WeCom/WhatsApp: record the actual speaker (Wilson, not "the client"). | Brian Wu |
| 12 | `/handoff` (conversation handoff) is a separate, user-invoked skill. It does not check case completeness. | Brian Wu |

## Guardrails
- DRAFT-ONLY. Every email goes to Klaus as a bilingual preview and waits for "发".
- Never forward a pile of old threads to the receiver.
- No fabrication: if a fact is not in a document or email, say it is unknown in the memo.
- Internal requests never go to the client: check To/Cc/Bcc before every send.
- Firm rules still apply: emails to Hernán Cc Cassie + Joe; case label on every draft;
  external email bodies in English.
