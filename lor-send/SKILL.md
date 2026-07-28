---
name: lor-send
description: |
  Draft and send a Letter of Representation (LOR) for 凌图律所 / Lingtu Law Office
  (Law Office of Shenqi Cai APC). Use this skill whenever any of the following are
  mentioned: send LOR, send a letter of representation, draft LOR, LOR to carrier,
  LOR to insurance, notify the adjuster of representation, first-party / third-party
  LOR, 1P LOR, 3P LOR, or "/LOR" for a named case. Typical invocation: a driver name
  to point to the case + which LOR (1P/3P) + the assigned case manager
  (e.g. "send 1P LOR for Guanghua Li, assigned to Amos"). The skill finds the case in
  Drive, reads the intake sheet, drafts the LOR from the latest Drive template, renders
  a PDF, shows it for approval, then sends it to the carrier — **by BOTH email and fax
  whenever both are on file** (one channel if only one exists) — files the PDF in the case
  folder, and logs it on the case-tracking sheet.
  Always trigger for any "send/draft LOR" request, even a partial one.
---

# Send LOR — Letter of Representation

Draft an LOR from the firm's Drive template, populate it from the case's intake sheet,
send it to the carrier, file the PDF, and log it on the tracking sheet.

**Channel — send by BOTH email AND fax (primary). Resolve email+fax from the INTAKE first,
then the "insurance list" directory (Step 3):**
1. **Email (Step 6A)** — if an email is on file (intake adjuster email, else the list email),
   email it.
2. **Fax (Step 6B)** — if a fax is on file (intake `p1_adjuster_fax`, else the list
   `LOR Fax Number`), ALSO fax it (RingCentral, via the bundled `send-fax` engine).
3. **Both available → do BOTH** (this is the normal/primary path — email *and* fax). Only one
   on file → send that one. **Neither on file → do nothing** (no send, no draft) — tell the
   user and stop (Step 6C).

File + log (Steps 7–8) run after any actual send (email and/or fax).

Fully dependency-free — uses only the `gws` CLI (already authenticated) and the bundled
Python helpers. No python-docx / LibreOffice needed; the template's XML is edited in place
so letterhead and formatting are preserved, and PDF rendering is done by Google Drive.

## Invocation inputs

