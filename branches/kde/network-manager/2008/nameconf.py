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
import widgets

from icons import getIconSet
from comariface import comlink


class Window(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        
        self.old_host = None
        self.old_dns = None
        
        self.setCaption(i18n("Name Service Settings"))
        self.resize(260, 290)
        
        vb = QVBoxLayout(self)
        vb.setMargin(12)
        vb.setSpacing(6)
        
        line = widgets.HLine(i18n("Computer"), self)
        vb.addWidget(line)
        
        hb = QHBox(self)
        vb.addWidget(hb)
        hb.setSpacing(6)
        QLabel(i18n("Host name:"), hb)
        self.host = QLineEdit(hb)
        
        vb.addSpacing(6)
        line = widgets.HLine(i18n("Name servers"), self)
        vb.addWidget(line)
        
        vb2 = QVBox(self)
        vb.addWidget(vb2)
        vb2.setSpacing(3)
        
        self.dns = QListBox(vb2)
        
        hb = QHBox(vb2)
        hb.setSpacing(3)
        but = QPushButton(getIconSet("up", KIcon.Small), i18n("Up"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotUp)
        self.b1 = but
        but = QPushButton(getIconSet("down", KIcon.Small), i18n("Down"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotDown)
        self.b2 = but
        but = QPushButton(getIconSet("add", KIcon.Small), i18n("Add"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        but = QPushButton(getIconSet("remove", KIcon.Small), i18n("Remove"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotRemove)
        self.b3 = but
        
        self.connect(self.dns, SIGNAL("selectionChanged()"), self.slotSelection)
        self.slotSelection()
        
        hb = QWidget(self)
        vb.addSpacing(6)
        vb.addWidget(hb)
        lay = QHBoxLayout(hb)
        lay.setMargin(3)
        lay.setSpacing(12)
        lay.addStretch(1)
        but = QPushButton(getIconSet("apply", KIcon.Small), i18n("Apply"), hb)
        self.connect(but, SIGNAL("clicked()"), self.accept)
        lay.addWidget(but)
        but = QPushButton(getIconSet("cancel", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), self.reject)
        lay.addWidget(but)
        
        comlink.name_hook.append(self.slotName)
    
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
            ch.registerError(error)
            ch.registerDBusError(error)
            ch.registerAuthError(error)
            ch.call(dns, "")
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
