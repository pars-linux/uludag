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
import os
import re
import sys
import time

# QT & KDE Modules
from qt import *
from kdecore import *
from kdeui import *
from khtml import *
import kdedesigner

# UI
import firewall

# COMAR
import comar

def I18N_NOOP(str):
    return str

description = I18N_NOOP("Pardus Firewall Graphical User Interface")
version = "1.5.1"

def AboutData():
    global version,description
    
    about_data = KAboutData("firewall-config",
                            "Firewall Configuration",
                            version,
                            description,
                            KAboutData.License_GPL,
                            "(C) 2006 UEKAE/TÜBİTAK",
                            None, None,
                            "bahadir@pardus.org.tr")
    
    about_data.addAuthor("Bahadır Kandemir", None, "bahadir@pardus.org.tr")
    about_data.addCredit("Görkem Çetin", I18N_NOOP("GUI Design & Usability"), "gorkem@pardus.org.tr")
    about_data.addCredit("İsmail Dönmez", I18N_NOOP("Help with IPTables"), "ismail@pardus.org.tr")
    about_data.addCredit("Gürer Özen", I18N_NOOP("Help with KDE stuff"), "gurer@pardus.org.tr")

    return about_data

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def getIconPath(name, group=KIcon.Desktop):
    if not name:
        name = "package"
    return KGlobal.iconLoader().iconPath(name, group)

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

def portsOk(p):
    """Check multiport format"""
    if p.startswith("! "):
        p = p[2:]
    if p.count(",") + p.count(":") > 15:
        return 0
    l = p.split(",")
    for i in l:
        k = i.split(":")
        if len(k) > 2:
            return 0
        for j in k:
            if 0 >= atoi(j) <= 65535:
                return 0
    return 1

# Are we running as a separate standalone application or in KControl?
standalone = __name__=="__main__"

if standalone:
    programbase = QDialog
else:
    programbase = KCModule


class portlistItem(KListViewItem):
    def __init__(self, parent=None, rule={}):
        KListViewItem.__init__(self, parent)

        d = {"in": i18n("In"), "out": i18n("Out")}
        self.setText(0, d[rule["direction"]])

        if "src" in rule and "sport" in rule:
            src = "%s:%s" % (rule["src"], rule["sport"])
        elif "src" in rule and "sport" not in rule:
            src = "%s:*" % rule["src"]
        elif "src" not in rule and "sport" in rule:
            src = "*:%s" % rule["sport"]
        else:
            src = "*"
        self.setText(1, src)

        if "dst" in rule and "dport" in rule:
            dst = "%s:%s" % (rule["dst"], rule["dport"])
        elif "dst" in rule and "dport" not in rule:
            dst = "%s:*" % rule["dst"]
        elif "dst" not in rule and "dport" in rule:
            dst = "*:%s" % rule["dport"]
        else:
            dst = "*"
        self.setText(2, dst)

        d = {"REJECT": i18n("Reject"), "ACCEPT": i18n("Accept")}
        self.setText(3, d[rule["action"].upper()])

        self.ruleno = rule["no"]
        self.rule = rule.copy()
        del self.rule["no"]


class LogDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(i18n('Firewall Logs'))
        self.setModal(1)
        self.layout = QGridLayout(self)

        self.log = KTextEdit(self)
        self.log.setTextFormat(Qt.LogText)

        self.resize(500, 300)
        self.layout.addWidget(self.log, 1, 1)

    def showLog(self):
        self.log.setText("")

        log = "/var/log/netfilter.log"

        if not os.access(log, os.F_OK):
            return

        f = open(log)
        s = f.read()
        if s:
            self.log.append(s[:-1])
        f.close()

