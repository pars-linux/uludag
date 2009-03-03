#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from packagelistmodel import *

UNIVERSAL_PADDING = 6
MAIN_ICON_SIZE = 48

class PackageListDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        if not index.isValid():
            return

        opt = QtGui.QStyleOptionViewItemV4(option)
        if opt.widget:
            style = opt.widget.style()
        else:
            style = QApplication.style()

        style.drawPrimitive(QtGui.QStyle.PE_PanelItemViewItem, opt, painter, opt.widget)
        self.paintColMain(painter, option, index)

    def paintColMain(self, painter, option, index):
        left = option.rect.left()
        top = option.rect.top()
        width = option.rect.width()

        leftToRight = (painter.layoutDirection() == Qt.LeftToRight)

        pixmap = QtGui.QPixmap(option.rect.size())
        pixmap.fill(Qt.transparent)

        p = QtGui.QPainter(pixmap)
        p.translate(-option.rect.topLeft())

        textInner = 2 * UNIVERSAL_PADDING + MAIN_ICON_SIZE
        itemHeight = MAIN_ICON_SIZE + 2 * UNIVERSAL_PADDING

        title = index.model().data(index, Qt.DisplayRole)
        description = index.model().data(index, SummaryRole)

        p.drawText(left + textInner, top, width - textInner, itemHeight / 2, Qt.AlignBottom | Qt.AlignLeft, title)
        p.drawText(left + textInner, top + itemHeight / 2, width - textInner, itemHeight / 2, Qt.AlignTop | Qt.AlignLeft, description)

        if leftToRight:
            margin = left + UNIVERSAL_PADDING
        else:
            margin = left + width - UNIVERSAL_PADDING - MAIN_ICON_SIZE

        icon = index.model().data(index, Qt.DecorationRole)
        icon.paint(p, margin, top + UNIVERSAL_PADDING, MAIN_ICON_SIZE, MAIN_ICON_SIZE, Qt.AlignCenter)

        p.end()

        painter.drawPixmap(option.rect.topLeft(), pixmap)

    def editorEvent(self, event, model, option, index):
        return QtGui.QItemDelegate(self).editorEvent(event, model, option, index)

    def sizeHint(self, option, index):
        return QSize(0, MAIN_ICON_SIZE + 2 * UNIVERSAL_PADDING)

    def columnWidth(self, column, viewWidth):
        return viewWidth - 2 * columnWidth(1, viewWidth)
