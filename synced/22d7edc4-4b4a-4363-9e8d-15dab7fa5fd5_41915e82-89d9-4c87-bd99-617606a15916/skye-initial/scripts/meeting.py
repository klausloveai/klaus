#!/usr/bin/env python3
"""Spot a finalised 材料清单, then find an hour that works in LA and in China.

  detect  — is there a 定稿 / Final 材料清单 in this case folder yet?
  slots   — free hours common to Skye and 蔡律师 that a Beijing client can take

Usage:
  python3 meeting.py detect --case-root <ID>
  python3 meeting.py slots [--days 10] [--duration 60]
                          [--attendees skye.s@lingtulaw.com,cassie@lingtulaw.com]
                          [--la-window 09:00-17:30] [--cn-window 08:00-22:00]

## The time-zone squeeze

The firm is in America/Los_Angeles, the client in Asia/Shanghai — 15 hours
apart on PDT, 16 on PST. Two office days barely overlap: LA 17:00-20:00 is
Beijing 08:00-11:00 the next morning, and that is essentially the whole
workable band. (LA early morning, 06:00-07:00, is Beijing 21:00-22:00 the same
evening — reachable with --cn-window 08:00-23:00 if the client will take an
evening call.) Rather than hardcode "LA evening", both windows are parameters
and the script keeps only slots that sit **entirely** inside both, so daylight
saving on either side can't silently push a meeting into someone's night.

Every slot is reported with both local wall-clock times and both local dates,
because the Beijing date is usually the next day. A proposal that names one
date is the single easiest way to get a client to show up 24 hours late.

## Free/busy has a dangerous failure mode

Asking for a calendar you can't see returns `notFound` **and an empty busy
list** — indistinguishable from "completely free" if you only read `busy`.
This script treats any per-calendar error as fatal and proposes nothing, so a
scheduling suggestion is never built on a calendar it couldn't actually read.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gwslib import GwsError, gws, walk  # noqa: E402

LA = ZoneInfo("America/Los_Angeles")
CN = ZoneInfo("Asia/Shanghai")

DEFAULT_ATTENDEES = ["skye.s@lingtulaw.com", "cassie@lingtulaw.com"]

FINAL_MARKERS = ("定稿", "final")


def cmd_detect(args):
    hits = []
    for f, path in walk(args.case_root):
        name = f["name"]
        low = name.lower()
        if "材料清单" not in name:
            continue
        entry = {"id": f["id"], "name": name, "path": path,
                 "modified_by": (f.get("lastModifyingUser") or {}).get("emailAddress"),
                 "link": f"https://docs.google.com/document/d/{f['id']}/edit"}
        entry["final"] = any(m in low for m in FINAL_MARKERS)
        hits.append(entry)
    finals = [h for h in hits if h["final"]]
    json.dump({"case_root": args.case_root,
               "finalised": bool(finals),
               "final_checklists": finals,
               "all_checklists": hits,
               "signal": "文件名含「定稿」或 Final"},
              sys.stdout, ensure_ascii=False, indent=2)
    print()


def parse_window(text):
    start, end = text.split("-")
    sh, sm = (int(x) for x in start.split(":"))
    eh, em = (int(x) for x in end.split(":"))
    return sh * 60 + sm, eh * 60 + em


def minutes_of(dt):
    return dt.hour * 60 + dt.minute


def busy_intervals(attendees, start, end):
    body = {"timeMin": start.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z"),
            "timeMax": end.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z"),
            "timeZone": "America/Los_Angeles",
            "items": [{"id": a} for a in attendees]}
    data = gws(["calendar", "freebusy", "query"], body=body)
    cals = data.get("calendars", {})
    problems = {}
    blocks = []
    for who in attendees:
        info = cals.get(who)
        if info is None:
            problems[who] = "日历未返回（地址是否正确？）"
            continue
        if info.get("errors"):
            problems[who] = ", ".join(e.get("reason", "?") for e in info["errors"])
            continue
        for b in info.get("busy", []):
            blocks.append((datetime.fromisoformat(b["start"].replace("Z", "+00:00")),
                           datetime.fromisoformat(b["end"].replace("Z", "+00:00"))))
    return blocks, problems


def find_slots(blocks, day0, horizon, la_window, cn_window, dur):
    """Every free half-hour boundary whose whole meeting sits in both windows."""
    la_lo, la_hi = parse_window(la_window)
    cn_lo, cn_hi = parse_window(cn_window)
    out = []
    cursor = day0
    step = timedelta(minutes=30)
    while cursor + dur <= horizon:
        start_la, end_la = cursor.astimezone(LA), (cursor + dur).astimezone(LA)
        start_cn, end_cn = cursor.astimezone(CN), (cursor + dur).astimezone(CN)
        ok = (la_lo <= minutes_of(start_la) and minutes_of(end_la) <= la_hi
              and cn_lo <= minutes_of(start_cn) and minutes_of(end_cn) <= cn_hi
              and start_la.weekday() < 5 and start_cn.weekday() < 5
              and end_la.date() == start_la.date())
        if ok and not any(b0 < cursor + dur and cursor < b1 for b0, b1 in blocks):
            out.append({
                "start_utc": cursor.astimezone(ZoneInfo("UTC")).isoformat(),
                "la": start_la.strftime("%m/%d/%Y %H:%M") + "–" + end_la.strftime("%H:%M"),
                "la_date": start_la.strftime("%m/%d/%Y"),
                "la_hour": clock(start_la),
                "cn": start_cn.strftime("%m/%d/%Y %H:%M") + "–" + end_cn.strftime("%H:%M"),
                "cn_date": start_cn.strftime("%m/%d/%Y"),
                "cn_hour": clock(start_cn),
                "next_day_in_cn": start_cn.date() != start_la.date(),
                "phrasing": phrasing(start_la, start_cn),
            })
        cursor += step
    return out


# Relaxations to try, in the order we'd rather ask for them, when the firm's
# own hours and the client's leave no overlap at all. Asking a Beijing client
# for 07:30 is a smaller favour than asking two attorneys to stay past 17:30,
# so the client-side widenings come first.
RELAXATIONS = [
    ("把客户窗口放宽到 07:00 起", None, "07:00-22:00"),
    ("把客户窗口放宽到 06:30 起", None, "06:30-22:00"),
    ("律所延到 18:00", "09:00-18:00", None),
    ("律所延到 19:00", "09:00-19:00", None),
    ("律所提前到 07:00 开始（对应客户当晚 22 点后）", "07:00-17:30", "08:00-23:00"),
]


def cmd_slots(args):
    attendees = [a.strip() for a in args.attendees.split(",") if a.strip()]
    dur = timedelta(minutes=args.duration)

    now = datetime.now(LA)
    # Start tomorrow: proposing a meeting for later today, to a client who is
    # already asleep, wastes a round trip.
    day0 = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    horizon = day0 + timedelta(days=args.days)

    blocks, problems = busy_intervals(attendees, day0, horizon)
    if problems:
        json.dump({"status": "refused", "problems": problems,
                   "why": "有日历读不到。freebusy 对读不到的日历返回空 busy，"
                          "看起来像全天空闲，据此排会等于瞎猜。"},
                  sys.stdout, ensure_ascii=False, indent=2)
        print()
        sys.exit(2)

    slots = find_slots(blocks, day0, horizon, args.la_window, args.cn_window, dur)

    result = {"status": "ok", "attendees": attendees, "duration_min": args.duration,
              "la_window": args.la_window, "cn_window": args.cn_window,
              "searched": f"{day0.date()} … {horizon.date()} (LA)",
              "slot_count": len(slots), "slots": slots[:args.limit]}

    # An empty result here is usually arithmetic, not a full calendar: LA
    # 09:00-17:30 maps to Beijing 00:00-08:30 on PDT, so a one-hour meeting
    # inside both the firm's hours and a 08:00 Beijing start simply does not
    # exist for half the year. Saying "no times available" would send someone
    # hunting through calendars for a gap that was never possible. So when
    # nothing fits, re-run the search with each relaxation and report which
    # one actually opens the door, and by how much.
    if not slots:
        result["status"] = "no_overlap"
        result["diagnosis"] = ("律所时段和客户时段没有重合区间，不是日历排满了。"
                               "洛杉矶 09:00–17:30 对应北京次日 00:00–08:30（夏令时），"
                               "整点一小时的会落不进北京 08:00 之后。")
        tried = []
        for label, la_w, cn_w in RELAXATIONS:
            alt = find_slots(blocks, day0, horizon,
                             la_w or args.la_window, cn_w or args.cn_window, dur)
            tried.append({"放宽方式": label,
                          "la_window": la_w or args.la_window,
                          "cn_window": cn_w or args.cn_window,
                          "slot_count": len(alt),
                          "sample": alt[0] if alt else None})
        result["relaxations"] = tried
        result["next"] = "选一个放宽方式，用 --la-window / --cn-window 重跑。"

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


def clock(dt):
    """A wall-clock time a Chinese reader can't misread.

    Bare "6点" for an 18:00 meeting is the bug this exists to prevent: the
    firm's slots are LA evening and the client's are next-morning, so a
    12-hour rendering with no 上午/下午 puts the two sides twelve hours apart.
    Minutes are kept whenever they aren't zero — half-hour starts are normal
    here and "9点" for 09:30 sends someone to the wrong half of the hour.
    """
    h = dt.hour
    period = ("凌晨" if h < 6 else "上午" if h < 12 else
              "中午" if h == 12 else "下午" if h < 18 else "晚上")
    twelve = h % 12 or 12
    return f"{period}{twelve}点" if dt.minute == 0 else f"{period}{twelve}:{dt.minute:02d}"


def phrasing(start_la, start_cn):
    """The client-facing line, in the firm's wording.

    Both dates are always spelled out, not only when they differ. The firm's
    slots are late LA afternoon and the client's are the next morning, so the
    two dates disagree on essentially every proposal — and a line carrying one
    date is the single easiest way to get a client to dial in 24 hours late.
    Printing the China date unconditionally also means nobody has to notice
    whether "次日" was there or not.
    """
    same_day = start_cn.date() == start_la.date()
    cn_date = start_cn.strftime("%m/%d/%Y") + ("" if same_day else "（次日）")
    return (f"{start_la.strftime('%m/%d/%Y')} 洛杉矶时间{clock(start_la)}，"
            f"客户当地时间{cn_date} {clock(start_cn)}，"
            "您是否有空，我们约个会议，对一下材料；")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("detect", help="look for a 定稿/Final 材料清单")
    p.add_argument("--case-root", required=True)
    p.set_defaults(func=cmd_detect)

    p = sub.add_parser("slots", help="find candidate meeting times")
    p.add_argument("--days", type=int, default=10)
    p.add_argument("--duration", type=int, default=60)
    p.add_argument("--attendees", default=",".join(DEFAULT_ATTENDEES))
    p.add_argument("--la-window", default="09:00-17:30")
    p.add_argument("--cn-window", default="08:00-22:00")
    p.add_argument("--limit", type=int, default=8)
    p.set_defaults(func=cmd_slots)

    args = ap.parse_args()
    try:
        args.func(args)
    except GwsError as exc:
        sys.exit(f"gws error: {exc}")


if __name__ == "__main__":
    main()
