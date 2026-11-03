> **这是 `eb1a` 的完整 playbook。** 由 `skye-forms` 的 Step 1 路由进来，进来之后**从头读完**。
> 文中所有 `references/…`、`scripts/…`、`assets/…` 路径，都相对于 `<skill>/eb1a/`。

# EB-1A form filling (Lingtu Law · 人才移民)

An EB-1A filing is two to four forms plus two or three payments, and almost every
error in it is silent — a checkbox whose export value didn't match, a field name
that moved in a new edition, a fee that was right last quarter. So the shape of
this skill is: work from a written instruction doc, get the forms fresh, learn the
client's facts from their own case folder, fill through real AcroForm fields, then
read the result back with your eyes.

The set is **I-140, plus G-28 when the firm is attorney of record, I-907 when
premium processing is requested, G-1145, and one G-1650 per fee**. There is no
I-129, no supplement, no labor certification — an EB-1A is a self-petition on the
strength of the beneficiary's own record, which is why almost every "petitioner"
box on the I-140 points back at the beneficiary.

**Fill only from freshly downloaded official forms — never from a previous case's
PDF or a stored sample.** Those carry superseded editions (field names move),
can have damaged AcroForms, and drag stale data forward. Values come from the
case's filled 填表指令 doc; positions come from the current form's own printed
item numbers. The reference field maps here are navigation aids for those
positions — not a licence to copy answers from an old filing.

| File | When to read |
|---|---|
| `references/i-140.md` | before touching the I-140 — full field map, and the three firm-wide defaults |
| `references/g28-i907-g1650-g1145.md` | before touching G-28, I-907, G-1650 or G-1145 |
| `references/fees-and-filing.md` | fees, filing addresses, firm fixed data, Drive ids, the two learning precedents and their known defects, environment quirks on this Mac |
| `assets/eb1a-fill-instructions.md` | the markdown source of the 填表指令 master doc — use it to recreate or repair the Drive copy |

Two scripts: `scripts/uscis_forms.py` (fetch / dump / fill / render) and
`scripts/cjk_stamp.py`, which exists because **the I-140's Chinese fields cannot be
filled the ordinary way** — see below.

Setup, once per session:

```bash
export PATH="$HOME/.local/bin:$PATH"          # gws
PY=~/.local/opt/pdfvenv/bin/python            # pypdf + cryptography + reportlab
```

`cjk_stamp.py` needs reportlab in that venv (`$PY -m pip install reportlab`).

If `gws` 401s or says `invalid_grant`, run `gws auth login -s drive`, print the
URL, and let the user approve it in their own browser. Never handle their
password or 2FA.

---

## The three firm-wide defaults

These are decided policy, not per-case judgment. They apply to **every** I-140
this skill fills. The first two live on page 2, the third on page 3.

### 1. Part 4 Processing Information is always CP, Guangzhou, China

| Printed item | Field | Value |
|---|---|---|
| Part 4, 1.a. "Alien will apply for a visa abroad at a U.S. Embassy or U.S. Consulate at:" | `Line1a_Visa[0]` | `/1a` |
| Part 4, 1.b. City or Town | `Line1a_CityorTown[0]` | `Guangzhou` |
| Part 4, 1.c. Country | `Line1a_Country[0]` | `China` |
| Part 4, 2.a. "Alien is in the United States and will apply for adjustment of status" | `Line1b_Status[0]` | leave off |

Consular processing at Guangzhou is the default even when the beneficiary is
sitting in the US on an F-1 — the two boxes are mutually exclusive and the firm
files CP. Both stored precedents do exactly this. Depart from it only on an
explicit instruction from the attorney, and if you do, say so in the report.

**Consequence to keep straight:** on a CP case the dependents in Part 7 answer
"applying for a visa abroad" = Yes and "applying for adjustment of status" = No.
The Qing Yang precedent ticked Yes to *both* for the spouse, which is a
contradiction — see `references/fees-and-filing.md`.

### 2. The last-arrival block is filled only if the beneficiary is in the US

Page 2's *Information About His or Her Last Arrival in the United States* block
(printed items 10 through 11.c) is conditional. The form itself says so: "If the
person for whom you are filing is in the United States, provide the following
information."

