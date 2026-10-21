"""green_cells.py J8 DF15 ...   -> paints those 'Internal ' cells #00ff00 (repeatCell)."""
import json,subprocess,re,sys
SID="1Av8_fj3MAekCM6RujmGWuFsYRnSG6MMbAskvPkFcs2U"; SHEET=1554087303
def parse(a):
    m=re.match(r'([A-Z]+)(\d+)$',a); col=0
    for ch in m.group(1): col=col*26+ord(ch)-64
    return int(m.group(2))-1, col-1
reqs=[]
for a in sys.argv[1:]:
    r,c=parse(a)
    reqs.append({"repeatCell":{"range":{"sheetId":SHEET,"startRowIndex":r,"endRowIndex":r+1,"startColumnIndex":c,"endColumnIndex":c+1},
      "cell":{"userEnteredFormat":{"backgroundColor":{"red":0,"green":1,"blue":0}}},"fields":"userEnteredFormat.backgroundColor"}})
p=subprocess.run(["gws","sheets","spreadsheets","batchUpdate","--params",json.dumps({"spreadsheetId":SID}),"--json",json.dumps({"requests":reqs})],capture_output=True,text=True)
print("replies:",p.stdout.count('{}'),"of",len(reqs))
