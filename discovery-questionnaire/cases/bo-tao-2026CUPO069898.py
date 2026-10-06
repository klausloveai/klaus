# -*- coding: utf-8 -*-
"""Bo Tao v. Beas — Ventura 2026CUPO069898. Worked example of the case-module contract.
Served 9/25/2026 by OPC (Christine Hanna, Law Offices of Scott C. Stratman):
Answer, Demand for Jury + Notice of Posting Jury Fees, Demand for Production (19),
Special Interrogatories Set One (52 + CCP 2030.050 declaration), FROGs (54 checked),
Notice of Deposition (1/26/2027). Checked boxes read page-by-page off the scanned PDF."""

CASE = dict(
    short="Bo Tao",
    subtitle_en="Form Interrogatories (DISC-001) + Special Interrogatories, Set One",
    subtitle_zh="标准质询问卷 + 特别质询问卷（第一组）· 中英对照 · 客户填写表",
    client_title_zh="Bo Tao 诉 Beas 一案 · 请您填写",
    client_due_line="请在 2026 年 10 月 20 日前填好发回我们，我们需要时间整理、翻译并在期限内向对方提交正式答复。",
    header_rows=[
        ("Case 案件", "BO TAO v. EUTIMEO BEAS; RACHEL R. BEAS; BECKY BEAS; and DOES 1 through 20", None),
        ("Court 法院", "Superior Court of California, County of Ventura — Dept. 43 — Hon. Ben Coats", None),
        ("Case No. 案号", "2026CUPO069898", None),
        ("Propounding party 提问方", "Defendant RACHEL R. BEAS", None),
        ("Responding party 答复方", "Plaintiff BO TAO（＝您）", None),
        ("Set No. 组号", "One", None),
        ("Served 送达日", "September 25, 2026 (by electronic service)", None),
        ("Opposing counsel 对方律师", "Christine Hanna, Esq. — Law Offices of Scott C. Stratman", None),
        ("Response due 答复期限", "October 27, 2026", "yellow"),
        ("Date of incident 事发日期", "June 27, 2026", None),
    ],
    client_header_rows=[
        ("案件", "Bo Tao 诉 Eutimeo Beas、Rachel R. Beas、Becky Beas", None),
        ("法院 / 案号", "加州 Ventura 县高等法院　案号 2026CUPO069898", None),
        ("事发日期", "2026 年 6 月 27 日", None),
        ("请回填期限", "2026 年 10 月 20 日（周二）前发回我们", "yellow"),
    ],
    served_summary=[
        "Part 1 — Form Interrogatories — General (DISC-001)：对方共勾选 54 条，其中 52 条需要您回答（另 2 条由律所作答）。",
        "Part 2 — Special Interrogatories, Set One：共 52 条，其中 37 条需要您回答，10 条由律所依案卷作答，5 条由您和律所各填一部分。",
        "对方未勾选的部分（3.0 公司背景、16.0 被告方主张的大部分、17.0、20.0 机动车、50.0 合同）已经整节删除，不必理会。",
    ],
    extra_definitions=[("SUBJECT DOG", "涉案犬只 —— 本案中咬伤 / 弄伤您的那只狗。")],
)

# 对方实际勾选的 FROGs（逐页看图核对 2026-10-04）
CHECKED = (["1.1"] + [f"2.{i}" for i in range(1, 14)] + ["4.1", "4.2"]
           + [f"6.{i}" for i in range(1, 8)] + [f"7.{i}" for i in range(1, 4)]
           + [f"8.{i}" for i in range(1, 9)] + ["9.1", "9.2"]
           + ["10.1", "10.2", "10.3"] + ["11.1", "11.2"]
           + [f"12.{i}" for i in range(1, 8)] + ["13.1", "13.2"] + ["14.1", "14.2"]
           + ["15.1", "16.2"])
# 未勾：3.1-3.7、16.1、16.3-16.10、17.1、20.x、50.x
ATTORNEY_ONLY = {"15.1", "16.2"}   # 原告无抗辩可言 / 问原告"你是否主张原告没受伤"属对方套模板

LABEL_OVERRIDES = {("7.1", "(a) Describe the property"):
                   "财产描述（例：衣物、鞋、眼镜、手机、随身物品）"}

