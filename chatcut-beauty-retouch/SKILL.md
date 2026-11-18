---
name: chatcut-beauty-retouch
description: Retouch people in existing ChatCut clips with Beauty and Body controls (美颜、磨皮、瘦脸、大眼、化妆、口红、美体). Use for retouch, makeup, and slim requests; not for color grading or generating faces.
---

## Desktop connection in an external host

Use this procedure only for a ChatCut route compatible with the user's goal.
With working Desktop tools, continue. If tools are missing/disconnected, first
reconnect without installing Desktop:

`npx --yes --prefer-online @chatcut/cli@latest connect --no-install --json`

Use existing authorization for connection and ordinary recovery. Honor actual
host permission requirements without adding a repeated installation approval.
Never remove --no-install to accommodate an older CLI: unguarded connect may
install Desktop. An unsupported flag does not establish that Desktop is absent.
Read-only doctor, an installed trusted launcher and supported host connection
mechanisms can establish availability while the published CLI lacks the guard.

Only an actual Desktop installation requires a host permission click for:

`npx --yes --prefer-online @chatcut/cli@latest connect --allow-install --json`

Explain that this may download/install the signed production Desktop, open it
and connect CLI access. Submit the exact command through the host's supported
permission prompt so the user clicks approval. Auto-allow, standing grants,
bypass mode and a never-approve host cannot supply this installation click.
Do not add permission rules or skill tool pre-approvals. Without a supported
prompt, show the manual command without running it. If installation approval is denied,
respect it; do not retry installation through another tool, installer or flags.
The flag records approval already obtained; it cannot itself prove permission.
Never remove --allow-install or bypass publisher validation to work around a
CLI rejection. Preserve credentials, native-host opt-outs and ownership/path
boundaries during targeted configuration repair.

Check exit code, ok and the original result. Preserve the original error,
diagnose recoverable package, transport or inspection failures within existing
authorization, and inspect current state before retrying an uncertain mutation.
Resume the original task after recovery; continue independent authorized work
when a step remains blocked, honoring any refusal and upload restrictions.
A successful connection proves CLI access separately from native host loading.
Use skills read <name>, tools describe <name> --json and tools call as needed;
preserve projectId and follow actual sign-in/service permission results.
Before any paid generation, obtain a current supported quote for the exact
parameters and explicit approval covering that price and scope. Reuse an
existing approval that still covers the operation; do not invent pricing or
resubmit an uncertain paid job without inspecting its task and billing state.


# Beauty retouch

Keep the person's identity recognizable and change the features the user requested.

## Inspect, target, edit, verify

1. Read the relevant catalog once with `inspect_asset` for `builtin:effect-beauty`
   or `builtin:effect-body-shape`; read both only when needed. Use its exact control
   names or keys, ranges, makeup style IDs, and returned edit template.
2. Use `inspect_item` with `people: true` on the target footage to read detected
   people and face bounds, even before anything is applied.
   If several people appear and the request names one, map the person by position
   in those bounds and confirm against `preview_timeline` at the matching time.
   Do not infer identity from the numeric ID or detection order; resolve ambiguity
   before editing that person, and inspect each clip separately.
3. Apply the catalog's template through `edit_item`. Include `personId` for one
   person; omit it to target everyone. Preserve existing unrelated adjustments.
   Controls marked `everyoneOnly`, including Skin smoothing / 磨皮,
   Skin brightening / 美白, and Clarity / 清晰, cannot target one person.
   For a one-person request, explain this limit and leave those controls unchanged
   unless the user also wants everyone affected.
4. Verify the rendered result with `preview_timeline`, comparing the same time
   before and after. Check a representative moving or turned pose when present.
   Inspect processing status if output is still pending; a saved edit is not proof
   that retouching rendered. Check the intended person, skin texture, facial
   identity, makeup alignment, and nearby background lines before claiming success.

## Translate intent into controls

