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

from packagemodel import *

UNIVERSAL_PADDING = 6
FAV_ICON_SIZE = 24
DETAIL_LINE_OFFSET = 36
MAIN_ICON_SIZE = 48
DEFAULT_HEIGHT = MAIN_ICON_SIZE + 2 * UNIVERSAL_PADDING
MAX_HEIGHT = DEFAULT_HEIGHT * 4

(UP, DOWN) = range(2)

class PackageDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.parent = parent
        self.timeLine = QTimeLine(250)
        self.timeLine.setUpdateInterval(40)
        self.animatedHeight = DEFAULT_HEIGHT
        self.animationDirection = DOWN
        self.animatingRow = None
        QObject.connect(self.timeLine, SIGNAL("valueChanged(qreal)"), parent.ui.packageList.reset)
        QObject.connect(self.timeLine, SIGNAL("finished()"), self.animationFinished)

    def animationFinished(self):
        if self.animationDirection == DOWN:
            self.animationDirection = UP
            self.animatedHeight = MAX_HEIGHT
        else:
            self.animationDirection = DOWN
            self.animatedHeight = DEFAULT_HEIGHT

    def paint(self, painter, option, index):
        if not index.isValid():
            return

        opt = QtGui.QStyleOptionViewItemV4(option)
        if opt.widget:
            style = opt.widget.style()
        else:
            style = QtGui.QApplication.style()

#        style.drawPrimitive(QtGui.QStyle.PE_PanelItemViewItem, opt, painter, opt.widget)

        if index.column() == 1:
            self.paintColMain(painter, option, index)
        elif index.column() == 0:
            self.paintColCheckBox(painter, option, index)
        else:
            print "Unexpected column"

    def paintColCheckBox(self, painter, option, index):
        opt = QtGui.QStyleOptionViewItemV4(option)

        buttonStyle = QtGui.QStyleOptionButton()
        buttonStyle.state = QtGui.QStyle.State_On if index.model().data(index, Qt.CheckStateRole) == QVariant(Qt.Checked) else QtGui.QStyle.State_Off

        buttonStyle.rect = opt.rect.adjusted(4, -opt.rect.height() + 64, 0, -2)
        opt.widget.style().drawControl(QtGui.QStyle.CE_CheckBox, buttonStyle, painter, None)

    def paintColMain(self, painter, option, index):
        left = option.rect.left()
        top = option.rect.top()
        width = option.rect.width()

        pixmap = QtGui.QPixmap(option.rect.size())
        pixmap.fill(Qt.transparent)

        p = QtGui.QPainter(pixmap)
        p.translate(-option.rect.topLeft())

        textInner = 2 * UNIVERSAL_PADDING + MAIN_ICON_SIZE
        itemHeight = MAIN_ICON_SIZE + 2 * UNIVERSAL_PADDING

        margin = left + UNIVERSAL_PADDING

        icon_path = index.model().data(index, Qt.DecorationRole)
        icon = QtGui.QIcon(QtGui.QPixmap(icon_path.toString()))
        icon.paint(p, margin, top + UNIVERSAL_PADDING, MAIN_ICON_SIZE, MAIN_ICON_SIZE, Qt.AlignCenter)

        title = index.model().data(index, Qt.DisplayRole)
        summary = index.model().data(index, SummaryRole)
        description = index.model().data(index, DescriptionRole)
        version = index.model().data(index, VersionRole)

        normalFont = QtGui.QFont(KGlobalSettings.generalFont().family(), 10, QtGui.QFont.Normal)
        boldFont = QtGui.QFont(KGlobalSettings.generalFont().family(), 10, QtGui.QFont.Bold)

        # Package Name
        p.setFont(boldFont)
        p.drawText(left + textInner, top, width - textInner, itemHeight / 2, Qt.AlignBottom | Qt.AlignLeft, title.toString())

        # Package Summary
        p.setFont(normalFont)
        p.drawText(left + textInner, top + itemHeight / 2, width - textInner, itemHeight / 2, Qt.TextWordWrap, summary.toString())

        if self.animatingRow == index.row():
            normalDetailFont = QtGui.QFont(KGlobalSettings.generalFont().family(), 9, QtGui.QFont.Normal)
            boldDetailFont = QtGui.QFont(KGlobalSettings.generalFont().family(), 9, QtGui.QFont.Bold)

            # Package Detail Label
            position = top + MAIN_ICON_SIZE + FAV_ICON_SIZE

            p.setFont(boldDetailFont)
            p.drawText(left + FAV_ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, unicode("Açıklama:"))

            p.setFont(normalDetailFont)
            p.drawText(left + 2 * MAIN_ICON_SIZE, position, width - textInner - MAIN_ICON_SIZE, itemHeight / 2, Qt.TextWordWrap, description.toString())

            # Package Detail Version
            position += DETAIL_LINE_OFFSET

            p.setFont(boldDetailFont)
            p.drawText(left + FAV_ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, unicode("Sürüm:"))

            p.setFont(normalDetailFont)
            p.drawText(left + 2 * MAIN_ICON_SIZE, position, width - textInner - MAIN_ICON_SIZE, itemHeight / 2, Qt.TextWordWrap, version.toString())

        p.end()
        painter.drawPixmap(option.rect.topLeft(), pixmap)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease and index.column() == 0:
            toggled = Qt.Checked if model.data(index, Qt.CheckStateRole) == QVariant(Qt.Unchecked) else Qt.Unchecked
            return model.setData(index, toggled, Qt.CheckStateRole)
        if event.type() == QEvent.MouseButtonRelease and index.column() == 1:
            if self.animatingRow != index.row():
                self.resetRowAnimation(index.row())
            self.timeLine.start()
        return QtGui.QItemDelegate(self).editorEvent(event, model, option, index)

    def resetRowAnimation(self, row):
        self.timeLine.stop()
        self.timeLine.setCurrentTime(0)
        self.animatingRow = row
        self.animatedHeight = DEFAULT_HEIGHT
        self.animationDirection = DOWN

    def sizeHint(self, option, index):
        if index.column() == 1:
            width = 0
        else:
            width = FAV_ICON_SIZE

        if index.row() == self.animatingRow and self.timeLine.state() == QTimeLine.Running:
            if self.animationDirection == DOWN:
                self.animatedHeight += 25
                if self.animatedHeight > MAX_HEIGHT:
                    self.animatedHeight = MAX_HEIGHT
            else:
                self.animatedHeight -= 25
                if self.animatedHeight < DEFAULT_HEIGHT:
                    self.animatedHeight = DEFAULT_HEIGHT

        if index.row() == self.animatingRow:
            return QSize(width, self.animatedHeight)

        return QSize(width, MAIN_ICON_SIZE + 2 * UNIVERSAL_PADDING)