| Beneficiary | 10. Date of Last Arrival | 11.a. I-94 number | 11.b. Authorized stay expires | 11.c. Status on I-94 |
|---|---|---|---|---|
| **in the US** | from the I-94 | from the I-94 | from the I-94 | from the I-94 |
| **outside the US** | blank | **`Not in U.S.`** | blank | blank |

Items 12–15 (passport number, travel document, country of issuance, expiry) are
**not** part of the conditional block — they are filled either way, from the
passport.

**`Not in U.S.` is exactly 11 characters, and item 11.a is a comb field with
`MaxLen 11`.** "Not in the U.S." does not fit: the fill silently truncates it to
`Not in the` and the script only warns in passing. Verified by rendering — the
11-cell comb shows `N o t   i n   U . S .` and reads correctly. If someone asks
for different wording, count the characters first.

The Chujun Yang precedent (beneficiary abroad) left 11.a **blank**. This rule is
the firm's correction to that, so do not treat the precedent as authority here.

### 3. Page 3, Part 4 splits into three blocks — English address, Chinese name, Chinese address

| Printed | Field | What goes in it |
|---|---|---|
| 2.b | `Line1b_Country[0]` | the applicant's **country of birth**, in English (`China`) |
| 3.a – 3.f | `Line2a_StreetNumberName[0]`, `Line2b_Unit[*]`/`Line2b_AptSteFlrNumber[0]`, `Line2c_CityOrTown[0]`, `Line2e_Province[0]`, `Line2d_PostalCode[0]`, `Line2f_Country[0]` | that country-of-birth address, **in English / pinyin** |
| 4.a – 4.c | `Line3a_FamilyName2[0]` / `Line3b_GivenName2[0]` / `Line3c_MiddleName2[0]` | the applicant's **Chinese name** |
| 5.a – 5.g | `Line2a_InCareofName[1]`, `Line3d_StreetNumberName[0]`, `Line3e_Unit[*]`/`Line3e_AptSteFlrNumber[0]`, `Line3f_CityOrTown[0]`, `Line3h_Province[0]`, `Line3g_PostalCode[0]`, `Line3i_Country[0]` | the **same foreign address in Chinese characters** |

So the foreign address is entered twice — romanised in 3.a–3.f, in Chinese in
5.a–5.g — with the Chinese name sandwiched between them at 4.a–4.c. The form's own
heading calls 4.a–5.g the native-alphabet name and address, which for these clients
means Chinese.

Two cautions:

- **2.b is printed as "current country of residence or, if now in the United
  States, last country of permanent residence abroad."** For the great majority of
  these clients country of birth and country of residence are the same, so the
  firm rule is safe. **When they differ — born in China, living in Canada — follow
  the printed question and confirm with the attorney**, rather than applying the
  rule mechanically.
- Both address blocks carry the Province/Postal Code field-name inversion
  (`Line2e_Province` is printed 3.d, `Line2d_PostalCode` is printed 3.e; same for
  5.e/5.f). Position by the printed item number, never by the field name.

The most common way to get this wrong is filling the Chinese address into 3.a–3.f.
Check it on the render.

---

## Step 0 — Get this case's 填表指令 doc in front of you

Nothing gets filled from memory or from a previous case. Each fill run is driven
by a per-case copy of the instruction doc, so the client's facts and the field
destinations live in one place the whole team can read and correct.

**The doc always comes from the same place, and the finished forms always go
somewhere else — the client folder the user names in the request.**

| | Where | Id |
|---|---|---|
| **Read the doc from** (every run) | `0.testing` → `Test EB1A` → `2. Form` | folder `1WQuI4s1EcXucb7YI16eF-7iWEnNkW_DB` |
| **Write the filled forms to** | whichever client Drive folder the request names | — |

1. Read the doc from `Test EB1A / 2. Form`. Its sections: **一** the case
   parameters, **二** the firm's Fixed data, **三** the client-facts worksheet with
   each fact's page/Part/Item destination, **四** fees and the G-1650s, **五**
   signatures and mailing, **六** the post-fill self-check, **七** the materials
   checklist.
