---
name: settled-case-marketing-pkg
description: Post-settlement marketing package workflow for PI auto cases. Use this skill when the user wants to upload a settled case PDF into the Dashcam素材 folder in Google Drive for the marketing team, create a client subfolder for marketing materials, or share settled case materials with the 车祸部-Marketing team. Triggers on phrases like "create dashcam folder for [client]", "upload to Dashcam素材", "add settled case to marketing folder", "marketing package for [client]", "settled case materials", "upload case PDF for marketing", or any request involving organizing a PI auto case into the firm's dashcam/marketing Drive folder after settlement.
---

# Post-Settlement Marketing Package

When a PI auto case settles, this workflow organizes the case materials into the firm's **Dashcam素材** (Dashcam Materials) folder on Google Drive. The 车祸部-Marketing team uses these materials to find high-value settled cases for client outreach.

> **Scope:** PI auto cases only. Do NOT use for Hernán Simó's dog bite litigation cases.

---

## What you need from the user

Ask for anything that's missing before you start:

- **Client name** — first and last (e.g., "Cheng Peng")
- **Date of loss** — you'll convert whatever format they give you to M-D-YYYY (e.g., "2-5-2026" — hyphens, not slashes)
- **Case PDF** — a compiled PDF of the settlement materials, typically 2–3 pages: page 1 is the disbursement/settlement summary, pages 2–3 are accident photos. The user may attach it to the conversation or give you a local path.

---

## Steps

### 1. Derive the naming convention

Everything is named consistently:

```
Subfolder name:  {FirstName} {LastName}-{M-D-YYYY}
PDF filename:    {FirstName} {LastName}-{M-D-YYYY}.pdf
```

Example: client "Cheng Peng", date of loss 2/5/2026 → `Cheng Peng-2-5-2026`

If the user gives you a date like "February 5, 2026" or "2/5/2026", convert it to `2-5-2026`.

### 2. Create the client subfolder in Google Drive

Create a new folder inside the Dashcam素材 parent folder using `mcp__Google_Drive__create_file`:

- **Parent folder ID:** `1RgaAc-DYQWfLMWlo3w8loQ4_Cem1CgU7`
- **Name:** `{FirstName} {LastName}-{M-D-YYYY}` (e.g., `Cheng Peng-2-5-2026`)
- **MIME type:** `application/vnd.google-apps.folder`

Save the new folder's ID — you'll need it in the next step.

### 3. Upload the PDF into the new subfolder

Upload the compiled case PDF using `mcp__Google_Drive__create_file`:

- **Parent:** the subfolder ID from step 2
- **Name:** `{FirstName} {LastName}-{M-D-YYYY}.pdf`
- **MIME type:** `application/pdf`
- **Content:** the PDF the user provided

### 4. Confirm and give the user the WeChat link

After a successful upload, tell the user:

> ✅ Done! Marketing package created for **{FirstName} {LastName}**.
>
> Subfolder: `{FirstName} {LastName}-{M-D-YYYY}` — https://drive.google.com/drive/folders/{new-folder-id}
>
> **Next step — paste this link in 车祸部-Marketing on WeChat:**
> ```
> https://drive.google.com/drive/folders/{new-folder-id}
> ```

WeChat is not automated. The user copies and pastes the link themselves.

---

## Edge cases

**Subfolder already exists** — If a folder with this name already appears in Dashcam素材 (maybe from a prior run), confirm with the user before creating another one. They may want to upload into the existing folder instead.

**PDF not yet provided** — Do not proceed to the Drive steps without the PDF. Ask for it first.

**Date format variations** — Accept any reasonable format ("Feb 5 2026", "02/05/2026", "2-5-2026") and convert silently to M-D-YYYY with hyphens.

**Wrong case type** — If the context makes clear this is a dog bite case or Hernán Simó litigation matter, stop and let the user know this workflow is for PI auto only.
