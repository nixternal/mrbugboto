# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009 Richard A. Johnson <nixternal@gmail.com>                 #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
################################################################################
import email.FeedParser
import re
import urllib2
import xml.dom.minidom as minidom

from htmlentitydefs import entitydefs

from tracker_list import TRACKERS

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

def createOutput(bug):
    titles = ['Number:', 'Summary:', 'Product:', 'Component:', 'Version:',
	    'Statuses:', 'Severity:', 'Assigned To:', 'Target:', 'URL:']
    text = None
    for i in range(0, len(bug)):
	if not text:
	    text = titles[0].ljust(20) + bug[0].strip()
	else:
	    if i == 1 or i == 7:
		text += '\n' + titles[i].ljust(20) + bug[i].decode('utf-8').strip()
	    elif i == 2:
		if bug[i]:
		    text += '\n' + titles[i].ljust(20) + bug[i].strip()
		else:
		    text += '\n' + titles[i].ljust(20) + bug[i+1].strip()
	    elif i == 3 and bug[i] and bug[i-1]:
		text += '\n' + titles[i].ljust(20) + bug[i].strip()
	    elif i == 4 and bug[i]:
		text += '\n' + titles[i].ljust(20) + bug[i].strip()
	    elif i == 8 and bug[i]:
		text += '\n' + titles[i].ljust(20) + bug[i].strip()
	    else:
		if bug[i]:
		    text += '\n' + titles[i].ljust(20) + bug[i].strip()
    if not text:
	return 'ERROR: Something went wrong during the creation of the output.'
    return text

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
	    return "Could not parse XML returned by %s: %s" % (url, e)
	bug = bugdom.getElementsByTagName('bug')[0]
	if bug.hasAttribute('error'):
	    errortxt = bug.getAttribute('error')
	    if errortxt == 'NotFound':
		return "Bug not found: %s" % url.replace("xml", "show_bug")
	    return "Error getting %s bug #%s: %s" % (self.name, id, errortxt)
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
	    version = _getnodetxt(bug.getElementsByTagName('version')[0]).replace(' ', '.')
	    assignee = '(unavailable)'
	    try:
		assignee = _getnodetxt(bug.getElementsByTagName('assigned_to')[0])
	    except:
		pass
	except Exception, e:
	    return "Could not parse XML returned by %s bugzilla: %s" % (self.name, e)
	bug = [id, title, product, component, version, status, severity, assignee,
		None, url.replace('xml', 'show_bug')]
	html = createOutput(bug)
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
	    return "Unable to open %s. Please try again shortly." % bug_url
	if bugpage.geturl().endswith('+login'):
	    return "This bug is private: %s" % bug_url
	try:
	    bugdata = bugpage.read()
	except Exception, e:
	    if '404' in str(e):
		return "404 Error: %s" % bug_url
	    return "Could not parse data returned by %s: %s" % (self.description, e)
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
	    return "Could not parse data returned by %s: %s" % (self.description, e)
	t = taskdata['task']
	product = t
	component = None
	if '(' in t:
	    component = t[:t.find('(') -1]
	    product = product.replace(component, "").replace("(", "").strip(')')
	bug = [id, bugdata['title'], product, component, None,
		taskdata['status'], taskdata['importance'],
		taskdata['assignee'], taskdata['milestone'], bug_url]
	html = createOutput(bug)
	return html

def setupTracker(trigger):
    try:
	tracker = TRACKERS[trigger]
    except KeyError:
	return "%s is not a registered bug tracker." % trigger
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
    return bug

def runTracker(trigger, id):
    bug = setupTracker(trigger)
    try:
	if "Invalid trigger" in bug:
	    pass
    except TypeError:
	bug = bug.get_bug(id)
    return bug

if __name__ == '__main__':
    bug = runTracker('lp', '344707')
    print bug
