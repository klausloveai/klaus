# EB-1A fees, filing addresses, Drive ids, and precedents

Everything here has a date attached because all of it moves. Re-verify at the top
of each case — a stale fee is a rejected filing, not a cosmetic error.

## Fees — G-1055 Fee Schedule edition 05/29/26, read 2026-08-20

A concurrent EB-1A self-petition with premium processing is **three separate
payments**, so three G-1650s. Without premium, two.

| # | What | Amount | Where the number comes from |
|---|---|---|---|
| 1 | I-140 filing fee, paper | **$715** | G-1055 p.9 (online filing is $665 — not what the firm does) |
| 2 | Asylum Program Fee, **self-petitioner** rate | **$300** | G-1055 p.10: "$600 regular petitioner / $0 nonprofit / **$300 small employer or self-petitioner**" |
| 3 | I-907 premium processing, EB-1 (E11) | **$2,965** | G-1055 p.27, EB-1/EB-2/EB-3 row |

Both stored precedents paid $715 + $300, and Qing Yang additionally $2,965. Those
amounts are current as of the 05/29/26 fee schedule.

Two things to check every time:

- **The $300 is earned by the self-petitioner wording, not by an employee count.**
  If the intake describes an *employer-filed* EB-1A instead, the asylum program fee
  becomes $600, or $300 only if the employer has ≤25 FTE US employees, or $0 for a
  nonprofit — and I-140 page 1 items 5 and 6 must tell the same story as the
  amount paid.
- **Verify live.** Pull the current G-1055
  (`https://www.uscis.gov/sites/default/files/document/forms/g-1055.pdf`; I-140 on
  the page that starts its row, its "Additional Fees" continuation on the next
  page, and the I-907 row) rather than trusting this table. The O-1 work already
  has a case where a stored precedent's premium fee was $160 short.

Premium processing must be paid **separately** from the other fees — that is why it
gets its own G-1650 rather than being folded in.

## Filing addresses — read 2026-08-20 from `uscis.gov/i-140-addresses` (page last reviewed 04/08/2025)

**The lockbox depends on where the *beneficiary will work*** — not on the
petitioner's address, and not on the firm's. This is the opposite habit from I-129
work. It also depends on what travels in the same envelope.

### I-140 by itself

| Beneficiary will work in | Lockbox |
|---|---|
| AL AK AZ AR CA CO FL GA HI ID KY LA MD MS MT NV NM NC OK OR SC TN TX UT VA WA WV WY, Armed Forces, Guam, Marshall Is., N. Mariana Is., Puerto Rico, US Virgin Is. | **Dallas** — USPS: USCIS, Attn: I-140, P.O. Box 660128, Dallas, TX 75266-0128 · Courier: USCIS, Attn: I-140 (Box 660128), 2501 S. State Hwy. 121 Business, Suite 400, Lewisville, TX 75067-8003 |
| CT DE DC IL IN IA KS ME MA MI MN MO NE NH NJ NY ND OH PA RI SD VT WI | **Chicago** — USPS: USCIS, Attn: I-140, P.O. Box 88774, Chicago, IL 60680-1774 · Courier: USCIS, Attn: I-140 (Box 88774), 131 S. Dearborn St., 3rd Floor, Chicago, IL 60603-5517 |

### I-140 + I-907 (premium, no I-485)

| Beneficiary will work in | Lockbox |
|---|---|
| AK AZ AR CA CO GA HI ID LA MT NV NM OK OR TX UT WA WY, Armed Forces, Guam, Marshall Is., N. Mariana Is., US Virgin Is. | **Phoenix** — USPS: USCIS, Attn: Premium I-140, P.O. Box 21500, Phoenix, AZ 85036-1500 · Courier: USCIS, Attn: Premium I-140 (Box 21500), 2108 E. Elliot Rd., Tempe, AZ 85284-1806 |
| AL CT DE DC FL IL IN IA KS KY ME MD MA MI MN MS MO NE NH NJ NY NC ND OH PA RI SC SD TN VT VA WV WI, Puerto Rico | **Elgin** — USPS: USCIS, Attn: Premium I-140, P.O. Box 4008, Carol Stream, IL 60197-4008 · Courier: USCIS, Attn: Premium I-140 (Box 4008), 2500 Westfield Drive, Elgin, IL 60124-7836 |

