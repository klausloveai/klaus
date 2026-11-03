#!/usr/bin/env python3
"""随机抽取文案角度，保证每次生成的文案开头、重点、长度都不一样。
用法: python3 pick_angles.py [数量, 默认3]"""
import random, sys

openers = [
    "从当时的心情切入（慌/焦虑/懵/压力大）",
    "从一个具体细节切入（某次回复很快、某个解释很清楚）",
    "从对比切入（原来以为很复杂/很贵/很难沟通，结果不是）",
    "从给朋友的建议切入（如果你也遇到……）",
    "从结果或进度切入（现在已经……）",
    "从一句短感叹切入（一句话开头，不超过10个字）",
    "从时间线切入（刚开始……后来……现在……）",
]
highlights = [
    "沟通及时，消息有回应",
    "耐心解释，把复杂的事讲清楚",
    "流程透明，知道每一步在做什么",
    "专业，抓得住重点",
    "有人认真听我讲，不敷衍",
    "中文沟通方便，少了语言障碍",
    "Paralegal/案件经理跟进很细",
    "费用和预期说得清楚",
]
lengths = ["短（40-60字）", "中（80-120字）", "稍长（130-180字）"]
endings = [
    "推荐给有需要的朋友",
    "不加推荐语，自然收尾",
    "先加联系方式备用，有问题随时问",
    "感谢具体的人或团队",
    "一句祝福/轻松的话收尾",
]

n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
ops = random.sample(openers, min(n, len(openers)))
for i in range(n):
    print(f"版本{i+1}: 开头={ops[i % len(ops)]} | 重点={random.choice(highlights)} | 长度={random.choice(lengths)} | 结尾={random.choice(endings)}")
