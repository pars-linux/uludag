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
import kdedesigner
from mainform import mainForm

# COMAR
import comar

version = '1.1'

def AboutData():
    about_data = KAboutData('service-manager',
                            'Service Manager',
                            version,
                            'Service Manager Interface',
                            KAboutData.License_GPL,
                            '(C) 2006 UEKAE/TÜBİTAK',
                            None, None,
                            'bahadir@pardus.org.tr')
    about_data.addAuthor('Bahadır Kandemir', None, 'bahadir@pardus.org.tr')
    return about_data


def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)


def loadIconSet(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIconSet(name, group, size)


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(i18n('Service Manager'))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 300)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)

        if os.environ['LANG'].startswith('tr_TR'):
            self.htmlPart.openURL(KURL(locate('data', 'service-manager/help/tr/main_help.html')))
        else:
            self.htmlPart.openURL(KURL(locate('data', 'service-manager/help/en/main_help.html')))


class serviceItem(KListViewItem):
    def __init__(self, parent=None, name=None, type='server', state='off', package='', description=''):
        KListViewItem.__init__(self, parent)
        self.type = type
        self.status = ''
        self.service = package
        self.description = description
        self.setText(1, description)
        self.setState(state)
        self.setVisible(False)

    def setState(self, state='off'):
        self.status = state
        if state in ['on', 'started']:
            self.setPixmap(0, loadIcon('player_play'))
        elif state == 'stopped':
            self.setPixmap(0, loadIcon('player_pause'))
        else:
            self.setPixmap(0, loadIcon('player_stop'))

    def compare(self, other, col, asc):
        s1 = self.status in ['on', 'started']
        s2 = other.status in ['on', 'started']
        if col == 0:
            if s1 == s2:
                return 0
            elif s1 > s2:
                return 1
            else:
                return -1
        else:
            return QListViewItem.compare(self, other, col, asc)


