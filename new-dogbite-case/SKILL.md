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
  into the correct numbered subfolders, creates the Gmail case label and the case Google Chat
space, adds the case to the Dog Bite Cases tracker,
  drafts the Dog Owner POE (spoliation letter, variables highlighted, saved to ~/Downloads),
  and drafts the Hernán notification email (Cc Cassie + Joe, POE attached). Everything that
  goes outward is left as a DRAFT — nothing auto-sends; the DOL confirmation is the only stop.
  It does NOT file claims or prepare litigation forms (separate skills). Uses only THIS
  case's collected info — never copies data from another case. Handles JOINT cases with two
or more injured clients. Always trigger for any
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

## Step 2 — Read the RETAINER first, then the intake docx

**Start with the retainer**, not the intake form (Klaus, 2026-09-01). The zip carries a
`PI_Retainer*.pdf` — read it before anything else. It is the only document in the package
that is *independently* signed by the clients, so it is the cross-check on everything the
intake specialist transcribed. Pull from it:

- the **date of loss** as recited in the engagement clause (this is your DOL cross-check),
- the exact **client name(s)** as signed,
- the **signature dates** and the attorney signature date,
- the **fee split** (standard PI dog bite = 33.33% pre-suit / 40% post-suit),
- the **DocuSign envelope ID** (record it in the Activity Log),
- whether a **Joint Client Conflict Disclosure and Waiver** is included (multi-client cases).

⚠️ **Known defect (seen 2026-09-01, Peiyun Zhou):** the Joint Client Conflict Disclosure
pages are built on the firm's **automobile** template — the recitals speak of a "motor
vehicle accident" and of "drivers, passengers, owners, occupants … vehicles involved."
The operative retainer clause is correct, but flag the mismatch in the Step 10 report and
in the Hernán email; the firm needs a dog-bite version of that waiver.

## Step 2a — Read the intake docx

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

**Cross-check the DOL across all three sources before you ask** — the retainer's
engagement clause, the English intake, and the Chinese narrative. When all three agree,
say so when you ask; the gate then costs Klaus one word instead of a re-read.

**Multi-client cases** (two or more injured clients on one incident, jointly represented):
- Folder + label: **`<Client A> & <Client B>-<MMDDYY>`** — Klaus chose this over the
  single-name form on 2026-09-01 (Peiyun Zhou & Jian Wang-081726).
- Intake sheet: the **main tab is the primary injured client**; add a second tab named
  **`Client 2 - <Name>`** carrying that client's identity, injuries, treatment and billing
  (see Step 5b). Do NOT bury the second client in a Notes cell — their DOB, passport and
  bill balance are needed at demand time.
- Ask Klaus which naming he wants rather than assuming; both questions fit in one
  AskUserQuestion call alongside the DOL confirmation.

For a **minor** client, flag it: dog-bite minors need a Guardian Ad Litem (CIV-010/011)
downstream, and the folder/caption uses the parent-as-GAL wording.

## Step 3b — Create the klaus@ Gmail case label (nested, orange)

⚠️ **Corrected 2026-09-01.** The label is **nested under `⚖️Hernan Cases/`**, not a
top-level `DB-…`. Verified against all seven existing dog-bite labels — every one is
`⚖️Hernan Cases/DB-<Client>-<MMDDYY>` at `#ffad46` / `#ffffff`:

```
⚖️Hernan Cases/DB-Bo Tao-062726          ⚖️Hernan Cases/DB-Mudong Huang-062926
⚖️Hernan Cases/DB-Yi Cong-041226         ⚖️Hernan Cases/DB-Guolin Zhao-062126
⚖️Hernan Cases/DB-Lina Lu-070926         ⚖️Hernan Cases/DB-Weicong Lin-070926
⚖️Hernan Cases/DB-Gaoyang Qin-072626
```

```bash
gws gmail users labels create --params '{"userId":"me"}' \
  --json '{"name":"⚖️Hernan Cases/DB-<Client>-<MMDDYY>","labelListVisibility":"labelShow","messageListVisibility":"show","color":{"backgroundColor":"#ffad46","textColor":"#ffffff"}}'
# if 409 (exists): list labels, find the id, then patch name + color:
# gws gmail users labels update --params '{"userId":"me","id":"<ID>"}' \
#   --json '{"id":"<ID>","name":"⚖️Hernan Cases/DB-<Client>-<MMDDYY>","color":{"backgroundColor":"#ffad46","textColor":"#ffffff"}}'
```

**Then apply it to the case's mail:** the intake specialist's original "New Case" email
thread, and (after Klaus sends it) the Step 9 Hernán notification. Label only — do not
touch Klaus's stars or inbox state on threads he is still working.

