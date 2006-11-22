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

import nameconf
import connection
import newconn
import widgets
from icons import icons, getIconSet
from comariface import comlink


class IconButton(QPushButton):
    def __init__(self, name, parent):
        QPushButton.__init__(self, parent)
        self.setFlat(True)
        self.myset = getIconSet(name, KIcon.Small)
        self.setIconSet(self.myset)
        size = self.myset.iconSize(QIconSet.Small)
        self.myWidth = size.width() + 4
        self.myHeight = size.height() + 4
        self.resize(self.myWidth, self.myHeight)


class Connection(QWidget):
    def __init__(self, view, conn):
        self.is_odd = 0
        
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
        self.mypix = icons.get_state(comlink.links[conn.script].type, conn.state)
        self.check = QCheckBox(self)
        self.check.setGeometry(3, 3, self.check.width(), self.check.height())
        self.connect(self.check, SIGNAL("toggled(bool)"), self.slotToggle)
        self.check.setAutoMask(True)
        view.connections[conn.hash] = self
        
        self.edit_but = IconButton("configure.png", self)
        QToolTip.add(self.edit_but, i18n("Configure connection"))
        self.connect(self.edit_but, SIGNAL("clicked()"), self.slotEdit)
        self.diksi = IconButton("edittrash.png", self)
        QToolTip.add(self.diksi, i18n("Delete connection"))
        self.connect(self.diksi, SIGNAL("clicked()"), self.slotDelete)
        
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
    
    def mouseDoubleClickEvent(self, event):
        self.slotEdit()
    
    def updateState(self, state):
        # FIXME
        self.ignore_signal = True
        self.check.setChecked(self.active)
        self.ignore_signal = False
        self.mypix = icons.get_state(links.get_info(self.script).type, self.state)
        
        self.update()
    
    def addressText(self):
        addr = self.conn.net_addr
        if not addr:
            addr = i18n("Automatic")
            if self.conn.address:
                addr += " (%s)" % self.conn.address
        return addr
    
    def paintEvent(self, event):
        paint = QPainter(self)
        col = KGlobalSettings.baseColor()
        if self.is_odd:
            col = KGlobalSettings.alternateBackgroundColor()
        self.edit_but.setPaletteBackgroundColor(col)
        self.diksi.setPaletteBackgroundColor(col)
        paint.fillRect(event.rect(), QBrush(col))
        paint.drawPixmap(20, 3, self.mypix)
        paint.save()
        font = paint.font()
        #font.setUnderline(True)
        font.setPointSize(font.pointSize() + 2)
        #paint.pen().setColor(KGlobalSettings.linkColor())
        paint.drawText(53, self.myBase + 5, unicode(self.conn.name))
        paint.restore()
        paint.drawText(53, self.myHeight + self.myBase + 7, self.addressText())
    
    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        dip = (h - self.diksi.myHeight) / 2
        self.diksi.setGeometry(w - self.diksi.myWidth - 6 - 6, dip, self.diksi.myWidth, self.diksi.myHeight)
        self.edit_but.setGeometry(w - self.diksi.myWidth - 6 - 6 - self.edit_but.myWidth - 3, dip, self.edit_but.myWidth, self.edit_but.myHeight)
        return QWidget.resizeEvent(self, event)
    
    def sizeHint(self):
        fm = self.fontMetrics()
        rect = fm.boundingRect(unicode(self.conn.name))
        rect2 = fm.boundingRect(self.addressText())
        w = max(rect.width(), 80) + 32 + 16 + self.diksi.myWidth + 3 + self.edit_but.myWidth + 8 + 8
        w2 = max(rect2.width(), 80) + 32 + 16 + self.diksi.myWidth + 3 + self.edit_but.myWidth + 8 + 8
        w = max(w, w2)
        h = max(rect.height() + rect2.height(), 32) + 6
        return QSize(w, h)


class Device(QWidget):
    def __init__(self, parent, name, id):
        QWidget.__init__(self, parent.viewport())
        self.name = name
        self.f = QFont(self.font())
        self.f.setBold(True)
        fm = QFontMetrics(self.f)
        self.myBase = fm.ascent()
        self.connections = []
        parent.devices[id] = self
        self.setPaletteBackgroundColor(KGlobalSettings.baseColor())
        self.columns = 3
    
    def myHeight(self):
        fm = QFontMetrics(self.f)
        rect = fm.boundingRect(self.name)
        return rect.height() + 7
    
    def paintEvent(self, event):
        cg = self.colorGroup()
        QWidget.paintEvent(self, event)
        paint = QPainter(self)
        paint.fillRect(QRect(0, 0, self.width(), self.myHeight()), QBrush(KGlobalSettings.buttonBackground(), Qt.Dense3Pattern))
        paint.save()
        paint.setFont(self.f)
        paint.drawText(6, self.myBase + 3, self.name)
        paint.restore()
    
    def maxHint(self):
        maxw = 0
        maxh = 0
        for item in self.connections:
            hint = item.sizeHint()
            w = hint.width()
            h = hint.height()
            if w > maxw:
                maxw = w
            if h > maxh:
                maxh = h
        return maxw, maxh
    
    def columnHint(self, width):
        if self.connections == []:
            return 3
        maxw, maxh = self.maxHint()
        c = width / maxw
        if c < 1:
            c = 1
        if c > 3:
            c = 3
        return c
    
    def heightForWidth(self, width):
        h = self.myHeight()
        maxw, maxh = self.maxHint()
        L = len(self.connections)
        if L % self.columns != 0:
            L += self.columns
        return h + (L / self.columns) * maxh
    
    def myResize(self, aw, ah):
        childs = self.connections
        if not childs or len(childs) == 0:
            return
        
        i = 0
        j = 0
        maxw = aw / self.columns
        maxh = self.maxHint()[1]
        myh = self.myHeight()
        childs.sort(key=lambda x: x.conn.name)
        for item in childs:
            item.is_odd = (i + j) % 2
            item.setGeometry(i * maxw, myh + j * maxh, maxw, maxh)
            item.update()
            i += 1
            if i >= self.columns:
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
        self.viewport().setPaletteBackgroundColor(KGlobalSettings.baseColor())
    
    def myResize(self, width):
        th = 0
        names = self.devices.keys()
        names.sort()
        c = []
        for name in names:
            item = self.devices[name]
            c.append(item.columnHint(width))
        if c != []:
            c = min(c)
        for name in names:
            item = self.devices[name]
            item.columns = c
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
        
        self.stack = nameconf.Window(self)
        
        comlink.new_hook.append(self.view.add)
        comlink.delete_hook.append(self.view.remove)
        comlink.connect()
    
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
        comlink.queryNames()
        self.stack.show()
    
    def slotHelp(self):
        self.helpwin = widgets.HelpDialog("network-manager", i18n("Network Connections Help"), self)
        self.helpwin.show()
