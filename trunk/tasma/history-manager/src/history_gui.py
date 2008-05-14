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

import Commander
import pisi

historydb = pisi.db.historydb.HistoryDB()

def initDb():
    historydb.init()

class widgetMain(formMain):
    def __init__(self, parent):
        formMain.__init__(self, parent)

        # readOnly means you can't
        self.readOnly = False

        self.command = Commander.Commander(self)
        # selected/previously selected list item
        self.selected = None
        self.previous = None

        # by default shows only snapshot points
        #self.config = self.parent().config
        #if self.config.readEntry("snapshots_only") == "off":
        #    self.snapshotsCheckBox.setChecked(False)

        self.infoTextEdit.setTextFormat(Qt.RichText)
        self.snapshotsListView.clear()
        self.infoTextEdit.clear()
        self.snapshotsListView.setColumnWidth(1, 170)
        self.snapshotsListView.setSortColumn(1)
        self.snapshotsListView.setSortOrder(Qt.Descending)

        self.tabWidget.setTabLabel(self.tabWidget.page(0), i18n("History"))
        self.tabWidget.setTabLabel(self.tabWidget.page(1), i18n("Details"))

        # context menu
        self.popupmenu = QPopupMenu()
        self.popupmenu.insertItem(i18n("Delete Snapshot"), self.delete_snapshot)
        self.popupmenu.insertSeparator()
        self.popupmenu.insertItem(i18n("Restore to This Point"), self.take_back)

        # progress bar
        self.progress = None

        # create list items
        for operation in historydb.get_last():
            self.snapshotsListView.insertItem(widgetItem(self.snapshotsListView, operation))

        # list only snapshots or entire history
        if(self.snapshotsCheckBox.isChecked()):
            self.onlySnapshots(True)

        self.connect(self.tabWidget, SIGNAL("currentChanged(QWidget *)"), self.tabChanged)
        self.connect(self.snapshotsListView, SIGNAL("currentChanged(QListViewItem *)"), self.itemChanged)
        self.connect(self.snapshotsListView, SIGNAL("selectionChanged(QListViewItem *)"), self.itemChanged)
        self.connect(self.snapshotsCheckBox, SIGNAL("stateChanged(int)"), self.onlySnapshots)
        self.connect(self.snapshotsListView, SIGNAL("doubleClicked(QListViewItem *, const QPoint &, int)"), self.slotDoubleClicked)
        self.connect(self.snapshotPushButton, SIGNAL("clicked()"), self.take_snapshot)
        self.connect(self.restorePushButton, SIGNAL("clicked()"), self.take_back)
        self.connect(self.deletePushButton, SIGNAL("clicked()"), self.delete_snapshot)
        self.connect(self.snapshotsListView, SIGNAL("contextMenuRequested(QListViewItem *, const QPoint &, int)"), self.execPopup)
        
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.updateGui()
        else:
            event.ignore()
        
    def execPopup(self, item, point, col):
        if item == None:
            return
        self.snapshotsListView.setSelected(item, True)
        self.selected = item
        self.popupmenu.popup(point)
        
    def take_snapshot(self):
        message = i18n("This will take a New Snapshot")
        if not self.command.inProgress():
            if KMessageBox.Yes == KMessageBox.warningYesNo(self, message, i18n("Warning"), \
                    KGuiItem(i18n("Continue"), "ok"), KGuiItem(i18n("Cancel"), "no"),):
                self.command.takeSnapshot()

    def take_back(self, operation=None):
        if self.selected == None:
            return
        self.__take_back(self.selected.getOpNo())

    def __take_back(self, operation):
        message = i18n("This will take your system back at this point ! \n Are you sure ?")
        if not self.command.inProgress():
            if KMessageBox.Yes == KMessageBox.warningYesNo(self, message, i18n("Warning"), \
                    KGuiItem(i18n("Continue"), "ok"), KGuiItem(i18n("Cancel"), "no"),) and self.selected != None:
                self.command.takeBack(operation)

    def progressBar(self, new=False, header="", message="", timer=0):
        import time
        if new:
            self.progress = KProgressDialog(None, "", header, message, True)
            self.progress.progressBar().setTotalSteps(0)
            self.progress.progressBar().setTextEnabled(False)
            self.progress.show()
            start = time.time()
            while time.time() < start + 120:
                if self.progress.wasCancelled():
                    break
                percent = (time.time() - start) * 10
                self.progress.progressBar().setProgress(percent)
                qApp.processEvents(100)
            self.progress.close()
            self.progress = None
            KMessageBox.sorry(None, i18n("Failed : %s " % header))
        else:
            if self.progress:
                self.progress.close()
                self.progress = None

    def delete_snapshot(self):
        pass

    def done(self):
        KMessageBox.information(None, i18n("A New Snapshot has been taken."))

    def finished(self, data):
        print "finished"
        self.updateGui()

    def displayProgress(self, data):
        print "progress yay"

    def setReadOnly(self, true):
        if true:
            self.readOnly = True
        else:
            self.readOnly = False
        self.updateGui()

    def showErrorMessage(self, message):
        KMessageBox.error(None, message)

    def showWarningMessage(self, message):
        KMessageBox.warning(None, message)

    def updateGui(self):
        """ Updates ListView, buttons etc. """
        self.snapshotsListView.clear()
        initDb()
        for operation in historydb.get_last():
            self.snapshotsListView.insertItem(widgetItem(self.snapshotsListView, operation))
        if self.snapshotsCheckBox.isChecked():
            self.onlySnapshots(True)
        if self.readOnly:
            self.snapshotPushButton.setEnabled(False)
            self.restorePushButton.setEnabled(False)
        else:
            self.snapshotPushButton.setEnabled(True)
            self.restorePushButton.setEnabled(False)

    def pisiNotify(self, operation, args):
        if operation in ["started"]:
            print "operation started"
        elif operation in ["order"]:
            print "ordering packages"
        elif operation in ["removing"]:
            for i in args:
                print "Removing %s" % i
        elif operation in ["removed"]:
            print "package removed"
        elif operation in ["installing"]:
            for i in args:
                print "installing package %s" % i
        elif operation in ["extracting"]:
            for i in args:
                print "extracting package %s" % i
        elif operation in ["configuring"]:
            for i in args:
                print "configuring %s" % i
        elif operation in ["installed"]:
            print "package installed"
        elif operation in ["takingSnapshot"]:
            print "taking snapshot"
        elif operation in ["takingBack"]:
            print "taking back"
        else:
            print "another operation here", operation

    def itemChanged(self, item):
        """ triggered when listviewitem is changed """
        if self.readOnly:
            self.restorePushButton.setEnabled(False)
            self.deletePushButton.setEnabled(False)
            self.snapshotPushButton.setEnabled(False)
        else:
            self.snapshotPushButton.setEnabled(True)
            self.deletePushButton.setEnabled(True)
            self.restorePushButton.setEnabled(True)
        self.previous = self.selected or item
        print "item changed to : ", item.getOpNo()
        self.selected = item

    def tabChanged(self, parent):
        """ when tab widget changes, shows info of selected listitem """
        if(self.tabWidget.indexOf(parent) == 0):
            return
        if(self.selected == None):
            self.infoTextEdit.setText(i18n("Select an entry to view details"))
            return

        self.infoTextEdit.clear()

        information = """
Operation Date : <b>%s</b> at <b>%s</b><br>
Type : <b>%s</b><br>
""" % (self.selected.op_date, self.selected.op_time, self.selected.op_type)

        if self.selected.op_type == 'snapshot':
            information += """
There are <b>%d</b> packages in this snapshot """ % self.selected.getNumPackages()
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


class widgetItem(KListViewItem):
    """ class for listviewitem's """
    def __init__(self, parent, operation):
        KListViewItem.__init__(self, parent)

        if operation:
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



