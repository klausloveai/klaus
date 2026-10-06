# -*- coding: utf-8 -*-
"""DISC-001 Form Interrogatories-General (Rev. Jan 1 2024).
All 88 numbered interrogatories: English verbatim from the Judicial Council form,
Chinese translation + client-friendly sub-item labels. Source: courts.ca.gov disc001.pdf."""

# Each question: dict(n, en, cn, yn=False, note=None, groups=[(title, [ (en_label, cn_label), ... ], repeat)], lines=0)
# groups title None -> no sub-header line

S1 = dict(hdr="1.0  IDENTITY OF PERSONS ANSWERING THESE INTERROGATORIES  回答本问卷的人员", note=None, qs=[
 dict(n="1.1",
  en="State the name, ADDRESS, telephone number, and relationship to you of each PERSON who prepared or assisted in the preparation of the responses to these interrogatories. (Do not identify anyone who simply typed or reproduced the responses.)",
  cn="请列出协助准备本问卷答复的每一位人士的姓名、地址、电话，以及与您的关系。（仅负责打字或复印的人无需列出。）",
  groups=[(None, [("Name","姓名"),("ADDRESS","地址"),("Telephone","电话"),("Relationship to you","与您的关系")], 2)]),
])

S2 = dict(hdr="2.0  GENERAL BACKGROUND INFORMATION — INDIVIDUAL  个人背景资料", note=None, qs=[
 dict(n="2.1", en="State: (a) your name; (b) every name you have used in the past; and (c) the dates you used each name.",
  cn="请填写：(a) 您的姓名；(b) 您过去使用过的所有姓名；(c) 使用每个姓名的起止时间。",
  groups=[(None, [("(a) Your name","您现在的姓名（请与证件一致）")], 1),
          ("(b)(c) Former names 曾用名（如有）", [("Name","曾用名"),("Dates used","使用起止年月（例：2015年3月–2019年8月）")], 3)]),
 dict(n="2.2", en="State the date and place of your birth.", cn="请填写您的出生日期和出生地。",
  groups=[(None, [("Date of birth","出生日期"),("City","出生城市"),("State or province","省 / 州"),("Country","国家")], 1)]),
 dict(n="2.3", en="At the time of the INCIDENT, did you have a driver's license? If so, state: (a) the state or other issuing entity; (b) the license number and type; (c) the date of issuance; and (d) all restrictions.",
  cn="本次事故发生时，您是否持有驾驶执照？如果有，请填写：(a) 发照的州或机构；(b) 驾照号码及类型；(c) 发照日期；(d) 驾照上的所有限制。", yn=True,
  note="如持有，请将驾照正反面拍照发给我们。",
  groups=[(None, [("(a) State or other issuing entity","发照的州或机构（例：California）"),("(b) License number and type","驾照号码及类型（例：D1234567，C 类）"),("(c) Date of issuance","发照日期"),("(d) All restrictions","驾照上注明的限制（例：须配戴眼镜）")], 1)]),
 dict(n="2.4", en="At the time of the INCIDENT, did you have any other permit or license for the operation of a motor vehicle? If so, state: (a) the state or other issuing entity; (b) the license number and type; (c) the date of issuance; and (d) all restrictions.",
  cn="本次事故发生时，您是否持有其他可驾驶机动车的许可证或执照（例如外州驾照、学习驾照、商用驾照）？如果有，请填写：", yn=True,
  groups=[(None, [("(a) State or other issuing entity","发照的州或机构"),("(b) License number and type","号码及类型"),("(c) Date of issuance","发照日期"),("(d) All restrictions","所注明的限制")], 1)]),
 dict(n="2.5", en="State: (a) your present residence ADDRESS; (b) your residence ADDRESSES for the past five years; and (c) the dates you lived at each ADDRESS.",
  cn="请填写：(a) 您现在的居住地址；(b) 过去五年您居住过的所有地址；(c) 在每个地址居住的起止时间。",
  groups=[("(a) Present residence 现居住地址", [("ADDRESS","现住址（街道、城市、州、邮编）"),("Dates","居住起止年月（例：2022年6月–至今）")], 1),
          ("(b)(c) Residences for the past five years 过去五年曾居住的地址", [("ADDRESS","地址"),("Dates","居住起止年月")], 3)]),
 dict(n="2.6", en="State: (a) the name, ADDRESS, and telephone number of your present employer or place of self-employment; and (b) the name, ADDRESS, dates of employment, job title, and nature of work for each employer or self-employment you have had from five years before the INCIDENT until today.",
  cn="请填写：(a) 您现任雇主（或自雇经营场所）的名称、地址、电话；(b) 从事故发生前五年起至今，您所有雇主或自雇经历的名称、地址、受雇起止时间、职位和工作内容。",
  groups=[("(a) Present employer / self-employment 现任工作", [("Name","公司 / 单位名称"),("ADDRESS","地址"),("Telephone","电话"),("Dates of employment","受雇起止年月（例：2023年2月–至今）"),("Job title","职位名称"),("Nature of work","工作内容 / 性质")], 1),
          ("(b) Employment from five years before the INCIDENT until today 事故发生前五年至今的其他工作", [("Name","公司 / 单位名称"),("ADDRESS","地址"),("Dates of employment","受雇起止年月"),("Job title","职位名称"),("Nature of work","工作内容 / 性质")], 3)]),
 dict(n="2.7", en="State: (a) the name and ADDRESS of each school or other academic or vocational institution you have attended, beginning with high school; (b) the dates you attended; (c) the highest grade level you have completed; and (d) the degrees received.",
  cn="请填写：(a) 您从高中开始就读过的每一所学校或学术 / 职业培训机构的名称和地址；(b) 就读起止时间；(c) 您已完成的最高学历；(d) 所获学位。",
  groups=[("High school 高中", [("Name and ADDRESS","学校名称及地址"),("Dates of attendance","就读起止年月")], 1),
          ("College / university 大学或大专", [("Name and ADDRESS","学校名称及地址"),("Dates of attendance","就读起止年月")], 2),
          ("Other academic or vocational institution 其他学术或职业培训机构（例：美容学校、技工培训）", [("Name and ADDRESS","名称及地址"),("Dates of attendance","就读起止年月")], 1),
          (None, [("(c) Highest grade level completed","已完成的最高学历"),("(d) Degrees received","所获学位（例：学士、硕士）")], 1)]),
 dict(n="2.8", en="Have you ever been convicted of a felony? If so, for each conviction state: (a) the city and state where you were convicted; (b) the date of conviction; (c) the offense; and (d) the court and case number.",
  cn="您是否曾被判定犯有重罪（felony）？如果有，请就每一次定罪填写：(a) 定罪的城市和州；(b) 定罪日期；(c) 罪名；(d) 法院及案件编号。", yn=True,
  note="警告：请务必如实、完整地列出所有定罪记录；隐瞒会严重损害您的案件。",
  groups=[(None, [("(a) City and state where convicted","定罪的城市和州"),("(b) Date of conviction","定罪日期"),("(c) Offense","罪名"),("(d) Court and case number","法院名称及案件编号")], 2)]),
 dict(n="2.9", en="Can you speak English with ease? If not, what language and dialect do you normally use?",
  cn="您能否轻松地用英语进行口头交流？如果不能，您平时使用哪种语言和方言？", yn=True,
  groups=[(None, [("Language and dialect normally used","平时使用的语言及方言（例：中文普通话）")], 1)]),
 dict(n="2.10", en="Can you read and write English with ease? If not, what language and dialect do you normally use?",
  cn="您能否轻松地阅读和书写英文？如果不能，您平时使用哪种语言和方言？", yn=True,
  groups=[(None, [("Language and dialect normally used","平时使用的语言及方言")], 1)]),
 dict(n="2.11", en="At the time of the INCIDENT were you acting as an agent or employee for any PERSON? If so, state: (a) the name, ADDRESS, and telephone number of that PERSON; and (b) a description of your duties.",
  cn="本次事故发生时，您是否正在为他人（任何个人或公司）担任代理人或雇员，即是否正在工作或执行工作任务？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Name","该个人 / 公司名称"),("(a) ADDRESS","地址"),("(a) Telephone","电话"),("(b) Description of your duties","您当时的工作职责说明")], 1)]),
 dict(n="2.12", en="At the time of the INCIDENT did you or any other person have any physical, emotional, or mental disability or condition that may have contributed to the occurrence of the INCIDENT? If so, for each person state: (a) the name, ADDRESS, and telephone number; (b) the nature of the disability or condition; and (c) the manner in which the disability or condition contributed to the occurrence of the INCIDENT.",
  cn="本次事故发生时，您或任何其他人是否存在可能导致事故发生的身体、情绪或精神方面的残疾或状况？如果有，请就每一人填写：", yn=True,
  groups=[(None, [("(a) Name","姓名"),("(a) ADDRESS","地址"),("(a) Telephone","电话"),("(b) Nature of the disability or condition","残疾或状况的性质"),("(c) How it contributed to the INCIDENT","该状况如何导致事故发生")], 2)]),
 dict(n="2.13", en="Within 24 hours before the INCIDENT did you or any person involved in the INCIDENT use or take any of the following substances: alcoholic beverage, marijuana, or other drug or medication of any kind (prescription or not)? If so, for each person state: (a) the name, ADDRESS, and telephone number; (b) the nature or description of each substance; (c) the quantity of each substance used or taken; (d) the date and time of day when each substance was used or taken; (e) the ADDRESS where each substance was used or taken; (f) the name, ADDRESS, and telephone number of each person who was present when each substance was used or taken; and (g) the name, ADDRESS, and telephone number of any HEALTH CARE PROVIDER who prescribed or furnished the substance and the condition for which it was prescribed or furnished.",
  cn="在本次事故发生前 24 小时内，您或任何涉事人员是否使用或服用过下列物质：酒精饮料、大麻，或任何其他药品、药物（无论是否处方药）？如果有，请就每一人填写：", yn=True,
  note="警告：包括医生开具的日常处方药（如降压药、糖尿病药、过敏药、安眠药等），请如实填写。",
  groups=[(None, [("(a) Name","姓名"),("(a) ADDRESS","地址"),("(a) Telephone","电话"),("(b) Nature or description of the substance","药物 / 物质的名称及种类"),("(c) Quantity used or taken","服用量（例：20 毫克 / 20 盎司）"),("(d) Date and time taken","服用的日期及具体时间"),("(e) ADDRESS where taken","服用的地点"),("(f) Persons present (name, ADDRESS, telephone)","服用时在场者的姓名、地址、电话"),("(g) HEALTH CARE PROVIDER who prescribed it, and the condition","开药的医生 / 医疗机构名称、地址、电话，以及所针对的病症")], 2)]),
])

