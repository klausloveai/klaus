---
name: draft-lor
description: |
  Draft (do NOT send) a Letter of Representation (LOR) for 凌图律所 / Lingtu Law Office
  (Law Office of Shenqi Cai APC). Use this skill whenever any of the following are
  mentioned: draft LOR, draft a letter of representation, prepare an LOR, make an LOR,
  LOR draft, draft 1P/3P LOR, "/draft LOR" for a named client. Given a client name, the
  skill finds the case in Drive, determines the client's tracking sub-sheet and owning
  case manager (for the signature), reads the intake sheet, and renders the LOR PDF(s)
  from the latest Drive template for review. Defaults to drafting BOTH 1P and 3P unless
  the user specifies one. This skill ONLY drafts — it does not email, file, or update the
  tracking sheet (use the `lor-send` skill to send). Always trigger for any "draft LOR"
  request, even a partial one.
---

# Draft LOR — Letter of Representation (draft only)

Produce the LOR PDF(s) for review from the firm's Drive template, populated from the case's
intake sheet, with the signature auto-derived from the client's case manager. **Drafts only
— no email, no filing, no tracking-sheet update.** To send, use the `lor-send` skill.

Fully dependency-free and self-contained. Bundled helpers:
- `scripts/read_intake.py` — read LOR fields from the intake `.xlsx`
- `scripts/fill_lor.py` — fill template, strip yellow highlight
- `references/firm-directory.md` — CM signature + tab→CM mapping

## Inputs

- **Client** — the client/driver name (required; used to find the case + tracking row).
- **Type** — `1P`, `3P`, or **both** (DEFAULT = both 1P and 3P).

## Constants (same as lor-send)

- **LOR template folder:** `1QHz07DYO94ew2luwTbKF_AffmeNzPxHQ` → `3P LOR.docx`, `1P LOR.docx`.
  Always re-fetch the latest.
- **Shared Drive "PI Team Folder":** driveId `0ADBH3EXeXKRBUk9PVA`. Case folders named
  `Driver Name-M-D-YYYY`, containing the intake `.xlsx` (`<case name> Intake Sheet.xlsx`).
