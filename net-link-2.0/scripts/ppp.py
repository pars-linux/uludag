#!/usr/bin/python
# -*- coding: utf-8 -*-

def linkInfo():
    d = {
        "type": "dialup",
        "name": "Dialup Network", # TODO: Localize value
        "modes": "device,remote,auth",
    }
    return d

def authMethods():
    return [
        ("login", "Login/Password"), # TODO: Localize 2. element
    ]

def authParameters(mode):
    return [
        ("username", "Username", "text"), # TODO: Localize 2. element
        ("password", "Password", "pass"), # TODO: Localize 2. element
    ]

def remoteName():
    return "Phone Number" # TODO: Localize

def deviceModes():
    # TODO: Raise an exception here. "device_mode" mode not supported
    return []

def deviceList():
    # TODO: Return device dictionary
    return {}

def scanRemote(device):
    # TODO: Raise an exception here. "remote_scan" mode not supported
    return []

def setDevice(name, device):
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
    # TODO: Add/updat remote
    pass

def setNameService(name, namemode, nameserver):
    # TODO: Add/update name servers
    pass

def setAuthMethod(name, method):
    # TODO: Add/update auth mode
    pass

def setAuthParameters(name, key, value):
    # TODO: Add/update auth parameter
    pass

def getAuthMethod(name):
    # TODO: Return auth mode
    return None

def getAuthParameters(name):
    # TODO: Return auth parameters dictionary
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

def connectionInfo(name):
    # TODO: Return profile info
    return {}

def kernelEvent(data):
    # TODO: Handle UDEV event
    pass
