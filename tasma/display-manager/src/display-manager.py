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
from pardus.deviceutils import idsQuery
from zorg.consts import package_sep

import helpdialog
import dm_mainview
import driverdialog
import monitordialog
import hwdata
from utility import *

mod_name = 'Display Manager'
mod_app = 'display-manager'
mod_version = '0.1'

def AboutData():
    return KAboutData(
        mod_app,
        mod_name,
        mod_version,
        I18N_NOOP('Display Manager'),
        KAboutData.License_GPL,
        '(C) UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )

class DriverItem(KListViewItem):
    def __init__(self, parent, name, desc):
        QListViewItem.__init__(self, parent)

        self.name = name
        self.desc = desc
        self.setText(0, name)
        self.setText(1, desc)

class MonitorDialog(monitordialog.monitorDialog):
    def __init__(self, parent):
        monitordialog.monitorDialog.__init__(self, parent)
        self.groupBoxDetails.hide()
        # get a dict of monitor.db like:
        # vendor["Siemens"] = {'Siemens Nixdorf': [{'eisa_id': '','hsync': '','is_dpms': '','model': '','vref': ''}}

        allMonitorInfos = hwdata.getMonitorInfos()

        # hide listview caption.
        self.listViewMonitors.header().hide()

        for eachVendor in allMonitorInfos.keys():
            item = KListViewItem(self.listViewMonitors, "parent", "parent","parent")
            item.setText(0, eachVendor)
            self.listViewMonitors.setOpen(item,False)

            for eachModel in allMonitorInfos[eachVendor]:
                subitem = KListViewItem(item, eachModel["eisa_id"], eachModel["hsync"], eachModel["vref"], eachModel["is_dpms"])
                subitem.setText(0, eachModel["model"])

        self.connect(self.pushButtonCancel, SIGNAL("clicked()"), self.reject)
        self.connect(self.pushButtonOk, SIGNAL("clicked()"), self.accept)
        self.listViewMonitors.connect(self.listViewMonitors, SIGNAL("selectionChanged()"), parent.getSelectedMonitor)

class CardDialog(driverdialog.VideoCard):
    def __init__(self, parent):
        driverdialog.VideoCard.__init__(self, parent)

        # hide for now
        self.checkBoxProbe.hide()

        current = None
        dc = parent.displayConfiguration
        self.compatibleDriverList = {}
        self.allDriversList = []

        self.availableDrivers = hwdata.getAvailableDrivers()

        curdrv = dc._info.driver
        if dc._info.package != "xorg-video":
            curdrv += package_sep + dc._info.package

        for drv in hwdata.getCompatibleDriverNames(dc.card_vendor_id, dc.card_product_id):
            item = DriverItem(self.listViewVideoCard, drv, hwdata.drivers.get(drv, ""))
            self.compatibleDriverList[drv] =  item

            if drv == curdrv:
                current = item

        for d in self.availableDrivers:
            if not d in self.compatibleDriverList.keys():
                item = DriverItem(self.listViewVideoCard, d, self.availableDrivers[d])
                self.allDriversList.append(item)

                if d == curdrv:
                    current = item

        self.hideExtraDrivers()

        if current:
            self.listViewVideoCard.setCurrentItem(current)

        self.listViewVideoCard.setFocus()

        self.connect(self.pushButtonCancel, SIGNAL("clicked()"), self.reject)
        self.connect(self.pushButtonOk, SIGNAL("clicked()"), self.accept),
        self.connect(self.checkBoxAllDrivers, SIGNAL("toggled(bool)"), self.listExtraDrivers)

    def showExtraDrivers(self):
        for d in self.allDriversList:
            d.setVisible(True)

    def hideExtraDrivers(self):
        for d in self.allDriversList:
            d.setVisible(False)

    def listExtraDrivers(self):
        if self.checkBoxAllDrivers.isChecked():
            self.showExtraDrivers()
        else:
            self.hideExtraDrivers()

class MainWidget(dm_mainview.mainWidget):
    def __init__(self, parent):
        dm_mainview.mainWidget.__init__(self, parent)

        # hide for now
        self.buttonHelp.hide()
        self.buttonDetectDisplays.setDisabled(True)
        self.buttonMonitor2.setDisabled(True)

        import displayconfig
        self.displayConfiguration = displayconfig.DisplayConfig()

        self.checkBoxTrueColor.setChecked(self.displayConfiguration.true_color)
        if len(self.displayConfiguration.depths) == 1:
            self.checkBoxTrueColor.setDisabled(True)

        self.screenNames = { "1": i18n("Primary Screen"), "2": i18n("Secondary Screen") }

        #set button icons
        self.buttonCancel.setIconSet(getIconSet("cancel", KIcon.Small))
        self.buttonApply.setIconSet(getIconSet("ok", KIcon.Small))
        self.buttonHelp.setIconSet(getIconSet("help", KIcon.Small))

        self.pixVideoCard.setPixmap(getIconSet("video_card", KIcon.User).pixmap(QIconSet.Automatic, QIconSet.Normal))

        self.iconWide = getIconSet("monitor_wide", KIcon.User)
        self.iconNormal = getIconSet("monitor", KIcon.User)

        self.getCurrentConf()

        #set signals
        self.selectedScreen = "1"

        self.connect(self.screenImage1, SIGNAL("toggled(bool)"), self.getSelectedScreen)
        self.connect(self.screenImage2, SIGNAL("toggled(bool)"), self.getSelectedScreen)

        self.connect(self.screenImage1, SIGNAL("toggled(bool)"), self.switchBetweenScreens)
        self.connect(self.screenImage2, SIGNAL("toggled(bool)"), self.switchBetweenScreens)

        self.connect(self.checkBoxDualMode, SIGNAL("toggled(bool)"), self.enableExtendedOption)
        self.connect(self.checkBoxDualMode, SIGNAL("toggled(bool)"), self.buttonGroupDualModes, SLOT("setEnabled(bool)"))
        self.connect(self.radioBoxExtended, SIGNAL("toggled(bool)"), self.setDualModeOptions)

        self.connect(self.comboBoxOutput, SIGNAL("activated(int)"), self.setSelectedOutput)
        self.connect(self.comboBoxResolution, SIGNAL("activated(int)"), self.setSelectedMode)

        self.connect(self.buttonIdentifyDisplays, SIGNAL("clicked()"), self.identifyDisplays)

        self.connect(self.buttonCancel, SIGNAL("clicked()"),qApp, SLOT("quit()"))
        self.connect(self.buttonApply, SIGNAL("clicked()"),self.slotApply)
        self.connect(self.buttonHelp, SIGNAL("clicked()"),self.slotHelp)

        self.connect(self.buttonVideoCard, SIGNAL("clicked()"), self.slotCardSettings)
        self.connect(self.buttonMonitor1, SIGNAL("clicked()"), self.slotSelectMonitor)

        self.mntr =  MonitorDialog(self)

        for output in self.screenOutputs:
            self.comboBoxOutput.insertItem(output)
            for resolution in self.screenModes[output]:
                self.comboBoxResolution.insertItem(resolution)

        # disable dual mode if there's only one output
        if len(self.displayConfiguration.outputs) <= 1:
            self.checkBoxDualMode.setEnabled(0)
            self.groupBoxSecondaryScreen.hide()

        self.getCardInfo()
        self.getMonitorInfo()

        self.getResolutions(1)
        self.setIconbyResolution()

        if self.displayConfiguration.desktop_setup == "single":
            self.checkBoxDualMode.setChecked(False)
            self.buttonGroupDualModes.setDisabled(True)
            self.enableExtendedOption(False)
        else:
            if self.displayConfiguration.desktop_setup == "horizontal":
                self.radioBoxExtended.setChecked(True)
            else:
                self.radioBoxCloned.setChecked(True)
            self.checkBoxDualMode.setChecked(True)

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

    def getSelectedMonitor(self):
        if self.mntr.listViewMonitors.currentItem().key(1,0) == "parent":
            self.mntr.groupBoxDetails.hide()
        else:
            self.mntr.groupBoxDetails.show()
            self.mntr.lineEditHorizontal.setText(self.mntr.listViewMonitors.currentItem().key(1, 0))
            self.mntr.lineEditVertical.setText(self.mntr.listViewMonitors.currentItem().key(2, 0))

    def duplicateOutputs(self):
        message = i18n("Sorry, but you can use one device for each output.\nTry to select another output.")
        QMessageBox.warning(self, i18n("Duplicate Outputs!"), message, QMessageBox.Ok, QMessageBox.NoButton)

    def setIconbyResolution(self, resolution = None, screenId = None):
        if resolution == None:
            resolution = self.currentModes[self.currentOutput]

        x, y = resolution.split("x")

        if float(x)/float(y) >= 1.6:
            icon = self.iconWide
        else:
            icon = self.iconNormal

        if screenId == 2 or self.selectedScreen == "2":
            self.screenImage2.setIconSet(icon)
            self.pixMonitor2.setPixmap(icon.pixmap(QIconSet.Automatic, QIconSet.Normal))
        else:
            self.screenImage1.setIconSet(icon)
            self.pixMonitor1.setPixmap(icon.pixmap(QIconSet.Automatic, QIconSet.Normal))

    def getCurrentConf(self):
        # returns a dict of outputs: resolutions.
        self.screenModes = self.displayConfiguration.modes

        # returns a list of outputs
        self.screenOutputs = self.displayConfiguration.outputs

        # returns a dict of current outputs: resolutions
        self.currentModes = self.displayConfiguration.current_modes

    def setSelectedOutput(self):
        curOut =  str(self.comboBoxOutput.currentText())

        if self.selectedScreen == "1":
            if curOut == self.displayConfiguration.secondaryScr:
                self.duplicateOutputs()
            else:
                self.displayConfiguration.primaryScr = curOut
        else:
            if curOut == self.displayConfiguration.primaryScr:
                self.duplicateOutputs()
            else:
                self.displayConfiguration.secondaryScr = curOut

        self.getResolutions()

    def setDualModeOptions(self, extended):
        if extended:
            self.displayConfiguration.desktop_setup = "horizontal"
        else:
            self.displayConfiguration.desktop_setup = "clone"

    def setSelectedMode(self):
        curOut =  str(self.comboBoxOutput.currentText())
        curRes = str(self.comboBoxResolution.currentText())
        self.displayConfiguration.current_modes[curOut] = curRes
        self.setIconbyResolution(curRes)

    def getSelectedScreen(self):
        """Gets selected screen and sets groupbox name as screen's name"""

        self.selectedScreen = str(self.screenGroup.selected().textLabel())
        self.groupBoxScreens.setTitle(self.screenNames[self.selectedScreen])

    def enableExtendedOption(self, checked):
        """Enables <Extended> option checkbox if <Dual Mode> selected"""

        if checked:
            if self.displayConfiguration.secondaryScr is None:
                for output in self.displayConfiguration.outputs:
                    if output != self.displayConfiguration.primaryScr:
                        self.displayConfiguration.secondaryScr = output
                        break

            self.setIconbyResolution(str(self.currentModes[self.displayConfiguration.secondaryScr]),2)
            self.screenImage2.show()
            self.groupBoxSecondaryScreen.show()
            self.setDualModeOptions(self.radioBoxExtended.isChecked())
        else:
            self.screenImage2.hide()
            self.screenImage1.setState(QButton.On)
            self.groupBoxSecondaryScreen.hide()
            self.displayConfiguration.desktop_setup = "single"

    def switchBetweenScreens(self):
        if self.selectedScreen == "1":
            self.currentOutput = str(self.displayConfiguration.primaryScr)
            self.comboBoxOutput.setCurrentText(self.currentOutput)
        elif self.selectedScreen == "2":
            self.currentOutput = str(self.displayConfiguration.secondaryScr)
            self.comboBoxOutput.setCurrentText(self.currentOutput)
            self.comboBoxResolution.setCurrentText(self.currentModes[self.currentOutput])

        self.getResolutions()

    def getResolutions(self, firstBoot = None):
        """Gets resolutions due to selected output"""

        self.comboBoxResolution.clear() #it seems duplicatesEnabled doesn't work x(

        if firstBoot == 1:
            self.currentOutput = self.displayConfiguration.primaryScr
            self.comboBoxOutput.setCurrentText(self.currentOutput)
        else:
            self.currentOutput = str(self.comboBoxOutput.currentText())

        for resolution in self.screenModes[self.currentOutput]:
            self.comboBoxResolution.insertItem(resolution)

        self.comboBoxResolution.setCurrentText(self.currentModes[self.currentOutput])

    def getCardInfo(self):
        cardName = idsQuery("/usr/share/misc/pci.ids", self.displayConfiguration.card_vendor_id, self.displayConfiguration.card_product_id)
        self.textCardName.setText(cardName)
        self.textDriver.setText( i18n("Driver: %s" % self.displayConfiguration._info.driver))

    def getMonitorInfo(self):
        msgpnp = i18n("Plug and Play Monitor")

        if self.displayConfiguration._info.monitors.has_key(self.displayConfiguration.primaryScr):
            self.textMonitor1.setText("Manually selected monitor")
        else:
            self.textMonitor1.setText(msgpnp)

        if self.displayConfiguration.desktop_setup != "single":
            if self.displayConfiguration._info.monitors.has_key(self.displayConfiguration.secondaryScr):
                self.textMonitor2.setText("Manually selected monitor")
            else:
                self.textMonitor2.setText(msgpnp)

    def slotApply(self):
        self.displayConfiguration.true_color = self.checkBoxTrueColor.isChecked()

        kapp.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.displayConfiguration.apply()
        kapp.restoreOverrideCursor()

    def slotCardSettings(self):
        dlg = CardDialog(self)
        if dlg.exec_loop() == QDialog.Accepted:
            item = dlg.listViewVideoCard.currentItem()
            self.displayConfiguration.changeDriver(item.name)

    def slotSelectMonitor(self):
        self.mntr.exec_loop()

    def slotHelp(self):
        helpwin = helpdialog.HelpDialog()
        helpwin.exec_loop()

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
        self.setButtons(0)
        self.aboutdata = AboutData()
        attachMainWidget(self)
        self.mainwidget.buttonCancel.hide()

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
        print i18n('Display Manager is already started!')
        return

    kapp = KUniqueApplication(True, True, True)
    win = QDialog()

    DBusQtMainLoop(set_as_default=True)

    # PolicyKit Agent requires window ID
    from displayconfig import comlink
    comlink.winID = win.winId()

    win.setCaption(i18n('Display Manager'))
    win.setMinimumSize(400, 300)
    #win.resize(500, 300)
    attachMainWidget(win)
    win.setIcon(getIconSet("randr").pixmap(QIconSet.Small, QIconSet.Normal))
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())


if __name__ == '__main__':
    main()
