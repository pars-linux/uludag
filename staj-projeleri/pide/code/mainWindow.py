#!/usr/bin/env python
# coding=UTF-8
#
# Generated by pykdeuic4 from mainWindow.ui on Fri Sep  4 14:41:37 2009
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(265, 307)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(7, 10, 251, 251))
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 265, 23))
        self.menubar.setObjectName("menubar")
        self.menuKurulu_Paketlr = QtGui.QMenu(self.menubar)
        self.menuKurulu_Paketlr.setObjectName("menuKurulu_Paketlr")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuKurulu_Paketlr.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(kdecore.i18n("MainWindow"))
        self.menuKurulu_Paketlr.setTitle(kdecore.i18n("Network Users"))

