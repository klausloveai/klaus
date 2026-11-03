#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diff a local exhibit tree against a Drive folder, both directions.
Usage: drive_diff.py <LOCAL_ROOT> <DRIVE_FOLDER_ID>"""
import os,sys,json,subprocess,unicodedata as u
def gws(a):
    r=subprocess.run(['gws','drive']+a,capture_output=True,text=True)
    o=r.stdout; i=o.find('{'); return json.loads(o[i:]) if i>=0 else {}
def ls(pid):
    out=[];tok=None
    while True:
        p={"q":f"'{pid}' in parents and trashed=false","supportsAllDrives":True,
           "includeItemsFromAllDrives":True,"fields":"nextPageToken,files(id,name,mimeType)","pageSize":200}
        if tok: p["pageToken"]=tok
        d=gws(['files','list','--params',json.dumps(p)])
        out+=d.get('files',[]); tok=d.get('nextPageToken')
        if not tok: return out
def main(root,fid):
    drive=set(); st=[(fid,'')]
    while st:
        pid,pre=st.pop()
        for f in ls(pid):
            p=(pre+'/'+f['name']).lstrip('/')
            if f['mimeType'].endswith('folder'): st.append((f['id'],p)); drive.add(p+'/')
            else: drive.add(p)
    loc=set()
    for dp,dns,fns in os.walk(root):
        dns[:]=[x for x in dns if x!='_DISCARDED']
        if '_DISCARDED' in dp: continue
        for x in dns: loc.add(os.path.relpath(os.path.join(dp,x),root)+'/')
        for x in fns:
            if x!='.DS_Store': loc.add(os.path.relpath(os.path.join(dp,x),root))
    n=lambda s:{u.normalize('NFC',x) for x in s}
    D,L=n(drive),n(loc)
    print(f'--- Drive 有、本地无 ({len(D-L)}) ---')
    for x in sorted(D-L): print('  D>',x)
    print(f'--- 本地有、Drive 无 ({len(L-D)}) ---')
    for x in sorted(L-D): print('  L>',x)
if __name__=='__main__': main(sys.argv[1],sys.argv[2])
