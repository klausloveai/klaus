# Draft LOP — install & usage

A Claude Code / Cowork **skill** that drafts a Letter of Protection (to a treating medical
provider) for Lingtu Law Office from the firm's Drive template + the case's intake, and
delivers the PDF to your Downloads for review. **Draft only** — it does not email, fax,
file, or touch any sheet. To send, use the `send-lop` skill.

## Install

1. Unzip so the folder lives at:  `~/.claude/skills/draft-lop/`
   (the skill references `~/.claude/skills/draft-lop/scripts/...`, so keep this path).
2. Restart Claude Code / the Cowork app so the skill is picked up.
3. Verify it appears in your skills list as **draft-lop**.

## Prerequisites

- The **`gws` CLI** installed and authenticated as a firm Google account with access to:
  the templates folder, the "PI Team Folder" Shared Drive, and the case intake.
- **python3** (standard library only — no pip packages, no LibreOffice needed).

## Use

> "draft LOP for <client>, provider <provider name>"
> "draft a letter of protection for Jiuxiang Teng to Warm Springs Chiropractic"

The skill finds the case, reads the intake (client + date of loss), auto-derives the signing
case manager, fills the latest template, and drops the PDF in `~/Downloads`.

## Contents

- `SKILL.md` — the workflow (what Claude follows)
- `scripts/read_intake.py` — reads client + DOL from an `.xlsx` intake (dependency-free)
- `scripts/fill_lop.py` — fills the template + strips placeholder highlight + stamps the date
- `references/firm-directory.md` — case-manager signatures + tab→manager map

## Note for recipients

The skill contains firm-specific IDs (template folder, Shared Drive, tracking sheet) and the
team directory — it's intended for internal Lingtu Law use. Update `references/firm-directory.md`
and the IDs in `SKILL.md` if anything changes.
