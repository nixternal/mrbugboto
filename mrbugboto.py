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
from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document
from waveapi.ops import OpBuilder

from trackers import *

import re

def OnBlipSubmitted(properties, context):
    blip = context.GetBlipById(properties['blipId'])
    m = re.match('!(.+)#(.+)', blip.GetDocument().GetText())
    try:
	bug = runTracker(m.group(1), m.group(2))
    except AttributeError:
	return
    builder = OpBuilder(context)
    blip.GetDocument().SetText(" ")
    builder.DocumentAppendMarkup(blip.waveId, blip.waveletId, properties['blipId'], bug)

def OnRobotAdded(properties, context):
    context.GetRootWavelet().CreateBlip().GetDocument().SetText('Domo arigato, Mr. Bugboto')

if __name__ == '__main__':
    myRobot = robot.Robot('mrbugboto',
	    image_url='http://www.mrbugboto.appspot.com/assets/icon.png',
	    version='1',
	    profile_url='http://www.mrbugboto.appspont.com')
    myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
    myRobot.Run()
