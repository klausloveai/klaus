# Reading a served discovery packet

## What normally arrives

Six documents in one e-service email. Only the first three need written responses.

| Document | Response due? | What it drives |
|---|---|---|
| Form Interrogatories — General (DISC-001) | yes | the client questionnaire |
| Special Interrogatories, Set One | yes | the client questionnaire |
| Demand for Production (CCP §2031.010) | yes | the materials list at the end of the questionnaire |
| Answer | no | affirmative defenses — ammunition for our own FROG 15.1 |
| Demand for Jury + Notice of Posting Jury Fees | no | confirm **our** jury fees are posted — theirs does not cover us |
| Notice of Deposition | no | calendar it; tell the client it is far off |

## Extracting the content

- SROGs and RFP carry a text layer: `pdftotext -layout`.
- **FROGs are a scan.** No text layer. Render and read the boxes:
  `pdftoppm -png -r 100 FROGS-GENERAL.pdf page` then read each page image. The form is
  8 pages; a served copy runs 10–12 with the caption and proof of service.
- Page 1 also carries the propounding/responding parties, the set number, and which
  `INCIDENT` definition under Sec. 4(a) is checked.
- Grep for `jury` without excluding `injury` and every "Injury Photos.pdf" becomes a false
  positive. Use `grep -vi injury`.

## DISC-001 structure

88 numbered interrogatories, deliberately non-contiguous (5.0, 18.0, 19.0, 25.0, 30.0,
40.0, 60.0 are `[Reserved]`; 70.0 / 101.0 / 200.0 point at DISC-003 / DISC-004 / DISC-002),
so the same number means the same thing across every FROG form.

| | | | |
|---|---|---|---|
| 1.0 who answers (1) | 2.0 individual background (13) | 3.0 entity background (7) | 4.0 insurance (2) |
| 6.0 injuries (7) | 7.0 property damage (3) | 8.0 loss of income (8) | 9.0 other damages (2) |
| 10.0 medical history (3) | 11.0 prior claims (2) | 12.0 investigation (7) | 13.0 surveillance (2) |
| 14.0 statutory violations (2) | 15.0 denials/defenses (1) | 16.0 defendant's contentions (10) | 17.0 RFA follow-up (1) |
| 20.0 motor vehicle (11) | 50.0 contract (6) | | |

Form interrogatories do **not** count against the 35 specially-prepared limit
(CCP §2030.030(a)(1)–(2)), which is why a packet can carry 54 FROGs *and* 52 SROGs.

## Direction check — what the defence checked but cannot apply

Defence counsel check these out of habit when serving on a plaintiff:

- **3.0** entity background — only if the responding party is a company.
- **13.0** surveillance, **15.1** denials and affirmative defenses, **16.0** defendant's
  contentions — these are propounded *by* a plaintiff *to* a defendant. 15.1 asks about
  "your pleadings"; a plaintiff's complaint has no affirmative defenses. 16.2 asks the
  plaintiff whether *they* contend the plaintiff was not injured.
- **17.1** is meaningless unless Requests for Admission were served with the set.
- **20.0** motor vehicle on a dog-bite case; **50.0** contract on any PI case.

Keep these in the bilingual copy (they were served, they need a response) but put them in
`ATTORNEY_ONLY` so they never reach the client.

## Over the 35-SROG limit

CCP §2030.030(a)(1) gives 35 specially prepared interrogatories as of right. More is
allowed under §2030.040 with a §2030.050 **Declaration for Additional Discovery**, on three
grounds only: complexity/quantity of issues, the financial burden of deposition, or the
expedience of the method.

The limit is not a cap — it shifts the burden. Under **§2030.030(c)**, if the responding
party moves for a protective order on the ground that the number is unwarranted, *the
propounding party* must justify it. We cannot simply decline to answer the excess; that
earns sanctions without a protective order under §2030.090.

Things worth checking in their declaration, and objecting to in the preamble to our
responses even when we answer anyway:

- §2030.050's form requires the recital *"I have previously propounded a total of ___
  interrogatories to this party, of which ___ were not official form interrogatories."*
  It is often missing.
- Declarations copy-pasted from an RFA declaration say "admissions" throughout instead of
  "interrogatories."
- **§2030.060(d)**: "Each interrogatory shall be full and complete in and of itself. No
  preface or instruction shall be included." A set that opens with a paragraph of
  instructions ("In answering these Interrogatories, please furnish all information
  available to you…") violates this.

Standard play: preserve the objections in writing, then answer subject to them. A motion
over a curable defect costs more than the answers.

## Never ask the client for these

Render with no answer box and a red note that the firm handles it separately:

- **Social security number** — protected by the California constitutional right to privacy
  (art. I, §1); routinely propounded, rarely supportable without a showing of need.
- **Medicare Claim Number / HICN.**

Neither belongs in a document that travels by email or WeChat.

## Questions the client cannot answer

Billing-side SROGs (amounts billed, amounts accepted, amounts paid by any source,
write-downs and adjustments, which providers were attorney-referred under *Qaadir v.
Figueroa* (2021) 67 Cal.App.5th 790) come out of the firm's ledger, not the client's memory.
Mark them `F` so the questionnaire tells the client to skip them, and answer them from
the accounting records.

## Deadline

30 days from service (CCP §2030.260(a) / §2031.260), extended by 5 calendar days for mail
(§1013) or **2 court days for electronic service** (§1010.6(a)(3)(B)). Compute it, then
confirm against Hernán's calendar — he calendars these himself and court holidays are easy
to miss. Ask the client back roughly a week earlier to leave room to draft and translate.