NAP = [("Name","姓名"),("ADDRESS","地址"),("Telephone","电话")]

S3 = dict(hdr="3.0  GENERAL BACKGROUND INFORMATION — BUSINESS ENTITY  实体背景资料",
 note="（本节仅在答复方为公司、合伙、有限责任公司等实体时填写；个人客户整节跳过即可。）", qs=[
 dict(n="3.1", en="Are you a corporation? If so, state: (a) the name stated in the current articles of incorporation; (b) all other names used by the corporation during the past 10 years and the dates each was used; (c) the date and place of incorporation; (d) the ADDRESS of the principal place of business; and (e) whether you are qualified to do business in California.",
  cn="您是否为公司（corporation）？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Name in the current articles of incorporation","现行公司章程中的名称"),("(b) Other names used in the past 10 years and dates","过去 10 年使用过的其他名称及使用期间"),("(c) Date and place of incorporation","注册成立日期及地点"),("(d) ADDRESS of the principal place of business","主要营业场所地址"),("(e) Qualified to do business in California?","是否已取得在加州经营的资格")], 1)]),
 dict(n="3.2", en="Are you a partnership? If so, state: (a) the current partnership name; (b) all other names used by the partnership during the past 10 years and the dates each was used; (c) whether you are a limited partnership and, if so, under the laws of what jurisdiction; (d) the name and ADDRESS of each general partner; and (e) the ADDRESS of the principal place of business.",
  cn="您是否为合伙组织（partnership）？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Current partnership name","现用合伙名称"),("(b) Other names used in the past 10 years and dates","过去 10 年使用过的其他名称及使用期间"),("(c) Limited partnership? Under what jurisdiction?","是否为有限合伙；如是，依据哪一法域的法律"),("(d) Name and ADDRESS of each general partner","每位普通合伙人的姓名及地址"),("(e) ADDRESS of the principal place of business","主要营业场所地址")], 1)]),
 dict(n="3.3", en="Are you a limited liability company? If so, state: (a) the name stated in the current articles of organization; (b) all other names used by the company during the past 10 years and the date each was used; (c) the date and place of filing of the articles of organization; (d) the ADDRESS of the principal place of business; and (e) whether you are qualified to do business in California.",
  cn="您是否为有限责任公司（LLC）？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Name in the current articles of organization","现行组织章程中的名称"),("(b) Other names used in the past 10 years and dates","过去 10 年使用过的其他名称及使用期间"),("(c) Date and place of filing of the articles of organization","组织章程的备案日期及地点"),("(d) ADDRESS of the principal place of business","主要营业场所地址"),("(e) Qualified to do business in California?","是否已取得在加州经营的资格")], 1)]),
 dict(n="3.4", en="Are you a joint venture? If so, state: (a) the current joint venture name; (b) all other names used by the joint venture during the past 10 years and the dates each was used; (c) the name and ADDRESS of each joint venturer; and (d) the ADDRESS of the principal place of business.",
  cn="您是否为合营企业（joint venture）？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Current joint venture name","现用合营企业名称"),("(b) Other names used in the past 10 years and dates","过去 10 年使用过的其他名称及使用期间"),("(c) Name and ADDRESS of each joint venturer","每位合营方的名称及地址"),("(d) ADDRESS of the principal place of business","主要营业场所地址")], 1)]),
 dict(n="3.5", en="Are you an unincorporated association? If so, state: (a) the current unincorporated association name; (b) all other names used by the unincorporated association during the past 10 years and the dates each was used; and (c) the ADDRESS of the principal place of business.",
  cn="您是否为非法人团体（unincorporated association）？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Current name","现用名称"),("(b) Other names used in the past 10 years and dates","过去 10 年使用过的其他名称及使用期间"),("(c) ADDRESS of the principal place of business","主要营业场所地址")], 1)]),
 dict(n="3.6", en="Have you done business under a fictitious name during the past 10 years? If so, for each fictitious name state: (a) the name; (b) the dates each was used; (c) the state and county of each fictitious name filing; and (d) the ADDRESS of the principal place of business.",
  cn="过去 10 年内，您是否曾以虚拟商号（fictitious name / DBA）经营？如果有，请就每一商号填写：", yn=True,
  groups=[(None, [("(a) The name","商号名称"),("(b) Dates used","使用起止期间"),("(c) State and county of the filing","备案的州及县"),("(d) ADDRESS of the principal place of business","主要营业场所地址")], 2)]),
 dict(n="3.7", en="Within the past five years has any public entity registered or licensed your business? If so, for each license or registration: (a) identify the license or registration; (b) state the name of the public entity; and (c) state the dates of issuance and expiration.",
  cn="过去五年内，是否有任何公共机关为您的业务办理过登记或颁发过执照？如果有，请就每一项填写：", yn=True,
  groups=[(None, [("(a) Identify the license or registration","执照或登记的名称、编号"),("(b) Name of the public entity","颁发机关名称"),("(c) Dates of issuance and expiration","颁发日期及到期日期")], 2)]),
])

S4 = dict(hdr="4.0  INSURANCE  保险", note=None, qs=[
 dict(n="4.1", en="At the time of the INCIDENT, was there in effect any policy of insurance through which you were or might be insured in any manner (for example, primary, pro-rata, or excess liability coverage or medical expense coverage) for the damages, claims, or actions that have arisen out of the INCIDENT? If so, for each policy state: (a) the kind of coverage; (b) the name and ADDRESS of the insurance company; (c) the name, ADDRESS, and telephone number of each named insured; (d) the policy number; (e) the limits of coverage for each type of coverage contained in the policy; (f) whether any reservation of rights or controversy or coverage dispute exists between you and the insurance company; and (g) the name, ADDRESS, and telephone number of the custodian of the policy.",
  cn="本次事故发生时，是否存在任何有效的保险单，使您就本次事故引起的损害、索赔或诉讼可能获得任何形式的承保（例如：主险、按比例分摊险、超额责任险，或医疗费用险）？如果有，请就每一份保单填写：", yn=True,
  note="请把保险卡正反面、以及保单声明页（Declaration Page）拍照发给我们，已发过则无需重复。",
  groups=[(None, [("(a) Kind of coverage","险种（例：汽车责任险、医疗费用险、健康保险）"),("(b) Name and ADDRESS of the insurance company","保险公司名称及地址"),("(c) Name, ADDRESS, telephone of each named insured","每位被保险人的姓名、地址、电话"),("(d) Policy number","保单号"),("(e) Limits of coverage for each type","各险种的保额上限"),("(f) Any reservation of rights or coverage dispute?","与保险公司之间是否存在保留权利声明或承保争议"),("(g) Name, ADDRESS, telephone of the custodian of the policy","保单保管人的姓名、地址、电话")], 2)]),
 dict(n="4.2", en="Are you self-insured under any statute for the damages, claims, or actions that have arisen out of the INCIDENT? If so, specify the statute.",
  cn="就本次事故引起的损害、索赔或诉讼，您是否依据任何法律属于自保（self-insured）？如果是，请指明具体法条。", yn=True,
  groups=[(None, [("Specify the statute","法条名称 / 条号")], 1)]),
])

