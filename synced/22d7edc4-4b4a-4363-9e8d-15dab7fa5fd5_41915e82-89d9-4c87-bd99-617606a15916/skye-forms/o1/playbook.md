> **这是 `o1` 的完整 playbook。** 由 `skye-forms` 的 Step 1 路由进来，进来之后**从头读完**。
> 文中所有 `references/…`、`scripts/…`、`assets/…` 路径，都相对于 `<skill>/o1/`。

# O-1 form filling (Lingtu Law · 人才移民)

An O-1 filing is four or five forms and three payments, and almost every error in
it is silent — a checkbox whose export value didn't match, a field name that
moved in a new edition, a fee that was right last quarter. So the shape of this
skill is: work from a written instruction doc, get the forms fresh, learn the
client's facts from their own case folder, fill through real AcroForm fields,
then read the result back with your eyes.

The set is **I-129 + the O and P supplement, I-907, three G-1650s, and G-28 when
the firm is attorney of record**. G-1145 is not part of the O-1 package (samples
for it exist in the firm's library, but it is not one of the four).

**Fill only from freshly downloaded official forms — never from a previous case's
PDF, a stored sample, or the firm's `0 Sample` copies.** Those carry superseded
editions (field names move), can have damaged AcroForms, and drag stale firm data
forward (the retired `8186658535` phone, a blank bar number). Values come from
the case's filled 填表指令 doc; positions come from the current form's own printed
item numbers and instructions. The reference field maps here are derived from the
current blanks and are navigation aids for those positions — not a licence to
copy answers from an old filing.

Every fill run works from **that case's own copy of the 填表指令 doc** (Step 0) —
the Fixed/Flexible instruction sheet that says what data this case needs and
exactly where each fact goes. The reference files below are the machine-level
field maps behind it; read the relevant one before filling rather than
re-deriving it:

| File | When to read |
|---|---|
| `references/i-129-o1.md` | before touching I-129 or the O and P supplement |
| `references/g28-i907-g1650.md` | before touching G-28, I-907 or G-1650 |
| `references/fees-and-filing.md` | fees, lockbox address, firm fixed data, Drive ids, the learning precedents and their known defects, environment quirks on this Mac |
| `assets/o1-fill-instructions.md` | the markdown source of the 填表指令 master doc — use it to recreate or repair the Drive copy |

Setup, once per session:

```bash
export PATH="$HOME/.local/bin:$PATH"          # gws
PY=~/.local/opt/pdfvenv/bin/python            # pypdf + cryptography
```

If `gws` 401s or says `invalid_grant`, run `gws auth login -s drive`, print the
URL, and let the user approve it in their own browser. Never handle their
password or 2FA.

---

## Step 0 — Get this case's 填表指令 doc in front of you

Nothing gets filled from memory or from a previous case. Each fill run is driven
by a per-case copy of the instruction doc, so the client's facts and the field
destinations live in one place the whole team can read and correct.

**The doc always comes from the same place, and the finished forms always go
somewhere else — the client folder the user names in the request.**

| | Where | Id |
|---|---|---|
| **Read the doc from** (every run) | `0.testing` → `Test O1B` → `2. Form` | folder `1FiiQaAXjyj40TNObRHGaATICqEAM_mtM`, doc `18kd7cdGMaMA029Z2zEUAyx2JqqHi4TX3L8b8SaWIjR8` |
| Mirror copy (sample library) | `0 Sample （O1）` → `3.Forms / Offer / Itinerary` | `1prc4Qu-mex2vFzDybUI3m4GVZIrt7ep_vydY7eMQwFA` |
| **Write the filled forms to** | whichever client Drive folder the request names | — |

Read the `Test O1B / 2. Form` copy each run rather than working from memory of it:
that is where corrections land, so reading it is how a fix from last week actually
reaches this case. If the request does not say where the output goes, ask — do not
default to dropping client forms into the test folder.

Keep the mirror in sync when the instructions change (re-upload the same markdown
to both ids) so the sample library never becomes the stale one.

1. Read the doc from `Test O1B / 2. Form`. Its sections: **一** the case
   parameters (Step 1 below), **二** the firm's Fixed data, **三** the client-facts
   worksheet with each fact's form/page/Part/Item destination, **四** fees and the
   three G-1650s, **五** signatures and mailing, **六** the post-fill self-check,
   **七** the materials checklist.
2. Write this client's facts into a **copy** — either a copy dropped into the
   output folder named for the client (`O-1 填表指令 — <Client>`), or a working
   copy of your own. That filled copy, not your context and not a previous case,
   is what Step 4 pulls values from.
3. **Never record one client's facts in the `Test O1B` doc itself** — it is the
   source every future run reads. Corrections to the *instructions* (a moved
   field, a changed firm value, a new fee) do belong there, mirrored into
   `references/` here and into the sample-library copy so the three don't drift.
   `assets/o1-fill-instructions.md` is the markdown source if a Drive copy ever
   needs rebuilding.

If the doc and a reference file disagree, work out which is stale rather than
picking one — and say which you corrected.

## Step 1 — Settle the case parameters in section 一

Everything downstream forks on these, so settle them before reading a single
form. Section 一 of the doc is where the answers get written down.

Three things arrive **as instructions** rather than being derived: COS-or-CP, the
consulate city for Part 4 item 1.b, and whether this case has a G-28. If the
instruction is silent on any of them, ask — inferring them is how a package ends
up describing a different case than the one being filed.

### 1a. COS or CP — this arrives as an input

The instruction that starts the job states whether the case is **COS** (change of
status inside the US) or **CP** (consular processing). Do not infer it from the
beneficiary's current status, and do not carry it over from another case.

| | I-129 page 2, Part 2 item 4 |
|---|---|
| **CP** | `/A` — option a., notify the consulate in Part 4 |
| **COS** | `/B` — option b., change the status and extend the stay |

Part 4 item 1 is filled on **both** paths — the item exists for the case where a
change of status cannot be granted. Two of its three boxes are fixed for this
firm's O-1 work: **a. Type of Office is always `Consulate`** and **c. U.S. State
or Foreign Country is always `China`**. Only **b. Office Address (City)** varies,
and it comes from the instruction.

On a COS case Part 3 item 6 (current status and expiry) must be complete, and
those two values come from the I-94 — see Step 2.

If the instruction did not say which, ask. Guessing here changes what the
beneficiary actually gets.

### 1b. Version: with G-28 or without

This is the primary fork and it reaches four of the forms.

| | **with G-28** (firm files as attorney of record) | **without G-28** (petitioner self-files) |
|---|---|---|
| G-28 | yes, and its Part 3 client is the **petitioner** (role `/P`) | not filed |
| I-907 Part 1 | attorney's name + firm address; tick the G-28 box; bar number `348794` | petitioner's name + address; both left blank |
| I-907 Part 1 item 8 | **`/B`** attorney for the petitioner | **`/A`** I am the petitioner |
| I-907 Part 3 contact | firm phone / fax / email | petitioner's own phone / email |
| I-129 | **no G-28 field exists anywhere on the 02/27/26 edition** — the only affected spot is Part 8 (preparer) | Part 8 normally blank |
| RFEs / approval notices go to | firm address | petitioner's address — tell them, nothing routes through the firm |

Decide it from whether this case actually has a signed G-28, not from what a
previous case did: the two stored precedents are one of each.

### 1c. Sponsorship shape: company or individual agent

Mirrors the firm's own `a. Direct Employment` / `b. Agent-Based` sample folders.
It drives I-129 Part 1 (item 1 for an individual, item 2 for a company — they
are mutually exclusive), Part 5 items 12–17, I-907 Part 2 item 4, and the O
supplement's petitioner name. section 一.3 of the doc has the full table.

An O-1 petition is filed **by an employer or agent on behalf of a beneficiary**,
so the G-28 client is the **petitioner**, not the beneficiary. That is the
opposite of the firm's family and travel-document filings and the single most
consequential habit to break.

The self-petition case — beneficiary sponsoring through their own company — is
the shape that usually comes without a G-28, and it is also the one where the O
supplement item 7.a is **Yes** with an explanation in 7.b.

### 1d. Small employer

Whether the petitioner has 25 or fewer full-time-equivalent US employees, and
whether it is a nonprofit. This sets two of the three fee amounts and has to
match I-129 Part 5 item 15. Ask if the intake doesn't say — guessing produces an
underpayment, which USCIS rejects.

## Step 2 — Read the client's facts from their own case folder

Case folders live in the 人才移民 shared drive; `references/fees-and-filing.md`
has the drive and folder ids. Find this client's folder by name, then read
everything in the intake and forms subfolders — passport, I-94, visa, EAD,
company registration, employment agreement, itinerary, prior filings.

Forms subfolders are inconsistently named (`Forms`, `表格`, `2. Form`), so list
the case folder's children and pick by content rather than by expected name:

```bash
export PATH="$HOME/.local/bin:$PATH"
gws drive files list --params '{"q":"'"'"'<FOLDER_ID>'"'"' in parents and trashed=false","fields":"files(id,name,mimeType,size)","supportsAllDrives":true,"includeItemsFromAllDrives":true,"corpora":"allDrives","pageSize":200}'
```

Prefer the Drive connector's `read_file_content` for reading intake material: it
does server-side text extraction and OCR without pulling bytes to local disk,
which matters because these files carry passport numbers, I-94 numbers and
addresses. Keep local disk for the blank forms and the fill step only.

**Write each fact into section 三 of this case's 填表指令 copy as you find it**, then
build the values JSON from that. Going through the doc rather than straight from
intake to JSON is what makes the work reviewable — a colleague can check section 三
against the passport without reading any code, and the next person on the case
inherits it.

Section 三 is also the authoritative list of what to look for, and it deliberately mirrors
the firm's own `个人信息.docx` / `担保人信息.docx` / `信息采集表.xlsx` wording so
nobody has to translate between two vocabularies. It covers, beyond names and
addresses: beneficiary DOB, sex, country and **province** of birth, citizenship,
passport number/issue/expiry, I-94 number, date of last arrival, current status
and expiry, US residential address, last foreign address; petitioner FEIN, type
of business, year established, US employee count, gross and net annual income;
job title, wage and unit, hours, intended employment dates, nature of the event,
duties; the consultation/advisory-opinion answers; consulate city and country.

Aim to have the whole picture before filling anything, and leave a gap marked as
a gap rather than inventing it — a plausible-looking invented I-94 number is
worse than a blank you flagged.

### The I-94 is a required document, not an optional one

I-129 Part 3 item 6's **Current Nonimmigrant Status** and **Date Status Expires**
are read off the I-94 (`Class of Admission` and `Admit Until Date`) and nowhere
else. An I-20's OPT end date is a different fact and substituting it misstates
the record.

**If the case folder has no I-94 — or the one on file is over a year old — go get
one.** Drive it with the browser tools (Claude in Chrome, or the in-app browser
pane). `gws` cannot do this: it is a Google Workspace CLI and does not control a
browser.

1. Open `https://i94.cbp.dhs.gov/search/recent-search` → "Get Most Recent I-94/I-95"
   in the user's browser and drive it to the lookup form.
2. **The page opens a Terms of Service dialog that must be scrolled and accepted
   before the form unlocks. Do not click that acceptance yourself — hand it to the
   user.** Those same terms prohibit automated access to the site, so an agent
   clicking "I agree" would be asserting agreement to a condition it is not
   meeting. This is not a cookie banner to dismiss; it is the gate that binds the
   firm to the terms, and a person has to pass it.
3. Give the user the five values ready to paste — **Last/Surname, First (Given)
   Name, Date of Birth, Passport Number, Passport Country of Issuance** — all of
   which Part 3 already needs, so nothing extra is asked of the client. Leave the
   tab open on the form.
4. Once they save the result page as a PDF into the case's forms folder
   (`I-94 <Client Name>.pdf`), fill the two boxes from it.

Getting the browser to the form and staging the inputs is most of the work, so
this still saves the user real time — the handoff is one click and a paste, not a
task returned unstarted.

The saved PDF is the only artifact showing where those two values came from, which
is what makes them checkable by a colleague or an officer. The result also carries
the **passport number** CBP has on record, which is a useful cross-check against
the passport scan in the case file.

**Scope this tightly**: one record at a time, only for a client the firm is
actively representing, only for this filing — never over a list. If the surname,
given name or passport number is at all uncertain, confirm it with the client
rather than trying spelling variants; repeated failed attempts against a
government identity system are their own problem.

**Which passport number to use**: the one the beneficiary actually entered the US
on, which is not always the current passport. If they renewed after their last
entry, the lookup needs the older number — check the entry date against the
passport issue dates before submitting.

An I-94 records only the **most recent admission** — changing schools or moving
onto CPT/OPT does not create a new one. When the stored I-94 is over a year old,
re-pull it to confirm no newer admission exists instead of trusting the copy on
file.

## Step 3 — Get the forms fresh and verify their editions

Never fill a PDF stored in the case folder. A firm-stored copy can have a
silently broken AcroForm, and it will be whatever edition was current when
someone saved it — both stored O-1 precedents are on a superseded I-129 edition.

```bash
$PY scripts/uscis_forms.py fetch i-129 i-907 g-1650 g-28 --out forms
# drop g-28 on a no-G-28 case
```

This downloads each form, counts AcroForm fields against page widgets to prove
the form tree is intact, reads the edition from the footer, scrapes the Edition
Date from that form's own USCIS page, and compares the two. It exits non-zero
and tells you what to resolve if anything disagrees.

The USCIS page is the authority, not the footer. G-28's footer says it expired in
2021 while its page says the 09/17/18 edition is still usable — read the page's
wording rather than reasoning from the printed date.

**If a form's current edition differs from what the 填表指令 doc and
`references/` record, stop and tell the user before filling anything.** A new
edition can move field names and renumber items, which silently invalidates every
Page/Part/Item pointer in those files — the fill would appear to succeed while
landing values in the wrong places. Re-derive the affected field map, update the
doc and the reference, then fill.

**If the edition moved since the field maps were written, diff before filling.**
Pull the `get_fields()` key sets of the old and new PDFs and look at what
disappeared: that is how the one O-1-relevant change between I-129 01/20/25 and
02/27/26 was found (Part 5 item 15 went from one radio group to two independent
checkboxes, so the old key applies nothing at all). Update the reference file
with what you find so the next case doesn't rediscover it.

## Step 4 — Fill through real AcroForm fields

Values come from section 三 of the filled doc, which also names each fact's
form/page/Part/Item destination; the reference file gives the actual field name.
Section 一.2 lists the fields that differ between the with-G-28 and no-G-28
versions.

Read the field map for the form, build `{field_name: value}` JSON, then:

```bash
$PY scripts/uscis_forms.py fill forms/i-129.pdf values-i129.json --out out/i-129.pdf
```

`fill` goes page by page through each field's own appearance stream, which is
what makes narrow boxes and comb-style fields come out centred and unclipped.
It reports any key that matched no widget — **treat that list as an error, not a
warning**. An unapplied field is the main way this work goes wrong quietly: the
script says it wrote the file, the value simply isn't there.

Traps that have each cost a real correction:

- **Checkbox export values are not guessable.** Write the value `dump` reports
  under `on=`. Some are ordinary (`/Y`, `/N`), some are per-option (`/A`…`/F` on
  I-129 Part 2 item 4, `/CON`/`/PFI`/`/POE` for office type), and the Apt/Ste/Flr
  radios carry literal spaces: `"/ STE "`, not `"STE"`.
- **Yes/No is sometimes two fields, not one group.** I-129 Part 5 item 15 and the
  O supplement item 8 are pairs of independent checkboxes that both have on-state
  `/Y`; you pick the answer by choosing *which field* to set. Setting both ticks
  both.
- **Field names lie about position.** G-28's `Line6_EMail` is the phone box.
  I-907's `P3_Line5_MobileTelePhoneNumber[1]` is the fax box. I-129 Part 5 field
  names run one item behind the printed numbers. G-1650's `CB_CreditCardType` is
  the Checking/Savings pair. Resolve by rect from `dump`, never by the name.
- **Continuation pages repeat the name at index `[1]`.** G-28 page 4 and I-907
  page 7 both do this, per the form's instruction to put your name atop every
  extra sheet. Easy to fill the main name field and miss these.
- **Phone numbers are plain digits** — `8186658535`, not `(818) 665-8535`. Some
  boxes are narrower than they look and truncate formatted numbers silently.
- **Dropdowns need exact `/Opt` matches** — `CA`, not `California`.
- **Leave every signature and its date blank** unless the case is at the stage of
  recording an executed date. Signatures are wet-ink or e-signed by the actual
  person.
- **Never invent firm-sensitive data** — bar number, bank routing/account. Take
  it from `references/fees-and-filing.md` or a real prior filing, and ask if
  neither has it.

### The three G-1650s

One form per payment, never combined — USCIS requires the premium processing fee
to be submitted separately. Amounts, and the Small Employer logic that sets two
of them, are in `references/fees-and-filing.md`. **Verify them against the
current G-1055 every time**: the stored precedents paid $2,805 for premium
processing, which is now $2,965.

Before moving on, reconcile: I-129 Part 5 item 15 (Small Employer Yes/No), item
14 (employee count), and the two fee amounts have to tell one consistent story.

Naming them by amount (`g-1650-530.pdf`, `g-1650-300.pdf`, `g-1650-2965.pdf`) is
the convention one precedent already uses and it makes the mismatch obvious at a
glance.

## Step 5 — Read every filled page back with your eyes

```bash
$PY scripts/uscis_forms.py render out/i-129.pdf --out render --pages 1-8
$PY scripts/uscis_forms.py dump out/i-129.pdf --filled-only
```

Then actually look at the images against the intended values. A clean script run
proves the values were written, not that they were right — this is how you catch
a sex checkbox that was never assigned, a passport issue date sitting in the
expiry box, or text spilling out of a box. `dump --filled-only` is the fast
complement: it shows everything that carries a value, so a field you never meant
to touch stands out.

Check the O supplement pages (28–30) specifically. They carry the classification
box, the ownership question, and the consultation answers — the parts that make
it an O-1 petition rather than a generic I-129.

## Step 6 — Extract the pages needing a client signature

Pull the pages needing the **petitioner's own** signature (not the attorney's)
into one PDF for signing. Identify them from each form's own "Signature of..."
blocks rather than a remembered page number — page numbers shift between
editions. In a standard package that is I-129 Part 7 (page 7), the O supplement
Section 2 (page 30), I-907 Part 3, and G-28 Part 4.

