#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import dbus

from PyQt4 import QtGui
from PyQt4 import QtCore

from ui_mainwindow import Ui_MainManager
from interface import *
from listitem import *
from utility import *

import time

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        super(MainManager, self).__init__(parent)

        self.ui = Ui_MainManager()
        self.parent = parent

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        self.settings = QtCore.QSettings()
        self.createMenus()
        self.tweakUi()

        self.ops = []
        self.help = None

        self.proxyModel = SortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        self.item_model = OperationDataModel()
        self.proxyModel.setSourceModel(self.item_model)
        self.ui.lw.setModel(self.proxyModel)

        self.cface = ComarIface()
        self.pface = PisiIface(self)

        self.connectSignals()

        self.ui.listWidget.installEventFilter(self)
        self.ui.lw.installEventFilter(self)

        self.cface.listen(self.handler)

    def connectSignals(self):
        for val in ["All", "Snapshot", "Install", "Remove", "Upgrade", "Takeback"]:
            exec('self.connect(self.ui.%s, SIGNAL("clicked()"), self.changeListing)' % val)
        self.connect(self.pface, SIGNAL("finished()"), self.loadHistory)

        self.connect(self.ui.lw, SIGNAL("clicked(const QModelIndex &)"), self.loadIndex)
        self.connect(self.ui.operationTB, SIGNAL("currentChanged(int)"), self.tabChanged)
        self.connect(self.ui.restoreTB, SIGNAL("clicked()"), self.takeBack)
        self.connect(self.ui.newSnapshotTB, SIGNAL("clicked()"), self.takeSnapshot)
        self.connect(self.ui.helpTB, SIGNAL("clicked()"), self.showHelp)
        self.connect(self.ui.takeBackAction, SIGNAL("triggered()"), self.takeBack)
        self.connect(self.ui.copyAction, SIGNAL("triggered()"), self.copySelected)

    def createMenus(self):
        self.lwMenu = QtGui.QMenu()
        self.lwMenu.addAction(self.ui.takeBackAction)

        self.listWidgetMenu = QtGui.QMenu()
        self.listWidgetMenu.addAction(self.ui.copyAction)
        self.listWidgetMenu.addAction("Select All", self.ui.listWidget.selectAll)

    def copySelected(self):
        cb = QApplication.clipboard()

        selected = ""
        for i in self.ui.listWidget.selectedItems():
            selected += "%s \n" % i.text().replace('* ', '')

        cb.setText(selected, QtGui.QClipboard.Clipboard)

    def loadHistory(self):
        for i in self.ops:
            self.item_model.items.append(NewOperation(i))
        self.item_model.reset()
        self.ui.lw.setEnabled(True)

        self.status("Ready")
        self.enableButtons(True)

    def tweakUi(self):
        if self.settings.contains("pos") and self.settings.contains("size"):
            self.parent.move(self.mapToGlobal(self.settings.value("pos").toPoint()))
            self.parent.resize(self.settings.value("size").toSize())

        self.ui.progressBar.hide()
        self.ui.lw.verticalHeader().hide()
        self.ui.lw.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.ui.lw.horizontalHeader().setWindowFlags(Qt.FramelessWindowHint)

        self.enableButtons(False)

    def tabChanged(self, index):
        if index == 1:
            self.loadIndex(self.ui.lw.currentIndex())
        elif index == 0:
            self.showPlan()

    def loadIndex(self, index):
        self.ui.noLabel.setText("No: <b>%s</b>" % self.get(index, "op_no"))
        self.ui.typeLabel.setText("Type: <b>%s</b>" % self.get(index, "op_type_tr"))
        self.status("Operation details")

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
        print package, signal, args

        if signal == "status":
            self.status(" ".join(args))
        elif signal == "finished":
            self.status("Finished succesfully")
            self.enableButtons(True)
        elif signal == "progress":
            self.status("%s : %s/100" % (args[2], args[1]))
            self.enableButtons(False)

    def showPlan(self):
        if not len(self.ui.lw.selectedIndexes()):
            return
        current_index = self.ui.lw.currentIndex()
        current_op = int(self.get(current_index, "op_no"))
        current_type = self.get(current_index, "op_type")
        current_type_tr = self.get(current_index, "op_type_tr")
        current_date = self.get(current_index, "op_date")

        willbeinstalled, willberemoved = self.pface.historyPlan(current_op)
        self.status("Loading Plan")

        information = ""
        if current_type == "snapshot":
            configs = self.pface.historyConfigs(current_op)
            if configs and len(configs) != 0:
                information += "Configuration files in snapshot:"
                for i in configs.keys():
                    information += "<br><br><b> %s </b><br>" % i
                    for j in configs.get(i):
                        information += "%s \n" % ("/".join(j.split(str(current_op),1)[1].split(i,1)[1:]))

        message = "Takeback Plan for %s operation on %s <br><br>" % (current_type_tr, current_date)
        self.status("Takeback Plan %s" % current_date)

        if willbeinstalled and len(willbeinstalled) != 0:
            message += "<br> These package(s) will be <b>installed</b> :<br>"
            for i in range(len(willbeinstalled)):
                message += "%s <br>" % willbeinstalled[i]

        if willberemoved and len(willberemoved) != 0:
            message += "<br> These package(s) will be <b>removed</b> :<br>"
            for i in range(len(willberemoved)):
                message += "%s <br>" % willberemoved[i]

        message += "<br>"

        self.ui.textEdit.setText(message + information)

    def changeListing(self):
        self.status("Listing %s Operations" % QObject.sender(self).objectName())

        self.proxyModel.sortby = QObject.sender(self).objectName().toLower()
        self.proxyModel.sort(ICON, Qt.DescendingOrder)
        self.proxyModel.reset()

    def status(self, txt):
        if self.ui.progressBar.isVisible():
            self.ui.progressBar.setFormat(txt)
            self.ui.opTypeLabel.hide()
        else:
            self.ui.opTypeLabel.setText(txt)
            self.ui.opTypeLabel.show()

    def get(self, index, prop):
        return self.item_model.getProperty(index, prop).toString()

    def showHelp(self):
        if self.help == None:
            self.help = HelpDialog(self)
            self.help.show()
        else:
            self.help.show()

    def takeBack(self):
        willbeinstalled, willberemoved = None, None
        try:
            willbeinstalled, willberemoved = self.pface.historyPlan(int(self.get(self.ui.lw.currentIndex(), "op_no")))
        except ValueError:
            return

        current_date = self.get(self.ui.lw.currentIndex(), "op_date")
        current_time = self.get(self.ui.lw.currentIndex(), "op_time")

        reply = QtGui.QMessageBox.warning(self, "Takeback operation verification",
            "<center>This will restore your system back to : <b>%s</b> - <b>%s</b><br>" % (current_date, current_time) + \
            "If you're unsure, click Cancel and see TakeBack Plan.</center>",
             QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

        if reply == QtGui.QMessageBox.Ok:
            self.status("Taking back to : %s" % current_date)
            self.enableButtons(False)

            try:
                QtCore.QCoreApplication.processEvents()
                self.cface.takeBack(int(self.get(self.ui.lw.currentIndex(), "op_no")))
            except dbus.DBusException:
                self.status("Authentication Failed")
                self.enableButtons(True)

    def takeSnapshot(self):
        reply = QtGui.QMessageBox.question(self, "Start new snapshot",
            "<center>This will take a snapshot of your system.<br>Click Ok when you're ready.</center>",
             QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

        if reply == QtGui.QMessageBox.Cancel:
            return

        self.status("Taking New Snapshot")
        self.enableButtons(False)

        try:
            QtCore.QCoreApplication.processEvents()
            self.cface.takeSnap()
        except dbus.DBusException:
            self.status("Authentication Failed")
            self.enableButtons(True)

    def closeEvent(self, event=None):
        self.settings.setValue("pos", QtCore.QVariant(self.mapToGlobal(self.pos())))
        self.settings.setValue("size", QtCore.QVariant(self.size()))
        self.settings.sync()

        if self.pface.isRunning():
            self.pface.quit()
            self.pface.wait()

        if event != None:
            event.accept()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ContextMenu:
            if obj == self.ui.lw:
                self.lwMenu.popup(event.globalPos())
                return True
            elif obj == self.ui.listWidget:
                self.listWidgetMenu.popup(event.globalPos())
                return True

        elif event.type() == QEvent.Hide:
            self.closeEvent()
            return True

        return QtCore.QObject.eventFilter(self, obj, event)

    def enableButtons(self, true):
        for val in ["All", "Snapshot", "Install", "Remove", "Upgrade", "Takeback", "restoreTB", "newSnapshotTB", "helpTB"]:
            exec('self.ui.%s.setEnabled(%s)' % (val, true))
