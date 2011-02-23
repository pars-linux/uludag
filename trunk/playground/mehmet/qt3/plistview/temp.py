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

# !!!!!!!!!!! viewportun dışında yapışık bi header olsa iyi olur
# !!!! butonlar hover olunca gözüksün seçeneği ekle
class PListView(QScrollView):
    itemHeight = 24
    iconHeight = 16
    arrowSize = 8
    def __init__(self, parent):
        QScrollView.__init__(self, parent)
        self.parent = parent
        self.items = []
        self.selectedItem = None
        self.hoverItem = None

        self.baseColor = KGlobalSettings.baseColor()
        self.selectedColor = KGlobalSettings.highlightColor()
        self.hoverColor = KGlobalSettings.buttonBackground()
        self.viewport().setPaletteBackgroundColor(self.baseColor)

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
    PLVCheckBoxType = 3
    PLVButtonGroupType = 4

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

        self.icon = QPixmap("/usr/share/icons/BCTango/16x16/categories/package_network_www.png")

        self.installEventFilter(self)
        self.show()

    def findDepth(self):
        parent = self.parent

    def resetOldSelected(self, item):
        item.isSelected = False
        item.repaint()

    def eventFilter(self, target, event):
        if(event.type() == QEvent.MouseButtonPress):
            if not self.parent.selectedItem == self:
                if self.parent.selectedItem:
                    self.resetOldSelected(self.parent.selectedItem)
                self.parent.selectedItem = self
                self.isSelected = True
                self.repaint()
        elif (event.type() == QEvent.MouseButtonDblClick):
            print 'collapse or expand'
        elif (event.type() == QEvent.MouseButtonRelease):
            pass
        elif (event.type() == QEvent.Enter):
            self.parent.hoverItem = self
            self.repaint()
        elif (event.type() == QEvent.Leave):
            self.parent.hoverItem = None
            self.repaint()
        return False

    def setWidgetsBg(self, color):
        for w in self.widgets:
            w.setPaletteBackgroundColor(color)

    def setWidgetsGeometry(self, width, height):
        if len(self.widgets):
            excess = 6
            for w in self.widgets:
                excess += w.width() + self.widgetSpacing
                mid = (height - w.height()) / 2
                w.setGeometry(width - excess, mid, w.width(), w.height())

    def paintEvent(self, event):
        paint = QPainter(self)

        color = self.parent.baseColor
        if self.isSelected:
            color = self.parent.selectedColor
        elif self.parent.hoverItem == self:
            color = self.parent.hoverColor
        paint.fillRect(event.rect(), QBrush(color))
        if len(self.widgets) > 0:
            self.setWidgetsBg(color)

        dip = (self.height() - self.icon.height()) / 2
        paint.drawPixmap(2 + PListView.arrowSize + 6, dip, self.icon)

        col = QColor(0,0,0)
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
        return QSize(w, h)

    def addWidgetItem(self, type, args=None):
        if type == self.PLVIconButtonType:
            return self.addPLVIconButton(args, self)
        elif type == self.PLVRadioButtonType:
            return self.addPLVRadioButton(args, self)
        elif type == self.PLVCheckBoxType:
            return self.addPLVCheckBox(args, self)
        elif type == self.PLVButtonGroupType:
            return self.addPLVButtonGroup(args, self)

    def addPLVIconButton(self, args, parent):
        plvib = PLVIconButton(parent, args)
        if parent == self:
            self.widgets.append(plvib)
        return plvib

    def addPLVRadioButton(self, args, parent):
        plvrb = PLVRadioButton(parent, args)
        if parent == self:
            self.widgets.append(plvrb)
        return plvrb

    def addPLVCheckBox(self, args, parent):
        plvrb = PLVCheckBox(parent, args)
        if parent == self:
            self.widgets.append(plvrb)
        return plvrb

    def addPLVButtonGroup(self, args, parent):
        plvbg = PLVButtonGroup(parent, args)
        buttonList = []
        blist = args[0]
        for type in blist:
            if type == self.PLVIconButtonType:
                buttonList.append(plvbg.layout().addWidget(self.addPLVIconButton(args, args[1][args[0].index(type)], plvbg)))
            elif type == self.PLVRadioButtonType:
                buttonList.append(plvbg.layout().addWidget(self.addPLVRadioButton(args, plvbg)))
            elif type == self.PLVCheckBoxType:
                buttonList.append(plvbg.layout().addWidget(self.addPLVCheckBox(args, plvbg)))
        self.widgets.append(plvbg)
        return [plvbg, buttonList]

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
        self.resize(16, 16)

class PLVCheckBox(QCheckBox):
    def __init__(self, parent, args):
        QCheckBox.__init__(self, parent)
        self.resize(20, 20)

class PLVButtonGroup(QButtonGroup):
    buttonSpacing = 8
    def __init__(self, parent, args):
        QButtonGroup.__init__(self, parent)
        layout = QHBoxLayout(self)
        self.resize((16+self.buttonSpacing)*len(args[0]), 16)
        self.setFrameShape(QButtonGroup.NoFrame)



