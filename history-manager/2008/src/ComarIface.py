#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import QMutex, SIGNAL
from kdecore import i18n

import dbus
import dbus.mainloop.qt3

from handler import CallHandler

class ComarIface:
    """ Comar Interface to communicate with Comar """
    def __init__(self, handler=None, errHandler=None):
        self.errHandler = errHandler
        self.handler = handler
        # package-manager sync
        self.com_lock = QMutex()
        if self.setupBusses():
            self.setupSignals()
        else:
            self.errHandler()
            return

    def setupBusses(self):
        try:
            # get system and session busses
            self.sysBus = dbus.SystemBus()
            self.sesBus = dbus.SessionBus()
        except dbus.DBusException:
            self.errHandler(i18n("Cannot connect to dbus"))
            return False
        return True

    def setupSignals(self):
        self.sysBus.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.System.Manager", member_keyword="signal", path_keyword="path")

    def handleSignals(self, *args, **kwargs):
        signal = kwargs["signal"]
        if self.handler:
            self.handler(signal, args)

    def busError(self, exception):
        message = i18n("D-Bus Error") + str(exception)
        self.setupBusses()
        self.errHandler(message)

    def comarAuthError(self, exception):
        self.errHandler(i18n("COMAR Auth Error") + str(exception))

    def comarError(self, exception):
        message = ""
        if not "urlopen error" in exception.message:
            message += i18n("COMAR Error")
        self.errHandler(message + "<br>" + str(exception))

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        self.errHandler(message)

    def callMethod(self, method, action, handler, handleErrors, *args):
        ch = CallHandler("System.Manager", method, action, self.sysBus, self.sesBus)

        if handleErrors:
            ch.registerError(self.comarError)
            ch.registerAuthError(self.comarAuthError)
            ch.registerDBusError(self.busError)
            ch.registerCancel(self.cancelError)
        if handler:
            ch.registerDone(handler)

        ch.call(*args)

    def takeSnapshot(self):
        self.com_lock.lock()
        self.callMethod("takeSnapshot", "tr.org.pardus.comar.system.manager.takesnapshot", self.handler, True)

    def takeBack(self, operation):
        self.com_lock.lock()
        self.callMethod("takeBack", "tr.org.pardus.comar.system.manager.takeback", None, True, int(operation))

    def cancel(self):
        obj = self.sysBus.get_object("tr.org.pardus.comar", "/", introspect=False)
        obj.cancel(dbus_interface="tr.org.pardus.comar")

