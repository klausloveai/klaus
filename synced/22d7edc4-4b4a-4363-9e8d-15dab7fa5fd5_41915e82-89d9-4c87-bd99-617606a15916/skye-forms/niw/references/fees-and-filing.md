# NIW fees, filing addresses, Drive ids, and known failure modes

Everything here has a date attached because all of it moves. Re-verify at the top
of each case — a stale fee is a rejected filing, not a cosmetic error.

## Fees — G-1055 Fee Schedule edition 05/29/26, read 2026-08-24

An EB-2 NIW self-petition with premium processing is **three separate payments**,
so three G-1650s. Without premium, two.

| # | What | Amount | Where the number comes from |
|---|---|---|---|
| 1 | I-140 filing fee, paper | **$715** | G-1055 p.9 (online filing is $665 — not what the firm does) |
| 2 | Asylum Program Fee, **self-petitioner** rate | **$300** | G-1055 p.10: "$600 regular petitioner / $0 nonprofit / **$300 small employer or self-petitioner**" |
| 3 | I-907 premium processing, EB-2 (E21 NIW) | **$2,965** | G-1055 p.27 — the row reads "EB-1 (E11, E12, E13), **EB-2 (E21 NIW, E21 non-NIW)**, or EB-3 … Paper Filing: $2,965" |

**The premium fee is the same for NIW as for EB-1** — the fee schedule puts them in
one row. There is no NIW discount.

**The firm's own NIW Checklist says $2,805, and that number is stale.** It was the
premium fee before the current schedule. The Checklist is otherwise the best guide
to this package; this one line is not. Pull the current G-1055 every time
(`https://www.uscis.gov/sites/default/files/document/forms/g-1055.pdf`) rather
than trusting either the Checklist or this table.

Two more things to check every time:

- **The $300 is earned by the self-petitioner wording, not by an employee count.**
  If a case is somehow *employer-filed*, the asylum program fee becomes $600, or
  $300 for an employer with ≤25 FTE US employees, or $0 for a nonprofit — and
  I-140 page 1 items 5 and 6 must tell the same story as the amount paid.
- Premium processing must be paid **separately** from the other fees. That is why
  it gets its own G-1650 rather than being folded in.

**The Checklist's client-facing fee message**, for reference — it is what the firm
tells the client, and it is where the 加急 decision actually gets made:

> 1（必须）$715 基础申请费 + $300 难民费 · 2（可选）加急费 · 3（可选）$80 邮局加急快递费（加急 1-2 天，不加急 3-5 天）

## Filing addresses — read 2026-08-24 from `uscis.gov/i-140-addresses` (page last reviewed 04/08/2025)

**The lockbox depends on where the *beneficiary will work*** — not on the
petitioner's address, and not on the firm's. It also depends on what travels in
the same envelope. Nothing about this is NIW-specific: the I-140 address tables
do not split by classification.

### I-140 by itself

| Beneficiary will work in | Lockbox |
|---|---|
| AL AK AZ AR CA CO FL GA HI ID KY LA MD MS MT NV NM NC OK OR SC TN TX UT VA WA WV WY, Armed Forces, Guam, Marshall Is., N. Mariana Is., Puerto Rico, US Virgin Is. | **Dallas** — USPS: USCIS, Attn: I-140, P.O. Box 660128, Dallas, TX 75266-0128 · Courier: USCIS, Attn: I-140 (Box 660128), 2501 S. State Hwy. 121 Business, Suite 400, Lewisville, TX 75067-8003 |
| CT DE DC IL IN IA KS ME MA MI MN MO NE NH NJ NY ND OH PA RI SD VT WI | **Chicago** — USPS: USCIS, Attn: I-140, P.O. Box 88774, Chicago, IL 60680-1774 · Courier: USCIS, Attn: I-140 (Box 88774), 131 S. Dearborn St., 3rd Floor, Chicago, IL 60603-5517 |

### I-140 + I-907 (premium, no I-485) — the common NIW shape

