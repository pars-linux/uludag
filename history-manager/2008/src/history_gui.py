#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *
from kdecore import *
from kdeui import *

from historygui import formMain
from progress import progressForm
from utility import *

import Commander
import pisi

import PisiIface

class widgetMain(formMain):
    def __init__(self, parent):
        # get history database from pisi
        self.historydb = pisi.db.historydb.HistoryDB()

        # init gui
        formMain.__init__(self, parent)

        # help window
        self.help = None
        # progress bar window
        self.progress = widgetProgress(self)
        # pisi commands interface
        self.command = Commander.Commander(self)

        # selected/previously selected list item
        self.selected = None
        # maybe we need it sometime
        self.previous = None
        # id of latest history entry, used while adding
        # new operation to list
        self.latest = 0

        # gui looks better
        self.snapshotsListView.clear()
        self.snapshotsListView.setColumnWidth(0, 10)
        self.snapshotsListView.setColumnWidth(1, 170)
        self.snapshotsListView.setSortColumn(1)
        self.snapshotsListView.setSortOrder(Qt.Descending)
        self.toolBox.setCurrentIndex(1)

        # set labels
        self.setCaption(i18n("History Manager"))
        # show snapshots by default
        self.comboBox.insertItem(i18n("All Operations"), 0)
        self.comboBox.insertItem(i18n("Snapshots"), 1)
        self.comboBox.insertItem(i18n("Upgrades"), 2)
        self.comboBox.insertItem(i18n("Removes"), 3)
        self.comboBox.insertItem(i18n("Installations"), 4)
        self.comboBox.insertItem(i18n("TakeBacks"), 5)
        self.comboBox.setCurrentItem(0)
        self.toolBox.setItemLabel(0, i18n("Take Back Plan"))
        self.toolBox.setItemLabel(1, i18n("Operation Details"))
        self.helpPushButton.setText(i18n("Help"))
        self.restorePushButton.setText(i18n("Restore"))
        self.snapshotPushButton.setText(i18n("New Snapshot"))
        self.snapshotsListView.header().setLabel(0, " ")
        self.snapshotsListView.header().setLabel(1, i18n("Date"))
        self.toolBox.setItemToolTip(0, i18n("Your system will be restored to that date if you click Take Back button.<br>These are the package installation and removals, also configuration files below (in snapshots) will overwrite your current configuration files."))

        # set icons
        self.helpPushButton.setIconSet(loadIconSet("help", KIcon.Small))
        self.restorePushButton.setIconSet(loadIconSet("reload", KIcon.Small))
        self.snapshotPushButton.setIconSet(loadIconSet("add_user", KIcon.Small))
        self.toolBox.setItemIconSet(0, loadIconSet("date", KIcon.Small))
        self.toolBox.setItemIconSet(1, loadIconSet("details", KIcon.Small))

        # context menu
        self.popupmenu = QPopupMenu()
        self.popupmenu.insertItem(loadIconSet("reload", KIcon.Small), i18n("Restore to This Point"), self.take_back)

        # context menu for operation details
        self.oppopup = QPopupMenu()
        self.oppopup.insertItem(i18n("Copy"), self.copyToClipboard)
        self.oppopup.insertItem(i18n("Select All"), self.selectAllOps)

        # this hangs a little bit with a huge history
        self.updateGui()

        # make connections
        self.connect(self.toolBox, SIGNAL("currentChanged(int)"), self.pageChanged)
        self.connect(self.snapshotsListView, SIGNAL("currentChanged(QListViewItem *)"), self.itemChanged)
        self.connect(self.snapshotsListView, SIGNAL("selectionChanged(QListViewItem *)"), self.itemChanged)
        self.connect(self.snapshotPushButton, SIGNAL("clicked()"), self.take_snapshot)
        self.connect(self.restorePushButton, SIGNAL("clicked()"), self.take_back)
        self.connect(self.helpPushButton, SIGNAL("clicked()"), self.showHelp)
        self.connect(self.snapshotsListView, SIGNAL("contextMenuRequested(QListViewItem *, const QPoint &, int)"), self.execPopup)
        self.connect(self.opDetailsListBox, SIGNAL("contextMenuRequested(QListBoxItem *, const QPoint &)"), self.execOpPopup)
        self.connect(self.comboBox, SIGNAL("activated(int)"), self.comboItemChanged)

    # show help window
    def showHelp(self):
        if not self.help:
            self.help = HelpDialog(self)
            self.help.show()
        else:
            self.help.show()

    # re-initialize history database for up to date entries
    def initDb(self):
        self.historydb.init()
        # PisiIface.reloadPisi()
        # self.historydb = pisi.db.historydb.HistoryDB()

    def keyPressEvent(self, event):
        # F5 Key may refresh list
        if event.key() == Qt.Key_F5:
            self.updateGui()
        else:
            event.ignore()

    def execPopup(self, item, point, col):
        # ContextMenu
        if item == None:
            return
        self.snapshotsListView.setSelected(item, True)
        self.selected = item
        self.popupmenu.popup(point)

    def execOpPopup(self, item, point):
        if item == None:
            return
        self.oppopup.popup(point)

    def selectAllOps(self):
        self.opDetailsListBox.selectAll(True)

    def copyToClipboard(self):
        cb = QApplication.clipboard()

        selected = ""
        for i in range(self.opDetailsListBox.count()):
            if self.opDetailsListBox.item(i).isSelected():
                selected += self.opDetailsListBox.item(i).text() + '\n'

        cb.setText(selected, QClipboard.Clipboard)

    def take_snapshot(self):
        self.__take_snapshot()

    def __take_snapshot(self):
        message = i18n("This will take a New Snapshot of your system")
        if not self.command.inProgress():
            if 0 == QMessageBox.question(self, i18n("Warning"), \
                    message, i18n("Continue"), i18n("Cancel")):
                self.enableButtons(False)
                self.progress.reset()
                self.command.takeSnapshot()

    def take_back(self, operation=None):
        if self.selected == None:
            return
        self.__take_back(self.selected.getOpNo())

    def __take_back(self, operation):
        willbeinstalled, willberemoved = PisiIface.getPlan(operation)
        qmessage = i18n("This will restore your system back to : %1 %2\nIf you're unsure, click Cancel and see TakeBack Plan")\
                .arg(self.selected.getDate()).arg(self.selected.getTime())

        if not self.command.inProgress():
            if 0 == QMessageBox.question(self, i18n("Warning"), \
                    qmessage, i18n("Continue"), i18n("Cancel")):
                self.enableButtons(False)
                self.progress.reset()
                self.progress.setTotalSteps((len(willbeinstalled)+len(willberemoved))*2)
                self.command.takeBack(operation)

    def enableButtons(self, true):
        # dont enable buttons in progress
        if self.command.inProgress():
            return
        self.restorePushButton.setEnabled(true)
        self.snapshotPushButton.setEnabled(true)

    def finished(self, data, err=None):
        # this is called after an operation finishes
        # err is error if operation cancelled, a message otherwise
        message = ""
        if data == "System.Manager.takeBack":
            message = i18n("Take Back operation completed")
        elif data == "System.Manager.takeSnapshot":
            message = i18n("New Snapshot Taken")
        elif data == "System.Manager.cancelled":
            message = i18n("Operation Cancelled")
            if err:
                message += ("<br>" + err)
        # update gui after operation
        self.progress.setCurrentOperation(message)
        self.progress.setCurrentOperation(i18n("Updating User Interface"))
        if data == "System.Manager.cancelled":
            self.progress.setCurrentOperation(i18n("Finished with Errors"))
            self.showErrorMessage(i18n("Operation Finished with Errors"))
        else:
            # this adds last operation from db to list
            self.addLast()
            self.progress.setCurrentOperation(i18n("Finished Succesfully"))
        self.enableButtons(True)
        self.progress.hide()

    def displayProgress(self, data):
        try:
            operation, percent, message = data
            self.progress.updateProgressBar(percent)
        except ValueError:
            try:
                operation, package, percent, area, speed, hede, hodo = data
                self.progress.progressTextLabel.setText(i18n("Fetching %1").arg(package))
                self.progress.setSteps(percent)
                if percent == 100:
                    self.progress.increase()
            except ValueError:
                pass

    def showErrorMessage(self, message):
        QMessageBox.critical(self, i18n("Error"), message, i18n("OK"))

    def showWarningMessage(self, message):
        QMessageBox.warning(self, i18n("Warning"), message, i18n("OK"))

    def updateGui(self):
        """ Updates ListView, buttons etc. """
        self.snapshotsListView.clear()
        self.initDb()
        for operation in self.historydb.get_last():
            item = widgetItem(self.snapshotsListView, operation)
            # need this while updating gui after an operation
            if operation.no > self.latest:
                self.latest = operation.no
            # not "All Operations"
            if self.comboBox.currentItem() != 0:
                if (item.getTypeInt() != self.comboBox.currentItem()):
                    item.setVisible(False)

    def addLast(self):
        """ after an operation, add latest operation to list """
        self.initDb()
        op = self.historydb.get_last()
        op = op.next()
        if op.no > self.latest:
            self.latest = op.no
        self.snapshotsListView.insertItem(widgetItem(self.snapshotsListView, op))

    def pisiNotify(self, operation, args):
        """ notify gui of pisi events """
        if operation in ["policy_auth_admin"]:
            # starting authentication
            pass
        elif operation in ["policy_yes"]:
            # access granted
            self.progress.show()
            self.progress.setCurrentOperation(i18n("<b>Access Granted</b><br>"))
        elif operation in ["policy_no"]:
            # not allowed
            self.showErrorMessage(i18n("<b>Access Denied</b><br>"))
        elif operation in ["started"]:
            self.progress.setCurrentOperation(i18n("Operation Started"))
        elif operation in ["order"]:
            self.progress.setCurrentOperation(i18n("Ordering Packages for Operation"))
        elif operation in ["removing"]:
            for i in args:
                self.progress.setCurrentOperation(i18n("Removing    : %1").arg(i))
        elif operation in ["removed"]:
            self.progress.increase(2)
        elif operation in ["installing"]:
            for i in args:
                self.progress.setCurrentOperation(i18n("Installing  : %1").arg(i))
        elif operation in ["extracting"]:
            for i in args:
                self.progress.setCurrentOperation(i18n("Extracting  : %1").arg(i))
        elif operation in ["configuring"]:
            for i in args:
                self.progress.setCurrentOperation(i18n("Configuring  : %1").arg(i))
        elif operation in ["installed"]:
            self.progress.increase()
        elif operation in ["takingSnapshot"]:
            self.progress.setHeader(i18n("Taking a Snapshot of System "))
        elif operation in ["takingBack"]:
            self.progress.setHeader(i18n("Taking System Back to %1 %2 <br>").arg(self.selected.getDate()).arg(self.selected.getTime()))
        else:
            # another signal, unhandled
            print "another operation here", operation

    def comboItemChanged(self, num):
        self.showOperations()
        self.showOperations(num)

    def itemChanged(self, item):
        """ triggered when a listviewitem is changed """
        self.previous = self.selected or item
        self.selected = item
        self.restorePushButton.setEnabled(True)
        self.toolBox.setCurrentIndex(1)
        self.pageChanged(self.toolBox.currentIndex())

    def pageChanged(self, num):
        """ when toolbox pages change, this function is called """
        if self.selected == None:
            self.opDetailsListBox.clear()
            self.opDetailsListBox.insertItem(i18n("Select an entry to view details"))
            self.planTextEdit.setText(i18n("Select an entry to view details"))
            return

        self.noLabel.setText(i18n("No: <b>%1</b>").arg(self.selected.getOpNo()))
        self.typeLabel.setText(i18n("Type: <b>%1</b>").arg(self.selected.getTypeTr()))
        if num == 0:
            self.setTakeBackPlan()
            return

        information = ""

        self.opDetailsListBox.clear()
        self.planTextEdit.clear()

        if self.selected.getType() == 'snapshot':
            self.opDetailsListBox.insertItem(\
                    i18n("There are %1 packages in this snapshot")\
                    .arg(self.selected.getNumPackages()))
            return

        for package in self.selected.op_pack:
            self.opDetailsListBox.insertItem("* %s" % package.__str__())

    def setTakeBackPlan(self):
        willbeinstalled, willberemoved = PisiIface.getPlan(self.selected.getOpNo())

        information = ""
        if self.selected.getType() == 'snapshot':
            # configuration files in a snapshot
            configs = self.historydb.get_config_files(self.selected.getOpNo())
            if len(configs) != 0:
                information += "<br>" + i18n("Configuration files in snapshot:")
                for i in configs.keys():
                    information += "<br><br><b>" + i + "</b><br>"
                    for j in configs.get(i):
                        information += "/".join(j.split(str(self.selected.getOpNo()),1)[1].split(i,1)[1:])
            self.planTextEdit.setText(information)

        message = i18n("Take Back Plan for %1 operation on %2")\
                .arg(self.selected.getTypeTr()).arg(self.selected.getDate()) + "<br><br>"
        if len(willbeinstalled) != 0:
            message += "<br>" + i18n("These package(s) will be <b>installed</b> :") + "<br>"
            for i in range(len(willbeinstalled)):
                message += willbeinstalled[i] + "<br>"

        if len(willberemoved) != 0:
            message += "<br>" + i18n("These package(s) will be <b>removed</b> :") + "<br>"
            for i in range(len(willberemoved)):
                message += willberemoved[i] + "<br>"

        message += "<br>"
        self.planTextEdit.setText(message + information)


    def showOperations(self, operation=None):
        """ Shows only operation, or all history if operation is None """
        it = QListViewItemIterator(self.snapshotsListView)
        itm = it.current()
        while itm:
            if operation:
                if itm.getTypeInt() != int(operation):
                    itm.setVisible(False)
                else:
                    itm.setVisible(True)
            else:
                itm.setVisible(True)
            it += 1
            itm = it.current()

        # sorts by date
        self.snapshotsListView.sort()

    def slotDoubleClicked(self, item, pos, var):
        """ open more info tab if doubleclicked """
        self.snapshotsListView.setCurrentItem(item)
        self.tabWidget.setCurrentPage(1)

