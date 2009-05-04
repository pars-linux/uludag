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
        self.waitFunctions = []
        self.link.listenSignals("Network.Link", self.postProcessor)

    def capabilities(self, package):
        return self.link.Network.Link[package].linkInfo()

    def authMethods(self, package):
        return self.link.Network.Link[package].authMethods()

    def authParameters(self, package, method):
        return self.link.Network.Link[package].authParameters(method)

    def remoteName(self, package):
        return self.link.Network.Link[package].remoteName()

    def connections(self, package):
        return list(self.link.Network.Link[package].connections())

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

    def reconnect(self, package, profile):
        self.disconnect(package, profile)
        self.registerFunc("stateChanged","down", self.connect, package, profile)

    def registerFunc(self, waitSignal, waitValue, func, package, profile):
        data = {"signal" :waitSignal,
                "value"  :waitValue,
                "func"   :func,
                "package":package,
                "profile":profile}
        self.waitFunctions.append(data)

    def setState(self, package, profile, state):
        self.link.Network.Link[package].setState(profile, state, async=self.handler)

    def info(self, package, profile):
        return self.link.Network.Link[package].connectionInfo(str(profile))

    def authType(self, package, profile):
        return self.link.Network.Link[package].getAuthMethod(profile)

    def authInfo(self, package, profile):
        return self.link.Network.Link[package].getAuthParameters(profile)

    def handler(self, *args):
        print args

    def postProcessor(self, package, signal, args):
        finishedFunctions = []
        args = map(lambda x: unicode(x), list(args))
        # walk in waiting functions
        for waitFunc in self.waitFunctions:
            if signal == str(waitFunc["signal"]) and args[1].startswith(waitFunc["value"]):
                if package == str(waitFunc["package"]) and unicode(args[0]) == waitFunc["profile"]:
                    # run the function
                    waitFunc["func"](waitFunc["package"], waitFunc["profile"])
                    # and pop it from queue
                    finishedFunctions.append(waitFunc)
        # remove all finished functions
        for finishedFunc in finishedFunctions:
            self.waitFunctions.remove(finishedFunc)

    def listen(self, func):
        self.link.listenSignals("Network.Link", func)

    def updateConnection(self, package, profile, data):
        info = self.capabilities(package)
        modes = info["modes"].split(",")

        if "device" in modes:
            self.link.Network.Link[package].setDevice(profile,  data["device_id"],  async=self.handler)

        if "net" in modes:
            self.link.Network.Link[package].setAddress(profile, data["net_mode"],
                                                                data["net_address"],
                                                                data["net_mask"],
                                                                data["net_gateway"],async=self.handler)
            self.link.Network.Link[package].setNameService(profile, data["name_mode"],
                                                                data["name_server"], async=self.handler)

        if "remote" in modes:
            self.link.Network.Link[package].setRemote(profile, data["remote"])

        if "auth" in modes:
            self.link.Network.Link[package].setAuthMethod(profile, data["auth"])

            for key, label, type_ in self.link.Network.Link[package].authParameters(data["auth"]):
                self.link.Network.Link[package].setAuthParameters(profile, key, data.get("auth_%s" % key, ""), async=self.handler)

    def deleteConnection(self, package, profile):
        self.link.Network.Link[package].deleteConnection(profile, aysnc=self.handler)

    def devices(self, package):
        return self.link.Network.Link[package].deviceList()

    def packages(self):
        return list(self.link.Network.Link)

    def linkInfo(self, package):
        return self.link.Network.Link[package].linkInfo()

    def scanRemote(self, device, package="wireless_tools", func=None):
        if func:
            self.link.Network.Link[package].scanRemote(device, async=func)
        else:
            return self.link.Network.Link[package].scanRemote(device)

