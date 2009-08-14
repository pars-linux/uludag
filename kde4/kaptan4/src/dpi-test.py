#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DpiPreview(QLabel):
    def __init__(self, text, initialDpi):
        QLabel.__init__(self, text)

        self.scr = QX11Info.appScreen()
        self.dpi = initialDpi

    def paintEvent(self, event):
        #print "*********************"

        oldDpiX = QX11Info.appDpiX(self.scr)
        oldDpiY = QX11Info.appDpiY(self.scr)

        QX11Info.setAppDpiX(self.scr, self.dpi)
        QX11Info.setAppDpiY(self.scr, self.dpi)

        QLabel.paintEvent(self, event)
        qApp.processEvents()

        QX11Info.setAppDpiX(self.scr, oldDpiX)
        QX11Info.setAppDpiY(self.scr, oldDpiY)

    """
    def resizeEvent(self, event):
        self.update()
    """

    def setDpi(self, value):
        self.dpi = value
        self.repaint()

class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        msg = QLabel("Choose DPI value")
        vb = QVBoxLayout()
        sld = QSlider(Qt.Horizontal)
        sld.setMinimum(96)
        sld.setMaximum(400)
        self.pv = DpiPreview("Hello", QX11Info.appDpiX())

        vb.addWidget(msg)
        vb.addWidget(sld)
        vb.addWidget(self.pv)
        self.setLayout(vb)

        sld.valueChanged.connect(self.dpiChanged)

    def dpiChanged(self, value):
        print value
        self.pv.setDpi(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = Main()
    wnd.show()

    app.exec_()
