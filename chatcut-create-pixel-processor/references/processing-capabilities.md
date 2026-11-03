# Pixel Effect processing capabilities

Pixel Effects can consume native analysis and matte results derived from original source media. Declare every dependency in `push_asset.processingCapabilities`; undeclared namespaces are not exposed, and Export must know the complete demand before encoding.

```json
{
  "filePath": "/absolute/project.chatcutproject/assets/pixel-effect/face-follow/effect.ts",
  "type": "pixel-effect",
  "name": "Face Follow",
  "processingCapabilities": ["face-tracking"],
  "properties": []
}
```

Supported declarations:

| Capability           | Render namespace   | Result                                                            |
| -------------------- | ------------------ | ----------------------------------------------------------------- |
| `face-tracking`      | `faceTracking`     | `faces`: observations or `null`                                   |
| `object-tracking`    | `objectTracking`   | `rect`: normalized selected-object rectangle or `null`            |
| `portrait-matte`     | `portraitMatte`    | `matteImage`, `matteWidth`, `matteHeight`                         |
| `smart-object-matte` | `smartObjectMatte` | selected-object matte fields                                      |
| `camera-motion`      | `cameraMotion`     | `pose`, `observation`, and optional window                        |
| `color-descriptor`   | `sourceColor`      | original-video sidecar image, dimensions, and nullable descriptor |

Each declared namespace is passed directly to `render`, alongside `frame`, `progress`, and `timeSeconds`. Results are fresh for the current source sample. `null` means unavailable: draw a deterministic fallback, normally the unmodified input. Do not retain host-owned matte or source images across renders.

## Face tracking

`faceTracking.faces` is `null` while unavailable and `[]` when analysis completed but found no face. Face coordinates are normalized to the display-oriented original source. Observations include bounds and facial keypoints. Select a face deterministically every frame—for example, largest area with confidence as a tie-breaker—and derive the focal point from stable landmarks such as the eye midpoint.

```js
render({ faceTracking }) {
  const faces = faceTracking.faces;
  const face = Array.isArray(faces) && faces.length
    ? faces.reduce((best, candidate) => {
        const area = (value) =>
          Math.max(0, value.bounds.right - value.bounds.left) *
          Math.max(0, value.bounds.bottom - value.bounds.top);
        return area(candidate) > area(best) ||
          (area(candidate) === area(best) && candidate.confidence > best.confidence)
          ? candidate
          : best;
      })
    : null;
  if (!face) {
    ctx.drawImage(input, 0, 0, width, height);
    return;
  }
  const x = (face.keypoints.leftEye.x + face.keypoints.rightEye.x) / 2;
  const y = (face.keypoints.leftEye.y + face.keypoints.rightEye.y) / 2;
  // Reconstruct this frame's crop or decoration from x/y; do not accumulate motion.
}
```

Face identity continuity, smoothing, framing, and loss behavior belong to the Effect. Keep seeking deterministic: smoothing may use a bounded source-time window only when the runtime supplies one; do not depend on playback history.

## Object tracking and mattes

`objectTracking.rect` requires a confirmed selection stored on the placed Effect. The rectangle uses normalized source coordinates. When it is null, preserve the input. Do not author a fake trajectory.

HTML matte capabilities expose `matteImage: HTMLImageElement | null`; Web capabilities expose the corresponding GPU texture. The matte contains premultiplied white with the matte in alpha. For Canvas 2D, draw the input to an owned staging canvas, switch to `destination-in`, draw the current matte, then composite the result. Smart Object Matte also requires a confirmed source-bound point selection; Portrait Matte does not.

## Source selection and validation

Capability processing reads an original compatible source, independently of the Effect's current pixel input. Item-targeted effects automatically use that item's source. Track-range effects automatically choose the first compatible active source unless the placed Effect has an explicit per-capability `processing[capability].trackId`.

Native import validation checks declarations and exposes namespaces with unavailable synthetic results. It proves fallback execution only, not real analysis readiness. Apply the Effect to representative media, preview multiple frames including backward seeks, and verify actual tracking or matte output before delivery.

For the engine-level contract and maintained examples, see Blink's Processing, Pixel Effects, and HTML Pixel Effects documentation together with its processing Pixel Effect examples.
