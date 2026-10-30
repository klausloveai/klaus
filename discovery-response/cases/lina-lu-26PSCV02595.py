# -*- coding: utf-8 -*-
"""Lina Lu v. Arlene Luna (LASC 26PSCV02595) -- Plaintiff's responses to the Luna
defendants' Set One (FROG 51 / RFA A-G / RFP 11), one package per propounding defendant.

Facts trace to: client questionnaire returned 10/15/2026 (WeChat), USC Arcadia ER record
and itemized bill (redacted), BHIPS invoice + treatment plan 9/16/2026, IVHS Animal Bite
Reporting Form 7/9/2026, Azusa PD card + CAD, Amazon Incident Response message 7/11/2026,
CA driver license, L.A. Care card, Intact coverage letter 8/27/2026, Prop 22 claim form.
«[... TO BE CONFIRMED]» = client fact still open (round-2 form).
«[FOR HERNAN ...]» = attorney decision.
"""
import sys, os, copy
sys.path.insert(0, os.path.expanduser("~/.claude/skills/discovery-response/scripts"))
from common import *          # noqa
import pos
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH as A

OUT = os.path.expanduser("~/Downloads/Lina Lu Discovery Responses to Luna Set One (DRAFT)")
os.makedirs(OUT, exist_ok=True)

H = "FOR HERN\u00c1N \u2014 REMOVE BEFORE SERVICE"
def flag(t): return "«[%s] %s»" % (H, t)
def tbc(t=""): return "«[TO BE CONFIRMED%s]»" % (": " + t if t else "")

ATTY = ["Hern\u00e1n S. Sim\u00f3 (SBN 354175)", "LINGTU LAW OFFICE", "Law Office of Shenqi Cai, APC",
        "13191 Crossroads Parkway North, Suite 295", "City of Industry, California 91746",
        "Telephone: (626) 479-2207", "Facsimile: (626) 479-2207",
        "Electronic Mail: hernan.s@lingtulaw.com", "", "Attorneys for Plaintiff", "LINA LU"]
COURT = ["SUPERIOR COURT OF THE STATE OF CALIFORNIA", "COUNTY OF LOS ANGELES"]
LEFT = [("LINA LU,", False, None), ("", False, None), ("Plaintiff,", False, A.CENTER),
        ("", False, None), ("v.", False, A.CENTER), ("", False, None),
        ("ARLENE LUNA; ROSALBA LUNA; AMAZON LOGISTICS, INC.; RICHARD REYES and ZORAIDA TORRES, "
         "as Trustees of the TORRES REYES FAMILY TRUST; and DOES 2 through 25, inclusive,", False, None),
        ("", False, None), ("Defendants.", False, A.CENTER)]

LUNA_ADDR = "152 East Kirkwall Road, Azusa, California 91702"
APD = "Azusa Police Department, 725 North Alameda Avenue, Azusa, California 91702, (626) 812-3200"
USC = "USC Arcadia Hospital, 300 West Huntington Drive, Arcadia, California 91007, (626) 898-8000"
BHIPS = ("Saul Lahijani, M.D., Beverly Hills Institute of Plastic Surgery, 8654 Wilshire Boulevard, "
         "Beverly Hills, California 90211, (310) 550-6886")
IVHS = "Inland Valley Humane Society, 500 Humane Way, Pomona, California 91766, (909) 623-9777"
COUNSEL_CONTACT = "who may be contacted only through Responding Party's counsel of record"
BATES = "«[BATES RANGE TO BE INSERTED]»"


