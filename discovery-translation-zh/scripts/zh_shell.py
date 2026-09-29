# -*- coding: utf-8 -*-
"""Chinese client-verification build — shared chrome and boilerplate."""
import sys, copy, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'discovery-response', 'scripts'))
from common import (load_base, grab_protos, rewrite_head, truncate_body, emit,
                    page_break, set_footer, WD_ALIGN_PARAGRAPH)

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CJKFONT = "Songti SC"

def cjk(p):
    """Times New Roman for the Latin runs, Songti SC for the CJK ones."""
    for r in p._p.findall(W + "r"):
        rPr = r.find(W + "rPr")
        if rPr is None:
            rPr = r.makeelement(W + "rPr", {}); r.insert(0, rPr)
        for f in rPr.findall(W + "rFonts"):
            rPr.remove(f)
        rPr.insert(0, rPr.makeelement(W + "rFonts", {
            W + "eastAsia": CJKFONT, W + "ascii": "Times New Roman",
            W + "hAnsi": "Times New Roman"}))
    return p

def E(doc, protos, kind, text, bold=None):
    return cjk(emit(doc, protos, kind, text, bold=bold))

# ---- boilerplate, one rendering used everywhere ----
OBJ_PRIVACY = "答复方对本条质询提出异议，理由是其所寻求的信息属于《加利福尼亚州宪法》第一条第一款所保护的隐私范围。"
OBJ_WP      = "答复方对本条质询提出异议，理由是其所寻求的材料受《民事诉讼法》第 2018.030 条规定的律师工作成果原则保护。"
OBJ_EXPERT  = "答复方对本条质询提出异议，理由是其要求在《民事诉讼法》第 2034.210 条至第 2034.310 条规定的披露期限之前提供专家意见。"
OBJ_BRITT   = "答复方对本条请求提出异议，理由是其所寻求的信息属于《加利福尼亚州宪法》第一条第一款所保护的隐私范围，且未限定于本案所涉的伤情。(Britt v. Superior Court (1978) 20 Cal.3d 844, 863-864.)"
OBJ_PREMATURE = "答复方对本条质询提出异议，理由是其要求作出法律结论，且在本诉讼现阶段主张尚属过早。"

SWO  = "在不放弃上述异议的前提下，答复方答复如下："
CONT = "调查与取证仍在进行中，答复方保留依《民事诉讼法》第 2030.310 条修改及补充本答复的权利。"
CONT_P = "调查与取证仍在进行中，答复方保留于日后收到其他文件时补充本次出示的权利。"

COMPLY = "答复方将完全遵从本条请求。凡处于答复方占有、保管或控制之下且未提出异议的文件，均随本答复一并出示。"
UNABLE = "答复方无法遵从本条请求，因为并不存在、亦从未存在处于答复方占有、保管或控制之下的响应文件。答复方已进行勤勉查找与合理查询。"
NO_WITHHOLD = "基于上述异议，答复方未扣留任何响应文件。"

# ------------------------------------------------------------------ per-case
# Fill CASE for the matter, then import build_shell / verification / signature.
CASE = {
    "atty": ["Hernán S. Simó (SBN 354175)", "LAW OFFICE OF SHENQI CAI APC",
             "13191 Crossroads Parkway North, Suite 295",
             "City of Industry, California 91746",
             "电话：(626) 479-2207", "传真：(626) 479-2207",
             "电邮：hernan.s@lingtulaw.com", "", "原告代理律师", "<CLIENT>", ""],
    "court":      ["加利福尼亚州高等法院", "<县名> (COUNTY OF ...)"],
    "plaintiff":  "<CLIENT>",
    "defendants": "<DEFENDANT>；及 DOES 1 至 20，",
    "cross":      True,          # adds 及相关反诉。 to the caption
    "case_no":    "<CASE NO.>",
    "dept":       "<DEPT>",
    "filed":      "起诉日期：<date>",
    "tsc":        "审前会议：<date>",
    "trial":      "开庭日期：尚未指定",
    "propounder": "被告 <DEFENDANT>",
    "responder":  "原告 <CLIENT>",
    "set":        "第一组",
}