| Beneficiary will work in | Lockbox |
|---|---|
| AK AZ AR CA CO GA HI ID LA MT NV NM OK OR TX UT WA WY, Armed Forces, Guam, Marshall Is., N. Mariana Is., US Virgin Is. | **Phoenix** — USPS: USCIS, Attn: Premium I-140, P.O. Box 21500, Phoenix, AZ 85036-1500 · Courier: USCIS, Attn: Premium I-140 (Box 21500), 2108 E. Elliot Rd., Tempe, AZ 85284-1806 |
| AL CT DE DC FL IL IN IA KS KY ME MD MA MI MN MS MO NE NH NJ NY NC ND OH PA RI SC SD TN VT VA WV WI, Puerto Rico | **Elgin** — USPS: USCIS, Attn: Premium I-140, P.O. Box 4008, Carol Stream, IL 60197-4008 · Courier: USCIS, Attn: Premium I-140 (Box 4008), 2500 Westfield Drive, Elgin, IL 60124-7836 |

### The other two combinations

- **I-140 + I-485** (any state): Dallas, `Attn: NFB`, P.O. Box 660867, Dallas, TX
  75266-0867 · Courier: Box 660867, 2501 S. State Highway 121 Business, Suite 400,
  Lewisville, TX 75067-8003.
- **I-140 + I-485 + I-907**: Elgin or Phoenix again, but the **state split differs**
  from the I-140+I-907 table above. Look it up rather than reusing the row above.
- **I-907 alone, to upgrade a pending I-140**: Phoenix `Attn: I-907` P.O. Box 21300
  / Elgin `Attn: I-907` P.O. Box 4200 — again by the beneficiary's work state.

**On a case with no settled US job** there is no work state to route by. Ask the
attorney which address to use; do not pick one from the client's home address.

## Where the case files live

The 人才移民 shared drive, id `0AIXy3tjXMf-MUk9PVA`. NIW client folders sit
directly under the **`NIW`** folder, `1D7hKuq2qi4daqIegvjM3YUiN3WKsawjy`, at the
drive root. Find this case's folder by the client name in the request.

| What | Id |
|---|---|
| 人才移民 shared drive | `0AIXy3tjXMf-MUk9PVA` |
| `NIW` (all NIW client folders) | `1D7hKuq2qi4daqIegvjM3YUiN3WKsawjy` |
| `0.testing` sandbox | `12TUuLKoQ5d4UK8ehHbn1y3hrY54YbdVW` |
| → `Test NIW` | `1OBxlBcVnKq4m80ZInc-0J3z9lwgi0sOM` |
| → → **`2. Form` — the 填表指令 doc lives here** | `1-ugvpZGYxWp_zQoOujMQHb6M-i1AOPaP` |

`Test NIW` mirrors the standard case layout (`0. Intake`, `0. Shared Folder`,
`1. Initial`, `2. Form`, `3. Petition Letter & Exhibits`, `4. Final Scanned`,
`5. RFE`, `6. Approval Letter`, `7. NVC Letter`, `8. 弃用`) — the same tree
`skye-case-drive` builds for a real NIW case.

**Forms subfolders are not consistently named** across older cases (`02.表格`,
`Forms`, or a case folder that *is* the forms folder), while `skye-case-drive`
creates `2. Form`. List the case folder's children and pick by content rather than
by expected name.

**Only ever open the folder of the client you are filling for.** The field maps in
this skill are complete; there is no reason to read another client's forms, and
their contents are not a reference for this case.

### The firm's own NIW Checklist

The firm has a two-page NIW Checklist — a paper form the reviewer fills in by hand
— and it is the closest thing to a written NIW procedure the firm has. Its twelve
steps: fee payment from client → cover page → G-28 → I-907 → G-1145 (no-premium
only) → I-140 with five named field checks → the three 9089 pieces →
passport/visa/I-94 → index of exhibits → certificate of translation → Drive upload
→ shipping and case-entry follow-up.

Everything in this skill marked "the Checklist says" comes from that document, and
what it says has been carried into these reference files, so a fill run does not
need to go and find a copy. Two of its items are out of date: the $2,805 premium
fee, and its `Form Link` hyperlinks, which point at whatever edition was current
when it was written.

### The intake questionnaire this skill reads from

`1. Personal Information.docx` is the firm's bilingual NIW intake sheet. It is
**richer than the EB-1A one**: as well as the applicant block it carries **five
Work Experience blocks** (company name, worksite address, job title, start/end
mm/yyyy, hours per week, job duties in 3–5 sentences), which is exactly what
ETA-9089 Appendix A Section E and the Appendix C continuation sheets need.

