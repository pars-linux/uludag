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

class Entry(QListBoxItem):
    def __init__(self, parent, title, description="", os_type="Unknown", checked=False, index=None):
        QListBoxItem.__init__(self, parent)
        self.title = title
        self.description = description
        self.checked = checked
        self.os_type = os_type
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
        if self.os_type == "Pardus":
            self.icon = QPixmap("pardus.png")
        elif self.os_type == "Linux":
            self.icon = QPixmap("/usr/share/icons/Tulliana-2.0/32x32/apps/penguin.png")
        elif self.os_type == "Windows":
            self.icon = QPixmap("/usr/share/icons/Tulliana-2.0/32x32/apps/wabi.png")
        else:
            self.icon = QPixmap("/usr/share/icons/Tulliana-2.0/32x32/apps/akregator_empty.png")
    
    def paint(self, painter):
        color = KGlobalSettings.baseColor()
        if self.isSelected():
            color = KGlobalSettings.highlightColor()
        elif self.entry_index % 2:
            color = KGlobalSettings.alternateBackgroundColor()
        painter.fillRect(0, 0, 32000, 44, QBrush(color, Qt.SolidPattern))
        
        fm = QFontMetrics(self.fontTitle)
        fm2 = QFontMetrics(self.fontDesc)
        
        if self.isSelected():
            painter.setPen(KGlobalSettings.activeTextColor())
        else:
            painter.setPen(KGlobalSettings.textColor())
        painter.setFont(self.fontTitle)
        painter.drawText(2 * self.padding + self.icon.width(), self.padding + fm.ascent(), self.title)
        
        if self.isSelected():
            painter.setPen(KGlobalSettings.activeTextColor())
        else:
            painter.setPen(QColor(100, 100, 100))
        painter.setFont(self.fontDesc)
        painter.drawText(2 * self.padding + self.icon.width(), self.padding + fm.height() + 4 + fm2.ascent(), self.description)
        
        painter.drawPixmap(self.padding, self.padding, self.icon)
    
    def height(self, box):
        return self.icon.height() + 2 * self.padding
