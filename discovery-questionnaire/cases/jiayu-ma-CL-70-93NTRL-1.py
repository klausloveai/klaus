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
     "法律上我们必须在期限内逐条书面回答，并且由您本人宣誓签字。这份中文问卷是我们把那些问题整理、翻译、"
     "合并之后的版本 —— 您只要照着填，剩下的格式和法律措辞由我们来处理。", False),
    ("请在每个问题下面的空白格里直接打字或手写。格子会自动变大，写多少都可以。", False),
    ("有几题下面我们已经写上了您今年八月填过的内容。那一份当时很多地方留了空白，这次必须填完整。"
     "已经写上的部分请您核对一遍：对的就写「正确」，有出入或有补充的请直接改。", False),
    ("与您情况无关的题，请写「不适用」，不要留空。留空在法律上会被当成拒绝回答，可能被罚。", True),
    ("记不清的，就写「记不清」，再尽量给个大概时间或范围。千万不要猜、不要编 —— 这份回答是您宣誓作出的，"
     "对方会拿去和病历、保险记录逐条核对。", True),
    ("这次最关键的是两件事：① 2026 年 4 月 21 日那次事故，和这次伤到的部位有重叠（头部、手部），"
     "对方一定会拿它来说您现在的症状不是这次事故造成的；② 您看过的每一家医疗机构都要列全。"
     "这两处请务必写细、写准。", True),
    ("有红色字的地方请特别留意，那是最容易出问题的几处。", False),
]

G1 = ("一、基本信息", [
 ("本份问卷由谁协助您填写？请写姓名、地址、电话，以及与您的关系。（只负责打字的人不用写。）",
  2, "FROG 1.1", None),
 ("您的姓名，以及过去用过的其他姓名和使用年份。\n"
  "我们八月的记录：Jiayu Ma；没有用过其他姓名。请确认。",
  2, "FROG 2.1", None),
 ("您的出生日期和出生地。\n我们八月的记录：1997 年 1 月 27 日，出生于中国广东台山。请确认。",
  2, "FROG 2.2", None),
 ("您的驾照：发照州、驾照号和类型、发照日期、有无限制。\n"
  "我们八月的记录：加州 Y2849591，C 类，2025 年 3 月 13 日签发，限制「须配戴眼镜」；没有其他州的驾照或许可证。请确认。",
  3, "FROG 2.3、2.4", None),
 ("您现在的住址，以及事故发生前五年住过的每一个地址和居住起止年月。\n"
  "我们八月的记录：1731 Walnut St, San Gabriel, CA 91776，2020 年至今。"
  "请补上 2020 年之前住过的地址。",
  4, "FROG 2.5", None),
 ("您现在的工作：公司名称、地址、电话、职位、工作内容、入职时间。"
  "另外请列出事故发生前五年至今做过的其他工作（同样信息）。\n"
  "我们八月的记录只有：聚点，18558 Gale Ave #272, City of Industry, CA 91748，2022–2024，经理。"
  "现在的工作是空白的，请务必补上。",
  5, "FROG 2.6、8.2", "现在的工作信息是空的，这一栏直接影响误工索赔，请填完整。"),
 ("学历：高中起每一所学校的名称、地址、就读年月、最高学历和学位。\n"
  "我们八月的记录：Alhambra High School，2012–2015。高中之后的学校和最高学历是空白的，请补上。",
  4, "FROG 2.7", None),
 ("您是否曾被判定犯有重罪（felony）？如果有，请写明定罪的城市和州、日期、罪名、法院和案件编号。",
  3, "FROG 2.8",
  "八月这题留了空白，这次必须明确回答「有」或「没有」。请务必如实、完整填写 —— 隐瞒会严重损害您的案件。"),
 ("您能否轻松地用英语口头交流？能否阅读和书写英文？如果不能，平时用什么语言和方言？",
  2, "FROG 2.9、2.10",
  "这题决定您签署宣誓书时是否需要翻译人员，请如实回答。"),
 ("事故发生时，您是否正在上班或替别人办事（例如送货、跑单）？如果是，请写明雇主名称、地址、电话和您当时的职责。",
  3, "FROG 2.11", None),
 ("事故发生时，您或其他涉事人员身上是否有任何身体、情绪或精神方面的状况，可能影响了事情的发生？",
  3, "FROG 2.12", None),
 ("事故发生前 24 小时内，您或任何涉事人员是否服用过酒精、大麻或任何药物（含医生开的日常处方药）？"
  "如有，请写药名、用量、服用时间和地点、在场的人、开药医生。",
  4, "FROG 2.13",
  "包括降压药、糖尿病药、过敏药、安眠药等日常处方药。八月这题留了空白，这次请明确回答。"),
])

