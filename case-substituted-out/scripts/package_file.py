#!/usr/bin/env python3
"""
Build the client-file delivery package for case-substituted-out.

  1. mirror the Drive case folder locally, applying the exclusions
  2. zip it
  3. report the BASE64-ENCODED size against Gmail's 25 MB limit
  4. optionally mirror the same package into a `Case Sub` folder inside the case
     folder in Drive (server-side files.copy -- byte identical, no re-upload)

gws refuses to write outside the current working directory, so the local mirror
always runs with relative paths from inside the destination.

    python3 package_file.py <CASE_FOLDER_ID> --dest ~/Downloads/"<Client> - Substitution Out"
    python3 package_file.py <CASE_FOLDER_ID> --dest ... --drive-mirror
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

# Internal records that never go to successor counsel.
EXCLUDE_PATTERNS = [
    r'Intake Sheet',        # our case-management sheet: SSN + internal workflow checklist
    r'Intake Responses',    # raw intake capture
]

GOOGLE_EXPORT = {
    'application/vnd.google-apps.document':
        ('application/pdf', '.pdf'),
    'application/vnd.google-apps.spreadsheet':
        ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
}


def gws(*args) -> dict:
    r = subprocess.run(['gws', *args], capture_output=True, text=True)
    out = r.stdout
    if '{' not in out:
        raise RuntimeError((r.stderr or out)[-500:])
    return json.loads(out[out.index('{'):])


def ls(folder_id: str) -> list[dict]:
    return gws('drive', 'files', 'list', '--params', json.dumps({
        'q': f"'{folder_id}' in parents and trashed=false",
        'fields': 'files(id,name,mimeType)', 'pageSize': 200,
        'includeItemsFromAllDrives': True, 'supportsAllDrives': True,
        'corpora': 'allDrives'})).get('files', [])


def excluded(name: str) -> bool:
    return any(re.search(p, name, re.I) for p in EXCLUDE_PATTERNS)


def safe(name: str) -> str:
    return re.sub(r'[/\x00]', '_', name)


# ---------------------------------------------------------------- local mirror

def mirror_local(folder_id: str, dest: str) -> tuple[int, int, list[str]]:
    os.makedirs(dest, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(dest)                      # gws will not write above cwd
    kept, skipped = [], []
    total = [0]

    def walk(fid: str, rel: str):
        os.makedirs(rel, exist_ok=True) if rel else None
        for f in ls(fid):
            name = safe(f['name'])
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                walk(f['id'], os.path.join(rel, name) if rel else name)
                continue
            if excluded(name):
                skipped.append(os.path.join(rel, name) if rel else name)
                continue
            out = os.path.join(rel, name) if rel else name
            if f['mimeType'] in GOOGLE_EXPORT:
                mime, ext = GOOGLE_EXPORT[f['mimeType']]
                if not out.endswith(ext):
                    out += ext
                p = json.dumps({'fileId': f['id'], 'mimeType': mime,
                                'supportsAllDrives': True})
                subprocess.run(['gws', 'drive', 'files', 'export', '--params', p,
                                '--output', out], capture_output=True, text=True)
            else:
                p = json.dumps({'fileId': f['id'], 'alt': 'media',
                                'supportsAllDrives': True})
                subprocess.run(['gws', 'drive', 'files', 'get', '--params', p,
                                '--output', out], capture_output=True, text=True)
            if os.path.exists(out) and os.path.getsize(out) > 0:
                kept.append(out); total[0] += os.path.getsize(out)
            else:
                print(f'  !! failed: {out}', file=sys.stderr)

    walk(folder_id, '')
    os.chdir(cwd)
    return len(kept), total[0], skipped


# ---------------------------------------------------------------- drive mirror

def mirror_drive(case_folder_id: str) -> str:
    """Create `Case Sub/Client File` inside the case folder and server-side copy
    everything (minus exclusions) into it. Returns the Case Sub folder id."""
    def mkdir(name, parent):
        for f in ls(parent):
            if f['name'] == name and f['mimeType'].endswith('folder'):
                return f['id']
        return gws('drive', 'files', 'create',
                   '--params', json.dumps({'supportsAllDrives': True}),
                   '--json', json.dumps({
                       'name': name,
                       'mimeType': 'application/vnd.google-apps.folder',
                       'parents': [parent]}))['id']

    sub = mkdir('Case Sub', case_folder_id)
    cf = mkdir('Client File', sub)

    def walk(src, dst):
        for f in ls(src):
            if f['mimeType'].endswith('folder'):
                if f['name'] == 'Case Sub':
                    continue
                walk(f['id'], mkdir(f['name'], dst))
            elif not excluded(f['name']):
                gws('drive', 'files', 'copy',
                    '--params', json.dumps({'fileId': f['id'], 'supportsAllDrives': True}),
                    '--json', json.dumps({'name': f['name'], 'parents': [dst]}))

    walk(case_folder_id, cf)
    return sub


# ---------------------------------------------------------------- zip + sizing

def build_zip(dest: str, client: str) -> str:
    src = os.path.join(dest, 'Client File')
    zip_path = os.path.join(dest, f'{client} - Client File.zip')
    if os.path.exists(zip_path):
        os.remove(zip_path)
    subprocess.run(['zip', '-r', '-q', zip_path, 'Client File',
                    '-x', '.*', '-x', '__MACOSX/*'], cwd=dest, check=True)
    return zip_path


def size_report(zip_path: str, letters: list[str]) -> bool:
    """Gmail's 25 MB cap applies AFTER base64, which inflates by 4/3.
    Returns True if it fits as a direct attachment."""
    def enc(b):  # base64 expansion
        return b * 4 / 3

    raw = os.path.getsize(zip_path)
    total = enc(raw) + sum(enc(os.path.getsize(p)) for p in letters if os.path.exists(p))
    total += 20_000  # headers + body
    mb = 1024 * 1024
    print(f'  zip          {raw/mb:7.1f} MB raw  -> {enc(raw)/mb:7.1f} MB encoded')
    for p in letters:
        if os.path.exists(p):
            s = os.path.getsize(p)
            print(f'  {os.path.basename(p)[:38]:38} {s/mb:5.2f} MB -> {enc(s)/mb:5.2f} MB')
    print(f'  ---- email total {total/mb:.1f} MB   (Gmail limit 25 MB)')
    fits = total < 25 * mb
    print('  verdict:', 'ATTACH THE ZIP DIRECTLY' if fits else
          'TOO BIG -- Klaus must put it on Dropbox and give you the link')
    print('  letter enclosure line must read:',
          '"Client file (electronic copy)"' if fits else '"Client file (secure link)"')
    return fits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case_folder_id')
    ap.add_argument('--dest', required=True, help='local staging dir')
    ap.add_argument('--client', default=None, help='client name for the zip filename')
    ap.add_argument('--letters', nargs='*', default=[], help='letter PDFs to size alongside')
    ap.add_argument('--drive-mirror', action='store_true',
                    help='also build Case Sub/Client File inside the Drive case folder')
    a = ap.parse_args()

    dest = os.path.expanduser(a.dest)
    client = a.client or os.path.basename(dest.rstrip('/')).split(' - ')[0]

    n, total, skipped = mirror_local(a.case_folder_id, os.path.join(dest, 'Client File'))
    print(f'mirrored {n} files, {total/1048576:.1f} MB')
    if skipped:
        print('EXCLUDED (internal, not handed over):')
        for s in skipped:
            print('   -', s)

    zp = build_zip(dest, client)
    print(f'\nzip: {zp}')
    size_report(zp, [os.path.expanduser(p) for p in a.letters])

    if a.drive_mirror:
        sub = mirror_drive(a.case_folder_id)
        print(f'\nDrive Case Sub: https://drive.google.com/drive/folders/{sub}')
        print('Upload the letter PDFs into that folder, then have Klaus verify before sending.')


if __name__ == '__main__':
    main()
