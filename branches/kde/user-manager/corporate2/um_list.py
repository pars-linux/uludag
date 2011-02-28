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

def getIcon(name, group=KIcon.Small):
    return KGlobal.iconLoader().loadIcon(name, group)

# !!!!!!!!!!! viewportun dışında yapışık bi header olsa iyi olur
# !!!! butonlar hover olunca gözüksün seçeneği ekle
class PListView(QScrollView):

    itemHeight = 24
    iconSize = 16
    arrowSize = 8
    depthSize = 12

    def __init__(self, parent, name=None):
        QScrollView.__init__(self, parent, name)
        self.parent = parent
        self.firstItem = None
        self.items = [] # tüm itemler. hiyerarşi yok
        self.visibleitems = []
        self.selectedItem = None
        self.hoverItem = None

        self.layout = QBoxLayout(self.viewport(), 0, 0)
        self.layout.setDirection(QVBoxLayout.TopToBottom)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        #self.spacer = QSpacerItem(4, 4, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #self.layout.insertItem(-1, self.spacer)

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
        self.repaint()
        #self.layout.removeItem(self.spacer)
        #self.layout.insertItem(-1, self.spacer)

    def myResize(self, width):
        mw = 0
        th = 0
        for i in self.visibleitems:
            h = i.sizeHint().height()
            mw = max(mw, i.sizeHint().width())
            #i.setGeometry(0, th, width, h)
            th += h
        #self.setMinimumSize(QSize(mw, 0))
        if th > self.height():
            self.resizeContents(width - 12, th)
        else:
            self.resizeContents(width, th)
        #print 'myresize içiiiiiii'
        self.setContentsPos(0,0)
        #self.updateContents(0,0, 50,500)

    def remove(self, item):
        it = item.firstChild
        while it:
            self.remove(it)
            it = it.nextItem
        previousItem = self.findPreviousItem(item)
        previousItem.nextItem = item.nextItem
        self.layout.remove(item)
        self.items.remove(item)

    def findPreviousItem(self, item):
        previous = None
        if item.parentItem:
            it = item.parentItem.firstChild
        else:
            it = self.firstItem
        while it:
            if it == item:
                return previous
            else:
                previous = it
                it = it.nextItem

    def add(self, item):
        # pop spacer
        #self.layout.removeItem(self.spacer)
        self.items.append(item)
        self.visibleitems.append(item)
        size = QSize(self.width(), self.height())
        self.resizeEvent(QResizeEvent(size , QSize(0, 0)))
        if item.parentItem:
            index = self.layout.findWidget(item.parentItem)
            self.layout.insertWidget(index+1, item)
            if item.parentItem.firstChild: # childların sonuna ekle
                lastChild = item.parentItem.findLastChild()
                lastChild.nextItem = item
            else: # first child olarak ekle
                item.parentItem.firstChild = item
            #item.reparent(self, 0, QPoint(0,0), False)
        else:
            # add to end (index = -1)
            #self.layout.removeItem(self.spacer)
            self.layout.insertWidget(-1, item)
            #self.layout.insertItem(-1, self.spacer)
            if not self.firstItem:
                self.firstItem = item
            else:
                lastSibling = self.findLastSibling(self.firstItem)
                lastSibling.nextItem = item
        # push spacer
        #self.layout.insertItem(-1, self.spacer)
        #if item.parentItem:
        #    item.hide()

    def findLastSibling(self, item):
        if not item.nextItem:
            return item
        else:
            it = item.nextItem
        while it:
            if not it.nextItem:
                return it
            it = it.nextItem


