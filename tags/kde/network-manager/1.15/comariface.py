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
import comar
from qt import *
from kdecore import *
from kdeui import *

CONNLIST, CONNINFO, CONNINFO_AUTH, DEVICES, NAME_HOST, NAME_DNS, REMOTES = range(1, 8)


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
        self.denied_hook = []
        self.warn_limited_access = False
    
    def emitNoConn(self):
        map(lambda x: x(), self.noconn_hook)
    
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
        self.name = None
        self.devid = None
        self.devname = None
        self.remote = None
        self.state = "unavailable"
        self.message = None
        self.net_mode = "auto"
        self.net_addr = None
        self.net_mask = None
        self.net_gate = None
        self.auth_mode = "none"
        self.auth_user = None
        self.auth_pass = None
        self.dns_mode = "default"
        self.dns_server = None
        self.parse(data)
        self.hash = self.hash(self.script, self.name)
        self.got_auth = True
        self.first_time = True
    
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
            elif key == "net_mask":
                self.net_mask = value
            elif key == "net_gateway":
                self.net_gate = value
            elif key == "namemode":
                self.dns_mode = value
            elif key == "nameserver":
                self.dns_server = value
            elif key == "state":
                if " " in value:
                    self.state, self.message = value.split(" ", 1)
                else:
                    self.state = value


class AuthMode:
    def __init__(self, mode):
        self.id, self.type, self.name = mode.split(",", 2)


class Link:
    def __init__(self, script, data):
        self.script = script
        self.remote_name = None
        self.auth_modes = []
        for line in data.split("\n"):
            key, value = line.split("=", 1)
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


