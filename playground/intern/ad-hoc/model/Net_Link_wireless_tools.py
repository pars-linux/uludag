#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

name_msg = {
    "en": "Wireless network",
    "tr": "Kablosuz ağlar"
}

dhcp_fail_msg = {
    "en": "Could not get address",
    "tr": "Adres alınamadı"
}

no_device_msg = {
    "en": "Device is not plugged",
    "tr": "Aygıt takılı değil"
}

wpa_psp_msg = {
    "en": "WPA PreShared Key",
    "tr": "WPA Ortak Parola"
}

wpa_fail_msg = {
    "en": "Authentication failed",
    "tr": "Kimlik doğrulama başarısız",
}

no_supplicant_msg = {
    "en": "WPA supplicant not found",
    "tr": "WPA supplicant bulunamadı",
}

import os
import re
import socket
import array
import struct
import fcntl
import subprocess

from pardus import netutils
from pardus import iniutils

# Open connection db
DB = iniutils.iniDB(os.path.join("/etc/network", script()))

# From </usr/include/wireless.h>
SIOCSIWMODE = 0x8B06    # set the operation mode
SIOCGIWMODE = 0x8B07    # get operation mode
SIOCGIWRATE = 0x8B21    # get default bit rate
SIOCSIWESSID = 0x8B1A   # set essid
SIOCGIWESSID = 0x8B1B   # get essid


class Point:
    def __init__(self, id=None):
        self.ssid = ""
        self.mode = ""
        self.mac = ""
        self.encryption = "none"
        self.qual = ""
        self.protocol = ""
        self.channel = ""
        if id:
            if " (" in id and id.endswith(")"):
                self.ssid, rest = id.split(" (", 1)
                self.mode, self.mac = rest.split(" ", 1)
                self.mac = self.mac[:-1]
            else:
                self.ssid = id
    
    def id(self):
        d = {
            "remote": self.ssid,
            "mode": self.mode,
            "mac": self.mac,
            "encryption": self.encryption,
            "quality": self.qual,
            "protocol": self.protocol,
            "channel": self.channel,
        }
        return d


