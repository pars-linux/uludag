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

server = xmlrpclib.Server('http://localhost:8000')

print "Provided Methods: %s\n" % server.system.listMethods()

print "Update repository: %s" % server.updateRepository()

print "WorkQueue: %s" % server.getWorkQueue()
print "WaitQueue: %s" % server.getWaitQueue()

print "Remove A from WorkQueue: %s" % server.removeFromWorkQueue("system/base/bzip2/pspec.xml")
print "Append B to WaitQueue: %s" % server.appendToWaitQueue("system/base/bzip2/pspec.xml")
print "Append A to WorkQueue: %s" % server.appendToWorkQueue("system/base/gzip/pspec.xml")
print "Transfer A to WaitQueue: %s" % server.transferToWorkQueue("system/base/gzip/pspec.xml")

print "WorkQueue: %s" % server.getWorkQueue()
print "WaitQueue: %s" % server.getWaitQueue()

print server.buildPackages()
