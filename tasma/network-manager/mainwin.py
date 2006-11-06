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
from kdeui import *
import stack
import connection
from links import links
import comar
import widgets
from icons import icons


class MinButton(QPushButton):
    def __init__(self, title, parent):
        QPushButton.__init__(self, title, parent)
        self.title = title
        f = self.font()
        f.setPointSize(f.pointSize() - 2)
        self.setFont(f)
        self.hide()
    
    def mySize(self):
        fm = self.fontMetrics()
        rect = fm.boundingRect(self.title)
        return (rect.width(), rect.height())


class Connection(QWidget):
    def __init__(self, view, script, data):
        name, devid, devname = unicode(data).split("\n")
        dev = view.devices.get(devid, None)
        if not dev:
            dev = Device(view, devname, devid)
            dev.show()
        QWidget.__init__(self, dev)
        
        self.name = name
        self.script = script
        self.active = True
        self.state = "down"
        
        fm = self.fontMetrics()
        self.myBase = fm.ascent()
        self.mypix = QImage("wireless.png")
        self.mypix = self.mypix.scale(32, 32)
        self.mypix = QPixmap(self.mypix)
        self.check = QCheckBox(self)
        self.check.setAutoMask(True)
        self.edit_but = MinButton("Edit", self)
        self.del_but = MinButton("Delete", self)
        view.connections["%s %s" % (script, name)] = self
        self.show()
        
        view.comlink.call_package("Net.Link.getAddress", script, [ "name", name ], id=3)
        view.comlink.call_package("Net.Link.getState", script, [ "name", name ], id=4)
    
    def slotComar(self, reply):
        pass
    
    def paintEvent(self, event):
        paint = QPainter(self)
        paint.fillRect(event.rect(), QBrush(QColor("white")))
        paint.drawPixmap(16, 0, self.mypix)
        paint.drawText(49, self.myBase + 1, self.name)
    
    def resizeEvent(self, event):
        pix = event.size().width()
        w1, h1 = self.edit_but.mySize()
        w2, h2 = self.del_but.mySize()
        self.edit_but.setGeometry(pix - w1 - w2 - 20, 0, w1 + 8, h1 + 8)
        self.del_but.setGeometry(pix - w2 - 8, 0, w2 + 8, h2 + 8)
        return QWidget.resizeEvent(self, event)
    
    def enterEvent(self, event):
        self.edit_but.show()
        self.del_but.show()
        return QWidget.enterEvent(self, event)
    
    def leaveEvent(self, event):
        self.edit_but.hide()
        self.del_but.hide()
        return QWidget.leaveEvent(self, event)
    
    def sizeHint(self):
        fm = self.fontMetrics()
        rect = fm.boundingRect(self.name)
        w = rect.width() + 2 + 32 + 16
        h = max(rect.height(), 32) + 2
        return QSize(w, h)


class Device(QWidget):
    def __init__(self, parent, name, id):
        QWidget.__init__(self, parent.viewport())
        self.name = name
        fm = self.fontMetrics()
        self.myBase = fm.ascent()
        self.mypix = QImage("ethernet.png")
        self.mypix = self.mypix.scale(24, 24)
        self.mypix = QPixmap(self.mypix)
        self.connections = []
        parent.devices[id] = self
    
    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        paint = QPainter(self)
        paint.drawPixmap(0, 0, self.mypix)
        paint.drawText(25, self.myBase + 1, self.name)
    
    def heightForWidth(self, width):
        fm = self.fontMetrics()
        rect = fm.boundingRect(self.name)
        h = max(rect.height(), 24) + 2
        
        if not self.children():
            return h
        
        maxw = 0
        maxh = 0
        for item in self.children():
            hint = item.sizeHint()
            w2 = hint.width()
            h2 = hint.height()
            if w2 > maxw:
                maxw = w2
            if h2 > maxh:
                maxh = h2
        c = width / maxw
        if c < 1:
            c = 1
        if c > 3:
            c = 3
        L = len(self.children())
        if L % c != 0:
            L += c
        h += (maxh + 2) * (L / c)
        
        return h
    
    def resizeEvent(self, event):
        aw = event.size().width()
        ah = event.size().height()
        
        maxw = 0
        maxh = 0
        childs = self.children()
        if not childs or len(childs) == 0:
            return QWidget.resizeEvent(self, event)
        for item in childs:
            hint = item.sizeHint()
            w = hint.width()
            h = hint.height()
            if w > maxw:
                maxw = w
            if h > maxh:
                maxh = h
        
        i = 0
        j = 0
        c = aw / maxw
        if c < 1:
            c = 1
        if c > 3:
            c = 3
        maxw = aw / c
        for item in childs:
            item.setGeometry(i * maxw, 32 + j * maxh, maxw, maxh)
            i += 1
            if i >= c:
                i = 0
                j += 1
        
        return QWidget.resizeEvent(self, event)


