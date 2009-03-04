#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import dbus

from PyQt4 import QtGui
from PyQt4 import QtCore

from ui_mainwindow import Ui_MainManager
from interface import ComarIface, PisiIface
from listitem import *

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        super(MainManager, self).__init__(parent)

        self.ui = Ui_MainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        self.item_model = OperationDataModel()

        self.cface = ComarIface()
        self.pface = PisiIface()

        self.cface.listen(self.handler)
        self.loadHistory()

    def loadHistory(self):
        for operation in self.pface.historyDb().get_last():
            self.item_model.items.append(NewOperation(operation))

    def handler(self, package, signal, args):
        print package, signal, args

    def showPlan(self, op):
        willbeinstalled, willberemoved = self.pface.plan(operation)

