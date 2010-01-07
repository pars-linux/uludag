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
import comar
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
    def __init__(self, parent=None, name=None, ports=''):
        QCheckBox.__init__(self, parent, name)
        self.ports = ports
        msg = i18n('Reject all outgoing connection through ports %s')
        self.setText(msg.replace('%s', ports.replace(':', '-')))

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
            ports = self.linePorts.text().replace('-', ':')
            ports = ports.replace(' ', '')

            return ports
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
        for key, (name, ports) in rules.filter.iteritems():
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
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("Network.Firewall", self.handleSignals)
        self.link.listenSignals("System.Service", self.handleSignals)

        # Signals
        self.connect(mainwidget.pushStatus, SIGNAL('clicked()'), self.slotStatus)
        self.connect(mainwidget.pushCancel, SIGNAL('clicked()'), self, SLOT('close()'))
        self.connect(mainwidget.pushOk, SIGNAL('clicked()'), self.slotOk)
        self.connect(mainwidget.pushApply, SIGNAL('clicked()'), self.slotApply)
        self.connect(mainwidget.pushNewRule, SIGNAL('clicked()'), self.slotDialog)

        # Init
        self.getState()

    def handleSignals(self, package, signal, args):
        pass

    def slotChanged(self):
        if not standalone:
            self.changed()
        return

    def getState(self):
        def handleState(package, exception, args):
            _state = args[0]
            self.state = "off"
            mainwidget.pushStatus.setEnabled(True)
            if _state  == "on":
                self.state = "on"
                self.getRules()
            self.setState(self.state)
        self.link.Network.Firewall["iptables"].getState(async=handleState)

    def getRules(self):
        def handleIncoming(package, exception, args):
            if exception:
                return
            ports = args[0].get("port_exceptions", "").split()
            for checkbox in self.incoming:
                if not set(rules.filter[checkbox.name()][1].split()) - set(ports):
                    checkbox.setChecked(True)
                else:
                    checkbox.setChecked(False)
        self.link.Network.Firewall["iptables"].getModuleParameters("block_incoming", async=handleIncoming)

        def handleOutgoing(package, exception, args):
            if exception:
                return
            ports = args[0].get("port_exceptions", "").split()
            for chk in self.advanced:
                chk.close(True)
            self.advanced = []
            for port in ports:
                chk = AdvancedRuleCheckBox(mainwidget.frameAdvanced, ports=port)
                chk.setChecked(True)
                mainwidget.frameAdvancedLayout.addWidget(chk)
                self.advanced.append(chk)
                chk.show()
                self.connect(chk, SIGNAL('clicked()'), self.slotChanged)
        self.link.Network.Firewall["iptables"].getModuleParameters("block_outgoing", async=handleOutgoing)

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
            mainwidget.frameIncoming.setEnabled(True)
            mainwidget.frameAdvanced.setEnabled(True)
            mainwidget.pushNewRule.setEnabled(True)
        else:
            mainwidget.frameIncoming.setEnabled(False)
            mainwidget.frameAdvanced.setEnabled(False)
            mainwidget.pushNewRule.setEnabled(False)

    def slotStatus(self):
        mainwidget.pushStatus.setEnabled(False)
        if self.state == 'on':
            def handleState(package, exception, args):
                if exception:
                    self.setState("on")
                    mainwidget.pushStatus.setEnabled(True)
                else:
                    self.setState("off")
                    mainwidget.pushStatus.setEnabled(True)
                    self.link.Network.Firewall["iptables"].setModuleState("block_incoming", "off")
                    self.link.Network.Firewall["iptables"].setModuleState("block_outgoing", "off")

            self.link.Network.Firewall["iptables"].setState("off", async=handleState)
        else:
            def handleState(package, exception, args):
                if exception:
                    self.setState("off")
                    mainwidget.pushStatus.setEnabled(True)
                else:
                    self.setState("on")
                    mainwidget.pushStatus.setEnabled(True)
                    self.link.Network.Firewall["iptables"].setModuleState("block_incoming", "on")
                    self.link.Network.Firewall["iptables"].setModuleState("block_outgoing", "on")

            self.link.Network.Firewall["iptables"].setState("on", async=handleState)

    def slotOk(self):
        self.saveAll()
        self.close()

    def slotApply(self):
        self.saveAll()

    def slotDialog(self):
        dialog = dialogRule(mainwidget)
        ports = dialog.exec_loop()
        if ports:
            ports = str(ports)
            chk = AdvancedRuleCheckBox(mainwidget.frameAdvanced, ports=ports)
            chk.setChecked(True)
            mainwidget.frameAdvancedLayout.addWidget(chk)
            self.advanced.append(chk)
            chk.show()
            if not standalone:
                self.changed()
            self.connect(chk, SIGNAL('clicked()'), self.slotChanged)

    def setRule(self, table, rule):
        rule = '-t %s %s' % (table, rule)
        self.link.Net.Filter["iptables"].setRule(rule)

    def saveAll(self):
        # Tab 1 - Incoming Connections
        ports = []
        for checkbox in self.incoming:
            if checkbox.isChecked():
                ports.extend(rules.filter[checkbox.name()][1].split(","))
        self.link.Network.Firewall["iptables"].setModuleParameters("block_incoming", {"port_exceptions": " ".join(ports)})

        # Tab 2 - Advanced
        ports = []
        for checkbox in self.advanced:
            if checkbox.isChecked():
                ports.append(checkbox.ports)
        self.link.Network.Firewall["iptables"].setModuleParameters("block_outgoing", {"port_exceptions": " ".join(ports)})

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
