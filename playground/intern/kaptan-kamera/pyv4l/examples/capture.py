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

print "-----------------------------"

pic = vid.getPicture()
print "pic:", pic 
print "Picture Brighness: %d" % pic[0]
print "Hue: %d" % pic[1]
print "Colour: %d" % pic[2]
print "Contrast: %d" % pic[3]
print "Whiteness: %d" %  pic[4]
print "Depth: %d" % pic[5]
print "Palette: %d" % pic[6]


#vid.setPicture(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], v4l.VIDEO_PALETTE_RGB24)
#
#print "-----------------------------"
#
#pic = vid.getPicture()
#print "pic:", pic 
#print "Picture Brighness: %d" % pic[0]
#print "Hue: %d" % pic[1]
#print "Colour: %d" % pic[2]
#print "Contrast: %d" % pic[3]
#print "Whiteness: %d" %  pic[4]
#print "Depth: %d" % pic[5]
#print "Palette: %d" % pic[6]


print "-----------------------------"


print "RGB24: %d" % v4l.VIDEO_PALETTE_RGB24
print "YUYV: %d" % v4l.VIDEO_PALETTE_YUYV


print "-----------------------------"
#print "vid.setupImage(cap[4], cap[5], v4l.VIDEO_PALETTE_YUYV) is shown"
#print "vid.setupImage(cap[4], cap[5], v4l.VIDEO_PALETTE_RGB24) is shown"
#print "vid.setupImage(cap[4], cap[5], pic[6]) is shown"
print "vid.setupImage(cap[4], cap[5], 0) is shown"

#vid.setupImage(cap[4], cap[5], v4l.VIDEO_PALETTE_YUYV)
#vid.setupImage(cap[4], cap[5], v4l.VIDEO_PALETTE_RGB24)
#vid.setupImage(cap[4], cap[5], pic[6])
vid.setupImage(cap[4], cap[5], 0)

vid.preQueueFrames()

output = vid.getImage(0)
im = Image.fromstring("RGB", (cap[4], cap[5]), output)

# save with PIL as jpeg
im.save("xyz.jpg","JPEG")
# Display image in xv
im.show()