2. Write this client's facts into a **copy** — either one dropped into the output
   folder named for the client (`EB1A 填表指令 — <Client>`), or a working copy of
   your own. That filled copy, not your context and not a previous case, is what
   Step 4 pulls values from.
3. **Never record one client's facts in the `Test EB1A` doc itself** — it is the
   source every future run reads. Corrections to the *instructions* (a moved
   field, a changed firm value, a new fee) do belong there, mirrored into
   `references/` here so the two don't drift.
   `assets/eb1a-fill-instructions.md` is the markdown source if the Drive copy
   ever needs rebuilding.

If the doc and a reference file disagree, work out which is stale rather than
picking one — and say which you corrected.

## Step 1 — Settle the case parameters

Everything downstream forks on these, so settle them before reading a single
form. Section 一 of the doc is where the answers get written down.

Three things arrive **as instructions** rather than being derived: whether this
case has a **G-28**, whether the client is paying for **premium processing**, and
the **worksite state** (which decides the lockbox). If the instruction is silent
on any of them, ask.

### 1a. With G-28 or without

The primary fork; it reaches every form in the set.

| | **with G-28** (firm files as attorney of record) | **without G-28** (self-petitioner files) |
|---|---|---|
| G-28 | yes, Part 3 client role `/P` **Petitioner** | not filed |
| I-140 page 1 attorney block | tick `G28CheckBox[0]` = `/Y`, fill bar number `348794`, attorney USCIS account `063938833828` | leave the whole block blank |
| I-140 mailing address (Part 1 item 3, Part 3 item 2) | the firm address, so notices route through the firm | the beneficiary's own US address |
| I-907 Part 1 | attorney's name + firm address; tick the G-28 box; bar number | self-petitioner's name + address; both left blank |
| I-907 Part 1 item 8 | **`/B`** attorney for the petitioner | **`/A`** I am the petitioner |
| I-907 Part 3 contact | firm phone / fax / email | client's own phone / email |
| G-1145 | firm mailbox (`cassie@lingtulaw.com`) + firm phone | see the note in `references/g28-i907-g1650-g1145.md` — the no-G-28 precedent has no G-1145 at all; ask |
| G-1650 bank block | the firm's ACH account, in full | the precedent left it empty — **ask who pays before filling** |
| RFEs / approval notices go to | firm address | the client's address; nothing routes through the firm |

Decide it from whether this case actually has a signed G-28, not from what a
previous case did: the two stored precedents are one of each.

### 1b. Premium processing or not

Premium processing is available for the E11 classification and costs **$2,965**.
It is an extra form (I-907), an extra payment (its own G-1650), **and a different
lockbox** — see `references/fees-and-filing.md`.

- Qing Yang (no G-28) filed I-907. Chujun Yang (with G-28) did not.
- The premium fee must be paid **separately** from the other fees. That is the
  reason it gets its own G-1650 rather than being folded in.
- I-907 may not be filed by a beneficiary or co-applicant of the primary form. On
  a self-petition the beneficiary *is* the petitioner, so this is fine — but say
  so rather than leaving a reader to wonder.

### 1c. Who is the petitioner

Almost always **the beneficiary themself** — I-140 Part 5 item 1.b. `Self`
(`Line1b_Self[0]` = `/Y`). That single checkbox is what makes the rest of the
form coherent:

- Part 1 (person or organization filing) = the beneficiary's own name and
  address, item 2 Company Name left blank
- Part 5 items 2–8 (type of business, date established, employees, income,
  NAICS, labor certification) are company-only; the precedents put `N.A.` in
  item 2 and leave the rest blank
- Part 5 items 11 and 12 (Occupation, Annual Income) **are** filled — they are
  the "if an individual is filing this petition" block
- Part 6 item 7 "Is this a new position?" and the worksite address describe the
  beneficiary's intended US employment, which on a CP case is often not settled;
  the Chujun Yang precedent wrote `To be determined` in the worksite street box
  and explained it in Part 11

An employer-filed EB-1A (Part 5 item 1.a `Employer`) is possible but rare here.
If the intake describes one, the asylum program fee changes — see the fee table.

## Step 2 — Read the client's facts from their own case folder

