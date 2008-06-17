#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

name_msg = {
    "en": "VPN Connection",
    "tr": "VPN Bağlantısı"
}

"""dhcp_fail_msg = {
    "en": "Could not get address",
    "tr": "Adres alınamadı"
}

no_device_msg = {
    "en": "Device is not plugged",
    "tr": "Aygıt takılı değil"
}"""

import os
import subprocess

from pardus import netutils
from pardus import iniutils

# Open connection db
DB = iniutils.iniDB(os.path.join("/etc/network/openvpn.db"))
CFG_FL = "/etc/network/openvpnclient.conf"

# Internal functions

def _get(dict, key, default):
    val = default
    if dict and dict.has_key(key):
        val = dict[key]
    return val

def stopSameDev(myname):
    conns = DB.listDB()
    for name in conns:
        if myname == name:
            continue
        dev = Dev(name)
        
        notify("Net.Link", "stateChanged", (name, "down", ""))
        if dev.state == "up":
            d = DB.getDB(name)
            d["state"] = "down"
            DB.setDB(name, d)


class Dev:
    def __init__(self, name, want=False):
        dict = DB.getDB(name)
        if want:
            if not dict:
                fail("No such connection")
        self.dev = _get(dict, "dev", "tun")
        self.name = name
        self.state = _get(dict, "state", "down")
        self.protocol = _get(dict, "protocol", "UDP")
        self.domain = _get(dict, "domain", None)
        self.port = _get(dict, "port", "1194")
        self.ca = _get(dict, "ca", None)
        self.cert = _get(dict, "cert", None)
        self.key = _get(dict, "key", None)
        self.chipher = _get(dict, "chipher", None)
    
    def up(self):
        vpnfl = open(CFG_FL, "w")
        vpnfl.write("client\n")
        vpnfl.write("dev %s\n" % self.dev)
        vpnfl.write("proto %s\n" % self.protocol)
        vpnfl.write("remote %s %s\n" % (self.domain, self.port))
        vpnfl.write("resolv-retry infinite\nnobind\npersist-key\npersist-tun\ncomp-lzo\nmute 20\nverb 3\n")
        vpnfl.write("ca %s\n" % self.ca)
        vpnfl.write("cert %s\n" % self.cert)
        vpnfl.write("key %s\n" % self.key)
        if self.chipher != None:
            vpnfl.write("chipher %s\n" % self.chipher)
        vpnfl.close()
        d = DB.getDB(self.name)
        d["state"] = "up"
        DB.setDB(self.name, d)
        notify("Net.Link", "stateChanged", (self.name, "connecting", self.domain))
        subprocess.call(["/usr/sbin/openvpn","--config","%s" %CFG_FL])
        notify("Net.Link", "stateChanged", (self.name, "up", self.domain))
        #else:
	    #pass
            #raise error
    
    def down(self):
        if subprocess.call(["usr/bin/killall", "openvpn"]):
            d = DB.getDB(self.name)
            d["state"] = "down"
            DB.setDB(self.name, d)
            notify("Net.Link", "stateChanged", (self.name, "down", ""))
        else:
	    pass
            #raise error


# Net.Link API

def linkInfo():
    d = {
        "type": "vpn",
        "modes": "device,vpn",
        "name": _(name_msg),
    }
    return d

def deviceList():
    vpnlist = {
        "device":"VPN Device",
    }
    return vpnlist

def setVpn(name, domain, port, protocol, ca, cert, key, chipher):
    d = DB.getDB(name)
    if domain != "":
        d["domain"] = domain
    if port != "":
        d["port"] = port
    if protocol != "":
        d["protocol"] = protocol
    if ca != "":
        d["ca"] = ca
    if cert != "":
        d["cert"] = cert
    if key != "":
        d["key"] = key
    if chipher != "":
        d["chipher"] = chipher
    DB.setDB(name, d)
    notify("Net.Link", "connectionChanged", ("configured", name))

def scanRemote():
    fail("Not supported")

def setConnection(name, device):
    d = DB.getDB(name)
    changed = "device" in d
    d["device"] = device
    DB.setDB(name, d)
    if changed:
        notify("Net.Link", "connectionChanged", ("configured", name))
    else:
        notify("Net.Link", "connectionChanged", ("added", name))

def deleteConnection(name):
    dev = Dev(name)
    if dev.state == "up":
        dev.down()
    DB.remDB(name)
    notify("Net.Link", "connectionChanged", ("deleted", name))

def setRemote(name, remote):
    fail("Not supported")

def getState(name):
    d = DB.getDB(name)
    return d.get("state", "down")

def setState(name, state):
    dev = Dev(name)
    if state != "up" and state != "down":
        fail("unknown state")
    
    if state == "up":
        stopSameDev(name)
        dev.up()
    else:
        dev.down()
    

def connections():
    return DB.listDB()

def connectionInfo(name=None):
    dev = Dev(name, True)
    d = {}
    d["name"] = name    
    d["dev"] = dev.dev
    d["state"] = dev.state
    d["protocol"] = dev.protocol
    d["domain"] = dev.domain
    d["port"] = dev.port
    d["ca"] = dev.ca
    d["cert"] = dev.cert
    d["key"] = dev.key
    return d

def getAuthentication(name):
    return ("", "", "")

"""def kernelEvent(data):
    type, dir = data.split("@", 1)
    if not dir.startswith("/class/net/"):
        return
    devname = dir[11:]
    flag = 1
    
    if type == "add":
        ifc = netutils.IF(devname)
        if ifc.isWireless():
            return
        devuid = ifc.deviceUID()
        notify("Net.Link", "deviceChanged", ("add", "net", devuid, netutils.deviceName(devuid)))
        conns = DB.listDB()
        for conn in conns:
            dev = Dev(conn)
            if dev.ifc and dev.ifc.name == devname:
                if dev.state == "up":
                    dev.up()
                    return
                flag = 0
        if flag:
            notify("Net.Link", "deviceChanged", ("new", "net", devuid, netutils.deviceName(devuid)))
    
    elif type == "remove":
        conns = DB.listDB()
        for conn in conns:
            dev = Dev(conn)
            # FIXME: dev.ifc is not enough :(
            if dev.ifc and dev.ifc.name == devname:
                if dev.state == "up":
                    notify("Net.Link", "stateChanged", (dev.name, "inaccessible", "Device removed"))
        notify("Net.Link", "deviceChanged", ("removed", "net", devname, ""))
"""
