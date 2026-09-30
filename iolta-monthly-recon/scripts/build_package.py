#!/usr/bin/env python3
"""
Build the State Bar reconciliation package for one month of IOLTA #3618.

    python3 build_package.py --month 2026-06 --bank-end 1049028.91 \
        [--stmt-pdf "/path/eStmt.pdf"] [--stmt-csv "/path/stmt.csv"] [--dry-run]

Produces, in `Monthly Reconciliations/<YYYY-MM> State Bar Package/`, the six attachments
Rule 1.15 Standard (1)(d) calls for plus the reconciliation form, and verifies
    line 1 (journal) == line 2 (client ledgers) == line 3 (bank + in-transit - outstanding)
to the cent before it writes anything. It never plugs a difference: if the three do not
agree it prints the gap and exits non-zero.
"""
import argparse, calendar, datetime, json, os, re, shutil, sys
from collections import defaultdict

try:
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
except ImportError:
    sys.exit("need openpyxl:  pip3 install openpyxl")

BASE = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/"
                          "Lingtu Law-Disbursement/IOLTA#3618/")
OLD  = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/"
                          "Lingtu Law-Disbursement/IOLTA #4854/Account#4854-Journal-Reconciled.xlsx")
MR   = BASE + "Monthly Reconciliations/"
DISB_ID = "1Av8_fj3MAekCM6RujmGWuFsYRnSG6MMbAskvPkFcs2U"
MONEY = "#,##0.00_);(#,##0.00)"

# Client-name variants that are the SAME person. Each merge was verified by the fee
# identity (settlement - client - liens - 1/3 fee == 0). Never add one without that proof.
MERGE = {
    'Chih-Ming Huang':'Chih Ming Huang', 'Renjie Zhuo (& Quin Zhong)':'Renjie Zhuo',
    'Xiaohua Yu & Rouwen Lin':'Xiaohua Yu', 'Yuran N Zhou':'Yuran Zhou',
    'Christin Vivian Liu':'Christina Vivian Liu', 'Chunling Shum':'Chunling Shun',
    'Chloe Sha':'Chloe Sha (minor)', 'Rabia Bai':'Rabia Bai (minor)',
    'Haoming Qian':'Haoming Qian (minor)', 'Sung Park':'Sung Park (minor)',
    'Rongrong Hu':'Rongrong He', 'Bole Wang':'Beini Wang', 'Jun Li':'Jiayi Li',
    'Junfeng Zhao':'Jianfeng Zhao', 'Liang Huang':'Lirong Huang', 'Yajing Li':'Yining Li',
    'Yuncheng Wu':'Yanzhong Wu',
    'Danny Qin (erroneous dup of 80089 — refund pending)':'Danny Qin',
}
norm = lambda c: MERGE.get(str(c).strip(), str(c).strip())
num  = lambda v: v if isinstance(v, (int, float)) else 0.0
def f(v):
    if isinstance(v, datetime.datetime): return v.strftime("%m/%d/%Y")
    return "" if v is None else str(v)

# ---------------------------------------------------------------- sources
def load_journal():
    ws = openpyxl.load_workbook(BASE + "Account-Journal.xlsx", data_only=True)["Account journal"]
    last = 9
    for r in range(10, ws.max_row + 1):
        if any(ws.cell(r, c).value is not None for c in range(1, 15)): last = r
    return ws, last

def issued(ws, r):
    d = ws.cell(r, 1).value
    if isinstance(d, datetime.datetime): return d.date()
    blob = f(ws.cell(r, 5).value) + " " + f(ws.cell(r, 10).value)
    m = re.search(r"check (\d{1,2})/(\d{1,2})/(\d{4})", blob) or re.search(r"\((\d{1,2})/(\d{1,2})/(\d{4})\)", blob)
    return datetime.date(int(m.group(3)), int(m.group(1)), int(m.group(2))) if m else None

def cleared(ws, r):
    c = ws.cell(r, 13).value
    return c.date() if isinstance(c, datetime.datetime) else None

