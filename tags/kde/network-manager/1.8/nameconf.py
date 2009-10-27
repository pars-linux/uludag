#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
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


class Window(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        
        self.old_host = None
        self.old_dns = None
        
        self.setCaption(i18n("Name Service Settings"))
        self.setMinimumSize(280, 320)
        
        vb = QVBox(self)
        vb.setMargin(6)
        vb.setSpacing(6)
        self.setCentralWidget(vb)
        
        widgets.HLine(i18n("Computer"), vb)
        
        hb = QHBox(vb)
        hb.setSpacing(6)
        QLabel(i18n("Host name:"), hb)
        self.host = widgets.Edit(hb)
        
        widgets.HLine(i18n("Name servers"), vb)
        
        vb2 = QVBox(vb)
        vb2.setSpacing(3)
        
        self.dns = QListBox(vb2)
        
        hb = QHBox(vb2)
        hb.setSpacing(3)
        but = QPushButton(getIconSet("add.png", KIcon.Small), i18n("Add"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        but = QPushButton(getIconSet("remove.png", KIcon.Small), i18n("Remove"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotRemove)
        
        hb = QWidget(vb)
        lay = QHBoxLayout(hb)
        lay.setMargin(3)
        lay.setSpacing(12)
        lay.addStretch(1)
        but = QPushButton(getIconSet("apply.png", KIcon.Small), i18n("Apply"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotApply)
        lay.addWidget(but)
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotCancel)
        lay.addWidget(but)
        
        comlink.name_hook.append(self.slotName)
    
    def slotApply(self):
        host = str(self.host.edit.text())
        if self.old_host != host:
            comlink.com.Net.Stack.setHostNames(hostnames=host)
        item = self.dns.firstItem()
        dns = []
        while item:
            dns.append(str(item.text()))
            item = item.next()
        dns = "\n".join(dns)
        if self.old_dns != dns:
            comlink.com.Net.Stack.setNameServers(nameservers=dns)
        self.hide()
    
    def slotCancel(self):
        self.hide()
    
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
    
    def slotRemove(self):
        item = self.dns.selectedItem()
        if item:
            self.dns.removeItem(self.dns.index(item))
    
    def slotName(self, hostname, servers):
        self.dns.clear()
        self.old_dns = servers.split("\n")
        for item in self.old_dns:
            self.dns.insertItem(item)
        
        self.old_host = hostname
        self.host.edit.setText(hostname)
