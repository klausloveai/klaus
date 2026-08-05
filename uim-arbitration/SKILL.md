---
name: uim-arbitration
description: |
  Prepare and serve a UIM/UM (underinsured/uninsured motorist) ARBITRATION package for
  凌图律所 / Law Office of Shenqi Cai APC (Hernán Simó litigation line) — take the attorney's
  drafted Demand for Arbitration + discovery (RFP / SROG / RFA / Form Interrogatories DISC-001
  with its Sec. 4(a)(2) attachment) + cover letter, then: get the client to sign the workers'
  comp declaration, build the Proof of Service on the firm template for each document (correct
  §11580.2 service split), fill the DISC-001 form, normalize all dates to the service date,
  assemble the ready-to-serve set, and — on Klaus's go — draft the two service emails and the
  attorney status/confirmation reply and calendar the response deadlines. Use whenever any of
  these come up: "UIM arbitration", "UM arbitration", "Demand for Arbitration", "serve the
  arbitration demand and discovery", "prepare/serve discovery on the carrier in arbitration",
  "11580.2", "FROG/RFP/RFA/SROG for a UIM case", "/uim-arbitration" for a named case, or when
  Hernán sends a Demand-for-Arbitration + discovery package to prepare and serve. It PREPARES
  and DRAFTS only — it never mails, e-serves, e-files, or sends any email without Klaus's
  explicit approval (IOLTA-grade red line). Serves north-star goal ② (litigation → systematize
  → scale). See [[hernan-email]], [[pleading-template-and-contact-standard]], [[add-pos]].
---

# UIM / UM Arbitration — prepare & serve the Demand + discovery

End-to-end workflow to turn an attorney-drafted UIM arbitration package into a served set.
The attorney (Hernán) drafts the substantive documents; this skill does the client signature,
the proofs of service, the DISC-001 form fill, date normalization, assembly, and the
draft-only service emails + calendaring. **Never sends/mails/e-serves without Klaus's go.**

