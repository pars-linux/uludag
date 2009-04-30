#!/usr/bin/python
# -*- coding: utf-8 -*-

MSG_WIRELESS = {
    "en": "Wireless",
    "tr": "Kablosuz Ağlar",
}

MSG_DHCP_FAILED = {
    "en": "Unable to get address.",
    "tr": "Adres alınamadı.",
}

MSG_NO_SUPPLICANT = {
    "en": "WPA supplicant not found.",
    "tr": "WPA supplicant bulunamadı.",
}

MSG_NO_SUPPLICANT_SERVICE = {
    "en": "Unable to start WPA supplicant service.",
    "tr": "WPA servisi başlatılamadı.",
}

MSG_WPA_FAILED = {
    "en": "Authentication failed.",
    "tr": "Kimlik doğrulama başarısız.",
}

import os
import re
import socket
import array
import struct
import fcntl
import subprocess

from pardus import netutils, iniutils

# From </usr/include/wireless.h>
SIOCSIWMODE = 0x8B06    # set the operation mode
SIOCGIWMODE = 0x8B07    # get operation mode
SIOCGIWRATE = 0x8B21    # get default bit rate
SIOCSIWESSID = 0x8B1A   # set essid
SIOCGIWESSID = 0x8B1B   # get essid

def listProfiles():
    db = iniutils.iniDB(os.path.join("/etc/network-link", script()))
    return db.listDB()

class Profile:
    def __init__(self, name):
        self.name = name
        self.db = iniutils.iniDB(os.path.join("/etc/network-link", script()))
        self.info = self.db.getDB(self.name)

    def delete(self):
        self.db.remDB(self.name)

    def save(self, no_notify=False):
        is_new = self.name not in listProfiles()
        self.db.setDB(self.name, self.info)
        if no_notify:
            return
        if is_new:
            notify("Network.Link", "connectionChanged", ("added", self.name))
        else:
            notify("Network.Link", "connectionChanged", ("changed", self.name))

class AccessPoint:
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
    modes = ['auto', 'adhoc', 'managed', 'master', 'repeat', 'second', 'monitor']

    def __init__(self, ifc):
        self.sock = None
        self.ifc = ifc
        self.ssid = None

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
        self.ssid = ssid
        point = AccessPoint(ssid)
        buffer = array.array('c', point.ssid + '\x00')
        addr, length = buffer.buffer_info()
        arg = struct.pack("iHH", addr, length, 1)
        self._call(SIOCSIWESSID, arg)
        if self.getSSID() is point.ssid:
            return True
        else:
            return False

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
                point = AccessPoint()
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
                if "WPA" in ie or "WPA2" in ie:
                    point.encryption = "wpa-psk"
            if "Authentication Suites" in line:
                point.auth_suit = line.split(":")[1].strip()
                if "802.1x" in point.auth_suit:
                    point.encryption = "802.1x"
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
            return False

    def setEncryption(self, mode=None, parameters=None):
        supplicant = True
        try:
            import wpa_supplicant
        except ImportError:
            supplicant = False

        os.system("/usr/sbin/iwconfig %s enc off" % self.ifc.name)

        if supplicant and wpa_supplicant.isWpaServiceUsable():
            wpa_supplicant.disableAuthentication(self.ifc.name)

        # TODO a guessEncryption() function to determine if its wep or wepascii or open (no enc)
        # TODO check returning data from iwconfig, these calls dont work most of the time but we simply pass
        if mode == "wep":
            os.system("/usr/sbin/iwconfig '%s' enc restricted '%s'" % (self.ifc.name, parameters["password"]))
        elif mode == "wepascii":
            os.system("/usr/sbin/iwconfig '%s' enc restricted 's:%s'" % (self.ifc.name, parameters["password"]))
        elif mode == "wpa-psk":
            if not supplicant:
                fail(_(MSG_NO_WPA))
            if not wpa_supplicant.startWpaService():
                fail(_(MSG_NO_SUPPLICANT_SERVICE))
            ret = wpa_supplicant.setWpaAuthentication(self.ifc.name, self.ssid, parameters["password"])
            if not ret:
                fail(_(MSG_WPA_FAILED))
        elif mode == "802.1x":
            pass

    def getBitrate(self, ifname):
        # Note for UI coder, KILO is not 2^10 in wireless tools world
        result = self._call(SIOCGIWRATE)
        size = struct.calcsize('ihbb')
        m, e, i, pad = struct.unpack('ihbb', result[16:16+size])
        if e == 0:
            bitrate =  m
        else:
            bitrate = float(m) * 10**e
        return bitrate

