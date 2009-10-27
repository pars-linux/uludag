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
import stack
import connection
from links import links
import comar
import widgets
from icons import icons, getIconSet


def connHash(script, name):
    return unicode("%s %s" % (script, name))


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
        dev.connections.append(self)
        
        self.name = name
        self.script = script
        self.devid = devid
        self.active = False
        self.state = "down"
        self.address = ""
        self.got_address = None
        
        fm = self.fontMetrics()
        self.myBase = fm.ascent()
        self.myHeight = fm.height()
        self.mypix = icons.get_state("net", self.state)
        self.check = QCheckBox(self)
        self.connect(self.check, SIGNAL("toggled(bool)"), self.slotToggle)
        self.check.setAutoMask(True)
        self.edit_but = MinButton(i18n("Edit"), self)
        self.connect(self.edit_but, SIGNAL("clicked()"), self.slotEdit)
        self.del_but = MinButton(i18n("Delete"), self)
        self.connect(self.del_but, SIGNAL("clicked()"), self.slotDelete)
        view.connections[connHash(script, name)] = self
        self.show()
        
        self.view = view
        view.comlink.call_package("Net.Link.getAddress", script, [ "name", name ], id=3)
        view.comlink.call_package("Net.Link.getState", script, [ "name", name ], id=4)
        
        self.ignore_signal = False
    
    def slotComar(self, reply):
        pass
    
    def slotToggle(self, on):
        if self.ignore_signal:
            return
        com = self.view.comlink
        dev = self.parent()
        if on:
            com.call_package("Net.Link.setState", self.script, [ "name", self.name, "state", "up" ])
        else:
            com.call_package("Net.Link.setState", self.script, [ "name", self.name, "state", "down" ])
    
    def slotDelete(self):
        m = i18n("Should I delete the\n'%s'\nconnection?")
        if KMessageBox.Yes == KMessageBox.questionYesNo(self, unicode(m) % self.name, i18n("Delete connection?")):
            self.view.comlink.call_package("Net.Link.deleteConnection", self.script, [ "name", self.name ])
    
    def slotEdit(self):
        w = connection.Window(self.view.parent(), self.name, self.script)
    
    def updateState(self, state):
        msg = ""
        if "\n" in state:
            state, msg = state.split("\n", 1)
        if state == "on":
            self.active = True
        elif state == "off":
            self.active = False
        elif state in ("up", "connecting", "down"):
            self.state = state
        
        if state == "down":
            self.got_address = None
        
        self.ignore_signal = True
        self.check.setChecked(self.active)
        self.ignore_signal = False
        self.mypix = icons.get_state(links.get_info(self.script).type, self.state)
        
        self.update()
    
    def paintEvent(self, event):
        cg = self.colorGroup()
        paint = QPainter(self)
        paint.fillRect(event.rect(), QBrush(cg.midlight()))
        paint.drawPixmap(20, 3, self.mypix)
        paint.drawText(53, self.myBase + 4, self.name)
        addr = self.address
        if not addr:
            addr = i18n("Automatic")
            if self.got_address:
                addr += " (%s)" % self.got_address
        paint.drawText(53, self.myHeight + self.myBase + 5, addr)
    
    def resizeEvent(self, event):
        pix = event.size().width()
        w1, h1 = self.edit_but.mySize()
        w2, h2 = self.del_but.mySize()
        self.edit_but.setGeometry(pix - w1 - w2 - 20 - 4, 1, w1 + 8, h1 + 8)
        self.del_but.setGeometry(pix - w2 - 8 - 4, 1, w2 + 8, h2 + 8)
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
        w = max(rect.width(), 120) + 32 + 16 + 8
        h = max(rect.height(), 32) + 6
        return QSize(w, h)


class Device(QWidget):
    def __init__(self, parent, name, id):
        QWidget.__init__(self, parent.viewport())
        self.name = name
        f = self.font()
        f.setPointSize(f.pointSize() + 1)
        self.setFont(f)
        fm = self.fontMetrics()
        self.myBase = fm.ascent()
        self.connections = []
        parent.devices[id] = self
    
    def myHeight(self):
        fm = self.fontMetrics()
        rect = fm.boundingRect(self.name)
        return max(rect.height() + 6, 24) + 2
    
    def paintEvent(self, event):
        cg = self.colorGroup()
        QWidget.paintEvent(self, event)
        paint = QPainter(self)
        paint.fillRect(QRect(0, 0, self.width(), self.myHeight()), QBrush(cg.mid(), Qt.Dense7Pattern))
        paint.fillRect(QRect(0, self.myHeight(), self.width(), self.height() - self.myHeight()), QBrush(cg.midlight()))
        paint.drawText(25, self.myBase + 5, self.name)
    
    def heightForWidth(self, width):
        h = self.myHeight()
        
        if self.connections == []:
            return h
        
        maxw = 0
        maxh = 0
        for item in self.connections:
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
        L = len(self.connections)
        if L % c != 0:
            L += c
        h += (maxh + 2) * (L / c)
        
        return h
    
    def myResize(self, aw, ah):
        myh = self.myHeight()
        
        maxw = 0
        maxh = 0
        childs = self.connections
        if not childs or len(childs) == 0:
            return
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
        childs.sort(key=lambda x: x.name)
        for item in childs:
            item.setGeometry(i * maxw, myh + j * maxh, maxw, maxh)
            i += 1
            if i >= c:
                i = 0
                j += 1
    
    def resizeEvent(self, event):
        size = event.size()
        self.myResize(size.width(), size.height())
        return QWidget.resizeEvent(self, event)


