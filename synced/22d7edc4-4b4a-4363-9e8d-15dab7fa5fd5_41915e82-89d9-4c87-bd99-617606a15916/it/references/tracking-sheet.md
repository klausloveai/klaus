# Lingtu Case Tracking Sheet — deep reference

Read this only when something in SKILL.md's Step 5 doesn't hold anymore: the
spreadsheet ID stops resolving, you're writing to a tab that isn't in the
known-tabs table, or a write produces a cell that looks right but doesn't
behave right (dropdown/checkbox stopped being selectable, a formula column
shows a frozen number instead of recalculating).

## Re-resolving the spreadsheet if the ID breaks

More than one file in this Drive is named "Lingtu Case Tracking Sheet". The
real one lives directly in the "SIA 高徒" shared drive. If
`1krpgB6Mzd6fBsUzP2LKe9F0sfBad4Wb0ZlwdYSbrzeE` (the ID in SKILL.md) ever 404s,
re-find it and verify before trusting a new ID:

```bash
gws drive files list --params '{"q": "name='"'"'Lingtu Case Tracking Sheet'"'"' and trashed=false", "fields": "files(id,name,parents)", "supportsAllDrives": true, "includeItemsFromAllDrives": true, "corpora": "allDrives"}'
gws drive drives get --params '{"driveId": "<CANDIDATE_PARENT_ID>", "fields": "id,name"}'
```

The correct file's parent must resolve to drive name "SIA 高徒" (drive ID
`0AE7q4ToQFsarUk9PVA`). Don't just take the first search hit.

## Why a plain string write can look right but behave wrong

Several columns are backed by `ONE_OF_LIST` dropdown validation, `BOOLEAN`
checkbox validation, or formulas (auto-numbering, computed balances). Writing
`"TRUE"` as a string instead of an actual boolean, or a literal number instead
of the formula the column actually uses, makes the cell *display* correctly
but stops it being a selectable dropdown/checkbox and breaks any formula
downstream that reads it.

Worse: a **blank row** (one sitting empty past the end of existing data, or a
row you just inserted) has no data validation on it at all — it's a plain
cell. Writing a value that happens to match a dropdown option string doesn't
make it a dropdown. You must bring the formatting over explicitly before (or
together with) writing the value.

### Diagnosing an unfamiliar tab

Read an existing **data** row (not the header) with grid data to see what
each column actually is:

```bash
gws sheets spreadsheets get --params '{"spreadsheetId": "<SSID>", "ranges": ["'"'"'<TAB>'"'"'!A<SAMPLE_ROW>:Z<SAMPLE_ROW>"], "includeGridData": true, "fields": "sheets(data(rowData(values(userEnteredValue,dataValidation))))"}'
```

Look for `dataValidation.condition.type` (`ONE_OF_LIST` with a `values` list,
or `BOOLEAN`) and for `userEnteredValue.formulaValue` (a formula, not a typed
value — e.g. `=row()-1` or `=H2-I2`). Once you've mapped a tab's columns, add
the map to SKILL.md's known-tabs table so future runs skip this step.

### Carrying formatting/validation into a new row

Copy format + validation from an adjacent real data row before/with writing
values — `values update` only touches the value, never the format, so this
must happen as its own step:

```bash
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId": "<SSID>"}' --json '{
  "requests": [
    {"copyPaste": {"source": {"sheetId": <SHEET_ID>, "startRowIndex": <SRC-1>, "endRowIndex": <SRC>, "startColumnIndex": 0, "endColumnIndex": <NCOLS>}, "destination": {"sheetId": <SHEET_ID>, "startRowIndex": <DST-1>, "endRowIndex": <DST>, "startColumnIndex": 0, "endColumnIndex": <NCOLS>}, "pasteType": "PASTE_FORMAT"}},
    {"copyPaste": {"source": {"sheetId": <SHEET_ID>, "startRowIndex": <SRC-1>, "endRowIndex": <SRC>, "startColumnIndex": 0, "endColumnIndex": <NCOLS>}, "destination": {"sheetId": <SHEET_ID>, "startRowIndex": <DST-1>, "endRowIndex": <DST>, "startColumnIndex": 0, "endColumnIndex": <NCOLS>}, "pasteType": "PASTE_DATA_VALIDATION"}}
  ]
}'
```

### Inserting a row mid-table (e.g. right after a header, not at the bottom)

```bash
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId": "<SSID>"}' --json '{"requests": [{"insertDimension": {"range": {"sheetId": <SHEET_ID>, "dimension": "ROWS", "startIndex": <INSERT_INDEX_0BASED>, "endIndex": <INSERT_INDEX_0BASED+1>}, "inheritFromBefore": false}}]}'
```

`inheritFromBefore: false` pulls formatting from the row that ends up *after*
the insertion point — use this when inserting right below a header, so the
new row inherits from the real data row being pushed down, not from the
header. If you insert in the middle of existing data instead, `true` (inherit
from the row now above it) is usually right — use judgment based on which
neighbor is an actual data row.

### Cleaning up a misplaced row

If an earlier attempt wrote a row in the wrong place (e.g. appended at the
bottom of a tab that sorts newest-first), don't leave both copies: confirm
the stray row's contents match what you're about to write correctly, then
`deleteDimension` it once the correctly-placed row is verified good.

```bash
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId": "<SSID>"}' --json '{"requests": [{"deleteDimension": {"range": {"sheetId": <SHEET_ID>, "dimension": "ROWS", "startIndex": <ROW-1>, "endIndex": <ROW>}}}]}'
```

## Highlighting a cell (background color, not a value)

```bash
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId": "<SSID>"}' --json '{
  "requests": [{
    "repeatCell": {
      "range": {"sheetId": <SHEET_ID>, "startRowIndex": <ROW-1>, "endRowIndex": <ROW>, "startColumnIndex": <COL-1>, "endColumnIndex": <COL>},
      "cell": {"userEnteredFormat": {"backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}}},
      "fields": "userEnteredFormat.backgroundColor"
    }
  }]
}'
```
