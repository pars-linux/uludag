#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
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

import helpdialog
import dm_mainview
import displayconfig
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
        '(C) 2007 UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )

class MainWidget(dm_mainview.mainWidget):
    def __init__(self, parent):
        dm_mainview.mainWidget.__init__(self, parent)

        self.displayConfiguration = displayconfig.DisplayConfig()

        if not self.displayConfiguration._randr12:
            message = i18n("Sorry, Display Manager currently does not support your driver.")
            QMessageBox.critical(self, i18n("No Support"), message, QMessageBox.Ok, QMessageBox.NoButton)
            sys.exit()

        self.checkBoxTrueColor.setChecked(self.displayConfiguration.true_color)

        self.screenNames = { "1":"Primary Screen", "2": "Secondary Screen" }

        #set button icons
        self.buttonCancel.setIconSet(getIconSet("cancel", KIcon.Small))
        self.buttonApply.setIconSet(getIconSet("ok", KIcon.Small))
        self.buttonHelp.setIconSet(getIconSet("help", KIcon.Small))

        self.iconWide = getIconSet("display_manager_wide", KIcon.User)
        self.iconNormal = getIconSet("display_manager_normal", KIcon.User)

        self.getCurrentConf()

        #set signals
        self.selectedScreen = "1"

        self.connect(self.screenImage1, SIGNAL("toggled(bool)"), self.getSelectedScreen)
        self.connect(self.screenImage2, SIGNAL("toggled(bool)"), self.getSelectedScreen)

        self.connect(self.screenImage1, SIGNAL("toggled(bool)"), self.switchBetweenScreens)
        self.connect(self.screenImage2, SIGNAL("toggled(bool)"), self.switchBetweenScreens)

        self.connect(self.checkBoxDualMode, SIGNAL("toggled(bool)"), self.enableExtendedOption)
        self.connect(self.checkBoxExtended, SIGNAL("toggled(bool)"), self.setExtendedOption)

        self.connect(self.comboBoxOutput, SIGNAL("activated(int)"), self.setSelectedOutput)
        self.connect(self.comboBoxResolution, SIGNAL("activated(int)"), self.setSelectedMode)

        self.connect(self.buttonIdentifyDisplays, SIGNAL("clicked()"), self.identifyDisplays)

        self.connect(self.buttonCancel, SIGNAL("clicked()"),qApp, SLOT("quit()"))
        self.connect(self.buttonApply, SIGNAL("clicked()"),self.slotApply)
        self.connect(self.buttonHelp, SIGNAL("clicked()"),self.slotHelp)

        for output in self.screenOutputs:
            self.comboBoxOutput.insertItem(output)
            for resolution in self.screenModes[output]:
                self.comboBoxResolution.insertItem(resolution)

        # remove later.
        self.displayConfiguration.secondaryScr = "VGA"

        self.getResolutions(1)
        self.setIconbyResolution()

        if not self.currentDualMode == "single":
            if self.currentDualMode == "horizontal":
                self.checkBoxDualMode.setChecked(1)
                self.checkBoxExtended.setChecked(1)
            else:
                self.checkBoxDualMode.setChecked(1)
        else:
            self.screenImage2.hide()

    def duplicateOutputs(self):
        message = i18n("Sorry, but you can use one device for each output.\nTry to select another output.")
        QMessageBox.warning(self, i18n("Duplicate Outputs!"), message, QMessageBox.Ok, QMessageBox.NoButton)

    def setIconbyResolution(self, resolution = None, screenId = None):
        if resolution == None:
            resolution = self.currentModes[self.currentOutput]

        x, y = resolution.split("x")

        icon = self.iconWide if float(x)/float(y) >= 1.6 else self.iconNormal

        if screenId == 2 or self.selectedScreen == "2":
            self.screenImage2.setIconSet(icon)
        else:
            self.screenImage1.setIconSet(icon)

    def getCurrentConf(self):
        # returns a dict of outputs: resolutions.
        self.screenModes = self.displayConfiguration.modes

        # returns a list of outputs
        self.screenOutputs = self.displayConfiguration.outputs

        # returns a dict of current outputs: resolutions
        self.currentModes = self.displayConfiguration.current_modes

        # returns dual mode status
        self.currentDualMode = self.displayConfiguration.desktop_setup

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

    def setExtendedOption(self):
        if self.checkBoxExtended.isChecked():
            self.displayConfiguration.desktop_setup = "horizontal"
        else:
            self.displayConfiguration.desktop_setup = self.currentDualMode
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

    def enableExtendedOption(self):
        """Enables <Extended> option checkbox if <Dual Mode> selected"""

        if self.checkBoxDualMode.isChecked():
            self.setIconbyResolution(str(self.currentModes[self.displayConfiguration.secondaryScr]),2)
            self.screenImage2.show()
            self.checkBoxExtended.setEnabled(1)
            self.displayConfiguration.desktop_setup = "clone"
        else:
            self.screenImage2.hide()
            self.screenImage1.setState(QButton.On)
            self.checkBoxExtended.setEnabled(0)
            self.displayConfiguration.desktop_setup = self.currentDualMode

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

    def identifyDisplays(self):
        # what's the fucking dcop call for that!?
        pass

    def slotApply(self):
        self.displayConfiguration.apply()

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

    def aboutData(self):
        return self.aboutdata


# KCModule factory
def create_display_manager(parent, name):
    global kapp

    kapp = KApplication.kApplication()
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
    win.setCaption(i18n('Display Manager'))
    win.setMinimumSize(400, 300)
    #win.resize(500, 300)
    attachMainWidget(win)
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())


if __name__ == '__main__':
    main()
