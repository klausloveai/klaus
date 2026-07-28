# Document Naming & Placement

## → 2#Accident Info
- Firstname Lastname-Driver License.ext
- Firstname Lastname-Passport.ext / -California ID Card.ext / -Instruction Permit.ext
- Firstname Lastname-Auto Insurance Card.pdf  (or [Temporary]/[EXPIRED] prefix)
- 1P-License Plate.ext
- 3P-Driver License.ext (or .pdf if front+back combined)
- 3P-Auto Insurance Card.pdf  (or [Temporary]/[EXPIRED] prefix)
- 3P-License Plate.ext
- Vehicle Damage Photos.pdf  (combined, auto-rotated)
- Scene Photos.pdf  (combined, auto-rotated)
- Scene Video 1.mov / Scene Video 2.mov
- Dashcam Video 1.mov / Dashcam Video 2.mov
- Police Card.ext  (NO client name prefix)
- Accident Location Map.ext
- [Platform] Delivery Screenshot.png
- Vehicle Registration.ext
- Injury Photos.pdf

## → 4#Bodily Injury Claim
- Health Insurance Cards (per-client subfolder if multi-client)
- Visit summaries / medical records (per-client subfolder if multi-client)
- Firstname Lastname-ER Medical Records-[Provider]-[Date].pdf
- Firstname Lastname-Urgent Care Visit Summary.pdf

## → 1#Legal Documents
- Intake Responses.zip  ← original WeChat export zip, renamed, EVERY case

## → Case Folder ROOT
- Social Security cards
- Unidentified/unclassifiable documents

## Combining Images into PDF
- Multi-page AIC / declarations page → single PDF
- HIC front+back → single PDF
- Multiple scene photos → Scene Photos.pdf
- Multiple PD photos → Vehicle Damage Photos.pdf
- 3P DL front+back → 3P-Driver License.pdf
- Injury photos → Injury Photos.pdf
- Check MD5 hashes before combining — no duplicates

## Special Prefixes
[DUPLICATE] — exact duplicate files
[EXPIRED] — expired AIC (1P or 3P, including CAARP)
[Temporary] — temp/binder AIC or valid CAARP temp card

## Key Rules
- Police Card filename does NOT include client name prefix
- Vehicle damage photos are NEVER labeled "1P-Vehicle Photo"
- Videos copy as-is (.mov/.mp4), cannot convert to PDF
- Same video in both Dashcam and Scene folders: file once as Dashcam Video 1.mov
- HEIC → convert to PDF where possible; if fails, preserve .heic with note
