#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *
from kdecore import *
from kdeui import *

from sm_utility import *

import kdedesigner
from service_manager import formMain

import comar


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
            self.setPixmap(0, getIcon('player_play', 16))
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
                return -1
            else:
                return 1
        else:
            return QListViewItem.compare(self, other, col, asc)


class widgetMain(formMain):
    def __init__(self, parent):
        self.comar = comar.Link()
        self.comar.localize()
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)

        formMain.__init__(self, parent)

        self.listServices.setSorting(1)
        self.listServices.setColumnText(0, '')
        self.listServices.setColumnWidth(0, 22)
        self.listServices.setColumnWidthMode(0, QListView.Manual)

        self.buttonStart.setIconSet(getIconSet('player_play', 32))
        self.buttonStop.setIconSet(getIconSet('player_stop', 32))

        self.radioAutoRun.setEnabled(False)
        self.radioNoAutoRun.setEnabled(False)
        self.buttonStart.setEnabled(False)
        self.buttonStop.setEnabled(False)

        # Access Control
        self.wheel = False
        self.comar.can_access('System.Service.setState', id=10)

        # Populate list
        self.populateList()

        # Notify list
        self.comar.ask_notify('System.Service.changed', id=1)

        # Connections
        self.connect(self.checkServersOnly, SIGNAL('clicked()'), self.slotListServers)
        self.connect(self.listServices, SIGNAL('selectionChanged()'), self.slotSelectionChanged)
        self.connect(self.buttonStart, SIGNAL('clicked()'), self.slotStart)
        self.connect(self.buttonStop, SIGNAL('clicked()'), self.slotStop)
        self.connect(self.radioAutoRun, SIGNAL('clicked()'), self.slotOn)
        self.connect(self.radioNoAutoRun, SIGNAL('clicked()'), self.slotOff)

    def slotComar(self, sock):
        reply = self.comar.read_cmd()
        if reply.command == 'notify':
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
            elif reply.id == 10:
                self.wheel = True
        elif reply.command == 'denied':
            if reply.id != 10:
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
                if self.wheel:
                    self.buttonStop.setEnabled(True)
                info.append(i18n('%s is running.').replace('%s', item.description))
            else:
                if self.wheel:
                    self.buttonStart.setEnabled(True)
                info.append(i18n('%s is not running.').replace('%s', item.description))
        else:
            QToolTip.add(self.buttonStart, i18n('Execute startup script'))
            QToolTip.add(self.buttonStop, i18n('Execuete shutdown script'))

            info.append(item.description)

            if self.wheel:
                self.buttonStop.setEnabled(True)
                self.buttonStart.setEnabled(True)

        if self.wheel:
            self.radioAutoRun.setEnabled(True)
            self.radioAutoRun.setChecked(False)
            self.radioNoAutoRun.setEnabled(True)
            self.radioNoAutoRun.setChecked(False)

        if item.autostart:
            self.radioAutoRun.setChecked(True)
        else:
            self.radioNoAutoRun.setChecked(True)

        self.textInformation.setText(unicode('\n'.join(info)))

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
        self.comar.call_package('System.Service.setState', item.package, {'state': 'on'}, id=5)

    def slotOff(self):
        item = self.listServices.selectedItem()
        if item.type != 'server' and not self.confirmOff():
            self.radioAutoRun.setChecked(True)
            self.radioNoAutoRun.setChecked(False)
            return
        self.comar.call_package('System.Service.setState', item.package, {'state': 'off'}, id=5)

    def confirmStop(self):
        msg = i18n('If you stop this service, you may have problems.\nAre you sure you want to stop this service?')
        return KMessageBox.warningYesNo(self, msg, i18n('Warning')) != 4

    def confirmOff(self):
        msg = i18n('If you disable this service, you may have problems.\nAre you sure you want to do this?')
        return KMessageBox.warningYesNo(self, msg, i18n('Warning')) != 4