EB1A case folders live in the 人才移民 shared drive under the `EB1A` folder;
`references/fees-and-filing.md` has the ids. Find this client's folder by name,
then read the intake material — `个人信息` / `Personal Information_EB1A.docx`,
passport scan, visa page, I-94, I-20, marriage certificate, CV.

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

**Write each fact into section 三 of this case's 填表指令 copy as you find it**,
then build the values JSON from that. Going through the doc rather than straight
from intake to JSON is what makes the work reviewable — a colleague can check
section 三 against the passport without reading any code.

Section 三 deliberately mirrors the firm's own `Personal Information_EB1A.docx`
wording so nobody has to translate between two vocabularies. What that
questionnaire does **not** carry, and you must read off documents:

| Fact | Source |
|---|---|
| passport number, country of issuance, expiry | passport bio page |
| I-94 number, date of last arrival, class of admission, admit-until date | the I-94 itself (only if the beneficiary is in the US) |
| A-Number, SSN | prior filings / EAD / SSN card, if any |
| state or province of birth | intake gives city+province together — split it |

Aim to have the whole picture before filling anything, and leave a gap marked as
a gap rather than inventing it — a plausible-looking invented I-94 number is
worse than a blank you flagged.

### The I-94, when the beneficiary is in the US

If the beneficiary is inside the US, items 10, 11.a, 11.b and 11.c come off the
I-94 (`Admission Date`, the record number, `Admit Until Date`, `Class of
Admission`) and nowhere else. An I-20's OPT end date is a different fact and
substituting it misstates the record.

**If the case folder has no I-94 — or the one on file is over a year old — go get
one.** Drive it with the browser tools; `gws` cannot do this.

1. Open `https://i94.cbp.dhs.gov/search/recent-search` → "Get Most Recent
   I-94/I-95" and drive it to the lookup form.
2. **The page opens a Terms of Service dialog that must be scrolled and accepted
   before the form unlocks. Do not click that acceptance yourself — hand it to
   the user.** Those same terms prohibit automated access, so an agent clicking
   "I agree" would be asserting agreement to a condition it is not meeting.
3. Give the user the five values ready to paste — **Last/Surname, First (Given)
   Name, Date of Birth, Passport Number, Passport Country of Issuance** — all of
   which the I-140 already needs. Leave the tab open on the form.
4. Once they save the result page as a PDF into the case's forms folder
   (`I-94 <Client Name>.pdf`), fill the four boxes from it.

The saved PDF is the only artifact showing where those values came from, which is
what makes them checkable by a colleague or an officer.

**Scope this tightly**: one record at a time, only for a client the firm is
actively representing, only for this filing — never over a list. **Which passport
number**: the one the beneficiary actually entered on, which is not always the
current passport.

If the beneficiary is outside the US, skip all of this — item 11.a gets
`Not in U.S.` and nothing else in the block is filled.

## Step 3 — Get the forms fresh and verify their editions

```bash
$PY scripts/uscis_forms.py fetch i-140 g-28 i-907 g-1650 g-1145 --out forms
# drop g-28 on a no-G-28 case; drop i-907 when premium isn't requested
```

This downloads each form, counts AcroForm fields against page widgets to prove
the form tree is intact, reads the edition from the footer, scrapes the Edition
Date from that form's own USCIS page, and compares the two. It exits non-zero and
tells you what to resolve if anything disagrees.

The USCIS page is the authority, not the footer. G-28's footer says it expired in
2021 while its page still lists 09/17/18 as the edition date — read the page's
wording rather than reasoning from the printed date.

**If a form's current edition differs from what the 填表指令 doc and
`references/` record, stop and tell the user before filling anything.** A new
edition can move field names and renumber items, which silently invalidates every
Page/Part/Item pointer in those files. Re-derive the affected field map, update
the doc and the reference, then fill. Diff the old and new `get_fields()` key
sets — what disappeared is what moved.

## Step 4 — Fill through real AcroForm fields

Values come from section 三 of the filled doc, which also names each fact's
page/Part/Item destination; the reference file gives the actual field name.

```bash
$PY scripts/uscis_forms.py fill forms/i-140.pdf values-i140.json --out out/i-140.pdf
```

