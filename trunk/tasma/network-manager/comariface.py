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

CONNLIST, CONNINFO, CONNINFO_ADDR, CONNINFO_AUTH, CONNINFO_REMOTE = range(5)


class Connection:
    @staticmethod
    def hash(script, name):
        return unicode("%s %s" % (script, name))
    
    def __init__(self, script, data):
        self.script = script
        self.name, self.devid, self.devname = data.split("\n")
        self.active = False
        self.remote = None
        self.state = "down"
        self.net_mode = "auto"
        self.net_addr = None
        self.net_mask = None
        self.net_gate = None


class Link:
    def __init__(self, script, data):
        self.script = script
        self.type, self.name, self.remote_name = data.split("\n", 2)
        self.modes = []


class ComarInterface:
    def __init__(self):
        self.com = None
        self.links = {}
        self.connections = {}
    
    def connect(self):
        self.com = comar.Link()
        #self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)
        #self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
    
    def slotComar(self, sock):
        reply = self.com.read()
        if not reply:
            return
        if reply.command != "result":
            print reply
            return
        
        if reply.id == CONNLIST:
            if reply.data != "":
                for name in reply.data.split("\n"):
                    self.com.Net.Link[reply.script].connectionInfo(name=name, id=CONNINFO)
        
        if reply.id == CONNINFO:
            conn = Connection(reply.script, reply.data)
            self.connections[Connection.hash(conn.script, conn.name)] = conn
            script = self.com.Net.Link[conn.script]
            script.getAddress(name=conn.name, id=CONNINFO_ADDR)
            modes = self.links[conn.script].modes
            if "remote" in modes:
                script.getRemote(name=conn.name, id=CONNINFO_REMOTE)
            if "passauth" in modes or "keyauth" in modes or "loginauth" in modes:
                script.getAuthentication(name=conn.name, id=CONNINFO_AUTH)
        
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
        
        if reply.id == CONNINFO_REMOTE:
            name, remote = reply.data.split("\n")
            conn = self.getConn(reply.script, name)
            conn.remote = remote
    
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
        for link in self.links.values():
            print "Link:", link.script, link.name, ",".join(link.modes)
    
    def queryConnections(self):
        self.com.Net.Link.connections(id=CONNLIST)


comlink = ComarInterface()
comlink.connect()
comlink.queryLinks()
comlink.queryConnections()
import time
start = time.time()
while True:
    cur = time.time()
    if (cur - start) > 5.0:
        break
    comlink.slotComar(0)

for conn in comlink.connections.values():
    print conn.script, conn.name, conn.remote, conn.net_mode
