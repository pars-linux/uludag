#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, uic

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        uic.loadUi("screens/screenRepo.ui", self)

        self.desc = "Repository Screen"
        
        self.frameError.setVisible(0)
        self.lineOther.setDisabled(1)

        self.connect(self.radioPardus, QtCore.SIGNAL("clicked()"), self.slotContrib)
        self.connect(self.radioOther, QtCore.SIGNAL("clicked()"), self.slotOther)

    def slotContrib(self):
        # self.checkContrib.setDisabled(0)
        self.lineOther.setDisabled(1)

    def slotOther(self):
        self.lineOther.setDisabled(0)
        # self.checkContrib.setDisabled(1)
