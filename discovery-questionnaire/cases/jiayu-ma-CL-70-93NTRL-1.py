# -*- coding: utf-8 -*-
"""Jiayu Ma v. Tesla Insurance Services — UM/UIM arbitration, Claim CL-70-93NTRL-1.
Served 9/29/2026 by Colman Perkins Law Group (Tiffany Lam SBN 351861 / Sara Young SBN 136681),
electronic service only from jtoney@colmanlawgroup.com:
  FROG01 (DISC-001, 64 boxes checked — read page-by-page off the flattened PDF 2026-10-08)
  SROG01 (21, under the 35 limit, no 2030.050 declaration needed)
  RFP01  (26)
  2026.09.29 UM Arb Response (Tesla affords coverage, reserves all defenses)
Hernán calendared the response deadline as October 29, 2026.
DOL 11/14/2025. Prior counsel Dan A. Everakes / Tharpe & Howell is out.
NOTE: the client part-filled the firm's old Auto Questionnaire in Aug 2026 — the handful of
answers he gave are pre-filled below for confirmation rather than re-asked.
"""

CASE = dict(
    short="Jiayu Ma",
    subtitle_en="Form Interrogatories (DISC-001) + Special Interrogatories + Demand for Production, Set One",
    subtitle_zh="标准质询问卷 + 特别质询问卷 + 文件提供要求（第一组）· 中英对照 · 客户填写表",
    client_title_zh="Jiayu Ma 诉 Tesla Insurance 保险仲裁案 · 请您填写",
    client_due_line="请在 2026 年 10 月 20 日前填好发回我们，我们需要时间整理、翻译并在 10 月 29 日期限前向对方提交正式答复。",
    header_rows=[
        ("Matter 案件", "Jiayu Ma v. Tesla Insurance Services — Uninsured/Underinsured Motorist Arbitration", None),
        ("Claim No. 理赔号", "CL-70-93NTRL-1　（对方卷宗号 TIS-4624）", None),
        ("Propounding party 提问方", "Respondent, Tesla Insurance Services", None),
        ("Responding party 答复方", "Claimant, Jiayu Ma（＝您）", None),
        ("Set No. 组号", "One (1)", None),
        ("Served 送达日", "September 29, 2026（仅电子送达）", None),
        ("Opposing counsel 对方律师",
         "Tiffany Lam, Esq. / Sara Young, Esq. — Colman Perkins Law Group, Glendale", None),
        ("Response due 答复期限", "October 29, 2026", "yellow"),
        ("Date of loss 事发日期", "November 14, 2025", None),
    ],
    client_header_rows=[
        ("案件", "Jiayu Ma 诉 Tesla Insurance Services（UM / UIM 保险仲裁）", None),
        ("理赔号", "CL-70-93NTRL-1", None),
        ("事发日期", "2025 年 11 月 14 日", None),
        ("请回填期限", "2026 年 10 月 20 日前发回我们", "yellow"),
    ],
    served_summary=[
        "Part 1 — Form Interrogatories — General (DISC-001)：对方共勾选 64 条，全部需要您回答。",
        "Part 2 — Special Interrogatories, Set One：共 21 条，其中 18 条需要您回答，3 条涉及敏感号码或账单金额由律所处理。",
        "对方同时送达 Request for Production of Documents 共 26 项，需要您配合提供的材料列在中文问卷最后一节。",
        "对方未勾选的部分（3.0 公司背景、15.0、16.2–16.10、17.0、50.0 合同）已经整节删除，不必理会。",
    ],
    extra_definitions=[
        ("PSYCHOTHERAPIST", "心理治疗师 —— 包括精神科医生、心理学家、临床社工、婚姻家庭治疗师等（Evid. Code §1010）。"),
        ("LOCATION", "地点 —— 本次事故发生的具体位置。"),
    ],
)

# 对方实际勾选的 FROGs（逐页看图核对 2026-10-08）
CHECKED = (["1.1"] + [f"2.{i}" for i in range(1, 14)] + ["4.1", "4.2"]
           + [f"6.{i}" for i in range(1, 8)] + [f"7.{i}" for i in range(1, 4)]
           + [f"8.{i}" for i in range(1, 9)] + ["9.1", "9.2"]
           + ["10.1", "10.2", "10.3"] + ["11.1", "11.2"]
           + [f"12.{i}" for i in range(1, 8)] + ["13.1", "13.2"] + ["14.1", "14.2"]
           + ["16.1"] + [f"20.{i}" for i in range(1, 12)])