`fill` goes page by page through each field's own appearance stream, which is what
makes narrow boxes and comb-style fields come out centred and unclipped. It
reports any key that matched no widget — **treat that list as an error, not a
warning**. An unapplied field is the main way this work goes wrong quietly: the
script says it wrote the file, the value simply isn't there.

Traps that have each cost a real correction, I-140 first:

- **The I-140's field names do not match its printed item numbers.** In Part 3's
  Other Information block the names run two ahead (printed item 3 Date of Birth is
  `Line5_DateOfBirth`); in the arrival block they run one behind (printed 11.a is
  `Line14a_ArrivalDeparture`, printed 11.c is `Line15_CurrentNon`); in every
  address block the letters are offset (printed 3.a is `Line6a_...` in Part 1).
  Resolve by rect from `dump`, never by the name.
- **Province and Postal Code are swapped in every address block.** On page 1,
  printed 3.g Province is `Line6h_Province` and printed 3.h Postal Code is
  `Line6g_PostalCode`. Same inversion on page 2 (2.g / 2.h) and twice on page 3
  (3.d / 3.e and 5.e / 5.f).
- **Printed Part numbers are one ahead of the field prefixes on pages 6–7.**
  Printed Part 8 (petitioner's contact + signature) uses `Part7_*` fields;
  printed Part 9 (interpreter) uses `Part8_*`; printed Part 11 (additional
  information) uses `Pt9Line*`.
- **Yes/No is two independent checkboxes, not one radio group.** `Line5_Yes[0]` /
  `Line5_No[0]`, `P1_Line5_Checkbox[1]` / `[0]`, and so on. Set **only** the one
  you want, to its own on-state. The precedents set both members to the same
  value; it happens to render correctly because the other box's on-state doesn't
  match, but it is not a pattern to copy.
- **Item 11.a is a comb field with `MaxLen 11`.** See the firm-defaults section.
- **Part 7 persons 3–6 (page 5) have mismatched indices** — the name/DOB fields
  and the country/relationship fields for the same person carry different `[N]`.
  If a case has more than two dependents, re-derive that page with `dump` by
  rect.
- **Checkbox export values are not guessable.** Write the value `dump` reports
  under `on=`. The Apt/Ste/Flr radios carry literal spaces: `"/ APT "`, not
  `"APT"`. Part 2's petition type is `/a`…`/h`; Part 4's is `/1a` / `/1b`.
- **Continuation pages repeat the name at index `[1]`.** I-140 page 8, G-28 page
  4, I-907 page 7. Easy to fill the main name field and miss these.
- **Phone numbers are plain digits** — `4155479999`, not `(415) 547-9999`.
- **Dropdowns need exact `/Opt` matches** — `CA`, not `California`.
- **Leave every signature and its date blank** unless the case is at the stage of
  recording an executed date. Signatures are wet-ink or e-signed by the person.
- **Never invent firm-sensitive data** — bar number, bank routing/account. Take
  it from `references/fees-and-filing.md` and ask if it isn't there.

### The Chinese fields need a second pass

`fill` cannot write the Chinese answers rule 3 requires. The I-140's text fields
carry a Helvetica `/DA`, which has no CJK glyphs: pypdf stores 杨 correctly but the
appearance stream it generates renders every character as `?`. Acrobat would
regenerate with a substituted font; Preview.app and poppler will not — so what
prints is `?`. Verified by render.

So fill everything else first, then stamp the Chinese:

```bash
$PY scripts/uscis_forms.py fill forms/i-140.pdf values-i140.json --out out/step1.pdf
$PY scripts/cjk_stamp.py out/step1.pdf cjk-values.json --out "out/i-140-waiting signature.pdf"
```

`cjk_stamp.py` finds each named field by rect, clears it, and draws the text there
with an **embedded** TrueType (Songti.ttc on this Mac). The embedding is the point:
reportlab's built-in `STSong-Light` CID font is not embedded, so Acrobat shows it
and poppler shows *nothing at all* — an invisible answer, which is worse than `?`
because the read-back looks like an empty box you forgot. Never accept that
fallback.

Consequences to report each time: the Chinese is page content, not a form value,
so the field reads empty in Acrobat and cannot be edited by typing over it. To
change a Chinese answer, re-run fill + stamp.

Two length traps in the same neighbourhood, both found on a live case:

- **Part 4 item 3.a has `MaxLen 34`.** A full romanised street line truncates
  silently. Keep 3.a short and put the whole address in Part 11.
- **Part 11's text boxes are multiline, but pypdf does not wrap.** It writes one
  long line and everything past the right edge is invisible. Put explicit `\n`
  breaks in the value (~40 characters per line) and check the render.

### The G-1650s

One form per payment, never combined. A standard EB-1A self-petition is:

| # | What | Amount | Naming |
|---|---|---|---|
| 1 | I-140 paper filing fee | $715 | `g-1650-715.pdf` |
| 2 | Asylum Program Fee (self-petitioner rate) | $300 | `g-1650-300.pdf` |
| 3 | I-907 premium processing (E11) — only if requested | $2,965 | `g-1650-2965.pdf` |

Naming them by amount is the convention both precedents use and it makes a
mismatch obvious at a glance. **Verify all three against the current G-1055 every
time.** Amounts, the employer-size logic, and the "self-petitioner" wording that
earns the $300 rate are in `references/fees-and-filing.md`.

## Step 5 — Read every filled page back with your eyes

```bash
$PY scripts/uscis_forms.py render out/i-140.pdf --out render --pages 1-8
$PY scripts/uscis_forms.py dump out/i-140.pdf --filled-only
```

Then actually look at the images against the intended values. A clean script run
proves the values were written, not that they were right — this is how you catch a
ZIP code with two digits transposed (the Qing Yang precedent has exactly that in
two places), a passport issue date sitting in the expiry box, or text spilling out
of a box. `dump --filled-only` is the fast complement: everything carrying a value
shows up, so a field you never meant to touch stands out.

Check pages 2 and 3 specifically every time — they carry all three firm defaults,
and every one of them is an invisible failure if it lands wrong. On page 3 look at
which alphabet is in which block: Chinese characters in 3.a–3.f means the two
address blocks got swapped.

## Step 6 — Extract the pages needing a client signature

Pull the pages needing the **client's own** signature (not the attorney's) into one
PDF for signing. Identify them from each form's own "Signature of..." blocks
rather than a remembered page number — page numbers shift between editions. In a
standard package that is I-140 Part 8 (page 6), I-907 Part 3, and G-28 Part 4.

