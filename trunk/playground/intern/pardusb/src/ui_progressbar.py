# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progressbar.ui'
#
# Created: Mon Aug 16 14:43:53 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProgressDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(330, 157)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(40, 90, 251, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 30, 311, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "The Checksum of the image file is checking now...", None, QtGui.QApplication.UnicodeUTF8))

