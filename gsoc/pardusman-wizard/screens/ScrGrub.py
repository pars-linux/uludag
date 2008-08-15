#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, uic
import gettext

_ = gettext.gettext

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        uic.loadUi("screens/screenGrub.ui", self)

        self.desc = "grub screen"
        self.frameError.setVisible(0)
        self.chosen = "data/grub-default.jpg"
        self.setImage()
        
        self.connect(self.buttonOpen, QtCore.SIGNAL("clicked()"), self.getImage)
    
    def setImage(self, file = "data/grub-default.jpg"):
        back = QtGui.QPixmap(QtCore.QString(file))
        self.labelBack.setPixmap(back)
        
    def getImage(self):
        file = QtGui.QFileDialog.getOpenFileName(self,  _("Choose new background image"),  ("/home"), _("Images (*.png *.jpg)"))
        
        if not file:
            return 0
        else:
            self.setImage(file)
        
        self.chosen = str(file)