class ConnectionView(QScrollView):
    def __init__(self, parent, comlink):
        QScrollView.__init__(self, parent)
        self.comlink = comlink
        self.devices = {}
        self.connections = {}
    
    def myResize(self, width):
        th = 0
        names = self.devices.keys()
        names.sort()
        for name in names:
            item = self.devices[name]
            h = item.heightForWidth(width)
            item.setGeometry(0, th, width, h)
            item.myResize(width, h)
            th += h
    
    def resizeEvent(self, event):
        w = event.size().width()
        self.myResize(w)
        return QScrollView.resizeEvent(self, event)
    
    def add(self, script, data):
        name = data.split("\n")[0]
        if self.find(script, name) != None:
            return
        Connection(self, script, data)
        self.myResize(self.width())
    
    def remove(self, script, name):
        conn = self.find(script, name)
        if not conn:
            return
        dev = self.devices[conn.devid]
        conn.hide()
        dev.removeChild(conn)
        dev.connections.remove(conn)
        del self.connections[connHash(script, name)]
        self.myResize(self.width())
    
    def find(self, script, name):
        return self.connections.get(connHash(script, name), None)


class Widget(QVBox):
    def __init__(self, *args):
        QVBox.__init__(self, *args)
        self.setMargin(6)
        self.setSpacing(6)
        
        bar = QToolBar("lala", None, self)
        
        but = QToolButton(getIconSet("add.png"), i18n("New connection"), "lala", self.slotCreate, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        bar.addSeparator()
        
        but = QToolButton(getIconSet("configure.png"), i18n("Name Service Settings"), "lala", self.slotSettings, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        bar.addSeparator()
        
        but = QToolButton(getIconSet("help.png"), i18n("Help"), "lala", self.slotHelp, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        self.comar = comar.Link()
        
        self.view = ConnectionView(self, self.comar)
        
        self.stack = stack.Window(self, self.comar)
        links.query(self.comar)
        
        self.comar.ask_notify("Net.Link.stateChanged")
        self.comar.ask_notify("Net.Link.connectionChanged")
        self.comar.ask_notify("Net.Link.deviceChanged")
        
        self.comar.call("Net.Link.connections", id=1)
        
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
    
    def uniqueName(self):
        id = 0
        while True:
            name = unicode(i18n("Unconfigured")) + " " + str(id)
            if not self.findConn(name):
                return name
            id += 1
    
    def slotHelp(self):
        self.helpwin = widgets.HelpDialog("network-manager", i18n("Network Connections Help"), self)
        self.helpwin.show()
    
    def slotComar(self, sock):
        reply = self.comar.read_cmd()
        self.handleComar(reply)
    
    def handleComar(self, reply):
        if reply.command == "result":
            if reply.id == 1:
                if reply[2] == "":
                    self.comar.call_package("Net.Link.deviceList", reply[3], id=5)
                else:
                    for name in reply[2].split("\n"):
                        self.comar.call_package("Net.Link.connectionInfo", reply.script, [ "name", name ], id=2)
            elif reply.id == 2:
                self.view.add(reply.script, reply.data)
            elif reply.id == 3:
                name, mode, rest = reply.data.split("\n", 2)
                if "\n" in rest:
                    addr, gate = rest.split("\n", 1)
                else:
                    addr = rest
                conn = self.view.find(reply.script, name)
                if conn:
                    if mode == "manual":
                        conn.address = addr
                    else:
                        conn.address = None
                        if addr != "":
                            conn.got_address = addr
                    conn.update()
            elif reply.id == 4:
                name, state = reply.data.split("\n")
                conn = self.view.find(reply.script, name)
                if conn:
                    if state == "up":
                        conn.active = True
                    else:
                        conn.active = False
                    conn.updateState(state)
            elif reply.id == 5:
                return
                #FIXME
                if reply[2] == '' or reply[3] == "ppp":
                    return
                devs = reply[2].split("\n")
                for dev in devs:
                    uid, rest = dev.split(" ", 1)
                    name = self.uniqueName()
                    self.comar.call_package("Net.Link.setConnection", reply[3], [ "name", name, "device", uid ])
                    Connection(self.links, self.comar, name, reply[3])
            elif reply.id == 42:
                links.slotComar(reply)
            elif reply.id > 42:
                self.stack.slotComar(reply)
        
        elif reply.command == "notify":
            if reply.notify == "Net.Link.stateChanged":
                name, state = reply.data.split("\n", 1)
                conn = self.view.find(reply.script, name)
                if conn:
                    conn.updateState(state)
            
            elif reply.notify == "Net.Link.connectionChanged":
                mode, name = reply.data.split(" ", 1)
                if mode == "added":
                    self.comar.call_package("Net.Link.connectionInfo", reply.script, [ "name", name ], id=2)
                elif mode == "deleted":
                    self.view.remove(reply.script, name)
                elif mode == "gotaddress":
                    name, addr = name.split("\n", 1)
                    conn = self.view.find(reply.script, name)
                    if conn:
                        conn.got_address = addr
                        conn.update()
                elif mode == "configured":
                    type, name = name.split(" ", 1)
                    if type == "device":
                        self.comar.call_package("Net.Link.connectionInfo", reply.script, [ "name", name ], id=2)
                    elif type == "address":
                        self.comar.call_package("Net.Link.getAddress", reply.script, [ "name", name ], id=3)
                    elif type == "state":
                        self.comar.call_package("Net.Link.getState", reply.script, [ "name", name ], id=4)
            
            elif noti == "Net.Link.deviceChanged":
                # FIXME
                return
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
