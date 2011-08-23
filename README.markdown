Python library for accessing Greenview web service
=============

Installation
-------

Download the source and run

python setup.py install

OR, Download and run the [windows installer](https://github.com/ggstuart/greenview/archives/master "Windows installer").


Usage
-------

Two fairly trivial examples of using the webservice are provided in the examples module.

The plotting.py script uses matplotlib (which you may need to install) to plot a weeks data for five buildings.
The update.py module can be run as a script to generate json files for five buildings or use the greenview.maintain() function in your own script.

Very simple example
-------

import greenview

ws = greenview.WebService()
r = ws.GraemeLatestReading(213)
d = ws.GraemeLatestReadingDate(213)
w = ws.GraemeLatestWeek(213)

print r.to_json(indent=4)
print d.to_json(indent=4)

#compact json
print w.to_json(separators=(',', ':'))

#pretty json dumped into a file
with open('output/output.json', 'w') as outfile:
    outfile.write(w.to_json(indent=4))