class widgetProgress(progressForm):
    """ progress bar widget """
    def __init__(self, parent=None, steps=100):
        progressForm.__init__(self, parent)

        self.parent = parent
        self.setCaption(i18n("Progress"))
        animatedPisi = QMovie(locate("data","package-manager/pisianime.gif"))
        self.animeLabel.setMovie(animatedPisi)

        self.progressBar.setTotalSteps(steps)

        self.connect(self.cancelPushButton, SIGNAL("clicked()"), self.checkCancelandClose)

    def checkCancelandClose(self):
        self.parent.command.cancel()
        self.hide()

    def enableCancel(self, true):
        self.cancelPushButton.setEnabled(true)

    def setCurrentOperation(self, mes):
        self.progressTextLabel.setText(mes)

    def setHeader(self, mes):
        self.bigTextLabel.setText("<h4><b>%s</b></h4>" % mes)

    def updateProgressBar(self, progress, totalSteps=None):
        if totalSteps:
            self.progressBar.setProgress(float(progress), totalSteps)
            return
        self.progressBar.setProgress(float(progress))

    def reset(self):
        self.setCurrentOperation(i18n("<b>Preparing PiSi...</b>"))
        self.progressBar.setProgress(0)
        self.progressBar.setTotalSteps(100)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            return
        else:
            progressForm.keyPressEvent(self, event)

    def setTotalSteps(self, num):
        self.progressBar.setTotalSteps(num)

    def setSteps(self, percent):
        self.percentTextLabel.setText("%s%d" % ("%", percent))

    def increase(self, num=1):
        self.progressBar.setProgress(self.progressBar.progress() + num)

class widgetItem(QListViewItem):
    """ class for listviewitem's """

    def __init__(self, parent, operation):
        QListViewItem.__init__(self, parent)

        self.op_no = operation.no
        self.op_type = operation.type
        self.op_date = operation.date
        self.op_time = operation.time
        self.op_pack = operation.packages
        self.op_tag = operation.tag
        self.op_type_int = 0

        self.setText(1, "%s     %s" % (self.op_date, self.op_time))

        # op_type_int = 0 -> All Operations
        if self.op_type == 'snapshot':
            self.setPixmap(0, loadIcon("snapshot", KIcon.Small))
            self.op_type_int = 1
            self.op_type_tr = i18n("snapshot")
        elif self.op_type == 'upgrade':
            self.setPixmap(0, loadIcon("upgrade", KIcon.Small))
            self.op_type_int = 2
            self.op_type_tr = i18n("upgrade")
        elif self.op_type == 'remove':
            self.setPixmap(0, loadIcon("remove", KIcon.Small))
            self.op_type_int = 3
            self.op_type_tr = i18n("remove")
        elif self.op_type == 'install':
            self.setPixmap(0, loadIcon("install", KIcon.Small))
            self.op_type_int = 4
            self.op_type_tr = i18n("install")
        elif self.op_type == 'takeback':
            self.setPixmap(0, loadIcon("takeback", KIcon.Small))
            self.op_type_int = 5
            self.op_type_tr = i18n("takeback")

    def getNumPackages(self):
        return len(self.op_pack)

    def getOpNo(self):
        return self.op_no

    def getDate(self):
        return self.op_date

    def getTime(self):
        return self.op_time

    def getType(self):
        return self.op_type

    def getTypeInt(self):
        return self.op_type_int

    def getTypeTr(self):
        return self.op_type_tr

