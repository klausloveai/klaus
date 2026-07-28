---
name: send-lop
description: |
  Draft and send a Letter of Protection (LOP) for 凌图律所 / Lingtu Law Office
  (Law Office of Shenqi Cai APC). Use this skill whenever any of the following are
  mentioned: send LOP, send a letter of protection, LOP to provider, LOP to the clinic,
  protect the provider's bill, "/LOP" for a named client + provider. Typical invocation:
  a client name + the treating provider's name + the provider's email (or an explicit
  "fax it" instruction with a fax number). The skill finds the case in Drive, reads the
  intake sheet (client + date of loss), drafts the LOP from the latest Drive template,
  renders a PDF, shows it for approval, then sends it to the provider — **email by default,
  fax only on explicit instruction** — and files the PDF in the case folder's
  `1#Legal Documents`. It does NOT update any tracking sheet. Always trigger for any
  "send LOP" request, even a partial one.
---

# Send LOP — Letter of Protection

Draft an LOP from the firm's Drive template, populate it from the case's intake sheet
(client + date of loss) + the provider name you give, send it to the **treating provider**,
and file the PDF. A Letter of Protection asks the provider to treat the client + hold their
bills, with payment to come from the eventual settlement/judgment.

**Channel — email by default; fax only when explicitly instructed:**
1. **Email (default)** — the CM provides the **provider's email**; send a new email with the
   LOP PDF attached (Step 6A).
2. **Fax (only on explicit instruction)** — the CM says "fax it" + gives a fax number → fax
   via the bundled `send-fax` engine (Step 6B).
3. If neither an email nor a fax instruction is given, **ask** which to use (or fall back to
   delivering the PDF to Downloads as a draft and stop — no file).

File (Step 7) runs only after an actual send. **No tracking-sheet update** (unlike LOR).

Fully dependency-free — uses only the `gws` CLI (already authenticated) and bundled Python
helpers. No python-docx / LibreOffice needed; the template XML is edited in place so the
letterhead/formatting is preserved, and PDF rendering is done by Google Drive.

## Invocation inputs

- **Client** — the client/driver name (used to find the Drive case folder + intake row). Required.
- **Provider** — the treating provider's name as it should read on the letter. Required.
- **Delivery** — the **provider's email** (default channel) OR an explicit "fax it" + fax #.
  Required for an actual send (ask if missing).
- **Case manager** — whose signature goes on the letter (e.g. "assigned to Amos"). If not
  given, derive from the client's tracking tab; confirm if unsure.

## Constants

- **Send-from:** ALWAYS the connected `gws` account — whichever account is authenticated.
  Get it with `gws gmail users getProfile --params '{"userId":"me"}'`. Do NOT send as any
  other address (Gmail only allows verified send-as aliases; a different sender would bounce).
- **LOP template folder:** `1Uf8UNfArJjKVkqYMcSf7hwr3WXWO1riT`. The LOP file is
  **`3. - Letter of Protection.docx`** (id `1hIjalN6Nf-Efa7pXhgf5_TW8nHYhgzvj`) — the firm
  renumbers files, so **always re-fetch by `name contains 'Letter of Protection'`**.
- **Shared Drive "PI Team Folder":** driveId `0ADBH3EXeXKRBUk9PVA`. Case folders named
  `Driver Name-M-D-YYYY`, containing a `1#Legal Documents` subfolder and the intake `.xlsx`.
