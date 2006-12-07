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


class Connection:
    @staticmethod
    def hash(script, name):
        return unicode("%s %s" % (script, name))
    
    def __init__(self, script, data):
        self.script = None
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
        self.hash = self.hash(self.script, self.name)
    
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
        self.new_hook = []
        self.connections = {}
    
    def connect(self):
        self.com = comar.Link()
        self.com.localize()
        self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)
        self.notifier.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
    
    def queryConnections(self):
        self.com.Net.Link.connections(id=CONNLIST)
    
    def slotComar(self, sock):
        reply = self.com.read_cmd()
        if reply.command == "result":
            self.handleReply(reply)
        else:
            print reply
    
    def handleReply(self, reply):
        if reply.id == CONNLIST:
            if reply.data != "":
                for name in reply.data.split("\n"):
                    self.com.Net.Link[reply.script].connectionInfo(name=name, id=CONNINFO)
        
        elif reply.id == CONNINFO:
            conn = Connection(reply.script, reply.data)
            map(lambda x: x(conn), self.new_hook)
            self.connections[conn.hash] = conn


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


class NetTray(KSystemTray):
    def __init__(self, parent):
        KSystemTray.__init__(self, parent)
        self.setPixmap(self.loadIcon("network"))
        menu = self.contextMenu()
        KAction(i18n("Edit Connections..."), "configure", KShortcut.null(), self.slotEdit, self).plug(menu)
        menu.insertSeparator(1)
        self.devices = {}
        comlink.new_hook.append(self.slotNew)
    
    def slotEdit(self):
        os.system("network-manager")
    
    def slotNew(self, conn):
        menu = self.contextMenu()
        dev = self.devices.get(conn.devid, None)
        if not dev:
            dev = KPopupMenu(self)
            menu.insertItem(unicode(conn.devname), dev, -1, 1)
            self.devices[conn.devid] = dev
        dev.insertItem(unicode(conn.name), -1)


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
