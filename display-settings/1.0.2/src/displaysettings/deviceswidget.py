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

# zorg
from zorg.hwdata import driverPackages
from zorg.utils import run

# UI
from displaysettings.ui_devices import Ui_devicesWidget

# Backend
from displaysettings.backend import Interface

from displaysettings.item import ItemListWidgetItem, ItemWidget
from displaysettings.carddialog import VideoCardDialog
from displaysettings.outputdialog import OutputDialog

from displaysettings.device import Output

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

        # Disable module if no packages provide backend or
        # no valid configuration is found
        if not self.checkBackend():
            parent.setDisabled(True)


        self.cardDialog = VideoCardDialog(self, self.iface)
        self.configureCardButton.clicked.connect(self.cardDialog.show)

        self.outputDialogs = {}
        self.firstLoad = True

        self.configChanged.connect(self.slotConfigChanged)

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

    def suggestDriver(self):
        config = self.iface.getConfig()
        dontAskAgainName = "Driver Suggestion"
        shouldBeShown, answer = kdeui.KMessageBox.shouldBeShownYesNo(dontAskAgainName)
        if not shouldBeShown or not config:
            return

        preferredDriver = config.preferredDriver(installed=False)
        if preferredDriver is None or preferredDriver == self.iface.getDriver():
            return

        isInstalled = preferredDriver == config.preferredDriver()

        if isInstalled:
            msg = kdecore.i18n("<qt>To get better performance, you may want to "
                            "use <b>%1</b> driver provided by hardware vendor. "
                            "Do you want to use this driver?</p></qt>",
                            preferredDriver)
            answer = kdeui.KMessageBox.questionYesNo(self, msg,
                        QtCore.QString(),
                        kdeui.KStandardGuiItem.yes(),
                        kdeui.KStandardGuiItem.no(),
                        dontAskAgainName)
            if answer == kdeui.KMessageBox.Yes:
                self.cardDialog.setDriver(preferredDriver)

        else:
            pm = str(kdecore.KStandardDirs.findExe("package-manager"))
            if not pm:
                return

            package = driverPackages.get(preferredDriver)
            if package is None:
                return
            msg = kdecore.i18n("<qt>To get better performance, you may want to "
                            "use <b>%1</b> driver provided by hardware vendor. "
                            "To use it, you must install <b>%2</b> package and"
                            " choose <b>%1</b> from video card options.</qt>",
                            preferredDriver, package)
            startPMButton = kdeui.KGuiItem(kdecore.i18n("Start Package Manager"),
                                            kdeui.KIcon("package-manager"))
            answer = kdeui.KMessageBox.questionYesNo(self, msg,
                        QtCore.QString(),
                        startPMButton,
                        kdeui.KStandardGuiItem.cont(),
                        dontAskAgainName)
            if answer == kdeui.KMessageBox.Yes:
                run(pm, "--show-mainwindow")

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
            self.addItem(output.name, output.name,
                         output.getTypeString(), output.getIcon())

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

        enableIgnoreButton = True
        if not dlg.ignored:
            config = self.iface.getConfig()
            count = self.outputList.count()

            def isIgnored(name):
                d = self.outputDialogs.get(name)
                if d is None:
                    output = config.outputs.get(name)
                    if output is None:
                        return False
                    else:
                        return output.ignored
                else:
                    return d.ignored

            for i in range(count):
                item = self.outputList.item(i)
                outputName = item.getId()
                if outputName == dlg.outputName:
                    continue

                if not isIgnored(outputName):
                    break
            else:
                enableIgnoreButton = False

        dlg.ignoreOutputCheck.setEnabled(enableIgnoreButton)
        dlg.show()

    def load(self):
        if not self.iface.isReady():
            return

        self.iface.query()

        # Card info
        info = "<qt>%s<br><i>%s</i></qt>" % (self.iface.cardModel, self.iface.cardVendor)
        self.cardInfoLabel.setText(info)
        self.cardDialog.load()

        # Output dialogs
        for dlg in self.outputDialogs.values():
            dlg.load()

        # Output list
        self.refreshOutputList()

        if self.firstLoad:
            self.firstLoad = False
            self.suggestDriver()

    def save(self):
        try:
            self.cardDialog.apply()
            for dlg in self.outputDialogs.values():
                dlg.apply()
            self.iface.sync()

            kdeui.KMessageBox.information(self,
                    kdecore.i18n("You must restart your X session for the "
                                 "changes to take effect."),
                    QtCore.QString(),
                    "Display Device Configuration Saved")

            # XXX really needed?
            self.load()

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
