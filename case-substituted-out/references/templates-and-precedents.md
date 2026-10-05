# Templates and precedents

## Templates (Drive)

| File | Drive ID | Notes |
| --- | --- | --- |
| `Notice of Attorney Lien - 1st Party Insurance.docx` | `1sdLmiuckOA3KlrSkTr-uG7LLvQbY1UsV` | adds a UM/UIM + med-pay sentence the 3P version lacks |
| `Notice of Attorney Lien - 3rd Party Insurance.docx` | `1KQ1X6kEvvtVUF4HEH868qTv0Z1lUnU3M` | has a `Your Insured` row the 1P version lacks |
| `Notice of Attorney Lien - Successor Attorney.docx` | `1JqY8Mfro1sQBm64FQoGMQQtvv1EyOyrI` | the long one; ships as 7 body paragraphs |
| `Sub Out Letter to Attorney Asserting Lien.pdf` | `1dWTiubFWi9ue5OO0f2WJg576nvNV_guT` | **older generation — check before using.** The .docx above supersedes it |

There is **no provider template.** Derive it from the 3P file (SKILL.md Step 5).

## Fill slots

Both carrier templates:

```
Month Day, Year          adjuster@carrier.com     Carrier Name
Adjuster Name  (x2: the Attn: line and the Dear line)
Client Name    Insured Name (3P only)   MM/DD/YYYY
Policy Number  Claim Number
New Firm Name  New Firm Address  (###) ###-####
teamemail@lingtulaw.com
```

Successor template:

```
Month Day, Year   (x3: letter date / their letter's date / retainer execution date)
info@newfirm.com  New Firm Name  Attorney Name  Street Address  City, State ZIP
Client Name  MM/DD/YYYY
Carrier (x2: 1P then 3P)   Claim Number (x2: 1P then 3P)
Mr./Ms. Client  (x3 -- only the first is a yellow slot; the other two are inside
                 body paragraphs, so patch them with set_para or a text replace)
1P Carrier / 3P Carrier  (inside the "Notice of this lien has been given to ..."
                 sentence AND the Enclosure line -- these span runs, so they will
                 NOT match a run-level fill. Use set_para.)
teamemail@lingtulaw.com
```

⚠️ `Policy Number` and `Claim Number` each appear **twice** — once as the plain label run and
once as the yellow value run. Filling by text match alone swaps them. `fill_letter.Letter.fill`
only touches yellow runs, which is what makes this safe.

## Prior sub-outs (read these before drafting)

| Case | Successor firm | What it shows |
| --- | --- | --- |
| **Shuhua Yan** | CK Law (Christie Kim) | the fullest set — 1P Mercury + 3P Farmers + successor; includes the "letter went to our general info address" paragraph and the `Complete client file (transmitted by secure electronic link)` enclosure line |
| **Jinfa Lu** | J. Jay Chang | 1P Tesla Insurance + successor |
| **Chaoli Ding** | — | 1P + 3P + attorney |
| **Shufen Dong** | — | 1P + 3P + attorney |
| **Jiajun He** (2026-10) | Welch & Chen | 3P only (no 1P existed) + provider; zip attached instead of a link. See the worked example |

House style confirmed across all of them:

- `Dear John Grier:` — bare full name, no honorific
- letterhead uses the **general** office line (888-343-9794) and general fax (626-323-8181),
  not the CM's direct line (that rule is for *forms*, see [[feedback_form_firm_phone_cm]])
- signature block: `LAW OFFICE OF SHENQI CAI, APC` — **never** "d/b/a Lingtu Law Office"
  (the firm has no registered DBA; the Lingtu letterhead logo is fine)
  [[feedback_no_dba_lingtu]]
- **no costs figure and no fee figure** appears in any precedent letter. That is a gap, not a
  rule — if the other firm asked in writing, answer (SKILL.md Step 6)

## Known defect in the signed retainers

PI auto retainers executed through at least 2026-10 contain
`Law Office of Shenqi Cai, APC D/B/A Lingtu Law Office` in the opening paragraph. The firm has
**never registered a DBA**. Executed copies cannot be changed, and one goes to successor counsel
in every sub-out. Flag it to Klaus when it comes up; the template fix is tracked separately.