WHO_NOTES = {"C": None,
             "CF": "本题请您填写您知道的部分，其余由律所依案卷补充。",
             "F": "本题由律所依据案卷和账单记录作答，您无需填写。"}
PRIVACY = {50, 52}
PRIVACY_NOTE = "本题涉及个人敏感号码，律所将另行处理并评估异议，请勿填写在本表上。"

SROGS = [
(1,"Please describe in complete detail how the subject incident happened, for which you have sued in this lawsuit.",
 "请完整、详细地描述本案所诉事故是如何发生的。","C"),
(2,"Please state all the facts on which you base your contentions of fault or responsibility on the part of each defendant you have sued in this subject lawsuit.",
 "请说明您主张每一位被告有过错或应负责任所依据的全部事实。","CF"),
(3,"Please state the name, address and telephone number of any witness to each fact on which you base your contentions of fault or responsibility on the part of each defendant you have sued in this subject lawsuit.",
 "请说明可以证明上述每一项事实的证人的姓名、地址和电话。","C"),
(4,"Please identify with particularity any document which supports each fact on which you base your contentions of fault or responsibility on the part of each defendant you have sued in this subject lawsuit.",
 "请具体指明可以支持上述每一项事实的文件。","CF"),
(5,"Please state whether you or any person representing you has had any conversations with any defendant or defendant's employees or agents.",
 "您或任何代表您的人，是否曾与任何被告、或被告的雇员或代理人有过交谈？","C"),
(6,"If you or any person representing you has had any conversations with defendants, please fully identify the parties involved and dates of said conversations.",
 "如果有过交谈，请完整说明参与交谈的人员以及交谈的日期。","C"),
(7,"If you or any person representing you has had any conversations with any defendant or defendant's employees or agents, please state the exact statements made if known, or if not, the general substance of the statements made.",
 "如果有过交谈，请说明当时所说的确切内容；如记不清确切用词，请说明大致内容。","C"),
(8,"If you contend any unsafe condition caused your injury please identify each such condition?",
 "如果您主张是某种不安全的状况导致了您受伤，请逐一指明每一项该状况。","C"),
(9,"For each condition you contend constituted an unsafe condition, state whether you contend that any defendant had knowledge of the defect prior to your injury?",
 "就您主张的每一项不安全状况，请说明您是否主张任何被告在您受伤之前就已知悉该缺陷。","C"),
(10,"For each condition you contend constituted an unsafe condition, identify all facts that relate to your contentions that defendant had knowledge of the condition.",
 "就每一项不安全状况，请说明与「被告知悉该状况」这一主张相关的全部事实。","C"),
(11,"For each condition you contend constituted an unsafe condition, identify any persons who have any knowledge of any facts that relate to your contention that a defendant had knowledge of those facts.",
 "就每一项不安全状况，请指明知悉上述事实的人。","C"),
(12,"For each condition you contend constituted an unsafe condition, identify any documents that relate to your contention that a defendant had knowledge of the condition.",
 "就每一项不安全状况，请指明与该主张相关的文件。","CF"),
(13,"If you contend that the propounding party had knowledge of any previous violent propensities of the SUBJECT DOG, state each and every fact in support of such contentions.",
 "如果您主张提问方（RACHEL R. BEAS）事先知悉涉案犬只过往的暴力倾向，请说明支持该主张的每一项事实。","C"),
(14,"Describe in complete detail the activities you were engaged in when you were injured by the SUBJECT DOG.",
 "请完整、详细地描述您被涉案犬只咬伤 / 弄伤时正在做什么。","C"),
(15,"If you contend that there was any defect of the premises owned by this propounding party that contributed to the incident alleged, state each and every fact in support of such contention.",
 "如果您主张提问方所有的房产存在缺陷并促成了本次事故，请说明支持该主张的每一项事实。","C"),
(16,"If you contend that this propounding party has actual or constructive knowledge of any defect of the premises that you contend contributed to the incident, state each and every fact in support of such contention.",
 "如果您主张提问方对该房产缺陷有实际知悉或推定知悉，请说明支持该主张的每一项事实。","C"),
(17,"If you contend that the propounding party had any prior knowledge of any dangerous propensities of the SUBJECT DOG, state each and every fact in support of your contention.",
 "如果您主张提问方事先知悉涉案犬只的危险倾向，请说明支持该主张的每一项事实。","C"),
(18,"State each place where the SUBJECT DOG bit you.",
 "请说明涉案犬只咬到您身体的每一个部位。","C"),
(19,"If the SUBJECT DOG did not bite you, describe how you were injured, due to the SUBJECT DOG.",
 "如果涉案犬只并未咬到您，请描述您是如何因该犬只而受伤的。","C"),
(20,"When you first saw the SUBJECT DOG, where were you?",
 "您第一次看到涉案犬只时，您在什么位置？","C"),
(21,"When you first saw the SUBJECT DOG, what was it doing?",
 "您第一次看到涉案犬只时，它在做什么？","C"),
(22,"After you first saw the SUBJECT DOG, what, if anything, did you do to move away from the dog?",
 "看到该犬只之后，您做了什么来躲避它（如果有的话）？","C"),
(23,"State where you were when the incident occurred.",
 "事故发生时，您具体在什么位置？","C"),
(24,"State each and every fact in support of your contention that the propounding party was the owner of the SUBJECT DOG.",
 "请说明支持「提问方是涉案犬只主人」这一主张的每一项事实。","C"),
(25,"Please identify fully (i.e. by name, address and telephone number) each person with any knowledge regarding any harm you claim in this subject lawsuit, including, but not limited to, each person who witnessed you in an injured condition at any time since the accident which is the subject of this lawsuit.",
 "请完整列出（姓名、地址、电话）所有了解您在本案中所主张伤害情况的人，包括事故后任何时间见过您受伤状态的每一个人。","C"),
(26,"If you claim that any physical, emotional or mental condition or disability was aggravated due to the claimed fault of any defendant in this subject lawsuit, please state all facts to describe the aggravation (i.e. stating what the condition or disability was and how it was aggravated).",
 "如果您主张本次事故加重了您既有的身体、情绪或精神方面的病症或残疾，请说明该病症原本是什么、以及是如何被加重的。","C"),
(27,"For each HEALTH CARE PROVIDER that you went to due to the incident that is the subject of this lawsuit, please state the amount of the billing from each such provider for the health care treatment provided to you due to the subject incident.",
 "就您因本次事故看过的每一家医疗机构，请说明其就本次事故治疗所开出的账单金额。","F"),
(28,"For each HEALTH CARE PROVIDER that you went to due to the incident that is the subject of this lawsuit, please state each amount the HEALTH CARE PROVIDER accepted as payment from anyone for the health care treatment provided to you due to the subject incident.",
 "就每一家医疗机构，请说明其实际从任何人处接受的付款金额。","F"),
(29,"For each health care service that you received due to the incident that is the subject of this lawsuit, please state the amount paid by anyone (e.g. your health care insurance carriers, government plans, private vendors purchasing a lien) at any time as a result of your medical care.",
 "就您接受的每一项医疗服务，请说明由任何一方（健保公司、政府计划、购买留置权的第三方等）支付的金额。","F"),
(30,"For each health care service that you received due to the incident that is the subject of this lawsuit, please state the amounts of any adjustments or reductions to the billed amounts that were made by anyone.",
 "就每一项医疗服务，请说明任何一方对账单金额所作的调整或减免金额。","F"),
(31,"For each HEALTH CARE PROVIDER that you went to due to the incident that is the subject of this lawsuit, please state the name of each HEALTH CARE PROVIDER followed by the amount that you paid to the provider for services rendered due to the incident that is the subject of this lawsuit.",
 "请列出每一家医疗机构的名称，以及【您自己】就本次事故实际付给该机构的金额。","CF"),
(32,"Please identify any money you owe currently for any and all health care treatment you received due to the incident that is the subject of this lawsuit, including the amount you owe currently and to whom you owe any sum currently.",
 "请说明目前仍欠付的医疗费用：欠多少、欠给谁。","F"),
(33,"For each HEALTH CARE PROVIDER that you went to due to the incident, if you contend that any of the HEALTH CARE PROVIDERs gratuitously wrote off any amounts owed to such providers, please state all facts in support of such contention.",
 "如果您主张任何医疗机构无偿免除了应付款项，请说明支持该主张的全部事实。","F"),
(34,"For each HEALTH CARE PROVIDER that you went to due to the incident, if you contend that any of the HEALTH CARE PROVIDERs gratuitously wrote off any amounts owed to such providers, please identify by name and address each such HEALTH CARE PROVIDER and the specific amounts you claim were gratuitously written off.",
 "如主张有无偿免除，请列明该医疗机构的名称、地址，以及被免除的具体金额。","F"),
(35,"For each HEALTH CARE PROVIDER that you went to due to the incident that is the subject of this lawsuit, identify which ones were referred to you by your attorney (Qaadir v. Figueroa, 67 Cal.App.5th 790 (2021)).",
 "请指明其中哪些医疗机构是由您的律师转介的。","F"),
(36,"Have you been a beneficiary of Medicare or Medi-Cal at any time since the incident on which this lawsuit is based?",
 "自本次事故以来，您是否在任何时间曾是 Medicare 或 Medi-Cal 的受益人？","C"),
(37,"Please describe with particularity any and all Medicare or Medi-Cal benefits you have received in connection with any injuries arising out of the incident on which this lawsuit is based.",
 "请具体说明您就本次事故的伤害所领取过的所有 Medicare 或 Medi-Cal 福利。","C"),
(38,"State the name and address of your medical insurance carrier, or carriers that provided medical and/or health care coverage to you since the incident on which this lawsuit is based.",
 "请说明自本次事故以来为您提供医疗 / 健康保险的保险公司的名称和地址。","C"),
(39,"For each insurer, HMO, governmental entity and/or employer that provided medical and/or health care coverage to you since the incident on which this lawsuit is based, please state your membership and/or provider identification number.",
 "就上述每一家保险公司 / HMO / 政府机构 / 雇主，请说明您的会员号或被保险人识别号。","C"),
(40,"Please state all facts to describe how you mitigated any harm that you are claiming in this subject lawsuit.",
 "请说明您为减轻本案所主张的损害做过哪些事（例如按时就诊、遵医嘱、尽快复工等）。","C"),
(41,"Please state the name, address and telephone number of your primary care physician or regular HEALTH CARE PROVIDER at any time during the past ten years.",
 "请说明您过去十年内的家庭医生 / 常去医疗机构的名称、地址和电话。","C"),
(42,"Please state the name, address and telephone number of each and every HEALTH CARE PROVIDER who has provided—at any time during the 10 year period before the incident which is subject matter of this lawsuit—any health care treatment of any kind for any pain or other complaint to the same part(s) of your body that you claim was injured in the subject incident.",
 "本次事故发生前十年内，凡就您本案所主张受伤的【同一身体部位】提供过任何治疗的医疗机构，请逐一列出名称、地址和电话。","C"),
(43,"Please list each and every economic damage you are claiming in this subject lawsuit.",
 "请逐项列出您在本案中主张的每一项经济损失。","CF"),
(44,"Identify any Health App you've used on any electronic device in the past 5 years to track your physical activity.",
 "请列出您过去五年内在任何电子设备上用来记录运动 / 身体活动的健康类 App。","C"),
(45,"Identify any wearable technology or device that you have used in the past 5 years to track your physical activity.",
 "请列出您过去五年内使用过的、用来记录运动 / 身体活动的可穿戴设备（例如 Apple Watch、Fitbit）。","C"),
(46,"Identify by name and address any physical fitness facility where you've been a member in the past 5 years.",
 "请列出您过去五年内办过会员的健身房 / 运动场所的名称和地址。","C"),
(47,"Identify all persons you believe can provide testimony about the impact of your injuries you allege were caused by this accident on your activities.",
 "请列出您认为能够就「本次受伤对您日常活动的影响」作证的所有人。","C"),
(48,"Describe what activities of daily living, hobbies, and chores, if any, were affected by your injuries resulting from the subject incident.",
 "请描述因本次受伤而受到影响的日常生活活动、兴趣爱好和家务。","C"),
(49,"For all activities, hobbies, and chores you claim were affected by the subject incident, identify the length of time said activities of daily living, hobbies, and chores were affected by your injuries resulting from the subject accident.",
 "就上述每一项受影响的活动、爱好和家务，请说明受影响持续了多长时间。","C"),
(50,"Please state your social security number.",
 "请提供您的社会安全号（SSN）。","F"),
(51,"Have you ever been enrolled in Medicare Part A and/or Medicare Part B?",
 "您是否曾加入过 Medicare Part A 和 / 或 Part B？","C"),
(52,"If your answer to the preceding interrogatory is in the affirmative, please state your Medicare Claim Number and/or Medicare HICN number.",
 "如上题回答为「是」，请提供您的 Medicare Claim Number 或 HICN 号码。","F"),
]

