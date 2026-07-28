---
name: draft-lop
description: |
  Draft (do NOT send) a Letter of Protection (LOP) for 凌图律所 / Lingtu Law Office
  (Law Office of Shenqi Cai APC). Use this skill whenever any of the following are
  mentioned: draft LOP, draft a letter of protection, prepare an LOP, make an LOP,
  LOP draft, "/draft LOP" for a named client + provider. Given a client name and the
  treating provider's name, the skill finds the case in Drive, reads the intake sheet
  (client + date of loss), derives the signing case manager, and renders the LOP PDF
  from the latest Drive template for review. This skill ONLY drafts — it does not email,
  fax, file, or update any sheet (use the `send-lop` skill to send). Always trigger for
  any "draft LOP" request, even a partial one.
---

# Draft LOP — Letter of Protection (draft only)

Produce the LOP PDF for review from the firm's Drive template, populated from the case's
intake sheet (client + date of loss) and the provider name you give, with the signature
auto-derived from the case manager. **Draft only — no email, no fax, no filing.** To send,
use the `send-lop` skill.

A Letter of Protection goes to a **treating medical provider** (not an insurer): it tells
the provider the firm represents the client and asks them to treat + hold their bills, with
payment to come from the eventual settlement/judgment.

Fully dependency-free and self-contained. Bundled helpers:
- `scripts/read_intake.py` — read client + DOL from the intake `.xlsx`
- `scripts/fill_lop.py` — fill the template, strip the yellow highlight, stamp today's date
- `references/firm-directory.md` — CM signature + tab→CM mapping

## Inputs

- **Client** — the client/driver name (required; used to find the case + intake row).
- **Provider** — the treating provider's name as it should read on the letter (required;
  e.g. "Warm Springs Chiropractic"). LOP is provider-facing, so this is mandatory.
- **Case manager** — whose signature goes on the letter (e.g. "assigned to Amos"). If not
  given, derive from the client's tracking tab (see firm-directory.md); confirm if unsure.

## Constants

- **LOP template folder:** `1Uf8UNfArJjKVkqYMcSf7hwr3WXWO1riT` (the firm "templates" folder).
  The LOP file is **`3. - Letter of Protection.docx`** (id `1hIjalN6Nf-Efa7pXhgf5_TW8nHYhgzvj`),
  but the firm renumbers files — **always re-fetch by `name contains 'Letter of Protection'`**.
- **Shared Drive "PI Team Folder":** driveId `0ADBH3EXeXKRBUk9PVA`. Case folders named
  `Driver Name-M-D-YYYY`, containing the intake `.xlsx` (`<case name> Intake Sheet.xlsx`).
