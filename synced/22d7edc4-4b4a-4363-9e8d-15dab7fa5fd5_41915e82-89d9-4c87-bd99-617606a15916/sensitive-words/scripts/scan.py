#!/usr/bin/env python3
"""移民内容敏感词扫描 / 替换。

用法：
  python scan.py --mode subtitle 字幕.srt            # 只出报告
  python scan.py --mode copy --fix 文案.txt           # 报告 + 输出替换后的文本
  echo "最近移民局出了新规" | python scan.py --mode cover --fix

mode:
  subtitle  字幕、花字（剪辑软件里显示，国旗 emoji 会变方框 → 用 USA）
  copy      小红书标题、正文、tag、朋友圈等文案（可以用 🇺🇸）
  cover     封面（不用 z / G / J / gwy 这类字母替代，换真正的英文或改写）

报告分三类：
  AUTO    固定替换，--fix 会直接改
  REVIEW  需要人看一眼：要改写、可能误伤、或封面上没有现成英文
  BANNED  直接不出现的词，--fix 不会改，必须人工删或换说法
"""
import argparse
import re
import sys

# ---- 替换表 -------------------------------------------------------------
# 每项：词 -> {mode: 替换}；mode 缺省用 "default"。替换值为 None 表示只提示不自动改。
REPLACE = {
    # 一、固定替换
    "美国": {"subtitle": "USA", "cover": "USA", "default": "🇺🇸"},
    "国务院": {"cover": "State Dept", "default": "gwy"},
    "移民局": {"cover": "USCIS", "default": "移民J"},
    "政策": {"cover": "policy", "default": "z策"},
    "新规": {"cover": "new rule", "default": "新G"},
    "最": {"cover": None, "default": "z"},
    "政": {"cover": None, "default": "z"},
    "规": {"cover": None, "default": "G"},
    "局": {"cover": None, "default": "J"},
    "钱": {"default": "💰"},
    # 二、延伸替换
    "国会议员": {"default": "congressman"},
    "国会": {"default": "Congress"},
    "中国": {"default": "China"},
    "执法": {"default": "enforcement"},
    "律师费": {"default": "legal fee"},
    "免费": {"default": "free"},
    "费用": {"cover": None, "default": "f用"},
    "价格": {"default": "💰"},
    "多少钱": {"default": "💰"},
    "工资": {"default": "salary"},
    "收入": {"default": "income"},
    "投资": {"cover": None, "default": "tz"},
    "中介": {"cover": None, "default": "zj"},
    "加微信": {"default": "滴滴"},
    "微信": {"default": "V"},
    "私信": {"default": "DM"},
    "电话": {"default": "主页"},
    "联系方式": {"default": "主页"},
    "链接": {"default": "主页"},
    "网址": {"default": "主页"},
    "非法打工": {"default": "unauthorized work"},
    "非法": {"default": "undocumented"},
    "黑户": {"default": "undocumented"},
    "偷渡": {"default": "undocumented"},
    "遣返": {"default": "deport"},
    "驱逐": {"default": "deport"},
    "庇护": {"default": "asylum"},
    "难民": {"default": "refugee"},
    "出国": {"cover": None, "default": "chu国"},
}

# 替换后仍建议人工看的词（附提示）
REVIEW_NOTES = {
    "非法": "替换成 undocumented 后尽量整句不提",
    "黑户": "替换成 undocumented 后尽量整句不提",
    "偷渡": "替换成 undocumented 后尽量整句不提",
    "局": "单字替换，注意'结局/局面'这类是否需要改写",
}

# 只提示、不自动替换（容易误伤）
REVIEW_ONLY = [
    (r"(?<![利滋湿红圆温丰浸])润(?![滑色笔肤泽])", "'润'指出国时改成 chu国"),
]

# 三、直接不出现
BANNED = [
    (r"保证", "承诺用语"),
    (r"包过", "承诺用语"),
    (r"100\s*%|百分之百", "承诺用语"),
    (r"绝对", "承诺用语"),
    (r"第一(?![次步天个年批周轮])", "极限词（第一次/第一步等不算）"),
    (r"唯一", "极限词"),
    (r"顶级", "极限词"),
    (r"最好", "极限词"),
    (r"(成功|通过|获批|过签)率", "成功率/通过率类承诺"),
    (r"\d+(\.\d+)?\s*%", "百分比，确认不是成功率承诺"),
    (r"党", "敏感时政"),
    (r"领导人|主席|总书记", "敏感时政"),
    (r"绕过法律|钻空子|绕开法律|规避法律", "不能出现"),
    (r"\b[A-Z]{3}\d{10}\b", "疑似 USCIS 案件号"),
    (r"\bA-?\d{8,9}\b", "疑似 A-number"),
    (r"\b[A-Z]{1,2}\d{7,8}\b", "疑似护照/证件号"),
]

