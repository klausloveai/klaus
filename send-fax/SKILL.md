---
name: send-fax
description: |
  Send a fax via RingCentral for 凌图律所 / Lingtu Law Office. Use whenever any of the
  following are mentioned: send a fax, fax this, fax a document, fax to a number, fax
  the LOR/letter/records, "/fax", or any request to transmit a PDF by fax. The user
  provides a destination fax number plus a subject line (usually a claim #), an optional
  note, and an optional attachment (PDF). The skill renders a Classic cover page with the
  subject + note, attaches the file(s), sends via the RingCentral Fax API, and confirms
  delivery status. Always trigger for any "send/fax" request, even a partial one.
---

# Send Fax (RingCentral)

Transmit a fax through the firm's RingCentral account. Dependency-free — a single bundled
Python script (`scripts/rc_fax.py`, stdlib only) handles JWT auth, the multipart upload,
and delivery polling. Credentials live in `~/.ringcentral.env` (chmod 600).

## Inputs (collect these, ask only for what's missing)

- **Fax number** — destination, normalized to E.164 (`+1` + 10 digits). A bare
  `626-240-2046` / `6262402046` → `+16262402046`. **Required.**
- **Subject line** — short; usually the **claim #**. Goes on the cover page as `Re: …`.
  **Required.**
- **Note** — optional cover-page message (e.g. "Hi Adjuster, … please confirm receipt.").
- **Attachment** — optional path(s) to the PDF(s) to fax. If omitted, only the cover page
  is sent. Repeatable.
- **Cover page** — defaults to **Classic**. Other valid names: None, Ancient, Blank,
  Clasmod, Confidential, Contempo, Elegant, Express, Formal, Jazzy, Modern, Urgent.

## Constants

- **Credentials:** `~/.ringcentral.env` — `RC_CLIENT_ID`, `RC_CLIENT_SECRET`, `RC_JWT`,
  `RC_SERVER=https://platform.ringcentral.com` (production). App = "Demonstration App"
  under the Lingtu Law account, JWT auth flow, `Faxes` scope.
- **Engine:** `~/.claude/skills/send-fax/scripts/rc_fax.py`.
- **Firm fax line:** `626-240-2046` (`+16262402046`) — a safe self-test target.

## Step 1 — Normalize & preview

Normalize the fax number to E.164. Then **show the user a one-line preview and get explicit
confirmation before sending** — a fax is outward-facing:

> Fax → `+1XXXXXXXXXX` · cover **Classic** · Re: `<subject>` · note: `<note or —>` ·
> attach: `<filenames or none>`

## Step 2 — Send

```bash
python3 ~/.claude/skills/send-fax/scripts/rc_fax.py \
  --to "+1XXXXXXXXXX" \
  --subject "<subject / claim#>" \
  --note "<optional note>" \
  --attach "/abs/path/Doc.pdf" \
  --cover Classic
```

- Repeat `--attach` for multiple files (they concatenate in order after the cover page).
- Omit `--note` and/or `--attach` when not provided.
- The script auto-polls `message-store` for up to ~3 minutes and prints a JSON result:
  `{ok, id, status, pages, to, ...}`. `status` ends at `Sent` (success) or a `*Failed`/`Error`.
- Add `--no-poll` to fire-and-forget (returns immediately at `Queued`).

## Step 3 — Report

Report the message id, final status, and page count. If `status` is a failure (or a
`faxErrorCode` is present), surface it — common causes: not-a-fax-line / no answer
(`PhoneLineUnavailable`), or busy. Faxing to the firm's own line `+16262402046` is the
quickest way to prove the pipeline end to end.

## Notes

- **Subject vs. note:** the cover page only has one free-text area, so the script renders it
  as `Re: <subject>` followed by a blank line and the `<note>`. There is no separate fax
  "subject" field in the API.
- **E.164 only.** RingCentral rejects un-prefixed numbers; always add `+1` for US/Canada.
- This skill is also called by **lor-send** as its fax fallback (email primary → fax when no
  adjuster email).
- Setup details / how the credentials were provisioned: see memory `ringcentral_fax.md`.