def stopSameDevice(name):
    profile = Profile(name)
    device = profile.info["device"]
    for pn in listProfiles():
        if pn == name:
            continue
        pro = Profile(pn)
        if pro.info["device"] == device:
            setState(pn, "down")

def registerNameServers(profile, iface):
    name_mode = profile.info.get("name_mode", "default")
    name_servers = []
    name_domain = ""
    if name_mode == "auto":
        for server in iface.autoNameServers():
            name_servers.append(server)
        name_domain = iface.autoNameSearch()
    elif name_mode == "custom":
        for server in profile.info.get("name_server", ",").split():
           if server.strip():
               name_servers.append(server.strip())
    elif name_mode == "default":
        name_servers = call("dnsmasq", "Network.Stack", "getNameServers")
    call("dnsmasq", "Network.Stack", "registerNameServers", (iface.name, name_servers, name_domain))

def unregisterNameServers(iface):
    call("dnsmasq", "Network.Stack", "unregisterNameServers", (iface.name, [], ""))

# Network.Link methods

def linkInfo():
    d = {
        "type": "wifi",
        "name": _(MSG_WIRELESS),
        "modes": "device,device_mode,remote,remote_scan,net,auto,auth",
    }
    return d

def authMethods():
    return [
        ("wep", "WEP"),                     # TODO: Localize 2. element
        ("wepascii", "WEP ASCII"),          # TODO: Localize 2. element
        ("wpa-psk", "WPA Pre Shared Key"),  # TODO: Localize 2. element
        ("802.1x", "WPA Dynamic Key"),      # TODO: Localize 2. element
    ]

def authParameters(mode):
    if mode in ("wep", "wepascii", "wpa-psk"):
        return [
            ("password", "Password", "pass"), # TODO: Localize 2. element
        ]
    elif mode == "802.1x":
        return [
            ("username", "Username", "text"),           # TODO: Localize 2. element
            ("password", "Password", "pass"),           # TODO: Localize 2. element
            ("cert_cli", "Client Certificate", "file"), # TODO: Localize 2. element
            ("cert_ca", "CA Certificate", "file"),      # TODO: Localize 2. element
            ("keyfile", "Keyfile", "file"),             # TODO: Localize 2. element
        ]

def remoteName():
    return "ESS ID"

def deviceModes():
    return [
        ("managed", "Managed"), # TODO: Localize 2. element
        ("adhoc", "Ad Hoc"),    # TODO: Localize 2. element
    ]

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

def setDevice(name, device):
    profile = Profile(name)
    profile.info["device"] = device
    profile.save()

def setDeviceMode(name, mode):
    profile = Profile(name)
    profile.info["device_mode"] = mode
    profile.save()

def deleteConnection(name):
    profile = Profile(name)
    profile.delete()
    notify("Network.Link", "connectionChanged", ("deleted", name))

def setAddress(name, mode, address, mask, gateway):
    profile = Profile(name)
    profile.info["net_mode"] = mode
    profile.info["net_address"] = address
    profile.info["net_mask"] = mask
    profile.info["net_gateway"] = gateway
    profile.save()

def setRemote(name, remote):
    profile = Profile(name)
    profile.info["remote"] = remote
    profile.save()

def setNameService(name, namemode, nameserver):
    profile = Profile(name)
    profile.info["name_mode"] = namemode
    profile.info["name_server"] = nameserver
    profile.save()

def setAuthMethod(name, method):
    profile = Profile(name)
    profile.info["auth"] = method
    profile.save()

