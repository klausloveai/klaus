---
name: "template"
description: "Build a reusable Fixed(firm-standing-data)/Flexible(client-specific-data) template for a recurring paperwork or form-filling workflow at Lingtu Law / SIA 高徒, and store the master copy in the matching case-type folder under \"0. Template\" → \"1. Initial\" so future cases reuse it. Use this whenever the user asks to \"整理成 template\", \"把这个流程做成模板\", generalize a one-off case's data-gathering into something reusable, or says a workflow should become \"Universal\" — not just for I-131 (see the `case` skill for that concrete instance), but for any case type this firm handles where the same forms get filled repeatedly with mostly-the-same firm data and a few client-specific facts."
---

# Building a Fixed/Flexible data template

This skill is about the *method*, not any one case type. It's how the `case`
skill's own Fixed/Flexible template (`I-131 材料信息模板`) got built, and the
same method applies to any other recurring filing this firm does — G-28-heavy
petitions, other USCIS forms, anything with a firm-standing part and a
client-specific part.

## The core idea

Every recurring paperwork workflow splits into two kinds of data:

- **Fixed** — the firm's own standing information (attorney name, bar number,
  firm address, bank account for ACH, etc.). Identical on every case of this
  type. Collect it once, write it down, never re-derive it.
- **Flexible** — whatever's specific to *this* client and *this* case. Always
  different. Has to come from that case's actual intake materials every time.

A template that only separates these two isn't enough on its own — the
valuable part is pinning *exactly where each Flexible fact goes* (which
document, which page, which section/part, which item number). Without that,
next time still means re-opening every form and re-figuring out the mapping.
With it, filling a new case becomes: read the client's facts, look each one
up in the template, paste into the named location. That's the whole point.

## Step 1 — Learn from a real reference example, not from guessing

The single most reliable way to learn what's Fixed is to get an **actual
completed instance** of the same paperwork from a previous, real case — not
to ask the user to enumerate the firm's standing data from memory, and not to
assume plausible-looking values. Real filed examples surface things nobody
would think to state up front: which checkbox the firm actually picks when a
form's own blank-template default turns out to be wrong, which of two
identically-named-looking fields is the one that's actually used, formatting
conventions (plain digits vs. formatted phone numbers), and so on.

If the user doesn't hand you one unprompted, ask for one, or search the
firm's Drive for a prior filled/signed example of the same document before
asking the user to supply values directly. A firm-wide Drive search by form
name or "sample" often turns up exactly this. When you get one:

- Compare it field-by-field against a blank copy of the same form.
- Whatever's identical to what you'd expect on a *different* client's version
  of the same form (attorney info, firm address, bar number, bank account,
  boilerplate checkbox choices) is **Fixed** — record it once.
- Whatever's clearly that-client's-own-fact (name, dates, numbers, addresses)
  is **Flexible** — note where it goes, not what value it had.
- Anything ambiguous (a checkbox whose "right" answer isn't obvious from the
  form alone) — the real example is the tiebreaker. If the real example
  contradicts a blank template's own default, trust the real example; it
  reflects what actually got filed, and note the discrepancy so it doesn't
  get silently reintroduced later.

## Step 2 — Concretize every Flexible item's destination

For each Flexible fact, write down every place across every document in the
workflow where it's needed — a single fact like "client's phone number" often
feeds several different forms and even more than one spot within the same
form. Use the concrete format: **document name → page number → Part/Section
→ Item number**. This is what makes the difference between a template that
merely lists what to collect and one that actually speeds up the next case —
the goal is that filling becomes direct lookup-and-paste, not re-deriving
structure from scratch.

Call out anything non-obvious you discover while doing this: fields whose
internal name doesn't match their visual position, fields that silently
truncate certain input formats, choice fields that need an exact string
match against a fixed options list, checkboxes whose group members aren't
where their internal ordering suggests. Future-you (or whoever fills the next
case) needs the trap explained, not just the correct value.

## Step 3 — Write the template with two clearly separated sections

- **Section 1: Fixed.** The firm's standing data, as a flat list — name,
  address, phone, license/bar numbers, bank details, whatever's relevant to
  this document set. State clearly that it's reused identically every case.
- **Section 2: Flexible.** One entry per client-fact, each annotated with
  every concrete destination from Step 2. Group related facts together
  (basic bio, contact info, address, case-specific facts, fees) rather than
  listing them in arbitrary form order — the person filling this out later is
  thinking in terms of "what do I know about this client," not "what's field
  47."
- Optionally, a short materials checklist at the end for what source
  documents to pull each Flexible fact from.

## Step 4 — Store it so it actually gets reused

Store one copy — a blank master in the template library (`0. Template` →
`{case-type folder}` → `1. Initial`), with the Flexible section left blank
(or with instructional placeholders). This is the single source of truth for
this case type going forward.

Don't hand-create a second, case-specific copy — the `it` skill's own
Step 6 already copies every file sitting in the matching template subfolder
into each new case's corresponding subfolder when the case is set up, so a
copy lands in that case's `1. Initial` automatically. Once it's there, fill
in its Flexible section with that client's actual facts — it becomes the
working reference for filling out the forms for this specific case, not a
separate "material summary" doc. If a case's `1. Initial` doesn't yet have
a copy (e.g. it was set up before this template existed), copy it over
yourself rather than skipping this step.

## Step 5 — Treat it as living, not a one-time artifact

When a bug or correction surfaces later (wrong field mapping, a formatting
rule that turns out to truncate input, a checkbox that should've been
checked and wasn't), fix it in the template immediately — both the master
copy in the template library and, if relevant, the field-location reference
used by whatever skill fills these forms. The template's value compounds
only if it stays accurate; a stale template that still has last year's wrong
assumption in it is worse than no template, since it looks authoritative.

## Applying this beyond I-131

The `case` skill is the concrete result of running this process once, for
I-131 + G-28 + G-1145 + G-1650. To do the same for a different case type at
this firm: find (or ask for) a real filed example of that case type's forms,
walk Steps 1–5 above, and produce that case type's own Fixed/Flexible
template plus (if the fill-mechanics are novel enough to be worth capturing)
a sibling skill documenting the forms' field maps the way `case`'s field map
appendix does for I-131's four forms.

