#!/usr/bin/python
# -*- coding: utf-8 -*-

# Qt Libs
from PyQt4.QtGui import QWidget, QFrame, QGraphicsLinearLayout, QPixmap

# Custom Widget
from itemui import Ui_connectionItem

class ConnectionItem(QWidget):

    def __init__(self, parent, package, name, dialog):
        QWidget.__init__(self, parent)

        self.ui = Ui_connectionItem()
        self.ui.setupUi(self)

        self.ui.connectionSignal.hide()

        self.dialog = dialog
        self.name = name
        self.package = package
        self.setText(name)
        self.setState()

    def enterEvent(self, event):
        self.ui.frame.setFrameShadow(QFrame.Raised)

    def leaveEvent(self, event):
        self.ui.frame.setFrameShadow(QFrame.Plain)

    def mouseReleaseEvent(self, event):
        self.dialog.parent.hide()
        self.dialog.iface.toggle(self.package, self.name)

    def setText(self, text):
        self.ui.connectionName.setText(text)

    def setState(self, state="down"):
        if state.startswith("up"):
            self.ui.connectionStatus.setPixmap(QPixmap(":/icons/check.png"))
        elif state == "connecting":
            self.ui.connectionStatus.setPixmap(QPixmap(":/icons/working.png"))
        else:
            self.ui.connectionStatus.setPixmap(
                    QPixmap(":/icons/network-%s.png" % self.package))
        self.lastState = state

