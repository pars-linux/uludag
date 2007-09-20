# -*- coding: utf-8 -*-

from qt import *
from kutils import *

class MultiTabWidget(QWidget):    
    def __init__(self, parent = None, orient = KMultiTabBar.Horizontal, pos = KMultiTabBar.Top, name = None):
        QWidget.__init__(self, parent, name)
        if orient == KMultiTabBar.Horizontal:
            layout = QVBoxLayout(self, 6, 6)
        else:
            layout = QHBoxLayout(self, 6, 6)
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
        
    def addTab(self, widget, pix = None, id = -1, string = ""):
        if not pix:
            pix = QPixmap()
        self.tabWidget.appendTab(pix, id, string)
        self.stack.addWidget(widget, id)
        tab = self.tabWidget.tab(id)
        
        if self.orientation == KMultiTabBar.Horizontal:
            self.setFixedHeight(tab.height()+10)
        else:
            self.setFixedWidth(tab.width()+10)
        
        self.connect(tab, SIGNAL("clicked(int)"), self.tabClicked)
        
    def tabClicked(self, id):
        but = self.tabWidget.tab(id)
        if but.isOn():
            self.stack.show()
            self.stack.raiseWidget(id)
            if self.activeTabID != -1:
                self.tabWidget.tab(self.activeTabID).setOn(False)
                self.tabWidget.setTab(self.activeTabID, False)
            self.activeTabID = id
            self.tabWidget.setTab(self.activeTabID, True)
            
            # size related stuff
            if self.orientation == KMultiTabBar.Horizontal:
                if self.bigSize == -1:
                    self.bigSize = 200
                self.setMaximumHeight(700)
                self.resize(self.width(), self.bigSize)
            else:
                if self.bigSize == -1:
                    self.bigSize = 200
                self.setMaximumWidth(700)
                self.resize(self.bigSize, self.width())
                
        else: #tab is closing
            self.stack.hide()
            self.tabWidget.setTab(id, False)
            if self.orientation == KMultiTabBar.Horizontal:
                self.bigSize = self.height()
                self.setFixedHeight(self.tabWidget.tab(self.activeTabID).height() + 10)
            else:
                self.bigSize = self.width()
                self.setFixedWidth(self.tabWidget.tab(self.activeTabID).width() + 10)
            self.activeTabID = -1
            
    def setStyle(self, style):
        self.tabWidget.setStyle(style)

    def setPosition(self, pos):
        self.tabWidget.setPosition(pos)
            
