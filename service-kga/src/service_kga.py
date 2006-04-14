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
    about_data = KAboutData('service_kga',
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


class MainApplication(programbase):
    def __init__(self, parent=None, name=None):
        global standalone

        if standalone:
            QDialog.__init__(self, parent, name)
            self.setCaption(i18n("Service Manager"))
            self.setMinimumSize(520, 420)
            self.resize(520, 420)
        else:
            KCModule.__init__(self, parent, name)
            KGlobal.locale().insertCatalogue("service_kga")
            # Create a configuration object.
            self.config = KConfig("service_kga")
            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("service_kga")
        
        # Initialize main widget
        self.mainwidget = serviceWidget.serviceWidget(self)
        toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
        toplayout.addWidget(self.mainwidget)

        # Initialize Comar
        self.comar = comar.Link()

        # Populate list
        self.populateList()
       
        # Notify lists
        self.comar.ask_notify('System.Service.changed')
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)
        
        # Connections
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        self.connect(self.mainwidget.pushStart, SIGNAL("clicked()"), self.slotStart)
        self.connect(self.mainwidget.pushStop, SIGNAL("clicked()"), self.slotStop)

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
                    replies.append(reply)
            else:
                return [reply]

        self.mainwidget.listServices.clear()
        for service in collect(self.comar):
            info = service[2].split('\n')

            item = KListViewItem(self.mainwidget.listServices, None)
            
            if info[1] in ['on', 'started']:
                item.setPixmap(0, loadIcon('ledgreen'))
            elif info[1] in ['off', 'stopped']:
                item.setPixmap(0, loadIcon('ledred'))
                
            item.setText(1, service[3])
            item.setText(2, i18n(info[0].title()))
            if info[1] in ['on', 'stopped']:
                item.setText(3, i18n('Yes'))
            else:
                item.setText(3, i18n('No'))
            item.setText(4, info[2])
            

    def slotComar(self, sock):
        info = self.comar.read_cmd()[2].split('\n')
        item = self.mainwidget.listServices.firstChild()
        while item:
            if item.text(1) == info[1]:
                if info[2] == 'started':
                    item.setPixmap(0, loadIcon('ledgreen'))
                elif info[2] == 'stopped':
                    item.setPixmap(0, loadIcon('ledred'))
                return
            item = item.nextSibling()

    def slotStart(self):
        pass

    def slotStop(self):
        pass

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
        print i18n("Service KGA is already running!")
        return
    kapp = KUniqueApplication(True, True, True)
    myapp = MainApplication()
    kapp.setMainWidget(myapp)
    sys.exit(myapp.exec_loop())


# Factory function for KControl
def create_service_kga(parent, name):
    global kapp    
    kapp = KApplication.kApplication()
    return MainApplication(parent, name)

if standalone:
    main()
