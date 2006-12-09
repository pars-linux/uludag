#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import sys
import comar
from qt import *
from kdecore import *
from kdeui import *

I18N_NOOP = lambda x: x

CONNLIST, CONNINFO = range(2)


class Device:
    def __init__(self, devid, devname):
        self.mid = -1
        self.devid = devid
        self.devname = devname
        self.connections = {}
        self.menu_name = unicode(devname)
        if len(self.menu_name) > 25:
            self.menu_name = self.menu_name[:22] + "..."


class Connection:
    def __init__(self, script, data):
        self.mid = -1
        self.device = None
        self.script = script
        self.name = None
        self.devid = None
        self.devname = None
        self.remote = None
        self.state = "unavailable"
        self.message = None
        self.net_mode = "auto"
        self.net_addr = None
        self.net_gateway = None
        self.parse(data)
        self.menu_name = unicode(self.name)
    
    def parse(self, data):
        for line in data.split("\n"):
            key, value = line.split("=", 1)
            if key == "name":
                self.name = value
            elif key == "device_id":
                self.devid = value
            elif key == "device_name":
                self.devname = value
            elif key == "remote":
                self.remote = value
            elif key == "net_mode":
                self.net_mode = value
            elif key == "net_address":
                self.net_addr = value
            elif key == "net_gateway":
                self.net_gate = value
            elif key == "state":
                if " " in value:
                    self.state, self.message = value.split(" ", 1)
                else:
                    self.state = value


class Comlink:
    def __init__(self):
        self.change_hook = []
        self.state_hook = []
        self.devices = {}
    
    def connect(self):
        self.com = comar.Link()
        self.com.localize()
        self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)
        self.notifier.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
    
    def queryConnections(self):
        self.com.ask_notify("Net.Link.stateChanged")
        self.com.ask_notify("Net.Link.connectionChanged")
        self.com.Net.Link.connections(id=CONNLIST)
    
    def slotComar(self, sock):
        reply = self.com.read_cmd()
        if reply.command == "result":
            self.handleReply(reply)
        elif reply.command == "notify":
            self.handleNotify(reply)
        else:
            print reply
    
    def handleReply(self, reply):
        if reply.id == CONNLIST:
            if reply.data != "":
                for name in reply.data.split("\n"):
                    self.com.Net.Link[reply.script].connectionInfo(name=name, id=CONNINFO)
        
        elif reply.id == CONNINFO:
            conn = Connection(reply.script, reply.data)
            dev = self.devices.get(conn.devid, None)
            if not dev:
                dev = Device(conn.devid, conn.devname)
                self.devices[conn.devid] = dev
            dev.connections[conn.name] = conn
            conn.device = dev
            map(lambda x: x(), self.change_hook)
    
    def handleNotify(self, reply):
        if reply.notify == "Net.Link.stateChanged":
            name, state = reply.data.split("\n", 1)
            conn = self.getConn(reply.script, name)
            if conn:
                msg = None
                if " " in state:
                    state, msg = state.split(" ", 1)
                conn.message = msg
                conn.state = state
                map(lambda x: x(conn), self.state_hook)
    
    def getConn(self, script, name):
        for dev in self.devices.values():
            for conn in dev.connections.values():
                if conn.script == script and conn.name == name:
                    return conn
        return None
    
    def getConnById(self, mid):
        for dev in self.devices.values():
            for conn in dev.connections.values():
                if conn.mid == mid:
                    return conn
        return None


comlink = Comlink()


class Icons:
    def _pix(self, name):
        img = QImage(locate("data", "network-manager/" + name))
        img = img.smoothScale(24, 24)
        return QPixmap(img)
    
    def load_icons(self):
        self.iconmap = {
            "net-up": self._pix("ethernet-online.png"),
            "net-connecting": self._pix("ethernet-connecting.png"),
            "net-down": self._pix("ethernet-offline.png"),
            "wifi-up": self._pix("wireless-online.png"),
            "wifi-connecting": self._pix("wireless-connecting.png"),
            "wifi-down": self._pix("wireless-offline.png"),
            "dialup-up": self._pix("dialup-online.png"),
            "dialup-connecting": self._pix("dialup-connecting.png"),
            "dialup-down": self._pix("dialup-offline.png")
        }
    
    def get_state(self, type, state):
        if not type in ("net", "wifi", "dialup"):
            type = "net"
        if not state in ("up", "connecting", "down"):
            state = "down"
        return self.iconmap.get("%s-%s" % (type, state))


icons = Icons()