class servicesForm(mainForm):
    def __init__(self, parent=None, name=None):
        mainForm.__init__(self, parent, name)

        self.listServices.setSorting(1)
        self.listServices.setColumnText(0, '')

        self.buttonStart.setIconSet(loadIconSet('player_play', size=32))
        self.buttonPause.setIconSet(loadIconSet('player_pause', size=32))
        self.buttonStop.setIconSet(loadIconSet('player_stop', size=32))

        # Initialize Comar
        self.comar = comar.Link()

        # Populate list
        self.populateList()

        # Notify list
        self.comar.ask_notify('System.Service.changed', id=1)
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)

        # Connections
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)
        self.connect(self.checkServersOnly, SIGNAL('clicked()'), self.slotListServers)
        self.connect(self.listServices, SIGNAL('selectionChanged()'), self.slotSelectionChanged)

        self.connect(self.buttonStart, SIGNAL('clicked()'), self.slotStart)
        self.connect(self.buttonPause, SIGNAL('clicked()'), self.slotPause)
        self.connect(self.buttonStop, SIGNAL('clicked()'), self.slotStop)

    def handleComar(self, reply):
        if reply[0] == self.comar.RESULT_START:
            # ask for more
            self.handleComar(self.comar.read_cmd())
        elif reply[0] == self.comar.NOTIFY:
            # get more information with System.Service.info
            info = reply[2].split('\n')
            self.getServiceStatus(info[1])
        elif reply[0] == self.comar.RESULT:
            info = reply[2].split('\n')
            if reply[1] == 2:
                # add to list
                self.addServiceItem(reply)
            elif reply[1] == 3:
                item = self.listServices.firstChild()
                while item:
                    if item.service == reply[3]:
                        # update item
                        item.setState(info[1])
                        if item == self.listServices.selectedItem():
                            self.updateItemStatus(item)
                        break
                    item = item.nextSibling()
                if not item:
                    # new service, add to list
                    self.addServiceItem(reply)
            elif reply[1] == 4:
                # get more information with System.Service.info
                self.getServiceStatus(reply[3])
        elif reply[0] == self.comar.DENIED:
            KMessageBox.error(self, i18n('You are not allowed to do this operation.'), i18n('Access Denied'))
        elif reply[0] == self.comar.ERROR:
            KMessageBox.error(self, i18n('COMAR script execution failed.'), i18n('Script Error'))
        elif reply[0] == self.comar.FAIL:
            if reply[2] == 'Unable to start service':
                KMessageBox.error(self, i18n('Unable to start service.'), i18n('Failed'))
            elif reply[2] == 'Unable to stop service':
                KMessageBox.error(self, i18n('Unable to stop service.'), i18n('Failed'))
            else:
                KMessageBox.error(self, i18n('Unable to complete operation:\n%s') % reply[2], i18n('Failed'))
            item = self.listServices.selectedItem()
            if item:
                self.updateItemStatus(item)

    def populateList(self):
        self.comar.call('System.Service.info', id=2)
        self.handleComar(self.comar.read_cmd())

    def addServiceItem(self, reply):
        info = reply[2].split('\n')
        si = serviceItem(self.listServices, reply[3], info[0], info[1], reply[3], info[2])
        if not self.checkServersOnly.isChecked() or info[0] == 'server':
            si.setVisible(True)

    def getServiceStatus(self, service):
        item = self.listServices.firstChild()
        while item:
            if item.service == service:
                # give comar time to update service status
                time.sleep(0.5)
                self.comar.call_package('System.Service.info', item.service, id=3)
                self.handleComar(self.comar.read_cmd())
                break
            item = item.nextSibling()

    def updateItemStatus(self, item):
        if not item:
            self.buttonStart.setEnabled(False)
            self.buttonPause.setEnabled(False)
            self.buttonStop.setEnabled(False)
            self.textInformation.setText('')
            return

        self.buttonStart.setEnabled(item.status in ['off', 'stopped'])
        self.buttonPause.setEnabled(item.status in ['on', 'started'])
        self.buttonStop.setEnabled(item.status in ['on', 'stopped'])

        info = []
        if item.status in ['on', 'started']:
            info.append(i18n('%s is running.').replace('%s', item.description))
        elif item.status == 'stopped':
            info.append(i18n('%s is paused.').replace('%s', item.description))
        else:
            info.append(i18n('%s is stopped.').replace('%s', item.description))
        self.textInformation.setText('\n'.join(info))

    def slotComar(self, sock):
        self.handleComar(self.comar.read_cmd())

    def slotListServers(self):
        item = self.listServices.firstChild()
        while item:
            item.setVisible(not self.checkServersOnly.isChecked() or item.type == 'server')
            item = item.nextSibling()

        item = self.listServices.selectedItem()
        if not item or not item.isVisible():
            self.updateItemStatus(None)

    def slotSelectionChanged(self):
        item = self.listServices.selectedItem()
        self.updateItemStatus(item)

    def slotStart(self):
        item = self.listServices.selectedItem()
        self.buttonStart.setEnabled(0)
        self.comar.call_package('System.Service.setState', item.service, {'state': 'on'}, id=4)

    def slotPause(self):
        item = self.listServices.selectedItem()
        self.buttonPause.setEnabled(0)
        self.comar.call_package('System.Service.stop', item.service, id=4)

    def slotStop(self):
        item = self.listServices.selectedItem()
        self.buttonStop.setEnabled(0)
        self.comar.call_package('System.Service.setState', item.service, {'state': 'off'}, id=4)

    """
    def slotHelp(self):
        self.helpwin = HelpDialog(self)
        self.helpwin.show()
    """


class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue('service-manager')
        KGlobal.iconLoader().addAppDir('service-manager')
        self.config = KConfig('service-manager')
        self.aboutdata = AboutData()

        widget = servicesForm(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(widget)

    def aboutData(self):
        return self.aboutdata


# KCModule factory
def create_service_manager(parent, name):
    global kapp

    kapp = KApplication.kApplication()
    return Module(parent, name)


def main():
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    if not KUniqueApplication.start():
        print i18n('Service Manager is already running!')
        return
    app = KUniqueApplication(True, True, True)

    win = QDialog()
    win.setCaption(i18n('Service Manager'))
    win.setMinimumSize(520, 420)
    win.resize(520, 420)
    win.setIcon(loadIcon('service_manager', size=128))
    widget = servicesForm(win)
    toplayout = QVBoxLayout(win, 0, KDialog.spacingHint())
    toplayout.addWidget(widget)

    app.setMainWidget(win)
    sys.exit(win.exec_loop())

if __name__ == '__main__':
    main()
