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
  to the receiver copying the team. Starts with a readiness check (is now a good point to hand
  over, and which related cases must move with it). Version 1.2 — built from Brian Wu v. Azucanela
  and Zelaya v. CB Kitchen (2026-10-21/25). DRAFT-ONLY for every email; Klaus approves each send.
---

# case-transfer 1.3

**Built from:** Brian C. Wu v. Azucanela LLC, Klaus → Allison Pan, 2026-10-21 to 10-23.
The worked example's real IDs are in `assets/config.example.brian-wu.json`.
**1.1:** Zelaya v. CB Kitchen, Klaus → Allison Pan, 2026-10-23 (a transfer picked up after a day-1 handoff
email had already gone out). Config: `assets/config.example.cb-kitchen.json`.

**1.3:** Xicheng Li v. United Airlines, Klaus → Allison Pan, 2026-10-25 (lessons 28–37): Gate 1 opens with a case snapshot and self-contained in-flight items; Gate 3 shows a recipient table; Phase 7 drafts the client WeChat notice and lists snoozed threads.

**1.2:** readiness check, related cases, in-flight handover, Activity Log + WhatsApp in the inventory,
receiver calendar, client notice, sender clean-up (from the CB Kitchen follow-up and the Guolin Zhao /
Weicong Lin assessment, 2026-10-25).

**Dry run** = `inventory` + `audit` only. Both are read-only (audit writes attachments to the local workdir).
Stop at Gate 1.
Refine this file after every transfer: add what went wrong to **Lessons** and bump the version.

## What "done" means

The receiver can run the case from Drive alone:
1. Every case email thread is either **active** (receiver is on it) or **archived** (PDF + index).
2. Every email attachment is in the case folder (MD5-verified), in a sensible subfolder.
3. One **Case Transfer Memo** (English) says where the case stands, what happens next and
   when, what is risky, and where everything lives.
4. One **Parties & Service List** says who is who.
5. The team got **one** transfer-complete email. Nobody got a pile of forwards.

## Klaus's four checks (2026-10-26 — every transfer, every case)
Learned from the first three transfers (Brian Wu, CB Kitchen, Xicheng Li). Gate 1 is organised
around these four, in this order:
1. **Emails — who must see Allison.** Every still-active thread gets the receiver Cc'd (Phase 5
   rule: quote + re-attach). Then introduce the receiver to everyone outside the firm who will
   write to us again: opposing counsel (or a pro per party — by mail if no email), providers,
   lien/funding companies, carriers and WC adjusters, other counsel (e.g. the client's WC
   attorney). A thread owned by another staff member (Claire's appointment threads) → that person
   introduces the receiver in her own thread; Klaus does not reply there. Client → Klaus adds the
   receiver to the WeChat / WeCom group; the receiver introduces herself.
2. **Calendar — make it current, then add the receiver.** Re-check every date against its source
   (extensions, continued hearings, recomputed deadlines). Fix stale events, add missing ones
   (service deadlines, jury fees, SOL), delete junk, then add the receiver as a guest on each
   event the sender owns; ask the attorney to add her to his.
3. **Treatment — first-hand, per provider.** Name, address, phone, email, contact person; visit
   dates and count; what records and bills we hold (Drive path) and what is still missing; lien or
   not, and who funds it. Read the records themselves, not the summary — the records can settle
   questions the summary leaves open (Weicong Lin: the ER MAR showed no rabies PEP).
4. **To-do — what remains.** One list per case: item · owner · due date · source.
Related cases (Weicong Lin + Guolin Zhao) go through the four checks together.

## Order of work — inventory first, email last

Brian Wu did it backwards: a handoff email went out on day 1, the archive was built on day 3,
and the day-1 email's to-do list (an extension stipulation) was already obsolete. It took a
second "transfer complete" email to fix. **Do not send anything to the receiver until Phase 5.**

### Phase −1 — Is now a good time? (read-only, before anything else)
Answer one question for Klaus: **transfer now, wait until a milestone, or transfer now with carve-outs.**
Read: the case's calendar entries for the next 30 days, its open `控制台 Tasks`, its last ~10
Activity Log rows, and the last message of every thread from the past two weeks.

| Check | Good point | Bad point |
|---|---|---|
| Hard deadlines in the next 2–3 weeks | none, or only the other side's | ours, and the sender holds the context |
| In-flight actions (service orders, filings under review, ex parte) | none, or nothing time-critical | something can fail before the receiver is up to speed |
| Attorney availability | attorney reachable | attorney away while a deadline lands (Hernán out 10/21–11/03) |
| Stage | waiting (on service, records, the other side) | mid-negotiation, mid-filing |
| Receiver's load | a few cases | several already handed over the same week |

- **Related cases move together, in one session.** Check for a CM-015 Notice of Related Case and for
  shared defendants or addresses. Guolin Zhao (26NWCV02260) and Weicong Lin (26NWCV03394) share all
  three defendants and the same failed service address — one person must decide service for both.
  One memo per case, each pointing to the other; write the shared decision once.
- **Never a candidate:** Klaus's own PI auto litigation cases (Jiayu Ma, Sai Choi Lau, Chao Zheng,
  presumed Chunpeng Wu) — memory `klaus-keeps-pi-auto-litigation`.