# 未勾：3.1-3.7、15.1、16.2-16.10、17.1、50.1-50.6
ATTORNEY_ONLY = set()   # 这次没有纯律所条目：16.1 在 UM 里问的是"对方司机是否有责"，客户答得了

WHO_NOTES = {"C": None,
             "CF": "本题请您填写您知道的部分，其余由律所依案卷补充。",
             "F": "本题由律所依据案卷、账单和 EOB 作答，您无需填写。"}
PRIVACY = {1, 16, 18}
PRIVACY_NOTE = "本题涉及个人敏感号码，律所将另行处理并评估异议，请勿填写在本表上。"

SROGS = [
(1, "Please state YOUR social security number.",
 "请提供您的社会安全号（SSN）。", "F"),
(2, "IDENTIFY YOUR primary treating physician/family doctor at the time of the INCIDENT.",
 "请指明本次事故发生时您的主治医生 / 家庭医生（姓名、地址、电话）。", "C"),
(3, "Have YOU been involved in any other accidents (including, but not limited to, automobile, premises or on-the-job) which caused YOU any injury during the last ten (10) years (regardless of whether a claim was made for same)?",
 "过去十年内，您是否还发生过其他造成您受伤的事故（车祸、场所事故、工伤等均算）？无论当时有没有索赔都要回答。", "C"),
(4, "If you have been involved in any accidents (including, but not limited to, automobile, premises or on-the-job) which caused you any injury during the last ten (10) years, please IDENTIFY each HEALTH CARE PROVIDER who rendered care to you as a result of any accident.",
 "如果有，请列出因那些事故为您治疗过的每一家医疗机构（名称、地址、电话）。", "C"),
(5, "If medical care was available to you from any Health Maintenance Organization (e.g., Kaiser Foundation) during the two (2) years prior to the date of these interrogatories, provide your subscriber number.",
 "过去两年内，如果您可以通过任何 HMO（例如 Kaiser）就医，请提供您的会员号 / 投保人编号。", "C"),
(6, "If you have injured yourself since the INCIDENT, please IDENTIFY each HEALTH CARE PROVIDER who rendered care to you as a result of any such injury.",
 "本次事故之后您如果又受过伤，请列出为该次受伤治疗过的每一家医疗机构。", "C"),
(7, "If YOU contend that this INCIDENT aggravated any pre-existing physical or mental condition, describe such aggravation and the body parts included.",
 "如果您主张本次事故加重了您原有的身体或精神状况，请描述是怎么加重的，以及涉及哪些身体部位。", "C"),
(8, "IDENTIFY each HEALTH CARE PROVIDER who treated YOU for any condition which YOU claim was aggravated by the INCIDENT.",
 "请列出为您治疗该「被加重的状况」的每一家医疗机构。", "C"),
(9, "If YOU contend that the INCIDENT caused YOU any disfigurement including, but not limited to, scarring, fully describe each disfigurement.",
 "如果您主张本次事故造成了外观损伤（例如疤痕），请逐一完整描述。", "C"),
(10, "IDENTIFY each entity (including, but not limited to, insurance company and/or insurance plan, government, Medi-Cal, or other individual) which paid any part of any medical bills which you incurred as a result of the INCIDENT (Howell v. Hamilton Meats & Produce (2011) 52 Cal.4th 541).",
 "请列出为您本次事故的医疗费支付过任何部分的每一方（保险公司、政府、Medi-Cal、Medicare 或个人）。", "CF"),
(11, "If any entity has paid any part of Claimant's medical bills incurred as a result of the INCIDENT, itemize the amount of payment made to each such HEALTH CARE PROVIDER.",
 "如有第三方付款，请逐项列明付给每一家医疗机构的金额。", "F"),
(12, "If any HEALTH CARE PROVIDER who treated Claimant for the INCIDENT accepted payment for less than the full amount billed, itemize the amount accepted by each HEALTH CARE PROVIDER.",
 "如果有医疗机构接受了低于账单全额的付款，请逐项列明每家实际接受的金额。", "F"),
(13, "If you contend that the INCIDENT caused you to suffer emotional distress, please IDENTIFY each PSYCHOTHERAPIST with whom you treated for the INCIDENT.",
 "如果您主张本次事故造成了精神痛苦，请列出您因此看过的每一位心理治疗师。", "C"),
(14, "If you contend that the INCIDENT caused you to suffer emotional distress, please IDENTIFY each PSYCHOTHERAPIST with whom you treated during the five (5) years prior to the INCIDENT.",
 "如果您主张精神损害，请列出事故发生前五年内您看过的每一位心理治疗师。", "C"),
(15, "If YOU have filed a claim with the California Workers Compensation Appeals Board within the last five (5) years, please provide all case numbers.",
 "过去五年内，您是否向加州工伤上诉委员会（WCAB）提出过申请？如有，请提供所有案件编号。", "C"),
(16, "If YOU have ever been enrolled in Medicare Part A or Part B, provide your Medicare Claim Number.",
 "如果您曾加入 Medicare Part A 或 Part B，请提供您的 Medicare Claim Number。", "F"),
(17, "IDENTIFY YOUR cell phone provider at the time of the INCIDENT.",
 "请说明事故发生时您的手机运营商是哪一家。", "C"),
(18, "IDENTIFY YOUR account number for YOUR cell phone provider at the time of the INCIDENT.",
 "请提供事故发生时您手机账户的账号。", "F"),
(19, "IDENTIFY YOUR cell phone number for YOUR cell phone at the time of the INCIDENT.",
 "请提供事故发生时您使用的手机号码。", "C"),
(20, "Please identify by way of name, address and phone number all health care providers that you presented to following the subject accident on November 14, 2025.",
 "请列出 2025 年 11 月 14 日事故之后您就诊过的所有医疗机构的名称、地址和电话。", "C"),
(21, "Please IDENTIFY all HEALTH CARE PROVIDERS, by way of name, address and phone number, that you have presented to within the last ten years for complaints related to any body part for which you are claiming injury from the subject INCIDENT.",
 "过去十年内，凡就您本次主张受伤的【同一身体部位】看过的所有医疗机构，请列出名称、地址和电话。", "C"),
]

