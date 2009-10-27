#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import comar

link = comar.Link()

device_id = None
for device_id in link.Network.Link["wireless_tools"].deviceList():
    break

if not device_id:
    print "No wireless device"
    sys.exit()

link.Network.Link["wireless_tools"].setDevice("Deneme", device_id)
link.Network.Link["wireless_tools"].setAddress("Deneme", "auto", "", "", "")
link.Network.Link["wireless_tools"].setRemote("Deneme", "Pardus")
link.Network.Link["wireless_tools"].setAuthMethod("Deneme", "wpa-psk")
link.Network.Link["wireless_tools"].setAuthParameters("Deneme", "password", "mypassword")
link.Network.Link["wireless_tools"].setState("Deneme", "up")
