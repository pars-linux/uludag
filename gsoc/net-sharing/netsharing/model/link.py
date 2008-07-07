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

brcmd = "/usr/sbin/brctl"
ifcfg = "/sbin/ifconfig"

def addBridge(br_name):
    tup_obj = commands.getstatusoutput("%s show" % brcmd)
    if tup_obj[0] == 0:
        output = str(tup_obj[1])
        if output.find("%s\t" % br_name) != -1:
            fail("This bridge already exists")

    tup_obj = commands.getstatusoutput("%s addbr %s" %(brcmd, br_name))
    if tup_obj[0] != 0:
        fail("%s cannot created" % br_name)
    commands.getstatusoutput("%s %s up" %(ifcfg, br_name))

def delBridge(br_name):
    commands.getstatusoutput("%s %s down" % (ifcfg, br_name))
    tup_obj =  commands.getstatusoutput("%s delbr %s" % (brcmd, br_name))
    if tup_obj[0] != 0:
        fail(str(tup_obj[1]))
    
def addInterface(br_name, if_name):
    tup_obj = commands.getstatusoutput("%s show" % brcmd)
    if tup_obj[0] == 0:
        output = str(tup_obj[1])
	if output.find("%s\t" % br_name) != -1:
            if output.find(if_name) != -1:
                fail("The interface %s already exists in %s" % (if_name, br_name))
	else:
	    fail("There is no such bridge to add an interface")

    tup_obj = commands.getstatusoutput("%s addif %s %s" %(brcmd, br_name, if_name))
    
    if tup_obj[0] != 0:
        fail("Interface %s cannot be added to the bridge %s " % (if_name, br_name))

def delInterface(br_name, if_name):
    commands.getstatusoutput("%s delif %s %s" % (brcmd, br_name, if_name))

def checkShare(int_if, shr_if):
    commands.getstatusoutput("/sbin/ifconfig %s" %(shr_if))
    if tup_obj
    