CJK_SUB = {"subtitle": [("🇺🇸", "USA"), ("🇨🇳", "China")]}


def build_regex():
    words = sorted(REPLACE, key=len, reverse=True)
    return re.compile("|".join(re.escape(w) for w in words))


def lookup(word, mode):
    table = REPLACE[word]
    return table[mode] if mode in table else table["default"]


def scan_line(line, mode, rx):
    hits = []
    # 先找禁用词区间，落在里面的替换词不再重复报（如“最好”不报“最”）
    banned_spans = []
    for pat, note in BANNED:
        for m in re.finditer(pat, line):
            if any(s <= m.start() < e for s, e in banned_spans):
                continue
            hits.append(("BANNED", m.group(0), "删掉或换说法", note, m.start()))
            banned_spans.append((m.start(), m.end()))
    for pat, note in REVIEW_ONLY:
        for m in re.finditer(pat, line):
            hits.append(("REVIEW", m.group(0), "看语境", note, m.start()))

    def in_banned(pos):
        return any(s <= pos < e for s, e in banned_spans)

    out, last = [], 0
    for m in rx.finditer(line):
        word = m.group(0)
        if in_banned(m.start()):
            continue
        rep = lookup(word, mode)
        if rep is None:
            hits.append(("REVIEW", word, "封面上改写或换英文", "封面不用字母替代", m.start()))
            continue
        kind = "REVIEW" if word in REVIEW_NOTES else "AUTO"
        hits.append((kind, word, rep, REVIEW_NOTES.get(word, ""), m.start()))
        out.append(line[last:m.start()])
        prev = "".join(out)[-1:]
        nxt = line[m.end():m.end() + 1]
        if prev.isascii() and prev.isalnum() and rep[:1].isascii() and rep[:1].isalnum():
            rep = " " + rep
        if nxt.isascii() and nxt.isalnum() and rep[-1:].isascii() and rep[-1:].isalnum():
            rep = rep + " "
        out.append(rep)
        last = m.end()
    out.append(line[last:])
    fixed = "".join(out)
    for a, b in CJK_SUB.get(mode, []):
        if a in fixed:
            hits.append(("AUTO", a, b, "剪辑软件里国旗会显示成方框", fixed.index(a)))
            fixed = fixed.replace(a, b)
    hits.sort(key=lambda h: h[4])
    return fixed, hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="文本/字幕文件，省略则读 stdin")
    ap.add_argument("--mode", choices=["subtitle", "copy", "cover"], required=True)
    ap.add_argument("--fix", action="store_true", help="输出自动替换后的全文")
    ap.add_argument("-o", "--output", help="--fix 时写入此文件（默认打印）")
    args = ap.parse_args()

    if args.files:
        sources = [(f, open(f, encoding="utf-8").read()) for f in args.files]
    else:
        sources = [("<stdin>", sys.stdin.read())]

    rx = build_regex()
    counts = {"AUTO": 0, "REVIEW": 0, "BANNED": 0}
    fixed_all = []
    for name, text in sources:
        fixed_lines = []
        for i, line in enumerate(text.splitlines(), 1):
            fixed, hits = scan_line(line, args.mode, rx)
            fixed_lines.append(fixed)
            for kind, word, rep, note, _ in hits:
                counts[kind] += 1
                extra = f"  ({note})" if note else ""
                print(f"[{kind}] {name}:{i}  {word} → {rep}{extra}  | {line.strip()}")
        fixed_all.append("\n".join(fixed_lines))

    print(f"\n合计：AUTO {counts['AUTO']}  REVIEW {counts['REVIEW']}  BANNED {counts['BANNED']}  (mode={args.mode})")

    if args.fix:
        result = "\n\n".join(fixed_all) + "\n"
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"已写入 {args.output}")
        else:
            print("\n----- 替换后 -----")
            print(result, end="")
    sys.exit(1 if counts["BANNED"] or counts["REVIEW"] else 0)


if __name__ == "__main__":
    main()
