---
name: case-settles
description: >
  THE entry point for "a PI-auto case settled, here is the paperwork" at 凌图律所 / Law Office of
  Shenqi Cai APC. **Trigger it whenever Klaus drops a disbursement PDF with little or no text** —
  a file named like `<Client>-Disbursements.pdf`, `<Client>-Disbursement_Letter.pdf`, or a scanned
  settlement/checks packet — and on: "案子结了", "和解完了走一下流程", "这个案子入账", "跑完整流程",
  "settled case", "record this disbursement". **Explicit invocation is `/case-settles`** — that always
  fires this pipeline, no inference needed. A bare attachment with zero words also counts: when a
  disbursement PDF arrives with no instruction, default to running this pipeline. It orchestrates end-to-end in one pass —
  verify math + funding → Disbursement Sheet → Account Journal → archive + move to "8. Settled" →
  Pending→Completed sheet → send the team "Case settled" email (default: send, no approval gate) →
  extract marketing material → file the case into its DOL-year folder → Activity Log + _STATE.md.
  Detail lives in `accounting-agent` (money) and `settled-case-marketing-pkg` (marketing); this
  skill owns the ORDER, the STOP gates, and the final verification. PI auto only — never dog-bite /
  Hernán Simó litigation.
---

# case-settles — settled-case end-to-end pipeline (PI auto)

One dropped disbursement PDF should come out the other end as: books updated, case archived,
marketing material extracted, case filed by DOL year, one Activity Log line, and a team email
sitting in drafts waiting on Klaus.

**Read the detail skills, don't re-derive them:**
`~/.claude/skills/accounting-agent/SKILL.md` — Trigger A, Steps 1–4c (IDs, column map, gotchas)
`~/.claude/skills/settled-case-marketing-pkg/SKILL.md` — Step 4d (marketing paths, PII rules)

## Hard STOP gates — never pass these on your own
1. **Underfunded** — the settlement money is not confirmed in #3618 (→ #4854 → Lashine 5429). Stop.
2. **Math doesn't tie** — `Total ≠ Recovery + Fee + Case Cost + Σ reduced liens`, or a figure Klaus
   gave conflicts with the letter/checks. Raise it, never guess a number into a trust ledger.
3. ~~Sending the team email~~ — **NO LONGER A GATE.** Klaus 2026-08-21: "之后都默认发就行" — build it and
   **send it**, then re-apply the case label (sending drops it). Still stop and ask if something about the case
   itself is unresolved (funding, math, a DOL conflict you had to pick a side on).
4. **Not PI auto** — dog-bite / Hernán litigation: do the money steps only, no marketing package.
5. **Confidentiality** — a settlement agreement with a confidentiality clause: skip marketing, tell Klaus.

---

## Phase 0 — Read and verify (before touching anything)
1. From the PDF: client(s), DOL, total settlement, attorney fee, case cost, client recovery, each
   provider's original → reduced lien, and every check (#, payee, amount, date).
2. Confirm PI auto. Note the retainer shape actually used — standard 1/3 vs medical-first 50/50
   (Fang Liu: $6,000 − $500 lien = $5,500 split 50/50 → fee $2,750, NOT 1/3).
3. Identity check: `Total = Recovery + Fee + Case Cost + Σ(reduced liens)`.
4. **Funding check** in the journal; underfunded → gate 1.
5. **Dedup by CHECK NUMBER**, never by client name — one client can have several deposits.

## Phase 1 — Disbursement Sheet
6. **Fresh row search by client name.** The sheet is re-sorted constantly; a cached row number
   writes onto another client (this really happened — Gui Ying Li and Tony Tao Zhou got clobbered).
   No row → append after the last used client row with the full formula set.
7. Write A (disburse date = the client check's date), C DOL, D/E/F/G/H by coverage, J, K, L,
   M `=SUM(Y{r}:…)`, N `=I-J-K-M-L`, O/P.
8. New provider → new column, header = `=HYPERLINK(<W9 url>,"<payee entity>")`, and **widen that
   row's M range to include it** or N won't zero.
9. **Re-search the row again**, then color: A no fill · received coverage green · I/M/N/O green ·
   J/K yellow · L green if zero else yellow · P yellow · Q–T yellow · provider cells yellow.
10. Read back and confirm **N = zero**.

## Phase 2 — Account Journal
11. Back up `Account-Journal.xlsx` to `Backups/` first.
12. Append one row per check under the current month's `--- PENDING ---` block: payee · `Check` ·
    check # · purpose (include the lien reduction and the check date) · amount · client.
    **Content only — no cleared dates** (those come from the month-end bank record).
13. Start the empty-row scan **past the header block (row 300+), never row 1** — the header has
    merged cells and openpyxl raises on write.
14. Read the rows back.

## Phase 3 — Archive + move
15. Copy the disbursements PDF into the case's `6#…Settlement Documents` subfolder (`files copy`
    if it is already in Drive).
