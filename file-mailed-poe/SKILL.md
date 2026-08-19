---
name: file-mailed-poe
description: >-
  File a mailed letter, its USPS certified-mail receipt, or a returned envelope into the
  right Lingtu case folder — renamed to the firm's numbered house convention — for 凌图律所 /
  Law Office of Shenqi Cai APC (Hernán Simó dog-bite and litigation cases). Klaus drops the
  file(s) and calls this skill; it finds the case, works out whether each file is the letter,
  its receipt, or a return, gives it the correct number and name, moves it into
  "2. Legal Documents/Mailed POE", then reads the receipt for the certified-mail number and
  mailing date and writes that to the Case Log, the Activity Log, and the matching Google
  Task. Triggers: "归档这个回执", "把这个 POE 存进案件夹", "file this receipt", "存挂号回执",
  "这是退件", "备份进 case folder", "/file-mailed-poe", or simply dropping a POE / records-request
  letter, a green USPS certified-mail receipt, or a photo of returned mail and asking to file it.
  Covers preservation (POE/spoliation) letters AND agency records requests — anything that goes
  out by certified mail. It never deletes and never overwrites; anything ambiguous is left in
  place and raised with Klaus.
---

# File a Mailed Document / Receipt / Return into the Case Folder

Klaus mails a letter, keeps the green certified-mail receipt, and sometimes gets the
envelope back. All three belong in the case's `2. Legal Documents/Mailed POE` folder,
numbered so the letter and its proof of mailing sit together. This skill does the
filing, the renaming, and the logging.

## The house naming convention

Derived from the Weicong Lin folder (items 5+ are the current standard; items 1–4 use
an older `POE Receipt - <target>` form — do not copy that):

```
<N>. <Client> - <Document Name>.pdf              the letter that was mailed
<N>. <Client> - <Document Name> - Receipt.pdf    its USPS certified-mail receipt
<N>. <Client> - <Document Name> - Return.<ext>   the envelope, if it came back
```

**A receipt or a return reuses the number of the letter it belongs to.** Only a new
letter takes the next free number. Numbers are per case and never reused.

## ⚠️ Where Klaus can drop files

macOS blocks this tool from **reading** `~/Downloads` (writing there is fine). So a file
sitting in Downloads cannot be filed. Readable drop points:

- the **case folder itself** (the Drive mount is fully readable and writable), or
- `~/Desktop`, `~/Documents`, `/tmp`.

If Klaus points at something in `~/Downloads`, say so and ask him to move it to the
Desktop — do not silently fail or guess at the contents.

## Step 1 — Identify the case and the files

Get the client name from what Klaus said or from the filenames. The script resolves the
case folder itself; if the name is ambiguous it stops rather than guessing.

## Step 2 — Dry run the plan

```bash
python3 ~/.claude/skills/file-mailed-poe/scripts/file_poe.py \
  --case "Weicong Lin" --files "/path/a.pdf" "/path/b.jpg"
```

It prints, for each file: whether it read as **letter / receipt / return**, the number it
will take, and the exact destination name. It never writes without `--apply`.

Useful flags:
- `--attach-to N` — force a receipt/return onto letter N (use when the auto-match is
  wrong or the filenames share too few words; the script refuses to guess below a
  2-word overlap).
- `--name "…"` — set the document name explicitly, when the dropped filename is unhelpful.
- `--create-folder` — for a case that has no POE subfolder yet (some cases call it `POE`;
  the script finds either, and creates `Mailed POE` only when told to).
- `--move` — move instead of the default copy (default leaves Klaus's original alone).

**Show Klaus the plan and get his go before applying** — this writes into a live case
folder.

## Step 3 — Apply

Re-run with `--apply`. Existing destinations are skipped, never overwritten.

## Step 4 — Read the receipt, then log it

This is the part that makes the filing worth something later. Open the receipt (PDF or
photo — convert HEIC first: `sips -s format jpeg -Z 1100 in.HEIC --out out.jpg`, since
HEIC often exceeds the image read limit) and read off:

- the **certified-mail number** (20 digits, usually printed vertically up the left edge,
  grouped `9589 0710 5270 …`),
- the **date mailed** (the round USPS postmark and/or the typed date),
- the **addressee and address** as actually written on the receipt, and
- whether **Return Receipt** was purchased — the Extra Services boxes are often all
  `$0.00`, meaning there will be **no signed green card**, only tracking. Say so plainly;
  attorneys ask for the "return card" and it may not exist.

For a returned envelope, read the yellow USPS label — `UNCLAIMED`, `ATTEMPTED NOT KNOWN`,
`VACANT`, `INSUFFICIENT ADDRESS` — the reason changes what it means. "Unclaimed" means the
address was fine and nobody signed; check whether the same letter also went first-class
(the letter's own `VIA …` line says), because that copy was probably delivered.

Then write it down in the three places that survive the session
([[feedback-work-record-sources]]):

1. **Case Log** — the table embedded in the case's intake sheet at row 30+, newest first.
2. **Activity Log** — one appended row, per CLAUDE.md, with every Ref/ID captured
   (certified number, date mailed, recipient).
3. **The Google Task** for that item — update its notes, and complete it if the mailing
   closes it out.

## Guardrails

- **Never delete, never overwrite.** Copy by default; the original stays where Klaus put it.
- **Never invent a certified number or a mailing date** — read them off the receipt, and if
  the photo is unreadable, say so and ask for a better one.
- If a file cannot be confidently classified or matched to a letter, **leave it and ask**.
- One case at a time; never move a file between cases.
- Related: [[dogbite-file-patrol]] sorts loose files already sitting in a case-folder
  lobby into the numbered subfolders — this skill is the narrower, deliberate version for
  mailed documents and their proof of mailing.
