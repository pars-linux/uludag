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

import sys
import time
from qt import *
from kdecore import *
from kdeui import *

import dbus
from handler import CallHandler

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
        self.auth_user = None
        self.auth_pass = None
        self.auth_anon = None
        self.auth_auth = None
        self.auth_inner = None
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
        self.dns_mode = data.get("namemode", "default")
        self.dns_server = data.get("nameserver")
        self.apmac = data.get("apmac")
        self.channel = data.get("channel")
        self.device_mode = data.get("device_mode", "Managed")
        state = data.get("state", "unavailable")
        if " " in state:
            self.state, self.message = state.split(" ", 1)
        else:
            self.state = state
            self.message = None


class AuthMode:
    def __init__(self, mode):
        self.id, self.type, self.name = mode.split(",", 2)


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
            elif key == "auth_modes":
                for mode in value.split(";"):
                    self.auth_modes.append(AuthMode(mode))
            elif key == "remote_name":
                self.remote_name = value
            elif key == "device_modes":
                self.device_modes = value.split(",")


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
            return
        try:
            func = getattr(iface, method)
            return func(*args)
        except dbus.DBusException, exception:
            self.error(exception)

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
        if signal == "connectionChanged":
            what, profile = args
            if what == "added":
                ch = self.callHandler(script, "Net.Link", "connectionInfo", "tr.org.pardus.comar.net.link.get")
                ch.registerDone(self.handleConnectionInfo, script)
                ch.call(profile)
            elif what == "deleted":
                conn = self.getConn(script, profile)
                if conn:
                    self.emitDelete(conn)
                    del self.connections[conn.hash]
            elif what == "configured":
                conn = self.getConn(script, profile)
                if conn:
                    ch = self.callHandler(script, "Net.Link", "connectionInfo", "tr.org.pardus.comar.net.link.get")
                    ch.registerDone(self.handleConnectionInfo, script)
                    ch.call(profile)

        elif signal == "stateChanged":
            profile, state, msg = args
            conn = self.getConn(script, profile)
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

    def listenSignals(self):
        self.busSys.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.Net.Link", member_keyword="signal", path_keyword="path")

    def queryLinks(self):
        scripts = self.callSys("listModelApplications", "Net.Link")
        if scripts:
            for script in scripts:
                info = self.call(script, "Net.Link", "linkInfo")
                if info:
                    self.links[script] = Link(script, info)

    def queryNames(self): 
        def handlerHost(host):
            self.name_host = host
            if self.name_dns:
                self.emitName(self.name_host, self.name_dns)
        def handlerDNS(dns):
            self.name_dns = dns
            if self.name_host:
                self.emitName(self.name_host, self.name_dns)

        ch = self.callHandler("baselayout", "Net.Stack", "getHostName", "tr.org.pardus.comar.net.stack.get")
        ch.registerDone(handlerHost)
        ch.call()

        ch2 = self.callHandler("baselayout", "Net.Stack", "getNameServers", "tr.org.pardus.comar.net.stack.get")
        ch2.registerDone(handlerDNS)
        ch2.call()

    def handleConnectionInfo(self, script, info):
        def handler(conn, mode, username, password, channel, auth, anon, inner, clicert, cacert, prikey, prikeypass):
            conn.got_auth = True
            conn.auth_mode = mode
            conn.auth_user = username
            conn.auth_pass = password
            conn.channel = channel
            conn.auth_anon = anon
            conn.auth_auth = auth
            conn.auth_inner = inner
            conn.auth_ca_cert = cacert
            conn.auth_client_cert = clicert
            conn.auth_private_key = prikey
            conn.auth_private_key_pass = prikeypass

            if conn.first_time:
                conn.first_time = False
                self.emitNew(conn)
            else:
                self.emitConfig(conn)

        modes = self.links[script].modes
        conn = Connection(script, info)
        old_conn = self.getConn(script, conn.name)
        if old_conn:
            old_conn.parse(info)
            if "auth" in modes:
                ch = self.callHandler(script, "Net.Link", "getAuthentication", "tr.org.pardus.comar.net.link.get")
                ch.registerDone(handler, old_conn)
                ch.call(old_conn.name)
            else:
                self.emitConfig(old_conn)
            return
        self.connections[conn.hash] = conn
        if "auth" in modes:
            ch = self.callHandler(script, "Net.Link", "getAuthentication", "tr.org.pardus.comar.net.link.get")
            ch.registerDone(handler, conn)
            ch.call(conn.name)
        else:
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
                if script == 'wireless_tools':
                    self.emitNoWifi()
                # if no connections present, start listening for signals now
                if len(self.links) == self.nr_empty:
                    if self.first_time:
                        self.first_time = False
                        self.emitNoConn()
                        # get signals
                        self.listenSignals()
        ch = self.callHandler(script, "Net.Link", "connections", "tr.org.pardus.comar.net.link.get")
        ch.registerDone(handler)
        ch.call()

    def queryDevices(self, script):
        def handler(info):
            self.emitDevices(script, info)
        ch = self.callHandler(script, "Net.Link", "deviceList", "tr.org.pardus.comar.net.link.get")
        ch.registerDone(handler)
        ch.call()

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
