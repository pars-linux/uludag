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
import time

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
    
    about_data = KAboutData("guvenlik_kga",
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
            KGlobal.locale().insertCatalogue("guvenlik_kga")
            # Create a configuration object.
            self.config = KConfig("guvenlik_kga")
            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("guvenlik_kga")
        
        mainwidget = firewall.MainWindow(self)
        toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
        toplayout.addWidget(mainwidget)

        self.aboutus = KAboutApplication(self)

        # Icons
        mainwidget.pixmapFW.setPixmap(loadIcon("guvenlik_kga", size=48))

        icon = lambda x: QPixmap(locate("data", "guvenlik_kga/%s" % x))
        mainwidget.pixmapIncoming.setPixmap(icon("incoming.png"))
        mainwidget.pixmapICMP.setPixmap(icon("icmp.png"))
        mainwidget.pixmapLogs.setPixmap(icon("logs.png"))

        #self.connect(mainwidget.pushCancel, SIGNAL("clicked()"), self, SLOT("close()"))
        #self.connect(mainwidget.pushOk, SIGNAL("clicked()"), self.saveAll)
        #self.connect(mainwidget.pushHelp,SIGNAL("clicked()"),self.showHelp)

        # Signals - Firewall Status
        self.connect(mainwidget.pushStatus, SIGNAL("clicked()"), self.slotStatus)

        self.connect(mainwidget.checkWFS, SIGNAL("clicked()"), self.slotWFS)
        self.connect(mainwidget.checkMail, SIGNAL("clicked()"), self.slotMail)
        self.connect(mainwidget.checkFTP, SIGNAL("clicked()"), self.slotFTP)
        self.connect(mainwidget.checkRemote, SIGNAL("clicked()"), self.slotRemote)
        self.connect(mainwidget.checkFS, SIGNAL("clicked()"), self.slotFS)
        
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
            name = chk("description").split(":")[1]
            if name in ["WFS", "Mail", "FTP", "Remote", "FS"]:
                eval("mainwidget.check%s" % name).setChecked(1)
                self.rules["out"][name] = self.rules["out"].get(name, []) + [no]
            # Incoming connections - Allowed ports
            elif chk("description").startswith("guvenlik_kga:in:"):
                self.rules["in"][rule["dport"]] = self.rules["in"].get(rule["dport"], []) + [no]
                if len(self.rules["in"][rule["dport"]]) == 1:
                    item = QListViewItem(mainwidget.listPorts, rule["dport"], chk("description")[16:])
                    mainwidget.listPorts.insertItem(item)
                    # Show warning message
                    mainwidget.textWarning.setEnabled(1)
            # Incoming connections - Magic Reject-Else Rule
            elif chk("description") == "guvenlik_kga:RejectElse":
                self.rules["in"]["R"] = self.rules["in"].get("R", []) + [no]
            # ICMP/8 (ping)
            elif chk("description") == "guvenlik_kga:icmp":
                mainwidget.checkICMP.setChecked(1)
                self.rules["icmp"] = no

    def addRule(self, **rule):
        """Add rule"""
        self.comar.call("Net.Filter.getID")
        rule["no"] = self.comar.read_cmd()[2]

        self.comar.call("Net.Filter.setRule", rule)
        return self.comar.read_cmd()
        
    def removeRule(self, no):
        self.comar.call("Net.Filter.unsetRule", {"no": no})
        self.comarError(self.comar.read_cmd())

    def comarError(self, res):
        if res[0] == self.comar.RESULT:
            return
        if res[0] == self.comar.DENIED:
            KMessageBox.error(mainwidget, i18n("You are not allowed to do this operation."), i18n("Access Denied"))
        elif res[0] == self.comar.FAIL:
            if res[2] == "Invalid port":
                KMessageBox.error(mainwidget, i18n("Port number is in invalid format."), i18n("Failed"))
            else:
                KMessageBox.error(mainwidget, i18n("Unable to complete operation."), i18n("Failed"))
        else:
            KMessageBox.error(mainwidget, i18n("Unable to execute method."), i18n("Script Error"))

    def slotAdd(self):
        if not mainwidget.linePort.text() or not mainwidget.lineDescription.text():
            KMessageBox.error(mainwidget, i18n("Both port number and description required."), i18n("Error"))
            return
        if str(mainwidget.linePort.text()) in self.rules["in"]:
            KMessageBox.error(mainwidget, i18n("Port number is already in list."), i18n("Error"))
            return
            
        res = self.addRule(dport=mainwidget.linePort.text(),
                           description="guvenlik_kga:in:%s" % mainwidget.lineDescription.text(),
                           protocol="tcp",
                           direction="in",
                           action="Accept",
                           log=0)

        if res[0] == self.comar.RESULT:
            self.rules["in"][str(mainwidget.linePort.text())] = [res[2]]
        else:
            self.comarError(res)
            return

        res = self.addRule(dport=mainwidget.linePort.text(),
                           description="guvenlik_kga:in:%s" % mainwidget.lineDescription.text(),
                           protocol="udp",
                           direction="in",
                           action="Accept",
                           log=0)

        self.rules["in"][str(mainwidget.linePort.text())] += [res[2]]
        
        # Add to list
        item = QListViewItem(mainwidget.listPorts, mainwidget.linePort.text(), mainwidget.lineDescription.text())
        mainwidget.listPorts.insertItem(item)
        mainwidget.linePort.setText("")
        mainwidget.lineDescription.setText("")

        # Re-Insert "Reject Else" rules
        if "R" in self.rules["in"]:
            for i in self.rules["in"]["R"]:
                self.removeRule(i)
        self.rules["in"]["R"] = []
        # TCP
        res = self.addRule(description="guvenlik_kga:RejectElse",
                           protocol="tcp",
                           type="connections",
                           direction="in",
                           action="Reject")
        self.rules["in"]["R"] += [res[2]]
        # UDP
        #res = self.addRule(description="guvenlik_kga:RejectElse",
        #                   protocol="udp",
        #                   direction="Iin",
        #                   action="Reject")
        #self.rules["in"]["R"] += [res[2]]

        # Show warning message
        mainwidget.textWarning.setEnabled(1)

    def slotDelete(self):
        item = mainwidget.listPorts.selectedItem()
        if item:
            for i in self.rules["in"][str(item.text(0))]:
                self.removeRule(i)
            del self.rules["in"][str(item.text(0))]
            mainwidget.listPorts.takeItem(item)
            if len(self.rules["in"]) == 1:
                for i, j in enumerate(self.rules["in"]["R"]):
                    self.removeRule(j)
                self.rules["in"]["R"] = []

                # Hide warning message
                mainwidget.textWarning.setEnabled(0)

    def slotStatus(self):
        self.comar.call("Net.Filter.getState")
        if self.comar.read_cmd()[2] == "on":
            self.comar.call("Net.Filter.setState", {"state": "off"})
            mainwidget.pushStatus.setText(i18n("&Start Firewall"))
            mainwidget.textStatus.setText(i18n("<b><font size=\"+1\">Firewall is not running</font></b>"))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(182, 41, 31))
            mainwidget.textStatus2.setText(i18n("Click here to start the firewall"))
        else:
            self.comar.call("Net.Filter.setState", {"state": "on"})
            mainwidget.pushStatus.setText(i18n("&Stop Firewall"))
            mainwidget.textStatus.setText(i18n("<b><font size=\"+1\">Firewall is running</font></b>"))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(41, 182, 31))
            mainwidget.textStatus2.setText(i18n("Click here to stop the firewall and allow all incoming connections"))
        self.comar.read_cmd()

    def slotOut(self, chk, name, port):
        if chk.isChecked():
            self.rules["out"][name] = []
            res = self.addRule(protocol="tcp",
                               dport=port,
                               description="guvenlik_kga:%s" % name,
                               direction="out",
                               action="Reject",
                               log=1)
            self.rules["out"][name] += [res[2]]
            res = self.addRule(protocol="udp",
                               dport=port,
                               description="guvenlik_kga:%s" % name,
                               direction="out",
                               action="DROP",
                               log=1)
            self.rules["out"][name] += [res[2]]
        else:
            for i, j in enumerate(self.rules["out"][name]):
                self.removeRule(j)
            self.rules["out"][name] = []
            
    def slotWFS(self):
        self.slotOut(mainwidget.checkWFS, "WFS", "139")
        
    def slotMail(self):
        self.slotOut(mainwidget.checkMail, "Mail", "25,110")

    def slotFTP(self):
        self.slotOut(mainwidget.checkFTP, "FTP", "21")

    def slotRemote(self):
        self.slotOut(mainwidget.checkRemote, "Remote", "22")

    def slotFS(self):
        # FIXME: p2p ports required
        self.slotOut(mainwidget.checkFS, "FS", "30000:40000")

    def slotICMP(self):
        if mainwidget.checkICMP.isChecked():
            res = self.addRule(protocol="icmp",
                               type="8",
                               description="guvenlik_kga:icmp",
                               direction="in",
                               action="Reject",
                               log=1)
            self.rules["icmp"] = res[2]
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
def create_guvenlik_kga(parent,name):
    global kapp
    
    kapp = KApplication.kApplication()
    #icons.load_icons()
    return MainApplication(parent, name)

if standalone:
    main()
