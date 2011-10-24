Python library for accessing Greenview web service
=============

Installation
-------

Download the latest source and run

    python setup.py install

OR, Download and run the [windows installer](https://github.com/ggstuart/greenview/archives/master "Windows installer").


Usage
-------

The [gvUpdate](https://github.com/ggstuart/gvUpdate "gvUpdate") project provides a script generate json files for five buildings.

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

