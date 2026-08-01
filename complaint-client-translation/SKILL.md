---
name: complaint-client-translation
description: >-
  Translate a finalized litigation COMPLAINT into Chinese and draft the bilingual
  client email asking the client to review and confirm the facts, for 凌图律所 /
  Law Office of Shenqi Cai APC (Hernán Simó litigation). Use this AFTER the attorney
  has finalized/conformed a complaint and BEFORE filing — every complaint gets a
  Chinese translation sent to the client for confirmation. Triggers: "translate the
  complaint for the client", "中文译本给客人确认", "发起诉状给客人核对", "起诉状翻译",
  "complaint client review", "/complaint-client-translation" for a named case, or as
  the post-finalization step chained from `file-complaint` / `dogbite-file-complaint`.
  It DRAFTS ONLY — never sends. Klaus reviews and sends every email himself.
---

# Complaint → Chinese Translation for Client Confirmation

Standing rule (Klaus, 2026-07): **every complaint must be translated into Chinese and
sent to the client to confirm the facts before it is filed.** This skill produces that
translation and the client email as DRAFTS.

## Inputs
The finalized/conformed **English complaint** (PDF or docx) from the case folder, plus the
client's name + email (from the intake sheet). If only a client name is given, find the
case folder the way the other Lingtu skills do and confirm with Klaus.

## Steps

1. **Read the finalized complaint** in full (it is the source of truth). Note any
   paragraph the client specifically must verify (e.g., a language-barrier / police-report
   paragraph, the incident facts) — call it out in the email.

2. **Produce a faithful Chinese translation → PDF ONLY.** Translate the whole complaint
   (caption, parties, jurisdiction, general allegations, causes of action, prayer).
   - Put a grey disclaimer at the top: 【中文译本 · 仅供客户核对】…正式版本以英文原件为准；如有出入，以英文原件为准。
   - CJK font: PingFang SC (set `w:eastAsia`); build docx → convert with
     `soffice --headless --convert-to pdf`.
   - **Deliver the PDF only — do NOT keep/give the `.docx`** (Klaus's standing preference).
   - Save to `~/Downloads/<Client>/` (and the case folder if it is materialized).

3. **Draft the bilingual client email — ENGLISH FIRST, then Chinese** (Klaus's format,
   2026-07). To the client; **always Cc Hernán (hernan.s@lingtulaw.com)** — mandatory on
   every client complaint-review email. From klaus@.
   - Attach the **English complaint + the Chinese translation** (gs-compress the PDFs if the
     combined base64 would blow the CLI arg limit — keep the whole draft under ~1 MB raw).
   - Ask the client to read carefully, confirm the facts are accurate, **specifically review
     the flagged paragraph(s)**, and either reply to confirm or tell us what to correct;
     say that once confirmed we will file with the court.
   - Client-facing tone: plain, warm, no markdown/bold, Chinese full-width punctuation
     (see [[feedback-client-message-plain]]).
   - Subject bilingual, e.g. `<Client> — Complaint (Final Version) for Your Review / <中文>案起诉状（定稿）请您核对`.
   - Build the draft in **klaus@** via `gws gmail users drafts create` (not the other Gmail MCP account).

4. **Deliver**: show Klaus the translation location + the drafted email text; leave the
   Gmail draft in klaus@ for him to review and send.

## Guardrails
- **DRAFT ONLY — never send.** Klaus sends every outbound email himself.
- **PDF only** for the translation — never hand Klaus the docx.
- **Always Cc Hernán** on the client email.
- **No fabrication** — faithful translation of what the complaint says; if the client flags
  a factual difference, route it to Hernán (do not silently change the complaint).
- Runs after the complaint is finalized; the filing itself is `file-complaint` /
  `dogbite-file-complaint`. See [[hernan-litigation-conventions]], [[hernan-email-tone]].
