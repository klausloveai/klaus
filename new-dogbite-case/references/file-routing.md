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

## Multi-client cases (added 2026-09-01)
- Shared documents (retainer + joint conflict waiver, client IDs, scene, delivery label,
  animal-control screenshots) are filed ONCE and named with **both** clients:
  `<Client A> & <Client B> - <doc>.pdf`.
- Per-client medical evidence stays **per client**, named with that client alone:
  `Peiyun Zhou - ER Records (Sharp Memorial) 8-17-26 to 8-22-26.pdf`,
  `Jian Wang - Sharp Memorial Billing Statement ($6,207.84 balance).pdf`. This is what
  makes the demand packages separable later.
- Number multi-file series so they sort: `Peiyun Zhou - Injury Video 01.mov` … `07.mov`.
- The intake specialist's file index (if the zip carries one) is worth keeping at the root
  as `0. Intake File Index (from <name>).txt` — it records what she believed she sent, and
  it has already been wrong once (indexed 4 videos, the zip held 7).

## A file whose name asserts a fact it cannot support
Rename it so the caveat travels with the file. A "dog reference" image that is only a
lookalike must be filed as
`Dog Reference (comparison image only - NOT the actual dog).pdf` — otherwise it turns up
in a demand package two months later looking like a photograph of the dog.

## ⚠️ sort_files.py runs exactly once
It uploads unconditionally and has no dedupe. Re-running it duplicates every file. Verify
by listing the destination folders, never by re-running. See SKILL.md Step 6.
