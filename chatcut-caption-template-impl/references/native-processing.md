# Native inputs for caption templates

For cutouts, text behind a presenter, depth, segmentation, landmarks, tracking, camera-follow or beat-driven captions, use native processing inputs. The live `edit_captions.json` parameter help lists the installed Flux runtime's supported types and uses. Only request admitted types. Flux owns source selection, model preparation, processing and cache reuse; author the visual response in the template and declare its inputs in the caption edit.

## Available result families

| Type                  | Use and current result at the declared ID                                                                                      |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `portrait-matte`      | Person cutout / captions behind a presenter: `matteImage`, `matteWidth`, `matteHeight`                                         |
| `smart-object-matte`  | Selected-object cutout: the same matte fields; requires a confirmed source-bound seed                                          |
| `depth-matte`         | Depth-aware layers: `depthImage`, `depthWidth`, `depthHeight`; packed relative depth, not alpha                                |
| `person-segmentation` | Person category masks: `analysisImage`, `maskRects`, observation dimensions/timestamp                                          |
| `hair-segmentation`   | Hair masks: the same probability-atlas fields                                                                                  |
| `object-tracking`     | Follow a selected object: `{rect}` in source UV, or `rect:null` when lost; requires a seed rectangle                           |
| `face-tracking`       | Fast face-follow graphics: `{faces}` with normalized bounds, confidence, trajectory ID and five named keypoints                |
| `face-analysis`       | Dense facial geometry: `{landmarks,matrices,width,height,timestamp}`                                                           |
| `pose-analysis`       | Pose-driven graphics: `{landmarks,worldLandmarks,width,height,timestamp}`                                                      |
| `hand-analysis`       | Hand-driven graphics: the same landmark fields plus `handedness`                                                               |
| `beauty-analysis`     | Appearance observations: nullable `faces`, each with `id` and 106 normalized `[x,y]` points; optional atlas data               |
| `body-analysis`       | Appearance observations: nullable `bodies`, each with `id` and 18 `[x,y,confidence]` points; optional atlas data               |
| `camera-motion`       | Camera-follow graphics: `{pose,observation}`; nullable pose includes accumulated 2D transform, rotation, scale and translation |
| `beat-tracking`       | Beat-synchronized graphics: `null` or `{beats:[{beat,timestamp}]}` in integer microseconds of the consumer clock               |

`landmarks` groups use `[x,y,z,visibility,presence]`; world landmarks use metres. Face matrices are column-major 4×4 metric camera transforms. Do not treat these as the five named keypoints from Face Tracking or the 106 points from Beauty.

## Caption templates: declare in edit_captions

For a custom caption treatment, author or revise project-owned source with the caption-template workflow. Bind it with one `edit_captions` call; declarations and source bindings travel together in `style.template.capabilities`. No `push_asset`, published catalog ID or user-provided example is required.

```json
{
  "action": "set_track_style",
  "json": "{\"trackId\":\"<caption-track-id>\",\"revision\":\"<read_captions revision>\",\"mode\":\"merge\",\"style\":{\"template\":{\"path\":\"/absolute/project/workspace/caption.jsx\",\"runtime\":\"remotion\",\"capabilities\":[{\"id\":\"portrait\",\"type\":\"portrait-matte\"}]}}}"
}
```

Use `set_card_style` only for an intentional Card exception; item-wide `style` applies the same binding to all captions. Caption declarations accept `{id,type,trackId?,enabled?,selection?}` without `condition`. Omitted `enabled` means true. Omit the capability's `trackId` for automatic original-media selection across visible source tracks; an explicit value selects a media Track, not the caption Track identified by the outer `trackId`. The usual unambiguous ID prefixes returned by tools are accepted and resolved before persistence. Each declaration resolves independently. Captions still receive actual words/timings through `caption_v1` or HTML's caption properties.

A declaration requests an input; authored source consumes it to produce the visual treatment. For text behind a presenter, draw the actual caption into an owned Canvas, then erase only the current portrait's alpha. Declaring `portrait-matte` alone does not restyle ordinary captions. The Agent authors this source as part of fulfilling the request; it must not ask the user to provide implementation code.

