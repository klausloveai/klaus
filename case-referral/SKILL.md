---
name: case-referral
description: |
  Refer a PI case OUT to a partner firm in another state for 凌图律所 / Lingtu Law Office
  (Law Office of Shenqi Cai APC). Use whenever any of these are mentioned: case referral,
  refer this case out, refer to Morgan & Morgan / M&M / Bob / Babatunde, refer to Lowe Law,
  out-of-state case, "we're not licensed there", 转案, 转介案子给外所, 案子转出去,
  "/case-referral". Typical invocation: a client name (+ optionally which partner firm).
  The skill finds the case in Drive, reads the intake sheet + police report + scene photos,
  builds the firm's formatted **Lead Details** Word doc, combines the photos into ONE pdf,
  drafts a short cover email to the partner firm (Cc Cassie + Joe), and creates a Gmail
  DRAFT on klaus@ with all three attachments. DRAFT-ONLY — Klaus sends it himself. After the
  send, label the thread `🤝Lingtu Cases/Case Referral` and log the Activity Log row.
  Always trigger for any "refer this case out" request, even a partial one.
---

# Case Referral — refer a case out to an out-of-state partner firm

Sibling of `chiro-referral` / `pm-referral` / `mri-referral` — but those send a **medical**
referral to a clinic. This one hands an entire **case** to another law firm.
**DRAFT-ONLY: never send.** Klaus reviews and sends every referral himself.

## Invocation inputs
- **Case** — client/driver name (finds the Drive case folder).
- **Partner firm** — default **Morgan & Morgan / Babatunde ("Bob")**; see
  `references/partner-firms.md`. Lowe Law Group is the alternate — check their licensed-state
  list before routing there.
- Everything else is read from the case file.

## Constants
- Shared Drive **PI Team Folder** `0ADBH3EXeXKRBUk9PVA`. Case folder `<Client>-<M-D-YYYY>`
  → intake `.xlsx` + `1#Legal Documents` (intake zips), `2#Accident Info` (police card,
  scene photos), `3#Property Damage Claim`.
- **FROM = klaus@** (attorney-to-attorney; the case-mailbox rule does not apply here).
- **Cc = `"Shenqi Cai, Esq." <cassie@lingtulaw.com>` + `Joe Wu <joe@lingtulaw.com>`** — always.
- Gmail label: **`🤝Lingtu Cases/Case Referral`** (`Label_5720772518312974967`, purple #b99aff).
- Output folder: `~/Downloads/<Client> - <Firm> Referral/`.
- Scratch: session scratchpad.

---

## Step 1 — Find the case and pull the source material
Search the Shared Drive by client name. Watch for **two folders with the same client name**
(an older case and the new one) — disambiguate by the date in the folder name and confirm the
DOL with Klaus if it is not obvious. Then collect:
- the intake `.xlsx`
- `2#Accident Info` → police card, scene photos, insurance card, DL
- `1#Legal Documents` → intake zips (the ORIGINAL client photos usually live only in here;
  the `2#Accident Info` PDFs are compiled versions)

Zip filenames are mojibake — decode `cp437 → gbk` (see [[pi_intake_zip_extraction]]).

## Step 2 — Read the intake + the police report
Dump every populated cell of the intake sheet. Then **read the police card and the scene
photos with vision** — do not rely on the intake's party labels.

> **Mandatory cross-check.** The intake's "3P" column is filled by whoever hit our client, which
> is frequently *not* the at-fault driver in a multi-vehicle crash. Compare the damage patterns
> in the photos against the intake's 3P/Other-Party assignment. Broadside crush = struck;
> destroyed front end = striker. **If they disagree, stop and tell Klaus before drafting** — it
> changes which carrier matters and whether UM/UIM is the real recovery. This exact mismatch
> occurred on Bingcheng Ye (2026-09-18).

## Step 3 — Build the Lead Details doc
Fill a JSON against `references/lead-details-fields.md` (worked example:
`references/example-bingcheng-ye.json`), then:
```bash
python3 ~/.claude/skills/case-referral/scripts/build_referral_lead_details.py \
  "Lead Details - <Clients>.docx" data.json
```
Question set and field order are **Morgan & Morgan's — never change them**; only our formatting
is ours. Blank template: `assets/Lingtu Law - Case Referral Lead Details (TEMPLATE).docx`
(run the script with no JSON to regenerate it).

All the liability analysis belongs **here**, not in the email.

## Step 4 — Combine the photos into ONE pdf
```bash
python3 ~/.claude/skills/case-referral/scripts/combine_photos.py "Scene Photos.pdf" img1.jpg img2.jpg
```
- Scene / vehicle-damage photos → **one** `Scene Photos.pdf`. Never attach loose jpgs.
- **Police card / accident report stays its own attachment** — it is a document, not a photo.
- Video (dashcam etc.) attaches separately; mind Gmail's 25 MB cap.
- **Never attach** driver licenses, SSNs, insurance cards or the raw intake sheet — PII that the
  receiving firm gets only after they take the case.

## Step 5 — Draft the cover email
Follow `references/email-template.md` exactly. The three rules Klaus enforces:
1. **No liability analysis** — bare mechanism only; the doc and photos carry the argument.
2. **No fee percentage** — let them offer ([[referral_fee_never_quote_first]]).
3. **Short paragraphs**, one idea each, and state the ask (e.g. clients need provider
   recommendations in that state).

Signature = klaus@'s configured Gmail signature, fetched and appended verbatim — never typed.

## Step 6 — Create the Gmail DRAFT (never send)
Build a `multipart/mixed` MIME with the three attachments, write it to `draft.eml`, then:
```bash
gws gmail users drafts create --params '{"userId":"me"}' \
  --upload draft.eml --upload-content-type message/rfc822
```
To revise, **update the same draft id** (`gws gmail users drafts update`) — do not create a
second draft. Verify To/Cc/Subject/attachments afterwards with `drafts get`.

Show Klaus the rendered body + attachment list and **STOP**. Default is draft; there is no
auto-send path in this skill.

## Step 7 — After Klaus sends
1. **Label the thread** `🤝Lingtu Cases/Case Referral` via `threads.modify`.
2. **Activity Log** — one append-only row:
   `<date> | <time> | <Case> | 起草 | 转案给 <Firm>：Lead Details + 照片 PDF + police card，已发 <contact> | Klaus | <police report # / claim #> | Local | manual:case-referral | 等 <Firm> 回复是否接案`
3. Copy the packet into the case folder in Drive ([[feedback_always_file_to_case_folder]]).
4. Follow-up sits with the partner firm — no calendar deadline unless the case has a real one
   (SOL, government claim). If it does, put it in the **subject line** too.

## Never
- Never send. Never quote a fee. Never argue liability in the cover email.
- Never change M&M's field names or their order.
- Never assert fault as settled fact — attribute it ("scene photographs show…", "per client…").
