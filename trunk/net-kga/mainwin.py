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
import connection
import links
import comar
import widgets


class Connection(QListBoxItem):
    def __init__(self, box, comar, name, link_name):
        QListBoxItem.__init__(self, box)
        self.comar = comar
        self.name = name
        self.link_name = link_name
        self.device = ""
        self.device_name = ""
        self.address = ""
        self.f1 = QFont()
        self.f2 = QFont()
        self.f1.setBold(True)
        self.f1.setPointSize(self.f1.pointSize() + 4)
        self.pix = QPixmap("ether.png")
        comar.call_package("Net.Link.connectionInfo", link_name, [ "name", name ], id=2)
        comar.call_package("Net.Link.getAddress", link_name, [ "name", name ], id=3)
    
    def paint(self, painter):
        fm = QFontMetrics(self.f1)
        fm2 = QFontMetrics(self.f2)
        painter.setPen(Qt.black)
        painter.setFont(self.f1)
        painter.drawText(32 + 9, 3 + fm.ascent(), unicode(self.name))
        painter.setFont(self.f2)
        painter.drawText(32 + 9, 3 + fm.height() + 3 + fm2.ascent(),
            "%s" % (self.device_name))
        painter.drawText(32 + 9, 3 + fm.height() + 3 + fm2.height() + 3 + fm2.ascent()
            , "Offline, " + self.address)
        painter.drawPixmap(3, 3, self.pix)
    
    def height(self, box):
        fm = QFontMetrics(self.f1)
        fm2 = QFontMetrics(self.f2)
        return 3 + fm.height() + 3 + fm2.height() + 3 + fm2.height() + 3
    
    def width(self, box):
        return 100


class Widget(QVBox):
    def __init__(self, *args):
        QVBox.__init__(self, *args)
        self.setMargin(6)
        self.setSpacing(6)
        
        self.links = QListBox(self)
        
        box = QHBox(self)
        but = QPushButton("Create", box)
        self.connect(but, SIGNAL("clicked()"), self.slotCreate)
        but = QPushButton("Edit", box)
        self.connect(but, SIGNAL("clicked()"), self.slotEdit)
        but = QPushButton("Connect", box)
        self.connect(but, SIGNAL("clicked()"), self.slotConnect)
        but = QPushButton("Disconnect", box)
        self.connect(but, SIGNAL("clicked()"), self.slotDisconnect)
        
        self.comar = comar.Link()
        self.comar.call("Net.Link.connections", id=1)
        
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
    
    def slotComar(self, sock):
        reply = self.comar.read_cmd()
        if reply[0] == self.comar.RESULT:
            if reply[1] == 1:
                for conn in reply[2].split("\n"):
                    if conn != "None":
                        Connection(self.links, self.comar, conn, reply[3])
            elif reply[1] == 2:
                name, dev, devname = reply[2].split("\n")
                conn = self.links.firstItem()
                while conn:
                    if conn.name == name:
                        conn.device = dev
                        conn.device_name = devname
                        self.links.updateItem(conn)
                        return
                    conn = conn.next()
            elif reply[1] == 3:
                name, addr = reply[2].split("\n")
                conn = self.links.firstItem()
                while conn:
                    if conn.name == name:
                        conn.address = addr
                        self.links.updateItem(conn)
                        return
                    conn = conn.next()
    
    def slotCreate(self):
        links.Window(self)
    
    def slotEdit(self):
        conn = self.links.selectedItem()
        if conn:
            w = connection.Window(self, conn.name, conn.link_name)
    
    def slotConnect(self):
        conn = self.links.selectedItem()
        if conn:
            self.comar.call("Net.Link.setState", [ "name", conn.name, "state", "up" ])
    
    def slotDisconnect(self):
        conn = self.links.selectedItem()
        if conn:
            self.comar.call("Net.Link.setState", [ "name", conn.name, "state", "down" ])
