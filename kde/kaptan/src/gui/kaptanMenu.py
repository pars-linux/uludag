#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, SIGNAL

class Menu:

    def __init__(self, titles, labelWidget):
        self.zoom = 5
        self.defaultFontSize = 8
        self.position = 0
        self.menuText = ""
        self.menuNode = " <span style='font-size:%spt;'>%s</span> "

        # get titles
        self.titles = titles

        # get label widget
        self.label = labelWidget

    def move(self):
        self.menuText = ""
        lastItemIndex = len(self.titles)

        for index in range(0, lastItemIndex):
            menuItemText = self.titles[index]
            if index == (self.position - 1):
                self.menuText += self.menuNode % (self.defaultFontSize, menuItemText)
            if index == (self.position):
                self.menuText += self.menuNode % (self.defaultFontSize + self.zoom, menuItemText)
            if index == (self.position + 1):
                self.menuText += self.menuNode % (self.defaultFontSize, menuItemText)

        self.label.setText(self.menuText)

    def next(self):
        self.position += 1
        self.move()

    def prev(self):
        self.position -= 1
        self.move()

    def start(self):
        self.position = 0
        self.move()
