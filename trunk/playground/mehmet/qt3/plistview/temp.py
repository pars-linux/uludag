#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import os
import locale

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

class PListView(QScrollView):
    def __init__(self, parent):
        QScrollView.__init__(self, parent)
        self.viewport().setPaletteBackgroundColor(QColor(255,255,255))
        self.parent = parent
        self.items = []
        self.selectedItem = None

    def clear(self):
        #çocukları da silinecek !!!!!!!!!!
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

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

class PListViewItem(QWidget):
    def __init__(self, parent=None, name=None, text="text"):
        QWidget.__init__(self, parent.viewport(), name)
        self.parent = parent
        self.text = text
        self.widget = None

        self.isExpanded = False
        self.isSelected = False
        self.depth = -1

        self.parentItem = None
        self.nextItem = None
        self.firstChild = None

        #self.widget = QPushButton("Radio", self)
        self.icon = QPixmap("/usr/share/icons/BCTango/32x32/actions/down.png")

        self.fillColor = QColor(25,255,255)
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

    def paintEvent(self, event):

        paint = QPainter(self)
        col = QColor(200,200,200)
        paint.fillRect(event.rect(), QBrush(self.fillColor))
        if self.widget:
            self.widget.setPaletteBackgroundColor(col)

        dip = (self.height() - self.icon.height()) / 2
        paint.drawPixmap(6, dip, self.icon)

        oldFont = paint.font()
        font = QFont(oldFont)
        font.setItalic(True)
        font.setPointSize(10)

        col = QColor(20,20,20)
        self.setPaletteBackgroundColor(col)
        paint.fillRect(QRect(100, 40, 40, 40), QBrush(col))
        #paint.drawText(120, 40, unicode(self.text))
        arr = QPointArray(3)
        arr.setPoint(0, QPoint(20,20))
        arr.setPoint(1, QPoint(70,30))
        arr.setPoint(2, QPoint(60,40))
        paint.drawPolygon(arr)
        if self.isExpanded:
            pass
        else:
            pass

        paint.drawText(12 + self.icon.width() + 6, 12, unicode(self.text))

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        if self.widget:
            self.widget.setGeometry(w - self.widget.width() - 6, 5, self.widget.width(), self.widget.height())
        return QWidget.resizeEvent(self, event)

    def sizeHint(self):
        f = QFont(self.font())
        f.setPointSize(f.pointSize() + 1)
        f.setBold(True)
        fm = QFontMetrics(f)
        extra = 0
        if self.widget:
            extra = self.widget.width()
        w = 6 + self.icon.width() + 6 +  30 + extra + 6

        f.setPointSize(f.pointSize() - 2)
        fm2 = self.fontMetrics()
        w2 = 6 + self.icon.width() + 6 +  30 + extra + 6

        w = max(w, w2)
        h = max(fm.height() + 10, 24) + 10
        return QSize(w, h)




