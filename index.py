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
from version import *
print """<!doctype html "about:legacy-compat">
<html lang="en">
    <head>
	<meta charset=utf-8>
	<meta name="description" content="Information about Google Wave Robot Mr. Bugboto.">
	<meta name="keywords" content="Google, Wave, Robot, Bugs, Query">
	<title>Mr. Bugboto</title>
	<link href="assets/style.css" type="text/css" rel="Stylesheet">
    </head>
    <body>
	<div id="header" class="row"><div class="column grid">
	    <a href="http://mrbugboto.appspot.com"><img src="assets/logo.png" /></a>
	    <h3>Querying bug trackers via the Google Wave...Dōmo arigatō!</h3>
        </div></div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div class="row section_wrapper">
	    <div class="column grid title_wrapper"><p>Introduction</p></div>
	    <div class="column grid">
		<p>Mr. Bugboto, a robot for <a href="http://wave.google.com">Google Wave</a>, is a query tool for various open source bug trackers.</p>"""
print '		<p>Current version: <strong>%s</strong></p>' % VERSION
print """   </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div class="row section_wrapper">
	    <div class="column grid title_wrapper"><p>How to use</p></div>
	    <div class="column grid">
		<ul>
		    <li>Add <code>mrbugboto@appspot.com</code> to your wave.</li>
		    <li>Start a conversation in the wave and enter the trigger plug the bug number. Example: <code>!lp#442079</code></li>
		</ul>
		<p><a href="http://mrbugboto.appspot.com/trackers/">List of available triggers</a></p>
	    </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div class="row section_wrapper">
	    <div class="column grid title_wrapper"><p>Source code</p></div>
	    <div class="column grid">
		<p>Mr. Bugboto is stored at <a href="http://code.google.com/p/mrbugboto">http://code.google.com/p/mrbugboto</a>, and is licensed under the <a href="http://www.gnu.org/licenses/gpl-3.0.txt">GPL Version 3</a>.</p>
	    </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div class="row section_wrapper">
	    <div class="column grid title_wrapper"><p>Filing bugs</p></div>
	    <div class="column grid">
		<p>To request a new tracker to be added to the robot, or file a bug, do so on the <a href="http://code.google.com/p/mrbugboto/issues/list">robot's issues page</a>. If you experience a crash, please enter the trigger/tracker and bug number that you used that caused the issue. If any text was printed out to a blip from the robot, either take a screenshot and attach it, or copy and paste its output.</p>
	    </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div id="footer" class="row"><div class="column grid">
		<p>Copyright &copy; 2009 by <a href="http://www.nixternal.com">Richard A. Johnson</a> - Verbatim copying and distribution of this entire article are permitted worldwide, without royalty, in any medium, provided this notice, and the copyright notice, are preserved.</p>
        </div></div>
    </body>
</html>"""
# vim: set tw=0:
