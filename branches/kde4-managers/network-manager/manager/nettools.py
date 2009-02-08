#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import comar

class Iface:
    """
        Network operations abstraction layer
    """

    def __init__(self):
        # Connect to COMAR
        self.link = comar.Link()

        # COMAR 3.0
        # self.link = comar.Link("3")
        # self.link.setLocale()

        # Listeners
        self.listener_conn_new = []
        self.listener_conn_del = []
        self.listener_conn_edit = []
        self.listener_conn_info = []
        self.listener_conn_list = []
        self.listener_conn_state = []
        self.listener_back_info = []

        # Listen network signals
        self.link.listenSignals("Net.Link", self.__signalHandler)

    def __signalHandler(self, package, signal, args):
        if signal == "connectionChanged":
            operation, profile = args
            if operation == "deleted":
                for func in self.listener_conn_del:
                    func(package, profile)
            elif operation == "added":
                for func in self.listener_conn_new:
                    func(package, profile)
            elif operation == "changed":
                for func in self.listener_conn_edit:
                    func(package, profile)
        elif signal == "stateChanged":
            profile, state, message = args
            for func in self.listener_conn_state:
                func(package, profile, state, message)

    def __handleConnectionInfo(self, package, exception, results):
        if not exception:
            info = results[0]
            profile = info["name"]
            for func in self.listener_conn_info:
                func(package, profile, info)

    def __handleConnectionList(self, package, exception, results):
        if not exception:
            profiles = results[0]
            for func in self.listener_conn_list:
                func(package, profiles)

    def __handleBackendInfo(self, package, exception, results):
        if not exception:
            info = results[0]
            for func in self.listener_back_info:
                func(package, info)

    def __handleConnectionDelete(self, package, exception, results):
        pass

    def __handleConnectionState(self, package, exception, results):
        pass

    def listenConnectionNew(self, func):
        """
            Registers function to be called after 'new connection' signal fetched.
            Backend and profile name will be passed to function as arguments.
        """
        self.listener_conn_new.append(func)

    def listenConnectionDel(self, func):
        """
            Registers function to be called after 'deleted connection' signal fetched.
            Backend and profile name will be passed to function as arguments.
        """
        self.listener_conn_del.append(func)

    def listenConnectionEdit(self, func):
        """
            Registers function to be called after 'updated connection' signal fetched.
            Backend and profile name will be passed to function as arguments.
        """
        self.listener_conn_edit.append(func)

    def getConnectionInfo(self, backend, profile):
        """
            Gets connection informatio of profile on specified backend.
        """
        self.link.Net.Link[backend].connectionInfo(profile, async=self.__handleConnectionInfo)

    def listenConnectionInfo(self, func):
        """
            Registers function to be called after connection info fetched.
            Backend name, profile name and profile info will be passed to function as arguments.
        """
        self.listener_conn_info.append(func)

    def getConnectionList(self, backend):
        """
            Gets connection list of specified backend.
        """
        self.link.Net.Link[backend].connections(async=self.__handleConnectionList)

    def listenConnectionList(self, func):
        """
            Registers function to be called after connection list fetched.
            Backend name and package list will be passed to function as arguments.
        """
        self.listener_conn_list.append(func)

    def getBackendInfo(self):
        """
            Gets backend list.
        """
        self.link.Net.Link.linkInfo(async=self.__handleBackendInfo)

    def listenBackendInfo(self, func):
        """
            Registers function to be called after backend information fetched.
            Backend name and information will be passed to function as arguments.
        """
        self.listener_back_info.append(func)

    def listenConnectionState(self, func):
        """
            Registers function to be called after a connection state signal fetched.
            Backend name, profile name, state and info message will be passed to function as arguments.
        """
        self.listener_conn_state.append(func)

    def deleteConnection(self, backend, profile):
        """
            Deletes a profile on specified backend.
        """
        self.link.Net.Link[backend].deleteConnection(profile, async=self.__handleConnectionDelete)

    def setState(self, backend, profile, state):
        """
            Sets state of a profile on specified backend.
        """
        self.link.Net.Link[backend].setState(profile, state, async=self.__handleConnectionState)