G2 = ("二、事故经过", [
 ("本次事故的日期、时间和具体地点（最近的街道地址或路口）。",
  3, "FROG 20.1", None),
 ("请就每一辆涉事车辆填写：年份 / 厂牌 / 型号 / 车牌号；驾驶人姓名、地址、电话；"
  "除驾驶人外每位乘客的姓名、地址、电话；登记车主；承租人；其他所有人；以及同意驾驶人用车的人。"
  "请分「您的车辆」和「对方车辆」两段写。",
  6, "FROG 20.2", None),
 ("本次行程的出发地址和目的地地址；以及您从出发到事故地点所走的路线，"
  "和事故发生前途中每一次停留的地点（红灯停车除外）。",
  4, "FROG 20.3、20.4", None),
 ("事故发生前 500 英尺路段，每一辆车所在的街道 / 道路名称、所在车道、行驶方向。",
  3, "FROG 20.5", None),
 ("事故是否发生在路口？如果是，请描述该路口的所有交通管制设施、信号灯或标志。",
  3, "FROG 20.6", None),
 ("事故发生时是否有面向您的交通信号灯？如果有：您第一次看到它时在什么位置、当时是什么颜色、"
  "该颜色已持续几秒、从您看到到事故发生灯色有没有变过。",
  3, "FROG 20.7", None),
 ("请说明事故是怎么发生的 —— 分「事故发生前一刻」「事故发生时」「事故发生后一刻」三个时点，"
  "分别写出您的车辆和对方车辆的速度、方向和位置。然后再用文字完整描述一遍经过"
  "（撞击部位、先后顺序、事发后双方的反应）。",
  8, "FROG 20.8",
  "这是整份问卷最重要的一题，请尽量写细。"),
 ("您是否掌握任何信息，显示某辆车的故障或缺陷导致了本次事故，或加重了事故中所受的伤害"
  "（例如安全带、安全气囊失灵）？如有，请写明车辆、故障内容、知情人和部件保管人。",
  4, "FROG 20.9、20.10", None),
 ("您认为除您以外，还有谁（对方司机或其他人）对本次事故的发生或您的伤害负有责任？"
  "请写出您这么认为所依据的全部事实、知情人的姓名地址电话，以及能支持这一点的文件。",
  5, "FROG 16.1、14.1",
  "这题是对方在问「您凭什么说是我方被保险人之外的人造成的」。请把您知道的事实写全。"),
 ("因本次事故，是否有任何人被开罚单或被指控违规？如有，请写明姓名地址电话、被指违反的法条、"
  "有没有作出答辩、以及法院或行政机关名称和案件编号。",
  3, "FROG 14.2", None),
 ("请列出事故发生时您使用的手机号码，以及当时的手机运营商。",
  2, "SROG 17、19",
  "对方另外还要您的手机账户账号 —— 那一项我们会代为处理并评估提出异议，您不用填。"),
])

