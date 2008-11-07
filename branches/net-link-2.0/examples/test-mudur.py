#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# How Mudur bring network devices up
#

import os
import sys

if os.getuid() != 0:
    print "Run as root"
    sys.exit(1)

import comar
link = comar.Link()

for package in link.Network.Link:
    for profile in link.Network.Link[package].connections():
        info = link.Network.Link[package].connectionInfo(profile)
        if info.get("state", "down").startswith("up"):
            print "Bringing up %s" % info["device_id"]
            link.Network.Link[package].setState(profile, "up", quiet=True)
