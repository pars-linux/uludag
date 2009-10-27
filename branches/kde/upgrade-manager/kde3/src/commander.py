# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import string

from kdeui import KMessageBox
from kdecore import i18n
from qt import QObject, QTimer, PYSIGNAL
import comariface

class Commander(QObject):
    def __init__(self):
        QObject.__init__(self)
        try:
            self.comar = comariface.ComarIface(self.handler, self.errHandler)
        except:
            print "Cannot connect to Comar daemon"

    def errHandler(self):
        print "error"
        pass

    def handler(self, signal, data):
        if len(data) > 1:
            args = data[1:]
        else:
            args = None

        if signal == "finished":
            command = str(data[0])
            self.emit(PYSIGNAL("stepFinished(QString)"), (command,))
        elif signal == "started":
            command = data[0]
            self.emit(PYSIGNAL("stepStarted(QString)"), (command,))
        elif signal == "progress":
            print "progress"
        elif signal == "error":
            print "Error: ", str(data)
        elif signal == "status":
            if data[0] == "downloading":
                self.emit(PYSIGNAL("statusDownloading(int, int)"), (data[1], data[2],))
            elif data[0] == "installing":
                self.emit(PYSIGNAL("statusInstalling(QString, int, int)"), (data[1], data[2], data[3], ))
            elif data[0] == "configuring":
                self.emit(PYSIGNAL("statusConfiguring()"), ())
        elif signal == "warning":
            print "Warning: ", str(data)
        elif signal == "PolicyKit" and "policy.no" in data:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.sorry(None, message, i18n("Error"))
        else:
            print "Got notification : %s with data : %s" % (signal, data)

    def prepare(self):
        self.comar.prepare()

    def setRepositories(self):
        self.comar.setRepositories()

    def download(self):
        self.comar.download()

    def upgrade(self):
        self.comar.upgrade()

    def cleanup(self):
        self.comar.cleanup()

    def cancel(self):
        self.comar.cancel()
