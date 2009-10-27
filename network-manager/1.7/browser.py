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


class ConnectionTipper(QToolTip):
    def maybeTip(self, point):
        conn = self.parent
        
        rect = conn.rect()
        rect.setWidth(rect.width() - conn.del_but.myWidth - conn.edit_but.myWidth - 6 - 6 - 4)
        rect.setX(rect.x() + conn.pix_start)
        if not rect.contains(point):
            return
        
        conn = conn.conn
        link = comlink.links[conn.script]
        tip = "<nobr>"
        tip += i18n("Name:")
        tip += " <b>%s</b>" % unicode(conn.name)
        tip += "</nobr>"
        if "remote" in link.modes:
            tip += "<br><nobr>%s: %s</nobr>" % (link.remote_name, unicode(conn.remote))
        if "auth" in link.modes:
            if conn.auth_mode != "none":
                tip += "<br><nobr>%s</nobr>" % unicode(i18n("Authentication"))
        if "net" in link.modes:
            tip += "<br><nobr>"
            tip += i18n("Address:")
            if conn.net_mode == "auto":
                tip += " "
                tip += i18n("Automatic")
            else:
                tip += " %s" % conn.net_addr
            tip += "</nobr>"
        
        self.tip(rect, tip)


class Connection(QWidget):
    def __init__(self, view, conn):
        self.is_odd = 0
        dev = view.devices.get(conn.devid, None)
        if not dev:
            dev = Device(view, conn.devname, conn.devid)
            dev.show()
        QWidget.__init__(self, dev)
        self.tipper = ConnectionTipper(self)
        self.tipper.parent = self
        dev.connections.append(self)
        
        self.view = view
        self.conn = conn
        
        self.mypix = icons.get_state(comlink.links[conn.script].type, conn.state)
        if self.conn.state in ("inaccessible", "unavailable"):
            self.mypix = KIconEffect().apply(self.mypix, KIconEffect.ToGray, 1, QColor(), False)
        self.check = QCheckBox(self)
        self.check.setChecked(self.conn.state in ("up", "connecting", "inaccessible"))
        QToolTip.add(self.check, i18n("Turn on/off connection"))
        self.check.setGeometry(6, 3, 16, 16)
        self.connect(self.check, SIGNAL("toggled(bool)"), self.slotToggle)
        self.check.setAutoMask(True)
        
        w = self.check.width()
        self.pix_start = 6 + w + 3
        w = self.mypix.width()
        self.text_start = self.pix_start + w + 6
        
        view.connections[conn.hash] = self
        
        self.edit_but = IconButton("configure.png", self)
        QToolTip.add(self.edit_but, i18n("Configure connection"))
        self.connect(self.edit_but, SIGNAL("clicked()"), self.slotEdit)
        self.del_but = IconButton("cancel.png", self)
        QToolTip.add(self.del_but, i18n("Delete connection"))
        self.connect(self.del_but, SIGNAL("clicked()"), self.slotDelete)
        
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
    
    def updateState(self):
        self.ignore_signal = True
        self.check.setChecked(self.conn.state in ("up", "connecting", "inaccessible"))
        self.ignore_signal = False
        self.mypix = icons.get_state(comlink.links[self.conn.script].type, self.conn.state)
        if self.conn.state in ("inaccessible", "unavailable"):
            self.mypix = KIconEffect().apply(self.mypix, KIconEffect.ToGray, 1, QColor(), False)
        self.update()
    
    def addressText(self):
        text = ""
        if self.conn.state == "up":
            text = self.conn.net_addr
            if not text:
                text = self.conn.message
        else:
            if self.conn.message:
                text = unicode(self.conn.message)
        return text
    
    def paintEvent(self, event):
        paint = QPainter(self)
        col = KGlobalSettings.baseColor()
        if self.is_odd:
            col = KGlobalSettings.alternateBackgroundColor()
        self.edit_but.setPaletteBackgroundColor(col)
        self.del_but.setPaletteBackgroundColor(col)
        paint.fillRect(event.rect(), QBrush(col))
        dip = (self.height() - self.mypix.height()) / 2
        paint.drawPixmap(self.pix_start, dip, self.mypix)
        paint.save()
        font = paint.font()
        font.setPointSize(font.pointSize() + 2)
        font.setBold(True)
        fm = QFontMetrics(font)
        paint.drawText(self.text_start, fm.ascent() + 5, unicode(self.conn.name))
        fark = fm.height()
        paint.restore()
        fm = self.fontMetrics()
        paint.drawText(self.text_start, 5 + fark + 3 + fm.ascent(), self.addressText())
    
    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        dip = (h - self.check.height()) / 2
        self.check.move(6, dip)
        dip = (h - self.del_but.myHeight) / 2
        self.del_but.setGeometry(w - self.del_but.myWidth - 6 - 6, dip, self.del_but.myWidth, self.del_but.myHeight)
        self.edit_but.setGeometry(w - self.del_but.myWidth - 6 - 6 - self.edit_but.myWidth - 3, dip, self.edit_but.myWidth, self.edit_but.myHeight)
        return QWidget.resizeEvent(self, event)
    
    def sizeHint(self):
        f = QFont(self.font())
        f.setPointSize(f.pointSize() + 2)
        f.setBold(True)
        fm = QFontMetrics(f)
        fm2 = self.fontMetrics()
        rect = fm.boundingRect(unicode(self.conn.name))
        rect2 = fm2.boundingRect(self.addressText())
        w = self.text_start + min(rect.width(), 240) + 6 + self.edit_but.myWidth + 3 + self.del_but.myWidth + 6
        w2 = self.text_start + min(rect2.width(), 240) + 6 + self.edit_but.myWidth + 3 + self.del_but.myWidth + 6
        w = max(w, w2)
        h = max(fm.height() + 3 + fm2.height(), 32) + 10
        return QSize(w, h)


