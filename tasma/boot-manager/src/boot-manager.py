#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

# Python Modules
import sys

# KDE/QT Modules
from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

# Widget
from mainwidget import mainForm 

def AboutData():
    about_data = KAboutData("boot_manager",
                            "Boot Manager",
                            "1.0.0",
                            "Boot Manager",
                            KAboutData.License_GPL,
                            "(C) 2006 UEKAE/TÜBİTAK",
                            None, None,
                            "bahadir@pardus.org.tr")
    
    about_data.addAuthor("Bahadır Kandemir", None, "bahadir@pardus.org.tr")
    
    return about_data


# Are we running as a separate standalone application or in KControl?
standalone = __name__=="__main__"


if standalone:
    programbase = QDialog
else:
    programbase = KCModule


class MainApplication(programbase):
    def __init__(self, parent=None, name=None):
        global standalone

        if standalone:
            QDialog.__init__(self, parent, name)
            self.setCaption(i18n("Boot Manager"))
            self.setMinimumSize(520, 420)
            self.resize(520, 420)
        else:
            KCModule.__init__(self, parent, name)
            KGlobal.locale().insertCatalogue("boot-manager")
            # Create a configuration object.
            self.config = KConfig("boot-manager")
            self.setButtons(0)
            self.aboutdata = AboutData()

        #self.setIcon(loadIcon("boot_manager", size=128))

        # The appdir needs to be explicitly otherwise we won"t be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("boot-manager")
        
        # Initialize main widget
        self.mainwidget = mainForm(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(self.mainwidget)

        # Connections
        self.connect(self.mainwidget.comboOS, SIGNAL("activated(int)"), self.slotOS)

    def slotOS(self, id):
        stack = self.mainwidget.widgetStack
        stack.raiseWidget(id)
        if id == 1:
            stack.hide()
        else:
            stack.show()

    def __del__(self):
        pass

    # KControl virtual void methods
    def load(self):
        pass
        
    def save(self):
        pass
        
    def defaults(self):
        pass        
        
    def sysdefaults(self):
        pass
    
    def aboutData(self):
        return self.aboutdata
    
    def buttons(self):
        return KCModule.Help


def main():
    global kapp
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    if not KUniqueApplication.start():
        print i18n("Boot Manager is already running!")
        return
    kapp = KUniqueApplication(True, True, True)
    myapp = MainApplication()
    kapp.setMainWidget(myapp)
    sys.exit(myapp.exec_loop())


# Factory function for KControl
def create_service_manager(parent, name):
    global kapp    
    kapp = KApplication.kApplication()
    return MainApplication(parent, name)

if standalone:
    main()
