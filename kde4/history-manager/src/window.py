#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus

from PyQt4 import QtGui
from PyQt4 import QtCore

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from mainwindow import Ui_MainManager
from interface import *
from utility import *

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

        self.ops = {}

        self.cface = ComarIface()
        self.pface = PisiIface(self)

        self.connectSignals()

        self.ui.listWidget.installEventFilter(self)
        self.ui.lw.installEventFilter(self)

        self.cface.listen(self.handler)

    def connectSignals(self):
        self.connect(self.pface, SIGNAL("finished()"), self.loadHistory)

        self.connect(self.ui.lw, SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self.loadIndex)
        self.connect(self.ui.operationTB, SIGNAL("currentChanged(int)"), self.tabChanged)
        self.connect(self.ui.restoreTB, SIGNAL("clicked()"), self.takeBack)
        self.connect(self.ui.newSnapshotTB, SIGNAL("clicked()"), self.takeSnapshot)
        self.connect(self.ui.takeBackAction, SIGNAL("triggered()"), self.takeBack)
        self.connect(self.ui.copyAction, SIGNAL("triggered()"), self.copySelected)

    def loadHistory(self):
        self.ui.lw.clear()

        for (k, v) in self.ops.items():
            NewOperation(v, self.ui.lw)

        self.ui.lw.setEnabled(True)
        self.status(i18n("Ready"))
        self.enableButtons(True)

    def tweakUi(self):
        if self.settings.contains("pos") and self.settings.contains("size"):
            self.parent.move(self.mapToGlobal(self.settings.value("pos").toPoint()))
            self.parent.resize(self.settings.value("size").toSize())

        self.parent.setWindowIcon(QtGui.QIcon(":/icons/history-manager.png"))
        self.ui.progressBar.hide()

        self.ui.lw.headerItem().setText(1, i18n("Date"))
        self.ui.lw.headerItem().setText(2, i18n("Time"))
        self.ui.lw.header().resizeSection(0, 40)

        self.ui.lw.header().setResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.lw.header().setResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.lw.header().setResizeMode(2, QHeaderView.Stretch)

        self.enableButtons(False)

    def tabChanged(self, index):
        if index == 1:
            QtCore.QCoreApplication.processEvents()
            self.loadIndex(self.ui.lw.currentItem(), 0)
        elif index == 0:
            self.showPlan()

    def loadIndex(self, item, column):
        self.ui.noLabel.setText("%s <b>%s</b>" % (i18n("No:"), self.get(item, "op_no")))
        self.ui.typeLabel.setText("%s <b>%s</b>" % (i18n("Type:"), self.get(item, "op_type_tr")))
        self.status(i18n("Operation details"))

        self.ui.listWidget.clear()
        self.ui.operationTB.setCurrentIndex(1)

        if self.get(item, "op_type") == "snapshot":
            self.ui.listWidget.insertItem(self.ui.listWidget.count() + 1, \
                    QtGui.QListWidgetItem(i18n("There are %1 packages in this snapshot", self.get(item, "op_pack_len"))))
            return

        # FIXME
        for val in self.get(item, "op_pack"):
            self.ui.listWidget.insertItem(self.ui.listWidget.count() +1, \
                    QtGui.QListWidgetItem(" * %s" % val))

    def showPlan(self):
        if not len(self.ui.lw.selectedIndexes()):
            return
        current_index = self.ui.lw.currentItem()
        current_op = int(self.get(current_index, "op_no"))
        current_type = self.get(current_index, "op_type")
        current_type_tr = self.get(current_index, "op_type_tr")
        current_date = self.get(current_index, "op_date")

        willbeinstalled, willberemoved = self.pface.historyPlan(current_op)
        self.status(i18n("Loading Plan"))

        information = ""
        if current_type == "snapshot":
            configs = self.pface.historyConfigs(current_op)
            if configs and len(configs) != 0:
                information += i18n("Configuration files in snapshot:")
                for i in configs.keys():
                    information += "<br><br><b> %s </b><br>" % i
                    for j in configs.get(i):
                        information += "%s \n" % ("/".join(j.split(str(current_op),1)[1].split(i,1)[1:]))

        message = i18n("Takeback Plan for %1 operation on %2 <br><br>", current_type_tr, current_date)
        self.status(i18n("Takeback Plan %1", current_date))

        if willbeinstalled and len(willbeinstalled) != 0:
            message += i18n("<br> These package(s) will be <b>installed</b> :<br>")
            for i in range(len(willbeinstalled)):
                message += "%s <br>" % willbeinstalled[i]

        if willberemoved and len(willberemoved) != 0:
            message += i18n("<br> These package(s) will be <b>removed</b> :<br>")
            for i in range(len(willberemoved)):
                message += "%s <br>" % willberemoved[i]

        message += "<br>"

        self.ui.textEdit.setText(message + information)

    def changeListing(self):
        self.status(i18n("Listing %1 Operations", QObject.sender(self).objectName()))

    def status(self, txt):
        if self.ui.progressBar.isVisible():
            self.ui.progressBar.setFormat(txt)
            self.ui.opTypeLabel.hide()
        else:
            self.ui.opTypeLabel.setText(txt)
            self.ui.opTypeLabel.show()

    def get(self, item, prop):
        return eval("item.%s" % prop)


    def takeBack(self):
        willbeinstalled, willberemoved = None, None
        try:
            willbeinstalled, willberemoved = self.pface.historyPlan(int(self.get(self.ui.lw.currentItem(), "op_no")))
        except ValueError:
            return

        current_date = self.get(self.ui.lw.currentItem(), "op_date")
        current_time = self.get(self.ui.lw.currentItem(), "op_time")

        reply = QtGui.QMessageBox.warning(self, i18n("Takeback operation verification"),
            i18n("<center>This will restore your system back to : <b>%1</b> - <b>%2</b><br>", current_date, current_time) + \
            i18n("If you're unsure, click Cancel and see TakeBack Plan.</center>"),
             QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

        if reply == QtGui.QMessageBox.Ok:
            self.status(i18n("Taking back to : %1", current_date))
            self.enableButtons(False)

            try:
                QtCore.QCoreApplication.processEvents()
                self.cface.takeBack(int(self.get(self.ui.lw.currentItem(), "op_no")))
            except dbus.DBusException:
                # FIXME
                self.status(i18n("Authentication Failed"))
                self.enableButtons(True)

    def takeSnapshot(self):
        reply = QtGui.QMessageBox.question(self, i18n("Start new snapshot"),
            i18n("<center>This will take a snapshot of your system.<br>Click Ok when you're ready.</center>"),
             QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

        if reply == QtGui.QMessageBox.Cancel:
            return

        self.status(i18n("Taking New Snapshot"))
        self.enableButtons(False)

        try:
            QtCore.QCoreApplication.processEvents()
            self.cface.takeSnap()
        except dbus.DBusException:
            self.status(i18n("Authentication Failed"))
            self.enableButtons(True)

    def handler(self, package, signal, args):
        print package, signal, args

        if signal == "status":
            self.status(" ".join(args))
        elif signal == "finished":
            self.status(i18n("Finished succesfully"))
            self.enableButtons(True)
        elif signal == "progress":
            self.status("%s : %s/100" % (args[2], args[1]))
            self.enableButtons(False)

    def createMenus(self):
        self.lwMenu = QtGui.QMenu()
        self.lwMenu.addAction(self.ui.takeBackAction)

        self.listWidgetMenu = QtGui.QMenu()
        self.listWidgetMenu.addAction(self.ui.copyAction)
        self.listWidgetMenu.addAction(i18n("Select All"), self.ui.listWidget.selectAll)

    def copySelected(self):
        cb = QApplication.clipboard()

        selected = ""
        for i in self.ui.listWidget.selectedItems():
            selected += "%s \n" % i.text().replace('* ', '')

        cb.setText(selected, QtGui.QClipboard.Clipboard)

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
        for val in ["restoreTB", "newSnapshotTB", "operationTB"]:
            exec('self.ui.%s.setEnabled(%s)' % (val, true))
