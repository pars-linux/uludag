# -*- coding: utf-8 -*-

from qt import *
from kutils import *

SIZEOPENED = 110
SIZECLOSED = 30

class MultiTabWidget(QWidget):
    def __init__(self, parent = None, orient = KMultiTabBar.Horizontal, pos = KMultiTabBar.Top, name = None):
        QWidget.__init__(self, parent, name)
        if orient == KMultiTabBar.Horizontal:
            layout = QVBoxLayout(self, 3)
        else:
            layout = QHBoxLayout(self, 3)
        layout.setAutoAdd(True)
        if pos == KMultiTabBar.Top or pos == KMultiTabBar.Left:
            self.tabWidget = KMultiTabBar(orient, self)
            self.tabWidget.setPosition(pos)
            self.stack = QWidgetStack(self)
        else:
            self.stack = QWidgetStack(self)
            self.tabWidget = KMultiTabBar(orient, self)
            self.tabWidget.setPosition(pos)
        self.stack.hide()
        self.tabWidget.setStyle(KMultiTabBar.KDEV3ICON)  
        
        self.activeTabID = -1      
        self.bigSize = -1
        self.orientation = orient
        self.setFixedHeight(SIZECLOSED)
        
    def addTab(self, widget, pix = None, id = -1, string = ""):
        if not pix:
            pix = QPixmap()
        self.tabWidget.appendTab(pix, id, string)
        self.stack.addWidget(widget, id)
        tab = self.tabWidget.tab(id)
        self.connect(tab, SIGNAL("clicked(int)"), self.tabClicked)
        
    def removeTab(self, id):
        self.shrinkTab()
        self.tabWidget.removeTab(id)
        self.stack.removeWidget(self.stack.widget(id))
        
    def tabClicked(self, id):
        if self.tabWidget.isTabRaised(id):
            self.expandTab(id)
        else: #tab is closing
            self.shrinkTab()
            
    def setStyle(self, style):
        self.tabWidget.setStyle(style)

    def setPosition(self, pos):
        self.tabWidget.setPosition(pos)
            
    def expandTab(self, id = 0):
        self.stack.show()
        self.stack.raiseWidget(id)
        if self.activeTabID != -1:
            self.tabWidget.tab(self.activeTabID).setOn(False) #raise the old activated button
            self.tabWidget.setTab(self.activeTabID, False) #mark it as closed
        self.activeTabID = id
        self.tabWidget.setTab(self.activeTabID, True)
        
        # size related stuff
        if self.bigSize == -1:
                self.bigSize = 100
        if self.orientation == KMultiTabBar.Horizontal:
            self.setMaximumHeight(500)
            self.setMinimumHeight(110)
            self.resize(self.width(), self.bigSize)
        else:
            self.setMaximumWidth(500)
            self.setMinimumWidth(110)
            self.resize(self.bigSize, self.height())
        self.updateGeometry()
            
    def shrinkTab(self):
        self.stack.hide()
        if self.activeTabID != -1:
            self.tabWidget.setTab(self.activeTabID, False)
        if self.orientation == KMultiTabBar.Horizontal:
            self.bigSize = self.height()
            self.setFixedHeight(SIZECLOSED)
        else:
            self.bigSize = self.width()
            self.setFixedWidth(SIZECLOSED)
        self.activeTabID = -1
        self.updateGeometry()
