#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
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

import mainview
from utility import *

version = "0.5"

def AboutData():
    return KAboutData(
        "user-manager",
        "User Manager",
        version,
        I18N_NOOP("User Management"),
        KAboutData.License_GPL,
        "(C) 2005-2006 UEKAE/TÜBİTAK",
        None,
        None,
        "bugs@pardus.org.tr"
    )


class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue("user-manager")
        self.config = KConfig("user-manager")
        self.setButtons(self.Help)
        self.aboutdata = AboutData()
        KGlobal.iconLoader().addAppDir("user-manager")
        self.mainwidget = mainview.UserManager(self, self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(self.mainwidget)
    
    def load(self):
        pass
    
    def save(self):
        self.mainwidget.execute()
    
    def defaults(self):
        pass        
    
    def sysdefaults(self):
        pass
    
    def aboutData(self):
        return self.aboutdata
    
    def buttons(self):
        return KCModule.Help


class App(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setCaption(i18n("User Manager"))
        self.setMinimumSize(620, 380)
        self.resize(520, 420)
        KGlobal.iconLoader().addAppDir("user-manager")
        self.mainwidget = mainview.UserManager(self, self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(self.mainwidget)

#        self.aboutus = KAboutApplication(self)


# This is the entry point used when running this module outside of kcontrol.
def main():
    global kapp
    
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    
    if not KUniqueApplication.start():
        print i18n("User manager module is already started!")
        return
    
    kapp = KUniqueApplication(True, True, True)
    myapp = App()
    kapp.setMainWidget(myapp)
    sys.exit(myapp.exec_loop())

# Factory function for KControl
def create_user_manager(parent,name):
    global kapp
    
    kapp = KApplication.kApplication()
    return Module(parent, name)


if __name__ == "__main__":
    main()
