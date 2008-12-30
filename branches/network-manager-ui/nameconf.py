#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import *
from kdeui import *

from icons import getIconSet
from comariface import comlink

from nameConf import NameConf

class Window(NameConf):
    def __init__(self, parent):
        NameConf.__init__(self, parent)

        self.old_host = None
        self.old_dns = None

        self.fillLabels()

        self.connect(self.b1, SIGNAL("clicked()"), self.slotUp)
        self.connect(self.b2, SIGNAL("clicked()"), self.slotDown)
        self.connect(self.b3, SIGNAL("clicked()"), self.slotRemove)
        self.connect(self.b4, SIGNAL("clicked()"), self.slotAdd)

        self.connect(self.dns, SIGNAL("selectionChanged()"), self.slotSelection)
        self.slotSelection()

        self.connect(self.applyBut, SIGNAL("clicked()"), self.accept)
        self.connect(self.cancelBut, SIGNAL("clicked()"), self.reject)

        comlink.name_hook.append(self.slotName)

    def fillLabels(self):
        self.setCaption(i18n("Name Service Settings"))
        self.hostNameLabel.setText(i18n("Host name:"))
        self.nameServLabel.setText(i18n("Name servers"))

        self.b1.setIconSet(getIconSet("up", KIcon.Small))
        self.b1.setText(i18n("Up"))
        self.b2.setIconSet(getIconSet("down", KIcon.Small))
        self.b2.setText(i18n("Down"))
        self.b3.setIconSet(getIconSet("remove", KIcon.Small))
        self.b3.setText(i18n("Remove"))
        self.b4.setIconSet(getIconSet("add", KIcon.Small))
        self.b4.setText(i18n("Add"))
        self.applyBut.setIconSet(getIconSet("apply", KIcon.Small))
        self.applyBut.setText(i18n("Apply"))
        self.cancelBut.setIconSet(getIconSet("cancel", KIcon.Small))
        self.cancelBut.setText(i18n("Cancel"))

    def accept(self):
        host = str(self.host.text())
        dns = []

        item = self.dns.firstItem()
        while item:
            dns.append(str(item.text()))
            item = item.next()

        self.done = 0
        def handler():
            self.done += 1
            if self.done == 2:
                self.setEnabled(True)
                QDialog.accept(self)

        def error(exception):
            self.setEnabled(True)

        def cancel():
            self.setEnabled(True)

        if self.old_host != host:
            self.setEnabled(False)
            ch = comlink.callHandler("baselayout", "Net.Stack", "setHostName", "tr.org.pardus.comar.net.stack.set")
            ch.registerDone(handler)
            ch.registerCancel(cancel)
            ch.registerError(error)
            ch.registerDBusError(error)
            ch.registerAuthError(error)
            ch.call(host)
        else:
            self.done += 1

        if self.old_dns != dns:
            self.setEnabled(False)
            ch = comlink.callHandler("baselayout", "Net.Stack", "setNameServers", "tr.org.pardus.comar.net.stack.set")
            ch.registerDone(handler)
            ch.registerCancel(cancel)
            ch.registerError(cancel)
            ch.registerDBusError(cancel)
            ch.registerAuthError(cancel)
            ch.call(dns, False)
        else:
            self.done += 1

        if self.done == 2:
            self.setEnabled(True)
            QDialog.accept(self)


    def reject(self):
        QDialog.reject(self)

    def slotSelection(self):
        item = self.dns.selectedItem()
        self.b1.setEnabled(item != None and item.prev() != None)
        self.b2.setEnabled(item != None and item.next() != None)
        self.b3.setEnabled(item != None)

    def slotUp(self):
        item = self.dns.selectedItem()
        prev = item.prev()
        if item and prev:
            pprev = prev.prev()
            self.dns.takeItem(item)
            if pprev:
                self.dns.insertItem(item, pprev)
            else:
                self.dns.insertItem(item, 0)
            self.dns.setCurrentItem(item)
            self.slotSelection()

    def slotDown(self):
        item = self.dns.selectedItem()
        next = item.next()
        if item and next:
            self.dns.takeItem(item)
            self.dns.insertItem(item, next)
            self.dns.setCurrentItem(item)
            self.slotSelection()

    def slotAdd(self):
        tmp = KInputDialog.getText(
            i18n("Add Name Server"),
            i18n("Name server:"),
            "",
            self,
            "lala",
            QRegExpValidator(QRegExp("[0123456789.:]*"), self)
        )
        if tmp[1]:
            self.dns.insertItem(tmp[0])
            self.slotSelection()

    def slotRemove(self):
        item = self.dns.selectedItem()
        if item:
            self.dns.removeItem(self.dns.index(item))
            self.slotSelection()

    def slotName(self, hostname, servers):
        self.dns.clear()
        self.old_dns = servers
        for item in self.old_dns:
            self.dns.insertItem(item)

        self.old_host = hostname
        self.host.setText(hostname)

