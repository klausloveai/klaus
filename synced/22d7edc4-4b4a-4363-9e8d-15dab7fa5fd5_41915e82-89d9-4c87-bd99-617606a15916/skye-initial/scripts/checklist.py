#!/usr/bin/env python3
"""Read and write the 材料清单 Google Doc in the firm's house format.

Four subcommands:

  dump    — the doc as indented plain text, with a section map (indices + names)
  init    — write a whole checklist into the blank doc skye-case-drive created
  insert  — add lines to the end of one named section of an existing checklist
  mark    — stamp ✅ / （已有） onto an existing line

## Why `insert` exists, and why there is no "rewrite"

These docs are worked in by hand. Every real sample carries Google Docs comment
threads — the attorney asking "两位 principal 可以吗", the paralegal answering
underneath — anchored to specific characters, plus 客户 replies and inline
edits made between our runs. Replacing the body wholesale orphans every one of
those comments and silently discards edits nobody told us about. So a client's
new upload never triggers a rewrite: it appends a line to the right section,
or ticks a line that's already there. The doc accumulates rather than being
regenerated, which is also how the humans use it.

`init` is the one exception, and it refuses to run on a doc that already has
content unless you pass --force.

## Source-text format (for init / insert)

  @title   Qing Yang EB1A 材料清单     bold title line
  @meta    DDL：10/01/2026             plain line under the title
  @urgent  加急                        plain line, yellow highlight
  @section 奖项：                      section header (blank line inserted above)
  @hr                                  the ________________ divider (dual-track)
  @blank                               an empty line
  * text                               bullet, level 0
  \t* text                             bullet, level 1 (one tab per level)

House format, read off the live samples: Times New Roman 12pt throughout, the
title bold, section headers plain text ending in a full-width colon, body as
disc bullets nested with tabs. Nothing is a Docs Heading style — the firm's
docs use none, and introducing them would make new checklists render
differently from every existing one.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gwslib import GwsError, gws  # noqa: E402

FONT = {"weightedFontFamily": {"fontFamily": "Times New Roman"},
        "fontSize": {"magnitude": 12, "unit": "PT"}}
YELLOW = {"color": {"rgbColor": {"red": 1, "green": 1}}}


# --------------------------------------------------------------------------- #
# source text -> pieces
# --------------------------------------------------------------------------- #

def parse_source(text):
    pieces = []
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("@title "):
            pieces.append({"kind": "title", "text": stripped[7:].strip(), "level": 0})
        elif stripped.startswith("@meta "):
            pieces.append({"kind": "meta", "text": stripped[6:].strip(), "level": 0})
        elif stripped.startswith("@urgent "):
            pieces.append({"kind": "urgent", "text": stripped[8:].strip(), "level": 0})
        elif stripped.startswith("@section "):
            pieces.append({"kind": "blank", "text": "", "level": 0})
            pieces.append({"kind": "section", "text": stripped[9:].strip(), "level": 0})
        elif stripped == "@hr":
            pieces.append({"kind": "meta", "text": "________________", "level": 0})
        elif stripped == "@blank" or not stripped:
            pieces.append({"kind": "blank", "text": "", "level": 0})
        else:
            level = len(line) - len(line.lstrip("\t"))
            body = line.lstrip("\t")
            if body.startswith("* "):
                body = body[2:]
            elif body.startswith("*"):
                body = body[1:]
            pieces.append({"kind": "bullet", "text": body.strip(), "level": level})
    # A leading blank (from a first @section) just adds a stray empty line.
    while pieces and pieces[0]["kind"] == "blank":
        pieces.pop(0)
    return pieces


def assemble(pieces, leading_newlines=0):
    """Return (text, spans). Spans carry offsets relative to the text start."""
    out, spans = [], []
    cursor = leading_newlines
    out.append("\n" * leading_newlines)
    for p in pieces:
        # A bullet's nesting level is expressed as leading tabs; the Docs API
        # reads them, applies the nesting, and strips them. That is the only
        # supported way to create a nested list in one pass.
        body = ("\t" * p["level"] + p["text"]) if p["kind"] == "bullet" else p["text"]
        chunk = body + "\n"
        spans.append({"start": cursor, "end": cursor + len(chunk),
                      "kind": p["kind"], "level": p["level"]})
        out.append(chunk)
        cursor += len(chunk)
    return "".join(out), spans


def style_requests(base_index, text, spans, trailing_newline=True, start_offset=0):
    """Requests that follow the insertText, in an order whose indices stay valid.

    Text-style and paragraph-style updates don't change the document's length,
    so they can be computed straight off the inserted string. createParagraphBullets
    *does* shorten the text (it consumes the leading tabs), so those go last and
    run back-to-front — a later range can't disturb an earlier one it sits after.
    """
    reqs = []
    total = len(text)
    end = base_index + total
    if trailing_newline:
        end -= 1  # never include the closing newline of the last paragraph
    # start_offset skips a leading newline that belongs to the paragraph above
    # the insertion point — without it the paragraph-level requests below would
    # reach back and strip that paragraph's own bullet.
    start = base_index + start_offset
    if end <= start:
        return reqs
    whole = {"startIndex": start, "endIndex": end}

    # Text inserted directly after a bulleted paragraph joins that paragraph's
    # list at its nesting level, and createParagraphBullets then leaves it
    # there regardless of how many leading tabs the new text carries — a
    # top-level bullet appended under a level-2 line comes out at level 2.
    # Stripping list membership first makes the tab count the only thing that
    # decides nesting. Neither this nor the style updates below change the
    # document's length, so the offsets stay valid.
    reqs.append({"deleteParagraphBullets": {"range": whole}})

    reqs.append({"updateParagraphStyle": {
        "range": whole,
        "paragraphStyle": {"namedStyleType": "NORMAL_TEXT",
                           "indentStart": {"magnitude": 0, "unit": "PT"},
                           "indentFirstLine": {"magnitude": 0, "unit": "PT"}},
        "fields": "namedStyleType,indentStart,indentFirstLine"}})

    # Inserted text inherits the style of whatever character precedes it, which
    # in these docs is regularly a bold header or a blue underlined link. Reset
    # explicitly rather than hoping the insertion point is clean.
    reqs.append({"updateTextStyle": {
        "range": whole,
        "textStyle": {"bold": False, "italic": False, "underline": False,
                      "foregroundColor": {"color": {"rgbColor": {}}},
                      "backgroundColor": {},
                      **FONT},
        "fields": ("bold,italic,underline,foregroundColor,backgroundColor,"
                   "weightedFontFamily,fontSize,link")}})

    for s in spans:
        if s["kind"] not in ("title", "urgent"):
            continue
        r = {"startIndex": base_index + s["start"], "endIndex": base_index + s["end"] - 1}
        if r["endIndex"] <= r["startIndex"]:
            continue
        style = {"bold": True}
        fields = "bold"
        if s["kind"] == "urgent":
            style["backgroundColor"] = YELLOW
            fields += ",backgroundColor"
        reqs.append({"updateTextStyle": {"range": r, "textStyle": style, "fields": fields}})

    runs, current = [], None
    for s in spans:
        if s["kind"] == "bullet":
            if current is None:
                current = [s["start"], s["end"]]
            else:
                current[1] = s["end"]
        elif current is not None:
            runs.append(current)
            current = None
    if current is not None:
        runs.append(current)

    for start, stop in reversed(runs):
        reqs.append({"createParagraphBullets": {
            "range": {"startIndex": base_index + start, "endIndex": base_index + stop - 1},
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})
    return reqs


# --------------------------------------------------------------------------- #
# reading the doc
# --------------------------------------------------------------------------- #

def get_doc(doc_id):
    return gws(["docs", "documents", "get"], params={"documentId": doc_id})


def paragraphs(doc):
    out = []
    for el in doc.get("body", {}).get("content", []):
        p = el.get("paragraph")
        if not p:
            continue
        text = "".join(r["textRun"]["content"] for r in p.get("elements", [])
                       if "textRun" in r)
        bullet = p.get("bullet")
        out.append({"start": el["startIndex"], "end": el["endIndex"],
                    "text": text.rstrip("\n"),
                    "bullet": bullet is not None,
                    "level": bullet.get("nestingLevel", 0) if bullet else None})
    return out


def body_end(doc):
    content = doc.get("body", {}).get("content", [])
    return content[-1]["endIndex"] if content else 2


def section_index(paras):
    """Non-bulleted, non-empty lines are the section headers in this format."""
    return [p for p in paras if not p["bullet"] and p["text"].strip()
            and p["text"].strip() != "________________"]


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #

def cmd_dump(args):
    doc = get_doc(args.doc_id)
    paras = paragraphs(doc)
    if args.json:
        json.dump({"title": doc.get("title"), "paragraphs": paras,
                   "sections": [{"text": p["text"], "start": p["start"]}
                                for p in section_index(paras)]},
                  sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    print(f"# {doc.get('title')}  ({args.doc_id})")
    for p in paras:
        if p["bullet"]:
            print("\t" * p["level"] + "* " + p["text"])
        else:
            print(p["text"])
    print("\n--- sections ---")
    for p in section_index(paras):
        print(f"[{p['start']}] {p['text']}")


def cmd_init(args):
    src = open(args.source, encoding="utf-8").read() if args.source else sys.stdin.read()
    pieces = parse_source(src)
    if not pieces:
        sys.exit("source is empty")

    doc = get_doc(args.doc_id)
    existing = "".join(p["text"] for p in paragraphs(doc)).strip()
    if existing and not args.force:
        sys.exit(f"doc {args.doc_id} already has content ({len(existing)} chars) — "
                 "use `insert` to add to it, or --force to overwrite from scratch")

    requests = []
    if existing and args.force:
        requests.append({"deleteContentRange": {
            "range": {"startIndex": 1, "endIndex": body_end(doc) - 1}}})

    text, spans = assemble(pieces)
    requests.append({"insertText": {"location": {"index": 1}, "text": text}})
    requests += style_requests(1, text, spans)

    if args.dry_run:
        json.dump({"doc_id": args.doc_id, "requests": requests},
                  sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    gws(["docs", "documents", "batchUpdate"], params={"documentId": args.doc_id},
        body={"requests": requests})
    print(json.dumps({"doc_id": args.doc_id, "status": "written",
                      "paragraphs": len(pieces),
                      "link": f"https://docs.google.com/document/d/{args.doc_id}/edit"},
                     ensure_ascii=False))


def cmd_insert(args):
    src = open(args.source, encoding="utf-8").read() if args.source else sys.stdin.read()
    pieces = parse_source(src)
    if not pieces:
        sys.exit("source is empty")

    doc = get_doc(args.doc_id)
    paras = paragraphs(doc)
    sections = section_index(paras)
    end_of_body = body_end(doc)

    if args.section:
        target = None
        want = args.section.strip().rstrip("：:")
        for p in sections:
            if p["text"].strip().rstrip("：:") == want:
                target = p
                break
        if target is None:
            for p in sections:
                if want in p["text"]:
                    target = p
                    break
        if target is None:
            names = "\n".join(f"  - {p['text']}" for p in sections)
            sys.exit(f"section {args.section!r} not found. Sections in this doc:\n{names}")
        # End of the section = just past its last non-empty line. Stopping at
        # the last *non-empty* line keeps the new bullets above the blank
        # separator rather than orphaned in the gap before the next section.
        insert_at = target["end"]
        started = False
        for p in paras:
            if p["start"] < target["start"]:
                continue
            if p["start"] == target["start"]:
                started = True
                continue
            if not started:
                continue
            if not p["bullet"] and p["text"].strip():
                break
            if p["text"].strip():
                insert_at = p["end"]
    else:
        insert_at = max(p["end"] for p in paras if p["text"].strip()) if any(
            p["text"].strip() for p in paras) else 1

    # Splice in *before* the preceding paragraph's newline and carry two
    # newlines at the front: the first terminates that paragraph, the second
    # forms a throwaway empty paragraph that the new bullets sit under.
    #
    # The empty paragraph is what makes nesting come out right. createParagraph-
    # Bullets reads nesting from leading tabs only when the paragraph above the
    # range is not itself a list item; run it directly under a level-1 bullet
    # and every new line lands one level deeper than its tab count asked for —
    # a top-level bullet appended below a sub-bullet becomes a sub-bullet.
    # Clearing the inherited bullets first does not help; the neighbour still
    # sets the baseline. A plain paragraph in between breaks that inheritance,
    # and deleting it afterwards leaves the levels alone. Entering one character
    # early is also the only form that works at the very end of the body, where
    # index end_of_body-1 is the final newline and nothing may follow it.
    insert_at = min(max(insert_at - 1, 1), end_of_body - 1)
    text, spans = assemble(pieces, leading_newlines=2)
    text = text[:-1]
    spans[-1]["end"] -= 1

    requests = [{"insertText": {"location": {"index": insert_at}, "text": text}}]
    requests += style_requests(insert_at, text, spans, trailing_newline=False,
                               start_offset=1)
    # Last, so the bullet requests above still see the indices they were built
    # from — everything this shifts sits after it.
    requests.append({"deleteContentRange": {
        "range": {"startIndex": insert_at + 1, "endIndex": insert_at + 2}}})

    if args.dry_run:
        json.dump({"doc_id": args.doc_id, "insert_at": insert_at, "requests": requests},
                  sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    gws(["docs", "documents", "batchUpdate"], params={"documentId": args.doc_id},
        body={"requests": requests})
    clean_trailing_bullet(args.doc_id)
    print(json.dumps({"doc_id": args.doc_id, "section": args.section,
                      "inserted_at": insert_at, "lines": len(pieces),
                      "status": "inserted"}, ensure_ascii=False))


def clean_trailing_bullet(doc_id):
    """Un-bullet the empty paragraph Docs keeps at the end of the body.

    Appending at the very end consumes the document's final newline, and Docs
    then re-creates a closing paragraph that inherits the bullet from the line
    above it — leaving a stray empty bullet under the last real one. Runs as
    its own call because the indices it needs only exist after the insert.
    """
    doc = get_doc(doc_id)
    paras = paragraphs(doc)
    if not paras:
        return
    last = paras[-1]
    if last["text"].strip() or not last["bullet"]:
        return
    gws(["docs", "documents", "batchUpdate"], params={"documentId": doc_id},
        body={"requests": [{"deleteParagraphBullets": {
            "range": {"startIndex": last["start"], "endIndex": last["end"]}}}]})


def cmd_mark(args):
    doc = get_doc(args.doc_id)
    paras = paragraphs(doc)
    hits = [p for p in paras if args.match in p["text"]]
    if not hits:
        sys.exit(f"no line contains {args.match!r}")
    if len(hits) > 1 and not args.all:
        listing = "\n".join(f"  [{h['start']}] {h['text']}" for h in hits)
        sys.exit(f"{len(hits)} lines match {args.match!r} — narrow the match, "
                 f"or pass --all:\n{listing}")

    requests = []
    for h in sorted(hits, key=lambda h: h["start"], reverse=True):
        if args.marker in h["text"]:
            continue
        requests.append({"insertText": {"location": {"index": h["end"] - 1},
                                        "text": args.marker}})
    if not requests:
        print(json.dumps({"doc_id": args.doc_id, "status": "already marked"},
                         ensure_ascii=False))
        return
    if args.dry_run:
        json.dump({"doc_id": args.doc_id, "requests": requests,
                   "lines": [h["text"] for h in hits]},
                  sys.stdout, ensure_ascii=False, indent=2)
        print()
        return
    gws(["docs", "documents", "batchUpdate"], params={"documentId": args.doc_id},
        body={"requests": requests})
    print(json.dumps({"doc_id": args.doc_id, "marked": [h["text"] for h in hits],
                      "marker": args.marker}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("dump", help="read the checklist as text + section map")
    p.add_argument("--doc-id", required=True)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_dump)

    p = sub.add_parser("init", help="write a full checklist into a blank doc")
    p.add_argument("--doc-id", required=True)
    p.add_argument("--source", help="source text file (default: stdin)")
    p.add_argument("--force", action="store_true", help="overwrite an already-filled doc")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("insert", help="append lines to one section")
    p.add_argument("--doc-id", required=True)
    p.add_argument("--section", help="section header text; omit to append at the end")
    p.add_argument("--source", help="source text file (default: stdin)")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_insert)

    p = sub.add_parser("mark", help="stamp a marker onto an existing line")
    p.add_argument("--doc-id", required=True)
    p.add_argument("--match", required=True, help="substring identifying the line")
    p.add_argument("--marker", default=" ✅")
    p.add_argument("--all", action="store_true", help="mark every matching line")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_mark)

    args = ap.parse_args()
    try:
        args.func(args)
    except GwsError as exc:
        sys.exit(f"gws error: {exc}")


if __name__ == "__main__":
    main()
