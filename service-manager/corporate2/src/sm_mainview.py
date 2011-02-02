#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006,2010, TUBITAK/UEKAE
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
from backend import Backend

import kdedesigner
from service_manager import formMain

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
            self.setText(0, "")

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
        formMain.__init__(self, parent)

        self.backend = Backend(self)

        self.editSearch.setFocus()

        self.listServices.setResizeMode(QListView.LastColumn)
        self.listServices.setSorting(1)
        self.listServices.setColumnText(0, '')
        self.listServices.setColumnWidth(0, 21)
        self.listServices.setColumnWidthMode(0, QListView.Manual)

        self.buttonClearSearch.setIconSet(getIconSet('locationbar_erase', 16))
        self.buttonStart.setIconSet(getIconSet('player_play', 32))
        self.buttonStop.setIconSet(getIconSet('player_stop', 32))
        self.buttonRestart.setIconSet(getIconSet('reload', 32))

        self.radioAutoRun.setEnabled(False)
        self.radioNoAutoRun.setEnabled(False)
        self.buttonStart.setEnabled(False)
        self.buttonStop.setEnabled(False)
        self.buttonRestart.setEnabled(False)

        # Populate list
        self.populateList()

        # Configuration file
        self.config = self.parent().config
        if self.config.readEntry("servers_only") == "off":
            self.checkServersOnly.setChecked(False)

        # Connections
        self.connect(self.checkServersOnly, SIGNAL('clicked()'), self.slotListServers)
        self.connect(self.listServices, SIGNAL('selectionChanged()'), self.slotSelectionChanged)
        self.connect(self.buttonClearSearch, SIGNAL('clicked()'), self.editSearch.clear)
        self.connect(self.buttonStart, SIGNAL('clicked()'), self.slotStart)
        self.connect(self.buttonStop, SIGNAL('clicked()'), self.slotStop)
        self.connect(self.buttonRestart, SIGNAL('clicked()'), self.slotRestart)
        self.connect(self.radioAutoRun, SIGNAL('clicked()'), self.slotOn)
        self.connect(self.radioNoAutoRun, SIGNAL('clicked()'), self.slotOff)
        self.connect(self.editSearch, SIGNAL('textChanged(const QString &)'), self.slotSearch)
        self.connect(self.listServices, SIGNAL('doubleClicked(QListViewItem*)'), self.slotDoubleClicked)

    def handleSignals(self, script, signal, args):
        # print 'COMAR:', script, signal, args
        if signal == "Changed":
            package, state = args
            item = self.findItem(package)
            # update if neccessary
            if state in ['started', 'stopped']:
                state = state == 'started'
                if item.state != state:
                    item.setState(state)
                    if item == self.listServices.selectedItem():
                        self.updateItemStatus(item)
            elif state in ['on', 'off']:
                autostart = state == 'on'
                if item.autostart != autostart:
                    item.setAutoStart(autostart)
            # item is new, add to list
            if not item:
                self.backend.info(package, async = self.addServiceItem)

    # start or stop service when the item is double clicked
    def slotDoubleClicked(self, item):
        # if it's not started
        if not item.state:
            self.backend.start(item.package)
        else:
            self.backend.stop(item.package)

    def populateList(self):
        packages = self.backend.services()
        for package in packages:
            self.backend.info(package, async = self.addServiceItem)

    def findItem(self, package):
        item = self.listServices.firstChild()
        while item:
            if item.package == package:
                return item
            item = item.nextSibling()
        return None

    def addServiceItem(self, package, exception, args):
        if exception:
            return
        _type, _desc, _state = args
        state = _state in ['conditional_started', 'started', 'on']
        autostart = _state in ['stopped', 'on'] #TODO: add support for conditional services

        si = serviceItem(self.listServices, package, _type, state, autostart, _desc)

        if not self.checkServersOnly.isChecked() or _type == 'server':
            si.setVisible(True)

    def updateItemStatus(self, item):
        self.buttonStart.setEnabled(False)
        self.buttonStop.setEnabled(False)
        self.buttonRestart.setEnabled(False)
        self.textInformation.setText(i18n('Select a service from list.'))

        info = []

        if not item:
            return

        QToolTip.add(self.buttonClearSearch, i18n('Clear Search'))
        QToolTip.add(self.buttonStart, i18n('Start'))
        QToolTip.add(self.buttonStop, i18n('Stop'))
        QToolTip.add(self.buttonRestart, i18n('Restart'))

        if item.state:
            self.buttonStop.setEnabled(True)
            self.buttonRestart.setEnabled(True)
            info.append(unicode(i18n('%s is running.').replace('%s', item.description)))
        else:
            self.buttonStart.setEnabled(True)
            info.append(unicode(i18n('%s is not running.').replace('%s', item.description)))

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
        if self.checkServersOnly.isChecked():
            self.config.writeEntry("servers_only", "on")
        else:
            self.config.writeEntry("servers_only", "off")
        self.slotSearch(self.editSearch.text())

    def slotSelectionChanged(self):
        item = self.listServices.selectedItem()
        self.updateItemStatus(item)

    def slotStart(self):
        item = self.listServices.selectedItem()
        if self.backend.start(item.package):
           self.buttonStart.setEnabled(False)

    def slotStop(self):
        item = self.listServices.selectedItem()
        if item.type != 'server' and not self.confirmStop():
            return
        if self.backend.stop(item.package):
            self.buttonStop.setEnabled(False)
            self.buttonRestart.setEnabled(False)

    def slotRestart(self):
        item = self.listServices.selectedItem()
        if self.backend.stop(item.package):
            self.backend.start(item.package)
            self.buttonStop.setEnabled(False)
            self.buttonRestart.setEnabled(False)

    def slotOn(self):
        item = self.listServices.selectedItem()
        state = self.backend.set_state(item.package, "on")
        self.radioAutoRun.setChecked(state)
        self.radioNoAutoRun.setChecked(not state)

    def slotOff(self):
        item = self.listServices.selectedItem()
        if item.autostart:
            if item.type != 'server' and not self.confirmOff():
                self.radioAutoRun.setChecked(True)
                self.radioNoAutoRun.setChecked(False)
                return
            state = self.backend.set_state(item.package, "off")
            self.radioAutoRun.setChecked(not state)
            self.radioNoAutoRun.setChecked(state)

    def slotSearch(self, text):
        item = self.listServices.firstChild()
        while item:
            item.setVisible(text.lower() in item.description.lower() + item.package.lower())
            if self.checkServersOnly.isChecked() and item.type != 'server':
                item.setVisible(False)
            item = item.nextSibling()

        item = self.listServices.selectedItem()
        if not item or not item.isVisible():
            self.updateItemStatus(None)

    def confirmStop(self):
        msg = i18n('If you stop this service, you may have problems.\nAre you sure you want to stop this service?')
        return KMessageBox.warningYesNo(self, msg, i18n('Warning')) != 4

    def confirmOff(self):
        msg = i18n('If you disable this service, you may have problems.\nAre you sure you want to do this?')
        return KMessageBox.warningYesNo(self, msg, i18n('Warning')) != 4