## 0. Inputs to gather first
From the attorney's email(s) and the case file, confirm:
- **Case / claim**: claimant name, insurer, claim no., policy no., date(s) of loss, UIM per-person + per-accident limits, the underlying 3P limit already exhausted.
- **Documents** (attorney-drafted): Cover Letter, Demand for Arbitration, Requests for Production, Special Interrogatories, Requests for Admission, Form Interrogatories **Attachment "Sec. 4(a)(2)"** (lists which DISC-001 boxes to check), and a blank fillable **DISC-001**.
- **Opposing counsel (OPC)**: firm, attorney name, address, phone, and **all known service emails** (Hernán's rule: list every known email to defeat non-delivery claims).
- **Insurer direct-service info**: insurer's address of record (from the certified policy dec page) + the **adjuster** name + phone + claims email.
- **Service date** = the ACTUAL day it goes in the mail / is e-served. Ask Klaus. Everything below is dated to this day.

⚠️ **Verify, don't invent**: pull the insurer address from the certified dec page, the OPC emails from the actual correspondence, the DISC-001 box list from the attorney's Sec. 4(a)(2) attachment. Never fabricate an address, email, SBN, or date.

## 1. The §11580.2 service split (the core rule — get this right)
Under **Ins. Code §11580.2(f)** the CCP Title 4 discovery tools apply to the arbitration.
Under **§11580.2(i)(1)(C)** the insured formally institutes arbitration by notifying **the insurer** in writing by **certified mail, return receipt requested**.

| Document | Serve on | Method |
|---|---|---|
| **Demand for Arbitration** | **BOTH** the insurer directly (Attn: adjuster, at its address of record) **AND** opposing counsel | certified mail RRR **+** e-mail |
| **All discovery** (RFP, SROG, RFA, FROG/DISC-001 + attachment) | **Opposing counsel only** (party is represented) | certified mail RRR + e-mail |
| **Cover Letter** | goes with the OPC package (it's addressed to OPC) | — |

So the served set = **two certified mailings = two green cards**: (1) OPC package (cover letter + Demand + all discovery), (2) insurer (Demand only). Keep both green cards + returned receipts in the file. "…to Tesla" in a document title just names the Respondent; it is NOT the service recipient.

## 2. Client signs the workers' comp declaration
The Demand contains a **declaration re workers' compensation** the **client** signs under penalty of perjury. Send via DocuSign (client's own email). Confirm the executed date fills the whole "Executed on ____, 20__" line (month + day, not just the day). This can be done before service; the declaration date ≤ service date is fine.

## 3. Build the Proof of Service (firm template, 3 modes)
Use `scripts/pos_kit.py` — it downloads the firm POS template (Drive id in the script), fills it, and builds the POS on the firm's pleading paper. **Set `SERVE_DATE` first** (it prints as the POS declaration date and must equal the real service date).

Modes (per document): `'opc'` (OPC only) · `'tesla'` (insurer only) · `'both'` (OPC + insurer row w/ adjuster).
- **Demand → `both`** · **all discovery → `opc`**.
- Every POS: check **By United States mail, certified mail, return receipt requested** + **By electronic mail**; list all known OPC emails; the insurer row carries `Attn: <adjuster>` + phone + claims email.
- Update the `COUNSEL`/`OUTSIDE` constants and the `service_rows()` blocks in the script per case (OPC name/firm/address/emails; insurer name/address/adjuster).

Two ways to attach the POS:
- **Discovery docx** (has an inline POS to replace) → `splice(src_docx, out_pdf, title, set_no, mode, page_break=True, fix_dated=True)`. `page_break=True` puts the POS on its own page and the Service List on its own page (house preference). `fix_dated=True` replaces the doc's auto-updating "Dated:" Word field with the static SERVE_DATE.
- **Signed Demand PDF** (already signed/flattened) → build the POS standalone with `build_standalone_pdf(out_pdf, title, '', mode='both')` and append it to the signed 6 pages with pypdf.

Convert docx→PDF with LibreOffice: `soffice --headless --convert-to pdf` (Google-conversion drops pleading rules — don't use it for these).

## 4. Fill the DISC-001 Form Interrogatories
DISC-001 is a **static XFA** court form (`dynamicRender=forbidden`). Do NOT drop XFA + set NeedAppearances (renders as tofu). Instead **update the XFA `datasets` packet** (Adobe reads it) AND set the AcroForm checkbox `/AS`+`/V` as a backstop, keeping XFA. `scripts/fill_disc001.py` maps every checkbox to its datasets path + on-state.
- **Boxes to check** = exactly the list in the attorney's Sec. 4(a)(2) attachment (e.g. Jiayu Ma: 1.1; 3.1–3.7; 4.1–4.2; 12.1–12.7; 13.1–13.2; 14.1–14.2; 15.1; 16.1–16.10; 17.1). Check nothing else.
- **Page-1 definition 4(a)**: check **(2)** ("INCIDENT includes the following…") and point it to the attachment — because the attachment supplies the custom INCIDENT definition.
- **Header / caption — firm arbitration standard** (verified against Zhiping Liu's DISC-001):
  - Attorney block: Hernán S. Simó (SBN 354175), LAW OFFICE OF SHENQI CAI APC, address, tel & fax (626) 479-2207, email hernan.s@ then klaus@.
  - Court line "SUPERIOR COURT OF CALIFORNIA, COUNTY OF" → fill with **"IN THE MATTER OF THE ARBITRATION BETWEEN"**.
  - SHORT TITLE = **"<Claimant last name> v. <Insurer short>"** (e.g. "Ma v. Tesla Ins. Co.").
  - **CASE NUMBER = blank** (arbitration has no court case no.).
  - Propounding = "Claimant <Name>"; Responding = "Respondent <Insurer>"; Set No. = **ONE**.
- **DISC-001 needs no separate POS** — it is served with the Sec. 4(a)(2) attachment, whose POS covers both. Serve the two files together (DISC-001 first, then attachment+POS). Merging them programmatically can break the XFA form — combine in Adobe if one file is wanted.

## 5. Normalize dates
Every POS declaration date, and every discovery doc's "Dated:" attorney line, = **SERVE_DATE**. Kill auto-updating Word DATE fields (they'd recompute to the open date). The client declaration and the attorney's own drafted dates stay as signed.

## 6. Assemble the ready-to-serve set
One folder (e.g. `~/Downloads/<Client>, final/`) with the correct mix:
- Cover Letter · **Demand = `both` version** · RFP/SROG/RFA = `opc` · FROG Attachment = `opc` (POS on own page) · DISC-001 (filled).
Spot-check each: correct recipients, certified+email checked, SERVE_DATE, no stray old dates.

## 7. Service (draft-only; Klaus executes)
Klaus mails the two certified packages himself. This skill then drafts (Gmail drafts, never sends):
- **Service email #1 → OPC** (all known OPC emails): "served herewith by e-mail and by certified mail RRR" + the full list; attach the whole set.
- **Service email #2 → insurer adjuster** (claims email; Attn: adjuster): the Demand only; cite §11580.2(i)(1)(C).
- Sent from klaus@ (the POS declarant) with Klaus's preset signature. Build multipart .eml with attachments and create via `gws ... drafts create --upload <eml> --upload-content-type message/rfc822`.

## 8. Calendar the deadlines (Google Calendar, remind 1 day before)
Once served:
- **Discovery responses due** = service date + 30 days + the CCP §§1013/1010.6 extension (mail +5 cal. days).
- **20-day date** for the insurer's response to the single-neutral-arbitrator demand (§11580.2(f); else petition LASC per CCP §1281.6).
Add attendees (Hernán / team) only if Klaus says so — adding guests sends invites.

## 9. Draft the attorney confirmation reply
Reply to Hernán (draft-only) confirming what was served, to whom, by what method, on what date; the two green cards kept; the calendared dates; and the status of any apportionment / outstanding-treatment follow-ups. Tone per [[hernan-email]].

## Red lines
- **Draft/prepare only.** No mailing, e-service, e-filing, or email send without Klaus's explicit approval.
- Never fabricate an address, email, SBN, date, or medical fact.
- POS date = actual service date (penalty-of-perjury). If service slips a day, re-date everything.
- Contact block on firm docs: tel & fax **(626) 479-2207**; email hernan.s@ then klaus@.