# ======================================================================= FROG
def frog(d):
    """d = 'ARLENE LUNA' or 'ROSALBA LUNA'. Answers are identical in both sets."""
    other = "Rosalba Luna" if d == "ARLENE LUNA" else "Arlene Luna"
    R = []
    def q(n, *paras): R.append((n, list(paras)))

    q("1.1", "Responding Party, LINA LU, with the assistance of her attorneys of record, Hern\u00e1n S. "
             "Sim\u00f3, Lingtu Law Office, Law Office of Shenqi Cai, APC, 13191 Crossroads Parkway North, "
             "Suite 295, City of Industry, California 91746, (626) 479-2207. The responses were translated "
             "for Responding Party by " + tbc("TRANSLATOR NAME") + ", of the same office.")
    q("2.1", ("sub", "(a)\tLina Lu."), ("sub", "(b)\tNone."), ("sub", "(c)\tNot applicable."))
    q("2.2", ("sub", "(a)\tFebruary 20, 1982."),
             ("sub", "(b)\tDaqing, Heilongjiang Province, People's Republic of China."))
    q("2.3", ("sub", "(a)\tCalifornia; license number Y7171029."), ("sub", "(b)\tClass C."),
             ("sub", "(c)\tNovember 28, 2024 (date of issue shown on the current license)."),
             ("sub", "(d)\tNone."))
    q("2.4", "No.")
    q("2.5", ("sub", "(a)\t415 West Duarte Road, Unit 3, Arcadia, California 91007."),
             ("sub", "(b)\t20 Genoa Street, Apartment A, Arcadia, California 91006 (the address shown on "
                     "Responding Party's driver license)."),
             ("sub", "(c)\t415 West Duarte Road: November 1, 2025 to the present. 20 Genoa Street: 2018 to "
                     "October 2025."))
    q("2.6", ("sub", "(a)\tResponding Party is self-employed as an independent contractor delivering packages "
                     "through the Amazon Flex program operated by Amazon Logistics, Inc., 410 Terry Avenue North, Seattle, Washington 98109, represented in this action by Brockman Quayle Bennett, 12481 High Bluff Drive, Suite 301, San Diego, California 92130, (858) 788-3900."),
             ("sub", "(b)\t(1) Amazon Flex delivery partner (independent contractor), package delivery, from "
                     "approximately July 2025 to the present. (2) Uber Eats delivery partner (independent "
                     "contractor), Uber Technologies, Inc., food delivery, for a little over one year before July 2025. "
                     "Responding Party had no other employment since July 2021. "
                     + flag("Client (voice, October 25): Flex since about July 2025, Uber Eats for a year-plus before "
                            "that. Our February 25, 2026 car-crash intake lists her occupation as 'Housewife,' but the "
                            "Vanguard pain management note of June 30, 2026 records 'She is employed. Delivery' and that "
                            "she 'had to take 2 months off work' after the collision. The intake entry is wrong; correct "
                            "it in the PI file before the car-crash demand.")))
    q("2.7", ("sub", "(a)\tDaqing Petroleum School, Daqing, Heilongjiang Province, People's Republic of China."),
             ("sub", "(b)\t1994 to 1997."),
             ("sub", "(c)\tVocational secondary school diploma (China). Responding Party did not attend high "
                     "school in the United States and holds no other degree."))
    q("2.8", "No.")
    q("2.9", "No. Responding Party speaks Mandarin Chinese.")
    q("2.10", "No. Responding Party reads and writes Chinese.")
    q("2.11", "No. Responding Party was not acting as an agent or employee of any PERSON. At the time of the "
              "INCIDENT she was delivering a package to 152 East Kirkwall Road, Azusa, California, as an "
              "independent contractor through the Amazon Flex program operated by Amazon Logistics, Inc.",
          flag("The Prop 22 / occupational-accident framing (independent contractor, not employee) must hold "
               "here: an employee answer would invite a workers' compensation exclusivity defense to the "
               "fourth cause of action against Amazon. Confirm the wording."))
    q("2.12", "No.")
    q("2.13", "No.")
    q("4.1", "Yes. Responding Party identifies the following:",
          ("sub", "1.\t(a) Health insurance (medical expense coverage). (b) L.A. Care Health Plan, L.A. Care Covered "
                  "(Covered California), Silver 94 HMO, 1200 West 7th Street, Los Angeles, California 90017. (c) Lina Lu, "
                  "415 West Duarte Road, Unit 3, Arcadia, California 91007. (d) Member identification "
                  "number 623871067, effective May 1, 2026. (e) Responding Party does not know the limits. "
                  "(f) Responding Party is not aware of any reservation of rights. (g) Not applicable. "
                  "(h) L.A. Care Health Plan."),
          ("sub", "2.\t(a) Occupational accident coverage, which pays accident medical expense and other scheduled "
                  "benefits to independent contractors delivering for Amazon Logistics, Inc. (b) Homeland "
                  "Insurance Company of New York, administered by Intact Insurance, Occupational Accident "
                  "Claims, 188 Inverness Drive West, Suite 600, Englewood, Colorado 80112. (c) Amazon "
                  "Logistics, Inc., 410 Terry Avenue North, Seattle, Washington 98109, represented in this action by Brockman Quayle Bennett, 12481 High Bluff Drive, Suite 301, San Diego, California 92130, (858) 788-3900. (d) Policy number 216-002-630 "
                  "(claim number 0AB504616). (e) Responding Party does not know the limits. (f) By letter "
                  "dated August 27, 2026, Intact Insurance stated that Responding Party is potentially "
                  "covered, subject to the terms and conditions of the policy, and that the policy is "
                  "secondary to other insurance. (g) Not applicable. (h) Amazon Logistics, Inc. and Homeland "
                  "Insurance Company of New York."),
          "Responding Party has not received Medicare or Medi-Cal benefits since the INCIDENT "
          + ".",
          flag("Old Republic (Reserv, claim 26ATCA842575927) business auto policy: listed nowhere above "
               "because it denied MedPay on August 21, 2026 and you closed that line on September 2. "
               "4.1 asks for policies under which she 'might be insured.' Add it, or leave it out?"))
    q("6.1", "Yes.")
    q("6.2", "Responding Party sustained an open dog-bite wound to the outer (lateral) aspect of her left ankle, "
             "with bleeding, swelling and a stinging sensation, diagnosed at USC Arcadia Hospital as an open "
             "bite of the left ankle, initial encounter (S91.052A). The wound has healed with a scar on the "
             "outer left ankle measuring approximately 2.5 centimeters by 1 centimeter, which Saul Lahijani, "
             "M.D. described on September 16, 2026 as accompanied by fat necrosis. Responding Party also "
             "suffers emotional distress: fear and shortness of breath when she sees a dog, disturbed sleep "
             "and nightmares in which she wakes up suddenly, and distress about the appearance of the scar.")
    q("6.3", "Yes.",
          ("sub", "(a)\tThe scar on her left ankle; " + tbc("CURRENT PHYSICAL ANKLE SYMPTOMS (ACHING, NUMBNESS, PAIN WHEN WALKING)")
                  + "; fear and shortness of breath when she sees a dog; disturbed sleep and nightmares; "
                  "reluctance to wear clothing or shoes that expose her ankles."),
          ("sub", "(b)\tResponding Party describes each of these complaints as continuing without improvement "
                  "since the INCIDENT " + tbc("SAME / BETTER / WORSE, PER COMPLAINT") + "."),
          ("sub", "(c)\tThe scar is constant. The fear and shortness of breath occur whenever she encounters a "
                  "dog or a situation similar to the INCIDENT. The sleep disturbance occurs nearly every night."))
    q("6.4", "Yes.",
          ("sub", "1.\t(a) " + USC + ". (b) Emergency department examination and treatment: wound irrigation, "
                  "tetanus, diphtheria and pertussis (Tdap) vaccination, and a prescription for oral "
                  "antibiotics. (c) July 9, 2026. (d) $1,898.00 in hospital charges ($1,644.00 emergency "
                  "service; $254.00 Tdap vaccine). The hospital's bill states that the emergency physicians "
                  "bill separately; Responding Party has not received a separate physician bill "
                  + tbc() + "."),
          ("sub", "2.\t(a) Thomas Yu, M.D., Allied Pacific IPA, 1448 South San Gabriel Boulevard, San Gabriel, California 91776, (626) 288-0300. "
                  "(b) Office visit for difficulty sleeping since the INCIDENT; prescription of a sleep aid. (c) July 28, 2026. "
                  "(d) " + tbc("CHARGES OR COPAY") + "."),
          ("sub", "3.\t(a) " + BHIPS + ". (b) Plastic surgery consultation and evaluation of the left ankle scar, "
                  "with photographs and chart review. (c) September 16, 2026. (d) $3,500.00."),
          flag("Lahijani's invoice and treatment plan are addressed to Lingtu Law Firm and the visit "
               "produced a medical-legal report. List him here as a health care provider (and produce in RFP 4, "
               "10, 11), or treat him as a retained consultant under Code of Civil Procedure section 2018.030 "
               "and the 6.4 exclusion for experts? The same choice drives 6.7 and RFP 4, 10 and 11."))
    q("6.5", "Yes.",
          ("sub", "(a)\tAmoxicillin-clavulanate 875 milligrams / 125 milligrams oral tablets, one tablet twice a "
                  "day, quantity 14; Tdap vaccine administered at the hospital; and a sleep aid prescribed by Thomas Yu, M.D. "
                  "on July 28, 2026 " + tbc("NAME OF SLEEP MEDICATION, DATES TAKEN, COST") + "."),
          ("sub", "(b)\tElvis Santillan, PA, USC Arcadia Hospital, " + USC.split(", ", 1)[1] + " (antibiotic); Thomas Yu, "
                  "M.D. (sleep aid)."),
          ("sub", "(c)\tAntibiotic: July 9, 2026, for seven days. Sleep aid: from July 28, 2026 " + tbc("END DATE") + "."),
          ("sub", "(d)\t$3.00 (Sunny Bay Pharmacy, July 9, 2026)."))
    q("6.6", "No.")
    q("6.7", "Yes.",
          ("sub", "(a)\t" + BHIPS + "."),
          ("sub", "(b)\tThe scar and fat necrosis of the outer left ankle."),
          ("sub", "(c)\tSteroid therapy before surgery; stage one fat grafting; stage two excision of the scar, "
                  "tissue advancement and reapproximation of the wound edges; and a non-surgical plan of up to "
                  "twelve laser or microneedling treatments."),
          ("sub", "(d)\tAs stated in the treatment plan dated September 16, 2026."),
          ("sub", "(e)\tSteroid therapy $3,500.00; stage one $36,500.00 (including $6,500.00 operating room and "
                  "$5,000.00 anesthesia); stage two $72,000.00 (including $8,500.00 operating room and $8,000.00 "
                  "anesthesia); subtotal $112,000.00. Non-surgical treatments $1,250.00 to $2,500.00 each, up to "
                  "twelve treatments, not included in the subtotal."),
          flag("The client wrote on October 15 that she will NOT have the surgery. The answer above is still "
               "true (6.7 asks what was advised, not what she elected). Whether to add a sentence about her "
               "election, and what future medical damages to claim, is yours; see also the Lahijani note at 6.4."))
    q("7.1", "No.")
    q("7.2", "Not applicable.")
    q("7.3", "Not applicable.")
    q("8.1", "No.",
          flag("Client: no days off and no lost earnings of her own. Updated October 28: her husband, also an "
               "Uber driver earning about $200 to $300 a day, rode along with her for about two weeks after the "
               "bite, after which she worked alone again. That is his loss, not hers, so 8.1 can stay 'No'; "
               "whether to claim the value of his help is the 9.1 decision. 'No' here waives her own lost "
               "earnings and earning capacity (8.2 through 8.8 go unanswered). Confirm 'No.'"))
    for n in range(2, 9):
        q("8.%d" % n, "Not applicable.")
    q("9.1", "No, other than the general damages for pain, suffering and emotional distress described in "
             "the responses to interrogatories 6.2 and 6.3.",
          flag("Client (voice, October 25, 22:47): no other out-of-pocket costs beyond the $50 emergency "
               "copayment and the $3 pharmacy charge, which match the receipts in 6.5 and 9.2. Her husband rode "
               "along for about two weeks at a cost to him of about $200 to $300 a day (14 days x $200 = $2,800; "
               "14 days x $300 = $4,200; we have no record of the actual days he lost). Claim it here as the "
               "reasonable value of his assistance, or leave it out? If claimed, we need proof of his Uber "
               "earnings. She says he has no pay stubs (paid only when he drives); his Uber earnings history would be the "
               "proof."))
    q("9.2", "Yes. The itemized bill of USC Arcadia Hospital; Responding Party's receipt for her $50.00 emergency "
             "copayment to USC Arcadia Hospital on July 9, 2026; the Sunny Bay Pharmacy receipt for $3.00 dated "
             "July 9, 2026; the invoice and treatment plan of Beverly Hills Institute of Plastic Surgery dated "
             "September 16, 2026; and the lien statement of Katch, on behalf of L.A. Care Health Plan, dated "
             "August 21, 2026. Responding Party's counsel has each document.")
    q("10.1", "No.")
    q("10.2", "Yes. Before the INCIDENT Responding Party was injured in a motor vehicle collision on February 25, 2026 "
              "(see the response to interrogatory 11.1) and was treated for neck and back pain, a contusion of the left "
              "hand, pain in the right arm, headaches, dizziness, nausea, fear of driving and recurring nightmares.",
          ("sub", "(a)\tOn July 9, 2026 Responding Party still had intermittent low back pain, right hip pain, and "
                  "occasional neck stiffness and right-arm numbness, for which she was under pain management care; "
                  "her neck pain and right elbow pain had resolved by about late June 2026. Her treatment records of "
                  "June 30, July 3 and July 14, 2026 record no headaches, dizziness, nausea, fear of driving or sleep "
                  "complaints."),
          ("sub", "(b)\tSince the INCIDENT Responding Party has had nightmares and does not sleep soundly."),
          ("sub", "(c)\tPomona Valley Hospital Medical Center, 1798 North Garey Avenue, Pomona, California 91767, "
                  "(909) 865-9500, emergency department, February 25, 2026; Care Ambulance Service, Inc., February 25, "
                  "2026; Prestige Integrative Health Center, 5553 Rosemead Boulevard, Temple City, California 91780, "
                  "(626) 286-5800, chiropractic, February 26, 2026 to July 3, 2026; Sun Imaging, Inc., 7715 Garvey "
                  "Avenue, Rosemead, California 91770, (626) 280-0431, magnetic resonance imaging, April 28, 2026; "
                  "Vanguard Interventional Pain Specialists, 707 South Garfield Avenue, Suite 304, Alhambra, California "
                  "91801, (626) 281-7246, pain management, June 30, 2026 and July 14, 2026."),
          flag("Client answered 10.2 'no' on October 15, but our own PI file (Lina Lu / Zesen Wang, DOL February 25, "
               "2026) shows she was still in treatment when the dog bit her (chiropractic to July 3, pain management "
               "June 30 and July 14) and that the car-crash intake lists fear of driving and recurring nightmares. "
               "The nightmares overlap the emotional distress claimed in 6.2 and 6.3. The defense will find this "
               "through the L.A. Care records. Draft discloses it. Note also: the July 28, 2026 PCP visit was for sleep "
               "problems (client voice, October 25), the same complaint as the pre-existing nightmares. Client "
               "(voice, October 25, 22:48): 'after that car accident I had no symptoms' and the nightmares began after "
               "the bite. (a) is answered from the car-crash records instead (Drive, Lina Lu/Zesen Wang 2/25/2026, "
               "folder 4): Prestige chiropractic discharged her July 3 as 'better' with intermittent back tightness, "
               "neck stiffness and right-arm numbness, referred to pain management; Vanguard June 30: low back 6/10 "
               "daily, elbow and neck intermittent; Vanguard July 14 (five days after the bite): neck and elbow pain "
               "resolved, low back episodes every two weeks, right hip 6/10, naproxen, epidural or PRP if worse. "
               "Sleep: the only record is the February 26 chiropractic intake ('driving-related anxiety and "
               "fragmented sleep patterns due to acute pain'); nothing after that. That helps 6.2/6.3. Against us: "
               "the July 14 note, five days after the bite, says nothing about the ankle or sleep and records "
               "'patient appears normal.'"))
    q("10.3", "No.")
    q("11.1", "Yes.",
          ("sub", "1.\tMotor vehicle collision: (a) February 25, 2026, approximately 7:51 a.m., Golden Springs Drive at "
                  "Willow Green Road, Diamond Bar, California. (b) Isis Sabrea Curiel, 24120 Willow Creek Road, Diamond "
                  "Bar, California 91765, insured by State Farm (claim number 7597D933B); and Responding Party's own "
                  "insurer, Tesla Insurance (claim number CL-81-93JHZT-4). (c) None; no action has been filed. "
                  "(d) Lingtu Law Office, Law Office of Shenqi Cai, APC, 13191 Crossroads Parkway North, Suite 295, "
                  "City of Industry, California 91746, (626) 479-2207. (e) Neck and back pain, contusion of the left "
                  "hand, pain in the right arm, headaches, dizziness, nausea, fear of driving and recurring nightmares. "
                  "(f) Pending. (g) Not applicable."),
          ("sub", "2.\tOccupational accident claim: (a) July 9, 2026, 152 East Kirkwall Road, Azusa, California. "
                  "(b) Homeland Insurance Company of New York, through Intact Insurance, Occupational Accident "
                  "Claims, 188 Inverness Drive West, Suite 600, Englewood, Colorado 80112. (c) None. "
                  "(d) Hern\u00e1n S. Sim\u00f3, Lingtu Law Office. (e) Claim number 0AB504616; open."),
          ("sub", "3.\tClaim to USAA under the policy insuring Richard Reyes: (a) same INCIDENT. (b) USAA, "
                  "claim number 015775868-810. (c) This action. (d) Hern\u00e1n S. Sim\u00f3. (e) Open."),
          flag("11.1 reads 'except for this action.' Claims 2 and 3 above arise from the same INCIDENT. Disclose "
               "them (draft), or answer 'No' as to other incidents only? Old Republic / Reserv (claim "
               "26ATCA842575927) is omitted for the reason given at 4.1."))
    q("11.2", "No. The occupational accident claim identified in response to interrogatory 11.1 is not a claim "
              "for workers' compensation benefits.")
    q("12.1",
          ("sub", "(a)\tResponding Party; a young female, whose name is unknown to Responding Party, who was at the "
                  "residence at 152 East Kirkwall Road, Azusa, California 91702, at the time of the INCIDENT and "
                  "carried the dog into the house afterward; the young female's mother and brother, whose names are unknown to "
                  "Responding Party, who came to the residence after the bite and before the police arrived; Fuguo Wang, "
                  "Responding Party's husband, " + COUNSEL_CONTACT + ", who arrived as the police arrived; and "
                  "Defendants Arlene Luna and Rosalba Luna, " + LUNA_ADDR + ", (626) 224-5809, to the extent either "
                  "was present."),
          ("sub", "(b)\tResponding Party, the young female, and the young female's mother and brother, described above."),
          ("sub", "(c)\tOfficer Cristian Castro, badge number 1224, and Officer Torres, badge number 1234, " + APD
                  + "; the Azusa Police Department dispatcher who received Responding Party's 911 call; and Fei Li, a friend of "
                  "Responding Party, (626) 262-3246, who interpreted by telephone between Responding Party and the young "
                  "female's mother and brother."),
          ("sub", "(d)\tEach person named above; Fuguo Wang, Responding Party's husband, " + COUNSEL_CONTACT
                  + "; Fei Li, identified on the Animal Bite Reporting Form as the person who reported the bite, "
                  "a friend of Responding Party, (626) 262-3246 " + tbc("ADDRESS")
                  + "; M. Valdez, number 14, " + IVHS + ", who submitted the Animal Bite Reporting Form; "
                  "the agent of Amazon's Incident Response Team who signed as Mountassir, Amazon Logistics, Inc.; "
                  "and Richard Reyes and Zoraida Torres, as Trustees of the Torres Reyes Family Trust, through "
                  "their counsel, Wingert Grebing Brubaker & Walshok LLP."))
    q("12.2", O_WP() + " " + SWO1 + " No.")
    q("12.3", O_WP() + " " + SWO1 + " No.")
    q("12.4", "Yes.",
          ("sub", "(a)\tEight images: three photographs of the premises, four photographs of the injury, and one "
                  "screenshot of the Amazon Flex delivery record."),
          ("sub", "(b)\tThe house at 152 East Kirkwall Road; the wrought-iron front gate; the street in front of the "
                  "house with an Azusa Police Department vehicle; Responding Party's left ankle wound and scar; and the "
                  "Amazon Flex record showing package 5662, addressed to Arlene Luna, delivered to the front door or "
                  "porch at 8:39 a.m."),
          ("sub", "(c)\tThe premises photographs and the delivery record on July 9, 2026; the injury photographs on "
                  "July 9, 2026 and on later dates through September 8, 2026."),
          ("sub", "(d)\tResponding Party, " + COUNSEL_CONTACT + ". Saul Lahijani, M.D. also took photographs on "
                  "September 16, 2026."),
          ("sub", "(e)\tResponding Party and her counsel; Amazon Logistics, Inc. holds its own delivery record and any "
                  "proof-of-delivery photograph; Beverly Hills Institute of Plastic Surgery holds its photographs. The "
                  "proof-of-delivery photograph was taken and uploaded through the Amazon Flex application and is not "
                  "saved on Responding Party's telephone."),
          flag("8:39 a.m. appears here because the delivery record is a photograph concerning the INCIDENT. It fixes "
               "the time in a verified answer. The client confirmed on October 29 that the bite came right after the photo, "
               "so 8:39 is consistent with her account and with RFA C. Keep, or describe the record "
               "without the time?"))
    q("12.5", "Yes. Responding Party drew a diagram of the premises showing the house, the garage, the walkway, "
              "the lawn, the front gate and the direction from which the dog came, on August 13, 2026. Responding Party's counsel has a copy.")
    q("12.6", "Yes.",
          ("sub", "1.\t(a) Azusa Police Department dispatch; Officers Cristian Castro, number 1224, and Torres, "
                  "number 1234, responded. (b) July 9, 2026; computer-aided dispatch call detail report, "
                  "incident number 26-23363. The Azusa Police Department stated in its response to public "
                  "records request PDRR2026-67 dated October 1, 2026 that no written incident report was "
                  "prepared. (c) Azusa Police Department. (d) " + APD + "."),
          ("sub", "2.\t(a) M. Valdez, number 14, " + IVHS + ". (b) July 9, 2026; County of Los Angeles "
                  "Department of Public Health, Veterinary Public Health Program, Animal Bite Reporting Form "
                  "(activity 4432). (c) County of Los Angeles Department of Public Health, Veterinary Public "
                  "Health Program, (213) 288-7060. (d) Inland Valley Humane Society; the Department of Public "
                  "Health; Responding Party's counsel has a copy."),
          ("sub", "3.\t(a) Responding Party, through the Amazon Flex application. (b) July 2026; incident "
                  "report to Amazon on or before July 11, 2026, Amazon claim number FLX2026153035. (c) Amazon Logistics, Inc. "
                  "(d) Amazon Logistics, Inc."))
    q("12.7", "No.")
    q("13.2", "No. Neither Responding Party nor anyone acting on her behalf has conducted surveillance of any "
              "individual involved in the INCIDENT or any party to this action.")
    q("14.1", "Yes. Defendants Arlene Luna and Rosalba Luna, " + LUNA_ADDR + ", (626) 224-5809: "
              + flag("Name the statute(s) or ordinance(s). Candidates to verify against the text before citing: "
                     "the Azusa Municipal Code dog-at-large / leash provision; the dog was unlicensed per the bite "
                     "report. Civil Code section 3342 imposes liability; it is not a violation."))
    q("14.2", "No, to Responding Party's knowledge. The Azusa Police Department has stated that no written report "
              "was prepared, and the City of Azusa stated on October 16, 2026, in response to public records "
              "request CPR2026-348, that it holds no animal control records for 152 East Kirkwall Road since "
              "January 1, 2021.")
    q("17.1", "Responding Party's responses to Requests for Admission A, B, C, D, E, F and G are not unqualified "
              "admissions. For each:")
    R[-1][1].extend(rfa_171(d))
    return R