PREAMBLE = [
    ("对方律师（被告方）已经正式送来了三套问题，法律上我们必须在期限内逐条书面回答，"
     "并且由您本人宣誓签字。这份中文问卷是我们把那些问题整理、翻译、合并之后的版本 —— "
     "您只要照着填，剩下的格式和法律措辞由我们来处理。", False),
    ("请在每个问题下面的空白格里直接打字或手写。格子会自动变大，写多少都可以。", False),
    ("与您情况无关的题，请写「不适用」，不要留空。留空在法律上会被当成拒绝回答，可能被法院处罚。", True),
    ("记不清的，就写「记不清」，再尽量给个大概时间或范围。千万不要猜、不要编 —— "
     "这份回答是您宣誓作出的，对方会拿去和病历、保险记录逐条核对。", True),
    ("这份问卷里问到的旧伤、既往索赔、重罪记录等，看起来像是在为难您，但这些对方都查得到。"
     "如实写出来我们可以提前准备；被对方先查出来，才是真正伤害案件的。", True),
    ("有红色字的地方请特别留意，那是最容易出问题的几处。", False),
]

DOCS_HEADING = "十一、需要您提供的材料"
DOCS_SUBNOTE = "对方同时送达了 Demand for Production（共 19 项要求），以下是其中需要您配合的部分。"
DEPO_NOTE = ("另外请注意：对方已经通知，将于 2027 年 1 月 26 日上午 9:00 以远程视频方式对您进行"
             "庭外取证（deposition）。时间还早，届时我们会提前帮您充分准备，现在不用担心。")
