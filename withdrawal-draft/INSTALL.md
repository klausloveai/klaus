# Withdrawal Draft — install & usage

A Claude Code / Cowork **skill** that drafts a **Withdrawal of Representation** letter for
Lingtu Law Office from the firm's Drive template + the case's intake sheet, computes the
statute-of-limitations deadline (California 2-year default; web-searches the governing
state's PI SOL for out-of-state accidents), strips all yellow highlight so the letter is
ready to send, and delivers the PDF to your Downloads **and** the case folder root in
Drive. It drafts & files only — it does not email, fax, or mail the letter.

## Install

1. Unzip so the folder lives at:  `~/.claude/skills/withdrawal-draft/`
   (the skill references `~/.claude/skills/withdrawal-draft/scripts/...`, so keep this path).
2. Restart Claude Code / the Cowork app so the skill is picked up.
3. Verify it appears in your skills list as **withdrawal-draft**.

## Prerequisites

- The **`gws` CLI** installed and authenticated as a firm Google account with access to
  the `1. Templates` folder and the "PI Team Folder" Shared Drive.
- **python3** (standard library only — no pip packages, no LibreOffice needed).

## Use

> "draft withdrawal letter for <client name>"
> "withdraw from <client>'s case"   ·   "/withdrawal-draft <client>"

The skill finds the case, reads the intake sheet (name / address / DOL / accident
location), determines the SOL deadline, fills the latest template, drops the PDF in
`~/Downloads`, and uploads it to the case folder root ("lobby") in Drive.

## Contents

- `SKILL.md` — the workflow (what Claude follows)
- `scripts/read_intake.py` — reads client / address / DOL / accident location from the intake `.xlsx`
- `scripts/fill_withdrawal.py` — fills the template, computes the SOL deadline, strips highlight, stamps date
- `references/state-sol.md` — per-state PI SOL guidance (web-search-to-confirm for out-of-state)

## Note for recipients

The skill contains firm-specific IDs (Drive template + Shared Drive) — it's intended for
internal Lingtu Law use. The signature (Shenqi Cai, Esq.) and contact email
(`klaus@lingtulaw.com`) are baked into the Drive template, not the skill. Update the IDs in
`SKILL.md` if anything changes.
