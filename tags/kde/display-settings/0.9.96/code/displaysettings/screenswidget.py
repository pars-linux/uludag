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

import dbus

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
        self.scene.outputSelected.connect(self.slotUpdateOutputProperties)

        # Backend
        self.iface = Interface()
        self.iface.listenSignals(self.signalHandler)

        # Disable module if no packages provide backend or
        # no valid configuration is found
        if not self.checkBackend():
            parent.setDisabled(True)

        self.extendDisplays.toggled.connect(self.emitConfigChanged)
        self.detectButton.clicked.connect(self.slotDetectClicked)
        self.modeList.currentIndexChanged.connect(self.slotModeSelected)
        self.rateList.currentIndexChanged[int].connect(self.slotRateSelected)
        self.rotationList.currentIndexChanged[int].connect(self.slotRotationSelected)

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

        elif not self.iface.isReady():
            answer = kdeui.KMessageBox.questionYesNo(self, kdecore.i18n(
                "Cannot find a valid configuration. Display settings won't "
                "be enabled until you create a new configuration.\n"
                "Would you like to create a safe configuration now?"))
            if answer == kdeui.KMessageBox.Yes:
                try:
                    self.iface.safeConfig()
                    self.iface.readConfig()
                except dbus.DBusException, exception:
                    if "Comar.PolicyKit" in exception._dbus_error_name:
                        kdeui.KMessageBox.error(self, kdecore.i18n("Access denied."))
                    else:
                        kdeui.KMessageBox.error(self, str(exception))

            return self.iface.isReady()

        return True

    def signalHandler(self, package, signal, args):
        pass

    def detectOutputs(self, onlyConnected=False):
        self.iface.query()
        config = self.iface.getConfig()
        self._outputs = self.iface.getOutputs()
        currentOutputsDict = dict((x.name, x) for x in self._outputs)

        self._left = None
        self._right = None
        self._cloned = True
        self._modeLists = {}
        self._rateList = []
        self._modes = {}
        self._rates = {}
        self._rotations = {}

        connectedList = []

        for output in self._outputs:
            output.config = config.outputs.get(output.name)
            connected = output.connection == Output.Connected

            self._modeLists[output.name] = self.iface.getModes(output.name)
            if output.config is None:
                self._modes[output.name] = ""
                self._rates[output.name] = ""
                self._rotations[output.name] = "normal"
            else:
                self._modes[output.name] = output.config.mode
                self._rates[output.name] = output.config.refresh_rate
                self._rotations[output.name] = output.config.rotation

            if connected:
                connectedList.append(output)
            elif onlyConnected:
                continue

            if output.config is None or onlyConnected:
                if connected:
                    print "Trying to add %s as it is connected." % output.name
                    if self._left is None:
                        self._left = output
                    elif self._right is None:
                        self._right = output

                    w, h, x, y = self.iface.getGeometry(output)
                    if x or y:
                        self._cloned = False

            elif output.config.enabled:
                print "Trying to add %s as it is enabled by config." % output.name
                if output.config.right_of and \
                        output.config.right_of in currentOutputsDict:
                    self._right = output
                    self._left = currentOutputsDict[output.config.right_of]
                    self._cloned = False

                elif self._left is None:
                    self._left = output
                elif self._right is None:
                    self._right = output

        if self._left is None:
            if connectedList:
                self._left = connectedList[0]
            else:
                self._left = self._outputs[0]

    def populateOutputsMenu(self):
        menu = QtGui.QMenu(self)

        for output in self._outputs:
            if output.outputType == Output.UnknownOutput:
                text = output.name
            else:
                text = kdecore.i18nc(
                        "Shown in menus, lists, etc. "
                        "%1 = localized output type, "
                        "%2 = output name (LVDS, VGA, etc.)",
                        "%1 (%2)", output.getTypeString(), output.name)
            action = QtGui.QAction(text, self)
            action.setData(QtCore.QVariant(output.name))
            action.setCheckable(True)
            if output in (self._left, self._right):
                action.setChecked(True)
            menu.addAction(action)

        menu.triggered.connect(self.slotOutputToggled)
        self.outputsButton.setMenu(menu)

    def populateRateList(self):
        output = self._selectedOutput
        if output:
            currentMode = self._modes[output.name]

            self.rateList.currentIndexChanged.disconnect(self.slotRateSelected)
            self.rateList.clear()
            self.rateList.addItem(kdecore.i18n("Auto"))
            if currentMode:
                self._rateList = self.iface.getRates(output.name, currentMode)
                rates = map(lambda x: "%s Hz" % x, self._rateList)
                self.rateList.addItems(rates)
            self.rateList.currentIndexChanged.connect(self.slotRateSelected)

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

        output = self.scene.selectedOutput()
        self.slotUpdateOutputProperties(output)

    def slotDetectClicked(self):
        self.detectOutputs(onlyConnected=True)
        self.populateOutputsMenu()
        self.refreshOutputsView()
        self.slotUpdateOutputProperties(self._left)
        self.configChanged.emit()

    def slotUpdateOutputProperties(self, output):
        self._selectedOutput = output
        title = kdecore.i18n("Output Properties - %1", output.name)
        self.propertiesBox.setTitle(title)

        self.modeList.currentIndexChanged.disconnect(self.slotModeSelected)
        self.modeList.clear()
        self.modeList.addItem(kdecore.i18n("Auto"))
        self.modeList.addItems(self._modeLists[output.name])
        self.modeList.currentIndexChanged.connect(self.slotModeSelected)

        currentMode = self._modes[output.name]
        if currentMode:
            index = self.modeList.findText(currentMode)
            if index > -1:
                self.modeList.setCurrentIndex(index)
        else:
            self.modeList.setCurrentIndex(0)

        if self.rateList.currentIndex() < 0:
            self.populateRateList()

        currentRate = self._rates[output.name]
        if currentRate:
            index = self._rateList.index(currentRate)
            self.rateList.setCurrentIndex(index+1)
        else:
            self.rateList.setCurrentIndex(0)

        currentRotation = self._rotations[output.name]
        if currentRotation:
            opts = ("normal", "left", "inverted", "right")
            index = opts.index(currentRotation)
            self.rotationList.setCurrentIndex(index)
        else:
            self.rotationList.setCurrentIndex(0)

    def slotModeSelected(self, index):
        if index < 0:
            return

        output = self._selectedOutput
        if output:
            currentMode = str(self.modeList.currentText()) if index else ""
            self._modes[output.name] = currentMode
            self.populateRateList()
            self.configChanged.emit()

    def slotRateSelected(self, index):
        if index < 0:
            return

        output = self._selectedOutput
        if output:
            currentRate = self._rateList[index-1] if index else ""
            self._rates[output.name] = currentRate

            self.configChanged.emit()

    def slotRotationSelected(self, index):
        if index < 0:
            return

        output = self._selectedOutput
        if output:
            opts = ("normal", "left", "inverted", "right")
            self._rotations[output.name] = opts[index]

            self.configChanged.emit()

    def load(self):
        if not self.iface.isReady():
            return

        self.detectOutputs()
        self.populateOutputsMenu()
        self.refreshOutputsView()
        self.slotUpdateOutputProperties(self._left)

        self.extendDisplays.setChecked(not self._cloned)

    def save(self):
        try:
            for output in self._outputs:
                enabled = output in (self._left, self._right)
                self.iface.setOutput(output.name, enabled, False)
                if enabled:
                    self.iface.setMode(output.name,
                                        self._modes[output.name],
                                        self._rates[output.name])
                    self.iface.setRotation(output.name,
                                        self._rotations[output.name])

            left = self._left.name if self._left else None
            right = self._right.name if self._right else None
            cloned = not self.extendDisplays.isChecked()
            self.iface.setSimpleLayout(left, right, cloned)

            self.iface.sync()
            self.iface.applyNow()

            kdeui.KMessageBox.information(self,
                    kdecore.i18n("You must restart your X session for all the "
                                 "changes to take effect."),
                    QtCore.QString(),
                    "Screen Configuration Saved")

        except dbus.DBusException, exception:
            if "Comar.PolicyKit" in exception._dbus_error_name:
                kdeui.KMessageBox.error(self, kdecore.i18n("Access denied."))
            else:
                kdeui.KMessageBox.error(self, str(exception))

            QtCore.QTimer.singleShot(0, self.emitConfigChanged)

    def emitConfigChanged(self):
        self.configChanged.emit()

    def defaults(self):
        print "** defaults"
