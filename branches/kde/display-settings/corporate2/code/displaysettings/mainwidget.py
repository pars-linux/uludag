# -*- coding: utf-8 -*-
#
# Copyright (C) TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import sys

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

# zorg
from zorg import hwdata
from zorg.utils import run

# UI
from displaysettings.carddialog import VideoCardDialog
from displaysettings.outputdialog import OutputDialog
from displaysettings.entryview import EntryView
from displaysettings.ui.help import HelpDialog
from displaysettings.ui.mainview import mainWidget

# Backend
from displaysettings.backend import Interface

from displaysettings.device import Output
from displaysettings.utility import *


class MainWidget(mainWidget):
    def __init__(self, parent):
        mainWidget.__init__(self, parent)

        # hide for now
        self.buttonHelp.hide()

        # "Apply" button will be enabled when config changed
        self.buttonApply.setDisabled(True)

        # set button icons
        self.buttonCancel.setIconSet(getIconSet("cancel", KIcon.Small))
        self.buttonApply.setIconSet(getIconSet("ok", KIcon.Small))
        self.buttonHelp.setIconSet(getIconSet("help", KIcon.Small))
        # use reload icon for now. will be replaced with swap icon later.
        self.buttonSwap.setPixmap(getIcon("reload", KIcon.Toolbar))

        self.pixVideoCard.setPixmap(getIcon("video_card", KIcon.User))

        self.iconWide = getIconSet("monitor_wide", KIcon.User)
        self.iconNormal = getIconSet("monitor", KIcon.User)

        # output list
        self.outputList = EntryView(self.devicesPage)
        self.devicesPage.layout().addWidget(self.outputList)

        # Backend
        self.iface = Interface()

        # Disable module if no packages provide backend or
        # no valid configuration is found
        if self.checkBackend():
            self.textNotReady.hide()
        else:
            self.screenImage1.hide()
            self.screenImage2.hide()
            self.buttonSwap.hide()
            self.setDisabled(True)

        self.suggestDriver()

        self.cardDialog = VideoCardDialog(self, self.iface)
        self.outputDialogs = {}

        # set signals
        self.connect(self.screenImage1, SIGNAL("toggled(bool)"), self.slotOutputSelected)

        self.connect(self.buttonCancel, SIGNAL("clicked()"), qApp, SLOT("quit()"))
        self.connect(self.buttonApply, SIGNAL("clicked()"), self.save)
        self.connect(self.buttonHelp, SIGNAL("clicked()"), self.slotHelp)
        self.connect(self.buttonSwap, SIGNAL("clicked()"), self.slotSwap)

        self.connect(self.extendDisplays, SIGNAL("toggled(bool)"), self.emitConfigChanged)
        self.connect(self.detectButton, SIGNAL("clicked()"), self.slotDetectClicked)
        self.connect(self.modeList, SIGNAL("activated(int)"), self.slotModeSelected)
        self.connect(self.rateList, SIGNAL("activated(int)"), self.slotRateSelected)
        self.connect(self.rotationList, SIGNAL("activated(int)"), self.slotRotationSelected)

        self.connect(self.cardDialog, PYSIGNAL("configChanged"), self.emitConfigChanged)
        self.connect(self.configureCardButton, SIGNAL("clicked()"), self.cardDialog.show)

    def checkBackend(self):
        """
            Check if there are packages that provide required backend.
        """
        if not len(self.iface.getPackages()):
            KMessageBox.error(self, i18n(
                "There are no packages that provide backend for this "
                "application.\nPlease be sure that packages are installed "
                "and configured correctly."))
            return False

        elif not self.iface.isReady():
            answer = KMessageBox.questionYesNo(self, i18n(
                "Cannot find a valid configuration. Display settings won't "
                "be enabled until you create a new configuration.\n"
                "Would you like to create a safe configuration now?"))
            if answer == KMessageBox.Yes:
                try:
                    self.iface.safeConfig()
                    self.iface.readConfig()
                except dbus.DBusException, exception:
                    if "Comar.PolicyKit" in exception._dbus_error_name:
                        KMessageBox.error(self, i18n("Access denied."))
                    else:
                        KMessageBox.error(self, str(exception))

            return self.iface.isReady()

        return True

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

            if output.config is None:
                if connected:
                    print "Trying to add %s as it is connected and has no config." % output.name
                    if self._left is None:
                        self._left = output
                    elif self._right is None:
                        self._right = output

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

        self._selectedOutput = self._left

    def populateOutputsMenu(self):
        menu = QPopupMenu(self)
        menu.setCheckable(True)

        for i, output in enumerate(self._outputs):
            if output.outputType == Output.UnknownOutput:
                text = output.name
            else:
                text = i18n(
                        "Shown in menus, lists, etc. "
                        "%1 = localized output type, "
                        "%2 = output name (LVDS, VGA, etc.)",
                        "%1 (%2)").arg(output.getTypeString(), output.name)

            menu.insertItem(text, i)
            if output in (self._left, self._right):
                menu.setItemChecked(i, True)

        self.connect(menu, SIGNAL("activated(int)"), self.slotOutputToggled)
        self.outputsButton.setPopup(menu)

    def populateRateList(self):
        output = self._selectedOutput
        if output:
            currentMode = self._modes[output.name]

            self.rateList.clear()
            self.rateList.insertItem(i18n("Auto"))
            if currentMode:
                self._rateList = self.iface.getRates(output.name, currentMode)
                rates = map(lambda x: "%s Hz" % x, self._rateList)
                self.rateList.insertStrList(rates)

    def updateMenuStatus(self):
        menu = self.outputsButton.popup()
        for i, output in enumerate(self._outputs):
            if (self._left and self._left.name == output.name) \
                    or (self._right and self._right.name == output.name):

                menu.setItemChecked(i, True)
            else:
                menu.setItemChecked(i, False)

    def refreshOutputsView(self):
        scrLeft = self.screenImage1
        scrRight = self.screenImage2

        scrLeft.setIconSet(self.iconNormal)
        scrRight.setIconSet(self.iconNormal)

        scrLeft.setTextLabel(self._left.name)

        if self._right:
            scrRight.setTextLabel(self._right.name)
            scrRight.show()
            self.buttonSwap.show()
        else:
            scrRight.hide()
            self.buttonSwap.hide()

        if self._selectedOutput not in (self._left, self._right):
            self._selectedOutput = self._left

    def refreshOutputList(self):
        self.outputList.clear()

        for index, output in enumerate(self.iface.getOutputs()):
            self.outputList.add(index, output.name,
                                output.getTypeString(), output.getIcon(),
                                self.slotOutputEdit)

    def slotOutputToggled(self, id):
        output = self._outputs[id]
        menu = self.outputsButton.popup()

        # checked is the new toggle status.
        checked = not menu.isItemChecked(id)

        if checked:
            # Output activated.

            # If the right output is already selected,
            # shift left.
            if self._right:
                self._left = self._right

            # Place the activated output on right.
            self._right = output

        elif self._right is None:
            # All outputs deselected. Reject the toggle.
            checked = True

        elif output.name == self._left.name:
            # Left output deselected. Shift right output to the left.
            self._left = self._right
            if self._right:
                self._right = None

        else:
            # Right output is deselected.
            self._right = None

        # Update item for the new toggle status.
        menu.setItemChecked(id, checked)

        self.updateMenuStatus()
        self.refreshOutputsView()
        self.slotUpdateOutputProperties()
        self.emitConfigChanged()

    def slotDetectClicked(self):
        self.detectOutputs(onlyConnected=True)
        self.populateOutputsMenu()
        self.refreshOutputsView()
        self.slotUpdateOutputProperties()
        self.emitConfigChanged()

    def slotOutputSelected(self, leftSelected):
        output = self._left if leftSelected else self._right
        self._selectedOutput = output
        self.slotUpdateOutputProperties()

    def slotUpdateOutputProperties(self):
        output = self._selectedOutput
        modes = self._modeLists[output.name]
        title = i18n("Output Properties - %1").arg(output.name)
        self.propertiesBox.setTitle(title)

        self.modeList.clear()
        self.modeList.insertItem(i18n("Auto"))
        self.modeList.insertStrList(modes)

        currentMode = self._modes[output.name]
        if currentMode in modes:
            index = modes.index(currentMode) + 1 # +1 for "Auto"
            self.modeList.setCurrentItem(index)
            self.slotModeSelected(index)
        else:
            self.modeList.setCurrentItem(0)
            self.slotModeSelected(0)

        self.populateRateList()

        currentRate = self._rates[output.name]
        if currentRate in self._rateList:
            index = self._rateList.index(currentRate) + 1 # +1 for "Auto"
            self.rateList.setCurrentItem(index)
            self.slotRateSelected(index)
        else:
            self.rateList.setCurrentItem(0)
            self.slotRateSelected(0)

        currentRotation = self._rotations[output.name]
        if currentRotation:
            opts = ("normal", "left", "inverted", "right")
            index = opts.index(currentRotation)
            self.rotationList.setCurrentItem(index)
            self.slotRotationSelected(index)
        else:
            self.rotationList.setCurrentItem(0)
            self.slotRotationSelected(0)

    def slotModeSelected(self, index):
        if index < 0:
            return

        output = self._selectedOutput
        if output:
            currentMode = str(self.modeList.currentText()) if index else ""
            self._modes[output.name] = currentMode
            self.populateRateList()
            self.emitConfigChanged()

    def slotRateSelected(self, index):
        if index < 0:
            return

        output = self._selectedOutput
        if output:
            currentRate = self._rateList[index-1] if index else ""
            self._rates[output.name] = currentRate

            self.emitConfigChanged()

    def slotRotationSelected(self, index):
        if index < 0:
            return

        output = self._selectedOutput
        if output:
            opts = ("normal", "left", "inverted", "right")
            self._rotations[output.name] = opts[index]

            self.emitConfigChanged()

    def suggestDriver(self):
        config = self.iface.getConfig()
        dontAskAgainName = "Driver Suggestion"
        shouldBeShown, answer = KMessageBox.shouldBeShownYesNo(dontAskAgainName)
        if not shouldBeShown or not config:
            return

        preferredDriver = config.preferredDriver(installed=False)
        if preferredDriver is None or preferredDriver == self.iface.getDriver():
            return

        isInstalled = preferredDriver == config.preferredDriver()

        if isInstalled:
            msg = i18n("<qt>To get better performance, you may want to "
                            "use <b>%1</b> driver provided by hardware vendor. "
                            "Do you want to use this driver?</p></qt>") \
                            .arg(preferredDriver)
            answer = KMessageBox.questionYesNo(self, msg,
                        QString.null,
                        KStdGuiItem.yes(),
                        KStdGuiItem.no(),
                        dontAskAgainName)
            if answer == KMessageBox.Yes:
                self.cardDialog.setDriver(preferredDriver)

        else:
            package = hwdata.driverPackages.get(preferredDriver)
            if package is None:
                return
            msg = i18n("<qt>To get better performance, you may want to "
                            "use <b>%1</b> driver provided by hardware vendor. "
                            "To use it, you must install <b>%2</b> package and"
                            " choose <b>%1</b> from video card options.</qt>") \
                            .arg(preferredDriver, package)
            startPMButton = KGuiItem(i18n("Start Package Manager"),
                                            getIconSet("package-manager"))
            answer = KMessageBox.questionYesNo(self, msg,
                        QString.null,
                        startPMButton,
                        KStdGuiItem.cont(),
                        dontAskAgainName)
            if answer == KMessageBox.Yes:
                run("package-manager", "--show-mainwindow")


    def slotHelp(self):
        helpwin = HelpDialog()
        helpwin.exec_loop()

    def slotSwap(self):
        self._left, self._right = self._right, self._left

        self.refreshOutputsView()
        self.emitConfigChanged()

        if self.screenImage1.isOn():
            self.screenImage2.setOn(True)
        else:
            self.screenImage1.setOn(True)

    def slotOutputEdit(self, index):
        outputName = self._outputs[index].name

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
                outputName = item.title
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

        self.detectOutputs()
        self.populateOutputsMenu()
        self.refreshOutputsView()
        self.slotUpdateOutputProperties()

        self.extendDisplays.setChecked(not self._cloned)

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
        if not self.iface.isReady():
            return

        try:
            self.cardDialog.apply()
            for dlg in self.outputDialogs.values():
                dlg.apply()

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

            KMessageBox.information(self,
                    i18n("You must restart your X session for all the "
                         "changes to take effect."),
                    QString.null,
                    "Screen Configuration Saved")

            self.buttonApply.setDisabled(True)

        except dbus.DBusException, exception:
            if "Comar.PolicyKit" in exception._dbus_error_name:
                KMessageBox.error(self, i18n("Access denied."))
            else:
                KMessageBox.error(self, str(exception))

            QTimer.singleShot(0, self.emitConfigChanged)

    def emitConfigChanged(self):
        self.emit(PYSIGNAL("configChanged"), ())
        self.buttonApply.setEnabled(True)

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    self.mainwidget = MainWidget(self)
    toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
    toplayout.addWidget(self.mainwidget)
    self.aboutus = KAboutApplication(self)