From the user's request, determine:
- **Case** — the driver/client name (used to find the Drive case folder).
- **Type** — `1P` (client's own carrier: UM/UIM/MedPay) and/or `3P` (at-fault carrier).
- **Case manager** — whose signature goes on the letter (e.g. "assigned to Amos").

Ask only for whichever of these is missing.

## Constants

- **Send-from = the CASE-RESPONSIBLE team inbox, NOT a personal address** (firm rule). Map the
  case's tracking tab → team inbox via [[firm-directory]]: **`Picase@` → `picase@lingtulaw.com`**,
  `Claims@` (Amos) → `claims@lingtulaw.com`, `Piteam@` (Jerry) → `piteam@lingtulaw.com`. Never
  send an LOR from `klaus@…` (a personal box) just because that's the connected account.
  **Technical method:** send **through the team inbox's own `gws` store** so the From is
  genuinely that inbox — prefix gmail commands with
  `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-<inbox> GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-<inbox>/credentials.json`
  (stores exist for `gws-picase`, `gws-claims`, `gws-piteam`). No send-as alias needed.
  **But the email's signature = the INVOKING user's own Gmail signature** (the skill-runner's,
  e.g. Klaus's) — NOT the team inbox's — fetched from the invoker's **default** `gws` store
  (`settings.sendAs.signature`, HTML); never compose one (Step 6A). So: **From = team inbox,
  Gmail signature = whoever ran the skill, LOR letter signature = the case's CM** (three
  independent identities). If the team inbox's store isn't set up on the machine, **STOP and
  tell the user** (don't send from a personal box).
- **LOR template folder:** `1QHz07DYO94ew2luwTbKF_AffmeNzPxHQ` (`0. LOR Templates`). It holds
  **one subfolder per team** — `Picase@`, `Claims@`, `Piteam@` — and each contains that team's
  own `1P LOR - <CM>.docx` / `3P LOR - <CM>.docx` (the letterhead **fax number is that CM's
  direct line**, which is why the template is per-team). **There are no root-level masters** —
  always pick the subfolder matching the case's tracking tab, and match the file by the
  `<1P|3P> LOR` name pattern (never hardcode the CM's name — it changes with staffing).
  Always re-fetch the latest.
- **Shared Drive "PI Team Folder":** driveId `0ADBH3EXeXKRBUk9PVA`. Case folders are named
  `Driver Name-M-D-YYYY` and contain a `1#Legal Documents` subfolder and the intake
  `.xlsx` (`<case name> Intake Sheet.xlsx`).
- **Tracking sheet "PI Master Sheet":** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`.
  CM tabs: `Claims(Amos)`, `Piteam(Jerry)`, `Picase`. **Tab layouts differ — always read
  the live header row** (see Step 8).
- **Carrier directory:** the **`insurance list`** tab in the same PI Master Sheet —
  columns `Insurance Name | Phone Number | Email | LOR Fax Number | …`. Source for the
  carrier's LOR fax + claims email. Matched by insurer name via `scripts/match_carrier.py`.
- **Signature directory:** `references/firm-directory.md` (case manager → name / direct
  phone / work email).
- **Fax engine:** `~/.claude/skills/send-fax/scripts/rc_fax.py` (RingCentral; creds in
  `~/.ringcentral.env`). Firm's own fax line: `626-240-2046`.

> The `gws` JSON output is prefixed with a `Using keyring backend: keyring` banner line —
> strip everything before the first `{` before `json.loads`, or write to a file and slice.
> **`gws` rejects `-o`/`--upload` paths outside the current directory** (and the Bash cwd
> resets between calls). Use a scratch dir under `$HOME` — this skill uses `~/lor_work`
> (`mkdir -p ~/lor_work`) and absolute `$HOME/lor_work/...` paths everywhere, never `/tmp`.

---

## Step 1 — Find the case in Drive

Search the Shared Drive for the case folder by driver name:

```bash
DRV=0ADBH3EXeXKRBUk9PVA
gws drive files list --params '{"q":"name contains '\''Guanghua Li'\'' and mimeType='\''application/vnd.google-apps.folder'\'' and trashed=false","corpora":"drive","driveId":"'$DRV'","includeItemsFromAllDrives":true,"supportsAllDrives":true,"fields":"files(id,name)"}' --format json
```

If more than one folder matches, show them and ask which case. Capture the case folder id.
Then list its children to get (a) the intake `.xlsx` id and (b) the `1#Legal Documents`
subfolder id:

```bash
gws drive files list --params '{"q":"'\''<CASE_FOLDER_ID>'\'' in parents and trashed=false","supportsAllDrives":true,"includeItemsFromAllDrives":true,"fields":"files(id,name,mimeType)"}' --format json
```

## Step 2 — Read the intake sheet

```bash
gws drive files get --params '{"fileId":"<INTAKE_XLSX_ID>","alt":"media","supportsAllDrives":true}' -o $HOME/lor_work/intake.xlsx
python3 ~/.claude/skills/lor-send/scripts/read_intake.py $HOME/lor_work/intake.xlsx
```

This returns client, DOL, and 1P/3P insurer, policy#, insured (3P), claim#, adjuster,
adjuster email. **Claim # and adjuster fields are often blank at LOR stage** — that is
expected; you'll collect them in Step 3.

Field → template token mapping:

| Template token | 1P source | 3P source |
|---|---|---|
| `[Client Name]` / `[Client Name(s)]` | `client` | `client` |
| `[Date of Loss]` | `dol` → `Month D, YYYY` | same |
| `[Claim Number]` | `p1_claim` | `p3_claim` |
| `[Insured Name]` (3P only) | — | `p3_insured` |
| `[Policy Number]` | `p1_policy` | `p3_policy` |
| `[Case Manager Name]` / `[Phone Number]` / `[Email Address]` | from directory by CM | same |

Convert DOL from `MM/DD/YYYY` to `Month D, YYYY` (e.g. `05/30/2026` → `May 30, 2026`).
For multi-client cases, confirm with the user whether all clients go on one 3P letter
(`[Client Name(s)]` = comma/and-joined) or just the named client.

## Step 3 — Resolve channel (carrier directory), claim #, signature

**Channel decision — INTAKE first, then the insurance list, else DO NOTHING.** Resolve the
carrier's fax + email from two sources and **always prefer the intake sheet's value** (it's
case-specific), only falling back to the `insurance list` directory:

| | intake (preferred) | fallback |
|---|---|---|
| **Fax** | `p1_adjuster_fax` (I22) for 1P · (intake has no 3P fax cell) | insurance-list `LOR Fax Number` |
| **Email** | `p1_adjuster_email` (I18) · `p3_adjuster_email` (L22) | insurance-list email |

Only hit the directory for whatever the intake is missing:
```bash
SS=1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM
gws sheets spreadsheets values get --params "{\"spreadsheetId\":\"$SS\",\"range\":\"insurance list!A1:Z200\"}" --format json > $HOME/lor_work/ins.json
python3 ~/.claude/skills/lor-send/scripts/match_carrier.py "<intake insurer for this type>" $HOME/lor_work/ins.json
# -> {"matched": "...", "fax": "+1...|null", "email": "...|null"}
```

Final values: **email = intake email if present, else list email**; **fax = intake fax if
present, else list fax**. Treat blank / `Pending` / a Mercury `MyClaim+<claim#>@…` template
with no real claim # as "not present". Then decide — **send through every channel that exists**:
1. **email available → EMAIL it** (Step 6A).
2. **fax available → ALSO FAX it** (Step 6B). Both 1 and 2 fire when both are on file — that's
   the normal primary path (email **and** fax for redundancy).
3. **neither email NOR fax (in EITHER intake or the list) → DO NOTHING.** Do not send, do not
   draft-to-Downloads — tell the user there's no email/fax on file for this carrier and stop
   (Step 6C; Steps 7–8 also skip).

If the user explicitly asks for one channel only ("email only" / "fax only"), honor that instead.

- **Claim #** — needed for the subject/cover. If blank in intake, **ask the user.**
- **Greeting name** — adjuster name (`p1_adjuster`/`p3_adjuster`) if present, else "Adjuster".
- **Signature** — look the case manager up in `references/firm-directory.md`:
  `[Case Manager Name]` = full name, `[Phone Number]` = direct line, `[Email Address]` =
  work email. (For draft-style runs the CM comes from the client's tracking tab; for an
  explicit "assigned to X" use X.) If the CM isn't listed, ask for their direct line + email.

Build `$HOME/lor_work/lor_fields.json` with only the tokens the chosen template uses (see the token
table in the original test; 3P adds `[Insured Name]`, 1P omits it).

## Step 4 — Fetch the latest template & fill

The template is **per-team**: pick the subfolder matching the case's tracking tab, then take
that team's `1P`/`3P` file by name pattern (do NOT hardcode the CM's name).

```bash
FOLDER=1QHz07DYO94ew2luwTbKF_AffmeNzPxHQ   # 0. LOR Templates
TEAM="Picase@"        # case's tracking tab → "Picase@" | "Claims@" | "Piteam@"
TYPE="1P"             # or "3P"

# 1) that team's template subfolder
SUB=$(gws drive files list --params "{\"q\":\"'$FOLDER' in parents and name='$TEAM' and mimeType='application/vnd.google-apps.folder' and trashed=false\",\"fields\":\"files(id)\",\"supportsAllDrives\":true,\"includeItemsFromAllDrives\":true}" --format json | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['files'][0]['id'])")

# 2) that team's template for this type — "<TYPE> LOR - <CM>.docx"
TID=$(gws drive files list --params "{\"q\":\"'$SUB' in parents and name contains '$TYPE LOR' and trashed=false\",\"fields\":\"files(id,name)\",\"supportsAllDrives\":true,\"includeItemsFromAllDrives\":true}" --format json | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['files'][0]['id'])")

gws drive files get --params "{\"fileId\":\"$TID\",\"alt\":\"media\",\"supportsAllDrives\":true}" -o $HOME/lor_work/lor_template.docx

python3 ~/.claude/skills/lor-send/scripts/fill_lor.py \
  $HOME/lor_work/lor_template.docx $HOME/lor_work/lor_filled.docx $HOME/lor_work/lor_fields.json
```

`fill_lor.py` **strips the yellow placeholder highlight** (so the official letter is clean)
and **aborts if any `[token]` is unfilled** — do not proceed past an error.

## Step 5 — Render PDF (Drive convert → export → trash temp Doc)

**PDF filename convention:** `LOR - <Client> <DOL-dash> (<1P|3P>).pdf`, where `<DOL-dash>` is the
intake DOL with `/`→`-` and **no leading zeros** (e.g. `06/04/2026` → `6-4-2026`) — same date
format as the case folder name. Example: `LOR - Enyu Bai 6-4-2026 (1P).pdf`. This makes the
fax-success forwarder able to disambiguate same-name clients with multiple cases. For a
multi-client 3P letter, use the named/first client + that case's DOL.

```bash
DOCID=$(gws drive files create --upload $HOME/lor_work/lor_filled.docx \
  --upload-content-type application/vnd.openxmlformats-officedocument.wordprocessingml.document \
  --json '{"name":"__lor_tmp","mimeType":"application/vnd.google-apps.document"}' \
  --params '{"supportsAllDrives":true,"fields":"id"}' --format json \
  | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['id'])")
gws drive files export --params "{\"fileId\":\"$DOCID\",\"mimeType\":\"application/pdf\"}" \
  -o "$HOME/lor_work/LOR - <Client> <DOL-dash> (1P).pdf"
gws drive files delete --params "{\"fileId\":\"$DOCID\",\"supportsAllDrives\":true}"
```

## Step 6 — Approval, then send (MANDATORY approval)

Show the user the rendered PDF and **every channel + recipient** that will be used (email
address AND fax #) + subject. **Never send without explicit approval** — an LOR is
outward-facing to a carrier. On approval, run **BOTH branches that apply**: **6A email** and
**6B fax** — when both an email and a fax are on file, do both (the normal path); when only one
is on file, do just that one. If neither was found, **do nothing** (6C) — already decided in
Step 3.

### Step 6A — Email (send when the carrier has a claims email — usually together with 6B fax)

**From = the case-responsible team inbox** (tab→inbox: `Picase@` → `picase@`, `Claims@` →
`claims@`, `Piteam@` → `piteam@`). Send **THROUGH that inbox's own gws store** so the From is
genuinely that inbox (no send-as alias needed):
`GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-<inbox>` (e.g. `gws-picase`, `gws-claims`,
`gws-piteam`) `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-<inbox>/credentials.json`.
If that store isn't set up on the machine, STOP and tell the user (don't fall back to a
personal box).

Subject: `Claim No. <claim#>`.

**Signature: DO NOT compose it — use the INVOKING user's own Gmail signature** (the person
running the skill, e.g. Klaus), **NOT the team inbox's**. Fetch it from the invoker's
**default** `gws` store (no `CONFIG_DIR` override) and build an **HTML** email (the signature
is HTML with the firm logo + footer):
```bash
# signature = the invoker's OWN (default gws store, e.g. klaus@) — NOT the team inbox's
gws gmail users settings sendAs list --params '{"userId":"me"}' --format json   # -> sendAs[].signature
```
Build a `multipart/mixed` MIME inline (Python `email.mime`): a `text/html` part =
`<div dir="ltr">Hi Adjuster,<br><br>LOR attached for your review, and please confirm receipt.</div>`
**+ the fetched signature HTML**; plus the LOR PDF attachment(s); base64url-encode →
`{"raw": ...}`. (`build_email.py` is plain-text only — don't use it here; the configured
signature is HTML.) Then send **through the team-inbox store** (so From = the team inbox, even
though the signature is the invoker's):
```bash
CFG=$HOME/.config/gws-<inbox>   # the case's team-inbox store (e.g. gws-picase)
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$CFG GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$CFG/credentials.json \
  gws gmail users messages send --params '{"userId":"me"}' --json '{"raw":"<RAW>"}' --format json
```
Attach the 1P and 3P PDFs together if both are being emailed. Capture the returned message id.

### Step 6B — Fax (send when the carrier has an LOR fax # — usually together with 6A email)

Fax via the `send-fax` engine **even if 6A already emailed it** (email + fax both go out when
both are on file). Cover = **Classic**; **subject = the claim #**; note = LOR cover text.

```bash
python3 ~/.claude/skills/send-fax/scripts/rc_fax.py \
  --to "<fax from match_carrier, +1XXXXXXXXXX>" \
  --to-name "<matched carrier> Claims" \
  --subject "Claim No. <claim#>" \
  --note "Hi Adjuster, LOR attached for your review, and please confirm receipt. — <Case Manager Name>, Lingtu Law Office | Direct <phone>" \
  --attach "$HOME/lor_work/LOR - <Client> <DOL-dash> (3P).pdf" \
  --cover Classic
```

- Repeat `--attach` to fax 1P and 3P together (cover first, then each PDF in order).
- The script polls and prints `{ok,id,status,pages}`. It may still read `Queued` if the poll
  window closes before RingCentral flips it to `Sent` — that's normal; report the id + last
  status. Surface any `*Failed`/`Error`/`faxErrorCode`.

### Step 6C — Neither email nor fax → DO NOTHING

If no email AND no fax was found in either the intake or the insurance list (Step 3.3), **do
nothing**: do not send, do not deliver a draft. Tell the user there's no email/fax on file for
this carrier and ask them to add one to the intake / insurance list if they want it sent. Skip
Steps 7–8.5. (The rendered PDF stays in `~/lor_work` until cleanup; don't drop it to Downloads.)

## Step 7 — File the sent PDF into the case folder

> Steps 7–8 run **only after an actual send** (email 6A or fax 6B). Skip both for draft-only (6C).

Upload the PDF (NOT converted) into the case's `1#Legal Documents` subfolder for the record
(the PDF is already under `~/lor_work`, so no copy is needed):

```bash
gws drive files create --upload "$HOME/lor_work/LOR - <Client> <DOL-dash> (3P).pdf" \
  --upload-content-type application/pdf \
  --json '{"name":"LOR - <Client> <DOL-dash> (3P).pdf","parents":["<LEGAL_DOCS_FOLDER_ID>"]}' \
  --params '{"supportsAllDrives":true,"fields":"id,webViewLink"}' --format json
```

## Step 7.5 — Label the sent LOR email (EMAIL channel only)

> Only for the **email** channel (Step 6A). Skip for fax (6B) and draft-only (6C) — there's no
> sent email to tag.

After the email goes out, tag the sent message **in the same team-inbox `gws` store it was
sent from** so the case is easy to find: apply the **case's Gmail label** (the one combined
label per case, by client name — never a per-client/sub-label, see
[[feedback-case-label-one-per-case]]) **+ `INBOX`** (so it surfaces in the inbox, not just
Sent) **+ `STARRED`**.

```bash
CFG=$HOME/.config/gws-picase   # the case's team-inbox store (same one used to send)
# find the case label id by client name (exact match on the combined case label)
LBL=$(GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$CFG GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$CFG/credentials.json \
  gws gmail users labels list --params '{"userId":"me"}' --format json 2>/dev/null \
  | python3 -c "import sys,json;s=sys.stdin.read();d=json.loads(s[s.index('{'):]);print(next((l['id'] for l in d['labels'] if l['name']=='<Client>'),''))")
# apply case label + INBOX + STARRED to the sent message (id captured in Step 6A)
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$CFG GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$CFG/credentials.json \
  gws gmail users messages modify --params "{\"userId\":\"me\",\"id\":\"<SENT_MSG_ID>\"}" \
  --json "{\"addLabelIds\":[\"$LBL\",\"INBOX\",\"STARRED\"]}" --format json
```

If the case label doesn't exist in that inbox, surface it and ask (don't create a new variant).

## Step 8 — Log it on the tracking sheet (no color change)

**The case's tracking row is NOT necessarily on the signing CM's tab** — the case manager
who signs the letter is independent of which tab tracks the case (e.g. Guanghua Li signs
under Amos but is tracked on `Picase`). So **find the row by client name**, don't assume
CM→tab:

1. **Locate the case row.** Search the CM tabs (`Claims(Amos)`, `Piteam(Jerry)`, `Picase`)
   for the client in the `Client Name` column (col B). Read each candidate tab's live header
   row to map columns. If the client appears on exactly one tab, use it; if on none or
   several, ask the user which tab/row.
2. **Find the LOR column(s)** from that tab's live headers and **write the sent date with NO
   formatting change** — `values update` (`valueInputOption: USER_ENTERED`), never a
   formatting `batchUpdate`:

   - **Separate `1LOR` / `3LOR` columns** (e.g. `Picase`: `1LOR`=col F, `3LOR`=col I): put
     the date in the matching column (`1P`→`1LOR`, `3P`→`3LOR`). **Match the existing format
     in that column — Picase uses bare `M/D`** (e.g. `5/30`), not `M/D/YYYY`. Replaces `P`.
   - **Single `LOR Status` column** (e.g. `Claims(Amos)`, col E): use the firm's shorthand
     `M/D(s)1P` or `M/D(s)3P` (the `(s)` = sent). If both sent the same day, write
     `M/D(s)1P&3P`. **If the cell already holds a prior LOR entry, do not clobber it** —
     show the existing value and confirm whether to combine (e.g. `3/31(s)1P&3P`) or append.

   ```bash
   # Picase example: 3P LOR sent 5/30 for the client in row 3 → 3LOR is col I
   gws sheets spreadsheets values update \
     --params '{"spreadsheetId":"1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM","range":"Picase!I3","valueInputOption":"USER_ENTERED"}' \
     --json '{"values":[["5/30"]]}'
   ```
3. Show the user the exact cell + value before writing; confirm if overwriting anything.

## Step 8.5 — Notify the team in the case Chat space (after an actual send)

> Runs **only after an actual send** (email 6A / fax 6B), like Steps 7–8. Skip for draft-only (6C).

Post a short update to the case's Google Chat space so the team knows the LOR went out.
Post via the plain `gws` store (the connected account, which is a member of the case spaces).
**Message format:** `【Claude AI】 sent <1P|3P> LOR via <channels>`, where `<channels>` lists every
channel actually used — `email & fax` when both went out, else `email` or `fax`. E.g.
`【Claude AI】 sent 3P LOR via email & fax`. If both parties were sent in one run, combine:
`【Claude AI】 sent 1P & 3P LOR via email & fax`.

Find the space by case name (display name contains the client), then post the text:
```bash
SPACE=$(gws chat spaces list --params '{"pageSize":1000}' --format json \
  | python3 -c "import sys,json;s=sys.stdin.read();d=json.loads(s[s.index('{'):]);\
import re;print(next((x['name'] for x in d['spaces'] if '<Client>' in (x.get('displayName') or '')),''))")
gws chat spaces messages create --params "{\"parent\":\"$SPACE\"}" \
  --json '{"text":"【Claude AI】 sent 3P LOR via email & fax"}'
```
Outbound Chat posts may be permission-gated — if blocked, surface the exact message + space
and ask the user to approve (or they may post it themselves). Don't double-post if the user
says they'll send it.

## Step 9 — Confirm & clean up

Report: type(s), **channels used (email and/or fax)** + recipient(s) (email address AND/OR
fax #), subject, the Gmail message id **and/or** fax id+status (report both when both went
out), the **email label/INBOX/STARRED tagging** (Step 7.5, email only), the filed PDF link,
the tracking-sheet cell updated, and the **team Chat notice** posted (Step 8.5). For **neither
email nor fax (6C)**: report that nothing was sent (no email/fax on file), no file/log done.
Clean up: `rm -rf ~/lor_work`.

---

## Channel summary

Carrier directory (`insurance list` tab) drives the channels, decided in Step 3:
**send BOTH email (6A) AND fax (6B) when both are on file (primary path) → only one channel if
only one is on file → do-nothing (6C) when neither is on file.**
Fax is live via RingCentral, handled by the bundled **`send-fax`** engine
(`~/.claude/skills/send-fax/scripts/rc_fax.py`, creds in `~/.ringcentral.env`). The firm's
own fax line is `626-240-2046` (`+16262402046`).

## Notes & gotchas

- **Always re-fetch the template** from Drive each run — the firm edits it; never cache.
- Claim # / adjuster email are usually blank in intake at LOR stage → expect to prompt.
- The intake sheet is an `.xlsx` (not a Google Sheet); read it with `read_intake.py`.
- "Your Insured" (3P) = the at-fault **policyholder** (`p3_insured` / intake L8), not the
  3P driver.
- Tracking-sheet writes use `values update` only — this preserves cell colors ("no color
  change"). Never apply a formatting batchUpdate in Step 8.
- If `fill_lor.py` reports leftover placeholders, a field/token name was wrong — fix
  `lor_fields.json`; never hand-edit the docx.
