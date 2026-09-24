---
name: picase-sync
description: Refresh the Picase 案件台 dashboard from Google Workspace and republish the artifact. Use when Klaus says /picase-sync, "sync 一下", "更新 dashboard", "板子刷新", or after files have been renamed, filed, or added in a case folder and the board should reflect it.
---

# picase-sync — refresh the board

The board is a **static snapshot**. Nothing on it updates by itself. This skill
is the whole refresh: Google Workspace → database → payload → built page →
published artifact, at the same URL every time.

## Run it

```bash
cd ~/lingtu-cms && ./sync.sh            # full — Sheets, Drive, Chat, case folders (~2 min)
cd ~/lingtu-cms && ./sync.sh --quick    # case folders only (~20 s)
```

Use `--quick` when only Drive changed — a file renamed, filed into a subfolder,
or newly uploaded. Use the full run when the tracking sheet, the ops sheet, or
Chat changed, or when you are not sure.

`sync.sh` backs up `data/cms.db` before a full run and keeps the last five
backups. A failed pull therefore costs nothing; restore with
`cp data/cms.db.bak-<stamp> data/cms.db`.

## Then publish

The script stops at a built file because publishing is not something a shell can
do. Finish it:

```
Artifact: url=https://claude.ai/artifact/FnTCxBaNVDHbDVgaN9jcxg
          file_path=~/lingtu-cms/board/picase-board.html
```

**Always pass that `url`.** Publishing without it creates a second board, and
Klaus's own edits (status, titles, attachments, colours) live in `localStorage`
keyed to the artifact's origin — a new URL loses every one of them.

If the Artifact tool refuses the publish because this conversation has not read
the artifact yet, read it first (`action: "read"` with that url), then publish.

## What actually runs

| Step | Script | Reads | Writes |
|---|---|---|---|
| 1 | `sync/run_all.py` | Tracking sheet, ops sheet, Activity Log, 控制台 Tasks, Drive case folders, Chat spaces | `data/cms.db` |
| 2 | `sync/scan_litigation.py` | every litigation case folder's filenames, court e-file stamps, One Legal receipts | `data/lit_docs.json` |
| 3 | `board/export.py` | `cms.db` + `lit_docs.json` | `board/data.json` |
| 4 | `board/build.py` | `head.html` + `body.html` + `data.json` | `board/picase-board.html` |

Every Google read goes through the **`gws` CLI** as `klaus@lingtulaw.com`
(`sync/gws_api.py` is a thin wrapper over it). Read-only: nothing in this path
writes to Drive, Sheets, or Gmail.

## Limits worth stating out loud

- **Klaus's board edits never come back.** Statuses, renamed rows, hand-attached
  documents and highlights live only in his browser. The sync cannot read them,
  and nothing here overwrites them — rows are matched by a stable event id.
- **`board/data.json` is regenerated every run.** Anything hand-added to it is
  lost unless it is folded into `export.py` (see `BILL_EXTRACT` and `SEC_EN`
  there for the pattern).
- **A file has to be named to the canonical grammar to become an event.**
  `<M-D-YYYY> <Type>(<party>)[ - <part>].ext`. A file that does not parse still
  appears under Documents; it just does not land on the timeline.
