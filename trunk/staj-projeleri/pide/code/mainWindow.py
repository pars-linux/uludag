#!/usr/bin/env python
# coding=UTF-8
#
# Generated by pykdeuic4 from mainWindow.ui on Mon Sep  7 09:54:25 2009
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(266, 340)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(7, 10, 251, 251))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(75, 266, 97, 24))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 266, 23))
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
        self.pushButton.setText(kdecore.i18n("Servisleri Bul"))
        self.menuKurulu_Paketlr.setTitle(kdecore.i18n("Network Users"))

