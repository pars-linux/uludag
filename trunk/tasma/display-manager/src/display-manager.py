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

        # set button icons
        loader = KGlobal.iconLoader()
        self.buttonCancel.setIconSet(QIconSet(loader.loadIcon("cancel", KIcon.Small)))
        self.buttonApply.setIconSet(QIconSet(loader.loadIcon("ok", KIcon.Small)))
        self.buttonHelp.setIconSet(QIconSet(loader.loadIcon("help", KIcon.Small)))

        icon = getIconSet("screen.png", KIcon.User)
        self.screenImage1.setIconSet(icon)
        self.screenImage2.setIconSet(icon)

        # returns a dict of outputs: resolutions.
        """
        {'LVDS': ['1280x800', '1280x768', '1024x768', '800x600', '640x480'],
        'S-video': ['800x600', '640x480']}
        """
        #self.screenModes = self.displayConfiguration.modes
        self.screenModes = {'LVDS': ['1280x800', '1280x768', '1024x768', '800x600', '640x480'], 'S-video': ['800x600', '640x480']}

        # returns a list of outputs
        #['VGA-0', 'LVDS', 'S-video']
        #self.screenOutputs = self.displayConfiguration.outputs

        self.screenOutputs = ['LVDS', 'S-video']

        # returns a dict of current outputs: resolutions
        #self.currentModes = self.displayConfiguration.current_modes
        self.currentModes = {'LVDS': '1280x800', 'S-video': '800x600', 'VGA-0': '800x600'}

        self.selectedScreen = 0
        self.connect(self.screenImage1, SIGNAL("toggled(bool)"), self.getSelectedScreen)
        self.connect(self.screenImage2, SIGNAL("toggled(bool)"), self.getSelectedScreen)
        self.connect(self.checkBoxDualMode, SIGNAL("toggled(bool)"), self.enableExtendedOption)
        self.connect(self.comboBoxOutput, SIGNAL("activated(int)"), self.setResolutions)

        for output in self.screenOutputs:
            self.comboBoxOutput.insertItem(output)

        self.setResolutions()

    def getSelectedScreen(self):
        """Gets selected screen and sets groupbox name as screen's name"""

        self.selectedScreen =  self.screenGroup.selected()
        self.groupBoxScreens.setTitle(self.selectedScreen.textLabel())

    def enableExtendedOption(self):
        """Enables <Extended> option checkbox if <Dual Mode> selected"""

        if self.checkBoxDualMode.isChecked():
            self.checkBoxExtended.setEnabled(1)
        else:
            self.checkBoxExtended.setEnabled(0)

    def setResolutions(self):
        """Sets resolutions due to selected output"""

        self.currentOutput =  str(self.comboBoxOutput.currentText())
        self.comboBoxResolution.clear() #it seems duplicatesEnabled doesn't work x(

        for resolution in self.screenModes[self.currentOutput]:
            self.comboBoxResolution.insertItem(resolution)

        self.comboBoxResolution.setCurrentText(self.currentModes[self.currentOutput])

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
