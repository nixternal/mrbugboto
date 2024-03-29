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
from optparse import OptionParser
from trackers import *
parser = OptionParser(usage="Usage: %prog -t arg1 -n arg2")
parser.add_option("-t", "--trigger", action="store", type="string", dest="trigger",
	default="lp", help="Trigger for the bug tracker")
parser.add_option("-n", "--number", action="store", type="string", dest="number",
	default="100", help="Number of the bug to query in the bug tracker")
(options, args) = parser.parse_args()
print runTracker(options.trigger, options.number)
