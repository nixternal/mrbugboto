import email.FeedParser
import re
import urllib2
import xml.dom.minidom as minidom
from htmlentitydefs import entitydefs

entre = re.compile('&(\S*?);')
def _getnodetxt(node):
    L = []
    for childnode in node.childNodes:
	if childnode.nodeType == childnode.TEXT_NODE:
	    L.append(childnode.data)
    val = ''.join(L)
    if node.hasAttribute('encoding'):
	encoding = node.getAttribute('encoding')
	if encoding == 'base64':
	    try:
		val = val.decode('base64')
	    except:
		val = 'Cannot convert bug data from base64.'
    while entre.search(val):
	entity = entre.search(val).group(1)
	if entity in entitydefs:
	    val = entre.sub(entitydefs[entity], val)
	else:
	    val = entre.sub('?', val)
    return val

def outputToHTML(bug):
    html = "<br /><br /><br />"
    html += "<b>Bug Number:</b><pre>   %s</pre><br />" % bug[0]
    html += "<b>Product:</b><pre>       %s</pre><br />" % bug[1]
    if bug[2]:
	html += "<b>Component:</b><pre>    %s</pre><br />" % bug[2]
    html += "<b>Summary:</b><pre>       %s</pre><br />" % bug[3]
    html += "<b>Importance:</b><pre>    %s</pre><br />" % bug[4]
    html += "<b>Status:</b><pre>            %s</pre><br />" % bug[5]
    if bug[6]:
	html += "<b>Assigned To:</b><pre>  %s</pre><br />" % bug[6]
    else:
	html += "<b>Assigned To:</b><pre>  Nobody</pre><br />"
    html += "<b>Bug URL:</b><pre>         %s</pre>" % bug[7]
    return html

class BugTrackerError(Exception):
    pass

class BugTrackerNotAvailable(Exception):
    pass

class BugNotFoundError(Exception):
    pass

class BugTracker:
    def __init__(self, name=None, url=None, description=None):
	self.name = name
	self.url = url
	self.description = description

    def get_bug(self, id):
	raise BugTrackerError("Bugtracker class does not implement get_bug")

    def get_tracker(self, url):
	raise BugTrackerError("Bugtracker class does not implement get_tracker")

class Bugzilla(BugTracker):
    def get_bug(self, id):
	url = '%s/xml.cgi?id=%s' % (self.url, id)
	try:
	    bugxml = urllib2.urlopen(url).read()
	    bugdom = minidom.parseString(bugxml)
	except Exception, e:
	    raise BugTrackerError, 'Could not parse XML returned by %s: %s' % (url, e)
	bug = bugdom.getElementsByTagName('bug')[0]
	if bug.hasAttribute('error'):
	    errortxt = bug.getAttribute('error')
	    if errortxt == 'NotFound':
		raise BugNotFoundError
	    raise BugTrackerError, 'Error getting %s bug #%s: %s' % (self.name, id, errortxt)
	try:
	    title = _getnodetxt(bug.getElementsByTagName('short_desc')[0])
	    status = _getnodetxt(bug.getElementsByTagName('bug_status')[0])
	    try:
		status += ": " + _getnodetxt(bug.getElementsByTagName('resolution')[0])
	    except:
		pass
	    product = _getnodetxt(bug.getElementsByTagName('product')[0])
	    component = _getnodetxt(bug.getElementsByTagName('component')[0])
	    severity = _getnodetxt(bug.getElementsByTagName('bug_severity')[0])
	    assignee = '(unavailable)'
	    try:
		assignee = _getnodetxt(bug.getElementsByTagName('assigned_to')[0])
	    except:
		pass
	except Exception, e:
	    raise BugTrackerError, 'Could not parse XML returned by %s bugzilla: %s' % (self.name, e)
	bug = [id, product, component, title, severity, status, assignee, url.replace('xml', 'show_bug')]
	html = outputToHTML(bug)
	return html

