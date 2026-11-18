# Import an existing animation

Import the completed deliverable into the task project at the most editable
level verified to work. Keep original source in the project workspace.

For Remotion source, read Runtime APIs first: use a composition entry rather
than its registration root, pass `item.props` to it, expose editable properties,
and use the composition's real width, height and duration. Only registered
modules resolve; fonts load by family name. Validate the actual entry through
`push_asset` with `type:"motion-graphic"`, inspect its saved properties and compare
composed frames with the original. An adapter is not proof of conversion.

For HTML/GSAP/canvas source, follow the HTML runtime contract and seek animation
from supplied timeline time rather than autonomous tickers. Lottie JSON needs a
supported wrapper, not a raw source import. Do not claim arbitrary animation
formats work without testing them.

If source cannot run faithfully, render with its original tool and import the
finished file after rendering succeeds. Use H.264 MP4 for opaque full-frame
pieces; for transparent overlays prefer ProRes 4444 MOV and verify alpha over
footage. Do not promise WebM/HEVC alpha or animated SVG/APNG support without a
verified composed result. Describe a rendered asset as video: its internal
text/layers are not editable in ChatCut. Offer the preserved source separately.

Import only the deliverable, never its folder, previews or earlier drafts.
Reuse the existing asset/item for a revision when supported; do not assume
`push_asset` deduplicates or that overwriting source automatically refreshes an
open project. Verify after each update and report any unresolved refresh.
