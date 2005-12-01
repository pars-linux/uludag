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
import comar
import widgets

unique = 100
unique2 = 100000

class Connection(QListBoxItem):
    def __init__(self, box, comar, name, link_name):
        global unique
        global unique2
        QListBoxItem.__init__(self, box)
        self.cid = unique
        unique += 1
        self.cid2 = unique2
        unique2 += 1
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
        comar.call_package("Net.Link.connectionInfo", link_name, [ "name", name ], id=self.cid)
        comar.call_package("Net.Link.getAddress", link_name, [ "name", name ], id=self.cid2)
    
    def paint(self, painter):
        fm = QFontMetrics(self.f1)
        fm2 = QFontMetrics(self.f2)
        painter.setPen(Qt.black)
        painter.setFont(self.f1)
        painter.drawText(32 + 9, 3 + fm.ascent(), unicode(self.name))
        painter.setFont(self.f2)
        painter.drawText(32 + 9, 3 + fm.height() + 3 + fm2.ascent(),
            "%s, %s" % (self.device, self.device_name))
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
            elif reply[1] >= 100 and reply[1] < 100000:
                conn = self.links.firstItem()
                while conn:
                    if conn.cid == reply[1]:
                        dev = reply[2].split(" ", 1)
                        conn.device = dev[0]
                        conn.device_name = dev[1]
                        self.links.updateItem(conn)
                        return
                    conn = conn.next()
            elif reply[1] >= 100000:
                conn = self.links.firstItem()
                while conn:
                    if conn.cid2 == reply[1]:
                        addr = reply[2].split(" ", 1)
                        conn.address = addr[0]
                        self.links.updateItem(conn)
                        return
                    conn = conn.next()
    
    def slotCreate(self):
        self.comar.get_packages("Net.Link")
        links = self.comar.read_cmd()
        connection.Window(self, "new connection", links[2], 1)
    
    def slotEdit(self):
        conn = self.links.selectedItem()
        w = connection.Window(self, conn.name, conn.link_name)
    
    def slotConnect(self):
        conn = self.links.selectedItem()
        self.comar.call("Net.Link.setState", [ "name", conn.name, "state", "up" ])
    
    def slotDisconnect(self):
        conn = self.links.selectedItem()
        self.comar.call("Net.Link.setState", [ "name", conn.name, "state", "down" ])
