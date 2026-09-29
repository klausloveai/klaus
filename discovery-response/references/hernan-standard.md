# The Hernán standard — what he changed, and the check that catches it

**How to read this file.** Every rule below came from an actual correction, logged in
`revisions/`. Each is one of: **LAW** (an authority does not say what it was cited for),
**PROCEDURE** (a required element was missing), **METHOD** (the reasoning was wrong), or
**STYLE** (house format). LAW and PROCEDURE rules are mostly enforced by
`scripts/preflight.py` — run it and the machine catches them. **METHOD rules are not
mechanizable; they only work if you read this file before drafting.** That is the whole
reason it is short.

Provenance: round 1 — Yi Cong v. Edpao, FROG + RFP Set One, returned 2026-09-28
(`revisions/2026-09-28-yi-cong-frog-rfp.md`).


## A. Citation must support the proposition

| Was cited for | Why it failed | Check |
|---|---|---|
| Food & Agric. Code §30801 — "dog owner must license" | The section **authorizes counties to adopt** licensing ordinances; it imposes no duty on the owner. Health & Safety Code §121690 is the one that binds the owner. | Read the section text, not a summary of it. |
| Catholic Mut. Relief Soc. v. Superior Court (2007) 42 Cal.4th 358 — health-insurance discovery | It is a **reinsurance** case. | State §2017.210's reach affirmatively instead of leaning on a case about a different product. |
| Coito v. Superior Court (2012) 54 Cal.4th 480 — attorney-client privilege | Coito is **work product**. A-C privilege is Evid. Code §954. | One authority per theory; do not let a cite straddle two. |
| Webb / Schnabel — "the tax-return privilege is not waived by a lost-earnings claim" | Neither case says that. | Say what the case holds: returns are privileged **from compelled disclosure**. Verify pin cites (Webb 513, not 513-514; Schnabel 718-721, not 719-721). |

**Rule: before citing, ask whether the case's actual issue is the proposition you need.
"Right conclusion, wrong dispute" is the dangerous failure — it reads as correct.**

## B. Never assert past the document

- "the license was obtained **only at the quarantine release**" — the Animal Control report
  does not say that; it was inferred from the timeline. Removed.
- "obtained the medications **in connection with his urgent-care treatment**" — the pharmacy
  labels contradict it. Reduced to what the labels show.
- An answer that contradicts another answer is the same failure: RFP 9 said he bought
  medication at urgent care and lost the receipt, while FROG 9.1 said he paid ~$70 to the
  clinic. Made consistent.

## C. Match the question's time window

FROG 8.4 asks for monthly income **"at the time of the INCIDENT."** The draft averaged the
eight weeks *after* it. Corrected to the four weekly payments closest to the incident
(13W–16W): $7,977.74 ÷ 4 = **$1,994.44/week → $8,642.57/month**, and FROG 8.7 at 74 days
off = **$21,083.51**.

**Show the arithmetic in the answer** so the defence can verify it against the produced
documents. "At the time of" ≠ "over the claim period."

## D. Internal consistency

- An employer end-date must be the last **worked** week, not the last **payment** date.
- FROG 8.2(c) "the date your employment began" means with the employer **at the time of the
  incident**, not the start of the career. Split into both facts if they differ.
- Diagnoses must match the records **verbatim**. The draft listed F43.21; the records say
  F32.1 (major depressive disorder, single episode, moderate), F43.22, F43.10.

## E. Procedure that gets forgotten

1. **Proof of service.** Every party who has **appeared** is served, not just the
   propounding party. Co-defendants who answered get the responses; the caption picks up
   `AND RELATED CROSS-ACTION` once a cross-complaint is filed. List every electronic
   service address from their Notice of E-Service.
2. **Verification.** It must not contradict the answers. Client who cannot read English →
   the verification says the responses were **translated to him**, plus a **Declaration of
   Translator** for whoever translated.
3. **CCP §2031.240.** Withholding on privilege requires the response itself to **describe
   what is withheld** — whose statement, who took it, when, who holds it. "A privilege log
   will be provided on request" is not compliance.

## F. Additions that protect the case

- Disclose **every** person named in a report as present, even non-witnesses to the event
  (the other three fire-crew members). Undisclosed witnesses can be excluded later.
- A withholding response should still **point to what does exist** — e.g. the agency reports
  that record statements made at the scene — so the answer is not a bare refusal.

## G. Objection discipline

Where an objection is made but everything is still produced, add:

> **No responsive document is being withheld on the basis of the objection stated above.**

Without it the objection reads as cover for withholding, which is the standard
meet-and-confer and motion-to-compel opening.

Objection form, per his signed work: **one ground, one cite, no stacking.**

> Responding Party objects to this interrogatory to the extent that it seeks material
> protected by the attorney work product doctrine under Code of Civil Procedure section
> 2018.030. Subject to and without waiving that objection, Responding Party responds: No.

Supplementation clause carries the statute: *"...reserves the right to amend and to
supplement this response under Code of Civil Procedure section 2030.310."*

## H. House format

- Dates written out: **April 12, 2026**, never 04/12/2026.
- Addresses unabbreviated: Parkway North, Boulevard, Suite, California.
- Abbreviations spelled out on first use: magnetic resonance imaging, x-ray, computed
  tomography.
- Signature block `By: ______________________________`, name without `, Esq.`
- Proper names spelled as the source document spells them (Duesenberg, not Dusenberg).
- No Chinese characters anywhere in a served document.

## Open question carried forward

Ontario Fire Department address: the prehospital care report header reads **415 East B
Street** (Fire Administration); the Animal Control activity card reads **425 E B ST**
(Ontario Fire Dispatch). Hernán standardised on 425. Confirm which he wants before reusing.