# ======================================================================= RFA
def rfa_items(d):
    who = "Arlene Luna" if d == "ARLENE LUNA" else "Rosalba Luna"
    return [
        ("A", "%s does not own the dog that you allege bit you on or about July 9, 2026" % who),
        ("B", "%s was not physically present on or about July 9, 2026 when you allege that the dog bit you "
              "at 152 East Kirkwall Road, Azusa, California 91702" % who),
        ("C", "You did not seek medical treatment for the dog bite you alleged occurred on July 9, 2026 for "
              "more than one hour after the time of the incident"),
        ("D", "You were able to walk away from the premises immediately after the dog allegedly bit you on "
              "July 9, 2026"),
        ("E", "The dog that you allege bit you had never bitten anyone prior to July 9, 2026."),
        ("F", "The person that was physically present when you made the delivery on July 9, 2026 told you that "
              "a dog was loose and to immediately leave the premises"),
        ("G", "Instead of leaving as the person warned you that a dog was loose, you decided to take a picture "
              "of the package you delivered on July 9, 2026"),
    ]

INQ = ("After a reasonable inquiry concerning the matter, the information known or readily obtainable by "
       "Responding Party is insufficient to enable her to admit or deny this request.")

CALL = "Client (phone call with Klaus, October 29): she was bitten just after she put the package down and took the delivery photograph. She went back to her car, saw the wound bleeding, FIRST CONTACTED OUR OFFICE (Klaus), then called 911, and waited in the car without treating the wound. While she waited, the girl's mother and brother came home and spoke to her in English; she called her friend Li Fei, who interpreted by phone (per Li Fei, the family said they have a dog and that she did not understand English). The officers spoke with her through a phone, said it was not a criminal matter, gave her a card, told her she could leave, and went to talk to the family. Her husband arrived as the officers did and rinsed the wound with water from the car's first-aid kit. She then drove her husband's car, picked up Li Fei, and went to USC Arcadia Hospital; her husband drove her car away. "

