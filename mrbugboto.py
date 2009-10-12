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
from waveapi import document
from waveapi import events
from waveapi import model
from waveapi import robot

from trackers import *
from version import *

import re

def OnBlipSubmitted(properties, context):
    orig_blip = context.GetBlipById(properties['blipId'])
    m = re.match('^.*!(.+)#(\d+).*$', orig_blip.GetDocument().GetText())
    try:
	bug = runTracker(m.group(1), m.group(2))
    except AttributeError:
	return
    new_blip = context.GetRootWavelet().CreateBlip().GetDocument()
    new_blip.AnnotateDocument('style/fontFamily', 'monospace')
    new_blip.AppendText('\n%s' % bug)

def OnRobotAdded(properties, context):
    blip = context.GetRootWavelet().CreateBlip().GetDocument()
    blip.AnnotateDocument('style/fontFamily', 'monospace')
    blip.AppendText('Dōmo arigatō, Mr. Bugboto! Version %s\nPlease review http://mrbugboto.appspot.com for information on how to use this robot.' % VERSION)

if __name__ == '__main__':
    myRobot = robot.Robot('mrbugboto-trunk',
	    image_url='http://www.mrbugboto-trunk.appspot.com/assets/icon.png',
	    version=VERSION,
	    profile_url='http://www.mrbugboto-trunk.appspot.com')
    myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
    myRobot.Run()
