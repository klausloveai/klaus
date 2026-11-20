#!/usr/bin/env python3
"""RingCentral 入站传真：列出未处理的新传真并下载 PDF + 渲染 PNG；处理完按规则在 RingCentral 标已读。
用法：
  rc_inbox.py new [--days 14] --out <dir>     列出未处理的入站传真，下载到 <dir>，打印 JSON
  rc_inbox.py mark <message_id> <status> [note]   记一份为已处理（status: filed / unclaimed / skipped_spam / misdirected / duplicate / error）
                                                  filed / duplicate 自动在 RingCentral 标已读；其余保持未读等 Klaus 看
  rc_inbox.py read <message_id>                   只把一份标已读（补标用）
凭据：~/.ringcentral.env（JWT，不入库）。已处理记录：~/.claude/automation/fax-intake/state/processed.json
"""
import sys, os, json, datetime, subprocess, urllib.request
sys.path.insert(0, os.path.expanduser('~/.claude/skills/send-fax/scripts'))
import rc_fax
STATE = os.path.expanduser('~/.claude/automation/fax-intake/state/processed.json')

def load_state():
    try: return json.load(open(STATE))
    except Exception: return {}

def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, 'w'), ensure_ascii=False, indent=1)

def cmd_new(days, out):
    env = rc_fax.load_env(os.path.expanduser('~/.ringcentral.env'))
    server, tok = rc_fax.get_token(env)
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime('%Y-%m-%dT00:00:00Z')
    url = server + f'/restapi/v1.0/account/~/extension/~/message-store?messageType=Fax&direction=Inbound&dateFrom={since}&perPage=100'
    recs = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={'Authorization': 'Bearer ' + tok})).read()).get('records', [])
    done = load_state(); os.makedirs(out, exist_ok=True); res = []
    for r in sorted(recs, key=lambda x: x['creationTime']):
        mid = str(r['id'])
        if mid in done: continue
        f = r.get('from', {}); pdfs = []
        for i, a in enumerate(r.get('attachments', [])):
            data = urllib.request.urlopen(urllib.request.Request(a['uri'], headers={'Authorization': 'Bearer ' + tok})).read()
            p = os.path.join(out, f'fax_{mid}_{i}.pdf'); open(p, 'wb').write(data)
            subprocess.run(['pdftoppm', '-r', '80', '-png', p, p[:-4]], check=False)
            pdfs.append(p)
        res.append({'message_id': mid, 'received': r['creationTime'], 'pages': r.get('faxPageCount'),
                    'from_number': f.get('phoneNumber'), 'from_name': (f.get('name') or '').strip(),
                    'to_number': (r.get('to') or [{}])[0].get('phoneNumber'), 'pdfs': pdfs})
    print(json.dumps(res, ensure_ascii=False, indent=1))

AUTO_READ = {'filed', 'duplicate'}  # Klaus 11/20：归档并核对 MD5 / 重复件原件已归档 → 标已读；待认领、发错人、出错 → 留未读

def set_read(mid):
    env = rc_fax.load_env(os.path.expanduser('~/.ringcentral.env'))
    server, tok = rc_fax.get_token(env)
    url = server + f'/restapi/v1.0/account/~/extension/~/message-store/{mid}'
    req = urllib.request.Request(url, data=json.dumps({'readStatus': 'Read'}).encode(), method='PUT',
                                 headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read()).get('readStatus')

def cmd_mark(mid, status, note=''):
    s = load_state(); rec = {'status': status, 'note': note, 'at': datetime.datetime.now().isoformat(timespec='minutes')}
    if status in AUTO_READ:
        try: rec['rc_read'] = set_read(mid)
        except Exception as e: rec['rc_read'] = f'error: {e}'
    else:
        rec['rc_read'] = 'kept unread'
    s[str(mid)] = rec; save_state(s); print('marked', mid, status, '| RingCentral:', rec['rc_read'])

def cmd_read(mid):
    s = load_state(); st = set_read(mid)
    if str(mid) in s: s[str(mid)]['rc_read'] = st; save_state(s)
    print('read', mid, st)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'new':
        days = int(a[a.index('--days') + 1]) if '--days' in a else 14
        cmd_new(days, a[a.index('--out') + 1])
    elif a and a[0] == 'mark' and len(a) >= 3:
        cmd_mark(a[1], a[2], ' '.join(a[3:]))
    elif a and a[0] == 'read' and len(a) == 2:
        cmd_read(a[1])
    else:
        print(__doc__); sys.exit(1)
