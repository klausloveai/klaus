# O-1 fees, filing addresses, Drive ids, and precedents

Everything here has a date attached because all of it moves. Re-verify at the
top of each case — a stale fee is a rejected filing, not a cosmetic error.

## Fees — G-1055 Fee Schedule edition 05/29/26, read 2026-08-20

A concurrent O-1 filing with premium processing is **three separate payments**,
so three G-1650s:

| # | What | Regular petitioner | Small employer (≤25 FTE) | Nonprofit |
|---|---|---|---|---|
| 1 | I-129, O petition (paper) | $1,055 | **$530** | $530 |
| 2 | Asylum Program Fee | $600 | **$300** | $0 |
| 3 | I-907 premium processing, O classification | $2,965 | $2,965 | $2,965 |

Premium processing is $2,965 regardless of employer size, and it must be paid
separately from the other fees — that is the reason it gets its own G-1650
rather than being folded in.

Two things to check every time:

- **The employer-size answer has to be consistent.** I-129 Part 5 item 15
  ("25 or fewer full-time equivalent US employees?") is the declaration that
  earns the reduced $530 + $300. If that box says No, the amounts must be
  $1,055 + $600. Reconcile the checkbox and the two G-1650s against I-129 Part 5
  item 14 (employee count) before assembling.
- **Verify the amounts live.** Pull the current G-1055
  (`https://www.uscis.gov/sites/default/files/document/forms/g-1055.pdf`,
  Appendix A for I-129, the I-907 row for premium processing) rather than
  trusting this table. Both stored precedents paid **$2,805** for premium
  processing, which was correct when they were filed in January 2026 and is
  $160 short today. That is exactly how this fails.

## Filing address — read 2026-08-20 from `uscis.gov/i-129-addresses`

The lockbox depends on the **petitioner's primary office state** and on whether
I-907 goes in the same envelope. For a California petitioner filing I-129 for
O-1A/O-1B **together with I-907**:

> USCIS Dallas Lockbox
> USPS: USCIS, Attn: Premium I-129 O, P.O. Box 660090, Dallas, TX 75265-0090
> FedEx/UPS/DHL: USCIS, Attn: Premium I-129 O (Box 660090), 2501 S. State Highway 121 Business, Suite 400, Lewisville, TX 75067-8003

Non-premium O petitions go to a **different box number** at the same lockbox
(`Attn: I-129 O`), and the state-to-lockbox split differs slightly between the
premium and non-premium tables — Iowa, Kansas, Tennessee and West Virginia move
between them. Look the case up on the page; do not derive it from this note.

`uscis.gov/i-907` confirms that when premium processing is requested for an
I-129, the I-907 goes to whatever address the I-129 page gives — there is no
separate I-907 address for this case type.

## Where the case files live

The 人才移民 shared drive, id `0AIXy3tjXMf-MUk9PVA`; O-1 client folders sit under
`1-g_HDMHwSi7PtV5Nlyw1nUCwXGbQkwpS`. Case folders are named `客户姓名 + 案件类型`
(e.g. `Xiran Liu O1B`, `Ziqing Shi`) and are built by the `skye-case-drive` skill,
which also owns the standard subfolder layout and the 案件总表 tracking row.

Forms folders are **not** consistently named — the two precedents use `Forms` and
`表格`, and `skye-case-drive` creates `2. Form`. Search the case folder's children
for a forms-ish folder rather than assuming a name.

## Drive ids — 人才移民 shared drive `0AIXy3tjXMf-MUk9PVA`

