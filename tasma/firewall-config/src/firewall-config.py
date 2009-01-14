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
import kdedesigner

# UI
import firewall
import dialog

# DBus
import dbus
import dbus.mainloop.qt3

from handler import CallHandler

# Rules
import rules

def I18N_NOOP(str):
    return str

description = I18N_NOOP('Pardus Firewall Graphical User Interface')
version = '2.0.4'

def AboutData():
    global version, description

    about_data = KAboutData('firewall-config',
                            'Firewall Configuration',
                            version,
                            description,
                            KAboutData.License_GPL,
                            '(C) 2006 UEKAE/TÜBİTAK',
                            None, None,
                            'bahadir@pardus.org.tr')

    about_data.addAuthor('Bahadır Kandemir', None, 'bahadir@pardus.org.tr')
    about_data.addCredit('Görkem Çetin', I18N_NOOP('GUI Design & Usability'), 'gorkem@pardus.org.tr')
    about_data.addCredit('İsmail Dönmez', I18N_NOOP('Help with IPTables'), 'ismail@pardus.org.tr')
    about_data.addCredit('Gürer Özen', I18N_NOOP('Help with KDE stuff'), 'gurer@pardus.org.tr')

    return about_data

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def loadIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group, 0, False)

# Are we running as a separate standalone application or in KControl?
standalone = __name__ == '__main__'

if standalone:
    programbase = QDialog
else:
    programbase = KCModule


class AdvancedRuleCheckBox(QCheckBox):
    def __init__(self, parent=None, name=None, rule=''):
        QCheckBox.__init__(self, parent, name)
        self.rule = rule

        protocol = re.findall('-p ([a-z]+)', self.rule)[0]
        ports = re.findall('--dports ([0-9,:]+)', self.rule)[0]

        if self.rule.startswith('-A PARDUS-IN-USER'):
            dir = 'in'
        else:
            dir = 'out'

        if self.rule.endswith('-j ACCEPT'):
            action = 'accept'
        else:
            action = 'reject'

        if dir == 'in':
            if action == 'accept':
                msg = i18n('Accept all incoming connection through ports %s')
            else:
                msg = i18n('Reject all incoming connection through ports %s')
        else:
            if action == 'accept':
                msg = i18n('Accept all outgoing connection through ports %s')
            else:
                msg = i18n('Reject all outgoing connection through ports %s')

        self.setText(msg.replace('%s', '%s (%s)' % (ports.replace(':', '-'), protocol)))


def checkPortFormat(ports):
    '''Check multiport format'''
    if ports.count(',') + ports.count('-') > 15:
        return False
    for port in ports.split(','):
        grp = port.split('-')
        if len(grp) > 2:
            return False
        for p in grp:
            if not p.isdigit() or p.startswith("0") or 0 > int(p) or int(p) > 65535:
                return False
    return True

class dialogRule(dialog.dialogRule):
    def __init__(self, parent=None, name=None):
        dialog.dialogRule.__init__(self, parent, name)

        self.connect(self.pushCancel, SIGNAL('clicked()'), self, SLOT('reject()'))
        self.connect(self.pushOK, SIGNAL('clicked()'), SLOT('accept()'))

        # Load icons for buttons
        self.pushCancel.setIconSet(loadIconSet('cancel', group=KIcon.Small))
        self.pushOK.setIconSet(loadIconSet('ok', group=KIcon.Small))

    def accept(self):
        if checkPortFormat(str(self.linePorts.text())):
            dialog.dialogRule.accept(self)
        else:
            KMessageBox.sorry(self, i18n('Invalid port range.'), i18n('Error'))

    def exec_loop(self):
        if dialog.dialogRule.exec_loop(self):
            direction = ['IN', 'OUT'][self.radioOut.isChecked()]
            action = ['ACCEPT', 'REJECT'][self.radioReject.isChecked()]
            protocol = self.comboProtocol.currentText().lower()
            ports = self.linePorts.text().replace('-', ':')
            ports = ports.replace(' ', '')

            return '-A PARDUS-%s-USER -p %s -m multiport --dports %s -j %s' % (direction, protocol, ports, action)
        else:
            return False