class Device(QWidget):
    def __init__(self, parent, name, id):
        QWidget.__init__(self, parent.viewport())
        self.name = name
        self.devid = id
        self.f = QFont(self.font())
        self.f.setPointSize(self.f.pointSize() + 1)
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
        d = []
        for name in names:
            item = self.devices[name]
            c.append(item.columnHint(width))
            d.append(len(item.connections))
        if c != []:
            c = min(c)
            d = max(d)
            if d < 3 and c > d:
                c = d
        for name in names:
            item = self.devices[name]
            item.columns = c
            h = item.heightForWidth(width)
            item.setGeometry(0, th, width, h)
            item.myResize(width, h)
            th += h
        self.resizeContents(width, th)
    
    def resizeEvent(self, event):
        QScrollView.resizeEvent(self, event)
        self.myResize(self.visibleWidth())
    
    def add(self, conn):
        Connection(self, conn)
        self.myResize(self.contentsWidth())
    
    def remove(self, conn):
        conn = self.connections.get(conn.hash, None)
        if not conn:
            return
        dev = self.devices[conn.conn.devid]
        conn.hide()
        conn.deleteLater()
        dev.connections.remove(conn)
        del self.connections[conn.conn.hash]
        if len(dev.connections) == 0:
            dev.hide()
            dev.deleteLater()
            del self.devices[dev.devid]
        self.myResize(self.contentsWidth())
    
    def stateUpdate(self, conn):
        conn = self.connections.get(conn.hash, None)
        if not conn:
            return
        conn.updateState()
    
    def configUpdate(self, conn):
        conn = self.connections.get(conn.hash, None)
        if not conn:
            return
        dev = conn.parent()
        if dev.devid != conn.conn.devid:
            temp = conn.conn
            conn.hide()
            conn.deleteLater()
            dev.connections.remove(conn)
            del self.connections[conn.conn.hash]
            if len(dev.connections) == 0:
                dev.hide()
                dev.deleteLater()
                del self.devices[dev.devid]
            self.add(temp)
    
    def hotPlug(self, uid, info):
        dev = Device(self, info, uid)
        dev.show()
        self.myResize(self.contentsWidth())


class Widget(QVBox):
    def __init__(self, *args):
        QVBox.__init__(self, *args)
        self.setMargin(6)
        self.setSpacing(6)
        
        bar = QToolBar("lala", None, self)
        
        but = QToolButton(getIconSet("add.png"), "", "lala", self.slotCreate, bar)
        but.setTextLabel(i18n("New connection"), False)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        but = QToolButton(getIconSet("configure.png"), "", "lala", self.slotSettings, bar)
        but.setTextLabel(i18n("Name Service Settings"), False)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        lab = QToolButton(bar)
        lab.setEnabled(False)
        bar.setStretchableWidget(lab)
        
        but = QToolButton(getIconSet("help.png"), "", "lala", self.slotHelp, bar)
        but.setTextLabel(i18n("Help"), False)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        self.view = ConnectionView(self)
        
        self.stack = nameconf.Window(self)
        
        comlink.new_hook.append(self.view.add)
        comlink.delete_hook.append(self.view.remove)
        comlink.config_hook.append(self.view.configUpdate)
        comlink.state_hook.append(self.view.stateUpdate)
        comlink.hotplug_hook.append(self.view.hotPlug)
        comlink.noconn_hook.append(self.slotCreate)
        comlink.connect()
    
    def slotCreate(self):
        newconn.ask_for_new(self)
    
    def slotSettings(self):
        self.stack.hide()
        comlink.queryNames()
        self.stack.show()
    
    def slotHelp(self):
        self.helpwin = widgets.HelpDialog("network-manager", i18n("Network Connections Help"), self)
        self.helpwin.show()
