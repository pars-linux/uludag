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
from kdecore import i18n

import connection
import widgets
from icons import icons
from comariface import comlink


class LinkItem(QListBoxItem):
    def __init__(self, box, link):
        QListBoxItem.__init__(self, box)
        self.link = link
        
        self.f1 = QFont()
        self.f1.setBold(True)
        #self.f1.setPointSize(self.f1.pointSize() + 1)
        #self.pix = QPixmap("ether.png")
    
    def paint(self, painter):
        fm = QFontMetrics(self.f1)
        painter.setPen(Qt.black)
        painter.setFont(self.f1)
        painter.drawText(3, 3 + fm.ascent(), unicode(self.link.name))
        #painter.drawText(32 + 9, 3 + fm.ascent(), unicode(self.name))
        #painter.drawPixmap(3, 3, self.pix)
    
    def height(self, box):
        fm = QFontMetrics(self.f1)
        ts = 3 + fm.height() + 3
        #ts = 3 + fm.height() + 3
        #if ts < 32 + 3 + 3:
        #    ts = 32 + 3 + 3
        return ts
    
    def width(self, box):
        return 100


class Window(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setMinimumSize(340, 340)
        self.resize(340, 340)
        self.setCaption(i18n("Create a new connection"))
        self.my_parent = parent
        vb = QVBoxLayout(self)
        vb.setSpacing(6)
        vb.setMargin(12)
        
        lab = QLabel(i18n("Select device:"), self)
        vb.addWidget(lab)
        
        self.links = QListView(self)
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
            item.setText(1, link.name)
            item.setText(2, link.script)
            item.setOpen(True)
            comlink.queryDevices(link.script)
        
        but = QPushButton(i18n("Configure the connection"), self)
        vb.addWidget(but)
        self.connect(but, SIGNAL("clicked()"), self.accept)
        but.setDefault(True)
    
    def reject(self):
        comlink.device_hook.remove(self.slotDevices)
        QDialog.reject(self)
    
    def accept(self):
        comlink.device_hook.remove(self.slotDevices)
        link = self.links.selectedItem()
        if link:
            connection.Window(self.my_parent, i18n("new connection"), link.link_name, 1)
        QDialog.accept(self)
    
    def slotDevices(self, script, devices):
        item = self.links.firstChild()
        # FIXME: better handling
        while item:
            if item.text(2) == script:
                parent = item
                break
            item = item.nextSibling()
        if devices != "":
            for device in devices.split("\n"):
                uid, info = device.split(" ", 1)
                item = QListViewItem(parent, "", info)


class Links:
    def ask_for_create(self, parent):
        if len(self.links) == 0:
            QMessageBox.warning(parent, i18n("Install network packages!"),
                i18n("No package with COMAR network scripts are installed yet."),
                QMessageBox.Ok, QMessageBox.NoButton)
            return
        
        if len(self.links) == 1:
            connection.Window(parent, i18n("new connection"), self.links[self.links.keys()[0]], 1)
            return
        
        self.w = Window(parent, self.links)
        self.w.show()
