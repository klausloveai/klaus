# -*- coding: utf-8 -*-
"""Lina Lu v. Arlene Luna — LASC 26PSCV02595 (Pomona Courthouse South, Dept. O).

Served 10/05/2026 BY MAIL out of the office of Franklin J. Love (POS signed by
Jacqueline Alvarez, 800 S Barranca Ave Ste 100, Covina) — six sets, three per
defendant, Arlene Luna and Rosalba Luna propounding separately:
  Form Interrogatories—General (DISC-001), 51 checked, IDENTICAL on both sets
  Requests for Admission (DISC-020), 7 items lettered A–G, not numbered
  Request for Production of Documents, 11 items
Checked boxes read page by page off the scan on 2026-10-14; the two defendants'
FROG selections were compared page by page and are the same.
Response deadline 11/09/2026 = 30 days + 5 calendar days for mail (CCP 1013(a)).
"""

CASE = dict(
    short="Lina Lu",
    subtitle_en="Form Interrogatories (DISC-001) + Requests for Admission, Set One",
    subtitle_zh="标准质询问卷 + 要求承认事实（第一组）· 中英对照 · 客户填写表",
    client_title_zh="Lina Lu 诉 Arlene Luna 一案 · 请您填写",
    client_due_line="请在 2026 年 10 月 24 日（周五）前填好发回我们。我们必须在 11 月 9 日前向对方提交正式答复，中间需要时间整理、翻译并交律师定稿。",
    header_rows=[
        ("Case 案件", "LINA LU v. ARLENE LUNA; ROSALBA LUNA; AMAZON LOGISTICS, INC.; RICHARD REYES and ZORAIDA TORRES, as Trustees of the TORRES REYES FAMILY TRUST; and DOES 2 through 25", None),
        ("Court 法院", "Superior Court of California, County of Los Angeles — Pomona Courthouse South — Dept. O — Hon. Christian R. Gullon", None),
        ("Case No. 案号", "26PSCV02595", None),
        ("Propounding party 提问方", "Defendants ARLENE LUNA and ROSALBA LUNA — 两人各送达一整套，内容相同", None),
        ("Responding party 答复方", "Plaintiff LINA LU（＝您）", None),
        ("Set No. 组号", "One", None),
        ("Served 送达日", "October 5, 2026 (by first-class mail, from Covina)", None),
        ("Opposing counsel 对方律师", "None of record — both defendants appear In Pro Per. The documents were prepared and served out of the office of Franklin J. Love, who confirmed in writing on October 14, 2026 that he is not attorney of record.", None),
        ("Response due 答复期限", "November 9, 2026 — 30 days + 5 calendar days for service by mail (CCP §§ 2030.260, 2031.260, 2033.250; § 1013(a))", "yellow"),
        ("Date of incident 事发日期", "July 9, 2026", None),
    ],
    client_header_rows=[
        ("案件", "Lina Lu 诉 Arlene Luna、Rosalba Luna 等", None),
        ("法院 / 案号", "加州洛杉矶县高等法院 Pomona 分院　案号 26PSCV02595", None),
        ("事发日期", "2026 年 7 月 9 日", None),
        ("请回填期限", "2026 年 10 月 24 日（周五）前发回我们", "yellow"),
    ],
    served_summary=[
        "Part 1 — Form Interrogatories — General (DISC-001)：两名被告各勾选 51 条，两套内容完全相同，因此您只需回答一遍。",
        "Part 2 — Requests for Admission（要求承认事实）：每名被告各 7 条，以字母 A–G 编号。这是本次最需要小心的一部分 —— 逾期不答，法律上视为您全部承认。",
        "对方同时送达了 Request for Production of Documents（每名被告各 11 项），需要您提供的材料列在本表最后一节。",
        "对方未勾选的部分（3.0 公司背景、13.1 监视、15.0 抗辩、16.0 被告方主张、20.0 机动车、50.0 合同）已整节删除，不必理会。",
    ],
    extra_definitions=[
        ("SUBJECT DOG", "涉案犬只 —— 2026 年 7 月 9 日在 152 East Kirkwall Road 咬伤您的那只小型白色犬。"),
        ("INCIDENT", "本案事故 —— 指 2026 年 7 月 9 日上午您在 152 East Kirkwall Road, Azusa 送货时被犬只咬伤这一事件及其前后情形。对方勾选的是 DISC-001 的标准定义，没有另行自定义。"),
    ],
)

