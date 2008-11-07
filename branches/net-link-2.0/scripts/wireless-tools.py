#!/usr/bin/python
# -*- coding: utf-8 -*-

def linkInfo():
    d = {
        "type": "wifi",
        "name": "Wireless", # TODO: Localize value
        "modes": "device,devicemode,remote,remote_scan,net,auto,auth",
    }
    return d

def authMethods():
    return [
        ("wep", "WEP"),
        ("wepascii", "WEP ASCII"),
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
    return "ESS ID" # TODO: Localize

def deviceModes():
    return [
        ("managed", "Managed"), # TODO: Localize 2. element
        ("adhoc", "Ad Hoc"),    # TODO: Localize 2. element
    ]

def deviceList():
    # TODO: Return device dictionary
    return {}

def scanRemote(device):
    # TODO: Return scan results
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
    # TODO: Add/update remote
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
