#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, uic

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        uic.loadUi("screens/screenSystemType.ui", self)

        self.desc = "System Type Screen"
        self.frameError.setVisible(0)
        self.chosen = "Install CD"
        
        self.connect(self.radioInstall, QtCore.SIGNAL("clicked()"), self.slotRadio)
        self.connect(self.radioLive, QtCore.SIGNAL("clicked()"), self.slotRadio)

    def slotRadio(self):
        self.chosen = str(self.sender().text())
