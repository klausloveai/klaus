"""read_pending.py "<tab>" ["<tab>" ...]  -> dumps A1:F45 of each Pending Disbursed tab with colors (G/Y/W/O).
Matches by sheet title (API returns sheets in index order, not request order)."""
import json,subprocess,sys
SID="1b_vPr9WD7P9arR6DTTJRxeWs0apk8DTiTgc2iAzIrR0"
params={"spreadsheetId":SID,"ranges":[f"'{t}'!A1:F45" for t in sys.argv[1:]],"includeGridData":True,
        "fields":"sheets(properties(sheetId,title),data.rowData.values(formattedValue,effectiveFormat.backgroundColor))"}
o=subprocess.run(["gws","sheets","spreadsheets","get","--params",json.dumps(params)],capture_output=True,text=True).stdout
d=json.loads(o[o.find('{'):])
def col(b):
    if not b: return '.'
    g=(b.get('red',0),b.get('green',0),b.get('blue',0))
    return {(0,1,0):'G',(1,1,0):'Y',(1,1,1):'W'}.get(g,'O')
for s in d['sheets']:
    p=s['properties']; print('=====',p['title'],'sheetId',p['sheetId'])
    for i,row in enumerate(s['data'][0].get('rowData',[])):
        line=' | '.join((c.get('formattedValue') or '')+'['+col(c.get('effectiveFormat',{}).get('backgroundColor'))+']' for c in row.get('values',[]))
        if line.replace('[.]','').replace('[W]','').replace('|','').strip(): print(' ',i+1,line)