| What | Id |
|---|---|
| O-1 client folders | `1-g_HDMHwSi7PtV5Nlyw1nUCwXGbQkwpS` |
| `0 Sample （O1）` | `1u6SW71oWNmuJlVAAebi7NHzwz8J7U2cT` |
| → `1. Information Collection Sheet` | `1OCB_vjhx-TypWB8mRwn43tSD46D2o55K` |
| → → `a. Chinese`（个人信息.docx / 担保人信息.docx / 信息采集表.xlsx） | `10B1UPsd53x-vaB3f9HAuljkNUL2-pcRy` |
| → `3.Forms / Offer / Itinerary` | `1sooJKRk-zKJMLZ6pvGtqAS25PcD6lmzQ` |
| → → **填表指令 master doc** | `1prc4Qu-mex2vFzDybUI3m4GVZIrt7ep_vydY7eMQwFA` |
| → → `a. Direct Employment`（公司担保 samples） | `1i01m4vE6ET3Kjl06mzuy7YP43kzt_580` |
| → → `b. Agent-Based`（个人担保 samples） | `1X4Og499aBINWRdlxWjgNBqD5gsfoD0QC` |
| → → `c. G-1145 w/, w/out G-28` | `1IrVzqWhdLchrrw1VngErxEFSiGyQ7Kht` |
| → → `d. G-1650 with G28` | `1ck1S88v6yEfz38OjZ7JYURUvK-VLTLFc` |
| → `5. Signature Guidance and Page` | `1wCAq51El3eQUe40JgJjqWfyPA7bp6FOw` |
| → `2. Cover/PL/Index`（PL template, owned by skye-case-drive） | `1KlSs38B0r4XWDSIJRw5m7puEZXttb4Qi` |
| `0.testing` sandbox (drive root) | `12TUuLKoQ5d4UK8ehHbn1y3hrY54YbdVW` |
| → `Test O1B` → `2. Form` | `1FiiQaAXjyj40TNObRHGaATICqEAM_mtM` |
| → → **填表指令 template copy** | `18kd7cdGMaMA029Z2zEUAyx2JqqHi4TX3L8b8SaWIjR8` |
| `YUQIAN TAO_O1A` → `13_表格 Forms (I-129)` | `1MwH8JQaJ7xrtUpxsGDrThlviMvXssksR` |

The firm's own with/without-G-28 and company/individual-sponsor distinctions are
already expressed in this folder tree — `a.`/`b.` for sponsorship shape and `c.`
for the G-1145 variants. Follow that vocabulary rather than inventing new labels.

The 信息采集表 / 个人信息 / 担保人信息 files are the firm's existing intake
questionnaires. §2 of the 填表指令 doc mirrors their wording on purpose; if those
questionnaires change, update §2 to match instead of maintaining a second
vocabulary.

Note the firm's own **G-28 master sample** (in `a. Direct Employment`, dated
11/26/2025, placeholder client "Zhang San") carries two things that are now
stale: the retired phone `8186658535`, and a **blank Part 2 item 1.b bar
number**. The August 2026 filing fills the bar number correctly, so that
omission has been fixed in practice — but anyone starting from the old sample
will inherit both. Check those two cells whenever a G-28 comes from an old file.

Keep the two template copies in sync: the sample-library master and the
`Test O1B` copy are byte-identical today, and both should be updated together
(re-upload the same markdown to each) so neither becomes the stale one.

## Precedents, newest first

| Case | Class | Version | I-129 edition | Value as a reference |
|---|---|---|---|---|
| **YUQIAN TAO_O1A** (2026-08-12) | O-1A | with G-28, company sponsor | **02/27/26 — current** | **Primary.** Same edition as the blank you will fetch, so field names as well as values transfer. Covers the non-small-employer branch (33 employees), change-of-status (Part 2 item 4 = `/B`), a filled Part 6, and O supp item 8 = No with the explanation routed to Part 9 |
| Ziqing Shi (2026-01-27) | O-1B | with G-28, individual agent | 01/20/25 — superseded | Values only |
| Xiran Liu O1B (2026-01) | O-1B | **no G-28**, self-petition via own LLC | 01/20/25 — superseded | The only no-G-28 sample |

Folder ids: `YUQIAN TAO_O1A` → `13_表格 Forms (I-129)`
`1MwH8JQaJ7xrtUpxsGDrThlviMvXssksR` (i-129 / g-28 / i-907, all "waiting
signature"; no G-1650 in that folder).

## The two older learning precedents

Both are O-1B, both on I-129 edition 01/20/25, both signed 01/27/2026.

**Xiran Liu O1B** — `Forms` folder `10xq4IVcC229Xx1SHQPUKKZN0ysZcZMbW`
Self-petition through the beneficiary's own company (Chingsam LLC, EIN
990665791, Pasadena CA). No G-28 in the folder. I-907 Part 1 item 8 = `/A`
("I am the petitioner"), correct for these facts. O supplement item 7.a = Yes
with "The beneficiary owns the petitioning company." in 7.b. Three G-1650s at
$530 / $300 / $2,805.

