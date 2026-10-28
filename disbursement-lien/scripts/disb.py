#!/usr/bin/env python3
"""Lingtu Law — disbursement letter + lien reduction letter generator.

Usage:
    python3 disb.py run CASE.json --out DIR [--lien all|none|"Name A,Name B"] [--dis simple|detail|formal|none]

CASE.json (money as numbers; see SKILL.md for the full schema):
{
  "client": "Zhiping Liu", "dol": "1/3/2025", "letter_date": "October 21, 2026",
  "total": 245000.00, "sources": {"3P": 0, "UIM": 245000},
  "fee": 98000.00, "fee_label": "40%", "case_cost": 0, "net": 95770.00,
  "providers": [
    {"name": "TBI Specialists", "lien": 3200.00, "reduced": 1500.00,
     "payee": "Apogee Capital Fund 5, LLC (assignee of TBI Specialists Inc.)",
     "addr1": "614 South Capital of Texas Highway", "csz": "Austin, TX 78746"}
  ],
  "guardian": null,
  "formal": {"claim_no": "...", "carrier": "...", "check_no": "...", "check_date": "..."}
}

Templates are pulled live from Drive (gws) on every run. Nothing is sent anywhere.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from xml.sax.saxutils import escape

DISB_TEMPLATE_ID = "1wLq7KWY26XdO3NnD3BFS86RcMTVukucN"   # Disbursement Letter Template.docx
LIEN_TEMPLATE_ID = "15tADzza9OwXvBVqkNQrXUNkEpZjQvCEY"   # Lien Reduction Template.docx
SOFFICE = shutil.which("soffice") or "/opt/homebrew/bin/soffice"

# Header contact: Klaus direct line, which is VoiceFax -> phone and fax are the same number.
# 626-240-2046 must never appear (claims@ fax-to-email). 626-614-6666 is a personal cell.
PHONE = "(626) 479-2207"

DEPOSIT_CLAUSE = (" Additionally, upon receipt of the settlement check, we kindly ask that your "
                  "office deposit it within thirty (30) days of receipt.")


# ---------------------------------------------------------------- helpers
def money(x):
    return "${:,.2f}".format(x)


def fetch(file_id, dest):
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["gws", "drive", "files", "get", "--params",
                        json.dumps({"fileId": file_id, "alt": "media", "supportsAllDrives": True})],
                       cwd=td, check=True, capture_output=True, text=True)
        files = os.listdir(td)
        if not files:
            raise RuntimeError(f"gws returned nothing for {file_id}")
        shutil.copy(os.path.join(td, files[0]), dest)
    with zipfile.ZipFile(dest) as z:          # must be a real docx
        z.getinfo("word/document.xml")
    return dest


def read_xml(docx, part="word/document.xml"):
    with zipfile.ZipFile(docx) as z:
        return z.read(part).decode("utf-8")


def fix_header(h):
    """Text-only edits inside existing runs. Never adds/removes paragraphs (they hold the logo)."""
    h = re.sub(r'(<w:t[^>]*>)614(</w:t>)', r'\g<1>479\g<2>', h)
    h = re.sub(r'(<w:t[^>]*>)6666(</w:t>)', r'\g<1>2207\g<2>', h)
    h = h.replace("Fax: (626) 240-2046", f"Fax: {PHONE}")
    # Disbursement template has a phone line only: keep it as the template has it, no Fax added
    # (Klaus 2026-10-28: "for disbursement, no need include fax, stick with template").
    plain = re.sub(r'<[^>]+>', '', h)
    assert "240-2046" not in plain and "614" not in plain, "header still carries a forbidden number"
    return h


def write_pdf(template, doc_xml, out_pdf, one_page=False):
    with tempfile.TemporaryDirectory() as td:
        docx = os.path.join(td, "letter.docx")
        with zipfile.ZipFile(template) as zin, zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as zout:
            for it in zin.infolist():
                data = zin.read(it.filename)
                if it.filename == "word/document.xml":
                    data = doc_xml.encode("utf-8")
                elif it.filename.startswith("word/header") and it.filename.endswith(".xml"):
                    data = fix_header(data.decode("utf-8")).encode("utf-8")
                zout.writestr(it, data)
        subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", td, docx],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pdf = os.path.join(td, "letter.pdf")
        if one_page:
            from pypdf import PdfReader, PdfWriter
            r = PdfReader(pdf); w = PdfWriter(); w.add_page(r.pages[0])
            with open(out_pdf, "wb") as f:
                w.write(f)
        else:
            shutil.copy(pdf, out_pdf)
    return out_pdf


def strip_highlights(x):
    return re.sub(r'<w:highlight w:val="yellow"/>\n?', '', x)


def para_bounds(xml, needle):
    i = xml.find(needle)
    assert i >= 0, f"not found: {needle}"
    ps = max(xml.rfind("<w:p ", 0, i), xml.rfind("<w:p>", 0, i))
    pe = xml.find("</w:p>", i) + len("</w:p>")
    return ps, pe


def safe_name(s):
    return re.sub(r'[\\/:*?"<>|.,]', '', s).strip()


# ---------------------------------------------------------------- reconcile
def reconcile(c):
    provs = c.get("providers", [])
    liens = round(sum(p["reduced"] for p in provs if not p.get("exclude_from_dis")), 2)
    c["liens"] = liens
    if c.get("sources"):
        assert abs(sum(c["sources"].values()) - c["total"]) < 0.005, "sources do not add up to total"
    gap = round(c["total"] - c["fee"] - c.get("case_cost", 0) - liens - c["net"], 2)
    if abs(gap) >= 0.005:
        raise SystemExit(f"RECONCILE FAIL: total {money(c['total'])} - fee {money(c['fee'])} - cost "
                         f"{money(c.get('case_cost', 0))} - liens {money(liens)} != net {money(c['net'])} "
                         f"(off by {money(gap)}). Stop and ask which cell governs.")
    return liens


# ---------------------------------------------------------------- lien letter
def lien_letter(c, p, tpl, outdir):
    payee = p.get("payee") or p["name"]
    for k in ("addr1", "csz"):
        if not p.get(k):
            raise SystemExit(f"{p['name']}: missing remit-to {k}. Get the W-9 first.")
    xml = read_xml(tpl)
    if "within thirty (30) days" not in xml:
        xml = xml.replace("contact our office at (626) 614-6666.",
                          "contact our office at (626) 614-6666." + DEPOSIT_CLAUSE)
    for k, v in {"[DATE]": c["letter_date"], "[PROVIDER NAME]": payee,
                 "[PROVIDER ADDRESS LINE 1]": p["addr1"], "[PROVIDER CITY, STATE ZIP]": p["csz"],
                 "[CLIENT NAME]": c["client"], "[DATE OF ACCIDENT]": c["dol"],
                 "[LIEN AMOUNT]": money(p["lien"]), "[PROPOSED AMOUNT]": money(p["reduced"])}.items():
        assert xml.count(k) >= 1, f"lien template missing {k}"
        xml = xml.replace(k, escape(v))
    xml = xml.replace("(626) 614-6666", PHONE)
    # date paragraph centered (house rule)
    ps, pe = para_bounds(xml, escape(c["letter_date"]))
    p_ = re.sub(r'<w:jc w:val="[^"]*"/>', '', xml[ps:pe])
    p_ = p_.replace("<w:pPr>", '<w:pPr><w:jc w:val="center"/>', 1) if "<w:pPr>" in p_ \
        else re.sub(r'(<w:p[^>]*>)', r'\1<w:pPr><w:jc w:val="center"/></w:pPr>', p_, count=1)
    xml = xml[:ps] + p_ + xml[pe:]
    # signature block: Date column at 4.5" so long payee names don't push it out of line
    for m in reversed(list(re.finditer(r'<w:p[ >].*?</w:p>', xml, re.S))):
        t = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', m.group(0)))
        if t.startswith("________________") or t.endswith("Date"):
            q = m.group(0).replace('w:pos="5040"', 'w:pos="6480"')
            q = q.replace("<w:t>" + "_" * 32 + "</w:t>", "<w:t>" + "_" * 50 + "</w:t>", 1)
            xml = xml[:m.start()] + q + xml[m.end():]
    xml = strip_highlights(xml)
    label = p.get("file_name") or re.sub(r"\s*\(.*?\)", "", p["name"]).split(" / ")[0]
    out = os.path.join(outdir, f"{c['client']}-{safe_name(label)} Medical Lien Reduction and Release.pdf")
    return write_pdf(tpl, xml, out)


# ---------------------------------------------------------------- disbursement letter
LABELS = ["TOTAL SETTLEMENT AMOUNT", "ATTORNEY FEE", "MEDICAL LIENS", "CASE COST", "AMOUNT TO CLIENT"]
RT = '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9360"/></w:tabs>'


def fix_alignment(xml):
    for lab in LABELS:
        i = xml.find(lab)
        if i == -1:
            continue
        ps = max(xml.rfind("<w:p ", 0, i), xml.rfind("<w:p>", 0, i))
        pe = xml.find("</w:p>", i) + 6
        para = xml[ps:pe]
        new = re.sub(r"<w:tabs>.*?</w:tabs>", RT, para, count=1, flags=re.S)
        new = re.sub(r'(<w:t[^>]*>)([^<]*)(</w:t>)',
                     lambda m: m.group(1) + m.group(2).rstrip("…. ") + m.group(3), new, count=1)
        tabrun = r'<w:r>(?:(?!</w:r>)[\s\S])*?<w:tab/>(?:(?!</w:r>)[\s\S])*?</w:r>'
        new = re.sub(r'(?:' + tabrun + r'){2,}', '<w:r><w:tab/></w:r>', new)
        xml = xml[:ps] + new + xml[pe:]
    return xml


def row(label, amount="", indent=0, italic=False, bold=False, leader=True):
    rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + \
          '<w:color w:val="000000"/></w:rPr>'
    tabs = RT if leader else '<w:tabs><w:tab w:val="right" w:pos="9360"/></w:tabs>'
    amt = f'<w:r>{rpr}<w:tab/></w:r><w:r>{rpr}<w:t>{escape(amount)}</w:t></w:r>' if amount else ""
    ind = f'<w:ind w:left="{indent}"/>' if indent else ""
    return (f'<w:p><w:pPr><w:spacing w:after="40" w:line="240" w:lineRule="auto"/>{ind}{rpr}{tabs}</w:pPr>'
            f'<w:r>{rpr}<w:t xml:space="preserve">{escape(label)}</w:t></w:r>{amt}</w:p>')


def para(text, bold=False, underline=False, just=True, space_after=120):
    rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + ('<w:u w:val="single"/>' if underline else "") + \
          '<w:color w:val="000000"/></w:rPr>'
    ppr = (f'<w:pPr><w:spacing w:after="{space_after}" w:line="240" w:lineRule="auto"/>'
           + ('<w:jc w:val="both"/>' if just else '') + rpr + '</w:pPr>')
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def total_display(c):
    s = money(c["total"])
    src = {k: v for k, v in (c.get("sources") or {}).items() if v}
    if len(src) > 1:
        s += "  (" + " + ".join(f"{k} {money(v)}" for k, v in src.items()) + ")"
    return s


def dis_letter(c, tpl, outdir, variant="simple"):
    xml = read_xml(tpl)
    LTOK = "[MEDICAL LIENS &amp; CASE COSTS]"
    assert xml.count(LTOK) == 1, "dis template: medical-liens token missing"
    cost = c.get("case_cost", 0) or 0
    provs = [p for p in c.get("providers", []) if not p.get("exclude_from_dis")]
    if not provs and not cost:                                   # nothing to deduct
        ps, pe = para_bounds(xml, LTOK); xml = xml[:ps] + xml[pe:]
    else:
        xml = xml.replace(LTOK, escape(money(c["liens"])))
        ps, pe = para_bounds(xml, "MEDICAL LIENS AND CASE COSTS")
        med = xml[ps:pe].replace("MEDICAL LIENS AND CASE COSTS", "MEDICAL LIENS", 1)
        extra = ""
        if cost:
            extra = xml[ps:pe].replace("MEDICAL LIENS AND CASE COSTS", "CASE COST", 1) \
                              .replace(escape(money(c["liens"])), escape(money(cost)), 1)
        if not provs:
            med = ""
        xml = xml[:ps] + med + extra + xml[pe:]
    client_line = c["client"] if not c.get("guardian") else \
        f"{c['client']} (Minor), by and through Guardian {c['guardian']}"
    for k, v in {"[CLIENT NAME]": client_line, "[DATE OF LOSS]": c["dol"],
                 "[TOTAL SETTLEMENT]": total_display(c), "[ATTORNEY FEE]": money(c["fee"]),
                 "[AMOUNT TO CLIENT]": money(c["net"])}.items():
        assert xml.count(k) >= 1, f"dis template missing {k}"
        xml = xml.replace(k, escape(v))
    xml = fix_alignment(xml)
    xml = xml.replace("ATTORNEY FEE", f"ATTORNEY FEE ({c['fee_label']})", 1)

    if variant in ("detail", "formal") and provs:
        ps, pe = para_bounds(xml, "MEDICAL LIENS")
        block = row("Medical Provider  (original lien → amount paid)", indent=540, italic=True, leader=False)
        for p in provs:
            block += row(f"{p.get('payee_short') or p['name']}   ({money(p['lien'])} → paid)",
                         money(p["reduced"]), indent=540)
        orig = sum(p["lien"] for p in provs)
        block += row("Total original medical billing", money(orig), indent=540)
        block += row("Total reduction negotiated for you", "−" + money(orig - c["liens"]), indent=540)
        xml = xml[:pe] + block + xml[pe:]

    if variant == "formal":
        xml = formalize(xml, c)
    xml = strip_highlights(xml)
    suffix = "Settlement Disbursement Statement" if variant == "formal" else "Disbursement Letter"
    out = os.path.join(outdir, f"{c['client']}-{suffix}.pdf")
    return write_pdf(tpl, xml, out, one_page=(variant != "formal"))


# ---------------------------------------------------------------- formal version
def clauses(c):
    return [
        ("1.  ATTORNEY'S FEES AND COSTS.",
         "The attorney's fee shown above was calculated at the contingency rate set forth in the written "
         "Attorney-Client Fee Agreement you signed at the outset of this matter, and the costs shown above "
         "are the actual costs and expenses advanced by this office on your behalf. You confirm that the fee "
         "and costs shown above are consistent with that Agreement, and that no other fee, cost, or advance "
         "is claimed against your recovery."),
        ("2.  PAYMENT OF THE MEDICAL LIENS ITEMIZED ABOVE.",
         "This office will pay, from the settlement proceeds, only those medical providers and lienholders "
         "itemized above, and only in the reduced amounts itemized above. Each of those reductions was "
         "negotiated by this office and confirmed in writing by the provider. You are not required to pay "
         "those providers any additional amount for the treatment covered by their signed lien reductions."),
        ("3.  LIENS, BILLS, AND REIMBURSEMENT CLAIMS NOT ITEMIZED ABOVE.",
         "You are solely responsible for any medical bill, lien, claim, or right of reimbursement that is not "
         "itemized above, including without limitation: bills from providers not listed; charges incurred "
         "after the date of this statement; claims by any health plan, health insurer, HMO, ERISA plan, "
         "Medi-Cal, Medicare, Tricare, workers' compensation carrier, or other public or private payor; "
         "hospital liens; and any claim asserted by a person or entity of which this office has not been "
         "informed. You acknowledge that (a) you may have a legal duty to notify and reimburse such "
         "lienholders or payors, (b) such lienholders or payors may pursue you directly, and (c) YOU SHOULD "
         "SEEK THE ADVICE OF INDEPENDENT COUNSEL REGARDING ANY SUCH OBLIGATION OR PENALTY UNDER CALIFORNIA "
         "OR FEDERAL LAW. You further agree to indemnify, defend, and hold this office and its attorneys and "
         "staff harmless from any claim, demand, lien, cost, or expense asserted by any provider, payor, or "
         "lienholder that is not itemized above, or that arises from information you did not disclose to "
         "this office."),
        ("4.  YOUR INDEPENDENT DECISION TO SETTLE; NO GUARANTEE.",
         "You decided to accept this settlement voluntarily and of your own free will, after having the "
         "opportunity to ask questions and to consider the risks, costs, delay, and uncertainty of continued "
         "litigation. This office made no promise, guarantee, prediction, or representation to you as to the "
         "amount of any settlement, verdict, or recovery, and you did not rely on any such promise or "
         "guarantee in agreeing to settle or in approving this disbursement."),
        ("5.  THE SETTLEMENT IS FULL, FINAL, AND IRREVOCABLE.",
         "You understand that the settlement of this claim is full, final, and irreversible; that you have "
         f"released the adverse party and its insurer from all claims arising out of the incident of {c['dol']}; "
         "that the claim cannot be reopened, renegotiated, or pursued further for any reason, including if "
         "your injuries prove more serious than presently known or if you later require additional "
         "treatment; and that no further money will be paid to you on account of this incident by any party, "
         "insurer, or by this office."),
        ("6.  FUTURE MEDICAL CARE AND EXPENSES.",
         "Any medical care, treatment, therapy, procedure, or examination you receive after the date of this "
         "statement is your sole financial responsibility, and this office has no obligation to pay for or "
         "arrange it. The decision whether to obtain further care is yours alone, to be made with your own "
         "treating physicians."),
        ("7.  APPROVAL OF THIS ACCOUNTING AND AUTHORIZATION TO DISBURSE.",
         "You have received and reviewed this itemized accounting; you have had a full opportunity to ask "
         "questions about every figure in it and to request any supporting document, including the settlement "
         "check, the provider bills, and each signed lien reduction; every question you asked has been "
         "answered to your satisfaction; and you approve this accounting as accurate and complete. You "
         "authorize and direct this office to disburse the settlement proceeds exactly as set forth above, and "
         "you agree that upon disbursement in accordance with this statement, this office has fully accounted "
         "for and properly distributed all settlement funds received in this matter, and you will make no "
         "further claim against this office with respect to the receipt, accounting, or distribution of those "
         "funds."),
        ("8.  YOUR RIGHT TO INDEPENDENT COUNSEL.",
         "You have been advised, and you acknowledge, that you have the right to consult independent counsel "
         "of your own choosing, at your own expense, regarding this settlement, this accounting, and your "
         "rights and obligations, before signing this statement. You have had a reasonable opportunity to do "
         "so, and you sign this statement either after having consulted such counsel or having freely chosen "
         "not to."),
        ("9.  NO TAX, PUBLIC-BENEFIT, OR FINANCIAL ADVICE.",
         "This office has not given you tax, accounting, immigration, or public-benefit advice, and gives none "
         "here. Settlement proceeds may affect your income taxes or your eligibility for needs-based public "
         "benefits such as Medi-Cal, SSI, or subsidized housing. You should consult your own tax advisor or "
         "benefits counselor regarding these consequences."),
        ("10.  CONCLUSION OF REPRESENTATION.",
         "Upon disbursement of the funds as set forth above, this office's representation of you in this "
         "matter is concluded, and this office will have no further duty to you with respect to this claim, "
         "including no duty to monitor deadlines, respond to providers, or pursue any additional recovery. "
         "Your file will be closed and maintained, and thereafter destroyed, in accordance with this office's "
         "ordinary file-retention policy and applicable law. You may request a copy of your client file at "
         "any time before it is destroyed."),
        ("11.  ENTIRE UNDERSTANDING AS TO THIS DISBURSEMENT.",
         "This statement, together with your written Attorney-Client Fee Agreement, sets out the entire "
         "understanding between you and this office as to the amount and manner of the disbursement of these "
         "settlement proceeds. No oral statement by anyone modifies it. If any provision of this statement is "
         "held unenforceable, the remaining provisions remain in full force and effect."),
    ]


def formalize(xml, c):
    f = c.get("formal") or {}
    paras = list(re.finditer(r'<w:p[ >].*?</w:p>', xml, re.S))
    txt = [''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', m.group(0))) for m in paras]
    i0 = next(i for i, t in enumerate(txt) if "ATTORNEY FEES AND REIMBURS" in t)
    i1 = next(i for i, t in enumerate(txt) if "I HAVE READ, UNDERSTAND" in t)
    body = para("The following is an itemized statement of the disbursement of the settlement proceeds "
                "recovered in this matter, provided to you in accordance with the California Rules of "
                "Professional Conduct, rule 1.15, and your written Attorney-Client Fee Agreement. Please read "
                "every paragraph carefully before you sign.")
    for hd, b in clauses(c):
        body += para(hd, bold=True, just=False, space_after=40) + para(b)
    body += '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
    body += para("AUTHORIZATION AND APPROVAL OF CLIENT", bold=True, underline=True, just=False, space_after=80)
    body += para(f"Client: {c['client']}          Date of Loss: {c['dol']}          "
                 f"Net Amount Payable to Client: {money(c['net'])}", just=False)
    body += para("I HAVE READ, UNDERSTAND, AND AGREE TO THE FOREGOING SETTLEMENT DISBURSEMENT STATEMENT, "
                  "INCLUDING PARAGRAPHS 1 THROUGH 11 ABOVE. I CONFIRM THAT THE FIGURES SET FORTH ABOVE ARE "
                  "CORRECT AND THAT I APPROVE THEM. I AUTHORIZE AND DIRECT THE LAW OFFICE OF SHENQI CAI, APC "
                  "(LINGTU LAW OFFICE) TO DISBURSE THE SETTLEMENT PROCEEDS EXACTLY AS SET FORTH ABOVE. I "
                  "FURTHER ACKNOWLEDGE THAT MY ATTORNEY HAS ADVISED ME TO SEEK INDEPENDENT COUNSEL, IF I SO "
                  "CHOOSE, REGARDING MY RIGHTS AND OBLIGATIONS BEFORE SIGNING, AND THAT I SIGN THIS STATEMENT "
                  "FREELY AND VOLUNTARILY.")
    xml = xml[:paras[i0].start()] + body + xml[paras[i1].end():]
    head = ""
    for lab, key in (("CLAIM NO.", "claim_no"), ("SETTLING CARRIER", "carrier")):
        if f.get(key):
            head += para(f"{lab}: {f[key]}", just=False, space_after=0)
    if f.get("check_no"):
        head += para(f"SETTLEMENT CHECK: No. {f['check_no']}, dated {f.get('check_date', '')}, in the amount "
                     f"of {money(c['total'])}", just=False, space_after=0)
    head += para(f"DATE OF THIS STATEMENT: {c['letter_date']}", just=False, space_after=80)
    ps, pe = para_bounds(xml, "DATE OF LOSS:")
    return xml[:pe] + head + xml[pe:]


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "check"])
    ap.add_argument("case")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lien", default="all", help='all | none | "Name A,Name B" (matches provider name)')
    ap.add_argument("--dis", default="simple", choices=["simple", "detail", "formal", "none"])
    a = ap.parse_args()
    c = json.load(open(a.case))
    liens = reconcile(c)
    print(f"RECONCILE OK  total {money(c['total'])} - fee {money(c['fee'])} - cost "
          f"{money(c.get('case_cost', 0))} - liens {money(liens)} = net {money(c['net'])}")
    if a.cmd == "check":
        return
    os.makedirs(a.out, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        lt, dt = os.path.join(td, "lien.docx"), os.path.join(td, "disb.docx")
        if a.lien != "none":
            fetch(LIEN_TEMPLATE_ID, lt)
            wanted = None if a.lien == "all" else [w.strip().lower() for w in a.lien.split(",")]
            for p in c.get("providers", []):
                if wanted and not any(w in p["name"].lower() for w in wanted):
                    continue
                if a.lien == "all" and p.get("reduced_color") == "green":
                    print(f"SKIP lien  {p['name']}: reduced cell is green (already agreed)")
                    continue
                if p.get("skip_lien") or abs(p["reduced"] - p["lien"]) < 0.005:
                    print(f"SKIP lien  {p['name']}: {p.get('skip_lien') or 'no reduction'}")
                    continue
                if not (p.get("addr1") and p.get("csz")):
                    print(f"STOP lien  {p['name']}: no W-9 / remit-to address. Request the W-9 first.")
                    continue
                print("WROTE", lien_letter(c, p, lt, a.out))
        if a.dis != "none":
            open_ = [p["name"] for p in c.get("providers", [])
                     if not p.get("exclude_from_dis") and p.get("reduced_color") not in (None, "", "green")]
            if open_:
                print(f"WARNING dis is PROVISIONAL — reductions not yet agreed (not green): {', '.join(open_)}")
            fetch(DISB_TEMPLATE_ID, dt)
            print("WROTE", dis_letter(c, dt, a.out, a.dis))


if __name__ == "__main__":
    main()