class Applet(KMainWindow):
    def __init__(self):
        KMainWindow.__init__(self)
        self.setCaption(i18n("Network Panel Applet Settings"))
    
    def start(self):
        comlink.connect()
        comlink.queryConnections()
    
    def setMenu(self, menu):
        KAction(i18n("Firewall..."), "firewall_config", KShortcut.null(), self.startFirewall, self).plug(menu)
        KAction(i18n("Edit Connections..."), "configure", KShortcut.null(), self.startManager, self).plug(menu)
        menu.insertSeparator(1)
        menu.insertItem(i18n("Icon Per Device"), self.noGroup, 0, -1, 1)
        mid = menu.insertItem(i18n("Single Icon"), self.deviceGroup, 0, -1, 1)
        menu.setItemChecked(mid, True)
    
    def startManager(self):
        os.system("network-manager")
    
    def startFirewall(self):
        os.system("firewall-config")
    
    def noGroup(self, id):
        print "no group"
    
    def deviceGroup(self, id):
        print "device group"


class ConnectionItem(QCustomMenuItem):
    def __init__(self, conn):
        QCustomMenuItem.__init__(self)
        self.conn = conn
        self.mypix = icons.get_state("net", conn.state)
        self.text_start = self.mypix.width() + 6
    
    def paint(self, paint, cg, act, enabled, x, y, w, h):
        paint.setFont(self.my_font)
        fm = paint.fontMetrics()
        paint.drawPixmap(x + 3, y + (h - self.mypix.height()) / 2, self.mypix)
        paint.drawText(x + self.text_start, y + fm.ascent(), self.conn.menu_name)
        if self.conn.message:
            paint.drawText(x + self.text_start, y + fm.height() + fm.ascent(), unicode(self.conn.message))
    
    def sizeHint(self):
        fm = QFontMetrics(self.my_font)
        rect = fm.boundingRect(self.conn.menu_name)
        tw, th = rect.width(), fm.height()
        if self.conn.message:
            rect2 = fm.boundingRect(self.conn.message)
            tw = max(tw, rect2.width())
        tw += self.text_start
        th += 3 + fm.height()
        th = max(th, self.mypix.height() + 6)
        return QSize(tw, th)
    
    def setFont(self, font):
        self.my_font = QFont(font)


class NetTray(KSystemTray):
    def __init__(self, parent):
        KSystemTray.__init__(self, parent)
        self.setPixmap(self.loadIcon("network"))
        menu = self.contextMenu()
        parent.setMenu(menu)
        self.popup = None
    
    def buildPopup(self):
        menu = KPopupMenu()
        keys = comlink.devices.keys()
        keys.sort()
        for key in keys:
            dev = comlink.devices[key]
            dev_mid = menu.insertTitle(dev.menu_name)
            conn_keys = dev.connections.keys()
            conn_keys.sort(reverse=True)
            for conn_key in conn_keys:
                conn = dev.connections[conn_key]
                conn.mid = menu.insertItem(ConnectionItem(conn), -1, menu.indexOf(dev_mid) + 1)
                if conn.state in ("up", "connecting", "inaccessible"):
                    menu.setItemChecked(conn.mid, True)
                menu.connectItem(conn.mid, self.slotSelect)
        return menu
    
    def mousePressEvent(self, event):
        if event.button() == event.LeftButton:
            if self.popup:
                self.popup.close()
                self.popup = None
            else:
                self.popup = self.buildPopup()
                self.popup.popup(event.globalPos())
        else:
            KSystemTray.mousePressEvent(self, event)
    
    def slotSelect(self, mid):
        menu = self.contextMenu()
        conn = comlink.getConnById(mid)
        if menu.isItemChecked(mid):
            comlink.com.Net.Link[conn.script].setState(name=conn.name, state="down")
        else:
            comlink.com.Net.Link[conn.script].setState(name=conn.name, state="up")


def main():
    about = KAboutData(
        "network-applet",
        I18N_NOOP("Network Applet"),
        "0.1",
        None,
        KAboutData.License_GPL,
        "(C) 2006 UEKAE/TÜBİTAK",
        None,
        None,
        "bugs@pardus.org.tr"
    )
    KCmdLineArgs.init(sys.argv, about)
    app = KApplication()
    KGlobal.locale().insertCatalogue("network-manager")
    icons.load_icons()
    win = Applet()
    win.start()
    tray = NetTray(win)
    tray.show()
    win.tray = tray
    app.exec_loop()

if __name__ == "__main__":
    main()