PREAMBLE = [
    ("Tesla 保险公司已经同意承保并进入仲裁程序。对方律师（Colman Perkins Law Group）正式送来了三套书面问题，"
     "法律上我们必须在期限内逐条书面回答，并且由您本人宣誓签字。", False),
    ("我们已经先把能查的都替您填好了 —— 警方报告、病历、保险资料、八月已经交给对方的材料，"
     "这些我们手上都有，不用再麻烦您回忆。全问卷 50 题，其中 28 题我们已经填上答案，"
     "只有 22 题需要您自己回答。", False),
    ("所以这份问卷分两种：", False),
    ("　【我们已填，请核对】—— 蓝色字是我们写好的答案。请您看一遍：对的就在下面写「正确」；"
     "有出入、或者要补充的，请直接在蓝字上面改。我们可能记错，以您为准。", False),
    ("　【请您填写】—— 这些只有您知道，我们查不到，请您填在空白格里。", False),
    ("格子会随着您打字自动变大，写多少都可以。", False),
    ("与您情况无关的题，请写「不适用」，不要留空。留空在法律上会被当成拒绝回答，可能被罚。", True),
    ("记不清的，就写「记不清」，再尽量给个大概时间或范围。千万不要猜、不要编 —— "
     "这份回答是您宣誓作出的，对方会拿去和病历、保险记录逐条核对。", True),
    ("这次最要紧的是三件事：① 2026 年 4 月 21 日那次事故，和这次伤到的部位有重叠（头部、手部），"
     "对方一定会拿它来说您现在的症状不是这次事故造成的；② 您看过的每一家医疗机构都要列全；"
     "③ 受伤部位的照片我们一张都没有，请务必找出来。", True),
    ("有红色字的地方请特别留意，那是最容易出问题的几处。", False),
]