## Step 3c — Create the case Google Chat space

Also missing from v1. Every dog-bite case has a Chat space; match the existing ones.

- **Name:** `<Client>-<M/D/YYYY DOL>(Dog Bite Case)` — note the slashed date and the
  literal suffix, e.g. `Weicong Lin-7/9/2026(Dog Bite Case)`.
- **Settings:** `spaceType: SPACE`, `spaceThreadingState: THREADED_MESSAGES`,
  then `HISTORY_ON`.
- **Members:** the same six as every other dog-bite space. Copy the member IDs off an
  existing space rather than guessing emails — `gws chat spaces members list` on
  `spaces/AAQA3e2w-3w` (Weicong Lin) returns the canonical roster; klaus@ is the manager
  and is added automatically as creator, so add the other five.

⚠️ **The API rejects `spaceHistoryState` at create time** ("Don't set space history state.
After creating the space, set space history state by calling update space API"). Create
first, then patch:

```bash
SP=$(gws chat spaces create --json '{"spaceType":"SPACE","displayName":"<Client>-<M/D/YYYY>(Dog Bite Case)","spaceThreadingState":"THREADED_MESSAGES"}' | jq -r .name)
gws chat spaces patch --params "{\"name\":\"$SP\",\"updateMask\":\"spaceHistoryState\"}" --json '{"spaceHistoryState":"HISTORY_ON"}'
for u in <the five member ids>; do
  gws chat spaces members create --params "{\"parent\":\"$SP\"}" --json "{\"member\":{\"name\":\"users/$u\",\"type\":\"HUMAN\"}}"
done
```

Post one 简体中文 setup summary to the space at the end (client + DOL + location, both
clients if joint, folder path, and the open items awaiting Hernán).

## Step 4 — Duplicate the template

```bash
python3 ~/.claude/skills/new-dogbite-case/scripts/build_case.py \
  14scr16zZnF05TVj-iXSonjTAQpo7_ceA \
  1ewaJIoeLHoc3lG3dIyDTfWwuSt6HYRVt \
  "<Client>-<MMDDYY>" "<Client>"
```
Prints JSON with `case_folder_id`, `subfolders` (name→id), and `intake_sheet_id`. Keep it.

## Step 5 — Fill the intake sheet

⚠️ **Dump the sheet's real labels first. Do not trust the static map.** The template has
drifted from `references/intake-sheet-map.md` at least once (caught 2026-09-01: the whole
Incident block was off by one row from row 5, so every value from "Provoked?" down landed
against the wrong label). One command, every time, before you build `fields.json`:

```bash
for pair in "B:C" "E:F" "H:I" "K:L"; do L=${pair%%:*}; V=${pair##*:}
  echo "=== labels $L / values $V"
  gws sheets spreadsheets values get --params "{\"spreadsheetId\":\"<ID>\",\"range\":\"${L}2:${V}28\"}" \
  | python3 -c 'import json,sys
d=json.load(sys.stdin)
for i,r in enumerate(d.get("values",[]),start=2):
    lab=(r[0] if r else "").replace(chr(10)," ")[:55]
    if lab.strip(): print(f"{i:>3} {lab}")'
done
```

Build `fields.json` against **those** labels, then **read the sheet back and diff** what
landed against what you sent — the fill script reports a count, not a per-cell result, so
a silently dropped or misaligned field only shows up on a read-back. If you have to
re-map, `values batchClear` the affected ranges first; the script fills and yellows but
does not clear stale text.

Build `~/dogbite_work/fields.json` — a flat map of **value-cell A1 → string** — from the
intake. Fill only what the intake supports; omit unknowns (the script yellows them).
Never invent facts. Then:

```bash
python3 ~/.claude/skills/new-dogbite-case/scripts/fill_intake_sheet.py \
  "<intake_sheet_id>" ~/dogbite_work/fields.json
```
Prints counts (`value_cells`, `filled`, `yellowed_blank`). The script keeps the template's
pre-filled "Pending" cells and highlights every empty data cell #FFE599.

### Step 5b — Second client tab (multi-client cases only)

Add a `Client 2 - <Name>` tab to the same spreadsheet via `sheets.spreadsheets.batchUpdate`
`addSheet`, then write a two-column label/value block: name, DOB, gender, passport or DL
number, immigration status, phone, email, address, marital status, occupation, language,
role in the incident; then INJURIES, MEDICAL, BILLING and NOTES sections. Bold column A,
wrap column B, and paint the unknown value cells `#FFE599` so the second client's pending
items are as visible as the first's. Record the joint-representation basis (retainer +
conflict waiver dates and DocuSign envelope) in the NOTES row.

