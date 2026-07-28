# Insurance Directory Lookup

## Source

**Spreadsheet:** PI Master Sheet — ID `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`
**Tab:** `insurance list`
**Range to read:** `insurance list!A1:D200` (columns: Insurance Name, Phone Number, Email, LOR Fax Number)

```bash
gws sheets +read \
  --spreadsheet "1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM" \
  --range "insurance list!A1:D200" \
  --format json > /tmp/insurance_list.json
```

## Matcher

Reuse the fuzzy carrier matcher from the lor-send skill — **do not duplicate it**.

```bash
python3 ~/.claude/skills/lor-send/scripts/match_carrier.py \
  "<insurer name from AIC>" /tmp/insurance_list.json
```

Returns JSON: `{"matched": "<dir name|null>", "fax": "<E.164|null>", "email": "<str|null>"}`

Fax is automatically normalized to E.164 (+1XXXXXXXXXX).

## Column → Cell Mapping

| Directory column | 1P cell | 3P cell | Yellow rule |
|---|---|---|---|
| Phone Number | **I17** | **L21** | No yellow if filled from directory |
| Email | **I18** | **L22** | No yellow if filled (see Mercury below) |
| LOR Fax Number | **I22** | *(no 3P fax cell)* | No yellow if filled |

**I16 (1P PD Adjuster) and L20 (3P PD Adj) always stay "Pending"+yellow — these are
case-specific and cannot be pre-filled from the directory.**

## Lookup Logic

```
1. Read insurance list tab → /tmp/insurance_list.json (cache once; reuse for both 1P + 3P)
2. For each insurer (1P from I5, 3P from L5):
     result = match_carrier.py(insurer_name, /tmp/insurance_list.json)
     if result["matched"]:
         fill phone, email, fax per column mapping above (no yellow)
     else:
         leave "Pending"+yellow (existing behavior)
         note "no directory match for [insurer]" in summary → add to insurance list
```

## Mercury Insurance — Special Email Rule

Mercury's claims email is **claim-number-specific**, not a fixed address:

```
MyClaim+{CAPA-XXXXXXXX}@mercuryinsurance.com
```

Detection: `result["matched"]` contains "mercury" (case-insensitive).

| Claim# at intake time | Write to I18 / L22 | Yellow |
|---|---|---|
| Known (e.g. CAPA-1234567) | `MyClaim+CAPA-1234567@mercuryinsurance.com` | No |
| Unknown / "Pending" | `MyClaim+[CLAIM#]@mercuryinsurance.com` | **Yes** |

When claim# is "Pending", add to the summary:
> ⚠️ Mercury detected — update I18/L22 to `MyClaim+{CAPA#}@mercuryinsurance.com` once claim number is received.

Phone (I17/L21) and fax (I22) still fill normally from the directory (no claim# needed).

## Fallback Behavior

- **No match in directory** → keep "Pending"+yellow; note insurer name in summary so it can be added to the list.
- **Match found but field blank in directory** (e.g. email column empty) → keep "Pending"+yellow for that specific field only; fill any non-blank fields normally.
- **Directory read fails** → skip lookup entirely; keep all contact cells as "Pending"+yellow; note the failure in summary.
