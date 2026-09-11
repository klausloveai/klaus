#!/usr/bin/env python3
"""
add_deadline.py — create a litigation deadline on Klaus's calendar in the firm's shape.

Usage:
    python3 add_deadline.py config.json

Everything about the shape that is not negotiable is enforced here rather than left to the
caller: Tomato color, all-day event, exclusive end date, and a description assembled in a
fixed order so every deadline event reads the same way.

config.json:
{
  "summary": "<Case> — <what is due> Due",
  "date": "YYYY-MM-DD",                       // the deadline itself
  "attendees": ["hernan.s@lingtulaw.com"],    // optional, defaults to Hernán
  "reminders_minutes": [1440],                // optional, defaults to 1 day before
  "send_updates": "all",                      // optional: all | none (default all)
  "description_blocks": {                     // all optional, emitted in this order
    "served":      "what was served/filed, itemized, on whom, when, by what method",
    "computation": "the arithmetic, with the statute cited",
    "matter":      "case no., court, department, judge",
    "counsel":     "opposing counsel + service email",
    "if_missed":   "consequence of blowing it"
  },
  "description": "..."                        // optional raw override; wins over blocks
}

Requires: gws on PATH (authenticated as klaus@).
"""
import json, sys, subprocess, datetime

TOMATO = "11"                                   # Google event colorId — Tomato (#dc2127)
DEFAULT_ATTENDEES = ["hernan.s@lingtulaw.com"]
BLOCK_ORDER = ["served", "computation", "matter", "counsel", "if_missed"]
BLOCK_LABEL = {
    "served":      "SERVED / FILED",
    "computation": "COMPUTATION",
    "matter":      "MATTER",
    "counsel":     "OPPOSING COUNSEL",
    "if_missed":   "IF THIS PASSES",
}


def gws(*args):
    r = subprocess.run(["gws", *args], capture_output=True, text=True)
    s = r.stdout
    i = s.find("{")
    if i < 0:
        raise SystemExit(f"gws failed:\n{r.stdout}\n{r.stderr}")
    return json.JSONDecoder().raw_decode(s[i:])[0]


def build_description(cfg):
    if cfg.get("description"):
        return cfg["description"]
    blocks = cfg.get("description_blocks") or {}
    out = []
    for k in BLOCK_ORDER:
        v = (blocks.get(k) or "").strip()
        if v:
            out.append(f"{BLOCK_LABEL[k]}\n{v}")
    return "\n\n".join(out)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    cfg = json.load(open(sys.argv[1]))

    for req in ("summary", "date"):
        if not cfg.get(req):
            raise SystemExit(f"config is missing required field: {req}")

    start = datetime.date.fromisoformat(cfg["date"])
    end = start + datetime.timedelta(days=1)      # all-day end is exclusive

    body = {
        "summary": cfg["summary"],
        "colorId": TOMATO,                        # forced — see SKILL.md
        "start": {"date": start.isoformat()},
        "end": {"date": end.isoformat()},
        "description": build_description(cfg),
        "attendees": [{"email": e} for e in cfg.get("attendees", DEFAULT_ATTENDEES)],
        "reminders": {
            "useDefault": False,
            "overrides": [{"method": "popup", "minutes": m}
                          for m in cfg.get("reminders_minutes", [1440])],
        },
    }

    e = gws("calendar", "events", "insert",
            "--params", json.dumps({"calendarId": "primary",
                                    "sendUpdates": cfg.get("send_updates", "all")}),
            "--json", json.dumps(body))

    if e.get("colorId") != TOMATO:
        print("WARNING: event was not created Tomato — check it by hand.")
    print("created :", e.get("summary"))
    print("  date  :", e.get("start", {}).get("date"))
    print("  color :", e.get("colorId"), "(11 = Tomato)")
    print("  invite:", [a.get("email") for a in e.get("attendees", [])] or "none")
    print("  link  :", e.get("htmlLink"))
    print("  id    :", e.get("id"))
    print("\nReport the date AND the computation back to whoever asked for it.")


if __name__ == "__main__":
    main()
