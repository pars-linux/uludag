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
        self.update()
    
    def update(self):
        self.menu_name = unicode(self.name)
        if self.message:
            self.menu_name += " (%s)" % self.message
    
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
                conn.update()
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


class Applet(KMainWindow):
    def __init__(self):
        KMainWindow.__init__(self)
        self.setCaption(i18n("Network Panel Applet Settings"))
        
        vb = QVBox(self)
        vb.setMargin(12)
        vb.setSpacing(6)
        
        self.r1 = QRadioButton(i18n("Single icon mode"), vb)
        self.r2 = QRadioButton(i18n("Device icon mode"), vb)
        
        self.setCentralWidget(vb)
    
    def start(self):
        comlink.connect()
        comlink.queryConnections()
    
    def setMenu(self, menu):
        KAction(i18n("Firewall..."), "firewall_config", KShortcut.null(), self.startFirewall, self).plug(menu)
        KAction(i18n("Edit Connections..."), "configure", KShortcut.null(), self.startManager, self).plug(menu)
    
    def startManager(self):
        os.system("network-manager")
    
    def startFirewall(self):
        os.system("firewall-config")


class NetTray(KSystemTray):
    def __init__(self, parent):
        KSystemTray.__init__(self, parent)
        self.setPixmap(self.loadIcon("network"))
        menu = self.contextMenu()
        parent.setMenu(menu)
        comlink.change_hook.append(self.slotChange)
        comlink.state_hook.append(self.slotState)
    
    def slotChange(self):
        menu = self.contextMenu()
        menu.clear()
        menu.insertTitle("Network Applet")
        self.parent().setMenu(menu)
        menu.insertSeparator()
        for action in self.actionCollection().actions():
            action.plug(menu)
        
        keys = comlink.devices.keys()
        keys.sort(reverse=True)
        for key in keys:
            dev = comlink.devices[key]
            dev.mid = menu.insertTitle(dev.menu_name, -1, 0)
            conn_keys = dev.connections.keys()
            conn_keys.sort(reverse=True)
            for conn_key in conn_keys:
                conn = dev.connections[conn_key]
                conn.mid = menu.insertItem(conn.menu_name, self.slotSelect, 0, -1, menu.indexOf(dev.mid) + 1)
                if conn.state in ("up", "inaccessible"):
                    menu.setItemChecked(conn.mid, True)
    
    def slotSelect(self, mid):
        menu = self.contextMenu()
        conn = comlink.getConnById(mid)
        if menu.isItemChecked(mid):
            comlink.com.Net.Link[conn.script].setState(name=conn.name, state="down")
        else:
            comlink.com.Net.Link[conn.script].setState(name=conn.name, state="up")
    
    def slotState(self, conn):
        menu = self.contextMenu()
        mid = conn.mid
        if conn.state in ("up", "inaccessible"):
            menu.setItemChecked(mid, True)
        else:
            menu.setItemChecked(mid, False)
        menu.changeItem(mid, conn.menu_name)


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
    win = Applet()
    win.start()
    tray = NetTray(win)
    tray.show()
    win.tray = tray
    app.exec_loop()

if __name__ == "__main__":
    main()
