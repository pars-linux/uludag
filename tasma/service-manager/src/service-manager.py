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

version = '1.1.2'

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
    def __init__(self, parent=None, package='', type='server', state=False, autostart=False, description=''):
        KListViewItem.__init__(self, parent)

        self.package = package
        self.type = type
        self.state = state
        self.autostart = autostart
        self.description = unicode(description)

        self.setText(1, self.description)
        self.setText(3, self.package)

        self.setVisible(False)

        self.setState(state)
        self.setAutoStart(autostart)

    def setState(self, state):
        self.state = state

        if state:
            self.setPixmap(0, loadIcon('player_play'))
        else:
            self.setPixmap(0, QPixmap())

    def setAutoStart(self, autostart):
        self.autostart = autostart
        if self.autostart:
            self.setText(2, i18n('Yes'))
        else:
            self.setText(2, i18n('No'))

    def compare(self, other, col, asc):
        if col == 0:
            s1 = self.state
            s2 = other.state
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
        self.buttonStop.setIconSet(loadIconSet('player_stop', size=32))

        self.radioAutoRun.setEnabled(False)
        self.radioNoAutoRun.setEnabled(False)
        self.buttonStart.setEnabled(False)
        self.buttonStop.setEnabled(False)

        # Initialize Comar
        self.comar = comar.Link()
        self.comar.localize(os.environ['LANG'].split('_')[0])

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
        self.connect(self.buttonStop, SIGNAL('clicked()'), self.slotStop)
        self.connect(self.radioAutoRun, SIGNAL('clicked()'), self.slotOn)
        self.connect(self.radioNoAutoRun, SIGNAL('clicked()'), self.slotOff)

    def handleComar(self, reply):
        if reply.command == 'start':
            # ask for more
            self.handleComar(self.comar.read_cmd())
        elif reply.command == 'notify':
            # locate item
            item = self.findItem(reply.script)
            # update if neccessary
            if reply.data in ['started', 'stopped']:
                state = reply.data == 'started'
                if item.state != state:
                    item.setState(state)
                    if item == self.listServices.selectedItem():
                        self.updateItemStatus(item)
            elif reply.data in ['on', 'off']:
                autostart = reply.data == 'on'
                if item.autostart != autostart:
                    item.setAutoStart(autostart)
            # item is new, add to list
            if not item:
                self.comar.call_package('System.Service.info', reply.script, id=2)
                self.handleComar(self.comar.read_cmd())
        elif reply.command == 'result':
            info = reply.data.split('\n')
            if reply.id == 2: # System.Service.info
                self.addServiceItem(reply)
            elif reply.id in [3, 4]: # System.Service.{start,stop}
                state = reply.id == 3
                # locate item
                item = self.findItem(reply.script)
                # update if neccessary
                if item.state != state:
                    item.setState(state)
                    if item == self.listServices.selectedItem():
                        self.updateItemStatus(item)
        elif reply.command == 'denied':
            KMessageBox.error(self, i18n('You are not allowed to do this operation.'), i18n('Access Denied'))
        elif reply.command == 'error':
            KMessageBox.error(self, i18n('COMAR script execution failed.'), i18n('Script Error'))
        elif reply.command == 'fail':
            if reply.id in [3, 4]: # System.Service.{start,stop}
                state = reply.id == 3
                if state:
                    KMessageBox.error(self, i18n('Unable to start service.'), i18n('Failed'))
                    self.buttonStart.setEnabled(1)
                else:
                    KMessageBox.error(self, i18n('Unable to stop service.'), i18n('Failed'))
                    self.buttonStop.setEnabled(1)

    def populateList(self):
        self.comar.call('System.Service.info', id=2)
        self.handleComar(self.comar.read_cmd())

    def findItem(self, package):
        item = self.listServices.firstChild()
        while item:
            if item.package == package:
                return item
            item = item.nextSibling()
        return None

    def addServiceItem(self, reply):
        info = reply.data.split('\n')

        state = info[1] in ['started', 'on']
        autostart = info[1] in ['stopped', 'on']

        si = serviceItem(self.listServices, reply.script, info[0], state, autostart, info[2])

        if not self.checkServersOnly.isChecked() or info[0] == 'server':
            si.setVisible(True)

    def updateItemStatus(self, item):
        self.buttonStart.setEnabled(False)
        self.buttonStop.setEnabled(False)
        self.textInformation.setText(i18n('Select a service from list.'))

        info = []

        if not item:
            return

        if item.type in ['server', 'local']:
            QToolTip.add(self.buttonStart, i18n('Start'))
            QToolTip.add(self.buttonStop, i18n('Stop'))

            if item.state:
                self.buttonStop.setEnabled(True)
                info.append(i18n('%s is running.').replace('%s', item.description))
            else:
                self.buttonStart.setEnabled(True)
                info.append(i18n('%s is not running.').replace('%s', item.description))
        else:
            QToolTip.add(self.buttonStart, i18n('Execute startup script'))
            QToolTip.add(self.buttonStop, i18n('Execuete shutdown script'))

            info.append(item.description)

            self.buttonStop.setEnabled(True)
            self.buttonStart.setEnabled(True)

        self.radioAutoRun.setEnabled(True)
        self.radioAutoRun.setChecked(False)
        self.radioNoAutoRun.setEnabled(True)
        self.radioNoAutoRun.setChecked(False)
        if item.autostart:
            self.radioAutoRun.setChecked(True)
        else:
            self.radioNoAutoRun.setChecked(True)

        info.append('')

        self.textInformation.setText(unicode('\n'.join(info)))

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
        self.buttonStart.setEnabled(False)
        self.comar.call_package('System.Service.start', item.package, id=3)

    def slotStop(self):
        item = self.listServices.selectedItem()
        if item.type != 'server' and not self.confirmStop():
            return
        self.buttonStop.setEnabled(False)
        self.comar.call_package('System.Service.stop', item.package, id=4)

    def slotOn(self):
        item = self.listServices.selectedItem()
        self.buttonStop.setEnabled(False)
        self.comar.call_package('System.Service.setState', item.package, {'state': 'on'}, id=5)

    def slotOff(self):
        item = self.listServices.selectedItem()
        if item.type != 'server' and not self.confirmStop():
            self.radioAutoRun.setChecked(True)
            self.radioNoAutoRun.setChecked(False)
            return
        self.buttonStop.setEnabled(False)
        self.comar.call_package('System.Service.setState', item.package, {'state': 'off'}, id=5)

    def confirmStop(self):
        msg = i18n('If you stop this service, you may have problems.\nAre you sure you want to stop this service?')
        return KMessageBox.warningYesNo(self, msg, i18n('Warning')) != 4

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
