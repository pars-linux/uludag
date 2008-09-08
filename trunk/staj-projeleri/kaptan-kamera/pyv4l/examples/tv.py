#!/usr/bin/env python
# Sample TV viewing application for pyv4l >= 0.3 - by Michael Dove <pythondeveloper@optushome.com.au>
# Note: this does the imaging in grab mode. Performance is limited.  
# I average 35 fps @ 320x240. Disabling the writes to the tk window yeilds 90+ fps.

import v4l
import Image
import ImageChops
WIDTH = 320
HEIGHT = 240
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
vid.setupImage(WIDTH, HEIGHT, v4l.VIDEO_PALETTE_YUYV)
print vid.getChannel(0) # TV
vid.setChannel(0) # set to TV
vid.setFrequency(216250)

import Tkinter
tk=Tkinter.Tk()
import ImageTk
photo = ImageTk.PhotoImage("RGB",(WIDTH,HEIGHT))
label= Tkinter.Label(tk,text="mini TV",image=photo,width=WIDTH,height=HEIGHT)
label.pack()

vid.preQueueFrames()
nextFrame = 0;
vid.setVolume(5)
vid.mute()

try:
    while 1:
	output = vid.getImage(nextFrame)
	im = Image.fromstring("RGB", (WIDTH, HEIGHT), output)
	# invert colour for cable channels :)
	#im = ImageChops.invert(im) 

	# save with PIL as jpeg
	#im.save("xyz.jpg","JPEG")
	# Display image in xv
	#im.show()

	# update Tk label
	photo.paste(im)
	tk.update()
	nextFrame = vid.queueFrame()

except Tkinter.TclError:
    print "something"
    pass
vid.mute()

