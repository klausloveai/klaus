---
name: file-claim
description: |
  File an auto insurance claim ONLINE via the carrier's web portal for 凌图律所 /
  Lingtu Law Office (Law Office of Shenqi Cai APC). Use this skill whenever any of the
  following are mentioned: file a claim, file claim online, report a claim, open a claim,
  start a claim with the carrier, GEICO/Mercury/Progressive/Tesla claim, 1P/3P claim
  filing, "网上报案", "file claim", or "/file-claim" for a named case. Typical invocation:
  a driver/client name to find the case + which party (1P own carrier / 3P at-fault) +
  optionally the case manager. The skill finds the case in Drive, reads the intake sheet,
  verifies every form field with the user, then drives the carrier website in the browser
  (Claude-in-Chrome) following the carrier's playbook, PAUSES for explicit approval before
  the final submit, records the Claim Number + screenshot, files it to the case folder, and
  writes the Claim # back to the intake sheet and tracking row. GEICO 3P is implemented;
  other carriers are added as reference playbooks. Always trigger for any "file/report a
  claim" request, even a partial one.
---

# File Claim — Online Carrier Portal Filing

Drive a carrier's website to file an auto claim, populated from the case's intake sheet,
then record the resulting Claim Number, file the confirmation, and log it.

**This is an outward-facing, irreversible action** — submitting a claim notifies a real
insurer. The skill ALWAYS pauses for explicit user approval at the final submit (Step 6),
and never invents data: every field is read from the intake sheet and verified with the
user first. Login / 2FA / CAPTCHA are handled by the user in the live browser.

## Core principle — never answer a narrative field with made-up content

The goal is to **file successfully so the claim can advance** — NOT to fill every field
perfectly. Two classes of fields:

- **Narrative / substantive fields** (Facts of Loss, Purpose of Trip, any free-text "describe
  what happened"): **NEVER compose or guess.** If the intake sheet has the value, **copy it
  verbatim** (paste exactly). If it doesn't, **skip the field or enter a harmless filler like
  "1"**. A fabricated narrative can put wrong facts or an admission on the carrier's record —
  that is worse than leaving it blank. Not answering > answering wrong.
- **Logistical fields** (address, county, exact time, etc.): accuracy is secondary. If the
  intake lacks the value, use a reasonable placeholder (e.g. the client's home county when the
  accident location is unknown — see below) so the form proceeds; the CM corrects details with
  the adjuster later. These are allowed to be approximate/wrong.

When a single-value field maps to multiple intake people (e.g. a "Last Name" box but the
policyholder is "Miguel Garcia & Maria Reyesdiaz"), use the **first** person's last name.

## Supported carriers (playbooks)

| Carrier | Party | Playbook |
|---|---|---|
| GEICO | 3P (third-party) | `references/geico-3p.md` ✅ |
| Bristol West | 3P (third-party) | `references/bristol-west-3p.md` ✅ (firm-only contact) |
| Mercury | 1P | _not yet — add `references/mercury-1p.md`_ |
| Progressive | 3P | _not yet — add `references/progressive-3p.md`_ |
| Tesla | 3P | _not yet — add `references/tesla-3p.md`_ |

To add a carrier: write a new `references/<carrier>-<party>.md` in the same shape as
`geico-3p.md` (field map + numbered steps + FOL templates + post-filing checklist). The
orchestration below is carrier-agnostic.

## Invocation inputs

- **Case** — driver/client name (to find the Drive folder).
- **Party** — `1P` (client's own carrier) or `3P` (at-fault carrier). Determines which
  carrier playbook + which intake columns are used.
- **Carrier** — usually derived from the intake insurer for that party; confirm it maps to
  a supported playbook.
- **Case manager** — used for the contact block on the form (and the later LOR). Default to
  the case's tracking-tab owner; ask if ambiguous.

Ask only for whatever is missing or ambiguous.

## Constants

- **Shared Drive "PI Team Folder":** driveId `0ADBH3EXeXKRBUk9PVA`. Case folders named
  `Driver Name-M-D-YYYY`, containing `1#Legal Documents` and `<case> Intake Sheet.xlsx`.
- **Tracking sheet "PI Master Sheet":** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`.
  Tabs `Claims(Amos)`, `Piteam(Jerry)`, `Picase` — **read the live header row** before writing.
- **Firm contact for the form:** `~/.claude/skills/lor-send/references/firm-directory.md`
  (CM → direct line / team email). Firm ZIP `91746`.
- **Intake reader:** `scripts/read_intake_claim.py` (superset of lor-send's — adds vehicle /
  location / time / FOL fields).
- **Browser:** Claude-in-Chrome MCP (`navigate`, `read_page`/`get_page_text`, `find`,
  `computer`, `form_input`, `tabs_*`). Requires a connected, logged-in-as-needed browser.

> `gws` JSON output is prefixed with a `Using keyring backend: keyring` banner — strip
> everything before the first `{` before `json.loads`. Use a scratch dir under `$HOME`
> (`~/claim_work`), absolute paths, never `/tmp`.

---

## Step 1 — Find the case in Drive

```bash
DRV=0ADBH3EXeXKRBUk9PVA
gws drive files list --params '{"q":"name contains '\''<NAME>'\'' and mimeType='\''application/vnd.google-apps.folder'\'' and trashed=false","corpora":"drive","driveId":"'$DRV'","includeItemsFromAllDrives":true,"supportsAllDrives":true,"fields":"files(id,name)"}' --format json
```

If >1 match, show them and ask which. Capture the folder id, then list children to get the
intake `.xlsx` id and the `1#Legal Documents` subfolder id (`'<FOLDER_ID>' in parents ...`).

## Step 2 — Read the intake sheet

```bash
mkdir -p ~/claim_work
gws drive files get --params '{"fileId":"<INTAKE_XLSX_ID>","alt":"media","supportsAllDrives":true}' -o $HOME/claim_work/intake.xlsx
python3 ~/.claude/skills/file-claim/scripts/read_intake_claim.py $HOME/claim_work/intake.xlsx
```

Returns client, DOL, time, accident location, FOL, and the 1P/3P insurer, policy#,
policyholder, driver, vehicle, claim#, adjuster. **Claim # is normally blank** at filing
stage — that's the whole point; you're about to create it.

## Step 3 — Pick the carrier playbook + build the field set

1. From **party** + the intake insurer (`p3_insurer` for 3P, `p1_insurer` for 1P), pick the
   matching `references/<carrier>-<party>.md`. If none exists for that carrier/party, tell
   the user it's not implemented yet and stop (offer to do it manually / add a playbook).
2. **Read the playbook.** Build the form field set per its "Field map", pulling from the
   intake JSON + firm-directory (for the CM contact block) + the firm ZIP.
3. **County / city** and any field the intake doesn't carry: derive (e.g. city → county) and
   mark it for confirmation.

## Step 4 — Verify EVERY field with the user (mandatory)

Show a compact table of every value that will be typed into the form, flagging the
playbook's ⚠️ traps explicitly. For GEICO 3P that means **calling out**:
- **Last Name = policyholder (`p3_insured`), not the driver** — show both if they differ.
- **County** — show the derived value and ask for confirmation.
- **FOL** — show the exact sentence(s) that will be entered.

Do not open the browser until the user confirms the field set (or corrects it). This is the
cheap place to catch errors — fixing a filed claim is painful.

## Step 5 — Drive the carrier site (browser)

Confirm a browser is connected (`tabs_context_mcp` / `list_connected_browsers`); if not, ask
the user to open Chrome with the Claude extension and (for some carriers) log in.

Follow the playbook's numbered steps. After each navigation: read the page, match it to the
step's screenshot (`references/<carrier>-screens/stepNN.png` — Read it if the live page is
unclear), then fill/click. Adapt to live A/B variations — the playbook is intent, not a
pixel script. Fill all steps **up to but NOT including the final submit.**

If the site blocks automation (login wall, CAPTCHA, OTP), pause and ask the user to clear it
in the browser, then continue.

**⚠️ Move briskly — carrier report sessions time out.** Don't leave a half-filled claim idle
between steps. On GEICO, an idle pause mid-report produces a "Something Went Wrong" error
(easy to misread as a data/policy problem — it isn't). Batch actions, avoid long gaps; if you
see that error, just restart the report and run straight through. (An EXPIRED 3P policy is NOT
a blocker — it files to a claim number fine; coverage is the adjuster's call later.)

## Step 6 — Final submit (MANDATORY approval gate)

At the last screen before submission, **stop**. Show the user a screenshot/summary of the
fully-filled final page and the exact action ("click Submit / Report Claim"). **Submit only
after explicit approval.** Never auto-submit. (This is the one hard gate — a filed claim
can't be unfiled.)

## Step 7 — Capture the Claim Number (do it AT ONCE)

The confirmation page shows the Claim Number **once**. **Screenshot it immediately with
`save_to_disk: true`** and record the number — if the tab closes first, that page is
unrecoverable (a real lesson from the Liye Zhang run). Then click through any remaining
post-submit prompts.

## Step 8 — Record, notify, auto-LOR (firm-confirmed flow)

1. **Write the Claim # to the intake sheet.** The intake is an `.xlsx` in Drive (NOT a Google
   Sheet) — cell `L19` for 3P, `I15` for 1P (new-case cell-map). Edit inline + re-upload
   (overwrite same fileId): download, replace the cell with an `inlineStr` (claim #s are 16
   digits — store as text, not numeric, or precision is lost), preserve the cell's `s="..."`
   style, then `gws drive files update --upload`. openpyxl is NOT installed — use a
   zipfile/regex edit of `xl/worksheets/sheet1.xml`. Also log the case's tracking row.
2. **Post to the case Google Chat space** (NOT the Drive folder): the message
   **`【Claude AI】 <1P|3P> filed online, and claim# <CLAIM#>`** + the **confirmation screenshot**. Find the
   space by case name (`gws chat spaces list`). **Proven recipe (works):**
   ```bash
   SPACE="spaces/XXXX"
   # text only:
   gws chat spaces messages create --params "{\"parent\":\"$SPACE\"}" \
     --json '{"text":"【Claude AI】 3P filed online, and claim# <CLAIM#>"}'
   # with image attachment — two steps (media.upload needs the filename in the BODY):
   TOKEN=$(gws chat media upload --params "{\"parent\":\"$SPACE\"}" \
     --json '{"filename":"confirm.png"}' --upload <file.png> --upload-content-type image/png \
     --format json | python3 -c "import sys,json;s=sys.stdin.read();print(json.loads(s[s.index('{'):])['attachmentDataRef']['attachmentUploadToken'])")
   gws chat spaces messages create --params "{\"parent\":\"$SPACE\"}" \
     --json "{\"text\":\"3P filed online, and claim# <CLAIM#>\",\"attachment\":[{\"attachmentDataRef\":{\"attachmentUploadToken\":\"$TOKEN\"}}]}"
   ```
   ⚠️ **Screenshot-bridge caveat (this Cowork sandbox):** the browser tool's `save_to_disk`
   screenshots and the user's pasted images are written to the Cowork app sandbox, which the
   gws/Bash tool **cannot read** — so you can't auto-feed your own browser screenshot into the
   `media upload` above. The upload needs a **Bash-visible** file (e.g. under `~/Downloads`).
   `screencapture` works but grabs the whole screen (privacy risk — may expose other windows;
   don't post it). Practical options: post the **text automatically** (always works), and for
   the image either (a) the user drags the confirmation screenshot into the space, or (b) drop
   it in `~/Downloads` and upload via the recipe above.
3. **Auto-draft + fax the LOR.** Immediately invoke the **`lor-send`** skill for the same
   party (it drafts from the template with claim # + DOL + client and **sends fax-first** —
   GEICO has an LOR fax in the insurance-list directory). lor-send keeps its own pre-send
   approval gate.

## Step 9 — Confirm, prompt next actions, clean up

Report: carrier, party, **Claim Number**, intake/tracking cells updated, chat post, and LOR
fax status. Remind to confirm coverage / BI limits with the adjuster and tell the client not
to speak with the carrier directly. Clean up: `rm -rf ~/claim_work`.

---

## Notes & gotchas

- **Approval gate is non-negotiable** (Step 6). Filing is irreversible and outward-facing.
- **Policyholder vs driver** (3P Last Name) and **county** are the two recurring data traps —
  surfaced in Step 4 for GEICO; replicate per carrier.
- **Accident location/county unknown** (client doesn't remember): firm rule — fill a nearby,
  requirement-satisfying placeholder based on the **client's home address** (intake `C7`, i.e.
  the home county) so the report can proceed; the **CM updates the exact location with the
  adjuster afterward**. Always tell the user it's a placeholder and flag it in Step 4.
- Claim # is expected blank in intake before filing; you're creating it.
- Intake sheet is `.xlsx`, read with `read_intake_claim.py`. Tracking sheet is a Google
  Sheet — `values update` only, never a formatting batchUpdate.
- Always file as the correct party: GEICO 3P = "I had an incident with a GEICO customer",
  NOT "I am insured with GEICO" (despite the source file being named "...1P").
- If a field genuinely isn't in the intake (e.g. county, exact time), derive + confirm; do
  not guess silently.