- **Tracking sheet "PI Master Sheet":** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`,
  tabs `Claims(Amos)`, `Piteam(Jerry)`, `Picase` — only used to auto-derive the signing CM.
- **Tab → case manager:** `Picase` → **Klaus Liu** (current), `Claims(Amos)` → **Amos Feng**,
  `Piteam(Jerry)` → **Jerry Piao** (see firm-directory.md for phone/email).
- **Scratch dir:** `~/lop_work` (`mkdir -p ~/lop_work`). `gws` rejects `-o`/`--upload` paths
  outside the current dir, and the Bash cwd resets between calls — always use absolute
  `$HOME/lop_work/...` paths, never `/tmp`. Strip the `Using keyring backend` banner before
  `json.loads` (slice from the first `{`).

## Template tokens

| Template token | Source |
|---|---|
| `[Client Name]` | intake `client` (C4). Multi-client → comma/and-joined; confirm with user |
| `[Date of Loss]` | intake `dol` (C2) → `Month D, YYYY` (e.g. `05/30/2026` → `May 30, 2026`) |
| `[Provider Name]` | the **Provider** input (appears in RE line + greeting) |
| `[Case Manager Name]` | signing CM full name (from directory) |
| `[Phone Number]` | CM direct line (from directory) |
| `[Email Address]` | CM team inbox (from directory) |

---

## Step 1 — Find the case in Drive

```bash
mkdir -p ~/lop_work
DRV=0ADBH3EXeXKRBUk9PVA
gws drive files list --params '{"q":"name contains '\''<CLIENT>'\'' and mimeType='\''application/vnd.google-apps.folder'\'' and trashed=false","corpora":"drive","driveId":"'$DRV'","includeItemsFromAllDrives":true,"supportsAllDrives":true,"fields":"files(id,name)"}' --format json
```

If multiple folders match, show them and ask which case. Capture the case folder id, then
list its children to get the intake `.xlsx` id:

```bash
gws drive files list --params '{"q":"'\''<CASE_FOLDER_ID>'\'' in parents and trashed=false","supportsAllDrives":true,"includeItemsFromAllDrives":true,"fields":"files(id,name,mimeType)"}' --format json
```

## Step 2 — Read the intake (client + DOL)

The intake is **either** an `.xlsx` (`<case> Intake Sheet.xlsx`, older cases) **or** a native
**Google Sheet** named like the case (`<Driver> - M/D/YYYY`, newer cases). Both use the same
layout — **C2 = Date of Loss, C4 = Driver/Client name**. Branch by the intake's `mimeType`:

```bash
# (A) native Google Sheet  → read C2 + C4 directly via the Sheets API
gws sheets spreadsheets values batchGet --params '{"spreadsheetId":"<INTAKE_ID>","ranges":["C2","C4"]}' --format json
#     C2 = DOL (e.g. 02/09/2026) ; C4 = client (e.g. Jiuxiang Teng)

# (B) .xlsx file  → download then parse
gws drive files get --params '{"fileId":"<INTAKE_ID>","alt":"media","supportsAllDrives":true}' -o $HOME/lop_work/intake.xlsx
python3 ~/.claude/skills/draft-lop/scripts/read_intake.py $HOME/lop_work/intake.xlsx
```

> `read_intake.py` only handles `.xlsx` — do NOT run it on a Google-Sheet intake (the
> `alt=media` download returns HTML). Use branch (A) for Google Sheets.

Use `client` and `dol`. Convert DOL to `Month D, YYYY`. For multi-client cases, confirm
whether all clients go on one letter.

## Step 3 — Resolve the signing case manager

Look the CM up in `references/firm-directory.md`: `[Case Manager Name]` = full name,
`[Phone Number]` = direct line, `[Email Address]` = team inbox. Use the CM named at
invocation; else derive from the client's tracking tab. If the CM isn't listed, ask for
their direct line + work email.

Build `$HOME/lop_work/lop_fields.json` with the six tokens above, e.g.:
```json
{"[Client Name]":"Jiu Xiang Teng","[Date of Loss]":"February 10, 2026",
 "[Provider Name]":"Warm Springs Chiropractic","[Case Manager Name]":"Jerry Piao",
 "[Phone Number]":"626-598-6352","[Email Address]":"piteam@lingtulaw.com"}
```

## Step 4 — Fetch the latest template & fill

```bash
FOLDER=1Uf8UNfArJjKVkqYMcSf7hwr3WXWO1riT
TID=$(gws drive files list --params "{\"q\":\"'$FOLDER' in parents and name contains 'Letter of Protection' and trashed=false\",\"fields\":\"files(id,name)\",\"supportsAllDrives\":true,\"includeItemsFromAllDrives\":true}" --format json | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['files'][0]['id'])")
gws drive files get --params "{\"fileId\":\"$TID\",\"alt\":\"media\",\"supportsAllDrives\":true}" -o $HOME/lop_work/lop_template.docx

python3 ~/.claude/skills/draft-lop/scripts/fill_lop.py \
  $HOME/lop_work/lop_template.docx $HOME/lop_work/lop_filled.docx $HOME/lop_work/lop_fields.json
```

`fill_lop.py` strips the yellow placeholder highlight and **aborts if any `[token]` is left
unfilled** — do not proceed past an error (a wrong token name in `lop_fields.json` is the
usual cause; fix the JSON, never hand-edit the docx).

## Step 5 — Render PDF (Drive convert → export → trash temp Doc)

```bash
DOCID=$(gws drive files create --upload $HOME/lop_work/lop_filled.docx \
  --upload-content-type application/vnd.openxmlformats-officedocument.wordprocessingml.document \
  --json '{"name":"__lop_tmp","mimeType":"application/vnd.google-apps.document"}' \
  --params '{"supportsAllDrives":true,"fields":"id"}' --format json \
  | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['id'])")
gws drive files export --params "{\"fileId\":\"$DOCID\",\"mimeType\":\"application/pdf\"}" \
  -o "$HOME/lop_work/LOP - <Client> - <Provider>.pdf"
gws drive files delete --params "{\"fileId\":\"$DOCID\",\"supportsAllDrives\":true}"
```

## Step 6 — Deliver the draft for review

```bash
cp "$HOME/lop_work/LOP - <Client> - <Provider>.pdf" ~/Downloads/
```

Tell the user the LOP draft is in `~/Downloads`, name the client + provider + DOL it was
built for, and remind them this is **draft-only** — nothing was sent or filed. To send it,
use the **send-lop** skill (provider email default; fax on explicit instruction).

## Notes & gotchas

- **Always re-fetch the template** from Drive each run — the firm edits it; never cache.
- The intake sheet is an `.xlsx` (not a Google Sheet); read it with `read_intake.py`.
- LOP needs only client + DOL + provider + signature — no insurer/policy/claim#.
- If `fill_lop.py` reports leftover placeholders, a token name was wrong — fix the JSON.
