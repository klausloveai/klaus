#!/usr/bin/env python3
"""按房间名后缀 + PI Master Sheet 状态，把某个组的案件群分成 active / closed / unmatched。

用法:  python3 classify_spaces.py <TEAM_TAB> <SUFFIX>
例:    python3 classify_spaces.py 'Claims@' A
       python3 classify_spaces.py 'Piteam@' J
       python3 classify_spaces.py 'Picase@' R

读 members.json，抓 Master Sheet 对应 tab (B=客户名, D=Case Status)，写 a_split.json。

⚠️ 后缀是唯一可靠判据。绝不用"CM 是不是群成员"分组 —— Amos 在 557 个空间里占 507 个。
"""
import json, re, subprocess, sys, collections

MASTER = '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM'
CLOSED = ('Completed', 'Withdrawn', 'Substituted')

tab    = sys.argv[1]
suffix = sys.argv[2].upper()

raw = subprocess.run(['gws','sheets','spreadsheets','values','get','--params',
        json.dumps({"spreadsheetId": MASTER, "range": f"{tab}!A1:D400"})],
        capture_output=True, text=True).stdout
vals = json.loads(raw[raw.index('{'):]).get('values', [])

def norm(s): return re.sub(r'[^a-z]', '', s.lower())

status = {}
for r in vals[1:]:
    if len(r) > 1 and r[1].strip() and r[1].strip() != 'Example Row':
        status[norm(r[1])] = (r[3].strip() if len(r) > 3 else '')
print(f'{tab}: {len(status)} client rows')

rows = []
for n, dn, ms, e in json.load(open('members.json')):
    d = dn or ''
    m = re.search(r'\(([A-Za-z ]{1,3})\)\s*$', d.strip())
    if not m or m.group(1).strip().upper() != suffix:
        continue
    base = re.sub(r'\([^)]*\)\s*$', '', d)
    found = ''
    for p in re.split(r'[/\-–]', base):
        k = norm(p)
        if len(k) > 4 and k in status:
            found = status[k]; break
    rows.append((d, n, found))

act = [x for x in rows if x[2] and not any(z in x[2] for z in CLOSED)]
clo = [x for x in rows if x[2] and     any(z in x[2] for z in CLOSED)]
unm = [x for x in rows if not x[2]]

print(f'({suffix}) spaces: {len(rows)}')
for k, v in collections.Counter(x[2] or '<no match>' for x in rows).most_common():
    print(f'  {v:4d}  {k}')
print(f'\nACTIVE {len(act)} | CLOSED {len(clo)} | UNMATCHED {len(unm)}')
print('推荐范围 = ACTIVE + UNMATCHED =', len(act) + len(unm))
json.dump({'active': act, 'closed': clo, 'unmatched': unm}, open('a_split.json','w'))
print('-> a_split.json')