G1 = ("一、基本信息", [
 ("本份问卷由谁协助您填写？请写姓名、地址、电话，以及与您的关系。（只负责打字的人不用写。）",
  2, "FROG 1.1", None),
 ("您的姓名，以及过去用过的其他姓名和使用年份。",
  2, "FROG 2.1", None,
  "姓名：Jiayu Ma\n曾用名：没有用过其他姓名"),
 ("您的出生日期和出生地。",
  2, "FROG 2.2", None,
  "出生日期：1997 年 1 月 27 日\n出生地：中国 广东省 台山"),
 ("您的驾照：发照州、驾照号和类型、发照日期、有无限制。",
  3, "FROG 2.3、2.4", None,
  "发照州：加利福尼亚州\n驾照号及类型：Y2849591，C 类\n发照日期：2025 年 3 月 13 日\n"
  "限制：须配戴矫正眼镜\n其他驾照或许可证：没有"),
 ("您现在的住址，以及事故发生前五年住过的每一个地址和居住起止年月。",
  4, "FROG 2.5",
  "2020 年之前住在哪里，我们没有记录，这一段请您补上。",
  "现住址：1731 Walnut Street, San Gabriel, CA 91776\n居住期间：2020 年 — 至今\n"
  "2020 年之前的地址：（请补）"),
 ("工作经历（这一题只是背景资料，不是在问工资损失）：事故发生前五年至今您做过的每一份工作 —— "
  "公司名称、地址、电话、职位、工作内容、起止年月。",
  5, "FROG 2.6、8.2",
  "我们在 2026 年 8 月已经正式书面告知对方：您在事发时没有雇主、本案不主张工资损失。"
  "这一题请如实写工作经历即可，不要填写任何工资损失金额。",
  "2022 — 2024：聚点，18558 Gale Ave #272, City of Industry, CA 91748，职位：经理\n"
  "2024 — 2025 年 11 月 14 日（事发时）：无雇主\n"
  "事发之后至今：（如有工作请补）"),
 ("学历：高中起每一所学校的名称、地址、就读年月、最高学历和学位。",
  4, "FROG 2.7", None,
  "高中：Alhambra High School，2012 — 2015\n高中之后的学校 / 培训：（请补，没有就写「没有」）\n"
  "最高学历：（请补）"),
 ("您是否曾被判定犯有重罪（felony）？如果有，请写明定罪的城市和州、日期、罪名、法院和案件编号。",
  3, "FROG 2.8",
  "八月那份问卷这题留了空白，这次必须明确回答「有」或「没有」。请务必如实、完整填写 —— "
  "隐瞒会严重损害您的案件。"),
 ("您能否轻松地用英语口头交流？能否阅读和书写英文？如果不能，平时用什么语言和方言？",
  2, "FROG 2.9、2.10",
  "这题决定您签署宣誓书时是否需要翻译人员，请如实回答。"),
 ("事故发生时，您是否正在上班或替别人办事（例如送货、跑单）？",
  3, "FROG 2.11", None,
  "否。事故发生时您没有雇主，也不是在为他人执行工作任务。"),
 ("事故发生时，您或其他涉事人员身上是否有任何身体、情绪或精神方面的状况，可能影响了事情的发生？",
  3, "FROG 2.12", None),
 ("事故发生前 24 小时内，您或任何涉事人员是否服用过酒精、大麻或任何药物（含医生开的日常处方药）？"
  "如有，请写药名、用量、服用时间和地点、在场的人、开药医生。",
  4, "FROG 2.13",
  "包括降压药、糖尿病药、过敏药、安眠药等日常处方药。警方报告记载双方均未饮酒，"
  "但用药这一项报告没写，需要您自己回答。"),
])

