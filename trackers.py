import urllib2
import email.FeedParser

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
	if '(' in t:
	    t = t[:t.find('(') -1]
	html = "<br /><br /><br />"
	html += "<b>Bug Number:</b><pre>   %s</pre><br />" % id
	html += "<b>Component:</b><pre>    %s</pre><br />" % t
	html += "<b>Summary:</b><pre>       %s</pre><br />" % bugdata['title']
	html += "<b>Importance:</b><pre>    %s</pre><br />" % taskdata['importance']
	html += "<b>Status:</b><pre>            %s</pre><br />" % taskdata['status']
	html += "<b>Assigned to:</b><pre>  %s</pre><br />" % taskdata['assignee']
	html += "<b>Bug URL:</b><pre>         %s</pre>" % bug_url
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

#if __name__ == '__main__':
#    bug = runTracker('lp', '442079')
#    for x in bug:
#	if x:
#	    print x
