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

# COMAR
import comar

# Rules
import rules

def I18N_NOOP(str):
    return str

description = I18N_NOOP('Pardus Firewall Graphical User Interface')
version = '1.6.5'

def AboutData():
    global version, description

    about_data = KAboutData('firewall-config',
                            'Firewal Configuration',
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

    def accept(self):
        if checkPortFormat(str(self.linePorts.text())):
            dialog.dialogRule.accept(self)
        else:
            QMessageBox.critical(self, i18n('Error'), i18n('Invalid port range.'))

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
        for key, (list_rules, name) in rules.filter.iteritems():
            if key.startswith('in'):
                chk = QCheckBox(mainwidget.frameIncoming, key)
                chk.setText(i18n(name))
                frameIncomingLayout.addWidget(chk)
                self.incoming.append(chk)
                self.connect(chk, SIGNAL('clicked()'), self.slotChanged)

        # Icons
        self.setIcon(loadIcon('firewall_config', size=48))
        mainwidget.pixmapFW.setPixmap(loadIcon('firewall_config', size=48))
        mainwidget.pixmapIncoming.setPixmap(loadIcon('server.png', size=48))
        mainwidget.pixmapAdvanced.setPixmap(loadIcon('gear.png', size=48))
        mainwidget.pushNewRule.setPixmap(loadIcon('add.png', size=32))

        # COMAR
        self.comar = comar.Link()
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)

        # COMAR - Notify List
        self.comar.ask_notify('Net.Filter.changed', id=1)

        # Access Control
        self.wheel = False
        self.comar.can_access('System.Service.setState', id=10)

        # Signals
        self.connect(mainwidget.pushStatus, SIGNAL('clicked()'), self.slotStatus)
        self.connect(mainwidget.pushCancel, SIGNAL('clicked()'), self, SLOT('close()'))
        self.connect(mainwidget.pushOk, SIGNAL('clicked()'), self.slotOk)
        self.connect(mainwidget.pushApply, SIGNAL('clicked()'), self.slotApply)
        self.connect(mainwidget.pushNewRule, SIGNAL('clicked()'), self.slotDialog)

        # Get FW state
        self.comar.call('Net.Filter.getProfile', id=4)

        self.comar.call('Net.Filter.getState', id=3)

    def slotChanged(self):
        if not standalone:
            self.changed()

    def setState(self, state):
        self.state = state
        if self.state == 'on' and self.profile == rules.profile:
            mainwidget.pushStatus.setText(i18n('&Stop Firewall'))
            mainwidget.textStatus.setText(i18n('<b><font size=\'+1\'>Firewall is running</font></b>'))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(41, 182, 31))
            mainwidget.textStatus2.setText(i18n('Click here to stop the firewall and allow all incoming and outgoing connections.'))

            # Load FW rules
            self.comar.call('Net.Filter.getRules', id=2)
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
                chk = AdvancedRuleCheckBox(mainwidget.frameAdvanced, rule=custom_rule)
                chk.setChecked(True)
                mainwidget.frameAdvancedLayout.addWidget(chk)
                self.advanced.append(chk)
                chk.show()
                self.connect(chk, SIGNAL('clicked()'), self.slotChanged)

            if self.wheel:
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


    def slotComar(self, sock):
        reply = self.comar.read_cmd()
        if reply.command == 'notify':
            # State changed
            info = reply.data.split('\n')
            if info[0] == 'state':
                self.setState(info[1])
                if self.wheel:
                    mainwidget.pushStatus.setEnabled(True)
            elif info[0] == 'profile':
                self.profile = {
                    'profile': info[1],
                    'save_filter': info[2],
                    'save_mangle': info[3],
                    'save_nat': info[4],
                    'save_raw': info[5],
                }
        elif reply.command == 'result':
            if reply.id == 2:
                # Get Rules
                self.emptyRules()
                for rule in reply.data.split('\n'):
                    if not rule:
                        continue
                    table, rule = rule.split(' ', 1)
                    self.rules[table].append(rule)
                self.updateRules()
            elif reply.id == 3:
                # Get State
                self.setState(reply.data)
                if self.wheel:
                    mainwidget.pushStatus.setEnabled(True)
            elif reply.id == 4:
                # Get Profile
                info = reply.data.split('\n')
                self.profile = {
                    'profile': info[0],
                    'save_filter': info[1],
                    'save_mangle': info[2],
                    'save_nat': info[3],
                    'save_raw': info[4],
                }
            elif reply.id == 10:
                self.wheel = True
                mainwidget.pushStatus.setEnabled(True)
                mainwidget.frameIncoming.setEnabled(True)
                mainwidget.frameAdvanced.setEnabled(True)
                mainwidget.pushNewRule.setEnabled(True)
        elif reply.command == 'fail':
            if reply.id == 5:
                if self.wheel:
                    mainwidget.pushStatus.setEnabled(True)
        elif reply.command == "denied":
            KMessageBox.error(self, i18n("You are not allowed to edit firewall settings."), i18n("Access Denied"))


    def slotStatus(self):
        mainwidget.pushStatus.setEnabled(False)
        if self.state == 'on':
            self.comar.call('Net.Filter.setState', {'state': 'off'}, id=5)
        else:
            self.comar.call('Net.Filter.setProfile', rules.profile, id=6)
            self.comar.call('Net.Filter.setState', {'state': 'on'}, id=5)

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
        self.comar.call('Net.Filter.setRule', {'rule': rule}, id=10)

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
    return MainApplication(parent, name)

if standalone:
    main()
