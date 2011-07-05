# -*- coding: utf-8

from qt import *
from kdeui import *
from kdecore import *

import pisi

#from pisi import specfile as spec
#from pisi.dependency import Dependency
#from pisi.conflict import Conflict
#from pisi.replace import Replace
import os
import shutil

import kdedesigner

from pakito.gui.pspecWidget.historyWidgetUI import HistoryWidgetUI
from pakito.gui.pspecWidget.dialogs.historyDialog import HistoryDialog
from pakito import xmlUtil

class historyWidget(HistoryWidgetUI):
    def __init__(self, parent,xmlUtil):
        HistoryWidgetUI.__init__(self, parent)
        il = KGlobal.iconLoader()

        self.xmlUtil = xmlUtil

        self.pbAddHistory.setIconSet(il.loadIconSet("edit_add", KIcon.Toolbar))
        self.pbRemoveHistory.setIconSet(il.loadIconSet("edit_remove", KIcon.Toolbar))
        self.pbBrowseHistory.setIconSet(il.loadIconSet("fileopen", KIcon.Toolbar))

        self.connect(self.pbAddHistory, SIGNAL("clicked()"), self.slotAddHistory)
        self.connect(self.pbRemoveHistory, SIGNAL("clicked()"), self.slotRemoveHistory)
        self.connect(self.pbBrowseHistory, SIGNAL("clicked()"), self.slotBrowseHistory)
        self.connect(self.lvHistory, SIGNAL("executed(QListViewItem *)"), self.slotBrowseHistory)

        self.lvHistory.setSorting(-1)


    def addRelease(self, rel, reverse=False):
        if not rel.type:
            rel.type = ""
        lvi = KListViewItem(self.lvHistory, rel.release,
                                rel.date, rel.version,
                                unicode(rel.comment), rel.name,
                                rel.email, rel.type)
        if reverse:
            lvi.moveItem(self.lvHistory.lastItem())

    def slotAddHistory(self):
        dia = HistoryDialog(self, relValue = self.lvHistory.childCount() + 1)
        if dia.exec_loop() == QDialog.Accepted:
            res = dia.getResult()
            lvi = QListViewItem(self.lvHistory, res[0], res[1], res[2], res[4], res[5], res[6], res[3])
	    self.syncHistory()

    def slotRemoveHistory(self):
        lvi = self.lvHistory.selectedItem()
        if lvi:
            self.lvHistory.takeItem(lvi)
	    self.syncHistory()

    def slotBrowseHistory(self):
        lvi = self.lvHistory.selectedItem()
        if not lvi:
            return
        dia = HistoryDialog(self, [str(lvi.text(0)), str(lvi.text(1)), str(lvi.text(2)), str(lvi.text(6)), unicode(lvi.text(3)), unicode(lvi.text(4)), str(lvi.text(5))])
        if dia.exec_loop() == QDialog.Rejected:
            return
        res = dia.getResult()
        lvi.setText(0, res[0])
        lvi.setText(1, res[1])
        lvi.setText(2, res[2])
        lvi.setText(3, res[4])
        lvi.setText(4, res[5])
        lvi.setText(5, res[6])
        lvi.setText(6, res[3])

        self.syncHistory()

    def getHistoryList(self):
        ret = []
        iterator = QListViewItemIterator(self.lvHistory)
        while iterator.current():
            lvi = iterator.current()
            l = [str(lvi.text(0)), str(lvi.text(1)),str(lvi.text(2)), str(lvi.text(3)),str(lvi.text(4)), str(lvi.text(5)),str(lvi.text(6))]
            ret.append(l)
            iterator += 1
        return ret

    def setBuildDepList(self, l):
        self.lvHistory.clear()
        for his in l:
            KListViewItem(self.lvHistory, his[0], his[1],his[2], his[3],his[4], his[5],his[6])

    def syncHistory(self):
        #synchronize xml tree with listview
        import pakito.xmlUtil
        history = self.getHistoryList()

        while self.xmlUtil.deleteTagByPath("History", "Update"):
            pass

        history.reverse()

        for his in history:
            if his !=[]:
                if his[6]!="":
                    d={"release":his[0],"Type":his[6]}
                else:
                    d={"release":his[0]}
                historyNode = self.xmlUtil.getTagByPath("History","Update")
                if historyNode!=None:
                    self.xmlUtil.addTagAbove(historyNode, "Update","\n",**d)
                else:
                    historyNode = self.xmlUtil.getTagByPath("History")
                    self.xmlUtil.addTag(historyNode, "Update","\n",**d)
                node = self.xmlUtil.getTagByPath("History","Update")
            if  his[1] != "":
                self.xmlUtil.addTag(node, "Date", his[1])
            if  his[2] != "":
                self.xmlUtil.addTag(node, "Version", his[2])
            if  his[3] != "":
                self.xmlUtil.addTag(node, "Comment", his[3])
            if  his[4] != "":
                self.xmlUtil.addTag(node, "Name", his[4])
            if  his[5] != "":
                self.xmlUtil.addTag(node, "Email", his[5])

        self.xmlUtil.write()

    def fill(self, history):
        self.lvHistory.clear()
        for rel in history:
            self.addRelease(rel)