# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
#TODO:
#- left right position duzelecek
#- kamera yoksa gorunmeyebilir
# Please read the COPYING file.
#


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import ki18n
from PyKDE4.kdecore import i18n
import ImageQt

from gui.ScreenWidget import ScreenWidget
from gui.avatarWidget import Ui_Form

import subprocess
import os

import Image
import select
import v4l2capture

class Widget(QtGui.QWidget, ScreenWidget):

    title = ki18n("Kullanıcı profili")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self, None)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.drawCrop = DrawCropMask(self.ui.camGoruntu)

        Widget.desc = QVariant(unicode("Kullanıcı profilinizi oluşturun"))

        self.pictureTaken = 0

        for dev in os.listdir("/dev"):
            if dev.startswith("video"):
                cam = v4l2capture.Video_device(os.path.join("/dev", dev))
                cam_driver, cam_card, cam_bus, cam_capabilities = cam.get_info()
                cam_str = "%s - %s" % (cam_card, os.path.join("/dev", dev))

                if "video_capture" in cam_capabilities:
                    if "radio" in cam_capabilities or "tuner" in cam_capabilities:
                        continue
                    self.ui.comboBox.addItem(cam_str)

        self.timer = QtCore.QTimer(self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.refreshCam)
        self.connect(self.ui.comboBox, QtCore.SIGNAL('activated(QString)'), self.activateCam)
        self.connect(self.ui.saveButton, QtCore.SIGNAL('clicked()'), self.savePicture)
        self.connect(self.ui.takeButton, QtCore.SIGNAL('clicked()'), self.showPicture)
        self.connect(self.ui.takeAgainButton, QtCore.SIGNAL('clicked()'), self.activateCam)
        self.connect(self.ui.chooseFileButton, QtCore.SIGNAL('clicked()'), self.chooseFile)

        self.ui.saveButton.hide()
        self.ui.takeAgainButton.hide()

    def activateCam(self):
        # Skip first item
        if self.ui.comboBox.currentIndex() == 0:
            return

        self.ui.takeButton.show()
        self.ui.saveButton.hide()
        self.ui.takeAgainButton.hide()
        self.timer.stop()
        cam = str(self.ui.comboBox.currentText())
        cam = cam.split("-")[1].strip()
        self.video = v4l2capture.Video_device(cam)

        self.size_x, self.size_y = self.video.set_format(320, 240)
        self.video.create_buffers(10)
        self.video.queue_all_buffers()
        self.video.start()

        select.select((self.video,), (), ())

        self.timer.setInterval(30)
        self.timer.start()

    def refreshCam(self):
        try:
            self.image_data = self.video.read_and_queue()
            self.image_raw = Image.fromstring("RGB", (self.size_x, self.size_y), self.image_data)
            self.image = ImageQt.ImageQt(self.image_raw).mirrored(True, False)
            self.ui.camGoruntu.setPixmap(QtGui.QPixmap.fromImage(self.image))
            self.updateCropMask()
        except:
            pass

    def showPicture(self):
        self.timer.stop()
        self.video.stop()
        self.ui.saveButton.show()
        self.ui.takeAgainButton.show()
        self.ui.takeButton.hide()

    def savePicture(self):
        self.pictureTaken = 1
        home = os.path.expanduser("~")
        self.image.save("profilim.jpg")
        self.foto = Image.open("profilim.jpg")
        self.space = (85, 70, 235, 195)
        self.paste = self.foto.crop(self.space)
        self.paste.save(home + "/new.jpg")
        os.rename(home + "/new.jpg", home + "/.face.icon")

    def shown(self):
        pass

    def execute(self):
        if not self.pictureTaken == 1:
            self.timer.stop()
            try:
                self.video.stop()
            except:
                pass

        return True

    def chooseFile(self):
        self.selectedFile = QFileDialog.getOpenFileName(None,"Open Image", os.environ["HOME"], 'Image Files (*.png *.jpg *bmp)')
        print self.selectedFile

        if self.selectedFile.isNull():
            return
        else:
            home = os.path.expanduser("~")

        self.ui.camGoruntu.setPixmap(QtGui.QPixmap(str(self.selectedFile)))
        self.ui.camGoruntu.update()

        self.paste.save(home + "/new2.jpg")
        os.rename(home + "/new2.jpg", home + "/.face.icon")


class DrawCropMask(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(QtCore.QRect(0, 0, 320, 240))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(20,20,20, 0))
        painter.setBrush(QBrush(QColor(0, 0, 0, 200)))

        rect = QRect(0, 0, 85, 240) # x, y, w, h
        rect2 = QRect(85, 0, 150, 45) 
        rect3 = QRect(235, 0, 85, 240)
        rect4 = QRect(85, 195, 150, 45)
        painter.drawRect(rect)
        painter.drawRect(rect2)
        painter.drawRect(rect3)
        painter.drawRect(rect4)

        painter.setBrush(QBrush(QColor(20, 20, 20, 100)))

        painter.end()

    def updateCropMask(self):
        self.update()
