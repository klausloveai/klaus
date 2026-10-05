# Worked example — Jiajun He, 2026-10

First full run of this workflow. Recording the traps, because most of them cost a round trip.

## The case

- **Client** Jiajun He · DOL 08/15/2026 · Montebello
- **Drive** `Jiajun He-8-15-2026` = `1pIKgwZsxv6ZKpCfUpZHN4_zUNU8lvKPb`
- **CM** Ryan Wei → Picase@ (Jenkins took over picase@ on 2026-10-02 mid-handover)
- **3P** Farmers · policy 189661039 · claim 5044424448-1 · BI adjuster Kara Bachus-Litton ·
  `myclaim@farmersinsurance.com` · insured Adriana Raya Acosta · liability 100% accepted
- **1P** Progressive — **no claim ever opened** (see trap 2)
- **Provider** Prestige Integrative Health Center (chiro) · `Prestige5553@hotmail.com`
- **Retainer** PI Auto Retainer **(New)** 50/50, DocuSigned **08/17/2026**, contains both the
  ATTORNEY LIEN clause and an AUTHORIZATION FOR RELEASE OF RECORDS
- **Successor** Welch & Chen Law Associates · Fang L. Chen, Esq. · 801 S. Garfield Ave., Suite 288,
  Alhambra, CA 91801 · (626) 288-8811 · fax (626) 240-5133 · **`pi.welchandchen@gmail.com`**

## Timeline

| Date | Event |
| --- | --- |
| 09/28 | Welch & Chen email the termination letter + Designation of Attorney to **picase@**; client signed the same day |
| 09/30 | Amos forwards to klaus@; Klaus tells the team to stop work and not contact the client |
| 10/01 | Klaus has Tiana notify the clinic informally |
| 10/05 | Three letters sent; file delivered; Activity Log row A687; Chat posted |

## Traps

**1 — "No contact information" was wrong.** Their letterhead prints only phone and fax, and a web
search for the firm turns up no email. I nearly sent Klaus to phone them. The packet itself had
arrived **by email** from `pi.welchandchen@gmail.com` — buried in a forwarded block, so it was not
in the forwarded message's headers. *Search the mail first.* Now Step 1.

**2 — The 1P claim did not exist.** Intake showed Progressive policy 861253248 with period
**08/17/2026–02/17/2027** against a DOL of **08/15/2026** — the policy incepted *two days after the
loss*. Claim # and adjuster were both "Pending", coverage "Pending", and the case folder held only
a 3P LOR. Klaus confirmed: no 1P. The whole 1P row came out of the successor letter and no 1P
letter was sent. *Always check the 1P policy period against the DOL.*

**3 — Their letter asked four things; the precedents answer two.** Welch & Chen asked for advanced
costs (amount + description) and attorney's fee (amount + itemized basis). Neither the Shuhua Yan
nor the Jinfa Lu letter answers either. Copying the precedent would have left the request hanging.
Final answer: costs stated as **none advanced**; **no fee figure**, lien described as the reasonable
value of services to be determined on resolution.

**4 — I broke the letterhead.** To claw back 3 lines I deleted "blank" paragraphs from
`word/header1.xml`. Those paragraphs position the logo, the gold band, and the black rule — the
header visibly collapsed and Klaus caught it from a screenshot. Restored from the template.
**Never touch header XML.** Shrink only in the body.

**5 — The date was left-aligned.** House rule is centered, on every document, and Klaus had said so
before. Templates default to left, so centering must be an explicit step.
Now [[feedback_letter_date_centered]].

**6 — 25 MB is the *encoded* size.** The zip was 15.4 MB raw, which felt comfortably under — but
base64 inflates by 4/3, so the message was 21.1 MB. It fit, barely. A 19 MB zip would not have.
*Compute `raw × 4/3` before deciding Dropbox vs attachment.*

**7 — Enclosure wording and delivery method desync.** The letter said
`Client file (secure link)` from the Dropbox assumption; once the zip turned out to fit, both the
enclosure line and the email body had to change to match. Decide the delivery method before
finalizing the letter.

**8 — `gws` will not write outside the cwd.** The first recursive download failed on every file
with "resolves to ... which is outside the current directory". Run the mirror from inside the
destination with relative paths.

## Package as delivered

15 files / 15.4 MB zipped. **Excluded at Klaus's direction:** `Jiajun He-8-15-2026 Intake Sheet.xlsx`
and `Intake Responses.zip`.

```
1#Legal Documents/      PI Auto Retainer (New).pdf, LOR - Jiajun He 8-15-2026 (3P).pdf
2#Accident Info/        Police Card, Scene Photos, Vehicle Damage Photos,
                        both parties' DL / plate / insurance cards (9 files)
3#Property Damage/      estimate, supplement, CCC, UP-062526-1830
4#Bodily Injury Claim/  EMPTY  (no medicals were ever ordered)
5#Demand Package/       EMPTY
6#Settlement Documents/ EMPTY
```

The empty folders were left in place so Klaus could diff the package against the live case folder.
**There were no medical records at all** — flagged to him explicitly before sending, since the
letter's "all medical records and bills in this office's possession" reads as if there were some.

## Sent

`klaus@` → `pi.welchandchen@gmail.com`, Cc `picase@lingtulaw.com`, 21.1 MB,
Gmail msg `1a10afda54151360`. Attachments: successor lien letter, Farmers lien notice copy,
`Jiajun He - Client File.zip`.

Drive: `Case Sub` = `1DXn2XiUqQ5fW1dKJ1MDtbZzmFAvBTLvs`
Activity Log row A687.

## Why the Farmers notice went to successor counsel

Klaus asked. The reason is not "the template says so" — it is that **successor counsel, not the
adjuster, decides how the settlement draft gets cut.** Putting the actual carrier notice in their
hands makes the co-payee requirement unavoidable at the moment it matters, and if the fee is later
disputed, "they held the notice" beats "our letter said we had notified the carrier." Nothing in
that letter is adverse to us — no figures, no strategy.

## Still open

Waiting on Welch & Chen's **written confirmation of receipt**. File it in the case folder when it
arrives: it is the only proof we discharged the CRPC 1.16(e)(1) delivery duty, and it is what a
later lien fight will turn on. Keep our own copy of the file until the lien is **resolved and paid**,
not merely until the case settles.
