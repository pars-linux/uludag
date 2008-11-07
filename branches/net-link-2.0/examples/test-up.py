#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
link = comar.Link()

link.Network.Link["net_tools"].setDevice("Deneme", "pci:11ab_436a_eth0")
link.Network.Link["net_tools"].setAddress("Deneme", "manual", "192.168.3.233", "255.255.255.0", "192.168.3.1")
link.Network.Link["net_tools"].setState("Deneme", "up")
