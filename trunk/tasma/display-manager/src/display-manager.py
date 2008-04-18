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
        self.checkBoxTrueColor.setChecked(self.displayConfiguration.true_color)

        self.screenNames = { "1":"Primary Screen", "2": "Secondary Screen" }

        # set button icons
        loader = KGlobal.iconLoader()
        self.buttonCancel.setIconSet(QIconSet(loader.loadIcon("cancel", KIcon.Small)))
        self.buttonApply.setIconSet(QIconSet(loader.loadIcon("ok", KIcon.Small)))
        self.buttonHelp.setIconSet(QIconSet(loader.loadIcon("help", KIcon.Small)))

        icon = getIconSet("display-manager.png", KIcon.User)
        self.screenImage1.setIconSet(icon)
        self.screenImage2.setIconSet(icon)

        self.getCurrentConf()

        #set signals
        self.selectedScreen = 1

        self.connect(self.screenImage1, SIGNAL("toggled(bool)"), self.getSelectedScreen)
        self.connect(self.screenImage2, SIGNAL("toggled(bool)"), self.getSelectedScreen)

        self.connect(self.screenImage1, SIGNAL("toggled(bool)"), self.switchBetweenScreens)
        self.connect(self.screenImage2, SIGNAL("toggled(bool)"), self.switchBetweenScreens)

        self.connect(self.checkBoxDualMode, SIGNAL("toggled(bool)"), self.enableExtendedOption)

        self.connect(self.comboBoxOutput, SIGNAL("activated(int)"), self.setSelectedModes)
        self.connect(self.comboBoxResolution, SIGNAL("activated(int)"), self.setSelectedModes)

        self.connect(self.comboBoxOutput, SIGNAL("activated(int)"), self.getResolutions)

        self.connect(self.buttonCancel, SIGNAL("clicked()"),qApp, SLOT("quit()"))
        self.connect(self.buttonApply, SIGNAL("clicked()"),self.slotApply)
        self.connect(self.buttonHelp, SIGNAL("clicked()"),self.slotHelp)


        self.getCurrentConf()

        for output in self.screenOutputs:
            self.comboBoxOutput.insertItem(output)
            for resolution in self.screenModes[output]:
                self.comboBoxResolution.insertItem(resolution)

        self.getResolutions()

    def getCurrentConf(self):
        # returns a dict of outputs: resolutions.
        self.screenModes = self.displayConfiguration.modes

        # returns a list of outputs
        self.screenOutputs = self.displayConfiguration.outputs

        # returns a dict of current outputs: resolutions
        self.currentModes = self.displayConfiguration.current_modes

    def setSelectedModes(self):
        curOut =  str(self.comboBoxOutput.currentText())
        curRes = str(self.comboBoxResolution.currentText())

        if self.selectedScreen == 1:
            self.displayConfiguration.primaryScr = curOut
        else:
            self.displayConfiguration.secondaryScr = curOut

        self.displayConfiguration.current_modes[curOut] = curRes

    def getSelectedScreen(self):
        """Gets selected screen and sets groupbox name as screen's name"""

        self.selectedScreen = str(self.screenGroup.selected().textLabel())
        self.groupBoxScreens.setTitle(self.screenNames[self.selectedScreen])

    def enableExtendedOption(self):
        """Enables <Extended> option checkbox if <Dual Mode> selected"""

        if self.checkBoxDualMode.isChecked():
            self.checkBoxExtended.setEnabled(1)
        else:
            self.checkBoxExtended.setEnabled(0)

    def switchBetweenScreens(self):
        if self.selectedScreen == 1:
            self.currentOutput = str(self.displayConfiguration.primaryScr)
            self.comboBoxOutput.setCurrentText(self.currentOutput)
            self.comboBoxResolution.setCurrentText(self.currentModes[self.currentOutput])
        elif self.selectedScreen == 2:
            self.currentOutput = "TV"
            #self.currentOutput = str(self.displayConfiguration.secondaryScr)
            self.comboBoxOutput.setCurrentText(self.currentOutput)
            self.comboBoxResolution.setCurrentText(self.currentModes[self.currentOutput])

    def getResolutions(self, hede = None):
        """Gets resolutions due to selected output"""

        self.comboBoxResolution.clear() #it seems duplicatesEnabled doesn't work x(
        self.currentOutput = str(self.comboBoxOutput.currentText())

        for resolution in self.screenModes[self.currentOutput]:
            self.comboBoxResolution.insertItem(resolution)

        self.comboBoxResolution.setCurrentText(self.currentModes[self.currentOutput])

    def slotApply(self):
        pass

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
