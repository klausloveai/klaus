> **这是 `niw` 的完整 playbook。** 由 `skye-forms` 的 Step 1 路由进来，进来之后**从头读完**。
> 文中所有 `references/…`、`scripts/…`、`assets/…` 路径，都相对于 `<skill>/niw/`。

# EB-2 NIW form filling (Lingtu Law · 人才移民)

An NIW filing is four to seven forms across two agencies plus two or three
payments, and almost every error in it is silent — a checkbox whose export value
didn't match, a field name that moved in a new edition, a fee that was right last
quarter. So the shape of this skill is: work from a written instruction doc, get
the forms fresh, learn the client's facts from their own case folder, fill through
real AcroForm fields, then read the result back with your eyes.

The set is **I-140, ETA-9089 Appendix A + Appendix C + Final Determination, plus
G-28 when the firm is attorney of record, I-907 when premium processing is
requested, G-1145 when it is not, and one G-1650 per fee.**

**Fill only from freshly downloaded official forms — never from a previous case's
PDF or a stored sample.** Those carry superseded editions, can have damaged
AcroForms, and drag stale data forward. On this form set that is not a theoretical
risk: **75 of ETA-9089 Appendix A's field names changed at the last edition
boundary**, and the two stored 9089 precedents are on the old one.

| File | When to read |
|---|---|
| `references/i-140.md` | before touching the I-140 — full field map, and what differs from the firm's EB-1A I-140 |
| `references/eta-9089.md` | before touching Appendix A, Appendix C or the Final Determination |
| `references/g28-i907-g1650-g1145.md` | before touching G-28, I-907, G-1650 or G-1145 |
| `references/fees-and-filing.md` | fees, filing addresses, firm fixed data, Drive ids, the three precedents and their defects, environment quirks on this Mac |
| `assets/niw-fill-instructions.md` | the markdown source of the 填表指令 master doc — use it to recreate or repair the Drive copy |

Two scripts: `scripts/forms.py` (fetch / dump / fill / render, USCIS **and** DOL)
and `scripts/cjk_stamp.py`, which exists because **the I-140's Chinese fields
cannot be filled the ordinary way** — see below.

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

## The three NIW rules

These apply to **every** NIW I-140 this skill fills.

### 1. Part 2 is 1.h, the NIW box — never 1.d

Page 2, Part 2 item **1.h**, "An alien applying for an NIW (who **IS** a member of
the professions holding an advanced degree or an alien of exceptional ability)":
field `prt2PetitionType[6]`, export value `/h`. All three precedents do this and
the firm's own NIW Checklist lists it as a thing to verify by hand.

**1.d is the trap.** Its printed text also mentions advanced degree and
exceptional ability — but it reads "who is **NOT** seeking a National Interest
Waiver". Ticking it asks USCIS for the wrong classification.

Whatever goes here must agree with I-907 Part 2 item 3, which reads `EB-2 NIW`.

### 2. Part 4 Processing Information is always CP, Guangzhou, China

| Printed item | Field | Value |
|---|---|---|
| Part 4, 1.a. "Alien will apply for a visa abroad at a U.S. Embassy or U.S. Consulate at:" | `Line1a_Visa[0]` | `/1a` |
| Part 4, 1.b. City or Town | `Line1a_CityorTown[0]` | `Guangzhou` |
| Part 4, 1.c. Country | `Line1a_Country[0]` | `China` |
| Part 4, 2.a. "Alien is in the United States and will apply for adjustment of status" | `Line1b_Status[0]` | leave off |

Consular processing at Guangzhou is the default even when the beneficiary is
sitting in the US on an H-1B. The Checklist states it as "Page 2, Part 4, Q1a:
Yes? Guangzhou, China?". Depart from it only on an explicit instruction from the
attorney, and if you do, say so in the report.

**Fill all three boxes.** Ticking `/1a` and leaving 1.b and 1.c empty — a consular
box naming no consulate — has shipped on a filed form, as has leaving the whole of
item 1 blank.

