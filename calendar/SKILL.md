---
name: calendar
description: |
  Create a litigation deadline on Klaus's Google Calendar for 凌图律所 / Lingtu Law, in the
  firm's standard shape: Tomato-colored all-day event, a title that names the case and what
  is due, a description that shows the computation and the authority, and Hernán invited.
  Use whenever any of these come up: calendar the deadline, 设置日历, 加个期限, 记一下 due date,
  "calendar the deadline to respond", "diary this to me", response due, answer due, discovery
  responses due, CM-110 due, jury fees due, CPRA determination due, statute of limitations,
  "/calendar". Hernán ends most task emails with an instruction to calendar something —
  that is this skill. It ALSO carries the California date-computation rules (service-method
  extensions, court days vs calendar days, judicial holidays) so the date on the calendar is
  the real deadline and not a guess. It only writes to the calendar; it never serves, files,
  or emails anything.
---

# Calendar — litigation deadlines

Klaus's calendar is the firm's deadline system. A deadline that is on it in the wrong shape
is nearly as bad as one that is missing, because nobody can tell from the title what is due
or verify the date. This skill produces one consistent shape.

## House shape (all five, every time)

1. **Color = Tomato, `colorId` `"11"`.** Non-negotiable for anything that is a deadline.
   Google Calendar has no per-type default color — the only way to get Tomato reliably is to
   set `colorId` on creation, which is why this skill exists. (Set 2026-09-11 by Klaus; the
   27 then-existing deadline events were back-filled to Tomato the same day.)
2. **All-day event on the deadline date.** Not a timed event — a deadline is a day, not an
   appointment. The exception is a court appearance, which is timed and takes the department's
   actual calendar time.
3. **Title = `<Case> — <what is due> Due`**, with the case number when the matter is filed.
   Say who owes it when that is not obvious:
   - `Yi Cong v. Rhea Edpao — Defendant's Discovery Responses Due`
   - `CB Kitchen (26CHCV01306) — Plaintiff's Discovery Responses Due`
   - `Bo Tao: EXTENDED deadline for Rachel and Becky Beas to answer Complaint`
   Mark an extended date as `EXTENDED` in the title so nobody works off the original.
4. **Description carries the proof.** Anyone opening the event must be able to check the date
   without opening the file:
   - what was served or filed, itemized, and on whom
   - the service date **and the method** (the method drives the extension)
   - the computation, written out, with the statute cited
   - case number, court, department, judge
   - opposing counsel and their service email
   - what happens if it passes — this is what makes the event actionable
5. **Invite Hernán** (`hernan.s@lingtulaw.com`). Add `cassie@lingtulaw.com` and
   `joe@lingtulaw.com` when the whole team is carrying the matter. Reminder 1 day before
   (1440 minutes); add 7 days (10080) for a court date or anything that needs preparation.

## Computing the date — do this before creating anything

**Never put "30 days from service" on the calendar as 30 calendar days without checking the
service method.** Hernán's task emails say "30 days"; the real date is 30 days plus the
extension the service method earns. Getting this wrong understates the deadline and invites a
premature meet-and-confer, or overstates it and misses a motion.

| Underlying period | Authority |
|---|---|
| Respond to Summons and Complaint — 30 days after service | CCP §412.20(a)(3) |
| Respond to an amended complaint — 30 days after service | CCP §471.5(a) |
| Interrogatory responses — 30 days after service | CCP §2030.260(a) |
| Demand for production responses — 30 days after service | CCP §2031.260(a) |
| Requests for admission responses — 30 days after service | CCP §2033.250(a) |
| Statement of Damages after a request — 15 days | CCP §425.11 |
| Case Management Statement (CM-110) — file **and serve** no later than 15 calendar days before the CMC | CRC 3.725(a) |
| Meet and confer before the CMC — no later than 30 calendar days before the CMC | CRC 3.724 |
| Advance jury fees, $150 **per side** — on or before the date set for the initial CMC | CCP §631(b), (c); waiver under §631(f)(5) |
| CPRA determination — 10 days, extendable by written notice by no more than 14 | Gov. Code §7922.535(a), (b) |
| Government claim — 6 months from accrual | Gov. Code §911.2(a) |
| Suit after written rejection of a government claim — 6 months | Gov. Code §945.6(a)(1) |
| Personal injury statute of limitations — 2 years | CCP §335.1 |
| Motion notice — 16 court days before the hearing | CCP §1005(b) |

