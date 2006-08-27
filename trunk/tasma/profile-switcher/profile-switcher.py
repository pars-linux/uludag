#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

""" Standart Python Modules """
import sys

""" Gettext Support """
import gettext
__trans = gettext.translation("profiler-switcher", fallback=True)
_  =  __trans.ugettext

""" PyQt and PyKDE Modules """
from qt import QToolTip, QTimer, QSize, QPixmap, QIconSet, QProgressBar, SIGNAL
from kdecore import KIcon, KIconLoader, KCmdLineArgs, KAboutData, KUniqueApplication, KGlobal
from kdeui import KSystemTray, KPopupMenu, KAboutDialog, KMessageBox

from comarInterface import *

class SystemTray(KSystemTray):
    def __init__(self, *args):
        self.ID = {}

        apply(KSystemTray.__init__, (self,) + args)

        """ comarInterface instance """
        self.comarInterface = comarInterface()

        """ get connections """
        self.wirelessConnections = self.comarInterface.listWirelessConnections()
        self.wiredConnections = self.comarInterface.listWiredConnections()

        """ Create tray icon Loader """
        self.setPixmap(self.loadIcon("network"))

        """ list all connections into Connections menu """
        # FIXME: Show IP Addresses when comarAPI supports
        if self.wirelessConnections.__len__() > 0:
            wirelessMenu = KPopupMenu(self.contextMenu())
            for entry in self.wirelessConnections:
                entry = unicode(entry)
                if self.comarInterface.isWirelessConnectionActive(entry):
                    self.ID[wirelessMenu.insertItem(self.loadIconSet("remote"), entry)] = entry
                else:
                    self.ID[wirelessMenu.insertItem(self.loadIconSet("stop"), entry)] = entry
            self.contextMenu().insertItem(self.loadIconSet("remote"), _("Wireless Profiles"), wirelessMenu)
            self.connect(wirelessMenu, SIGNAL("activated(int)"), self.switchWirelessConnection)

        if self.wiredConnections.__len__() > 0:
            wiredMenu = KPopupMenu(self.contextMenu())
            for entry in self.wiredConnections:
                entry = unicode(entry)
                if self.comarInterface.isWiredConnectionActive(entry):
                    self.ID[wiredMenu.insertItem(self.loadIconSet("kcmpci"), entry)] = entry
                else:
                    self.ID[wiredMenu.insertItem(self.loadIconSet("stop"), entry)] = entry
            self.contextMenu().insertItem(self.loadIconSet("kcmpci"), _("Wired Profiles"), wiredMenu)
            self.connect(wiredMenu, SIGNAL("activated(int)"), self.switchWiredConnection)

        """ FIXME: Create new connection """
        # self.contextMenu().insertSeparator()
        # self.contextMenu().insertItem(_("Create New Connection Profile"))

        """ Go go go... """
        self.show()

    def switchWirelessConnection(self, activated):
        try:
            invertedID = dict([[v,k] for k,v in self.ID.items()]) 
            activeOne = self.comarInterface.getActiveWirelessConnection()
            if activeOne:
                if not self.ID[activated] == activeOne:
                    self.comarInterface.deactivateWirelessConnection(activeOne)
                    self.contextMenu().changeItem(invertedID[activeOne], QIconSet(self.loadIconSet("stop")), self.contextMenu().text(invertedID[activeOne]))

                    self.comarInterface.activateWirelessConnection(self.ID[activated])
                    self.contextMenu().changeItem(activated, QIconSet(self.loadIconSet("remote")), self.contextMenu().text(activated))
            else:
                self.comarInterface.activateWirelessConnection(self.ID[activated])
                self.contextMenu().changeItem(activated, QIconSet(self.loadIconSet("remote")), self.contextMenu().text(activated))
        except KeyError:
            pass

    def switchWiredConnection(self, activated):
        try:
            invertedID = dict([[v,k] for k,v in self.ID.items()]) 
            activeOne = self.comarInterface.getActiveWiredConnection()
            if activeOne:
                if not self.ID[activated] == activeOne:
                    self.comarInterface.deactivateWiredConnection(activeOne)
                    self.contextMenu().changeItem(invertedID[activeOne], QIconSet(self.loadIconSet("stop")), self.contextMenu().text(invertedID[activeOne]))
    
                    self.comarInterface.activateWiredConnection(self.ID[activated])
                    if self.ID[activated] == self.comarInterface.getActiveWiredConnection():
                        self.contextMenu().changeItem(activated, QIconSet(self.loadIconSet("kcmpci")), self.contextMenu().text(activated))
            else:
                self.comarInterface.activateWiredConnection(self.ID[activated])
                if self.ID[activated] == self.comarInterface.getActiveWiredConnection():
                    self.contextMenu().changeItem(activated, QIconSet(self.loadIconSet("kcmpci")), self.contextMenu().text(activated))
        except KeyError:
            pass

    def loadIcon(self, iconName, size = 16):
        return KGlobal.iconLoader().loadIcon(iconName, KIcon.Desktop, size)

    def loadIconSet(self, iconName, size = 16):
        return KGlobal.iconLoader().loadIconSet(iconName, KIcon.Desktop, size)

if __name__ == "__main__":
    appName = "profile-switcher"
    programName = "profiler-switcher"
    description = "COMAR Profile Switcher Tool"
    license = KAboutData.License_GPL_V2
    version = "0.1"
    copyright = "(C) 2006 S.Çağlar Onur <caglar@uludag.org.tr>"

    aboutData = KAboutData(appName, programName, version, description, license, copyright)

    aboutData.addAuthor("S.Çağlar Onur", "Maintainer", "caglar@uludag.org.tr")

    KCmdLineArgs.init(sys.argv, aboutData)

    """ Use KUniqueApplication and initialize """
    gettext.install(appName)
    app = KUniqueApplication(True, True, True)
    trayWindow = SystemTray(None, appName)

    app.setMainWidget(trayWindow)

    """ Enter main loop """
    app.exec_loop()