class Launchpad(BugTracker):
    def _parse(self, task):
	parser = email.FeedParser.FeedParser()
	parser.feed(task)
	return parser.close()

    def _sort(self, task1, task2):
	try:
	    statuses   = ['Rejected', 'Fix Released', 'Fix Committed',
		'Unconfirmed','Needs Info','Confirmed','In Progress']
	    severities = ['Undecided', 'Wishlist', 'Minor', 'Low', 'Normal',
		'Medium', 'Major', 'High', 'Critical']
	    if task1['status'] not in statuses and task2['status'] in statuses:
		return -1
	    if task1['status'] in statuses and task2['status'] not in statuses:
		return 1
	    if task1['importance'] not in severities and task2['importance'] in severities:
		return -1
	    if task1['importance'] in severities and task2['importance'] not in severities:
		return 1
	    if not (task1['status'] == task2['status']):
		if statuses.index(task1['status']) < statuses.index(task2['status']):
		    return -1
		return 1
	    if not (task1['importance'] == task2['importance']):
		if severities.index(task1['importance']) < severities.index(task2['importance']):
		    return -1
		return 1
	except:
	    return 0
	return 0

    def get_bug(self, id):
	bug_url = '%s/bugs/%s' % (self.url, id)
	try:
	    bugpage = urllib2.urlopen('%s/+text' % bug_url)
	except Exception, e:
	    raise BugTrackerError, 'Could not open %s: %s' % (bug_url, e)
	if bugpage.geturl().endswith('+login'):
	    raise BugTrackerError, "This bug is private."
	try:
	    bugdata = bugpage.read()
	except Exception, e:
	    if '404' in str(e):
		raise BugNotFoundError
	    raise BugTrackerError, 'Could not parse data returned by %s: %s' % (self.description, e)
	try:
	    data = bugdata.split('\n\n')
	    bugdata = data[0]
	    taskdata = data[1:]
	    parser = email.FeedParser.FeedParser()
	    parser.feed(bugdata)
	    bugdata = parser.close()
	    taskdata = map(self._parse, taskdata)
	    taskdata.sort(self._sort)
	    taskdata = taskdata[-1]
	except Exception, e:
	    raise BugTrackerError, 'Could not parse data returned by %s: %s' % (self.description, e)
	t = taskdata['task']
	product = t
	component = None
	if '(' in t:
	    component = t[:t.find('(') -1]
	    product = product.replace(component, "").replace("(", "").strip(')')
	bug = [id, product, component, bugdata['title'], taskdata['importance'],
		taskdata['status'], taskdata['assignee'], bug_url]
	html = outputToHTML(bug)
	return html

TRACKERS = {
	'lp': ('Launchpad', 'https://launchpad.net', 'Bug tracker used for various open source projects, including Ubuntu'),
	'kde': ('Bugzilla', 'https://bugs.kde.org', 'Bug tracker for the KDE project'),
	'gnome': ('Bugzilla', 'https://bugs.gnome.org', 'Bug tracker for the GNOME project'),
	'deb': ('Debian', 'http://www.debian.org/Bugs', 'Bug tracker for the Debian project'),
}

def setupTracker(trigger):
    try:
	tracker = TRACKERS[trigger]
    except KeyError:
	raise BugTrackerNotAvailable("%s is not a registered bug tracker" % trigger)
    url = tracker[1]
    desc = tracker[2]
    tracker = tracker[0]
    if tracker == 'Launchpad':
	bug = Launchpad()
	bug.__init__(tracker, url, desc)
    elif tracker == 'Bugzilla':
	bug = Bugzilla()
	bug.__init__(tracker, url, desc)
    elif tracker == 'Debian':
	bug = Debian()
	bug.__init__(tracker, url, desc)
    else:
	raise BugTrackerNotAvailable("%s is not a valid trigger" % trigger)
    return bug

def runTracker(trigger, id):
    bug = setupTracker(trigger)
    bug = bug.get_bug(id)
    return bug

if __name__ == '__main__':
    bug = runTracker('gnome', '589153')
    #bug = runTracker('kde', '209744')
    #bug = runTracker('lp', '442079')
    print bug
