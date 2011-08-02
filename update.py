"""maintain json files with the latest week of data
    To be called regularly e.g. as a cron job
"""
import greenview, csv, datetime, os.path
ws = greenview.WebService()

class DateRecord(object):
    """represents a file on disk with a simple list of dates"""
    def __init__(self, fileName):
        """read file into data array"""
        self.format = "%d/%m/%Y %H:%M:%S"
        self.filename = fileName
        self.data = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as date_file:
                reader = csv.reader(date_file)
                for row in reader:
                    self.data.append(datetime.datetime.strptime(row[0], self.format))

    def updateFile(self, date):
        """Add a date to the end of the array and write all back to file"""
        self.data.append(date)
        with open(self.filename, 'w') as date_file:
            writer = csv.writer(date_file)
            for record in self.data:
                writer.writerow([datetime.datetime.strftime(record, self.format)])

    def latestDownload(self):
        """return the latest date downloaded"""
        try:
            return self.data[-1]
        except IndexError:
            return None


def maintain(root, meter_id):
    dr = DateRecord(os.path.join(root, 'date%s.csv' % meter_id))
    latest_in_file = dr.latestDownload()
    latest_on_server = ws.GraemeLatestReadingDate(meter_id).datetime
    if not latest_in_file or (latest_in_file < latest_on_server):
        print 'downloading %s...' % meter_id,
        w = ws.GraemeLatestWeek(meter_id)
        dataFile = os.path.join(root, 'data%s.json' % meter_id)
        with open(dataFile, 'w') as outfile:
            outfile.write(w.to_json(separators=(',', ':')))
        dr.updateFile(latest_on_server)
        print 'ok'

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), 'data')
    for meter_id in [213, 69, 111, 15, 490]:
        maintain(root, meter_id)


