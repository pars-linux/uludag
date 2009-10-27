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
import commands

from pardus import netutils
from pardus import iniutils

# Open connection db
DB = iniutils.iniDB(os.path.join("/etc/network", script()))
CFG_FL = "/etc/openvpn/openvpnclient.conf"
PID_FL = "/etc/openvpn/openvpn.pid"

# Internal functions

def _get(dict, key, default):
    val = default
    if dict and dict.has_key(key):
        val = dict[key]
    return val

def _getPid(pidfile):
    """Read process ID from a .pid file."""
    try:
        pid = file(pidfile).read()
    except IOError, e:
        if e.errno != 2:
            raise
        return None
    # Some services put custom data after the first line
    pid = pid.split("\n")[0]
    # Non-pid data is also seen when stopped state in some services :/
    if len(pid) == 0 or len(filter(lambda x: not x in "0123456789", pid)) > 0:
        return None
    return int(pid)

def stopSameDev(myname):
    conns = DB.listDB()
    for name in conns:
        if myname == name:
            continue
        dev = Dev(name)
        notify("Net.Link", "stateChanged", (name, "down", ""))
        if dev.state == "up":
            retcode =  subprocess.call(["/usr/bin/kill", dev.pid])
            d = DB.getDB(dev.name)
            d["state"] = "down"
            DB.setDB(dev.name, d)

class Dev():
    def __init__(self, name, want=False):
        dict = DB.getDB(name)
        if want:
            if not dict:
                fail("No such connection")
        self.dev = _get(dict, "device", "tun")
        self.name = name
        self.state = _get(dict, "state", "down")
        self.protocol = _get(dict, "protocol", "UDP")
        self.domain = _get(dict, "domain", "not set")
        self.port = _get(dict, "port", "1194")
        self.ca = _get(dict, "ca", "ca.crt")
        self.cert = _get(dict, "cert", "client.crt")
        self.key = _get(dict, "key", "client.key")
        self.chipher = _get(dict, "chipher", "")
        self.pid = _get(dict,"pid","")
    
    def up(self):
        vpnfl = open(CFG_FL, "w")
        vpnfl.write("daemon\n")
        vpnfl.write("client\n")
        vpnfl.write("dev %s\n" % self.dev)
        vpnfl.write("proto %s\n" % self.protocol)
        vpnfl.write("remote %s %s\n" % (self.domain, self.port))
        vpnfl.write("tls-exit\nresolv-retry infinite\nnobind\npersist-key\npersist-tun\ncomp-lzo\nmute 20\nverb 3\n")
        vpnfl.write("ca %s\n" % self.ca)
        vpnfl.write("cert %s\n" % self.cert)
        vpnfl.write("key %s\n" % self.key)
        vpnfl.write("writepid %s\n" % (PID_FL))
        if self.chipher != "":
            vpnfl.write("cipher %s\n" % self.chipher)
        vpnfl.close()
        notify("Net.Link", "stateChanged", (self.name, "connecting", ""))
        ret = subprocess.Popen(["/usr/sbin/openvpn","--config",CFG_FL])
        if ret == 0:
            d = DB.getDB(self.name)
            pid =  _getPid(PID_FL)
            if pid != None:
                d["pid"] = str(pid)
            else:
                d["pid"] = ""
            d["state"] = "up"
            DB.setDB(self.name, d)
            notify("Net.Link", "stateChanged", (self.name, "up", self.domain))

        else:
             notify("Net.Link", "stateChanged", (self.name, "down", ""))
             fail("Unable to set vpn connection. Check your configuration")
    
    def down(self):
        try:            
            retcode =  subprocess.call(["/usr/bin/kill", self.pid])
            d = DB.getDB(self.name)
            d["state"] = "down"
            d["pid"] = ""
            DB.setDB(self.name, d)
            notify("Net.Link", "stateChanged", (self.name, "down", ""))
        except:
            notify("Net.Link", "stateChanged", (self.name, "down", ""))
            fail("Unable to shutdown vpn connection")

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
        "tun":"tun",
        "tap":"tap"
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
    d["device"] = dev.dev
    d["state"] = dev.state
    d["protocol"] = dev.protocol
    d["domain"] = dev.domain
    d["port"] = dev.port
    d["ca"] = dev.ca
    d["cert"] = dev.cert
    d["key"] = dev.key
    d["chipher"] = dev.chipher
    return d

def getAuthentication(name):
    return ("", "", "")

def kernelEvent(data):
    pass
