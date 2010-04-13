#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
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

from packagemodel import *
from rowanimator import RowAnimator

from context import *

DEFAULT_ICON = ('applications-other', 'package')
DARKRED = QtGui.QColor('darkred')
WHITE = QtGui.QColor('white')
RED = QtGui.QColor('red')
TYPE_COLORS = {'critical':RED, 'security':DARKRED}

DETAIL_LINE_OFFSET = 36
ICON_PADDING = 0
ROW_HEIGHT = 52
ICON_SIZE = 2

class PackageDelegate(QtGui.QItemDelegate):

    AppStyle = QtGui.qApp.style

    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.rowAnimator = RowAnimator(parent.packageList)
        self.defaultIcon = KIcon(DEFAULT_ICON, 32)
        self.animatable = True

        self._max_height = ROW_HEIGHT
        self.font = Pds.settings('font','Sans').split(',')[0]

        self.normalFont = QtGui.QFont(self.font, 10, QtGui.QFont.Normal)
        self.boldFont = QtGui.QFont(self.font, 10, QtGui.QFont.Bold)
        self.normalDetailFont = QtGui.QFont(self.font, 9, QtGui.QFont.Normal)
        self.boldDetailFont = QtGui.QFont(self.font, 9, QtGui.QFont.Bold)
        self.tagFont = QtGui.QFont(self.font, 7, QtGui.QFont.Normal)
        self.tagFontFM = QtGui.QFontMetrics(self.tagFont)

        fontMetric = QtGui.QFontMetrics(self.boldFont)

        self._titles = {'description': i18n("Description:"),
                        'website'    : i18n("Website:"),
                        'release'    : i18n("Release:"),
                        'repository' : i18n("Repository:"),
                        'size'       : i18n("Package Size:")}

        self.baseWidth = fontMetric.width(max(self._titles.values(), key=len)) + ICON_SIZE

    def paint(self, painter, option, index):
        if not index.isValid():
            return
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

        buttonStyle.rect = opt.rect.adjusted(4, -opt.rect.height() + 54, 0, -2)
        PackageDelegate.AppStyle().drawControl(QtGui.QStyle.CE_CheckBox, buttonStyle, painter, None)

    def paintInfoColumn(self, painter, option, index):
        left = option.rect.left()
        top = option.rect.top()
        width = option.rect.width()

        pixmap = QtGui.QPixmap(option.rect.size())
        pixmap.fill(Qt.transparent)

        p = QtGui.QPainter(pixmap)
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)
        p.translate(-option.rect.topLeft())

        textInner = 2 * ICON_PADDING + ROW_HEIGHT - 10
        itemHeight = ROW_HEIGHT + 2 * ICON_PADDING

        margin = left + ICON_PADDING - 10

        title = index.model().data(index, Qt.DisplayRole).toString()
        summary = index.model().data(index, SummaryRole).toString()
        description = index.model().data(index, DescriptionRole)
        size = index.model().data(index, SizeRole)
        homepage = index.model().data(index, HomepageRole)
        ptype = str(index.model().data(index, TypeRole).toString())

        icon = index.model().data(index, Qt.DecorationRole).toString()
        if icon:
            icon = QtGui.QIcon(KIconLoader.load(icon, forceCache = True).scaled(QSize(32, 32), Qt.KeepAspectRatio))
        else:
            icon = self.defaultIcon

        icon.paint(p, margin, top + ICON_PADDING, ROW_HEIGHT, ROW_HEIGHT, Qt.AlignCenter)

        foregroundColor = option.palette.color(QtGui.QPalette.Text)
        p.setPen(foregroundColor)

        # Package Name
        p.setFont(self.boldFont)
        p.drawText(left + textInner, top, width - textInner, itemHeight / 2, Qt.AlignBottom | Qt.AlignLeft, title)
        if ptype not in ('None', 'normal'):
            p.setFont(self.tagFont)
            rect = self.tagFontFM.boundingRect(option.rect, Qt.TextWordWrap, ptype)
            p.setPen(TYPE_COLORS[ptype])
            p.setBrush(TYPE_COLORS[ptype])
            p.drawRoundRect(width - rect.width() - 1, top + (itemHeight / 2) - (rect.height() / 2), rect.width() + 4, rect.height(), 10, 10)
            p.setPen(WHITE)
            p.drawText(width - rect.width() + 1, top + (itemHeight / 2) - (rect.height() / 2), rect.width(), rect.height(), Qt.AlignCenter, ptype)
            p.setPen(foregroundColor)

        # Package Summary
        p.setFont(self.normalFont)
        elided_summary = QtGui.QFontMetrics(self.normalFont).elidedText(summary, Qt.ElideRight, width - textInner)
        p.drawText(left + textInner, top + itemHeight / 2, width - textInner, itemHeight / 2, Qt.TextDontClip, elided_summary)

        if self.rowAnimator.currentRow() == index.row():
            _left = left + self.baseWidth
            _width = width - _left - 2
            repository = index.model().data(index, RepositoryRole)
            version = index.model().data(index, VersionRole)

            # Package Detail Label
            position = top + ROW_HEIGHT

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['description'])

            p.setFont(self.normalDetailFont)

            fontMetrics = QtGui.QFontMetrics(self.normalDetailFont)
            rect = fontMetrics.boundingRect(option.rect, Qt.TextWordWrap, description.toString())
            p.drawText(_left, position, _width, rect.height(), Qt.TextWordWrap, description.toString())

            # Package Detail Homepage
            position += rect.height()

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['website'])

            p.setFont(self.normalDetailFont)
            rect = fontMetrics.boundingRect(option.rect, Qt.TextWordWrap, homepage.toString())
            p.drawText(_left, position, _width, rect.height(), Qt.TextWordWrap, homepage.toString())

            # Package Detail Version
            position += rect.height()

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['release'])

            p.setFont(self.normalDetailFont)
            rect = fontMetrics.boundingRect(option.rect, Qt.TextWordWrap, version.toString())
            p.drawText(_left, position, _width, rect.height(), Qt.TextWordWrap, version.toString())

            # Package Detail Repository
            position += rect.height()

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['repository'])

            p.setFont(self.normalDetailFont)
            p.drawText(_left, position, _width, itemHeight / 2, Qt.TextWordWrap, repository.toString())

            # Package Detail Size
            position += rect.height()

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['size'])

            p.setFont(self.normalDetailFont)
            p.drawText(_left, position, _width, itemHeight / 2, Qt.TextWordWrap, size.toString())

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

