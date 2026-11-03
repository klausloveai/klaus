# File → PDF conversion

The finalized folder mixes `.pdf`, `.docx`, `.pptx` and images. Every route below has a
silent-failure mode that yields a PDF with the *wrong content* rather than an error, so
**verify every conversion against its source** before merging.

Verification that works: normalise both texts, cut the source into 40-character shingles, and
require ~60% to appear in the PDF. Do not use a prefix match — generated documents reorder
text boxes and headers, so a correct conversion can fail a prefix test.

Note a crude XML text dump of a `.docx` also picks up drawing-shape ids (long digit strings),
so overlay-heavy files legitimately score low. Render those and look rather than failing them
automatically.

---

## .docx → PDF

**Default route: Google Drive.** Copy the file to a native Google Doc, export as PDF, delete
the copy. Fully scriptable, parallelises about five wide, no GUI:

```
gws drive files copy  --params '{"fileId":"<ID>","supportsAllDrives":true}' \
                      --json   '{"mimeType":"application/vnd.google-apps.document","name":"TMPCONV"}'
gws drive files export --params '{"fileId":"<COPY_ID>","mimeType":"application/pdf"}' -o out.pdf
gws drive files delete --params '{"fileId":"<COPY_ID>","supportsAllDrives":true}'
```

Run with `cwd` set to the output directory and a bare `-o` filename — `gws` rejects paths
outside the current directory.

**Drive drops Word text boxes.** A screenshot-with-English-callouts translation comes out with
the overlay missing entirely — the PDF renders the image and nothing else. Any translation
whose English sits in text boxes over a screenshot must go through Word.

**Word is the only faithful renderer for text-box overlays**, and every one of its traps is
silent:

- Sandboxed: cannot read or write `/private/tmp`. Stage files under `~/Documents`.
- Refuses paths longer than ~255 bytes. Copy to a short temp name first.
- `open POSIX file X` returns nothing, so you must use `active document`. When the open
  silently fails, `active document` is still the *previous* file and save-as writes the wrong
  content under the right name.
- Save-as-PDF does **not** close the source. Documents pile up until Word stops opening
  anything. Always close: `repeat with i from (count of documents) to 1 by -1 / close document i saving no`.
- `close document "name"` is unsupported (-1708); only `close document <index>` works — so
  never close by index while the user has their own documents open. Note which documents were
  already open, and restore them afterwards.
- Polling `name of active document` in a tight AppleScript `repeat` starves Word's event loop
  and the open never completes. Use a plain open + save-as with no polling.
- Once wedged, only a full quit + `pkill -9` + relaunch recovers it.

**Pages** opens `.docx` and scripts easily, but renders Word text boxes as black-filled boxes
with invisible text. Not usable for overlay translations.

## .pptx → PDF

Keynote:

```applescript
tell application "Keynote"
  set d to open POSIX file "<in.pptx>"
  export d to file ((POSIX file "<out.pdf>") as text) as PDF
  close d saving no
end tell
```

The `as text` coercion on the destination matters; without it the export fails.

## Images → PDF

`scripts/img2pdf.py` places each image on a US Letter page with 0.5-inch margins, centred.

Very tall captures (aspect ratio > 2.5, e.g. a full-page mobile scroll at 1179×12210) get
sliced into full-width segments. Fitting one of those onto a single page shrinks it to
illegibility, which defeats the purpose of filing it.

HEIC/HEIF files (common from iPhone, sometimes with a `.JPG` extension) need
`sips -s format png in.JPG --out out.png` first — PIL cannot open them.
