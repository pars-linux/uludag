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
version = "1.2"

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

def atoi(s):
    """String to integer"""
    t = ""
    for c in s.lstrip():
        if c in "0123456789":
            t += c
        else:
            break
    try:
        ret = int(t)
    except:
        ret = 0
    return ret

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

        # Signals - Firewall Status
        self.connect(mainwidget.pushStatus, SIGNAL("clicked()"), self.slotStatus)

        # COMAR
        self.comar = comar.Link()

        # COMAR - Notify List
        self.comar.ask_notify('Net.Filter.changed', id=1)
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)

        # Signals
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)
        self.connect(mainwidget.pushCancel, SIGNAL("clicked()"), self, SLOT("close()"))
        self.connect(mainwidget.pushOk, SIGNAL("clicked()"), self.slotOk)
        self.connect(mainwidget.pushApply,SIGNAL("clicked()"),self.slotApply)

        # Load FW rules
        self.no = 0
        self.rules = {"in": {}, "out": {}, "other": {}}
        self.comar.call_package("Net.Filter.getRules", "iptables", id=2)
        self.handleComar(self.comar.read_cmd())
        
        # Get FW state
        self.state = "off"
        self.comar.call_package("Net.Filter.getState", "iptables", id=3)
        self.handleComar(self.comar.read_cmd())

    def slotComar(self, sock):
        self.handleComar(self.comar.read_cmd())

    def setStatus(self, status):
        if status == "on":
            mainwidget.pushStatus.setText(i18n("&Stop Firewall"))
            mainwidget.textStatus.setText(i18n("<b><font size=\"+1\">Firewall is running</font></b>"))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(41, 182, 31))
            mainwidget.textStatus2.setText(i18n("Click here to stop the firewall and allow all incoming and outgoing connections."))
        else:
            mainwidget.pushStatus.setText(i18n("&Start Firewall"))
            mainwidget.textStatus.setText(i18n("<b><font size=\"+1\">Firewall is not running</font></b>"))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(182, 41, 31))
            mainwidget.textStatus2.setText(i18n("Click here to start the firewall and allow connections only to specified services."))

    def handleComar(self, reply):
        if reply[0] == self.comar.NOTIFY:
            # State changed
            info = reply[2].split("\n")
            if info[2] == "state":
                self.state = info[3]
                self.setStatus(info[3])
        elif reply[0] == self.comar.RESULT:
            if reply[1] == 2:
                # Get Rules
                rules = eval(reply[2])
                for rule in rules: 
                    no = rule["no"]
                    self.no = atoi(no)
                    desc = rule.get("description", "")
                    if not desc.startswith("filter:"):
                        continue
                    filter, dir, name = desc.split(":")
                    if dir in ["in", "out"]:
                        if name in ["DNS", "Web", "WFS", "Mail", "FTP", "Remote", "FS", "IRC", "IM"]:
                            eval("mainwidget.check%s%s" % (dir, name)).setChecked(1)
                            self.rules[dir][name] = self.rules[dir].get(name, []) + [no]
                        elif name == "reject":
                            self.rules[dir][name] = self.rules[dir].get(name, []) + [no]
                    elif dir == "other" and name == "ICMP":
                        eval("mainwidget.check%s%s" % (dir, name)).setChecked(1)
                        self.rules[dir][name] = self.rules[dir].get(name, []) + [no]
                
                if "reject" not in self.rules["in"]:
                    self.addRule("in", "reject")
                if "reject" not in self.rules["out"]:
                    self.addRule("out", "reject")
            elif reply[1] == 3:
                # Get State
                self.state = reply[2]
                self.setStatus(reply[2])

    
    def slotStatus(self):
        if self.state == "on":
            self.comar.call_package("Net.Filter.setState", "iptables", {"state": "off"})
        else:
            self.comar.call_package("Net.Filter.setState", "iptables", {"state": "on"})

    def slotOk(self):
        self.saveAll()
        self.close()

    def slotApply(self):
        self.saveAll()

    def saveAll(self):
        for dir in ["in", "out", "other"]:
            s1 = set(self.rules[dir].keys()) - set(["reject"])
            s2 = []

            if dir in ["in", "out"]:
                for name in ["DNS", "Web", "WFS", "Mail", "FTP", "Remote", "FS", "IRC", "IM"]:
                    if eval("mainwidget.check%s%s" % (dir, name)).isChecked():
                        s2.append(name)
            elif dir == "other":
                name = "ICMP"
                if eval("mainwidget.check%s%s" % (dir, name)).isChecked():
                    s2.append(name)
            s2 = set(s2)

            for name in s1 - s2:
                for no in self.rules[dir][name]:
                    self.removeRule(no)
                del self.rules[dir][name]
            for name in s2 - s1:
                no = self.addRule(dir, name)
                self.rules[dir][name] = self.rules[dir].get(name, []) + [no]

    def addRule(self, dir, name):
        def append(no):
            self.rules[dir][name] = self.rules[dir].get(name, []) + [no]

        desc = "filter:%s:%s" % (dir, name)
        if dir == "out":
            if name == "reject":
                # TCP
                no = self.setRule(protocol="tcp", direction="out", type="connections", action="reject", log=1, description=desc)
                append(no)
                # UDP
                no = self.setRule(protocol="udp", direction="out", action="reject", log=1, description=desc)
                append(no)
            elif name == "DNS":
                # TCP
                no = self.setRule(protocol="tcp", direction="out", dport="53", action="accept", description=desc)
                append(no)
                # UDP - In
                no = self.setRule(protocol="udp", direction="in", sport="53", action="accept", description=desc)
                append(no)
                # UDP - Out
                no = self.setRule(protocol="udp", direction="out", dport="53", action="accept", description=desc)
                append(no)
            elif name == "Web":
                no = self.setRule(protocol="tcp", direction="out", dport="80,443", action="accept", description=desc)
                append(no)
            elif name == "WFS":
                no = self.setRule(protocol="tcp", direction="out", dport="139", action="accept", description=desc)
                append(no)
            elif name == "Mail":
                no = self.setRule(protocol="tcp", direction="out", dport="25,110", action="accept", description=desc)
                append(no)
            elif name == "FTP":
                no = self.setRule(protocol="tcp", direction="out", dport="21", action="accept", description=desc)
                append(no)
            elif name == "Remote":
                no = self.setRule(protocol="tcp", direction="out", dport="22", action="accept", description=desc)
                append(no)
            elif name == "FS":
                # FIXME: p2p ports
                no = self.setRule(protocol="tcp", direction="out", dport="5000-5500", action="accept", description=desc)
                append(no)
            elif name == "IRC":
                no = self.setRule(protocol="tcp", direction="out", dport="6665-6669,7000", action="accept", description=desc)
                append(no)
            elif name == "IM":
                # Jabber - TCP
                no = self.setRule(protocol="tcp", direction="out", dport="5222,5269", action="accept", description=desc)
                append(no)
                # Jabber - UDP
                no = self.setRule(protocol="tcp", direction="out", dport="5222,5269", action="accept", description=desc)
                append(no)
                # MSN - TCP
                no = self.setRule(protocol="tcp", direction="out", dport="6891-6901", action="accept", description=desc)
                append(no)
                # MSN - UDP
                no = self.setRule(protocol="udp", direction="out", dport="2001-2120,6801,6901", action="accept", description=desc)
                append(no)
        elif dir == "in":
            if name == "reject":
                no = self.setRule(protocol="tcp", direction="in", type="connections", action="reject", log=1, description=desc)
                append(no)
                no = self.setRule(protocol="udp", direction="in", action="reject", log=1, description=desc)
                append(no)
            elif name == "DNS":
                # TCP
                no = self.setRule(protocol="tcp", direction="in", dport="53", action="accept", description=desc)
                append(no)
                # UDP - In
                no = self.setRule(protocol="udp", direction="in", dport="53", action="accept", description=desc)
                append(no)
                # UDP - Out
                no = self.setRule(protocol="udp", direction="out", sport="53", action="accept", description=desc)
                append(no)
            elif name == "Web":
                no = self.setRule(protocol="tcp", direction="in", dport="80,443", action="accept", description=desc)
                append(no)
            elif name == "WFS":
                no = self.setRule(protocol="tcp", direction="in", dport="139", action="accept", description=desc)
                append(no)
            elif name == "Mail":
                no = self.setRule(protocol="tcp", direction="in", dport="25,110", action="accept", description=desc)
                append(no)
            elif name == "FTP":
                no = self.setRule(protocol="tcp", direction="in", dport="21", action="accept", description=desc)
                append(no)
            elif name == "Remote":
                no = self.setRule(protocol="tcp", direction="in", dport="22", action="accept", description=desc)
                append(no)
            elif name == "FS":
                # FIXME: p2p ports
                no = self.setRule(protocol="tcp", direction="in", dport="5000-5500", action="accept", description=desc)
                append(no)
            elif name == "IRC":
                no = self.setRule(protocol="tcp", direction="in", dport="6665-6669,7000", action="accept", description=desc)
                append(no)
            elif name == "IM":
                # Jabber - TCP
                no = self.setRule(protocol="tcp", direction="in", dport="5222,5269", action="accept", description=desc)
                append(no)
                # Jabber - UDP
                no = self.setRule(protocol="tcp", direction="in", dport="5222,5269", action="accept", description=desc)
                append(no)
        elif dir == "other":
            if name == "ICMP":
                no = self.setRule(protocol="icmp", direction="in", type="8", action="reject", description=desc)
                append(no)

        # Reorder "REJECT" rules
        if dir in ["in", "out"] and name != "reject":
            if dir == "out" and name == "DNS":
                # Remove old
                for no in self.rules["in"]["reject"]:
                    self.removeRule(no)
                for no in self.rules["out"]["reject"]:
                    self.removeRule(no)
                # Add new
                self.addRule("in", "reject")
                self.addRule("out", "reject")
            else:
                # Remove old
                for no in self.rules[dir]["reject"]:
                    self.removeRule(no)
                # Add new
                self.addRule(dir, "reject")

    def setRule(self, **rule):
        self.no += 1
        rule["no"] = self.no
        self.comar.call_package("Net.Filter.setRule", "iptables", rule, id=10)
        self.handleComar(self.comar.read_cmd())
        return rule["no"]

    def removeRule(self, no):
        self.comar.call_package("Net.Filter.unsetRule", "iptables", {"no": no})
        self.handleComar(self.comar.read_cmd())

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
