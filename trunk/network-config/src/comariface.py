# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import comar

class comarLink:
    def __init__(self):
        self.link = comar.Link()
        self.link.localize()
    
    def getScriptInfo(self, script):
        self.link.Net.Link[script].linkInfo()
        reply = self.link.read_cmd()
        
        info = {}
        if reply.command != "result":
            return info
        
        for lines in reply.data.split("\n"):
            if not lines:
                continue
            key, value = lines.split("=", 1)
            info[key] = value
        
        return info
    
    def getScripts(self):
        self.link.get_packages("Net.Link")
        reply = self.link.read_cmd()
        
        if reply.command != "result":
            return []
        
        scripts = reply.data.split("\n")
        
        return scripts
    
    def getConnections(self):
        connections = []
        for script in self.getScripts():
            if not script:
                continue
            self.link.Net.Link[script].connections()
            reply = self.link.read_cmd()
            if reply.command != "result":
                return []
            for connection in reply.data.split("\n"):
                if not connection:
                    continue
                connections.append("%s %s" % (script, connection))
        return connections
    
    def getConnectionInfo(self, script, name):
        self.link.Net.Link[script].connectionInfo(name=name)
        reply = self.link.read_cmd()
        
        if reply.command != "result":
            return {}
        
        info = {"script": reply.script}
        for device in reply.data.split("\n"):
            if not device:
                continue
            key, value = device.split("=", 1)
            info[key] = value
        
        return info
    
    def getAuthentication(self, script, name):
        self.link.Net.Link[script].getAuthentication(name=name)
        reply = self.link.read_cmd()
        
        if reply.command != "result":
            return []
        
        return reply.data.split("\n")
    
    def getDevices(self, script):
        self.link.Net.Link[script].deviceList()
        reply = self.link.read_cmd()
        
        devices = {}
        if reply.command != "result":
            return devices
        
        for device in reply.data.split("\n"):
            if not device:
                continue
            id, name = device.split(" ", 1)
            devices[id] = name
        
        return devices
    
    def getRemotes(self, script, device):
        self.link.Net.Link[script].scanRemote(device=device)
        reply = self.link.read_cmd()
        
        remotes = []
        if reply.command != "result":
            return remotes
        
        for remote in reply.data.split("\n"):
            if not remote:
                continue
            name, mac, quality = "", "", ""
            for info in remote.split():
                if info.startswith("remote="):
                    name = info.split("=", 1)[1]
                elif info.startswith("mac="):
                    mac = info.split("=", 1)[1]
                elif info.startswith("quality="):
                    quality = info.split("=", 1)[1]
            remotes.append("%s %s %s" % (name, quality, mac))
        
        return remotes
    
    def setState(self, name, state):
        self.link.Net.Link.setState(name=name,
                                    state=state)
        self.link.read_cmd()
    
    def setConnection(self, script, name, device, mode, address=None, mask=None, gateway=None, remote=None, auth_mode=None, auth_value=None):
        self.link.Net.Link[script].setConnection(name=name,
                                                 device=device)
        self.link.read_cmd()
        
        if mode:
            self.link.Net.Link[script].setAddress(name=name,
                                                  mode=mode,
                                                  address=address,
                                                  mask=mask,
                                                  gateway=gateway)
        else:
            self.link.Net.Link[script].setAddress(name=name)
        self.link.read_cmd()
        
        if remote:
            self.link.Net.Link[script].setRemote(name=name,
                                                 remote=remote)
        else:
            self.link.Net.Link[script].setRemote(name=name)
        self.link.read_cmd()
        
        if auth_mode:
            if "\n" in auth_value:
                username, password = auth_value.split("\n")
                self.link.Net.Link[script].setAuthentication(name=name,
                                                             authmode="login",
                                                             user=username,
                                                             password=password)
            else:
                self.link.Net.Link[script].setAuthentication(name=name,
                                                             authmode=auth_mode,
                                                             key=auth_value)
        else:
            self.link.Net.Link[script].setAuthentication(name=name)
        self.link.read_cmd()