def rfa_resp(d):
    arl = d == "ARLENE LUNA"
    who = "Arlene Luna" if arl else "Rosalba Luna"
    a = ([INQ + " Responding Party has no personal knowledge of who owns the dog. Her inquiry included the "
          "Animal Bite Reporting Form completed on July 9, 2026 and submitted by the Inland Valley Humane "
          "Society, which identifies the owner as Rosalba Luna of 152 East Kirkwall Road; Amazon's delivery "
          "record, which identifies Arlene Luna as the addressee of the package; and the message of Amazon's "
          "Incident Response Team dated July 11, 2026, stating that it contacted the customer and obtained the "
          "dog's rabies vaccination information from the customer. Responding Party has served "
          "interrogatories and requests for admission on Arlene Luna concerning the ownership and keeping of "
          "the dog, to which responses are not yet due.",
          flag("Alternative: deny on information and belief (Arlene as keeper / harborer: package addressee who "
               "supplied the vaccination record to Amazon). A denial later disproved risks costs of proof under "
               "Code of Civil Procedure section 2033.420.")]
         if arl else
         ["Deny."])
    b = ["Responding Party does not know %s by sight. Admit that, when the dog bit her, the only person "
         "Responding Party saw at the residence was a girl who appeared to be about 13 to 15 years old, standing at "
         "the side door of the garage, and that no adult was nearby. Except as expressly admitted, Responding Party "
         "is unable to admit or deny this request: she does not know whether %s was inside the house. "
         % (who, who) + INQ,
         flag("Client (October 29 call): the girl was about 13 to 15, at the garage side door, no adult nearby; "
              "the girl's mother and brother came home only after the bite. Draft is a partial admission. Still "
              "open: the CAD (her 911 report) and her Prop 22 claim form say 'the dog owner' was on the porch; she "
              "does not remember who filled in the claim form. Ages of Arlene and Rosalba are not in our file; if "
              "either could be the 13-to-15-year-old, this answer must change.")]
    c = ["Admit that the records of USC Arcadia Hospital reflect her arrival at the emergency department at "
         "10:43 a.m. on July 9, 2026, more than one hour after the dog bit her. Except as expressly admitted, "
         "Responding Party denies this request. The dog bit her at about 8:39 a.m., immediately after she put the "
         "package down and photographed it. She returned to her car, found the wound bleeding, telephoned 911, and "
         "remained at the scene until Azusa Police Department officers arrived, spoke with her and told her she could "
         "leave. Her husband, who arrived as the officers did, rinsed the wound with clean water from a first-aid kit. "
         "She then drove, picking up a friend on the way, to the USC Arcadia Hospital emergency department.",
         flag(CALL + "The gap between the bite (about 8:39) and the 911 call (9:34) is now mostly explained, but "
              "part of it is her call to our office. The draft does not mention that call. Disclose that she first "
              "contacted counsel (fact of contact, not content), or leave it out? Klaus: check your own WeChat/phone "
              "log for the time of her July 9 contact before Hernan decides. Note also: Li Fei went with her to the "
              "emergency room, which may be where the triage note's 'friends dog' came from.")]
    dd = ["Admit that Responding Party was able to walk, with difficulty and with pain, numbness and bleeding "
          "from her left ankle, out of the front gate after the young female carried the dog into the house. "
          "Except as expressly admitted, Responding Party denies this request. She did not walk away from the premises. "
          "She went to her car in front of the residence, telephoned 911, and remained there until Azusa Police "
          "Department officers arrived, spoke with her and told her she could leave.",
          flag("Resolved by the October 29 call: she stayed in her car at the residence until the officers released "
               "her; the round-1 line 'after the bite I drove away by myself' refers to leaving for the hospital after "
               "the police. Note for Hernan only: her husband drove her car (with the Flex packages, if any remained) "
               "away from the scene. Not asked further.")]
    e = [INQ + " Responding Party has no personal knowledge of the dog's history. Her inquiry, which is "
         "continuing, includes: (1) a public records request to the Azusa Police Department (PDRR2026-67), "
         "which responded on October 1, 2026 that no written report was prepared for this INCIDENT; (2) a "
         "public records request to the City of Azusa (CPR2026-348), which responded on October 16, 2026 that it "
         "holds no animal control records for 152 East Kirkwall Road since January 1, 2021, and that animal "
         "control services have been provided by the Inland Valley Humane Society since July 1, 2026; (3) public "
         "records requests to the County of Los Angeles Department of Animal Care and Control and Department of "
         "Public Health dated August 13, 2026, to which no records have been produced; and (4) interrogatories "
         "and requests for admission served on the Luna defendants concerning the dog's history, to which "
         "responses are not yet due."]
    f = ["Deny. Responding Party had taken one step inside the front gate. The young female was at the side "
         "door of the garage, about two to three steps away, and may have said something in a very low voice; Responding "
         "Party did not hear or understand what was said. Responding Party asked whether she could leave the "
         "package there, and the young female answered \"OK.\" No one told Responding Party that a dog was loose "
         "or that she should leave the premises.",
         flag("Client (voice, October 25, 22:44): the girl at the garage side door said something very quietly "
              "that she did not catch; she asked 'can I leave it here?', the girl said 'OK', she put the package "
              "down and was bitten. On October 29 she put the girl two to three steps away and said the dog came "
              "around the right side of the house (the garage is on the left), matching her August 13 diagram; her "
              "round-1 answer said 'left side,' which looks like a slip. At two to three steps the defense will ask "
              "how she could not hear; the answer is the language. Not a clean 'no one said anything.' The draft "
              "discloses the low-voice remark so the deposition cannot surprise us; a bare 'Deny' is the "
              "alternative. Same choice for G and 17.1 F. Added October 29: after the bite the girl's mother and brother "
              "came home and, through Li Fei interpreting by phone, said the house has a dog and that the client did "
              "not understand English. Expect the Lunas to say the girl warned her in English; the draft's 'did not "
              "hear or understand' fits that. Li Fei is now a witness to the family's statements (12.1(c)).")]
    g = ["Deny."]
    return {"A": a, "B": b, "C": c, "D": dd, "E": e, "F": f, "G": g}


