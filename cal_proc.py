from datetime import datetime, timedelta, date
from yaml import load
from glob import glob
from sys import stderr
import json, re, markdown, os.path
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

################################################################################
###                         Some helper functions                            ###
################################################################################
def fixworking():
    """change to this script's directory as the working directory"""
    import os, os.path
    os.chdir(os.path.realpath(os.path.dirname(__file__)))


def debug(*args, **kargs):
    """Helper to print to stderr"""
    kargs['file'] = stderr
    print(*args, **kargs)

def prettyjson(d, newlineindent=2, maxinline=79):
    """The way I like to see JSON:
    commas begin lines
    short collections inline
    no extra spaces"""
    s = json.dumps(d, separators=(',',':'))
    indent = 0
    instr = False
    def skipshort(start, maxlen):
        """Given the starting index of a list or dict, returns either
        the same index, if it is too long,
        or the index of the last character of the list/dict"""
        nest = 0
        instr = False
        i = start
        comma = False
        while i < len(s) and ((not comma) or (i < start+maxlen)):
            if instr:
                if s[i] == '\\': i+=1
                elif s[i] == '"': instr = False
            else:
                if s[i] == '"': instr = True
                elif s[i] in '[{': nest += 1
                elif s[i] in ']}':
                    nest -= 1
                    if nest == 0: return i
                elif s[i] == ',': comma = True
            i += 1
        return start
    chunks = []
    i=0
    last=0
    indents = []
    while i < len(s):
        if instr:
            if s[i] == '\\': 
                i+=1
            elif s[i] == '"': instr = False
        elif s[i] == '"': instr = True
        else:
            if s[i] in '[{':
                end = skipshort(i, maxinline-(i-last)-indent)
                if end > i: i = end
                elif (i-last) < 8:
                    indents.append(indent)
                    indent += (i-last)
                else:
                    chunks.append(s[last:i])
                    indents.append(indent)
                    indent += newlineindent
                    chunks.append('\n'+' '*indent)
                    last = i
            elif s[i] in ']}':
                chunks.append(s[last:i])
                chunks.append('\n'+' '*indent + s[i])
                indent = indents.pop()
                last = i+1
            elif s[i] == ',':
                chunks.append(s[last:i])
                chunks.append('\n'+' '*indent)
                last = i
        i += 1
    if last < i: chunks.append(' '*indent + s[last:i])
    return ''.join(chunks)


################################################################################
###                         The main data mungers                            ###
################################################################################

numgap = re.compile(r'([a-zA-Z])([0-9])')
codeclass = re.compile(r'[{][.][^}]+[}]')

weekdays = ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')

def calendar(data, linkfile):
    oneday = timedelta(1)
    things = {}
    breaks = [
        (date.min, data['Special Dates']['Courses begin']-oneday), 
        (data['Special Dates']['Courses end']+oneday, date.max), 
    ]
    for k,v in data['Special Dates'].items():
        if 'recess' in k or 'break' in k or 'Reading' in k:
            if type(v) is dict: breaks.append((v['start'], v['end']))
            else: breaks.append((v, v))
        else:
            things.setdefault(v, []).append(k)
    for k,v in data['assignments'].items():
        if k.startswith('.'): continue
        if v is None or 'due' not in v: continue
        d = v['due']
        if isinstance(d, datetime): d = d.date()
        things.setdefault(d, []).append(k)
    d = min(things.keys())
    end = max(things.keys())
    weeks = [[]]
    classidx = 0
    while d <= end:
        wd = weekdays[d.weekday()]
        if wd == 'Sun': weeks.append([])
        noclass = any(a <= d <= b for a,b in breaks)
        if d in things or ((not noclass) and wd in ('Tue','Thu')):
            today = {'day':wd, 'date':d}
            if (not noclass) and wd in ('Tue','Thu'): 
                d1 = data['classes'][classidx] if classidx < len(data['classes']) else ''
                if type(d1) is str: d1 = [d1]
                if not d1: d1 = []
                r = []
                for _ in d1:
                    r.extend(data['reading'].get(_, [])[:])
                today['topic'] = (' <span class="and">and</span> '.join(d1) if d1 else 'TBD')
                today['reading'] = ('<span class="reading">' + ', '.join(r)+'</span>' if r else '')
                if d in linkfile:
                    links = []
                    for k,v in linkfile[d].items():
                        if k != 'files':
                            links.append('['+k+']('+v+')')
                    links.extend('['+os.path.basename(_)+']('+_+')' for _ in linkfile[d].get('files',[]))
                    today['links'] = ' <span class="links">'+', '.join(links)+'</span>'
                classidx += 1
            if noclass:
                today['break'] = True
            for k in things.get(d,[]):
                if k in data['assignments']:
                    name = numgap.sub(r'\1 \2', k)
                    if 'title' in data['assignments'][k]:
                        name = '<a href="'+k.lower()+'-'+data['assignments'][k]['title']+'.html">' + name + ' ' + data['assignments'][k]['title']+'</a>'
                    elif k.startswith('PA') and type(data['assignments'][k].get('files',None)) is str:
                        name = '<a href="'+ k.lower()+'-'+data['assignments'][k]['files'][:-3]+'.html">' + name + ' '+data['assignments'][k]['files'][:-3]+'</a>'
                    elif 'writeup' in data['assignments'][k]:
                        name = '<a href="'+data['assignments'][k]['writeup']+'">' + name +'</a>'
                    today.setdefault('due', []).append(name)
                else:
                    today.setdefault('other', []).append(k)
            weeks[-1].append(today)
        d += oneday
    return weeks

