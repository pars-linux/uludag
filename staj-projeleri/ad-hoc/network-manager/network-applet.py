#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import sys
import time
from qt import *
from kdecore import *
from kdeui import *
import  dcopext
import autoswitch
import pynotify

import dbus
from dbus.mainloop.qt3 import DBusQtMainLoop
from handler import CallHandler

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
    @staticmethod
    def hash(script, name):
        return unicode("%s %s" % (script, name))
    
    def __init__(self, script, data):
        self.mid = -1
        self.device = None
        self.script = script
        self.name = None
        self.devid = None
        self.devname = None
        self.remote = None
        self.apmac = None
        self.state = "unavailable"
        self.message = None
        self.net_mode = "auto"
        self.net_addr = None
        self.net_gateway = None
        self.parse(data)
        self.hash = self.hash(self.script, self.name)
        self.menu_name = unicode(self.name)
    
    def parse(self, data):
        for key, value in data.iteritems():
            if key == "name":
                self.name = value
            elif key == "device_id":
                self.devid = value
            elif key == "device_name":
                self.devname = value
            elif key == "remote":
                self.remote = value
            elif key == "apmac":
                self.apmac = value
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
        for key, value in data.iteritems():
            if key == "type":
                self.type = value
            elif key == "name":
                self.name = value
            elif key == "modes":
                self.modes = value.split(",")
            elif key == "remote_name":
                self.remote_name = value


