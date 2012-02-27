# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/hm_window.ui'
#
# Created: Mon Feb 20 12:57:47 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.calendarWidget = QtGui.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(260, 90, 272, 143))
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.allButton = QtGui.QPushButton(self.centralwidget)
        self.allButton.setGeometry(QtCore.QRect(10, 10, 61, 41))
        self.allButton.setText(QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.allButton.setObjectName(_fromUtf8("allButton"))
        self.installsButton = QtGui.QPushButton(self.centralwidget)
        self.installsButton.setGeometry(QtCore.QRect(90, 10, 111, 41))
        self.installsButton.setText(QtGui.QApplication.translate("MainWindow", "Installations", None, QtGui.QApplication.UnicodeUTF8))
        self.installsButton.setObjectName(_fromUtf8("installsButton"))
        self.removalsButton = QtGui.QPushButton(self.centralwidget)
        self.removalsButton.setGeometry(QtCore.QRect(190, 10, 99, 41))
        self.removalsButton.setText(QtGui.QApplication.translate("MainWindow", "Removals", None, QtGui.QApplication.UnicodeUTF8))
        self.removalsButton.setObjectName(_fromUtf8("removalsButton"))
        self.upgradesButton = QtGui.QPushButton(self.centralwidget)
        self.upgradesButton.setGeometry(QtCore.QRect(280, 10, 99, 41))
        self.upgradesButton.setText(QtGui.QApplication.translate("MainWindow", "Upgrades", None, QtGui.QApplication.UnicodeUTF8))
        self.upgradesButton.setObjectName(_fromUtf8("upgradesButton"))
        self.revertsButton = QtGui.QPushButton(self.centralwidget)
        self.revertsButton.setGeometry(QtCore.QRect(370, 10, 99, 41))
        self.revertsButton.setText(QtGui.QApplication.translate("MainWindow", "Reverts", None, QtGui.QApplication.UnicodeUTF8))
        self.revertsButton.setObjectName(_fromUtf8("revertsButton"))
        self.snapshotsButton = QtGui.QPushButton(self.centralwidget)
        self.snapshotsButton.setGeometry(QtCore.QRect(460, 10, 99, 41))
        self.snapshotsButton.setText(QtGui.QApplication.translate("MainWindow", "Snapshots", None, QtGui.QApplication.UnicodeUTF8))
        self.snapshotsButton.setObjectName(_fromUtf8("snapshotsButton"))
        self.detailWidget = QtGui.QWidget(self.centralwidget)
        self.detailWidget.setGeometry(QtCore.QRect(270, 250, 251, 241))
        self.detailWidget.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(165, 165, 165);\n"
"    border-bottom-left-radius: 50px;\n"
"    border-top-right-radius: 50px;\n"
"}"))
        self.detailWidget.setObjectName(_fromUtf8("detailWidget"))
        self.detailListWidget = QtGui.QListWidget(self.detailWidget)
        self.detailListWidget.setGeometry(QtCore.QRect(10, 41, 231, 151))
        self.detailListWidget.setObjectName(_fromUtf8("detailListWidget"))
        self.widgetCloseButton = QtGui.QPushButton(self.detailWidget)
        self.widgetCloseButton.setGeometry(QtCore.QRect(190, 10, 31, 23))
        self.widgetCloseButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../images/dialog-close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.widgetCloseButton.setIcon(icon)
        self.widgetCloseButton.setObjectName(_fromUtf8("widgetCloseButton"))
        self.snapshotButton = QtGui.QPushButton(self.centralwidget)
        self.snapshotButton.setGeometry(QtCore.QRect(20, 490, 81, 61))
        self.snapshotButton.setText(QtGui.QApplication.translate("MainWindow", "Snapshot", None, QtGui.QApplication.UnicodeUTF8))
        self.snapshotButton.setObjectName(_fromUtf8("snapshotButton"))
        self.revertButton = QtGui.QPushButton(self.centralwidget)
        self.revertButton.setGeometry(QtCore.QRect(690, 490, 81, 61))
        self.revertButton.setText(QtGui.QApplication.translate("MainWindow", "Revert", None, QtGui.QApplication.UnicodeUTF8))
        self.revertButton.setObjectName(_fromUtf8("revertButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