- **Tracking sheet "PI Master Sheet":** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`,
  tabs `Claims(Amos)`, `Piteam(Jerry)`, `Picase` — only to auto-derive the signing CM.
- **Signature directory:** `references/firm-directory.md` (CM → full name / direct line / inbox).
- **Fax engine:** `~/.claude/skills/send-fax/scripts/rc_fax.py` (RingCentral; creds in
  `~/.ringcentral.env`). Firm's own fax line: `626-240-2046`.
- **Scratch dir:** `~/lop_work` (`mkdir -p ~/lop_work`). `gws` rejects `-o`/`--upload` paths
  outside the current dir, and the Bash cwd resets between calls — use absolute
  `$HOME/lop_work/...` paths, never `/tmp`. Strip the `Using keyring backend` banner before
  `json.loads` (slice from the first `{`).

## Template tokens

| Template token | Source |
|---|---|
| `[Client Name]` | intake `client` (C4). Multi-client → comma/and-joined; confirm with user |
| `[Date of Loss]` | intake `dol` (C2) → `Month D, YYYY` |
| `[Provider Name]` | the **Provider** input (RE line + greeting) |
| `[Case Manager Name]` / `[Phone Number]` / `[Email Address]` | signing CM (from directory) |

---

## Step 1 — Find the case in Drive

```bash
mkdir -p ~/lop_work
DRV=0ADBH3EXeXKRBUk9PVA
gws drive files list --params '{"q":"name contains '\''<CLIENT>'\'' and mimeType='\''application/vnd.google-apps.folder'\'' and trashed=false","corpora":"drive","driveId":"'$DRV'","includeItemsFromAllDrives":true,"supportsAllDrives":true,"fields":"files(id,name)"}' --format json
```

If more than one folder matches, show them and ask which case. Capture the case folder id,
then list its children to get (a) the intake id (Google Sheet or `.xlsx` — see Step 2) and
(b) the **legal-documents subfolder** — its name starts with `1#` (e.g. `1#Legal Documents`
or `1#Folder-Retainer&LOR&HIPAA`; the exact suffix varies by case vintage):

```bash
gws drive files list --params '{"q":"'\''<CASE_FOLDER_ID>'\'' in parents and trashed=false","supportsAllDrives":true,"includeItemsFromAllDrives":true,"fields":"files(id,name,mimeType)"}' --format json
```

## Step 2 — Read the intake (client + DOL)

The intake lives in the case folder and is **either** an `.xlsx` (`<case> Intake Sheet.xlsx`,
older cases) **or** a native **Google Sheet** named like the case (`<Driver> - M/D/YYYY`,
newer cases). Both use the same layout — **C2 = Date of Loss, C4 = Driver/Client name**.
Pick the right branch by the intake file's `mimeType`:

```bash
# (A) native Google Sheet  → read C2 + C4 directly via the Sheets API
gws sheets spreadsheets values batchGet --params '{"spreadsheetId":"<INTAKE_ID>","ranges":["C2","C4"]}' --format json
#     C2 = DOL (e.g. 02/09/2026) ; C4 = client (e.g. Jiuxiang Teng)

# (B) .xlsx file  → download then parse
gws drive files get --params '{"fileId":"<INTAKE_ID>","alt":"media","supportsAllDrives":true}' -o $HOME/lop_work/intake.xlsx
python3 ~/.claude/skills/send-lop/scripts/read_intake.py $HOME/lop_work/intake.xlsx
```

> `read_intake.py` only handles `.xlsx` — do NOT run it on a Google-Sheet intake (the
> `alt=media` download returns HTML, not a spreadsheet). Use branch (A) for Google Sheets.

Use `client` and `dol` (→ `Month D, YYYY`). LOP ignores insurer/claim fields. For
multi-client cases, confirm whether all clients go on one letter.

## Step 3 — Resolve the signing CM + provider + channel

- **Signature** — look the CM up in `references/firm-directory.md` (full name / direct line /
  team inbox). Use the CM named at invocation; else derive from the client's tracking tab. If
  the CM isn't listed, ask for their direct line + work email.
