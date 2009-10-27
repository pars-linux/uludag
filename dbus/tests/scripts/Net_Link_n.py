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
    "en": "Ethernet network",
    "tr": "Ethernet ağları"
}

dhcp_fail_msg = {
    "en": "Could not get address",
    "tr": "Adres alınamadı"
}

no_device_msg = {
    "en": "Device is not plugged",
    "tr": "Aygıt takılı değil"
}

import os

from pardus import netutils
from pardus import iniutils

# Open connection db
DB = iniutils.iniDB(os.path.join("/etc/network", script()))

# Internal functions

def _get(dict, key, default):
    val = default
    if dict and dict.has_key(key):
        val = dict[key]
    return val

def stopSameDev(myname, myuid):
    conns = DB.listDB()
    for name in conns:
        if myname == name:
            continue
        dev = Dev(name)
        if myuid != dev.uid:
            continue
        
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
        self.uid = _get(dict, "device", None)
        self.name = name
        self.ifc = None
        if self.uid:
            self.ifc = netutils.findInterface(self.uid)
        self.state = _get(dict, "state", "down")
        self.mode = _get(dict, "mode", "auto")
        self.address = _get(dict, "address", None)
        self.mask = _get(dict, "mask", None)
        self.gateway = _get(dict, "gateway", None)
        self.namemode = _get(dict, "namemode", "default")
        self.nameserver = _get(dict, "nameserver", None)
        self.mtu = _get(dict, "mtu", 1500)
        try:
            self.mtu = int(self.mtu)
        except:
            self.mtu = 1500
    
    def dns(self):
        if self.namemode == "default":
            srvs = []
        elif self.namemode == "auto":
            srvs = self.ifc.autoNameServers()
            if not srvs:
                srvs = []
        else:
            srvs = [ self.nameserver ]
        # Use nameservers
        call("baselayout", "Net.Stack", "useNameServers", (srvs, self.ifc.autoNameSearch()))
    
    def up(self):
        ifc = self.ifc
        if self.mode == "manual":
            ifc.setAddress(self.address, self.mask)
            ifc.up()
            if self.gateway:
                route = netutils.Route()
                route.setDefault(self.gateway)
                self.dns()
            d = DB.getDB(self.name)
            d["state"] = "up"
            DB.setDB(self.name, d)
            notify("Net.Link", "stateChanged", (self.name, "up", self.address))
        else:
            notify("Net.Link", "stateChanged", (self.name, "connecting", ""))
            ret = ifc.startAuto()
            if ret == 0 and ifc.isUp():
                self.dns()
                addr = ifc.getAddress()[0]
                d = DB.getDB(self.name)
                d["state"] = "up"
                DB.setDB(self.name, d)
                notify("Net.Link", "stateChanged", (self.name, "up", unicode(addr)))
            else:
                notify("Net.Link", "stateChanged", (self.name, "inaccessible", _(dhcp_fail_msg)))
                fail("DHCP failed")
        ifc.setMTU(self.mtu)
    
    def down(self):
        ifc = self.ifc
        if self.mode != "manual":
            ifc.stopAuto()
        ifc.down()
        d = DB.getDB(self.name)
        d["state"] = "down"
        DB.setDB(self.name, d)
        notify("Net.Link", "stateChanged", (self.name, "down", ""))


# Net.Link API

def linkInfo():
    d = {
        "type": "net",
        "modes": "device,net,auto",
        "name": _(name_msg),
    }
    return d

def deviceList():
    iflist = {}
    for ifc in netutils.interfaces():
        if ifc.isEthernet() and not ifc.isWireless():
            uid = ifc.deviceUID()
            info = netutils.deviceName(uid)
            iflist[uid] = info
    return iflist

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
    if dev.ifc and dev.state == "up":
        dev.down()
    DB.remDB(name)
    notify("Net.Link", "connectionChanged", ("deleted", name))

def setAddress(name, mode, address, mask, gateway):
    dev = Dev(name)
    if dev.state == "up":
        dev.address = address
        dev.gateway = gateway
        dev.up()
    d = DB.getDB(name)
    d["mode"] = mode
    d["address"] = address
    d["mask"] = mask
    d["gateway"] = gateway
    DB.setDB(name, d)
    notify("Net.Link", "connectionChanged", ("configured", name))

def setRemote(name, remote):
    fail("Not supported")

def setMTU(name, mtu):
    pass

def setNameService(name, namemode, nameserver):
    if not namemode in ("default", "auto", "custom"):
        fail("invalid namemode")
    d = DB.getDB(name)
    d["namemode"] = namemode
    d["nameserver"] = nameserver
    DB.setDB(name, d)
    notify("Net.Link", "connectionChanged", ("configured", name))

def getState(name):
    d = DB.getDB(name)
    return d.get("state", "down")

def setState(name, state):
    dev = Dev(name)
    if state != "up" and state != "down":
        fail("unknown state")
    
    if not dev.ifc:
        return
    
    if state == "up":
        stopSameDev(name, dev.uid)
        dev.up()
    else:
        dev.down()

def connections():
    return DB.listDB()

def connectionInfo(name=None):
    dev = Dev(name, True)
    d = {}
    d["name"] = name
    if dev.uid:
        d["device_id"] = dev.uid
        d["device_name"] = netutils.deviceName(dev.uid)
    d["net_mode"] = dev.mode
    if dev.address:
        d["net_address"] = dev.address
    if dev.mask:
        d["net_mask"] = dev.mask
    if dev.gateway:
        d["net_gateway"] = dev.gateway
    d["namemode"] = dev.namemode
    if dev.nameserver:
        d["nameserver"] = dev.nameserver
    if dev.state == "up":
        if dev.ifc:
            if dev.mode == "auto":
                if dev.ifc.isAuto() and dev.ifc.isUp():
                    state = "up " + dev.ifc.getAddress()[0]
                else:
                    state = "inaccessible " + _(dhcp_fail_msg)
            else:
                if dev.ifc.isUp():
                    state = "up " + dev.ifc.getAddress()[0]
                else:
                    state = "down"
        else:
            state = "inaccessible " + _(no_device_msg)
    else:
        if dev.ifc:
            state = "down"
        else:
            state = "unavailable"
    d["state"] = state
    return d

def getAuthentication(name):
    return ("", "", "")

def kernelEvent(data):
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