Qing Yang works in Jersey City NJ and filed with I-907 → **Elgin**.

### The other two combinations

- **I-140 + I-485** (any state): Dallas, `Attn: NFB`, P.O. Box 660867, Dallas, TX
  75266-0867 · Courier: Box 660867, 2501 S. State Highway 121 Business, Suite 400,
  Lewisville, TX 75067-8003.
- **I-140 + I-485 + I-907**: Elgin or Phoenix again, but the **state split differs**
  from the I-140+I-907 table above (AL, FL, KY, MD, MS, NC, SC, TN, VA, WV and
  Puerto Rico move around). Look it up rather than reusing the row above.
- **I-907 alone, to upgrade a pending I-140**: Phoenix `Attn: I-907` P.O. Box 21300
  / Elgin `Attn: I-907` P.O. Box 4200 — again by the beneficiary's work state.

**On a CP case with no settled US job** — the common EB-1A shape, where Part 6 says
`To be determined` — there is no work state to route by. Ask the attorney which
address to use; do not pick one from the client's home address.

## Where the case files live

The 人才移民 shared drive, id `0AIXy3tjXMf-MUk9PVA`. EB1A client folders sit
directly under the **`EB1A`** folder, `1rDPCJzYAiG13SzJjkrTqc9D7eUxU12xR`, at the
drive root. Case folders are named after the client and are built by the
`skye-case-drive` skill, which also owns the standard subfolder layout and the
案件总表 tracking row.

Forms folders are **not** consistently named — the two precedents use `Forms` and
`表格`, while `skye-case-drive` creates `2. Form`. Search the case folder's children
for a forms-ish folder rather than assuming a name.

| What | Id |
|---|---|
| 人才移民 shared drive | `0AIXy3tjXMf-MUk9PVA` |
| `EB1A` (all EB1A client folders) | `1rDPCJzYAiG13SzJjkrTqc9D7eUxU12xR` |
| `0.testing` sandbox | `12TUuLKoQ5d4UK8ehHbn1y3hrY54YbdVW` |
| → `Test EB1A` | `121tOT12uZynNfGtDR6cd379dU2VzrZTm` |
| → → **`2. Form` — the 填表指令 doc lives here** | `1WQuI4s1EcXucb7YI16eF-7iWEnNkW_DB` |
| `Qing Yang` (precedent, no G-28) | `1qguvbw3I1LFqCaygShBQNIFaHLAfMVwz` |
| → `Forms` | `1NaB9wpVdsWK9PEZdQMbb7E0F-iP_3c7Y` |
| → `个人信息 ✅` → `Personal Information_EB1A.docx` | `1Ly7Hgu18KusqZ7t-H2j82uSwFWWfeWlo` |
| `Chujun Yang` (precedent, with G-28) | `1I0gyRq8AHsnWD3oRZRKVaflU7EDE45My` |
| → `表格` | `1lA_IxHKshgSWg1GPsgNROzSGfiz8NPLG` |
| → `个人信息.docx` | `1OKLQpCA72vdNWqhLcwfREApuedoj0rht` |

`Test EB1A` mirrors the standard case layout (`0. Intake`, `0. Shared Folder`,
`1. Initial`, `2. Form`, `3. Petition Letter & Exhibits`, `4. Final Scanned`,
`5. RFE`, `6. Approval Letter`, `7. NVC Letter`, `8. 弃用`) — the same tree
`skye-case-drive` builds for a real EB1A case.

### The intake questionnaire this skill reads from

`Personal Information_EB1A.docx` / `个人信息.docx` is the firm's own bilingual
intake sheet. Section 三 of the 填表指令 doc mirrors its wording on purpose; if the
questionnaire changes, update section 三 to match rather than maintaining a second
vocabulary. Its rows:

Last / First / Middle Name · Date of Birth · Highest Academic Degree · Institution ·
Month and Year Degree Attained · Birthplace (City, Province) · Current Position and
Company · Worksite Address · Annual Income (USD) · Mailing Address in USA ·
Foreign Address (with postal code) · Telephone (USA) · Foreign Telephone · Email ·
then the same name/DOB/country-of-birth block for spouse and for each child under 21.

