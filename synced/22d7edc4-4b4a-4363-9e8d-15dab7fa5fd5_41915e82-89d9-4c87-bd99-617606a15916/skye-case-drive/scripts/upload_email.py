#!/usr/bin/env python3
"""The "here's where to upload your materials" email, written as a Google Doc.

A doc rather than a Gmail draft, because whoever actually emails the client
isn't necessarily whoever built the folder — a draft sits in one person's
mailbox, a doc in the case folder is there for whoever picks the case up.

It lands in the case *root* folder, not in "0. Shared Folder" — the shared
folder is the one the client can see, and a staff-facing "copy this and send it"
doc doesn't belong in the client's own upload space.

Importable (`compose()` — used by build_case_drive.py) and runnable on its own
to (re)write the doc for a case that already exists:

  python3 upload_email.py --folder-id <0.SHARED_FOLDER_ID> \
      --client-name "Xuan Shen" --case-type EB1A \
      --shared-folder-link "https://drive.google.com/drive/folders/..." \
      [--to client@example.com] [--lang zh|en] [--print-only]
"""

import argparse
import json
import subprocess
import sys

CASE_LABEL = {"O1": "O-1", "O1A": "O-1A", "O1B": "O-1B", "EB1A": "EB-1A", "NIW": "NIW"}

DOC_MIME = "application/vnd.google-apps.document"

ZH = """{name} 您好，

我是凌图律师事务所（Lingtu Law）负责您 {case} 申请的团队。我们已经为您的案件建立了专属材料文件夹，请通过下面的链接上传您的申请材料：

{link}

请上传的内容包括：
1. 个人身份材料（护照、签证/I-94、当前身份证明等）
2. 学历与工作经历材料（学位证、成绩单、在职证明、简历/CV）
3. 支持性证据（奖项、媒体报道、发表作品、评审记录、会员证书、薪资证明等）
4. 其他您认为对本次申请有帮助的材料

上传说明：
- 这个文件夹只有您和我们的案件团队可以访问，请放心上传。
- 建议按类别建子文件夹，文件名尽量写清楚内容和日期。
- 材料可以分批上传，不需要一次传完；每次上传后我们都能看到。

如果链接打不开，或者您在上传中遇到任何问题，直接回复这封邮件告诉我们即可。

祝好，
凌图律师事务所 Lingtu Law
"""

EN = """Dear {name},

I'm writing from Lingtu Law regarding your {case} petition. We've set up a dedicated folder for your case materials — please upload your documents here:

{link}

Please include:
1. Identity documents (passport, visa / I-94, current status documents)
2. Education and employment records (degrees, transcripts, employment letters, CV)
3. Supporting evidence (awards, press coverage, publications, judging records, memberships, salary evidence)
4. Anything else you believe supports your case

Notes:
- Only you and your case team can access this folder.
- Subfolders by category, with clear file names and dates, help us move faster.
- You can upload in batches; we'll see each upload as it arrives.

If the link doesn't open or you run into any trouble uploading, just reply to this email.

Best regards,
Lingtu Law
"""

ZH_HEADER = "以下是发给客户的材料上传指引邮件，直接复制发送即可。"
EN_HEADER = "Ready-to-send email for the client. Copy the subject and body as-is."

# Name follows the email's language so the doc reads consistently with what's
# inside it.
ZH_DOC_NAME = "材料上传指引邮件 - {name}"
EN_DOC_NAME = "Document Upload Instructions - {name}"


def doc_name_for(client_name, lang="zh"):
    return (ZH_DOC_NAME if lang == "zh" else EN_DOC_NAME).format(name=client_name)


def compose(client_name, case_type, shared_folder_link, to=None, lang="zh", body=None):
    """Return (subject, body, doc_text) for the client's upload-instructions email."""
    key = case_type.strip().upper().replace("-", "").replace(" ", "")
    case = CASE_LABEL.get(key, case_type)

    if body is None:
        body = (ZH if lang == "zh" else EN).format(
            name=client_name, case=case, link=shared_folder_link)

    if lang == "zh":
        subject = f"[Lingtu Law] {client_name} {case} 申请 - 材料上传文件夹"
        label_to, label_subject, label_body = "收件人", "主题", "正文"
        sep, missing = "：", "（待补充客户邮箱）"
        header = ZH_HEADER
    else:
        subject = f"[Lingtu Law] {client_name} — {case} petition: document upload folder"
        label_to, label_subject, label_body = "To", "Subject", "Body"
        sep, missing = ": ", "(client email pending)"
        header = EN_HEADER

    lines = [header, "", f"{label_to}{sep}{to or missing}",
             f"{label_subject}{sep}{subject}", "", label_body, "", body.rstrip(), ""]
    return subject, body, "\n".join(lines)


def gws(args):
    proc = subprocess.run(["gws"] + args, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"gws {' '.join(args[:3])} failed: {(proc.stderr or proc.stdout).strip()}")
    out = proc.stdout.strip()
    data = json.loads(out) if out else {}
    if isinstance(data, dict) and "error" in data:
        sys.exit(json.dumps(data["error"], ensure_ascii=False))
    return data


def write_doc(folder_id, client_name, doc_text, doc_name=None, lang="zh"):
    """Create the email doc inside folder_id and return its id/name/link."""
    name = doc_name or doc_name_for(client_name, lang)
    doc = gws(["drive", "files", "create",
               "--params", json.dumps({"supportsAllDrives": True, "fields": "id,name"}),
               "--json", json.dumps({"name": name, "mimeType": DOC_MIME,
                                     "parents": [folder_id]}, ensure_ascii=False)])
    gws(["docs", "+write", "--document", doc["id"], "--text", doc_text])
    return {"doc_id": doc["id"], "doc_name": name,
            "doc_link": f"https://docs.google.com/document/d/{doc['id']}/edit"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder-id", help="Where to create the doc — normally the case root folder")
    ap.add_argument("--client-name", required=True)
    ap.add_argument("--case-type", required=True)
    ap.add_argument("--shared-folder-link", required=True)
    ap.add_argument("--to", help="Client email, filled into the 收件人 line")
    ap.add_argument("--lang", default="zh", choices=["zh", "en"])
    ap.add_argument("--body-file", help="Use this file's contents as the body instead of the built-in wording")
    ap.add_argument("--doc-name")
    ap.add_argument("--print-only", action="store_true", help="Show the wording without creating the doc")
    args = ap.parse_args()

    body = None
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as fh:
            body = fh.read()

    subject, body, doc_text = compose(args.client_name, args.case_type,
                                      args.shared_folder_link, to=args.to,
                                      lang=args.lang, body=body)
    if args.print_only:
        print(doc_text)
        return
    if not args.folder_id:
        sys.exit("--folder-id is required unless --print-only")

    result = write_doc(args.folder_id, args.client_name, doc_text, args.doc_name, args.lang)
    result["subject"] = subject
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