G3 = ("三、证人、照片与调查", [
 ("请写出下列每一类人的姓名、地址、电话：① 目击事故本身、或事故前后紧接情形的人；"
  "② 在现场说过话的人；③ 在现场听到他人谈论事故的人；④ 您认为了解本次事故情况的其他人。",
  5, "FROG 12.1", None),
 ("是否有照片、录像、监控、行车记录仪拍到现场、车辆或您的伤？"
  "请写明数量、拍的是什么、拍摄日期、谁拍的、现在在谁手里。",
  4, "FROG 12.4",
  "对方在文件里明确要求提供「原始照片」，不接受复印件或截图。"
  "请把原始数码文件（手机原图、原视频）发给我们，不要用微信压缩过的图或翻拍。"),
 ("事故之后您有没有再回过现场？什么时候去的？有没有拍照或录像？",
  3, "FROG 12.7", None),
 ("是否有任何人就本次事故作过报告（警方事故报告、保险公司报告、公司内部报告）？"
  "请写明制作人姓名 / 职务 / 工号 / 单位、报告日期和类型、为谁制作、现在谁持有。",
  3, "FROG 12.6", None),
 ("您或任何代表您的人，是否就本次事故询问过任何人，或取得过任何人的书面、录音、录像陈述？"
  "如有，请写明被询问人、询问人、日期，以及现在谁持有。",
  3, "FROG 12.2、12.3", None),
 ("您或任何代表您的人，是否知道有任何与本次事故有关的现场图、复制件或模型？",
  2, "FROG 12.5", None),
 ("您或任何代表您的人，是否对任何涉事人员进行过跟踪监视？是否就此制作过书面报告？",
  2, "FROG 13.1、13.2",
  "这两题通常答「没有」，但仍须明确回答，不能留空。"),
])

G4 = ("四、受伤与治疗", [
 ("请列出这次事故造成的所有受伤部位和伤情。\n"
  "我们八月的记录：头部、腰部、肩部、手部。请确认，并补上当时漏掉的部位和具体伤情描述。",
  4, "FROG 6.1、6.2", None),
 ("到今天为止您还有哪些不适？每一项请分别说明：① 具体症状和部位；② 在好转 / 没有变化 / 在加重；"
  "③ 多久发作一次、每次持续多久。",
  5, "FROG 6.3", None),
 ("请列出因为这次事故您看过的每一家医院、急诊、诊所、推拿 / 针灸、理疗、影像中心（MRI / X-ray）"
  "和专科医生：名称、地址、电话、看了什么、就诊起止日期、至今费用。",
  7, "FROG 6.4、SROG 20",
  "必须列全，包括只去过一次的。对方会直接去这些机构调病历；漏掉的那家，"
  "它的治疗费用很可能拿不回来。"),
 ("因为这次受伤您吃过哪些药（包括自己在药房买的止痛药、药膏、贴剂）？"
  "请写药名、谁开的、开药日期、起止服用日期、花了多少钱。",
  4, "FROG 6.5", None),
 ("有没有救护车、护理、医疗器材等其他医疗相关支出？请写明项目、日期、费用、提供方。",
  3, "FROG 6.6", None),
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
 ("这次受伤之前，您在同一个身体部位（头部、腰部、肩部、手部）有没有受过伤或有过不适？"
  "如果有：是哪个部位、什么时候开始和结束、看过哪些医生（名称、地址、电话）。"
  "另外请列出过去十年内，凡就这些部位看过的所有医疗机构。",
  5, "FROG 10.1、SROG 21",
  "请务必如实填写。对方会去调取您的病历，隐瞒旧伤反而会被用来攻击本次受伤的因果关系。"),
 ("事故发生前，您本来就有哪些身体、精神或情绪方面的健康问题？"
  "本次事故有没有让它们加重？如果有，请说明原本是什么状况、怎么被加重的、涉及哪些部位，"
  "以及为此治疗过的医疗机构。",
  5, "FROG 10.2、SROG 7、8", None),
 ("本次事故【之后】，您是否又发生过其他事故或再次受伤？\n"
  "我们八月的记录：2026 年 4 月 21 日另有一次事故，伤到头部和手部。\n"
  "请就那一次补充完整：发生日期和地点、涉及的其他人（姓名 / 电话 / 地址）、您的受伤部位、"
  "为此看过的所有医生和医疗机构、治疗方式和持续时间。",
  7, "FROG 10.3、SROG 3、4、6",
  "这是本案最关键的一题。4/21/2026 那次事故伤到的头部和手部，和本次事故重叠，"
  "对方一定会拿它来主张您现在的症状不是本次事故造成的。请写得尽量具体，"
  "特别是哪些治疗是针对哪一次事故 —— 分清楚了才守得住本次的赔偿。"),
 ("过去十年内，除了上面两次之外，您是否还发生过其他造成受伤的事故（车祸、场所事故、工伤都算）？"
  "无论当时有没有索赔都要回答。如有，请写明时间地点，以及因此治疗过的医疗机构。",
  4, "SROG 3、4", None),
 ("请说明本次事故发生时，您的主治医生 / 家庭医生是谁（姓名、地址、电话）。",
  2, "SROG 2", None),
 ("除本案外，过去十年内您是否曾就人身伤害提起过诉讼，或提出过书面索赔？"
  "如有，请写明时间 / 地点、对方是谁、法院和案号、当时的律师、结果、受伤情况。",
  5, "FROG 11.1", None),
 ("过去十年内（对方另问过去五年），您是否提出过工伤赔偿申请？"
  "如有，请写明时间地点、当时的雇主、工伤保险公司和理赔号、领取期间、受伤情况、"
  "治疗机构，以及 WCAB 案件编号。",
  5, "FROG 11.2、SROG 15", None),
])

