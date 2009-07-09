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
        self.scene.outputsChanged.connect(self.slotChangeDisplays)

        # Backend
        self.iface = Interface()
        self.iface.listenSignals(self.signalHandler)

        # Fail if no packages provide backend
        self.checkBackend()

        self.detectButton.clicked.connect(self.slotDetectClicked)

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

    def detectOutputs(self):
        config = self.iface.getConfig()
        self._outputs = self.iface.getOutputs()
        currentOutputsDict = dict((x.name, x) for x in self._outputs)

        self._left = None
        self._right = None
        self._cloned = True

        for output in self._outputs:
            output.config = config.outputs.get(output.name)

            if output.connection == Output.Connected:
                if output.config is None:
                    if self._left is None:
                        self._left = output
                    elif self._right is None:
                        self._right = output
                elif output.config.enabled:
                    if output.config.right_of and \
                            output.config.right_of in currentOutputsDict:
                        self._right = output
                        self._left = currentOutputsDict[output.config.right_of]
                        self._cloned = False

    def populateOutputsMenu(self):
        menu = QtGui.QMenu(self)

        for output in self._outputs:
            text = kdecore.i18nc(
                    "Shown in menus, lists, etc. "
                    "%1 = localized output type, "
                    "%2 = output name (LVDS, VGA, etc.)",
                    "%1 (%2)", output.getTypeString(), output.name)
            action = QtGui.QAction(text, self)
            action.setIcon(output.getIcon())
            action.setData(QtCore.QVariant(output.name))
            action.setCheckable(True)
            if output in (self._left, self._right):
                action.setChecked(True)
            menu.addAction(action)

        menu.triggered.connect(self.slotOutputToggled)
        self.outputsButton.setMenu(menu)

    def updateMenuStatus(self):
        for act in self.outputsButton.menu().actions():
            name = str(act.data().toString())
            if (self._left and self._left.name == name) \
                or (self._right and self._right.name == name):
                act.setChecked(True)
            else:
                act.setChecked(False)

    def refreshOutputsView(self):
        self.scene.setOutputs(self._outputs, self._left, self._right)

    def slotOutputToggled(self, action):
        name = str(action.data().toString())
        checked = action.isChecked()
        currentOutputsDict = dict((x.name, x) for x in self._outputs)
        output = currentOutputsDict[name]

        if checked:
            if self._right:
                self._left = self._right

            self._right = output
        elif self._right is None:
            action.setChecked(True)
            return
        elif output.name == self._left.name:
            self._left = self._right
            if self._right:
                self._right = None
        else:
            self._right = None

        self.updateMenuStatus()
        self.refreshOutputsView()
        self.configChanged.emit()

    def slotChangeDisplays(self, left, right):
        currentOutputsDict = dict((x.name, x) for x in self._outputs)
        left = str(left)
        right = str(right)
        if left:
            self._left = currentOutputsDict.get(left)

        if right:
            self._right = currentOutputsDict.get(right)

        self.updateMenuStatus()
        self.refreshOutputsView()
        self.configChanged.emit()

    def slotOutputSelected(self, action):
        print action.data().toString(), "selected"

    def slotDetectClicked(self):
        self.load()
        self.configChanged.emit()

    def load(self):
        self.detectOutputs()
        self.populateOutputsMenu()
        self.refreshOutputsView()

        self.clonedCheckBox.setChecked(self._cloned)

    def save(self):
        pass

    def defaults(self):
        print "** defaults"