def caption(title_zh):
    left = [(CASE["plaintiff"] + "，", False, None), ("", False, None),
            ("原告，", False, WD_ALIGN_PARAGRAPH.CENTER), ("", False, None),
            ("诉", False, None), ("", False, None),
            (CASE["defendants"], False, None), ("", False, None),
            ("被告。", False, WD_ALIGN_PARAGRAPH.CENTER)]
    if CASE.get("cross"):
        left += [("", False, None), ("及相关反诉。", False, None)]
    right = [("案号：" + CASE["case_no"], False, None),
             ("审判庭：" + CASE["dept"], False, None), ("", False, None),
             (title_zh, True, None), ("", False, None),
             (CASE["filed"], False, None), (CASE["tsc"], False, None),
             (CASE["trial"], False, None)]
    return left, right

def parties():
    return ["提问方\t：\t" + CASE["propounder"],
            "答复方\t：\t" + CASE["responder"],
            "组别\t\t：\t" + CASE["set"]]

PRELIM_ZH = ("本答复仅为本案之目的、并就本案作出。每一项答复均受一切适当异议之限制（包括但不限于就证据能力、"
             "关联性、实质性、适当性及可采性提出的异议）；若该等陈述由出庭作证的证人作出，上述异议足以使其被排除。"
             "上述全部异议及其理由均予保留，并可于庭审时由法院裁定。作出本答复之一方尚未完成对本案相关事实的调查，"
             "尚未完成本案的证据开示程序，亦尚未完成庭审准备。因此，以下答复的作出不影响答复方于庭审时提出"
             "其后发现之证据以证明其后发现之重要事实的权利。")

NOTICE_ZH = ("【致客户：本件为英文正式答复的中文译本，仅供您核对内容之用。对方律师收到的是英文本。"
             "请逐条核对，如有任何一处与事实不符，请在签字前告知本所。】")

def build_shell(title_zh, footer_zh):
    doc = load_base(); protos = grab_protos(doc)
    left, right = caption(title_zh)
    rewrite_head(doc, CASE["atty"], CASE["court"], left, right, parties())
    for i in range(0, 19):
        cjk(doc.paragraphs[i])
    for c in doc.tables[0].rows[0].cells:
        for p in c.paragraphs: cjk(p)
    truncate_body(doc, 18)
    set_footer(doc, footer_zh); cjk(doc.sections[0].footer.paragraphs[1])
    return doc, protos

def verification(doc, protos, title_zh):
    page_break(doc, protos)
    E(doc, protos, "head", "宣誓认证 (VERIFICATION)")
    E(doc, protos, "body", "\t本人 YI CONG 声明：")
    E(doc, protos, "prelim",
      "本人系上述案件之原告。本人的母语为普通话，不能流利阅读英文。前述" + title_zh +
      "已由英文口译为普通话向本人宣读，本人知悉其内容。除依据传闻与确信陈述之事项外，"
      "上述内容均属本人所知之真实情况；就该等依据传闻与确信陈述之事项，本人相信其为真实。")
    E(doc, protos, "prelim", "本人依加利福尼亚州法律在伪证罪处罚下声明，上述内容真实无误。")
    E(doc, protos, "body", "")
    E(doc, protos, "body", "\t于 2026 年 ____ 月 ____ 日在加利福尼亚州 ____________________ 签署。")
    E(doc, protos, "body", "")
    E(doc, protos, "body", "\t\t\t\t\t______________________________")
    E(doc, protos, "body", "\t\t\t\t\t" + CASE["plaintiff"])
    E(doc, protos, "body", "")
    E(doc, protos, "head", "口译人声明 (DECLARATION OF TRANSLATOR)")
    E(doc, protos, "body", "\t本人 ______________________________ 声明：")
    E(doc, protos, "prelim",
      "本人精通英文与普通话。本人于 2026 年 ____ 月 ____ 日将前述答复及宣誓认证由英文口译为普通话"
      "向 " + CASE["plaintiff"] + " 转述，其表示已理解上述内容。本人依加利福尼亚州法律在伪证罪处罚下声明，"
      "上述内容真实无误。")
    E(doc, protos, "body", "")
    E(doc, protos, "body", "\t\t\t\t\t______________________________")
    E(doc, protos, "body", "\t\t\t\t\t口译人签名")

def signature(doc, protos):
    E(doc, protos, "body", "")
    E(doc, protos, "body", "日期：" + CASE.get("dated", "____ 年 ____ 月 ____ 日") + "\t\t\tLAW OFFICE OF SHENQI CAI APC")
    E(doc, protos, "body", "")
    E(doc, protos, "body", "\t\t\t\t\t______________________________")
    E(doc, protos, "body", "\t\t\t\t\tHernán S. Simó")
    E(doc, protos, "body", "\t\t\t\t\t原告 " + CASE["plaintiff"] + " 之代理律师")