def mdinline(txt):
    html = markdown.markdown(codeclass.sub('', txt))
    if html.count('<p>') == 1:
        html = html[3:-4]
    return html
    
def divify(weeks):
    ans = '<div id="schedule" class="agenda">'
    for w in weeks:
        ans += '<div class="week">\n'
        for d in w:
            ans += '<div class="day ' + d['day']
            if d.get('break',False): ans += ' break'
            ans += '"><span class="date">' + d['date'].strftime('%d %b').lstrip('0') + '</span>'
            if 'other' in d:
                ans += '<div class="other">' + '</div><div class="other">'.join(d['other'])+'</div>'
            if 'topic' in d: 
                ans += '<div class="topic"><strong>'+mdinline(d['topic'])+'</strong>'
                if 'reading' in d: ans += mdinline(d['reading'])
                ans += '</div>'
            if 'links' in d: ans += '<div class="links">'+mdinline(d['links'])+'</div>'
            if 'due' in d:
                ans += '<div class="due">'
                for e in d['due']:
                    ans += ' <span'
                    if 'PA ' in e: ans += ' class="pa"'
                    elif 'Lab ' in e: ans += ' class="lab"'
                    ans += '>' + e + '</span>'
                ans += '</div>'
            ans += '</div>'
        ans += '\n</div>\n'
    return ans + '</div>'

################################################################################
###                            Run as a program                              ###
################################################################################

