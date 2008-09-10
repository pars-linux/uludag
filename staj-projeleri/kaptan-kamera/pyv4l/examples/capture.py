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
#vid.setupImage(WIDTH, HEIGHT, v4l.VIDEO_PALETTE_YUYV)
vid.setupImage(WIDTH, HEIGHT, v4l.VIDEO_PALETTE_RGB24)

vid.preQueueFrames()

output = vid.getImage(0)
im = Image.fromstring("RGB", (WIDTH, HEIGHT), output)

# save with PIL as jpeg
im.save("xyz.jpg","JPEG")
# Display image in xv
im.show()