def load_disbursements():
    """Disbursement Sheet `Internal ` tab -> [(date, client, fee+cost)]."""
    import subprocess
    out = subprocess.run(
        ["gws", "sheets", "spreadsheets", "values", "get", "--params",
         json.dumps({"spreadsheetId": DISB_ID, "range": "Internal !A1:R400",
                     "valueRenderOption": "UNFORMATTED_VALUE"})],
        capture_output=True, text=True).stdout
    j = json.loads(out[out.index("{"):])
    ser = lambda s: (datetime.date(1899,12,30) + datetime.timedelta(days=int(s))) \
                    if isinstance(s,(int,float)) and s > 1000 else None
    rows = []
    for r in j["values"][2:]:
        r = list(r) + [""] * 18
        nm = norm(r[1]);  dt = ser(r[0])
        if not nm or nm == "Template" or not dt: continue
        fee  = float(r[10]) if isinstance(r[10], (int, float)) else 0.0
        cost = float(r[11]) if isinstance(r[11], (int, float)) else 0.0
        rows.append((dt, nm, fee, cost))
    return rows

def carryover(disb):
    """Per-client #4854 carryover = their #4854 remainder less fees swept before 5/1."""
    w4 = openpyxl.load_workbook(OLD, data_only=True)["Acct 4854 (Jan-May 2026)"]
    rem = defaultdict(float)
    for r in range(7, w4.max_row + 1):
        c = str(w4.cell(r, 9).value or "").strip()
        if c: rem[norm(c)] += num(w4.cell(r, 6).value) - num(w4.cell(r, 7).value)
    taken = defaultdict(float)
    for dt, nm, fee, cost in disb:
        if dt >= datetime.date(2026, 5, 1): continue
        # the March sweep took fee only; Wei Li's $80.40 case cost stayed in trust
        taken[nm] += fee + (0 if nm == "Wei Li" else cost)
    out = {c: round(rem[c] - taken.get(c, 0), 2) for c in rem}
    tot = round(sum(out.values()), 2)
    if abs(tot - 386306.90) > 0.005:
        sys.exit(f"carryover allocation is {tot:,.2f}, must be 386,306.90 — fix before continuing")
    return out

def sweep_allocation(ws, last, eom, disb):
    """Each fee sweep belongs to the clients disbursed the PREVIOUS month.
    Returns {client: [(date, conf, label, amount)]} for sweeps on or before eom."""
    by_month = defaultdict(list)
    for dt, nm, fee, cost in disb:
        if fee or cost: by_month[dt.strftime("%Y-%m")].append((nm, fee + cost))
    alloc = defaultdict(list)
    for r in range(10, last + 1):
        cli = str(ws.cell(r, 9).value or "")
        amt = num(ws.cell(r, 7).value)
        if "Operating" not in cli or not amt: continue
        d = ws.cell(r, 1).value
        if not isinstance(d, datetime.datetime) or d.date() > eom: continue
        prev = (d.date().replace(day=1) - datetime.timedelta(days=1)).strftime("%Y-%m")
        cases = by_month.get(prev, [])
        tot = round(sum(a for _, a in cases), 2)
        if abs(tot - amt) > 0.02:
            sys.exit(f"sweep {d.date()} is {amt:,.2f} but {prev} fees total {tot:,.2f} — "
                     f"cannot allocate to clients; resolve before continuing")
        conf = f(ws.cell(r, 4).value)
        # A 1/3 fee on a settlement that does not divide by three leaves a fraction of a cent
        # in the Disbursement Sheet. The bank moved whole cents, so each client's share is
        # rounded and the rounding difference is carried by the largest share — the shares
        # must add back to the sweep exactly or the client ledgers will not total the journal.
        shares = [[nm, round(a, 2)] for nm, a in cases if a]
        drift = round(amt - sum(x[1] for x in shares), 2)
        if drift and shares:
            big = max(range(len(shares)), key=lambda k: shares[k][1])
            shares[big][1] = round(shares[big][1] + drift, 2)
        if abs(sum(x[1] for x in shares) - amt) > 0.005:
            sys.exit(f"sweep {d.date()} allocation {sum(x[1] for x in shares):,.2f} != {amt:,.2f}")
        for nm, a in shares:
            alloc[nm].append((d, conf, f"{d.strftime('%-m/%-d')} sweep — {prev} fees", a))
    return alloc

