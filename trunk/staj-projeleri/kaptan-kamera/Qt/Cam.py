#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import qt
import v4l
import Image

class Cam:
    def __init__(self, ui):
        self.ui = ui
        self.WIDTH = 320
        self.HEIGHT = 240
        self.device = None
        self.picture = None
        self.capabilities = None
        self.nextFrame = 0

    def start(self):
#       print "start"
        if( self.ui.timer.isActive() ):
            return

        if(self.device == None):
            self.device = v4l.video('/dev/video0')
            self.picture = self.device.getPicture()
            self.capabilities = self.device.getCapabilities()
            self.device.preQueueFrames()
            self.ui.connect(self.ui.timer, qt.SIGNAL("timeout()"), self.ui.cam.getFrame)

        self.ui.timer.start(100)



    def getFrame(self):
#       print "getFrame"
        if(None == self.device):
            print "No device on"
            return
#       else:
#           print "Device:", self.device
        out = self.device.getImage(self.nextFrame)
        imTemp = Image.fromstring("RGB", (self.WIDTH, self.HEIGHT), out)
        PILstring = imTemp.convert("RGB").tostring("jpeg", "RGB")
        im = qt.QImage(qt.QByteArray(PILstring))
        image = qt.QPixmap(im)
        self.ui.lbl_screen.setPixmap(image)
        self.nextFrame = self.device.queueFrame()

    def capture(self):
#       print "capture"
        if(self.device == None):
            self.device = v4l.video('/dev/video0')
            self.device.preQueueFrames()
        out = self.device.getImage(self.nextFrame)
        image = Image.fromstring("RGB", (self.WIDTH, self.HEIGHT), out)
        image.save("image.jpg", "JPEG")
        self.ui.timer.stop()




