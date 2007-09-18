# -*- coding: utf-8 -*-

from qt import *
from kutils import *

class MultiTabWidget(QWidget):
    Vertical, Horizontal = 0, 1
    
    def __init__(self, parent = None, orient = KMultiTabBar.Horizontal, pos = KMultiTabBar.Top, name = None):
        QWidget.__init__(self, parent, name)
        if orient == KMultiTabBar.Horizontal:
            layout = QVBoxLayout(self, 3, 3)
            layout.setAutoAdd(True)
            if pos == KMultiTabBar.Top:
                self.tabWidget = KMultiTabBar(orient, self)
                self.tabWidget.setPosition(pos)
                self.stack = QWidgetStack(self)
            else:
                self.stack = QWidgetStack(self)
                self.tabWidget = KMultiTabBar(orient, self)
                self.tabWidget.setPosition(pos)
        else:
            layout = QHBoxLayout(self, 3, 3)
            layout.setAutoAdd(True)
            if pos == KMultiTabBar.Left:
                self.tabWidget = KMultiTabBar(orient, self)
                self.tabWidget.setPosition(pos)
                self.stack = QWidgetStack(self)
            else:
                self.stack = QWidgetStack(self)
                self.tabWidget = KMultiTabBar(orient, self)
                self.tabWidget.setPosition(pos)
        self.stack.hide()
        self.tabWidget.setStyle(KMultiTabBar.KDEV3ICON)
        
    def addTab(self, widget, pix = None, id = -1, string = ""):
        if not pix:
            pix = QPixmap()
        self.tabWidget.appendTab(pix, id, string)
        self.stack.addWidget(widget, id)
        but = self.tabWidget.tab(id)
        self.connect(but, SIGNAL("clicked(int)"), self.tabClicked)
        
    def tabClicked(self, id):
        but = self.tabWidget.tab(id)
        if but.isOn():
            self.stack.show()
            self.stack.raiseWidget(id)
        else:
            self.stack.hide()
            
    def setStyle(self, style):
        self.tabWidget.setStyle(style)

    def setPosition(self, pos):
        self.tabWidget.setPosition(pos)
            
