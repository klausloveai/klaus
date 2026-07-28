#!/usr/bin/env python3
"""Fill the "Withdrawal of Representation" .docx template (no dependencies).

This template marks its blanks with LITERAL yellow-highlighted placeholder text
(NOT [bracketed] tokens like the LOR/LOP templates). The placeholders are each a
clean single run, so direct string replacement on word/document.xml is safe as
long as longer placeholders are replaced before shorter substrings.

Placeholders replaced:
  "Client Name"        -> client name(s); for multiple clients the caller joins
                          them with "and" (e.g. "Fan Bi and Yulin Yuan", or
                          "A, B and C"). Salutation only — no recipient address block.
  "DOL"                -> date of loss, MM/DD/YYYY
  "DOL Plus 2 Year"    -> SOL deadline = DOL + sol_years, MM/DD/YYYY
  "Teamemail"          -> the case's owning team mailbox (e.g. picase@lingtulaw.com)
  DATE field cache     -> stamped to today ("Month D, YYYY")

Statute-of-limitations text (California-general by default; changed for out-of-state).
The wording and the deadline ALWAYS stay in sync — pass sol_years AND the matching
sol_words (e.g. Minnesota -> sol_years=6, sol_words="six years"):
  "Under California law"            -> "Under <state> law"
  "two years"                       -> "<sol_words>"

Two structural edits are also applied so the output matches the firm's preferred
layout (the Drive template is tighter / signed differently than the desired letter):
  * a blank line is inserted before each body paragraph (Dear ... / Please ... /
    Important Notice ... / Your complete file ... / Yours sincerely);
  * the "Shenqi Cai, Esq." signature line is removed, leaving only "Lingtu Law Office".

The yellow highlight is stripped after filling so the finished letter is clean.

Usage:  python3 fill_withdrawal.py <template.docx> <out.docx> <fields.json>

fields.json:
  {
    "client":    "Fan Bi and Yulin Yuan", # one name, or several joined with "and"
    "dol":       "05/21/2026",            # raw MM/DD/YYYY from the intake sheet
    "sol_years": 2,                        # integer; 2 for CA, else the state's PI SOL
    "state":     "California",             # governing state for the SOL sentence
    "sol_words": "two years",              # word form of sol_years (MUST match)
    "teamemail": "picase@lingtulaw.com"    # the case's owning team mailbox
  }
After filling, the script verifies no placeholder text remains and exits non-zero
if any is left (so the skill never produces a half-filled letter).
"""
import sys, json, re, html, zipfile, datetime

# Body paragraphs that should each be preceded by a blank line.
SPACING_MARKERS = (
    "Please be advised",
    "Important Notice Regarding",
    "Your complete file",
    "Yours sincerely",
)
PARA_RE = r"<w:p[ >].*?</w:p>"   # one paragraph (paragraphs never nest)


def norm_date(mdy):
    """'5/21/2026' or '05/21/2026' -> zero-padded 'MM/DD/YYYY'."""
    m, d, y = [int(x) for x in re.split(r"[/\-]", mdy.strip())]
    return "%02d/%02d/%04d" % (m, d, y)


def add_years(mdy, n):
    """DOL + n years, MM/DD/YYYY (Feb 29 -> Mar 1 fallback)."""
    m, d, y = [int(x) for x in re.split(r"[/\-]", mdy.strip())]
    base = datetime.date(y, m, d)
    try:
        end = base.replace(year=y + n)
    except ValueError:
        end = base.replace(year=y + n, month=3, day=1)
    return "%02d/%02d/%04d" % (end.month, end.day, end.year)


MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")


