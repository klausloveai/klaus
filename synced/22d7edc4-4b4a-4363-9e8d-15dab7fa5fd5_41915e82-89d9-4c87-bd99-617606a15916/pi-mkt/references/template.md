# Canva template reference — 新-猜猜看系列模板

Template design ID: **DAHG9rQstfw** (16 pages, 1080×1440). Never edit it; always `copy-design`.

## Page map

| Page | Content |
|---|---|
| 1 | 封面 (cover) — the only cover page |
| 2 | MAPFRE |
| 3 | Aspire General Insurance |
| 4 | Kemper |
| 5 | Fred Loya Insurance |
| 6 | American Family Insurance |
| 7 | AXA |
| 8 | USAA |
| 9 | Bristol West |
| 10 | Farmers |
| 11 | GEICO |
| 12 | Allstate |
| 13 | Mercury Insurance |
| 14 | State Farm |
| 15 | AAA (Interinsurance Exchange of the Automobile Club / CSAA / Auto Club) |
| 16 | Tesla Insurance |

Match on the payer printed on the check, not the claimant's own insurer. "Interinsurance Exchange of the Automobile Club" → AAA (15). "Progressive", "Travelers", "Nationwide", "Liberty Mutual", "Infinity", "Wawanesa" etc. are not in the template, see "Insurer not in template" below.

`copy-design` with `page_numbers: [1, <insurer page>]` → the new design has exactly two pages: index 1 = cover, index 2 = reveal.

## Elements to change

Element IDs carry over from the template on every copy (e.g. cover check `LBz6hjkvl3088rSq`, photos `LBjktp9clWg88VnG` / `LB2g3Np5gkFR6S6z`, reveal check `LBvgGLfVzFJtNQTy`, magnifier `LBgRRfy813hkN8P3`). Only the page prefix of the locator changes (`<pageId>-<elementId>`), so read design_content once per copy for the page IDs and still sanity-check by position/text.

### Cover (page index 1)
| What | How to recognise it | Operation |
|---|---|---|
| Left accident photo | `shape` at top≈225, left≈85, ~435×498 | `update_fill` image |
| Right accident photo | `shape` at top≈225, left≈560, ~449×497 | `update_fill` image |
| Check image | `shape` at top≈749, left≈67, ~945×358 | `update_fill` with **check_cover.png** |
| Case number | text child of the top-right group, starts with `#LT-` | `replace_text` |
| 事故类型 value | text at top≈1186 (under the "事故类型" label) | `replace_text`, then `position_element` back to left≈179.85, same top |
| 受伤详情 value | text at top≈1314 (under "受伤详情") | `replace_text`, then `position_element` back to left≈179.85, same top |

Leave alone: logo, "ACCIDENT PHOTOS", "左滑解锁赔偿金额" lock badge, labels, icons, background rects (several are locked).

### Reveal (page index 2)
| What | How to recognise it | Operation |
|---|---|---|
| Check image | `shape` at top≈295, left≈68, ~945×358 | `update_fill` with **check_reveal.png** |
| Magnifier | `shape` ~266×266 with TWO paths (circle + glass overlay) at top≈350, left≈720 | `update_fill` with **check_reveal.png** (only the circle path is replaceable), then `crop_media` with the values `redact.py` prints |
| Case number | text starting `#LT-` in the top-right group | `replace_text` |
| 结案天数 | text ending `天高效结案` at top≈1098 | `replace_text` e.g. `37天高效结案` |
| Insurer logo | rotated `rect` (~16°) at top≈797, left≈290, ~354×105, `isMediaReplaceable: true` | only touch when swapping in a new insurer |

`replace_text` on a centred text box shrinks/grows it around its centre, so the text drifts sideways. Re-position the cover's two value lines to their original `left` so they stay flush with the labels. The number/days lines are centred by design and can stay.

## Insurer not in template

Don't stop and ask. Instead:
1. Copy pages `[1, 12]` (Allstate page, a clean horizontal logo slot).
2. Find the insurer's official logo as a PNG/SVG with a transparent or white background (the company's own site or Wikimedia Commons), then `upload-asset-from-url`.
3. `update_fill` the logo rect on page 2 with it.
4. Say in the final report that the logo was swapped in and should get a look.

## Verifying after commit

Canva's API thumbnails stay stale for a while after a commit (URL contains `fallbackstale=T`). Don't trust them. Open a transaction with `read-design` (`open_transaction: true`, `element_ids` of the changed elements), confirm each `mediaId` / text is the new one, then `edit-design finalize: cancel` to close it without changes. The edit-time thumbnails returned by `edit-design` are accurate; save those as the preview for the user.
