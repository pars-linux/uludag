#!/usr/bin/python
# -*- coding: utf-8 -*-
# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# KDE Stuff
from PyKDE4 import kdeui

# Application Stuff

class ServiceItem(QtGui.QListWidgetItem):

    def __init__(self, package, parent):
        QtGui.QListWidgetItem.__init__(self, parent)
        self.package = package

class ServiceItemWidget(QtGui.QWidget):

    def __init__(self, package, parent, item):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_ServiceItemWidget()
        self.ui.setupUi(self)

        self.ui.labelName.setText(package)

        self.toggleButtons()

        self.ui.buttonStart.setIcon(kdeui.KIcon("media-playback-start"))
        self.ui.buttonStop.setIcon(kdeui.KIcon("media-playback-stop"))
        self.ui.buttonReload.setIcon(kdeui.KIcon("view-refresh"))

        self.toggled = False
        self.iface = parent.iface
        self.item = item
        self.package = package
        self.type = None
        self.desc = None
        self.connect(self.ui.buttonStart, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonStop, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.buttonReload, SIGNAL("clicked()"), self.setService)
        self.connect(self.ui.checkStart, SIGNAL("clicked()"), self.setService)
