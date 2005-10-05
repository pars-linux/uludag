#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors:  İsmail Dönmez <ismail@uludag.org.tr>

import sys
from qt import *
from kdecore import *
from kdeui import *

import kdedesigner
import NewConnection
import EthernetPage
import MainWindow

description = "Pardus Ağ Ayarları Aracı"
version = "0.0.1"

############################################################################
def AboutData():
    global version,description
    
    about_data = KAboutData("network", "network_kga", version, \
        description, KAboutData.License_GPL, "(C) 2005 UEAKE/TÜBİTAK", None, None,\
        "ismail@uludag.org.tr")
    about_data.addAuthor("İsmail Dönmez", None, "ismail@uludag.org.tr")
    return about_data

############################################################################
def loadIcon(name, group=KIcon.Desktop):
        return KGlobal.iconLoader().loadIcon(name, group)

############################################################################
def loadIconSet(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIconSet(name, group)
            
############################################################################
class MainWidget(MainWindow.MainWindow):
    def __init__(self,parent=None):
        MainWindow.MainWindow.__init__(self,parent)
	self.wizardLabel.setPixmap(loadIcon("wizard"))
	self.localNetworkLabel.setPixmap(loadIcon("network"))
        self.wirelessLabel.setPixmap(loadIcon("remote"))
	self.wirelessDisconnectedLabel.setPixmap(loadIcon("socket"))
	
    # Hide top title
    def layOutTitleRow(self, layout, title):
        KWizard.layOutTitleRow(self, layout, title)
        iter = layout.iterator()
        while iter.current():
            iter.current().widget().hide()
            iter.next()

############################################################################
# The base class that we use depends on whether this is running inside
# kcontrol or as a standalone application.
# Are we running as a separate standalone application or in KControl?
standalone = __name__=='__main__'

if standalone:
    programbase = MainWidget
else:
    programbase = KCModule
    
class MainApplication(programbase):
    ########################################################################
    def __init__(self,parent=None,name=None):
        global standalone
        if standalone:
            pass
            MainWidget.__init__(self, parent)
            self.show()
        else:
            KCModule.__init__(self,parent,name)
            # Create a configuration object.
            self.config = KConfig("network_kga")
            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("network_kga")
        
        if standalone:
            mainwidget = self            
        else:
            toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
            mainwidget = MainWidget(self)
            toplayout.addWidget(mainwidget)

        self.aboutus = KAboutApplication(self)
                
    ########################################################################
    def __del__(self):
        pass

    ########################################################################
    def exec_loop(self):
        global programbase
        
        # Load configuration here
        self.__loadOptions()
        
        programbase.exec_loop(self)
        
        # Save configuration here
        self.__saveOptions()

    ########################################################################
    def __loadOptions(self):
        global kapp
        config = kapp.config()
        config.setGroup("General")
        size = config.readSizeEntry("Geometry")
        if size.isEmpty()==False:
            self.resize(size)

    #######################################################################
    def __saveOptions(self):
        global kapp
        config = kapp.config()
        config.setGroup("General")
        config.writeEntry("Geometry", self.size())
        config.sync()

    #######################################################################
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
        # Return the KAboutData object which we created during initialisation.
        return self.aboutdata
    
    def buttons(self):
        # Only supply a Help button. Other choices are Default and Apply.
        return KCModule.Help

############################################################################
# This is the entry point used when running this module outside of kcontrol.
def main():
    global kapp
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)
    kapp = KApplication()
    myapp = MainApplication()
    myapp.exec_loop()
    
############################################################################
# Factory function for KControl
def create_kcontrol_module(parent,name):
    global kapp
    kapp = KApplication.kApplication()
    return MainApplication(parent, name)
    
############################################################################
if standalone:
    main()

