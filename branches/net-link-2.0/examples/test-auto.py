#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
link = comar.Link()

link.Network.Link["net_tools"].setDevice("Deneme", "pci:11ab_436a_eth0")
link.Network.Link["net_tools"].setAddress("Deneme", "auto", "", "", "")
link.Network.Link["net_tools"].setState("Deneme", "up")