class MainApplication(programbase):
    def __init__(self, parent=None, name=None):
        global standalone
        global mainwidget
        global logwin

        if standalone:
            QDialog.__init__(self,parent,name)
            self.setCaption(i18n("Firewall Configuration"))
            self.setMinimumSize(566, 544)
            self.resize(566, 544)
        else:
            KCModule.__init__(self,parent,name)
            KGlobal.locale().insertCatalogue("firewall_config")
            # Create a configuration object.
            self.config = KConfig("firewall_config")
            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("firewall_config")
        
        mainwidget = firewall.MainWindow(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(mainwidget)

        self.aboutus = KAboutApplication(self)

        logwin = LogDialog(self)

        # Icons
        mainwidget.pixmapFW.setPixmap(loadIcon("firewall_config", size=48))
        mainwidget.pixmapIncoming.setPixmap(loadIcon("krfb.png", size=48))

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
        self.connect(mainwidget.pushApply, SIGNAL("clicked()"),self.slotApply)

        self.connect(mainwidget.pushAdd, SIGNAL("clicked()"),self.slotAdd)
        self.connect(mainwidget.pushRemove, SIGNAL("clicked()"),self.slotRemove)

        self.connect(mainwidget.pushLog, SIGNAL("clicked()"),self.slotLog)

        # Load FW rules
        self.no = 0
        self.rules = {"in": {}, "out": {}, "other": {}}
        self.removed = []
        self.comar.call("Net.Filter.getRules", id=2)
        self.handleComar(self.comar.read_cmd())
        
        # Get FW state
        self.state = "off"
        self.comar.call("Net.Filter.getState", id=3)
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
                    if dir == "in":
                        if name in ["DNS", "Web", "WFS", "Mail", "FTP", "Remote", "FS", "IRC", "IM"]:
                            eval("mainwidget.check%s%s" % (dir, name)).setChecked(1)
                        self.rules[dir][name] = self.rules[dir].get(name, []) + [no]
                    elif dir == "out":
                        self.rules[dir][name] = self.rules[dir].get(name, []) + [no]
                    elif dir == "other" and name == "ICMP":
                        eval("mainwidget.check%s%s" % (dir, name)).setChecked(1)
                        self.rules[dir][name] = self.rules[dir].get(name, []) + [no]
                    elif dir == "adv":
                        item = portlistItem(mainwidget.listAdvanced, rule)

                # Insert missing base rules
                # DNS Service
                if "DNS" not in self.rules["out"]:
                    self.addRule("out", "DNS")
                # Reject-Else
                if "reject" not in self.rules["in"]:
                    self.addRule("in", "reject")

            elif reply[1] == 3:
                # Get State
                self.state = reply[2]
                self.setStatus(reply[2])

    
    def slotStatus(self):
        if self.state == "on":
            self.comar.call("Net.Filter.setState", {"state": "off"})
        else:
            self.comar.call("Net.Filter.setState", {"state": "on"})

    def slotOk(self):
        self.saveAll()
        self.close()

    def slotApply(self):
        self.saveAll()

    def slotAdd(self):
        rule = {"no": -1, "description": "filter:adv:0", "protocol": "tcp"}

        if mainwidget.lineFromIP.text():
            rule["src"] = str(mainwidget.lineFromIP.text())
        if mainwidget.lineFromPort.text():
            rule["sport"] = str(mainwidget.lineFromPort.text())
            if not portsOk(rule["sport"]):
                KMessageBox.error(mainwidget, i18n("Ports must be in valid format.\n\nE.g.: 1000-1500,2000,3000"), i18n("Error"))
                return
        if mainwidget.lineToIP.text():
            rule["dst"] = str(mainwidget.lineToIP.text())
        if mainwidget.lineToPort.text():
            if not portsOk(rule["dport"]):
                KMessageBox.error(mainwidget, i18n("Ports must be in valid format.\n\nE.g.: 1000-1500,2000,3000"), i18n("Error"))
                return
            rule["dport"] = str(mainwidget.lineToPort.text())
       
        if mainwidget.comboDirection.currentItem():
            rule["direction"] = "out"
        else:
            rule["direction"] = "in"

        if mainwidget.comboAction.currentItem():
            rule["action"] = "reject"
        else:
            rule["action"] = "accept"

        item = portlistItem(mainwidget.listAdvanced, rule)

    def slotRemove(self):
        item = mainwidget.listAdvanced.selectedItem()
        if item:
            if item.ruleno > -1:
                self.removed.append(item.ruleno)
            mainwidget.listAdvanced.takeItem(item)

    def slotLog(self):
        logwin.show()
        logwin.showLog()

    def saveAll(self):
        for dir in ["in", "out", "other"]:
            s1 = set(self.rules[dir].keys()) - set(["reject"])
            s2 = []

            if dir == "out":
                # Add default DNS service
                s2.append("DNS")
            elif dir == "in":
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

        # Adv
        item = mainwidget.listAdvanced.firstChild()
        while item:
            if item.ruleno == -1:
                no = self.setRule(**item.rule)
                item.ruleno = no
            item = item.nextSibling()

        for i in self.removed:
            self.removeRule(i)
        self.removed = []

        # Re-order Reject-Else rules
        self.reorder("in")

    def addRule(self, dir, name):
        def append(no):
            self.rules[dir][name] = self.rules[dir].get(name, []) + [no]

        desc = "filter:%s:%s" % (dir, name)
        if dir == "out":
            if name == "DNS":
                # UDP
                no = self.setRule(protocol="udp", direction="in", sport="53", action="accept", description=desc)
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

    def reorder(self, dir):
        # Remove old
        for no in self.rules[dir]["reject"]:
            self.removeRule(no)
        # Add new
        self.addRule(dir, "reject")

    def setRule(self, **rule):
        self.no += 1
        rule["no"] = self.no
        self.comar.call("Net.Filter.setRule", rule, id=10)
        self.handleComar(self.comar.read_cmd())
        return rule["no"]

    def removeRule(self, no):
        self.comar.call("Net.Filter.unsetRule", {"no": no})
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
def create_firewall_config(parent,name):
    global kapp
    
    kapp = KApplication.kApplication()
    #icons.load_icons()
    return MainApplication(parent, name)

if standalone:
    main()
