# PM referral email — template & signature

**PM_Referral_Lingtu Law** template (Pain Management — ongoing treatment, same shape as chiro,
NOT a one-time imaging study). Subject + body below; fill the `<...>` slots from the intake +
clinic info. Keep wording exact.

## Subject
```
PM_Referral_Lingtu Law_<Client Name>
```

## Body (plain text — rendered as HTML divs, see SKILL Step 5)
```
Hi Pain Management Office,

Our client(s) sustained injuries in an auto accident and has been referred for pain management evaluation and treatment. Please contact the patient directly to schedule an initial appointment at your earliest availability.

<Type of accident>          ← intake F5 Point of Impact (e.g. "T-bone")
<Date of Loss>              ← intake C2 (MM/DD/YYYY)
<Time>                      ← intake C3 (e.g. "9:00 AM") — omit the line if blank
<Client Name>              ← intake C4 (add position e.g. "(driver)" if known)
<Date of Birth>            ← intake C5
<Phone#>                   ← intake C6
<Address>                  ← intake C7

If the patient(s) is unreachable or misses the appointment, please contact our office immediately so we may assist further.

<SIGNATURE — see below>
```

The seven client lines render as **plain values, no labels** (matching the firm's sent
referrals). Drop any line whose intake value is blank rather than printing an empty line.

PM is **ongoing treatment**, so — unlike an MRI referral — there is **no required study/region
line**. If the user volunteers a specific reason (e.g. "for the low-back injections"), you may add
one short line after the intro, but never invent one.

## Signature — DO NOT compose it; use the sender's configured Gmail signature

The firm has each team member's signature set in Gmail (with logo + footer). **Never write the
signature yourself.** Fetch the **configured signature** of the FROM account and append it
verbatim:
```bash
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-picase GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-picase/credentials.json \
  gws gmail users settings sendAs list --params '{"userId":"me"}' --format json
# -> take sendAs[?].signature (HTML) for the FROM email (e.g. picase@lingtulaw.com)
```
The signature is **HTML** (it embeds the firm logo + "Formerly known as LaShine" + the CCR /
confidentiality footer), so the email **must be sent as HTML**: build a `multipart/mixed`
message = `text/html` body (the content above as `<div>` lines) + the fetched signature HTML +
any attachment. (`build_email.py` is plain-text only — build the HTML MIME inline, see SKILL Step 5.)

Body content lines (everything ABOVE the signature) — compose these; the signature is appended.

## CM directory (signature source)
| CM | ext | direct (D) |
|---|---|---|
| Ryan Wei | 106 | 626-376-9162 |
| Klaus Liu | — | 626-479-2207 |
| Amos Feng | — | 626-598-1129 |
| Jerry Piao | — | 626-598-6352 |

(Full list / future CMs: `references/firm-directory.md`. Add ext numbers there as needed.)
