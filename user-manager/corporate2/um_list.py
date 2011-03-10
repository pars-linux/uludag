#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import os
import qt
import locale

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner
from kdecore import *
from kdeui import *
import kdedesigner

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

        self.header = None

        """self.layout = QBoxLayout(self.viewport(), 0, 0)
        self.layout.setDirection(QVBoxLayout.TopToBottom)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)"""
        #self.setStaticBackground(True)
        self.enableClipper(True)

        self.baseColor = KGlobalSettings.baseColor()
        self.selectedColor = KGlobalSettings.highlightColor()
        self.hoverColor = KGlobalSettings.buttonBackground()
        self.viewport().setPaletteBackgroundColor(self.baseColor)

    def showSelected(self):
        self.ensureVisible(0, self.visibleitems.index(self.selectedItem)*self.itemHeight)

    def clear(self):
        #çocukları da silinecek !!!!!!!!!! böyleyken hepsini siliyo işte
        for e in self.items:
            e.hide()
        self.items = []

    def resizeEvent(self, event):
        QScrollView.resizeEvent(self, event)
        self.myResize(self.visibleWidth())
        #self.repaint()

    def viewportResizeEvent(self, e):
        for x in self.visibleitems:
            x.resize(self.width(), self.itemHeight)
        if self.header:
            if self.verticalScrollBar().isVisible():
                width = self.verticalScrollBar().pos().x()-2
            else:
                width = self.width()-4
            #self.header.resize(width-4, self.header.headerHeight)
            self.header.setGeometry(2,2,width, self.header.headerHeight)

    def myResize(self, width):
        mw = 0
        th = 0
        th = (len(self.visibleitems)*self.itemHeight)+self.getHeaderHeight()
        #for i in self.visibleitems:
            #h = i.sizeHint().height()
            #mw = max(mw, i.sizeHint().width())
            #i.setGeometry(0, th, width, h)
            #th += h
        #self.setMinimumSize(QSize(mw, 0))
        if th > self.height():
            self.resizeContents(width - 16, th)
            for i in self.visibleitems:
                i.setWidgetsGeometry(self.firstItem.width(), self.firstItem.height())
        else:
            self.resizeContents(width, th)
            for i in self.visibleitems:
                if self.firstItem:
                    i.setWidgetsGeometry(self.firstItem.width(), self.firstItem.height())
        #self.setContentsPos(0,0)
        #self.updateContents(0,0, 50,500)

    def remove(self, item):
        it = item.firstChild
        while it:
            self.remove(it)
            it = it.nextItem
        previousItem = self.findPreviousItem(item)
        if not previousItem: # sen ilk çocuksun ve başka çocuk yok
            if item.parentItem: # kök değil
                item.parentItem.firstChild = None
        else:
            previousItem.nextItem = item.nextItem
        item.clear()
        item.hide()
        self.removeChild(item)
        self.items.remove(item)
        if item in self.visibleitems:
            self.visibleitems.remove(item)
        #self.moveChild(item, 0, 0)
        del item
        """if not self.findAnItemWhoHasAChild(item):
            self.setSiblingHasChild(item, False)"""

    def findAnItemWhoHasAChild(self, item):
        it = item.parentItem
        while it:
            if it.firstChild:
                return it
            it = it.nextItem
        return

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

    def getHeaderHeight(self):
        headerHeight = 0
        if self.header and self.header.isVisible:
            headerHeight = PListViewHeader.headerHeight
        return headerHeight

    def shiftLowerItems(self, item):
        for i in range(self.visibleitems.index(item), len(self.visibleitems)):
            shiftItem = self.visibleitems[i]
            self.moveChild(shiftItem, 0, (self.visibleitems.index(shiftItem)*self.itemHeight)+self.getHeaderHeight())
            #print self.visibleitems.index(item)*self.itemHeight
            #print self.visibleitems[i].name

    def add(self, item):
        ### Ekleme yapıldığında collapsed ise açılmalı !!!!!!!!
        ### NAsıl ise öyle kalmalı burda açma kapama yapma
        size = QSize(self.width(), self.height())
        self.resizeEvent(QResizeEvent(size , QSize(0, 0)))
        if item.parentItem:
            if not item.parentItem in self.items:
                return # 
            lastChild = item.parentItem.findLastChild()
            if lastChild:
                self.items.insert(self.items.index(lastChild)+1, item)
                lastChild.nextItem = item
            else:
                self.items.insert(self.items.index(item.parentItem)+1, item)
                item.parentItem.firstChild = item
            if item.parentItem.isExpanded: # çocuk gözükecek
                # kendinden önce gözükür durumda olan eleman ya kardeşidir ya da atası
                previousItem = self.findPreviousItem(item)
                if lastChild: # sen ilk çocuksun ve başka çocuk yok
                    self.visibleitems.insert(self.visibleitems.index(lastChild)+1, item)
                else:
                    self.visibleitems.insert(self.visibleitems.index(item.parentItem)+1, item)
                self.addChild(item, 0, (self.visibleitems.index(item)*self.itemHeight)+self.getHeaderHeight())
                self.shiftLowerItems(item)
            # is resize really required? try to remove below line
            item.resize(item.parentItem.width(), self.itemHeight)
            #self.setSiblingHasChild(item.parentItem, True)

        else:
            self.items.insert(len(self.items), item) # en sona ekle
            self.visibleitems.insert(len(self.visibleitems), item) # parentı yoksa  mutlaka visible olur
            self.addChild(item, 0, (self.visibleitems.index(item)*self.itemHeight)+self.getHeaderHeight())
            if not self.firstItem:
                self.firstItem = item
            else:
                lastSibling = self.findLastSibling(self.firstItem)
                lastSibling.nextItem = item
        #if item.parentItem:
        #    item.hide()

    def showHeader(self):
        self.header.isVisible = True
        self.addChild(self.header, 0, 0)
        if len(self.visibleitems):
            self.shiftLowerItems(self.visibleitems[0])

    def hideHeader(self):
        self.header.isVisible = False
        self.removeChild(item)
        if len(self.visibleitems):
            self.shiftLowerItems(self.visibleitems[0])

    def addHeader(self, header):
        self.header = header
        self.items.insert(0, header)
        if len(self.visibleitems):
            self.shiftLowerItems(self.visibleitems[0])

    def setSiblingHasChild(self, item, hasChild):
        if item.parentItem:
            it = item.parentItem.firstChild
        else:
            it = self.firstItem
        while it:
            it.siblingHasChild = hasChild
            it.repaint()
            it = it.nextItem

    def findLastSibling(self, item):
        if not item.nextItem:
            return item
        else:
            it = item.nextItem
        while it:
            if not it.nextItem:
                return it
            it = it.nextItem

    def clearSelection(self):
        if self.selectedItem:
            self.selectedItem.isSelected = False
            self.selectedItem.repaint()
            self.selectedItem = None
        for i in self.items:
            if isinstance(i, PListViewHeader):
                continue
            for w in i.widgets:
                if isinstance(w, PLVButtonGroup):
                    w.setExclusive(False)
                    for b in w.buttonList:
                        if isinstance(b, PLVRadioButton):
                            b.setOn(False)
                        elif isinstance(b, PLVIconRadioButton):
                            b.setOn(False)
                            b.isMouseOver = False


