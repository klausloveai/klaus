#!/usr/bin/env python3
"""把一个人批量加进 targets.json 列出的 Chat 空间，然后逐个复核 PRESENT。

用法:
  1) 先建 targets.json:  [["显示名","spaces/xxx"], ...]
     常规 = a_split.json 的 active + unmatched，再加三个共享群:
       PI Team Chat     spaces/AAQAYUyVfMg
       Treatment Team   spaces/AAQABniKvxc
       Treatment Notice spaces/AAQARYNZEFo
  2) python3 bulk_add.py <user@lingtulaw.com 或 users/<id>>

第一次用 email 形式即可，Chat API 接受 users/<email>；返回值里带永久 user id。
角色一律默认 ROLE_MEMBER。
"""
import json, subprocess, sys, concurrent.futures as cf
from collections import Counter

who = sys.argv[1]
UID = who if who.startswith('users/') else f'users/{who}'
T = [tuple(x) for x in json.load(open('targets.json'))]

def add(t):
    dn, n = t
    p = subprocess.run(['gws','chat','spaces','members','create','--params',
        json.dumps({"parent": n}), '--json',
        json.dumps({"member": {"name": UID, "type": "HUMAN"}})],
        capture_output=True, text=True, timeout=120)
    try:
        d = json.loads(p.stdout[p.stdout.index('{'):])
    except Exception:
        return (dn, n, 'PARSE_FAIL', (p.stdout + p.stderr)[-200:])
    if 'error' in d:
        return (dn, n, 'ERROR', d['error'].get('message','')[:160])
    return (dn, n, 'OK', d.get('member',{}).get('name'))

res = []
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(add, T):
        res.append(r); print(r[2], '|', r[0], flush=True)
json.dump(res, open('add_result.json','w'))
print(f"\n=== ADD OK {sum(1 for r in res if r[2]=='OK')} / {len(res)} ===")
for r in res:
    if r[2] != 'OK': print('FAIL:', r[0], r[1], r[3])

# 复核 —— 不要只信 create 的返回值
real = next((r[3] for r in res if r[2]=='OK' and str(r[3]).startswith('users/')), UID)
def chk(t):
    dn, n = t
    p = subprocess.run(['gws','chat','spaces','members','list','--params',
        json.dumps({"parent": n, "pageSize": 100})], capture_output=True, text=True, timeout=120)
    try: d = json.loads(p.stdout[p.stdout.index('{'):])
    except Exception: return (dn, 'CHECK_FAIL')
    ids = {m.get('member',{}).get('name') for m in d.get('memberships', [])}
    return (dn, 'PRESENT' if real in ids else 'MISSING')
v = []
with cf.ThreadPoolExecutor(10) as ex:
    for x in ex.map(chk, T): v.append(x)
print('\n=== VERIFY ===', Counter(s for _, s in v))
for dn, s in v:
    if s != 'PRESENT': print('  !!', dn, s)
print('user id =', real)
