# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n

from gui.ScreenWidget import ScreenWidget
from gui.dpiWidget import Ui_dpiWidget

class DpiPreview(QtGui.QLabel):
    def __init__(self, text, initialDpi):
        QtGui.QLabel.__init__(self, text)

        self.scr = QtGui.QX11Info.appScreen()
        self.dpi = initialDpi

    def paintEvent(self, event):
        oldDpiX = QtGui.QX11Info.appDpiX(self.scr)
        oldDpiY = QtGui.QX11Info.appDpiY(self.scr)

        QtGui.QX11Info.setAppDpiX(self.scr, self.dpi)
        QtGui.QX11Info.setAppDpiY(self.scr, self.dpi)

        QtGui.QLabel.paintEvent(self, event)

        QtGui.QX11Info.setAppDpiX(self.scr, oldDpiX)
        QtGui.QX11Info.setAppDpiY(self.scr, oldDpiY)

    def setDpi(self, value):
        self.dpi = value
        self.repaint()

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Welcome")
    desc = ki18n("Welcome to Kaptan Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_dpiWidget()
        self.ui.setupUi(self)

        currentDpi = QtGui.QX11Info.appDpiX()
        self.pv = DpiPreview(ki18n("This is a sample text using 10 point font.").toString(), currentDpi)
        self.pv.setWordWrap(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pv.setFont(font)
        self.pv.setMinimumSize(200,100)
        self.pv.setAlignment(Qt.AlignTop)

        self.ui.verticalLayout.addWidget(self.pv)
        self.ui.horizontalSlider.valueChanged.connect(self.pv.setDpi)

        self.ui.horizontalSlider.setValue(currentDpi)
        self.ui.spinBox.setValue(currentDpi)
    def shown(self):
        pass

    def execute(self):
        return True


