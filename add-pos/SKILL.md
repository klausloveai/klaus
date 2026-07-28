---
name: add-pos
description: |
  Prepare a California Proof of Service (POS) and attach a copy to the end of each
  attorney-signed document being e-served, for 凌图律所 / Lingtu Law Office (Law Office
  of Shenqi Cai APC), then run the full serve workflow. Use this skill whenever any of
  the following are mentioned: add POS, attach a proof of service, prepare POS, serve
  discovery/pleadings with a proof of service, "POS for these documents", e-serve these
  files, 加 POS, 做 proof of service, 出 POS, e-serve, "/add-pos" for a set of documents.
  Typical invocation: the user uploads the attorney-signed PDFs to e-serve (a case/client
  name + opposing counsel's DESIGNATED e-service email). The skill pulls the firm's Drive
  POS template ("POS Template.docx" — pleading format, double side-rules, line numbers,
  auto-date, {{tokens}}), appends a matching POS to EACH document, drops the results into
  a client-name folder in Downloads, drafts the e-serve email as a Gmail draft on klaus@
  with the PDFs attached, and WAITS for the user to review and say "send". Only after the
  user says send does it send, then set the response-deadline calendar event and invite
  Hernán + Cassie. It never sends or serves without the user's explicit "send". Always
  trigger for any "add a POS / prepare proof of service / e-serve these" request.
---

# Add Proof of Service (POS) + e-serve workflow

Attach a California electronic-service Proof of Service to a set of attorney-signed
documents, then run them through the firm's e-serve workflow. The firm POS template lives
in **Google Drive** (`POS Template.docx`, file id `19BhkRUm99mGnajKmAP-vaQCoFzfZnWCU`) — a
pleading-format POS with the firm's double side-rules, line numbers 1–28, a Word DATE
auto-field, and `{{tokens}}`. **Always pull it from Drive; never hand-rebuild it**
(reconstructing locally is how the format drifts — this was the lesson that created this skill).

## The finalized workflow (Klaus's exact steps)

When the user invokes `/add-pos` (or a trigger phrase) and uploads the attorney-signed
files, run this end to end:

1. **Add POS** to each uploaded attorney-signed file (the files needing e-serve).
2. **Client folder in Downloads** — create `~/Downloads/<Client Name>/` and put the
   POS'd files there (not loose in Downloads).
3. **Draft the e-serve email** as a Gmail draft on **klaus@** with the POS'd PDFs
   attached; show it to the user and **WAIT** — do not send until the user says "send"/"发".
4. **After the user says send** → send the draft, then **set a calendar deadline**
   (the responding party's due date) and **invite BOTH Hernán and Cassie**.

Steps 3 and 4 are hard gates: the email is only ever a draft until the explicit "send",
and the calendar is only created after the send actually happens.

## Golden rules (read first)

1. **One POS content, attached to each document.** All documents served in the same
   transmission share ONE POS body listing every document served. Attach a copy to the end
   of each document; the body is identical — only the footer title + page numbers change to
   match each host document.
2. **The attorney's signed documents are NOT re-signed or re-dated.** Their signature/
   verification date stays. Only the POS carries the **serve date** (= today, auto-filled)
   and the **declarant's** name (default: Klaus Liu; typed/conformed signature is fine for
   e-service).
3. **Serve ONLY to the DESIGNATED e-service address.** Opposing counsel's opening letter
   usually says service to any other address is invalid and the correspondence email does
   NOT accept service. The POS Service List lists **only the designated service address**.
   The correspondence email may be CC'd on the service *email* as courtesy, never as the
   service address.
4. **Date is automatic.** The template's date is a Word DATE field → fills to the serve
   day. Generate on the serve day. Never hardcode a date.
5. **Clean text, no overlay patching.** Fill the docx tokens and regenerate; never paste
   white boxes over a baked PDF.
6. **Right-margin gap** (~0.13") is applied so a long documents-served list never touches
   the right pleading rule.
7. **Draft, then gate on "send".** The email is created as a Gmail DRAFT only. Do NOT send,
   serve, or create the calendar until the user explicitly says "send"/"发". After sending,
   set the calendar and invite Hernán + Cassie.

## Inputs to collect (ask only for what's missing)

- **Case / client** — names the client folder and output files.
- **Documents to serve** — the uploaded attorney-signed PDFs (paths). For each, its
  **caption title** (the bold document title, used for that document's POS footer). Note
  the exact titles for the "documents served" list.
- **Set No.** (e.g., "One") if the documents are discovery sets.
- **Opposing counsel service block** — name + bar #, firm, address, phone, fax, and the
  **designated e-service email** (confirm from the opening letter — designated ONLY).
- **Case caption** — case name (short) + arbitration/court caption + claim/case no. (for
  carriers: Claim No. + Defense File No.).
- **Declarant** — who serves (default: Klaus Liu).
- **Serve date** — today (drives the calendar deadline in step 4).

## Steps

1. **Pull the template from Drive** into the client folder (run gws from inside the dir;
   `--output` must be relative):
   ```bash
   mkdir -p ~/Downloads/"<Client Name>" && cd ~/Downloads/"<Client Name>" && \
   gws drive files get \
     --params '{"fileId":"19BhkRUm99mGnajKmAP-vaQCoFzfZnWCU","alt":"media"}' \
     --output "POS Template.docx"
   ```
   (If the id ever fails, search Drive: `name='POS Template.docx'`.)

2. **Confirm the designated service address** against opposing counsel's opening letter.
   If two emails are given (service vs. correspondence), use ONLY the service one in the POS.

3. **Build the config JSON** (see `scripts/build_pos.py` docstring for the exact shape):
   - `outdir`: `~/Downloads/<Client Name>/` — the client folder (step-2 golden rule).
   - `documents_served_lines`: a LIST of every document served, one title per entry — the
     single source of truth (builds both the POS "documents served" line and the email body).
   - `set_no`, the service-list fields, `declarant`.
   - `documents[]`: one entry per document — `src` (the signed PDF) and `footer_title`
     (that document's own caption title). Output name auto-derives as
     `<original filename> (with POS).pdf`; page-number start is host page count + 1.
   - `email{}`: `claimant`, `service_desc`, `designated_letter_date`, `to` (the service
     address, or a LIST for multi-defendant), `cc`, and for carriers `claim_no` +
     `defense_file_no`.
   - `"create_draft": true` → after building the PDFs, the builder creates the Gmail draft
     on klaus@ with the POS'd PDFs attached and prints the draft id.

4. **Run the builder**:
   ```bash
   python3 ~/.claude/skills/add-pos/scripts/build_pos.py config.json
   ```
   It fills tokens, strips highlight, applies the right-margin gap, sets each document's
   footer + page start, appends the POS to each ORIGINAL document, writes the combined PDFs
   to the client folder named `<original> (with POS).pdf`, writes `service_email.txt`, and
   (with `create_draft`) creates the **Gmail draft** on klaus@ with the PDFs attached.
   (Set `"skip_build": true` to skip the PDFs and only produce the email.)

5. **Verify + present the draft**: the builder reports leftover tokens (none) and page
   counts. Spot-render one POS page to confirm footer title, page number, serve date, and
   the right-rule clearance; confirm the Service List shows only the designated address.
   Show the user the drafted email (subject/to/cc/body + attachments) and **STOP** — ask
   them to review and say "send" when ready.

6. **On "send" (explicit user approval only)**:
   - Send the Gmail draft:
     ```bash
     gws gmail users drafts send --params '{"userId":"me","id":"<DRAFT_ID>"}'
     ```
   - **Set the calendar deadline** = the responding party's response due date. For our
     discovery served on the other side by e-service: **serve date + 30 days + 2 court
     days** (skip weekends/court holidays; if it lands on a weekend, roll forward and flag
     it). This is the date to follow up if no responses arrive. Create it on Klaus's Google
     Calendar and **invite Hernán (`hernan.s@lingtulaw.com`) + Cassie (`cassie@lingtulaw.com`)**;
     default reminder 1 day before. Title convention: `<Case> — <what's due> Due`.

## Service-email conventions (per James Zhan, co-counsel)

- **Subject** = `[Case caption] / [what this email is]`. Carriers (State Farm, etc.):
  include **Claim No.** + **Defense File No.** → `[Case] | Claim No.: … | Defense File
  No.: … — Service of …` (carriers route by those).
- **To = ALL defense counsel in the case** (each defendant's attorney has a right to know).
  Pass `email.to` as a LIST of all designated service addresses; the builder joins them.
- **Different attachments per defendant → SEPARATE emails.** Run the skill once per
  defendant. One-respondent matters (e.g. a UM arbitration vs. State Farm) = a single email.
- Only the **designated service address(es)** count for service; correspondence-only emails
  go in `cc`.
- **Body default is simple/conversational** (the carrier IDs live in the subject; the POS
  attached to each document does the formal §1010.6 work). Klaus prefers this plain style.

## Notes / gotchas learned

- The template also exists as a **human-fill version** with `{{tokens}}` highlighted yellow;
  the builder strips highlight after filling, so either works — prefer plain `POS Template.docx`.
- Downloads may get tidied between steps; the client folder is the stable home for outputs.
- Deposition scheduling reminder: opposing counsel commonly requires the depo date to be
  **≥10 days after** the claimant's discovery responses are served.
- The default declarant/sender is Klaus (klaus@). gws default account = klaus@.
