#!/usr/bin/env python3
"""Build a 人才移民 case Drive folder (O1 / EB1A / NIW) in one shot.

Creates the case root, the standard subfolder set, copies the case type's
petition-letter templates into "3. Draft Petition Letter", and (optionally)
writes the intake note into a Google Doc under "0. Intake".

Everything it touches lives in the "人才移民" shared drive, so every Drive call
carries the allDrives params — without them the API answers "no such file"
instead of erroring, which is the single most common way this workflow
silently half-succeeds.

Usage:
  python3 build_case_drive.py --case-type EB1A --client-name "Xuan Shen" \
      [--intake-note-file note.txt] [--intake-note "..."] \
      [--include-rfe] [--dry-run] [--force]

Prints a JSON report on stdout: folder ids, links, what was copied, what was
skipped. Non-zero exit means nothing downstream (sharing, tracking sheet)
should be attempted.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import criteria_folders  # noqa: E402  (sibling module — the statutory folder layouts)
import upload_email  # noqa: E402  (sibling module — the email wording lives there)

DRIVE_ID = "0AIXy3tjXMf-MUk9PVA"  # 人才移民 shared drive

# label -> where client folders live, and which folder holds that type's
# petition-letter templates. Both were read off the live Drive; if the firm
# reorganizes, re-read them rather than patching names here.
CASE_TYPES = {
    "O1": {
        "parent": "1-g_HDMHwSi7PtV5Nlyw1nUCwXGbQkwpS",   # "O-1"
        "pl_folder": "1KlSs38B0r4XWDSIJRw5m7puEZXttb4Qi",  # 0 Sample（O1）/2. Cover-PL-Index
    },
    "EB1A": {
        "parent": "1rDPCJzYAiG13SzJjkrTqc9D7eUxU12xR",
        "pl_folder": "1NPZYMtv4fEQm9hNkd1o_ZZ0ndSLaoaYu",
    },
    "NIW": {
        "parent": "1D7hKuq2qi4daqIegvjM3YUiN3WKsawjy",
        "pl_folder": "1yTrJRlTCr9bpR_lSFdWqdRjBNVxtpKBi",
    },
}

# Fixed order, roughly the case's chronology. The two 0-prefixed folders are
# deliberate: "0. Shared Folder" is the only one the client ever sees, kept
# adjacent to "0. Intake" so nobody shares the wrong one by muscle memory.
#
# "3. Petition Letter & Exhibits" holds the letter AND the exhibits together
# because the firm no longer drafts a whole PL up front — it writes one
# criterion at a time alongside that criterion's exhibits and the index, so
# splitting them across two folders just means working in two windows.
BASE_SUBFOLDERS = [
    "0. Intake",
    "0. Shared Folder",
    "1. Initial",
    "2. Form",
    "3. Petition Letter & Exhibits",
    "4. Final Scanned",
    "5. RFE",
    "6. Approval Letter",
]


def subfolders_for(case_key):
    """Folder list for a case type, numbered without gaps.

    O-1 is a nonimmigrant visa, so it never reaches the National Visa Center —
    an NVC folder on an O-1 case is a folder that stays empty forever and makes
    people wonder what they forgot to put in it. EB1A and NIW are immigrant
    petitions and do get one.
    """
    folders = list(BASE_SUBFOLDERS)
    if case_key != "O1":
        folders.append("7. NVC Letter")
    # Number 弃用 off the last folder rather than off len(folders) — the two
    # 0-prefixed folders would otherwise push the count two ahead of the
    # numbering and leave a gap.
    last = int(folders[-1].split(".", 1)[0])
    folders.append(f"{last + 1}. 弃用")
    return folders


PL_FOLDER = "3. Petition Letter & Exhibits"

FOLDER_MIME = "application/vnd.google-apps.folder"
DOC_MIME = "application/vnd.google-apps.document"

ALL_DRIVES = {
    "supportsAllDrives": True,
    "includeItemsFromAllDrives": True,
    "corpora": "allDrives",
}


class GwsError(RuntimeError):
    pass


def gws(args, params=None, body=None):
    cmd = ["gws"] + args
    if params is not None:
        cmd += ["--params", json.dumps(params, ensure_ascii=False)]
    if body is not None:
        cmd += ["--json", json.dumps(body, ensure_ascii=False)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise GwsError(f"{' '.join(args)} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    out = proc.stdout.strip()
    if not out:
        return {}
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        raise GwsError(f"{' '.join(args)} returned non-JSON: {out[:400]}")
    if isinstance(data, dict) and "error" in data:
        raise GwsError(f"{' '.join(args)}: {json.dumps(data['error'], ensure_ascii=False)}")
    return data


def list_children(folder_id, fields="files(id,name,mimeType)"):
    params = dict(ALL_DRIVES)
    params.update({
        "q": f"'{folder_id}' in parents and trashed=false",
        "fields": fields,
        "orderBy": "name",
        "pageSize": 200,
    })
    return gws(["drive", "files", "list"], params=params).get("files", [])


def create_folder(name, parent):
    return gws(
        ["drive", "files", "create"],
        params={"supportsAllDrives": True, "fields": "id,name"},
        body={"name": name, "mimeType": FOLDER_MIME, "parents": [parent]},
    )


def link(folder_id):
    return f"https://drive.google.com/drive/folders/{folder_id}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case-type", required=True, help="O1 | EB1A | NIW (case-insensitive; O-1/O1A accepted)")
    ap.add_argument("--client-name", required=True, help="Client's English full name, e.g. 'Xuan Shen'")
    ap.add_argument("--folder-name", help="Override the case root folder name entirely")
    ap.add_argument("--intake-note")
    ap.add_argument("--intake-note-file")
    ap.add_argument("--client-email", help="Recorded in the intake doc only; sharing is a separate step")
    ap.add_argument("--include-rfe", action="store_true",
                    help="Also copy RFE-specific templates (skipped by default — they only apply once an RFE arrives)")
    ap.add_argument("--force", action="store_true", help="Build even if a same-named folder already exists")
    ap.add_argument("--lang", default="zh", choices=["zh", "en"],
                    help="Language of the client's upload-instructions doc")
    ap.add_argument("--numbered-criteria", action="store_true",
                    help="Prefix each statutory criterion folder with its number from the regulation")
    ap.add_argument("--no-checklist", action="store_true",
                    help="Skip the blank 材料清单 doc in the case root")
    ap.add_argument("--no-email-doc", action="store_true",
                    help="Skip writing the upload-instructions doc into 0. Shared Folder")
    ap.add_argument("--parent", help="Testing only: build under this folder instead of the case type's real parent")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    given = args.case_type.strip().upper().replace("-", "").replace(" ", "")
    # O-1A vs O-1B share one Drive tree but stay distinct in the tracking sheet,
    # so keep the subtype around for the intake doc and the report.
    subtype = {"O1A": "O-1A", "O1B": "O-1B", "O1": "O-1"}.get(given, given)
    key = "O1" if given in ("O1A", "O1B", "O1") else given
    if key not in CASE_TYPES:
        sys.exit(f"unknown case type {args.case_type!r}; expected one of O1 / EB1A / NIW")
    cfg = dict(CASE_TYPES[key])
    if args.parent:
        cfg["parent"] = args.parent

    client = " ".join(args.client_name.split())
    # O-1 folders carry the A/B subtype (O1A / O1B) so the folder name matches
    # the tracking sheet at a glance. Plain "O1" is fine when intake hasn't
    # settled A vs B yet — the team renames it by hand once the case starts.
    name_suffix = given if given in ("O1A", "O1B") else key
    root_name = args.folder_name or f"{client} {name_suffix}"

    note = args.intake_note
    if args.intake_note_file:
        with open(args.intake_note_file, encoding="utf-8") as fh:
            note = fh.read()

    report = {
        "case_type": key,
        "case_subtype": subtype,
        "client_name": client,
        "root_folder_name": root_name,
        "dry_run": bool(args.dry_run),
    }

    # Duplicate check first — a second folder for the same client is worse than
    # a failed run, because the two then drift apart silently and half the team
    # ends up working in the stale one.
    #
    # Exact-name matching alone isn't enough here: older cases in this drive are
    # named with no case type at all ("Qing Yang", "Cheng Chen"), and finished
    # ones get a ✅ or a specialty appended ("Yizhen Zhang EB1A 摄影师"). So also
    # look for anything that merely *starts with* the client's name. That's a
    # softer signal — a client can legitimately have two cases under the same
    # parent — so it's reported as a warning and the build continues, while an
    # exact name match still stops the run.
    siblings = list_children(cfg["parent"], fields="files(id,name)")
    def _norm(x):
        return " ".join(x.split()).strip().lower()
    exact = [f for f in siblings if _norm(f["name"]) == _norm(root_name)]
    similar = [f for f in siblings
               if f not in exact and _norm(f["name"]).startswith(_norm(client))]
    if exact and not args.force:
        report["error"] = "duplicate"
        report["existing"] = [{"id": f["id"], "name": f["name"], "link": link(f["id"])} for f in exact]
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(2)
    report["duplicate_overridden"] = bool(exact and args.force)
    if similar:
        report["possible_existing_cases"] = [
            {"id": f["id"], "name": f["name"], "link": link(f["id"])} for f in similar]

    templates = [f for f in list_children(cfg["pl_folder"]) if f["mimeType"] != FOLDER_MIME]
    to_copy, skipped = [], []
    for f in templates:
        if not args.include_rfe and "rfe" in f["name"].lower():
            skipped.append(f["name"])
        else:
            to_copy.append(f)
    report["templates_to_copy"] = [f["name"] for f in to_copy]
    report["templates_skipped"] = skipped

    if args.dry_run:
        report["subfolders"] = subfolders_for(key)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    root = create_folder(root_name, cfg["parent"])
    report["root_folder_id"] = root["id"]
    report["root_folder_link"] = link(root["id"])

    subs = {}
    for name in subfolders_for(key):
        created = create_folder(name, root["id"])
        subs[name] = created["id"]
    report["subfolders"] = {n: {"id": i, "link": link(i)} for n, i in subs.items()}
    report["shared_folder_id"] = subs["0. Shared Folder"]
    report["shared_folder_link"] = link(subs["0. Shared Folder"])

    draft_id = subs[PL_FOLDER]
    copied = []
    for f in to_copy:
        made = gws(
            ["drive", "files", "copy"],
            params={"fileId": f["id"], "supportsAllDrives": True, "fields": "id,name"},
            body={"name": f["name"], "parents": [draft_id]},
        )
        copied.append({"name": made.get("name", f["name"]), "id": made["id"]})
    report["templates_copied"] = copied

    # One subfolder per statutory criterion, plus the case type's non-criterion
    # pieces. Built for every criterion the law lists, not just the ones this
    # case will claim — which three-or-more carry the case isn't known until the
    # background materials are in, and pruning a folder is faster than hunting
    # down the regulation to add one.
    crit_names = criteria_folders.folders_for(subtype, numbered=args.numbered_criteria)
    if crit_names:
        report["criteria_folders"] = criteria_folders.create_in(draft_id, crit_names)
    else:
        # Plain "O1" with no A/B: the two subtypes share almost no criteria, so
        # scaffolding one would mean building the wrong case.
        report["criteria_folders_skipped"] = (
            "O-1 subtype (A or B) not set — rerun criteria_folders.py once it is")

    # The client's upload instructions live in the case root as a doc, not as
    # one person's Gmail draft — whoever ends up emailing the client can copy it
    # from the case folder. Deliberately NOT inside "0. Shared Folder": that one
    # is client-visible, and a doc telling staff what to send the client isn't
    # something the client should be reading over our shoulder.
    if not args.no_email_doc:
        subject, _, doc_text = upload_email.compose(
            client, subtype, report["shared_folder_link"],
            to=args.client_email, lang=args.lang)
        info = upload_email.write_doc(root["id"], client, doc_text,
                                      lang=args.lang)
        info["subject"] = subject
        report["upload_email_doc"] = info

    # A blank 材料清单 in the case root. Deliberately empty: it gets filled in
    # live during the meeting with the client, criterion by criterion, and a
    # pre-filled template would just be text someone has to delete first.
    if not args.no_checklist:
        cl = gws(
            ["drive", "files", "create"],
            params={"supportsAllDrives": True, "fields": "id,name"},
            body={"name": f"{client} 材料清单", "mimeType": DOC_MIME,
                  "parents": [root["id"]]},
        )
        report["checklist_doc"] = {
            "doc_id": cl["id"], "doc_name": cl.get("name", f"{client} 材料清单"),
            "doc_link": f"https://docs.google.com/document/d/{cl['id']}/edit"}

    if note and note.strip():
        doc = gws(
            ["drive", "files", "create"],
            params={"supportsAllDrives": True, "fields": "id,name"},
            body={"name": f"Intake Note - {client}", "mimeType": DOC_MIME,
                  "parents": [subs["0. Intake"]]},
        )
        header = [
            "Intake Note",
            "",
            f"客户姓名：{client}",
            f"案件类型：{subtype}",
        ]
        if args.client_email:
            header.append(f"客户邮箱：{args.client_email}")
        header += [f"登记日期：{date.today().isoformat()}", "", "Intake 备注", note.rstrip(), ""]
        gws(["docs", "+write", "--document", doc["id"], "--text", "\n".join(header)])
        report["intake_doc_id"] = doc["id"]
        report["intake_doc_link"] = f"https://docs.google.com/document/d/{doc['id']}/edit"

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except GwsError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)