class ConnectionView(QScrollView):
    def __init__(self, parent, comlink):
        QScrollView.__init__(self, parent)
        self.comlink = comlink
        self.devices = {}
        self.connections = {}
    
    def myResize(self, width):
        th = 0
        for name in self.devices:
            item = self.devices[name]
            h = item.heightForWidth(width)
            item.setGeometry(0, th, width, h)
            th += h
    
    def resizeEvent(self, event):
        w = event.size().width()
        self.myResize(w)
        return QScrollView.resizeEvent(self, event)
    
    def find(self, script, name):
        return self.connections.get("%s %s" % (script, name), None)


class Widget(QVBox):
    def __init__(self, *args):
        QVBox.__init__(self, *args)
        self.setMargin(6)
        self.setSpacing(6)
        
        box = QHBox(self)
        lab = QLabel(i18n("Network connections:"), box)
        box.setStretchFactor(lab, 5)
        but = QPushButton(i18n("Settings"), box)
        self.connect(but, SIGNAL("clicked()"), self.slotSettings)
        box.setStretchFactor(but, 1)
        
        self.comar = comar.Link()
        
        self.links = ConnectionView(self, self.comar)
        #self.connect(self.links, SIGNAL("doubleClicked(QListBoxItem *)"), self.slotDouble)
        
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
        but = QPushButton(i18n("Help"), box)
        self.connect(but, SIGNAL("clicked()"), self.slotHelp)
        
        self.stack = stack.Window(self, self.comar)
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
    
    def slotHelp(self):
        self.helpwin = widgets.HelpDialog("network-manager", i18n("Network Connections Help"), self)
        self.helpwin.show()
    
    def slotComar(self, sock):
        reply = self.comar.read_cmd()
        self.handleComar(reply)
    
    def handleComar(self, reply):
        if reply[0] == self.comar.RESULT:
            if reply[1] == 1:
                if reply[2] == "":
                    self.comar.call_package("Net.Link.deviceList", reply[3], id=5)
                else:
                    for name in reply[2].split("\n"):
                        self.comar.call_package("Net.Link.connectionInfo", reply.script, [ "name", name ], id=2)
            elif reply[1] == 2:
                conn = Connection(self.links, reply.script, reply.data)
                self.links.myResize(self.links.width())
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
                if reply[2] == '' or reply[3] == "ppp":
                    return
                devs = reply[2].split("\n")
                for dev in devs:
                    uid, rest = dev.split(" ", 1)
                    name = self.uniqueName()
                    self.comar.call_package("Net.Link.setConnection", reply[3], [ "name", name, "device", uid ])
                    Connection(self.links, self.comar, name, reply[3])
            elif reply[1] == 42:
                links.slotComar(reply)
            elif reply[1] > 42:
                self.stack.slotComar(reply)
        
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
                        self.links.sort(True)
                elif mode == "deleted":
                    conn = self.findConn(name)
                    if conn:
                        self.links.removeItem(self.links.index(conn))
                elif mode == "gotaddress":
                    name, addr = name.split("\n", 1)
                    conn = self.findConn(name)
                    if conn:
                        conn.address = addr
                        self.links.updateItem(conn)
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
    
    def slotSettings(self):
        self.stack.hide()
        self.stack.show()
    
    def slotDouble(self, conn):
        if conn:
            connection.Window(self, conn.name, conn.link_name)
    
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
            if KMessageBox.Yes == KMessageBox.questionYesNo(self, unicode(m) % conn.name, i18n("Delete connection?")):
                self.comar.call_package("Net.Link.deleteConnection", conn.link_name, [ "name", conn.name ])
    
    def slotConnect(self):
        conn = self.links.selectedItem()
        if conn:
            # stop other connections on same device
            item = self.links.firstItem()
            count = 0
            while item:
                if item.online == "up" and item.link_name == conn.link_name and item.device == conn.device:
                    self.comar.call_package("Net.Link.setState", item.link_name, [ "name", item.name, "state", "down" ], id=6)
                    count += 1
                item = item.next()
            if count:
                replies = []
                while 1:
                    rep = self.comar.read_cmd()
                    if rep[1] == 6:
                        count -= 1
                        if count == 0:
                            break
                    else:
                        replies.append(rep)
                if replies:
                    for rep in replies:
                        self.handleComar(rep)
            # up up up!
            self.comar.call_package("Net.Link.setState", conn.link_name, [ "name", conn.name, "state", "up" ])
    
    def slotDisconnect(self):
        conn = self.links.selectedItem()
        if conn:
            self.comar.call_package("Net.Link.setState", conn.link_name, [ "name", conn.name, "state", "down" ])