Name the output so its state is unmistakable — the precedents use
`i-140-waiting signature.pdf` / `g-28- waiting signature.pdf`, which is a good
habit. A filled package with blank signature fields is **not mailable**; say so
explicitly when reporting completion rather than letting "filled" read as "ready
to ship". Qing Yang's folder also keeps a `签名教程.pdf` and a `signed & scanned`
subfolder — follow that pattern for the client hand-off.

## Step 7 — Upload back to Drive and log it

Upload the filled PDFs to the case's forms folder with names that say what they
are, then delete the local copies — they contain client PII and the scratchpad is
not where this data should live.

Confirm the filing address before anything gets mailed. For the I-140 it depends
on **where the beneficiary will work** — not the petitioner's address, which is
the habit I-129 work builds — and on whether I-907 and/or I-485 travel in the
same envelope. `references/fees-and-filing.md` has the full current table; on a
CP case with no settled worksite, ask the attorney which state to file from
rather than guessing a lockbox.

If the case folder has an Activity Log, append a dated, attributed entry naming
which forms were filled, at which editions, and what remains outstanding.

---

## Learning from the stored precedents

Two completed filings were read once, on 2026-08-20, to build the field maps and
learn the firm's data: **Qing Yang** (no G-28, self-petition, beneficiary in the US
on F-1, with I-907) and **Chujun Yang** (with G-28, self-petition, beneficiary
abroad, no I-907). That work is done and it lives in `references/`.

**Do not reopen them to fill a new case.** They are not inputs to the job: the
current blank form plus the case's own 填表指令 doc are. Both carry confirmed
defects — a transposed bar number, two transposed ZIP codes, contradictory
dependent answers, half-empty G-1650s — all catalogued in
`references/fees-and-filing.md`. Copy their structure, never their contents.

If you learn something new about a form — a moved field, a corrected firm value, a
fee change — write it back into the relevant reference file so the next case starts
from it.
