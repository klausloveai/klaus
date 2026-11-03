---
name: "case"
description: "Prepare a USCIS filing package for a Lingtu Law / SIA 高徒 client whose case folder already exists in Google Drive (built via the \"it\" skill). Universal across case/form types — required forms, attachment order, and fixed/flexible data are learned per-case from that case's \"1. Initial\" and \"3. Draft\" folders instead of being hardcoded. Covers organizing intake materials, determining which forms a case needs, downloading and verifying current USCIS forms, filling them with the firm's fixed data plus the client's flexible case data, extracting client-signature pages, completing the cover letter, assembling the final package, and purchasing/printing the shipping label. Use whenever asked to prepare, fill, or complete a USCIS filing/case package (I-131, I-485, I-765, I-130, etc.), fill forms for an immigration case, organize a client's materials, or print a shipping label for a USCIS filing — even mentioning just one form or step, since this covers the whole package end to end for any case type."
---

# USCIS Filing Package Preparation (Lingtu Law / SIA 高徒)

This skill is **universal across case types** (I-131, I-485, I-765, I-130, etc.) — it
does not assume any particular form package. What forms this specific case needs,
what order they get assembled in, and what data goes where is learned per-case from
that case's own `1. Initial` and `3. Draft` folders, not hardcoded here.

This skill assumes the client's case folder already exists in Google Drive with the
standard 9-subfolder structure (see the `it` skill) — `0. Intake`, `0. Shared Folder`,
`1. Initial`, `2. Form`, `3. Draft`, `4. Final`, `5. Scanned`, `6. I-797`, `7. Deleted`.
Use `gws` (CLI) for all Drive/Docs operations, never the web UI.

## Step 0 — Learn this case's required forms from Initial and Draft

Before doing anything else, read the case's own `1. Initial` and `3. Draft` folders
to determine what this specific case actually needs — don't assume it's a reentry
permit or any other specific package.

- `1. Initial` should contain (or, per Step 1, will come to contain) a
  Fixed/Flexible master template doc for this case type — e.g.
  `I-131 材料信息模板 (Fixed 律所固定信息 + Flexible 客户信息)` for a reentry
  permit case, but the equivalent doc for whatever case type this is. Its title
  and section headers name the case type and the forms it covers. If this case's
  `1. Initial` doesn't have its own copy yet, find the matching master in
  `0. Template` (matched by case type, same lookup the `it` skill already did
  when the folder was created) and copy it in before proceeding.
- `3. Draft` should contain a cover-letter draft. Once it's filled in (Step 5),
  its "We have attached the following supporting documents..." list is the
  authoritative list of forms/attachments and their order for this case — read
  it rather than guessing from the case type alone.
- Cross-check the two: the template doc tells you which forms/fields exist and
  what data each needs; the cover letter tells you the attachment order. If
  they disagree about which forms are included, the cover letter wins for
  what actually gets mailed, but flag the discrepancy rather than silently
  picking one.
- If neither folder has enough to determine the form list (e.g. a brand-new
  case with no template copied yet and no cover letter drafted), ask the user
  which forms this case requires rather than guessing.

Everything below refers to "the case's forms" — substitute whatever set Step 0
identified (could be one form, could be four, could be a set this skill has
never handled before).

## Step 1 — Read and organize intake materials

The matching template in `1. Initial` (per Step 0) is the universal source of
truth for this case — it lists every firm-fixed value and every client-flexible
field the case's forms need, organized by section. Fill in its Flexible section
for this client as you work through the rest of Step 1. This doc — not any
field-map reference — is what should evolve as the firm's standing data or the
client's facts change; a field map (Step 3) stays about *where on the page*
each field lives, not *what value* goes there.

Read **every** file in `0. Intake` and `0. Shared Folder` — docx, images, PDFs,
whatever type, not just ID photos — using the Drive connector's
`read_file_content` tool. It does server-side text extraction and OCR (for images)
without ever pulling bytes to local disk, which matters here: these files carry
real client PII (passport, green card, SSN), so avoid touching local disk for
anything that's just a read.

- Give each file a clear descriptive name and classify it; **copy** (not move)
  into `1. Initial` with the clean names. Originals stay in `0. Shared Folder`.
- Fill in the case's copy of the Fixed/Flexible template doc with everything
  extracted: legal name, A-number, DOB, SSN, green card number/category/dates,
  passport number/dates, addresses, phone/email, travel plan, urgency notes,
  case timeline (adjust to whatever fields this case type's template actually
  asks for). This is the single source of truth you'll pull values from in
  Step 3 — no need for a separate `材料信息摘要` doc once this template exists.
- If the case-root `Activity Log` is a raw `.docx` rather than a native Google
  Doc, the Docs API can't append to it. Convert it via Drive's native
  copy-with-mimeType-change (`gws drive files copy` with json body
  `{"mimeType": "application/vnd.google-apps.document", ...}`) — this preserves
  content with no local download — then trash (not permanently delete) the old
  `.docx`. From then on, append dated + attributed entries with `gws docs +write`.

## Step 2 — Always get fresh forms straight from USCIS.gov

**Never fill the PDF sitting in the case's `2. Form` folder.** A firm-stored copy
can have a silently broken AcroForm — a real example had 339 of 342 form fields
orphaned from the field tree (pypdf's `get_fields()` found only 7, despite 342
widgets existing on the pages), which forces an unreliable manual
text-overlay workaround with alignment bugs. Instead, for **each** form Step 0
identified:

1. Download the current PDF directly from USCIS.gov into a local scratchpad
   (this is the one place local disk is justified — see Step 3). USCIS forms
   follow the pattern `https://www.uscis.gov/sites/default/files/document/forms/{form-number}.pdf`
   (e.g. `i-131.pdf`, `g-28.pdf`, `i-485.pdf`) — confirm the exact filename on
   the form's own USCIS.gov page (e.g. `uscis.gov/i-131`) if unsure.
2. Verify the download has an intact AcroForm before trusting it: with pypdf,
   `PdfReader(path).get_fields()` count should be close to the total widget
   count summed across every page's `page.get("/Annots")`. If `get_fields()`
   returns drastically fewer than the widget total, the form is broken —
   re-download and re-check rather than working around it.
3. Open that form's own USCIS.gov page and expand the **"Edition Date"**
   accordion panel. This is the authority on whether the PDF's printed
   "Expires" date is stale-but-still-valid (USCIS often keeps an edition valid
   well past its printed expiration while a new one is pending) or truly
   superseded — don't assume either way from the footer date alone. If using
   the Browser tool, `navigate` to uscis.gov can be blocked by policy in some
   environments; use `preview_start` with the URL instead, then
   `get_page_text` / `read_page` + `computer` click to expand the accordion.

## Step 3 — Fill with real AcroForm field values, using a documented field map

Local processing (download blank template → fill → upload the result to Drive →
delete the local copy) is the only viable approach here, since Drive/Docs APIs
have no native way to set PDF form field values. Keep it scoped to blank
templates only (no client PII in the template itself), and delete local copies
right after the filled PDF is uploaded back to Drive.

**Reuse a known field map when this case's form matches one already built;
build and save a new one otherwise.** The **Known field maps** appendix at the
end of this skill currently covers I-131 (14pp), G-28 (4pp), G-1145 (1pp), and
G-1650 (1pp) — read the relevant entry before filling any of those. For any
other form this case needs that isn't in the appendix yet: walk each page's
`/Annots`, resolve each widget's `/Parent` chain to build the dotted field name
(e.g. `form1[0].P5[0].Part2_Line3_State[0]`), and note its page, type
(`Tx`/`Btn`/`Ch`), and rect. Mark each entry **FIXED** (the firm's own standing
data — reuse identically every case) or **FLEXIBLE** (pull from that case's
copy of the Fixed/Flexible template doc from Step 1). Once built, this map
holds until USCIS republishes that form with a new edition date — save it back
into this skill (ask the user, then use the skill-saving mechanism) so the next
case with the same form is a fast lookup instead of a re-derivation.

