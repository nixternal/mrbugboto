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
