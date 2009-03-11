#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import dbus

from PyQt4 import QtGui
from PyQt4 import QtCore

from ui_mainwindow import Ui_MainManager
from interface import *
from listitem import *

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        super(MainManager, self).__init__(parent)

        self.ui = Ui_MainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        self.ops = []

        self.item_model = OperationDataModel()
        self.ui.lw.setModel(self.item_model)

        self.cface = ComarIface()
        self.pface = PisiIface(self)

        self.connectSignals()
        self.cface.listen(self.handler)

    def connectSignals(self):
        for val in ["Snapshot", "Install", "Remove", "Update", "Takeback"]:
            exec('self.connect(self.ui.%s, SIGNAL("clicked()"), self.changeListing)' % val)
        self.connect(self.pface, SIGNAL("finished()"), self.loadHistory)

    def loadHistory(self):
        for i in self.ops:
            self.item_model.items.append(NewOperation(i))
        self.item_model.reset()
        self.ui.lw.setEnabled(True)
        self.ui.opTypeLabel.setText("- All Operations")
        self.ui.lw.adjustSize()

    def handler(self, package, signal, args):
        pass

    def showPlan(self, op):
        willbeinstalled, willberemoved = self.pface.plan(operation)

    def changeListing(self):
        self.ui.opTypeLabel.setText("- Listing %s Operations" % QObject.sender(self).objectName())