Its rows: Last / First / Middle Name · Date of Birth · Highest Academic Degree ·
Name of Institution that issued the degree · Month and Year Degree Attained ·
入学时间 · Birthplace (City, Province) · Current Position and Company · Worksite
Address · Annual Income (USD) · Mailing Address in USA · Foreign Address (with
postal code) · Telephone (USA) · Foreign Telephone · Email · the spouse and
children blocks · then Work Experience 1–5.

Its second half is a document checklist and a criteria guide for the petition
letter — passport scans, relationship documents, degree certificates and
transcripts, professional licences, current US status document, I-94, SSN, CV.
**Section 三 of the 填表指令 doc mirrors this sheet's wording on purpose**; if the
questionnaire changes, update section 三 rather than maintaining a second
vocabulary.

**What it does not carry, and the forms need**: passport number / country of
issuance / expiry, I-94 number and class of admission, A-Number, SSN, the birth
province split out of the combined "城市，省份" cell, the SOC code, and the degree
level / major / institution / country / mm-yyyy for **each** degree rather than
only the highest.

Two traps in how it answers its own questions:

- **"Worksite Address" is sometimes answered with the employer's offices**
  ("hybrid, the company has offices in two cities"). That is not a worksite. A
  remote or hybrid worker's worksite is their own address, and getting this wrong
  routes the package to the wrong lockbox.
- **Annual income on the sheet and the figure on a previous draft form have
  disagreed.** Take the number from a pay document, not from another box.

## Known failure modes on already-filed NIW packages

Three completed NIW filings were read once, on 2026-08-24, to build the field maps
in this skill and to learn the firm's practice. **That reading is done. Do not open
them again** — the current blank forms plus this case's own 填表指令 doc are the
inputs to a fill run, and another client's data is not a reference.

What those filings taught, as a checklist of things that have actually gone wrong
and silently shipped. Every one of these is a box the script will happily leave
however you left it:

**I-140 page 2**

- Part 4 item 1 left **entirely blank** — no CP box, no consulate city, no country.
- `/1a` ticked with **1.b City and 1.c Country empty** — a consular box naming no
  consulate.
- Items 11.b and 11.c blank, and **item 12 passport number blank**, on a client who
  was in the US.
- Item 10 Date of Last Arrival blank while 11.a–11.c were filled.
- The whole last-arrival block filled from a **B-2 admission that had already
  expired**, for a client who was living abroad at the time of filing. The right
  answer there is `Not in U.S.` in 11.a and nothing else.

**I-140 page 3**

- The Chinese address block half-written — street and postal code in, city,
  province and country left empty.
- Item 2.b country of residence blank.

**I-140 pages 4–8**

- Annual income (Part 5 item 12) and wages (Part 6 item 8) agreeing with each other
  but not with the intake sheet.
- A ticked No in a Part 7 person-2 block that had **no name in it** — an answer
  about a dependent who does not exist.
- Printed Part 11 (page 8) left entirely empty, **including the name / A-Number
  header**, on every one of the three.
- Printed Part 10 (preparer) empty although the firm prepared the petition — ask
  the attorney whether that is deliberate.

**G-28**

- The client's name **reversed** — family name and given name swapped — while the
  I-140 in the same package had it right.
- Part 2 items 1.a licensing authority, 1.b bar number and 1.d firm name all blank.
- The page-4 continuation name repeat left blank.
- Stale firm letterhead: a superseded firm name, a superseded San Marino address,
  and a retired phone number.
- All five members of `Line4_Checkbox` set to `/P` instead of just `[3]`.

**I-907**

- Item 6 ticked **both Yes and No**, with a physical address one street number away
  from its own mailing address.
- Part 3 item 1 also ticked both `/Y` and `/N`.
- A retired phone number and a personal mailbox in Part 3 instead of the firm's
  confirmed contact block.

**I-140 page 1, both G-28 cases**

- `attyUSCISOnlineNum` blank although the firm has one (`063938833828`).

**ETA-9089 Appendix A**

- A lower education block inheriting the **higher block's institution name and
  month/year** while carrying its own country — describing a degree that does not
  exist.

