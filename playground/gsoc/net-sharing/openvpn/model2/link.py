#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import commands

from pardus import netutils
from pardus import iniutils

#Net.Share 

ifcfg = "/sbin/ifconfig"
dhcpfl = "/etc/dhcp/dhcpd.conf"
namefl = "/etc/resolv.conf"

def checkShare(net_addr, net_mode, net_mask, name_srv):
    subnet = get_subnet(net_addr, net_mask)

    if name_srv == "":
        nmfl = open(namefl, "r")
        name_srv = nmfl.readline().split(" ")[1][:-1]
        nmfl.close()

    dhfl = open(dhcpfl, "w")
    dhfl.write("ddns-update-style interim;\n")
    dhfl.write("ignore client-updates;\n\n")
    dhfl.write("max-lease-time 500;\n")
    dhfl.write("default-lease-time 500;\n")
    if net_mode == "manual":
        dhfl.write("option domain-name-servers %s;\n" %(name_srv))
        dhfl.write("option routers %s;\n" % (net_addr))
        dhfl.write("option subnet-mask %s;\n" % (net_mask))
        dhfl.write("subnet %s netmask %s {\n" %(subnet, net_mask))
        ip = net_addr.split(".")
        dhfl.write("   range %s.%s.%s.2 %s.%s.%s.254;\n"%(ip[0], ip[1], ip[2], ip[0], ip[1], ip[2]))
    else:
        dhfl.write("option domain-name-servers 193.140.100.220;\n")
        dhfl.write("option routers 192.168.120.1;\n")
        dhfl.write("option subnet-mask 255.255.255.0;\n")
        dhfl.write("subnet 192.168.120.0 netmask 255.255.255.0 {\n")
        dhfl.write("   range 192.168.120.2 192.168.120.254;\n")

    dhfl.write("}\n")
    dhfl.close()

def get_subnet(net_addr, net_mask):
    addr = net_addr.split(".")
    mask = net_mask.split(".")
    addr[0] = str( int(addr[0]) & int(mask[0]))
    addr[1] = str( int(addr[1]) & int(mask[1]))
    addr[2] = str( int(addr[2]) & int(mask[2]))
    addr[3] = str( int(addr[3]) & int(mask[3]))
    return str(addr[0]+"."+addr[1]+"."+addr[2]+"."+addr[3])

