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

import connection
import widgets
from icons import icons, getIconSet
from comariface import comlink


class Window(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setMinimumSize(340, 340)
        self.resize(340, 340)
        self.setCaption(i18n("Create a new connection"))
        vb = QVBoxLayout(self)
        vb.setSpacing(6)
        vb.setMargin(12)
        
        lab = QLabel(i18n("Select device:"), self)
        vb.addWidget(lab)
        
        self.links = QListView(self)
        self.connect(self.links, SIGNAL("doubleClicked(QListViewItem *, const QPoint &, int)"), self.slotDouble)
        self.connect(self.links, SIGNAL("selectionChanged()"), self.slotSelection)
        self.connect(self.links, SIGNAL("collapsed(QListViewItem *)"), self.slotCollapse)
        self.links.setAllColumnsShowFocus(True)
        vb.addWidget(self.links)
        self.links.addColumn("")
        self.links.addColumn("")
        self.links.header().hide()
        links = comlink.links.values()
        links.sort(key=lambda x: x.name)
        
        comlink.device_hook.append(self.slotDevices)
        for link in links:
            item = QListViewItem(self.links)
            item.setSelectable(False)
            item.setPixmap(0, icons.get_state(link.type, "up"))
            item.setText(1, unicode(link.name))
            item.setText(2, link.script)
            item.setOpen(True)
            comlink.queryDevices(link.script)
        
        hb = QHBox(self)
        hb.setSpacing(6)
        but = QPushButton(getIconSet("add", KIcon.Small), i18n("Create"), hb)
        but.setEnabled(False)
        self.connect(but, SIGNAL("clicked()"), self.accept)
        but.setDefault(True)
        self.but = but
        
        but = QPushButton(getIconSet("cancel", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), self.reject)
        
        vb.addWidget(hb)
        self.show()
    
    def reject(self):
        comlink.device_hook.remove(self.slotDevices)
        QDialog.reject(self)
    
    def accept(self):
        comlink.device_hook.remove(self.slotDevices)
        item = self.links.selectedItem()
        if item:
            link = comlink.links[str(item.parent().text(2))]
            connection.Window(self.parent(), None, link, (str(item.text(2)), str(item.text(1))))
        QDialog.accept(self)
    
    def slotDouble(self, item, point, col):
        if item and self.links.selectedItem() != None:
            self.links.setSelected(item, True)
            self.accept()
    
    def slotCollapse(self, item):
        item.setOpen(True)
        child = item.firstChild()
        if child:
            self.links.setCurrentItem(child)
            child.setSelected(True)
    
    def slotSelection(self):
        item = self.links.selectedItem()
        self.but.setEnabled(item != None)
    
    def slotDevices(self, script, devices):
        item = self.links.firstChild()
        parent = None
        while item:
            if item.text(2) == script:
                parent = item
                break
            item = item.nextSibling()
        if not parent:
            return
        if devices != "":
            for device in devices.split("\n"):
                uid, info = device.split(" ", 1)
                item = QListViewItem(parent, "", info, uid)
        else:
            item = QListViewItem(parent, "", i18n("No suitable device found"))
            item.setSelectable(False)
    
    def closeEvent(self, event):
        QDialog.closeEvent(self, event)

def ask_for_new(parent):
    if len(comlink.links) == 0:
        QMessageBox.warning(parent, i18n("Install network packages!"),
            i18n("No package with COMAR network scripts are installed yet."),
            QMessageBox.Ok, QMessageBox.NoButton)
        return
    win = Window(parent)