G2 = ("二、事故经过", [
 ("本次事故的日期、时间和具体地点。",
  3, "FROG 20.1", None,
  "日期：2025 年 11 月 14 日（星期五）\n时间：上午 10:00\n"
  "地点：Puente Avenue，Nelson Avenue 以南约 164 英尺处，City of Industry，洛杉矶县\n"
  "（GPS 34.046331, -117.98599；当时下雨、路面湿滑、白天）"),
 ("涉事车辆与人员的完整信息。",
  7, "FROG 20.2、20.11", None,
  "【您的车辆】2017 Tesla Model X，黑色，车牌 9TKF799 (CA)，VIN 5YJXCDE23HF033157\n"
  "　驾驶人／登记车主：Jiayu Ma，1731 Walnut Street, San Gabriel, CA 91776，(626) 747-3362\n"
  "　（登记地址另记为 173 Amberwood Dr, Walnut, CA 91789）\n"
  "　乘客：Amy Hengye Chen（生日 1998/05/10），22050 Roundup Drive, Walnut, CA 91789，(626) 277-7668\n"
  "　保险：Tesla，保单号 TLACAAR9993NTRL　｜　事故后由 Haddicks Tow (626) 330-3289 拖走\n"
  "【对方车辆】2007 Mazda 6，银色，车牌 8BEC710 (CA)，VIN 1YVHP80C675M59273\n"
  "　驾驶人／登记车主：Karen Elizabeth Prado（生日 1989/11/16），225 Basetdale Avenue, "
  "La Puente, CA 91746，(626) 262-8193，驾照 Y8181781 (CA)\n"
  "　保险：National General，保单号 2029729427　｜　同样由 Haddicks Tow 拖走"),
 ("本次行程的出发地址和目的地；以及您从出发到事故地点所走的路线，和途中每一次停留的地点"
  "（红灯停车除外）。",
  4, "FROG 20.3、20.4",
  "这一题只有您知道，警方报告里没有，请务必填写。"),
 ("事故发生前 500 英尺路段，每一辆车所在的街道、车道和行驶方向。",
  3, "FROG 20.5", None,
  "双方车辆均沿 Puente Avenue 由北向南（southbound）行驶，同在第 1 车道。\n"
  "该路段双向共 2 条直行车道，限速 40 英里／小时。"),
 ("事故是否发生在路口？该处有哪些交通管制设施、信号灯或标志？",
  3, "FROG 20.6、20.7", None,
  "否。事故发生在 Puente Avenue 路段上，位于 Nelson Avenue 以南约 164 英尺处，不在路口。\n"
  "警方报告记载该处「无交通管制设施」，因此当时没有面向您的交通信号灯。"),
 ("事故是怎么发生的？请就「事故发生前一刻」「事故发生时」「事故发生后一刻」三个时点，"
  "分别写出两辆车的速度、方向和位置；然后再用文字完整描述一遍经过。",
  8, "FROG 20.8",
  "下面是警方报告记载的骨架。请您补上细节：当时为什么停下（前车、红灯、车流）、"
  "撞击有多重、身体当下的感觉、事发后双方说了什么、各自做了什么。这是整份问卷最重要的一题。",
  "【事发前一刻】您的 Tesla：在 Puente Avenue 南行第 1 车道上「已停止」。\n"
  "　对方 Mazda：同一车道南行，「直行前进」中。\n"
  "【事发时】对方车辆从后方追撞您车尾部（警方认定为 rear-end 追尾）。\n"
  "【事发后】两车均需拖走：您的车损列为「中度」，对方车损列为「重大」，均由 Haddicks Tow 拖离。\n"
  "　您当场向警方表示颈部和背部疼痛，由洛杉矶县消防 87 队救护（EMS 编号 FAULK 604）"
  "送往 Queen of the Valley 医院。"),
 ("您是否掌握任何信息，显示某辆车的故障或缺陷导致了本次事故，或加重了事故中所受的伤害？",
  3, "FROG 20.9、20.10", None,
  "没有。警方报告对两辆车均记载「无明显既有机械缺陷」。"),
 ("您认为除您以外，还有谁对本次事故的发生或您的伤害负有责任？依据是什么？"
  "知道这些事实的人是谁？有哪些文件能支持？",
  5, "FROG 16.1、14.1",
  "下面是我们依据警方报告写的。如果您还知道别的事实（例如对方当场说了什么），请补上。",
  "责任方：对方驾驶人 Karen Elizabeth Prado。\n"
  "依据：警方报告将本次事故的「主要碰撞原因」认定为对方违反加州车辆法第 22350 条"
  "（基本速度法 —— 未按路况保持安全车速）。当时下雨、路面湿滑，您的车辆已经停止，"
  "对方直行追撞您车尾。警方同时记载双方均未饮酒、手机均未在使用中。\n"
  "知情人：您本人；乘客 Amy Hengye Chen；对方驾驶人；制作报告的警员 Juan Nava（编号 629494）。\n"
  "支持文件：交通事故报告 No. 925-11016-1412-471；您在现场拍摄的照片和视频。"),
 ("因本次事故，是否有任何人被开罚单或被指控违规？",
  3, "FROG 14.2",
  "警方报告把主要碰撞原因认定在对方身上（车辆法 22350），但报告上「是否开具传票」那一栏"
  "不够清楚。这一项我们会向法院和警局核实，您只要写下您当场看到或听到的情况即可。"),
 ("事故发生时您使用的手机号码，以及当时的手机运营商。",
  2, "SROG 17、19",
  "对方另外还要您的手机账户账号 —— 那一项我们会代为处理并提出异议，您不用填。"
  "顺带说明：警方报告已经记载双方「手机均未在使用中」，这对我们很有利。",
  "手机号码：(626) 747-3362\n当时的运营商：（请补）"),
])

