#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import qt
import v4l
import Image

class Cam:
    def __init__(self, ui):
        self.ui = ui
        self.WIDTH = 320
        self.HEIGHT = 240
        self.deviceDic = {}
        self.picture = None
        self.capabilities = None
        self.nextFrame = 0
        self.array = qt.QByteArray(self.WIDTH*self.HEIGHT*3)

        list = os.listdir("/dev/v4l")
        for i in list:
            self.ui.cb_video.insertItem(i)

    def start(self):
#       print "start"

        tmpPath =  "/dev/" + str(self.ui.cb_video.currentText())
        if tmpPath not in self.deviceDic:
            self.deviceDic[tmpPath] = v4l.video(tmpPath)

        self.device = self.deviceDic[tmpPath]
        self.picture = self.device.getPicture()
        self.capabilities = self.device.getCapabilities()
        self.device.preQueueFrames()
        self.nextFrame = 0
        self.ui.connect(self.ui.timer, qt.SIGNAL("timeout()"), self.ui.cam.getFrame)
        self.ui.timer.start(100)


    def RGB2BGR(self, str):
        list = [l for l in str]
        for i in range(0, len(list), 3):
            temp = list[i+2]
            list[i+2] = list[i]
            list[i] = temp
        return "".join(list)

    def from24to32(self, str):
        list = [l for l in str]
        newstr = []
        # for i in range(940):
        newstr.append(940 * '\x00')
        for i in range(0, len(list), 3):
            newstr.append(list[i])
            newstr.append(list[i+1])
            newstr.append(list[i+2])
            newstr.append('\x00')
        return qt.QString("".join(newstr))

    @staticmethod
    def toPixmap(pgm):
        """Convert PGM data to pixmap"""
        pixmap = qt.QPixmap()
        pixmap.loadFromData(pgm, "PGM")
        return pixmap


    def getFrame(self):
#       print "getFrame"
        if(None == self.device):
            print "No device on"
            return
#       else:
#           print "Device:", self.device
        out = self.device.getImage(self.nextFrame)

        #out = self.RGB2BGR(out)
        #imTemp = Image.fromstring("RGB", (self.WIDTH, self.HEIGHT), out)
        #PILstring = imTemp.convert("RGB").tostring("jpeg", "RGB")
        #im = qt.QImage(qt.QByteArray(PILstring))

        #im = qt.QImage(out, self.WIDTH, self.HEIGHT, 24, 0, 2**24, qt.QImage.IgnoreEndian)


        # tmp = self.from24to32(out)

        # tmp = qt.QString(out)

        # im = qt.QImage(self.WIDTH, self.HEIGHT,32,qt.QImage.IgnoreEndian)
        # im.loadFromData(tmp)

        # image = qt.QPixmap(im)

        # tmp = self.RGB2BGR(out)
        im = "P6 %s %s 16777216\n%s" % (self.WIDTH, self.HEIGHT, out)
        pixmap = self.toPixmap(im)
        self.ui.lbl_screen.setPixmap(pixmap)
        self.nextFrame = self.device.queueFrame()

    def capture(self):
#       print "capture"
        tmpPath =  "/dev/" + str(self.ui.cb_video.currentText())
        if tmpPath not in self.deviceDic:
            self.deviceDic[tmpPath] = v4l.video(tmpPath)


        self.device = self.deviceDic[tmpPath]
        self.picture = self.device.getPicture()
        self.capabilities = self.device.getCapabilities()
        self.device.preQueueFrames()

        out = self.device.getImage(self.nextFrame)
        out = self.RGB2BGR(out)
        image = Image.fromstring("RGB", (self.WIDTH, self.HEIGHT), out)
        image.save("image.jpg", "JPEG")
        self.ui.timer.stop()