class PListViewItem(QWidget):

    PLVIconButtonType = 1
    PLVRadioButtonType = 2
    PLVCheckBoxType = 3
    PLVButtonGroupType = 4

    widgetSpacing = 2

    PLVIMouseClicked = 101
    PLVIMouseDoubleClicked = 102

    def __init__(self, parent=None, name=None, text="text", parentItem=None, data=None, icon=None):
        QWidget.__init__(self, parent.viewport(), name)
        self.buffer = QPixmap()
        self.parent = parent
        self.text = text
        self.widgets = []

        self.data = data

        self.isExpanded = False
        self.isSelected = False
        self.depth = -1

        self.parentItem = parentItem
        self.nextItem = None
        self.firstChild = None

        self.icon = getIcon(icon) if icon else None

        self.installEventFilter(self)

        self.setMaximumHeight(self.parent.itemHeight)
        self.setMinimumHeight(self.parent.itemHeight)

        self.setDepth()
        self.depthExtra = self.depth * PListView.depthSize

        self.show()

    def setItemIcon(self, icon):
        self.icon = getIcon(icon) if icon else None
        self.repaint()

    def isInArrowArea(self, x):
        if ((self.depthExtra + self.parent.depthSize) > x) and (self.depthExtra < x):
            return True
        return False

    def findLastChild(self):
        child = self.firstChild
        while child:
            if child.nextItem:
                child = child.nextItem
            else:
                return child
        return

    def setDepth(self):
        parent = self.parentItem
        depth = 0
        while parent:
            parent = parent.parentItem
            depth += 1
        self.depth = depth

    def resetOldSelected(self, item):
        item.isSelected = False
        item.repaint()
    # normal listviewde first child olmadığı zaman arrow gözükmez ve + işareti çıkmadığı için tıklama yapılmaz.
    # burda çocuğu olmasa dahi arrow gözükecek ve expanded signali yollanacak, adam slotta denetlesin
    # böyle bir şeyi yapma sebebi, expanded olduğunda listenin altını doldurmak isteği, öbür türlü fake bi kayıt koymak ve sonra
    # onu silmek gerekiyo
    def expandOrCollapse(self):
        #if not self.firstChild:
        #    return False
        self.isExpanded = not self.isExpanded
        self.repaint()
        if self.isExpanded:
            self.showChilds()
            self.parent.emit(PYSIGNAL("expanded"), (self,))
        else:
            self.hideChilds()
            self.parent.emit(PYSIGNAL("collapsed"), (self,))
        self.parent.resizeEvent(QResizeEvent(QSize(self.width(), self.height()), QSize(self.width(), self.height())))

    def eventFilter(self, target, event):
        if(event.type() == QEvent.MouseButtonPress):
            if not self.parent.selectedItem == self:
                if self.parent.selectedItem:
                    self.resetOldSelected(self.parent.selectedItem)
                self.parent.selectedItem = self
                self.isSelected = True
                self.repaint()
            if self.isInArrowArea(event.pos().x()):
                self.isSelected = True
                self.expandOrCollapse()
            self.parent.emit(PYSIGNAL("clicked"), (event, self,))
        elif (event.type() == QEvent.MouseButtonDblClick):
            self.expandOrCollapse()
            #print 'event filter içiii'
            #self.parent.scrollBy(0,500)
            #self.parent.ensureVisible(event.pos().x(), self.pos().y())
            #print event.pos().x(), self.pos().y()
            self.parent.emit(PYSIGNAL("clicked"), (event, self,))
        elif (event.type() == QEvent.MouseButtonRelease):
            pass
        elif (event.type() == QEvent.Enter):
            self.parent.hoverItem = self
            self.repaint()
        elif (event.type() == QEvent.Leave):
            self.parent.hoverItem = None
            self.repaint()
        return False

    def showChilds(self):
        child = self.firstChild
        while child:
            child.show()
            if child not in self.parent.visibleitems:
                self.parent.visibleitems.append(child)
            child = child.nextItem

    def hideChilds(self):
        child = self.firstChild
        while child:
            child.hide()
            if child in self.parent.visibleitems:
                self.parent.visibleitems.remove(child)
            if child.firstChild:
                child.isExpanded = False
                child.hideChilds()
            child = child.nextItem

    def getChilds(self):
        childs = []
        it = self.firstChild
        while it:
            childs.append(it)
            it = it.nextItem
        return childs

    def setWidgetsBg(self, color):
        for w in self.widgets:
            w.setPaletteBackgroundColor(color)

    def setWidgetsGeometry(self, width, height):
        excess = 6
        for w in self.widgets:
            excess += w.width() + self.widgetSpacing
            mid = (height - w.height()) / 2
            w.setGeometry(width - excess, mid, w.width(), w.height())

    def paintEvent(self, event):

        #paint = QPainter(self)
        paint = QPainter(self.buffer)
        if not paint.isActive():
            paint.begin(self.buffer)

        color = self.parent.baseColor
        if self.isSelected:
            color = self.parent.selectedColor
        elif self.parent.hoverItem == self:
            color = self.parent.hoverColor
        #paint.fillRect(event.rect(), QBrush(color))
        paint.fillRect(event.rect(), QBrush(color))
        if len(self.widgets) > 0:
            self.setWidgetsBg(color)

        if self.icon:
            dip = (self.height() - self.icon.height()) / 2
            paint.drawPixmap(self.depthExtra + 2 + PListView.arrowSize + 6, dip, self.icon)
        else:
            dip = (self.height() - self.parent.iconSize) / 2

        col = QColor(0,0,0)
        #self.setPaletteBackgroundColor(col)
        arr = QPointArray(3)
        top = (self.height() - PListView.arrowSize) / 2
        if self.isExpanded:
            arr.setPoint(0, QPoint(self.depthExtra+2,10))
            arr.setPoint(1, QPoint(self.depthExtra+10,10))
            arr.setPoint(2, QPoint(self.depthExtra+6,14))
        else:
            arr.setPoint(0, QPoint(self.depthExtra+4,dip+4))
            arr.setPoint(1, QPoint(self.depthExtra+4,dip+12))
            arr.setPoint(2, QPoint(self.depthExtra+8,dip+8))
        oldBrush = paint.brush()
        paint.setBrush(QBrush(col))
        paint.drawPolygon(arr)
        paint.setBrush(oldBrush)

        font = paint.font()
        fm = QFontMetrics(font)
        ascent = fm.ascent()
        mid = (self.height()+8) / 2
        paint.drawText(self.depthExtra + 2 + PListView.arrowSize + 6 + self.parent.iconSize + 6, mid, unicode(self.text))

        paint.end()
        bitBlt(self, 0, 0, self.buffer)

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        self.setWidgetsGeometry(w, h)
        self.buffer = QPixmap(w,h)
        self.handleItemText()
        return QWidget.resizeEvent(self, event)

    def handleItemText(self):
        pass

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



