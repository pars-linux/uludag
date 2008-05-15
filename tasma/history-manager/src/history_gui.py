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
from utility import *

import Commander
import pisi

class widgetMain(formMain):
    def __init__(self, parent):
        self.historydb = pisi.db.historydb.HistoryDB()
        formMain.__init__(self, parent)

        # readOnly means you can't
        self.readOnly = False
        self.help = None

        self.command = Commander.Commander(self)
        # selected/previously selected list item
        self.selected = None
        self.previous = None

        # gui looks better
        self.infoProgressBar.hide()
        self.infoTextEdit.setReadOnly(True)
        self.snapshotsListView.clear()
        self.infoTextEdit.clear()
        self.snapshotsListView.setColumnWidth(0, 10)
        self.snapshotsListView.setColumnWidth(1, 170)
        self.snapshotsListView.setSortColumn(1)
        self.snapshotsListView.setSortOrder(Qt.Descending)

        # set labels
        self.setCaption(i18n("History Manager"))
        self.snapshotsCheckBox.setText(i18n("List only snapshots"))
        self.tabWidget.setTabLabel(self.tabWidget.page(0), i18n("History"))
        self.tabWidget.setTabLabel(self.tabWidget.page(1), i18n("Details"))
        self.helpPushButton.setText(i18n("Help"))
        self.restorePushButton.setText(i18n("Restore"))
        self.snapshotPushButton.setText(i18n("New Snapshot"))
        self.snapshotsListView.header().setLabel(0, i18n("Id"))
        self.snapshotsListView.header().setLabel(1, i18n("Date"))
        self.snapshotsListView.header().setLabel(2, i18n("Type"))

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

        # create list items
        for operation in self.historydb.get_last():
            self.snapshotsListView.insertItem(widgetItem(self.snapshotsListView, operation))

        # list only snapshots or entire history
        if(self.snapshotsCheckBox.isChecked()):
            self.onlySnapshots(True)

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

    def showHelp(self):
        if not self.help:
            self.help = HelpDialog(self)
            self.help.show()
        else:
            self.help.show()

    def changeTab(self):
        self.tabWidget.showPage(self.tabWidget.page(1-self.tabWidget.currentPageIndex()))

    def initDb(self):
        self.historydb.init()

    def keyPressEvent(self, event):
        # F5 Key refreshes list
        if event.key() == Qt.Key_F5:
            self.updateGui()
        else:
            event.ignore()

    def execPopup(self, item, point, col):
        # ContextMenu pops up
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
                self.snapshotsListView.clear()
                qApp.processEvents(100)
                self.command.takeSnapshot()

    def take_back(self, operation=None):
        if self.selected == None:
            # this should not happed
            print "hello, someone's trying to take_back to None"
            return
        self.__take_back(self.selected.getOpNo())

    def __take_back(self, operation):
        message = i18n("This will restore your system back to : %1 %2\nAre you sure ?")\
                  .arg(self.selected.getDate()).arg(self.selected.getTime())
        if not self.command.inProgress():
            if 0 == QMessageBox.question(self, i18n("Warning"), \
                    message, i18n("Continue"), i18n("Cancel")):
                self.enableButtons(False)
                self.snapshotsListView.clear()
                qApp.processEvents(100)
                self.command.takeBack(operation)

    def delete_snapshot(self):
        pass

    def enableButtons(self, true):
        self.restorePushButton.setEnabled(true)
        self.snapshotPushButton.setEnabled(true)
        self.tabWidget.setTabEnabled(self.tabWidget.page(0), true)

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
                message += err
        # update gui after operation
        self.infoTextEdit.append(message)
        self.infoTextEdit.append(i18n("Updating User Interface, please wait a while"))
        qApp.processEvents(100)
        self.updateGui()
        if data == "System.Manager.cancelled":
            self.infoTextEdit.append(i18n("Finished with Errors"))
        else:
            self.infoTextEdit.append(i18n("Finished Succesfully"))
        self.enableButtons(True)

    def displayProgress(self, data):
        print "progress yay"

    def setReadOnly(self, true):
        # This disables gui from starting any operation
        if true:
            self.readOnly = True
        else:
            self.readOnly = False
        self.updateGui()

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
            if self.snapshotsCheckBox.isChecked():
                if item.getType() != 'snapshot':
                    item.setVisible(False)
            self.snapshotsListView.insertItem(widgetItem(self.snapshotsListView, operation))
        if self.readOnly:
            self.snapshotPushButton.setEnabled(False)
            self.restorePushButton.setEnabled(False)
        else:
            self.snapshotPushButton.setEnabled(True)
            self.restorePushButton.setEnabled(False)

    def startProgress(self):
        # qt3 is deprecated
        pass

    def pisiNotify(self, operation, args):
        """ notify gui of events """
        if operation in ["policy_yes"]:
            self.tabWidget.setCurrentPage(1)
            self.infoTextEdit.clear()
            self.startProgress()
            self.infoTextEdit.append(i18n("<b>Access Granted</b><br>"))
        elif operation in ["policy_no"]:
            self.tabWidget.setCurrentPage(1)
            self.infoTextEdit.clear()
            self.infoTextEdit.append(i18n("<b>Access Denied</b><br>"))
        elif operation in ["started"]:
            self.infoTextEdit.append(i18n("Operation Started"))
        elif operation in ["order"]:
            self.infoTextEdit.append(i18n("Ordering Packages for Operation"))
        elif operation in ["removing"]:
            for i in args:
                self.infoTextEdit.append(i18n("Removing    : %1").arg(i))
        elif operation in ["removed"]:
            self.infoTextEdit.append(i18n("OK") + "<br>")
        elif operation in ["installing"]:
            for i in args:
                self.infoTextEdit.append(i18n("Installing  : %1").arg(i))
        elif operation in ["extracting"]:
            for i in args:
                self.infoTextEdit.append(i18n("Extracting  : %1").arg(i))
        elif operation in ["configuring"]:
            for i in args:
                self.infoTextEdit.append(i18n("Configuring  : %1").arg(i))
        elif operation in ["installed"]:
            self.infoTextEdit.append(i18n("OK") + "<br>")
        elif operation in ["takingSnapshot"]:
            self.infoTextEdit.append(i18n("Taking a Snapshot of System ") + "<br>")
        elif operation in ["takingBack"]:
            self.infoTextEdit.append(i18n("Taking System Back to %1 %2 <br>").arg(self.selected.getDate()).arg(self.selected.getTime()))
        else:
            print "another operation here", operation

    def itemChanged(self, item):
        """ triggered when listviewitem is changed """
        if self.readOnly:
            self.restorePushButton.setEnabled(False)
            self.snapshotPushButton.setEnabled(False)
        else:
            self.snapshotPushButton.setEnabled(True)
            self.restorePushButton.setEnabled(True)
        self.previous = self.selected or item
        self.selected = item

    def tabChanged(self, parent):
        """ when tab widget changes, shows info of selected listitem """
        if(self.tabWidget.indexOf(parent) == 0):
            return
        if(self.selected == None):
            self.infoTextEdit.setText(i18n("Select an entry to view details"))
            return

        self.infoTextEdit.clear()

        information = i18n("<b>Operation Date : </b>%1 %2<br><b>Operation Type : </b>%3<br>")\
                      .arg(self.selected.getDate()).arg(self.selected.getTime()).arg(self.selected.getType())

        if self.selected.getType() == 'snapshot':
            information += i18n("There are <b>%1</b> packages in this snapshot").arg(self.selected.getNumPackages())
            self.infoTextEdit.setText(information)
            return

        for package in self.selected.op_pack:
            information += "%s %s" % (package.__str__(), "<br>")

        self.infoTextEdit.setText(information)
        return

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

        self.snapshotsListView.sort()

    def slotDoubleClicked(self, item, pos, var):
        """ open more info tab if doubleclicked """
        self.snapshotsListView.setCurrentItem(item)
        self.tabWidget.setCurrentPage(1)


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

        self.setText(0, str(self.op_no))
        self.setText(1, "%s %s" % (self.op_date, self.op_time))
        self.setText(2, self.op_type)

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



