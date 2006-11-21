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
import newconn
import widgets
from icons import icons, getIconSet
from comariface import comlink


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
    def __init__(self, view, conn):
        dev = view.devices.get(conn.devid, None)
        if not dev:
            dev = Device(view, conn.devname, conn.devid)
            dev.show()
        QWidget.__init__(self, dev)
        dev.connections.append(self)
        
        self.view = view
        self.conn = conn
        
        fm = self.fontMetrics()
        self.myBase = fm.ascent()
        self.myHeight = fm.height()
        self.mypix = icons.get_state("net", conn.state)
        self.check = QCheckBox(self)
        self.connect(self.check, SIGNAL("toggled(bool)"), self.slotToggle)
        self.check.setAutoMask(True)
        self.edit_but = MinButton(i18n("Edit"), self)
        self.connect(self.edit_but, SIGNAL("clicked()"), self.slotEdit)
        self.del_but = MinButton(i18n("Delete"), self)
        self.connect(self.del_but, SIGNAL("clicked()"), self.slotDelete)
        view.connections[conn.hash] = self
        self.show()
        
        self.ignore_signal = False
    
    def slotToggle(self, on):
        if self.ignore_signal:
            return
        dev = self.parent()
        if on:
            comlink.com.Net.Link[self.conn.script].setState(name=self.conn.name, state="up")
        else:
            comlink.com.Net.Link[self.conn.script].setState(name=self.conn.name, state="down")
    
    def slotDelete(self):
        conn = self.conn
        m = i18n("Should I delete the\n'%s'\nconnection?")
        if KMessageBox.Yes == KMessageBox.questionYesNo(self, unicode(m) % conn.name, i18n("Delete connection?")):
            comlink.com.Net.Link[conn.script].deleteConnection(name=conn.name)
    
    def slotEdit(self):
        w = connection.Window(self.view.parent(), self.conn)
    
    def updateState(self, state):
        # FIXME
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
        paint.drawText(53, self.myBase + 4, unicode(self.conn.name))
        addr = self.conn.net_addr
        if not addr:
            addr = i18n("Automatic")
            if self.conn.address:
                addr += " (%s)" % self.conn.address
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
        rect = fm.boundingRect(self.conn.name)
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
    def __init__(self, parent):
        QScrollView.__init__(self, parent)
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
    
    def add(self, conn):
        Connection(self, conn)
        self.myResize(self.width())
    
    def remove(self, conn):
        conn = self.connections.get(conn.hash, None)
        if not conn:
            return
        dev = self.devices[conn.conn.devid]
        conn.hide()
        dev.removeChild(conn)
        dev.connections.remove(conn)
        del self.connections[conn.conn.hash]
        self.myResize(self.width())


class Widget(QVBox):
    def __init__(self, *args):
        QVBox.__init__(self, *args)
        self.setMargin(6)
        self.setSpacing(6)
        
        bar = QToolBar("lala", None, self)
        
        but = QToolButton(getIconSet("add.png"), i18n("New connection"), "lala", self.slotCreate, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        but = QToolButton(getIconSet("configure.png"), i18n("Name Service Settings"), "lala", self.slotSettings, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        bar.addSeparator()
        
        but = QToolButton(getIconSet("help.png"), i18n("Help"), "lala", self.slotHelp, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        self.view = ConnectionView(self)
        
        #self.stack = stack.Window(self, self.comar)
        
        comlink.new_hook.append(self.view.add)
        comlink.delete_hook.append(self.view.remove)
        comlink.connect()
    
    def uniqueName(self):
        # old remains
        id = 0
        while True:
            name = unicode(i18n("Unconfigured")) + " " + str(id)
            if not self.findConn(name):
                return name
            id += 1
    
    def handleComar(self, reply):
        pass
        # old remains
        #    elif noti == "Net.Link.deviceChanged":
        #        type, rest = data.split(" ", 1)
        #        if type != "new":
        #        nettype, uid, info = rest.split(" ", 2)
        #        self.comar.call_package("Net.Link.setConnection", script, [ "name", name, "device", uid ])
    
    def slotCreate(self):
        win = newconn.Window(self)
        win.show()
    
    def slotSettings(self):
        self.stack.hide()
        self.stack.show()
    
    def slotHelp(self):
        self.helpwin = widgets.HelpDialog("network-manager", i18n("Network Connections Help"), self)
        self.helpwin.show()
