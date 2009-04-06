#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import comar

class NetworkIface:
    """ Network Interface """

    def __init__(self):
        self.link = comar.Link()

    def connections(self, package):
        return list(self.link.Net.Link[package].connections())

    def connect(self, package, profile):
        self.setState(package, profile, "up")

    def disconnect(self, package, profile):
        self.setState(package, profile, "down")

    def toggle(self, package, profile):
        info = self.info(package, profile)
        if str(info['state']) == "down":
            self.connect(package, profile)
        else:
            self.disconnect(package, profile)

    def delete(self, package, profile):
        self.link.Net.Link[package].deleteConnection(profile)

    def setState(self, package, profile, state):
        self.link.Net.Link[package].setState(profile, state, async=self.handler)

    def info(self, package, profile):
        return self.link.Net.Link[package].connectionInfo(str(profile))

    def handler(self, *args):
        pass

    def listen(self, func):
        self.link.listenSignals("Net.Link", func)