class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue(mod_app)
        self.config = KConfig(mod_app)
        self.setButtons(KCModule.Apply)
        self.aboutdata = AboutData()
        attachMainWidget(self)

        self.mainwidget.layout().setMargin(0)
        self.mainwidget.frameDialogButtons.hide()

        self.connect(self.mainwidget, PYSIGNAL("configChanged"), self.changed)

        self.load()

    def load(self):
        self.mainwidget.load()

    def save(self):
        self.mainwidget.save()

    def aboutData(self):
        return self.aboutdata


# KCModule factory
def create_display_settings(parent, name):
    global kapp

    kapp = KApplication.kApplication()
    if not dbus.get_default_main_loop():
        DBusQtMainLoop(set_as_default=True)
    return Module(parent, name)


# Standalone
def main():
    global kapp

    about = AboutData()
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()

    if not KUniqueApplication.start():
        print i18n('Display Settings module is already started!')
        return

    kapp = KUniqueApplication(True, True, True)
    win = QDialog()

    DBusQtMainLoop(set_as_default=True)

    win.setCaption(i18n('Display Settings'))
    win.setMinimumSize(400, 300)
    #win.resize(500, 300)
    attachMainWidget(win)
    win.setIcon(getIconSet("randr").pixmap(QIconSet.Small, QIconSet.Normal))
    kapp.setMainWidget(win)

    QTimer.singleShot(0, win.mainwidget.load)

    sys.exit(win.exec_loop())


if __name__ == '__main__':
    main()
