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

import functools
import sys
import time
from qt import *
from kdecore import *
from kdeui import *

import dbus
import comar

CONNLIST, CONNINFO, CONNINFO_AUTH, DEVICES, NAME_HOST, NAME_DNS, REMOTES, CONNEXISTS = range(1, 9)


class Hook:
    def __init__(self):
        self.new_hook = []
        self.delete_hook = []
        self.state_hook = []
        self.config_hook = []
        self.device_hook = []
        self.name_hook = []
        self.remote_hook = []
        self.hotplug_hook = []
        self.noconn_hook = []
        self.nowifi_hook = []
        self.denied_hook = []
        self.denied_hook = []
        self.warn_limited_access = False

    def emitNoConn(self):
        map(lambda x: x(), self.noconn_hook)

    def emitNoWifi(self):
        map(lambda x: x(), self.nowifi_hook)

    def emitNew(self, conn):
        map(lambda x: x(conn), self.new_hook)

    def emitDevices(self, script, devices):
        map(lambda x: x(script, devices), self.device_hook)

    def emitName(self, hostname, servers):
        map(lambda x: x(hostname, servers), self.name_hook)

    def emitRemotes(self, script, remotes):
        map(lambda x: x(script, remotes), self.remote_hook)

    def emitHotplug(self, uid, info):
        map(lambda x: x(uid, info), self.hotplug_hook)

    def _emit(self, conn, func, hook):
        if conn:
            getattr(conn, func)()
            map(lambda x: x(conn), hook)
        else:
            map(lambda x: x(self), hook)

    def emitDelete(self, conn=None):
        self._emit(conn, "emitDelete", self.delete_hook)

    def emitConfig(self, conn=None):
        self._emit(conn, "emitConfig", self.config_hook)

    def emitState(self, conn=None):
        self._emit(conn, "emitState", self.state_hook)

    def emitDenied(self):
        map(lambda x: x(), self.denied_hook)

class Connection(Hook):
    @staticmethod
    def hash(script, name):
        return unicode("%s %s" % (script, name))

    def __init__(self, script, data):
        Hook.__init__(self)
        self.script = script
        self.auth_mode = "none"
        self.auth_username = None
        self.auth_password = None
        self.auth_cert_cli = None
        self.auth_cert_ca = None
        self.auth_keyfile = None
        self.channel = None
        self.device_mode = "Managed"
        self.parse(data)
        self.hash = self.hash(self.script, self.name)
        self.got_auth = True
        self.first_time = True

    def parse(self, data):
        self.name = data.get("name")
        self.devid = data.get("device_id")
        self.devname = data.get("device_name")
        self.remote = data.get("remote")
        self.net_mode = data.get("net_mode", "auto")
        self.net_addr = data.get("net_address")
        self.net_mask = data.get("net_mask")
        self.net_gate = data.get("net_gateway")
        self.dns_mode = data.get("name_mode", "default")
        self.dns_server = data.get("name_server")
        self.device_mode = data.get("device_mode", "Managed")
        state = data.get("state", "unavailable")
        if " " in state:
            self.state, self.message = state.split(" ", 1)
        else:
            self.state = state
            self.message = None


class AuthMode:
    def __init__(self, _id, label, paramters):
        self.id = _id
        self.name = label
        self.paramters = paramters


class Link:
    def __init__(self, script, data):
        self.script = script
        self.remote_name = None
        self.auth_modes = []
        for key, value in data.iteritems():
            if key == "type":
                self.type = value
            elif key == "name":
                self.name = value
            elif key == "modes":
                self.modes = value.split(",")
            elif key == "remote_name":
                self.remote_name = value