- **Tracking sheet "PI Master Sheet":** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`,
  tabs `Claims(Amos)`, `Piteam(Jerry)`, `Picase`.
- **Tab → case manager:** `Picase` → **Klaus Liu** (current), `Claims(Amos)` → **Amos Feng**,
  `Piteam(Jerry)` → **Jerry Piao** (see firm-directory.md for phone/email).
- **Scratch dir:** `~/lor_work` (`mkdir -p ~/lor_work`). `gws` rejects `-o`/`--upload` paths
  outside the current dir, and the Bash cwd resets between calls — always use absolute
  `$HOME/lor_work/...` paths, never `/tmp`. Strip the `Using keyring backend` banner before
  `json.loads` (slice from the first `{`).

---

## Step 1 — Find the case in Drive

```bash
mkdir -p ~/lor_work
DRV=0ADBH3EXeXKRBUk9PVA
gws drive files list --params '{"q":"name contains '\''<CLIENT>'\'' and mimeType='\''application/vnd.google-apps.folder'\'' and trashed=false","corpora":"drive","driveId":"'$DRV'","includeItemsFromAllDrives":true,"supportsAllDrives":true,"fields":"files(id,name)"}' --format json
```

If multiple folders match, show them and ask which case. Then list the case folder's children
to get the intake `.xlsx` id:

```bash
gws drive files list --params '{"q":"'\''<CASE_FOLDER_ID>'\'' in parents and trashed=false","supportsAllDrives":true,"includeItemsFromAllDrives":true,"fields":"files(id,name,mimeType)"}' --format json
```

## Step 2 — Determine tracking tab → case manager (signer)

Find the client in the `Client Name` column (col B) of the CM tabs to determine the owning
case manager (this becomes the letter's signature — no need to ask the user):

```bash
SS=1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM
for TAB in "Picase" "Claims(Amos)" "Piteam(Jerry)"; do
  gws sheets spreadsheets values get --params "{\"spreadsheetId\":\"$SS\",\"range\":\"$TAB!B1:B200\"}" --format json
done
```

Map the matching tab → case manager (Picase→Klaus Liu, Claims(Amos)→Amos Feng,
Piteam(Jerry)→Jerry Piao). Look the CM's phone/email up in `firm-directory.md`. If the client
is on no tab or several, ask the user which case manager to sign.

## Step 3 — Read the intake sheet

```bash
gws drive files get --params '{"fileId":"<INTAKE_XLSX_ID>","alt":"media","supportsAllDrives":true}' -o $HOME/lor_work/intake.xlsx
python3 ~/.claude/skills/draft-lor/scripts/read_intake.py $HOME/lor_work/intake.xlsx
```

Field → token mapping (same as lor-send):

| Token | 1P | 3P |
|---|---|---|
| `[Client Name]` / `[Client Name(s)]` | `client` | `client` |
| `[Date of Loss]` | `dol` → `Month D, YYYY` | same |
| `[Claim Number]` | `p1_claim` | `p3_claim` |
| `[Insured Name]` (3P only) | — | `p3_insured` |
| `[Policy Number]` | `p1_policy` | `p3_policy` |
| `[Case Manager Name]`/`[Phone Number]`/`[Email Address]` | from CM (Step 2) | same |

**Draft-stage missing values:** if `claim#`, `policy#`, or `insured` is blank in the intake
sheet, fill the token with `Pending` so the draft renders cleanly, and **flag each
`Pending` field in your summary** so the user fills it before sending. Convert DOL
`MM/DD/YYYY` → `Month D, YYYY`. Multi-client cases: confirm whether all clients go on one 3P
letter or just the named client.

## Step 4 — Render the requested draft(s)

For each requested type (default both), build `$HOME/lor_work/fields_<type>.json` with only
that template's tokens (3P adds `[Insured Name]`; 1P omits it), then:

```bash
FOLDER=1QHz07DYO94ew2luwTbKF_AffmeNzPxHQ
NAME="3P LOR.docx"   # and/or "1P LOR.docx"
TID=$(gws drive files list --params "{\"q\":\"'$FOLDER' in parents and name='$NAME' and trashed=false\",\"fields\":\"files(id)\",\"supportsAllDrives\":true,\"includeItemsFromAllDrives\":true}" --format json | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['files'][0]['id'])")
gws drive files get --params "{\"fileId\":\"$TID\",\"alt\":\"media\",\"supportsAllDrives\":true}" -o $HOME/lor_work/template_3P.docx

python3 ~/.claude/skills/draft-lor/scripts/fill_lor.py \
  $HOME/lor_work/template_3P.docx $HOME/lor_work/filled_3P.docx $HOME/lor_work/fields_3P.json

# Render PDF via Drive (convert → export → trash temp Doc)
# PDF name convention: `LOR - <Client> <DOL-dash> (<1P|3P>).pdf` — <DOL-dash> = intake DOL with
# `/`→`-`, no leading zeros (06/04/2026 → 6-4-2026), same as the case folder date. e.g.
# `LOR - Enyu Bai 6-4-2026 (1P).pdf`. Keeps same-name clients with multiple cases distinguishable.
DOCID=$(gws drive files create --upload $HOME/lor_work/filled_3P.docx \
  --upload-content-type application/vnd.openxmlformats-officedocument.wordprocessingml.document \
  --json '{"name":"__draftlor_tmp","mimeType":"application/vnd.google-apps.document"}' \
  --params '{"supportsAllDrives":true,"fields":"id"}' --format json \
  | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['id'])")
gws drive files export --params "{\"fileId\":\"$DOCID\",\"mimeType\":\"application/pdf\"}" \
  -o "$HOME/lor_work/LOR - <Client> <DOL-dash> (3P).pdf"
gws drive files delete --params "{\"fileId\":\"$DOCID\",\"supportsAllDrives\":true}"
```

`fill_lor.py` strips the yellow highlight and aborts on any unfilled `[token]`.

## Step 5 — Deliver the draft(s) for review

Copy the finished PDF(s) to the user's Downloads folder so they have the real files to open,
then show each rendered PDF (read it back):

```bash
cp "$HOME/lor_work/LOR - <Client> <DOL-dash> (1P).pdf" "$HOME/lor_work/LOR - <Client> <DOL-dash> (3P).pdf" ~/Downloads/ 2>/dev/null
```

Report:
- Client, DOL, the case manager/signer (and which tab it was derived from), carrier(s).
- Any fields rendered as `Pending` (claim#/policy#/insured) that need filling before sending.
- The delivered paths: `~/Downloads/LOR - <Client> <DOL-dash> (<type>).pdf`.

**Do NOT send, file to Drive, or update the tracking sheet** — that's the `lor-send` skill.
After delivering to Downloads, clear the scratch dir: `rm -rf ~/lor_work`.

## Notes

- Always re-fetch the template from Drive — the firm edits it; never cache.
- Signer is auto-derived from the tracking tab; only ask if the client isn't found or is on
  multiple tabs.
- "Your Insured" (3P) = the at-fault **policyholder** (`p3_insured` / intake L8).
- This skill is read-only against Drive/Sheets except for the throwaway temp Doc used for PDF
  conversion (created then immediately trashed).
