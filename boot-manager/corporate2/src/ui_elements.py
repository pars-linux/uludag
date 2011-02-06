# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *
from kdecore import *
from kdeui import *

import os.path

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
        self.currentEntry = None
        self.parent = parent

    def clear(self):
        for e in self.entries:
            e.hide()
        self.entries = []

    def add(self, editWidget, index, title, description, pardus, os_data):
        e = Entry(self, editWidget, index, title, description, pardus, os_data, self)
        self.entries.append(e)
        size = QSize(self.width(), self.height())
        self.resizeEvent(QResizeEvent(size , QSize(0, 0)))
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
        if th > self.height():
            self.resizeContents(width - 12, th)
        else:
            self.resizeContents(width, th)

class Entry(QWidget):
    def __init__(self, parent, editWidget, index, title, description, pardus, os_data, view):
        QWidget.__init__(self, parent.viewport())
        self.editWidget = editWidget

        self.parent = parent
        self.index = index
        self.title = title
        self.description = description
        self.pardus = pardus
        self.os_data = os_data
        self.view = view

        if self.pardus:
            os_type = "pardus"
        else:
            os_type = os_data["os_type"]

        if not os.path.exists(locate("data", "boot-manager/%s.png" % os_type)):
            os_type = "other"

        # Set icon for the entry
        self.icon = QImage(locate("data", "boot-manager/%s.png" % os_type))
        self.icon.smoothScale(32, 32)
        self.icon = QPixmap(self.icon)

        self.pushEdit = IconButton(self, "configure")
        QToolTip.add(self.pushEdit, i18n("Edit entry"))
        self.connect(self.pushEdit, SIGNAL("clicked()"), self.slotEdit)

        self.pushDelete = IconButton(self, "cancel")
        QToolTip.add(self.pushDelete, i18n("Delete entry"))
        self.connect(self.pushDelete, SIGNAL("clicked()"), self.slotDelete)

        self.checkbox = QCheckBox(self)
        self.checkbox.resize(16, 16)
        try:
            if os_data["default"] == "yes":
                self.checkbox.setChecked(True)
                self.parent.currentEntry = self
        except:
            pass
        self.connect(self.checkbox, SIGNAL("released()"), self.slotDefaultReleased)

        self.show()

    def setDefaultHandler(self, package, exception, args):
        if exception:
            self.parent.currentEntry.checkbox.setChecked(True)
            self.checkbox.setChecked(False)
            return
        self.parent.parent.checkSaved.setChecked(False)
        self.parent.currentEntry = self

    def slotDefaultReleased(self):
        old = self.parent.currentEntry
        if old == self:
            self.checkbox.setChecked(True)
            return
        if self.parent.currentEntry:
            self.parent.currentEntry.checkbox.setChecked(False)
        self.editWidget.parent.backend.setOption(self.editWidget.parent.package, "default", str(self.index), async = self.setDefaultHandler)

    def slotEdit(self):
        self.editWidget.editEntry(self.os_data)

    def slotDelete(self):
        if not len(self.view.entries) == 1:
            self.editWidget.deleteEntry(self.index, self.title)
        else:
            KMessageBox.error(self, i18n("This is the last entry, you cannot delete it!"))

    def paintEvent(self, event):
        paint = QPainter(self)
        col = KGlobalSettings.baseColor()
        paint.fillRect(event.rect(), QBrush(col))
        self.pushEdit.setPaletteBackgroundColor(col)
        self.pushDelete.setPaletteBackgroundColor(col)
        self.checkbox.setPaletteBackgroundColor(col)

        dip = (self.height() - self.icon.height()) / 2
        paint.drawPixmap(20, dip, self.icon)

        font = paint.font()
        font.setPointSize(font.pointSize() + 1)
        font.setBold(True)
        if "default" in self.os_data and self.os_data["default"] != "saved":
            font.setUnderline(True)
        fm = QFontMetrics(font)
        paint.drawText(20 + self.icon.width() + 6, fm.ascent() + 5, unicode(self.title))

        fark = fm.height()
        font.setPointSize(font.pointSize() - 2)
        font.setUnderline(False)
        fm = self.fontMetrics()
        paint.drawText(20 + self.icon.width() + 6, 5 + fark + 3 + fm.ascent(), unicode(self.description))

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        self.checkbox.setGeometry(4, 20, self.checkbox.width(), self.checkbox.height())
        self.pushEdit.setGeometry(w - self.pushEdit.myWidth - 6 - 6 - self.pushEdit.myWidth - 3, 6, self.pushEdit.myWidth, self.pushEdit.myHeight)
        self.pushDelete.setGeometry(w - self.pushDelete.myWidth - 6 - 6, 6, self.pushDelete.myWidth, self.pushDelete.myHeight)
        return QWidget.resizeEvent(self, event)

    def sizeHint(self):
        f = QFont(self.font())
        f.setPointSize(f.pointSize() + 1)
        f.setBold(True)
        fm = QFontMetrics(f)
        rect = fm.boundingRect(unicode(self.title))
        w = 6 + self.checkbox.width() + self.icon.width() + 6 + rect.width() + 30 + self.pushEdit.myWidth + 3 + self.pushDelete.myWidth + 6

        f.setPointSize(f.pointSize() - 2)
        fm2 = self.fontMetrics()
        rect2 = fm2.boundingRect(unicode(self.description))
        w2 = 6 + self.checkbox.width() + self.icon.width() + 6 + rect2.width() + 30 + self.pushEdit.myWidth + 3 + self.pushDelete.myWidth + 6

        w = max(w, w2)
        h = max(fm.height() + 3 + fm2.height(), 32) + 10
        return QSize(w, h)

class ComboList(QComboBox):
    def __init__(self, parent):
        QComboBox.__init__(self, parent)
        self.elements = {}

    def addItem(self, name, label):
        label = unicode(label)
        self.elements[name] = label
        self.insertItem(label)

    def getSelected(self):
        label = unicode(self.currentText())
        for name in self.elements:
            if label == unicode(self.elements[name]):
                return name

    def setSelected(self, name):
        label = self.elements[name]
        self.setCurrentText(label)
