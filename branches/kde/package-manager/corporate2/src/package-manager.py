#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# System
import sys

# PyQt/PyKDE
from qt import *
from kdecore import *
from kdeui import *
from kio import *
import kdedesigner

# Local imports
import PmDcop
from PmLogging import logger
import Globals
from MainWidget import *
import Settings

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

def handleException(exception, value, tb):
    logger.error("".join(traceback.format_exception(exception, value, tb)))

description = I18N_NOOP("GUI for PiSi package manager")
version = "1.4.0"

def AboutData():
    global version,description

    about_data = KAboutData("package-manager", I18N_NOOP("Package Manager"), version, description, KAboutData.License_GPL,
                            "(C) 2005, 2006, 2007, 2008 UEKAE/TÜBİTAK", None, None)

    about_data.addAuthor("Gökçen Eraslan", I18N_NOOP("Developer and Current Maintainer"), "gokcen@pardus.org.tr")
    about_data.addAuthor("Faik Uygur", I18N_NOOP("Developer"), "faik@pardus.org.tr")
    about_data.addAuthor("İsmail Dönmez", I18N_NOOP("Original Author"), "ismail@pardus.org.tr")
    about_data.addAuthor("Gökmen Göksel",I18N_NOOP("CSS/JS Meister"), "gokmen@pardus.org.tr")
    about_data.addAuthor("Görkem Çetin",I18N_NOOP("GUI Design & Usability"), "gorkem@pardus.org.tr")
    about_data.addCredit("Ahmet Aygün", I18N_NOOP("Authors of PiSi API"), "ahmet@pardusman.org")
    about_data.addCredit("A. Murat Eren", I18N_NOOP("Authors of PiSi API"), "meren@pardus.org.tr")
    about_data.addCredit("Bahadır Kandemir", I18N_NOOP("Authors of PiSi API"), "bahadir@pardus.org.tr")
    about_data.addCredit("Barış Metin", I18N_NOOP("Authors of PiSi API"), "baris@pardus.org.tr")
    about_data.addCredit("Furkan Duman", I18N_NOOP("Authors of PiSi API"), "coderlord@gmail.com")
    about_data.addCredit("Gürer Özen", I18N_NOOP("Authors of PiSi API"), "gurer@pardus.org.tr")
    about_data.addCredit("Onur Küçük", I18N_NOOP("Authors of PiSi API"), "onur@pardus.org.tr")
    about_data.addCredit("S. Çağlar Onur", I18N_NOOP("Authors of PiSi API"), "caglar@pardus.org.tr")

    return about_data