G6 = ("六、保险", [
 ("您的健康保险：保险公司名称、地址、保单号 / 会员号，以及所有被保险人的姓名、地址、电话。\n"
  "我们八月的记录只有「红白卡」（即 Medicare）。请补上完整信息；如果同时还有别的健保也一并写。",
  4, "FROG 4.1、SROG 5、10",
  "请把健保卡（含红白卡）正反面拍照发给我们。您若是 Medicare 受益人，"
  "我们必须在和解前处理 Medicare 的求偿，这一步漏了会影响最后拿到手的金额。"
  "对方另外要您的 Medicare Claim Number —— 那一项由我们处理，您不用填在这张表上。"),
 ("就本次事故引起的损害，您是否依据任何法律属于自保（self-insured）？如果是，请指明具体法条。",
  2, "FROG 4.2", None),
])

G7 = ("七、财产损失与误工", [
 ("本次事故造成了哪些财产损失？请描述物品、损坏的性质和部位、索赔金额及计算方式；"
  "如果已出售，请写明买方姓名 / 地址 / 电话、出售日期和售价。\n"
  "我们八月的记录：车辆尾部受损。请补上车辆年份 / 厂牌 / 型号 / 车牌号和金额。",
  4, "FROG 7.1", None),
 ("上述财产是否有人出具过书面估价单或评估报告？如有，请写明出具人、日期、持有副本的人、"
  "以及报告中载明的金额。",
  3, "FROG 7.2", None),
 ("上述财产是否已经修理？如有，请写明修理日期、修理内容、费用、修理厂，以及是谁付的钱。",
  3, "FROG 7.3", None),
 ("您是否因为这次事故损失工资？如果有：事故前最后一次上班是哪天？哪些日子没能上班？"
  "什么时候复工的（按每个工作单位分别写）？",
  4, "FROG 8.1、8.3、8.5、8.6",
  "如有误工，请提供事故前三个月和事故后三个月的工资单、收入证明或请假记录。"),
 ("您事故发生时的收入：时薪或月薪、每周上几天、每天几小时、月收入大约多少？"
  "至今一共损失了多少工资，是怎么算出来的？",
  4, "FROG 8.4、8.7", None),
 ("将来还会继续损失收入吗？如果会，请说明依据的事实、预估金额、预估多久不能工作、怎么计算的。",
  3, "FROG 8.8", None),
 ("除以上之外还有哪些自付开销？（自费医药费、交通费、停车费、护工费、请人做家务的费用等）"
  "请写项目、日期、金额、付给谁；并说明有哪些单据可以证明。",
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