class PListViewItem(QWidget):

    PLVIconButtonType = 1
    PLVRadioButtonType = 2
    PLVCheckBoxType = 3
    PLVButtonGroupType = 4
    PLVFlatComboType = 5
    PLVIconRadioButtonType = 6

    widgetSpacing = 2

    PLVIMouseClicked = 101
    PLVIMouseDoubleClicked = 102

    textLength = 0

    def __init__(self, parent=None, name=None, text="text", parentItem=None, data=None, icon=None, enableWidgetHiding=False):
        QWidget.__init__(self, parent.viewport(), name)
        self.buffer = QPixmap()
        self.parent = parent
        self.text = text
        self.textOut = text
        self.widgets = []

        self.data = data

        self.isExpanded = False
        self.isSelected = False
        self.siblingHasChild = False
        self.depth = -1

        self.parentItem = parentItem
        self.nextItem = None
        self.firstChild = None

        self.enableWidgetHiding = enableWidgetHiding
        self.threeDotLength = self.fontMetrics().width("...")

        self.icon = icon

        self.flickerCtrl = False

        self.installEventFilter(self)

        self.setMaximumHeight(self.parent.itemHeight)
        self.setMinimumHeight(self.parent.itemHeight)

        self.setDepth()
        self.depthExtra = self.depth * PListView.depthSize
        self.parent.add(self)
        self.show()

    def clear(self):
        for w in self.widgets:
            w.hide()
        self.widgets = []

    def setItemIcon(self, icon):
        self.icon = icon
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
        if item.enableWidgetHiding:
            item.hideWidgets()
        item.repaint()

    def expand(self):
        if not self.firstChild:
            return False
        self.showChilds()
        self.parent.emit(PYSIGNAL("expanded"), (self,))
        self.parent.shiftLowerItems(self)
        self.parent.resizeEvent(QResizeEvent(QSize(self.parent.visibleWidth(), len(self.parent.visibleitems)*self.parent.itemHeight), QSize(0, 0)))

    def collapse(self):
        if not self.firstChild:
            return False
        self.hideChilds()
        self.parent.emit(PYSIGNAL("collapsed"), (self,))
        self.parent.shiftLowerItems(self)
        self.parent.resizeEvent(QResizeEvent(QSize(self.parent.visibleWidth(), len(self.parent.visibleitems)*self.parent.itemHeight), QSize(0, 0)))

    def expandOrCollapse(self):
        if not self.firstChild:
            return False
        self.isExpanded = not self.isExpanded
        if self.isExpanded:
            self.showChilds()
            self.parent.emit(PYSIGNAL("expanded"), (self,))
        else:
            self.hideChilds()
            self.parent.emit(PYSIGNAL("collapsed"), (self,))
        self.parent.shiftLowerItems(self)
        self.parent.resizeEvent(QResizeEvent(QSize(self.parent.visibleWidth(), len(self.parent.visibleitems)*self.parent.itemHeight), QSize(0, 0)))
        self.repaint()
        #self.parent.resizeContents(self.parent.visibleWidth(), len(self.visibleitems)*self.itemHeight)

    def hideWidgets(self):
        for w in self.widgets:
            w.hide()

    def showWidgets(self):
        if self.flickerCtrl:
            return
        for w in self.widgets:
            w.show()

    def eventFilter(self, target, event):
        if(event.type() == QEvent.MouseButtonPress):
            if not self.parent.selectedItem == self:
                if self.parent.selectedItem:
                    self.resetOldSelected(self.parent.selectedItem)
                self.parent.selectedItem = self
                self.isSelected = True
                self.repaint()
            if self.firstChild and self.isInArrowArea(event.pos().x()):
                self.isSelected = True
                self.expandOrCollapse()
            self.parent.emit(PYSIGNAL("clicked"), (event, self,))
            self.setFocus()
            self.flickerCtrl = True
        elif (event.type() == QEvent.MouseButtonDblClick):
            self.expandOrCollapse()
            self.parent.emit(PYSIGNAL("clicked"), (event, self,))
        elif (event.type() == QEvent.MouseButtonRelease):
            self.flickerCtrl = False
        elif (event.type() == QEvent.Enter):
            self.parent.hoverItem = self
            if self.enableWidgetHiding:
                self.showWidgets()
            self.repaint()
        elif (event.type() == QEvent.Leave):
            self.parent.hoverItem = None
            if self.enableWidgetHiding:
                self.hideWidgets()
            self.repaint()
        elif (event.type() == QEvent.KeyPress):
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.expandOrCollapse()
            elif event.key() == Qt.Key_Up:
                index = self.parent.visibleitems.index(self)
                previous = self.parent.visibleitems[index-1]
                self.resetOldSelected(self)
                self.parent.selectedItem = previous
                previous.isSelected = True
                previous.repaint()
                previous.setFocus()
                self.parent.showSelected()
                return True
            elif event.key() == Qt.Key_Down:
                index = self.parent.visibleitems.index(self)
                if index == len(self.parent.visibleitems)-1:
                    index = -1
                next = self.parent.visibleitems[index+1]
                self.resetOldSelected(self)
                self.parent.selectedItem = next
                next.isSelected = True
                next.repaint()
                next.setFocus()
                self.parent.showSelected()
                return True
            elif event.key() == Qt.Key_Tab:
                return False
            self.setFocus()
            return True
        self.parent.resizeEvent(QResizeEvent(QSize(self.parent.visibleWidth(), len(self.parent.visibleitems)*self.parent.itemHeight), QSize(0, 0)))
        return False

    def showChilds(self):
        self.isExpanded = True
        child = self.firstChild
        index = self.parent.visibleitems.index(self)
        while child:
            if child not in self.parent.visibleitems:
                self.parent.visibleitems.insert(index+1, child)
            index += 1
            child.resize(self.width(), self.height())
            child.show()
            child = child.nextItem
        self.parent.setContentsPos(0, self.parent.visibleitems.index(self)*self.parent.itemHeight)

    def hideChilds(self):
        self.isExpanded = False
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
            if isinstance(w, PLVButtonGroup):
                for i in w.buttonList:
                    i.setPaletteBackgroundColor(color)
                    i.bgcolor = color

    def setWidgetsGeometry(self, width, height):
        excess = 4
        if self.parent.verticalScrollBar().isVisible():
            excess += 12
        for w in self.widgets:
            excess += w.width() + self.widgetSpacing
            mid = (height - w.height()) / 2
            w.setGeometry(width - excess, mid, w.width(), w.height())
        self.textLength = self.width() - self.parent.iconSize - self.parent.arrowSize - self.threeDotLength - 10 - 2 - (self.parent.depthSize*self.depth) - excess
        if self.textLength < self.threeDotLength:
            self.textLength = 0
        self.calculateTextOut()

    def calculateTextOut(self):
        if not self.isVisible():
            return
        self.textOut = self.text
        width = self.fontMetrics().width(self.textOut)
        if width < self.textLength:
            return
        wi = self.decrementTextOutToHalf()
        ctrl = False
        while True:
            if wi <= 0:
                self.textOut = "..."
                return
            if wi < self.textLength:
                ctrl = True
                break
                #wi = self.incrementTextOutByHalf()
                break
            else:
                wi = self.decrementTextOutToHalf()
                if ctrl:
                    break
        while True:
            total = len(self.textOut)+1
            txt = self.text[:total]
            wi = self.fontMetrics().width(txt)
            if wi >= self.textLength:
                break
            self.textOut = txt
        self.textOut += "..."

    def decrementTextOutToHalf(self):
        total = len(self.textOut)/2
        self.textOut = self.textOut[:total]
        return self.fontMetrics().width(self.textOut)

    def incrementTextOutByHalf(self):
        total = (len(self.textOut)*3)/2
        self.textOut = self.text[:total]
        return self.fontMetrics().width(self.textOut)

    def isInViewArea(self):
        itemCount = ((self.parent.visibleHeight()-self.parent.getHeaderHeight())/self.parent.itemHeight)+1
        firstVisibleItemIndex = ((self.parent.contentsY()+self.parent.getHeaderHeight())/self.parent.itemHeight)-1
        lastVisibleItemIndex = firstVisibleItemIndex+itemCount
        myIndex = self.parent.visibleitems.index(self)
        if myIndex >= firstVisibleItemIndex and myIndex <= lastVisibleItemIndex:
            return True
        return False

    def paintEvent(self, event):
        if not self.isInViewArea():
            return
        paint = QPainter(self)
        #paint = QPainter(self.buffer)
        if not paint.isActive():
            #paint.begin(self.buffer)
            paint.begin(self)

        color = self.parent.baseColor
        if self.isSelected:
            color = self.parent.selectedColor
        elif self.parent.hoverItem == self:
            color = self.parent.hoverColor
        paint.fillRect(event.rect(), QBrush(color))
        if len(self.widgets) > 0:
            self.setWidgetsBg(color)

        if self.icon:
            dip = (self.height() - self.icon.height()) / 2
        else:
            dip = (self.height() - self.parent.iconSize) / 2

        arrow = PListView.arrowSize+4
        if self.firstChild:
            col = QColor(0,0,0)
            arr = QPointArray(3)
            if self.isExpanded:
                arr.setPoint(0, QPoint(self.depthExtra+2,dip+6))
                arr.setPoint(1, QPoint(self.depthExtra+10,dip+6))
                arr.setPoint(2, QPoint(self.depthExtra+6,dip+10))
            else:
                arr.setPoint(0, QPoint(self.depthExtra+4,dip+4))
                arr.setPoint(1, QPoint(self.depthExtra+4,dip+12))
                arr.setPoint(2, QPoint(self.depthExtra+8,dip+8))
            oldBrush = paint.brush()
            paint.setBrush(QBrush(col))
            paint.drawPolygon(arr)
            paint.setBrush(oldBrush)

        paint.drawPixmap(self.depthExtra + 2 + arrow + 2, dip, self.icon)

        font = paint.font()
        fm = QFontMetrics(font)
        ascent = fm.ascent()
        mid = (self.height()+8) / 2
        #font.setStyleStrategy(QFont.NoAntialias)
        paint.setFont(font)

        dx = self.depthExtra + 2 + arrow + 2 + self.parent.iconSize + 6
        paint.drawText(dx, mid, unicode(self.textOut))

        paint.end()
        #bitBlt(self, 0, 0, self.buffer)

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        self.setWidgetsGeometry(w, h)
        #self.buffer = QPixmap(w,h)
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
        elif type == self.PLVFlatComboType:
            return self.addPLVFlatCombo(args, self)

    def addPLVIconButton(self, args, parent):
        plvib = PLVIconButton(parent, args)
        if parent == self:
            self.widgets.append(plvib)
            if self.enableWidgetHiding:
                plvib.hide()
        return plvib

    def addPLVRadioButton(self, args, parent):
        plvrb = PLVRadioButton(parent, args)
        if parent == self:
            self.widgets.append(plvrb)
            if self.enableWidgetHiding:
                plvrb.hide()
        return plvrb

    def addPLVCheckBox(self, args, parent):
        plvcb = PLVCheckBox(parent, args)
        if parent == self:
            self.widgets.append(plvcb)
            if self.enableWidgetHiding:
                plvcb.hide()
        return plvcb

    def addPLVFlatCombo(self, args, parent):
        plvfc = PLVFlatCombo(parent, args)
        if parent == self:
            self.widgets.append(plvfc)
            if self.enableWidgetHiding:
                plvfc.hide()
        return plvfc

    def addPLVIconRadioButton(self, icon, parent):
        plvirb = PLVIconRadioButton(parent, icon)
        if parent == self:
            self.widgets.append(plvirb)
            if self.enableWidgetHiding:
                plvirb.hide()
        return plvirb

    def addPLVButtonGroup(self, args, parent):
        plvbg = PLVButtonGroup(parent, args)
        blist = args[0]
        index = 0
        for type in blist:
            if type == self.PLVIconButtonType:
                ib = self.addPLVIconButton(args, args[1][args[0].index(type)], plvbg)
                plvbg.layout().addWidget(ib)
                plvbg.buttonList.append(ib)
            elif type == self.PLVRadioButtonType:
                rb = self.addPLVRadioButton(args, plvbg)
                plvbg.layout().addWidget(rb)
                plvbg.buttonList.append(rb)
            elif type == self.PLVCheckBoxType:
                cb = self.addPLVCheckBox(args, plvbg)
                plvbg.layout().addWidget(cb)
                plvbg.buttonList.append(cb)
            elif type == self.PLVIconRadioButtonType:
                cb = self.addPLVIconRadioButton(args[1][index], plvbg)
                plvbg.layout().addWidget(cb)
                plvbg.buttonList.append(cb)
            index += 1
        self.widgets.append(plvbg)
        if self.enableWidgetHiding:
            plvbg.hide()
        return [plvbg, plvbg.buttonList]

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
        self.show()

