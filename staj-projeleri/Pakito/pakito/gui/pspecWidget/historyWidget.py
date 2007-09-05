# -*- coding: utf-8

from qt import *
from kdeui import *
from kdecore import *

from pisi import specfile as spec
from pisi.dependency import Dependency
from pisi.conflict import Conflict
from pisi.replace import Replace

from pakito.gui.pspecWidget.historyWidgetUI import HistoryWidgetUI
from pakito.gui.pspecwidget.dialogs.historyDialog import HistoryDialog

class historyWidget(HistoryWidgetUI):
    def __init__(self, parent):
        HistoryWidgetUI.__init__(self, parent)
        il = KGlobal.iconLoader()

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

    def slotRemoveHistory(self):
        lvi = self.lvHistory.selectedItem()
        if lvi:
            self.lvHistory.takeItem(lvi) 

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

    def fill(self, history):
        self.lvHistory.clear()
        for rel in history:
            self.addRelease(rel)