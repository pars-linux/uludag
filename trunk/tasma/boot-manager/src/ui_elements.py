# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *
from kdecore import *
from kdeui import *

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

class IconButton(QPushButton):
    def __init__(self, parent, icon_name):
        QPushButton.__init__(self, parent)
        self.setFlat(True)
        self.myset = getIconSet(icon_name, KIcon.Small)
        self.setIconSet(self.myset)
        size = self.myset.iconSize(QIconSet.Small)
        self.myWidth = size.width() + 4
        self.myHeight = size.height() + 4
        self.resize(self.myWidth, self.myHeight)

class EntryView(QScrollView):
    def __init__(self, parent):
        QScrollView.__init__(self, parent)
        self.viewport().setPaletteBackgroundColor(KGlobalSettings.baseColor())
        self.entries = []
    
    def clear(self):
        for e in self.entries:
            e.hide()
        self.entries = []
    
    def add(self, editWidget, index, title, description, default, pardus, os_data):
        e = Entry(self.viewport(), editWidget, index, title, description, default, pardus, os_data)
        self.entries.append(e)
        self.myResize(self.contentsWidth())
        return e
    
    def resizeEvent(self, event):
        QScrollView.resizeEvent(self, event)
        self.myResize(self.visibleWidth())
    
    def myResize(self, width):
        mw = 0
        th = 0
        for e in self.entries:
            h = e.sizeHint().height()
            mw = max(mw, e.sizeHint().width())
            e.setGeometry(0, th, width, h)
            th += h
        self.setMinimumSize(QSize(mw, 0))
        self.resizeContents(width, th)

class Entry(QWidget):
    def __init__(self, parent, editWidget, index, title, description, default, pardus, os_data):
        QWidget.__init__(self, parent)
        self.editWidget = editWidget
        
        self.index = index
        self.title = title
        self.description = description
        self.default = default
        self.pardus = pardus
        self.os_data = os_data
        
        if self.pardus:
            os_type = "pardus"
        else:
            os_type = os_data["os_type"]
        
        self.icon = QImage(locate("data", "boot-manager/%s.png" % os_type))
        self.icon.smoothScale(32, 32)
        self.icon = QPixmap(self.icon)
        
        self.pushEdit = IconButton(self, "configure")
        QToolTip.add(self.pushEdit, i18n("Edit entry"))
        self.connect(self.pushEdit, SIGNAL("clicked()"), self.slotEdit)
        
        self.pushDelete = IconButton(self, "cancel")
        QToolTip.add(self.pushDelete, i18n("Delete entry"))
        self.connect(self.pushDelete, SIGNAL("clicked()"), self.slotDelete)
        
        self.show()
    
    def slotEdit(self):
        self.editWidget.editEntry(self.os_data)
    
    def slotDelete(self):
        self.editWidget.deleteEntry(self.index)
    
    def paintEvent(self, event):
        paint = QPainter(self)
        col = KGlobalSettings.baseColor()
        paint.fillRect(event.rect(), QBrush(col))
        self.pushEdit.setPaletteBackgroundColor(col)
        self.pushDelete.setPaletteBackgroundColor(col)
        
        dip = (self.height() - self.icon.height()) / 2
        paint.drawPixmap(6, dip, self.icon)
        
        font = paint.font()
        font.setPointSize(font.pointSize() + 1)
        font.setBold(True)
        fm = QFontMetrics(font)
        paint.drawText(6 + self.icon.width() + 6, fm.ascent() + 5, unicode(self.title))
        
        fark = fm.height()
        font.setPointSize(font.pointSize() - 2)
        fm = self.fontMetrics()
        paint.drawText(6 + self.icon.width() + 6, 5 + fark + 3 + fm.ascent(), unicode(self.description))
        
    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        self.pushEdit.setGeometry(w - self.pushEdit.myWidth - 6 - 6 - self.pushEdit.myWidth - 3, 6, self.pushEdit.myWidth, self.pushEdit.myHeight)
        self.pushDelete.setGeometry(w - self.pushDelete.myWidth - 6 - 6, 6, self.pushDelete.myWidth, self.pushDelete.myHeight)
        return QWidget.resizeEvent(self, event)
    
    def sizeHint(self):
        f = QFont(self.font())
        f.setPointSize(f.pointSize() + 1)
        f.setBold(True)
        fm = QFontMetrics(f)
        rect = fm.boundingRect(unicode(self.title))
        w = 6 + self.icon.width() + 6 + rect.width() + 30 + self.pushEdit.myWidth + 3 + self.pushDelete.myWidth + 6
        
        f.setPointSize(f.pointSize() - 2)
        fm2 = self.fontMetrics()
        rect2 = fm2.boundingRect(unicode(self.description))
        w2 = 6 + self.icon.width() + 6 + rect2.width() + 30 + self.pushEdit.myWidth + 3 + self.pushDelete.myWidth + 6
        
        w = max(w, w2)
        h = max(fm.height() + 3 + fm2.height(), 32) + 10
        return QSize(w, h)