S6 = dict(hdr="6.0  PHYSICAL, MENTAL, OR EMOTIONAL INJURIES  身体、精神或情绪上的伤害", note=None, qs=[
 dict(n="6.1", en="Do you attribute any physical, mental, or emotional injuries to the INCIDENT? (If your answer is “no,” do not answer interrogatories 6.2 through 6.7.)",
  cn="您是否认为本次事故造成了您身体、精神或情绪上的伤害？（如果回答「否」，6.2 至 6.7 不必填写。）", yn=True),
 dict(n="6.2", en="Identify each injury you attribute to the INCIDENT and the area of your body affected.",
  cn="请列出您认为由本次事故造成的每一处伤害，以及受影响的身体部位。", lines=4,
  note="请尽量完整，例如：颈部扭伤、下背部疼痛、右肩、左膝、头痛、失眠、焦虑等。"),
 dict(n="6.3", en="Do you still have any complaints that you attribute to the INCIDENT? If so, for each complaint state: (a) a description; (b) whether the complaint is subsiding, remaining the same, or becoming worse; and (c) the frequency and duration.",
  cn="到今天为止，您是否仍有由本次事故引起的不适或症状？如果有，请就每一项填写：", yn=True,
  groups=[(None, [("(a) Description","症状描述（部位、感觉）"),("(b) Subsiding, the same, or becoming worse?","在好转 / 没有变化 / 在恶化"),("(c) Frequency and duration","发作频率及每次持续时间（例：每周 3–4 次，每次约 2 小时）")], 3)]),
 dict(n="6.4", en="Did you receive any consultation or examination (except from expert witnesses covered by Code of Civil Procedure sections 2034.210–2034.310) or treatment from a HEALTH CARE PROVIDER for any injury you attribute to the INCIDENT? If so, for each HEALTH CARE PROVIDER state: (a) the name, ADDRESS, and telephone number; (b) the type of consultation, examination, or treatment provided; (c) the dates you received consultation, examination, or treatment; and (d) the charges to date.",
  cn="就您认为由本次事故造成的伤害，您是否接受过任何医疗机构的问诊、检查或治疗？如果有，请就每一家医疗机构填写：", yn=True,
  note="请把所有看过的医院、急诊、诊所、推拿 / 针灸、理疗、影像中心（MRI/X-ray）、专科医生全部列出，包括只去过一次的。",
  groups=[(None, [("(a) Name","医疗机构 / 医生姓名"),("(a) ADDRESS","地址"),("(a) Telephone","电话"),("(b) Type of consultation, examination, or treatment","问诊 / 检查 / 治疗的类型"),("(c) Dates received","就诊起止日期"),("(d) Charges to date","至今的费用金额")], 3)]),
 dict(n="6.5", en="Have you taken any medication, prescribed or not, as a result of injuries that you attribute to the INCIDENT? If so, for each medication state: (a) the name; (b) the PERSON who prescribed or furnished it; (c) the date it was prescribed or furnished; (d) the dates you began and stopped taking it; and (e) the cost to date.",
  cn="因本次事故造成的伤害，您是否服用过任何药物（无论是否处方药）？如果有，请就每一种药物填写：", yn=True,
  note="包括自己在药房买的止痛药、药膏、贴剂等。",
  groups=[(None, [("(a) Name","药物名称"),("(b) PERSON who prescribed or furnished it","开药或提供者（医生 / 药房）"),("(c) Date prescribed or furnished","开药 / 取药日期"),("(d) Dates you began and stopped taking it","开始及停止服用的日期"),("(e) Cost to date","至今的花费")], 3)]),
 dict(n="6.6", en="Are there any other medical services necessitated by the injuries that you attribute to the INCIDENT that were not previously listed (for example, ambulance, nursing, prosthetics)? If so, for each service state: (a) the nature; (b) the date; (c) the cost; and (d) the name, ADDRESS, and telephone number of each provider.",
  cn="除上述以外，因本次事故的伤害，您是否还需要过其他医疗相关服务（例如救护车、护理、义肢、医疗器材）？如果有，请就每一项填写：", yn=True,
  groups=[(None, [("(a) Nature","服务内容"),("(b) Date","日期"),("(c) Cost","费用"),("(d) Name, ADDRESS, telephone of the provider","提供方名称、地址、电话")], 2)]),
 dict(n="6.7", en="Has any HEALTH CARE PROVIDER advised that you may require future or additional treatment for any injuries that you attribute to the INCIDENT? If so, for each injury state: (a) the name and ADDRESS of each HEALTH CARE PROVIDER; (b) the complaints for which the treatment was advised; and (c) the nature, duration, and estimated cost of the treatment.",
  cn="是否有任何医疗机构告知您，就本次事故造成的伤害您将来可能还需要治疗或进一步治疗？如果有，请就每一处伤害填写：", yn=True,
  groups=[(None, [("(a) Name and ADDRESS of the HEALTH CARE PROVIDER","医疗机构 / 医生名称及地址"),("(b) Complaints for which treatment was advised","针对哪些症状建议治疗"),("(c) Nature, duration, and estimated cost of the treatment","建议的治疗方式、预计疗程及预估费用")], 2)]),
])

S7 = dict(hdr="7.0  PROPERTY DAMAGE  财产损失", note=None, qs=[
 dict(n="7.1", en="Do you attribute any loss of or damage to a vehicle or other property to the INCIDENT? If so, for each item of property: (a) describe the property; (b) describe the nature and location of the damage to the property; (c) state the amount of damage you are claiming for each item of property and how the amount was calculated; and (d) if the property was sold, state the name, ADDRESS, and telephone number of the seller, the date of sale, and the sale price.",
  cn="您是否认为本次事故造成了车辆或其他财产的损失或损坏？如果有，请就每一项财产填写：", yn=True,
  groups=[(None, [("(a) Describe the property","财产描述（车辆请写年份 / 厂牌 / 型号 / 车牌号）"),("(b) Nature and location of the damage","损坏的性质及部位"),("(c) Amount claimed and how it was calculated","索赔金额及计算方式"),("(d) If sold: seller's name, ADDRESS, telephone; date of sale; sale price","如已出售：出售人姓名、地址、电话；出售日期；售价")], 2),
          ("Current status of your vehicle 您车辆目前的状态（请在对应项后打勾）", [("Repaired","已修好"),("Waiting to be repaired","等待修理"),("Totaled","全损"),("Sold","已出售")], 1)]),
 dict(n="7.2", en="Has a written estimate or evaluation been made for any item of property referred to in your answer to the preceding interrogatory? If so, for each estimate or evaluation state: (a) the name, ADDRESS, and telephone number of the PERSON who prepared it and the date prepared; (b) the name, ADDRESS, and telephone number of each PERSON who has a copy of it; and (c) the amount of damage stated.",
  cn="上一题所列财产，是否有人出具过书面的估价单或评估报告？如果有，请就每一份填写：", yn=True,
  groups=[(None, [("(a) Name, ADDRESS, telephone of the preparer, and the date prepared","出具人的名称、地址、电话，以及出具日期"),("(b) Name, ADDRESS, telephone of each PERSON who has a copy","持有该文件副本者的名称、地址、电话"),("(c) Amount of damage stated","报告中载明的损失金额")], 2)]),
 dict(n="7.3", en="Has any item of property referred to in your answer to interrogatory 7.1 been repaired? If so, for each item state: (a) the date repaired; (b) a description of the repair; (c) the repair cost; (d) the name, ADDRESS, and telephone number of the PERSON who repaired it; and (e) the name, ADDRESS, and telephone number of the PERSON who paid for the repair.",
  cn="7.1 题所列的财产是否已经修理？如果有，请就每一项填写：", yn=True,
  groups=[(None, [("(a) Date repaired","修理日期"),("(b) Description of the repair","修理内容说明"),("(c) Repair cost","修理费用"),("(d) Name, ADDRESS, telephone of the repairer","修理厂 / 修理人的名称、地址、电话"),("(e) Name, ADDRESS, telephone of who paid for the repair","支付修理费者的姓名、地址、电话")], 2)]),
])

