"""maintain json files with the latest week of data
    To be called regularly e.g. as a cron job
"""
import greenview, os.path
from datetime import datetime
import logging

class DateRecord(object):
    """represents a file on disk with a simple list of dates"""
    def __init__(self, fileName, max_len=None):
        """read file into data array"""
        self.max_len = max_len
        self.format = "%d/%m/%Y %H:%M:%S"
        self.filename = fileName
        self.data = []
        if os.path.exists(self.filename):
            from csv import reader as rdr
            with open(self.filename, 'r') as date_file:
                reader = rdr(date_file)
                for row in reader:
                    self.data.append(datetime.strptime(row[0], self.format))

    def updateFile(self, date):
        """Add a date to the end of the array and write all back to file"""
        from csv import writer as wtr
        self.data.append(date)
        if self.max_len is not None:
            while len(self.data) > self.max_len:
                self.data = self.data[1:]
            
        with open(self.filename, 'w') as date_file:
            writer = wtr(date_file)
            for record in self.data:
                writer.writerow([datetime.strftime(record, self.format)])

    def latestDownload(self):
        """return the latest date downloaded"""
        try:
            return self.data[-1]
        except IndexError:
            return None

def maintain(root, meter_id):
    dateFile = os.path.join(root, 'date_%04i.csv' % meter_id)
    ws = greenview.WebService()
    dr = DateRecord(dateFile, max_len=1)
    latest_in_file = dr.latestDownload()
    latest_on_server = ws.GraemeLatestReadingDate(meter_id).datetime
    if not latest_in_file or (latest_in_file < latest_on_server):
        print 'downloading %04i...' % meter_id,
        w = ws.GraemeLatestWeek(meter_id)
        dataFile = os.path.join(root, 'data_%04i.json' % meter_id)
        with open(dataFile, 'w') as outfile:
            outfile.write(w.to_json(separators=(',', ':')))
        dr.updateFile(latest_on_server)
        print 'ok'
    else:
        print '%04i already downloaded (%s)' % (meter_id, latest_in_file)

def main(root):
    logging.basicConfig(filename=os.path.join(root, 'update.log'), level=logging.INFO, format='%(levelname)s: %(asctime)s %(message)s')
    logging.info('Started')
    try:    
        for meter_id in [213, 69, 111, 15, 490]:
            maintain(root, meter_id)
    except greenview.ServerError, e:
        logging.error(e.message)
    logging.info('Finished')
    
if __name__ == "__main__":    
    root = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(root): os.makedirs(root)
    main(root)