**Consequence to keep straight:** on a CP case the dependents in Part 7 answer
"applying for a visa abroad" = Yes and "applying for adjustment of status" = No.

### 3. The last-arrival block comes off the client's I-94, and only if they are in the US

Page 2's *Information About His or Her Last Arrival in the United States* block
(printed items 10 through 11.c) is conditional — the form says "If the person for
whom you are filing is in the United States, provide the following information."

| Client | 10. Date of Last Arrival | 11.a. I-94 number | 11.b. Authorized stay expires | 11.c. Status on I-94 |
|---|---|---|---|---|
| **in the US** | from the I-94 | from the I-94 | from the I-94 | from the I-94 |
| **not in the US** | blank | **`Not in U.S.`** | blank | blank |

Three things follow from that:

- **On an F-1 or J-1, item 11.b is `D/S`.** That is what a duration-of-status I-94
  actually shows, and the firm's Checklist states it as a rule ("Page 2, Part 3,
  Q11b: If F1 or J1 status, write 'D/S' instead of specific date"). Substituting a
  date — an I-20 program end date, an OPT end date — misstates the record.
- **The value for 11.a is `Not in U.S.`, exactly 11 characters.** Item 11.a is a
  comb field with `MaxLen 11`, verified on the current blank. `not in the U.S.` is
  15 characters: the fill warns once, stores the full string, and the printed
  appearance shows `n o t  i n  t h e` with the `U.S.` gone — verified by rendering
  both. 11 cells is a hard limit, so count the characters before changing the
  wording.
- **Items 12–15 are outside the block.** Passport number, travel document, country
  of issuance and expiry are filled either way, from the passport. The passport
  number at item 12 is a commonly missed box.

A client living abroad who once visited on a since-expired visa is **not in the
US**: 11.a reads `Not in U.S.` and the rest stays blank. Filling the block from a
stale admission has shipped on a filed form and is the wrong answer.

### The addresses are the applicant's

Not a special rule, but worth saying once because the EB-1A work builds a
different habit: I-140 Part 1 item 3 and Part 3 item 2, G-28 item 13, and I-907
printed item 8 all ask for **the applicant's own address**, so that is what goes in
them. Attorney representation does not change what those questions ask.

---

## Step 0 — Get this case's 填表指令 doc in front of you

Nothing gets filled from memory or from a previous case. Each fill run is driven
by a per-case copy of the instruction doc, so the client's facts and the field
destinations live in one place the whole team can read and correct.

| | Where | Id |
|---|---|---|
| **Read the doc from** (every run) | `0.testing` → `Test NIW` → `2. Form` | folder `1-ugvpZGYxWp_zQoOujMQHb6M-i1AOPaP` |
| **Write the filled forms to** | whichever client Drive folder the request names | — |

1. Read the doc from `Test NIW / 2. Form`. Its sections: **一** the case
   parameters, **二** the firm's Fixed data, **三** the client-facts worksheet with
   each fact's page/Part/Item destination, **四** the ETA-9089 worksheet, **五**
   fees and the G-1650s, **六** signatures and mailing, **七** the post-fill
   self-check, **八** the materials checklist.
2. Write this client's facts into a **copy** — either one dropped into the output
   folder named for the client (`NIW 填表指令 — <Client>`), or a working copy of
   your own. That filled copy, not your context and not a previous case, is what
   Step 4 pulls values from.
3. **Never record one client's facts in the `Test NIW` doc itself** — it is the
   source every future run reads. Corrections to the *instructions* (a moved
   field, a changed firm value, a new fee) do belong there, mirrored into
   `references/` here so the two don't drift.

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

