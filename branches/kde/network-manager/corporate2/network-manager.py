#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys

from qt import *
from kdecore import *
from kdeui import *

from icons import icons, getIconSet

import dbus
from dbus.mainloop.qt3 import DBusQtMainLoop

def I18N_NOOP(x):
    return x

mod_version = "2.1.6"
mod_app = "network-manager"


def AboutData():
    return KAboutData(
        mod_app,
        "Network Manager",
        mod_version,
        I18N_NOOP("Network Manager"),
        KAboutData.License_GPL,
        "(C) 2005-2006 UEKAE/TÜBİTAK",
        None,
        None,
        "bugs@pardus.org.tr"
    )

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    icons.load_icons()
    # Import module after setting DBus mainloop
    # This module makes async. calls on startup
    import browser
    self.mainwidget = browser.Widget(self)
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
def create_network_manager(parent, name):
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
    KCmdLineArgs.addCmdLineOptions ([("auto-connect", I18N_NOOP("Just try to connect automatically"))])
    KUniqueApplication.addCmdLineOptions()
    args = KCmdLineArgs.parsedArgs()
    
    """
    if args.isSet("auto-connect"):
        # Import module after setting DBus mainloop
        # This module makes async. calls on startup
        import autoswitch
        autoSwitch = autoswitch.autoSwitch(notifier = False)
        autoSwitch.scanAndConnect(force=True)
        sys.exit()
    """
    
    if not KUniqueApplication.start():
        print i18n("Network manager module is already started!")
        return
    
    kapp = KUniqueApplication(True, True, True)
    win = QDialog()
    
    DBusQtMainLoop(set_as_default=True)
    
    # PolicyKit Agent requires window ID
    from comariface import comlink
    comlink.winID = win.winId()
    
    win.setCaption(i18n("Network Manager"))
    win.setMinimumSize(500, 440)
    win.resize(620, 440)
    attachMainWidget(win)
    win.setIcon(getIconSet("network").pixmap(QIconSet.Small, QIconSet.Normal))
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())


if __name__ == "__main__":
    main()