Fill with `PdfWriter.update_page_form_field_values(page, values_dict,
auto_regenerate=False)` per page — this renders through each field's own
native appearance stream, which correctly centers text in narrow boxes (single
digit weight boxes, comb-style SSN fields, etc.) automatically. Don't hand-roll
a reportlab text overlay unless the AcroForm is unrecoverably broken even after
a fresh download (should essentially never happen if Step 2 was followed).

Traps to watch for, all confirmed by hand on real forms (apply the same
suspicion to any new form, not just the ones below):
- **Checkbox/radio groups**: don't infer the right option from its internal
  state code (`/A` vs `/P` vs `/BD`) — pull each option's rect and match
  against the visible label layout (left-to-right, top-to-bottom).
- **Field names can be mislabeled relative to their visual position.**
  G-28's `Line6_EMail` and `Line7_MobileTelephoneNumber` fields are swapped —
  the one named `EMail` sits at the visual Mobile Phone box and vice versa.
  Confirm via rect, never trust the name string alone. Check for this on every
  new form, not just G-28.
- **Choice/dropdown fields** need an exact match against the field's `/Opt`
  list (check `reader.get_fields()[key].get("/Opt")`) — e.g. state must be
  `"CA"`, not `"California"`.
- **Comb/fixed-length fields** (e.g. SSN) want plain digits with no
  separators and will truncate or warn if given the wrong format.
- **Phone numbers should always be plain digits, no parentheses or dashes**
  (e.g. `2133329039`, not `(213) 332-9039`) — some phone-number boxes are
  narrower than they look and will silently truncate formatted numbers
  (confirmed: `(213) 332-9039` got cut to `(213) 332-` on I-131 Part 10). If
  the case only has one phone number, put that same number in both the
  Daytime and Mobile boxes rather than leaving Mobile blank.
- **G-28 Part 4, Item 1 has two checkboxes that both matter** when mail is
  routed to the attorney's address: 1.a (original notices) and 1.b (secure
  identity documents / travel documents). Check both, not just 1.a, whenever
  the case's mail-to-firm setup applies and the secured document category fits
  (e.g. a Reentry Permit or travel document — check for other secure-document
  categories on non-I-131 cases too).
- **Continuation/additional-info pages repeat the client's name in a second,
  separately-indexed field** — easy to fill the "main" name field and miss
  this one. I-131 (Part 13) and G-28 (Part 6/"Additional Information") both
  have a name field at the top of their extra-space page, per the form's own
  instruction to put your name atop every additional sheet — check whether
  any other form in this case's package has the same pattern.
- **Never fabricate firm-specific sensitive data** — attorney bar number,
  USCIS online account number, firm bank routing/account number. If it's not
  already in the Known field maps appendix, search the firm's Drive for a real
  prior filed example of that form before asking the user; only ask directly
  if nothing turns up. A wrong bank routing number or bar number is a real
  error, not a cosmetic one.
- **Verify consequential facts live**, don't just trust an intake note — check
  the current filing fee against USCIS's G-1055 Fee Schedule page even when
  the note is probably right, since fees and mailing addresses change over time.

**After filling, render every page** (`pdftoppm -jpeg -r 150`) and visually
read each one back against the intended values. This catches things a
no-errors script run won't — e.g. a Male/Female checkbox that was simply
never assigned a value.

## Step 4 — Extract client-signature-only pages

