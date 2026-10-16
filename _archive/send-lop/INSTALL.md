# Send LOP — install & usage

A Claude Code / Cowork **skill** that drafts **and sends** a Letter of Protection to a
treating medical provider for Lingtu Law Office: it builds the PDF from the firm's Drive
template + the case intake, shows it for approval, then sends it — **email by default, fax
only on explicit instruction** — and files the PDF in the case folder. It does NOT update
any tracking sheet. To only draft (no send), use the `draft-lop` skill.

## Install

1. Unzip so the folder lives at:  `~/.claude/skills/send-lop/`
   (the skill references `~/.claude/skills/send-lop/scripts/...`, so keep this path).
2. Restart Claude Code / the Cowork app so the skill is picked up.
3. Verify it appears in your skills list as **send-lop**.

## Prerequisites

- The **`gws` CLI** installed and authenticated as a firm Google account with **`gmail.send`**
  (to email the provider) plus Drive/Sheets access to the templates folder, the "PI Team
  Folder" Shared Drive, and the case intake. (`gws auth status` should list `gmail.send`.)
- **python3** (standard library only).
- **Fax (optional path only):** if you'll ever send an LOP by fax, you also need the
  `send-fax` skill installed at `~/.claude/skills/send-fax/` and `~/.ringcentral.env`
  (the firm's RingCentral credentials, chmod 600). Email-only use does not need this.

## Use

> "send LOP for <client>, provider <provider name>, to <provider email>"
> "send a letter of protection for Jiuxiang Teng to Warm Springs Chiropractic, email billing@warmspringschiro.com"
> "fax the LOP for <client> to <provider> at <fax #>"   ← fax only when you say so

The skill finds the case, reads the intake (client + date of loss), drafts the LOP, renders
the PDF, **shows it for your approval**, then sends (email default / fax on request) and files
the PDF in the case's `1#…` legal-documents subfolder.

## Safety

- **Always pauses for explicit approval** before sending — an LOP is outward-facing.
- Sends only from the connected `gws` account (no spoofed senders).
- Files the sent PDF; does not modify the PI Master Sheet.

## Contents

- `SKILL.md` — the workflow (what Claude follows)
- `scripts/read_intake.py` — reads client + DOL from an `.xlsx` intake
- `scripts/fill_lop.py` — fills the template + strips highlight + stamps the date
- `scripts/build_email.py` — builds the email with the PDF attachment
- `references/firm-directory.md` — case-manager signatures + tab→manager map

## Note for recipients

Firm-specific IDs + directory are baked in — internal Lingtu Law use. Update
`references/firm-directory.md` and the IDs in `SKILL.md` if anything changes.
