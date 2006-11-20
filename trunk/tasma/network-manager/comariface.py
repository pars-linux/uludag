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

import comar
from qt import *

CONNLIST, CONNINFO, CONNINFO_ADDR, CONNINFO_AUTH, CONNINFO_REMOTE = range(1, 6)


class Hook:
    def __init__(self):
        self.new_hook = []
        self.delete_hook = []
        self.state_hook = []
        self.config_hook = []
    
    def emitNew(self, conn):
        map(lambda x: x(conn), self.new_hook)
    
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


class Connection(Hook):
    @staticmethod
    def hash(script, name):
        return unicode("%s %s" % (script, name))
    
    def __init__(self, script, data):
        Hook.__init__(self)
        self.script = script
        self.name, self.devid, self.devname = data.split("\n")
        self.remote = None
        self.active = False
        self.state = "down"
        self.address = None
        self.net_mode = "auto"
        self.net_addr = None
        self.net_mask = None
        self.net_gate = None
        self.hash = self.hash(self.script, self.name)


class Link:
    def __init__(self, script, data):
        self.script = script
        self.type, self.name, self.remote_name = data.split("\n", 2)
        self.modes = []


class ComarInterface(Hook):
    def __init__(self):
        Hook.__init__(self)
        self.com = None
        self.links = {}
        self.connections = {}
    
    def connect(self):
        self.com = comar.Link()
        self.queryLinks()
        self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)
        self.notifier.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        self.queryConnections()
    
    def slotComar(self, sock):
        reply = self.com.read_cmd()
        if reply.command == "result":
            self.handleReply(reply)
        elif reply.command == "notify":
            self.handleNotify(reply)
        else:
            # FIXME: handle errors
            print reply
    
    def handleReply(self, reply):
        if reply.id == CONNLIST:
            if reply.data != "":
                for name in reply.data.split("\n"):
                    self.com.Net.Link[reply.script].connectionInfo(name=name, id=CONNINFO)
        
        if reply.id == CONNINFO:
            conn = Connection(reply.script, reply.data)
            self.connections[conn.hash] = conn
            script = self.com.Net.Link[conn.script]
            script.getAddress(name=conn.name, id=CONNINFO_ADDR)
            modes = self.links[conn.script].modes
            i = 1
            if "remote" in modes:
                script.getRemote(name=conn.name, id=CONNINFO_REMOTE)
                i += 1
            if "passauth" in modes or "keyauth" in modes or "loginauth" in modes:
                script.getAuthentication(name=conn.name, id=CONNINFO_AUTH)
                #i += 1
            conn.i = i
        
        if reply.id == CONNINFO_ADDR:
            name, mode, addr, gate = reply.data.split("\n", 3)
            mask = ""
            if "\n" in gate:
                gate, mask = gate.split("\n")
            conn = self.getConn(reply.script, name)
            conn.net_mode = mode
            conn.net_addr = addr
            conn.net_mask = mask
            conn.net_gate = gate
            conn.i -= 1
            if conn.i == 0:
                self.emitNew(conn)
        
        if reply.id == CONNINFO_REMOTE:
            name, remote = reply.data.split("\n")
            conn = self.getConn(reply.script, name)
            conn.remote = remote
            conn.i -= 1
            if conn.i == 0:
                self.emitNew(conn)
    
    def handleNotify(self, reply):
        if reply.notify == "Net.Link.connectionChanged":
            what, name = reply.data.split(" ", 1)
            if what == "added":
                self.com.Net.Link[reply.script].connectionInfo(name=name, id=CONNINFO)
            elif what == "deleted":
                conn = self.getConn(reply.script, name)
                if conn:
                    self.emitDelete(conn)
            elif what == "gotaddress":
                name, addr = name.split("\n", 1)
                conn = self.getConn(reply.script, name)
                if conn:
                    conn.address = addr
                    self.emitConfig(conn)
            elif what == "configured":
                type, name = name.split(" ", 1)
                # FIXME: query them: device, adress, state
        
        elif reply.notify == "Net.Link.stateChanged":
            name, state = reply.data.split("\n", 1)
            conn = self.getConn(reply.script, name)
            if conn:
                if state == "on":
                    conn.active = True
                elif state == "off":
                    conn.active = False
                elif state in ("up", "connecting", "down"):
                    conn.state = state
                self.emitState(conn)
    
    def getConn(self, script, name):
        hash = Connection.hash(script, name)
        return self.connections.get(hash, None)
    
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
                self.links[reply.script] = Link(reply.script, reply.data)
        for link in self.links.values():
            self.com.Net.Link[link.script].modes()
            reply = self.com.read_cmd()
            link.modes = reply.data.split(",")
    
    def queryConnections(self):
        self.com.ask_notify("Net.Link.deviceChanged")
        self.com.ask_notify("Net.Link.connectionChanged")
        self.com.ask_notify("Net.Link.stateChanged")
        self.com.Net.Link.connections(id=CONNLIST)


comlink = ComarInterface()