S8 = dict(hdr="8.0  LOSS OF INCOME OR EARNING CAPACITY  收入或工作能力损失", note=None, qs=[
 dict(n="8.1", en="Do you attribute any loss of income or earning capacity to the INCIDENT? (If your answer is “no,” do not answer interrogatories 8.2 through 8.8.)",
  cn="您是否认为本次事故造成了您的收入损失或工作能力损失？（如果回答「否」，8.2 至 8.8 不必填写。）", yn=True,
  note="如回答「是」，请提供事故发生前三个月及事故发生后三个月的工资单、收入证明或请假记录，作为工资损失索赔的证据。"),
 dict(n="8.2", en="State: (a) the nature of your work; (b) your job title at the time of the INCIDENT; and (c) the date your employment began.",
  cn="请填写：(a) 您的工作性质；(b) 事故发生时的职位名称；(c) 入职日期。",
  groups=[(None, [("(a) Nature of your work","工作性质 / 内容"),("(b) Job title at the time of the INCIDENT","事故发生时的职位"),("(c) Date your employment began","入职日期")], 1)]),
 dict(n="8.3", en="State the last date before the INCIDENT that you worked for compensation.",
  cn="请填写事故发生前，您最后一次有薪工作的日期。",
  groups=[(None, [("Last date worked for compensation before the INCIDENT","事故前最后一次有薪工作的日期")], 1)]),
 dict(n="8.4", en="State your monthly income at the time of the INCIDENT and how the amount was calculated.",
  cn="请填写事故发生时您的月收入，以及该金额的计算方式。",
  groups=[(None, [("Hourly or monthly pay rate","时薪或月薪"),("Days worked per week","每周工作天数"),("Hours worked per day","每天工作小时数"),("Weeks worked per month","每月工作周数"),("Monthly income at the time of the INCIDENT","事故发生时的月收入"),("How the amount was calculated","计算方式说明")], 1)]),
 dict(n="8.5", en="State the date you returned to work at each place of employment following the INCIDENT.",
  cn="请填写事故后您在每一个工作单位复工的日期。",
  groups=[(None, [("Place of employment","工作单位名称"),("Date you returned to work","复工日期")], 2)]),
 dict(n="8.6", en="State the dates you did not work and for which you lost income as a result of the INCIDENT.",
  cn="请填写因本次事故而未能工作、并因此损失收入的时间段。", lines=3,
  note="例：2026年3月5日–2026年4月18日。"),
 dict(n="8.7", en="State the total income you have lost to date as a result of the INCIDENT and how the amount was calculated.",
  cn="请填写因本次事故至今损失的收入总额，以及该金额的计算方式。",
  groups=[(None, [("Total income lost to date","至今的收入损失总额"),("How the amount was calculated","计算方式说明")], 1)]),
 dict(n="8.8", en="Will you lose income in the future as a result of the INCIDENT? If so, state: (a) the facts on which you base this contention; (b) an estimate of the amount; (c) an estimate of how long you will be unable to work; and (d) how the claim for future income is calculated.",
  cn="因本次事故，您将来是否还会有收入损失？如果会，请填写：", yn=True,
  groups=[(None, [("(a) Facts on which you base this contention","您作此主张所依据的事实"),("(b) Estimate of the amount","预估金额"),("(c) Estimate of how long you will be unable to work","预估无法工作的时间长度"),("(d) How the claim is calculated","计算方式说明")], 1)]),
])

S9 = dict(hdr="9.0  OTHER DAMAGES  其他损失", note=None, qs=[
 dict(n="9.1", en="Are there any other damages that you attribute to the INCIDENT? If so, for each item of damage state: (a) the nature; (b) the date it occurred; (c) the amount; and (d) the name, ADDRESS, and telephone number of each PERSON to whom an obligation was incurred.",
  cn="除上述以外，您是否还有其他因本次事故造成的损失？如果有，请就每一项填写：", yn=True,
  note="例如：自付医疗费、交通费、租车费、护工费、家务帮佣费、误餐费等。",
  groups=[(None, [("(a) Nature","损失性质 / 项目"),("(b) Date it occurred","发生日期"),("(c) Amount","金额"),("(d) Name, ADDRESS, telephone of each PERSON to whom an obligation was incurred","应付款对象的名称、地址、电话")], 3)]),
 dict(n="9.2", en="Do any DOCUMENTS support the existence or amount of any item of damages claimed in interrogatory 9.1? If so, describe each document and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT.",
  cn="是否有任何文件可以证明 9.1 题所列损失的存在或金额？如果有，请描述每一份文件，并填写持有人的姓名、地址、电话。", yn=True,
  groups=[(None, [("Description of the DOCUMENT","文件名称 / 内容描述（例：收据、发票、账单）"),("Name, ADDRESS, telephone of the PERSON who has it","持有人姓名、地址、电话")], 3)]),
])

CONT4 = [("(a) Facts on which you base your contention","您作此主张所依据的全部事实"),
         ("(b) Names, ADDRESSES, telephone numbers of all PERSONS who have knowledge of the facts","知悉上述事实的所有人的姓名、地址、电话"),
         ("(c) DOCUMENTS and other tangible things that support your contention, and who has each","支持该主张的所有文件及实物，以及各自的持有人姓名、地址、电话")]

def contention(n, en, cn, first_label=None):
    items = ([(first_label[0], first_label[1])] if first_label else [])
    pref = ["(b)","(c)","(d)"] if first_label else ["(a)","(b)","(c)"]
    for p,(e,c) in zip(pref, CONT4):
        items.append((p+" "+e.split(") ",1)[1], c))
    return dict(n=n, en=en, cn=cn, yn=True, groups=[(None, items, 1)])

S10 = dict(hdr="10.0  MEDICAL HISTORY  既往病史", note=None, qs=[
 dict(n="10.1", en="At any time before the INCIDENT did you have complaints or injuries that involved the same part of your body claimed to have been injured in the INCIDENT? If so, for each state: (a) a description of the complaint or injury; (b) the dates it began and ended; and (c) the name, ADDRESS, and telephone number of each HEALTH CARE PROVIDER whom you consulted or who examined or treated you.",
  cn="在本次事故之前，您是否曾在本次事故所主张受伤的同一身体部位有过不适或受过伤？如果有，请就每一次填写：", yn=True,
  note="请务必如实填写。对方会去调取您的病历，隐瞒旧伤反而会被用来攻击您本次受伤的因果关系。",
  groups=[(None, [("(a) Description of the complaint or injury","症状或受伤的描述（哪个部位、什么情况）"),("(b) Dates it began and ended","开始及结束的时间（例：2019年9月–2020年6月）"),("(c) Name, ADDRESS, telephone of each HEALTH CARE PROVIDER","所有看过的医生 / 医疗机构的名称、地址、电话")], 3)]),
 dict(n="10.2", en="List all physical, mental, and emotional disabilities you had immediately before the INCIDENT. (You may omit mental or emotional disabilities unless you attribute any mental or emotional injury to the INCIDENT.)",
  cn="请列出本次事故发生前您已有的所有身体、精神及情绪方面的残疾或健康问题。（如果您并未就本次事故主张精神或情绪方面的损害，则精神 / 情绪方面可以不填。）", lines=3),
 dict(n="10.3", en="At any time after the INCIDENT, did you sustain injuries of the kind for which you are now claiming damages? If so, for each incident giving rise to an injury state: (a) the date and the place it occurred; (b) the name, ADDRESS, and telephone number of any other PERSON involved; (c) the nature of any injuries you sustained; (d) the name, ADDRESS, and telephone number of each HEALTH CARE PROVIDER who you consulted or who examined or treated you; and (e) the nature of the treatment and its duration.",
  cn="本次事故之后，您是否又受过与本案所主张伤害同类的伤？如果有，请就每一次事件填写：", yn=True,
  groups=[(None, [("(a) Date and place it occurred","发生日期及地点"),("(b) Name, ADDRESS, telephone of any other PERSON involved","其他涉事人员的姓名、地址、电话"),("(c) Nature of any injuries you sustained","您的受伤部位及性质"),("(d) Name, ADDRESS, telephone of each HEALTH CARE PROVIDER","所有看过的医生 / 医疗机构的名称、地址、电话"),("(e) Nature of the treatment and its duration","治疗方式及持续时间")], 2)]),
])