class PLVRadioButton(QRadioButton):
    def __init__(self, parent, args):
        QRadioButton.__init__(self, parent)
        self.resize(16, 16)
        self.show()

class PLVIconRadioButton(QRadioButton):
    def __init__(self, parent, icon):
        QRadioButton.__init__(self, parent)
        self.resize(20, 20)
        self.setMinimumSize(QSize(20,20))
        self.setMaximumSize(QSize(20,20))
        self.show()
        self.parent = parent
        self.icon = icon
        self.isMouseOver = False
        self.installEventFilter(self)
        self.baseColor = KGlobalSettings.baseColor()
        self.bgcolor = self.baseColor
        self.selectedColor = KGlobalSettings.calculateAlternateBackgroundColor(KGlobalSettings.highlightColor())
        self.hoverColor = KGlobalSettings.calculateAlternateBackgroundColor(KGlobalSettings.buttonBackground())
        if isinstance(self.parent, PLVButtonGroup):
            self.connect(self, SIGNAL("toggled(bool)"), self.slotToogle)

    def slotToogle(self):
        for b in self.parent.buttonList:
            b.repaint()

    def eventFilter(self, target, event):
        if (event.type() == QEvent.Enter):
            self.isMouseOver = True
            self.repaint()
        elif (event.type() == QEvent.Leave):
            self.isMouseOver = False
            self.repaint()
        elif(event.type() == QEvent.MouseButtonPress):
            if not self.isOn():
                self.setOn(not self.isOn())
        return False

    def paintEvent(self, event):
        #üzerine gelip gelip durunca koyulaşıyo????
        paint = QPainter(self)
        if not paint.isActive():
            paint.begin(self)
        if self.isOn():
            paint.fillRect(0, 0, 20, 20, QBrush(self.selectedColor))
            oldPen = paint.pen()
            paint.setPen(QPen(QColor(50,50,50)))
            paint.drawRoundRect(0, 0, 20, 20)
            paint.setPen(oldPen)
        elif self.isMouseOver:
            paint.fillRect(0, 0, 20, 20, QBrush(self.hoverColor))
            oldPen = paint.pen()
            paint.setPen(QPen(QColor(50,50,50)))
            paint.drawRoundRect(0, 0, 20, 20)
            paint.setPen(oldPen)
        else:
            paint.fillRect(0, 0, 20, 20, QBrush(self.bgcolor))
        #    paint.fillRect(0, 0, 20, 20, QBrush(0))
        #oldBrush = paint.brush()
        #paint.setBrush(QBrush(self.selectedColor))
        #paint.drawRoundRect(0, 0, 20, 20)
        #paint.setBrush(oldBrush)
        paint.drawPixmap(2, 2, self.icon, 0, 0, 20, 20)
        paint.end()