# ---------------------------------------------------------------- styling
BOLD  = Font(bold=True);  TITLE = Font(bold=True, size=14)
HF    = Font(bold=True, color="FFFFFF"); HB = PatternFill("solid", fgColor="305496")
THIN  = Border(bottom=Side(style="thin")); RED = PatternFill("solid", fgColor="FFC7CE")
def head(ws, row, cols, widths):
    for i, h in enumerate(cols, 1):
        c = ws.cell(row, i); c.value = h; c.font = HF; c.fill = HB
        c.alignment = Alignment(horizontal="center", wrap_text=True); c.border = THIN
    for col, w in zip("ABCDEFGHIJ", widths): ws.column_dimensions[col].width = w
def titles(ws, t, sub):
    ws["A1"] = t; ws["A1"].font = TITLE; ws["A2"] = sub

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True, help="YYYY-MM")
    ap.add_argument("--bank-end", type=float, required=True)
    ap.add_argument("--stmt-pdf"); ap.add_argument("--stmt-csv")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    y, m = map(int, a.month.split("-"))
    eom = datetime.date(y, m, calendar.monthrange(y, m)[1])
    MON = datetime.date(y, m, 1).strftime("%B")

    ws, last = load_journal()
    disb  = load_disbursements()
    carry = carryover(disb)
    sweeps = sweep_allocation(ws, last, eom, disb)

    inp, OS, DIT = [], [], []
    for r in range(10, last + 1):
        d, s = num(ws.cell(r, 6).value), num(ws.cell(r, 7).value)
        if not (d or s): continue
        i = issued(ws, r)
        if i is None or i > eom: continue
        inp.append(r)
        c = cleared(ws, r)
        if c is None or c > eom: (OS if s else DIT).append(r)
    os_amt  = round(sum(num(ws.cell(r, 7).value) for r in OS), 2)
    dit_amt = round(sum(num(ws.cell(r, 6).value) for r in DIT), 2)
    J = round(sum(num(ws.cell(r, 6).value) for r in inp) - sum(num(ws.cell(r, 7).value) for r in inp), 2)
    adj = round(a.bank_end + dit_amt - os_amt, 2)

    led = defaultdict(float); rows_by = defaultdict(list)
    for c, v in carry.items(): led[c] += v
    for r in inp:
        cli = str(ws.cell(r, 9).value or "").strip()
        if not cli or cli.startswith(("Carryover", "Operating")): continue
        led[norm(cli)] += num(ws.cell(r, 6).value) - num(ws.cell(r, 7).value)
        rows_by[norm(cli)].append(r)
    for c, lst in sweeps.items():
        for _, _, _, amt in lst: led[c] -= amt
    L = round(sum(led.values()), 2)

    print(f"line 1  trust account journal        {J:>14,.2f}")
    print(f"line 2  total client ledgers         {L:>14,.2f}")
    print(f"line 3  adjusted bank                {adj:>14,.2f}")
    print(f"        bank statement ending        {a.bank_end:>14,.2f}")
    print(f"        + outstanding deposits ({len(DIT)})  {dit_amt:>14,.2f}")
    print(f"        - outstanding disburse ({len(OS)})  {os_amt:>14,.2f}")
    neg = {c: round(v, 2) for c, v in led.items() if v < -0.004}
    print(f"negative client ledgers: {neg or 'none'}")
    if abs(J - L) > 0.005 or abs(J - adj) > 0.005:
        sys.exit(f"\nTHE THREE DO NOT AGREE — journal vs ledgers {J-L:,.2f}, journal vs bank {J-adj:,.2f}. "
                 f"Nothing written. Resolve every difference by name before re-running.")
    print("\nthe three agree to the cent")
    if a.dry_run:
        print("dry run — nothing written"); return

    PKG = f"{MR}{a.month} State Bar Package/"
    os.makedirs(PKG, exist_ok=True)

    # ---- reconciliation form
    src = f"{MR}Recon-3618-{a.month}-{MON}.xlsx"
    if os.path.exists(src):
        sup = f"{MR}Recon-3618-{a.month}-{MON} (SUPERSEDED {datetime.date.today()}).xlsx"
        if not os.path.exists(sup): shutil.copy2(src, sup)
        dst = PKG + f"Recon-3618-{a.month}-{MON} (AMENDED).xlsx"
    else:
        src = BASE + "Templates/Reconciliation-Form.xlsx"
        dst = PKG + f"Recon-3618-{a.month}-{MON}.xlsx"
    shutil.copy2(src, dst)
    wb = openpyxl.load_workbook(dst); w = wb["Reconciliation form"]
    w["D4"] = "Law Office of Shenqi Cai APC"; w["D5"] = "Bank of America"
    w["D6"] = "California IOLTA Trust Account"; w["D7"] = "3252 1786 3618"
    w["J4"] = MON; w["L4"] = y; w["L5"] = datetime.datetime(2026, 5, 4); w["L6"] = "(active)"
    w["L7"] = eom.strftime("%m/%d/%Y")          # reconciliation date = month end, always
    w["L19"] = J; w["L25"] = J; w["L34"] = 0; w["L39"] = J
    w["L44"] = a.bank_end; w["L46"] = dit_amt; w["L48"] = os_amt; w["L50"] = adj
    w["B58"] = "Klaus Liu"; w["B67"] = "Shenqi Cai"; w["F67"] = 348794
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())
    w["L58"] = today; w["L67"] = today          # signature date = the real day, never back-dated
    wb.save(dst)

    # ---- 1 journal
    wb = openpyxl.Workbook(); w = wb.active; w.title = f"Account Journal {a.month}"
    titles(w, "Attachment 1 — Trust Account Journal",
           f"IOLTA #3618 · Law Office of Shenqi Cai APC · all entries through {eom:%m/%d/%Y} · Rule 1.15 Standard (1)(b)")
    head(w, 4, ["Date","Payor / Payee","Method","Check #","Purpose","Deposit","Disbursement","Balance","Client","Cleared"],
         (12,38,20,12,42,14,14,14,26,12))
    r = 5
    for jr in inp:
        for col, src_c in ((1,1),(2,2),(3,3),(4,4),(5,5),(9,9),(10,13)):
            w.cell(r, col).value = f(ws.cell(jr, src_c).value)
        for col, src_c in ((6,6),(7,7)):
            v = num(ws.cell(jr, src_c).value)
            if v: w.cell(r, col).value = v; w.cell(r, col).number_format = MONEY
        w.cell(r,8).value = f"=N(F{r})-N(G{r})" if r == 5 else f"=H{r-1}+N(F{r})-N(G{r})"
        w.cell(r,8).number_format = MONEY
        r += 1
    w.cell(r+1,5).value = f"TRUST ACCOUNT JOURNAL BALANCE {eom:%m/%d/%Y}"; w.cell(r+1,5).font = BOLD
    w.cell(r+1,8).value = f"=H{r-1}"; w.cell(r+1,8).font = BOLD; w.cell(r+1,8).number_format = MONEY
    w.freeze_panes = "A5"
    wb.save(PKG + f"1 - Account Journal (through {eom:%m-%d-%Y}).xlsx")

    # ---- 2 client ledgers  (+ summary rows for 4)
    clients = sorted(set(rows_by) | set(k for k, v in carry.items() if abs(v) > 0.004) | set(sweeps))
    wb = openpyxl.Workbook(); wb.remove(wb.active); summ = wb.create_sheet("Summary")
    used, srows = set(), []
    def tab(c):
        t = re.sub(r"[\[\]\:\*\?\/\\]", "-", c)[:31].strip(); b, i = t, 2
        while t.lower() in used: t = b[:28] + f"~{i}"; i += 1
        used.add(t.lower()); return t
    for c in clients:
        t = tab(c); sh = wb.create_sheet(t)
        titles(sh, c, f"IOLTA #3618 · Law Office of Shenqi Cai APC · Rule 1.15 Standard (1)(a) · as of {eom:%m/%d/%Y}")
        head(sh, 4, ["Date","Payor / Payee","Method","Check #","Purpose","Deposit","Disbursement","Balance"],
             (12,38,20,12,44,14,14,14))
        items = []
        if abs(carry.get(c, 0)) > 0.004:
            v = carry[c]
            items.append((datetime.date(2026,5,4), "Bank of America — FDES Transfer", "Funds Transfer Credit",
                          "", "Carryover from closed IOLTA #4854", v if v > 0 else 0.0, -v if v < 0 else 0.0))
        for jr in rows_by.get(c, []):
            items.append((issued(ws, jr) or eom, f(ws.cell(jr,2).value), f(ws.cell(jr,3).value),
                          f(ws.cell(jr,4).value), f(ws.cell(jr,5).value),
                          num(ws.cell(jr,6).value), num(ws.cell(jr,7).value)))
        for dt, conf, lbl, amt in sweeps.get(c, []):
            items.append((dt.date(), "Bank of America — Transfer to Operating CHK 2995",
                          "Funds Transfer Debit", conf, f"Attorney fee + case cost ({lbl})", 0.0, amt))
        items.sort(key=lambda x: x[0])
        rr, dp, ds = 5, 0.0, 0.0
        for dt, payee, meth, ck, purp, dep, dis in items:
            sh.cell(rr,1).value = dt.strftime("%m/%d/%Y") if hasattr(dt, "strftime") else dt
            sh.cell(rr,2).value = payee; sh.cell(rr,3).value = meth
            sh.cell(rr,4).value = ck;    sh.cell(rr,5).value = purp
            if dep: sh.cell(rr,6).value = dep; sh.cell(rr,6).number_format = MONEY; dp += dep
            if dis: sh.cell(rr,7).value = dis; sh.cell(rr,7).number_format = MONEY; ds += dis
            sh.cell(rr,8).value = f"=N(F{rr})-N(G{rr})" if rr == 5 else f"=H{rr-1}+N(F{rr})-N(G{rr})"
            sh.cell(rr,8).number_format = MONEY
            rr += 1
        sh.cell(rr+1,5).value = f"Balance held in trust {eom:%m/%d/%Y}"; sh.cell(rr+1,5).font = BOLD
        sh.cell(rr+1,8).value = f"=H{rr-1}"; sh.cell(rr+1,8).font = BOLD; sh.cell(rr+1,8).number_format = MONEY
        sh.freeze_panes = "A5"
        # the authoritative balance is led[c] — the same running total that produced line 2.
        # dp-ds re-adds the rows in a different order and can drift a cent on rounding.
        bal = round(led[c], 2)
        if abs((dp - ds) - bal) > 0.005:
            sys.exit(f"{c}: ledger rows total {dp-ds:,.2f} but running balance is {bal:,.2f}")
        srows.append((c, t, dp, ds, bal))
    def summary_sheet(sh, with_tab):
        titles(sh, "Attachment 4 — Client Ledger Summary with Balances",
               f"IOLTA #3618 · Law Office of Shenqi Cai APC · as of {eom:%m/%d/%Y} · Rule 1.15 Standard (1)(d)")
        cols = ["Client","Ledger tab","Total Deposits","Total Disbursements",f"Balance {eom:%m/%d/%Y}"] if with_tab \
               else ["Client","Total Deposits","Total Disbursements",f"Balance {eom:%m/%d/%Y}"]
        head(sh, 4, cols, (34,34,18,20,20) if with_tab else (36,18,20,20))
        rr = 5; off = 0 if with_tab else -1
        for c, t, dp, ds, bal in sorted(srows, key=lambda x: -x[4]):
            sh.cell(rr,1).value = c
            if with_tab: sh.cell(rr,2).value = t
            for cc, v in ((3+off,dp),(4+off,ds),(5+off,bal)):
                sh.cell(rr,cc).value = v; sh.cell(rr,cc).number_format = MONEY
            if bal < -0.004: sh.cell(rr,5+off).fill = RED
            rr += 1
        sh.cell(rr,1).value = "TOTAL — agrees to the trust account journal"; sh.cell(rr,1).font = BOLD
        for cc in (3+off, 4+off, 5+off):
            col = openpyxl.utils.get_column_letter(cc)
            sh.cell(rr,cc).value = f"=SUM({col}5:{col}{rr-1})"; sh.cell(rr,cc).font = BOLD
            sh.cell(rr,cc).number_format = MONEY
        sh.freeze_panes = "A5"
    summary_sheet(summ, True)
    wb.move_sheet("Summary", -(len(wb.sheetnames) - 1))
    wb.save(PKG + f"2 - Client Ledgers (as of {eom:%m-%d-%Y}).xlsx")
    wb4 = openpyxl.Workbook(); summary_sheet(wb4.active, False); wb4.active.title = "Summary"
    wb4.save(PKG + f"4 - Client Ledger Summary with Balances ({eom:%m-%d-%Y}).xlsx")

    # ---- 3 statement
    if a.stmt_pdf and os.path.exists(a.stmt_pdf):
        shutil.copy2(a.stmt_pdf, PKG + f"3 - Bank Statement with Check Images ({a.month}).pdf")
    if a.stmt_csv and os.path.exists(a.stmt_csv):
        shutil.copy2(a.stmt_csv, PKG + f"3a - Bank Statement export ({a.month}).csv")

    # ---- 5 outstanding deposits
    wb = openpyxl.Workbook(); w = wb.active; w.title = "Outstanding Deposits"
    titles(w, "Attachment 5 — List of Outstanding Deposits",
           f"IOLTA #3618 · deposits recorded on or before {eom:%m/%d/%Y} not yet on the bank statement")
    head(w, 4, ["Date received","Payor","Client","Amount"], (16,40,30,16))
    rr = 5
    if DIT:
        for jr in sorted(DIT, key=lambda r: -num(ws.cell(r,6).value)):
            w.cell(rr,1).value = f(ws.cell(jr,1).value); w.cell(rr,2).value = f(ws.cell(jr,2).value)
            w.cell(rr,3).value = f(ws.cell(jr,9).value)
            w.cell(rr,4).value = num(ws.cell(jr,6).value); w.cell(rr,4).number_format = MONEY
            rr += 1
    else:
        w.cell(5,1).value = "NONE"; w.cell(5,1).font = BOLD
        w.cell(5,2).value = f"Every deposit recorded through {eom:%m/%d/%Y} appears on the statement."
        rr = 6
    w.cell(rr+1,1).value = "TOTAL OUTSTANDING DEPOSITS"; w.cell(rr+1,1).font = BOLD
    w.cell(rr+1,4).value = dit_amt; w.cell(rr+1,4).font = BOLD; w.cell(rr+1,4).number_format = MONEY
    wb.save(PKG + f"5 - Outstanding Deposits ({eom:%m-%d-%Y}).xlsx")

    # ---- 6 outstanding disbursements
    wb = openpyxl.Workbook(); w = wb.active; w.title = "Outstanding Disbursements"
    titles(w, "Attachment 6 — List of Outstanding Disbursements",
           f"IOLTA #3618 · checks written on or before {eom:%m/%d/%Y} that had not cleared at {eom:%m/%d/%Y}")
    head(w, 4, ["Check #","Date issued","Payee","Client","Amount","Date cleared","Status today"],
         (12,14,40,26,14,14,30))
    rr = 5; stale = []
    today = datetime.date.today()
    for jr in sorted(OS, key=lambda r: -num(ws.cell(r,7).value)):
        cl = f(ws.cell(jr,13).value); amt = num(ws.cell(jr,7).value)
        iss = issued(ws, jr)
        w.cell(rr,1).value = f(ws.cell(jr,4).value); w.cell(rr,2).value = iss.strftime("%m/%d/%Y") if iss else ""
        w.cell(rr,3).value = f(ws.cell(jr,2).value); w.cell(rr,4).value = f(ws.cell(jr,9).value)
        w.cell(rr,5).value = amt; w.cell(rr,5).number_format = MONEY
        w.cell(rr,6).value = cl
        if cl:
            w.cell(rr,7).value = "cleared " + cl
        else:
            old = iss and (today - iss).days > 90
            w.cell(rr,7).value = "STILL OUTSTANDING — over 90 days, stale-dated" if old else "still outstanding"
            w.cell(rr,7).fill = RED
            if old: stale.append((f(ws.cell(jr,4).value), amt))
        rr += 1
    w.cell(rr+1,1).value = "TOTAL OUTSTANDING DISBURSEMENTS"; w.cell(rr+1,1).font = BOLD
    w.cell(rr+1,5).value = os_amt; w.cell(rr+1,5).font = BOLD; w.cell(rr+1,5).number_format = MONEY
    if stale:
        w.cell(rr+3,1).value = ('Checks marked STILL OUTSTANDING are printed "VOID AFTER 90 DAYS" and are now '
                                'past that date. They need to be voided and re-issued; the client ledgers still '
                                'show the money owed to those payees.')
    w.freeze_panes = "A5"
    wb.save(PKG + f"6 - Outstanding Disbursements ({eom:%m-%d-%Y}).xlsx")

    print(f"\nwrote {PKG}")
    for fn in sorted(os.listdir(PKG)): print("  ", fn)
    if stale:
        print(f"\nSTALE-DATED, need voiding and re-issue: {len(stale)} checks "
              f"{sum(x[1] for x in stale):,.2f} — {', '.join(c for c,_ in stale)}")

if __name__ == "__main__":
    main()
