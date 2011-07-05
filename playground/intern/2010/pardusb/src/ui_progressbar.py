# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progressbar.ui'
#
# Created: Sat Aug 21 01:40:33 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(323, 95)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 60, 311, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 281, 20))
        self.label.setText("")
        self.label.setObjectName("label")
        self.line = QtGui.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(100, 40, 118, 3))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