Use the catalog descriptions to choose the region and direction. The table pairs English display labels with exact
Chinese control names; write the returned control key or Chinese name:

| Request                                                 | Control or category                                                                                                          |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 磨皮、柔化皮肤 / soften skin texture                    | Skin smoothing / 磨皮                                                                                                        |
| 提亮肤色 / brighten skin                                | Skin brightening / 美白; do not add this to an unspecified retouch request                                                   |
| 全身磨皮、美白 / smooth or brighten body skin           | The same Beauty Skin smoothing / 磨皮 and Skin brightening / 美白; they reach all visible skin and Body has no skin controls |
| 肤色不均 / patchy skin                                  | Even skin / 匀肤                                                                                                             |
| 淡化痘印、斑点 / reduce blemishes                       | Blemish removal / 祛斑祛痘                                                                                                   |
| 淡化黑眼圈、法令纹 / soften dark circles or smile lines | Dark circles / 祛黑眼圈; Smile lines / 祛法令纹                                                                              |
| 瘦脸 / slim the cheeks                                  | Slim face / 瘦脸                                                                                                             |
| 收一点下颌骨 / slim the jaw a little                    | Jaw width / 下颌骨; Jawline definition / 下颌线 for the lower border                                                         |
| 大眼、亮眼 / enlarge or brighten eyes                   | Enlarge eyes / 大眼; Brighten eyes / 亮眼                                                                                    |
| 瘦鼻、缩小嘴 / narrow nose or smaller mouth             | Slim nose / 瘦鼻; negative Mouth size / 嘴大小                                                                               |
| 柔粉口红 / soft pink lips                               | Lipstick / 口红; choose a light dusty-pink style by description, such as Lipstick-8                                          |
| 腮红、眼线、睫毛 / blush, eyeliner, lashes              | Blush / 腮红; Eyeliner / 眼线; Lashes / 睫毛                                                                                 |
| 修容、高光 / contour or highlight makeup                | Contour / 修容; Highlight / 高光                                                                                             |
| 瘦腰、瘦手臂、长腿 / slim waist, slim arms, longer legs | Body: Slim waist / 瘦腰; Slim arms / 瘦手臂; Longer legs / 长腿                                                              |

For “slim the jaw a little and add a soft pink lip,” combine Jaw width with one
light pink Lipstick style and its amount; do not stack multiple face-slimming controls.
Saved presets are the user's own and reachable by name through the catalog's
preset workflow. There are no built-in presets, makeup sets, skin-tone controls,
or manual brushes in this agent workflow.

## Start gently, then judge the rendered footage

The reference extremes show pronounced shape changes and smoothing at 100;
makeup reference previews are amplified up to 2×. The following are conservative
starting heuristics on the catalog's numeric scale, not verified optimum values:

| Adjustment                                         | Initial value from neutral                                                         |
| -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Skin smoothing                                     | 10–25 on 0–100                                                                     |
| Requested skin brightening or clarity              | 5–10 on 0–100                                                                      |
| Local skin corrections                             | 10–20 on 0–100                                                                     |
| Face, jaw, eye, or nose shaping                    | 5–15 on 0–100                                                                      |
| Two-way feature position or size                   | 3–8 in the intended direction; check the catalog's sign                            |
| Lipstick, blush, eye makeup, contour, or highlight | Omit `amount` to use the style's default, about 60–80; lower it if too strong      |
| Body proportions                                   | 20–40 on 0–100, 10–20 on -50..50; 瘦腰、丰胸、美胯 stay subtle even at their limit |

Use small changes from existing values when already adjusted. Go further when
requested or when the actual preview shows the intended change is still insufficient;
raise one control at a time and preview again. Keep skin texture and recognizable
features, and reduce strength if contours, makeup edges, or background lines distort.
A weak effect on one frame is not a reason to maximize every control.

Body has no per-person choice. With several people in frame, the engine applies most
Body controls to just one of them and 长腿 stretches the whole lower frame, so tell the
user when the preview shows that this is not what they asked for.