def rfa_171(d):
    who = "Arlene Luna" if d == "ARLENE LUNA" else "Rosalba Luna"
    LUNAS = "Arlene Luna and Rosalba Luna, " + LUNA_ADDR + ", (626) 224-5809"
    ME = "Responding Party, " + COUNSEL_CONTACT
    out = []
    def blk(letter, facts, persons, docs):
        out.append(("sub", "Request for Admission %s: (a) %s. (b) %s (c) %s. (d) %s." % (letter, letter, facts, persons, docs)))
    if d == "ARLENE LUNA":
        blk("A", "Responding Party has no personal knowledge of ownership. The Animal Bite Reporting Form identifies "
                 "Rosalba Luna as the owner; Amazon's delivery record identifies Arlene Luna as the addressee; "
                 "Amazon's Incident Response Team obtained the dog's vaccination information from the customer.",
            LUNAS + "; M. Valdez, number 14, " + IVHS + "; Amazon Logistics, Inc.",
            "Animal Bite Reporting Form dated July 9, 2026 (Inland Valley Humane Society; Responding Party's "
            "counsel has a copy); Amazon proof-of-delivery record (Amazon Logistics, Inc.); message of Amazon's "
            "Incident Response Team dated July 11, 2026 (Responding Party's counsel)")
    else:
        blk("A", "The Animal Bite Reporting Form completed on July 9, 2026 identifies Rosalba Luna, 152 East "
                 "Kirkwall Road, (626) 224-5809, as the owner of the dog, a male Chihuahua named Melo.",
            LUNAS + "; M. Valdez, number 14, " + IVHS,
            "Animal Bite Reporting Form dated July 9, 2026 (Inland Valley Humane Society; Responding Party's "
            "counsel has a copy)")
    blk("B", "Responding Party does not know %s by sight. When the dog bit her, the only person she saw at the "
             "residence was a girl about 13 to 15 years old at the side door of the garage; no adult was nearby. The "
             "girl's mother and brother arrived after the bite." % who,
        ME + "; " + LUNAS, "None known to Responding Party at this time")
    blk("C", "The dog bit Responding Party at about 8:39 a.m., immediately after she photographed the delivered "
             "package. She returned to her car, telephoned 911, and waited at the scene until the Azusa Police "
             "Department officers released her; her husband rinsed the wound with clean water; she then drove, "
             "picking up a friend, to the USC Arcadia Hospital emergency department, arriving at 10:43 a.m.",
        ME + "; Officers Castro and Torres, " + APD + "; " + USC,
        "Azusa Police Department call detail report, incident 26-23363 (Azusa Police Department; Responding "
        "Party's counsel has a copy); USC Arcadia Hospital emergency department record of July 9, 2026 (USC "
        "Arcadia Hospital; Responding Party's counsel)")
    blk("D", "Responding Party walked out of the front gate with difficulty, pain, numbness and bleeding after the "
             "dog was carried inside, went to her car in front of the residence, telephoned 911, and remained there until the "
             "officers spoke with her and told her she could leave.",
        ME + "; Officers Castro and Torres, " + APD + "; Fuguo Wang, Responding Party's husband, " + COUNSEL_CONTACT
        + "; Fei Li, (626) 262-3246",
        "Azusa Police Department call detail report, incident 26-23363")
    blk("E", "See the response to Request for Admission E, which sets out the inquiry made.",
        "Azusa Police Department, " + APD.split(", ", 1)[1] + "; City of Azusa; " + IVHS
        + "; County of Los Angeles Department of Animal Care and Control; County of Los Angeles Department of "
        "Public Health; " + LUNAS,
        "Azusa Police Department responses to request PDRR2026-67; City of Azusa response to request "
        "CPR2026-348 dated October 16, 2026; Responding Party's requests to the County dated August 13, 2026 and "
        "follow-up letters dated October 20, 2026 (Responding Party's counsel has each)")
    blk("F", "No one told Responding Party before the bite that a dog was loose or that she should leave. As she "
             "stepped inside the gate the young female may have said something in a low voice, which Responding "
             "Party did not hear or understand. The young "
             "female agreed that the package could be left at the door; after the bite she said \"sorry\" and "
             "carried the dog into the house.",
        ME + "; the young female described in response to interrogatory 12.1",
        "None known to Responding Party at this time")
    blk("G", "No one warned Responding Party that a dog was loose. She photographed the delivered package because "
             "the Amazon Flex delivery process requires a proof-of-delivery photograph, and she took it before "
             "the dog bit her.",
        ME + "; Amazon Logistics, Inc.",
        "Amazon Flex proof-of-delivery record for package 5662 (Amazon Logistics, Inc.; Responding Party's "
        "counsel has a screenshot); " + tbc("AMAZON FLEX PHOTO-ON-DELIVERY POLICY DOCUMENT"))
    return out


