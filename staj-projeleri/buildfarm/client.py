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
import config

if __name__ == "__main__":
    
    # Handle command-line arguments
    
    
    remoteURI = "https://" + config.HOST + ":" + str(config.PORT)
    server = xmlrpclib.ServerProxy(remoteURI)

    print "Provided Methods: %s\n" % server.system.listMethods()

