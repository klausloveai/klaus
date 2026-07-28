---
name: new-dogbite-case
description: |
  Set up a new DOG BITE case for Hernán Simó / 凌图律所 (Law Office of Shenqi Cai APC)
  in the "Hernan Simo Cases" shared drive. Use this skill whenever an intake specialist
  sends a dog-bite intake email + zip and a case folder is requested, or when any of the
  following are mentioned: new dog bite case, dog bite intake, dog-bite case folder,
  狗咬案, 建 dog bite case, 狗咬 intake, "/new-dogbite-case" for a named client, or a
  "<Client>_Dog Bite.zip" is uploaded. Given the intake zip, the skill: reads the intake
  docx (structured tables + narrative) AND vision-reads the client ID (authoritative for
  name / DOB / gender), confirms the client name + DATE OF LOSS with the user, duplicates
  the "Dog Bite Case Template" into "1. Dog Bite Cases" as
  "<Client>-<MMDDYY DOL>", auto-transcribes the intake into the copied "0. Intake Sheet"
  (unknown fields left empty + yellow-highlighted), files the zip's documents — renamed —
  into the correct numbered subfolders, adds the case to the Hernán Litigation Tracker,
  drafts the Dog Owner POE (spoliation letter, variables highlighted, saved to ~/Downloads),
  and drafts the Hernán notification email (Cc Cassie + Joe, POE attached). Everything that
  goes outward is left as a DRAFT — nothing auto-sends; the DOL confirmation is the only stop.
  It does NOT file claims or prepare litigation forms (separate skills). Uses only THIS
  case's collected info — never copies data from another case. Always trigger for any
  "set up / build a new dog bite case" request, even a partial one.
---

# New Dog Bite Case — build the case folder (Hernan Simo Cases)

Given a dog-bite intake zip, stand up the full case folder from the firm's template:
duplicate the template tree, auto-fill the intake sheet (unknowns → yellow), and sort
the intake documents into the right subfolders. **v1 builds the case only** — POE/LOR
letters, claims, and litigation forms are separate skills, triggered later.

Dependency-free: uses only `gws`, `python3` stdlib, and the bundled scripts.

## Constants — "Hernan Simo Cases" shared drive (`driveId 0APtYw9adyTl8Uk9PVA`)
- **`1. Dog Bite Cases`** (where new case folders go): `1ewaJIoeLHoc3lG3dIyDTfWwuSt6HYRVt`
- **`Dog Bite Case Template`** (duplicated per case): `14scr16zZnF05TVj-iXSonjTAQpo7_ceA`
  - `0. Intake Sheet` (Google Sheet) + six subfolders `1. Incident & Liability`,
    `2. Legal Documents`, `3. Medical Record & Bill`, `4. Litigation`,
    `5. Cost & Receipt`, `6. Settlement & Disbursement`.
- Firm-level assets (not touched here, for later stages): `2. Template/POE` (POE
  spoliation letters — dog-owner + landlord variants), `2. Template/LOR`,
  `3. Litigation Forms`.
- **Scratch dir:** `~/dogbite_work` (`mkdir -p`). Bash cwd resets between calls — use
  absolute `$HOME/...` paths, never `/tmp`.

Bundled scripts (`scripts/`, all import `gws_util.py`):
- `build_case.py` — recursively duplicate the template into a new case folder.
- `fill_intake_sheet.py` — write `fields.json` into the copied sheet; yellow-highlight blanks.
- `sort_files.py` — upload the zip's files, renamed, into the right subfolders.

References: `references/intake-sheet-map.md` (value-cell map + docx→field guidance),
`references/file-routing.md` (zip → subfolder + rename rules).

---

## Step 1 — Get + extract the intake zip

The intake specialist sends an email with a `<Client>_Dog Bite.zip`. Usually it is
already in `~/Downloads`. Extract it with CJK-filename recovery (WeChat zips carry
mojibake names; macOS `unzip` mangles them):

```bash
mkdir -p ~/dogbite_work
python3 - <<'PY'
import zipfile, os
zp = zipfile.ZipFile(os.path.expanduser("~/Downloads/<CLIENT>_Dog Bite.zip"))
dst = os.path.expanduser("~/dogbite_work/extract")
for info in zp.infolist():
    name = info.filename
    if not (info.flag_bits & 0x800):
        raw = name.encode('cp437')
        for enc in ('utf-8','gbk'):
            try: name = raw.decode(enc); break
            except: pass
    if info.is_dir() or name.split('/')[-1].startswith('._') or '__MACOSX' in name:
        continue
    t = os.path.join(dst, name); os.makedirs(os.path.dirname(t), exist_ok=True)
    open(t,'wb').write(zp.read(info))
    print(name)
PY
```

