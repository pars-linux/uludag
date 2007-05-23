# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import xmlrpclib

class Bugzilla:

    def __init__(self):
        self.uri = "http://bugs.pardus.org.tr/xmlrpc.cgi"
        self.debug = False

    def connect(self):
        connection = xmlrpclib.ServerProxy(self.uri)
        try:
            versionInfo = connection.Bugzilla.version()
            if not int(versionInfo['version'][0]) > 2:
                raise "ServerError","Server has an old version of Bugzilla."
        except:
            raise "ConnectionError","Cannot reach the server: %s." % self.uri

        self.connection = connection
