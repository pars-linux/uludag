#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# System
import sys
import comar

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# Application Stuff
from backend import ServiceIface
from about import aboutData
from ui import Ui_mainManager
from uiitem import Ui_ServiceItemWidget
from widgets import ServiceItemWidget, ServiceItem

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_mainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        # Call Comar
        self.iface = ServiceIface()
        self.widgets = {}

        # Fill service list
        services = self.iface.services()
        services.sort()
        for service in services:
            item = ServiceItem(service, self.ui.listServices)
            self.widgets[service] = ServiceItemWidget(service, self, item)
            self.ui.listServices.setItemWidget(item, self.widgets[service])
            item.setSizeHint(QSize(38,48))
 
        # Update service status and follow Comar for state changes
        self.getServices()

    def handleServices(self, package, exception, results):
        # Handle request and fill the listServices in the ui
        if not exception:
            self.widgets[package].updateService(results)

    def getServices(self):
        self.iface.services(self.handleServices)
        self.iface.listen(self.handler)

    def handler(self, package, signal, args):
        self.widgets[package].setState(args[1])
        # print args, signal, package