# 对方实际勾选的 FROGs —— 2026-10-14 逐页看图核对，Arlene 与 Rosalba 两套相同
CHECKED = (["1.1"]
           + [f"2.{i}" for i in range(1, 14)]          # 2.1–2.13 全部
           + ["4.1"]                                   # 4.2 未勾
           + [f"6.{i}" for i in range(1, 8)]           # 6.1–6.7 全部
           + [f"7.{i}" for i in range(1, 4)]           # 7.1–7.3 全部
           + [f"8.{i}" for i in range(1, 9)]           # 8.1–8.8 全部
           + ["9.1", "9.2"]
           + ["10.1", "10.2", "10.3"]
           + ["11.1", "11.2"]
           + [f"12.{i}" for i in range(1, 8)]          # 12.1–12.7 全部
           + ["13.2"]                                  # 13.1 未勾 —— 13.2 因此无所指
           + ["14.1", "14.2"]
           + ["17.1"])
# 未勾：3.1–3.7、4.2、13.1、15.1、16.1–16.10、20.x、50.x

# 这两条不问客户：17.1 取决于我们对 RFA 怎么答，13.2 是我方调查/监视，属律所与律师工作范围
ATTORNEY_ONLY = {"17.1", "13.2"}

LABEL_OVERRIDES = {
    ("7.1", "(a) Describe the property"):
        "财产描述（例：送货时穿的鞋袜、衣物、手机、随身物品）",
}

WHO_NOTES = {
    "C": None,
    "CF": "本题请您填写您知道的部分，其余由律所依案卷补充。",
    "F": "本题由律所依据案卷作答，您无需填写。",
}

# ---- Part 2 = Requests for Admission，不是 Special Interrogatories ----
PART2_EN = "PART 2  —  REQUESTS FOR ADMISSION, SET ONE  (DISC-020)"
PART2_ZH = "要求承认事实（第一组）—— 每名被告各 7 条，字母编号"
PART2_PREFIX = "Request"

# RFA 原文逐字录入（Arlene 那套；Rosalba 那套只把 A、B 两条里的名字换成 Rosalba Luna）
SROGS = [
("A", "Arlene Luna does not own the dog that you allege bit you on or about July 9, 2026",
 "Arlene Luna 不是咬您那只狗的主人。（Rosalba 那套同一条问的是 Rosalba Luna）"
 "　您知道什么？您见过谁遛这只狗、谁喂它、谁把它带回屋里？", "C"),
("B", "Arlene Luna was not physically present on or about July 9, 2026 when you allege that the dog bit you at 152 East Kirkwall Road, Azusa, California 91702",
 "事发当时 Arlene Luna 人不在现场。（Rosalba 那套问的是 Rosalba Luna）"
 "　当时门廊上站着的那个人，您能否辨认是谁？是年长的还是年轻的？", "C"),
("C", "You did not seek medical treatment for the dog bite you alleged occurred on July 9, 2026 for more than one hour after the time of the incident",
 "您在被咬后一个多小时内都没有去就医。"
 "　请写清楚：被咬大约几点？到急诊室大约几点？中间做了什么（打 911、继续送货、回家、找人开车）？", "C"),
("D", "You were able to walk away from the premises immediately after the dog allegedly bit you on July 9, 2026",
 "被咬之后您能够立刻自行走开。"
 "　您当时是自己走的吗？走路是否困难、是否流血、是否需要扶？", "C"),
("E", "The dog that you allege bit you had never bitten anyone prior to July 9, 2026.",
 "这只狗在 2026 年 7 月 9 日之前从未咬过人。"
 "　您是否听说过、或从邻居 / 其他送货员 / 网上看到过这只狗以前咬人、扑人、凶人的事？", "CF"),
("F", "The person that was physically present when you made the delivery on July 9, 2026 told you that a dog was loose and to immediately leave the premises",
 "送货时在场的那个人曾告诉您有狗跑出来了、叫您立刻离开。"
 "　这件事是否发生过？对方具体说了什么？用的是中文还是英文？是在您被咬之前还是之后说的？", "C"),
("G", "Instead of leaving as the person warned you that a dog was loose, you decided to take a picture of the package you delivered on July 9, 2026",
 "在对方警告您有狗跑出来之后，您没有离开，而是决定拍摄您送达的包裹。"
 "　您是什么时候拍的照片 —— 被咬之前还是之后？拍照是 Amazon 送货流程强制要求的吗？", "C"),
]

