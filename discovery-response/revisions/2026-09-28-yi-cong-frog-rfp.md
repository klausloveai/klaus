# 2026-09-28 — Yi Cong v. Edpao (CIVSB2619725), FROG + RFP Set One

**Reviewer:** Hernán S. Simó · **Drafter:** Klaus · **Round:** 1 (first use of this workflow)

| | |
|---|---|
| Sent for review | 2026-09-25 |
| Returned | 2026-09-28 |
| Scope | FROG Set One (51 answers), RFP Set One (19 requests), index, production |
| Substantive changes | 12 distinct issues |
| Preventable by a check that existed at the time | 0 — no gate existed |
| New checks added to preflight.py | 6 |
| Carried as prose only | 6 |

## What became a rule

| # | Correction | Class | Now enforced by |
|---|---|---|---|
| 1 | Food & Agric. §30801 cited for an owner duty — it only authorizes county ordinances | LAW | `preflight` BAD_CITES |
| 2 | Catholic Mut. Relief Soc. cited for health insurance — it is a reinsurance case | LAW | `preflight` BAD_CITES |
| 3 | "tax privilege not waived by a lost-earnings claim" — Webb/Schnabel do not say it | LAW | `preflight` BAD_CITES |
| 4 | Coito cited for attorney-client privilege — it is work product | LAW | prose (§954 vs §2018.030) |
| 5 | Verification said the client "read" the responses, contradicting FROG 2.9/2.10 | PROCEDURE | `preflight` verification check |
| 6 | Declaration of Translator missing | PROCEDURE | `preflight` verification check |
| 7 | Objection made, everything produced, no withholding sentence | PROCEDURE | `preflight` objection check |
| 8 | §2031.240 — a privilege log "on request" is not compliance; describe the withheld item | PROCEDURE | prose |
| 9 | No proof of service for co-defendants who had appeared | PROCEDURE | prose (docket check) |
| 10 | FROG 8.4 "at the time of the INCIDENT" answered with a post-incident average | METHOD | prose |
| 11 | Facts asserted past the document (licence timing, medication provenance) | METHOD | prose |
| 12 | Internal contradictions (employer end-date, "continuously" vs the work gap, diagnosis codes) | METHOD | prose |

## Cosmetic, folded into preflight as warnings

Dates written out · addresses unabbreviated · abbreviations spelled out on first use ·
`By: ______` with no `, Esq.` · proper names spelled as the source spells them.

## Judgment calls he made (not rules — record so the next draft starts closer)

- **Kept** the loss-of-earnings claim despite the earnings pattern, resting it on the
  Healthier Minds records (unemployed and occupationally impaired on 8/10; "considerable
  time away from work" on 9/10). The lesson is not "always claim" — it is that the
  treating records, not the payment records, are what carry a psychological wage claim.
- **Declined** to cite City of Ontario ordinances or to name the Camden defendants in
  FROG 14.1, because the claim against Camden is premises liability, not statutory.
- **Confirmed** withholding the client's recorded statement.

## Open

Ontario Fire Department address — the prehospital report header says 415 East B Street
(Fire Administration); the Animal Control card says 425 E B ST (Fire Dispatch). He
standardised on 425 and attributed it to the fire report. Unresolved; ask before reusing.