G3 = ("三、证人、照片与调查", [
 ("目击本次事故、或事故前后紧接情形的人；在现场说过话的人；您认为了解本次事故情况的其他人 —— "
  "请写出姓名、地址、电话。",
  5, "FROG 12.1", None,
  "乘客：Amy Hengye Chen，22050 Roundup Drive, Walnut, CA 91789，(626) 277-7668"
  "（事发时坐在您车内）\n"
  "对方驾驶人：Karen Elizabeth Prado，225 Basetdale Avenue, La Puente, CA 91746，(626) 262-8193\n"
  "出警警员：Juan Nava，编号 629494\n"
  "其他目击者：（如有请补；没有就写「没有其他目击者」）"),
 ("是否有照片、录像、监控、行车记录仪拍到现场、车辆或您的伤？请写明是谁拍的、什么时候拍的、"
  "现在在谁手里。",
  4, "FROG 12.4",
  "我们手上目前【一张伤处照片都没有】。如果您当时或之后拍过伤口、淤青、肿胀的照片，"
  "请务必找出来发给我们。照片和视频请发手机相册里的原始文件，不要用微信压缩过的图、"
  "也不要翻拍 —— 对方明确写了不接受截图和复印件。",
  "已有：现场照片 1 张（拍到对方车辆前端损坏、路面碎片、湿滑路面和到场警车），"
  "现场视频 1 段，均为您本人在 2025 年 11 月 14 日事故现场拍摄，已于 2026 年 8 月交给对方。\n"
  "伤处照片：（请提供）\n"
  "您车辆损坏的照片：（请提供）\n"
  "行车记录仪 / Tesla 车载录像：（如有请提供）"),
 ("事故之后您有没有再回过现场？什么时候去的？有没有拍照或录像？",
  3, "FROG 12.7", None),
 ("是否有任何人就本次事故作过报告？",
  3, "FROG 12.6", None,
  "有。加州交通事故报告（CHP 555）第 925-11016-1412-471 号，制作人警员 Juan Nava（编号 629494），"
  "2025 年 11 月 14 日制作，2025 年 11 月 19 日由 Ryan Nazaroff（编号 612130）复核。\n"
  "该报告已于 2026 年 8 月交给对方。除此之外您是否还知道有其他报告？（如有请补）"),
 ("您或任何代表您的人，是否就本次事故询问过任何人，或取得过任何人的书面、录音、录像陈述？",
  3, "FROG 12.2、12.3", None,
  "没有。我们在 2026 年 8 月已书面答复对方：未向任何证人取得过书面、录音或录像陈述；"
  "事发时您车上有一名乘客，也未向她取过陈述。请确认是否仍然如此。"),
 ("您或任何代表您的人，是否知道有任何与本次事故有关的现场图、复制件或模型？",
  2, "FROG 12.5", None,
  "没有。（警方报告本身附有现场示意图，除此之外我们不知道有其他图示或模型。）"),
 ("您或任何代表您的人，是否对任何涉事人员进行过跟踪监视？是否就此制作过书面报告？",
  2, "FROG 13.1、13.2", None,
  "没有，也没有制作过任何相关报告。"),
])

G4 = ("四、受伤与治疗", [
 ("请列出这次事故造成的所有受伤部位和伤情。",
  4, "FROG 6.1、6.2", None,
  "当场向警方表示：颈部和背部疼痛。\n"
  "您在八月问卷上写的受伤部位：头部、腰部、肩部、手部。\n"
  "请确认是否完整，有遗漏的部位请补上。"),
 ("到今天为止您还有哪些不适？每一项请分别说明：① 具体症状和部位；② 在好转 / 没有变化 / 在加重；"
  "③ 多久发作一次、每次持续多久。",
  5, "FROG 6.3",
  "这一题只有您知道，请务必按现在的实际情况写。"),
 ("请列出因为这次事故您看过的每一家医疗机构：名称、地址、电话、看了什么、就诊起止日期。",
  7, "FROG 6.4、SROG 20",
  "下面这份名单是从我们已经收到的病历整理的。请核对，并补上名单上没有的 —— "
  "包括只去过一次的、以及 2026 年 8 月之后新看的。漏掉的那一家，它的费用很可能拿不回来。",
  "1. Emanate Health Queen of the Valley Hospital（急诊）—— 2025 年 11 月 14 日\n"
  "2. Premier Integrative Health Center（脊椎推拿）—— 2025 年 11 月 17 日 至 2026 年 3 月 10 日\n"
  "3. Sun Imaging, Inc.（颈椎、腰椎 MRI）—— 2026 年 1 月 8 日\n"
  "4. Precision Pain Care Center，Tony Liu, D.O.（疼痛科）—— 2026 年 2 月 6 日 至 3 月 30 日\n"
  "5. RelivCare Surgery Center（介入治疗手术场所）—— 2026 年 2 月 12 日、3 月 16 日\n"
  "6. Southern California Injury Treatment Center，Victoria Trinh, M.D.（神经科）"
  "—— 2026 年 3 月 10 日 至 4 月 21 日\n"
  "7. Spectrum MRI Imaging Center（脑部 MRI）—— 2026 年 3 月 23 日\n"
  "8. 洛杉矶县消防局救护（87 队，EMS 编号 FAULK 604）—— 2025 年 11 月 14 日，记录我们仍在索取中\n"
  "9. 以上之外还看过的：（请补）"),
 ("因为这次受伤您吃过哪些药（包括自己在药房买的止痛药、药膏、贴剂）？"
  "请写药名、谁开的、起止服用日期、花了多少钱。",
  4, "FROG 6.5",
  "对方同时要求提供药品收据和处方单，麻烦一并找出来。"),
 ("有没有救护车、护理、医疗器材等其他医疗相关支出？",
  3, "FROG 6.6", None,
  "救护车：2025 年 11 月 14 日由洛杉矶县消防局 87 队送往 Queen of the Valley 医院"
  "（EMS 编号 FAULK 604）。该笔账单我们仍在索取。\n"
  "其他（护理、支架、颈圈、医疗器材等）：（请补）"),
 ("有没有医生告诉您以后还需要继续治疗或手术？是哪位医生、针对什么症状、预计怎么治、大概多少钱？",
  4, "FROG 6.7", None),
 ("本次事故是否造成了外观上的损伤，例如疤痕？如有，请逐一完整描述（部位、大小、现状）。",
  3, "SROG 9", None),
 ("您是否主张本次事故造成了精神上的痛苦？如果是：请列出事故之后您因此看过的每一位心理治疗师，"
  "以及事故发生前五年内您看过的每一位心理治疗师。",
  4, "SROG 13、14",
  "如果您并不打算主张精神损害，请明确写「不主张」—— 否则对方有权调取您过去五年的心理治疗记录。"),
])