class Wireless:
    modes = ['Auto', 'Ad-Hoc', 'Managed', 'Master', 'Repeat', 'Second', 'Monitor']
    
    def __init__(self, ifc):
        self.sock = None
        self.ifc = ifc
    
    def _call(self, func, arg = None):
        if arg is None:
            data = (self.ifc.name + '\0' * 32)[:32]
        else:
            data = (self.ifc.name + '\0' * 16)[:16] + arg
        try:
            result = self.ifc.ioctl(func, data)
        except IOError:
            return None
        return result
    
    def getSSID(self):
        buffer = array.array('c', '\0' * 16)
        addr, length = buffer.buffer_info()
        arg = struct.pack('Pi', addr, length)
        self._call(SIOCGIWESSID, arg)
        return buffer.tostring().strip('\x00')
    
    def setSSID(self, ssid):
        point = Point(ssid)
        buffer = array.array('c', point.ssid + '\x00')
        addr, length = buffer.buffer_info()
        arg = struct.pack("iHH", addr, length, 1)
        self._call(SIOCSIWESSID, arg)
        if self.getSSID() is point.ssid:
            return True
        else:
            return None
    
    def scanSSID(self):
        ifc = self.ifc
        if not ifc.isUp():
            # Some drivers cant do the scan while interface is down, doh :(
            ifc.setAddress("0.0.0.0")
            ifc.up()
        cmd = subprocess.Popen(["/usr/sbin/iwlist", ifc.name, "scan"], stdout=subprocess.PIPE)
        data = cmd.communicate()[0]
        points = []
        point = None
        for line in data.split("\n"):
            line = line.lstrip()
            if line.startswith("Cell "):
                if point != None:
                    points.append(point)
                point = Point()
            if "ESSID:" in line:
                i = line.find('"') + 1
                j = line.find('"', i)
                point.ssid = line[i:j]
            if "Protocol:" in line:
                point.protocol = line.split("Protocol:")[1]
            if "Encryption key:" in line:
                mode = line.split("Encryption key:")[1]
                if mode == "on":
                    point.encryption = "wepascii"
            if "IE:" in line:
                ie = line.split("IE:")[1].strip()
                if "WPA Version 1" in ie:
                    point.encryption = "wpa-psk"
                if "WPA2 Version 1" in ie:
                    point.encryption = "wpa-psk"
            if "Mode:" in line:
                point.mode = line.split("Mode:")[1]
            if "Channel:" in line:
                point.channel = line.split("Channel:")[1]
            if "Address:" in line:
                point.mac = line.split("Address:")[1].strip()
            if "Quality" in line:
                qual = line.split("Quality")[1][1:]
                qual = qual.split(" ")[0]
                if "/" in qual:
                    qual, max = qual.split("/")
                    # normalize to 0-100
                    if max != "100":
                        qual = (float(qual) * 100) / float(max)
                        qual = str(int(qual))
                point.qual = qual
        if point != None:
            points.append(point)
        return points
    
    def getMode(self):
        result = self._call(SIOCGIWMODE)
        mode = struct.unpack("i", result[16:20])[0]
        return self.modes[mode]
    
    def setMode(self, mode):
        arg = struct.pack("l", self.modes.index(mode))
        self._call(SIOCSIWMODE, arg)
        if self.getMode() is mode:
            return True
        else:
            return None
    
    def setEncryption(self, mode="none", username=None, password=None, ssid=None):
        have_supplicant = True
        try:
            import wpa_supplicant
        except ImportError:
            have_supplicant = False

        ifc = self.ifc

        # Disable all auth. mechanisms before try to authenticate another methods
        os.system("/usr/sbin/iwconfig %s enc off" % (ifc.name))
        if have_supplicant and wpa_supplicant.isWpaServiceUsable():
            #stop WPA authentication
            wpa_supplicant.disableAuthentication(ifc.name)

        if mode == "wep":
            os.system("/usr/sbin/iwconfig '%s' enc restricted '%s'" % (ifc.name, password))
        elif mode == "wepascii":
            os.system("/usr/sbin/iwconfig '%s' enc restricted 's:%s'" % (ifc.name, password))
        elif mode == "wpa-psk":
            if not have_supplicant:
                return _(no_supplicant_msg)
            if not wpa_supplicant.startWpaService():
                fail("Unable to start WPA service")
            ret = wpa_supplicant.setWpaAuthentication(ifc.name, ssid, password)
            if not ret:
                return _(wpa_fail_msg)
        elif mode == "peap-mschapv2":
            if not have_supplicant:
                return _(no_supplicant_msg)
            if not wpa_supplicant.startWpaService():
                fail("Unable to start WPA service")
            peap = wpa_supplicant.Wpa_EAP(ifc.name)
            peap.ssid = ssid
            peap.phase2 = "MSCHAPV2"
            ret = peap.authenticate(username, password)
            if not ret:
                return _(wpa_fail_msg)
        return ""
    
    def getBitrate(self, ifname):
        # Note for UI coder, KILO is not 2^10 in wireless tools world
        result = self._call(SIOCGIWRATE)
        size = struct.calcsize('ihbb')
        m, e, i, pad = struct.unpack('ihbb', result[16:16+size])
        if e == 0:
            bitrate =  m
        else:
            bitrate = float(m) * 10**e
        return bitrate
    def getLinkStatus(self, ifname):
        """ Get link status of an interface """
        link = self._readsys(ifname, "wireless/link")
        return int(link)
    def getNoiseStatus(self, ifname):
        """ Get noise level of an interface """
        noise = self._readsys(ifname, "wireless/noise")
        return int(noise) - 256
    def getSignalStatus(self, ifname):
        """ Get signal status of an interface """
        signal = self._readsys(ifname, "wireless/level")
        return int(signal) - 256


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
        self.remote = _get(dict, "remote", None)
        self.apmac = _get(dict, "apmac", None)
        self.mode = _get(dict, "mode", "auto")
        self.address = _get(dict, "address", None)
        self.mask = _get(dict, "mask", None)
        self.gateway = _get(dict, "gateway", None)
        self.authmode = _get(dict, "authmode", "none")
        self.user = _get(dict, "user", "")
        self.password = _get(dict, "password", "")
        self.namemode = _get(dict, "namemode", "default")
        self.nameserver = _get(dict, "nameserver", None)
        self.device_mode = _get(dict, "device_mode", "managed")
    
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
        if self.device_mode == "managed":
            ifc = self.ifc
            ifc.down()
            wifi = Wireless(ifc)
            wifi.setMode("Managed")
            notify("Net.Link", "stateChanged", (self.name, "connecting", ""))
            ifc.up()
            if self.remote:
                wifi.setSSID(self.remote)
            err = wifi.setEncryption(mode=self.authmode, username=self.user, password=self.password, ssid=self.remote)
            if err:
                notify("Net.Link", "stateChanged", (self.name, "inaccessible", err))
                fail("auth failed")
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
                ifc=self.ifc
                ifc.up()
                ret = ifc.startAuto()
                if ret == 0 and ifc.isUp():
                    self.dns()
                    addr = ifc.getAddress()[0]
                    d = DB.getDB(self.name)
                    d["state"] = "up"
                    DB.setDB(self.name, d)
                    notify("Net.Link", "stateChanged", (self.name, "up", addr))
                else:
                    notify("Net.Link", "stateChanged", (self.name, "inaccessible",  _(dhcp_fail_msg)))
                    fail("DHCP failed")
        elif self.device_mode == "ad-hoc":
            ifc = self.ifc
            wifi = Wireless(ifc)
            ifc.down()
            wifi.setMode("Ad-Hoc")
            notify("Net.Link", "stateChanged", (self.name, "connecting", ""))

            """
            err = wifi.setEncryption(mode=self.authmode, username=self.user, password=self.password, ssid=self.remote)

            if err:
                notify("Net.Link", "stateChanged", (self.name, "inaccessible", err))
                fail("auth failed")

            """
            if self.mode == "manual":
                ifc.setAddress(self.address, self.mask)
            else:
                subprocess.Popen(["/usr/sbin/avahi-autoipd", "-D", "--force-bind", ifc.name], stdout=subprocess.PIPE).wait()
                from time import sleep
                sleep(8) # FIXME: Give sometime to the auto-ip deamon for getting IP. Yeah time.sleep is evil and ugly but works for now. Will be fixed for non-Desperate housecoders :)

            subprocess.Popen(["/usr/sbin/iwconfig", ifc.name, "channel", "01"], stdout=subprocess.PIPE).wait() # FIXME: channel auto mode sometimes does not work. So, a 2 digit number (01,02,03 ... 10) must be given
            subprocess.Popen(["/usr/sbin/iwconfig", ifc.name, "key", self.password], stdout=subprocess.PIPE).wait()
            subprocess.Popen(["/usr/sbin/iwconfig", ifc.name, "essid", self.remote], stdout=subprocess.PIPE).wait()
            ifc.up()
            d=DB.getDB(self.name)
            d["state"]="up"
            DB.setDB(self.name,d)
            addr = ifc.getAddress()[0]
            notify("Net.Link", "stateChanged", (self.name, "up", addr))

    def down(self):
        ifc = self.ifc
        wifi = Wireless(ifc)
        if self.mode != "manual":
            ifc.stopAuto()
        if self.authmode != "" and self.authmode != "none":
            wifi.setEncryption("none", None, None, None)
        ifc.down()
        d = DB.getDB(self.name)
        d["state"] = "down"
        DB.setDB(self.name, d)
        notify("Net.Link", "stateChanged", (self.name, "down", ""))