def stamp_today(xml):
    """Stamp the letter date to today.

    The template's letter date has appeared in two forms as the firm edits it:
    (1) a live Word DATE field (cached value goes stale on Drive PDF conversion), and
    (2) plain static text like "June 24, 2026". Handle both:
      * update a DATE field's cached separate-value, and
      * replace any spelled-out "Month D, YYYY" date (the letter date is the only such
        date — DOL and the deadline render as MM/DD/YYYY), so a flattened static date is
        refreshed too.
    """
    today = datetime.date.today().strftime("%B %-d, %Y")
    # (1) live DATE field, if present
    pat = re.compile(
        r'(<w:instrText[^>]*>\s*DATE[^<]*</w:instrText>.*?'
        r'<w:fldChar[^>]*w:fldCharType="separate"[^>]*/>)(.*?)'
        r'(<w:fldChar[^>]*w:fldCharType="end"[^>]*/>)', re.S)
    def repl(m):
        mid = re.sub(r'(<w:t[^>]*>)[^<]*(</w:t>)',
                     lambda t: t.group(1) + html.escape(today) + t.group(2),
                     m.group(2), count=1)
        return m.group(1) + mid + m.group(3)
    xml = pat.sub(repl, xml, count=1)
    # (2) plain static spelled-out date
    xml = re.sub(r'(?:' + MONTHS + r') \d{1,2}, \d{4}', html.escape(today), xml)
    return xml


def _para_text(p):
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))


def add_paragraph_spacing(xml):
    """Insert an empty paragraph before each body paragraph so the letter reads with
    a blank line between paragraphs (the Drive template renders them tight)."""
    def repl(m):
        p = m.group(0)
        t = _para_text(p).lstrip()
        if any(t.startswith(mk) for mk in SPACING_MARKERS):
            return "<w:p/>" + p
        return p
    return re.sub(PARA_RE, repl, xml, flags=re.S)


def remove_signature_line(xml, needle="Cai, Esq."):
    """Drop the paragraph containing the attorney signature line, leaving only the
    firm name ('Lingtu Law Office')."""
    def repl(m):
        return "" if needle in _para_text(m.group(0)) else m.group(0)
    return re.sub(PARA_RE, repl, xml, flags=re.S)


def main():
    if len(sys.argv) != 4:
        sys.exit("usage: fill_withdrawal.py <template.docx> <out.docx> <fields.json>")
    src, out, fields_path = sys.argv[1], sys.argv[2], sys.argv[3]
    f = json.load(open(fields_path, encoding="utf-8"))

    client    = str(f["client"]).strip()
    dol_fmt   = norm_date(f["dol"])
    sol_years = int(f.get("sol_years", 2))
    deadline  = add_years(f["dol"], sol_years)
    state     = str(f.get("state", "California")).strip()
    sol_words = str(f.get("sol_words", "two years")).strip()
    teamemail = str(f["teamemail"]).strip()

    # Order matters: replace the longer "DOL Plus 2 Year" before the "DOL" substring,
    # and apply the SOL-sentence edits (no-ops for a California case).
    replacements = [
        ("DOL Plus 2 Year", deadline),
        ("DOL", dol_fmt),
        ("Client Name", html.escape(client)),
        ("Teamemail", html.escape(teamemail)),
        ("Under California law", "Under " + html.escape(state) + " law"),
        # "two years" is its own run (the words before it live in a separate run),
        # so the SOL period must be replaced on its own, not as part of a longer phrase.
        ("two years", html.escape(sol_words)),
    ]

    zin = zipfile.ZipFile(src)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                x = data.decode("utf-8")
                for needle, value in replacements:
                    x = x.replace(needle, value)
                x = re.sub(r'<w:highlight w:val="yellow"\s*/>', "", x)
                x = stamp_today(x)
                x = add_paragraph_spacing(x)
                x = remove_signature_line(x)
                data = x.encode("utf-8")
            zout.writestr(item, data)

    # Verify nothing was left unfilled (visible text only).
    body = zipfile.ZipFile(out).read("word/document.xml").decode("utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", "", body))
    leftovers = [p for p in ("Client Name", "DOL Plus 2 Year", "DOL", "Teamemail")
                 if p in text]
    if leftovers:
        sys.exit("ERROR: unfilled placeholders remain: " + ", ".join(sorted(set(leftovers))))
    print("OK: filled ->", out)
    print("   client   :", client)
    print("   DOL      :", dol_fmt)
    print("   state    :", state, "(SOL " + str(sol_years) + "y =", sol_words + ")")
    print("   deadline :", deadline)
    print("   teamemail:", teamemail)


if __name__ == "__main__":
    main()