G5 = ("五、既往病史与其他事故", [
 ("这次受伤之前，您在同一个身体部位（头部、颈部、腰背、肩部、手部）有没有受过伤或有过不适？"
  "如果有：哪个部位、什么时候开始和结束、看过哪些医生。另外请列出过去十年内，"
  "凡就这些部位看过的所有医疗机构。",
  5, "FROG 10.1、SROG 21",
  "请务必如实填写。对方会去调取您的病历，隐瞒旧伤反而会被用来攻击本次受伤的因果关系。"),
 ("事故发生前，您本来就有哪些身体、精神或情绪方面的健康问题？本次事故有没有让它们加重？"
  "如果有，请说明原本是什么状况、怎么被加重的、涉及哪些部位，以及为此治疗过的医疗机构。",
  5, "FROG 10.2、SROG 7、8", None),
 ("本次事故【之后】，您是否又发生过其他事故或再次受伤？",
  7, "FROG 10.3、SROG 3、4、6",
  "这是本案最关键的一题。4/21/2026 那次事故伤到的头部和手部，和本次事故重叠，"
  "对方一定会拿它来主张您现在的症状不是本次事故造成的。请写得尽量具体 —— "
  "特别是：您现在正在做的每一项治疗，分别是针对哪一次事故。分清楚了，本次的赔偿才守得住。",
  "我们已知：2026 年 4 月 21 日另有一次事故，您在八月问卷上写的受伤部位是头部和手部。\n"
  "请补充：\n　· 发生的日期、时间、地点\n　· 涉及的其他人（姓名／电话／地址）和对方保险\n"
  "　· 是否报警、有没有报案编号\n　· 您那次的受伤部位和伤情\n"
  "　· 为那次看过的所有医生和医疗机构、治疗方式、起止时间\n"
  "　· 您目前仍在接受的治疗，分别是针对 11/14/2025 还是 4/21/2026"),
 ("过去十年内，除上面两次之外，您是否还发生过其他造成受伤的事故（车祸、场所事故、工伤都算）？"
  "无论当时有没有索赔都要回答。",
  4, "SROG 3、4", None),
 ("本次事故发生时，您的主治医生 / 家庭医生是谁（姓名、地址、电话）？",
  2, "SROG 2", None),
 ("除本案外，过去十年内您是否曾就人身伤害提起过诉讼，或提出过书面索赔？",
  5, "FROG 11.1", None),
 ("过去十年内（对方另问过去五年），您是否提出过工伤赔偿申请？如有，请写明时间地点、雇主、"
  "工伤保险公司和理赔号、领取期间、受伤情况、治疗机构，以及 WCAB 案件编号。",
  5, "FROG 11.2、SROG 15", None),
])

