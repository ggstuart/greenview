import greenview

ws = greenview.WebService()
#r = ws.GraemeLatestReading(213)
#d = ws.GraemeLatestReadingDate(213)
w = ws.GraemeLatestWeek(213)

#print r.to_json(indent=4)
#print d.to_json(indent=4)

#compact json
print w.to_json(separators=(',', ':'))

#pretty json
with open('output/output.json', 'w') as outfile:
    outfile.write(w.to_json(indent=4))

