import json

v = float(input("new version num:"))
with open("./.config/setups.json", 'rb') as f:
    params = json.load(f)
    dictv = params
dictv['version'] = v
tojson = json.dumps(dictv)
savejson = open('./.config/setups.json', 'w')
savejson.write(tojson)
savejson.close()
print("Successful!")