16. Move the case folder → `8. Settled` (`1P35bCgC82Lh6Xftpbt03TX1Cs20G6BoB`). Use `8. Settled`,
    never the sibling `8. Completed`.

## Phase 4 — Pending → Completed
17. Pending tab: `✅` prefix on the client name, disburse date into C1, green every non-zero figure.
    No Pending tab yet → duplicate `Template` (sheetId 0) and fill it first.
18. `copyTo` the Completed sheet, rename the copy (multi-client `/`-joined, driver first).
19. `🔍 Search` index: insert a row at index 1 → `[disburse date, client, DOL, HYPERLINK to the new gid]`.
20. Delete the tab from Pending.

## Phase 5 — Team email  ← STOP GATE
21. **PI Master Sheet** `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM` — find the client in col B of
    the `Claims@` / `Piteam@` / `Picase@` tabs; the tab IS the owning mailbox.
22. Switch identity with **`GOOGLE_WORKSPACE_CLI_CONFIG_DIR`** (not `GWS_CONFIG_DIR`, silently
    ignored); confirm with `gmail users getProfile`.
23. Draft — To `cassie@` + `joe@` + **`elena.j@`**; Subject `<Client>-<DOL M/D/YYYY>-Disbursements`;
    body = flowing HTML: `Hi Team,` / `Case settled.` / the Completed-tab link.
24. Signature = **Klaus's own** (pull from the default config's `sendAs`). claims@'s preset
    signature is **Amos Feng's** — using it signs the wrong person.
25. Attach the disbursements PDF. Create as a DRAFT by writing an `.eml` and uploading with
    `uploadType=multipart` — `--json` blows the shell arg limit, `uploadType=media` is rejected.
26. Label the draft with the case's Gmail label in that mailbox. Label missing there but present in
    klaus@ → that case was run out of klaus@; **ask Klaus which mailbox**, don't create a new label.
27. **Send it** — `drafts send` (no approval needed as of 2026-08-21), then **re-apply the case label**:
    sending DROPS it and the sent message comes back `['SENT']` only. Verify To/Subject/labels after sending.
    Report what went out. If the case had an unresolved discrepancy, raise that in chat — but still send.

## Phase 6 — Marketing material  (PI auto only)
28. Resolve the `人伤` **shortcut** (`1YjOq97wy58uhV_5QMaoOIQ0te5oHShrj`) to its target
    (`1M1yRLjQyfHUnYlCOOCAD1kOzERJ9l9-W`) and write into the target.
29. Extract **only the carrier's settlement check** page(s) → `<Clients>-<M:D:YYYY>.pdf`. Never the
    client-recovery check (prints the client's home address), the fee/lien breakdown, or lien letters.
30. Folder 2 only → copy PD photos and **every video** as-is, original names, no merging. Skip
    driver licenses / insurance cards / police card / policy dec; flag hand-drawn diagrams and
    vehicle-less streetscapes showing a third party's house number.
31. Create `人伤/<Clients>-<M-D-YY>`; upload the check PDF **in two calls** (create --upload lands
    in the shared-drive root as "Untitled", then update to rename + reparent, `removeParents`
    `0ADBH3EXeXKRBUk9PVA`); copy the media in.
32. Move the case folder out of the `8. Settled` lobby into its **DOL-year** folder
    (`2024` / `2025` / `2026`).

## Phase 7 — Close out
33. Verify the whole chain: N = zero · journal rows present and row 2 of the xlsx still empty ·
    PDF in subfolder 6 · case folder in the year folder · marketing folder populated ·
    **no stray "Untitled" in the shared-drive root** · email draft labeled.
34. Append **one** Activity Log row (Category `会计` or `起草`, Source `Drive`, Ref = check #s +
    the marketing folder id).
35. Update `_STATE.md` in the IOLTA#3618 Drive folder — last case processed, anything left pending.
36. Report: what got done, what is waiting on Klaus, and **every discrepancy found** (DOL conflicts,
    retainer-type mismatches, cent-level gaps). Never bury these.