| | **with G-28** (firm files as attorney of record) | **without G-28** (self-petitioner files) |
|---|---|---|
| G-28 | yes, Part 3 client role `/P` **Petitioner** | not filed |
| I-140 page 1 attorney block | tick `G28CheckBox[0]` = `/Y`, bar number `348794`, attorney USCIS account `063938833828` | leave the whole block blank |
| I-140 / G-28 / I-907 mailing address | the applicant's own address either way | the applicant's own address |
| I-907 Part 1 | attorney's name + firm address; tick the G-28 box; bar number | self-petitioner's name + address; both left blank |
| I-907 Part 1 item 8 | **`/B`** attorney for the petitioner | **`/A`** I am the petitioner |
| I-907 Part 3 contact | firm phone / fax / email | client's own phone / email |
| **ETA-9089 Final Determination Section C** | Cai / Shenqi / Law Office of Shenqi Cai APC | **leave Section C entirely blank** |
| **G-1650 payment method** | the firm's ACH block, filled in full | **left entirely blank** — name and amount only, the client completes their own account |
| RFEs / approval notices go to | the client's address on the forms | the client's address |

Decide it from whether this case actually has a signed G-28, not from what a
previous case did.

### 1b. Premium processing or not — and the G-1145 that hangs off it

Premium processing on an EB-2 NIW (E21 NIW) costs **$2,965** — the same as EB-1,
the fee schedule puts them in one row. It is an extra form (I-907), an extra
payment, **and a different lockbox**.

**The G-1145 is the other side of the same switch.** The firm's Checklist heads
its G-1145 section "Form G-1145 (No Premium Processing)": a premium case gets its
acceptance news through the 15-day clock, so no e-notification form. So:

- premium requested → I-907, no G-1145, three G-1650s
- no premium → G-1145 (**as the first page of the package**), no I-907, two G-1650s

The firm's filed NIW cases all used premium, so there is no worked G-1145 example
to copy.

I-907 may not be filed by a beneficiary or co-applicant of the primary form. On a
self-petition the beneficiary *is* the petitioner, so this is fine — but say so
rather than leaving a reader to wonder.

### 1c. Who is the petitioner

Always **the beneficiary themself** — I-140 Part 5 item 1.b `Self`
(`Line1b_Self[0]` = `/Y`). That single checkbox is what makes the rest coherent:

- Part 1 = the beneficiary's own name and address, item 2 Company Name blank
- Part 5 items 2–8 (type of business, date established, employees, income, NAICS,
  labor certification) are company-only; the firm puts `N/A` in item 2 and leaves
  the rest blank
- Part 5 items 11 and 12 (Occupation, Annual Income) **are** filled
- Part 6 (proposed employment) is normally filled in full — unlike the firm's
  EB-1A CP cases, an NIW client usually has a real US job
- ETA-9089 Final Determination Section D is signed by the client with the title
  **`Self-Petitioner`**

### 1d. Is this a re-file?