Pull just the pages needing the **client's own** signature (not the
attorney's/preparer's) into one combined PDF. Identify these pages from each
form's own instructions (search for "Signature of..." blocks) rather than
assuming a fixed page number — page numbers shift between forms and even
between editions of the same form. For an I-131 + G-28 package specifically:
I-131 page 11 (Part 10, Applicant's Certification and Signature) + G-28 page 3
(Part 4, Signature of Client). Never fill in the client's actual signature or
date field — always leave those blank for wet-ink or e-signature execution.

## Step 5 — Learn `3. Draft`'s own instructions, then compose the cover letter / petition letter

Don't assume `3. Draft` only holds a fill-in-the-blank cover-letter template.
Read **everything** in the folder first — it may also contain instructions,
notes, or an outline doc telling you what this specific letter needs to say:
the legal basis or argument for the petition, specific facts or dates to
foreground, tone, or points the attorney wants raised. Those instructions,
not just a placeholder template, are what Step 5 is actually working from.

- **If `3. Draft` has only a boilerplate cover-letter template** (placeholder
  for the applicant's name and a specific USCIS mailing address baked in —
  the straightforward case, e.g. a reentry-permit filing): treat it as
  before. Verify the mailing address against the current
  `uscis-lockbox-filing-locations-chart` page — the correct lockbox depends
  on the **client's** state of residence and the specific form(s) being
  filed, not the firm's, so don't assume the template's address still
  applies for a different client or case type. Fill in the client's name,
  use today's date, and leave everything else as-is if the fee/address/
  form-list all check out.
- **If `3. Draft` contains substantive instructions or notes** (e.g. for a
  petition letter that needs to argue a specific legal basis, cite facts, or
  make a case-specific argument): use those instructions together with the
  case's Fixed/Flexible template from Step 1 to compose the letter's actual
  content, not just fill in placeholders. Ground every fact and argument in
  either the instructions or the case's own intake materials — never
  fabricate a fact or invent an argument angle. If the instructions leave
  something open (an argument choice, a fact you can't source from intake),
  ask the user rather than guessing.
- Either way, before moving on, confirm the letter's "We have attached the
  following supporting documents..." list is accurate — cross-check it
  against what Step 0/Step 1 actually determined this case needs. This list
  remains the authoritative form list and attachment order for Step 6.

## Step 6 — Assemble the final package

The cover letter is the authority on attachment order — it explicitly tells
USCIS what to expect and in what sequence ("We have attached the following
supporting documents..."), so the assembled PDF's page order must match that
list exactly, item for item. Read the *actual completed cover letter for
this case* before merging — don't assume it matches a previous case's order
or a previous case type's order (e.g. G-1650 → G-1145 → G-28 → I-131 →
passport → green card front/back was one I-131 case's order, but a different
case — even another I-131 case, let alone a different form entirely — could
list things differently, list fewer/more attachments, or omit a form
entirely). Getting this wrong isn't cosmetic — USCIS processes a paper filing
by scanning pages in order against what the cover letter claims, so a
mismatched order can cause processing delays or a document being missed.

Export the cover letter Google Doc to PDF (`gws drive files export`), put it
first, then append each attachment's PDF in the exact order the letter lists
them (cover letter itself is never counted as one of "the following
documents" — it precedes them). Merge with pypdf and upload the result to
`4. Final`.

**Important caveat**: this assembled package still has blank signature
fields (see Step 4) — it is not actually mailable until the client has
signed and those pages are swapped in for the real ones. Don't treat
"assembled" as "ready to ship" without checking signature status first, and
say so explicitly when reporting completion.

## Step 7 — Shipping label (only with explicit purchase confirmation)

Printing a label means spending real money from the firm's ShipSaving
balance — treat it like any other purchase: quote first, then get explicit
go-ahead before charging anything, and separately confirm before purchasing
if it turns out the client hasn't signed yet (see Step 6's caveat) — buying a
real label for an unsigned package is a demo/test action, not a normal
workflow step, so don't do it without the user clearly choosing that.

- ShipSaving auth is a permanent API token (`?api_token=...` query param on
  every request), not a login session — once you have a working token,
  reuse it; don't re-derive it by walking the web UI each time. If a
  previous conversation's token still validates against a free endpoint
  (e.g. `GET /api/balance`), that's confirmation it still works — ask the
  user whether to keep using it or rotate it first if it's ever been
  exposed in a place you're unsure about, but don't assume it needs rotating
  by default.
- Base URL `https://api.shipsaving.com`. Useful account-specific constants
  to record here once known (they're firm-standing, i.e. FIXED, not
  per-case): USPS `carrier_token`, `warehouse_name`.
- Get a rate quote first via `POST /api/rates/list` (free, no charge) with
  `from`/`to` addresses, package dims/weight, and `service_type`. For a
  standard document package, `usps_flat_rate_envelope` under
  `usps_priority_mail` is a reasonable default (flat rate regardless of
  actual content weight, ~2-day delivery).
- Only after the user confirms the quoted price, purchase via
  `GET /api/rates/buy?rate_id=...` (uses the `rate_id` from the quote) —
  this is the actual charge. Download the resulting `label_url` and upload
  it to `4. Final` alongside the package. Record the tracking number in the
  case's Activity Log.

---

# Known field maps appendix

This appendix accumulates field maps as they get built (Step 3). Each entry is
form-specific and tied to a USCIS edition date — **re-verify against Step 2's
edition check before reusing any entry**; if USCIS has published a new
edition, field names/pages may have shifted and that entry needs rebuilding.
When Step 3 builds a map for a form not yet listed here, add it to this
appendix so future cases benefit.

FIXED = the firm's own standing data, reuse identically every case.
FLEXIBLE = pull from that case's copy of its Fixed/Flexible template doc in
`1. Initial` (master copies live under `0. Template`, organized by case type).

All phone number fields should be entered as plain digits with no parentheses
or dashes (e.g. `4155479999`, not `(415) 547-9999`) — some phone boxes are
narrower than they look and will silently truncate a formatted number. When a
case only has one phone number, put it in both the Daytime and Mobile boxes
rather than leaving Mobile blank.

## Firm's fixed standing data (used across all forms, any case type)

| Item | Value |
|---|---|
| Attorney name | Shenqi Cai |
| Firm name | Law Office of Shenqi Cai APC |
| Firm address | 13191 Crossroads Pkwy N (or "Parkway" spelled out — either is fine), Ste 295, City of Industry, CA 91746, USA |
| Firm daytime/mobile phone | 4155479999 |
| Firm email | cassie@lingtulaw.com |
| Firm fax | 6262402046 |
| Bar number / licensing authority | 348794 / the State Bar of California |
| ACH bank account (G-1650) | Business account, Checking, Bank of America, Routing 121000358, Account 325210063004 |

If any of these ever look wrong or the user gives a correction, update this
table — don't silently keep using a stale value.

## USCIS mailing address (flexible — depends on client's state of residence and form)

**There are TWO different lockbox charts and they can give different answers
for the same state** — always check which one actually applies before
picking an address:

- `uscis.gov/uscis-lockbox-filing-locations-chart` ("...for Certain
  Non-Family-Based Forms") — applies to a **standalone** I-131, I-360, I-485,
  or I-765 (i.e. NOT filed concurrently with an I-130).
- `uscis.gov/forms/all-forms/uscis-lockbox-filing-locations-chart-for-certain-family-based-forms`
  ("...for Certain Family-Based Forms") — applies whenever an **I-130 is in
  the package**, including a concurrent I-130+I-485(+I-131+I-864) filing.
  When I-130 and I-485 are filed together, mail the *entire* package (I-130,
  I-130A, I-485, I-131, I-864, etc.) as one package to the address this chart
  gives for the client's state — do not split it across the two charts.

Confirmed lookups (re-verify per case — a new lockbox facility or chart
update can change these):

- **California, standalone I-131/I-485/I-765 (non-family-based chart) → USCIS
  Phoenix Lockbox** (Aug 2026): USPS `USCIS, Attn: NFB, P.O. Box 21281,
  Phoenix, AZ 85036-1281`; FedEx/UPS/DHL `USCIS, Attn: NFB (Box 21281), 2108
  E. Elliot Rd., Tempe, AZ 85284-1806`.
- **Georgia, standalone I-131/I-485 (non-family-based chart) → USCIS Dallas
  Lockbox** (Sep 2026): USPS `USCIS, Attn: NFB, P.O. Box 660867, Dallas, TX
  75266-0867`; FedEx/UPS/DHL `USCIS, Attn: NFB (Box 660867), 2501 S. State
  Hwy. 121 Business Suite 400, Lewisville, TX 75067-8003`.
- **Georgia, I-130 filed concurrently with I-485 (family-based chart) →
  USCIS Elgin Lockbox** (Sep 2026) — a *different* lockbox than the
  standalone-Georgia address above, confirming the two charts really can
  disagree for the same state: USPS `USCIS, Attn: AOS, P.O. Box 4109, Carol
  Stream, IL 60197-4109`; FedEx/UPS/DHL `USCIS, Attn: AOS (Box 4109), 2500
  Westfield Drive, Elgin, IL 60124-7836`.

Most of this firm's clients are CA residents on non-family-based filings, so
Phoenix Lockbox is the common case, but never assume it applies without
checking (a) the client's actual state and (b) whether I-130 is in this
specific package, since that alone can route to an entirely different
lockbox in another state.

---

## I-131 (14 pages) — edition 01/20/25

| Page | Part.Item | Field(s) | Value | Fixed/Flexible |
|---|---|---|---|---|
| 1 | Part 1, Item 1 | `P1[0].CB_AppType[0]` | Reentry Permit selected | Fixed for reentry-permit cases |
| 1 | top block | `P1[0].G28_Attached[0]` | Y | Fixed (G-28 always attached) |
| 4 | Part 2, Item 1 | `Part2_Line1_FamilyName[0]` / `Part2_Line1_GivenName[0]` | client name | Flexible |
| 5 | Part 2, Item 3 | `Part2_Line3_InCareofName/StreetNumberName/AptSteFlrNumber/Unit/CityTown/State/ZipCode/Country` | firm address (when mail-to-firm applies per client's stated preference) | Fixed-when-applicable |
| 5 | Part 2, Item 4 | `Part2_Line4_StreetNumberName/CityTown/State/ZipCode/Country` | client's actual home address | Flexible |
| 5 | Part 2, Item 5 | `#area[0].Part2_Line5_AlienNumber[0]` | client A-Number (digits only, no "A-" prefix) | Flexible |
| 5 | Part 2, Item 6 | `Part2_Line6_CountryOfBirth[0]` | client country of birth | Flexible |
| 5 | Part 2, Item 7 | `Part2_Line7_CountryOfCitizenshiporNationality[0]` | client citizenship | Flexible |
| 5 | Part 2, Item 8 | `Part2_Line8_Gender[0]`="/F" or `[1]`="/M" | client sex | Flexible |
| 5 | Part 2, Item 9 | `Part2_Line9_DateOfBirth[0]` | mm/dd/yyyy | Flexible |
| 5 | Part 2, Item 10 | `#area[1].Part2_Line10_SSN[0]` | 9 plain digits, no dashes (comb field) | Flexible |
| 7 | Part 3, Item 1 | `P3_Line1_Ethnicity[0]`="/NH" or `[1]`="/H" | Hispanic or not | Flexible |
| 7 | Part 3, Item 2 | `P3_Line2_Race_*` | select applicable race(s) | Flexible |
| 7 | Part 3, Item 3 | `P3_Line3_HeightFeet[0]` / `HeightInches[0]` (choice fields — value must match `/Opt` exactly, e.g. "5", "9") | height | Flexible |
| 7 | Part 3, Item 4 | `P3_Line4_Pound1/2/3[0]` (3 single-digit boxes) | weight in lbs | Flexible |
| 7 | Part 3, Item 5 | `P3_Line5_EyeColor[n]` | eye color | Flexible |
| 7 | Part 3, Item 6 | `P3_Line6_HairColor[n]` | hair color | Flexible |
| 7–8 | Part 4, Items 1, 2a, 3a, 4 | `P4_Line1/2a/3a/4_YesNo[1]`="/N" | "No" — default for a clean first-time reentry-permit case (no removal proceedings, no prior reentry permit/RTD, no prior AP, not a replacement) | Flexible if case facts differ from this default |
| 8 | Part 4, Item 7a | `#subform[7].P4_Line7a[1]`="/A" | mail reentry permit to Part 2 Item 3 address | Fixed (assumes mail-to-firm setup) |
| 9 | Part 4, Item 8a | `#subform[8].P4_Line8_CB[0]`="/A" | notification to Part 2 Item 3 address — **note**: the blank template sometimes defaults this to 8.b checked instead; a real filed example (Ruoyao Zhu) confirmed 8.a is the firm's actual practice, matching 7.a. If pulling from a template default, verify against a real precedent before trusting it. | Fixed |
| 9 | Part 4, Item 9b/9c | `#subform[8].P4_Line9b_Email[0]` (is actually Daytime Phone position) / `P4_Line9c_Email[0]` (is actually Email position) | client phone / client email — **field names are swapped from visual position, confirm via rect** | Flexible |
| 9 | Part 5, Item 1 | `#subform[8].P5_Line1_lessthan6/6months/1to2/2to3/3to4/morethan[0]` | client's total time spent outside the US in the relevant window | Flexible |
| 11 | Part 10, Item 1 | `#subform[10].Part10_Line1_DayPhone[0]` | client daytime phone | Flexible |
| 11 | Part 10, Item 2 | `#subform[10].Part10_Line2_MobilePhone[0]` | client mobile phone — if the case only has one phone number, fill this with the same value as Item 1 rather than leaving it blank | Flexible |
| 11 | Part 10, Item 3 | `#subform[10].Part10_Line3_Email[0]` | client email | Flexible |
| 11 | Part 10, Item 4 | `Part10_Line4_ApplicantSignature[0]` / `Part10_Line4_DateofSignature[0]` | **always leave blank** — this is the extracted client-signature page | — |
| 13 | Part 12 | `#subform[12].Part12_Line1_FamilyName/GivenName/Line2_NameofBusinessorOrgName/Line3_DayPhone/Line4_MobilePhone/Line5_Email` | Cai / Shenqi / firm name / firm phone(s) / firm email | Fixed; signature/date left blank for attorney to sign |
| 14 | Part 13 header | `#subform[13].Part2_Line1_FamilyName/GivenName` + `Global_ANumber[0].Part2_Line5_AlienNumber[0]` | client name + A-number | Flexible — only needed if Part 13 additional-info space is actually used |

---

## G-28 (4 pages) — edition 09/17/18

| Page | Part.Item | Field(s) | Value | Fixed/Flexible |
|---|---|---|---|---|
| 1 | Part 1 (attorney info) | `Pt1Line2a_FamilyName`/`Pt1Line2b_GivenName`/`Line3a_StreetNumber`/`Line3b_AptSteFlrNumber`+`Unit[0]`="/ STE "/`Line3c_CityOrTown`/`Line3d_State`/`Line3e_ZipCode`/`Line3h_Country`/`Line4_DaytimeTelephoneNumber`/`Pt1ItemNumber7_FaxNumber` | firm attorney block | Fixed |
| 1 | Part 1, mislabeled pair | `Line6_EMail[0]` (sits at visual **Mobile Phone** box) / `Line7_MobileTelephoneNumber[0]` (sits at visual **Email** box) | phone value goes in `Line6_EMail`, email value goes in `Line7_MobileTelephoneNumber` — confirmed by rect, not by name | Fixed |
| 1 | Part 2 (eligibility) | `CheckBox1[0]`="/Y" (eligible attorney) / `Pt2Line1a_LicensingAuthority` / `Pt2Line1b_BarNumber` / `Checkbox1dAmNot[0]`="/Y" (not subject to any order) / `Pt2Line1d_NameofFirmOrOrganization` | firm eligibility block | Fixed |
| 2 | Part 3, Item 1a/1b | `Line1a_USCIS[0]`="/Y" / `Line1b_ListFormNumber[0]` | matters before USCIS fixed; form number(s) filed (e.g. "I-131") is per-case | 1a Fixed, 1b Flexible |
| 2 | Part 3, Item 5 | `Line4_Checkbox[1]`="/A" (Applicant, confirmed by rect — row 1 left-to-right is Applicant/Petitioner/Requestor at x≈61/133/205; row 2 is Beneficiary-Derivative/Respondent at x≈61/181) | role of the person on whose behalf appearance is entered | Flexible (depends on which form/role is being filed) |
| 2 | Part 3, client info block | `Pt3Line5a_FamilyName`/`Pt3Line5b_GivenName`/`Line9_DaytimeTelephoneNumber`/`Line11_EMail` | client name + own contact info | Flexible |
| 2 | Part 3, Item 9 | `Pt3Line9_ANumber[0]` | client A-Number | Flexible |
| 2 | Part 3, Item 13 (mailing address) | `Line12a_StreetNumberName`/`Line12b_AptSteFlrNumber`+`Unit[0]`="/ STE "/`Line12c_CityOrTown`/`Line12d_State`/`Line12e_ZipCode`/`Line12h_Country` | per the form's own instructions, use the client's own mailing address **unless** it matches the safe mailing address used on the actual application being filed (i.e. mail-to-firm) — then firm address applies here too | Fixed-or-Flexible depending on case's mail-to setup |
| 3 | Part 4, Item 1a + 1b | `Pt4Line2a_CheckBox2a[0]`="/Y" (original notices) AND `Pt4Line2b_CheckBox2b[0]`="/Y" (secure identity docs / travel documents — check both when mail-to-firm applies and the underlying application is a secure-document category, e.g. a Reentry Permit) | notices + secure documents sent to attorney's business address | Fixed |
| — | **Item 13 ↔ Part 4 Item 1a/1b consistency check** | Whenever Item 13 (mailing address) is set to the **client's own** address, Part 4 Item 1a/1b must both be **unchecked** — checking them while Item 13 shows the client's own address creates a direct contradiction (it tells USCIS to route notices/secure documents to "the attorney's business address as listed in this form" while that address field itself holds the client's home). A real correction pass found both boxes still checked after Item 13 had been switched from the firm's address to the client's own — always re-check this pair together, never edit one without the other. | — |
| 3 | Part 4 + Part 5 signatures | `P5_Line6a_SignatureofApplicant[0]` (client) / `Line1_Signature[0]` (attorney) + date fields | **always leave blank** — page 3 is the extracted client-signature page (client's block); attorney signs separately | — |
| 4 | Part 6 (Additional Information), Item 1.a/1.b | `#subform[3].Pt3Line5a_FamilyName[1]` / `Pt3Line5b_GivenName[1]` | client name — **easy to miss**: this is a second, separate instance of the name field (index `[1]`, not `[0]`) repeated at the top of the Additional Information page per the form's own instructions ("Type or print your name at the top of each sheet"); confirmed missed on a first pass, fill it whenever filling page 2's client name fields | Flexible |

---

## I-130 (12 pages) — edition 04/01/24

Field names follow pattern `form1[0].#subform[N].Pt{Part}Line{Item}_{Descriptor}[0]`, but
**the internal `LineN` number does NOT reliably match the on-page displayed Item number**
(e.g. displayed "Item 6" for the beneficiary's city of birth is internally named
`Pt4Line7_CityTownOfBirth` — off by one from the internal counter used elsewhere on the
same page). Match by the `_Descriptor` suffix (self-explanatory: `_FamilyName`,
`_DateOfBirth`, `_CityTownOfBirth`, `_ClassOfAdmission`, etc.), never by the `LineN` prefix,
and always render + visually verify every page afterward — this is not optional on this form.

Checkbox/radio "on" export values are frequently **arbitrary short codes unrelated to the
visible label** — confirmed traps on this form: `Pt2Line36_LPR[0]` (Item 36 "Lawful
Permanent Resident") has on-value `/N`; `Pt4Line28_No[0]` (a "No" checkbox) has on-value
`/Y`. Always pull `/AP /N` keys per-widget before assuming a value string — never infer
from the field's own name.

- **Part 1** (relationship): `Pt1Line1_Spouse[0]`="/Y" etc. Item 4 (gained LPR through
  adoption) `Pt1Line4_No[0]`="/N".
- **Part 2** (Petitioner): A-Number `#area[4].Pt2Line1_AlienNumber[0]`, SSN
  `Pt2Line11_SSN[0]`, name `Pt2Line4a/b/c_FamilyName/GivenName/MiddleName[0]`. Sex
  `Pt2Line9_Male/Female[0]`="/Y". Mailing address unit type `Pt2Line10_Unit[0/1/2]` export
  values are `/APT `, `/STE`, `/FLR` (note trailing space on APT only — copy exactly).
  Item 11 "mailing same as physical" `Pt2Line11_Yes[0]`="/Y" — when Yes, leave the
  Physical Address 1/2 fields (Item 12–15) blank. Marital fields: `Pt2Line16_NumberofMarriages`,
  `Pt2Line17_Married[0]`="/Y", current-marriage date/place `Pt2Line18_DateOfMarriage`,
  `Pt2Line19a/b/d_CityTown/State/Country`. Parents: `Pt2Line24a-29` (Parent 1),
  `Pt2Line30a-35` (Parent 2). Item 36 "I am a" USC/LPR: `Pt2Line36_USCitizen[0]`/
  `Pt2Line36_LPR[0]`="/N" (see trap above). If LPR: Item 40 Class of Admission (free text,
  e.g. green card Category code like `E53`) + admission date/place `Pt2Line40a-e`; Item 41
  "gained LPR through marriage" `Pt2Line41_No[0]`="/N". Employment History Employer
  1 (current — type "Unemployed" if applicable) `Pt2Line40_EmployerOrCompName`+`Pt2Line42-43`,
  Employer 2 (prior) `Pt2Line44_EmployerOrOrgName`+`Pt2Line45-47`.
- **Part 3** (Biographic — petitioner): Ethnicity `Pt3Line1_Ethnicity[0]`="/NH" (Not
  Hispanic), Race `Pt3Line2_Race_Asian[0]`="/A" etc., Height as two **Choice** fields
  `Pt3Line3_HeightFeet[0]`/`HeightInches[0]` (plain digit strings as `/Opt` value, e.g.
  "5"/"9" — inches goes 0–11), Weight as 3 separate single-digit `Tx` boxes
  `Pt3Line4_Pound1/2/3[0]`, Eye color `Pt3Line5_EyeColor[n]` (BRN=index1 for Brown — check
  `/AP /N` per index, they're not in visible-label order), Hair color
  `Pt3Line6_HairColor[n]` (BLK=index1 for Black, same caveat).
- **Part 4** (Beneficiary): mirrors Part 2's structure for name/A-Number/SSN/DOB/birth
  city+country/sex/address (`Pt4Line1/3/4/7/8/9/11...`). Item 10 "has anyone else filed a
  petition" `Pt4Line10_No[0]`="/N". Marital info `Pt4Line17-24` (marital status is a 6-way
  checkbox group `Pt4Line18_MaritalStatus[0-5]` = W/A/S/SNM/M/D — Married is index 4="/M").
  "Beneficiary's Family" Person 1/2/3 (`Pt4Line25-36`) asks for the beneficiary's spouse
  AND children per the form's plain instructions — for a spousal petition this means
  re-listing the **petitioner** as Person 1 with Relationship="Spouse", not skipping it as
  redundant. Entry Information: Item 45 EVER in US `Pt4Line20_Yes[0]`="/Y"; Item 46 Class
  of Admission is a **Choice field** `Pt4Line21a_ClassOfAdmission[0]` needing an exact
  `/Opt` match (e.g. "F1" for F-1 student — NOT "F-1"); I-94 number field is internally
  named `#area[8].Pt4Line21b_ArrivalDeparture[0]`; Item 46.d "date authorized stay expires"
  accepts literal text `D/S` for Duration of Status. Passport/travel doc `Pt4Line22-25`.
  Employment `Pt4Line26-27` (Item 51-52 on page). Item 53 immigration proceedings
  `Pt4Line28_No[0]`="/Y" (trap — see above). Item 59 "last address lived together if
  filing for spouse" `Pt4Line56/57_*` — use the **current** shared address if still living
  together, not a historical one. Item 61 (AOS at USCIS office) City/State
  `Pt4Line60a/b_CityOrTown/State` — use the beneficiary's local field office city.
- **Part 5** (Other Info): Item 1 "ever previously filed a petition for this beneficiary
  or any other alien" is its own field pair `Part4Line1_Yes[0]`="/Y" / `Part4Line1_No[0]`="/N"
  (note the field is named "Part4Line1" despite living in the Part 5 section — another
  name/location mismatch; verify by rect/page, not name).
- **Part 6** (Petitioner's Statement/Contact/Signature): Item 1.a (reads English)
  `Pt6Line1Checkbox[0]`="/A", 1.b (used interpreter) `[1]`="/B". **Also check Item 2**
  (`Pt6Line2_Checkbox[0]`="/C") whenever the attorney/preparer actually filled out the
  form for the client (i.e. every case this firm handles) and fill the blank preparer-name
  field `Pt6Line2_RepresentativeName[0]` with the attorney's name — easy to skip since the
  form's own note only says "select 1.a or 1.b", but Item 2 is a separate, additional
  checkbox that applies whenever a preparer was involved, per the form's own instruction
  ("If applicable, select the box for Item Number 2"). Contact info
  `Pt6Line3/4/5_DaytimePhoneNumber/MobileNumber/Email`. Signature
  `P5_Line6a_SignatureofApplicant[0]` — **always leave blank**.
- **Part 7** (Interpreter) / **Part 8** (Preparer): leave Part 7 blank if no interpreter
  used. Part 8 is the attorney/preparer block (Fixed firm data) — field names split across
  two pages: page 1 has name/business/mailing address (`Pt8Line1a/1b_PreparerFamilyName/
  GivenName`, `Pt8Line2_BusinessName`, `Pt8Line3_*` address); page 2 has contact info +
  statement + signature. **Trap**: `Pt8Line5_PreparerFaxNumber[0]` is mislabeled — Part 8
  has no fax field on the actual page, this field sits at the visual "5. Preparer's Mobile
  Telephone Number" position. Put the firm's mobile/daytime number there (same number,
  per Fixed data), not a fax number. Item 7 preparer statement: not-attorney
  `Pt8Line7_Checkbox[0]`="/A" vs. attorney `[1]`="/B"; if attorney, sub-choice extends/does-not-extend
  beyond this petition `Pt8Line7b_Checkbox[0]`="/Y" (extends) / `[1]`="/N" (does not extend) —
  **firm standard is always "does not extend"** regardless of whether G-28 is also filed
  (an earlier version of this note said to pick "extends" whenever G-28 accompanies the
  petition; that was wrong and got corrected in a real filing — G-28 being filed doesn't
  change this answer). Preparer signature left blank.
- **Part 9** (Additional Information): repeats the petitioner's name + A-Number at the top
  (`#subform[11].Pt2Line4a/b_FamilyName/GivenName[1]` + `Pt2Line1_AlienNumber[1]` — note
  the `[1]` index, a second instance of the same field name used on page 1) — same
  "sign every extra sheet" pattern as I-131/G-28, fill it even if Part 9 itself stays blank.

---

## I-130A (6 pages) — edition 04/01/24

Filled entirely by/about the **spouse beneficiary** (not the petitioner). Same `Pt{Part}Line{N}_{Descriptor}` naming as I-130, same caveat about `LineN` not reliably matching displayed
Item numbers — match by descriptor suffix, verify visually.

- **Part 1**: A-Number, name (`Pt1Line1/3a/3b`). Two "Physical Address" slots
  (`Pt1Line4`+`Pt1Line5a/b` dates; `Pt1Line6`+`Pt1Line7a/b` dates) plus one "Last Address
  Outside the US" slot (`Pt1Line8`+`Pt1Line9a/b`) — same 2-slot-for-5-years limitation as
  I-130, use the most recent entries. Parent 1/2 info `Pt1Line10-23`. **Corrected trap**
  (an earlier version of this note wrongly claimed Parent 1's City/Town/Village of Birth
  and City/Town/Village of Residence had no fillable field at all — verified false by
  sorting every widget on the page by `/Rect` Y-position and checking internal names
  against visual position one by one; do this full sort whenever a field "seems missing"
  rather than trusting a prior note). The real mapping, confirmed by Y-sorted widget walk:
  `Pt1Line12CityTownOfBirth[0]` = Item 13 (Parent 1 City/Town/Village of **Birth**,
  despite the internal "Line12" number); `Pt1Line13_CountryofBirth[0]` = Item 14
  (Parent 1 Country of Birth); `Pt1Line14_CountryofBirth[0]` = Item 15 (Parent 1
  City/Town/Village of **Residence** — internally misnamed "CountryofBirth" despite
  being the residence-city field); `Pt1Line15_CountryofResidence[0]` = Item 16 (Parent 1
  Country of Residence). For Parent 2: `Pt1Line18_CityTownOfBirth[0]` = Item 20
  (City/Town/Village of Birth); `Pt1Line19_CountryofBirth[0]` = Item 21 (Country of
  Birth); `Pt1Line20_CityTownVillageofRes[0]` = Item 22 (City/Town/Village of Residence,
  correctly named this time); `Pt1Line21_CountryofResidence[0]` = Item 23 (Country of
  Residence). All eight fields exist and are fillable — don't leave any of them blank
  on the assumption the form lacks the field.
- **Part 2/3** (Employment): same current+prior employer pattern as I-130's Part 2
  employment section (`Pt2Line1-8`); Part 3 is for overseas employment only if not
  already covered — leave blank if the beneficiary never worked outside the US.
- **Part 4** (Statement/Contact/Signature): checkbox positions are **not in reading
  order** — this is a two-column page where Item 1.a (reads English) sits at the
  **bottom of the left column** (`Pt4Line1Checkbox[1]`="/A") while 1.b (interpreter,
  `Pt4Line1Checkbox[0]`="/B") and Item 2 (preparer assisted, `Pt4_Checkbox[0]`="/C" +
  `Pt4Line2_RepresentativeName[0]` for the preparer's name) sit at the **top of the right
  column** — confirmed only by rendering the blank page and reading positions visually;
  do not infer from field index order. Check Item 2 whenever a preparer helped (i.e.
  every case this firm handles), matching the I-130 Part 6 Item 2 pattern.
- **Part 5** (Interpreter) / **Part 6** (Preparer): same Fixed firm block as I-130
  Part 7/8, field names `Pt6Line1a/1b_PreparerFamilyName/GivenName`, `Pt6Line2_BusinessName`,
  `Pt6Line3_*` address, `Pt6Line4_DaytimePhoneNumber`. **Trap**: `Pt6Line5_PreparerFaxNumber[0]`
  is mislabeled exactly like I-130's — it sits at the visual "Mobile Telephone Number"
  slot, not a fax field; put the firm's daytime/mobile number there. Statement checkboxes
  `Pt6Line7_Checkbox[0/1]`="/A"(not attorney)/"/B"(attorney), extends/does-not-extend
  `Pt6Line7b_Checkbox[0/1]`="/Y"/"/N".
- **Part 7** (Additional Information): repeats name + A-Number at top
  (`Pt1Line3a/3b_FamilyName/GivenName[1]` + `Pt1Line1_AlienNumber[1]`) — same pattern as
  I-130 Part 9, fill even when the free-text area itself stays blank.

---

## I-864 (12 pages) — edition 08/24/26 (brand-new edition, flipped mandatory 08/31/26)

**Critical trap, worse than the usual `LineN` drift**: this form's internal field-name
`Part` prefixes are **systematically swapped** relative to the displayed Part numbers —
confirmed by cross-referencing every field against rendered page text, not assumed:

| Field prefix | Actually lands on displayed... |
|---|---|
| `P4_Line*` | **Part 2** (Information About You — the Sponsor) |
| `P2_Line*` | **Part 3** (Information About the Principal Immigrant) |
| `P3_Line*` | **Part 4** (Information About the Immigrants You Are Sponsoring) |
| `P5_Line*`, `P6_Line*`, `P7_Line*`, `P8_Line*`, `P9_*`, `P10_Line*`, `P11_Line*` | match their own displayed Part number normally (no swap past Part 4) |

Don't assume this pattern holds on the next edition — re-verify by rendering blank pages
and reading Part headers before reusing.

- **Part 1** (Basis): `P1_Line1a-f_CB[0-5]` = "/1A".."/1F" for items 1.a-1.f in order
  (1.a petitioner, 1.d only joint sponsor, etc.) — happens to match visible order here,
  unlike most checkbox groups on this form family.
- **Part 2 / Sponsor** (`P4_Line*`): name `P4_Line1a/1b_FamilyName/GivenName`, mailing
  address `P4_Line2*`, "mailing same as physical" `P1_Line3_Checkbox[0]`="/Y". **Trap**:
  `P4_Line7_CityofBirth[0]` is mislabeled — it sits at the displayed **"Country of
  Birth"** slot (Item 7), not city; put the country there. Immigration status
  `P4_Line11a/b/c_Checkbox[0]`="/A"(citizen)/"/B"(national)/"/C"(LPR) — independent
  checkboxes, not a radio group. SSN `P4_Line10_SocialSecurityNumber` and A-Number
  `#area[1].P4_Line12_AlienNumber` — **do not fabricate if missing**; a joint sponsor
  who isn't yet a client of record may not have these on file yet, leave blank and flag
  for follow-up rather than guessing. Military service `P4_Line14_Checkboxes[0/1]`="/Y"/"/N".
- **Part 3 / Principal Immigrant** (`P2_Line*`): mirrors sponsor fields — name, address,
  `P2_Line3_CountryCitizenship`, DOB, `#area[2].P2_Line5_AlienNumber`, phone. Same person
  across every sponsor's I-864 in a case (the beneficiary), copy verbatim each time.
- **Part 4 / Immigrants Sponsored** (`P3_Line*`): Item 1 "sponsoring the principal
  immigrant" `P3_Line1_Checkbox[0]`="/Y" — check this and leave the Family Member 1-4
  slots blank when there are no derivative beneficiaries.
- **Part 5** (Household Size, `P5_Line*` — no swap here): Item 1 = number of immigrants
  sponsored (usually "1"). Item 2 "Yourself" is model-filled as `P5_Line2_Yourself[0]`
  but note the rendered form shows it as a fixed "1" regardless — still write "1" for
  clarity. **Whether Item 3 (spouse) gets "0" or "1" depends entirely on whether that
  spouse is already the person counted in Item 1** — for the *petitioning* sponsor whose
  own spouse IS the intending immigrant, enter "0" (already counted); for an unrelated
  *joint* sponsor, enter "1" for their own spouse plus separately for any dependent
  children (`P5_Line4`). The overall sum goes in `Override[0]` (the actual "Household
  Size" box) — pypdf/Acrobat does not auto-sum these for you, compute and enter it
  yourself, then sanity-check against the case's own stated household size if one exists.
- **Part 6** (Employment/Income, `P6_Line*`): the four status checkboxes
  (`P6_Line1_Checkbox`/`P6_Line4_Checkbox`/`P6_Line5_Checkbox`/`P6_Line6_Checkbox`, each
  independently "employed"/"self-employed"/"retired"/"unemployed") are **easy to get
  wrong from stale intake data** — a client's own prior "Unemployed since [date]" answer
  and a separately-stated "current annual income" figure can directly contradict each
  other (unemployed but claiming income). Don't silently pick one; fill what the data
  actually says (including the contradiction) and flag it explicitly for the attorney —
  this is a substantive sufficiency question, not a form-filling one. If employment
  status is simply unknown (common for a joint sponsor who isn't the firm's own client),
  leave the checkbox group blank entirely rather than guessing "employed", and flag
  it — an incomplete-but-honest field beats a fabricated one on a document signed under
  penalty of perjury. **Item 16.a-c "total income... as reported on my Federal income tax
  returns"** wants the actual AGI line from each year's return — for a sponsor who files
  a *joint* return with a spouse, this is the joint AGI as printed on that return (not an
  attempted individual-only carve-out), since that's literally what "reported on my
  return" means; note the joint-filing nuance for the attorney regardless. Household size
  total → `P6_Line15_TotalHouseholdIncome`.
- **Part 8** (Sponsor's Contract/Statement/Signature): reads-English `P6_Line1_Checkbox[1]`="/A"
  (note: reuses the Part-6-prefixed field name on this page — yet another cross-part name
  collision, confirm by page+rect, not name) — check this and **Item 2** (preparer
  assisted) `P8_Line2_Checkbox[0]`="/Y" + `P8_Line2_Attorney[0]` for the attorney's name,
  matching the same "always check Item 2 when a preparer helped" pattern as I-130/I-130A.
  Contact info `P8_Line3/4_DaytimeTelephoneNumber/MobileTelephoneNumber` +
  `P7Line7_EmailAddress[0]` (yet another stray cross-part prefix on the email field name).
  Signature `P8_Line9a_ApplicantSignature[0]` — leave blank.
- **Part 9** (Interpreter) / **Part 10** (Preparer, Fixed firm data): straightforward,
  `P10_Line1a/1b_PreparersFamilyName/GivenName`, `P10_Line2_PreparersBusinessName`,
  `P10_Line4_PreparersDaytimePhoneNumber`. **Trap**: `P10_Line5_PreparersFaxNumber[0]` —
  verify against a render before assuming it's a real fax field; on sibling forms
  (I-130/I-130A) the same-sounding field name turned out to be mislabeled as the mobile
  slot — check this form's own page before reusing the firm's fax number there blindly.
- **Part 11** (Additional Information): name repeat at top uses the **Part-2/sponsor**
  prefix again (`P4_Line1a/1b_FamilyName/GivenName[1]` + `Global_ANumber[0].P4_Line12_AlienNumber[1]`)
  — consistent with the Part-swap table above, not a new pattern.

**Filing multiple I-864s in one case** (petitioner + one or more joint sponsors): each
person gets their own complete copy of this 12-page form — don't try to combine them.
Cross-check that the Principal Immigrant block (Part 3) is byte-identical across every
copy in the package, since that's the one thing that must never vary between sponsors.

---

## G-1145 (1 page) — edition 09/26/14 — entirely flexible

| Field | Value |
|---|---|
| `LastName[0]` / `FirstName[0]` | client name |
| `Email[0]` | client email |
| `MobilePhoneNumber[0]` | client mobile/phone (digits, no formatting needed) |

---

## G-1650 (1 page) — edition 06/03/25

| Section | Field(s) | Value | Fixed/Flexible |
|---|---|---|---|
| Applicant Info | `sfApplicantPetitionerName[0].GivenName/FamilyName` | client name | Flexible |
| Bank Account Holder | `sfBankAccountHolderInfo[0].CB_AccountType[0]`="/B" (Business), `GivenName`="Shenqi", `FamilyName`="Cai" | firm account holder | Fixed |
| | `sfBankAccountInformation[0].BusinessName[0]` | "Law Office of Shenqi Cai APC" | Fixed |
| Bank Account Info | `sfBankAccountInformation[0].CB_CreditCardType[1]`="/V" — **this field is misleadingly named "CreditCardType" but is actually the Checking-Account checkbox**, confirmed by rect (leftmost of the two boxes, matching "Checking Account" being left of "Savings Account" on the page) | Checking account selected | Fixed |
| | `sfBankAccountInformation[0].RoutingNumber[0]` / `AccountNumber[0]` / `BankName[0]` | 121000358 / 325210063004 / Bank of America | Fixed |
| | `sfBankAccountInformation[0].AuthorizedPaymentAmt[0]` | the verified current filing fee for the specific form/category (check USCIS G-1055 Fee Schedule each time — was $630 for I-131 Reentry Permit as of Aug 2026) | Flexible (form/category and time-dependent) |
| Signature | `AuthorizationandSignature[0].SignatureOfApplicant[0]` | **always leave blank** — Shenqi Cai signs personally since it's the firm's own account | — |

---

## I-485 (24 pages, ~820 fields) — edition 01/20/25 (see edition-update note below)

**Edition update (confirmed 09/2026):** USCIS has republished this form with
edition date 09/04/26. Diffed field-by-field against the 01/20/25 build below:
same field count (820), same field names by suffix, same checkbox/radio export
codes — only the `#subform[N]` index prefix shifted for many fields (e.g.
Marital Status moved from `#subform[6]` to `#subform[9]`). Practical upshot:
every trap and field-name suffix documented below still applies verbatim: to
reuse values from an older filled copy of this form, match by **suffix only**
(strip the `#subform[N]`/`#pageSet[...]`/`#area[N]` segments and compare what's
left) rather than by full dotted path, then re-verify a handful of checkbox
codes via `/_States_` before trusting the rest — don't assume this holds
forever; re-diff again next time USCIS bumps the edition date.

By far the largest and most treacherous form encountered so far. Internal field
names carry a `PtXLineY_...` prefix that is **frequently wrong** — both the
Part number and, on at least one page, the Line number itself. Do not trust
either number embedded in a field's own name; confirm the real Part by
rendering, and confirm the real visual position of any checkbox/radio group by
extracting widget `/Rect` coordinates (sort by descending Y within a page,
then by ascending X within a row) and cross-referencing against the rendered
page text. This form burned that lesson twice in one build:

- **Checkbox arrays with cryptic numeric export codes are NOT reliably in
  visual order.** `Pt6Line1_MaritalStatus[0..5]` has codes `/3,/1,/4,/2,/5,/7`
  — despite *looking* sequential, checking all 6 simultaneously (to eyeball
  the mapping) proved nothing, since all 6 boxes lit up regardless of order.
  The only reliable test is either (a) set ONE index at a time and render, or
  (b) pull `/Rect` and sort. Verified: index `[3]` code `/2` = "Married"
  (leftmost-to-rightmost visual order is index 1,3,0,2,4,5). Same trap on
  `Pt5Line2_YNNA[0..2]` (really Part 6 Item 2, spouse-in-armed-forces
  N/A·Yes·No) — code `/N` = the *rightmost* box ("No"), not the first one.
  By contrast, plain `/Y` / `/N` coded Yes-No pairs are always safe to target
  by state value regardless of physical widget order (confirmed across ~90
  Yes/No pairs) — the scrambling risk is specific to multi-way
  numeric/lettered code groups (Marital Status, the 5-bracket income/asset/
  liability groups, the 25-item public-charge exemption list, the 8-item
  education-level group), and only Marital Status/YNNA actually turned out
  scrambled; the rest (`Pt2Line3a_CB` immigrant category, `Pt3Line1_CB`
  exemption list, `Pt9Line53/59/60_CB` brackets, `Pt9Line61_CB` education,
  `Pt9Line56_CB` public-charge exemptions, `Pt2Line11_CB`/`Pt2Line2_CB`) were
  verified via `/Rect` and found correctly sequential — but every one of them
  was *checked* via Rect, none assumed.
- **Page 14 (subform 13, Part 9 items 10-22) has scrambled internal Line
  numbers**, unlike every other Part 9 page (15,16,17,20,21 all have internal
  numbers that increase monotonically top-to-bottom, matching real item
  numbers exactly). On page 14 specifically, walking widgets top-to-bottom by
  `/Rect` Y gave real-item → internal-name as: item14→`Pt8Line18_YesNo`,
  item15→`Pt8Line19_YesNo`, item16→`Pt8Line20_YesNo`, item17→`Pt8Line17_YesNo`
  (this one coincidentally matches), item18→`Pt8Line23_YesNo`,
  item19→`Pt8Line24a_YesNo`, item20→`Pt8Line24b_YesNo`,
  item21→`Pt8Line24c_YesNo`, item22→`Pt8Line22_YesNo`. Confirmed by the
  vertical gap between consecutive widgets (~18pt for a 1-line question,
  ~30pt for a 2-line question) lining up with the real item text's line
  count — a mismatch shows up immediately as an impossible gap.
- **Conditional follow-up items must be left BLANK, not defaulted to "No"**,
  whenever their trigger question is "No": items 20, 21 (depend on item 19),
  29 (depends on 28), 35.b (depends on 35.a), 40 (depends on 39), 77 (depends
  on 76), and the items 65/66 benefit/institutionalization tables (depend on
  63/64). Scan the page text for both `"If you answered ... is Yes"` and
  `"If your answer ... is Yes"` phrasing (the form uses both) before building
  the default-No list — grepping only one phrasing misses items 29/35.b/40.
- **Part 9's ~86 plain Yes/No eligibility questions** (spanning pages
  13-21, internally split between `Pt8Line*_YesNo` and `Pt9Line*_YesNo`
  prefixes despite all being visually Part 9) can be bulk-defaulted to "No"
  for a client with no adverse history — build the list by finding, for each
  base field name, whichever indexed sibling's `/_States_` contains `/N`,
  then exclude the conditional ones above. **This must be confirmed with the
  client before filing** if there is any chance the true answer to any of
  them is Yes — flag it, don't just default it, unless the client's own
  intake documents (or an explicit statement, e.g. "no criminal record", "no
  immigration violations") support No.
- **Employment/school history rows split across two mislabeled fields**:
  Part 4 Item 7's row has `Pt4Line7_EmployerName[0]` (left "Employer or
  School" box), `[1]` (which is actually the **Occupation** field, not a
  3rd employer-name slot), and `[2]` (right "Name of Employer, Company, or
  School" box — fill identically to `[0]`). The "If unemployed, source of
  financial support" field for that same row is `Part4Line7_StreetName[1]`
  (not a street name at all). Item 8's mirror fields:
  `Pt4Line8_EmployerName[0]`, `Pt4Line8_Occupation[0]` (these two ARE
  correctly named), and `Part4Line8_StreetName[0]` for its own
  source-of-support field. Confirmed only by filling each index with its own
  label text and rendering — guessing from the name alone would have been
  wrong for at least 3 of these 6 fields.
- **Part 5 (Parents) Line numbers shift by +1/+2 partway through**: Item 4
  (Parent 1 country of birth) is `Pt5Line5_CityTownOfBirth[0]`; item 5
  (Parent 2 legal name) is `Pt5Line6_Family/Given/MiddleName[0]`; item 6
  (Parent 2 name at birth) is `Pt5Line7_...`; item 7 (Parent 2 DOB) is
  `Pt5Line8_DateofBirth[0]`; item 8 (Parent 2 country of birth) is
  `Pt5Line10_CityTownOfBirth[0]`. The SAME `Pt5Line8_DateofBirth[]` array is
  then reused for Part 6 (Marital History) fields with no relation to
  parents at all: `[1]`=current spouse DOB (item 6), `[2]`=date of marriage
  to current spouse (item 9), `[3]`=prior spouse DOB (item 12). Only
  discovered by filling every index with a unique label and rendering pages
  10-11 side by side.
- **Part 10/11 contact-info fields are duplicated** with two different naming
  schemes on the same page (22): `Pt3Line3_DaytimePhoneNumber1` /
  `Pt3Line4_MobileNumber1` / `Pt3Line5_Email` (higher `/Rect` Y = top of
  page = the real **Part 10 Applicant** contact block) vs.
  `P3_Line4_DaytimeTelePhoneNumber` / `P3_Line5_MobileTelePhoneNumber` /
  `P3_Line6_Email` (lower Y = **Part 11 Interpreter** block — leave blank
  when no interpreter is used). Likewise `P12_SignatureApplicant[0]` /
  `P13_DateofSignature[0]` sit at the bottom of page 22 and are actually
  the **Part 11 interpreter's own signature line**, not Part 12/13 — leave
  blank.
- **Part 14 Additional Information text fields ARE multiline** (`/Ff`
  multiline bit set), but pypdf's/poppler's auto-generated appearance stream
  does not word-wrap long single-paragraph text — it just overflows off the
  visible box edge. Pre-wrap any addendum text into short lines with
  explicit `\r` line breaks (one fact per line) rather than relying on the
  field's own wrap behavior, and verify by rendering.
- Item 56 (public charge exemption) — for a standard case with no VAWA/
  asylee/refugee/etc. history, the correct box is "I do not fall under any
  of the exempt categories listed above and will complete Item Numbers
  57-66", which is `Pt9Line56_CB[23]`='/23' (verified via Rect: this is the
  3rd item at the top of page 19, following 22 items that spill onto the
  bottom of page 18 in a scrambled index order — codes matched their own
  index number exactly, unlike Marital Status, once Rect-sorted).
- Item 58/59/60 (household income/assets/liabilities brackets) — **do not
  guess a bracket** unless the client file has one clean, unambiguous
  consolidated household figure. Whether "household income" should include
  a cohabiting spouse's separate earnings changes which bracket applies;
  when that isn't settled in the record, leave the item blank and flag it
  for the client/attorney rather than picking a bracket.
- **Item 56 defaults to unchecked even when Items 57-66 are already filled
  in** — a real build had Household Size (57) and Education (61) correctly
  filled but the master Item 56 "I do not fall under any of the exempt
  categories..." checkbox itself left blank. Always check this box explicitly
  (`Pt9Line56_CB[23]`='/23') whenever Items 57-66 are being completed; don't
  assume filling the sub-items implies the parent selection is done.
- **Visa Number (`Pt1Line10_VisaNum[0]`, Part 1 Item 10) is NOT the I-94
  number** — it must be read off the physical visa foil in the passport,
  specifically the red-ink printed number in the bottom-right corner (labeled
  just a number, not "Visa Number" on the foil itself). Do not confuse it with
  the visa's black "Control Number" or with the separate I-94 arrival record
  number field elsewhere on the same page.
- **"Principal Applicant's Name/A-Number/DOB" block (Part 2, `Pt2Line2_*` /
  `Pt1Line2_DOB[0]`) must be filled even when the applicant checked "Principal
  Applicant"** (not "Derivative Applicant") — this firm's practice is to
  repeat the applicant's own name/A-Number/DOB here regardless, rather than
  leaving it blank because "the derivative-only instruction doesn't apply to
  me."
- **Two separate "In Care Of Name" fields exist for two different address
  blocks** on Part 1 (current physical/mailing address, page 3:
  `Part1_Item18_InCareOfName[0]`; prior address, page 4:
  `Pt1Line18_PriorInCareOfName[0]`) — fill both with the applicant's own name
  per the firm's standing In-Care-Of rule; don't fill only the first one you
  find.
- **Employer-or-School Item 7/8 ordering must be most-recent-first** — if the
  client has more than 2 employment/education entries in the lookback window,
  Item 7 (current) and Item 8 (2nd slot) must hold the two MOST RECENT
  entries; older entries go to Part 14 Additional Information. A real build
  initially put the oldest entry in Item 8 and pushed a more recent one to
  Add Info — backwards, and worth double-checking chronological order
  whenever there are 3+ entries to place.
- **Item 7's category field (`Pt4Line7_EmployerName[0]`) takes the literal
  word "School" or "Employer"**, not the institution's name (the actual name
  goes in `[2]`, the "Name of Employer, Company, or School" box) — if the
  person's Item 7 entry is fundamentally a school enrollment (e.g. a graduate
  student who also holds a paid Research/Teaching Assistant role at the same
  school), categorize it as "School" and add a companion "Employer" entry in
  Part 14 for the same institution/period, rather than writing the school's
  name into the category box.
- **Part 14 Additional Information has two parallel, both-valid field-naming
  schemes** for the same widgets on this edition: `pypdf.get_fields()` may
  report a filled value under one name (e.g. `Pt9Line3d_AdditionalInfo[0]`)
  while walking the page's `/Annots` `/Parent` chain directly gives a
  different name for the same widget (e.g. `P14_Line2_AdditionalInfo[0]`).
  Both keys work with `update_page_form_field_values` — if a value written
  under one name doesn't seem to appear, don't assume the field is missing;
  cross-check the other naming scheme before concluding data was lost. Each
  of the 4 text-box items has its own Page/Part/Item triple:
  `Pt9Line3a/b/c_*[0]` through `[3]` for items 2-5 respectively.
- **Each Additional Information entry must be its own separate Item** —
  don't combine two unrelated entries (e.g. two different schools) into one
  Item's text block just because both are "additional employment/education
  history"; give each its own Page/Part/Item triple and text box, and include
  the full address (not just city/country) for foreign entries.

*(Add new entries here as Step 3 builds them for other case types.)*

