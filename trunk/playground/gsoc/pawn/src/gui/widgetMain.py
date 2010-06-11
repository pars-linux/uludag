# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgetMain.ui'
#
# Created: Fri Jun 11 11:58:25 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(602, 343)
        self.verticalLayoutWidget = QtGui.QWidget(MainWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 110, 141, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.navigationLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.navigationLayout.setObjectName("navigationLayout")
        self.logo = QtGui.QLabel(MainWidget)
        self.logo.setGeometry(QtCore.QRect(0, 10, 141, 91))
        self.logo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.logo.setObjectName("logo")
        self.stackedWidget = QtGui.QStackedWidget(MainWidget)
        self.stackedWidget.setGeometry(QtCore.QRect(160, 60, 441, 231))
        self.stackedWidget.setMaximumSize(QtCore.QSize(551, 16777215))
        self.stackedWidget.setObjectName("stackedWidget")
        self.btnBack = QtGui.QPushButton(MainWidget)
        self.btnBack.setGeometry(QtCore.QRect(150, 300, 71, 41))
        self.btnBack.setObjectName("btnBack")
        self.btnNext = QtGui.QPushButton(MainWidget)
        self.btnNext.setGeometry(QtCore.QRect(530, 300, 71, 41))
        self.btnNext.setObjectName("btnNext")
        self.btnFinish = QtGui.QPushButton(MainWidget)
        self.btnFinish.setGeometry(QtCore.QRect(450, 300, 81, 41))
        self.btnFinish.setObjectName("btnFinish")
        self.lblHeading = QtGui.QLabel(MainWidget)
        self.lblHeading.setGeometry(QtCore.QRect(150, 10, 541, 41))
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
        self.logo.setText(QtGui.QApplication.translate("MainWidget", "Logo Label", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBack.setText(QtGui.QApplication.translate("MainWidget", "<Back", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNext.setText(QtGui.QApplication.translate("MainWidget", "Next>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFinish.setText(QtGui.QApplication.translate("MainWidget", "Finish", None, QtGui.QApplication.UnicodeUTF8))