- If the answer is "wait", name the milestone and the date it lands (e.g. "after the amended CM-110
  is filed, 11/6"), and say the trigger is the milestone, not the date.
- If the answer is "now with carve-outs", list each carve-out: what, who finishes it, by when.

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
- **Drive shows work done outside the sender's mailbox.** List case-folder files newer than the last case email and not attached to any email (Xicheng Li: Stine lien and InterHealth psych records came through Claire). Attribute each to a person to ask.
- **Don't trust the `All Cases` roster's Line/Stage columns** (Xicheng Li was listed as Dog Bite / Prep Complaint). Take stage from the docket, the Case Log and the last attorney email.
- **Gmail is not the whole record.** Also read the case's rows in the Activity Log
  (`1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA` → `Activity Log`) and its Case Log. Hernán gives
  many instructions on WhatsApp ("keep following up with the clerk", "the CMC is in November") and
  they exist only there. When the WhatsApp tools are connected, export the case's messages from the
  "Lingtu Law" group to the case folder as well, recording the actual speaker (Lesson 11).
- **List everything in flight**: open One Legal orders (service, filings under review) with order
  number, status and last update; pending court actions; anything waiting on a callback.

**Gate 1 → show Klaus.** Open with a **3-line case snapshot** (what happened and when — DOL with time zone, direction of travel or place; stage; attorney), because the sender may not remember the basics (Xicheng Li: Klaus asked "DOL 到底是哪一天" mid-transfer). Every in-flight or active item must be **self-contained**: who the other party is, what exactly they owe or we owe, the reference number, the due date ("Sedgwick 答复" and "Hernán 第 1 条电话" meant nothing without that). Then: thread counts, the exclude list with reasons, the proposed active list,
the in-flight list, and **one decision: is the client told about the handover, and how** (WeCom
group / WeChat — both need Klaus's hands). CB Kitchen skipped this by default and the client was
never told.

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
  - **If anything is in flight, add "3a. In flight right now"** after section 3: item · order/transaction
    number · status and last update (Pacific time) · next check · **who finishes it** (sender carve-out
    or receiver).
  - **Say what is not in the file** (section 6): other people's mailboxes (Cindy's fee records, the
    attorney's own emails), phone calls never logged, personal WeChat, paper mail. Name who to ask.
- **Email layout (Klaus 2026-10-26/27): tables, not paragraphs.** Seven sections: 1 Case at a glance · 2 Action items (# | Action | When | Notes) — questions for the attorney become receiver action items, and anything Claude found in records is marked "verify before raising" · 3 Treatment, records and bills (per provider: dates, records, bills, missing; leave out unrelated providers) · 4 Case costs advanced (date | cost | paid to | amount, from the actual receipts, plus "not billed yet" and "not confirmed") · 5 Dates · 6 Open orders with current status · 7 Where everything is. Attach any form the receiver must get signed. Inline styles only; screenshot it with headless Chrome before showing Klaus.
- **Email**: To receiver, Cc attorney + Cassie + Joe (ask Klaus about others). Short: transfer
  complete; the memo is the one reference; **the three most immediate items**; anything in an
  earlier email that is now obsolete; "nothing else is active." Link the memo (Lesson 4).
  - **Every date in the next 30 days, with a line asking the receiver to put them on their own
    calendar.** The receiver is not on events the attorney created — CB Kitchen's 10/26 deadline
    was on Hernán's calendar and not on Allison's. Ask the attorney to add the receiver to his events.
  - **Open One Legal orders**: list the order numbers and say that Klaus will forward their
    notifications (Klaus 2026-10-25: he forwards them by hand; orders the receiver places later
    notify the receiver). "Serve attempted" and "new message" notices are time-sensitive — forward
    the same day.

**Gate 3 → recipient table first** (To / Cc / Bcc for every draft, read back from the drafts), flagging anyone on the attorney's original message who was dropped; **then the bilingual preview** (`~/.claude/draft-review-format.md`), then wait for "发".

### Phase 7 — Wrap
- Case Log: one row — transferred to whom, effective date, what was archived, active threads,
  receiver's next steps, all message ids and sheet ids.
- Activity Log: one row (conclusion + counts + ids). Errors found later → **append a correction
  row**, never edit.
- **Relabel every touched thread and count**: messages carrying the label = messages in thread.
- Downloads: compare by MD5 against Drive, move matches to Trash.
- **Sender's leftovers** — CB Kitchen left four stale tasks (d29–d32, from 8/31) on Klaus's board:
  - `0. Tracking Sheet` → `控制台 Tasks`: close or mark every open task for the case
    "transferred to <receiver> <date>".
  - Klaus's calendar: list his own events for the case that are superseded (CB Kitchen had two
    10/12 entries) and delete them only with his OK. Never create events on the sender's calendar.
  - Case artifact (`~/.claude/skills/case-artifact/assets/applied.json`): if the case has one,
    update the handler and the dates on the same URL.
  - `All Cases` roster row (line, stage): fix only if Klaus still uses that sheet.
- **Snoozed threads**: list every case thread snoozed in the sender's mailbox and until when. The API cannot unsnooze; tell the sender to Unsnooze, or it reappears in his inbox after the transfer.
- **Client notice draft**: write the WeChat message to the client (Chinese, plain text, full-width punctuation, a blank line between paragraphs): who now handles the case, the attorney is unchanged, what is in progress, the receiver's email and direct line (leave blank if unknown, never guess), and the standing instruction (do not talk to the other side / sign anything).
- **Tell Klaus what only he can do**, as a list: add the receiver to the client's WeCom group;
  tell the client (if decided at Gate 1); ask the attorney to add the receiver to his calendar
  events; forward One Legal notifications for open orders; anything needing his login or CAPTCHA.

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
| 13 | `archive` changes directory to `~`. Pass the workdir as an **absolute path** (the script now does `abspath` itself). | CB Kitchen |
| 14 | "Already in Drive under another name" must be checked **by text, not by name**. Of 10 assumed duplicates, 4 differed; one (DISC-002) showed the served version had lost the attorney's street address. | CB Kitchen |
| 15 | Thread PDFs made before the transfer: **move** them into `Email Archive` (`addParents` + `removeParents`; shared drives allow one parent) and list them in `existing_pdfs`, or `archive` exports duplicates. | CB Kitchen |
| 16 | Read every earlier handoff email in full (they may be HTML-only) and fix its errors in the final email. CB Kitchen's day-1 email said the client was never billed for costs; the client had Zelled $1,000. | CB Kitchen |
| 17 | Look inside the destination folders before writing `dest_rules`. CB Kitchen's `Receipts` held another case's files; its own receipts were in `Case Cost`. | CB Kitchen |
| 18 | Non-ASCII display names (Hernán) in To/Cc: build the draft with `EmailMessage` + `headerregistry.Address`; `MIMEText` with raw string headers fails with "Invalid Cc header". | CB Kitchen |
| 19 | When two versions of a document exist, keep the one that was **sent** (check each attachment's message To/Date), and replace any DRAFT of it in Drive on the same file id. | CB Kitchen |
| 20 | Don't copy dates or "not in writing" claims from an earlier handoff. CB Kitchen's day-1 email dated Hernán's instruction 9/29 (UTC); it was 9/28 Pacific ("today's CMC"). It also called a pause agreement unwritten; the thread had "Agreed." Convert every Gmail `Date` to Pacific and search the thread before calling anything unwritten. | CB Kitchen |
| 21 | Adding the receiver to an active thread: the reply's last line in the transfer-complete email must match ("No other thread is active" contradicts the Phase 5 reply). Draft both, review together, send together. | CB Kitchen |
| 22 | The receiver was not on the attorney's calendar event for the next deadline (CB Kitchen, 10/26). List every 30-day date in the email, ask the receiver to calendar them, ask the attorney to add the receiver. | CB Kitchen |
| 23 | The client was never told the case changed hands. Make it a Gate 1 decision. | CB Kitchen |
| 24 | Stale tasks for the case stayed on the sender's control-tower board for weeks (d29–d32). Close them in Phase 7. | CB Kitchen |
| 25 | Related cases (CM-015) must move together: Guolin Zhao and Weicong Lin share defendants and one service problem. | Guolin Zhao / Weicong Lin |
| 26 | Attorney instructions given on WhatsApp live only in the Activity Log. Inventory reads the Activity Log and, when connected, exports WhatsApp. | Guolin Zhao |
| 27 | Don't hand over in the middle of an in-flight cluster while the attorney is away (Guolin Zhao: rush service due 11/2, amended CM-110 due 11/6, Hernán out to 11/3). Wait for the milestone, or hand over with written carve-outs. | Guolin Zhao |

| 28 | Manual `gws drive files create --upload` silently fails on a path outside the current directory (scratchpad, /tmp). Copy the file into the working directory and pass a **relative** path; check the returned md5Checksum. | Xicheng Li |
| 29 | A header read that prints only From/Cc hides the To line. Hernán's 10/21 emails were addressed to six people **including the receiver**, and our replies went to him alone. In inventory, list the full To/Cc of the last attorney message on each active thread and note whether the receiver is already on it. | Xicheng Li |
| 30 | Not every case folder has `5. Correspondence & Demand` (the aviation/PI template's 5 is `Cost & Receipt`). Ask where Email Archive goes; Xicheng Li used `2. Legal Documents`. | Xicheng Li |
| 31 | Adding the receiver to an external party's thread (adjuster): write **inside the thread but internal only** (To receiver, Cc attorney + partners), quoting the last service email with its attachments. Never put the adjuster on a handover note. | Xicheng Li |

| 32 | Open Gate 1 with a 3-line case snapshot (DOL + time zone, what happened, stage). The sender asked what the DOL was in the middle of the transfer. | Xicheng Li |
| 33 | In-flight items in Gate 1 must say who, what is owed, reference number and due date. "Sedgwick's reply" and "Hernán's item 1 call" had to be explained. | Xicheng Li |
| 34 | Before asking for "发", show a To/Cc/Bcc table read back from the drafts and flag who was dropped from the attorney's original list (Cindy, Claire). Klaus asked for it. | Xicheng Li |
| 35 | Draft the client WeChat notice in Phase 7 without being asked; leave the receiver's phone blank if not on file. | Xicheng Li |
| 36 | A thread snoozed in the sender's mailbox reappears after the transfer and the API cannot unsnooze it. List snoozed case threads in Phase 7. | Xicheng Li |
| 37 | Another person's work (treatment referrals, liens) appears only as Drive files. Compare Drive file dates against the last email and name who to ask. | Xicheng Li |

## Guardrails
- DRAFT-ONLY. Every email goes to Klaus as a bilingual preview and waits for "发".
- Never forward a pile of old threads to the receiver.
- No fabrication: if a fact is not in a document or email, say it is unknown in the memo.
- Internal requests never go to the client: check To/Cc/Bcc before every send.
- Firm rules still apply: emails to Hernán Cc Cassie + Joe; case label on every draft;
  external email bodies in English.