## Step 2 — Read the intake docx

The zip's `Initial Docs/<Client>_Dog Bite_Intake.docx` is the source of truth. It has
**4 structured tables** (internal intake, client basics, incident date/location/posture)
plus a **narrative** ("案件事实与时间线 / Case Facts & Timeline") holding the actual
dog-bite facts. Read the whole thing:

```bash
python3 - <<'PY'
import zipfile, re
z = zipfile.ZipFile("<abs path to intake docx>")
xml = z.read("word/document.xml").decode("utf-8")
xml = re.sub(r"</w:p>", "\n", xml)
print(re.sub(r"<[^>]+>", "", xml))
PY
```

Extract: client info (name, DOB, phone, email, address, occupation), **Date of Loss**
+ time, incident location & type, and — from the narrative — the fact of loss, wounds /
body part, leash status, owner conduct, animal-control contact, ER treatment, evidence
to preserve, dog description. Map these to sheet value cells per
`references/intake-sheet-map.md`.

### Step 2b — Vision-read the client ID (authoritative for name / DOB / gender)

The zip almost always includes the client's ID / driver-license image (`ID.jpg` or
similar). **Read it with vision** (the `Read` tool renders images) and treat the ID as
**authoritative** for the client's legal name, DOB, address, and gender — the docx is
transcribed by an intake specialist and can carry a typo or the *submitter's* name, not
the client's (same failure mode as new-case's "DL name is authoritative" rule).