**Payments**

- No G-1650 and no G-1145 anywhere, because all three used premium and paid by
  check. There is therefore **no worked G-1650 or G-1145 example** in the firm's
  NIW history to copy from; build them from `g28-i907-g1650-g1145.md`.

## Firm fixed data

Confirmed with the firm on **2026-08-24**. Older filed NIW forms disagree with this
table; the table wins.

| Item | Value |
|---|---|
| Attorney | Shenqi Cai (Family Name `Cai`, Given Name `Shenqi`) |
| Firm | Law Office of Shenqi Cai APC |
| Address | 13191 Crossroads Parkway N, Ste 295, City of Industry, CA 91746, USA |
| Phone | 4155479999 — digits only, used for both Daytime and Mobile |
| Fax | 6262402046 |
| Firm email | cassie@lingtulaw.com |
| Bar / authority | 348794 / the State Bar of California |
| Attorney USCIS Online Account Number | 063938833828 |
| ACH | Business · Checking · Bank of America · Routing 121000358 · Account 325210063004 (holder Shenqi Cai, Business Name `Law Office of Shenqi Cai APC`) |

**Retired values that appear on older NIW forms and must never be copied
forward**: the firm's former name and its former San Marino address, the phone
numbers `8186658535` and `7147171893`, and any `@lashinelaw.com` mailbox. If a
value you are about to write came off a previous form rather than out of this
table, stop and check it here.

`7147171893` is also the Zelle number the Checklist gives clients for the fee.
Since the firm's instruction is now to pay by **G-1650 ACH**, that line does not
apply to new cases — and it is not a form value either way.

## Environment notes for this Mac

- pypdf needs `cryptography` — USCIS PDFs are AES-encrypted with an empty
  password, and without it the first page access raises `DependencyError`. A ready
  venv: `~/.local/opt/pdfvenv/bin/python`.
- Reading a USCIS PDF prints `Ignoring padding error: Invalid padding bytes.`
  a few times. Harmless; filter it out of output rather than chasing it.
- **`WebFetch` gets HTTP 403 from uscis.gov**; `curl -A "Mozilla/5.0"` works, which
  is what `forms.py fetch` uses.
- **dol.gov is harder.** Its edge (Akamai) refuses `urllib` outright even with a
  full browser header set — the block keys off the TLS/HTTP fingerprint, not the
  headers — so `forms.py` shells out to `curl` for the three ETA-9089 files, with
  Referer and the `Sec-Fetch-*` trio. A blocked request comes back as an
  `Access Denied` **HTML body under a .pdf filename**, which then fails as a
  confusing pypdf parse error; `fetch` checks the `%PDF` magic for exactly that.
- **dol.gov's own HTML pages 403 even through curl**, so nothing here can scrape
  the DOL forms page to confirm the current ETA-9089 edition. `fetch` says so and
  asks for a human to open
  `https://www.dol.gov/agencies/eta/foreign-labor/forms` and look. Do not skip it —
  Appendix A's field names changed at the last edition boundary.
- `gws` lives in `~/.local/bin`; `export PATH="$HOME/.local/bin:$PATH"` first.
- `gws drive files get` takes `--params '{"fileId": "..."}'`, not `--file-id`, and
  `-o` only accepts a path **inside the current directory** — cd into the
  scratchpad first and pass a bare filename. Add `"alt":"media"` to download bytes.
- Every `gws drive files list` needs `supportsAllDrives`,
  `includeItemsFromAllDrives` and `corpora: allDrives`, or a shared-drive folder
  comes back as an empty list rather than an error.
- **zsh does not word-split unquoted parameters.** `set -- $pair` inside a loop
  silently gives you nothing; use `while read a b` or an array.
- `pdftoppm` is not on PATH but exists at
  `~/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/pdftoppm`;
  `forms.py render` already looks there. Its `-x -y -W -H` flags crop, which is the
  cheap way to eyeball one comb field instead of a whole page.
- Don't name a helper script `inspect.py` — it shadows the stdlib module pypdf
  imports and produces a confusing circular-import error.
- **Delete downloaded client PDFs from the scratchpad when the run is done.** They
  carry passport and I-94 numbers.
