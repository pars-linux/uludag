#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from qt import QString, QMutex, SIGNAL
from kdeui import KMessageBox
from kdecore import i18n

# DBus
import dbus
import dbus.mainloop.qt3

from handler import CallHandler

class ComarIface:
    def __init__(self, handler=None, errHandler=None):
        self.errHandler = errHandler
        self.handler = handler

        # setup dbus stuff
        self.setupBusses()
        self.setupSignals()

    def setupBusses(self):
        try:
            self.sysBus = dbus.SystemBus()
            self.sesBus = dbus.SessionBus()
        except dbus.DBusException:
            KMessageBox.error(None, i18n("Unable to connect to DBus."), i18n("DBus Error"))
            return False
        return True

    def setupSignals(self):
        self.sysBus.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.System.Upgrader", member_keyword="signal", path_keyword="path")

    def handleSignals(self, *args, **kwargs):
        signal = kwargs["signal"]
        # use args here
        if self.handler:
            self.handler(signal, args)

    def busError(self, exception):
        KMessageBox.error(None, str(exception), i18n("D-Bus Error"))
        self.setupBusses()
        self.errHandler()

    def comarAuthError(self, exception):
        KMessageBox.error(None, str(exception), i18n("COMAR Auth Error"))
        self.errHandler()

    def comarError(self, exception):
        if "urlopen error" in exception.message or "Socket Error" in exception.message:
            KMessageBox.error(None, i18n("Network error. Please check your network connections and try again."), i18n("COMAR Error"))
        elif "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.sorry(None, message, i18n("Error"))
        else:
            KMessageBox.error(None, QString.fromUtf8(str(exception)), i18n("COMAR Error"))

        self.errHandler()

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        self.errHandler()
        KMessageBox.sorry(None, message, i18n("Error"))

    def callSyncMethod(self, method, *args):
        ch = CallHandler("pisi", "System.Upgrader", method,
                         None,
                         self.sysBus, self.sesBus)

    def callMethod(self, method, action, handler, handleErrors, async = True, *args):
        print "Method: %s      Action: %s" % (method, action)
        ch = CallHandler("pisi", "System.Upgrader", method,
                         action, async,
                         self.sysBus, self.sesBus)

        if handleErrors:
            ch.registerError(self.comarError)
            ch.registerAuthError(self.comarAuthError)
            ch.registerDBusError(self.busError)
            ch.registerCancel(self.cancelError)

        if handler:
            ch.registerDone(handler)

        ch.call(*args)

    def prepare(self):
        self.callMethod("prepare", "tr.org.pardus.comar.system.upgrader.run", None, True, True)

    def setRepositories(self):
        self.callMethod("setRepositories", "tr.org.pardus.comar.system.upgrader.run", None, True, True)

    def download(self):
        self.callMethod("download", "tr.org.pardus.comar.system.upgrader.run", None, True, True)

    def upgrade(self):
        self.callMethod("upgrade", "tr.org.pardus.comar.system.upgrader.run", None, True, True)

    def cleanup(self):
        self.callMethod("cleanup", "tr.org.pardus.comar.system.upgrader.run", None, True, True)

    def cancel(self):
        obj = self.sysBus.get_object("tr.org.pardus.comar", "/", introspect=False)
        obj.cancel(dbus_interface="tr.org.pardus.comar")
