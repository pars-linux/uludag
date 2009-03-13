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
        self.tweakUi()

        self.ops = []

        self.item_model = OperationDataModel()
        self.ui.lw.setModel(self.item_model)

        self.cface = ComarIface()
        self.pface = PisiIface(self)

        self.installEventFilter(self)
        self.cface.listen(self.handler)

        self.connectSignals()

    def connectSignals(self):
        for val in ["All", "Snapshot", "Install", "Remove", "Update", "Takeback"]:
            exec('self.connect(self.ui.%s, SIGNAL("clicked()"), self.changeListing)' % val)
        self.connect(self.pface, SIGNAL("finished()"), self.loadHistory)

        self.connect(self.ui.lw, SIGNAL("clicked(const QModelIndex &)"), self.loadIndex)

    def loadHistory(self):
        ''' Load Pisi History to Model Data '''
        for i in self.ops:
            self.item_model.items.append(NewOperation(i))
        self.item_model.reset()
        self.ui.lw.setEnabled(True)
        self.ui.opTypeLabel.setText("- All Operations")
        self.ui.lw.adjustSize()

    def tweakUi(self):
        self.ui.lw.verticalHeader().hide()
        self.ui.lw.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.ui.lw.horizontalHeader().setWindowFlags(Qt.FramelessWindowHint)

    def loadIndex(self, index):
        ''' Load selected index details to Operations Window '''

        self.ui.noLabel.setText("No: <b>%s</b>" % self.get(index, "op_no"))
        self.ui.typeLabel.setText("Type: <b>%s</b>" % self.get(index, "op_type_tr"))

        self.ui.listWidget.clear()
        self.ui.operationTB.setCurrentIndex(1)

        if self.get(index, "op_type") == "snapshot":
            self.ui.listWidget.insertItem(self.ui.listWidget.count() + 1, \
                    QtGui.QListWidgetItem("There are %s packages in this snapshot" % self.get(index, "op_pack_len")))
            return

        for val in self.item_model.getProperty(index, "op_pack").toList():
            self.ui.listWidget.insertItem(self.ui.listWidget.count() +1, \
                    QtGui.QListWidgetItem(" * %s" % val.toString()))

    def handler(self, package, signal, args):
        pass

    def showPlan(self, op):
        willbeinstalled, willberemoved = self.pface.plan(operation)

    def changeListing(self):
        self.ui.opTypeLabel.setText("- Listing %s Operations" % QObject.sender(self).objectName())

    def get(self, index, prop):
        return self.item_model.getProperty(index, prop).toString()

    def closeEvent(self, event):
        # save window pos, and geo
        event.ignore()

    def eventFilter(self, obj, event):
        event_id = event.type()

        return QtGui.QWidget.event(self, event)

