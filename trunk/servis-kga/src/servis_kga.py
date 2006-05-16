#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

# Python Modules
import os
import sys
import time

# KDE/QT Modules
from qt import *
from kdecore import *
from kdeui import *
from khtml import *

# Widget
import serviceWidget

# COMAR
import comar


def AboutData():
    about_data = KAboutData('servis_kga',
                            'Service Manager',
                            '1.0.2',
                            'Service Manager Interface',
                            KAboutData.License_GPL,
                            '(C) 2006 UEKAE/TÜBİTAK',
                            None, None,
                            'bahadir@pardus.org.tr')
    
    about_data.addAuthor('Bahadır Kandemir', None, 'bahadir@pardus.org.tr')
    
    return about_data


def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)


# Are we running as a separate standalone application or in KControl?
standalone = __name__=='__main__'


if standalone:
    programbase = QDialog
else:
    programbase = KCModule


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(i18n('Service Manager'))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 300)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)

        if os.environ['LANG'].startswith('tr_TR'):
            self.htmlPart.openURL(KURL(locate('data', 'servis_kga/help/tr/main_help.html')))
        else:
            self.htmlPart.openURL(KURL(locate('data', 'servis_kga/help/en/main_help.html')))


class serviceItem(KListViewItem):
    def __init__(self, parent=None, name=None, type='server', state='off', package=''):
        KListViewItem.__init__(self, parent)
        self.service = package
        self.type = type

        self.setState(state)

        self.setText(1, name)
        self.setText(2, i18n(type.title()))
        self.setText(4, package)

        if self.type != "server":
            self.setEnabled(0)

    def setState(self, state='off'):
        self.status = state
        if state in ['on', 'started']:
            self.setPixmap(0, loadIcon('ledgreen'))
            if state == "on":
                self.setPixmap(3, loadIcon('button_ok', size=16))
        else:
            self.setPixmap(0, loadIcon('ledred'))
            if state == "off":
                self.setPixmap(3, loadIcon('button_cancel', size=16))


class MainApplication(programbase):
    def __init__(self, parent=None, name=None):
        global standalone

        if standalone:
            QDialog.__init__(self, parent, name)
            self.setCaption(i18n('Service Manager'))
            self.setMinimumSize(520, 420)
            self.resize(520, 420)
        else:
            KCModule.__init__(self, parent, name)
            KGlobal.locale().insertCatalogue('servis_kga')
            # Create a configuration object.
            self.config = KConfig('servis_kga')
            self.setButtons(0)
            self.aboutdata = AboutData()

        self.setIcon(loadIcon('servis_kga', size=128))

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir('servis_kga')
        
        # Initialize main widget
        self.mainwidget = serviceWidget.serviceWidget(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(self.mainwidget)

        # Initialize Comar
        self.comar = comar.Link()

        # Populate list
        self.populateList()
       
        # Notify list
        self.comar.ask_notify('System.Service.changed', id=1)
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)

        # Connections
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)
        self.connect(self.mainwidget.listServices, SIGNAL('selectionChanged(QListViewItem*)'), self.slotItemClicked)
        self.connect(self.mainwidget.pushSwitch, SIGNAL('clicked()'), self.slotSwitch)
        self.connect(self.mainwidget.pushHelp, SIGNAL('clicked()'), self.slotHelp)
        self.connect(self.mainwidget.listServices, SIGNAL('doubleClicked(QListViewItem*, const QPoint&, int)'), self.slotItemDBClicked)

    def handleComar(self, reply):
        if reply[0] == self.comar.RESULT_START:
            self.handleComar(self.comar.read_cmd())
        elif reply[0] == self.comar.NOTIFY:
            item = self.mainwidget.listServices.firstChild()
            info = reply[2].split('\n')

            while item:
                if item.service == info[1]:
                    item.setState(info[2])
                    break
                item = item.nextSibling()

            list = self.mainwidget.listServices
            if list.selectedItem():
                self.slotItemClicked(list.selectedItem())
        elif reply[0] == self.comar.RESULT:
            if reply[1] == 2:
                info = reply[2].split('\n')
                serviceItem(self.mainwidget.listServices, info[2], info[0], info[1], reply[3])

    def populateList(self):
        self.comar.call('System.Service.info', id=2)
        self.handleComar(self.comar.read_cmd())

    def slotComar(self, sock):
        self.handleComar(self.comar.read_cmd())

    def slotItemDBClicked(self, item, pos, col):
        if col == 3 and item and item.type == "server":
            if item.status in ['on', 'stopped']:
                self.comar.call_package('System.Service.setState', item.service, {"state": "off"})
            else:
                self.comar.call_package('System.Service.setState', item.service, {"state": "on"})
            self.handleComar(self.comar.read_cmd())

    def slotItemClicked(self, item):
        self.mainwidget.pushSwitch.setEnabled(1)
        if item.status == 'stopped':
            self.mainwidget.pushSwitch.setText(i18n('Start'))
        else:
            self.mainwidget.pushSwitch.setText(i18n('Stop'))

    def slotSwitch(self):
        self.mainwidget.pushSwitch.setEnabled(0)
        list = self.mainwidget.listServices
        if list.selectedItem().status == 'stopped':
            self.comar.call_package('System.Service.start', list.selectedItem().service)
        else:
            self.comar.call_package('System.Service.stop', list.selectedItem().service)

    def slotHelp(self):
        self.helpwin = HelpDialog(self)
        self.helpwin.show()

    def __del__(self):
        pass

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
        return self.aboutdata
    
    def buttons(self):
        return KCModule.Help


def main():
    global kapp
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    if not KUniqueApplication.start():
        print i18n("Service GUI is already running!")
        return
    kapp = KUniqueApplication(True, True, True)
    myapp = MainApplication()
    kapp.setMainWidget(myapp)
    sys.exit(myapp.exec_loop())


# Factory function for KControl
def create_servis_kga(parent, name):
    global kapp    
    kapp = KApplication.kApplication()
    return MainApplication(parent, name)

if standalone:
    main()