G6 = ("六、保险", [
 ("您的健康保险：计划名称、保单号或会员号，以及所有被保险人的姓名、地址、电话。"
  "另外请说明本次事故涉及的车辆保险。",
  5, "FROG 4.1、SROG 5、10",
  "请把 Medi-Cal 卡正反面、以及任何其他健保卡正反面拍照发给我们。"
  "另外请明确回答一件事：您是否曾经加入过 Medicare（Part A 或 Part B）？"
  "Medi-Cal 和 Medicare 是两回事，对方两样都问了。",
  "健康保险：Medi-Cal（您在八月问卷上写的「红白卡」）。加州医疗服务部（DHCS）就本次事故"
  "已支付 $484.58，并已将求偿金额减至 $363.44（DHCS 账号 C94683466F-001）。\n"
  "您的车辆保险：Tesla Insurance，保单号 TLACAAR9993NTRL —— 本次仲裁就是依据这张保单的"
  "「保险不足驾驶人」条款提出的。\n"
  "对方驾驶人的保险：National General，保单号 2029729427，人身伤害责任限额 $30,000／人。"
  "该限额已于 2026 年 3 月 9 日全额赔付完毕。\n"
  "其他健保（雇主团保、Covered CA、商业保险等）：（请补，没有就写「没有」）"),
 ("就本次事故引起的损害，您是否依据任何法律属于自保（self-insured）？",
  2, "FROG 4.2", None,
  "否。"),
])

G7 = ("七、财产损失与误工", [
 ("本次事故造成了哪些财产损失？请描述物品、损坏的性质和部位、索赔金额及计算方式。",
  4, "FROG 7.1", None,
  "车辆：2017 Tesla Model X，车牌 9TKF799。警方报告记载损坏程度为「中度」，损坏位置在车尾，"
  "事故后由 Haddicks Tow (626) 330-3289 拖离现场。\n"
  "除车辆外，是否还有其他物品损坏（手机、眼镜、随身物品等）？（请补）"),
 ("上述财产是否有人出具过书面估价单或评估报告？是否已经修理？"
  "请写明日期、内容、金额、修理厂，以及是谁付的钱。",
  4, "FROG 7.2、7.3",
  "我们档案里有维修估价补充单、Invoice 21372 和拖车收据，起草答复时会一并整理。"
  "请您确认车辆最后是修好了、卖掉了，还是判为全损。"),
 ("关于工资损失：我们在 2026 年 8 月已经书面告知对方，您在 2025 年 11 月 14 日事发时没有雇主，"
  "本案不主张工资损失（但保留「劳动能力减损」这一项）。请确认这个说法是否仍然准确。",
  4, "FROG 8.1–8.8",
  "如果事发时其实有收入来源（打零工、自雇、现金工作等），请现在说明，不要等到对方发现。"
  "宣誓后前后矛盾，比一开始就说清楚严重得多。"),
 ("除以上之外还有哪些自付开销？（自费医药费、交通费、停车费、护工费、请人做家务的费用等）"
  "请写项目、日期、金额、付给谁，并说明有哪些单据可以证明。",
  4, "FROG 9.1、9.2", None),
])

GROUPS = [G1, G2, G3, G4, G5, G6, G7]

DOCS_HEADING = "八、需要您提供的材料"
DOCS_SUBNOTE = ("对方同时送达了 Request for Production of Documents（共 26 项），"
                "以下是其中需要您配合的部分。我们在 2026 年 8 月已经向对方提交过一批材料"
                "（JM-000001 至 JM-000162），已经交过的不用重复，只补新的。")
RFP_DOCS = [
 "所有与本次事故有关的原始照片和视频（现场、车辆、伤处、行车记录仪）—— 请提供手机里的原始文件，"
 "不要用微信压缩过的图片或翻拍，对方明确表示不接受复印件和截图",
 "2026 年 4 月 21 日那次事故的所有材料：警方报告、理赔号、照片、病历和账单",
 "本次事故之后所有就诊的病历和账单（包括八月之后新增的部分）",
 "过去五年内，就同样身体部位看过医生的病历或报告",
 "所有药品收据、处方单（含自己在药房买的止痛药、药膏）",
 "健保卡正反面（含红白卡 / Medicare 卡），以及任何 EOB（Explanation of Benefits）或付款通知",
 "事故前三个月和事故后三个月的工资单 / 收入证明 / 请假记录",
 "车辆维修估价单、维修发票、拖车和租车收据",
 "警方事故报告、报案编号，或任何他人就本次事故所作的报告",
 "您自己记录的就诊日程、日记、备忘或录音（只要提到本次事故或您的伤情）",
 "加州驾照复印件",
 "任何目击者的书面、录音或录像陈述",
]
DEPO_NOTE = ("另外请注意：Tesla 在回函中已经声明保留对治疗必要性和合理性提出争议的权利，"
             "并且会安排独立医学检查（IME）和取证。这些都还没有排期，届时我们会提前帮您准备，"
             "现在不用担心。")
