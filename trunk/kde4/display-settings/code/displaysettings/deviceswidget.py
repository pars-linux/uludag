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
from displaysettings.ui_devices import Ui_devicesWidget

# Backend
from displaysettings.backend import Interface

# Config
#from displaysettings.config import

from displaysettings.item import ItemListWidgetItem, ItemWidget
from displaysettings.carddialog import VideoCardDialog
from displaysettings.outputdialog import OutputDialog

from displaysettings.device import Output

# Define descriptions and icons for output types
OUTPUT_TYPES = {
        Output.UnknownOutput:   ("",  "video-display"),
        Output.LaptopPanel:     (kdecore.i18n("Laptop Panel"), "computer-laptop"),
        Output.AnalogOutput:    (kdecore.i18n("Analog Output"), "video-display"),
        Output.DigitalOutput:   (kdecore.i18n("Digital Output"), "video-display"),
        Output.TVOutput:        (kdecore.i18n("TV Output"), "video-television"),
        }

class MainWidget(QtGui.QWidget, Ui_devicesWidget):

    configChanged = QtCore.pyqtSignal()

    def __init__(self, parent, embed=False):
        QtGui.QWidget.__init__(self, parent)

        if embed:
            self.setupUi(parent)
        else:
            self.setupUi(self)

        self.configureCardButton.setIcon(kdeui.KIcon("configure"))

        # Backend
        self.iface = Interface()
        self.iface.listenSignals(self.signalHandler)

        # Fail if no packages provide backend
        self.checkBackend()

        self.cardDialog = VideoCardDialog(self, self.iface)
        self.configureCardButton.clicked.connect(self.cardDialog.show)

        self.outputDialogs = {}

        self.configChanged.connect(self.slotConfigChanged)

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

    def makeItemWidget(self, id_, title="", description="", type_=None, icon=None):
        """
            Makes an item widget having given properties.
        """
        widget = ItemWidget(self.outputList, id_, title, description, type_, icon)

        self.connect(widget, QtCore.SIGNAL("editClicked()"), self.slotOutputEdit)

        return widget

    def addItem(self, id_, name="", description="", icon=""):
        """
            Adds an item to list.
        """

        type_ = "user"

        # Build widget and widget item
        widget = self.makeItemWidget(id_, name, description, type_, kdeui.KIcon(icon))
        widgetItem = ItemListWidgetItem(self.outputList, widget)

        # Add to list
        self.outputList.setItemWidget(widgetItem, widget)

    def refreshOutputList(self):
        self.outputList.clear()

        for output in self.iface.getOutputs():
            desc, icon = OUTPUT_TYPES[output.outputType]
            self.addItem(output.name, output.name, desc, icon)

    def slotConfigChanged(self):
        print "*** Config changed"

    def slotOutputEdit(self):
        widget = self.sender()
        outputName = widget.getId()

        dlg = self.outputDialogs.get(outputName)

        if dlg is None:
            dlg = OutputDialog(self, self.iface, outputName)
            dlg.load()
            self.outputDialogs[outputName] = dlg

        dlg.show()

    def load(self):
        print "** load"

        self.newConfig = {}

        # Card info
        info = "<qt>%s<br><i>%s</i></qt>" % (self.iface.cardModel, self.iface.cardVendor)
        self.cardInfoLabel.setText(info)
        self.cardDialog.load()

        # Output dialogs
        for dlg in self.outputDialogs.values():
            dlg.load()

        # Output list
        self.refreshOutputList()

    def save(self):
        self.cardDialog.apply()
        self.iface.sync()

    def defaults(self):
        print "** defaults"
