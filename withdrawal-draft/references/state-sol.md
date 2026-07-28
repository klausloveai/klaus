# Statute of Limitations (personal injury) — by state

This letter warns the client of the deadline to file their own PI lawsuit. The
governing state is **where the accident happened** (intake `F2` Accident Location),
not necessarily where the client lives.

## California (default)
- PI SOL = **2 years** (Code Civ. Proc. § 335.1). `sol_years=2`, `sol_words="two years"`,
  `state="California"`. No template SOL edits needed — the template is California-general.

## Out-of-state — ALWAYS web-search to confirm before drafting
PI statutes of limitations change (legislatures amend them; some states differ for
motor-vehicle vs. general PI). **Do not rely on memory or a static table.** For any
non-California accident:

1. `WebSearch` e.g. `"<state> personal injury statute of limitations 2026 car accident"`.
2. Confirm the current period (years) from an authoritative source (state code or a
   reputable legal summary). Note any motor-vehicle-specific rule.
3. Set `sol_years` (integer), `sol_words` (e.g. `"three years"`), `state` (e.g. `"Texas"`).
   **`sol_words` MUST match `sol_years`** — the sentence ("you generally have <sol_words>")
   and the deadline ("DOL + sol_years") have to agree. Don't leave the wording at "two
   years" when the period isn't two years.
4. Compute deadline = DOL + sol_years (the fill script does this) and **surface the
   state, period, source, and computed deadline in your summary, flagged for attorney
   confirmation** before the letter goes out.

### Confirmed examples (still re-verify)
- **Minnesota** = **6 years** (Minn. Stat. § 541.05) → `sol_years=6`, `sol_words="six years"`.

### Rough starting points (VERIFY each time — may be outdated)
Most states are 2 or 3 years. Common shorter ones: Kentucky, Louisiana, Tennessee
(historically ~1 year, several recently amended). Longer: Maine, Missouri, North Dakota,
Nebraska, Utah, Wyoming (4–6 years). These are hints for sanity-checking the search
result — never the final value.

The template itself hedges ("This deadline may be shorter depending on the specific
facts of your case. You should consult with another attorney promptly to confirm…"),
but the stated deadline must still be the firm's best good-faith figure.