# ======================================================================= RFP
RFP = [
    ("1", "Your medical records from Arcadia USC Hospital from your hospital visit on July 9, 2026."),
    ("2", "Itemized statement of hospital services you incurred at Arcadia USC Hospital on July 9, 2026"),
    ("3", "Any explanation of benefits from any insurance company or other third party that covered any portion "
          "of the hospital services you received at Arcadia USC Hospital on July 9, 2026."),
    ("4", "Itemized statement from any other medical provider that you allege was incurred by you as a result of "
          "the dog bit you allege you sustained on July 9, 2026."),
    ("5", "Any photograph or other form of reproduction that shows any injury that you alleged you incurred on "
          "July 9, 2026"),
    ("6", "Any contract of employment whether as a statutory employee or independent contractor with Amazon "
          "Logistics, Inc that was in force on July 9, 2026."),
    ("7", "All statement of earnings whether as a statutory employee or independent contractor with Amazon "
          "Logistics, Inc between January 1, 2025 and the date of this notice."),
    ("8", "Any written document that shows the amount of compensation you received for making the delivery to "
          "152 East Kirkwall Road, Azusa, California 91702 on July 9, 2026."),
    ("9", "Any written document that shows any other delivery you were scheduled to make on July 9, 2026 on behalf "
          "of Amazon Logistics, Inc or any other third party."),
    ("10", "Any written document that shows any monetary damages you allege you sustained from the dog bite you "
           "alleged you incurred on July 9, 2026."),
    ("11", "Any written document that shows any future damages you might incur that is related to the dog bite "
           "you allege that occurred on July 9, 2026"),
]
REDACT = ("Responding Party has redacted only her Social Security number and driver license number from the "
          "hospital's documents. " + O_PRIVACY("request") + " " + NO_WITHHOLD + " Only those two identifiers are redacted.")
