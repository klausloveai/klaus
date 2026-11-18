---
name: pi-team-bonus-monthly
description: 每月 1 号 9:00 算上个月 PI Team Bonus，起草 Amos/Jerry/Claire 三封核对邮件草稿（只起草，不发、不写表）
---

你在给 Klaus（klaus@lingtulaw.com，凌图律所 PI 合伙人）做上个月的 PI Team Bonus 月结。先用 `date` 读真实日期，「上个月」= 当前日期的上一个自然月。用简体中文回复，客户名保持英文。

## 红线
- **只起草，不发送**邮件；**不写** Team Bonus tab、不改任何表（memory 规定：当事人核对确认后才动表）。最后等 Klaus 说「发」。
- 绝不编造金额 / 日期；查不到就写「未核实」并列出来。

## 先读口径（必须读完再算）
1. `~/.claude/projects/-Users-klaus/memory/team_bonus_monthly_close.md`（口径、算式、核对邮件格式——以 2026-11-06 那段邮件格式为准）
2. `~/.claude/projects/-Users-klaus/memory/feedback_team_message_no_editorializing.md`
3. `~/lingtu-accounting/team-bonus_handoff_2026-11-03.md` §3（10 月范例）、§4.2（10/30 后的口径修正，优先于 memory 里旧的「两道 check 取并集」）、§6
关键口径（10/30 起）：只认**客户已签字的 disbursement letter，按签字日归月**；律师费以签字 letter 为准；Picase@ 案计 Amos、Jenkins 不计 CM bonus；Klaus@ / Klaus 本人办结的只计 Claire 件数；MedPay 只认进了签字 dis 的；CM 6%（$50k–80k）/ 8%（>$80k）累进；Amos Leadership = Jerry bonus × 25%；Claire =（部门件数 − 13）× $30；发放日 = 本月 16 日（写具体日期如 12/16）。

## 找案子（上个月签字的 dis letter）
- `2026-Disbursement Sheet` `1Av8_fj3MAekCM6RujmGWuFsYRnSG6MMbAskvPkFcs2U` 的 `Internal ` tab（名字带尾空格，只当线索）
- Drive `Case Disbursements` folder `1wIM0orXM7t4ogE6RgQIUAEYYU6pSRj2v` 里的签字 letter（逐份看图核签字日、总额、费率、律师费、垫付、诊所、客户到手；签名是图片，要渲染看）
- IOLTA Account Journal `~/Library/CloudStorage/GoogleDrive-klaus@lingtulaw.com/My Drive/Documents/Lingtu Law-Disbursement/IOLTA#3618/Account-Journal.xlsx`（诊所支票号、原账单→减免后、客户支票）
- PI Master Sheet `1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM`（经办信箱 / CM、DOL、retainer 类型）
- 用 Team Bonus tab 的重复检查（客户+DOL+律师费）排除以前月份已计的。
- 转诉讼的案子（规则 ④）**不要自己推断**，在报告里问 Klaus「上个月有哪些案子转诉讼、各自最后 written offer」。

## 起草三封邮件（klaus@ Gmail 草稿，gws；From klaus@，Cc 无）
- To：amos.f@lingtulaw.com / jerry.p@lingtulaw.com / claire.f@lingtulaw.com
- Subject：`<YYYY> 年 <M> 月 PI Team Bonus 核对 — <姓名>`
- 格式照 memory 2026-11-06 段：CM 版 = 认定数 + 一、案件明细表（签 dis 日 / 客户 / DOL / 3P / UM/UIM / MedPay / 和解总额 / 费率 / 律师费 / 垫付 / 诊所合计 / 客户到手 / 备注）+ 二、诊所明细表（客户 / 诊所 / 原账单 / 减免后 / 支票号）+ 口径句 + Bonus 算式 + 合计 + 核对问句 + 「没问题的话我就按这个数，<M>/16 发给你。」+「这封邮件请让你的 Claude 记录存档。」；Claire 版只列件数 + 案件清单（签 dis 日 / 客户 / DOL / 经办），**不列任何金额**。签名追加 `~/.claude/signatures/klaus_director_cm.html`。
- 可复用上次的生成脚本 `~/Downloads/任务总盘/Team Bonus/oct_bonus_drafts_v2.py`（它读 10 月核对 xlsx；这次先把上个月数据整理成同结构再跑，或改脚本），中间文件放 `~/Downloads/任务总盘/Team Bonus/`。
- 每件自检：3P+UM+MedPay = 总额；总额 − 律师费 − 垫付 − 诊所 = 客户到手；诊所明细之和 = 诊所合计；New 50% 律师费 =（总额 − 诊所）× 50%。

## 验收与交付
- 起草完调用 `Agent(subagent_type: "verifier")`，只给原材料（草稿 id、来源文件、本任务说明），不给你的判断；必改的改掉、❌ 先复核。
- 交给 Klaus：① 验收 summary ② 每人：本月件数、律师费、bonus 合计、草稿 id ③ 待 Klaus 拍板的问题（转诉讼、未核实项、异常）④ 最后一句「确认没问题就说"发"」。全文预览另存 `~/Downloads/任务总盘/Team Bonus/<姓名>_preview.md` 并用 SendUserFile 发给他。
- 如果上个月一份签字 letter 都找不到，直接报告「上个月 0 件」和你查过的范围（folder / tab / 时间窗），不要起草。