S11 = dict(hdr="11.0  OTHER CLAIMS AND PREVIOUS CLAIMS  其他及既往索赔", note=None, qs=[
 dict(n="11.1", en="Except for this action, in the past 10 years have you filed an action or made a written claim or demand for compensation for your personal injuries? If so, for each action, claim, or demand state: (a) the date, time, and place and location (closest street ADDRESS or intersection) of the INCIDENT giving rise to the action, claim, or demand; (b) the name, ADDRESS, and telephone number of each PERSON against whom the claim or demand was made or the action filed; (c) the court, names of the parties, and case number of any action filed; (d) the name, ADDRESS, and telephone number of any attorney representing you; (e) whether the claim or action has been resolved or is pending; and (f) a description of the injury.",
  cn="除本案以外，过去 10 年内您是否曾就人身伤害提起过诉讼，或提出过书面索赔或赔偿要求？如果有，请就每一次填写：", yn=True,
  groups=[(None, [("(a) Date, time, place and location of the INCIDENT","引起该索赔 / 诉讼的事件的日期、时间、地点（最近的街道地址或路口）"),("(b) Name, ADDRESS, telephone of each PERSON against whom the claim was made","被索赔人 / 被告的姓名、地址、电话"),("(c) Court, names of the parties, and case number","法院名称、双方当事人姓名、案件编号"),("(d) Name, ADDRESS, telephone of any attorney representing you","您当时代理律师的姓名、地址、电话"),("(e) Resolved or pending?","该索赔 / 诉讼已结案还是仍在进行"),("(f) Description of the injury","受伤情况描述")], 2)]),
 dict(n="11.2", en="In the past 10 years have you made a written claim or demand for workers' compensation benefits? If so, for each claim or demand state: (a) the date, time, and place of the INCIDENT giving rise to the claim; (b) the name, ADDRESS, and telephone number of your employer at the time of the injury; (c) the name, ADDRESS, and telephone number of the workers' compensation insurer and the claim number; (d) the period of time during which you received workers' compensation benefits; (e) a description of the injury; (f) the name, ADDRESS, and telephone number of any HEALTH CARE PROVIDER who provided services; and (g) the case number at the Workers' Compensation Appeals Board.",
  cn="过去 10 年内，您是否曾提出过书面的工伤赔偿（workers' compensation）申请？如果有，请就每一次填写：", yn=True,
  groups=[(None, [("(a) Date, time, and place of the INCIDENT","引起该工伤申请的事件的日期、时间、地点"),("(b) Name, ADDRESS, telephone of your employer at the time","受伤时雇主的名称、地址、电话"),("(c) Name, ADDRESS, telephone of the workers' compensation insurer, and the claim number","工伤保险公司的名称、地址、电话，以及理赔编号"),("(d) Period during which you received benefits","领取工伤赔偿金的期间"),("(e) Description of the injury","受伤情况描述"),("(f) Name, ADDRESS, telephone of any HEALTH CARE PROVIDER who provided services","提供治疗的医生 / 医疗机构的名称、地址、电话"),("(g) Case number at the Workers' Compensation Appeals Board","工伤上诉委员会（WCAB）的案件编号")], 2)]),
])

S12 = dict(hdr="12.0  INVESTIGATION — GENERAL  调查（一般）", note=None, qs=[
 dict(n="12.1", en="State the name, ADDRESS, and telephone number of each individual: (a) who witnessed the INCIDENT or the events occurring immediately before or after the INCIDENT; (b) who made any statement at the scene of the INCIDENT; (c) who heard any statements made about the INCIDENT by any individual at the scene; and (d) who YOU OR ANYONE ACTING ON YOUR BEHALF claim has knowledge of the INCIDENT (except for expert witnesses covered by Code of Civil Procedure section 2034).",
  cn="请填写下列每一类人员的姓名、地址、电话：",
  groups=[("(a) Who witnessed the INCIDENT, or the events immediately before or after  目击事故本身、或事故发生前后紧接情形的人", [("Name","姓名"),("ADDRESS","地址"),("Telephone","电话")], 3),
          ("(b) Who made any statement at the scene  在事故现场说过话的人", [("Name","姓名"),("ADDRESS","地址"),("Telephone","电话")], 2),
          ("(c) Who heard any statements made about the INCIDENT at the scene  在现场听到他人谈论事故的人", [("Name","姓名"),("ADDRESS","地址"),("Telephone","电话")], 2),
          ("(d) Who you claim has knowledge of the INCIDENT  您认为了解本次事故情况的其他人", [("Name","姓名"),("ADDRESS","地址"),("Telephone","电话")], 2)]),
 dict(n="12.2", en="Have YOU OR ANYONE ACTING ON YOUR BEHALF interviewed any individual concerning the INCIDENT? If so, for each individual state: (a) the name, ADDRESS, and telephone number of the individual interviewed; (b) the date of the interview; and (c) the name, ADDRESS, and telephone number of the PERSON who conducted the interview.",
  cn="您或任何代表您行事的人，是否就本次事故询问过任何人？如果有，请就每一人填写：", yn=True,
  groups=[(None, [("(a) Name, ADDRESS, telephone of the individual interviewed","被询问人的姓名、地址、电话"),("(b) Date of the interview","询问日期"),("(c) Name, ADDRESS, telephone of the PERSON who conducted it","进行询问者的姓名、地址、电话")], 2)]),
 dict(n="12.3", en="Have YOU OR ANYONE ACTING ON YOUR BEHALF obtained a written or recorded statement from any individual concerning the INCIDENT? If so, for each statement state: (a) the name, ADDRESS, and telephone number of the individual from whom the statement was obtained; (b) the name, ADDRESS, and telephone number of the individual who obtained the statement; (c) the date the statement was obtained; and (d) the name, ADDRESS, and telephone number of each PERSON who has the original statement or a copy.",
  cn="您或任何代表您行事的人，是否就本次事故取得过任何人的书面或录音 / 录像陈述？如果有，请就每一份填写：", yn=True,
  groups=[(None, [("(a) Name, ADDRESS, telephone of the individual who gave the statement","作出陈述者的姓名、地址、电话"),("(b) Name, ADDRESS, telephone of the individual who obtained it","取得该陈述者的姓名、地址、电话"),("(c) Date the statement was obtained","取得日期"),("(d) Name, ADDRESS, telephone of each PERSON who has the original or a copy","持有原件或副本者的姓名、地址、电话")], 2)]),
 dict(n="12.4", en="Do YOU OR ANYONE ACTING ON YOUR BEHALF know of any photographs, films, or videotapes depicting any place, object, or individual concerning the INCIDENT or plaintiff's injuries? If so, state: (a) the number of photographs or feet of film or videotape; (b) the places, objects, or persons photographed, filmed, or videotaped; (c) the date the photographs, films, or videotapes were taken; (d) the name, ADDRESS, and telephone number of the individual taking the photographs, films, or videotapes; and (e) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy of the photographs, films, or videotapes.",
  cn="您或任何代表您行事的人，是否知道有任何照片、影片或录像，拍到与本次事故或原告伤势有关的地点、物品或人员？如果有，请填写：", yn=True,
  note="请把您手上所有与事故有关的照片和视频（车损、现场、伤处、行车记录仪等）发给我们；已发过则无需重复。",
  groups=[(None, [("(a) Number of photographs or feet of film or videotape","照片张数或影片 / 录像长度"),("(b) Places, objects, or persons photographed","所拍摄的地点、物品或人员"),("(c) Date taken","拍摄日期"),("(d) Name, ADDRESS, telephone of the individual who took them","拍摄者的姓名、地址、电话"),("(e) Name, ADDRESS, telephone of each PERSON who has the original or a copy","持有原件或副本者的姓名、地址、电话")], 2)]),
 dict(n="12.5", en="Do YOU OR ANYONE ACTING ON YOUR BEHALF know of any diagram, reproduction, or model of any place or thing (except for items developed by expert witnesses covered by Code of Civil Procedure sections 2034.210–2034.310) concerning the INCIDENT? If so, for each item state: (a) the type (i.e., diagram, reproduction, or model); (b) the subject matter; and (c) the name, ADDRESS, and telephone number of each PERSON who has it.",
  cn="您或任何代表您行事的人，是否知道有任何与本次事故有关的现场图、复制件或模型？如果有，请就每一项填写：", yn=True,
  groups=[(None, [("(a) Type (diagram, reproduction, or model)","类型（示意图 / 复制件 / 模型）"),("(b) Subject matter","所描绘的内容"),("(c) Name, ADDRESS, telephone of each PERSON who has it","持有人的姓名、地址、电话")], 2)]),
 dict(n="12.6", en="Was a report made by any PERSON concerning the INCIDENT? If so, state: (a) the name, title, identification number, and employer of the PERSON who made the report; (b) the date and type of report made; (c) the name, ADDRESS, and telephone number of the PERSON for whom the report was made; and (d) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy of the report.",
  cn="是否有任何人就本次事故作过报告（例如警方事故报告、保险公司报告、公司内部报告）？如果有，请就每一份填写：", yn=True,
  groups=[(None, [("(a) Name, title, identification number, and employer of the PERSON who made the report","制作报告者的姓名、职务、工号、所属单位"),("(b) Date and type of report","报告日期及类型"),("(c) Name, ADDRESS, telephone of the PERSON for whom the report was made","报告是为谁制作的（名称、地址、电话）"),("(d) Name, ADDRESS, telephone of each PERSON who has the original or a copy","持有原件或副本者的姓名、地址、电话")], 2)]),
 dict(n="12.7", en="Have YOU OR ANYONE ACTING ON YOUR BEHALF inspected the scene of the INCIDENT? If so, for each inspection state: (a) the name, ADDRESS, and telephone number of the individual making the inspection (except for expert witnesses covered by Code of Civil Procedure sections 2034.210–2034.310); and (b) the date of the inspection.",
  cn="您或任何代表您行事的人，事后是否到事故现场查看过？如果有，请就每一次填写：", yn=True,
  groups=[(None, [("(a) Name, ADDRESS, telephone of the individual making the inspection","前往查看者的姓名、地址、电话"),("(b) Date of the inspection","查看日期"),("Any photos or video taken? If so, please provide","是否拍照 / 录像？如有，请提供给我们")], 2)]),
])

