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

import SimpleXMLRPCServer

""" helpers """
from helpers import qmanager
from helpers import repomanager

import main

class CombinedServerClass(qmanager.QueueManager, repomanager.RepositoryManager):
    pass

server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000))

# let server.system.listMethods
server.register_introspection_functions()

# export CombinedServerClass
server.register_instance(CombinedServerClass())

# export buildPackages
server.register_function(main.buildPackages)

# enter main loop
server.serve_forever()
