# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connsharing.ui'
#
# Created: Prş Haz 26 11:27:35 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!

from qt import *
from kdecore import *
from kdeui import *
from comariface import comlink
from handler import CallHandler
import commands

from icons import getIconSet
from connSharing import ConnSharing

# DBus

class connShare(ConnSharing):
    def __init__(self, parent=None):
        ConnSharing.__init__(self, parent, "connShare")
        self.parent = parent

        self.fillLabels()

        self.connect(self.sharecheckBox, SIGNAL("stateChanged(int)"), self.slotCheckBox)
        self.connect(self.applyBut, SIGNAL("clicked()"), self.shareConnection)
        self.connect(self.cancelBut, SIGNAL("clicked()"), self.close)

        # COMAR
        self.state = "off"
        self.getState()
        self.profiles = []

    def getProfiles(self):
        self.profiles = []
        self.intcombo.clear()
        self.sharecombo.clear()
        for myhash, profile in comlink.connections.iteritems():
            if profile  in self.profiles:
                continue
            if profile.script != "net_tools" and profile.script != "wireless_tools":
                continue
            self.profiles.append(profile)
            self.intcombo.insertItem(profile.name)
            self.sharecombo.insertItem(profile.name)

    def fillLabels(self):
        self.setCaption(i18n("Internet Connection Sharing"))
        self.sharecheckBox.setText(i18n("Share Internet Connection"))
        self.textLabel1.setText(i18n("Interface that goes to internet"))
        self.textLabel2.setText(i18n("Interface that will share connection"))
        self.applyBut.setText(i18n("Apply"))
        self.applyBut.setIconSet(getIconSet("apply", KIcon.Small))
        self.cancelBut.setText(i18n("Close"))
        self.cancelBut.setIconSet(getIconSet("cancel", KIcon.Small))

    def callMethod(self, method, action, model="Net.Filter"):
        ch = CallHandler("iptables", model, method,
                         action,
                         self.winId(),
                         comlink.busSys, comlink.busSes)
        ch.registerError(self.comarError)
        ch.registerAuthError(self.comarError)
        ch.registerDBusError(self.busError)
        return ch

    def busError(self, exception):
        KMessageBox.error(self, str(exception), i18n("D-Bus Error"))
        # where is setupBusses ?
        # self.setupBusses()

    def comarError(self, exception):
        KMessageBox.error(self, str(exception), i18n("COMAR Error"))

    #Errors
    def updownError(self, exception):
        KMessageBox.error(self, str(exception), i18n("Changing States of Interfaces Failed"))
    def dhcpError(self, exception):
        KMessageBox.error(self, str(exception), i18n("DHCP Server Error"))

    def getState(self):
        def handleState(_type, _desc, _state):
            self.state = "off"
            if _state in ["on", "started"]:
                def handleRules(rules):
                    self.state = "off"
                    for rule in rules:
                        if "POSTROUTING" in rule and "MASQUERADE" in rule:
                            self.state = "on"
                            self.sharecheckBox.setChecked(True)
                            self.groupBox1.setEnabled(True)
                            self.applyBut.setEnabled(True)
                            break
                ch = self.callMethod("getRules", "tr.org.pardus.comar.net.filter.get", "Net.Filter")
                ch.registerDone(handleRules)
                ch.call()
        ch = self.callMethod("info", "tr.org.pardus.comar.system.service.get", "System.Service")
        ch.registerDone(handleState)
        ch.call()

    def shareConnection(self):
        int_if = (self.profiles[self.intcombo.currentItem()].devname.split("(")[-1])[:-1]
        shr_if = (self.profiles[self.sharecombo.currentItem()].devname.split("(")[-1])[:-1]

        if int_if == shr_if:
            KMessageBox.information(self, i18n("The interfaces that you have selected must be different to share internet connection"), i18n("Check Selected Interfaces"))
            return

        #Set share settings(dhcp...)
        int = self.profiles[self.intcombo.currentItem()]
        shr = self.profiles[self.sharecombo.currentItem()]

        #İptables
        self.rule_add = str("-t nat -A POSTROUTING -o %s -j MASQUERADE" % (int_if))
        def notifyOK():
            KMessageBox.information(self, i18n("The sharing of your connection has been successfully done."), i18n("Sharing is OK"))
            self.close()

        def setRule():
            ch = self.callMethod("setRule", "tr.org.pardus.comar.net.filter.set")
            ch.registerDone(notifyOK)
            ch.call(self.rule_add)

        def setProfile():
            ch = self.callMethod("setProfile", "tr.org.pardus.comar.net.filter.set")
            ch.registerDone(setRule)
            ch.call("default","*","*","*","*")

        def startIptables():
            ch = self.callMethod("start", "tr.org.pardus.comar.system.service.set", "System.Service")
            ch.registerDone(setProfile)
            ch.call()

        #DHCP Server
        def startDHCP():
            ch = CallHandler("dhcp", "System.Service", "start", "tr.org.pardus.comar.system.service.set", self.winId(), comlink.busSys, comlink.busSes)
            ch.registerDone(startIptables)
            ch.registerError(self.dhcpError)
            ch.registerAuthError(self.comarError)
            ch.registerDBusError(self.busError)
            ch.call()

        #Down and up the interfaces to avoid lack of routing queries
        #down the interfaces
        #up the interfaces
        def upInt():
            ch = CallHandler(int.script, "Net.Link", "setState", "tr.org.pardus.comar.net.link", self.winId(), comlink.busSys, comlink.busSes)
            ch.registerDone(startDHCP)
            ch.registerError(self.updownError)
            ch.registerAuthError(self.comarError)
            ch.registerDBusError(self.busError)
            ch.call(int.name, "up")

        def upShr():
            ch = CallHandler(shr.script, "Net.Link", "setState", "tr.org.pardus.comar.net.link", self.winId(), comlink.busSys, comlink.busSes)
            ch.registerDone(upInt)
            ch.registerError(self.updownError)
            ch.registerAuthError(self.comarError)
            ch.registerDBusError(self.busError)
            ch.call(shr.name, "up")

        def downInt():
            if int.state == "up":
                ch = CallHandler(int.script, "Net.Link", "setState", "tr.org.pardus.comar.net.link", self.winId(), comlink.busSys, comlink.busSes)
                ch.registerDone(upShr)
                ch.registerError(self.updownError)
                ch.registerAuthError(self.comarError)
                ch.registerDBusError(self.busError)
                ch.call(int.name, "down")

        def updown():
            if shr.state == "up":
                ch = CallHandler(shr.script, "Net.Link", "setState", "tr.org.pardus.comar.net.link", self.winId(), comlink.busSys, comlink.busSes)
                ch.registerDone(downInt)
                ch.registerError(self.updownError)
                ch.registerAuthError(self.comarError)
                ch.registerDBusError(self.busError)
                ch.call(shr.name, "down")
            else:
                downInt()
        def setDHCP():
            ch = CallHandler("dhcp", "Net.Share", "checkShare", "tr.org.pardus.comar.net.share.set", self.winId(), comlink.busSys, comlink.busSes)
            ch.registerDone(updown)
            ch.registerError(self.dhcpError)
            ch.registerAuthError(self.comarError)
            ch.registerDBusError(self.busError)
            ch.call(shr.net_addr, shr.net_mode, shr.net_mask, shr.dns_server)

        if shr.name == None:
            shr.name = ""
        if shr.state == None:
            shr.state = "down"
        if shr.net_addr == None:
            shr.net_addr = ""
        if shr.net_mode == None:
            shr.net_mode = "auto"
        if shr.net_mask == None:
            shr.net_mask = ""
        if shr.dns_server == None:
            shr.dns_server = ""
        if shr.net_mode == "manual":
            setDHCP()
        if shr.net_mode == "auto":
            shr.net_addr = "10.10.10.1"
            shr.net_mask = "255.255.255.0"
            shr.net_mode = "manual"
            if int.net_mode == "manual":
                shr.net_gate = str(int.net_addr)
            else:
                exist = 0
                ifcfg = commands.getstatusoutput("/sbin/ifconfig %s" % int.devname.split("(")[-1][:-1])
                for addr in str(ifcfg[1]).split(" "):
                    if addr.startswith("addr:"):
                        shr.net_gate = addr[5:]
                        exist = 1
                if exist == 0:
                    KMessageBox.information(self, i18n("You do not have an ip address for the interface that goes to internet"), i18n("IP address not found"))
                    return

            ch = CallHandler(shr.script, "Net.Link", "setAddress", "tr.org.pardus.comar.net.link.set", self.winId(), comlink.busSys, comlink.busSes)
            ch.registerDone(setDHCP)
            ch.registerError(self.comarError)
            ch.registerAuthError(self.comarError)
            ch.registerDBusError(self.busError)
            ch.call(shr.name, shr.net_mode, shr.net_addr, shr.net_mask, shr.net_gate)

    def slotCheckBox(self):
        def handleState_dhcp(_type, _desc, _state):
            if _state in ["on", "started"]:
                ch = CallHandler("dhcp", "System.Service", "stop", "tr.org.pardus.comar.system.service.set", self.winId(), comlink.busSys, comlink.busSes)
                ch.registerError(self.comarError)
                ch.registerAuthError(self.comarError)
                ch.registerDBusError(self.busError)
                ch.call()
        def stopIptables():
            ch = self.callMethod("stop", "tr.org.pardus.comar.system.service.set", "System.Service")
            ch.call()

        def removeNatRules():
            ch = self.callMethod("setRule", "tr.org.pardus.comar.net.filter.set")
            ch.registerDone(stopIptables)
            ch.call("-t nat -F")

        def handleState_iptables(_type, _desc, _state):
            if _state in ["on", "started"]:
                removeNatRules()

        if not self.sharecheckBox.isOn():
            # FIXME gui freezes if checkbox is clicked 2 times without any other action

            ch = CallHandler("dhcp", "System.Service", "info", "tr.org.pardus.comar.system.service.set", self.winId(), comlink.busSys, comlink.busSes)
            ch.registerDone(handleState_dhcp)
            ch.registerError(self.comarError)
            ch.registerAuthError(self.comarError)
            ch.registerDBusError(self.busError)
            ch.call()

            ch = self.callMethod("info", "tr.org.pardus.comar.system.service.set", "System.Service")
            ch.registerDone(handleState_iptables)
            ch.call()

            self.groupBox1.setEnabled(False)
            self.applyBut.setEnabled(False)

        else:
            self.groupBox1.setEnabled(True)
            self.applyBut.setEnabled(True)