if __name__ == '__main__':
    fixworking()
    import os.path

    with open('markdown/cal.yaml') as stream:
        data = load(stream, Loader=Loader)

    links = {}
    try:
        with open('links.yaml') as stream:
            links = load(stream, Loader=Loader)
        if links is None: links = {}
    except: 
        pass
        
    #with open('assignments.json', 'w') as f:
        #f.write(prettyjson(assignments_json(data)))
    #with open('coursegrade.json', 'w') as f:
        #f.write(prettyjson(coursegrade_json(data), maxinline=16))
    
    with open('markdown/schedule.html', 'w') as f:
        f.write("""﻿<style>
    body { font-family: sans-serif; }
    .day a { text-decoration: none; background: rgba(255,127,0,0.125); padding:0ex 0.5ex; border-radius:0.5ex; color: inherit; border: 0.125ex solid rgba(255,127,0,0.25); white-space:pre }
    .due:before { content: "Due: "; font-size: 70.7%; opacity: 0.707;  }
    .other { background: #ffddbb; text-align: center; }
    .exam > .other { background: #ffbb77; text-align: center; }
    .day div.topics:before { content: "Topics: "; font-size: 70.7%; opacity: 0.707; }
    
    .hide, .calendar div.day.hide { display:none; }
    span.and { font-size:70.7%; font-weight: normal; }
    
    #schedule.calendar { border: 0.5ex solid #dddddd; border-radius:1ex; background-color: #dddddd; }
    .calendar div.day { background-color: white; }
    .calendar div.week, .calendar div.day { vertical-align:top; min-height:1em; }
    .calendar div.day { display:inline-block; width:calc(33.33% - 2ex); border-radius:1ex; padding:0.5ex; border: solid #dddddd 0.5ex; }
    .calendar div.day.past { opacity:0.7071; }
    .calendar div.day.current { border-color: #ffbb77; background: #fff7f0; }
    .calendar .Tue:first-child { margin-left: 0%; }
    .calendar .Thu:first-child { margin-left: 33.33%; }
    .calendar .Fri:first-child { margin-left: 66.66%; }
    .calendar .Tue + .Fri { margin-left: 33.33%; }
    .calendar .day.hide + .day { margin-left: 33.33%; }
    .calendar .day.hide + .day.hide + .day { margin-left: 66.66%; }
    /* .calendar div.due { background-color:#ffeedd; } */
    .calendar span.date { float:right; padding: 0ex 0ex 0.5ex 1ex; opacity:0.5; font-size: 70.7%; margin-top: -1.41ex; }
    .calendar .other { margin: -0.5ex -0.5ex 0.25ex -0.5ex; border-radius: 0.5ex 0.5ex 0ex 0ex; }
    .calendar .reading:before { content: "Reading: "; font-size:70.7%; opacity: 0.707; }
    .calendar .reading:not(.hide) { display: block; }
   
    .l001:before { content: "001 files: "; font-size:70.7%; opacity: 0.707; }
    .l002:before { content: "002 files: "; font-size:70.7%; opacity: 0.707; }
    .l003:before { content: "003 files: "; font-size:70.7%; opacity: 0.707; }
    .l1111:before { content: "1111 files: "; font-size:70.7%; opacity: 0.707; }
    .links:not(.hide) { display: block; }

    .calendar div.week { display:flex; flex-direction: row; align-items: flex-stretch; }
    .calendar div.week div.day { flex-grow: 0; flex-shrink: 1; flex-basis: auto; }
    
    
    .agenda div.week { border-top: thick solid #dddddd; min-height: 3em; background:#eeeeee; }
    .agenda .day + .day { border-top: thin dotted #777777; }
    .agenda .day { padding: 0.5ex 0ex; background: white; min-height:1.5em; }
    .agenda div.day.past { opacity:0.7071; }
    .agenda div.day.current { border: 0.25ex solid #ffbb77; padding:0.5ex; border-radius:1ex; background: #fff7f0; }
    .agenda span.date { float:left; opacity:0.5; }
    .agenda .Sun span.date:before { content: "Sun "; }
    .agenda .Mon span.date:before { content: "Mon "; }
    .agenda .Tue span.date:before { content: "Tue "; }
    .agenda .Wed span.date:before { content: "Wed "; }
    .agenda .Thu span.date:before { content: "Thu "; }
    .agenda .Fri span.date:before { content: "Fri "; }
    .agenda .Sat span.date:before { content: "Sat "; }
    .agenda .day div:not(.other) { clear:left; }
    .agenda .reading:before { content: "; see " }
    
.agenda .other { margin-top: -0.5ex; padding-bottom: 0.25ex; }
.agenda .current .other { margin: -0.5ex -0.5ex 0.25ex -0.5ex; }
    
    /* .agenda .day:nth-of-type(2n+1) { background-color: #f7f7f7; } */
</style>
<span style="width:2em; display:inline-block;">&nbsp;</span>
<input type="button" id="asAgenda" value="agenda view" onclick="view(true)"/>
<input type="button" id="asCalendar" value="calendar view" onclick="view(false)"/>
<input type="button" id="showPast" value="show past" onclick="view(undefined, true)"/>
<input type="button" id="hidePast" value="hide past" onclick="view(undefined, false)"/>
""")
        f.write(divify(calendar(data, links)))
        f.write("""<script>//<!--
function view(agenda, past) {
    if (typeof(past) == 'undefined') past = window.location.hash.indexOf('future') < 0;
    if (typeof(agenda) == 'undefined') agenda = window.location.hash.indexOf('age') > 0;
    if (agenda) document.getElementById('schedule').setAttribute('class','agenda');
    else document.getElementById('schedule').setAttribute('class','calendar');
    if (past) {
        var weeks = document.querySelectorAll('.week.past');
        for(var i=0; i<weeks.length; i+=1) {
            weeks[i].removeAttribute('style');
        }
    } else {
        var weeks = document.querySelectorAll('.week.past');
        for(var i=0; i<weeks.length; i+=1) {
            weeks[i].setAttribute('style', 'display:none;');
        }
    }
    window.location.hash = '#' + (agenda ? 'age' : 'cal') + '-' + (past ? 'full' : 'future');
}
var days = document.querySelectorAll('.day');
for(var i=0; i<days.length; i+=1) {
    var date = new Date(days[i].querySelector('.date').innerText + ' """+str(data['Special Dates']['Courses end'].year)+""" 23:59');
    if (date < new Date()) days[i].classList.add('past');
    else { days[i].classList.add('current'); break; }
}
var weeks = document.querySelectorAll('.week');
for(var i=0; i<weeks.length; i+=1) {
    if (weeks[i].querySelectorAll('.day:not(.past)').length == 0) {
        weeks[i].classList.add('past');
    }
}

view(window.location.hash.indexOf('age') > 0, window.location.hash.indexOf('future') < 0);
//--></script>""")
