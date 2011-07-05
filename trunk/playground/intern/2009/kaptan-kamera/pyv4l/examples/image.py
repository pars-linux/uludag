#!/usr/bin/env python
# Sample still image captured from TV for pyv4l >= 0.3 - by Michael Dove <pythondeveloper@optushome.com.au>
import v4l
import Image
import ImageChops
WIDTH = 924
HEIGHT = 576
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

tuner = vid.getTuner()
print "Tuner %d" %tuner[0]
print "Tuner Name: %s" %tuner[1]
print "Range Low: %d" %tuner[2]
print "Range High: %d" %tuner[3]
print "Flags: %d" %tuner[4]
print "Mode: %d" %tuner[5]
print "Signal Strength: %d" %tuner[6]
print "Frequency: %d" %vid.getFrequency()
vid.setChannel(0) # TV
vid.setFrequency(216250)
vid.setupImage(WIDTH, HEIGHT)
picture = vid.getPicture()
print "Brightness: %d" % picture[0]
print "Hue: %d" % picture[1]
print "Colour: %d" % picture[2]
print "Contrast: %d" % picture[3]
print "Whiteness: %d" % picture[4]
print "Depth: %d" % picture[5]
print "Palette: %d" % picture[6]
print vid.setPicture(15000, picture[1], picture[2], picture[3], picture[4], picture[5], picture[6])

vid.queueFrame() # queue up a single frame, no need to call preQueueFrames.
output = vid.getImage() # Get the image

# feed the image data in to PIL
im = Image.fromstring("RGB", (WIDTH, HEIGHT), output)
# Invert colour (cabletv)
# im = ImageChops.invert(im)
im.show() # show in xv

# save as JPEG using PIL
#im.save("pyv4l.jpg","JPEG")

vid.mute() # make sure volume is off


