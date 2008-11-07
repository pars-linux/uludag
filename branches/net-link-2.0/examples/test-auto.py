#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import comar

link = comar.Link()

device_id = None
for device_id in link.Network.Link["net_tools"].deviceList():
    break

if not device_id:
    print "No ethernet device"
    sys.exit()

link.Network.Link["net_tools"].setDevice("Deneme", device_id)
link.Network.Link["net_tools"].setAddress("Deneme", "auto", "", "", "")
link.Network.Link["net_tools"].setState("Deneme", "up")