```js
function erasePortrait(context, portrait) {
  const matrix = portrait?.sourceToViewport;
  const crop = portrait?.sourceCrop;
  if (
    !portrait?.matteImage ||
    !Array.isArray(matrix) ||
    matrix.length !== 6 ||
    !matrix.every(Number.isFinite) ||
    !Array.isArray(crop) ||
    crop.length !== 4 ||
    !crop.every(Number.isFinite)
  )
    return;
  context.save();
  context.globalAlpha = 1;
  context.globalCompositeOperation = "destination-out";
  context.setTransform(...matrix);
  context.beginPath();
  context.rect(crop[0], crop[1], crop[2] - crop[0], crop[3] - crop[1]);
  context.clip();
  context.drawImage(portrait.matteImage, 0, 0, 1, 1);
  context.restore();
}
```

Call this after drawing each frame's text, using `item.portrait` in Remotion or `ctx.portrait` in HTML. When its image is unavailable, the current text remains in front. An owned inverse CSS mask can preserve a DOM text layout instead. Keep any derived Canvas/mask/texture under the controller's normal disposal; never mutate borrowed native image elements.

To cancel a template at the target scope, use `style:{template:null}`. To keep its typography and only disable analysis, preserve the binding and set that declaration's `enabled:false`; source must render its unavailable-input fallback. Re-enable it or reapply the binding to reuse completed cached results. Absent `template` inherits from the parent; `template:null` stops inheritance, and an omitted field in a merge preserves the old override. The template, including all declarations, inherits atomically Item → Track → Card.

## Source mapping, image formats and selections

Every non-audio MG/caption input also supplies nullable `sourceItemId`, `sourceTimestamp`, `sourceCrop` and `sourceToViewport`. The timestamp is microseconds in the original source; trim, speed, cuts and seeking are resolved by Flux. `sourceToViewport:[a,b,c,d,e,f]` maps complete oriented source UV to local viewport pixels as `(a*u+c*v+e,b*u+d*v+f)`. Clip to `sourceCrop:[left,top,right,bottom]`; do not stretch a matte directly into a caption box. Remotion's local viewport is `item.width` × `item.height`, which may differ from `useVideoConfig()` composition dimensions. The native mapping accounts for source/Card affine placement and crop, not arbitrary preceding warps or other composited Items.

Matte images contain premultiplied white with foreground alpha, including a successful all-zero mask. Depth images are opaque packed data: R is the high byte and G the low byte of 16-bit relative depth. Segmentation uses an opaque probability atlas: each `maskRects` entry identifies a category plane in pixel coordinates; its red channel is probability. Using opaque depth/atlas alpha as a subject mask would erase the whole caption.

Image handles are valid for the current invocation only. Read the fresh image/mapping on every frame, never persist handles or reuse a previous sample when missing. `null` observations mean unavailable; empty arrays or a zero mask can be successful analysis. While native preparation is pending, Preview can hold its last complete composition; once a missing result is confirmed, authored fallback must be deterministic. Completion invalidates frames automatically. Capture/export wait for required processing and report required-result failures; Preview fallback is not export-success evidence.

Object Tracking selection is `{rect:{x,y,width,height},timestamp,contentSha256}`; rectangle coordinates are normalized to the full oriented source and timestamp is source microseconds. Smart Object selection retains `{id,itemId,assetId,contentSha256,sourceIn,timestamp,point,points?}` from the confirmed source seed; points use normalized `x,y` and optional `positive,step`. Preserve the exact returned source IDs, hash and seed after source inspection/selection; never invent them. Smart Object remains bound to that source Item, even if another Item reuses its Asset. A missing or mismatched seed is unavailable/rejected, not permission to choose an arbitrary object. Explicit source selection with no compatible active media never falls back to another Track.

## Verify the actual caption treatment

Read representative short/long Cards over real footage. Inspect generation/progress and the saved effective template; a successfully accepted declaration does not prove analysis or pixels. Preview current words, Card boundaries, source cuts, crop and backward seeks. Check missing-input fallback, disable/re-enable, `template:null` cancellation and save/reopen. Keep unrelated overrides and locks. Preview fallback does not prove an export succeeded.