class ComarInterface(Hook):
    def __init__(self):
        Hook.__init__(self)
        self.com = None
        self.links = {}
        self.connections = {}
        self.name_host = None
        self.name_dns = None
    
    def waitComar(self):
        dia = KProgressDialog(None, "lala", i18n("Waiting COMAR..."),
            i18n("Connection to the COMAR unexpectedly closed, trying to reconnect..."), True)
        dia.progressBar().setTotalSteps(50)
        dia.progressBar().setTextEnabled(False)
        dia.show()
        start = time.time()
        while time.time() < start + 5:
            try:
                self.com = comar.Link()
                dia.close()
                self.setupComar(False)
                return
            except comar.CannotConnect:
                pass
            if dia.wasCancelled():
                break
            percent = (time.time() - start) * 10
            dia.progressBar().setProgress(percent)
            qApp.processEvents(100)
        dia.close()
        KMessageBox.sorry(None, i18n("Cannot connect to the COMAR! If it is not running you should start it with the 'service comar start' command in a root console."))
        KApplication.kApplication().quit()
    
    def setupComar(self, first_time=True):
        self.com.localize()
        if first_time:
            self.queryLinks()
        self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)
        self.notifier.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        self.askNotifications()
        if first_time:
            self.queryConnections()
    
    def connect(self):
        try:
            self.com = comar.Link()
        except comar.CannotConnect:
            KMessageBox.sorry(None, i18n("Cannot connect to the COMAR! If it is not running you should start it with the 'service comar start' command in a root console."))
            sys.exit(0)
        self.setupComar()
    
    def slotComar(self, sock):
        try:
            reply = self.com.read_cmd()
        except comar.LinkClosed:
            self.notifier = None
            self.waitComar()
            return
        
        if reply.command == "result":
            self.handleReply(reply)
        elif reply.command == "denied":
            self.handleDenied(reply)
        elif reply.command == "notify":
            self.handleNotify(reply)
        elif reply.command == "start":
            pass
        elif reply.command == "end":
            if reply.id == CONNLIST:
                if self.nr_queried == 0:
                    self.emitNoConn()
        else:
            # FIXME: handle errors
            print reply
    
    def handleReply(self, reply):
        if reply.id == CONNLIST:
            if reply.data != "":
                for name in reply.data.split("\n"):
                    self.com.Net.Link[reply.script].connectionInfo(name=name, id=CONNINFO)
                self.nr_queried += 1
        
        if reply.id == CONNINFO:
            modes = comlink.links[reply.script].modes
            conn = Connection(reply.script, reply.data)
            old_conn = self.getConn(reply.script, conn.name)
            if old_conn:
                old_conn.parse(reply.data)
                if "auth" in modes:
                    comlink.com.Net.Link[old_conn.script].getAuthentication(name=old_conn.name, id=CONNINFO_AUTH)
                    old_conn.got_auth = False
                else:
                    self.emitConfig(old_conn)
                return
            self.connections[conn.hash] = conn
            if "auth" in modes:
                comlink.com.Net.Link[conn.script].getAuthentication(name=conn.name, id=CONNINFO_AUTH)
                conn.got_auth = False
            else:
                conn.first_time = False
                self.emitNew(conn)
        
        if reply.id == CONNINFO_AUTH:
            name, type = reply.data.split("\n", 1)
            conn = self.getConn(reply.script, name)
            if not conn:
                return
            if "\n" in type:
                type, rest = type.split("\n", 1)
            conn.auth_mode = type
            if type != "none":
                link = self.links[reply.script]
                for mode in link.auth_modes:
                    if mode.id == type:
                        if mode.type == "pass":
                            conn.auth_pass = rest
                        elif mode.type == "login":
                            conn.auth_user, conn.auth_pass = rest.split("\n")
                        break
            if not conn.got_auth:
                conn.got_auth = True
                if conn.first_time:
                    conn.first_time = False
                    self.emitNew(conn)
                else:
                    self.emitConfig(conn)
        
        if reply.id == DEVICES:
            self.emitDevices(reply.script, reply.data)
        
        if reply.id == NAME_HOST:
            self.name_host = reply.data
            if self.name_host and self.name_dns:
                self.emitName(self.name_host, self.name_dns)
        
        if reply.id == NAME_DNS:
            self.name_dns = reply.data
            if self.name_host and self.name_dns:
                self.emitName(self.name_host, self.name_dns)
        
        if reply.id == REMOTES:
            self.emitRemotes(reply.script, reply.data)
    
    def handleDenied(self, reply):
        self.emitDenied()
        if not self.warn_limited_access:
            self.warn_limited_access = True
            KMessageBox.sorry(None, i18n("You are not allowed to change network settings."))
    
    def handleNotify(self, reply):
        if reply.notify == "Net.Link.connectionChanged":
            what, name = reply.data.split(" ", 1)
            if what == "added":
                self.com.Net.Link[reply.script].connectionInfo(name=name, id=CONNINFO)
            elif what == "deleted":
                conn = self.getConn(reply.script, name)
                if conn:
                    self.emitDelete(conn)
                    del self.connections[conn.hash]
            elif what == "configured":
                conn = self.getConn(reply.script, name)
                if conn:
                    comlink.com.Net.Link[reply.script].connectionInfo(name=name, id=CONNINFO)
        
        elif reply.notify == "Net.Link.stateChanged":
            name, state = reply.data.split("\n", 1)
            conn = self.getConn(reply.script, name)
            if conn:
                msg = None
                if " " in state:
                    state, msg = state.split(" ", 1)
                conn.message = msg
                conn.state = state
                self.emitState(conn)
        
        elif reply.notify == "Net.Link.deviceChanged":
            type, rest = reply.data.split(" ", 1)
            if type == "new":
                type, uid, info = rest.split(" ", 2)
                self.emitHotplug(uid, info)
    
    def getConn(self, script, name):
        hash = Connection.hash(script, name)
        return self.connections.get(hash, None)
    
    def checkAccess(self, method, id=0):
        self.com.can_access("Net.Link.%s" % method, id=id)
    
    def askNotifications(self):
        self.com.ask_notify("Net.Link.deviceChanged")
        self.com.ask_notify("Net.Link.connectionChanged")
        self.com.ask_notify("Net.Link.stateChanged")
    
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
    
    def queryNames(self):
        self.com.Net.Stack.getHostNames(id=NAME_HOST)
        self.com.Net.Stack.getNameServers(id=NAME_DNS)
    
    def queryConnections(self):
        self.com.Net.Link.connections(id=CONNLIST)
        self.nr_queried = 0
    
    def queryDevices(self, script):
        self.com.Net.Link[script].deviceList(id=DEVICES)
    
    def queryRemotes(self, script, devid):
        self.com.Net.Link[script].scanRemote(device=devid, id=REMOTES)
    
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


comlink = ComarInterface()
