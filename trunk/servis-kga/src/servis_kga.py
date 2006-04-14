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
import sys
import time

# KDE/QT Modules
from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

# Widget
import serviceWidget

# COMAR
import comar


def AboutData():
    about_data = KAboutData('servis_kga',
                            'Service Manager',
                            '0.1',
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


class serviceItem(KListViewItem):
    def __init__(self, parent=None, name=None, type='server', state='off', description=''):
        KListViewItem.__init__(self, parent)
        self.name = name

        if state in ['on', 'started']:
            self.start()
        else:
            self.stop()
            
        self.setText(1, name)
        self.setText(2, i18n(type.title()))
        
        if state in ['on', 'stopped']:
            self.setText(3, i18n('Yes'))
        else:
            self.setText(3, i18n('No'))

        self.setText(4, description)

    def start(self):
        self.status = 'started'
        self.setPixmap(0, loadIcon('ledgreen'))
        
    def stop(self):
        self.status = 'stopped'
        self.setPixmap(0, loadIcon('ledred'))

    def setState(self, state='off'):
        if state in ['on', 'started']:
            self.start()
        else:
            self.stop()

        if state in ['on', 'stopped']:
            self.setText(3, i18n('Yes'))
        else:
            self.setText(3, i18n('No'))


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
       
        # Notify lists
        self.comar.ask_notify('System.Service.changed')
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)

        # Disable switch button
        self.mainwidget.pushSwitch.setEnabled(0)

        # Connections
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)
        self.connect(self.mainwidget.listServices, SIGNAL('selectionChanged(QListViewItem*)'), self.slotItemClicked)
        self.connect(self.mainwidget.pushSwitch, SIGNAL('clicked()'), self.slotSwitch)

    def populateList(self):
        self.comar.call('System.Service.info')

        def collect(c):
            reply = c.read_cmd()
            if reply[0] == c.RESULT_START:
                replies = []
                while True:
                    reply = c.read_cmd()
                    if reply[0] == c.RESULT_END:
                        return replies
                    if reply[0] == c.RESULT:
                        replies.append(reply)
            else:
                return [reply]

        #self.mainwidget.listServices.clear()
        for service in collect(self.comar):
            info = service[2].split('\n')
            serviceItem(self.mainwidget.listServices, service[3], info[0], info[1], info[2])

    def slotComar(self, sock):
        service = self.comar.read_cmd()[3]
        item = self.mainwidget.listServices.firstChild()
        time.sleep(1)
        self.comar.call_package('System.Service.info', service)
        state = self.comar.read_cmd()[2].split('\n')[1]

        while item:
            if item.name == service:
                item.setState(state)
                self.slotItemClicked(item)
                break
            item = item.nextSibling()
        self.mainwidget.pushSwitch.setEnabled(1)

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
            self.comar.call_package('System.Service.start', list.selectedItem().name)
        else:
            self.comar.call_package('System.Service.stop', list.selectedItem().name)

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
