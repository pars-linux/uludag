#!/usr/bin/python
# -*- coding: utf-8 -*-

MSG_ETHERNET = {
    "en": "Ethernet",
    "tr": "Ethernet Ağları",
}

MSG_DHCP_FAILED = {
    "en": "Unable to get address.",
    "tr": "Adres alınamadı.",
}

import os
from pardus import netutils, iniutils

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

    def save(self):
        is_new = self.name not in listProfiles()
        self.db.setDB(self.name, self.info)
        if is_new:
            notify("Network.Link", "connectionChanged", ("added", self.name))
        else:
            notify("Network.Link", "connectionChanged", ("changed", self.name))

def stopSameDevice(name):
    profile = Profile(name)
    device = profile.info["device"]
    for pn in listProfiles():
        if pn == name:
            continue
        pro = Profile(pn)
        if pro.info["device"] == device:
            setState(pn, "down")

# Network.Link methods

def linkInfo():
    return {
        "type": "net",
        "name": _(MSG_ETHERNET),
        "modes": "device,net,auto",
    }

def authMethods():
    # TODO: Raise an exception here. "auth" mode not supported
    return []

def authParameters(mode):
    # TODO: Raise an exception here. "auth" mode not supported
    return []

def remoteName():
    # TODO: Raise an exception here. "remote" mode not supported
    return ""

def deviceModes():
    # TODO: Raise an exception here. "device_mode" mode not supported
    return []

def deviceList():
    iflist = {}
    for ifc in netutils.interfaces():
        if ifc.isEthernet() and not ifc.isWireless():
            uid = ifc.deviceUID()
            info = netutils.deviceName(uid)
            iflist[uid] = info
    return iflist

def scanRemote(device):
    # TODO: Raise an exception here. "remote_scan" mode not supported
    return []

def setDevice(name, device):
    profile = Profile(name)
    profile.info["device"] = device
    profile.save()

def setDeviceMode(name, mode):
    # TODO: Raise an exception here. "device_mode" mode not supported
    pass

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
    # TODO: Raise an exception here. "remote" mode not supported
    pass

def setNameService(name, namemode, nameserver):
    # TODO: Add/update name servers
    pass

def setAuthMethod(name, method):
    # TODO: Raise an exception here. "auth" mode not supported
    pass

def setAuthParameters(name, key, value):
    # TODO: Raise an exception here. "auth" mode not supported
    pass

def getAuthMethod(name):
    # TODO: Raise an exception here. "auth" mode not supported
    return ""

def getAuthParameters(name):
    # TODO: Raise an exception here. "auth" mode not supported
    return {}

def getState(name):
    profile = Profile(name)
    return profile.info.get("state", "down")

def setState(name, state):
    profile = Profile(name)
    iface = netutils.findInterface(profile.info["device"])
    if state == "up":
        # Stop other profiles on same device
        stopSameDevice(name)
        # Notify clients
        notify("Network.Link", "stateChanged", (name, "connecting", ""))
        # Save state to profile database
        profile.info["state"] = "connecting"
        profile.save()
        if profile.info.get("net_mode", "auto") == "auto":
            # Start DHCP client
            ret = iface.startAuto()
            if ret == 0 and iface.isUp():
                address = iface.getAddress()
                if address:
                    # Save state to profile database
                    profile.info["state"] = "up " + address[0]
                    profile.save()
                    # Notify clients
                    notify("Network.Link", "stateChanged", (name, "up", address[0]))
                else:
                    iface.down()
                    # Save state to profile database
                    profile.info["state"] = "down"
                    profile.save()
                    # Notify clients
                    notify("Network.Link", "stateChanged", (name, "inaccesible", _(MSG_DHCP_FAILED)))
            else:
                iface.down()
                # Save state to profile database
                profile.info["state"] = "down"
                profile.save()
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
            iface.up()
            # Set default gateway
            route = netutils.Route()
            route.setDefault(net_gateway)
            # Save state to profile database
            profile.info["state"] = "up " + net_address
            profile.save()
            # Notify clients
            notify("Network.Link", "stateChanged", (name, "up", net_address))
    elif state == "down":
        if profile.info.get("net_mode", "auto") == "auto":
            iface.stopAuto()
        iface.down()
        # Save state to profile database
        profile.info["state"] = "down"
        profile.save()
        # Notify clients
        notify("Network.Link", "stateChanged", (name, "down", ""))

def connections():
    return listProfiles()

def connectionInfo(name):
    # TODO: Expand
    profile = Profile(name)
    device = profile.info["device"]
    return {
        "name": name,
        "device_id": device,
        "device_name": netutils.deviceName(device),
        "state": profile.info.get("state", "down"),
    }

def kernelEvent(data):
    # TODO: Handle UDEV event
    pass