- **Provider name** — from the invocation (mandatory; the letter is addressed to them).
- **Channel** — **email by default** (need the provider's email). If the user said "fax it",
  use fax (need a fax number). If neither the email nor a fax instruction is present, **ask**.

Build `$HOME/lop_work/lop_fields.json` with the six tokens (see table), e.g.:
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

python3 ~/.claude/skills/send-lop/scripts/fill_lop.py \
  $HOME/lop_work/lop_template.docx $HOME/lop_work/lop_filled.docx $HOME/lop_work/lop_fields.json
```

`fill_lop.py` strips the yellow highlight and **aborts on any unfilled `[token]`** — do not
proceed past an error.

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

## Step 6 — Approval, then send (MANDATORY approval)

Show the user the rendered PDF and the channel + recipient (provider email or fax #).
**Never send without explicit approval** — an LOP is outward-facing to a provider. Then use
the chosen branch.

### Step 6A — Email (DEFAULT)

Subject: `Letter of Protection — <Client>`. From = the connected account. Body
(`$HOME/lop_work/lop_body.txt`):
```
Hi <Provider name>,

Please find attached our Letter of Protection for <Client>. We ask that you continue the
necessary treatment and hold the bills until the resolution of the case, at which time
payment will be made from the settlement or judgment. Kindly send all billing to our office.

Thank you,
<Case Manager Name>
Lingtu Law Office | Law Office of Shenqi Cai APC
Direct: <direct phone>  |  <team inbox>
```

```bash
FROM=$(gws gmail users getProfile --params '{"userId":"me"}' --format json | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['emailAddress'])")
python3 ~/.claude/skills/send-lop/scripts/build_email.py \
  --to "<provider email>" --from "$FROM" \
  --subject "Letter of Protection — <Client>" \
  --body-file $HOME/lop_work/lop_body.txt \
  --attach "$HOME/lop_work/LOP - <Client> - <Provider>.pdf" \
  --attach-name "LOP - <Client> - <Provider>.pdf" \
  --out $HOME/lop_work/lop_msg.json
gws gmail users messages send --params '{"userId":"me"}' --json "$(cat $HOME/lop_work/lop_msg.json)" --format json
```

### Step 6B — Fax (ONLY on explicit instruction)

Cover = **Classic**; subject = `Letter of Protection — <Client>`; note = the cover text.

```bash
python3 ~/.claude/skills/send-fax/scripts/rc_fax.py \
  --to "<fax, +1XXXXXXXXXX>" \
  --to-name "<Provider>" \
  --subject "Letter of Protection — <Client>" \
  --note "Hi <Provider>, attached is our Letter of Protection for <Client>. Please continue treatment and hold the bills until case resolution; payment will follow from the settlement. Send all billing to our office. — <Case Manager Name>, Lingtu Law Office | Direct <phone>" \
  --attach "$HOME/lop_work/LOP - <Client> - <Provider>.pdf" \
  --cover Classic
```

The script polls and prints `{ok,id,status,pages}`; a trailing `Queued` is normal — report
the id + last status. Surface any `*Failed`/`Error`/`faxErrorCode`.

## Step 7 — File the sent PDF into the case folder

> Runs **only after an actual send** (6A or 6B). Upload the PDF into the case's
> legal-documents subfolder (the `1#…` folder found in Step 1):

```bash
gws drive files create --upload "$HOME/lop_work/LOP - <Client> - <Provider>.pdf" \
  --upload-content-type application/pdf \
  --json '{"name":"LOP - <Client> - <Provider>.pdf","parents":["<LEGAL_DOCS_FOLDER_ID>"]}' \
  --params '{"supportsAllDrives":true,"fields":"id,webViewLink"}' --format json
```

## Step 8 — Confirm & clean up

Report: channel (email / fax) + recipient, subject, the Gmail message id **or** fax id+status,
and the filed PDF link. (No tracking-sheet update for LOP.) Clean up: `rm -rf ~/lop_work`.

## Notes & gotchas

- **Always re-fetch the template** from Drive each run — the firm edits it; never cache.
- Default channel is **email** (LOP is usually a reply to a provider's request) — only fax
  when the user explicitly says so.
- The intake sheet is an `.xlsx` (not a Google Sheet); read it with `read_intake.py`.
- LOP needs only client + DOL + provider + signature — no insurer/policy/claim#.
- LOP does **not** touch the PI Master Sheet (unlike `lor-send`).
- If `fill_lop.py` reports leftover placeholders, a token name was wrong — fix the JSON;
  never hand-edit the docx.
