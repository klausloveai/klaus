# Motion Graphic native processing inputs

Use named native processing declarations when Motion Graphics or caption templates need source cutouts, depth, segmentation, landmarks, object/face tracking, camera motion or audio beats. HTML and Remotion share these inputs. Flux owns model preparation, processing, caching and source-time sampling; no separate analysis scheduler is needed.

Read the live tool parameter help for the installed consumer's supported types: `push_asset.capabilities` for assets, or `edit_captions.json` for caption templates. The list comes from the installed Flux runtime, not this guide. Use only admitted types. A capability available to Pixel Effects or source processing is not automatically admitted for MG/captions.

```json
{
  "filePath": "/absolute/project.chatcutproject/assets/motion-graphic/follow/entry.html",
  "type": "motion-graphic",
  "name": "Source Follow",
  "width": 1920,
  "height": 1080,
  "duration": 3000000,
  "properties": [],
  "capabilities": [{ "id": "subject", "type": "face-tracking" }]
}
```

The chosen `id`, not the capability type, names the runtime result. HTML reads `render(ctx)` → `ctx.subject`; Remotion reads the root component's `item.subject`. `item.props` remains editable property values. Declare every dependency at import so validation, preparation, playback, capture and export see the same demands. `processingCapabilities:string[]` is obsolete. IDs must be unique JavaScript identifiers and must not collide with runtime fields. An optional `condition` is a boolean expression over declared static property keys; condition properties cannot be animated.

## Bind original sources

Place the MG above compatible original footage, or select a source track explicitly for each dependency:

```text
edit_item({adds:[{type:"motion-graphic",assetId:"<mg-asset-id>",trackId:"<overlay-track-id>",startFrame:0,durationFrames:90,capabilities:[{id:"subject",trackId:"<video-track-id>"}]}]})
```

The asset holds declarations `{id,type,condition?}`; the placed Item holds source bindings `{id,trackId?}`. Source binding never belongs in `processing`, which configures Video/Audio source treatments. An update's `capabilities` array replaces all instance bindings, so preserve sibling entries; `[]` restores automatic selection, and omission preserves bindings. An explicit track with no compatible active clip gives unavailable results. Automatic selection scans the MG track and lower tracks for each capability independently. No inference runs on the rendered MG itself. Importing an asset without a placed consumer does not start source analysis.

The source clock follows placement, source trim, speed and cuts. Geometry is normalized to the display-oriented original source; map it through that source clip's crop and composition placement. The MG's canvas coordinates are not source coordinates. Analysis is independent of preceding Effect warps. Do not cache a previous subject or invent a trajectory during unavailable samples.

## Consume current results

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

For HTML, reconstruct each frame from the current result:

```js
export default function mount({ root }) {
  const marker = root.querySelector(".marker");
  return {
    render(ctx) {
      const face = ctx.subject?.faces?.[0];
      marker.hidden = !face;
      if (!face) return;
      const { leftEye, rightEye } = face.keypoints;
      marker.style.left = `${(leftEye.x + rightEye.x) * 50}%`;
      marker.style.top = `${(leftEye.y + rightEye.y) * 50}%`;
    },
    dispose() {},
  };
}
```

This example assumes the source fills the same viewport. For Remotion, read `const faces = item.subject?.faces` inside the root and return a deterministic empty/fallback graphic when unavailable. Select a subject consistently, handle empty arrays, and check body-point confidence. Keep animation tied to supplied frame/time and avoid playback-history state. A disabled declaration supplies the runtime's unavailable result; an undeclared namespace is absent. Successful empty analysis is distinct from unavailable analysis.

Beauty's 106 landmarks differ from Face Tracking's five keypoints. Flux derives another 88 auxiliary facial points through its geometry helper; raw `extra` is not that derived array. Plain custom Beauty/Body declarations request base detection. Optional skin/retouch/blemish/flow/fitting outputs remain nullable or empty and are not guaranteed by base detection. Built-in appearance settings determine extra model demands; there are no general `skin`/`retouch`/`fitting` switches in `push_asset.capabilities`. MG tracking does not enable the clip's Beauty controls.

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

## Validation and evidence

Import validation receives unavailable synthetic results and checks fallback execution, not source analysis. After a successful import, inspect the asset to verify declarations, place it on compatible media, and inspect its source bindings. Verify native processing progress or a job start with the consumer ID and capability ID before claiming the dependency runs. Preview representative frames and backward seeks when visual quality is requested. A successful `push_asset` or `edit_item` response alone proves neither processing readiness nor output quality.
