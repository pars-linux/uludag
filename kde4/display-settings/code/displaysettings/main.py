#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

# UI
from displaysettings.ui_main import Ui_mainWidget
from displaysettings.scene import DisplayScene

# Backend
from displaysettings.backend import Interface

# Config
#from displaysettings.config import

# Item widget
from displaysettings.item import ItemListWidgetItem, ItemWidget

class MainWidget(QtGui.QWidget, Ui_mainWidget):
    def __init__(self, parent, embed=False):
        QtGui.QWidget.__init__(self, parent)

        if embed:
            self.setupUi(parent)
        else:
            self.setupUi(self)

        self.scene = DisplayScene(self.graphicsView)

        # Backend
        self.iface = Interface()
        self.iface.listenSignals(self.signalHandler)

        # Fail if no packages provide backend
        self.checkBackend()

        self.reset()

    def checkBackend(self):
        """
            Check if there are packages that provide required backend.
        """
        if not len(self.iface.getPackages()):
            kdeui.KMessageBox.error(self, kdecore.i18n("There are no packages that provide backend for this application.\nPlease be sure that packages are installed and configured correctly."))
            return False
        return True

    def signalHandler(self, package, signal, args):
        pass

    def reset(self):
        info = "<qt>%s<br><i>%s</i></qt>" % (self.iface.cardModel, self.iface.cardVendor)
        self.cardInfoLabel.setText(info)

        self.refreshOutputList()

    def makeItemWidget(self, id_, title="", description="", type_=None, icon=None, state=None):
        """
            Makes an item widget having given properties.
        """
        widget = ItemWidget(self.listItems, id_, title, description, type_, icon, state)

        #self.connect(widget, QtCore.SIGNAL("stateChanged(int)"), self.slotItemState)
        #self.connect(widget, QtCore.SIGNAL("editClicked()"), self.slotItemEdit)
        #self.connect(widget, QtCore.SIGNAL("deleteClicked()"), self.slotItemDelete)

        return widget

    def addItem(self, id_, name="", description=""):
        """
            Adds an item to list.
        """

        type_ = "user"
        icon = "video-display"

        # Build widget and widget item
        widget = self.makeItemWidget(id_, name, description, type_, kdeui.KIcon(icon), None)
        widgetItem = ItemListWidgetItem(self.listItems, widget)

        # Add to list
        self.listItems.setItemWidget(widgetItem, widget)

    def refreshOutputList(self):
        self.listItems.clear()

        for output in self.iface.getOutputs():
            self.addItem(output.name, output.name, "Digital Output")
