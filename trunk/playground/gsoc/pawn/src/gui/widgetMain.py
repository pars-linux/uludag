# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgetMain.ui'
#
# Created: Sun Jun 13 15:00:43 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(456, 343)
        self.stackedWidget = QtGui.QStackedWidget(MainWidget)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 60, 441, 231))
        self.stackedWidget.setMaximumSize(QtCore.QSize(551, 16777215))
        self.stackedWidget.setObjectName("stackedWidget")
        self.btnBack = QtGui.QPushButton(MainWidget)
        self.btnBack.setGeometry(QtCore.QRect(0, 300, 71, 41))
        self.btnBack.setObjectName("btnBack")
        self.btnNext = QtGui.QPushButton(MainWidget)
        self.btnNext.setGeometry(QtCore.QRect(380, 300, 71, 41))
        self.btnNext.setObjectName("btnNext")
        self.btnFinish = QtGui.QPushButton(MainWidget)
        self.btnFinish.setGeometry(QtCore.QRect(300, 300, 81, 41))
        self.btnFinish.setObjectName("btnFinish")
        self.lblHeading = QtGui.QLabel(MainWidget)
        self.lblHeading.setGeometry(QtCore.QRect(10, 10, 441, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lblHeading.setFont(font)
        self.lblHeading.setObjectName("lblHeading")

        self.retranslateUi(MainWidget)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QtGui.QApplication.translate("MainWidget", "PArdus Windows iNstaller", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBack.setText(QtGui.QApplication.translate("MainWidget", "<Back", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNext.setText(QtGui.QApplication.translate("MainWidget", "Next>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFinish.setText(QtGui.QApplication.translate("MainWidget", "Finish", None, QtGui.QApplication.UnicodeUTF8))