# Net.Link API

def linkInfo():
    d = {
        "type": "wifi",
        "modes": "devicemode,device,remote,scan,net,auto,auth",
        "auth_modes": "wep,pass,WEP;wepascii,pass,WEP ASCII;wpa-psk,pass,%s;peap-mschapv2,login,PEAP/MSCHAPV2" % _(wpa_psp_msg),
        "name": _(name_msg),
        "remote_name": "ESS ID",
        "device_modes": "Ad-Hoc,Managed",
    }
    return d

def deviceList():
    iflist = {}
    for ifc in netutils.interfaces():
        if ifc.isWireless():
            uid = ifc.deviceUID()
            info = netutils.deviceName(uid)
            iflist[uid] = info
    return iflist

def scanRemote(device):
    if device:
        ifc = netutils.findInterface(device)
        if ifc:
            wifi = Wireless(ifc)
            points = map(lambda x: x.id(), wifi.scanSSID())
            return points
    return []

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
    dev = Dev(name, True)
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

def setRemote(name, remote, apmac):
    d = DB.getDB(name)
    d["remote"] = remote
    d["apmac"] = apmac
    DB.setDB(name, d)
    notify("Net.Link", "connectionChanged", ("configured", name))

def setConnectionMode(name, mode):
    d = DB.getDB(name)
    d["device_mode"] = mode
    DB.setDB(name, d)
    notify("Net.Link", "connectionChanged", ("configured", name))

