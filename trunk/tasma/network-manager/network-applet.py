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

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

CONNLIST, CONNINFO = range(1,3)


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


class Link:
    def __init__(self, script, data):
        self.script = script
        self.remote_name = None
        for line in data.split("\n"):
            key, value = line.split("=", 1)
            if key == "type":
                self.type = value
            elif key == "name":
                self.name = value
            elif key == "modes":
                self.modes = value.split(",")
            elif key == "remote_name":
                self.remote_name = value


class Comlink:
    def __init__(self):
        self.state_hook = []
        self.devices = {}
        self.links = {}
    
    def connect(self):
        self.com = comar.Link()
        self.com.localize()
    
    def queryConnections(self):
        self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)
        self.notifier.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        self.com.ask_notify("Net.Link.stateChanged")
        self.com.ask_notify("Net.Link.connectionChanged")
        self.com.Net.Link.connections(id=CONNLIST)
    
    def queryLinks(self):
        self.com.Net.Link.linkInfo()
        multiple = False
        while True:
            reply = self.com.read_cmd()
            if reply.command == "start":
                multiple = True
            if not multiple or reply.command == "end":
                break
            if reply.command == "result":
                try:
                    self.links[reply.script] = Link(reply.script, reply.data)
                except ValueError:
                    # background compat hack
                    pass
    
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
            map(lambda x: x(), self.state_hook)
    
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
                map(lambda x: x(), self.state_hook)
    
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
    
    def get_state(self, script, state):
        link = comlink.links.get(script, None)
        if link:
            type = link.type
        else:
            type = "net"
        if not type in ("net", "wifi", "dialup"):
            type = "net"
        if not state in ("up", "connecting", "down"):
            state = "down"
        return self.iconmap.get("%s-%s" % (type, state))


icons = Icons()


class Applet:
    def __init__(self, app):
        self.trays = []
        self.mode = 0
        self.app = app
        comlink.state_hook.append(self.updateIcons)
        app.connect(app, SIGNAL("shutDown()"), self.fixQuit)
    
    def fixQuit(self):
        for item in self.trays:
            item.deleteLater()
    
    def start(self):
        comlink.connect()
        comlink.queryLinks()
        comlink.queryConnections()
        if self.mode == 0:
            self.mode = -1
            self.noGroup(0)
        else:
            self.mode = -1
            self.deviceGroup(0)
    
    def setMenu(self, menu):
        KAction(i18n("Firewall..."), "firewall_config", KShortcut.null(), self.startFirewall, menu).plug(menu)
        KAction(i18n("Edit Connections..."), "configure", KShortcut.null(), self.startManager, menu).plug(menu)
        menu.insertSeparator(1)
        device_mid = menu.insertItem(i18n("Icon Per Device"), self.deviceGroup, 0, -1, 1)
        single_mid = menu.insertItem(i18n("Single Icon"), self.noGroup, 0, -1, 1)
        if self.mode == 0:
            menu.setItemChecked(single_mid, True)
        else:
            menu.setItemChecked(device_mid, True)
    
    def startManager(self):
        os.system("network-manager")
    
    def startFirewall(self):
        os.system("firewall-config")
    
    def reset(self):
        if len(self.trays) > 0:
            for item in self.trays:
                item.hide()
            tray = []
    
    def updateIcons(self):
        for item in self.trays:
            item.updateIcon()
    
    def noGroup(self, id):
        if self.mode == 0:
            return
        self.reset()
        self.mode = 0
        tray = NetTray(self)
        tray.show()
        tray.connect(tray, SIGNAL("quitSelected()"), self.slotQuit)
        self.trays = [tray]

    def deviceGroup(self, id):
        if self.mode == 1:
            return
        self.reset()
        self.mode = 1
        for dev in comlink.devices.values():
            tray = NetTray(self, dev)
            tray.show()
            tray.connect(tray, SIGNAL("quitSelected()"), self.slotQuit)
            self.trays.append(tray)
    
    def slotQuit(self):
        autostart = KMessageBox.questionYesNo(None, i18n("Should network-applet start automatically when you login?"))
        config = KConfig("network-appletrc")
        config.setGroup("General")
        if autostart == KMessageBox.Yes:
            config.writeEntry("AutoStart", "true")
        elif autostart == KMessageBox.No:
            config.writeEntry("AutoStart", "false")
        self.app.quit()


