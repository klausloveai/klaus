---
name: infinite-invoice
description: |
  Generate a client INVOICE (receipt for the service fee) for Klaus's DV / total-loss
  recovery business **Infinite DV** (Infinite Solutions Consulting LLC) — NOT Lingtu Law.
  Use this skill whenever any of the following are mentioned: 开 invoice, 出 invoice,
  出账单, 给 X 开/出 invoice, bill <client>, invoice for <client>, Infinite DV invoice,
  DV invoice, total loss invoice, "/invoice" for a named client. Typical invocation: just
  a client name (e.g. "给 Gongyao Wang 开 invoice"). The skill pulls that client's row from
  the "DV & Total Loss Gain Cases" sheet (vehicle, VIN, service fee, address, email, and
  which tab → DV vs total-loss wording), auto-assigns the next invoice number + dates,
  renders a branded one-page PDF (no Canva, headless Chrome) to ~/Downloads, and prints a
  ready-to-copy client email draft (English + 中文). It DOES NOT send the email and DOES NOT
  write back to the sheet — Klaus copy-pastes the draft and sends it himself. Always trigger
  for any "make an invoice for <client>" request, even a partial one.
---

# Infinite DV — Invoice generator

Make a service-fee invoice (the receipt Infinite DV sends a client to collect the fee),
pulling the client's data from the case sheet, and hand Klaus a copy-paste email to send.

**This is Infinite DV, a separate business from Lingtu Law.** Do not touch Lingtu tracking
sheets, Drive case folders, or Gmail here.

The tool lives at **`~/infinite-invoice/`** (template.html, generate_invoice.py, assets/,
invoice_for.py). Fully local & dependency-free: HTML template → headless Chrome → PDF.
Source data = the **"DV & Total Loss Gain Cases"** Google Sheet
(id `1Kg-t1oJ55GHRmzS7y7J1TOg4_mOmKE-hi-xupqrk1xg`), read via the `gws` CLI.

## Inputs
- **Client name** (required) — must exist in the DV tab or the Total Loss Gain tab.
- Optional: explicit overrides if the sheet is wrong/blank (service fee, vehicle, VIN).

## Steps

1. **Run the orchestrator** (it does everything: read sheet → PDF → email draft):
   ```
   python3 ~/infinite-invoice/invoice_for.py "<Client Name>"
   ```
   Add `--dry` to preview WITHOUT consuming an invoice number:
   ```
   python3 ~/infinite-invoice/invoice_for.py "<Client Name>" --dry
   ```
   It auto-resolves from the sheet: **service_type** (DV tab → `dv` wording; Total Loss Gain
   tab → `total_loss` wording), **vehicle, VIN, service fee, client address, recipient email,
   and the "gain"** (Settled Amount, used in the email). Invoice # auto-increments
   (`~/infinite-invoice/state.json`); dates = today / +7 days.

2. **Show Klaus the PDF.** It's saved to `~/Downloads/Invoice - <Client> - <INV#>.pdf`.
   Preview/attach it. It's a faithful clone of the old Canva invoice with the compliant
   wording (advisory/assessment fee, no "negotiating the claim", no bank acct#, Zelle + QR).

3. **Show the copy-paste EMAIL DRAFT** the script printed (To / Subject / English body / 中文
   body). **Do NOT send it** — Klaus copies it into infinitedv1@gmail.com (or WeChat) himself.
   The draft states the gain ("recovered an additional $X") verbally — by design this is NOT
   printed on the invoice (keeps the %-of-recovery basis in the signed agreement only).

4. **Sanity-check before presenting:** service fee should ≈ 40% of the gain. If the sheet
   fee is blank/looks wrong, or the client isn't found, tell Klaus and confirm the numbers
   before a real (non-dry) run. Flag any sheet typo (e.g. Status vs Settled Amount mismatch).

## What this skill does NOT do
- Does **not** send any email or fax, and does **not** auto-write the sheet.
- Does **not** create/modify Lingtu records.

## Overriding fields
If a field is wrong or missing in the sheet, write a small JSON and call the generator
directly instead of the orchestrator:
```
python3 ~/infinite-invoice/generate_invoice.py /path/to/invoice.json
```
JSON fields: `invoice_number, billed_to, date_issued, due_date, vehicle, vin, amount,
service_type ("dv"|"total_loss"), client_address (optional), tax (optional), note (optional)`.

## Notes / gotchas
- The case sheet can be **live re-sorted**; the orchestrator matches the client by **name**
  (re-reads the sheet each run), so it's order-independent.
- Company static info (Zelle `infinitedv`, JPMorgan, Terms, footer) is baked into
  `generate_invoice.py` `COMPANY`. Footer business address is still a placeholder pending a
  PO Box / virtual address.
- See memory: [[infinitedv_case_sheet]], [[infinite_invoice_agent]], [[infinitedv_company]].
