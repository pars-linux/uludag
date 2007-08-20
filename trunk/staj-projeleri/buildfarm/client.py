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

REMOTE_HOST = "localhost"
REMOTE_PORT = 443

import xmlrpclib

if __name__ == "__main__":
    
    # Handle command-line arguments
    
    remoteURI = "https://" + REMOTE_HOST + ":" + str(REMOTE_PORT)
    server = xmlrpclib.ServerProxy(remoteURI)

    print "Provided Methods: %s\n" % server.system.listMethods()

    # print server._buildPackages()
