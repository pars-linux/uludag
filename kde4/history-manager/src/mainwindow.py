#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import dbus

from PyQt4 import QtGui
from PyQt4 import QtCore

from ui_mainwindow import Ui_MainManager
from interface import ComarIface, PisiIface
from listitem import NewWidgetItem

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_MainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        self.cface = ComarIface()
        self.pface = PisiIface()

        self.cface.listen(self.handler)
        self.getHistory()

    def getHistory(self):
        for operation in self.pface.historyDb().get_last():
            item = NewWidgetItem(self.ui.lw, operation)

    def handler(self, package, signal, args):
        print package, signal, args

    def showPlan(self, op):
        willbeinstalled, willberemoved = self.pface.plan(operation)