**Ziqing Shi** — `表格` folder `18cNt9sqHarky4XCSNN6rnEsX6UFC_2-C`
Attorney-filed with G-28. Petitioner is an individual, Phyllis Tam (Arcadia CA),
acting as agent — I-129 Part 5 item 12 Type of Business = `Agent`. Beneficiary
Ziqing Shi, job title Producer, Motion Picture Production. O supplement item
7.a = No. G-1650s named by amount (`g-1650-530.pdf` etc.), a useful convention.

### Known defects in these precedents

Copy their *structure*, not their contents. Confirmed problems:

| Where | Problem |
|---|---|
| Ziqing G-28 Part 2 item 1.b | bar number left blank |
| Ziqing I-129 Part 5 item 9 | `Line8_Per` contains a bare `p`, and no wage amount |
| Xiran I-907 Part 2 item 2 | classification (`O-1B`) left blank |
| Xiran G-1650 ×2 | bank routing/account/name, business name and the Checking box all missing |
| both, G-1650 #3 | $2,805 premium processing fee, now $2,965 |
| both, I-129 Part 8 | preparer block left empty although the firm prepared the petition — worth asking the attorney whether that is deliberate |
| both | O-1B, so I-129 Part 6 (controlled technology) is blank and teaches nothing about the O-1A requirement |

## Firm fixed data

**Firm phone on O-1 forms is `4155479999`.** An earlier reading of this concluded
`8186658535`, based on the January 2026 filings and the `0 Sample` G-28 master —
the August 2026 filing overturns that:

| Source | Phone |
|---|---|
| `case` skill (I-131 etc.) | 4155479999 |
| Firm letterhead on `个人信息.docx` | (415) 547-9999 |
| `0 Sample` G-28 master sample (dated 11/26/2025) | 8186658535 |
| Ziqing Shi + Xiran Liu filings (Jan 2026) | 8186658535 |
| **YUQIAN TAO_O1A filing (Aug 2026, current editions)** | **4155479999** |

The newest filing agrees with the letterhead and with the firm's other case
types, and 818 appears only in artifacts from the same few months. Treat 818 as
retired and 415 as current — and be careful copying firm data forward out of the
January 2026 cases, which carry the old number.

Unchanged and consistent across both skills:

| Item | Value |
|---|---|
| Attorney | Shenqi Cai |
| Firm | Law Office of Shenqi Cai APC |
| Address | 13191 Crossroads Parkway N, Ste 295, City of Industry, CA 91746, USA |
| Fax | 6262402046 |
| Bar / authority | 348794 / the State Bar of California |
| ACH | Business · Checking · Bank of America · Routing 121000358 · Account 325210063004 |

## Environment notes for this Mac

- pypdf needs `cryptography` — USCIS PDFs are AES-encrypted with an empty
  password, and without it the first page access raises `DependencyError`. A
  ready venv: `~/.local/opt/pdfvenv/bin/python`.
- `WebFetch` gets HTTP 403 from uscis.gov. `curl -A "Mozilla/5.0"` works fine,
  which is what `uscis_forms.py fetch` uses.
- `gws` lives in `~/.local/bin`; `export PATH="$HOME/.local/bin:$PATH"` first.
- `gws drive files get` takes `--params '{"fileId": "..."}'`, not `--file-id`,
  and `-o` only accepts a path **inside the current directory** — cd into the
  scratchpad first and pass a bare filename.
- Every `gws drive files list` needs `supportsAllDrives`,
  `includeItemsFromAllDrives` and `corpora: allDrives`, or a shared-drive folder
  comes back as an empty list rather than an error.
- `pdftoppm` is not on PATH but exists at
  `~/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/pdftoppm`;
  `uscis_forms.py render` already looks there.
- Don't name a helper script `inspect.py` — it shadows the stdlib module pypdf
  imports and produces a confusing circular-import error.
