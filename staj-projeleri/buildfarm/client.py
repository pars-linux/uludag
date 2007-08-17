#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

import xmlrpclib

server = xmlrpclib.Server("https://localhost:443")

print "Provided Methods: %s\n" % server.system.listMethods()

print "Update repository: %s" % server.updateRepository()

print "WorkQueue: %s" % server.getWorkQueue()
print "WaitQueue: %s" % server.getWaitQueue()

print "Remove A from WorkQueue: %s" % server.removeFromWorkQueue("a/pspec.xml")
print "Append B to WaitQueue: %s" % server.appendToWaitQueue("b/pspec.xml")
print "Append A to WorkQueue: %s" % server.appendToWorkQueue("a/pspec.xml")
print "Transfer A to WaitQueue: %s" % server.transferToWorkQueue("a/pspec.xml")

print "WorkQueue: %s" % server.getWorkQueue()
print "WaitQueue: %s" % server.getWaitQueue()

#print server.buildPackages()
