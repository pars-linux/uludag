#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import *
import connection
from links import links
import comar
import widgets
from icons import icons


class Connection(QListBoxItem):
    def __init__(self, box, comar, name, link_name):
        QListBoxItem.__init__(self, box)
        self.comar = comar
        self.name = name
        self.online = "down"
        self.state = "down"
        self.link_name = link_name
        self.device = ""
        self.device_name = ""
        self.address = ""
        self.f1 = QFont()
        self.f2 = QFont()
        self.f1.setBold(True)
        self.f1.setPointSize(self.f1.pointSize() + 4)
        comar.call_package("Net.Link.connectionInfo", link_name, [ "name", name ], id=2)
        comar.call_package("Net.Link.getAddress", link_name, [ "name", name ], id=3)
        comar.call_package("Net.Link.getState", link_name, [ "name", name ], id=4)
    
    def paint(self, painter):
        if self.state == "up":
            text = unicode(i18n("Active")) + ", "
        else:
            text = unicode(i18n("Inactive")) + ", "
        fm = QFontMetrics(self.f1)
        fm2 = QFontMetrics(self.f2)
        painter.setPen(Qt.black)
        painter.setFont(self.f1)
        painter.drawText(48 + 9, 3 + fm.ascent(), unicode(self.name))
        painter.setFont(self.f2)
        painter.drawText(48 + 9, 3 + fm.height() + 3 + fm2.ascent(),
            "%s" % (self.device_name))
        painter.drawText(48 + 9, 3 + fm.height() + 3 + fm2.height() + 3 + fm2.ascent()
            , text + self.address)
        painter.drawPixmap(3, 3, icons.get_state(links.get_info(self.link_name).type, self.online))
    
    def height(self, box):
        fm = QFontMetrics(self.f1)
        fm2 = QFontMetrics(self.f2)
        ts = 3 + fm.height() + 3 + fm2.height() + 3 + fm2.height() + 3
        ps = 3 + 48 + 3
        if ts < ps:
            ts = ps
        return ts
    
    def width(self, box):
        return 100


class Widget(QVBox):
    def __init__(self, *args):
        QVBox.__init__(self, *args)
        self.setMargin(6)
        self.setSpacing(6)
        
        self.links = QListBox(self)
        
        box = QHBox(self)
        box.setSpacing(12)
        but = QPushButton(i18n("Create"), box)
        self.connect(but, SIGNAL("clicked()"), self.slotCreate)
        but = QPushButton(i18n("Edit"), box)
        self.connect(but, SIGNAL("clicked()"), self.slotEdit)
        but = QPushButton(i18n("Delete"), box)
        self.connect(but, SIGNAL("clicked()"), self.slotDelete)
        but = QPushButton(i18n("Connect"), box)
        self.connect(but, SIGNAL("clicked()"), self.slotConnect)
        but = QPushButton(i18n("Disconnect"), box)
        self.connect(but, SIGNAL("clicked()"), self.slotDisconnect)
        
        self.comar = comar.Link()
        
        links.query(self.comar)
        
        self.comar.call("Net.Link.connections", id=1)
        
        self.comar.ask_notify("Net.Link.stateChanged")
        self.comar.ask_notify("Net.Link.connectionChanged")
        self.comar.ask_notify("Net.Link.deviceChanged")
        
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
    
    def uniqueName(self):
        id = 0
        while True:
            name = unicode(i18n("Unconfigured")) + " " + str(id)
            if not self.findConn(name):
                return name
            id += 1
    
    def findConn(self, name):
        # lame iteration in absence of QListBox's own iterator
        item = self.links.firstItem()
        while item:
            if item.name == name:
                return item
            item = item.next()
        return None
    
    def slotComar(self, sock):
        reply = self.comar.read_cmd()
        if reply[0] == self.comar.RESULT:
            if reply[1] == 1:
                if reply[2] == "":
                    self.comar.call_package("Net.Link.deviceList", reply[3], id=5)
                else:
                    for conn in reply[2].split("\n"):
                        Connection(self.links, self.comar, conn, reply[3])
            elif reply[1] == 2:
                name, dev, devname = reply[2].split("\n")
                conn = self.findConn(name)
                if conn:
                    conn.device = dev
                    conn.device_name = devname
                    self.links.updateItem(conn)
                    return
            elif reply[1] == 3:
                name, mode, rest = reply[2].split("\n", 2)
                if "\n" in rest:
                    addr, gate = rest.split("\n", 1)
                else:
                    addr = rest
                conn = self.findConn(name)
                if conn:
                    conn.address = addr
                    self.links.updateItem(conn)
                    return
            elif reply[1] == 4:
                name, state = reply[2].split("\n")
                conn = self.findConn(name)
                if conn:
                    conn.state = state
                    if state == "up":
                        conn.online = state
                    self.links.updateItem(conn)
                    return
            elif reply[1] == 5:
                if reply[2] == '':
                    return
                uid, dev = reply[2].split(" ", 1)
                name = self.uniqueName()
                self.comar.call_package("Net.Link.setConnection", reply[3], [ "name", name, "device", uid ])
            elif reply[1] > 42:
                links.slotComar(reply)
        
        elif reply[0] == self.comar.NOTIFY:
            noti, script, data = reply[2].split("\n", 2)

            if noti == "Net.Link.stateChanged":
                name, state = data.split("\n", 1)
                conn = self.findConn(name)
                if conn:
                    conn.online = state
                    self.links.updateItem(conn)
                    return
            
            elif noti == "Net.Link.connectionChanged":
                mode, name = data.split(" ", 1)
                if mode == "added":
                    if not self.findConn(name):
                        Connection(self.links, self.comar, name, script)
                elif mode == "deleted":
                    conn = self.findConn(name)
                    if conn:
                        self.links.removeItem(self.links.index(conn))
                elif mode == "configured":
                    type, name = name.split(" ", 1)
                    if type == "device":
                        self.comar.call_package("Net.Link.connectionInfo", script, [ "name", name ], id=2)
                    elif type == "address":
                        self.comar.call_package("Net.Link.getAddress", script, [ "name", name ], id=3)
                    elif type == "state":
                        self.comar.call_package("Net.Link.getState", script, [ "name", name ], id=4)
            
            elif noti == "Net.Link.deviceChanged":
                type, rest = data.split(" ", 1)
                if type != "new":
                    return
                nettype, uid, info = rest.split(" ", 2)
                name = self.uniqueName()
                self.comar.call_package("Net.Link.setConnection", script, [ "name", name, "device", uid ])
    
    def slotCreate(self):
        links.ask_for_create(self)
    
    def slotEdit(self):
        conn = self.links.selectedItem()
        if conn:
            w = connection.Window(self, conn.name, conn.link_name)
    
    def slotDelete(self):
        m = i18n("Should I delete the\n'%s'\nconnection?")
        conn = self.links.selectedItem()
        if conn:
            if QMessageBox.Ok == QMessageBox.question(self, i18n("Delete connection?"), unicode(m) % conn.name, QMessageBox.Ok, QMessageBox.Cancel):
                self.comar.call_package("Net.Link.deleteConnection", conn.link_name, [ "name", conn.name ])
    
    def slotConnect(self):
        conn = self.links.selectedItem()
        if conn:
            self.comar.call_package("Net.Link.setState", conn.link_name, [ "name", conn.name, "state", "up" ])
    
    def slotDisconnect(self):
        conn = self.links.selectedItem()
        if conn:
            self.comar.call_package("Net.Link.setState", conn.link_name, [ "name", conn.name, "state", "down" ])
