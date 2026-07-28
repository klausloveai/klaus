# Draft LOR — install & usage

A Claude Code / Cowork **skill** that drafts a Letter of Representation (1P and/or 3P)
for Lingtu Law Office from the firm's Drive template + the case's intake sheet, and
delivers the PDF(s) to your Downloads for review. It only drafts — it does not send,
file, or touch the tracking sheet.

## Install

1. Unzip so the folder lives at:  `~/.claude/skills/draft-lor/`
   (the skill references `~/.claude/skills/draft-lor/scripts/...`, so keep this path).
2. Restart Claude Code / the Cowork app so the skill is picked up.
3. Verify it appears in your skills list as **draft-lor**.

## Prerequisites

- The **`gws` CLI** installed and authenticated as a firm Google account with access to:
  - the LOR template folder, the "PI Team Folder" Shared Drive, and the PI Master Sheet.
- **python3** (standard library only — no pip packages, no LibreOffice needed).

## Use

> "draft LOR for <client name>"   (defaults to BOTH 1P and 3P)
> "draft 3P LOR for <client name>"

The skill finds the case, auto-derives the signing case manager from the client's
tracking tab, fills the latest template, and drops the PDF(s) in `~/Downloads`.

## Contents

- `SKILL.md` — the workflow (what Claude follows)
- `scripts/read_intake.py` — reads LOR fields from the intake `.xlsx` (dependency-free)
- `scripts/fill_lor.py` — fills the template + strips placeholder highlight
- `references/firm-directory.md` — case-manager signatures + tab→manager map

## Note for recipients

The skill contains firm-specific IDs (Drive folder, Shared Drive, tracking sheet) and the
team directory — it's intended for internal Lingtu Law use. Update `references/firm-directory.md`
and the IDs in `SKILL.md` if anything changes.
