#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import dbus

from PyQt4 import QtGui

from ui_mainwindow import Ui_MainManager
from interface import ComarIface, PisiIface

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_MainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        self.cface = ComarIface()
        self.pface = PisiIface()

        self.iface.listen(self.handler)

    def handler(self, package, signal, args):
        pass