def setNameService(name, namemode, nameserver):
    if not namemode in ("default", "auto", "custom"):
        fail("invalid namemode")
    d = DB.getDB(name)
    d["namemode"] = namemode
    d["nameserver"] = nameserver
    DB.setDB(name, d)
    notify("Net.Link", "connectionChanged", ("configured", name))

def setAuthentication(name, authmode, user, password):
    d = DB.getDB(name)
    d["authmode"] = authmode
    d["user"] = user
    d["password"] = password
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
        fail("Device not found")
    
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
    if dev.remote:
        d["remote"] = dev.remote
        if dev.apmac:
            d["apmac"] = dev.apmac
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
    if dev.device_mode:
        d["device_mode"] = dev.device_mode
    if dev.state == "up":
        if dev.ifc:
            if dev.mode == "auto":
                if dev.ifc.isAuto() and dev.ifc.isUp():
                    state = "up "
                    try:
                        state += dev.ifc.getAddress()[0]
                    except:
                        pass
                else:
                    state = "inaccessible " + _(dhcp_fail_msg)
            else:
                if dev.ifc.isUp():
                    state = "up "
                    try:
                        state += dev.ifc.getAddress()[0]
                    except:
                        pass
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
    dev = Dev(name, True)
    return (dev.authmode, dev.user, dev.password)

def kernelEvent(data):
    type, dir = data.split("@", 1)
    if not dir.startswith("/class/net/"):
        return
    devname = dir[11:]
    flag = 1

    ifc = netutils.IF(devname)
    if type == "add":
        if not ifc.isWireless():
            return
        devuid = ifc.deviceUID()
        notify("Net.Link", "deviceChanged", ("added", "wifi", devuid, netutils.deviceName(devuid)))
        conns = DB.listDB()
        for conn in conns:
            dev = Dev(conn)
            if dev.ifc and dev.ifc.name == devname:
                if dev.state == "up":
                    dev.up()
                    return
                flag = 0
        if flag:
            notify("Net.Link", "deviceChanged", ("new", "wifi", devuid, netutils.deviceName(devuid)))

    elif type == "remove":
        conns = DB.listDB()
        for conn in conns:
            dev = Dev(conn)
            # FIXME: ifc is not enough here :(
            if dev.ifc and dev.ifc.name == devname:
                if dev.state == "up":
                    notify("Net.Link", "stateChanged", (dev.name, "inaccessible", "Device removed"))
        notify("Net.Link", "deviceChanged", ("removed", "wifi", devname, ""))