## Step 6 — Sort the documents into subfolders

Build `~/dogbite_work/routing.json` per `references/file-routing.md` (its `subfolders`
map = the `subfolders` from Step 4; `files` = each extracted file → subfolder + rename).
Then:

```bash
python3 ~/.claude/skills/new-dogbite-case/scripts/sort_files.py ~/dogbite_work/routing.json
```

⚠️ **`sort_files.py` is NOT idempotent — run it exactly once.** It uploads unconditionally,
so a second run duplicates every file (hit 2026-09-01: 22 files became 44). The script
prints a long JSON report; if you only read the tail and are unsure it completed, **verify
by listing the destination folders**, never by re-running. To clean up duplicates, list
each folder ordered by `createdTime`, keep the first of each name, and trash the rest.

## Step 7 — Add the case to the Hernán Litigation Tracker

⚠️ **Corrected 2026-09-01.** The id in v1 (`1GYM0ke371z4…`) **does not exist — it 404s**,
and the column list below it was invented. The real tracker is **`0. Tracking Sheet`**,
id **`1XmV816UBTWcEyo65jQPquPLwGyqvllNGbYSSAhrIILA`**, at the Hernan Simo Cases drive root
— the same workbook that holds the Activity Log and 控制台 Tasks. Append to the
**`Dog Bite Cases`** tab.

Its actual 14 columns, in order:

```
A DOL                B Client Name          C Referrer        D Case Status
E Note               F Note (platform:      G Health Ins.     H Occupational Ins.
                       Amazon Flex / GOFO /
                       SwiftX / Quince)
I Animal Control     J Deed Info            K POE1-Def        L POE2
M POE3               N Complaint
```

Unknown-at-intake columns are written `Pending`, matching the existing rows. Put this
case's own facts in E (never a cross-case comparison), the delivery platform in F, and the
animal-control agency plus activity number in I. There is no SOL column — carry the SOL
(DOL + 2 years) in the Activity Log and the Hernán email instead.

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
(`DATE \@ "MMMM d, yyyy"`) — `fill_poe.py` sets it. Convert docx→PDF (LibreOffice headless
is fine: `/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf`)
and save **both docx + PDF to `~/Downloads/<Client>/`**. Residence cases may also need a
**Landlord POE** — only draft it if THIS case establishes the property owner/manager;
otherwise note it as pending.

### ⚠️ ALWAYS read the filled POE back before you hand it over

The template body is **hard-coded to the fact pattern of the case it was built from**. It
asserts, in the DEMAND section:

> "We are informed by the Animal Control Bite Report that a Ring doorbell video camera
> installed at the subject premises captured the events leading up to, during, and
> immediately following this incident."

and then refers to "the Ring camera footage" twice more. **If your case has no bite report
and no known camera, sending that letter puts assertions in front of the adverse party
that we cannot support** — a direct hit on the firm's no-fabrication rule. Caught
2026-09-01 (Peiyun Zhou: neither existed).

Two other template quirks:
- The addressee line already appends "and Any/All Residents, Occupants, or Dog Owners", so
  `owner_name` must be a **bare name** — anything longer reads as a double addressee.
- The breed token renders as "a `[dog breed]` dog", **singular** — it breaks on multi-dog
  cases.

**When the template's recitals do not match the case, rewrite the body** rather than force
the tokens. Build it on `6. Letter Header.docx` (see the letterhead note below) and keep
the firm's section structure: DEMAND FOR PRESERVATION OF EVIDENCE / LITIGATION HOLD ON
ELECTRONICALLY STORED INFORMATION / CONSEQUENCES OF SPOLIATION / NEXT STEPS. Two demands
worth carrying into every dog-bite POE from now on, both from Hernán's own revisions:

1. **The animals themselves** — preserve and produce for inspection, with **not less than
   thirty (30) days advance written notice** before any sale, transfer, rehoming,
   relocation, surrender or euthanasia, plus each animal's present location and the
   identity of anyone it has already been transferred to. Dogs get moved; this is the one
   demand that cannot be made up for later.
2. **The premises as they were** — the gate, its latch and hardware, the fencing, the steps
   and **any warning signage**, in their date-of-loss condition.

### ⚠️ Letterhead fax — hard red line