class MainApplication(KMainWindow):
    def __init__(self,parent=None,name=None):
        KMainWindow.__init__(self,parent,name)
        self.statusLabel = QLabel("", self.statusBar())
        self.statusBar().addWidget(self.statusLabel)
        self.statusBar().setSizeGripEnabled(True)
        self.setCaption(i18n("Package Manager"))
        self.aboutus = KAboutApplication(self)
        self.helpWidget = None

        self.mainwidget = MainApplicationWidget(self)
        self.setCentralWidget(self.mainwidget)

        self.setupMenu()
        self.setupGUI(KMainWindow.ToolBar|KMainWindow.Keys|KMainWindow.StatusBar|KMainWindow.Save|KMainWindow.Create)
        self.fixHelpMenu()
        self.toolBar().setIconText(KToolBar.IconTextRight)
        self.dcop = PmDcop.PmDcop(self)

        self.tray = Tray.Tray(self)
        if self.mainwidget.settings.getBoolValue(Settings.general, "SystemTray"):
            if self.mainwidget.settings.getBoolValue(Settings.general, "UpdateCheck"):
                Globals.debug("Update check option is set.")
                interval = self.mainwidget.settings.getNumValue(Settings.general, "UpdateCheckInterval")
                Globals.debug("Update check will start in %s minute(s)" % interval)
                self.tray.updateInterval(interval)
            self.tray.show()

        self.connect(self.tray, SIGNAL("quitSelected()"), self.slotQuit)
        self.connect(kapp, SIGNAL("shutDown()"), self.slotQuit)

    def updateStatusBarText(self, text):
        self.statusLabel.setText(text)
        self.statusLabel.setAlignment(Qt.AlignHCenter)

    def queryClose(self):
        if self.mainwidget.settings.getBoolValue(Settings.general, "SystemTray") and not kapp.sessionSaving():
            Globals.debug("Minimizing to system tray.")
            self.hide()
            return False
        return True

    def queryExit(self):
        return not self.mainwidget.command.inProgress()

    def slotQuit(self):
        if self.mainwidget.command.inProgress():
            return
        # Don't know why but without this, after exiting package-manager, crash occurs. This may be a workaround or a PyQt bug.
        self.mainwidget.deleteLater()
        Globals.debug("package-manager is quiting.")
        kapp.quit()

    def setupMenu(self):
        fileMenu = QPopupMenu(self)
        settingsMenu = QPopupMenu(self)

        self.quitAction = KStdAction.quit(self.slotQuit, self.actionCollection())
        self.settingsAction = KStdAction.preferences(self.mainwidget.showPreferences, self.actionCollection())
        self.showInstalledAction = KToggleAction(i18n("Show Installed Packages"),"package",KShortcut.null(),
                                                 self.mainwidget.removeState,self.actionCollection(),
                                                 "show_installed_action")
        self.showNewAction = KToggleAction(i18n("Show New Packages"),"edit_add",KShortcut.null(),
                                           self.mainwidget.installState,self.actionCollection(),"show_new_action")
        self.showUpgradeAction = KToggleAction(i18n("Show Upgradable Packages"),"reload",KShortcut.null(),
                                               self.mainwidget.updateCheck ,self.actionCollection(),"show_upgradable_action")

        self.showNewAction.plug(fileMenu)
        self.showNewAction.setChecked(True)
        self.showInstalledAction.plug(fileMenu)
        self.showUpgradeAction.plug(fileMenu)
        self.quitAction.plug(fileMenu)
        self.settingsAction.plug(settingsMenu)
        self.setHelpMenuEnabled(False)

        self.menuBar().insertItem(i18n ("&File"), fileMenu,0,0)
        self.menuBar().insertItem(i18n("&Settings"), settingsMenu,1,1)

    def showHelp(self):
        Globals.debug("Showing help window.")
        helpwin = HelpDialog.HelpDialog(self, HelpDialog.MAINAPP)
        helpwin.show()

    def fixHelpMenu(self):
        helpMenu = self.helpMenu()
        helpMenu.removeItem(KHelpMenu.menuHelpContents)
        helpMenu.insertItem(i18n("Package Manager Help"),
                            KHelpMenu.menuHelpContents,
                            0)
        helpMenu.setAccel(Qt.Key_F1, KHelpMenu.menuHelpContents)
        helpMenu.connectItem(KHelpMenu.menuHelpContents, self.showHelp)
        self.menuBar().insertItem(i18n("&Help"), helpMenu)

def main():
    global kapp
    global packageToInstall

    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)
    KCmdLineArgs.addCmdLineOptions ([("install <package>", I18N_NOOP("Package to install")),
                                     ("show-mainwindow", I18N_NOOP("Show main window on startup")),
                                     ("debug", I18N_NOOP("Show debug output"))])

    if not KUniqueApplication.start():
        print i18n("Package Manager is already running!")
        return

    kapp = KUniqueApplication(True, True, True)

    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    debug = False

    args = KCmdLineArgs.parsedArgs()

    # pass references to Globals module, so they can be reached everywhere when needed
    Globals.init(kapp, debug)
    Globals.debug("package-manager started.")

    if args.isSet("install"):
        packageToInstall = args.getOption("install")
        Globals.setPackageToInstall(packageToInstall)
    else:
        packageToInstall = None

    if args.isSet("debug"):
         debug = True

    myapp = MainApplication()
    if not myapp.mainwidget.settings.getBoolValue(Settings.general, "SystemTray"):
        Globals.debug("SystemTray option is not set, showing main window.")
        myapp.show()
    else:
        if args.isSet("show-mainwindow"):
            Globals.debug("--show-mainwindow option is set. Showing main window.")
            myapp.show()

    kapp.setMainWidget(myapp)

    sys.excepthook = handleException

    LocaleData.setSystemLocale()

    sys.exit(kapp.exec_loop())

if __name__ == "__main__":
    main()