class DBusInterface:
    def __init__(self):
        self.state_hook = []
        self.connections = {}
        self.devices = {}
        self.links = {}
        
        self.dia = None
        self.busSys = None
        self.busSes = None
        
        self.first_time = True
        self.nr_queried = 0
        self.nr_conns = 0
        self.nr_empty = 0
        self.winID = 0
        
        if self.openBus():
            self.setup()
    
    def openBus(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException, exception:
            self.errorDBus(exception)
            return False
        return True
    
    def callHandler(self, script, model, method, action):
        ch = CallHandler(script, model, method, action, self.winID, self.busSys, self.busSes)
        ch.registerError(self.error)
        ch.registerDBusError(self.errorDBus)
        ch.registerAuthError(self.errorDBus)
        return ch
    
    def call(self, script, model, method, *args):
        try:
            obj = self.busSys.get_object("tr.org.pardus.comar", "/package/%s" % script)
            iface = dbus.Interface(obj, dbus_interface="tr.org.pardus.comar.%s" % model)
        except dbus.DBusException, exception:
            self.errorDBus(exception)
            return
        try:
            func = getattr(iface, method)
            return func(*args)
        except dbus.DBusException, exception:
            self.error(exception)
    
    def callSys(self, method, *args):
        try:
            obj = self.busSys.get_object("tr.org.pardus.comar", "/")
            iface = dbus.Interface(obj, dbus_interface="tr.org.pardus.comar")
        except dbus.DBusException, exception:
            self.errorDBus(exception)
        try:
            func = getattr(iface, method)
            return func(*args)
        except dbus.DBusException, exception:
            self.error(exception)
    
    def error(self, exception):
        print exception
    
    def errorDBus(self, exception):
        if self.dia:
            return
        self.dia = KProgressDialog(None, "lala", i18n("Waiting DBus..."), i18n("Connection to the DBus unexpectedly closed, trying to reconnect..."), True)
        self.dia.progressBar().setTotalSteps(50)
        self.dia.progressBar().setTextEnabled(False)
        self.dia.show()
        start = time.time()
        while time.time() < start + 5:
            if self.openBus():
                self.dia.close()
                self.setup()
                return
            if self.dia.wasCancelled():
                break
            percent = (time.time() - start) * 10
            self.dia.progressBar().setProgress(percent)
            qApp.processEvents(100)
        self.dia.close()
        KMessageBox.sorry(None, i18n("Cannot connect to the DBus! If it is not running you should start it with the 'service dbus start' command in a root console."))
        sys.exit()
    
    def setup(self, first_time=True):
        if first_time:
            self.queryLinks()
    
    def handleSignals(self, *args, **kwargs):
        path = kwargs["path"]
        signal = kwargs["signal"]
        if not path.startswith("/package/"):
            return
        script = path[9:]

        if signal == "stateChanged":
            profile, state, msg = args
            conn = self.getConn(script, profile)
            if conn:
                conn.message = msg
                conn.state = state
                map(lambda x: x(), self.state_hook)
        elif signal == "connectionChanged":
            what, profile = args
            if what == "added" or what == "configured":
                ch = self.callHandler(script, "Net.Link", "connectionInfo", "tr.org.pardus.comar.net.link.get")
                ch.registerDone(self.handleConnectionInfo, script)
                ch.call(profile)
            elif what == "deleted":
                conn = self.getConn(script, profile)
                if conn:
                    dev = self.devices.get(conn.devid, None)
                    if dev:
                        del dev.connections[conn.name]
                        if len(dev.connections) == 0:
                            del self.devices[dev.devid]
                    map(lambda x: x(), self.state_hook)
    
    def listenSignals(self):
        self.busSys.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.Net.Link", member_keyword="signal", path_keyword="path")
    
    def queryLinks(self):
        scripts = self.callSys("listModelApplications", "Net.Link")
        if scripts:
            for script in scripts:
                info = self.call(script, "Net.Link", "linkInfo")
                self.links[script] = Link(script, info)
    
    def handleConnectionInfo(self, script, info):
        conn = Connection(script, info)
        old_conn = self.getConn(script, conn.name)
        if old_conn:
            if old_conn.devid != conn.devid:
                dev = self.devices.get(old_conn.devid, None)
                if dev:
                    del dev.connections[old_conn.name]
                    if len(dev.connections) == 0:
                        del self.devices[dev.devid]
                dev = self.devices.get(conn.devid, None)
                if not dev:
                    dev = Device(conn.devid, conn.devname)
                    self.devices[conn.devid] = dev
                dev.connections[conn.name] = conn
            else:
                old_conn.parse(info)
            if self.first_time:
                map(lambda x: x(), self.state_hook)
            return
        dev = self.devices.get(conn.devid, None)
        if not dev:
            dev = Device(conn.devid, conn.devname)
            self.devices[conn.devid] = dev
        self.connections[conn.hash] = conn
        dev.connections[conn.name] = conn
        conn.device = dev
        if self.first_time:
            map(lambda x: x(), self.state_hook)
            # After all connections' information fetched...
            if self.nr_queried == len(self.links) and self.nr_conns == len(self.connections):
                self.first_time = False
                self.listenSignals()
    
    def queryConnections(self, script):
        def handler(profiles):
            self.nr_queried += 1
            for profile in profiles:
                self.nr_conns += 1
                _ch = self.callHandler(script, "Net.Link", "connectionInfo", "tr.org.pardus.comar.net.link.get")
                _ch.registerDone(self.handleConnectionInfo, script)
                _ch.call(profile)
            if not len(profiles):
                self.nr_empty += 1
                # if no connections present, start listening for signals now
                if len(self.links) == self.nr_empty:
                    if self.first_time:
                        self.first_time = False
                        # get signals
                        self.listenSignals()
        ch = self.callHandler(script, "Net.Link", "connections", "tr.org.pardus.comar.net.link.get")
        ch.registerDone(handler)
        ch.call()
    
    def getConn(self, script, name):
        hash = Connection.hash(script, name)
        return self.connections.get(hash, None)
    
    def getConnById(self, mid):
        for dev in self.devices.values():
            for conn in dev.connections.values():
                if conn.mid == mid:
                    return conn
        return None


class Icons:
    def _pix(self, name, justGetPath=False):
        path= locate("data", "network-manager/" + name)
        img = QImage(path)
        img = img.smoothScale(24, 24)
        if justGetPath:
            return path
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

    def getPath(self,icon):
        return KGlobal.iconLoader().iconPath(icon, KIcon.Desktop, True)

icons = Icons()


class Applet:
    def __init__(self, app):
        self.trays = []
        self.mode = 0
        self.app = app
        self.config = KConfig("network-appletrc")
        self.config.setGroup("General")
        self.autoConnect = self.config.readBoolEntry("AutoConnect",True)
        self.showNotifications = self.config.readBoolEntry("ShowNotifications",True)
        self.notifier = False
        comlink.state_hook.append(self.updateIcons)
        self.delayTimer = QTimer()
        app.connect(app, SIGNAL("shutDown()"), self.fixQuit)
        app.connect(self.delayTimer, SIGNAL("timeout()"), self.createNotifier)

    def createNotifier(self,dry=False):
        pynotify.init("network-applet")
        self.autoSwitch = autoswitch.autoSwitch(comlink, notifier=False)
        if self.showNotifications:
            self.notifier = pynotify.Notification("Network Manager")
            iconPath = KGlobal.iconLoader().iconPath("network", KIcon.Desktop, True)
            pos = self.trays[0].getPos()
            self.notifier.set_hint("x",pos['x'])
            self.notifier.set_hint("y",pos['y'])
            self.autoSwitch.setNotifier(self.notifier, iconPath)
        if self.autoConnect and not dry:
            self.autoSwitch.scanAndConnect(force=False)

    def fixQuit(self):
        self.config.sync()
        for item in self.trays:
            item.deleteLater()
    
    def start(self):
        for script in comlink.links:
            comlink.queryConnections(script)
        self.resetViews()
        if self.autoConnect:
            self.delayTimer.start(1000, True)

    def resetViews(self):
        if self.mode == 0:
            self.mode = -1
            self.noGroup(0)
        else:
            self.mode = -1
            self.deviceGroup(0)
    
    def setMenu(self, menu):
        KAction(i18n("Firewall..."), "firewall_config", KShortcut.null(), self.startFirewall, menu).plug(menu)
        KAction(i18n("Edit Connections..."), "configure", KShortcut.null(), self.startManager, menu).plug(menu)
        KAction(i18n("Connect Automatically"), "connect_creating", KShortcut.null(), self.scanAndConnect, menu).plug(menu)
        menu.insertSeparator(1)
        show_notify = menu.insertItem(i18n("Show Notifications"), self.setNotify, 0, -1, 1)
        menu.insertSeparator(1)
        device_mid = menu.insertItem(i18n("Icon Per Device"), self.deviceGroup, 0, -1, 1)
        single_mid = menu.insertItem(i18n("Single Icon"), self.noGroup, 0, -1, 1)
       
        if self.mode == 0:
            menu.setItemChecked(single_mid, True)
        else:
            menu.setItemChecked(device_mid, True)

        if self.showNotifications:
            menu.setItemChecked(show_notify, True)

    def scanAndConnect(self):
        if not self.notifier and self.showNotifications:
            self.createNotifier(dry=True)
        if self.showNotifications:
            pos = self.trays[0].getPos()
            self.notifier.set_hint("x",pos['x'])
            self.notifier.set_hint("y",pos['y'])
        self.autoSwitch.scanAndConnect()

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
        if not self.notifier and self.showNotifications:
            self.createNotifier(dry=True)
        for item in self.trays:
            item.updateIcon(self.notifier)
    
    def setNotify(self, id):
        if self.showNotifications:
            self.config.writeEntry("ShowNotifications", False)
            self.autoSwitch.setNotifier(False)
            self.notifier.close()
        else:
            self.config.writeEntry("ShowNotifications", True)
        self.showNotifications = self.config.readBoolEntry("ShowNotifications",True)
        self.resetViews()

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
        if not len(comlink.connections):
            return
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
        if autostart == KMessageBox.Yes:
            self.config.writeEntry("AutoStart", True)
        elif autostart == KMessageBox.No:
            self.config.writeEntry("AutoStart", False)
        self.config.sync()
        self.app.quit()


class ConnectionItem(QCustomMenuItem):
    def __init__(self, conn):
        QCustomMenuItem.__init__(self)
        self.conn = conn
        self.mypix = icons.get_state(conn.script, conn.state)
        self.text_start = self.mypix.width() + 6
    
    def addressText(self):
        text = ""
        if self.conn.state == "up":
            text = self.conn.net_addr
            if not text:
                text = unicode(self.conn.message)
        else:
            if self.conn.message:
                text = unicode(self.conn.message)
        return text
    
    def paint(self, paint, cg, act, enabled, x, y, w, h):
        paint.setFont(self.my_font)
        fm = paint.fontMetrics()
        paint.drawPixmap(x + 3, y + (h - self.mypix.height()) / 2, self.mypix)
        paint.drawText(x + self.text_start, y + fm.ascent(), self.conn.menu_name)
        paint.drawText(x + self.text_start, y + fm.height() + fm.ascent(), self.addressText())
    
    def sizeHint(self):
        fm = QFontMetrics(self.my_font)
        rect = fm.boundingRect(self.conn.menu_name)
        tw, th = rect.width(), fm.height()
        if self.addressText():
            rect2 = fm.boundingRect(self.addressText())
            tw = max(tw, rect2.width())
        tw += self.text_start
        th += 3 + fm.height()
        th = max(th, self.mypix.height() + 6)
        return QSize(tw, th)
    
    def setFont(self, font):
        self.my_font = QFont(font)


class NetTray(KSystemTray):
    NoNetworks = 1
    Unreachable = 2
    OfflineDisconnected = 3
    OfflineFailed = 4
    ShuttingDown = 5
    Offline = 6
    Establishing = 7
    Online = 8

    def __init__(self, parent, dev=None):
        KSystemTray.__init__(self)
        self.dcop = parent.app.dcopClient()
        self.warnNotifier = None
        self.setPixmap(self.loadIcon("network"))
        menu = self.contextMenu()
        parent.setMenu(menu)
        self.applet = parent
        self.popup = None
        self.dev = dev
        if dev:
            QToolTip.add(self, dev.devname)
        self.notifier = parent.notifier
        self.lastMessage = None
        self.updateIcon()

    def getPos(self):
        pt = self.mapToGlobal(QPoint(0,0))
        screen = QDesktopWidget()
        incr = 0
        if pt.y() < screen.screenGeometry().height()/2 and pt.y()<self.height():
            incr = self.width() - 4
        elif pt.y() > screen.screenGeometry().height() - self.height() - 80:
            incr = 0
        else:
            incr = self.width() / 2
        return {'x':pt.x() + self.height()/2, 'y':pt.y() + incr}

    def updateNetworkStatus(self, status):
        kded = dcopext.DCOPApp("kded", self.dcop)
        kded.networkstatus.setNetworkStatus("COMARNetworkStatus", status)


    def updateIcon(self,notifier=None):
        if notifier:
            self.notifier = notifier
        if self.dev:
            for conn in self.dev.connections.values():
                script = conn.script
                if conn.state == "connecting":
                    self.setPixmap(icons.get_state(script, "connecting"))
                    self.updateNetworkStatus(self.Establishing)
                    return
                elif conn.state == "up":
                    self.setPixmap(icons.get_state(script, "up"))
                    self.updateNetworkStatus(self.Online)
                    return
        else:
            script = "net-tools"
            self.lastMessage = None
            for dev in comlink.devices.values():
                for conn in dev.connections.values():
                    if not conn.message == None:
                        self.lastMessage = conn.message
                    if conn.state == "connecting":
                        self.notify(str(i18n("Connecting to <b>%1</b> ...").arg(unicode(conn.name))),"connect_creating")
                        self.setPixmap(icons.get_state(script, "connecting"))
                        self.updateNetworkStatus(self.Establishing)
                        return
                    elif conn.state == "up":
                        self.notify(str(i18n("Connected to <b>%1</b>").arg(unicode(conn.name))),"connect_established")
                        self.setPixmap(icons.get_state(script, "up"))
                        self.updateNetworkStatus(self.Online)
                        return

        if self.lastMessage:
            self.notify(str(i18n("Connection failed \n<b>%1</b>").arg(unicode(self.lastMessage))),"connect_no",True)
        else:
            self.notify(str(i18n("You are offline now")),"connect_no")
        self.setPixmap(icons.get_state(script, "down"))
        self.updateNetworkStatus(self.Offline)

    def notify(self,message,icon='network',warning=False):
        if self.notifier and self.applet.showNotifications:
            icon = str(icons.getPath(icon))
            if warning:
                self.notifier.close()
                if not self.warnNotifier:
                    self.warnNotifier = pynotify.Notification(str(i18n("Network Manager")),message,icon)
                self.notifier = self.warnNotifier
                self.notifier.close()
                self.notifier.set_urgency(pynotify.URGENCY_CRITICAL)
            else:
                if self.warnNotifier:
                    self.warnNotifier.close()
                self.notifier = self.applet.notifier
                self.notifier.set_urgency(pynotify.URGENCY_NORMAL)
            pos = self.getPos()
            self.notifier.set_hint("x",pos['x'])
            self.notifier.set_hint("y",pos['y'])
            self.notifier.clear_actions()
            self.notifier.set_timeout(4500)
            self.notifier.update(str(i18n("Network Manager")),message,icon)
            self.notifier.show()

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
        elif event.button() == event.MidButton:
            self.applet.scanAndConnect()
        else:
            KSystemTray.mousePressEvent(self, event)
    
    def slotSelect(self, mid):
        menu = self.contextMenu()
        conn = comlink.getConnById(mid)
        if conn.state in ("up", "connecting", "inaccessible"):
            state = "down"
        else:
            state = "up"
        ch = comlink.callHandler(conn.script, "Net.Link", "setState", "tr.org.pardus.comar.net.link.setstate")
        ch.call(conn.name, state)
        self.popup = None

def main():
    KLocale.setMainCatalogue("network-manager")
    about = KAboutData(
        "network-applet",
        I18N_NOOP("Network Applet"),
        "0.5",
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
    
    DBusQtMainLoop(set_as_default=True)
    
    # PolicyKit Agent requires window ID
    global comlink
    comlink = DBusInterface()
    
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    icons.load_icons()
    applet = Applet(app)
    applet.start()
    app.exec_loop()

if __name__ == "__main__":
    main()
