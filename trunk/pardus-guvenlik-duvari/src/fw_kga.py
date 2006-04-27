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

description = I18N_NOOP("Pardus Firewall Graphical User Interface")
version = "0.1"

def AboutData():
    global version,description
    
    about_data = KAboutData("fw_kga",
                            "Firewal Interface",
                            version,
                            description,
                            KAboutData.License_GPL,
                            "(C) 2006 UEKAE/TÜBİTAK",
                            None, None,
                            "bahadir@pardus.org.tr")
    
    about_data.addAuthor("Bahadır Kandemir", None, "bahadir@pardus.org.tr")
    
    return about_data

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

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
            self.setCaption(i18n("Firewall Interface"))
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

        # Icons
        mainwidget.pixmapFW.setPixmap(loadIcon("fw_kga", size=48))

        icon = lambda x: QPixmap(locate("data", "fw_kga/%s" % x))
        mainwidget.pixmapIncoming.setPixmap(icon("incoming.png"))
        mainwidget.pixmapICMP.setPixmap(icon("icmp.png"))
        mainwidget.pixmapLogs.setPixmap(icon("logs.png"))

        #self.connect(mainwidget.pushCancel, SIGNAL("clicked()"), self, SLOT("close()"))
        #self.connect(mainwidget.pushOk, SIGNAL("clicked()"), self.saveAll)
        #self.connect(mainwidget.pushHelp,SIGNAL("clicked()"),self.showHelp)

        # Signals - Firewall Status
        self.connect(mainwidget.pushStatus, SIGNAL("clicked()"), self.slotStatus)

        # Signals - Incoming connections
        self.connect(mainwidget.pushAdd, SIGNAL("clicked()"), self.slotAdd)
        self.connect(mainwidget.pushDelete, SIGNAL("clicked()"), self.slotDelete)

        # Signals - Other Features
        self.connect(mainwidget.checkICMP, SIGNAL("clicked()"), self.slotICMP)

        # COMAR
        self.comar = comar.Link()

        # Get FW state
        self.comar.call("Net.Filter.getState")
        if self.comar.read_cmd()[2] == "on":
            mainwidget.pushStatus.setText(i18n("&Stop Firewall"))
            mainwidget.textStatus.setText(i18n("<b><font size=\"+1\">Firewall is running</font></b>"))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(41, 182, 31))
            mainwidget.textStatus2.setText(i18n("Click here to stop the firewall and allow all incoming connections"))
        else:
            mainwidget.pushStatus.setText(i18n("&Start Firewall"))
            mainwidget.textStatus.setText(i18n("<b><font size=\"+1\">Firewall is not running</font></b>"))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(182, 41, 31))
            mainwidget.textStatus2.setText(i18n("Click here to start the firewall"))

        # Load FW rules
        self.rules = {"in": {}, "out": {}}
        self.comar.call("Net.Filter.getRules")
        rules = eval(self.comar.read_cmd()[2])
        for rule in rules: 
            no = rule["no"]
            chk = lambda x: rule.get(x, "")
            # Outgoing connections
            if chk("description") == "fw_kga:WFS":
                mainwidget.checkWFS.setChecked(1)
                self.rules["out"]["WFS"] = no
            elif chk("description") == "fw_kga:Mail":
                mainwidget.checkMail.setChecked(1)
                self.rules["out"]["Mail"] = no
            elif chk("description") == "fw_kga:FTP":
                mainwidget.checkFTP.setChecked(1)
                self.rules["out"]["FTP"] = no
            elif chk("description") == "fw_kga:Remote":
                mainwidget.checkRemote.setChecked(1)
                self.rules["out"]["Remote"] = no
            elif chk("description") == "fw_kga:FS":
                mainwidget.checkFS.setChecked(1)
                self.rules["out"]["FS"] = no
            # Incoming connections
            elif chk("description") == "fw_kga:RejectElse":
                self.rules["in"]["R"] = no
            elif chk("description").startswith("fw_kga:in:"):
                item = QListViewItem(mainwidget.listPorts, rule["dport"], chk("description")[10:])
                mainwidget.listPorts.insertItem(item)
                self.rules["in"][rule["dport"]] = no
            # ICMP/8 (ping)
            elif chk("description") == "fw_kga:icmp":
                mainwidget.checkICMP.setChecked(1)
                self.rules["icmp"] = no

    def addRule(self, **rule):
        """A"""
        self.comar.call("Net.Filter.getRules")
        nums = [i["no"] for i in eval(self.comar.read_cmd()[2])]

        if len(nums):
            rule["no"] = max(map(int, nums)) + 1
        else:
            rule["no"] = 1

        self.comar.call("Net.Filter.setRule", rule)
        if self.comar.read_cmd()[0] == self.comar.RESULT:
            return rule["no"]
        return -1
        
    def removeRule(self, no):
        self.comar.call("Net.Filter.unsetRule", {"no": no})
        self.comar.read_cmd()

    def slotAdd(self):
        if not mainwidget.linePort.text() or not mainwidget.lineDescription.text():
            return
        no = self.addRule(dport=mainwidget.linePort.text(),
                          description="fw_kga:in:%s" % mainwidget.lineDescription.text(),
                          chain="INPUT",
                          jump="ACCEPT",
                          log=0)
        if no > -1:
            item = QListViewItem(mainwidget.listPorts, mainwidget.linePort.text(), mainwidget.lineDescription.text())
            mainwidget.listPorts.insertItem(item)
            self.rules["in"][str(mainwidget.linePort.text())] = no
            mainwidget.linePort.setText("")
            mainwidget.lineDescription.setText("")

            # Re-Insert "Reject Else" rule
            if "R" in self.rules["in"]:
                self.removeRule(self.rules["in"]["R"])
            no = self.addRule(description="fw_kga:RejectElse",
                              chain="INPUT",
                              jump="REJECT")
            self.rules["in"]["R"] = no

    def slotDelete(self):
        item = mainwidget.listPorts.selectedItem()
        if item:
            self.removeRule(self.rules["in"][str(item.text(0))])
            del self.rules["in"][str(item.text(0))]
            mainwidget.listPorts.takeItem(item)
            if len(self.rules["in"]) == 1:
                self.removeRule(self.rules["in"]["R"])
                del self.rules["in"]["R"]

    def slotStatus(self):
        self.comar.call("Net.Filter.getState")
        if self.comar.read_cmd()[2] == "on":
            self.comar.call("Net.Filter.setState", {"name": "filter", "state": "off"})
            mainwidget.pushStatus.setText(i18n("&Start Firewall"))
            mainwidget.textStatus.setText(i18n("<b><font size=\"+1\">Firewall is not running</font></b>"))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(182, 41, 31))
            mainwidget.textStatus2.setText(i18n("Click here to start the firewall"))
        else:
            self.comar.call("Net.Filter.setState", {"name": "filter", "state": "on"})
            mainwidget.pushStatus.setText(i18n("&Stop Firewall"))
            mainwidget.textStatus.setText(i18n("<b><font size=\"+1\">Firewall is running</font></b>"))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(41, 182, 31))
            mainwidget.textStatus2.setText(i18n("Click here to stop the firewall and allow all incoming connections"))
        self.comar.read_cmd()

    def slotICMP(self):
        if mainwidget.checkICMP.isChecked():
            no = self.addRule(protocol="icmp",
                              extra="--icmp-type 8",
                              description="fw_kga:icmp",
                              chain="INPUT",
                              jump="DROP",
                              log=0)
            self.rules["icmp"] = no
        else:
            self.removeRule(self.rules["icmp"])
            del self.rules["icmp"]

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
