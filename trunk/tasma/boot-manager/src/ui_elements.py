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
    def __init__(self, parent, label, icon_name):
        QPushButton.__init__(self, parent)
        self.setFlat(True)
        self.myset = getIconSet(icon_name, KIcon.MainToolbar)
        self.setIconSet(self.myset)
        size = self.myset.iconSize(QIconSet.Large)
        self.myWidth = size.width() + 4
        self.myHeight = size.height() + 4
        self.resize(self.myWidth, self.myHeight)

class IconBox(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.layout = QHBoxLayout(self, 0, 6, "layout")
    
    def addWidget(self, item):
        if isinstance(item, QWidget):
            self.layout.addWidget(item)
        else:
            self.layout.addItem(item)

class Entry(QListBoxItem):
    def __init__(self, parent, title, description="", os_type="Unknown", pardus=False, checked=False, index=None):
        QListBoxItem.__init__(self, parent)
        self.parent = parent
        
        self.title = title
        self.description = description
        self.checked = checked
        self.os_type = os_type
        self.pardus = pardus
        self.entry_index = index
        
        self.setCustomHighlighting(True)
        self.setOs(os_type)
        
        self.fontTitle = QFont()
        self.fontTitle.setBold(True)
        self.fontTitle.setPointSize(self.fontTitle.pointSize() + 1)
        self.fontDesc = QFont()
        
        self.padding = 6
    
    def setOs(self, os_type):
        self.os_type = os_type
        if self.pardus:
            self.icon = QPixmap(locate("data", "boot-manager/pardus.png"))
        elif self.os_type == "linux":
            self.icon = QPixmap(locate("data", "boot-manager/linux.png"))
        elif self.os_type == "windows":
            self.icon = QPixmap(locate("data", "boot-manager/windows.png"))
        else:
            self.icon = QPixmap(locate("data", "boot-manager/other.png"))
    
    def paint(self, painter):
        color = KGlobalSettings.baseColor()
        if self.isSelected():
            color = KGlobalSettings.highlightColor()
        elif self.entry_index % 2:
            color = KGlobalSettings.alternateBackgroundColor()
        painter.fillRect(0, 0, 32000, 44, QBrush(color, Qt.SolidPattern))
        
        fm = QFontMetrics(self.fontTitle)
        fm2 = QFontMetrics(self.fontDesc)
        
        if not self.parent.isEnabled():
            painter.setPen(KGlobalSettings.inactiveTextColor())
        elif self.checked:
            painter.setPen(QColor(255, 0, 0))
        elif self.isSelected():
            painter.setPen(KGlobalSettings.activeTextColor())
        else:
            painter.setPen(KGlobalSettings.textColor())
        painter.setFont(self.fontTitle)
        painter.drawText(2 * self.padding + self.icon.width(), self.padding + fm.ascent(), self.title)
        
        if not self.parent.isEnabled():
            painter.setPen(KGlobalSettings.inactiveTextColor())
        elif self.isSelected():
            painter.setPen(KGlobalSettings.activeTextColor())
        else:
            painter.setPen(QColor(100, 100, 100))
        painter.setFont(self.fontDesc)
        painter.drawText(2 * self.padding + self.icon.width(), self.padding + fm.height() + 4 + fm2.ascent(), self.description)
        
        painter.drawPixmap(self.padding, self.padding, self.icon)
    
    def height(self, box):
        return self.icon.height() + 2 * self.padding
