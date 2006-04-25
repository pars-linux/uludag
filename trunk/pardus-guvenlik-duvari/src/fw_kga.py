#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

# Python Modules
import sys

# QT & KDE Modules
from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

# UI
import firewall

# COMAR
import comar

def I18N_NOOP(str):
    return str

description = I18N_NOOP("Pardus Firewall Interface")
version = "0.1"

def AboutData():
    global version,description
    
    about_data = KAboutData("fw_kga",
                            "Pardus Firewal Interface",
                            version,
                            description,
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
        global mainwidget

        if standalone:
            QDialog.__init__(self,parent,name)
            self.setCaption(i18n("Pardus Firewall Interface"))
            self.setMinimumSize(520, 420)
            self.resize(520, 420)
        else:
            KCModule.__init__(self,parent,name)
            KGlobal.locale().insertCatalogue("fw_kga")
            # Create a configuration object.
            self.config = KConfig("fw_kga")
            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("fw_kga")
        
        mainwidget = firewall.MainWindow(self)
        toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
        toplayout.addWidget(mainwidget)

        self.aboutus = KAboutApplication(self)

        self.connect(mainwidget.pushCancel, SIGNAL("clicked()"), self, SLOT("close()"))
        self.connect(mainwidget.pushOk, SIGNAL("clicked()"), self.saveAll)
        #self.connect(mainwidget.pushHelp,SIGNAL("clicked()"),self.showHelp)

        # COMAR
        self.comar = comar.Link()
        
    def addRule(self, **rule):
        self.comar.call("Net.Filter.listRules")
        nums = eval(self.comar.read_cmd()[2])

        if len(nums):
            rule["no"] = max(map(int, nums)) + 1
        else:
            rule["no"] = 1

        self.comar.call('Net.Filter.setRule', rule)
        self.comar.read_cmd()

    def saveAll(self):
        # Outgoing
        if mainwidget.checkWFS.isChecked():
            self.addRule(dport=139, chain="OUTPUT", jump="REJECT")

        if mainwidget.checkMail.isChecked():
            self.addRule(dport=110, chain='OUTPUT', jump='REJECT')
            self.addRule(dport=25, chain='OUTPUT', jump='REJECT')

        if mainwidget.checkFTP.isChecked():
            self.addRule(dport=21, chain='OUTPUT', jump='REJECT')

        if mainwidget.checkRemote.isChecked():
            self.addRule(dport=22, chain='OUTPUT', jump='REJECT')

        # FIXME: p2p ports here
        if mainwidget.checkFS.isChecked():
            self.addRule(dport=10101, chain='OUTPUT', jump='REJECT')

        # Incoming
        if mainwidget.listPorts.childCount() > 0:
            item = mainwidget.listPorts.firstChild()
            while item:
                self.addRule(dport=int(item.text(0)), chain='INPUT', jump='ACCEPT', log=0)
                item = item.nextSibling()

            # Except...
            self.addRule(chain='INPUT', jump='REJECT')

    def __del__(self):
        pass

    def exec_loop(self):
        global programbase
        
        programbase.exec_loop(self)

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

# This is the entry point used when running this module outside of kcontrol.
def main():
    global kapp
    
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    
    if not KUniqueApplication.start():
        print i18n("Pardus Firewall Interface is already running!")
        return
    
    kapp = KUniqueApplication(True, True, True)
    myapp = MainApplication()
    kapp.setMainWidget(myapp)
    #icons.load_icons()
    sys.exit(myapp.exec_loop())
    
# Factory function for KControl
def create_fw_kga(parent,name):
    global kapp
    
    kapp = KApplication.kApplication()
    #icons.load_icons()
    return MainApplication(parent, name)

if standalone:
    main()
