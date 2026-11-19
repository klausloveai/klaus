"""Shared helpers for chat-reply. Data lives in ~/lingtu-cm-study/chat-reply (not in git)."""
import json, os, subprocess, fcntl, contextlib
from pathlib import Path

DATA = Path.home() / "lingtu-cm-study" / "chat-reply"
QUEUE = DATA / "queue.json"
STATE = DATA / "state.json"
LOCK = DATA / ".lock"
GWS = "/opt/homebrew/bin/gws"
KLAUS = "users/111988730490738847997"
PEOPLE = {
    "users/111988730490738847997": "Klaus Liu",
    "users/100654574587915125622": "Amos Feng",
    "users/115783512348925922612": "Jerry Piao",
    "users/107684259109708001193": "Claire Feng",
    "users/116146631770326173882": "Jenkins Li",
    "users/108899532142274592679": "Angelina Meng",
    "users/113509312272055277455": "Tiana Deng",
    "users/109437088406471229871": "Ryan Wei",
    "users/114288518499270439854": "Yulu",
    "users/100380498563287542730": "claude@ (bot)",
}

def gws(*args):
    env = dict(os.environ, PATH="/opt/homebrew/bin:/usr/bin:/bin:" + os.environ.get("PATH", ""))
    r = subprocess.run([GWS, *args, "--format", "json"], capture_output=True, text=True, env=env)
    out = "\n".join(l for l in r.stdout.splitlines() if not l.startswith("Using keyring"))
    if r.returncode != 0:
        raise RuntimeError(f"gws {' '.join(args[:3])} failed: {r.stderr[-400:]}")
    return json.loads(out) if out.strip() else {}

def who(sender):
    n = (sender or {}).get("name", "")
    return PEOPLE.get(n) or (sender or {}).get("displayName") or n

@contextlib.contextmanager
def locked_queue():
    DATA.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        q = json.loads(QUEUE.read_text()) if QUEUE.exists() else []
        yield q
        tmp = QUEUE.with_suffix(".tmp")
        tmp.write_text(json.dumps(q, ensure_ascii=False, indent=1))
        tmp.replace(QUEUE)

def read_queue():
    return json.loads(QUEUE.read_text()) if QUEUE.exists() else []
