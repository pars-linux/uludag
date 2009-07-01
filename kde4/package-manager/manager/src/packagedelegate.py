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
from rowanimator import RowAnimator

DEFAULT_ICON = ":/data/package.png"
ICON_PADDING = 0
ICON_SIZE = 24
DETAIL_LINE_OFFSET = 36
ROW_HEIGHT = 72

class PackageDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.rowAnimator = RowAnimator(parent.packageList.reset)
        self.defaultIcon = QtGui.QIcon(QtGui.QPixmap(DEFAULT_ICON))
        self.animatable = True

    def paint(self, painter, option, index):
        if not index.isValid():
            return

        opt = QtGui.QStyleOptionViewItemV4(option)
        opt.state &= ~QtGui.QStyle.State_Selected
        opt.widget.style().drawPrimitive(QtGui.QStyle.PE_PanelItemViewItem, opt, painter, None)

        if index.flags() & Qt.ItemIsUserCheckable and index.column() == 0:
            self.paintCheckBoxColumn(painter, option, index)
        else:
            self.paintInfoColumn(painter, option, index)

    def paintCheckBoxColumn(self, painter, option, index):
        opt = QtGui.QStyleOptionViewItemV4(option)

        buttonStyle = QtGui.QStyleOptionButton()
        buttonStyle.state = QtGui.QStyle.State_On if index.model().data(index, Qt.CheckStateRole) == QVariant(Qt.Checked) else QtGui.QStyle.State_Off

        if option.state & QtGui.QStyle.State_MouseOver:
            buttonStyle.state |= QtGui.QStyle.State_HasFocus

        buttonStyle.rect = opt.rect.adjusted(4, -opt.rect.height() + 64, 0, -2)
        opt.widget.style().drawControl(QtGui.QStyle.CE_CheckBox, buttonStyle, painter, None)

    def paintInfoColumn(self, painter, option, index):
        left = option.rect.left()
        top = option.rect.top()
        width = option.rect.width()

        pixmap = QtGui.QPixmap(option.rect.size())
        pixmap.fill(Qt.transparent)

        p = QtGui.QPainter(pixmap)
        p.translate(-option.rect.topLeft())

        textInner = 2 * ICON_PADDING + ROW_HEIGHT
        itemHeight = ROW_HEIGHT + 2 * ICON_PADDING

        margin = left + ICON_PADDING

        icon_path = index.model().data(index, Qt.DecorationRole).toString()
        if icon_path == DEFAULT_ICON:
            icon = self.defaultIcon
        else:
            icon = QtGui.QIcon(QtGui.QPixmap(icon_path).scaled(QSize(32, 32), Qt.KeepAspectRatio))
        icon.paint(p, margin, top + ICON_PADDING, ROW_HEIGHT, ROW_HEIGHT, Qt.AlignCenter)

        title = index.model().data(index, Qt.DisplayRole)
        summary = index.model().data(index, SummaryRole)
        description = index.model().data(index, DescriptionRole)

        foregroundColor = option.palette.color(QtGui.QPalette.Text)
        normalFont = QtGui.QFont(KGlobalSettings.generalFont().family(), 10, QtGui.QFont.Normal)
        boldFont = QtGui.QFont(KGlobalSettings.generalFont().family(), 10, QtGui.QFont.Bold)
        normalDetailFont = QtGui.QFont(KGlobalSettings.generalFont().family(), 9, QtGui.QFont.Normal)
        boldDetailFont = QtGui.QFont(KGlobalSettings.generalFont().family(), 9, QtGui.QFont.Bold)

        p.setPen(foregroundColor)

        # Package Name
        p.setFont(boldFont)
        p.drawText(left + textInner, top, width - textInner, itemHeight / 2, Qt.AlignBottom | Qt.AlignLeft, title.toString())

        # Package Summary
        p.setFont(normalFont)
        p.drawText(left + textInner, top + itemHeight / 2, width - textInner, itemHeight / 2, Qt.TextWordWrap, summary.toString())

        if self.rowAnimator.currentRow() == index.row():

            repository = index.model().data(index, RepositoryRole)
            version = index.model().data(index, VersionRole)

            # Package Detail Label
            position = top + ROW_HEIGHT + ICON_SIZE

            p.setFont(boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, i18n("Description:"))

            p.setFont(normalDetailFont)
            p.drawText(left + 2 * ROW_HEIGHT, position, width - textInner - ROW_HEIGHT, itemHeight / 2, Qt.TextWordWrap, description.toString())

            # Package Detail Version
            position += DETAIL_LINE_OFFSET

            p.setFont(boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, i18n("Release:"))

            p.setFont(normalDetailFont)
            p.drawText(left + 2 * ROW_HEIGHT, position, width - textInner - ROW_HEIGHT, itemHeight / 2, Qt.TextWordWrap, version.toString())

            # Package Detail Repository
            position += DETAIL_LINE_OFFSET

            p.setFont(boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, i18n("Repository:"))

            p.setFont(normalDetailFont)
            p.drawText(left + 2 * ROW_HEIGHT, position, width - textInner - ROW_HEIGHT, itemHeight / 2, Qt.TextWordWrap, repository.toString())

        p.end()
        painter.drawPixmap(option.rect.topLeft(), pixmap)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease and index.column() == 0:
            toggled = Qt.Checked if model.data(index, Qt.CheckStateRole) == QVariant(Qt.Unchecked) else Qt.Unchecked
            return model.setData(index, toggled, Qt.CheckStateRole)
        if event.type() == QEvent.MouseButtonRelease and index.column() == 1 and self.animatable:
            self.rowAnimator.animate(index.row())
        return QtGui.QItemDelegate(self).editorEvent(event, model, option, index)

    def sizeHint(self, option, index):
        if self.rowAnimator.currentRow() == index.row():
            return self.rowAnimator.size()
        else:
            width = ICON_SIZE if index.column() == 0 else 0
            return QSize(width, ROW_HEIGHT)

    def setAnimatable(self, animatable):
        self.animatable = animatable

    def reset(self):
        self.rowAnimator.reset()