`6. Letter Header.docx` still prints **Fax: 626-240-2046**, which must NEVER appear on
firm letterhead (it is claims@'s fax-to-email). Every document built on it must patch
`word/header*.xml`: replace `626-240-2046` with the **general** fax `626-323-8181`, or with
the owning CM's direct line on case correspondence. Apply the documented clip fix in the
same pass (`<wp:posOffset>3708822</wp:posOffset>` → `2908722`, `<a:off x="3783900"` →
`x="2983800"`), or the top-right contact block prints past the paper edge.

## Step 9 — Draft the Hernán notification email (do NOT send)

Create a Gmail draft on **klaus@** (default gws): **To** hernan.s@lingtulaw.com, **Cc**
`cassie@lingtulaw.com, joe@lingtulaw.com` (per [[feedback_hernan_case_email_cc]]) — **add
the intake specialist (cindy.z@) when you quote her assessment or her legwork**, which the
full package below does. Never auto-send; Klaus reviews and sends.

**Write the full package, not a summary** (Klaus, 2026-09-01: "把所有掌握的信息和 case
folder 里有的信息都整理…同时结合 cindy 给我们发来的信息打包整理一个完整 email"). Hernán
opens the case from this email, so the liability picture has to be reconstructible from it
alone. Numbered sections, **bold labels**, flowing paragraphs:

1. **The clients** — full legal names, DOB, ID/passport numbers and validity, immigration
   status, contact, address, occupation, language and interpreter need; note any physical
   limitation that bears on the facts.
2. **The engagement** — signature dates, fee split, DocuSign envelope, joint-representation
   waiver, and any template defect found in Step 2.
3. **Date, place, what happened** — the full narrative, not a précis. Small details decide
   dog-bite liability (gate ajar, no barking heard, who intervened, whether the owner
   appeared, why 911 was late).
4. **Injuries and treatment** — per client, with admission and discharge dates, the
   repairing physician, discharge medications, and the billed / adjusted / outstanding
   figures.
5. **The dogs and the property** — the identification problem stated plainly. **Any
   delivery-recipient name is a LEAD ONLY**; say so explicitly and confirm the file does
   not record them as the owner anywhere.
6. **Witnesses** — who they are, what they did, what has already been tried to find them,
   and who tried.
7. **Animal Control** — agency, activity number (flag any conflict between documents),
   officer, and any outstanding agency request to the clients.
8. **Police** — or the absence of a report, and what that means for the record.
9. **What is in the case folder** — the inventory, by subfolder.
10. **What we do not have** — the honest gap list, including anything deliberately left
    blank rather than guessed.
11. **The preservation letter** — and, if you rewrote the template body, say so and say why.
12. **What you need from him** — a short numbered list of decisions, and a commitment not
    to move until he answers. Close with the SOL date.

**Attribute the intake specialist's judgment to her by name** ("Cindy's assessment on
intake, which I share, is …"). Her read on strengths, challenges and client cooperation is
evidence about the case, and Hernán should know whose read it is. Attach the POE PDF plus
any one or two small exhibits a section directly relies on (e.g. the agency screenshot
behind an activity-number conflict) — the folder link covers the rest. Keep the email to
THIS case's facts; surface cross-case observations to Klaus in the report, not the email.

**After Klaus sends it:** apply the Step 3b case label to the sent thread and archive it
(`threads.modify`, add label + remove INBOX). Label the intake specialist's original thread
too, but leave her thread's stars and inbox state alone — those are Klaus's own markers.

## Step 10 — Report

Give the user: case folder link; intake-sheet fill counts + the yellow (pending) Stage-2
to-do list (HO insurer, dog-owner identity, animal-control report#, quarantine/vax); file
routing; the tracker row; the Chat space; the Gmail label; the POE draft path in
`~/Downloads`; the Hernán email draft (Cc'd, POE attached, not sent); and any **cross-case
flags** worth Klaus's attention.

**Verify before you report.** List the folders, read the sheet back, list the drafts —
report what is actually there, not what the scripts said they did. Also surface, as their
own flagged items: any template defect you had to work around (retainer waiver, POE body,
letterhead fax, intake-sheet map drift), and anything you deliberately left blank rather
than infer.

**Append one Activity Log row** to `0. Tracking Sheet` (`Activity Log` tab) per
[[case-data-architecture]] — Category `立案/送达`, with the case-folder id, intake-sheet id,
Chat space, Gmail draft id and DocuSign envelope in the Ref/ID column, and the open items
awaiting Hernán in Next Step.

Then clear scratch: `rm -rf ~/dogbite_work`.

## Notes
- All Drive ops carry `supportsAllDrives`/`includeItemsFromAllDrives` (shared drive).
- The skill only CREATES items (folders, a sheet copy, uploaded files) — nothing is
  deleted or overwritten. Safe to re-run into a fresh folder if a build goes wrong (trash
  the bad folder).
- Dog-owner identity: do not assert it from the Amazon delivery recipient name alone —
  record that as a lead in the sheet's Notes and leave the owner fields yellow until the
  property deed / investigation confirms.
