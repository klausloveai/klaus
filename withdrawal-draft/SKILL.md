---
name: withdrawal-draft
description: |
  Draft (do NOT send) a WITHDRAWAL OF REPRESENTATION letter for 凌图律所 / Lingtu Law
  Office (Law Office of Shenqi Cai APC). Use this skill whenever any of the following are
  mentioned: draft withdrawal letter, withdrawal of representation, withdraw from a case,
  drop a client, terminate representation, 撤销代理函, 退案信, "/withdrawal-draft" for a
  named client. Given a client name, the skill finds the case in Drive, reads the intake
  sheet (client name(s), date of loss, accident location), fills the firm's Drive template
  (including the case's owning team mailbox), computes the statute-of-limitations deadline
  (California 2-year default; for out-of-state accidents it web-searches the governing
  state's PI SOL and adjusts the letter), strips all yellow highlight so the letter is
  ready to send, renders the PDF, and saves it to ~/Downloads AND the case folder root
  ("lobby") in Drive. Handles multi-client cases (driver + passenger[s]) by joining the
  client names with "/". It DRAFTS & FILES ONLY — it never emails, faxes, or mails the
  letter. Always trigger for any "draft a withdrawal letter" request, even a partial one.
---

# Withdrawal of Representation — draft & file (no send)

Produce a ready-to-send Withdrawal of Representation letter PDF from the firm's Drive
template, populated from the case's intake sheet, with the statute-of-limitations
deadline computed for the governing state. Strips all yellow highlight, saves to
`~/Downloads`, and uploads to the case folder root ("lobby") in Drive.
**Drafts & files only — never emails, faxes, or mails the letter.** A human (attorney)
reviews and sends.

Fully dependency-free and self-contained. Bundled helpers:
- `scripts/read_intake.py` — read client / DOL / accident location from the intake `.xlsx`
- `scripts/fill_withdrawal.py` — fill template, compute SOL deadline, strip yellow, stamp date
- `references/state-sol.md` — per-state PI SOL guidance (web-search-to-confirm for out-of-state)

## Inputs
- **Client** — the client/driver name (required; used to find the case + intake sheet).
- For a **multi-client case** (driver + passenger[s] / vehicle owner), confirm with the
  user which clients go on the letter; their names are joined with **`and`** in the
  salutation — two clients `A and B` (e.g. `Dear Fan Bi and Yulin Yuan`), three or more
  `A, B and C`.

## Constants
- **Withdrawal template:** folder `1. Templates` (id `1Uf8UNfArJjKVkqYMcSf7hwr3WXWO1riT`) →
  `2. Withdrawal of Representation.docx` (id `13iUtIbwrj3DPofRCFP-kgl7gXLfuuXPP`).
  Always re-fetch the latest — the firm edits templates; never cache.
- **Shared Drive "PI Team Folder":** driveId `0ADBH3EXeXKRBUk9PVA`. Case folders named
  `Driver Name-M-D-YYYY`, containing the intake `.xlsx` (`<case name> Intake Sheet.xlsx`).
- **Intake cells:** `C4`=Driver Name · `C2`=DOL (MM/DD/YYYY) · `F2`=Accident Location.
  Passenger names: `C24` (Pass1), `F24` (Pass2), `C49` (Pass3), `F49` (Pass4).
- **Template placeholders** (literal yellow-highlighted text, not `[brackets]`):
  `Client Name` (salutation only — the template has **no recipient address block**),
  `DOL`, `DOL Plus 2 Year` (= DOL + SOL years, MM/DD/YYYY), and `Teamemail` (the case's
  owning team mailbox). The letter date is stamped to today — the script handles both a
  live Word DATE field and a flattened static "Month D, YYYY" date (the template has been
  saved both ways). **Always re-fetch the
  template — the firm edits it (it has already changed: address block removed, contact
  email turned into the `Teamemail` placeholder). Re-inspect the placeholders if anything
  looks off.**
- **`fill_withdrawal.py` also applies two layout edits** so the output matches the firm's
  preferred letter (the Drive template renders tighter / signed differently than wanted):
  (1) inserts a blank line before each body paragraph (Dear / Please / Important Notice /
  Your complete file / Yours sincerely); (2) removes the `Shenqi Cai, Esq.` signature line,
  leaving only `Lingtu Law Office`. No action needed — the script does this automatically.
- **Team mailbox (`Teamemail`):** derive from the case's Master-sheet tab —
  `Picase`→`picase@lingtulaw.com`, `Claims(Amos)`→`claims@lingtulaw.com`,
  `Piteam(Jerry)`→`piteam@lingtulaw.com`. Master sheet:
  `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`. If the client isn't on any tab, ask the
  user which mailbox to use.
- **Scratch dir:** `~/wd_work` (`mkdir -p ~/wd_work`). `gws` rejects paths outside the
  current dir, and the Bash cwd resets between calls — always use absolute `$HOME/wd_work/...`,
  never `/tmp`. Strip the `Using keyring backend` banner before `json.loads` (slice from
  the first `{`).

---

## Step 1 — Find the case in Drive

```bash
mkdir -p ~/wd_work
DRV=0ADBH3EXeXKRBUk9PVA
gws drive files list --params '{"q":"name contains '\''<CLIENT>'\'' and mimeType='\''application/vnd.google-apps.folder'\'' and trashed=false","corpora":"drive","driveId":"'$DRV'","includeItemsFromAllDrives":true,"supportsAllDrives":true,"fields":"files(id,name)"}' --format json
```

If multiple folders match, show them and ask which case. Then list the case folder's
children to get the intake `.xlsx` id (and keep the **case folder id** — it's the upload
target in Step 6):

```bash
gws drive files list --params '{"q":"'\''<CASE_FOLDER_ID>'\'' in parents and trashed=false","supportsAllDrives":true,"includeItemsFromAllDrives":true,"fields":"files(id,name,mimeType)"}' --format json
```

## Step 2 — Read the intake sheet

```bash
gws drive files get --params '{"fileId":"<INTAKE_XLSX_ID>","alt":"media","supportsAllDrives":true}' -o $HOME/wd_work/intake.xlsx
python3 ~/.claude/skills/withdrawal-draft/scripts/read_intake.py $HOME/wd_work/intake.xlsx
```

Returns `client`, `dol`, `accident_location`. If `dol` is blank, stop and ask the user —
a withdrawal letter with a wrong/blank deadline must not be produced. (Client name also
lives in the case folder name as a cross-check.) For a multi-client letter, also pull the
passenger name(s) (`C24`/`F24`/`C49`/`F49`) and confirm with the user who goes on the
letter, then join the chosen names with `/`.

Also resolve the **team mailbox** for `Teamemail` from the Master-sheet tab (see Constants):

```bash
SS=1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM
for TAB in "Picase" "Claims(Amos)" "Piteam(Jerry)"; do
  gws sheets spreadsheets values get --params "{\"spreadsheetId\":\"$SS\",\"range\":\"$TAB!A1:H400\"}" --format json
done
```

## Step 3 — Determine the governing state & SOL

The letter warns the client of the deadline to file their **own** PI lawsuit. The
governing state is **where the accident happened** (`accident_location` / intake `F2`),
not necessarily where the client lives.

- **California accident (default):** `sol_years=2`, `sol_words="two years"`,
  `state="California"`. No SOL-sentence edits — the template is California-general.
- **Out-of-state accident:** follow `references/state-sol.md` — **`WebSearch` the current
  PI statute of limitations for that state** (e.g. `"<state> personal injury statute of
  limitations car accident 2026"`), confirm the period from an authoritative source, then
  set `sol_years` (int), `sol_words` (e.g. `"three years"`), and `state` (e.g. `"Texas"`).
  The fill script rewrites "Under California law…" → "Under <state> law…", the SOL period
  words, and the deadline. **The words and the deadline MUST stay in sync** — pass
  `sol_words` matching `sol_years` (e.g. Minnesota = 6-year PI SOL → `sol_years=6`,
  `sol_words="six years"`, deadline = DOL + 6). **Always flag out-of-state SOL in your
  summary for attorney confirmation.**

If the accident state is unclear from `F2`, ask the user before drafting.

## Step 4 — Fill the template

Build `$HOME/wd_work/fields.json`:

```json
{
  "client":    "<client name, or several joined with 'and'>",
  "dol":       "<C2 raw MM/DD/YYYY>",
  "sol_years": 2,
  "state":     "California",
  "sol_words": "two years",
  "teamemail": "<owning team mailbox, e.g. picase@lingtulaw.com>"
}
```

The script renders `DOL` and the deadline as `MM/DD/YYYY` (e.g. `05/21/2026` →
`05/21/2028`); the letter DATE field at the top stays spelled-out (`Month D, YYYY`).

Fetch the latest template and fill (the script formats the dates, computes the deadline,
strips yellow highlight, stamps the letter date to today, and aborts if any placeholder
is left unfilled):

```bash
TID=13iUtIbwrj3DPofRCFP-kgl7gXLfuuXPP
gws drive files get --params "{\"fileId\":\"$TID\",\"alt\":\"media\",\"supportsAllDrives\":true}" -o $HOME/wd_work/template.docx
python3 ~/.claude/skills/withdrawal-draft/scripts/fill_withdrawal.py \
  $HOME/wd_work/template.docx $HOME/wd_work/filled.docx $HOME/wd_work/fields.json
```

## Step 5 — Render the PDF

PDF name convention: `Withdrawal of Representation - <Client> <DOL-dash>.pdf`, where
`<DOL-dash>` = the intake DOL with `/`→`-` and no leading zeros (`03/01/2026` → `3-1-2026`),
matching the case-folder date. e.g. `Withdrawal of Representation - John Smith 3-1-2026.pdf`.

```bash
PDF="Withdrawal of Representation - <Client> <DOL-dash>.pdf"
DOCID=$(gws drive files create --upload $HOME/wd_work/filled.docx \
  --upload-content-type application/vnd.openxmlformats-officedocument.wordprocessingml.document \
  --json '{"name":"__wd_tmp","mimeType":"application/vnd.google-apps.document"}' \
  --params '{"supportsAllDrives":true,"fields":"id"}' --format json \
  | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['id'])")
gws drive files export --params "{\"fileId\":\"$DOCID\",\"mimeType\":\"application/pdf\"}" -o "$HOME/wd_work/$PDF"
gws drive files delete --params "{\"fileId\":\"$DOCID\",\"supportsAllDrives\":true}"
```

Read the rendered PDF back to eyeball it (letterhead, salutation name(s), DOL, deadline,
team email, no stray highlight). For a multi-client letter, use a name like
`Withdrawal of Representation - Fan Bi, Yilin Yuan 5-21-2026.pdf`.

## Step 6 — Deliver: case folder root ("lobby") + Downloads

**Always do BOTH** — the case folder root is the primary home; Downloads is an extra copy.
Even if the user says "save it to Downloads", still file it to the case folder root too
(unless they explicitly say to skip Drive).

```bash
# 1) local copy for the user
cp "$HOME/wd_work/$PDF" ~/Downloads/

# 2) upload to the CASE FOLDER ROOT (the "lobby" — sits beside 1#Legal Documents etc.)
gws drive files create --upload "$HOME/wd_work/$PDF" --upload-content-type application/pdf \
  --json '{"name":"'"$PDF"'","parents":["<CASE_FOLDER_ID>"]}' \
  --params '{"supportsAllDrives":true,"fields":"id,name,webViewLink"}' --format json
```

The "lobby" is the case folder **root** (the level you land on when you open the case,
beside the numbered subfolders) — NOT a subfolder. Do not place it in `1#Legal Documents`.

## Step 7 — Report

- Client name(s) on the letter, DOL, accident location, team mailbox used.
- Governing **state**, **SOL period**, and the computed **filing deadline** — for an
  out-of-state case, the web source used, **flagged for attorney confirmation**.
- Delivered paths: `~/Downloads/<PDF>` and the Drive case-folder link.
- Remind: this is a **draft for attorney review** — the skill did not send/mail it.

## Step 8 — Client WeChat message (always output, copy-paste ready)

After every draft, also print the client-facing Chinese WeChat message below, inside a
copy-paste block. Adapt **only the SOL sentence** to match the letter — swap the state name
to Chinese (加州 / 明尼苏达州 / …) and the period to a Chinese numeral (两年 / 三年 / 六年 …);
everything else is fixed. (California default shown.)

```
尊敬的客户您好，

🔔 本所已正式发出撤案通知，自即日起不再就您本次交通事故案件继续提供代理服务。本次撤案已生效，案件流程即刻停止，请您知悉。

⚠ 时效提醒
根据加州法律，您通常自事故发生之日起拥有两年的时间提出人身伤害索赔。如在该期限内未提起诉讼或达成解决，您的索赔权利可能会受到影响或被永久限制。建议您如需继续处理案件，尽快咨询其他律师以保护您的权益。

💬 后续事项说明

⏯案件状态：撤案通知已发出并生效，本所不再参与后续处理；

🙅🏻‍♂️您的行动：目前无需执行任何额外操作；

🗂资料需求：如您需要本案文件或希望转交给新的律师，请随时通过微信或电话与我们联系，我们将协助提供相关资料。

感谢您此前的信任与配合，祝您一切顺利。
```

Then clear scratch: `rm -rf ~/wd_work`.

## Notes
- Always re-fetch the template from Drive — never cache.
- The letter date is stamped to today on fill. The template's date has appeared as both a
  live Word DATE field (whose cached value goes stale on Drive PDF conversion) and as plain
  static text; the script refreshes either form (it replaces any spelled-out "Month D, YYYY"
  date — the only such date in the letter, since DOL/deadline are MM/DD/YYYY).
- Out-of-state: no state-specific withdrawal template exists in `Other States/` — this
  skill adapts the California-general template via the SOL edits above.
- Read-only against Drive/Sheets except: the throwaway temp Doc for PDF conversion (created
  then immediately trashed) and the final PDF uploaded to the case folder root.