PREAMBLE = [
    ("这是法院诉讼程序的一部分，不是可做可不做的表格。对方（被告）依法向您提出了书面问题，我们必须在法定期限内书面答复。", False),
    ("请在 2026 年 10 月 24 日（周五）前发回。我们必须在 11 月 9 日前提交正式答复，中间要整理、翻译并交律师定稿。", True),
    ("每一题都要有答案。不适用的请写「不适用」，不记得的请写「不记得」——  不要留空白。留空白在法律上等于没有回答。", True),
    ("不要猜。记不清就写「大概」「记不清确切日期，大约是某月」，不要编一个具体数字。您的答复最后要由您签字并以伪证罪责任担保其真实性。", True),
    ("旧伤、旧病、以前的索赔，请务必如实写。对方有权调取您的病历，隐瞒反而会被拿来攻击这次受伤与事故的因果关系。", True),
    ("有红色字的地方请特别留意，那是最容易出问题的几处。", False),
]

DOCS_HEADING = "十一、需要您提供的材料"
DOCS_SUBNEOTE = None
DOCS_SUBNOTE = "对方同时送达了 Request for Production of Documents（每名被告各 11 项），以下是其中需要您配合的部分。"

GROUPS = [
("一、基本信息", [
 ("您的姓名（与证件一致），以及过去用过的其他名字和使用年份。", 2, "FROG 1.1、2.1", None),
 ("出生日期、出生城市 / 省 / 国家。", 2, "FROG 2.2", None),
 ("现住址，以及过去五年住过的每一个地址和居住起止年月。", 4, "FROG 2.5", None),
 ("现在的工作：公司 / 平台名称、地址、电话、职位、工作内容、开始时间。另外请列出事发前五年至今做过的其他工作（同样信息）。", 5, "FROG 2.6、8.2", None),
 ("学历：高中起每一所学校的名称、地址、就读年月、最高学历和学位。", 4, "FROG 2.7", None),
 ("您的驾照：发照州、驾照号和类型、发照日期、有无限制（如须戴眼镜）。有其他州驾照或其他驾驶许可也请一并写。", 3, "FROG 2.3、2.4", None),
 ("您能否轻松地用英语口头交流？能否阅读和书写英文？如果不能，平时用什么语言和方言？", 2, "FROG 2.9、2.10",
  "这一题决定您的答复书最后要不要附翻译声明，请如实回答，不要为了省事写「能」。"),
 ("您是否曾被判定犯有重罪（felony）？如果有，请写明定罪的城市和州、日期、罪名、法院和案件编号。", 3, "FROG 2.8",
  "请务必如实、完整填写。隐瞒会严重损害您的案件。"),
]),
("二、事故经过", [
 ("请完整、详细地描述这次事故是怎么发生的 —— 从您接到这单、到达 152 East Kirkwall Road 开始，到狗出现、您被咬、以及事后发生了什么。写得越细越好。", 8, "FROG 2.11、12.1",
  "这是整份问卷最重要的一题，请尽量详细。"),
 ("事发当天的时间线，请尽量写准：① 您到达该址大约几点？② 被咬大约几点？③ 离开现场几点？④ 到医院几点？", 4, "RFA C",
  "对方第 C 条要您承认「被咬后一个多小时内没去就医」。时间点直接决定这一条怎么答，请尽量对照手机记录、Amazon App 记录或急诊单。"),
 ("您走到门口时的情形：① 前院的铁门是开着还是关着？② 您有没有打开它？③ 门上有没有任何警示牌（例如 Beware of Dog）？", 4, "FROG 12.1", None),
 ("您第一次看到那只狗时：① 您在哪里？② 狗在哪里、在做什么？③ 有没有拴绳？④ 看到之后您做了什么？", 5, "FROG 12.1", None),
 ("当时门廊上有没有人？是男是女、大概年纪、是否认得？那个人当时在做什么？被咬之后那个人做了什么（例如把狗带走、叫您打 911、进屋）？", 5, "RFA A、B、F",
  "对方要您承认「在场的人警告过您有狗跑出来、叫您立刻离开」。这一条是整套 RFA 里最关键的，请尽可能回忆清楚对方到底说了什么、用什么语言说的、在您被咬之前还是之后说的。"),
 ("狗咬到您身体的哪些部位？被咬时您在做什么？被咬后您是怎么离开的 —— 自己走的吗？走路有没有困难？", 4, "FROG 6.1、RFA D", None),
 ("您拍的那张包裹照片是什么时候拍的 —— 被咬之前还是之后？拍这张照片是不是 Amazon 送货流程要求的？", 4, "RFA G",
  "对方要把这张照片说成「您明知有狗还不走、留下来拍照」。如果拍照是 Amazon 强制的交付凭证，请务必写明，并把 App 里的记录保存下来。"),
 ("事发时您是在为 Amazon 送货（上班）吗？是以 Amazon Flex 独立承包司机的身份吗？", 2, "FROG 2.11", None),
 ("事发时您或在场其他人有没有任何身体、情绪或精神方面的状况可能影响了事情的发生？", 2, "FROG 2.12", None),
 ("事发前 24 小时内，您或任何涉事人员有没有服用过酒精、大麻或任何药物（含医生开的日常处方药）？如有，请写药名、用量、时间、地点、在场的人、开药医生。", 4, "FROG 2.13",
  "包括降压药、糖尿病药、过敏药、安眠药等日常处方药，请如实填写。"),
]),
("二之二、急诊当天的经过与你说过的话", [
 ("7 月 9 日被狗咬的大概时间是几点？", 2, "RFA C、FROG 12.1", None),
 ("被咬之后，到你去急诊室之前，你依先后顺序做了哪些事、去了哪些地方？", 5, "RFA C、D",
  "请按时间顺序写，包括有没有先回家、中间等了多久、等的原因。"),
 ("你大约几点到的急诊室？你是怎么去的（自己开车 / 家人送 / 叫车 / 救护车）？有没有人陪你去？", 4, "RFA C、D", None),
 ("在急诊室，最先问你情况的是护士还是医生？你记得对方的样子或名字吗？", 3, "FROG 6.4", None),
 ("你跟急诊室的人是用中文还是英文沟通的？", 2, "FROG 2.9、2.10", None),
 ("医院有没有安排翻译，或者问过你需不需要翻译？", 2, "FROG 2.9、2.10", None),
 ("当时你是怎么跟他们描述这件事的？请尽量回忆你当时说的原话，用你当时说的那种语言写。", 6, "FROG 12.1",
  "这一题请凭记忆如实写，不要事后整理成完整的说法。记不清就写「记不清」。"),
 ("你有没有告诉他们你当时正在送货、正在上班？", 3, "FROG 2.11", None),
 ("关于这只狗是谁的，你当时知道些什么？急诊室里有没有人问过你这是谁的狗？你是怎么回答的？", 5, "RFA A、E", None),
 ("你认识狗的主人吗？事发之前见过他们吗？有没有任何来往？", 3, "RFA A、B", None),
]),
("三、责任与狗主人", [
 ("据您所知，这只狗是谁养的？您凭什么这么认为（亲眼见过谁遛它 / 谁喂它 / 谁把它抱回屋 / 邻居说的）？", 4, "RFA A", None),
 ("这只狗以前有没有咬过人、扑过人或凶过人？您是怎么知道的？有没有听邻居、其他送货员说过，或在社区群、网上看到过？", 4, "RFA E",
  "对方要您承认「这只狗以前从没咬过人」。只要您有任何相反的见闻，请写下来，哪怕只是听说。"),
 ("您送货到这个地址，这是第一次吗？以前去过几次？以前有没有见过这只狗？", 3, "FROG 12.1", None),
 ("Amazon 的 App 或派单系统，有没有就这个地址给过任何提示或警告（例如有狗、谨慎投递）？", 3, "FROG 12.1",
  "请把 App 里这单的页面截图保存下来。这是我们对 Amazon 那条诉因的关键证据。"),
 ("现场有没有什么不安全的地方？（例如铁门没关 / 关不紧、围栏破损、狗没拴绳、没有警示牌）", 4, "FROG 12.1", None),
 ("有谁知道上面这些情况？请写姓名、地址、电话。", 3, "FROG 12.1", None),
]),
("四、现场证人与影像", [
 ("除了门廊上那个人以外，事发时附近还有没有其他人？（邻居、路人、其他送货员）请写您记得的一切。", 4, "FROG 12.1", None),
 ("事发后您有没有跟任何人说过这件事？（家人、朋友、Amazon 的人、邻居）是谁、什么时候、说了什么？", 4, "FROG 12.1", None),
 ("您自己拍过哪些照片或视频？（现场、铁门、狗、包裹、伤口）分别是什么时候拍的？请全部保留原始文件，不要删除、不要裁剪。", 4, "FROG 12.4",
  "请把原始照片连同拍摄时间一并发给我们，手机原图不要压缩转发。"),
 ("您知不知道那栋房子有没有门铃摄像头（Ring）或监控？邻居家有没有？", 3, "FROG 12.4", None),
 ("有没有任何人就这件事做过报告？（警方、动物管制、Amazon、保险公司）报告编号是多少？", 3, "FROG 12.6、14.2", None),
 ("有没有人来找您录过口供、做过笔录或录音？是谁、什么时候？", 3, "FROG 12.2、12.3", None),
 ("据您所知，有没有人因为这件事被开罚单、被指控违规，或被动物管制处理？", 3, "FROG 14.1、14.2", None),
 ("事发后您或任何人有没有再回去看过现场？什么时候、看到什么？", 3, "FROG 12.7", None),
]),
("五、受伤与治疗", [
 ("请列出这次事故造成的所有受伤部位和伤情。", 4, "FROG 6.1、6.2", None),
 ("到今天为止您还有哪些不适？每一项请说明：① 具体症状和部位；② 在好转 / 没变化 / 在加重；③ 多久发作一次、每次持续多久。", 5, "FROG 6.3", None),
 ("请列出因为这次事故您看过的每一家医院、急诊、诊所、专科医生、整形外科、影像中心：名称、地址、电话、看了什么、就诊起止日期。", 6, "FROG 6.4",
  "包括只去过一次的。漏掉的医疗记录以后可能拿不到，会直接影响赔偿金额。"),
 ("2026 年 7 月 28 日您是否去看过家庭医生（卡上写的是 Thomas Yu 医生）？如果去了，是为了什么、看了什么？", 3, "FROG 6.4",
  "我们的记录里有这个预约但没有就诊记录。请确认到底有没有去 —— 如果去了，我们要立刻去调病历。"),
 ("因为这次受伤您吃过哪些药？（包括自己在药房买的止痛药、药膏、贴剂）请写药名、谁开的、起止服用日期、花了多少钱。", 4, "FROG 6.5", None),
 ("有没有救护车、护理、医疗器材、交通等其他医疗相关支出？", 3, "FROG 6.6", None),
 ("整形外科 Dr. Lahijani 建议的治疗（术前类固醇、第一阶段脂肪移植、第二阶段瘢痕切除重建），您决定做吗？打算什么时候做？", 4, "FROG 6.7",
  "这个决定直接影响本案索赔金额，也影响这一题怎么答。请明确告诉我们：做 / 不做 / 还没决定。"),
 ("除此之外，还有没有其他医生告诉您以后需要继续治疗或手术？是哪位医生、针对什么症状、预计怎么治、大概多少钱？", 4, "FROG 6.7", None),
 ("这次受伤之前，您的左脚踝或左腿有没有受过伤或有过不适？什么时候、看过哪些医生？", 4, "FROG 10.1",
  "请务必如实填写。对方会去调取您的病历，隐瞒旧伤反而会被用来攻击本次受伤的因果关系。"),
 ("事故发生前，您本来就有哪些身体、精神或情绪方面的健康问题？这次事故有没有让它们加重？", 4, "FROG 10.2", None),
 ("事故之后，您有没有再受过伤（任何部位）？什么时候、怎么受的、看了哪些医生？", 3, "FROG 10.3", None),
]),
("六、保险", [
 ("您的健康保险：公司名称、保单号 / 会员号、投保人姓名。请把保险卡正反面拍照发给我们，已发过则不用重复。", 4, "FROG 4.1", None),
 ("自这次事故以来，您有没有用过 Medicare 或 Medi-Cal？有没有加入过 Medicare Part A 或 Part B？", 3, "FROG 4.1", None),
 ("除健保外，您自己有没有其他可能覆盖这次受伤的保险？（意外险、雇主提供的保险、信用卡附带保险等）", 3, "FROG 4.1", None),
]),
("七、财产损失", [
 ("这次事故损坏了哪些个人物品？（送货时穿的鞋袜、衣物、手机、随身物品）请描述物品、损坏情况、购买价和金额。", 4, "FROG 7.1",
  "如果当时穿的鞋袜或衣物还在，请原样保存好，不要清洗、不要丢弃。"),
 ("上述物品有没有做过估价或评估？有没有修过、换过或卖掉？", 3, "FROG 7.2、7.3", None),
]),
("八、误工与收入", [
 ("这次受伤之后，您有没有停止工作、减少接单，或有任何一天没能出车？", 3, "FROG 8.1、8.3、8.5、8.6",
  "我们目前的记录是「您没有停工、没有误工损失」。如果这不准确，请现在就告诉我们 —— 这一题答错，后面没法改。"),
 ("如果确实没有误工，请在这里写明「没有停工，没有误工损失」。如果有，请写：事发前最后一次出车是哪天？哪些日子没出车？什么时候恢复的？", 4, "FROG 8.1、8.6", None),
 ("事发时您的收入情况：每周出车几天、每天大约几小时、每月大约收入多少？", 4, "FROG 8.2、8.4", None),
 ("将来会不会因为这次受伤损失收入？（例如治疗期间无法出车）为什么、预计多少、多久？", 4, "FROG 8.8",
  "如果您决定做整形手术，术后恢复期会影响这一题，请一并考虑。"),
 ("除以上之外还有哪些自付开销？（自费医药费、交通费、停车费、护工费、请人代做家务的费用等）请写项目、日期、金额、付给谁。", 4, "FROG 9.1、9.2", None),
]),
("九、生活影响", [
 ("因为这次受伤，哪些日常活动、兴趣爱好、家务您做不了或做不好了？请尽量多列。", 5, "FROG 9.1",
  "这一题直接影响赔偿金额，请尽可能具体，例如「以前每天走路一小时，现在走二十分钟脚踝就疼」。"),
 ("上面每一项，受影响持续了多久？现在恢复了没有？", 4, "FROG 6.3", None),
 ("左脚踝的疤痕现在对您的生活有什么影响？（穿鞋、穿裙子、天气变化、外观带来的情绪影响）", 4, "FROG 6.1、6.3", None),
 ("谁最清楚您受伤前后的变化？请列 1–3 位：姓名、与您的关系、地址、电话。", 3, "FROG 12.1", None),
]),
("十、既往索赔", [
 ("除本案外，过去十年您有没有提出过其他人身伤害的索赔或诉讼？请写时间、地点、对方是谁、法院和案号、当时的律师、结果、伤情。", 5, "FROG 11.1", None),
 ("过去十年您有没有申请过工伤赔偿（workers' compensation）？请写时间、雇主、保险公司和理赔号、领取期间、伤情、治疗机构、WCAB 案号。", 5, "FROG 11.2",
  "本案中 Amazon 那边的 Homeland / Intact 理赔（claim 0AB504616）是「职业意外险」(occupational accident)，并不是 workers' compensation。请不要把它写成工伤赔偿；如果您此前确实另有真正的工伤申请，才写在这里。这一条由我们和律师一起定稿。"),
]),
]

RFP_DOCS = [
 "原始照片与视频 —— 现场、铁门、狗、包裹、伤口（请保留手机原图，不要删除、不要裁剪、不要压缩转发）",
 "Amazon Flex App 里 2026 年 7 月 9 日这一单的截图：派单信息、投递确认、包裹照片、时间戳",
 "Amazon Flex 的承包 / 服务协议（您注册时签的那份）",
 "2026 年 7 月 9 日前后的 Amazon 收入结算记录（我们只在确有必要时才提供，但请先找出来）",
 "健康保险卡正反面",
 "所有医疗收据、账单、自付凭证（含药房小票）",
 "整形外科 Dr. Lahijani 的报价单和治疗计划（如您手上另有副本）",
 "自付的交通费、停车费收据",
 "与 Amazon、被告或任何人就这件事往来的短信、微信、邮件截图",
 "送货时穿的鞋袜和衣物，如仍在请原样保存",
]
