import greenview

ws = greenview.WebService()
m = ws.gGetBuildingMeters()

#compact json
print m.to_json(separators=(',', ':'))

#pretty json
with open('output.json', 'w') as outfile:
    outfile.write(m.to_json(indent=4))

#xml
with open('output.xml', 'w') as outfile:
    outfile.write(m.to_xml())