class DBusInterface(Hook):
    def __init__(self):
        Hook.__init__(self)
        self.busSys = None
        self.busSes = None
        self.links = {}
        self.connections = {}
        self.name_host = None
        self.name_dns = None
        self.window = None

        self.dia = None

        self.first_time = True
        self.nr_queried = 0
        self.nr_conns = 0
        self.nr_empty = 0
        self.winID = 0

        self.link = comar.Link()
        self.link.setLocale()
        self.queryLinks()

    def error(self, exception):
        if "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
        elif "No such device" in exception.message:
            message = i18n("Network Manager was not able to communicate with your network device. If it's\n"
                           "a wireless interface, make sure that its radio switch is turned on. This is usually\n"
                           "done through a switch or Fn keys in modern notebooks.")

        elif "DHCP failed" in exception.message:
            message = i18n("The DHCP service was not able to assign an IP address to your network interface.\n"
                           "Make sure that the network you're trying to connect is able to assign IP addresses\n"
                           "through its DHCP service. Otherwise, you have to manually assign an IP address.")
        else:
            message = str(exception)

        msg = QMessageBox(i18n("Network Manager - Error"), message, QMessageBox.Warning, QMessageBox.Ok, QMessageBox.NoButton, QMessageBox.NoButton, self.window, "err", True)
        msg.setTextFormat(Qt.RichText)
        msg.show()
    """

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
    """

    def handleSignals(self, package, signal, args):
        if signal == "connectionChanged":
            what, profile = args
            if what == "added":
                self.link.Network.Link[package].connectionInfo(profile, async=self.handleConnectionInfo)
            elif what == "deleted":
                conn = self.getConn(package, profile)
                if conn:
                    self.emitDelete(conn)
                    del self.connections[conn.hash]
            elif what == "configured":
                conn = self.getConn(package, profile)
                if conn:
                    self.link.Network.Link[package].connectionInfo(profile, async=self.handleConnectionInfo)
        elif signal == "stateChanged":
            profile, state, msg = args
            conn = self.getConn(package, profile)
            if conn:
                conn.message = msg
                conn.state = state
                self.emitState(conn)

        elif signal == "deviceChanged":
            what, type, devid, devname = args
            if type == "new":
                self.emitHotplug(uid, info)

    def getConn(self, script, name):
        hash = Connection.hash(script, name)
        return self.connections.get(hash, None)

    def getAuth(self, script, name):
        method = self.link.Network.Link[script].getAuthMethod(name)
        return method, self.link.Network.Link[script].getAuthParameters(name)

    def queryLinks(self):
        scripts = list(self.link.Network.Link)
        if scripts:
            for script in scripts:
                info = self.link.Network.Link[script].linkInfo()
                if info:
                    self.links[script] = Link(script, info)
                for _met, _label in self.link.Network.Link[script].authMethods():
                    self.links[script].auth_modes.append(AuthMode(_met, _label, self.link.Network.Link[script].authParameters(_met)))

    def queryNames(self): 
        def handlerHost(package, exception, args):
            if exception:
                return
            self.name_host = args[0]
            if self.name_dns:
                self.emitName(self.name_host, self.name_dns)
        def handlerDNS(package, exception, args):
            if exception:
                return
            self.name_dns = args[0]
            if self.name_host:
                self.emitName(self.name_host, self.name_dns)

        self.link.Network.Stack["baselayout"].getHostName(async=handlerHost)
        self.link.Network.Stack["baselayout"].getNameServers(async=handlerDNS)

    def handleConnectionInfo(self, script, exception, args):
        if exception:
            return
        info = args[0]
        modes = self.links[script].modes
        conn = Connection(script, info)
        old_conn = self.getConn(script, conn.name)
        if old_conn:
            old_conn.parse(info)
            self.emitConfig(old_conn)
            return
        self.connections[conn.hash] = conn
        conn.first_time = False
        self.emitNew(conn)

        if self.first_time:
            # After all connections' information fetched...
            if self.nr_queried == len(self.links) and self.nr_conns == len(self.connections):
                self.first_time = False
                # check wireless profiles
                connections = [hash for hash, conn in self.connections.iteritems() if conn.script == "wireless_tools"]
                if not len(connections):
                    self.emitNoWifi()
                # get signals
                self.link.listenSignals("Network.Link", self.handleSignals)

    def queryConnections(self, script):
        def handler(package, exception, args):
            if exception:
                return
            self.nr_queried += 1
            profiles = args[0]
            for profile in profiles:
                self.nr_conns += 1
                self.link.Network.Link[script].connectionInfo(profile, async=self.handleConnectionInfo)
            if not len(profiles):
                self.nr_empty += 1
                if script == 'wireless_tools':
                    self.emitNoWifi()
                # if no connections present, start listening for signals now
                if len(self.links) == self.nr_empty:
                    if self.first_time:
                        self.first_time = False
                        self.emitNoConn()
                        # get signals
                        self.link.listenSignals("Network.Link", self.handleSignals)
        self.link.Network.Link[script].connections(async=handler)

    def queryDevices(self, script):
        def handler(package, exception, args):
            if exception:
                return
            info = args[0]
            self.emitDevices(package, info)
        self.link.Network.Link[script].deviceList(async=handler)

    def queryRemotes(self, script, devid):
        def handler(info):
            self.emitRemotes(script, info)
        ch = self.callHandler(script, "Net.Link", "scanRemote", "tr.org.pardus.comar.net.link.get")
        ch.registerDone(handler)
        ch.call(devid)

    def uniqueName(self):
        base_name = str(i18n("new connection"))
        id = 2
        name = base_name
        while True:
            found = False
            for item in self.connections.values():
                if item.name == name:
                    found = True
                    break
            if not found:
                return name
            name = base_name + " " + str(id)
            id += 1

comlink = DBusInterface()
