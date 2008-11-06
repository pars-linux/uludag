#!/usr/bin/python
# -*- coding: utf-8 -*-

def linkInfo():
    d = {
        "type": "net",
        "name": "Ethernet", # TODO: Localize value
        "modes": "device,net,auto",
    }
    return d

def authModes():
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
    # TODO: Return device dictionary
    return {}

def scanRemote(device):
    # TODO: Raise an exception here. "remote_scan" mode not supported
    return []

def setConnection(name, device):
    # TODO: Add/update device
    pass

def setDeviceMode(name, mode):
    # TODO: Add/update device mode
    pass

def deleteConnection(name):
    # TODO: Delete profile
    pass

def setAddress(name, mode, address, mask, gateway):
    # TODO:
    pass

def setRemote(name, remote):
    # TODO: Raise an exception here. "remote" mode not supported
    pass

def setNameService(name, namemode, nameserver):
    # TODO: Add/update name servers
    pass

def setAuthMode(name, mode):
    # TODO: Raise an exception here. "auth" mode not supported
    pass

def setAuthParameters(name, key, value):
    # TODO: Raise an exception here. "auth" mode not supported
    pass

def getAuthMode(name):
    # TODO: Raise an exception here. "auth" mode not supported
    return ""

def getAuthParameters(name):
    # TODO: Raise an exception here. "auth" mode not supported
    return {}

def getState(name):
    # TODO: Return state
    return "down"

def setState(name, state):
    # TODO: Change state
    pass

def connections():
    # TODO: Return list of profile names
    return []

def connectionInfo(name=None):
    # TODO: Return profile info
    return {}

def kernelEvent(data):
    # TODO: Handle UDEV event
    pass
