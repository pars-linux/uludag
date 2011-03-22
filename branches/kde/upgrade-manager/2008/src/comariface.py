#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4.QtCore import QSocketNotifier, QObject, SIGNAL

import comar
import pisi

from dumlogging import logger

class ComarIface(QObject):
    def __init__(self):
        self.com = comar.Link()

        # Notification
        self.com.ask_notify("System.Upgrader.progress")
        self.com.ask_notify("System.Upgrader.error")
        self.com.ask_notify("System.Upgrader.warning")
        self.com.ask_notify("System.Upgrader.notify")
        self.com.ask_notify("System.Upgrader.started")
        self.com.ask_notify("System.Upgrader.finished")
        self.com.ask_notify("System.Upgrader.cancelled")

        self.notifier = QSocketNotifier(self.com.sock.fileno(), QSocketNotifier.Read)

        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)

    def slotComar(self, sock):
        try:
            reply = self.comar.com.read_cmd()
        except:
            if not self.wait_comar():
                logger.error("Can not connect to comar daemon")
            return

        if reply.command == "notify":
            (notification, script, data) = (reply.notify, reply.script, reply.data)
            data = unicode(data)

            if notification == "System.Upgrader.error":
                pass

            elif notification == "System.Upgrader.notify":
                pass

            elif notification == "System.Upgrader.progress":
                pass

            elif notification == "System.Upgrader.started":
                self.emit(SIGNAL("stepStarted(QString)", data))

            elif notification == "System.Upgrader.finished":
                self.emit(SIGNAL("stepFinished(QString)", data))

            else:
                print "Got notification : %s , for script : %s , with data : %s" % (notification, script, data)

    def wait_comar(self):
        self.notifier.setEnabled(False)
        import socket, time
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        timeout = 5
        while timeout > 0:
            try:
                if pisi.api.ctx.comar_sockname:
                    sock.connect(pisi.api.ctx.comar_sockname)
                    return True
                else:
                    self.comar.notifier.setEnabled(True)
                    sock.connect("/var/run/comar.socket")
                    return True
            except socket.error:
                timeout -= 0.2
            time.sleep(0.2)
        return False

    def prepare(self):
        self.com.call("System.Upgrader.prepare")

    def setRepositories(self):
        self.com.call("System.Upgrader.setRepositories")

    def download(self):
        self.com.call("System.Upgrader.download")

    def upgrade(self):
        self.com.call("System.Upgrader.upgrade")

    def cleanup(self):
        self.com.call("System.Upgrader.cleanup")

    def cancel(self):
        self.com.cancel()
