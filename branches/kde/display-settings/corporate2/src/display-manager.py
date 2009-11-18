#!/usr/bin/python
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

import dbus
from dbus.mainloop.qt3 import DBusQtMainLoop
from zorg.utils import idsQuery, run
from zorg.consts import package_sep

# UI
import helpdialog
import dm_mainview
import driverdialog
import monitordialog

# Backend
from backend import Interface

# zorg
from zorg.hwdata import driverPackages
from zorg.utils import run

from zorg import hwdata
from utility import *

mod_name = 'Display Settings'
mod_app = 'display-settings'
mod_version = '0.5.80'

def AboutData():
    return KAboutData(
        mod_app,
        mod_name,
        mod_version,
        I18N_NOOP('Display Settings'),
        KAboutData.License_GPL,
        '(C) UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )

class MonitorDialog(monitordialog.monitorDialog):
    def __init__(self, parent):
        monitordialog.monitorDialog.__init__(self, parent)

        self.groupBoxDetails.hide()
        self.pushButtonOk.setEnabled(False)

        genericMonitors, vendorMonitors = hwdata.getMonitorInfos()

        crtText = i18n("CRT Monitor")
        lcdText = i18n("LCD Monitor")

        genericMonitors[crtText] = genericMonitors["Generic CRT Display"]
        genericMonitors[lcdText] = genericMonitors["Generic LCD Display"]
        del genericMonitors["Generic CRT Display"]
        del genericMonitors["Generic LCD Display"]

        vendors = {i18n("Standard Monitors"): genericMonitors, i18n("Vendors"): vendorMonitors}

        # hide listview caption.
        self.listViewMonitors.header().hide()

        for eachVendor in vendors:
            root = KListViewItem(self.listViewMonitors, "parent", "parent","parent")
            root.setText(0, eachVendor)
            self.listViewMonitors.setOpen(root,False)

            for eachSubVendor in vendors[eachVendor]:
                item = KListViewItem(root, "parent", "parent","parent")
                item.setText(0, eachSubVendor)
                self.listViewMonitors.setOpen(item,False)

                for eachModel in vendors[eachVendor][eachSubVendor]:
                    subitem = KListViewItem(item, eachModel["model"], eachSubVendor, eachModel["hsync"], eachModel["vref"])

        self.connect(self.pushButtonCancel, SIGNAL("clicked()"), self.reject)
        self.connect(self.pushButtonOk,     SIGNAL("clicked()"), self.accept)
        self.connect(self.listViewMonitors, SIGNAL("selectionChanged()"), self.getSelectedMonitor)
        self.connect(self.checkBoxPlugPlay, SIGNAL("toggled(bool)"), self.listViewMonitors.setDisabled)
        self.connect(self.checkBoxPlugPlay, SIGNAL("toggled(bool)"), self.groupBoxDetails.setDisabled)
        self.connect(self.checkBoxPlugPlay, SIGNAL("toggled(bool)"), self.slotPNP)

    def slotPNP(self, checked):
        if checked:
            self.pushButtonOk.setEnabled(True)
        else:
            self.getSelectedMonitor()

    def getSelectedMonitor(self):
        if self.listViewMonitors.currentItem().key(1,0) == "parent":
            self.groupBoxDetails.hide()
            self.pushButtonOk.setDisabled(True)
        else:
            self.groupBoxDetails.show()
            self.pushButtonOk.setEnabled(True)
            self.lineEditHorizontal.setText(self.listViewMonitors.currentItem().key(2, 0))
            self.lineEditVertical.setText(self.listViewMonitors.currentItem().key(3, 0))

class DriverItem(KListViewItem):
    def __init__(self, parent, name, desc):
        QListViewItem.__init__(self, parent)

        self.name = name
        self.desc = desc
        self.setText(0, name)
        self.setText(1, desc)

class CardDialog(driverdialog.VideoCard):
    def __init__(self, parent):
        driverdialog.VideoCard.__init__(self, parent)

        current = None
        dc = parent.dconfig
        self.extraDrivers = []

        availableDrivers = hwdata.getAvailableDriverNames()
        compatibleDrivers = hwdata.getCompatibleDriverNames(dc.card_vendor_id, dc.card_product_id)

        curdrv = dc._info.driver
        if dc._info.package != "xorg-video":
            curdrv += package_sep + dc._info.package

        for drv in compatibleDrivers:
            item = DriverItem(self.listViewVideoCard, drv, hwdata.drivers.get(drv, ""))

            if drv == curdrv:
                current = item

        for drv in availableDrivers:
            if not drv in compatibleDrivers:
                item = DriverItem(self.listViewVideoCard, drv, hwdata.drivers.get(drv, ""))
                self.extraDrivers.append(item)

                if drv == curdrv:
                    current = item

        self.showExtraDrivers(False)

        if current:
            self.listViewVideoCard.setCurrentItem(current)

        self.listViewVideoCard.setFocus()

        self.connect(self.pushButtonCancel, SIGNAL("clicked()"), self.reject)
        self.connect(self.pushButtonOk, SIGNAL("clicked()"), self.accept),
        self.connect(self.checkBoxAllDrivers, SIGNAL("toggled(bool)"), self.showExtraDrivers)

    def showExtraDrivers(self, show):
        for drv in self.extraDrivers:
            drv.setVisible(show)

    def accept(self):
        availableDrivers = hwdata.getAvailableDriverNames()
        item = self.listViewVideoCard.currentItem()

        if item.name in availableDrivers:
            QDialog.accept(self)
        else:
            if package_sep in item.name:
                package = item.name.split(package_sep, 1)[1]
            else:
                package = "xorg-video"

            msg = i18n("<qt>The driver you selected is not installed on your system. In order to use this driver, you must install <b>%1</b> package.</qt>").arg(package)
            buttonStartPM = KGuiItem(i18n("Start Package Manager"), getIconSet("package-manager"))
            answer = KMessageBox.warningYesNo(self, msg, QString.null, buttonStartPM, KStdGuiItem.cancel())

            if answer == KMessageBox.Yes:
                run("package-manager", "--show-mainwindow")

class MainWidget(dm_mainview.mainWidget):
    def __init__(self, parent):
        dm_mainview.mainWidget.__init__(self, parent)

        # hide for now
        self.buttonHelp.hide()

        self.screenNames = { 1: i18n("Primary Screen"), 2: i18n("Secondary Screen") }

        # set button icons
        self.buttonCancel.setIconSet(getIconSet("cancel", KIcon.Small))
        self.buttonApply.setIconSet(getIconSet("ok", KIcon.Small))
        self.buttonHelp.setIconSet(getIconSet("help", KIcon.Small))
        self.pixVideoCard.setPixmap(getIconSet("video_card", KIcon.User).pixmap(QIconSet.Automatic, QIconSet.Normal))
        # use reload icon for now. will be replaced with swap icon later.
        self.buttonSwap.setPixmap( getIconSet("reload", KIcon.Toolbar).pixmap(QIconSet.Automatic, QIconSet.Normal))

        self.iconWide = getIconSet("monitor_wide", KIcon.User)
        self.iconNormal = getIconSet("monitor", KIcon.User)

        # set signals
        self.connect(self.screenImage1, SIGNAL("toggled(bool)"), self.getSelectedScreen)

        #self.connect(self.checkBoxDualMode, SIGNAL("toggled(bool)"), self.enableExtendedOption)
        #self.connect(self.checkBoxDualMode, SIGNAL("toggled(bool)"), self.buttonGroupDualModes, SLOT("setEnabled(bool)"))
        #self.connect(self.radioBoxExtended, SIGNAL("toggled(bool)"), self.setDualModeOptions)

        #self.connect(self.comboBoxOutput, SIGNAL("activated(int)"), self.setSelectedOutput)
        #self.connect(self.comboBoxResolution, SIGNAL("activated(int)"), self.setSelectedMode)

        #self.connect(self.buttonDetectDisplays, SIGNAL("clicked()"), self.detectDisplays)
        #self.connect(self.buttonIdentifyDisplays, SIGNAL("clicked()"), self.identifyDisplays)

        self.connect(self.buttonCancel, SIGNAL("clicked()"), qApp, SLOT("quit()"))
        self.connect(self.buttonApply, SIGNAL("clicked()"), self.slotApply)
        self.connect(self.buttonHelp, SIGNAL("clicked()"), self.slotHelp)
        self.connect(self.buttonSwap, SIGNAL("clicked()"), self.slotSwap)

        #self.connect(self.buttonVideoCard, SIGNAL("clicked()"), self.slotCardSettings)
        #self.connect(self.buttonMonitor1, SIGNAL("clicked()"), lambda: self.slotSelectMonitor(1))
        #self.connect(self.buttonMonitor2, SIGNAL("clicked()"), lambda: self.slotSelectMonitor(2))


        # Backend
        self.iface = Interface()

        #self.reset()
        self.suggestDriver()

    def reset(self):
        import displayconfig
        self.dconfig = displayconfig.DisplayConfig()

        if self.dconfig._info:
            self.textNotReady.hide()
        else:
            self.screenImage1.hide()
            self.screenImage2.hide()
            self.buttonSwap.hide()
            self.setDisabled(True)
            return

        self.checkBoxTrueColor.setChecked(self.dconfig.true_color)
        if len(self.dconfig.depths) == 1:
            self.checkBoxTrueColor.setDisabled(True)

        self.selectedScreen = 1

        self.getCardInfo()
        self.getCurrentConf()
        self.updateWidgets()

    def detectDisplays(self):
        self.dconfig.detect()
        self.getCurrentConf()
        self.updateWidgets()

    def updateWidgets(self):
        self.comboBoxOutput.clear()
        for output in self.screenOutputs:
            self.comboBoxOutput.insertItem(getOutputName(output))
            for resolution in self.screenModes[output]:
                self.comboBoxResolution.insertItem(resolution)

        # disable dual mode if there's only one output
        if len(self.dconfig.outputs) <= 1:
            self.checkBoxDualMode.setDisabled(True)
            self.groupBoxSecondaryScreen.hide()
            self.buttonMonitor2.setDisabled(True)
        else:
            self.checkBoxDualMode.setEnabled(True)
            self.groupBoxSecondaryScreen.show()
            self.buttonMonitor2.setEnabled(True)

        self.getMonitorInfo()
        self.switchBetweenScreens()
        self.setIconbyResolution(1)

        if self.dconfig.desktop_setup == "single":
            self.checkBoxDualMode.setChecked(False)
            self.buttonGroupDualModes.setDisabled(True)
            self.enableExtendedOption(False)
        else:
            if self.dconfig.desktop_setup == "horizontal":
                self.radioBoxExtended.setChecked(True)
            else:
                self.radioBoxCloned.setChecked(True)
            self.checkBoxDualMode.setChecked(True)
            self.setIconbyResolution(2)

    def identifyDisplays(self):
        nod =  QApplication.desktop().numScreens()
        self.identifiers = []

        for i in range(nod):
            si = QLabel(QString.number(i+1), QApplication.desktop(), "Identify Displays", Qt.WX11BypassWM)

            fnt = QFont(KGlobalSettings.generalFont())
            fnt.setPixelSize(100)
            si.setFont(fnt)
            si.setFrameStyle(QFrame.Panel)
            si.setFrameShadow(QFrame.Plain)
            si.setAlignment(Qt.AlignCenter)

            screenCenter = QPoint(QApplication.desktop().screenGeometry(i).center())
            targetGeometry = QRect(QPoint(0,0), si.sizeHint())
            targetGeometry.moveCenter(screenCenter)
            si.setGeometry(targetGeometry)
            self.identifiers.append(si)
            si.show()

        QTimer.singleShot(1500, self.hideIdentifiers)

    def hideIdentifiers(self):
        for identifier in self.identifiers:
            identifier.hide()

    def duplicateOutputs(self):
        message = i18n("This output is already used by other screen.\nDo you want to swap between them?")
        answer = KMessageBox.warningYesNo(self, message)
        if answer == KMessageBox.Yes:
            self.slotSwap()
        else:
            self.comboBoxOutput.setCurrentText(getOutputName(self.currentOutput))

    def setIconbyResolution(self, screenId = None):
        if not screenId:
            screenId = self.selectedScreen

        if screenId == 1:
            screenImage = self.screenImage1
            pixMonitor = self.pixMonitor1
            resolution = self.currentModes[self.dconfig.primaryScr]
        else:
            screenImage = self.screenImage2
            pixMonitor = self.pixMonitor2
            resolution = self.currentModes[self.dconfig.secondaryScr]

        if "x" not in resolution:
            x, y = 4, 3
        else:
            x, y = resolution.split("x")

        if float(x)/float(y) >= 1.6:
            icon = self.iconWide
        else:
            icon = self.iconNormal

        screenImage.setIconSet(icon)
        pixMonitor.setPixmap(icon.pixmap(QIconSet.Automatic, QIconSet.Normal))

    def getCurrentConf(self):
        # returns a dict of outputs: resolutions.
        self.screenModes = self.dconfig.modes

        # returns a list of outputs
        self.screenOutputs = self.dconfig.outputs

        # returns a dict of current outputs: resolutions
        self.currentModes = self.dconfig.current_modes

    def setSelectedOutput(self):
        curOut = self.screenOutputs[self.comboBoxOutput.currentItem()]

        if self.selectedScreen == 1:
            if curOut == self.dconfig.secondaryScr:
                if self.dconfig.desktop_setup != "single":
                    self.duplicateOutputs()
                    return
                else:
                    self.dconfig.secondaryScr = None

            self.dconfig.primaryScr = curOut
        else:
            if curOut == self.dconfig.primaryScr:
                self.duplicateOutputs()
            else:
                self.dconfig.secondaryScr = curOut

        self.getResolutions()
        self.setIconbyResolution()
        self.getMonitorInfo()

    def setDualModeOptions(self, extended):
        if extended:
            self.dconfig.desktop_setup = "horizontal"
        else:
            self.dconfig.desktop_setup = "clone"

    def setSelectedMode(self):
        curOut = self.screenOutputs[self.comboBoxOutput.currentItem()]
        curRes = str(self.comboBoxResolution.currentText())
        self.dconfig.current_modes[curOut] = curRes
        self.setIconbyResolution()

    def getSelectedScreen(self, primarySelected):
        """Gets selected screen and sets groupbox name as screen's name"""

        if primarySelected:
            self.selectedScreen = 1
        else:
            self.selectedScreen = 2

        self.groupBoxScreens.setTitle(self.screenNames[self.selectedScreen])
        self.switchBetweenScreens()

    def enableExtendedOption(self, checked):
        """Enables <Extended> option checkbox if <Dual Mode> selected"""

        if checked:
            if self.dconfig.secondaryScr is None:
                for output in self.dconfig.outputs:
                    if output != self.dconfig.primaryScr:
                        self.dconfig.secondaryScr = output
                        break

            self.setIconbyResolution(2)
            self.screenImage2.show()
            self.groupBoxSecondaryScreen.show()
            self.buttonSwap.show()
            self.setDualModeOptions(self.radioBoxExtended.isChecked())
            self.getMonitorInfo()
        else:
            self.screenImage2.hide()
            self.screenImage1.setState(QButton.On)
            self.groupBoxSecondaryScreen.hide()
            self.buttonSwap.hide()
            self.dconfig.desktop_setup = "single"

    def switchBetweenScreens(self):
        if self.selectedScreen == 1:
            self.currentOutput = self.dconfig.primaryScr
        elif self.selectedScreen == 2:
            self.currentOutput = self.dconfig.secondaryScr

        self.comboBoxOutput.setCurrentText(getOutputName(self.currentOutput))
        self.getResolutions()

    def getResolutions(self):
        """Gets resolutions due to selected output"""

        self.comboBoxResolution.clear() #it seems duplicatesEnabled doesn't work x(

        self.currentOutput = self.screenOutputs[self.comboBoxOutput.currentItem()]

        for resolution in self.screenModes[self.currentOutput]:
            self.comboBoxResolution.insertItem(resolution)

        self.comboBoxResolution.setCurrentText(self.currentModes[self.currentOutput])

    def getCardInfo(self):
        vendorName, boardName = idsQuery(self.dconfig.card_vendor_id, self.dconfig.card_product_id)
        self.textCardName.setText("%s\n%s" % (boardName, vendorName))
        self.textDriver.setText( i18n("Driver: %1").arg(self.dconfig.driverName()))

    def getMonitorInfo(self):
        msgpnp = i18n("Plug and Play Monitor")
        monitors = self.dconfig.monitors

        def writeInfo(out, label):
            if monitors.has_key(out):
                label.setText(u"%s\n%s" % (monitors[out].model, monitors[out].vendor))
            else:
                label.setText(msgpnp)

        writeInfo(self.dconfig.primaryScr, self.textMonitor1)

        if self.dconfig.desktop_setup != "single":
            writeInfo(self.dconfig.secondaryScr, self.textMonitor2)

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
            package = driverPackages.get(preferredDriver)
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


    def slotApply(self):
        self.dconfig.true_color = self.checkBoxTrueColor.isChecked()

        kapp.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.dconfig.apply()
        kapp.restoreOverrideCursor()

    def slotCardSettings(self):
        dlg = CardDialog(self)
        if dlg.exec_loop() == QDialog.Accepted:
            item = dlg.listViewVideoCard.currentItem()
            self.dconfig.changeDriver(item.name)
            self.getCardInfo()
            self.checkBoxTrueColor.setEnabled(True)

    def slotSelectMonitor(self, nscr):
        dlg = MonitorDialog(self)
        if dlg.exec_loop() == QDialog.Accepted:
            if nscr == 1:
                out = self.dconfig.primaryScr
            else:
                out = self.dconfig.secondaryScr

            if dlg.checkBoxPlugPlay.isChecked():
                if self.dconfig.monitors.has_key(out):
                    del self.dconfig.monitors[out]
            else:
                from zorg.probe import Monitor

                item = dlg.listViewMonitors.currentItem()
                mon = Monitor()
                mon.model = str(item.key(0, 0))
                mon.vendor = str(item.key(1, 0))
                mon.hsync = str(item.key(2, 0)).replace(" ", "")
                mon.vref = str(item.key(3, 0)).replace(" ", "")

                self.dconfig.monitors[out] = mon

            from displayconfig import all_modes
            for output in self.dconfig.outputs:
                if self.dconfig.monitors.has_key(output):
                    self.dconfig.modes[output] = all_modes

            self.updateWidgets()

    def slotHelp(self):
        helpwin = helpdialog.HelpDialog()
        helpwin.exec_loop()

    def slotSwap(self):
        self.dconfig.primaryScr, self.dconfig.secondaryScr = self.dconfig.secondaryScr, self.dconfig.primaryScr
        self.updateWidgets()

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

        if self.mainwidget.dconfig._info:
            QTimer.singleShot(0, self.changed)

    def load(self):
        if self.mainwidget.dconfig._info:
            self.mainwidget.reset()
            QTimer.singleShot(0, self.changed)

    def save(self):
        if self.mainwidget.dconfig._info:
            self.mainwidget.slotApply()
            QTimer.singleShot(0, self.changed)

    def aboutData(self):
        return self.aboutdata


# KCModule factory
def create_display_manager(parent, name):
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

    # PolicyKit Agent requires window ID
    from displayconfig import comlink
    comlink.winID = win.winId()

    win.setCaption(i18n('Display Settings'))
    win.setMinimumSize(400, 300)
    #win.resize(500, 300)
    attachMainWidget(win)
    win.setIcon(getIconSet("randr").pixmap(QIconSet.Small, QIconSet.Normal))
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())


if __name__ == '__main__':
    main()
