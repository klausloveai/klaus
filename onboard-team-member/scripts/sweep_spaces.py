#!/usr/bin/env python3
"""并发拉取每个 Chat 空间的成员名单 → members.json

用法:
  gws chat spaces list --params '{"pageSize":1000,"filter":"spaceType = \"SPACE\""}' > spaces.json
  python3 sweep_spaces.py            # 读 spaces.json，写 members.json

557 个空间约 1 分钟。members.json 结构: [[space_name, displayName, [(dn,uid,type)...], err], ...]
"""
import json, subprocess, concurrent.futures as cf, sys

SPACES = sys.argv[1] if len(sys.argv) > 1 else 'spaces.json'
OUT    = sys.argv[2] if len(sys.argv) > 2 else 'members.json'

def get(s):
    n = s['name']
    try:
        out = subprocess.run(
            ['gws','chat','spaces','members','list','--params',
             json.dumps({"parent": n, "pageSize": 100})],
            capture_output=True, text=True, timeout=120)
        d = json.loads(out.stdout[out.stdout.index('{'):])
        ms = [(m.get('member',{}).get('displayName'),
               m.get('member',{}).get('name'),
               m.get('member',{}).get('type')) for m in d.get('memberships', [])]
        return n, s.get('displayName'), ms, None
    except Exception as e:
        return n, s.get('displayName'), None, str(e)[:120]

sp = json.load(open(SPACES))['spaces']
res = []
with cf.ThreadPoolExecutor(12) as ex:
    for r in ex.map(get, sp):
        res.append(r)
json.dump(res, open(OUT,'w'))
print(f'done {len(res)} spaces, errors {sum(1 for r in res if r[2] is None)} -> {OUT}')
