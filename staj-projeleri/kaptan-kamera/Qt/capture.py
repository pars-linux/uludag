#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form_capture_New.ui'
#
# Created: Cum Eyl 12 13:29:22 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *

import v4l
import Image

class Cam:
    def __init__(self, ui):
        self.ui = ui
        self.WIDTH = 320
        self.HEIGHT = 240
        self.device = None
        self.pic = None
        self.cap = None
        self.nextFrame = 0

    def start(self):
        print "start"
        self.device = v4l.video('/dev/video0')
        self.device.preQueueFrames()


    def show(self):
        print "show"

        self.ui.connect(self.ui.timer, SIGNAL("timeout()"), self.ui.cam.capture)
        self.ui.timer.start(100)

    def capture(self):
        print "capture"

        out = self.device.getImage(self.nextFrame)

        imTemp = Image.fromstring("RGB", (self.WIDTH, self.HEIGHT), out)

        PILstring = imTemp.convert("RGB").tostring("jpeg", "RGB")

        im = QImage(QByteArray(PILstring))
        image = QPixmap(im)
        #print "loadFromData:", image.loadFromData(out, len(out))
        self.ui.lbl_Screen.setPixmap(image)

        self.nextFrame = self.device.queueFrame()


    def stop(self):
        print "stop"

        self.ui.timer.stop()

        # del self.device




class form_Capture_New(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("form_Capture_New")



        self.btn_Start = QPushButton(self,"btn_Start")
        self.btn_Start.setGeometry(QRect(30,280,60,51))

        self.btn_Show = QPushButton(self,"btn_Show")
        self.btn_Show.setGeometry(QRect(110,280,60,51))

        self.btn_Capture = QPushButton(self,"btn_Capture")
        self.btn_Capture.setGeometry(QRect(190,280,60,51))

        self.btn_Stop = QPushButton(self,"btn_Stop")
        self.btn_Stop.setGeometry(QRect(270,280,60,51))

        self.lbl_Screen = QLabel(self,"lbl_Screen")
        self.lbl_Screen.setGeometry(QRect(30,30,320,240))
        self.lbl_Screen.setFrameShape(QLabel.NoFrame)
        self.lbl_Screen.setFrameShadow(QLabel.Plain)

        ##################################
        # QTimer Object
        self.timer = QTimer(self, "timer")

        self.languageChange()

        self.resize(QSize(371,362).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


        ##################################
        # Cam Object
        self.cam = Cam(self)

        self.connect(self.btn_Start, SIGNAL("clicked()"), self.cam.start)
        self.connect(self.btn_Show, SIGNAL("clicked()"), self.cam.show)
        self.connect(self.btn_Capture, SIGNAL("clicked()"), self.cam.capture)
        self.connect(self.btn_Stop, SIGNAL("clicked()"), self.cam.stop)


    def languageChange(self):
        self.setCaption(self.__tr("Capture"))
        self.btn_Start.setText(self.__tr("Start"))
        self.btn_Show.setText(self.__tr("Show"))
        self.btn_Capture.setText(self.__tr("Capture"))
        self.btn_Stop.setText(self.__tr("Stop"))
        self.lbl_Screen.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("form_Capture_New",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = form_Capture_New()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
