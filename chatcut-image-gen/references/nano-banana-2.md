# nano-banana-2 (Gemini 3.1 Flash Image)

Use `submit_image` with `model: "nano-banana-2"` for Nano Banana 2. ChatCut resolves this alias to Google's `gemini-3.1-flash-image` on the global Vertex endpoint. The existing `nano-banana` alias continues to select `gemini-3-pro-image` (Nano Banana Pro).

## Supported parameters

- `prompt`: describe the result and the role of each reference in order.
- `referenceAssetIds` and `referenceUrls`: up to **14 combined images**, with project references first. Inline project references accept PNG, JPEG, WebP, HEIC and HEIF, up to 7 MiB each. URL references follow the shared image-gen resource limits (5 MiB).
- `aspectRatio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `4:5`, `5:4`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`; default `16:9`. The four extreme ratios are specific to Nano Banana 2.
- `imageSize`: `512`, `1K`, `2K`, `4K`; default `1K`. `512` is specific to Nano Banana 2.
- `name` and `count`: shared image-gen parameters. Each result is a separate job.

`quality` and `background` are OpenAI controls. ChatCut's Nano Banana 2 route accepts text and image references. Search grounding and video input are not exposed by this route.

## Observed generation and documented modes

A saved 2026-10-27 request to `gemini-3.1-flash-image` in our Vertex project on the global endpoint returned HTTP 200 with a final non-thought 512×512 PNG. The request used `imageSize: "512"`, `aspectRatio: "1:1"`, a text-only prompt and `TEXT` + `IMAGE` response modalities. Usage was 18 prompt tokens and 747 IMAGE output tokens (765 total).

Google documents the sizes, aspect ratios and 14-image reference limit above. This receipt does not test those modes or other regions; their account-specific behavior remains unverified, and they remain available through this route.

```ts
submit_image({
  model: "nano-banana-2",
  prompt:
    "Generate one simple image: a plain blue square on a plain white background. No text.",
  imageSize: "512",
  aspectRatio: "1:1",
});
```

```ts
submit_image({
  model: "nano-banana-2",
  prompt:
    "Keep the first reference's character and use the second reference's setting.",
  referenceAssetIds: ["<character-id>", "<setting-id>"],
  name: "Character in setting",
});
```

Wait with `track_progress`; Desktop imports the completed image into the project. Inspect that result before any revision. Report access, quota, service or malformed-response failures with their returned diagnostics; do not silently substitute another model.

## Cost and availability

ChatCut Pro and credits are required. Estimates use the requested output size, an approximate prompt token count and known reference image inputs. Final usage uses reported prompt tokens when present; missing prompt usage retains that input estimate. Image output uses complete IMAGE modality counts. Text output uses complete TEXT counts or a valid candidate-token residual after complete IMAGE usage; thinking tokens are added once. Reported cached prompt tokens use the supplier's cached-input rate once. If modality usage is absent, image output uses a resolution estimate; unreported text/thinking usage is unknown. An estimate is not an exact supplier bill or proof that the configured Google account has model access.

At the standard global list rates, the saved usage computes to $0.044829: input $0.50/M + IMAGE output $60/M; cached input is $0.05/M and text/thinking output is $3/M when present. This is a list-rate calculation, not an invoice. The 512 image-only estimate uses 747 tokens ($0.04482); prompt tokenization is estimated until measured, and unknown text/thinking usage remains additional. ChatCut credit quotes use the accepted retail policy separately.

Official model capabilities and supplier rates were checked on 2026-10-27:

- [Google Cloud model and global availability](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-flash-image)
- [Google Cloud image generation pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing#image_generation)
- [Google Cloud implicit caching](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview)
