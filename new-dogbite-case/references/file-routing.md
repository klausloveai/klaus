# Intake zip → case subfolder routing + rename rules

The intake zip (from the intake specialist) is usually `<Client>_Dog Bite.zip`
containing an `Initial Docs/` folder. Files carry generic names; route + rename them
into the copied template's numbered subfolders. Build a `routing.json` (see
`scripts/sort_files.py` for the schema) and run the script.

macOS junk (`.DS_Store`, `._*`, the `__MACOSX/` tree) is skipped automatically.

## Routing table (v2 — Klaus-calibrated 2026-07-02)
| Incoming file (typical) | → destination | rename to |
|---|---|---|
| **Cindy's intake form (docx)** | **case folder ROOT (lobby)** | `0. Case Intake.docx` |
| Client ID / driver license | **`1. Incident & Liability`** | `<Client> - CA DL.jpg` (or `- ID.jpg`) |
| Incident scene photo/video | `1. Incident & Liability` | keep original name |
| Incident address photo | `1. Incident & Liability` | keep original name |
| Dog reference image | `1. Incident & Liability` | `Dog Reference.jpg` |
| Animal control / animal-safety contact | `1. Incident & Liability` | keep original name |
| Property deed | `1. Incident & Liability` | `<Client> - Property Deed.pdf` |
| Retainer / contingency agreement | `2. Legal Documents` | `<Client> - PI Contingency Agreement.pdf` |
| POE letters (later) | `2. Legal Documents` | firm naming |
| LOR letters (later) | `2. Legal Documents` | firm naming |
| **Injury photos** PDF/images | **`3. Medical Record & Bill`** | `<Client> - Injury Photos.pdf` |
| ER / medical records PDF | `3. Medical Record & Bill` | `<Client> - ER Records (<Facility>) <M-D-YY>.pdf` |

## The four Klaus rules (source of truth)
1. **Cindy's intake form** → renamed `0. Case Intake.docx`, kept in the **case folder root**
   (the "lobby"), beside the `0. Intake Sheet` — the two "0." files live at the root.
2. **Driver license / ID** → `1. Incident & Liability`.
3. **Retainer, POE, LOR** → `2. Legal Documents`.
4. **Injury photos** → `3. Medical Record & Bill`.

## Notes
- **Injury photos ≠ scene photos.** Injury photos (the client's wounds) are **medical**
  evidence → folder 3. Scene / address / dog / liability photos → folder 1.
- The two `0.` files (`0. Case Intake.docx`, `0. Intake Sheet`) stay in the root and must
  never be swept into a subfolder by any later maintenance routine.
- If a file's purpose is ambiguous, ask before routing rather than guessing.
- Keep original names when they are already descriptive (scene photo/video, address).
- Rename to lead with `<Client> - ` for the "identity" docs (ID, retainer, records) so
  they read clearly out of context; leave self-descriptive media as-is.
