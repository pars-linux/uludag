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

# COMAR
import comar

# Rules
import rules

def I18N_NOOP(str):
    return str

description = I18N_NOOP('Pardus Firewall Graphical User Interface')
version = '1.6.0'

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
            self.setButtons(0)
            self.aboutdata = AboutData()

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

        # Tab 1 - Incoming Connections
        self.incoming = []
        mainwidget.frameIncoming.setColumnLayout(0, Qt.Vertical)
        frameIncomingLayout = QVBoxLayout(mainwidget.frameIncoming.layout())
        frameIncomingLayout.setAlignment(Qt.AlignTop)

        # Tab 2 - Ingoing Connections
        self.outgoing = []
        mainwidget.frameOutgoing.setColumnLayout(0, Qt.Vertical)
        frameOutgoingLayout = QVBoxLayout(mainwidget.frameOutgoing.layout())
        frameOutgoingLayout.setAlignment(Qt.AlignTop)

        # Populate checkboxes
        for key, (rule, name) in rules.filter.iteritems():
            if key.startswith('in'):
                chk = QCheckBox(mainwidget.frameIncoming, key)
                chk.setText(name)
                frameIncomingLayout.addWidget(chk)
                self.incoming.append(chk)
            elif key.startswith('out'):
                chk = QCheckBox(mainwidget.frameOutgoing, key)
                chk.setText(name)
                frameOutgoingLayout.addWidget(chk)
                self.outgoing.append(chk)

        # Icons
        self.setIcon(loadIcon('firewall_config', size=48))
        mainwidget.pixmapFW.setPixmap(loadIcon('firewall_config', size=48))
        mainwidget.pixmapIncoming.setPixmap(loadIcon('server.png', size=48))
        mainwidget.pixmapOutgoing.setPixmap(loadIcon('socket.png', size=48))

        # COMAR
        self.comar = comar.Link()

        # COMAR - Notify List
        self.comar.ask_notify('Net.Filter.changed', id=1)
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)

        # Signals
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)
        self.connect(mainwidget.pushStatus, SIGNAL('clicked()'), self.slotStatus)

        self.connect(mainwidget.pushCancel, SIGNAL('clicked()'), self, SLOT('close()'))
        self.connect(mainwidget.pushOk, SIGNAL('clicked()'), self.slotOk)
        self.connect(mainwidget.pushApply, SIGNAL('clicked()'),self.slotApply)

        # Get FW state
        self.comar.call('Net.Filter.getProfile', id=4)
        self.handleComar(self.comar.read_cmd())

        self.comar.call('Net.Filter.getState', id=3)
        self.handleComar(self.comar.read_cmd())

    def slotComar(self, sock):
        self.handleComar(self.comar.read_cmd())

    def setState(self, state):
        self.state = state
        if self.state == 'on' and self.profile == rules.profile:
            mainwidget.pushStatus.setText(i18n('&Stop Firewall'))
            mainwidget.textStatus.setText(i18n('<b><font size=\'+1\'>Firewall is running</font></b>'))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(41, 182, 31))
            mainwidget.textStatus2.setText(i18n('Click here to stop the firewall and allow all incoming and outgoing connections.'))

            # Load FW rules
            self.comar.call('Net.Filter.getRules', id=2)
            self.handleComar(self.comar.read_cmd())
        else:
            mainwidget.pushStatus.setText(i18n('&Start Firewall'))
            mainwidget.textStatus.setText(i18n('<b><font size=\'+1\'>Firewall is not running</font></b>'))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(182, 41, 31))
            mainwidget.textStatus2.setText(i18n('Click here to start the firewall and allow connections only to specified services.'))
            self.updateRules()

    def updateRules(self):
        if self.state == 'on':
            # Tab 1 - Incoming Connections
            for checkbox in self.incoming:
                if rules.filter[checkbox.name()][0] in self.rules['filter']:
                    checkbox.setChecked(True)
                else:
                    checkbox.setChecked(False)
            # Tab 2 - Incoming Connections
            for checkbox in self.outgoing:
                if rules.filter[checkbox.name()][0] in self.rules['filter']:
                    checkbox.setChecked(True)
                else:
                    checkbox.setChecked(False)
            mainwidget.frameIncoming.setEnabled(True)
            mainwidget.frameOutgoing.setEnabled(True)
        else:
            mainwidget.frameIncoming.setEnabled(False)
            mainwidget.frameOutgoing.setEnabled(False)

    def emptyRules(self):
        self.rules = {
            'filter': [],
            'mangle': [],
            'nat': [],
            'raw': []
        }

    def handleComar(self, reply):
        if reply.command == 'notify':
            # State changed
            info = reply.data.split('\n')
            if info[0] == 'state':
                self.setState(info[1])
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
        elif reply.command == 'fail':
            if reply.id == 5:
                mainwidget.pushStatus.setEnabled(True)


    def slotStatus(self):
        mainwidget.pushStatus.setEnabled(False)
        if self.state == 'on':
            self.comar.call('Net.Filter.setState', {'state': 'off'}, id=5)
            self.handleComar(self.comar.read_cmd())
        else:
            self.comar.call('Net.Filter.setProfile', rules.profile, id=6)
            self.handleComar(self.comar.read_cmd())
            self.comar.call('Net.Filter.setState', {'state': 'on'}, id=5)
            self.handleComar(self.comar.read_cmd())

    def slotOk(self):
        self.saveAll()
        self.close()

    def slotApply(self):
        self.saveAll()

    def setRule(self, table, rule):
        rule = '-t %s %s' % (table, rule)
        self.comar.call('Net.Filter.setRule', {'rule': rule}, id=10)
        self.handleComar(self.comar.read_cmd())

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
                now_filter.append(rules.filter[checkbox.name()][0])

        # Tab 2 - Outgoing Connections
        for checkbox in self.outgoing:
            if checkbox.isChecked():
                now_filter.append(rules.filter[checkbox.name()][0])

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
