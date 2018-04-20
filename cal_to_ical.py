from yaml import load
from icalendar import *
import pytz, datetime, re

link = re.compile(r'\[([^\]]*)\]\(([^\)]*)\)')
def deMd(s):
    return link.sub(r'\1 (\2)', s.replace('`', ''))

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def fixworking():
    """change to this script's directory as the working directory"""
    import os, os.path
    os.chdir(os.path.realpath(os.path.dirname(__file__)))

eastern = pytz.timezone('America/New_York')

class RealCal:
    def __init__(self, name):
        self.name = name
        self.cal = Calendar()
        self.cal.add('prodid', '-//University of Virginia//'+name+'//EN')
        self.cal.add('calscale', 'GREGORIAN')
        self.cal.add('version', '2.0')
        self.cal.add('name', name)
    def event(self, name, start, duration=None, location=None, end=None, details=None):
        e = Event()
        e.add('dtstamp', datetime.datetime.now(tz=eastern))
        e.add('uid', name+start.isoformat()[:20].rstrip('0:T-'))
        e.add('dtstart', start)
        if end is not None: e.add('dtend', end)
        elif duration is not None: e.add('dtend', start+duration)
        e.add('summary', name)
        if location is not None: e.add('location', location)
        if details is not None: e.add('description', details)
        self.cal.add_component(e)
    def __str__(self):
        return self.cal.to_ical().decode('utf-8').replace('\r\n','\n').strip()
    def bytes(self):
        return self.cal.to_ical()

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def calendar(data):
    ans = RealCal('cs1110.s2018')

    m50 = datetime.timedelta(0, 50*60)
    m75 = datetime.timedelta(0, 75*60)
    m180 = datetime.timedelta(0, 180*60)
    m5 = datetime.timedelta(0, 5*60)
    
    breaks = []
    exams = {}
    for k,v in data['Special Dates'].items():
        if 'recess' in k or 'break' in k or 'Reading' in k:
            if type(v) is dict: breaks.append((v['start'], v['end']))
            else: breaks.append((v, v))
        elif 'xam' in k:
            exams[v] = k

    
    oneday = datetime.timedelta(1)
    d = data['Special Dates']['Courses begin']
    classnum = 0
    while d < data['Special Dates']['Courses end']:
        if not any(d >= b[0] and d <= b[1] for b in breaks):
            if d.weekday() in (1,3):
                sec001 = datetime.datetime(d.year, d.month, d.day, 14, 0, 0, tzinfo=eastern)

                topic = exams.get(d, data['classes'][classnum])
#                if topic in data['reading']: topic = deMd(topic) + '\r\nSee '+deMd(' and '.join(' and '.join(data['reading'][_]) for _ in topic)) +' for more'
 #               else: topic = deMd(topic)
                if d not in exams: classnum += 1

                ans.event('4810', sec001, m75, location='THN E316', details=topic)
        d += oneday
    
    e3 = data['Special Dates']['Final Exam']
    ans.event('Final Quiz', datetime.datetime(e3.year, e3.month, e3.day, 9, 0, 0, tzinfo=eastern), m180, location='THN E316')
    
    for a,v in data['assignments'].items():
        if a.lower().startswith('lab') or v.get('group','').lower() == 'lab': continue
        if 'due' not in v: continue
        d = v['due']
        if not isinstance(d, datetime.datetime):
            d = datetime.datetime(d.year, d.month, d.day, 23 if v.get('group') == 'project' else 9, 55, 0, tzinfo=eastern)
            ans.event(a+' due', d, m5)
            
    
    return ans



if __name__ == '__main__':
    fixworking()
    with open('markdown/cal.yaml') as stream:
        data = load(stream, Loader=Loader)
    cal = calendar(data)
    with open('markdown/cal.ics', 'wb') as f:
        f.write(cal.bytes())