class MainApplication(programbase):
    def __init__(self, parent=None, name=None):
        global standalone
        global mainwidget
        global logwin

        if standalone:
            QDialog.__init__(self,parent,name)
            self.setCaption(i18n('Firewall Configuration'))
        else:
            KCModule.__init__(self,parent,name)
            KGlobal.locale().insertCatalogue('firewall_config')
            # Create a configuration object.
            self.config = KConfig('firewall_config')
            self.aboutdata = AboutData()
            self.setButtons(KCModule.Help | KCModule.Apply)

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir('firewall_config')

        mainwidget = firewall.MainWindow(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(mainwidget)

        self.aboutus = KAboutApplication(self)

        # Initial conditions
        self.state = 'off'
        self.profile = {}
        self.emptyRules()
        mainwidget.pushStatus.setEnabled(False)

        if not standalone:
            mainwidget.groupButtons.hide()

        # Tab 1 - Incoming Connections
        self.incoming = []
        mainwidget.frameIncoming.setColumnLayout(0, Qt.Vertical)
        frameIncomingLayout = QVBoxLayout(mainwidget.frameIncoming.layout())
        frameIncomingLayout.setAlignment(Qt.AlignTop)

        # Tab 2 - Advanced
        self.advanced = []
        mainwidget.frameAdvanced.setColumnLayout(0, Qt.Vertical)
        mainwidget.frameAdvancedLayout = QVBoxLayout(mainwidget.frameAdvanced.layout())
        mainwidget.frameAdvancedLayout.setAlignment(Qt.AlignTop)

        # Populate checkboxes
        for key, (list_rules, name, ports) in rules.filter.iteritems():
            if key.startswith('in'):
                chk = QCheckBox(mainwidget.frameIncoming, key)
                chk.setText(i18n(name))
                QToolTip.add(chk, unicode(i18n("Ports: %s")) % ports)
                frameIncomingLayout.addWidget(chk)
                self.incoming.append(chk)
                self.connect(chk, SIGNAL('clicked()'), self.slotChanged)

        # Icons
        self.setIcon(loadIcon('firewall_config', size=48))
        mainwidget.pixmapFW.setPixmap(loadIcon('firewall_config', size=48))
        mainwidget.pixmapIncoming.setPixmap(loadIcon('server.png', size=48))
        mainwidget.pixmapAdvanced.setPixmap(loadIcon('gear.png', size=48))
        mainwidget.pushNewRule.setPixmap(loadIcon('add.png', size=32))

        mainwidget.pushOk.setIconSet(loadIconSet('ok', group=KIcon.Small))
        mainwidget.pushCancel.setIconSet(loadIconSet('cancel', group=KIcon.Small))
        mainwidget.pushHelp.setIconSet(loadIconSet('help', group=KIcon.Small))
        mainwidget.pushApply.setIconSet(loadIconSet('apply', group=KIcon.Small))

        # COMAR
        self.setupBusses()

        # Signals
        self.connect(mainwidget.pushStatus, SIGNAL('clicked()'), self.slotStatus)
        self.connect(mainwidget.pushCancel, SIGNAL('clicked()'), self, SLOT('close()'))
        self.connect(mainwidget.pushOk, SIGNAL('clicked()'), self.slotOk)
        self.connect(mainwidget.pushApply, SIGNAL('clicked()'), self.slotApply)
        self.connect(mainwidget.pushNewRule, SIGNAL('clicked()'), self.slotDialog)

        # Init
        self.getState()

    def setupBusses(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException:
            KMessageBox.error(self, i18n("Unable to connect to DBus."), i18n("DBus Error"))
            return False
        return True

    def handleSignals(self, *args, **kwargs):
        path = kwargs["path"]
        signal = kwargs["signal"]
        if not path.startswith("/package/"):
            return
        script = path[9:]
        #print script, signal

    def listenSignals(self):
        self.busSys.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.Net.Filter", member_keyword="signal", path_keyword="path")

    def callMethod(self, method, action, model="Net.Filter"):
        ch = CallHandler("iptables", model, method,
                         action,
                         self.winId(),
                         self.busSys, self.busSes)
        ch.registerError(self.comarError)
        ch.registerAuthError(self.comarError)
        ch.registerDBusError(self.busError)
        ch.registerCancel(self.cancelError)
        return ch

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        KMessageBox.sorry(None, message, i18n("Error"))

    def busError(self, exception):
        KMessageBox.error(None, str(exception), i18n("D-Bus Error"))
        self.setupBusses()

    def comarError(self, exception):
        if "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.error(None, message, i18n("Error"))
        else:
            KMessageBox.error(None, str(exception), i18n("COMAR Error"))

    def slotChanged(self):
        if not standalone:
            self.changed()
        return

    def getState(self):
        def handleState(_type, _desc, _state):
            self.state = "off"
            mainwidget.pushStatus.setEnabled(True)
            if _state in ["on", "started"]:
                self.state = "on"
                mainwidget.frameIncoming.setEnabled(True)
                mainwidget.frameAdvanced.setEnabled(True)
                mainwidget.pushNewRule.setEnabled(True)
                self.getProfile()
                self.getRules()
            self.setState(self.state)
        ch = self.callMethod("info", "tr.org.pardus.comar.system.service.get", "System.Service")
        ch.registerDone(handleState)
        ch.call()

    def getProfile(self):
        def handleProfile(profile, save_filter, save_nat, save_mangle, save_raw):
            self.profile = {
                'profile': profile,
                'save_filter': save_filter,
                'save_mangle': save_nat,
                'save_nat': save_mangle,
                'save_raw': save_raw,
            }
        ch = self.callMethod("getProfile", "tr.org.pardus.comar.net.filter.get")
        ch.registerDone(handleProfile)
        ch.call()

    def getRules(self):
        def handleRules(rules):
            self.emptyRules()
            for rule in rules:
                if not len(rule):
                    continue
                table, rule = rule.split(' ', 1)
                self.rules[table].append(rule)
            self.updateRules()
        ch = self.callMethod("getRules", "tr.org.pardus.comar.net.filter.get")
        ch.registerDone(handleRules)
        ch.call()

    def setState(self, state):
        self.state = state
        if self.state == 'on': #and self.profile == rules.profile:
            mainwidget.pushStatus.setText(i18n('&Stop Firewall'))
            mainwidget.textStatus.setText(i18n('<b><font size=\'+1\'>Firewall is running</font></b>'))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(41, 182, 31))
            mainwidget.textStatus2.setText(i18n('Click here to stop the firewall and allow all incoming and outgoing connections.'))

            # Load FW rules
            self.getRules()
        else:
            mainwidget.pushStatus.setText(i18n('&Start Firewall'))
            mainwidget.textStatus.setText(i18n('<b><font size=\'+1\'>Firewall is not running</font></b>'))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(182, 41, 31))
            mainwidget.textStatus2.setText(i18n('Click here to start the firewall and allow connections only to specified services.'))
            self.updateRules()

    def updateRules(self):
        if self.state == 'on':
            rules_processed = []
            # Tab 1 - Incoming Connections
            for checkbox in self.incoming:
                rules_processed.extend(rules.filter[checkbox.name()][0])
                if not set(rules.filter[checkbox.name()][0]) - set(self.rules['filter']):
                    checkbox.setChecked(True)
                else:
                    checkbox.setChecked(False)
            # Tab 2 - Advanced
            for chk in self.advanced:
                chk.close(True)
            self.advanced = []
            for custom_rule in set(self.rules['filter']) - set(rules_processed):
                if "--dports" not in custom_rule:
                    continue
                chk = AdvancedRuleCheckBox(mainwidget.frameAdvanced, rule=custom_rule)
                chk.setChecked(True)
                mainwidget.frameAdvancedLayout.addWidget(chk)
                self.advanced.append(chk)
                chk.show()
                self.connect(chk, SIGNAL('clicked()'), self.slotChanged)

            mainwidget.frameIncoming.setEnabled(True)
            mainwidget.frameAdvanced.setEnabled(True)
            mainwidget.pushNewRule.setEnabled(True)
        else:
            mainwidget.frameIncoming.setEnabled(False)
            mainwidget.frameAdvanced.setEnabled(False)
            mainwidget.pushNewRule.setEnabled(False)

    def emptyRules(self):
        self.rules = {
            'filter': [],
            'mangle': [],
            'nat': [],
            'raw': []
        }

    def slotStatus(self):
        mainwidget.pushStatus.setEnabled(False)
        if self.state == 'on':
            def handleOk():
                self.setState("off")
                mainwidget.pushStatus.setEnabled(True)
            def handleCancel():
                self.setState("on")
                mainwidget.pushStatus.setEnabled(True)
            def handleError(e):
                self.setState("on")
                mainwidget.pushStatus.setEnabled(True)

            ch = self.callMethod("setState", "tr.org.pardus.comar.system.service.get", "System.Service")
            ch.call("off")

            ch = self.callMethod("stop", "tr.org.pardus.comar.system.service.set", "System.Service")
            ch.registerCancel(handleCancel)
            ch.registerError(handleError)
            ch.registerAuthError(handleError)
            ch.registerDBusError(handleError)
            ch.registerDone(handleOk)
            ch.call()
        else:
            def handleOk():
                def handleState():
                    self.setState("on")
                    mainwidget.pushStatus.setEnabled(True)

                ch = self.callMethod("setState", "tr.org.pardus.comar.system.service.get", "System.Service")
                ch.call("on")

                ch = self.callMethod("start", "tr.org.pardus.comar.system.service.set", "System.Service")
                ch.registerDone(handleState)
                ch.call()
            def handleCancel():
                self.setState("off")
                mainwidget.pushStatus.setEnabled(True)
            def handleError(e):
                self.setState("off")
                mainwidget.pushStatus.setEnabled(True)

            ch = self.callMethod("setProfile", "tr.org.pardus.comar.net.filter.set")
            ch.registerCancel(handleCancel)
            ch.registerError(handleError)
            ch.registerAuthError(handleError)
            ch.registerDBusError(handleError)
            ch.registerDone(handleOk)
            ch.call(rules.profile["profile"], rules.profile["save_filter"], rules.profile["save_mangle"], rules.profile["save_nat"], rules.profile["save_raw"])

    def slotOk(self):
        self.saveAll()
        self.close()

    def slotApply(self):
        self.saveAll()

    def slotDialog(self):
        dialog = dialogRule(mainwidget)
        rule = dialog.exec_loop()
        if rule:
            chk = AdvancedRuleCheckBox(mainwidget.frameAdvanced, rule=rule)
            chk.setChecked(True)
            mainwidget.frameAdvancedLayout.addWidget(chk)
            self.advanced.append(chk)
            chk.show()
            if not standalone:
                self.changed()
            self.connect(chk, SIGNAL('clicked()'), self.slotChanged)

    def setRule(self, table, rule):
        rule = '-t %s %s' % (table, rule)
        ch = self.callMethod("setRule", "tr.org.pardus.comar.net.filter.set")
        ch.call(rule)

    def saveRules(self, table, now):
        s1 = set(self.rules[table])
        s2 = set(now)

        for rule in s1 - s2:
            self.setRule(table, rule.replace('-A', '-D', 1))
            self.rules[table].remove(rule)

        for rule in s2 - s1:
            self.setRule(table, rule)
            self.rules[table].append(rule)

    def saveAll(self):
        now_filter = []

        # Tab 1 - Incoming Connections
        for checkbox in self.incoming:
            if checkbox.isChecked():
                now_filter.extend(rules.filter[checkbox.name()][0])

        # Tab 2 - Advanced
        for checkbox in self.advanced:
            if checkbox.isChecked():
                now_filter.append(checkbox.rule)

        self.saveRules('filter', now_filter)

    def __del__(self):
        pass

    def exec_loop(self):
        global programbase
        programbase.exec_loop(self)

    # KControl virtual void methods
    def load(self):
        pass

    def save(self):
        self.saveAll()

    def defaults(self):
        pass

    def sysdefaults(self):
        pass

    def aboutData(self):
        # Return the KAboutData object which we created during initialisation.
        return self.aboutdata

# This is the entry point used when running this module outside of kcontrol.
def main():
    global kapp

    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)

    if not KUniqueApplication.start():
        print i18n('Pardus Firewall Interface is already running!')
        return

    kapp = KUniqueApplication(True, True, True)
    myapp = MainApplication()
    kapp.setMainWidget(myapp)
    sys.exit(myapp.exec_loop())

# Factory function for KControl
def create_firewall_config(parent,name):
    global kapp

    kapp = KApplication.kApplication()
    if not dbus.get_default_main_loop():
        dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
    return MainApplication(parent, name)

if standalone:
    main()
