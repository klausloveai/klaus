# 案件总表 — the 人才移民 tracking sheet

Spreadsheet ID `1hVkR6sLbQossobqyUA4bJ7Qg3P-mrYF2YupMJvdflEQ`, titled **案件总表**,
sits at the root of the 人才移民 shared drive. This is the sheet a new O1 / EB1A /
NIW case gets logged into — not the SIA 高徒 "Lingtu Case Tracking Sheet" that
the `it` skill writes to. Two different firms-worth of cases; don't cross them.

## Tabs

| sheetId | Title | Use |
|---|---|---|
| `354295660` | **法律** | the case register — this is the one you write |
| `311223653` | Form Responses 1 | raw intake form dump, read-only |
| `0` | 背景 | background research working sheet |
| `1794940758` | O1 OFFER | O-1 offer tracking |
| `836032669` | NIW未来计划 | NIW future-plan drafting |
| `1255719269` | 背景（证书版） | |
| `966222781` | 排期中需要回访 | |
| `1952222911` | 软著 | |
| `1437019248` | 学术 | |
| `1938641757` | 新闻 | |

Only 法律 gets a row at case-creation time. The others are working sheets that
fill in later as the case progresses — writing to them early just creates rows
nobody maintains.

## 法律 layout

Row 1 is a colour legend (白底 = 新案子第一次客户会议后, 红底 = 待签约签完后,
red flag = 不上 g28, 急 = special attention, H1B 抽签提醒, 陪跑每周一/五 follow up).
Row 2 is the header. **New cases go in at row 3 — the top of the data, right
under the header — not appended at the bottom.** The team reads this tab
newest-first, and a new case buried at row 165 is a case nobody sees.

| Col | Header | What to write for a new case |
|---|---|---|
| A | Task | client name as it appears on the folder, e.g. `Xuan Shen`. Existing rows sometimes append a note (`Jiumei Wang 二胡 戏曲 P3`) — fine to mirror that if the intake note has a distinguishing specialty. |
| B | Priority | `1`–`4`. `4` is the overwhelming default (normal queue); `1` is most urgent. Use `4` unless the intake says otherwise, and say which you used. |
| C | Assignee | free text, matched to a real person: KK, Betty, Skye, Cassie, Kathy, Nina — or a combination (`KK, Skye`). Leave blank if unassigned; don't invent a name. |
| D | Case Type | `O1A`, `O1B`, `EB1A`, `NIW`. Note the sheet distinguishes O-1A from O-1B even though the Drive folder is just `O-1`. |
| E | Status | `To be assigned` for a fresh case with no assignee, `In progress` once someone owns it. Later values: `Submitted`, `RFE`, `Approved`, `Denied`, `TERMINATED`. |
| F | 重要笔记 | the one- or two-line gist from the intake note — status/deadline facts the team needs at a glance, not the whole note (that lives in the intake doc). |
| G | Deadline | date, e.g. `10/1/2026`. Blank if none known. |
| H | Folder | plain URL of the **case root** folder. |
| I | 框架 | leave blank |
| J | Advisory Letter | leave blank |
| K | 新闻+推荐信 | leave blank |
| L | 未来计划 | leave blank |
| M | PL | leave blank |
| N | Exhibit | leave blank |
| O | Form | leave blank |
| P | Review and Backup | `FALSE` |
| Q | Collect Fees | `FALSE` |
| R | I-797 Approval Notice | leave blank |
| S | Intake Month | e.g. `2026-08`, or blank |
| T | Service Fees | number, if the intake states it |
| U | Service Center | leave blank |
| V | RFE officer | leave blank |

Columns I–O are per-stage progress markers (`not started` / `in progress` /
`completed`). A brand-new case has made no progress on any of them, so leaving
them empty is the honest answer — filling them with `not started` just adds
noise the team has to scan past.

## Writing the row

Two calls: insert a blank row 3, then fill it. Insert first rather than
overwriting — `insertDimension` with `inheritFromBefore: false` makes the new
row inherit formatting and data validation from the row *below* it (a real data
row), so dropdowns and colour rules carry over. Writing straight into a row you
didn't insert would push nothing down and overwrite a live client.

```bash
gws sheets spreadsheets batchUpdate \
  --params '{"spreadsheetId": "1hVkR6sLbQossobqyUA4bJ7Qg3P-mrYF2YupMJvdflEQ"}' \
  --json '{"requests": [{"insertDimension": {"range": {"sheetId": 354295660, "dimension": "ROWS", "startIndex": 2, "endIndex": 3}, "inheritFromBefore": false}}]}'

gws sheets spreadsheets values update \
  --params '{"spreadsheetId": "1hVkR6sLbQossobqyUA4bJ7Qg3P-mrYF2YupMJvdflEQ", "range": "'"'"'法律'"'"'!A3:V3", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["Xuan Shen","4","","EB1A","To be assigned","<gist>","","<folder url>","","","","","","","","FALSE","FALSE","","2026-08","",""]]}'
```

`startIndex: 2` is 0-based, so it inserts *at* row 3. Pass the full A:V width in
one row array (empty strings for columns you're leaving alone) so nothing lands
in the wrong column.

Verify afterwards by reading back the top of the data:

```bash
gws sheets +read --spreadsheet 1hVkR6sLbQossobqyUA4bJ7Qg3P-mrYF2YupMJvdflEQ --range '法律!A2:V4'
```

Row 3 should be the new client and row 4 the case that used to be at the top.
If row 3 is someone else's case, the insert didn't happen and you just
overwrote them — restore from version history immediately.

## Highlighting a row

The colour legend in row 1 is applied by hand as cell background colour, not by
a value. If asked to highlight (e.g. 红底 for 待签约), that's a `repeatCell`
`batchUpdate` against sheetId `354295660` with
`userEnteredFormat.backgroundColor`, `fields: "userEnteredFormat.backgroundColor"`.