- Cross-check the ID against the docx. If they **agree**, fill those cells confidently
  (e.g. gender goes from *inferred* to *document-confirmed* — the ID's `SEX` field).
- If they **disagree**, use the **ID** value in the sheet and **flag the discrepancy** in
  the Step 7 report for the CM. Do not silently keep the docx value.
- Note an **expired** license or a **state ID instead of a DL** in the report (minor
  follow-up, not blocking).
- Example (Bo Tao): ID showed `LN TAO / FN BO`, `DOB 09/15/1993`, `SEX M`, `6908 San
  Fernando Ave, La Conchita, CA 93001` — all matched the docx and confirmed C9 = Male.

If no ID image is in the zip, note it (the client ID is a Stage-1 item to collect) and
fill name/DOB from the docx, leaving gender yellow if the narrative's pronouns are the
only signal.

## Step 3 — Confirm Client + DATE OF LOSS, derive the folder name  ⚠️ gate

The folder is named **`<Client Name>-<MMDDYY DOL>`** (e.g. `Bo Tao-062726` for DOL
06/27/2026). Per firm convention, **always confirm the DOL with the user before naming
the folder / filling the sheet** — a WeChat→docx export has shifted dates before, and old
case folders were batch-named with a non-DOL date. State the client name + the DOL you
read and ask for a yes. Also confirm the client name spelling (matches the retainer).

For a **minor** client, flag it: dog-bite minors need a Guardian Ad Litem (CIV-010/011)
downstream, and the folder/caption uses the parent-as-GAL wording.

## Step 3b — Create the klaus@ Gmail case label (orange)

Once the client + DOL are confirmed, create a Gmail label in **klaus@** (default `gws`)
named **`DB-<Client>-<MMDDYY DOL>`** (e.g. `DB-Lina Lu-070926`) colored **orange**
(`backgroundColor #ffad46`, `textColor #ffffff`). Reuse if it already exists (patch the
color). This is klaus@'s own dog-bite case label (distinct from the team-mailbox PI labels).

```bash
gws gmail users labels create --params '{"userId":"me"}' \
  --json '{"name":"DB-<Client>-<MMDDYY>","labelListVisibility":"labelShow","messageListVisibility":"show","color":{"backgroundColor":"#ffad46","textColor":"#ffffff"}}'
# if 409 (exists): list labels, find the id, and patch color:
# gws gmail users labels update --params '{"userId":"me","id":"<ID>"}' --json '{"color":{"backgroundColor":"#ffad46","textColor":"#ffffff"}}'
```

## Step 4 — Duplicate the template

```bash
python3 ~/.claude/skills/new-dogbite-case/scripts/build_case.py \
  14scr16zZnF05TVj-iXSonjTAQpo7_ceA \
  1ewaJIoeLHoc3lG3dIyDTfWwuSt6HYRVt \
  "<Client>-<MMDDYY>" "<Client>"
```
Prints JSON with `case_folder_id`, `subfolders` (name→id), and `intake_sheet_id`. Keep it.

## Step 5 — Fill the intake sheet

Build `~/dogbite_work/fields.json` — a flat map of **value-cell A1 → string** — from the
intake, following `references/intake-sheet-map.md`. Fill only what the intake supports;
omit unknowns (the script yellows them). Never invent facts. Then:

```bash
python3 ~/.claude/skills/new-dogbite-case/scripts/fill_intake_sheet.py \
  "<intake_sheet_id>" ~/dogbite_work/fields.json
```
Prints counts (`value_cells`, `filled`, `yellowed_blank`). The script keeps the template's
pre-filled "Pending" cells and highlights every empty data cell #FFE599.

## Step 6 — Sort the documents into subfolders

Build `~/dogbite_work/routing.json` per `references/file-routing.md` (its `subfolders`
map = the `subfolders` from Step 4; `files` = each extracted file → subfolder + rename).
Then:

```bash
python3 ~/.claude/skills/new-dogbite-case/scripts/sort_files.py ~/dogbite_work/routing.json
```

## Step 7 — Add the case to the Hernán Litigation Tracker

Append one row to the tracker (Google Sheet id `1GYM0ke371z4tSJnTQl8Z6Mg_bwTiypmzx82jaAaZy64`,
Hernan Simo Cases drive root). Columns: Client | Case Type (Dog Bite) | DOL | Current Stage
(Intake / Pre-litigation) | Court/Case# (—) | Last Action ("Case set up <date>") | Next Due
(a real deadline from THIS case → **yellow #FFE599**; else blank) | SOL (DOL + 2yr) |
Attorney (Hernán / Klaus) | Case Folder (=HYPERLINK) | Notes (this case's own facts only).

## Step 8 — Draft the Dog Owner POE (do NOT send)

Fill the Dog Owner POE from **this case's own collected info** — never copy another case.
```bash
gws drive files get --params '{"fileId":"1Jrm0rA9khq4rKRFR-YKkZMm4w2ByaeEi","alt":"media","supportsAllDrives":true}' -o poe_template.docx   # 2. Template/POE/Dog Owner_Resident Template.docx
python3 ~/.claude/skills/new-dogbite-case/scripts/fill_poe.py poe_template.docx poe_fields.json poe_out.docx
```
`poe_fields.json` keys: owner_name, address, city_zip, client_name, date_of_incident,
location, dog_breed, county, delivery_clause. The firm template pre-highlights the fill-in
variables yellow (owner name/address/breed/etc.) so Hernán confirms them before signing;
leave anything the case doesn't establish as a highlighted `[… — confirm]` placeholder
(e.g. breed). The **[Date]** is a Word auto-date field formatted `July 15, 2026`
(`DATE \@ "MMMM d, yyyy"`) — `fill_poe.py` sets it. Convert docx→PDF via a throwaway Google
Doc (upload as gdoc → export PDF → delete) and save **both docx + PDF to `~/Downloads`** for
Klaus to eyeball/calibrate. Residence cases may also need a **Landlord POE** — only draft it
if THIS case establishes the property owner/manager; otherwise note it as pending.

## Step 9 — Draft the Hernán notification email (do NOT send)

Create a Gmail draft on **klaus@** (default gws): **To** hernan.s@lingtulaw.com, **Cc**
`cassie@lingtulaw.com, joe@lingtulaw.com` (per [[feedback_hernan_case_email_cc]]). HTML body,
warm/eager-to-learn tone (Klaus is learning litigation from Hernán) — **bold labels**
(Client / Date of loss / Location / What happened, and the bullet lead-ins). Summarize the
case, flag the liability tracks + any deadline + suspected owner (from this case only),
mention the POE is drafted, and include the case-folder link. **Attach the POE PDF.** Never
auto-send — Klaus reviews and sends. Keep the email to THIS case's facts; surface any
cross-case observation (e.g. same dog/owner as another firm case) to Klaus in the report
instead, not in the case files.

## Step 10 — Report

Give the user: case folder link; intake-sheet fill counts + the yellow (pending) Stage-2
to-do list (HO insurer, dog-owner identity, animal-control report#, quarantine/vax); file
routing; the tracker row; the POE draft path in `~/Downloads`; the Hernán email draft (Cc'd,
POE attached, not sent); and any **cross-case flags** worth Klaus's attention.

Then clear scratch: `rm -rf ~/dogbite_work`.

## Notes
- All Drive ops carry `supportsAllDrives`/`includeItemsFromAllDrives` (shared drive).
- The skill only CREATES items (folders, a sheet copy, uploaded files) — nothing is
  deleted or overwritten. Safe to re-run into a fresh folder if a build goes wrong (trash
  the bad folder).
- Dog-owner identity: do not assert it from the Amazon delivery recipient name alone —
  record that as a lead in the sheet's Notes and leave the owner fields yellow until the
  property deed / investigation confirms.
