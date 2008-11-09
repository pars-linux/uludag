#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import sys

link = comar.Link()

def printUsage():
    print "Usage: %s <command>" % sys.argv[0]
    print
    print "Commands:"
    print "    connections  Show connections"
    print "    devices      Show devices"
    print "    create       Create profile"

def getNumber(label, min_, max_):
    index_ = min_ - 1
    while index_ < min_ or index_ > max_:
        try:
            index_ = int(raw_input("%s > " % label))
        except ValueError:
            pass
    return index_

def printConnections():
    for package in link.Network.Link:
        info = link.Network.Link[package].linkInfo()
        print info["name"]
        for profile in link.Network.Link[package].connections():
            profileInfo = link.Network.Link[package].connectionInfo(profile)
            devname = profileInfo["device_name"].split(" - ")[0]
            print "  %s [%s]" % (profile, devname)

def printDevices():
    for package in link.Network.Link:
        info = link.Network.Link[package].linkInfo()
        print info["name"]
        for devid, devname in link.Network.Link[package].deviceList().iteritems():
            print "  %s" % devname

def getPackage():
    packages = []
    print "Select package:"
    index_ = 1
    for package in link.Network.Link:
        info = link.Network.Link[package].linkInfo()
        packages.append(package)
        print "  [%s] %s" % (index_, info["name"])
        index_ += 1
    if not len(packages):
        print "No network backends registered"
        return 1
    packageNo = getNumber("Package", 1, len(packages)) - 1
    return packages[packageNo]

def getDevice(package):
    devices = []
    print
    index_ = 1
    for devid, devname in link.Network.Link[package].deviceList().iteritems():
        devices.append(devid)
        print "  %s %s" % (index_, devname)
        index_ += 1
    if not len(devices):
        print "No devices on that backend"
        return 1
    devNo = getNumber("Device", 1, len(devices)) - 1
    return devices[devNo]

def getDeviceMode(package):
    device_modes = []
    print
    index_ = 1
    for modeName, modeDesc  in link.Network.Link[package].deviceModes():
        print "  [%s] %s" % (index_, modeDesc)
        device_modes.append(modeName)
        index_ += 1
    modeNo = getNumber("Device Mode", 1, len(device_modes)) - 1
    return device_modes[modeNo]

def getRemote(package, device):
    remote = None
    def scanRemote():
        remotes = []
        print
        index_ = 1
        for remotePoint in link.Network.Link[package].scanRemote(device):
            remotes.append(remotePoint["remote"])
            print "  [%s] %s" % (index_, remotePoint["remote"])
            index_ += 1
        print "  [%s] Scan Again" % index_
        print "  [%s] Enter Manually" % (index_ + 1)
        remoteNo = getNumber("Remote", 1, len(remotes) + 2) - 1
        if remoteNo < len(remotes):
            return remotes[remoteNo]
        elif remoteNo == len(remotes):
            return None
        else:
            return raw_input("Enter Remote > ")
    while not remote:
        remote = scanRemote()
    return remote

def getAuth(package):
    print
    print "  [1] No authentication"
    auths = []
    index_ = 2
    for authName, authDesc in link.Network.Link[package].authMethods():
        auths.append(authName)
        print "  [%s] %s" % (index_, authDesc)
        index_ += 1
    authNo = getNumber("Method", 1, len(auths) + 1) - 1
    if authNo == 0:
        return ""
    return auths[authNo - 1]

def getAuthSettings(package, auth):
    settings = []
    if auth:
        print
        for paramName, paramDesc, paramType in link.Network.Link[package].authParameters(auth):
            value = raw_input("%s > " % paramDesc)
            settings.append((paramName, value,))
    return settings

def main():
    try:
        command = sys.argv[1]
    except:
        printUsage()
        return 1

    if command == "connections":
        printConnections()
    elif command == "devices":
        printDevices()
    elif command == "create":
        settings = []
        # Select package
        package = getPackage()
        # Get backend info
        info = link.Network.Link[package].linkInfo()
        modes = info["modes"].split(",")
        # Select device
        if "device" in modes:
            device = getDevice(package)
            settings.append(("device", device))
            # Select device mode
            if "device_mode" in modes:
                deviceMode = getDeviceMode(package)
                settings.append(("device_mode", deviceMode))
        # Remote
        if "remote" in modes:
            if "remote_scan" in modes and "device" in modes:
                remote = getRemote(package, device)
            else:
                print
                remote = raw_input("Enter Remote >")
            settings.append(("remote", remote,))
        # Auth
        if "auth" in modes:
            auth = getAuth(package)
            settings.append(("auth", auth,))
            if auth:
                for key, value in getAuthSettings(package, auth):
                    settings.append(("auth_%s" % key, value,))
        print settings
        return
        # Address
        if "net" in modes:
            print
            auto = False
            if "auto" in modes:
                print "  [1] Enter manually"
                print "  [2] Get address automatically"
                auto = getNumber("Type", 1, 2) == 2
            if auto:
                settings.append(("net_mode", "auto"))
            else:
                net_address = raw_input("Address > ")
                net_mask = raw_input("Mask > ")
                net_gateway = raw_input("Gateway > ")
                settings.append(("net_mode", "manual"))
                settings.append(("net_address", net_address))
                settings.append(("net_mask", net_mask))
                settings.append(("net_gateway", net_gateway))
        # Create
        print
        print settings
    else:
        printUsage()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