UNABLE_NOW = ("Responding Party is unable to comply with this request in part because no responsive document is "
              "presently in her possession, custody or control; she believes %s has it. Responding Party has "
              "conducted a diligent search and a reasonable inquiry and will produce any responsive document she "
              "obtains.")

def rfp_resp():
    return {
        "1": [COMPLY + " " + BATES + ".", REDACT],
        "2": [COMPLY + " " + BATES + ".", REDACT],
        "3": ["Responding Party will comply with this request in part by producing the lien statement of Katch, on "
              "behalf of L.A. Care Health Plan, dated August 21, 2026 " + BATES + ". " + UNABLE_NOW % "L.A. Care "
              "Health Plan" + " " + tbc("CLIENT TO SEND ANY L.A. CARE EXPLANATION OF BENEFITS")],
        "4": [COMPLY + " Responding Party produces the invoice of Beverly Hills Institute of Plastic Surgery dated "
              "September 16, 2026, her receipt for the $50.00 copayment to USC Arcadia Hospital, and the Sunny Bay "
              "Pharmacy receipt dated July 9, 2026 " + BATES + ". " + tbc("THOMAS YU, M.D. STATEMENT FOR JULY 28, 2026"),
              flag("Lahijani invoice: produce, or withhold as consultant work product (see FROG 6.4)?")],
        "5": [COMPLY + " " + BATES + ". " + tbc("CLIENT'S ORIGINAL PHOTOGRAPH FILES WITH DATES")],
        "6": ["Responding Party was not an employee of Amazon Logistics, Inc. She will comply with this request by "
              "producing the Amazon Flex independent contractor terms in force on July 9, 2026 " + BATES + ". "
              + tbc("CLIENT TO DOWNLOAD THE AMAZON FLEX INDEPENDENT CONTRACTOR TERMS OF SERVICE")],
        "7": [O_PRIVACY("request") + " Responding Party does not claim lost earnings or loss of earning capacity "
              "in this action (see her response to Form Interrogatory 8.1), and her earnings from January 1, 2025 "
              "forward bear on no issue in the case. On the basis of this objection Responding Party is "
              "withholding her Amazon Flex earnings statements from January 1, 2025 to October 2, 2026, which "
              "are held by Amazon Logistics, Inc. and in the Amazon Flex application.",
              flag("Object and withhold (draft), or produce? If 8.1 changes to 'Yes,' this objection fails.")],
        "8": ["Responding Party is unable to comply with this request because no document showing compensation "
              "for the single delivery to 152 East Kirkwall Road has ever existed: the Amazon Flex program pays a "
              "fixed amount for a block of hours, not per package or per delivery. Responding Party has conducted a "
              "diligent search and a reasonable inquiry. She will produce the Amazon Flex record of her pay for the "
              "July 9, 2026 block " + tbc("CLIENT TO SEND SCREENSHOT OF JULY 9 BLOCK PAY") + ".",
              flag("Producing the block-pay screenshot is voluntary (it is not the document requested). Produce it, "
                   "or stop at the inability statement? Note RFP 7: if we object and withhold her Flex earnings "
                   "there, producing one block's pay here narrows that objection.")],
        "9": [tbc("JULY 9, 2026 ITINERARY FROM THE FLEX APP"),
              flag("The July 9 route will show the time of each stop and whether she kept delivering after 8:39 "
                   "a.m. Review it before deciding how to answer; it decides the bite-time question as well.")],
        "10": [COMPLY + " Responding Party produces the documents identified in her response to Form "
               "Interrogatory 9.2 " + BATES + "."],
        "11": [COMPLY + " Responding Party produces the treatment plan of Beverly Hills Institute of Plastic "
               "Surgery dated September 16, 2026 " + BATES + ".",
               flag("Same Lahijani decision as RFP 4.")],
    }

PROD_FLAG = flag("Production: the requests designate November 13, 2026 at 10:00 a.m. at the office of Franklin J. "
                 "Love, who wrote on October 14 that he is not attorney of record. Draft below: serve copies by mail "
                 "on Requesting Party at the address of record with these responses. Confirm.")
PROD_LINE = ("Responding Party will produce the documents identified below by serving copies on Requesting Party "
             "by mail at " + LUNA_ADDR + ", concurrently with these responses.")


# ======================================================================= build
TITLES = {
    "frog": ("FORM INTERROGATORIES \u2014 GENERAL", "RESPONSES TO FORM INTERROGATORIES", "FORM INTERROGATORY"),
    "rfa":  ("REQUESTS FOR ADMISSION", "RESPONSES TO REQUESTS FOR ADMISSION", "REQUEST FOR ADMISSION"),
    "rfp":  ("REQUEST FOR PRODUCTION OF DOCUMENTS", "RESPONSES TO REQUEST FOR PRODUCTION", "REQUEST FOR PRODUCTION"),
}

