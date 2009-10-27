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
from servicemanager.backend import ServiceIface
from servicemanager.about import aboutData
from servicemanager.ui_main import Ui_mainManager
from servicemanager.widgets import ServiceItemWidget, ServiceItem

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
        self.services = self.iface.services()
        self.services.sort()
        for service in self.services:
            item = ServiceItem(service, self.ui.listServices)
            item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
            item.setSizeHint(QSize(38,48))
            self.widgets[service] = ServiceItemWidget(service, self, item)
            self.ui.listServices.setItemWidget(item, self.widgets[service])
        self.infoCount = 0
        self.piece = 100/len(self.services)

        # Update service status and follow Comar for state changes
        self.getServices()

        # search line, we may use model view for correct filtering
        self.connect(self.ui.lineSearch, SIGNAL("textChanged(QString)"), self.doSearch)
        self.connect(self.ui.filterBox, SIGNAL("currentIndexChanged(int)"), self.filterServices)

    def doSearch(self, text):
        for service in self.services:
            if service.find(text) >= 0 or unicode(self.widgets[service].desc).lower().find(unicode(text).lower()) >= 0:
                self.widgets[service].item.setHidden(False)
            else:
                self.widgets[service].item.setHidden(True)
        if text == '':
            self.filterServices(self.ui.filterBox.currentIndex())

    def isLocal(self, service):
        return self.widgets[service].type == 'local'

    def filterServices(self, filterBy):
        Servers, SystemServices, StartupServices, RunningServices, AllServices = range(5)
        for service in self.services:
            if filterBy == Servers:
                if not self.isLocal(service):
                    self.widgets[service].item.setHidden(False)
                else:
                    self.widgets[service].item.setHidden(True)
            elif filterBy == SystemServices:
                if self.isLocal(service):
                    self.widgets[service].item.setHidden(False)
                else:
                    self.widgets[service].item.setHidden(True)
            elif filterBy == StartupServices:
                if self.widgets[service].runningAtStart:
                    self.widgets[service].item.setHidden(False)
                else:
                    self.widgets[service].item.setHidden(True)
            elif filterBy == RunningServices:
                if self.widgets[service].running:
                    self.widgets[service].item.setHidden(False)
                else:
                    self.widgets[service].item.setHidden(True)
            elif filterBy == AllServices:
                self.widgets[service].item.setHidden(False)

    def handleServices(self, package, exception, results):
        # Handle request and fill the listServices in the ui
        if not exception:
            self.widgets[package].updateService(results, True)
            self.infoCount+=1
            self.ui.progress.setValue(self.ui.progress.value() + self.piece)
            if self.infoCount == len(self.services):
                self.ui.progress.hide()
                self.ui.listServices.setEnabled(True)
                self.filterServices(self.ui.filterBox.currentIndex())
                self.doSearch(self.ui.lineSearch.text())

    def getServices(self):
        self.iface.services(self.handleServices)
        self.iface.listen(self.handler)

    def handler(self, package, signal, args):
        # print "COMAR :", args, signal, package
        self.widgets[package].setState(args[1])
        self.filterServices(self.ui.filterBox.currentIndex())
        self.doSearch(self.ui.lineSearch.text())