S13 = dict(hdr="13.0  INVESTIGATION — SURVEILLANCE  调查（跟踪监视）",
 note="（本节通常由被告方回答；如您为原告，一般整节不会被勾选。）", qs=[
 dict(n="13.1", en="Have YOU OR ANYONE ACTING ON YOUR BEHALF conducted surveillance of any individual involved in the INCIDENT or any party to this action? If so, for each surveillance state: (a) the name, ADDRESS, and telephone number of the individual or party; (b) the time, date, and place of the surveillance; (c) the name, ADDRESS, and telephone number of the individual who conducted the surveillance; and (d) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy of any surveillance photograph, film, or videotape.",
  cn="您或任何代表您行事的人，是否对任何涉事人员或本案任何当事人进行过跟踪监视？如果有，请就每一次填写：", yn=True,
  groups=[(None, [("(a) Name, ADDRESS, telephone of the individual or party","被监视者的姓名、地址、电话"),("(b) Time, date, and place of the surveillance","监视的时间、日期、地点"),("(c) Name, ADDRESS, telephone of the individual who conducted it","实施监视者的姓名、地址、电话"),("(d) Name, ADDRESS, telephone of each PERSON who has the original or a copy","持有监视照片 / 影片原件或副本者的姓名、地址、电话")], 2)]),
 dict(n="13.2", en="Has a written report been prepared on the surveillance? If so, for each written report state: (a) the title; (b) the date; (c) the name, ADDRESS, and telephone number of the individual who prepared the report; and (d) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy.",
  cn="是否就该监视制作过书面报告？如果有，请就每一份填写：", yn=True,
  groups=[(None, [("(a) Title","报告标题"),("(b) Date","报告日期"),("(c) Name, ADDRESS, telephone of the individual who prepared it","制作人的姓名、地址、电话"),("(d) Name, ADDRESS, telephone of each PERSON who has the original or a copy","持有原件或副本者的姓名、地址、电话")], 2)]),
])

S14 = dict(hdr="14.0  STATUTORY OR REGULATORY VIOLATIONS  违反法律、法规或规章", note=None, qs=[
 dict(n="14.1", en="Do YOU OR ANYONE ACTING ON YOUR BEHALF contend that any PERSON involved in the INCIDENT violated any statute, ordinance, or regulation and that the violation was a legal (proximate) cause of the INCIDENT? If so, identify the name, ADDRESS, and telephone number of each PERSON and the statute, ordinance, or regulation that was violated.",
  cn="您或任何代表您行事的人，是否主张任何涉事人员违反了法律、地方法规或规章，且该违反行为是本次事故的法律（近因）原因？如果是，请填写：", yn=True,
  groups=[(None, [("Name, ADDRESS, telephone of the PERSON","该人的姓名、地址、电话"),("Statute, ordinance, or regulation violated","所违反的法律 / 法规 / 规章（例：加州车辆法 Vehicle Code §22350 超速）")], 2)]),
 dict(n="14.2", en="Was any PERSON cited or charged with a violation of any statute, ordinance, or regulation as a result of this INCIDENT? If so, for each PERSON state: (a) the name, ADDRESS, and telephone number of the PERSON; (b) the statute, ordinance, or regulation allegedly violated; (c) whether the PERSON entered a plea in response to the citation or charge and, if so, the plea entered; and (d) the name and ADDRESS of the court or administrative agency, names of the parties, and case number.",
  cn="因本次事故，是否有任何人被开罚单或被指控违反法律、法规或规章？如果有，请就每一人填写：", yn=True,
  groups=[(None, [("(a) Name, ADDRESS, telephone of the PERSON","该人的姓名、地址、电话"),("(b) Statute, ordinance, or regulation allegedly violated","被指违反的法条"),("(c) Plea entered, if any","是否作出答辩；如有，答辩内容"),("(d) Name and ADDRESS of the court or agency, names of the parties, case number","法院或行政机关的名称及地址、双方当事人姓名、案件编号")], 2)]),
])

S15 = dict(hdr="15.0  DENIALS AND SPECIAL OR AFFIRMATIVE DEFENSES  否认与特别 / 积极抗辩",
 note="（本节通常由被告方回答；如您为原告，一般整节不会被勾选。）", qs=[
 dict(n="15.1", en="Identify each denial of a material allegation and each special or affirmative defense in your pleadings, and for each: (a) state all facts on which you base the denial or special or affirmative defense; (b) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of those facts; and (c) identify all DOCUMENTS and other tangible things that support your denial or special or affirmative defense, and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT.",
  cn="请指明您在诉状 / 答辩状中对重要事实主张的每一项否认，以及每一项特别抗辩或积极抗辩，并就每一项填写：",
  groups=[(None, [("Denial or defense identified","所指明的否认或抗辩事由"),("(a) All facts on which you base it","所依据的全部事实"),("(b) Names, ADDRESSES, telephone numbers of all PERSONS who have knowledge of those facts","知悉上述事实的所有人的姓名、地址、电话"),("(c) All DOCUMENTS and tangible things that support it, and who has each","支持该事由的所有文件及实物，以及各自持有人的姓名、地址、电话")], 2)]),
])

ABC = [("(b) All facts on which you base your contention","您作此主张所依据的全部事实"),
       ("(c) Names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts","知悉上述事实的所有人的姓名、地址、电话"),
       ("(d) All DOCUMENTS and other tangible things that support your contention, and who has each","支持该主张的所有文件及实物，以及各自持有人的姓名、地址、电话")]
ABC3 = [("(a) All facts on which you base your contention","您作此主张所依据的全部事实"),
        ("(b) Names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts","知悉上述事实的所有人的姓名、地址、电话"),
        ("(c) All DOCUMENTS and other tangible things that support your contention, and who has each","支持该主张的所有文件及实物，以及各自持有人的姓名、地址、电话")]