def build(kind, d):
    dname = d.title()
    long_t, head_t, label_t = TITLES[kind]
    title = "PLAINTIFF LINA LU\u2019S RESPONSES TO DEFENDANT %s\u2019S %s, SET ONE" % (d, long_t)
    doc = load_base()
    protos = grab_protos(doc)
    right = [("Case No.: 26PSCV02595", False, None), ("Assigned for all purposes to Department O", False, None),
             ("", False, None), (title, True, None), ("", False, None),
             ("Complaint Filed: July 27, 2026", False, None),
             ("First Amended Complaint Filed: August 31, 2026", False, None), ("Trial Date: Not Set", False, None)]
    rewrite_head(doc, ATTY, COURT, LEFT, right,
                 ["PROPOUNDING PARTY\t:\tDefendant %s" % d, "RESPONDING PARTY\t:\tPlaintiff LINA LU",
                  "SET NUMBER\t\t:\tONE"])
    truncate_body(doc)
    set_footer(doc, title)

    def para(item):
        if isinstance(item, tuple):
            emit(doc, protos, item[0], item[1])
        else:
            emit(doc, protos, "body", item)

    emit(doc, protos, "head", "PRELIMINARY STATEMENT")
    emit(doc, protos, "prelim", PRELIM)
    if kind == "rfp":
        emit(doc, protos, "body", PROD_LINE)
        emit(doc, protos, "body", PROD_FLAG)
    emit(doc, protos, "head", head_t)

    if kind == "frog":
        for n, paras in frog(d):
            emit(doc, protos, "label", "RESPONSE TO FORM INTERROGATORY NO. %s:" % n)
            for x in paras: para(x)
        emit(doc, protos, "body", CONT)
    elif kind == "rfa":
        resp = rfa_resp(d)
        for L, text in rfa_items(d):
            emit(doc, protos, "label", "REQUEST FOR ADMISSION NO. %s:" % L)
            emit(doc, protos, "body", text + ".")
            emit(doc, protos, "label", "RESPONSE TO REQUEST FOR ADMISSION NO. %s:" % L)
            for x in resp[L]: para(x)
    else:
        resp = rfp_resp()
        for n, text in RFP:
            emit(doc, protos, "label", "REQUEST FOR PRODUCTION NO. %s:" % n)
            emit(doc, protos, "body", text + ("" if text.endswith(".") else "."))
            emit(doc, protos, "label", "RESPONSE TO REQUEST FOR PRODUCTION NO. %s:" % n)
            for x in resp[n]: para(x)
        emit(doc, protos, "body", CONT_P)

    emit(doc, protos, "body", "")
    stop = Inches(3.5)
    def stopped(p):
        p.paragraph_format.tab_stops.clear_all(); p.paragraph_format.tab_stops.add_tab_stop(stop); return p
    stopped(emit(doc, protos, "body", "\tLINGTU LAW OFFICE"))
    signature_block(doc, protos, ["Hern\u00e1n S. Sim\u00f3"])
    stopped(emit(doc, protos, "body", "\tAttorneys for Plaintiff LINA LU"))

    # verification + translator (RFP responses need it too: CCP 2031.250)
    page_break(doc, protos)
    emit(doc, protos, "head", "VERIFICATION")
    emit(doc, protos, "body", VERIFICATION_TRANSLATED)
    emit(doc, protos, "body", "I declare under penalty of perjury under the laws of the State of California that the "
                              "foregoing is true and correct.")
    emit(doc, protos, "body", "Executed on ______________, 2026, at Arcadia, California.")
    emit(doc, protos, "body", "")
    stopped(emit(doc, protos, "body", "\t______________________________"))
    stopped(emit(doc, protos, "body", "\tLINA LU"))
    emit(doc, protos, "body", "")
    emit(doc, protos, "head", "DECLARATION OF TRANSLATOR")
    emit(doc, protos, "body", TRANSLATOR_DECL.replace("YI CONG, who stated that he", "LINA LU, who stated that she")
         .replace("I am fluent", "I, " + tbc("TRANSLATOR NAME") + ", am fluent"))
    emit(doc, protos, "body", "Executed on ______________, 2026, at City of Industry, California.")
    emit(doc, protos, "body", "")
    stopped(emit(doc, protos, "body", "\t______________________________"))
    stopped(emit(doc, protos, "body", "\t«[NAME TO BE INSERTED]»"))

    pos.build(doc, protos, served=title, method=("mail", "email"), declarant="Klaus Liu",
              case_name="Lina Lu v. Arlene Luna, et al.",
              court_line="Los Angeles County Superior Court, Case No. 26PSCV02595",
              page_break=page_break,
              parties=[
                  (["Arlene Luna", "152 East Kirkwall Road", "Azusa, California 91702", "(by United States mail)"],
                   ["//Defendant, in pro per://", "", "**ARLENE LUNA**"]),
                  (["Rosalba Luna", "152 East Kirkwall Road", "Azusa, California 91702", "(by United States mail)"],
                   ["//Defendant, in pro per://", "", "**ROSALBA LUNA**"]),
                  (["Colin H. Walshok", "Shealie E. Brew", "Wingert Grebing Brubaker & Walshok LLP",
                    "1230 Columbia Street, Suite 400", "San Diego, California 92101-3370",
                    "cwalshok@wingertlaw.com", "sbrew@wingertlaw.com", "lsherwood@wingertlaw.com",
                    "cstone@wingertlaw.com", "(by electronic mail)"],
                   ["//Attorneys for Defendants://", "",
                    "**RICHARD REYES and ZORAIDA TORRES, as Trustees of the TORRES REYES FAMILY TRUST**"]),
                  (["Matthew E. Bennett", "Samuel S. Beidokhti", "Brockman Quayle Bennett",
                    "12481 High Bluff Drive, Suite 301", "San Diego, California 92130",
                    "mbennett@bqblaw.com", "sbeidokhti@bqblaw.com", "(by electronic mail)"],
                   ["//Attorneys for Defendant://", "", "**AMAZON LOGISTICS, INC.**"]),
              ])
    short = {"frog": "Form Interrogatories", "rfa": "Requests for Admission", "rfp": "Requests for Production"}[kind]
    path = os.path.join(OUT, "Lina Lu - Responses to %s (%s, Set One) - DRAFT.docx" % (short, dname))
    doc.save(path)
    return path

if __name__ == "__main__":
    for d in ("ARLENE LUNA", "ROSALBA LUNA"):
        for k in ("frog", "rfa", "rfp"):
            print(build(k, d))
