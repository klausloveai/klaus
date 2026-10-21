"""Fetch 'Internal ' tab (A1:FZ320) with formatted values + background colors -> JSON file."""
import json,subprocess,sys
params={"spreadsheetId":"1Av8_fj3MAekCM6RujmGWuFsYRnSG6MMbAskvPkFcs2U",
        "ranges":["Internal !A1:FZ320"],"includeGridData":True,
        "fields":"sheets.data.rowData.values(formattedValue,effectiveFormat.backgroundColor)"}
r=subprocess.run(["gws","sheets","spreadsheets","get","--params",json.dumps(params)],capture_output=True,text=True)
o=r.stdout; json.dump(json.loads(o[o.find('{'):]),open(sys.argv[1],'w')); print("ok")
