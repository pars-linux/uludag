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
GRAY = QtGui.QColor('gray')
BLUE = QtGui.QColor('blue')

RECT = QRect()

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

        self.types = {'critical':(RED,     i18n('critical')),
                      'security':(DARKRED, i18n('security'))}

        self.font = Pds.settings('font','Sans').split(',')[0]

        self.normalFont = QtGui.QFont(self.font, 10, QtGui.QFont.Normal)
        self.boldFont = QtGui.QFont(self.font, 11, QtGui.QFont.Bold)
        self.normalDetailFont = QtGui.QFont(self.font, 9, QtGui.QFont.Normal)
        self.boldDetailFont = QtGui.QFont(self.font, 9, QtGui.QFont.Bold)
        self.tagFont = QtGui.QFont(self.font, 7, QtGui.QFont.Normal)

        self.tagFontFM = QtGui.QFontMetrics(self.tagFont)
        self.boldFontFM = QtGui.QFontMetrics(self.boldFont)
        self.boldDetailFontFM = QtGui.QFontMetrics(self.boldDetailFont)
        self.normalFontFM = QtGui.QFontMetrics(self.normalFont)
        self.normalDetailFontFM = QtGui.QFontMetrics(self.normalDetailFont)

        self._titles = {'description': i18n("Description:"),
                        'website'    : i18n("Website:"),
                        'release'    : i18n("Release:"),
                        'repository' : i18n("Repository:"),
                        'size'       : i18n("Package Size:"),
                        'installVers': i18n("Installed Version:")}

        self._titleFM = {}
        for key, value in self._titles.items():
            self._titleFM[key] = self.boldDetailFontFM.width(value) + ICON_SIZE + 3

        self.baseWidth = self.boldFontFM.width(max(self._titles.values(), key=len)) + ICON_SIZE
        self.parent = parent.packageList

    def paint(self, painter, option, index):
        if not index.isValid():
            return
        if index.flags() & Qt.ItemIsUserCheckable:
            if index.column() == 0:
                self.paintCheckBoxColumn(painter, option, index)
            else:
                self.paintInfoColumn(painter, option, index)
        else:
            self.paintInfoColumn(painter, option, index, width_limit = 10)

    def paintCheckBoxColumn(self, painter, option, index):
        opt = QtGui.QStyleOptionViewItemV4(option)

        buttonStyle = QtGui.QStyleOptionButton()
        buttonStyle.state = QtGui.QStyle.State_On if index.model().data(index, Qt.CheckStateRole) == QVariant(Qt.Checked) else QtGui.QStyle.State_Off

        if option.state & QtGui.QStyle.State_MouseOver:
            buttonStyle.state |= QtGui.QStyle.State_HasFocus

        buttonStyle.rect = opt.rect.adjusted(4, -opt.rect.height() + ROW_HEIGHT, 0, 0)
        PackageDelegate.AppStyle().drawControl(QtGui.QStyle.CE_CheckBox, buttonStyle, painter, None)

    def paintInfoColumn(self, painter, option, index, width_limit = 0):
        left = option.rect.left() + 3
        top = option.rect.top()
        width = option.rect.width() - width_limit

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
        ptype = str(index.model().data(index, TypeRole).toString())

        icon = index.model().data(index, Qt.DecorationRole).toString()
        if icon:
            pix = KIconLoader.load(icon, forceCache = True)
            if not pix.isNull():
                icon = QtGui.QIcon(pix.scaled(QSize(32, 32), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                icon = self.defaultIcon
        else:
            icon = self.defaultIcon

        icon.paint(p, margin, top + ICON_PADDING, ROW_HEIGHT, ROW_HEIGHT, Qt.AlignCenter)

        foregroundColor = option.palette.color(QtGui.QPalette.Text)
        p.setPen(foregroundColor)

        # Package Name
        p.setFont(self.boldFont)
        p.drawText(left + textInner, top, width - textInner, itemHeight / 2, Qt.AlignBottom | Qt.AlignLeft, title)

        tagWidth = 0

        if self.parent.showComponents:
            component = str(index.model().data(index, ComponentRole).toString())
            widthOfTitle = self.boldFontFM.width(title) + 6 + left + textInner

            p.setFont(self.tagFont)
            rect = self.tagFontFM.boundingRect(option.rect, Qt.TextWordWrap, component)
            p.setPen(GRAY)
            p.setBrush(GRAY)
            p.drawRoundRect(widthOfTitle , top + 12, rect.width() + 4, rect.height(), 10, 10)
            p.setPen(WHITE)
            p.drawText(widthOfTitle + 2, top + 12, rect.width(), rect.height(), Qt.AlignCenter, component)
            p.setPen(foregroundColor)

        if ptype not in ('None', 'normal'):
            p.setFont(self.tagFont)
            rect = self.tagFontFM.boundingRect(option.rect, Qt.TextWordWrap, ptype)
            p.setPen(self.types[ptype][0])
            p.setBrush(self.types[ptype][0])
            p.drawRoundRect(width - rect.width() - 1, top + (itemHeight / 2) - (rect.height() / 2), rect.width() + 4, rect.height(), 10, 10)
            p.setPen(WHITE)
            p.drawText(width - rect.width() + 1, top + (itemHeight / 2) - (rect.height() / 2), rect.width(), rect.height(), Qt.AlignCenter, self.types[ptype][1])
            p.setPen(foregroundColor)
            tagWidth = rect.width()

        # Package Summary
        p.setFont(self.normalFont)
        foregroundColor.setAlpha(160)
        p.setPen(foregroundColor)
        elided_summary = self.normalFontFM.elidedText(summary, Qt.ElideRight, width - textInner - tagWidth - 22)
        p.drawText(left + textInner, top + itemHeight / 2, width - textInner, itemHeight / 2, Qt.TextDontClip, elided_summary)
        foregroundColor.setAlpha(255)
        p.setPen(foregroundColor)

        if self.rowAnimator.currentRow() == index.row():
            description = index.model().data(index, DescriptionRole).toString()
            size = index.model().data(index, SizeRole).toString()
            homepage = index.model().data(index, HomepageRole).toString()
            installedVersion = str(index.model().data(index, InstalledVersionRole).toString())
            version = index.model().data(index, VersionRole)

            # Package Detail Label
            position = top + ROW_HEIGHT

            p.setFont(self.normalDetailFont)
            baseRect = QRect(left, position, width - 8, option.rect.height())
            rect = self.normalDetailFontFM.boundingRect(baseRect, Qt.TextWordWrap | Qt.TextDontClip, description)
            p.drawText(left + 2, position, width - 8, rect.height(), Qt.TextWordWrap | Qt.TextDontClip, description)

            # Package Detail Homepage
            position += rect.height() + 4

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['website'])

            p.setFont(self.normalDetailFont)
            homepage = self.normalDetailFontFM.elidedText(homepage, Qt.ElideRight, width - self._titleFM['website'])
            rect = self.normalDetailFontFM.boundingRect(option.rect, Qt.TextSingleLine, homepage)
            self.rowAnimator.hoverLinkFilter.link_rect = QRect(left + self._titleFM['website'] + 2, position + 2 + 32, rect.width(), rect.height())

            p.setPen(option.palette.color(QtGui.QPalette.Link))
            p.drawText(left + self._titleFM['website'], position, width, rect.height(), Qt.TextSingleLine, homepage)
            p.setPen(foregroundColor)

            # Package Detail Version
            position += rect.height()

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['release'])

            p.setFont(self.normalDetailFont)
            rect = self.normalDetailFontFM.boundingRect(option.rect, Qt.TextWordWrap, version.toString())
            p.drawText(left + self._titleFM['release'], position, width, rect.height(), Qt.TextWordWrap, version.toString())

            if not installedVersion == '':
                position += rect.height()

                p.setFont(self.boldDetailFont)
                p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['installVers'])

                p.setFont(self.normalDetailFont)
                rect = self.normalDetailFontFM.boundingRect(option.rect, Qt.TextWordWrap, installedVersion)
                p.drawText(left + self._titleFM['installVers'], position, width, rect.height(), Qt.TextWordWrap, installedVersion)

            # Package Detail Repository
            repository = index.model().data(index, RepositoryRole).toString()
            if not repository == '':
                position += rect.height()

                p.setFont(self.boldDetailFont)
                p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['repository'])

                p.setFont(self.normalDetailFont)
                p.drawText(left + self._titleFM['repository'], position, width, itemHeight / 2, Qt.TextWordWrap, repository)

            # Package Detail Size
            position += rect.height()

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['size'])

            p.setFont(self.normalDetailFont)
            p.drawText(left + self._titleFM['size'], position, width, itemHeight / 2, Qt.TextWordWrap, size)
            position += rect.height()
            self.rowAnimator.max_height = position - top + 8

        p.end()
        painter.drawPixmap(option.rect.topLeft(), pixmap)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease and index.column() == 0:
            toggled = Qt.Checked if model.data(index, Qt.CheckStateRole) == QVariant(Qt.Unchecked) else Qt.Unchecked
            return model.setData(index, toggled, Qt.CheckStateRole)
        __event = QtGui.QItemDelegate(self).editorEvent(event, model, option, index)
        if event.type() == QEvent.MouseButtonRelease and index.column() == 1 and self.animatable:
            if self.rowAnimator.row == index.row():
                if self.rowAnimator.hoverLinkFilter.link_rect.contains(event.pos()):
                    url = QUrl(model.data(index, HomepageRole).toString())
                    QtGui.QDesktopServices.openUrl(url)
                    return __event
            self.rowAnimator.animate(index.row())
        return __event

    def sizeHint(self, option, index):
        if self.rowAnimator.currentRow() == index.row() and not index.row() == 0:
            return self.rowAnimator.size()
        else:
            width = ICON_SIZE if index.column() == 0 else 0
            return QSize(width, ROW_HEIGHT)

    def setAnimatable(self, animatable):
        self.animatable = animatable

    def reset(self):
        self.rowAnimator.reset()
