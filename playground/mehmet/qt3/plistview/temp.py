#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import os
import locale

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner
from kdecore import *
from kdeui import *
import kdedesigner

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)


class PListView(QScrollView):
    itemHeight = 20
    iconHeight = 16
    arrowSize = 8
    def __init__(self, parent):
        QScrollView.__init__(self, parent)
        self.viewport().setPaletteBackgroundColor(QColor(255,255,255))
        self.parent = parent
        self.items = []
        self.selectedItem = None

    def clear(self):
        #çocukları da silinecek !!!!!!!!!! böyleyken hepsini siliyo işte
        for e in self.items:
            e.hide()
        self.items = []

    def resizeEvent(self, event):
        QScrollView.resizeEvent(self, event)
        self.myResize(self.visibleWidth())

    def myResize(self, width):
        mw = 0
        th = 0
        for i in self.items:
            h = i.sizeHint().height()
            mw = max(mw, i.sizeHint().width())
            i.setGeometry(0, th, width, h)
            th += h
        self.setMinimumSize(QSize(mw, 0))
        if th > self.height():
            self.resizeContents(width - 12, th)
        else:
            self.resizeContents(width, th)

    def add(self, item):
        pass

    def remove(self, item):
        pass

    def add(self, item):
        self.items.append(item)
        size = QSize(self.width(), self.height())
        self.resizeEvent(QResizeEvent(size , QSize(0, 0)))

class PListViewItem(QWidget):

    PLVIconButtonType = 1
    PLVRadioButtonType = 2

    widgetSpacing = 2

    def __init__(self, parent=None, name=None, text="text"):
        QWidget.__init__(self, parent.viewport(), name)
        self.parent = parent
        self.text = text
        self.widgets = []

        self.isExpanded = False
        self.isSelected = False
        self.depth = -1

        self.parentItem = None
        self.nextItem = None
        self.firstChild = None

        self.baseColor = QColor(200,200,200)
        #self.baseColor = KGlobalSettings.baseColor()

        #self.widget = QPushButton("Radio", self)
        self.icon = QPixmap("/usr/share/icons/BCTango/16x16/categories/package_network_www.png")

        self.fillColor = QColor(25,255,255)
        #self.fillColor = KGlobalSettings.buttonBackground()
        self.installEventFilter(self)
        self.show()

    def eventFilter(self, target, event):
        if(event.type()==QEvent.MouseButtonPress):
            pass
        elif(event.type()==QEvent.MouseButtonRelease):
            pass
        elif(event.type()==QEvent.Enter):
            pass
        elif(event.type()==QEvent.Leave):
            pass
        return False

    def setWidgetsBg(self):
        for w in self.widgets:
            w.setPaletteBackgroundColor(self.fillColor)

    def setWidgetsGeometry(self, width, height):
        if len(self.widgets):
            excess = 6
            for w in self.widgets:
                excess += w.width() + self.widgetSpacing
                mid = (height - w.height()) / 2
                w.setGeometry(width - excess, mid, w.width(), w.height())

    def paintEvent(self, event):
        paint = QPainter(self)
        col = QColor(200,200,200)
        paint.fillRect(event.rect(), QBrush(self.fillColor))
        if len(self.widgets):
            self.setWidgetsBg()

        dip = (self.height() - self.icon.height()) / 2
        paint.drawPixmap(2 + PListView.arrowSize + 6, dip, self.icon)

        col = QColor(20,20,20)
        self.setPaletteBackgroundColor(col)
        arr = QPointArray(3)
        top = (self.height() - PListView.arrowSize) / 2
        if self.isExpanded:
            arr.setPoint(0, QPoint(4,6))
            arr.setPoint(1, QPoint(12,6))
            arr.setPoint(2, QPoint(8,10))
        else:
            arr.setPoint(0, QPoint(4,dip+4))
            arr.setPoint(1, QPoint(4,dip+12))
            arr.setPoint(2, QPoint(8,dip+8))
        oldBrush = paint.brush()
        paint.setBrush(QBrush(col))
        paint.drawPolygon(arr)
        paint.setBrush(oldBrush)

        font = paint.font()
        fm = QFontMetrics(font)
        ascent = fm.ascent()
        mid = (self.height()+8) / 2
        paint.drawText(2 + PListView.arrowSize + 6 + self.icon.width() + 6, mid, unicode(self.text))

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        self.setWidgetsGeometry(w, h)
        return QWidget.resizeEvent(self, event)

    def sizeHint(self):
        f = QFont(self.font())
        fm = QFontMetrics(f)

        w = 1
        h = max(fm.height(), PListView.itemHeight)
        return QSize(w, 80)

    def addWidgetItem(self, type, args=None):
        if type == self.PLVIconButtonType:
            self.addPLVIconButton(args)
        elif type == self.PLVRadioButtonType:
            self.addPLVRadioButton(args)

    def addPLVIconButton(self, args):
        plvib = PLVIconButton(self, args)
        self.widgets.append(plvib)

    def addPLVRadioButton(self, args):
        plvrb = PLVRadioButton(self, args)
        self.widgets.append(plvrb)

class PLVIconButton(QPushButton):
    def __init__(self, parent, args):
        QPushButton.__init__(self, parent)
        self.setFlat(True)
        self.myset = getIconSet(args[0], KIcon.Small)
        self.setIconSet(self.myset)
        size = self.myset.iconSize(QIconSet.Small)
        self.myWidth = size.width()
        self.myHeight = size.height()
        self.resize(self.myWidth, self.myHeight)

class PLVRadioButton(QRadioButton):
    def __init__(self, parent, args):
        QRadioButton.__init__(self, parent)
        #self.myWidth = size.width()
        #self.myHeight = size.height()
        self.resize(16, 16)