**Then add the service-method extension to the responding party's time:**

| Service method | Extension | Authority |
|---|---|---|
| Electronic service | **+2 court days** | CCP §1010.6(a)(3)(B) |
| Mail, addressee inside California | **+5 calendar days** | CCP §1013(a) |
| Mail, addressee outside California but in the U.S. | +10 calendar days | CCP §1013(a) |
| Overnight delivery | +2 court days | CCP §1013(c) |
| Personal service | none | — |

**Counting rules.** Exclude the first day, include the last (CCP §12). If the last day falls
on a holiday, the period runs to the next day that is not a holiday (CCP §12a, §12b). A
**court day** excludes Saturdays, Sundays and judicial holidays (CCP §2016.060). California
judicial holidays are fixed by CCP §135: January 1, Martin Luther King Jr. Day, February 12,
Presidents' Day, March 31 (Cesar Chavez Day), Memorial Day, June 19, July 4, Labor Day,
November 11, Thanksgiving and the day after, and December 25.
**Columbus Day / Indigenous Peoples' Day is NOT a California judicial holiday** — a deadline
counted through the second Monday in October counts that day. This has come up.

Worked example, the one to copy: discovery e-served Wednesday 09/09/2026. 30 calendar days
→ Friday 10/09/2026. Plus 2 court days → Monday 10/12, Tuesday **10/13/2026**. That is the
date on the calendar, and the description says so.

## Run it

```bash
python3 ~/.claude/skills/calendar/scripts/add_deadline.py config.json
```

`config.json`:

```json
{
  "summary": "Yi Cong v. Rhea Edpao — Defendant's Discovery Responses Due",
  "date": "2026-10-13",
  "attendees": ["hernan.s@lingtulaw.com"],
  "reminders_minutes": [1440],
  "description_blocks": {
    "served": "Plaintiff's written discovery (Set One) e-served on Todd Vigus 09/09/2026: Form Interrogatories-General (DISC-001) + Sec. 4(a)(2) Attachment, Special Interrogatories, Requests for Admission, Demand for Production.",
    "computation": "30 calendar days from 09/09/2026 service = 10/09/2026 (Fri), plus 2 court days for electronic service (CCP 1010.6(a)(3)(B)) = 10/13/2026 (Tue). 10/12 is not a California judicial holiday (CCP 135).",
    "matter": "CIVSB2619725 — San Bernardino Superior, Dept. S24.",
    "counsel": "Defense counsel: Todd Vigus, VIGUS LAW, todd@viguslaw.com.",
    "if_missed": "If no responses: objections are waived (CCP 2030.290(a), 2031.300(a), 2033.280(a)) and a motion to compel lies."
  }
}
```

`colorId` is forced to `"11"` by the script — do not pass it and do not override it.
The script prints the created event's link; paste it back to Klaus.

## Changing an existing deadline

When a date moves, **patch the existing event; do not create a second one.** Two events for
one deadline is how a stale date gets worked off. Put `EXTENDED` in the title, restate the
original date in the description, and say who agreed to the extension and in writing where.

```bash
gws calendar events patch \
  --params '{"calendarId":"primary","eventId":"<ID>","sendUpdates":"all"}' \
  --json '{"summary":"... (extended to 9/30)","start":{"date":"2026-09-30"},"end":{"date":"2026-10-01"},"colorId":"11"}'
```

An all-day event's `end.date` is the day **after** the deadline — Google treats it as
exclusive. Getting this wrong puts the event on the wrong day in some views.

## Notes

- Klaus's calendar is `primary`; gws authenticates as klaus@.
- `sendUpdates`: `"all"` when a date changes and people are already invited; `"none"` for a
  cosmetic fix such as back-filling a color.
- Report the entry back to whoever asked for it — Hernán routinely asks for confirmation that
  the deadline is on the calendar, and the reply should state the date and the computation,
  not just "calendared."
- Related: [[jury-fee-notice-workflow]] (the $150 is its own deadline and its own filing),
  [[add-pos]] step 6 (service triggers the responding party's clock).