**Ask.** The firm has taken on an NIW after an earlier one was denied. On a
re-file, I-140 page 3 printed item 8 ("Has any immigrant visa petition ever been
filed by or on behalf of this person?") is **Yes**, with the earlier receipt
number, office and outcome written into Part 11. It is easy to default this to No,
and there is no worked example of the Yes branch to copy.

## Step 2 — Read the client's facts from their own case folder

NIW case folders live in the 人才移民 shared drive under the `NIW` folder;
`references/fees-and-filing.md` has the ids. Open **only this client's folder**,
then read the intake material — `1. Personal Information.docx`, passport scan,
visa page, I-94, I-20, marriage certificate, CV, degree certificates.

Forms subfolders are inconsistently named across older cases, so list this case
folder's children and pick by content rather than by expected name:

```bash
export PATH="$HOME/.local/bin:$PATH"
gws drive files list --params '{"q":"'"'"'<FOLDER_ID>'"'"' in parents and trashed=false","fields":"files(id,name,mimeType,size)","supportsAllDrives":true,"includeItemsFromAllDrives":true,"corpora":"allDrives","pageSize":200}'
```

Prefer the Drive connector's `read_file_content` for reading intake material: it
does server-side text extraction and OCR without pulling bytes to local disk,
which matters because these files carry passport numbers, I-94 numbers and
addresses. Keep local disk for the blank forms and the fill step only.

**Write each fact into sections 三 and 四 of this case's 填表指令 copy as you find
it**, then build the values JSON from that. Going through the doc rather than
straight from intake to JSON is what makes the work reviewable — a colleague can
check it against the passport without reading any code.

Section 三 mirrors `1. Personal Information.docx` on purpose. **That sheet is
richer than the EB-1A one**: it carries five Work Experience blocks, which feed
ETA-9089 Appendix A Section E and the Appendix C continuation sheets. What it does
**not** carry, and you must read off documents:

| Fact | Source |
|---|---|
| passport number, country of issuance, expiry | passport bio page |
| I-94 number, date of last arrival, class of admission, admit-until date | the I-94 itself (only if the beneficiary is in the US) |
| A-Number, SSN | prior filings / EAD / SSN card, if any |
| state or province of birth | intake gives city+province together — split it |
| **中文姓名 (page 3 items 4.a–4.c)** | **not on the intake sheet.** The Chinese-language exhibits in the case folder — 软著 folders, Chinese news coverage, signed Chinese contracts, 证书 — or ask the client |
| **the China address in Chinese characters (page 3 items 5.a–5.g)** | **not on the intake sheet** either; it gives the pinyin only. Same sources, or ask |
| SOC code for the job title | O*NET / the job description; must match Appendix A and the Final Determination |
| degree level, major, institution, country, mm/yyyy for **each** degree | diplomas and transcripts — the intake sheet gives only the highest |

Aim to have the whole picture before filling anything, and leave a gap marked as
a gap rather than inventing it.

**Two of those rows are the ones this step exists for.** The I-140 requires the
client's name and address in Chinese characters, and the firm's intake questionnaire
never asks for either — so they will be missing from the sheet on every case, and
the temptation is to record "client didn't provide" and ship page 3 half-empty.
That block is not optional for a Chinese national. Go and find the characters in the
Chinese-language material already sitting in the case folder before you conclude
they are unavailable; `references/i-140.md` lists where they hide and what counts as
enough evidence to write one down.

### The I-94, when the beneficiary is in the US

If the beneficiary is inside the US, items 10, 11.a, 11.b and 11.c come off the
I-94 and nowhere else, with `D/S` at 11.b for an F-1 or J-1. An I-20's OPT end date
is a different fact and substituting it misstates the record.

**If the case folder has no I-94 — or the one on file is over a year old — go get
one.** Drive it with the browser tools; `gws` cannot do this.

1. Open `https://i94.cbp.dhs.gov/search/recent-search` → "Get Most Recent
   I-94/I-95" and drive it to the lookup form.
2. **The page opens a Terms of Service dialog that must be scrolled and accepted
   before the form unlocks. Do not click that acceptance yourself — hand it to
   the user.** Those same terms prohibit automated access, so an agent clicking
   "I agree" would be asserting agreement to a condition it is not meeting.
3. Give the user the five values ready to paste — **Last/Surname, First (Given)
   Name, Date of Birth, Passport Number, Passport Country of Issuance**.
4. Once they save the result page as a PDF into the case's forms folder
   (`I-94 <Client Name>.pdf`), fill the four boxes from it.

**Scope this tightly**: one record at a time, only for a client the firm is
actively representing, only for this filing — never over a list. **Which passport
number**: the one the beneficiary actually entered on, which is not always the
current passport.

If the beneficiary is outside the US, skip all of this — item 11.a gets
`Not in U.S.` and nothing else in the block is filled. **Do not fill it from an
old expired entry**, which is how this has gone wrong before.

## Step 3 — Get the forms fresh and verify their editions

```bash
$PY scripts/forms.py fetch i-140 g-28 i-907 g-1650 g-1145 \
    eta-9089-appA eta-9089-appC eta-9089-final --out forms
# drop g-28 on a no-G-28 case; drop i-907 on a no-premium case; drop g-1145 on a premium case
```

For the USCIS forms this downloads each one, counts AcroForm fields against page
widgets to prove the form tree is intact, reads the edition from the footer,
scrapes the Edition Date from that form's own USCIS page, and compares the two.
The USCIS page is the authority, not the footer — G-28's footer says it expired in
2021 while its page still lists 09/17/18 as the edition date.

**For the three DOL forms the check is weaker, and the script says so.** dol.gov
serves the PDFs but 403s its own HTML pages from this Mac, so nothing can confirm
what DOL currently publishes. `fetch` compares the expiry in the URL against the
expiry printed in the file — which catches DOL replacing a file under the same
name — and then prints a "NOT FULLY VERIFIED" block asking for a human to open
`https://www.dol.gov/agencies/eta/foreign-labor/forms` and check the links still
read `Expires02-28-29`. **Do that, don't skip it**: Appendix A's field names
changed at the last edition boundary and would change again.

**If a form's current edition differs from what the 填表指令 doc and `references/`
record, stop and tell the user before filling anything.** A new edition can move
field names and renumber items, which silently invalidates every Page/Part/Item
pointer in those files. Re-derive the affected field map, update the doc and the
reference, then fill. Diff the old and new `get_fields()` key sets — what
disappeared is what moved.

## Step 4 — Fill through real AcroForm fields

Values come from sections 三 and 四 of the filled doc, which also name each fact's
destination; the reference files give the actual field name.

```bash
$PY scripts/forms.py fill forms/i-140.pdf values-i140.json --out out/i-140.pdf
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
  `Line14a_ArrivalDeparture`); in every address block the letters are offset.
  Resolve by rect from `dump`, never by the name.
- **Province and Postal Code are swapped in every address block.** On page 1,
  printed 3.g Province is `Line6h_Province` and printed 3.h Postal Code is
  `Line6g_PostalCode`. Same on page 2 and twice on page 3.
- **Printed Part numbers are one ahead of the field prefixes on pages 6–7.**
  Printed Part 8 uses `Part7_*`; printed Part 9 uses `Part8_*`; printed Part 11
  uses `Pt9Line*`.
- **Yes/No is two independent checkboxes, not one radio group.** Set **only** the
  one you want, to its own on-state. A filed I-907 ticks both Yes and No in two
  separate places.
- **Checkbox export values are not guessable.** Write the value `dump` reports
  under `on=`. The Apt/Ste/Flr radios carry literal spaces: `"/ APT "`. Part 2's
  petition type is `/a`…`/h`; Part 4's is `/1a` / `/1b`.
- **Continuation pages repeat the name at index `[1]`.** I-140 page 8, G-28 page
  4, I-907 page 7. These are the most commonly missed boxes in the whole set.
- **Phone numbers are plain digits** — `4155479999`, not `(415) 547-9999`.
- **Dropdowns need exact `/Opt` matches** — `CA`, not `California`. Note that
  ETA-9089 Appendix A's State box is **plain text**, not a dropdown.
- **Name order is Last, First** — the Checklist opens every form's section with
  it, because a reversed pair has reached a filed G-28.
- **Leave every signature and its date blank** unless the case is at the stage of
  recording an executed date.
- **Never invent firm-sensitive data** — bar number, bank routing/account. Take it
  from `references/fees-and-filing.md` and ask if it isn't there.

Then the ETA-9089, whose traps are different in kind — long field names that
differ only in capitalisation or a `_N` suffix. `references/eta-9089.md` has them
all; the four that bite hardest:

- Appendix A education **block b's country field carries no suffix**, so the `_N`
  on that one field runs one behind every other field in its block.
- Blocks d and e call the associate checkbox **`Associates`**, blocks a–c call it
  `Associate`.
- The three Section C `1b` fields differ **only by capitalisation** and carry no
  suffix at all.
- Section D block b's description field is named **`b`** — a single character.

### The Chinese fields need a second pass — and they are mandatory

The page-3 native-alphabet block (printed items 4.a–4.c and 5.a–5.g) is **required
for a Chinese national**, not an optional extra: the form's own condition is "if the
person's native alphabet is other than Roman letters". Shipping it blank is the
most common way this form goes out incomplete. If you do not have the characters,
that is a Step 2 problem — go back and find them.

`fill` cannot write the Chinese answers this block requires. The
I-140's text fields carry a Helvetica `/DA`, which has no CJK glyphs: pypdf stores
杨 correctly but the appearance stream it generates renders every character as
`?`. Acrobat would regenerate with a substituted font; Preview.app and poppler
will not — so what prints is `?`. Verified by render.

So fill everything else first, then stamp the Chinese:

```bash
$PY scripts/forms.py fill forms/i-140.pdf values-i140.json --out out/step1.pdf
$PY scripts/cjk_stamp.py out/step1.pdf cjk-values.json --out "out/i-140-waiting signature.pdf"
```

`cjk_stamp.py` finds each named field by rect, clears it, and draws the text there
with an **embedded** TrueType (Songti.ttc on this Mac). The embedding is the
point: reportlab's built-in `STSong-Light` CID font is not embedded, so Acrobat
shows it and poppler shows *nothing at all* — an invisible answer, which is worse
than `?` because the read-back looks like an empty box you forgot.

Split the values by script: the Apt/Ste/Flr tick, the unit number and the postal
code in 5.a–5.g are ASCII and go through `fill`; the characters go through the stamp
and must **not** also be passed to `fill`, or `?` is drawn on top of the stamp.

Consequences to report each time: the Chinese is page content, not a form value,
so the field reads empty in Acrobat, **`dump --filled-only` does not show it**, and
it cannot be edited by typing over it. A failed stamp therefore looks exactly like
a box you forgot — **the render is the only read-back that works here**. To change a
Chinese answer, re-run fill + stamp.

Two length traps in the same neighbourhood:

- **Part 4 item 3.a has `MaxLen 34`.** A full romanised street line truncates
  silently. Keep 3.a short and put the whole address in Part 11.
- **Part 11's text boxes are multiline, but pypdf does not wrap.** Put explicit
  `\n` breaks in the value (~40 characters per line) and check the render. The
  same is true of Appendix A's `1l` job-duties box and Appendix C's 1,500-character
  boxes.

### The ETA-9089's one-job problem

**Appendix A holds exactly one work experience.** The intake sheet collects five.
Experience 2 onward goes onto **Appendix C**, two per sheet, with the item number
lettered `E(b)`, `E(c)`, `E(d)`… and the text reproducing Appendix A's own 1–1l
labels inside the box. `references/eta-9089.md` has the template. Add more
Appendix C sheets rather than compressing a job out.

### The G-1650s

One form per payment, never combined:

| # | What | Amount | Naming |
|---|---|---|---|
| 1 | I-140 paper filing fee | $715 | `g-1650-715.pdf` |
| 2 | Asylum Program Fee (self-petitioner rate) | $300 | `g-1650-300.pdf` |
| 3 | I-907 premium processing (E21 NIW) — only if requested | $2,965 | `g-1650-2965.pdf` |

Naming them by amount makes a mismatch obvious at a glance. **Verify all three
against the current G-1055 every time** — the firm's own NIW Checklist still says
$2,805 for premium, which is stale.

**Whether the payment method gets filled forks on the G-28.** With a G-28 the firm
pays and the ACH block is completed in full. **Without a G-28 the G-1650 carries
only the applicant's name and the amount — account type, account holder, business
name, Checking/Savings, bank name, routing and account number are all left blank**
for the client to fill from their own account. The firm is not attorney of record
on those cases, so its account does not belong on a form the client submits.

A no-G-28 G-1650 therefore ships incomplete on purpose. **Say so in the hand-off**:
USCIS cannot pull the money from an empty bank block, so the client has to complete
all three forms before the package can be filed, and an incomplete block otherwise
reads as an omission.

The firm's earlier NIW filings used no G-1650 at all — the client Zelled the fee and
the firm wrote a check. If a case is to be paid by check instead, that is a departure
from the standing instruction: confirm it and note it.

## Step 5 — Read every filled page back with your eyes

```bash
$PY scripts/forms.py render out/i-140.pdf --out render --pages 1-8
$PY scripts/forms.py dump out/i-140.pdf --filled-only
```

Then actually look at the images against the intended values. A clean script run
proves the values were written, not that they were right — this is how you catch a
ZIP code with two digits transposed, a passport issue date sitting in the expiry
box, or text spilling out of a box. `dump --filled-only` is the fast complement:
everything carrying a value shows up, so a field you never meant to touch stands
out.

Check pages 2 and 3 of the I-140 specifically every time — they carry all three
NIW rules, and every one is an invisible failure if it lands wrong. On page 3:

- **items 4.a–4.c and 5.a–5.g must actually show Chinese characters.** Blank is a
  failure, and so is `?`. `dump` cannot tell you — only the render can.
- look at which alphabet is in which block: Chinese characters in 3.a–3.f means the
  two address blocks got swapped.

**Cross-check the three documents that describe the same job**: I-140 Part 6 items
1 and 2, ETA-9089 Appendix A Section E item 1g, and the Final Determination's
items 8–10 must agree on job title and SOC code. They travel in one envelope.

## Step 6 — Extract the pages needing a client signature

Pull the pages needing the **client's own** signature (not the attorney's) into one
PDF for signing. Identify them from each form's own "Signature of..." blocks
rather than a remembered page number — page numbers shift between editions. In a
standard NIW package that is:

- I-140 printed Part 8 (page 6)
- G-28 Part 4 (page 3)
- **ETA-9089 Final Determination page 2, Section B** — the Checklist names this one
  explicitly and it is the one an EB-1A habit would miss
- I-907 Part 3, **only on a no-G-28 case** — with a G-28 the requestor is the
  attorney, so the I-907 adds nothing to the client's packet

**The Checklist's signature standard: clear, handwritten (not electronic), and
dated.** It says this for every form in the set. An e-signature is not acceptable
here.

Name the output so its state is unmistakable — `i-140-waiting signature.pdf`,
`g-28-waiting signature.pdf`. A filled package with blank signature fields is
**not mailable**; say so explicitly when reporting completion rather than letting
"filled" read as "ready to ship".

## Step 7 — Upload back to Drive and log it

Upload the filled PDFs to the case's forms folder with names that say what they
are, then delete the local copies — they contain client PII and the scratchpad is
not where this data should live.

Confirm the filing address before anything gets mailed. For the I-140 it depends
on **where the beneficiary will work** — not the petitioner's address — and on
whether I-907 and/or I-485 travel in the same envelope.
`references/fees-and-filing.md` has the full current table.

The rest of the Checklist's tail is not this skill's job but is worth naming in the
hand-off, because a form package alone is not a filing: index of exhibits,
certificate of translation (check the pronouns and the name; media articles need a
real author, not "editor"), cover page, and the shipping / case-entry follow-up
dates.

If the case folder has an Activity Log, append a dated, attributed entry naming
which forms were filled, at which editions, and what remains outstanding.

---

## Where the knowledge in this skill came from

The field maps, the checkbox export values and the offsets were derived from the
**blank** forms — by `dump` against a render, page by page. Three completed NIW
filings and the firm's NIW Checklist were read once, on 2026-08-24, to learn the
firm's practice and to collect the ways this package has gone wrong before.

**That reading is finished, and it is not repeated per case.** The inputs to a fill
run are the current blank forms plus this case's own 填表指令 doc. Do not open
another client's case folder to see "how it was done last time": the field maps
here are complete, every failure mode found is written up anonymously in
`references/fees-and-filing.md`, and another client's forms are not a reference for
this one — several of them are wrong in ways that would propagate.

If you learn something new about a form — a moved field, a corrected firm value, a
fee change — write it back into the relevant reference file so the next case starts
from it, and keep it about the form rather than about the client it was found on.
