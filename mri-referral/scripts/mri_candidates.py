#!/usr/bin/env python3
"""MRI center candidates for a client address.

Usage: python3 mri_candidates.py "<client street, city, CA zip>" [--days 365]

1. Preference: counts how many MRI referrals each imaging center received from
   claims@/piteam@/picase@/klaus@ (sent mail, subject contains MRI).
2. Distance: Places API (New) text search per center family, straight-line miles
   from the client address. Key in ~/.clinic-map.env (CLINIC_MAPS_API_KEY).
Prints both tables; the human picks the 3 (see SKILL.md Step 2).
"""
import json, os, sys, math, subprocess, collections, urllib.request

ADDR = sys.argv[1]
DAYS = int(sys.argv[sys.argv.index('--days') + 1]) if '--days' in sys.argv else 365
CENTERS = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'references', 'mri_centers.json')))

def gws(cfg, args):
    env = dict(os.environ)
    if cfg:
        env['GOOGLE_WORKSPACE_CLI_CONFIG_DIR'] = os.path.expanduser(cfg)
    r = subprocess.run(['gws'] + args, capture_output=True, text=True, env=env).stdout
    try:
        return json.JSONDecoder().raw_decode(r[r.find('{'):])[0]
    except Exception:
        return {}

def preference():
    c = collections.Counter()
    for cfg in ('~/.config/gws-claims', '~/.config/gws-piteam', '~/.config/gws-picase', None):
        ids, tok = [], None
        while True:
            p = {'userId': 'me', 'q': f'in:sent subject:MRI newer_than:{DAYS}d', 'maxResults': 100}
            if tok:
                p['pageToken'] = tok
            d = gws(cfg, ['gmail', 'users', 'messages', 'list', '--params', json.dumps(p)])
            ids += [m['id'] for m in d.get('messages', [])]
            tok = d.get('nextPageToken')
            if not tok or len(ids) > 500:
                break
        for i in ids:
            d = gws(cfg, ['gmail', 'users', 'messages', 'get', '--params', json.dumps(
                {'userId': 'me', 'id': i, 'format': 'metadata', 'metadataHeaders': ['To']})])
            to = ' '.join(h['value'] for h in d.get('payload', {}).get('headers', []) if h['name'] == 'To').lower()
            for fam in CENTERS:
                if any(dom in to for dom in fam['email_match']):
                    c[fam['family']] += 1
    return c

def env_key():
    for line in open(os.path.expanduser('~/.clinic-map.env')):
        if line.startswith('CLINIC_MAPS_API_KEY'):
            return line.split('=', 1)[1].strip().strip('"\'')

KEY = env_key()

def places(q, center=None):
    body = {'textQuery': q, 'maxResultCount': 5}
    if center:
        body['locationBias'] = {'circle': {'center': center, 'radius': 30000}}
    r = urllib.request.Request('https://places.googleapis.com/v1/places:searchText', data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json', 'X-Goog-Api-Key': KEY,
                 'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.location,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.businessStatus'})
    return json.load(urllib.request.urlopen(r)).get('places', [])

def miles(a, b):
    dl = math.radians(b['latitude'] - a['latitude']); dn = math.radians(b['longitude'] - a['longitude'])
    x = math.sin(dl / 2) ** 2 + math.cos(math.radians(a['latitude'])) * math.cos(math.radians(b['latitude'])) * math.sin(dn / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(x)) * 0.621

home = places(ADDR)[0]['location']
pref = preference()
print(f'# client {ADDR} -> {home}\n# referrals sent in last {DAYS}d by family:')
for fam in sorted(CENTERS, key=lambda f: -pref[f['family']]):
    print(f"\n## {fam['family']}  referrals={pref[fam['family']]}  lang={fam.get('language','?')}  email={fam['referral_email']}")
    for p in places(fam['search'], home):
        if p.get('businessStatus') != 'OPERATIONAL':
            continue
        print(f"  {miles(home, p['location']):5.1f} mi | {p['displayName']['text']} | {p['formattedAddress']} | {p.get('nationalPhoneNumber')} | {p.get('rating')}({p.get('userRatingCount')})")
