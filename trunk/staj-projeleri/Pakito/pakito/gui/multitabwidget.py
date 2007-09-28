# -*- coding: utf-8 -*-

from qt import *
from kutils import *

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
        self.setMinimumHeight(50)
        
    def addTab(self, widget, pix = None, id = -1, string = ""):
        if not pix:
            pix = QPixmap()
        self.tabWidget.appendTab(pix, id, string)
        self.stack.addWidget(widget, id)
        tab = self.tabWidget.tab(id)
        
        if self.orientation == KMultiTabBar.Horizontal:
            self.setFixedHeight(tab.height()+6)
        else:
            self.setFixedWidth(tab.width()+6)
        
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
            self.setMaximumHeight(700)
            self.setMinimumHeight(120)
            self.resize(self.width(), self.bigSize)
        else:
            self.setMaximumWidth(700)
            self.resize(self.bigSize, self.height())
            
    def shrinkTab(self):
        self.stack.hide()
        if self.activeTabID != -1:
            self.tabWidget.setTab(self.activeTabID, False)
        if self.orientation == KMultiTabBar.Horizontal:
            self.bigSize = self.height()
            self.setFixedHeight(self.tabWidget.tab(self.activeTabID).height() + 10)
        else:
            self.bigSize = self.width()
            self.setFixedWidth(self.tabWidget.tab(self.activeTabID).width() + 10)
        self.activeTabID = -1