class ConnectionItem(QCustomMenuItem):
    def __init__(self, conn):
        QCustomMenuItem.__init__(self)
        self.conn = conn
        self.mypix = icons.get_state(conn.script, conn.state)
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
    def __init__(self, parent, dev=None):
        KSystemTray.__init__(self)
        self.setPixmap(self.loadIcon("network"))
        menu = self.contextMenu()
        parent.setMenu(menu)
        self.applet = parent
        self.popup = None
        self.dev = dev
        if dev:
            QToolTip.add(self, dev.devname)
        self.updateIcon()
    
    def updateIcon(self):
        if self.dev:
            for conn in self.dev.connections.values():
                script = conn.script
                if conn.state == "connecting":
                    self.setPixmap(icons.get_state(script, "connecting"))
                    return
                elif conn.state == "up":
                    self.setPixmap(icons.get_state(script, "up"))
                    return
        else:
            script = "net-tools"
            for dev in comlink.devices.values():
                for conn in dev.connections.values():
                    if conn.state == "connecting":
                        self.setPixmap(icons.get_state(script, "connecting"))
                        return
                    elif conn.state == "up":
                        self.setPixmap(icons.get_state(script, "up"))
                        return
        self.setPixmap(icons.get_state(script, "down"))
    
    def appendConns(self, menu, dev, idx):
        conn_keys = dev.connections.keys()
        conn_keys.sort(reverse=True)
        for conn_key in conn_keys:
            conn = dev.connections[conn_key]
            conn.mid = menu.insertItem(ConnectionItem(conn), -1, idx)
            if conn.state in ("up", "connecting", "inaccessible"):
                menu.setItemChecked(conn.mid, True)
            menu.connectItem(conn.mid, self.slotSelect)
    
    def buildPopup(self):
        menu = KPopupMenu()
        flag = True
        if self.dev:
            dev = self.dev
            dev_mid = menu.insertTitle(dev.menu_name)
            if len(dev.connections) > 0:
                self.appendConns(menu, dev, menu.indexOf(dev_mid) + 1)
                flag = False
        else:
            keys = comlink.devices.keys()
            keys.sort()
            for key in keys:
                dev = comlink.devices[key]
                dev_mid = menu.insertTitle(dev.menu_name)
                if len(dev.connections) > 0:
                    self.appendConns(menu, dev, menu.indexOf(dev_mid) + 1)
                    flag = False
        if flag:
            menu.insertItem(getIconSet("add"), i18n("New connection"), self.applet.startManager)
        return menu
    
    def mousePressEvent(self, event):
        if event.button() == event.LeftButton:
            if self.popup:
                self.popup.close()
                self.popup = None
            else:
                self.popup = self.buildPopup()
                pt = self.mapToGlobal(QPoint(0, 0))
                self.popup.popup(pt)
                h = self.popup.height()
                if h + 10 > pt.y():
                    y = pt.y() + self.height()
                else:
                    y = pt.y() - h
                self.popup.move(self.popup.x(), y)
        else:
            KSystemTray.mousePressEvent(self, event)
    
    def slotSelect(self, mid):
        menu = self.contextMenu()
        conn = comlink.getConnById(mid)
        if conn.state in ("up", "connecting", "inaccessible"):
            comlink.com.Net.Link[conn.script].setState(name=conn.name, state="down")
        else:
            comlink.com.Net.Link[conn.script].setState(name=conn.name, state="up")
        self.popup = None


def main():
    KLocale.setMainCatalogue("network-manager")
    about = KAboutData(
        "network-applet",
        I18N_NOOP("Network Applet"),
        "0.4",
        None,
        KAboutData.License_GPL,
        "(C) 2006 UEKAE/TÜBİTAK",
        None,
        None,
        "bugs@pardus.org.tr"
    )
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()
    app = KUniqueApplication(True, True, True)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    icons.load_icons()
    applet = Applet(app)
    applet.start()
    app.exec_loop()

if __name__ == "__main__":
    main()
