#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
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
import SetupUsers

def I18N_NOOP(str):
    return str

description = I18N_NOOP("User Management")
version = "0.1"

def AboutData():
    global version,description
    
    about_data = KAboutData("users_kga", "Users KGA", version, \
                            description, KAboutData.License_GPL,
                            "(C) 2005 UEKAE/TÜBİTAK", None, None, "ismail@uludag.org.tr")
    
    about_data.addAuthor("A. Murat Eren", None, "meren@uludag.org.tr")
    about_data.addAuthor("İsmail Dönmez", None, "ismail@uludag.org.tr")
    return about_data


# Are we running as a separate standalone application or in KControl?
standalone = __name__=='__main__'

if standalone:
    programbase = QDialog
else:
    programbase = KCModule
    
class MainApplication(programbase):
    def __init__(self, parent=None, name=None):
        global standalone
        global mainwidget

        if standalone:
            QDialog.__init__(self,parent,name)
            self.setCaption(i18n("Users Management"))
            self.setMinimumSize(520, 420)
            self.resize(520, 420)
        else:
            KCModule.__init__(self,parent,name)
            KGlobal.locale().insertCatalogue("users_kga")
            # Create a configuration object.
            self.config = KConfig("users_kga")
#            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("users_kga")
        

        self.mainwidget = SetupUsers.Widget(self)

        toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
        toplayout.addWidget(self.mainwidget)

        self.aboutus = KAboutApplication(self)

    def __del__(self):
        pass

    def exec_loop(self):
        global programbase
        
        programbase.exec_loop(self)

    # KControl virtual void methods
    def load(self):
        pass
    def save(self):
        self.mainwidget.execute()
    def defaults(self):
        pass        
    def sysdefaults(self):
        pass
    
    def aboutData(self):
        # Return the KAboutData object which we created during initialisation.
        return self.aboutdata
    
    def buttons(self):
        # Only supply a Help button. Other choices are Default and Apply.
        return KCModule.Help

# This is the entry point used when running this module outside of kcontrol.
def main():
    global kapp
    
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)

    if not KUniqueApplication.start():
        print i18n("Users module is already started!")
        return

    kapp = KUniqueApplication(True, True, True)
    myapp = MainApplication()
    kapp.setMainWidget(myapp)
    sys.exit(myapp.exec_loop())
    
# Factory function for KControl
def create_users_kga(parent,name):
    global kapp
    
    kapp = KApplication.kApplication()
    return MainApplication(parent, name)

if standalone:
    main()
