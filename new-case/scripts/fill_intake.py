#!/usr/bin/env python3
"""
fill_intake.py — 按「区块 + 标签」把值写进 intake xlsx（建案第 6 步唯一允许的写法）。

为什么有这个脚本（2026-11-16 Xinchen Hou 事故）：
  以前每次建案都现写一段 inline openpyxl，按 B 列标签建 label→cell 映射。模板里客户区
  (B5–B21) 和乘客区 (B28 起、E28 起…) 的标签大量重名（Date Birth / Phone / Address /
  Email / SSN …），映射「后者覆盖前者」→ 客户本人资料写进乘客 1 栏，随后乘客栏被填
  N/A 又把它盖掉。Xinchen Hou / Weiguo Mao / Yi Li 三案客户栏空白，CM 接手才发现。
  这个脚本把每个区块的行范围写死，区内重名自动编号（Adjuster / Adjuster 2），
  标签不存在直接报错，写完自检客户核心格。

用法：
    python3 fill_intake.py <intake.xlsx> <values.json>

values.json：
{
  "client":    {"Date of Loss": "11/14/2026", "Driver Name": "...", "Date Birth": "...", ...},
  "accident":  {"Accd Location": "...", "Fact of Loss": "...", ...},
  "1p":        {"1P Insurer": "...", "Policy#": "...", "Adjuster": "Pending", "Adjuster 2": "", ...},
  "3p":        {"3P Insurer": "...", "Driver": "...", ...},
  "passengers": [ {"Pass1 Name": "...", "Date Birth": "...", ...} ],   # 第 1–4 位乘客，按顺序
  "no_passengers": true,           # 表单明确说「没有乘客」才写 N/A；不知道（没表单）→ Pending
  "cells": {"R3": "Pending"}       # 区块外的个别格子，按地址写
}
默认值（Klaus 2026-11-16）：已知的先填，其余**所有**值格一律黄色 `Pending`，不准留空白。
  例外：模板自带的 Coverage/Liability Status、Accd Diagram；1P 第二个 Adjuster 块（I19–I22）、3P 第二个块（L23–L25）留空。
规则：每个写入的格子 = 黄色、Nunito 10、非粗体、左对齐、不换行（Klaus 2026-11-10：Claude 写的一律黄）。
值为 null 的键跳过（不写、不变黄）。
"""
import json
import sys
from collections import defaultdict

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill

# (标签列, 值列, 起始行, 结束行) —— 模板 2026-11 版。模板改版先改这里。
SECTIONS = {
    "client":   ("B", "C", 1, 22),
    "accident": ("E", "F", 1, 22),
    "1p":       ("H", "I", 1, 31),
    "3p":       ("K", "L", 1, 27),
    "pass1":    ("B", "C", 24, 45),
    "pass2":    ("E", "F", 24, 45),
    "pass3":    ("B", "C", 49, 70),
    "pass4":    ("E", "F", 49, 70),
}
CLIENT_CORE = ["Date Birth", "Phone", "Address", "Email"]
YELLOW = PatternFill("solid", fgColor="FFFF00")


def label_map(ws, sec):
    lc, vc, a, b = SECTIONS[sec]
    m, count = {}, defaultdict(int)
    for r in range(a, b + 1):
        v = ws[f"{lc}{r}"].value
        if not v:
            continue
        k = str(v).split("\n")[0].strip()
        count[k] += 1
        key = k if count[k] == 1 else f"{k} {count[k]}"
        m[key] = f"{vc}{r}"
    return m


def write(ws, cell, value):
    c = ws[cell]
    c.value = value
    c.fill = YELLOW
    c.font = Font(name="Nunito", size=10, bold=False)
    c.alignment = Alignment(horizontal="left", wrap_text=False)


def main():
    path, spec_path = sys.argv[1], sys.argv[2]
    spec = json.load(open(spec_path))
    wb = load_workbook(path)
    ws = wb.active
    written, errors = {}, []

    def fill(sec, values):
        m = label_map(ws, sec)
        for field, val in values.items():
            if val is None:
                continue
            if field not in m:
                errors.append(f"[{sec}] 没有标签「{field}」。可用：{', '.join(m)}")
                continue
            write(ws, m[field], val)
            written[m[field]] = (sec, field)

    for sec in ("client", "accident", "1p", "3p"):
        fill(sec, spec.get(sec, {}))

    pax = spec.get("passengers", [])
    if len(pax) > 4:
        errors.append("模板只有 4 个乘客区块")
    for i in range(4):
        sec = f"pass{i + 1}"
        if i < len(pax):
            fill(sec, pax[i])
        elif spec.get("no_passengers"):
            for cell in label_map(ws, sec).values():
                write(ws, cell, "N/A")

    for cell, val in spec.get("cells", {}).items():
        write(ws, cell, val)
        written[cell] = ("cells", cell)

    # 其余空值格一律黄色 Pending（Klaus 2026-11-16：「默认应该是黄色 pending all」）
    SKIP = {"I19", "I20", "I21", "I22", "L23", "L24", "L25"}
    NOY = {"coverage status", "liability status", "accd diagram", "clients index",
           "accident infomation", "1st party insurance", "3rd party insurance"}
    for sec in SECTIONS:
        lc, vc, a, b = SECTIONS[sec]
        for r in range(a, b + 1):
            lab = ws[f"{lc}{r}"].value
            k = f"{vc}{r}"
            if not lab or k in SKIP or str(lab).split("\n")[0].strip().lower() in NOY \
               or str(lab).startswith("Passenger "):
                continue
            if ws[k].value in (None, ""):
                write(ws, k, "Pending")

    # 自检 1：客户核心格不能空（不知道写 Pending）
    cm = label_map(ws, "client")
    for f in CLIENT_CORE:
        if ws[cm[f]].value in (None, ""):
            errors.append(f"客户 {f}（{cm[f]}）是空的——不知道就写 Pending")

    # 自检 2：客户的 DOB / 电话 / 邮箱不应出现在乘客区块（同住家人共用地址不算）
    probe = {f: str(ws[cm[f]].value).strip() for f in ("Date Birth", "Phone", "Email")
             if ws[cm[f]].value not in (None, "", "Pending", "N/A")}
    for i in range(4):
        pm = label_map(ws, f"pass{i + 1}")
        given = pax[i] if i < len(pax) else {}
        for f, v in probe.items():
            if f in given:          # 乘客自己的值是明确传进来的（家人共用电话/邮箱）→ 不算错
                continue
            if f in pm and str(ws[pm[f]].value).strip() == v:
                errors.append(f"乘客 {i + 1} 的 {f}（{pm[f]}）和客户一样：{v} —— 写错栏？")

    if errors:
        print("❌ 未保存：\n  " + "\n  ".join(errors))
        sys.exit(1)
    wb.save(path)
    print(f"✅ 写入 {len(written)} 格（全黄），客户核心格已核：" +
          ", ".join(f"{cm[f]}={ws[cm[f]].value}" for f in CLIENT_CORE))


if __name__ == "__main__":
    main()
