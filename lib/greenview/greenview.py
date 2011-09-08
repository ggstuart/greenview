from urllib2 import urlopen, HTTPError
from xml.dom.minidom import parse
import datetime, time, math
from numpy import array, arange, diff, interp
import logging, json

class Error(Exception): pass
class ServerError(Error): pass

def dateHandler(obj):
    if type(obj).__name__ == 'datetime':
        return obj.strftime("%d/%m/%Y %H:%M:%S")
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj))

class WebService(object):
    
    def __init__(self, base_url = 'http://duall.iesd.dmu.ac.uk/1010buildings/DuallWebService.asmx/'):
        self.base_url = base_url
        self.data = {}

    def getDocument(self, cmd, force):
        """Main generic interface, gets a file"""
        logging.debug('WebService.getDocument(%s, %s)' % (cmd, force))
        has_key = self.data.has_key(cmd)
        if (not has_key or force):
            logging.debug('Requesting %s' % cmd)
            try:
                xml = urlopen("%s%s" % (self.base_url, cmd))
                dom = parse(xml)
                xml.close()
                self.data[cmd] = dom
            except HTTPError, e:
                logging.error('Request failed (%s)' % (cmd, e))
                raise ServerError(e)
        return self.data[cmd]

    def gGetBuildingMeters(self, force=False):
        """Specific to getting meters data, passes file to specific object for data extraction"""
        dom = self.getDocument('gGetBuildingMeters', force)
        return gGetBuildingMeters(dom)

    def GraemeLatestReading(self, meter_id, force=False):
        cmd = 'GraemeLatestReading?meter_id=%s' % meter_id
        dom = self.getDocument(cmd, force)
        return GraemeLatestReading(dom)

    def GraemeLatestReadingDate(self, meter_id, force=False):
        cmd = 'GraemeLatestReadingDate?meter_id=%s' % meter_id
        dom = self.getDocument(cmd, force)
        return GraemeLatestReadingDate(dom)


    def GraemeLatestWeek(self, meter_id, inclusive=True, force=False):
        cmd = 'GraemeLatestWeek?meter_id=%s&inclusive=%s' % (meter_id, inclusive)
        dom = self.getDocument(cmd, force)
        return GraemeLatestWeek(dom)

    def Meter(self, meter_id, force=False):
        cmd = 'Meter?Meter_ID=%s' % meter_id
        dom = self.getDocument(cmd, force)
        return Meter(dom)

class Meter(object):
    def __init__(self, dom):
        meter = dom.getElementsByTagName('Meter')[0]
        self.id = meter.getElementsByTagName('Meter_ID')[0].childNodes[0].data.encode('ascii')
        self.units = meter.getElementsByTagName('Units')[0].childNodes[0].data.encode('ascii')
#        self.name = meter.getElementsByTagName('Meter_Name')[0].childNodes[0].data.encode('ascii')
        self.description = meter.getElementsByTagName('Meter_Description')[0].childNodes[0].data.encode('ascii')

class GraemeLatestWeek(object):
    def __init__(self, dom):
        self.datetime = []
        self.value = []
        for reading in dom.getElementsByTagName('reading'):
            self.datetime.append(datetime.datetime.strptime(reading.getElementsByTagName("datetime")[0].childNodes[0].data, "%d/%m/%Y %H:%M:%S"))
            self.value.append(reading.getElementsByTagName("value")[0].childNodes[0].data)

    def data(self, interpolated=True, consumption=True):
        data = {'datetime': self.datetime, 'value': self.value}
        if interpolated:
            resolution = 30*60  #half hourly
            dt = data['datetime']
            readings = data['value']
            ts = array([time.mktime(d.timetuple()) for d in dt])
            last = math.floor(max(ts)/resolution)*resolution
            first = last - 7*24*60*60
            new_ts = arange(first, last+1, resolution, dtype=float)
            if len(new_ts) != 337:
                print len(new_ts)
                raise Exception('Web service is not providing enough data to generate a week of consumption data')
            new_dt = [datetime.datetime.fromtimestamp(s) for s in new_ts]
            new_readings = interp(new_ts, ts, readings)
            data = {'datetime': new_dt, 'value': new_readings}
        if consumption:
            cons = diff(data['value'])
            dt = data['datetime'][1:]
            data = {'datetime': dt, 'value': cons}
        return data

    def to_json(self, interpolated=True, consumption=True, **kwargs):

        data = self.data(interpolated=interpolated, consumption=consumption)
        result = []
        for i in xrange(len(data['datetime'])):
            result.append({'datetime': data['datetime'][i], 'value': data['value'][i]})
        return json.dumps(result, default=dateHandler, **kwargs)

class GraemeLatestReading(object):
    def __init__(self, dom):
        self.data = {}
        reading = dom.getElementsByTagName('reading')[0]
        self.data['datetime'] = datetime.datetime.strptime(reading.getElementsByTagName("datetime")[0].childNodes[0].data, "%d/%m/%Y %H:%M:%S")
        self.data['value'] = reading.getElementsByTagName("value")[0].childNodes[0].data

    def to_json(self, **kwargs):
        return json.dumps(self.data, default=dateHandler, **kwargs)

class GraemeLatestReadingDate(object):
    def __init__(self, dom):
        self.datetime = datetime.datetime.strptime(dom.getElementsByTagName("datetime")[0].childNodes[0].data, "%d/%m/%Y %H:%M:%S")

    def to_json(self, **kwargs):
        return json.dumps(self.datetime, default=dateHandler, **kwargs)
        
class gGetBuildingMeters(object):
    def __init__(self, dom):
        self.data = []
        meters = dom.getElementsByTagName('Meter')
        for m in meters:
            record = {}
            record['Meter_ID'] = m.getElementsByTagName('Meter_ID')[0].childNodes[0].data.encode('ascii')
            record['Meter_Name'] = m.getElementsByTagName('Meter_Name')[0].childNodes[0].data.encode('ascii')
            dt = datetime.datetime.strptime(m.getElementsByTagName("DateTime")[0].childNodes[0].data, "%d/%m/%Y %H:%M:%S")
            increment = datetime.timedelta(minutes = -30)
            readings = [float(m.getElementsByTagName("Reading%s" % (i+1))[0].childNodes[0].data.encode('ascii')) for i in range(8)]
            readings.reverse()
            record['Readings'] = []
            for i in range(8):
                reading = {}
                reading['timestamp'] = dt+increment*i
                reading['value'] = readings[i]
                record['Readings'].append(reading)
            record['Readings'].reverse()
            self.data.append(record)

    def to_json(self, **kwargs):
        return json.dumps(self.data, default=dateHandler, **kwargs)

    def to_xml(self):
        return "<Meters>\n\t%s\n</Meters>" % "\n\t".join(['<Meter id="%s">%s\n\t</Meter>' % (m['Meter_ID'], '\n\t\t<Name>%s</Name>\n\t\t<Readings>\n\t\t\t%s\n\t\t</Readings>' % (m['Meter_Name'], '\n\t\t\t'.join(['<Reading timestamp="%s">\n\t\t\t\t<Value>%s</Value>\n\t\t\t</Reading>' % (r['timestamp'].isoformat(), r['value']) for r in m['Readings']]))) for m in self.data])