S16 = dict(hdr="16.0  DEFENDANT'S CONTENTIONS — PERSONAL INJURY  被告方的主张（人身伤害）",
 note="（本节由被告方回答；如您为原告，一般整节不会被勾选。）", qs=[
 dict(n="16.1", en="Do you contend that any PERSON, other than you or plaintiff, contributed to the occurrence of the INCIDENT or the injuries or damages claimed by plaintiff? If so, for each PERSON: (a) state the name, ADDRESS, and telephone number of the PERSON; (b) state all facts on which you base your contention; (c) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts; and (d) identify all DOCUMENTS and other tangible things that support your contention and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
  cn="您是否主张除您和原告以外的任何人，对本次事故的发生或原告主张的伤害、损失有责任？如果是，请就每一人填写：", yn=True,
  groups=[(None, [("(a) Name, ADDRESS, telephone of the PERSON","该人的姓名、地址、电话")]+ABC, 2)]),
 dict(n="16.2", en="Do you contend that plaintiff was not injured in the INCIDENT? If so: (a) state all facts on which you base your contention; (b) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts; and (c) identify all DOCUMENTS and other tangible things that support your contention and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
  cn="您是否主张原告在本次事故中并未受伤？如果是，请填写：", yn=True, groups=[(None, ABC3, 1)]),
 dict(n="16.3", en="Do you contend that the injuries or the extent of the injuries claimed by plaintiff as disclosed in discovery proceedings thus far in this case were not caused by the INCIDENT? If so, for each injury: (a) identify it; (b) state all facts on which you base your contention; (c) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts; and (d) identify all DOCUMENTS and other tangible things that support your contention and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
  cn="您是否主张，截至目前证据交换中原告所披露的伤害或伤害程度并非由本次事故造成？如果是，请就每一处伤害填写：", yn=True,
  groups=[(None, [("(a) Identify the injury","指明该处伤害")]+ABC, 2)]),
 dict(n="16.4", en="Do you contend that any of the services furnished by any HEALTH CARE PROVIDER claimed by plaintiff in discovery proceedings thus far in this case were not due to the INCIDENT? If so: (a) identify each service; (b) state all facts on which you base your contention; (c) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts; and (d) identify all DOCUMENTS and other tangible things that support your contention and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
  cn="您是否主张，截至目前证据交换中原告所主张的任何医疗服务并非因本次事故而产生？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Identify each service","指明该项医疗服务")]+ABC, 2)]),
 dict(n="16.5", en="Do you contend that any of the costs of services furnished by any HEALTH CARE PROVIDER claimed as damages by plaintiff in discovery proceedings thus far in this case were not necessary or unreasonable? If so: (a) identify each cost; (b) state all facts on which you base your contention; (c) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts; and (d) identify all DOCUMENTS and other tangible things that support your contention and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
  cn="您是否主张，截至目前证据交换中原告作为损失主张的任何医疗费用并无必要或不合理？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Identify each cost","指明该项费用")]+ABC, 2)]),
 dict(n="16.6", en="Do you contend that any part of the loss of earnings or income claimed by plaintiff in discovery proceedings thus far in this case was unreasonable or was not caused by the INCIDENT? If so: (a) identify each part of the loss; (b) state all facts on which you base your contention; (c) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts; and (d) identify all DOCUMENTS and other tangible things that support your contention and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
  cn="您是否主张，截至目前证据交换中原告所主张的工资或收入损失有任何部分不合理、或并非由本次事故造成？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Identify each part of the loss","指明该部分损失")]+ABC, 2)]),
 dict(n="16.7", en="Do you contend that any of the property damage claimed by plaintiff in discovery proceedings thus far in this case was not caused by the INCIDENT? If so: (a) identify each item of property damage; (b) state all facts on which you base your contention; (c) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts; and (d) identify all DOCUMENTS and other tangible things that support your contention and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
  cn="您是否主张，截至目前证据交换中原告所主张的任何财产损失并非由本次事故造成？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Identify each item of property damage","指明该项财产损失")]+ABC, 2)]),
 dict(n="16.8", en="Do you contend that any of the costs of repairing the property damage claimed by plaintiff in discovery proceedings thus far in this case were unreasonable? If so: (a) identify each cost item; (b) state all facts on which you base your contention; (c) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of the facts; and (d) identify all DOCUMENTS and other tangible things that support your contention and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
  cn="您是否主张，截至目前证据交换中原告所主张的财产修理费用有任何部分不合理？如果是，请填写：", yn=True,
  groups=[(None, [("(a) Identify each cost item","指明该项费用")]+ABC, 2)]),
 dict(n="16.9", en="Do YOU OR ANYONE ACTING ON YOUR BEHALF have any DOCUMENT (for example, insurance bureau index reports) concerning claims for personal injuries made before or after the INCIDENT by a plaintiff in this case? If so, for each plaintiff state: (a) the source of each DOCUMENT; (b) the date each claim arose; (c) the nature of each claim; and (d) the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT.",
  cn="您或任何代表您行事的人，是否持有任何文件（例如保险业索赔索引报告），涉及本案原告在本次事故之前或之后提出的人身伤害索赔？如果有，请就每一位原告填写：", yn=True,
  groups=[(None, [("(a) Source of each DOCUMENT","该文件的来源"),("(b) Date each claim arose","每一索赔的发生日期"),("(c) Nature of each claim","每一索赔的性质"),("(d) Name, ADDRESS, telephone of the PERSON who has each DOCUMENT","文件持有人的姓名、地址、电话")], 2)]),
 dict(n="16.10", en="Do YOU OR ANYONE ACTING ON YOUR BEHALF have any DOCUMENT concerning the past or present physical, mental, or emotional condition of any plaintiff in this case from a HEALTH CARE PROVIDER not previously identified (except for expert witnesses covered by Code of Civil Procedure sections 2034.210–2034.310)? If so, for each plaintiff state: (a) the name, ADDRESS, and telephone number of each HEALTH CARE PROVIDER; (b) a description of each DOCUMENT; and (c) the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT.",
  cn="您或任何代表您行事的人，是否持有来自此前未披露的医疗机构、涉及本案任何原告过去或现在身体、精神或情绪状况的文件？如果有，请就每一位原告填写：", yn=True,
  groups=[(None, [("(a) Name, ADDRESS, telephone of each HEALTH CARE PROVIDER","该医疗机构的名称、地址、电话"),("(b) Description of each DOCUMENT","文件内容描述"),("(c) Name, ADDRESS, telephone of the PERSON who has each DOCUMENT","文件持有人的姓名、地址、电话")], 2)]),
])

S17 = dict(hdr="17.0  RESPONSES TO REQUEST FOR ADMISSIONS  对「承认请求」的答复",
 note="（本条须与随本问卷一并送达的 Requests for Admission 对照填写；若对方未同时送达 RFA，则本条不适用。）", qs=[
 dict(n="17.1", en="Is your response to each request for admission served with these interrogatories an unqualified admission? If not, for each response that is not an unqualified admission: (a) state the number of the request; (b) state all facts on which you base your response; (c) state the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of those facts; and (d) identify all DOCUMENTS and other tangible things that support your response and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
  cn="对于随本问卷一并送达的每一项「承认请求」，您的答复是否均为无保留的承认？如果不是，请就每一项非无保留承认的答复填写：", yn=True,
  groups=[(None, [("(a) Number of the request","该承认请求的编号"),("(b) All facts on which you base your response","您作此答复所依据的全部事实"),("(c) Names, ADDRESSES, telephone numbers of all PERSONS who have knowledge of those facts","知悉上述事实的所有人的姓名、地址、电话"),("(d) All DOCUMENTS and tangible things that support your response, and who has each","支持该答复的所有文件及实物，以及各自持有人的姓名、地址、电话")], 3)]),
])