class PLVCheckBox(QCheckBox):
    def __init__(self, parent, args):
        QCheckBox.__init__(self, parent)
        self.resize(20, 20)
        self.show()

class PLVButtonGroup(QButtonGroup):
    buttonSpacing = 8
    def __init__(self, parent, args):
        QButtonGroup.__init__(self, parent)
        layout = QHBoxLayout(self)
        self.resize((16+self.buttonSpacing)*len(args[0]), parent.height())
        self.setFrameShape(QButtonGroup.NoFrame)
        self.buttonList = []
        self.show()

class PLVFlatComboPopupData:
    def __init__(self, popupText, popupSlot):
        self.popupText = popupText
        self.popupSlot = popupSlot

class PLVFlatCombo(QWidget):
    def __init__(self, parent, args):
        QWidget.__init__(self, parent)
        self.popup = None
        self.parent = parent
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.installEventFilter(self)
        self.__text = args[0][0].popupText
        textWidth = self.fontMetrics().width(self.__text)
        s = QSize(4+textWidth+24, PListView.itemHeight)
        self.setMinimumSize(s)
        self.setMaximumSize(s)
        self.show()
        self.selectionPopup = QPopupMenu(self)
        popupItemList = args[0]
        for i in popupItemList:
            self.selectionPopup.insertItem(i.popupText, i.popupSlot)

    def setText(self, text):
        self.__text = text
        textWidth = self.fontMetrics().width(self.__text)
        s = QSize(4+textWidth+24, PListView.itemHeight)
        self.setMinimumSize(s)
        self.setMaximumSize(s)
        si = QSize(self.parent.width(), self.parent.height())
        self.parent.resizeEvent(QResizeEvent(si , QSize(0, 0)))

    def eventFilter(self, target, event):
        if(event.type() == QEvent.MouseButtonPress):
            #self.selectionPopup.exec_loop(self.parent.mapToGlobal(QPoint(self.pos().x(), self.pos().y()+self.height())))
            self.selectionPopup.exec_loop(self.parent.mapToGlobal(QPoint(self.pos().x(), self.pos().y())))
            return True
        return False

    def paintEvent(self, event):
        paint = QPainter(self)
        if not paint.isActive():
            paint.begin(self)

        #color = QColor(160,160,60)
        #paint.fillRect(event.rect(), QBrush(color))
        #w.setPaletteBackgroundColor(color)

        font = paint.font()
        fm = QFontMetrics(font)
        ascent = fm.ascent()
        mid = (self.height()+8) / 2

        #while(x<self.width()):
        #x,y,w,h,flags,text
        textWidth = self.fontMetrics().width(self.__text)
        paint.drawText(4, 0, textWidth+4, self.height(), Qt.AlignLeft|Qt.AlignVCenter, self.__text)
        #    x+=textWidth

        #paint.drawText(4, mid, unicode("ABC"))

        dip = (self.height() - 10)/2

        col = QColor(0,0,0)
        arrUp = QPointArray(3)
        arrDown = QPointArray(3)
        self.depthExtra = self.width() - 16
        arrDown.setPoint(0, QPoint(self.depthExtra+2,dip+6))
        arrDown.setPoint(1, QPoint(self.depthExtra+10,dip+6))
        arrDown.setPoint(2, QPoint(self.depthExtra+6,dip+10))
        arrUp.setPoint(0, QPoint(self.depthExtra+2,dip+4))
        arrUp.setPoint(1, QPoint(self.depthExtra+10,dip+4))
        arrUp.setPoint(2, QPoint(self.depthExtra+6,dip))
        oldBrush = paint.brush()
        paint.setBrush(QBrush(col))
        paint.drawPolygon(arrUp)
        paint.drawPolygon(arrDown)
        paint.setBrush(oldBrush)

        paint.end()


