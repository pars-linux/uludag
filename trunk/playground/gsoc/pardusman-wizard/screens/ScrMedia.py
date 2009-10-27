#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, uic

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        uic.loadUi("screens/screenMedia.ui", self)

        self.desc = "Media select screen"
        self.frameError.setVisible(0)
        
        self.connect(self.radioCD, QtCore.SIGNAL("clicked()"), self.slotRadio)
        self.connect(self.radioSL, QtCore.SIGNAL("clicked()"), self.slotRadio)
        self.connect(self.radioDL, QtCore.SIGNAL("clicked()"), self.slotRadio)
        self.connect(self.radioExternal, QtCore.SIGNAL("clicked()"), self.slotRadio)
        
        self.sliderSize.setDisabled(1)
        self.spinSize.setDisabled(1)
        
    def slotRadio(self):
        if self.radioExternal.isChecked():
            self.sliderSize.setDisabled(0)
            self.spinSize.setDisabled(0)
        else:
            self.sliderSize.setDisabled(1)
            self.spinSize.setDisabled(1)
        
        self.chosen = str(self.sender().text())