GROUPS = [
("一、基本信息", [
 ("您的姓名（与证件一致）、以及过去用过的其他名字和使用年份。",2,"FROG 1.1、2.1",None),
 ("出生日期、出生城市 / 省州 / 国家。",2,"FROG 2.2",None),
 ("现住址，以及过去五年住过的每一个地址和居住起止年月。",4,"FROG 2.5",None),
 ("现在的工作：公司名称、地址、电话、职位、工作内容、入职时间。另外请列出事发前五年至今做过的其他工作（同样信息）。",5,"FROG 2.6、8.2",None),
 ("学历：高中起每一所学校的名称、地址、就读年月、最高学历和学位。",4,"FROG 2.7",None),
 ("您的驾照：发照州、驾照号和类型、发照日期、有无限制（如须戴眼镜）。有其他州驾照或许可证也请一并写。",3,"FROG 2.3、2.4",None),
 ("您能否轻松地用英语口头交流？能否阅读和书写英文？如果不能，平时用什么语言和方言？",2,"FROG 2.9、2.10",None),
 ("您是否曾被判定犯有重罪（felony）？如果有，请写明定罪的城市和州、日期、罪名、法院和案件编号。",3,"FROG 2.8",
  "请务必如实、完整填写。隐瞒会严重损害您的案件。"),
]),
("二、事故经过", [
 ("请完整、详细地描述这次事故是怎么发生的 —— 从您到那个地方开始，到狗出现、您受伤、以及事后发生了什么。写得越细越好。",8,"SROG 1、14",
  "这是整份问卷最重要的一题，请尽量详细。"),
 ("事发时您具体在什么位置？（街道地址、门口 / 人行道 / 院子里等）当时您正在做什么？",3,"SROG 14、23",None),
 ("您第一次看到那只狗时：① 您在哪里？② 狗在做什么？③ 看到之后您做了什么躲避？",4,"SROG 20、21、22",None),
 ("狗咬到您身体的哪些部位？如果不是咬伤，请说明您是怎么因为这只狗受伤的（例如被扑倒、躲闪时摔倒）。",3,"SROG 18、19",None),
 ("事发时您是否正在上班或替别人办事？",2,"FROG 2.11",None),
 ("事发时您或其他涉事人员身上有没有任何身体、情绪或精神方面的状况可能影响了事情的发生？",2,"FROG 2.12",None),
 ("事发前 24 小时内，您或任何涉事人员有没有服用过酒精、大麻或任何药物（含医生开的日常处方药）？如有，请写药名、用量、时间、地点、在场的人、开药医生。",4,"FROG 2.13",
  "包括降压药、糖尿病药、过敏药、安眠药等日常处方药，请如实填写。"),
]),
("三、责任与狗主人", [
 ("您为什么认为被告（Eutimeo Beas / Rachel R. Beas / Becky Beas）要负责？请说出您知道的全部事实。",5,"SROG 2",None),
 ("您凭什么认为他们是这只狗的主人？（例如亲眼见过他们遛狗、邻居说的、动物管制报告）",4,"SROG 24",None),
 ("这只狗以前有没有咬过人、扑过人或凶过人？您是怎么知道的？",4,"SROG 13、17",None),
 ("狗主人事先知不知道这只狗有危险性？您凭什么这么认为？",4,"SROG 9、10、16",None),
 ("现场有没有什么不安全的地方？（例如门没关、围栏破损、狗没拴绳、没有警示牌）",4,"SROG 8、15",None),
 ("有谁知道上面这些情况？请写姓名、地址、电话。",3,"SROG 11、25、FROG 12.1",None),
 ("有没有任何文件能证明以上事实？（动物管制记录、邻居短信、监控、社区投诉记录等）",3,"SROG 4、12",None),
]),
("四、现场证人与影像", [
 ("有谁目击了事故本身，或事故前后紧接着的情形？请写姓名、地址、电话。",4,"FROG 12.1",None),
 ("有没有照片、录像、监控、行车记录仪拍到现场、狗、或您的伤？是谁拍的、什么时候拍的、现在在谁手里？",4,"FROG 12.4",
  "请把您手上所有照片和视频发给我们，包括伤口照、现场照、狗的照片。已发过的不用重复。"),
 ("事故之后您有没有再回过现场？什么时候去的？有没有拍照？",2,"FROG 12.7",None),
 ("有没有任何人就这件事做过报告？（警方、动物管制、物业、保险公司）报告编号是多少？",3,"FROG 12.6、14.2",None),
 ("有没有人来找您录过口供、做过笔录或录音？是谁、什么时候？",3,"FROG 12.2、12.3",None),
 ("据您所知，有没有人因为这件事被开罚单或被指控违规？",2,"FROG 14.1、14.2",None),
]),
("五、与对方的接触", [
 ("事故之后，您或您的家人有没有和被告本人、他们的家人、雇员或代理人说过话？什么时候、在哪里、和谁？",3,"SROG 5、6",None),
 ("当时双方都说了什么？记得原话就写原话，记不清就写大意。",4,"SROG 7",None),
]),
("六、受伤与治疗", [
 ("请列出这次事故造成的所有受伤部位和伤情。",4,"FROG 6.1、6.2",None),
 ("到今天为止您还有哪些不适？每一项请说明：① 具体症状和部位；② 在好转 / 没变化 / 在加重；③ 多久发作一次、每次持续多久。",5,"FROG 6.3",None),
 ("请列出因为这次事故您看过的每一家医院、急诊、诊所、推拿 / 针灸、理疗、影像中心（MRI / X-ray）和专科医生：名称、地址、电话、看了什么、就诊起止日期。",6,"FROG 6.4、SROG 31",
  "包括只去过一次的。漏掉的医疗记录以后可能拿不到，会直接影响赔偿金额。"),
 ("因为这次受伤您吃过哪些药？（包括自己在药房买的止痛药、药膏、贴剂）请写药名、谁开的、起止服用日期、花了多少钱。",4,"FROG 6.5",None),
 ("有没有救护车、护理、医疗器材等其他医疗相关支出？",3,"FROG 6.6",None),
 ("有没有医生告诉您以后还需要继续治疗或手术？是哪位医生、针对什么症状、预计怎么治、大概多少钱？",4,"FROG 6.7",None),
 ("这次受伤之前，您在同一个身体部位有没有受过伤或有过不适？什么时候、看过哪些医生？",4,"FROG 10.1、SROG 42",
  "请务必如实填写。对方会去调取您的病历，隐瞒旧伤反而会被用来攻击本次受伤的因果关系。"),
 ("事故发生前，您本来就有哪些身体、精神或情绪方面的健康问题？这次事故有没有让它们加重？",4,"FROG 10.2、SROG 26",None),
 ("事故之后，您有没有再受过类似的伤？什么时候、怎么受的、看了哪些医生？",3,"FROG 10.3",None),
 ("请提供您过去十年的家庭医生 / 常去诊所的名称、地址、电话。",3,"SROG 41",None),
]),
("七、保险", [
 ("您的健康保险公司名称、地址、保单号、会员号。所有被保人的姓名、地址、电话。",4,"FROG 4.1、SROG 38、39",
  "请把保险卡正反面拍照发给我们，已发过则不用重复。"),
 ("自这次事故以来，您有没有用过 Medicare 或 Medi-Cal？有没有加入过 Medicare Part A 或 Part B？领过哪些福利？",3,"SROG 36、37、51",None),
]),
("八、财产损失与误工", [
 ("这次事故损坏了哪些个人物品？（衣服、鞋、眼镜、手机、随身物品）请描述物品、损坏情况、金额；修过或卖过也请说明。",4,"FROG 7.1、7.2、7.3",
  "对方点名要您事发时穿的那双鞋。请立刻把鞋子和当时穿的衣物原样保存好，不要清洗、不要丢弃。"),
 ("您有没有因为这次事故损失工资？如果有：事发前最后一次上班是哪天？哪些日子没能上班？什么时候复工的？",4,"FROG 8.1、8.3、8.5、8.6",
  "如有误工，请提供事发前三个月和事发后三个月的工资单或收入证明。"),
 ("您事发时的收入：时薪或月薪、每周上几天、每天几小时、月收入大约多少？至今一共损失了多少工资？",4,"FROG 8.4、8.7",None),
 ("将来还会继续损失收入吗？为什么？预计多少、多久？",3,"FROG 8.8",None),
 ("除以上之外还有哪些自付开销？（自费医药费、交通费、停车费、护工费、请人做家务的费用等）请写项目、日期、金额、付给谁。",4,"FROG 9.1、9.2、SROG 43",None),
 ("您为了减轻损失做过什么？（例如按时就诊、遵医嘱、尽快复工）",3,"SROG 40",None),
]),
("九、生活影响", [
 ("因为这次受伤，哪些日常活动、兴趣爱好、家务您做不了或做不好了？请尽量多列。",5,"SROG 48、FROG 9.1",
  "这一题直接影响赔偿金额，请尽可能具体，例如「以前每周打两次羽毛球，现在完全不能打」。"),
 ("上面每一项，受影响持续了多久？现在恢复了没有？",4,"SROG 49",None),
 ("谁最清楚您受伤前后的变化？请列 1–3 位：姓名、与您的关系、地址、电话。",3,"SROG 25、47",None),
 ("您过去五年有没有用过记录运动的手机 App 或可穿戴设备（Apple Watch、Fitbit 等）？办过哪些健身房会员？",3,"SROG 44、45、46",None),
]),
("十、既往索赔", [
 ("除本案外，过去十年您有没有提出过其他人身伤害的索赔或诉讼？请写时间、地点、对方是谁、法院和案号、当时的律师、结果、伤情。",5,"FROG 11.1",None),
 ("过去十年您有没有申请过工伤赔偿（workers' compensation）？请写时间、雇主、保险公司和理赔号、领取期间、伤情、治疗机构、WCAB 案号。",5,"FROG 11.2",None),
]),
]

RFP_DOCS = [
 "事发时穿的那双鞋，以及当时穿的衣物（请原样保存，不要清洗、不要丢弃）",
 "所有现场照片、伤口照片、视频、监控或行车记录仪影像",
 "健康保险卡正反面、保单声明页",
 "所有医疗收据、账单、自付凭证",
 "事发前三个月和事发后三个月的工资单 / 收入证明 / 请假记录",
 "自付的交通费、停车费、药房收据",
 "与被告或其家人往来的短信、微信、邮件截图",
 "警方报告、动物管制报告（如您手上有）",
 "Medicare / Medi-Cal 相关的通知或账单（如有）",
]