S20 = dict(hdr="20.0  HOW THE INCIDENT OCCURRED — MOTOR VEHICLE  事故经过（机动车）", note=None, qs=[
 dict(n="20.1", en="State the date, time, and place of the INCIDENT (closest street ADDRESS or intersection).",
  cn="请填写本次事故的日期、时间和地点（最近的街道地址或路口）。",
  groups=[(None, [("Date","日期"),("Time","时间"),("Place (closest street ADDRESS or intersection)","地点（最近的街道地址或路口）")], 1)]),
 dict(n="20.2", en="For each vehicle involved in the INCIDENT, state: (a) the year, make, model, and license number; (b) the name, ADDRESS, and telephone number of the driver; (c) the name, ADDRESS, and telephone number of each occupant other than the driver; (d) the name, ADDRESS, and telephone number of each registered owner; (e) the name, ADDRESS, and telephone number of each lessee; (f) the name, ADDRESS, and telephone number of each owner other than the registered owner or lien holder; and (g) the name of each owner who gave permission or consent to the driver to operate the vehicle.",
  cn="请就本次事故涉及的每一辆车填写：",
  groups=[("Vehicle 车辆（您的车辆 / 对方车辆，请注明）", [("(a) Year, make, model, and license number","年份、厂牌、型号、车牌号"),("(b) Name, ADDRESS, telephone of the driver","驾驶人的姓名、地址、电话"),("(c) Name, ADDRESS, telephone of each occupant other than the driver","除驾驶人外每位乘客的姓名、地址、电话"),("(c) Additional occupant","其他乘客（姓名、地址、电话）"),("(d) Name, ADDRESS, telephone of each registered owner","登记车主的姓名、地址、电话"),("(e) Name, ADDRESS, telephone of each lessee","承租人的姓名、地址、电话"),("(f) Name, ADDRESS, telephone of each owner other than the registered owner or lien holder","登记车主及留置权人以外的其他所有人的姓名、地址、电话"),("(g) Name of each owner who gave permission or consent to the driver","同意驾驶人使用该车的所有人姓名")], 2)]),
 dict(n="20.3", en="State the ADDRESS and location where your trip began and the ADDRESS and location of your destination.",
  cn="请填写本次行程的出发地址和地点，以及目的地的地址和地点。",
  groups=[(None, [("ADDRESS and location where your trip began","出发地址及地点"),("ADDRESS and location of your destination","目的地的地址及地点")], 1)]),
 dict(n="20.4", en="Describe the route that you followed from the beginning of your trip to the location of the INCIDENT, and state the location of each stop, other than routine traffic stops, during the trip leading up to the INCIDENT.",
  cn="请描述您从行程起点到事故地点所走的路线，并说明事故发生前途中每一次停留的地点（例行的红灯 / 路口停车除外）。", lines=4),
 dict(n="20.5", en="State the name of the street or roadway, the lane of travel, and the direction of travel of each vehicle involved in the INCIDENT for the 500 feet of travel before the INCIDENT.",
  cn="请就每一辆涉事车辆，填写事故发生前 500 英尺行驶路段的街道 / 道路名称、所在车道和行驶方向。",
  groups=[("Vehicle 车辆（您的车辆 / 对方车辆，请注明）", [("Name of the street or roadway","街道 / 道路名称"),("Lane of travel","所在车道（例：最左侧车道 / 中间车道）"),("Direction of travel","行驶方向（例：由南向北）")], 2)]),
 dict(n="20.6", en="Did the INCIDENT occur at an intersection? If so, describe all traffic control devices, signals, or signs at the intersection.",
  cn="事故是否发生在路口？如果是，请描述该路口的所有交通管制设施、信号灯或标志。", yn=True, lines=2),
 dict(n="20.7", en="Was there a traffic signal facing you at the time of the INCIDENT? If so, state: (a) your location when you first saw it; (b) the color; (c) the number of seconds it had been that color; and (d) whether the color changed between the time you first saw it and the INCIDENT.",
  cn="事故发生时，是否有面向您的交通信号灯？如果有，请填写：", yn=True,
  groups=[(None, [("(a) Your location when you first saw it","您第一次看到该信号灯时所在的位置"),("(b) The color","当时的灯色"),("(c) Number of seconds it had been that color","该灯色已持续的秒数"),("(d) Did the color change between the time you first saw it and the INCIDENT?","从您第一次看到，到事故发生时，灯色是否变化过")], 1)]),
 dict(n="20.8", en="State how the INCIDENT occurred, giving the speed, direction, and location of each vehicle involved: (a) just before the INCIDENT; (b) at the time of the INCIDENT; and (c) just after the INCIDENT.",
  cn="请说明事故是如何发生的，并就每一辆涉事车辆填写下列三个时点的速度、方向和位置：",
  groups=[("(a) Just before the INCIDENT  事故发生前一刻", [("Your vehicle: speed, direction, location","您的车辆：速度、方向、位置"),("Other vehicle: speed, direction, location","对方车辆：速度、方向、位置")], 1),
          ("(b) At the time of the INCIDENT  事故发生时", [("Your vehicle: speed, direction, location","您的车辆：速度、方向、位置"),("Other vehicle: speed, direction, location","对方车辆：速度、方向、位置")], 1),
          ("(c) Just after the INCIDENT  事故发生后一刻", [("Your vehicle: speed, direction, location","您的车辆：速度、方向、位置"),("Other vehicle: speed, direction, location","对方车辆：速度、方向、位置")], 1)],
  tail_lines=4, tail_note="请用文字完整描述事故经过（撞击部位、先后顺序、事发后双方的反应等）："),
 dict(n="20.9", en="Do you have information that a malfunction or defect in a vehicle caused the INCIDENT? If so: (a) identify the vehicle; (b) identify each malfunction or defect; (c) state the name, ADDRESS, and telephone number of each PERSON who is a witness to or has information about each malfunction or defect; and (d) state the name, ADDRESS, and telephone number of each PERSON who has custody of each defective part.",
  cn="您是否掌握任何信息，显示某辆车的故障或缺陷导致了本次事故？如果有，请填写：", yn=True,
  groups=[(None, [("(a) Identify the vehicle","指明该车辆（年份 / 厂牌 / 型号 / 车牌号）"),("(b) Identify each malfunction or defect","指明每一项故障或缺陷"),("(c) Name, ADDRESS, telephone of each PERSON who is a witness to or has information about it","目击或了解该故障者的姓名、地址、电话"),("(d) Name, ADDRESS, telephone of each PERSON who has custody of each defective part","保管该缺陷部件者的姓名、地址、电话")], 1)]),
 dict(n="20.10", en="Do you have information that any malfunction or defect in a vehicle contributed to the injuries sustained in the INCIDENT? If so: (a) identify the vehicle; (b) identify each malfunction or defect; (c) state the name, ADDRESS, and telephone number of each PERSON who is a witness to or has information about each malfunction or defect; and (d) state the name, ADDRESS, and telephone number of each PERSON who has custody of each defective part.",
  cn="您是否掌握任何信息，显示某辆车的故障或缺陷加重了本次事故中所受的伤害（例如安全带、安全气囊失灵）？如果有，请填写：", yn=True,
  groups=[(None, [("(a) Identify the vehicle","指明该车辆（年份 / 厂牌 / 型号 / 车牌号）"),("(b) Identify each malfunction or defect","指明每一项故障或缺陷"),("(c) Name, ADDRESS, telephone of each PERSON who is a witness to or has information about it","目击或了解该故障者的姓名、地址、电话"),("(d) Name, ADDRESS, telephone of each PERSON who has custody of each defective part","保管该缺陷部件者的姓名、地址、电话")], 1)]),
 dict(n="20.11", en="State the name, ADDRESS, and telephone number of each owner and each PERSON who has had possession since the INCIDENT of each vehicle involved in the INCIDENT.",
  cn="请填写本次事故所涉每一辆车，自事故发生以来的每一位所有人和每一位占有人的姓名、地址、电话。",
  groups=[("Vehicle 车辆（请注明是哪一辆）", [("Owner: name, ADDRESS, telephone","所有人的姓名、地址、电话"),("Who has had possession since the INCIDENT: name, ADDRESS, telephone","事故后占有该车者的姓名、地址、电话（例：拖车场、修理厂）")], 2)]),
])

S50 = dict(hdr="50.0  CONTRACT  合同",
 note="（本节仅用于合同纠纷案件；人身伤害案件通常整节不会被勾选。）", qs=[
 dict(n="50.1", en="For each agreement alleged in the pleadings: (a) identify each DOCUMENT that is part of the agreement and for each state the name, ADDRESS, and telephone number of each PERSON who has the DOCUMENT; (b) state each part of the agreement not in writing, the name, ADDRESS, and telephone number of each PERSON agreeing to that provision, and the date that part of the agreement was made; (c) identify all DOCUMENTS that evidence any part of the agreement not in writing and for each state the name, ADDRESS, and telephone number of each PERSON who has the DOCUMENT; (d) identify all DOCUMENTS that are part of any modification to the agreement, and for each state the name, ADDRESS, and telephone number of each PERSON who has the DOCUMENT; (e) state each modification not in writing, the date, and the name, ADDRESS, and telephone number of each PERSON agreeing to the modification, and the date the modification was made; (f) identify all DOCUMENTS that evidence any modification of the agreement not in writing and for each state the name, ADDRESS, and telephone number of each PERSON who has the DOCUMENT.",
  cn="就诉状中主张的每一份协议，请填写：",
  groups=[(None, [("(a) DOCUMENTS that are part of the agreement, and who has each","构成该协议的各份文件，以及各自持有人的姓名、地址、电话"),("(b) Each part of the agreement not in writing; who agreed to it; and the date it was made","协议中未形成书面的部分、同意该条款者的姓名 / 地址 / 电话，以及该部分达成的日期"),("(c) DOCUMENTS evidencing any part not in writing, and who has each","可证明非书面部分的文件，以及各自持有人的姓名、地址、电话"),("(d) DOCUMENTS that are part of any modification, and who has each","构成任何修改的文件，以及各自持有人的姓名、地址、电话"),("(e) Each modification not in writing, the date, and who agreed to it","未形成书面的每一项修改、日期，以及同意修改者的姓名、地址、电话"),("(f) DOCUMENTS evidencing any modification not in writing, and who has each","可证明非书面修改的文件，以及各自持有人的姓名、地址、电话")], 1)]),
 dict(n="50.2", en="Was there a breach of any agreement alleged in the pleadings? If so, for each breach describe and give the date of every act or omission that you claim is the breach of the agreement.",
  cn="诉状中主张的任何协议是否被违反？如果是，请就每一项违约描述您所主张的构成违约的每一作为或不作为，并写明日期。", yn=True, lines=3),
 dict(n="50.3", en="Was performance of any agreement alleged in the pleadings excused? If so, identify each agreement excused and state why performance was excused.",
  cn="诉状中主张的任何协议，其履行义务是否被免除？如果是，请指明被免除的每一份协议，并说明免除的理由。", yn=True, lines=3),
 dict(n="50.4", en="Was any agreement alleged in the pleadings terminated by mutual agreement, release, accord and satisfaction, or novation? If so, identify each agreement terminated, the date of termination, and the basis of the termination.",
  cn="诉状中主张的任何协议，是否曾因双方合意、免除、和解清偿或债务更新而终止？如果是，请指明被终止的每一份协议、终止日期及终止依据。", yn=True, lines=3),
 dict(n="50.5", en="Is any agreement alleged in the pleadings unenforceable? If so, identify each unenforceable agreement and state why it is unenforceable.",
  cn="诉状中主张的任何协议是否不可执行？如果是，请指明每一份不可执行的协议，并说明理由。", yn=True, lines=3),
 dict(n="50.6", en="Is any agreement alleged in the pleadings ambiguous? If so, identify each ambiguous agreement and state why it is ambiguous.",
  cn="诉状中主张的任何协议是否存在歧义？如果是，请指明每一份有歧义的协议，并说明理由。", yn=True, lines=3),
])

SECTIONS = [S1, S2, S3, S4, S6, S7, S8, S9, S10, S11, S12,
            S13, S14, S15, S16, S17, S20, S50]
ALL_NUMBERS = [q["n"] for s in SECTIONS for q in s["qs"]]
BY_NUMBER = {q["n"]: q for s in SECTIONS for q in s["qs"]}
