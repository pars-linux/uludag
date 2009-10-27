#!/usr/bin/env python
# Sample TV overlay viewing application for pyv4l >=0.4
# Author: Michael Dove <pythondeveloper@optushome.com.au>

from qt import *
from tvwindow import TVWindow
import sys
import v4l

class MainWindow(TVWindow):

    def __init__(self, width, height, *args, **kwargs):
	TVWindow.__init__(self, *args, **kwargs)
	self.width = width
	self.height = height
	vid = v4l.video('/dev/video')
	self.vid = vid
	vid.setupImage(self.width, self.height, v4l.VIDEO_PALETTE_YUV422P)
	vid.getChannel(0) # TV
	vid.setChannel(0) # set to TV
	vid.setFrequency(216250)
	vid.setVolume(5)
	vid.startCapture()


    def resizeEvent(self, resizeEvent):
	self.width = resizeEvent.size().width()
	self.height = resizeEvent.size().height()
	self.vid.setOverlay(self.x, self.y, self.width, self.height)


    def moveEvent(self, moveEvent):
	self.x = moveEvent.pos().x()
	self.y = moveEvent.pos().y()
	self.vid.setOverlay(self.x, self.y, self.width, self.height)
	
	

    def closeEvent(self, *args):
	self.vid.mute()
	self.vid.stopCapture()
	QApplication.exit(0)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = MainWindow(640, 480)
    a.setMainWidget(w)
    w.show()
    a.exec_loop()	