**What it does not carry, and the I-140 needs**: passport number / country of
issuance / expiry, I-94 number and status, A-Number, SSN, and the birth province
split out of the combined "城市，省份" cell. Degree and institution are for the
petition letter, not the forms.

## Precedents, newest first

Both were read once, on 2026-08-20, to build the field maps. Both are
self-petitions (I-140 Part 5 item 1.b `Self`) and both are on I-140 edition
06/07/24 — the current edition, so field names as well as values transfer.

| Case | Version | Beneficiary location | Premium | Forms in the folder |
|---|---|---|---|---|
| **Qing Yang** | **no G-28** | in the US, F-1, arrival 04/30/2026 | yes | i-140, i-907, g-1650 ×3 (715 / 300 / 2965), the saved I-94 PDF, 签名教程.pdf, `signed & scanned/` |
| **Chujun Yang** | with G-28 | abroad (Foshan, Guangdong) | no | i-140, g-28, g-1145, g-1650 ×2 (715 / 300) |

Between them they cover both G-28 branches, both sides of the last-arrival rule,
and both premium branches. Neither is an employer-filed EB-1A and neither uses
Part 7 page 5, so those two shapes are unmapped by example.

### Known defects in these precedents

Copy their *structure*, not their contents. Confirmed problems:

| Where | Problem |
|---|---|
| Chujun I-140 page 1 | `attyStateBarNumber` = `348749` — a transposition of `348794`. Its own G-28 has the correct number |
| Chujun I-140 page 1 | attorney USCIS Online Account Number left blank although the firm has one (`063938833828`) |
| Chujun I-140 Part 1 item 3.a | In Care Of Name blank while the address is the firm's — a reader cannot tell whose address it is |
| Chujun G-28 item 13 | client's mailing address is the **firm's**, and misspelled `Corssroads` |
| Chujun I-140 Part 6 item 1 | job title `Desigenr` — typo for `Designer` |
| Qing I-140 page 1 item 3.f and page 2 item 2.f | ZIP `07032`; the intake sheet, the I-907 and the same form's own Part 6 worksite all say `07302` |
| Qing I-140 Part 7 (spouse) | items 5 **and** 6 both ticked Yes — the spouse cannot both adjust status and apply for a visa abroad, and Part 4 of the same form says CP |
| Qing I-140 page 2 item 11.a | filled from the I-94 — correct, the beneficiary was in the US |
| Chujun I-140 page 2, whole arrival block | left entirely blank including 11.a. The firm's rule is now `Not in U.S.` in 11.a |
| Qing G-1650 ×3 | account type `/P` Personal, `BusinessName` = `N/A`, and no bank name / routing / account / account-holder name / Checking box |
| Qing I-907 Part 2 item 2 | classification written `EB-1` rather than the `E11` USCIS designates |
| both, printed Part 10 (preparer) | left empty although the firm prepared the petition — worth asking the attorney whether that is deliberate |

## Firm fixed data

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

`8186658535` appears in some older firm artifacts and is **retired** — never copy
it forward. The EB1A precedents agree on `4155479999`.

## Environment notes for this Mac

- pypdf needs `cryptography` — USCIS PDFs are AES-encrypted with an empty
  password, and without it the first page access raises `DependencyError`. A ready
  venv: `~/.local/opt/pdfvenv/bin/python`.
- Reading a USCIS PDF prints `Ignoring padding error: Invalid padding bytes.`
  a few times. Harmless; filter it out of output rather than chasing it.
- `WebFetch` gets HTTP 403 from uscis.gov. `curl -A "Mozilla/5.0"` works, which is
  what `uscis_forms.py fetch` uses. `uscis.gov/i-140-addresses` is a meta-refresh
  redirect — follow it to
  `uscis.gov/forms/all-forms/direct-filing-addresses-for-form-i-140-immigrant-petition-for-alien-worker`.
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
  `uscis_forms.py render` already looks there. Its `-x -y -W -H` flags crop, which
  is the cheap way to eyeball one checkbox instead of a whole page.
- Don't name a helper script `inspect.py` — it shadows the stdlib module pypdf
  imports and produces a confusing circular-import error.
