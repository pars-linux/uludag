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
from displaysettings.ui_screens import Ui_screensWidget
from displaysettings.scene import DisplayScene

# Backend
from displaysettings.backend import Interface

# Config
#from displaysettings.config import

from displaysettings.device import Output

class MainWidget(QtGui.QWidget, Ui_screensWidget):

    configChanged = QtCore.pyqtSignal()

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

        self.populateOutputsMenu()

    def checkBackend(self):
        """
            Check if there are packages that provide required backend.
        """
        if not len(self.iface.getPackages()):
            kdeui.KMessageBox.error(self, kdecore.i18n(
                "There are no packages that provide backend for this "
                "application.\nPlease be sure that packages are installed "
                "and configured correctly."))
            return False
        return True

    def signalHandler(self, package, signal, args):
        pass

    def populateOutputsMenu(self):
        menu = QtGui.QMenu(self)
        actionGroup = QtGui.QActionGroup(self)
        actionGroup.triggered.connect(self.slotOutputSelected)

        for output in self.iface.getOutputs():
            text = kdecore.i18nc(
                    "Shown in menus, lists, etc. "
                    "%1 = localized output type, "
                    "%2 = output name (LVDS, VGA, etc.)",
                    "%1 (%2)", output.getTypeString(), output.name)
            action = QtGui.QAction(text, self)
            action.setIcon(output.getIcon())
            action.setData(QtCore.QVariant(output.name))
            action.setCheckable(True)
            action.setActionGroup(actionGroup)
            if output.connection == Output.Connected:
                action.setChecked(True)
            menu.addAction(action)

        self.outputsButton.setMenu(menu)

    def slotOutputSelected(self, action):
        print action.data().toString(), "selected"

    def load(self):
        pass

    def save(self):
        pass

    def defaults(self):
        print "** defaults"
