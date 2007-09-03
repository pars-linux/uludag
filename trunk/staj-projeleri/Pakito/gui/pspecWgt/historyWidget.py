# -*- coding: utf-8

from qt import *
from kdeui import *
from kdecore import *

from pisi import specfile as spec
from pisi.dependency import Dependency
from pisi.conflict import Conflict
from pisi.replace import Replace

from historyWidgetUI import HistoryWidgetUI

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

    def addRelease(self, rel, reverse=False):
        if not rel.type:
            rel.type = ""
        lvi = KListViewItem(self.lvHistory, rel.release,
                                rel.date, rel.version,
                                rel.comment, rel.name,
                                rel.email, rel.type)
        if reverse:
            lvi.moveItem(self.lvHistory.lastItem())

    def slotAddHistory(self):
        pass

    def slotRemoveHistory(self):
        pass

    def slotBrowseHistory(self):
        pass
        
    def fill(self, history):
        self.lvHistory.clear()
        for rel in history:
            self.addRelease(rel)
    
    def get(self, history):
        while len(history) != 0:
            history.pop()
            
        iterator = QListViewItemIterator(self.lvHistory)
        while iterator.current():
            lvi = iterator.current()
            update = spec.Update()
            if str(lvi.text(0)).strip() != "":
                update.release = str(lvi.text(0))
            if str(lvi.text(1)).strip() != "":
                update.date = str(lvi.text(1))
            if str(lvi.text(2)).strip() != "":
                update.version = str(lvi.text(2))     
            if str(lvi.text(3)).strip() != "":
                update.comment = str(lvi.text(3))
            if str(lvi.text(4)).strip() != "":
                update.name = unicode(lvi.text(4))
            if str(lvi.text(5)).strip() != "":
                update.email = str(lvi.text(5))        
            if str(lvi.text(6)).strip() != "":
                update.type = str(lvi.text(6))
            history.insert(0,update)
            iterator += 1
