#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# How Mudur bring network devices up
#

import os
import sys
import time

if os.getuid() != 0:
    print "Run as root"
    sys.exit(1)

import comar
link = comar.Link()

for package in link.Network.Link:
    info = link.Network.Link[package].linkInfo()
    if info["type"] == "net":
        for profileName in link.Network.Link[package].connections():
            profileInfo = link.Network.Link[package].connectionInfo(profileName)
            if profileInfo.get("state", "down").startswith("up"):
                print "Bringing up %s" % profileInfo["device_id"]
                link.Network.Link[package].setState(profileName, "up", quiet=True)
    elif info["type"] == "wifi":
        devices = {}
        for deviceId in link.Network.Link[package].deviceList():
            devices[deviceId] = []
            for point in link.Network.Link[package].scanRemote(deviceId):
                devices[deviceId].append(point["remote"])
        #
        skip = False
        for profileName in link.Network.Link[package].connections():
            profileInfo = link.Network.Link[package].connectionInfo(profileName)
            if profileInfo.get("state", "down").startswith("up") and profileInfo.get("device_id", None) in devices:
                print "Bringing up %s" % profileInfo["device_id"]
                link.Network.Link[package].setState(profileName, "up", quiet=True)
                skip = True
                break
        #
        if not skip:
            for profileName in link.Network.Link[package].connections():
                profileInfo = link.Network.Link[package].connectionInfo(profileName)
                if profileInfo.get("device_id", None) in devices and profileInfo["remote"] in devices[profileInfo["device_id"]]:
                    print "Bringing up %s" % profileInfo["device_id"]
                    link.Network.Link[package].setState(profileName, "up", quiet=True)
                    break


# Give COMAR some time to get process ID
time.sleep(5)
