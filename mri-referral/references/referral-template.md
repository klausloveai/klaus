# MRI referral email — template & signature

**MRI_Referral_Lingtu Law** template (imaging study, not ongoing treatment). Subject + body
below; fill the `<...>` slots from the intake + clinic info + the ordered study. Keep wording exact.

## Subject
```
MRI_Referral_Lingtu Law_<Client Name>
```

## Body (plain text — rendered as HTML divs, see SKILL Step 5)
```
Hi Imaging Center,

Our client(s) sustained injuries in an auto accident and has been referred for MRI imaging. Please contact the patient directly to schedule the study at your earliest availability.

<Study / region(s) to image>   ← e.g. "MRI cervical spine without contrast" / "MRI L-spine + C-spine" — confirm in Step 3
<Type of accident>          ← intake F5 Point of Impact (e.g. "T-bone")
<Date of Loss>              ← intake C2 (MM/DD/YYYY)
<Time>                      ← intake C3 (e.g. "9:00 AM") — omit the line if blank
<Client Name>              ← intake C4 (add position e.g. "(driver)" if known)
<Date of Birth>            ← intake C5
<Phone#>                   ← intake C6
<Address>                  ← intake C7

We will provide the referring physician's order separately if required. If the patient(s) is unreachable or misses the appointment, please contact our office immediately so we may assist further.

<SIGNATURE — see below>
```

The study line goes FIRST, then the client lines render as **plain values, no labels** (matching
the firm's sent referrals). Drop any line whose value is blank rather than printing an empty line.

**The study/region is REQUIRED for an MRI referral** (the imaging center needs to know what to
scan). If the user didn't state it, derive a proposal from the intake injury regions (e.g. neck
pain → cervical spine, low-back pain → lumbar spine) and **confirm it in Step 3** — never guess
silently. If you can't determine a region, pause and ask.

## Signature — DO NOT compose it; use the sender's configured Gmail signature

The firm has each team member's signature set in Gmail (with logo + footer). **Never write the
signature yourself.** Fetch the **configured signature** of the FROM account and append it
verbatim:
```bash
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=$HOME/.config/gws-picase GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=$HOME/.config/gws-picase/credentials.json \
  gws gmail users settings sendAs list --params '{"userId":"me"}' --format json
# -> take sendAs[?].signature (HTML) for the FROM email (e.g. picase@lingtulaw.com)
```
The signature is **HTML** (logo + "Formerly known as LaShine" + CCR / confidentiality footer), so
the email **must be sent as HTML**: build a `multipart/mixed` message = `text/html` body (the
content above as `<div>` lines) + the fetched signature HTML + any attachment. (`build_email.py`
is plain-text only — build the HTML MIME inline, see SKILL Step 5.)

## CM directory (signature source)
| CM | ext | direct (D) |
|---|---|---|
| Ryan Wei | 106 | 626-376-9162 |
| Klaus Liu | — | 626-479-2207 |
| Amos Feng | — | 626-598-1129 |
| Jerry Piao | — | 626-598-6352 |

(Full list / future CMs: `references/firm-directory.md`. Add ext numbers there as needed.)
