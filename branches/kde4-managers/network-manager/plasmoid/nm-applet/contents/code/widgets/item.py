#!/usr/bin/python
# -*- coding: utf-8 -*-

# Qt Libs
from PyQt4.QtGui import QWidget, QFrame, QGraphicsLinearLayout, QPixmap, QIcon
from PyQt4.QtCore import SIGNAL

# Custom Widget
from itemui import Ui_connectionItem

_css = "padding-left:4px;text-align:left;padding-right:4px;"
_cssEnter = "border:1px solid rgba(255,255,255,90);border-radius:5px;background-color: rgba(255, 255, 255, 40);"
_cssLeave = "border:1px solid rgba(0,0,0,0);background-color: rgba(0,0,0,0);"

class ConnectionItem(QWidget):

    def __init__(self, parent, package, name, dialog):
        QWidget.__init__(self, parent)

        self.ui = Ui_connectionItem()
        self.ui.setupUi(self)

        self.dialog = dialog
        self.name = name
        self.package = package

        self.connect(self.ui.button, SIGNAL("clicked()"), self.toggleConnection)
        self.setState()

    def enterEvent(self, event):
        self.ui.button.setStyleSheet(_css + _cssEnter)

    def leaveEvent(self, event):
        self.ui.button.setStyleSheet(_css + _cssLeave)

    def toggleConnection(self):
        self.dialog.parent.hide()
        self.dialog.iface.toggle(self.package, self.name)

    def setText(self, text):
        self.ui.button.setText(text)
        self.updateGeometry()

    def setState(self, state="down", ip=''):
        if state.startswith("up"):
            icon = QIcon(QPixmap(":/icons/check.png"))
            self.setText("%s - %s" % (self.name, ip))
        elif state == "connecting":
            icon = QIcon(QPixmap(":/icons/working.png"))
            self.setText(self.name)
        elif state == "down":
            icon = QIcon(QPixmap(":/icons/network-%s.png" % self.package))
            self.setText(self.name)
        self.ui.button.setIcon(icon)
        self.lastState = state
        del icon

