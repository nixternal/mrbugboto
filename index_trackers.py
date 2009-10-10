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
from tracker_list import TRACKERS
print """<!doctype html system "about:legacy-compat">
<html lang="en">
    <head>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
	<meta name="description" content="Information about Google Wave Robot Mr. Bugboto.">
	<meta name="keywords" content="Google, Wave, Robot, Bugs, Query">
	<title>Mr. Bugboto</title>
	<link href="../assets/style.css" type="text/css" rel="Stylesheet">
    </head>
    <body>
	<div id="header" class="row"><div class="column grid">
	    <a href="http://mrbugboto.appspot.com"><img src="../assets/icon.png" /></a>
	    <h3>Querying bug trackers via the Google Wave...Dōmo arigatō!</h3>
        </div></div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div class="row section_wrapper">
	    <div class="column grid title_wrapper"><p>List of supported trackers</p></div>
	    <div class="column grid">
		<table style="width:780px;">
		    <tr><th style="text-align:left;">Trigger</th><th style="text-align:left;">Description</th><th style="text-align:left;">URL</th></tr>"""
# TABLE FOR TRIGGERS
table = None
i = 0
for x in TRACKERS.keys():
    if i%2 != 0:
	tr = '<tr class="odd_bg">'
    else:
	tr = '<tr>'
    if not table:
	table = tr + '<td class="trigger">%s</td><td>%s</td><td><a href="%s">%s</a></td></tr>' % (x, TRACKERS[x][2], TRACKERS[x][1], TRACKERS[x][1])
    else:
	table += tr + '<td class="trigger">%s</td><td>%s</td><td><a href="%s">%s</a></td></tr>' % (x, TRACKERS[x][2], TRACKERS[x][1], TRACKERS[x][1])
    i += 1
print table
# END TABLE FOR TRIGGERS
print """	</table>
		<br />
		<p class="note">To have a new tracker added, please <a href="http://code.google.com/p/mrbugboto/issues/list">file an issue report</a>.</p>
	    </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div class="row section_wrapper">
	    <div class="column grid title_wrapper"><p>Example</p></div>
	    <div class="column grid">
		<p>In a new blip:</p>
		<ul>
		    <li>Type an exclamation point <code>!</code></li>
		    <li>Type a trigger such as <code>lp</code>, <code>kde</code>, <code>gnome</code>, or any trigger from the above list</li>
		    <li>Type a number sign <code>#</code></li>
		    <li>Type a bug number you want to query</li>
		</ul>
		<p>When it is all put together, it would look something like: <code>!lp#442079</code></p>
		<p><img src="../assets/mrbugboto.jpg"></p>
	    </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div id="footer" class="row"><div class="column grid">
		<p>Copyright &copy; 2009 by <a href="http://www.nixternal.com">Richard A. Johnson</a> - Verbatim copying and distribution of this entire article are permitted worldwide, without royalty, in any medium, provided this notice, and the copyright notice, are preserved.</p>
        </div></div>
    </body>
</html>"""
# vim: set tw=0:
