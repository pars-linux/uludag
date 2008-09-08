#!/usr/bin/env python
# Sample TV overlay viewing application for pyv4l >= 0.4 - by Michael Dove <pythondeveloper@optushome.com.au>

import v4l
import time
import os
import sys

WIDTH = 640
HEIGHT = 480
X = 300
Y = 300
vid = v4l.video('/dev/video')

# set appropriate palette else you may get incorrect images
try: 
    vid.setupFrameBuffer()
except v4l.VideoError, e:
    print "WARNING:", e, "Attempting to run v4l-conf"
    vid.mute()
    del vid
    pipefd = os.popen('v4l-conf -q -c /dev/video')
    if (pipefd.close()):
	print "Unable to setup framebuffer"
	sys.exit(1)


vid = v4l.video('/dev/video')
cap = vid.getCapabilities()
print "Device Name: %s" % cap[0]
print "Type: %d" % cap[1]
print "Channels: %d" % cap[2]
print "Audios: %d" % cap[3]
print "Maximum Width: %d" % cap[4]
print "Maximum Height: %d" % cap[5]
print "Minimum Width: %d" % cap[6]
print "Minimum Height: %d" % cap[7]


vid.setupImage(WIDTH, HEIGHT, v4l.VIDEO_PALETTE_YUV422P)
vid.setOverlay(X, Y, WIDTH, HEIGHT)
vid.getChannel(0) # TV
vid.setChannel(0) # set to TV
vid.setFrequency(216250)

vid.startCapture()
time.sleep(10)
vid.stopCapture()
vid.mute()

