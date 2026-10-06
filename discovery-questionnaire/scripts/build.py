# -*- coding: utf-8 -*-
"""Build a discovery questionnaire .docx on the firm letterhead.

  python3 build.py master                      -> blank 88-FROG + SROG-slot template
  python3 build.py case    <case.py> [out]     -> bilingual working copy (what OPC served)
  python3 build.py client  <case.py> [out]     -> simplified Chinese client questionnaire

The case module supplies CASE / CHECKED / ATTORNEY_ONLY / SROGS / RFP_DOCS / GROUPS.
Draft-only: nothing here sends, serves or e-files.
"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import (para, blank, run, rpr, tbl_open, tbl_close, tr, tc,
                    row_full, row_label, row_box, W_TOTAL, W_LABEL, W_ANS,
                    build as pkg_build, sectpr, section_break_para,
                    HDR_RID, FOOT_RID, FOOTER_TEXT)
import frogs_disc001 as F

HERE = os.path.dirname(os.path.abspath(__file__))
LETTERHEAD = os.path.join(HERE, "..", "assets", "letterhead.docx")
RED, GRAY = "C00000", "808080"
YN = ("Yes or No?", "请在右侧填写「Yes 是」或「No 否」")


def qline(num, text, hl=None, bold_text=False):
    p = ('<w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
         + rpr(24) + '</w:pPr>')
    return f'<w:p>{p}{run(num + "  ", 24, True)}{run(text, 24, bold=bold_text, hl=hl)}</w:p>'


def load_case(path):
    spec = importlib.util.spec_from_file_location("case_data", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- FROG blocks
def render_frog(q, overrides=None):
    out = []; a = out.append
    a(tbl_open())
    body = qline(q["n"], q["en"]) + para(q["cn"], hl="yellow")
    if q.get("note"):
        body += para(q["note"], bold=True, color=RED, before=60)
    a(row_full(body, shade="EDEDED", height=300))
    if q.get("yn"):
        a(row_label(*YN, height=400))
    if q.get("lines"):
        a(row_box(q["lines"] * 360))
    for title, items, repeat in q.get("groups", []):
        if title:
            a(row_full(para(title, bold=True), shade="F7F7F7", height=280))
        for k in range(repeat):
            if repeat > 1:
                a(row_full(para(f"#{k+1}", bold=True), shade="FCFCFC", height=240))
            for en, cn in items:
                if overrides:
                    cn = overrides.get((q["n"], en), cn)
                a(row_label(en, cn))
    if q.get("tail_lines"):
        if q.get("tail_note"):
            a(row_full(para(q["tail_note"], bold=True), shade="F7F7F7", height=280))
        a(row_box(q["tail_lines"] * 360))
    a(tbl_close()); a(blank())
    return out


def instructions(extra_red=()):
    X = [para("填写说明", bold=True, after=40)]
    rows = [
        ("1.  每题先是英文原文（法院表格 / 对方原问），下面黄色那行是中文翻译。"
         "您只看黄色那行即可，答案填在右边空白格里。", False),
        ("2.  题目与您情况无关的，请写「不适用 / N/A」，不要留空。"
         "留空会被对方视为拒绝回答，可能被法院处罚。", True),
        ("3.  不确定、记不清的，请写「记不清」并尽量给出大致时间或范围。"
         "请勿猜测或编造 —— 这份答复是您宣誓作出的。", True),
        ("4.  标注「本题由律所作答」的，您跳过即可。", False),
        ("5.  需要提供的文件（保险卡、工资单、照片、视频、收据等）请一并拍照发给我们。", False),
    ]
    for t, red in list(rows) + list(extra_red):
        X.append(para(t, after=40, bold=red, color=(RED if red else None)))
    X.append(blank())
    return X


def definitions(extra=()):
    X = [para("本问卷中大写词语的含义", bold=True, after=60), tbl_open(3060, 6300)]
    base = [
        ("INCIDENT", "事故 —— 指本案所涉的这次事故 / 事件。"),
        ("ADDRESS", "地址 —— 完整的街道地址，包括城市、州和邮编。"),
        ("PERSON", "人 —— 包括自然人、商号、社团、组织、合伙、企业、信托、有限责任公司、公司或公共机关。"),
        ("DOCUMENT", "文件 —— 任何形式的书面或记录材料，包括手写、打印、照片、电子存储信息、短信、邮件、录音录像。"),
        ("HEALTH CARE PROVIDER", "医疗机构 —— 包括医院、急诊、诊所、医生、推拿师、针灸师、理疗师、影像中心。"),
        ("YOU OR ANYONE ACTING ON YOUR BEHALF",
         "您或代表您行事的任何人 —— 包括您本人、您的代理人、雇员、保险公司、律师、会计师、调查员。"),
    ]
    for en, cn in list(base) + list(extra):
        X.append(tr([tc(3060, para(en, bold=True), shade="F2F2F2"), tc(6300, para(cn))], 300))
    X.append(tbl_close())
    return X


CLOSING = [
    blank(),
    para("填好后请直接把这份文件发回我们。证据交换过程中我们可能会再就细节与您联系，"
         "请留意我们的电话和邮件。", center=True, after=60),
    para("During the discovery process we may contact you again to discuss specific details. "
         "Please be attentive to our calls or emails. Thank you.", center=True),
]


# ---------------------------------------------------------------- mode: master
def build_master(out):
    FOOTER_TEXT[0] = ("Law Office of Shenqi Cai APC  |  Discovery Questionnaire  |  Page ")
    X = []; A = X.append
    A(para("FORM INTERROGATORIES — GENERAL (DISC-001)", sz=32, bold=True, center=True, after=40))
    A(para("标准质询问卷 + 特别质询问卷 · 中英对照 · 客户填写表", sz=32, bold=True, center=True, after=160))
    A(tbl_open())
    for k in ("Client name / 客户姓名", "Date / 填写日期"):
        A(tr([tc(W_LABEL, para(k.split(' / ')[0]) + para(k.split(' / ')[1]), shade="FAFAFA"),
              tc(W_ANS, para())], 460))
    A(tbl_close()); A(blank())
    for x in instructions(): A(x)
    for x in definitions(): A(x)
    A(section_break_para(sectpr(2880, header=HDR_RID)))

    first = True
    for sec in F.SECTIONS:
        A(para(sec["hdr"], bold=True, center=True, brk=not first, after=60, keep=True))
        first = False
        if sec.get("note"): A(para(sec["note"], center=True, after=60))
        A(blank(sz=12))
        for q in sec["qs"]:
            for x in render_frog(q): A(x)

    A(para("SPECIAL INTERROGATORIES  特别质询（SROGs）", bold=True, center=True, brk=True, after=60))
    A(para("对方送达的 Special Interrogatories 按其编号逐条填入。加州上限 35 条"
           "（CCP §2030.030(a)(1)），超出须附 §2030.050 声明。", center=True, after=120))
    A(blank(sz=12))
    for _ in range(8):
        A(tbl_open())
        A(row_full(qline("SROG No. ____", "特别质询第 ____ 号（请填对方编号）", hl="yellow"),
                   shade="EDEDED", height=280))
        A(row_full(para("Question as served 对方原问（英文原文 + 中文翻译）", bold=True),
                   shade="F7F7F7", height=260))
        A(row_box(4 * 360))
        A(row_full(para("Your answer 您的回答", bold=True), shade="F7F7F7", height=260))
        A(row_box(5 * 360))
        A(tbl_close()); A(blank())
    for x in CLOSING: A(x)
    A(sectpr(1440, blank_header=True, footer=FOOT_RID))
    pkg_build("".join(X), out, base=LETTERHEAD)
    return len(F.ALL_NUMBERS)


# ---------------------------------------------------------------- mode: case
def build_case(c, out):
    C = c.CASE
    FOOTER_TEXT[0] = (f"Law Office of Shenqi Cai APC  |  {C['short']}  |  "
                      f"Discovery Questionnaire  |  Page ")
    keep = [n for n in c.CHECKED if n not in getattr(c, "ATTORNEY_ONLY", set())]
    X = []; A = X.append
    A(para("DISCOVERY QUESTIONNAIRE  证据交换问卷", sz=32, bold=True, center=True, after=40))
    A(para(C["subtitle_en"], sz=24, bold=True, center=True, after=20))
    A(para(C["subtitle_zh"], sz=24, bold=True, center=True, after=160))
    A(tbl_open(2700, 6660))
    for k, v, hl in C["header_rows"]:
        A(tr([tc(2700, para(k, bold=True), shade="F2F2F2"),
              tc(6660, para(v, hl=hl) if v else para())], 320))
    A(tbl_close()); A(blank())
    A(para(C["client_due_line"], bold=True, color=RED, center=True, after=60))
    A(blank())
    A(para("本次对方送达了什么", bold=True, after=40))
    for line in C["served_summary"]: A(para(line, after=40))
    A(blank())
    for x in instructions(): A(x)
    for x in definitions(C.get("extra_definitions", ())): A(x)
    A(section_break_para(sectpr(2880, header=HDR_RID)))

    A(para("PART 1  —  FORM INTERROGATORIES — GENERAL (DISC-001)", bold=True, center=True, after=40))
    A(para("标准质询问卷 —— 以下为对方实际勾选、需要您回答的条目", center=True, after=120))
    first = True
    ov = getattr(c, "LABEL_OVERRIDES", None)
    for sec in F.SECTIONS:
        qs = [q for q in sec["qs"] if q["n"] in keep]
        if not qs: continue
        A(para(sec["hdr"], bold=True, center=True, brk=not first, after=60, keep=True))
        first = False
        A(blank(sz=12))
        for q in qs:
            for x in render_frog(q, ov): A(x)

    srogs = getattr(c, "SROGS", [])
    if srogs:
        A(para("PART 2  —  SPECIAL INTERROGATORIES, SET ONE", bold=True, center=True, brk=True, after=40))
        A(para(f"特别质询问卷 —— 对方共 {len(srogs)} 条", center=True, after=120))
        A(blank(sz=12))
        notes = getattr(c, "WHO_NOTES", {})
        for n, en, zh, who in srogs:
            A(tbl_open())
            body = qline(f"No. {n}", en) + para(zh, hl="yellow")
            note = (getattr(c, "PRIVACY_NOTE", None) if n in getattr(c, "PRIVACY", set())
                    else notes.get(who))
            if note: body += para(note, bold=True, color=RED, before=60)
            A(row_full(body, shade="EDEDED", height=300))
            A(row_box(2 * 360 if who == "F" else 5 * 360))
            A(tbl_close()); A(blank())
    for x in CLOSING: A(x)
    A(sectpr(1440, blank_header=True, footer=FOOT_RID))
    pkg_build("".join(X), out, base=LETTERHEAD)
    return len(keep), len(srogs)


# ---------------------------------------------------------------- mode: client
def build_client(c, out):
    C = c.CASE
    FOOTER_TEXT[0] = f"凌图律师事务所  |  {C['short']}  |  证据交换问卷（中文版）  |  第 "
    X = []; A = X.append
    A(para("证据交换问卷", sz=36, bold=True, center=True, after=40))
    A(para(C["client_title_zh"], sz=24, bold=True, center=True, after=160))
    A(tbl_open(2520, 6840))
    for k, v, hl in C["client_header_rows"]:
        A(tr([tc(2520, para(k, bold=True), shade="F2F2F2"), tc(6840, para(v, hl=hl))], 320))
    A(tbl_close()); A(blank())
    A(para("请先读这一页", bold=True, after=60))
    for t, red in c.PREAMBLE:
        A(para(t, after=60, bold=red, color=(RED if red else None)))
    A(blank())
    A(para("填好后请直接把这份文件发回给我们。有任何不懂的地方，随时打电话或微信问我们，不要自己猜。",
           bold=True, center=True, after=60))
    A(section_break_para(sectpr(2880, header=HDR_RID)))

    n = 0
    for gi, (title, qs) in enumerate(c.GROUPS):
        A(para(title, bold=True, center=True, brk=(gi > 0), after=60, keep=True))
        A(blank(sz=12))
        for text, lines, xref, note in qs:
            n += 1
            A(tbl_open())
            body = qline(f"{n}.", text)
            if note: body += para(note, bold=True, color=RED, before=60)
            body += para(f"（对应 {xref}）", sz=16, color=GRAY, before=60)
            A(row_full(body, shade="EDEDED", height=300))
            A(row_box(lines * 360))
            A(tbl_close()); A(blank())

    docs = getattr(c, "RFP_DOCS", [])
    if docs:
        A(para(c.DOCS_HEADING, bold=True, center=True, brk=True, after=60))
        A(para("以下材料请拍照或扫描后一并发给我们，已经发过的不用重复。", center=True, after=60))
        if getattr(c, "DOCS_SUBNOTE", None):
            A(para(c.DOCS_SUBNOTE, center=True, color=GRAY, sz=20, after=120))
        A(blank(sz=12))
        A(tbl_open(600, 8760))
        for i, d in enumerate(docs, 1):
            first = (i == 1)
            A(tr([tc(600, para(f"{i}.", bold=True), shade="F7F7F7"),
                  tc(8760, para(d, bold=first, color=(RED if first else None)))], 360))
        A(tbl_close()); A(blank())
        if getattr(c, "DEPO_NOTE", None): A(para(c.DEPO_NOTE, after=60))
    A(blank())
    A(para("谢谢您的配合。在证据交换过程中我们可能还会就细节再与您联系，"
           "请留意我们的电话和邮件。", center=True))
    A(sectpr(1440, blank_header=True, footer=FOOT_RID))
    pkg_build("".join(X), out, base=LETTERHEAD)
    return n


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "master"
    if mode == "master":
        out = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(
            "~/Downloads/Discovery 客户问卷（FROGs + SROGs）- TEMPLATE.docx")
        print("FROGs:", build_master(out), "->", out)
    else:
        c = load_case(sys.argv[2])
        out = sys.argv[3] if len(sys.argv) > 3 else None
        if mode == "case":
            out = out or os.path.expanduser(f"~/Downloads/{c.CASE['short']} - Discovery Questionnaire (FROGs + SROGs, 中英) - DRAFT.docx")
            print("FROGs/SROGs:", build_case(c, out), "->", out)
        elif mode == "client":
            out = out or os.path.expanduser(f"~/Downloads/{c.CASE['short']} - 证据交换问卷（中文版·给客户）.docx")
            print("questions:", build_client(c, out), "->", out)
        else:
            sys.exit("mode must be master | case | client")