def setAuthParameters(name, key, value):
    profile = Profile(name)
    profile.info["auth_%s" % key] = value
    profile.save()

def getAuthMethod(name):
    profile = Profile(name)
    return profile.info.get("auth", "")

def getAuthParameters(name):
    profile = Profile(name)
    d = {}
    for key in profile.info:
        if key.startswith("auth_"):
            d[key[5:]] = profile.info[key]
    return d

def getState(name):
    profile = Profile(name)
    return profile.info.get("state", "down")

def setState(name, state):
    profile = Profile(name)
    iface = netutils.findInterface(profile.info["device"])
    device_mode = profile.info.get("device_mode", "managed")
    if device_mode == "managed":
        if state == "up":
            # Stop other profiles on same device
            stopSameDevice(name)
            # Notify clients
            notify("Network.Link", "stateChanged", (name, "connecting", ""))
            # Save state to profile database
            profile.info["state"] = "connecting"
            profile.save(no_notify=True)
            # Wifi settings
            wifi = Wireless(iface)
            wifi.setSSID(profile.info["remote"])
            # Set encryption
            wifi.setEncryption(getAuthMethod(name), getAuthParameters(name))
            if profile.info.get("net_mode", "auto") == "auto":
                # Start DHCP client
                ret = iface.startAuto()
                if ret == 0 and iface.isUp() and iface.getAddress():
                    address = iface.getAddress()
                    # Set nameservers
                    registerNameServers(profile, iface)
                    # Save state to profile database
                    profile.info["state"] = "up " + address[0]
                    profile.save(no_notify=True)
                    # Notify clients
                    notify("Network.Link", "stateChanged", (name, "up", address[0]))
                else:
                    iface.down()
                    # Save state to profile database
                    profile.info["state"] = "down"
                    profile.save(no_notify=True)
                    # Notify clients
                    notify("Network.Link", "stateChanged", (name, "inaccesible", _(MSG_DHCP_FAILED)))
            else:
                try:
                    net_address = profile.info["net_address"]
                    net_mask = profile.info["net_mask"]
                    net_gateway = profile.info["net_gateway"]
                except KeyError:
                    return
                # Set address
                iface.setAddress(net_address, net_mask)
                # Bring up interface
                iface.up()
                # Set default gateway
                route = netutils.Route()
                route.setDefault(net_gateway)
                # Set nameservers
                registerNameServers(profile, iface)
                # Save state to profile database
                profile.info["state"] = "up " + net_address
                profile.save(no_notify=True)
                # Notify clients
                notify("Network.Link", "stateChanged", (name, "up", net_address))
        elif state == "down":
            if profile.info.get("net_mode", "auto") == "auto":
                iface.stopAuto()
            # Set encryption to none
            wifi = Wireless(iface)
            wifi.setEncryption(None, None)
            # Reset Network Stack
            unregisterNameServers(iface)
            # Bring down interface
            iface.down()
            # Save state to profile database
            profile.info["state"] = "down"
            profile.save(no_notify=True)
            # Notify clients
            notify("Network.Link", "stateChanged", (name, "down", ""))
    elif device_mode == "adhoc":
        # TODO: AdHoc support
        pass

def connections():
    return listProfiles()

def connectionInfo(name):
    profile = Profile(name)
    device = profile.info["device"]
    return {
        "name": name,
        "device_id": device,
        "device_name": netutils.deviceName(device),
        "device_mode": profile.info.get("device_mode", "managed"),
        "net_mode": profile.info.get("net_mode", "auto"),
        "net_address": profile.info.get("net_address", ""),
        "net_mask": profile.info.get("net_mask", ""),
        "net_gateway": profile.info.get("net_gateway", ""),
        "remote": profile.info.get("remote", ""),
        "name_mode": profile.info.get("name_mode", "default"),
        "name_server": profile.info.get("name_server", ""),
        "state": profile.info.get("state", "down"),
    }

def kernelEvent(data):
    # TODO: Handle UDEV event
    pass
