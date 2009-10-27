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
from rules import named_rules

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
            self.setMinimumSize(566, 544)
            self.resize(566, 544)
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

        mainwidget.pushStatus.setEnabled(False)

        # Icons
        mainwidget.pixmapFW.setPixmap(loadIcon('firewall_config', size=48))
        mainwidget.pixmapIncoming.setPixmap(loadIcon('krfb.png', size=48))

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
        self.state = 'off'
        self.profile = ''
        self.rules = {}

        self.comar.call('Net.Filter.getProfile', id=4)
        self.handleComar(self.comar.read_cmd())

        self.comar.call('Net.Filter.getState', id=3)
        self.handleComar(self.comar.read_cmd())

    def slotComar(self, sock):
        self.handleComar(self.comar.read_cmd())

    def setState(self, state):
        self.state = state
        if self.state == 'on' and self.profile == 'pardus':
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
            mainwidget.frameCheckBoxes.setEnabled(False)

    def updateCheckBoxes(self):
        mainwidget.frameCheckBoxes.setEnabled(True)
        inRule = '-A PARDUS-USER %s -j ACCEPT'
        for named in named_rules:
            checkbox = eval('mainwidget.check%s' % named)
            if 'filter' in self.rules and inRule % named_rules[named] in self.rules['filter']:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

    def handleComar(self, reply):
        if reply.command == 'notify':
            # State changed
            info = reply.data.split('\n')
            if info[0] == 'state':
                self.setState(info[1])
                mainwidget.pushStatus.setEnabled(True)
            elif info[0] == 'profile':
                self.profile = info[1]
        elif reply.command == 'result':
            if reply.id == 2:
                # Get Rules
                self.rules = {}
                for rule in reply.data.split('\n'):
                    if not rule:
                        continue
                    table, rule = rule.split(' ', 1)
                    if table not in self.rules:
                        self.rules[table] = []
                    self.rules[table].append(rule)
                self.updateCheckBoxes()
            elif reply.id == 3:
                # Get State
                self.setState(reply.data)
                mainwidget.pushStatus.setEnabled(True)
            elif reply.id == 4:
                # Get Profile
                self.profile = reply.data.split('\n')[0]
        elif reply.command == 'fail':
            if reply.id == 5:
                mainwidget.pushStatus.setEnabled(True)


    def slotStatus(self):
        mainwidget.pushStatus.setEnabled(False)
        if self.state == 'on':
            self.comar.call('Net.Filter.setState', {'state': 'off'}, id=5)
            self.handleComar(self.comar.read_cmd())
        else:
            self.comar.call('Net.Filter.setProfile', {'profile': 'pardus', 'save_filter': 'PARDUS-USER'}, id=6)
            self.handleComar(self.comar.read_cmd())
            self.comar.call('Net.Filter.setState', {'state': 'on'}, id=5)
            self.handleComar(self.comar.read_cmd())

    def slotOk(self):
        self.saveAll()
        self.close()

    def slotApply(self):
        self.saveAll()


    def saveAll(self):
        if 'filter' not in self.rules:
            self.rules['filter'] = []
        s1 = self.rules['filter']
        s2 = []

        inRule = '-A PARDUS-USER %s -j ACCEPT'

        for named in named_rules:
            checkbox = eval('mainwidget.check%s' % named)
            if checkbox.isChecked():
                s2.append(inRule % named_rules[named])

        s1 = set(s1)
        s2 = set(s2)

        for rule in s1 - s2:
            self.setRule(rule.replace('-A PARDUS-USER', '-D PARDUS-USER'))
            self.rules['filter'].remove(rule)

        for rule in s2 - s1:
            self.setRule(rule)
            self.rules['filter'].append(rule)

    def setRule(self, rule):
        self.comar.call('Net.Filter.setRule', {'rule': rule}, id=10)
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
        print i18n('Pardus Firewall Interface is already running!')
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
