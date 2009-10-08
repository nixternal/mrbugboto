#!/usr/bin/env python
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
print """<!DOCTYPE HTML SYSTEM "about:legacy-compat">
<html lang="en">
    <head>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
	<meta name="description" content="Information about Google Wave Robot Mr. Bugboto.">
	<meta name="keywords" content="Google, Wave, Robot, Bugs, Query">
	<title>Mr. Bugboto</title>
	<link href="assets/style.css" type="text/css" rel="Stylesheet">
    </head>
    <body>
	<div id="header" class="row"><div class="column grid">
	    <img src="assets/icon.png" />
	    <h1>Mr. Bugboto</h1>
        </div></div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div id="intro" class="row">
	    <div id="introtitle" class="column grid"><span>Introduction</span></div>
	    <div class="column grid">
		<span>Mr. Bugboto, a robot for <a
		    href="http://wave.google.com">Google Wave</a>, is a query
		tool for various open source bug trackers.</span><br /><br />
	    </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div id="howto" class="row">
	    <div id="howtotitle" class="column grid"><span>How to use</span></div>
	    <div class="column grid">
		<ul>
		    <li>Add <code>mrbugboto@appspot.com</code> to your wave.</li>
		    <li>Start a conversation in the wave and enter the trigger
		    plug the bug number. Example: <code>!lp#442079</code></li>
		</ul>
	    </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div id="trackers" class="row">
	    <div id="trackerstitle" class="column grid"><span>List of supported trackers</span></div>
	    <div class="column grid">
		<table>
		    <tr><th style="text-align:left;">Tracker</th><th>Trigger</th></tr>
		    <tr><td style="width:150px;"><a href="http://bugs.gnome.org">GNOME Bugzilla</a></td><td class="trigger">gnome</td></tr>
		    <tr><td><a href="http://bugs.kde.org">KDE Bugzilla</a></td><td class="trigger">kde</td></tr>
		    <tr><td><a href="https://launchpad.net">Launchpad</a></td><td class="trigger">lp</td></tr>
		</table>
		<br />
	    </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div id="source" class="row">
	    <div id="sourcetitle" class="column grid"><span>Source code</span></div>
	    <div class="column grid">
		<span>Mr. Bugboto is stored at <a
		href="http://code.google.com/p/mrbugboto">http://code.google.com/p/mrbugboto</a>,
		and is licensed under the <a
		href="http://www.gnu.org/licenses/gpl-3.0.txt">GPL Version
		3</a>.</span><br /><br />
	    </div>
	</div>
	<div class="row"><div class="column grid">&nbsp;</div></div>
	<div id="footer" class="row"><div class="column grid">
		<p>Copyright &copy; 2009 by <a
		    href="http://www.nixternal.com">Richard A. Johnson</a>
		- Verbatim copying and distribution of this entire article are
		permitted worldwide, without royalty, in any medium, provided
	       	this notice, and the copyright notice, are preserved.</p>
		<p><a href="http://jigsaw.w3.org/css-validator/check/referer">Valid CSS level 3</a> | <a href="http://validator.w3.org/check?uri=referer">Valid HTML 5</a></p>
        </div></div>
    </body>
</html>"""
