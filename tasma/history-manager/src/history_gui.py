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
        self.infoProgressBar.hide()
        self.infoTextEdit.setReadOnly(True)
        self.snapshotsListView.clear()
        self.infoTextEdit.clear()
        self.snapshotsListView.setColumnWidth(0, 10)
        self.snapshotsListView.setColumnWidth(1, 10)
        self.snapshotsListView.setColumnWidth(2, 170)
        self.snapshotsListView.setSortColumn(2)
        self.snapshotsListView.setSortOrder(Qt.Descending)

        # set labels
        self.setCaption(i18n("History Manager"))
        self.snapshotsCheckBox.setText(i18n("List only snapshots"))
        self.tabWidget.setTabLabel(self.tabWidget.page(0), i18n("History"))
        self.tabWidget.setTabLabel(self.tabWidget.page(1), i18n("Details"))
        self.helpPushButton.setText(i18n("Help"))
        self.restorePushButton.setText(i18n("Restore"))
        self.snapshotPushButton.setText(i18n("New Snapshot"))
        self.snapshotsListView.header().setLabel(0, " ")
        self.snapshotsListView.header().setLabel(1, i18n("Id"))
        self.snapshotsListView.header().setLabel(2, i18n("Date"))
        self.snapshotsListView.header().setLabel(3, i18n("Type"))

        # set icons
        self.helpPushButton.setIconSet(loadIconSet("help", KIcon.Small))
        self.restorePushButton.setIconSet(loadIconSet("reload", KIcon.Small))
        self.snapshotPushButton.setIconSet(loadIconSet("add_user", KIcon.Small))
        self.tabWidget.setTabIconSet(self.tabWidget.page(0), loadIconSet("History_Manager", KIcon.Small))
        self.tabWidget.setTabIconSet(self.tabWidget.page(1), loadIconSet("details", KIcon.Small))

        # context menu
        self.popupmenu = QPopupMenu()
        self.popupmenu.insertItem(loadIconSet("details", KIcon.Small), i18n("Show Details"), self.changeTab)
        self.popupmenu.insertSeparator()
        self.popupmenu.insertItem(loadIconSet("reload", KIcon.Small), i18n("Restore to This Point"), self.take_back)

        # this hangs a little bit with a huge history
        self.updateGui()

        # make connections
        self.connect(self.tabWidget, SIGNAL("currentChanged(QWidget *)"), self.tabChanged)
        self.connect(self.snapshotsListView, SIGNAL("currentChanged(QListViewItem *)"), self.itemChanged)
        self.connect(self.snapshotsListView, SIGNAL("selectionChanged(QListViewItem *)"), self.itemChanged)
        self.connect(self.snapshotsCheckBox, SIGNAL("stateChanged(int)"), self.onlySnapshots)
        self.connect(self.snapshotsListView, SIGNAL("doubleClicked(QListViewItem *, const QPoint &, int)"), self.slotDoubleClicked)
        self.connect(self.snapshotPushButton, SIGNAL("clicked()"), self.take_snapshot)
        self.connect(self.restorePushButton, SIGNAL("clicked()"), self.take_back)
        self.connect(self.helpPushButton, SIGNAL("clicked()"), self.showHelp)
        self.connect(self.snapshotsListView, SIGNAL("contextMenuRequested(QListViewItem *, const QPoint &, int)"), self.execPopup)

    # show help window
    def showHelp(self):
        if not self.help:
            self.help = HelpDialog(self)
            self.help.show()
        else:
            self.help.show()

    # change tabwidget's tab
    def changeTab(self):
        self.tabWidget.showPage(self.tabWidget.page(1-self.tabWidget.currentPageIndex()))

    # re-initialize history database for up to date entries
    def initDb(self):
        self.historydb.init()

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

    def take_snapshot(self):
        self.__take_snapshot()

    def __take_snapshot(self):
        message = i18n("This will take a New Snapshot of your system")
        if not self.command.inProgress():
            if 0 == QMessageBox.question(self, i18n("Warning"), \
                    message, i18n("Continue"), i18n("Cancel")):
                self.enableButtons(False)
                self.command.takeSnapshot()

    def take_back(self, operation=None):
        if self.selected == None:
            return
        self.__take_back(self.selected.getOpNo())

    def __take_back(self, operation):
        message = i18n("This will restore your system back to : %1 %2\nAre you sure ?")\
                  .arg(self.selected.getDate()).arg(self.selected.getTime())
        if not self.command.inProgress():
            if 0 == QMessageBox.question(self, i18n("Warning"), \
                    message, i18n("Continue"), i18n("Cancel")):
                self.enableButtons(False)
                self.command.takeBack(operation)

    def delete_snapshot(self):
        # wont delete snapshots for now
        pass

    def enableButtons(self, true):
        # dont enable buttons in progress
        if self.command.inProgress():
            return
        self.restorePushButton.setEnabled(true)
        self.snapshotPushButton.setEnabled(true)

    def finished(self, data, err=None):
        # this is called after an operation finishes
        # err is error if operation cancelled, a message otherwise
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
            if self.snapshotsCheckBox.isChecked():
                if item.getType() != 'snapshot':
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
            self.progress.reset()
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
            self.infoTextEdit.append(i18n("OK") + "<br>")
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
            self.infoTextEdit.append(i18n("OK") + "<br>")
        elif operation in ["takingSnapshot"]:
            self.progress.setHeader(i18n("Taking a Snapshot of System "))
        elif operation in ["takingBack"]:
            self.progress.setHeader(i18n("Taking System Back to %1 %2 <br>").arg(self.selected.getDate()).arg(self.selected.getTime()))
        else:
            # another signal, unhandled
            print "another operation here", operation

    def itemChanged(self, item):
        """ triggered when a listviewitem is changed """
        self.previous = self.selected or item
        self.selected = item
        self.restorePushButton.setEnabled(True)

    def tabChanged(self, parent):
        """ when tab widget changes, shows info of selected listitem """
        if(self.tabWidget.indexOf(parent) == 0):
            return
        if(self.selected == None):
            self.infoTextEdit.setText(i18n("Select an entry to view details"))
            return

        self.infoTextEdit.clear()

        # weird information strings
        information = i18n("<b>Operation Date : </b>%1 %2<br><b>Operation Type : </b>%3<br>")\
                      .arg(self.selected.getDate()).arg(self.selected.getTime()).arg(self.selected.getType())

        # FIXME show packages and configuration files in a snapshot
        if self.selected.getType() == 'snapshot':
            information += i18n("There are <b>%1</b> packages in this snapshot").arg(self.selected.getNumPackages())
            self.infoTextEdit.setText(information)
            return

        for package in self.selected.op_pack:
            information += "%s %s" % (package.__str__(), "<br>")

        self.infoTextEdit.setText(information)

    def onlySnapshots(self, var):
        """ Shows only snapshots if var is True, else shows all history """
        it = QListViewItemIterator(self.snapshotsListView)
        itm = it.current()
        while itm:
            if itm.op_type != 'snapshot':
                if var:
                    itm.setVisible(False)
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
    def __init__(self, parent=None, steps=0):
        progressForm.__init__(self, parent)

        self.parent = parent
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
        self.bigTextLabel.setText("<h3><b>%s</b></h3>" % mes)

    def updateProgressBar(self, progress):
        self.progressBar.setProgress(float(progress))

    def reset(self):
        self.setCurrentOperation(i18n("<b>Preparing PiSi...</b>"))
        self.progressBar.setProgress(0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            return
        else:
            progressForm.keyPressEvent(self, event)

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

        self.setText(1, str(self.op_no))
        self.setText(2, "%s %s" % (self.op_date, self.op_time))
        self.setText(3, self.op_type)

        if self.op_type == 'snapshot':
            self.setPixmap(0, loadIcon("snapshot", KIcon.Small))
        elif self.op_type == 'upgrade':
            self.setPixmap(0, loadIcon("upgrade", KIcon.Small))
        elif self.op_type == 'remove':
            self.setPixmap(0, loadIcon("remove", KIcon.Small))
        elif self.op_type == 'install':
            self.setPixmap(0, loadIcon("install", KIcon.Small))
        elif self.op_type == 'takeback':
            self.setPixmap(0, loadIcon("takeback", KIcon.Small))

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

