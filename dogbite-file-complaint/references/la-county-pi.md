# LA County PI Filing — Reference

## Case-type → CM-010 box → CIV 109 action code + reason

For **personal injury** the CM-010 Item 1 box is always **Other PI/PD/WD (23)**
(tooltip `Other PI/PD/WD (23)`). The CIV 109 Column B action code differs by tort:

| Tort | CIV 109 Column B | code | reason |
|------|------------------|------|--------|
| Dog bite / animal attack | 2301 Premise Liability (…dog attack…) | `2301` | `4` |
| Slip / trip and fall, dangerous property condition | 2301 Premise Liability | `2301` | `4` |
| Assault / battery / intentional bodily injury | 2302 Intentional Bodily Injury | `2302` | `4` |
| Emotional distress (intentional) | 2303 IIED | `2303` | `4` |
| Other personal injury (catch-all) | 2304 Other PI/PD/WD | `2304` | `4` |
| Auto / motor-vehicle | 2201 Motor Vehicle (Auto (22) on CM-010!) | `2201` | `4` |

**Reason 4** = "Location where bodily injury, death or damage occurred" — the
correct basis for essentially every PI filing (the incident address determines the
courthouse). Reasons live at the top of CIV 109 page 1.

> Auto cases use CM-010 box **Auto (22)** not Other PI/PD/WD (23); adjust
> `case_type_tooltip` to `Auto (22)` and `civ109_action_code` to `2201`.

## Filing court — always confirm with the Locator

PI cases file in the district **where the incident occurred** (LASC General Order
2024-GEN-003, eff. 5/17/2024 — the central PI Hub is retired). Use the Filing Court
Locator with the incident **city + ZIP**; read the **Unlimited Civil** column.

Common Southeast-area result (verify each time — ZIPs can straddle districts):

| Incident city (ZIP) | Courthouse | District | Courthouse address |
|---|---|---|---|
| Huntington Park (90255) | Norwalk Courthouse | **Southeast** | 12720 Norwalk Blvd., Norwalk, CA 90650 |

Do not infer the district by map direction — some cities are geographically in one
area but administratively assigned to another. The Locator result is authoritative,
and the courthouse's own page shows its district (URL suffix `/Courthouse/info/SE`
= Southeast, `/WE` = West, etc.).

## House court format

- **SUM-100** court box: line 1 = courthouse **name** (`Norwalk Courthouse`);
  line 2 = `<street>, <city>, CA <zip>` (`12720 Norwalk Blvd, Norwalk, CA 90650`).
  The SUM-100 name box is narrow — keep line 1 to just the courthouse name.
- **CM-010**: `COUNTY OF` = `LOS ANGELES`; street + mailing = courthouse street;
  city/zip = courthouse city/zip; **BRANCH NAME = courthouse name** (`Norwalk
  Courthouse`).
- **CIV 109 Step 5**: certify filed in the **`<District>`** District (`Southeast`).
- **SUM-100 long party captions.** `FillText25` (defendant) and `FillText180`
  (plaintiff) are multiline fields, but pypdf does NOT auto-wrap — a long value
  renders as one line overflowing into the FOR-COURT-USE box. For multi-defendant
  or minor/GAL captions, put an explicit `\n` in the config value at a sensible
  break so it wraps to 2 lines (each line must fit the ~395pt field width). Match
  the complaint caption verbatim, including `, an individual` after each defendant
  — **never abbreviate defendants to "et al."** (they must be named for service);
  "et al." is only acceptable on the plaintiff side.

## Why the fill script does what it does (technical gotchas)

1. **XFA hybrid forms.** Judicial Council fillable PDFs carry an XFA layer; Acrobat
   renders XFA and ignores the AcroForm values you set. The script deletes `/XFA`
   so every viewer/e-filing portal uses the AcroForm values.
2. **Preserve pre-filled fields.** The templates already have the accented attorney
   block with its own appearance streams. The script never forces global
   `NeedAppearances` (which would regenerate — and possibly mangle — those); it
   only generates appearances for the fields it fills.
3. **Form-revision field-name drift.** The CM-010 Item-1 "Other PI/PD/WD (23)" box
   is `CheckBox23` in one revision and `Item1Check[5]` in another. The script finds
   it by **tooltip**, and reads each checkbox's own on-state from its `/AP` — so it
   works across revisions without hard-coded state values.
4. **CIV 109 Column B — revision-dependent.** On **Rev 04/26+** Column B "Type of
   Action" is a REAL radio field (`03`) whose kid widgets carry on-states like
   `/2301 Premise Liability`; `set_action_radio()` selects the kid whose on-state
   begins with the 4-digit action code (no coordinates, revision-proof). On **older**
   revisions the boxes are static `☐` glyphs, so the script falls back to
   `locate_civ109_boxes()` + stamping an X. `fill_civ109` tries the radio first and
   only stamps if no matching field exists. The reason radios, incident
   address, and district cert on the LAST page ARE real fields (found by tooltip:
   numbers `1`–`11`, `CITY`, `STATE`, `ZIP CODE`, `ADDRESS`, and the "I certify …
   properly filed" text). If a new revision shifts the layout, re-derive the stamp
   coordinate: render page 1 with gs, find the target box; the `☐` glyphs sit at
   x≈204, and the y for each row can be read by scanning glyph positions.
5. **Render with Ghostscript, not poppler.** `pdftoppm` mangles these forms' fonts
   (whole page shows placeholder boxes); `gs -sDEVICE=png16m` renders them faithfully.

## What stays blank
Case number (court assigns), attorney signature, and date. Also: no Guardian ad
Litem (CIV-010) unless the plaintiff is a minor. Later, add the property owner /
other defendants by DOE amendment and serve their agent for service.
