#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, uic

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        uic.loadUi("screens/screenUsers.ui", self)

        self.desc = "Add user"
        self.frameError.setVisible(0)
        
        self.connect(self.pass1, QtCore.SIGNAL("editingFinished()"), self.checkForm)
        self.connect(self.pass2, QtCore.SIGNAL("editingFinished()"), self.checkForm)
        self.connect(self.username, QtCore.SIGNAL("editingFinished()"), self.checkForm)
        
        self.connect(self.admin_pass1, QtCore.SIGNAL("editingFinished()"), self.checkForm)
        self.connect(self.admin_pass2, QtCore.SIGNAL("editingFinished()"), self.checkForm)
          
    def error(self,  message):
        self.hasError = 1
        self.labelError.setText(message)
        self.frameError.setVisible(1)
    
    def success(self):
        self.hasError = 0
        self.frameError.setVisible(0)
        
    def checkForm(self):
        message = []
        if self.pass2.text() != "" or self.pass1.text() != "":
                if self.pass1.text() != self.pass2.text():
                    message.append("User passwords do not match!")
                else:
                    if self.username.text() == self.pass1.text():
                        message.append("Don't use your user name or name as a password.")

        if self.admin_pass2.text() != "" or self.admin_pass1.text() != "":
                if self.admin_pass1.text() != self.admin_pass2.text():
                    message.append("Admin passwords do not match!")
        
        if message.__len__() == 0:
            self.success()
        else:
            self.error('\n'.join(message))