class PListViewHeader(QWidget):

    headerHeight = 24

    def __init__(self, parent=None, name=None, textMain="main-text", iconMain=None, textWidgets="text-widgets", iconWidgets=None):
        QWidget.__init__(self, parent, name)
        self.parent = parent
        self.textMain = textMain
        self.iconMain = iconMain
        self.textWidgets = textWidgets
        self.iconWidgets = iconWidgets

        self.isVisible = True

        self.setMaximumHeight(self.headerHeight)
        self.setMinimumHeight(self.headerHeight)

        self.parent.addHeader(self)
        self.show()

    def setWidgetsGeometry(self, width, height):
        return
        excess = 4
        if self.parent.verticalScrollBar().isVisible():
            excess += 12
        for w in self.widgets:
            excess += w.width() + self.widgetSpacing
            mid = (height - w.height()) / 2
            w.setGeometry(width - excess, mid, w.width(), w.height())
        self.textLength = self.width() - self.parent.iconSize - self.parent.arrowSize - self.threeDotLength - 10 - 2 - (self.parent.depthSize*self.depth) - excess
        self.calculateTextOut()

    def calculateTextOut(self):
        if not self.isVisible():
            return
        self.textOut = self.text
        width = self.fontMetrics().width(self.textOut)
        if width < self.textLength:
            return
        wi = self.decrementTextOutToHalf()
        ctrl = False
        while True:
            if wi <= 0:
                break
            if wi < self.textLength:
                ctrl = True
                wi = self.incrementTextOutByHalf()
                break
            else:
                wi = self.decrementTextOutToHalf()
                if ctrl:
                    break
        self.textOut += "..."

    def decrementTextOutToHalf(self):
        total = len(self.textOut)/2
        self.textOut = self.textOut[:total]
        return self.fontMetrics().width(self.textOut)

    def incrementTextOutByHalf(self):
        total = (len(self.textOut)*3)/2
        self.textOut = self.text[:total]
        return self.fontMetrics().width(self.textOut)

    def paintEvent(self, event):

        paint = QPainter(self)
        if not paint.isActive():
            paint.begin(self)

        #self.setPaletteBackgroundColor(self.parent.baseColor)
        paint.fillRect(0, 0, self.width(), self.height(), QBrush(0))

        iconMainWidth = 0
        if self.iconMain:
            dip = (self.height() - self.iconMain.height()) / 2
            paint.drawPixmap (2, dip, self.iconMain)
            iconMainWidth = self.iconMain.width() + 2
        #else:
        #    dip = (self.height() - self.parent.iconSize) / 2


        font = paint.font()
        fm = QFontMetrics(font)
        ascent = fm.ascent()
        mid = (self.height()+8) / 2
        #font.setStyleStrategy(QFont.NoAntialias)
        font.setBold(True)
        paint.setFont(font)

        dx = 2 + iconMainWidth + 4
        paint.drawText(dx, mid, unicode(self.textMain))
        #paint.drawText(0, 12, unicode("mana mana duub dubudb u"))

        paint.end()

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        self.setWidgetsGeometry(w, h)
        #self.buffer = QPixmap(w,h)
        """self.handleItemText()"""
        return QWidget.resizeEvent(self, event)

    def sizeHint(self):
        f = QFont(self.font())
        fm = QFontMetrics(f)

        w = 1
        h = max(fm.height(), PListViewHeader.headerHeight)
        return QSize(w, h)

