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

def dow(n):
    if type(n) is int: return n
    n = n.lower()
    if n.startswith('mo') or n == 'm': return 0
    if n.startswith('tu') or n == 't': return 1
    if n.startswith('we') or n == 'w': return 2
    if n.startswith('th') or n == 'h': return 3
    if n.startswith('fr') or n == 'f': return 4
    if n.startswith('sa') or n == 's': return 5
    if n.startswith('su') or n == 'u': return 6
    raise Exception("Unknown weekday: "+str(n))


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
        e.add('dtstamp', datetime.datetime.now(tz=start.tzinfo))
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
    name = data['meta']['name']
    month = data['Special Dates']['Courses begin'].month
    year = data['Special Dates']['Courses begin'].year
    finalurl = 'http://www.virginia.edu/registrar/exams.html#1{}{}'.format(year%100, month)
    calname = '{}.{}{}'.format(data['meta']['name'], ('S' if month < 5 else 'Su' if  month < 8 else 'F'), year)
    ans = RealCal(calname.lower())
    
    print(data['sections'])
    
    tz = pytz.timezone(data['meta'].get('timezone', 'America/New_York'))

    for sec in data['sections']:
        data['sections'][sec]['duration'] = datetime.timedelta(0, data['sections'][sec]['duration']*60)
        data['sections'][sec]['days'] = [dow(_) for _ in data['sections'][sec]['days']]
        if 'start' in data['sections'][sec]:
            data['sections'][sec]['hour'] = data['sections'][sec]['start'] // 60
            data['sections'][sec]['min'] = data['sections'][sec]['start'] % 60

    m5 = datetime.timedelta(0, 5*60)
    
    breaks = []
    exams = {}
    for k,v in data['Special Dates'].items():
        if 'recess' in k or 'break' in k or 'Reading' in k:
            if type(v) is dict: breaks.append((v['start'], v['end']))
            else: breaks.append((v, v))
        elif 'xam' in k or 'uiz' in k:
            exams[v] = k

    
    oneday = datetime.timedelta(1)
    d = data['Special Dates']['Courses begin']
    classnum = 0
    while d < data['Special Dates']['Courses end']:
        isclass = False
        if not any(d >= b[0] and d <= b[1] for b in breaks):
            for sname, sdat in data['sections'].items():
                if d.weekday() in sdat['days']:
                    start = datetime.datetime(d.year, d.month, d.day, sdat['hour'], sdat['min'], 0, tzinfo=tz)
                    if sdat['type'] == 'lecture':
                        isclass = True
                        topic = data['classes'][classnum] if classnum < len(data['classes']) else ''
                        if data['meta'].get('lecture exam',True):
                            topic = exams.get(d, topic)
                            isclass = d not in exams
                        if type(topic) is list:
                            topic = ' and '.join(topic)
                        ans.event(sname, start, sdat['duration'], location=sdat['room'], details=topic)
                    else:
                        ... # non-lecture currently handled elsewhere
        if isclass: classnum += 1
        d += oneday
    
    ended=d

    for e in exams:
        if e >= ended:
            ans.event(
                exams[e],
                datetime.datetime(e.year, e.month, e.day, data['meta']['final']['start'].hour, data['meta']['final']['start'].minute, 0, tzinfo=tz),
                datetime.timedelta(0, data['meta']['final']['duration']*60),
                location=data['meta']['final']['room']
            )
        elif not data['meta'].get('lecture exam',True):
            for sname, sdat in data['sections'].items():
                if sdat.get('type') == 'lab':
                    offby = max((abs(_+3),_) for _ in [e.weekday() - d for d in sdat['days']])[1]
                    d = e
                    d = datetime.datetime(d.year, d.month, d.day, sdat['start'] // 60, sdat['start'] % 60, 0, tzinfo=tz)
                    d -= datetime.timedelta(offby,0,0)
                    ans.event(exams[e] + '('+sname+')', d, sdat['duration'], location=sdat['room'], details=exams[e]+' for ' + sname)
                    
    
    for a,v in data['assignments'].items():
        if a.startswith('.'): continue
        if a.lower().startswith('lab') or v.get('group','').lower() == 'lab':
            for sname, sdat in data['sections'].items():
                if sdat['type'] == 'lab':
                    offby = max((abs(_+3),_) for _ in [v['due'].weekday() - d for d in sdat['days']])[1]
                    d = v['due']
                    d = datetime.datetime(d.year, d.month, d.day, sdat['start'] // 60, sdat['start'] % 60, 0, tzinfo=tz)
                    d -= datetime.timedelta(offby,0,0)
                    ans.event(sname, d, sdat['duration'], location=sdat['room'], details=a+": "+v['title'])
            continue
        if 'due' not in v: continue
        d = v['due']
        if not isinstance(d, datetime.datetime):
            d = datetime.datetime(d.year, d.month, d.day, 23 if v.get('group') == 'project' else 9, 55, 0, tzinfo=tz)
        else:
            d -= datetime.timedelta(0,60*5,0)
        ans.event(a+' due', d, m5)
            
    
    return ans



if __name__ == '__main__':
    import sys
    fixworking()
    with open('markdown/cal.yaml') as stream:
        data = load(stream, Loader=Loader)
    cal = calendar(data)
    with open('markdown/cal.ics', 'wb') as f:
        f.write(cal.bytes())
