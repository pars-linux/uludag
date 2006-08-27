# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

""" COMAR module """
import comar

class comarInterface:

    def __init__(self):
        """ initialize comar link """
        self.link = comar.Link()
        self.WIRED = "net-tools"
        self.WIRELESS = "wireless-tools"

    def listWirelessConnections(self):
        """ list all wireless connections """
        self.link.call_package("Net.Link.connections", self.WIRELESS)
        return self.link.read_cmd()[2].split("\n")

    def listWiredConnections(self):
        self.link.call_package("Net.Link.connections", self.WIRED)
        return self.link.read_cmd()[2].split("\n")

    def isWirelessConnectionActive(self, connection):
        self.link.call_package("Net.Link.getState", self.WIRELESS, [ "name", connection ])
        status = self.link.read_cmd()[2].split('\n')
        if status[1] == "up":
            return True
        else:
            return False

    def isWiredConnectionActive(self, connection):
        self.link.call_package("Net.Link.getState", self.WIRED, [ "name", connection ])
        status = self.link.read_cmd()[2].split('\n')
        if status[1] == "up":
            return True
        else:
            return False

    def getActiveWirelessConnection(self):
        for connection in self.listWirelessConnections():
            self.link.call_package("Net.Link.getState", self.WIRELESS, [ "name", connection ]) 
            status = self.link.read_cmd()[2].split("\n")
            if status[1] == "up":
                return status[0]

    def getActiveWiredConnection(self):
        for connection in self.listWiredConnections():
            self.link.call_package("Net.Link.getState", self.WIRED, [ "name", connection ]) 
            status = self.link.read_cmd()[2].split("\n")
            if status[1] == "up":
                return status[0]

    def activateWirelessConnection(self, connection):
        self.link.call_package("Net.Link.setState", self.WIRELESS, [ "name", connection, "state", "up" ])
        self.link.read_cmd()

    def deactivateWirelessConnection(self, connection):
        self.link.call_package("Net.Link.setState", self.WIRELESS, [ "name", connection, "state", "down" ])
        self.link.read_cmd()

    def activateWiredConnection(self, connection):
        self.link.call_package("Net.Link.setState", self.WIRED, [ "name", connection, "state", "up" ])
        self.link.read_cmd()

    def deactivateWiredConnection(self, connection):
        self.link.call_package("Net.Link.setState", self.WIRED, [ "name", connection, "state", "down" ])
        self.link.read_cmd()