Name the output so its state is unmistakable — the precedents use
`i-129 waiting signature.pdf` / `i-907 sigend.pdf`, which is a good habit. A
filled package with blank signature fields is **not mailable**; say so
explicitly when reporting completion rather than letting "filled" read as
"ready to ship".

## Step 7 — Upload back to Drive and log it

Upload the filled PDFs to the case's forms folder with names that say what they
are and what edition they're on, then delete the local copies — they contain
client PII and the scratchpad is not where this data should live.

Confirm the filing address before anything gets mailed: it depends on the
petitioner's office state *and* on whether I-907 is in the same envelope, and the
premium and non-premium tables split the states differently. Look it up on
`uscis.gov/i-129-addresses`; `references/fees-and-filing.md` has the current
California-with-premium answer as a starting point, not as a substitute.

If the case folder has an Activity Log, append a dated, attributed entry naming
which forms were filled, at which editions, and what remains outstanding.

---

## Learning from the stored precedents

Three completed filings (YUQIAN TAO_O1A Aug 2026 on the current edition; Xiran
Liu O1B and Ziqing Shi on the superseded 01/20/25) were read once to build the
field maps and to learn the firm's Fixed data. That work is done and it lives in
`references/`.

**Do not reopen them to fill a new case.** They are not inputs to the job: the
current blank form plus the case's own 填表指令 doc are. Going back to an old
filing is how stale firm data (`8186658535`, a blank bar number) and superseded
field names get reintroduced. If something is genuinely missing from
`references/` and the form's own instructions don't settle it, say so and ask —
don't reconstruct it from a precedent.

The one lesson from that exercise worth carrying: **resolve every checkbox by
rect against the printed label, never by reading order.** The I-907 Part 1 item 8
options are interleaved (`/B` is attorney-for-petitioner, `/D` is
attorney-for-applicant), and pairing labels to boxes in text order gets it
backwards — which is exactly the mistake an earlier version of these notes made.

If you learn something new about a form — a moved field, a corrected firm value,
a fee change — write it back into the relevant reference file so the next case
starts from it.
