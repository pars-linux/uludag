#!/usr/bin/python
# -*- coding: utf-8 -*-

import string

from kdecore import i18n
from qt import QObject, QTimer
import ComarIface

class Commander(QObject):
    def __init__(self, parent):
        QObject.__init__(self)
        self.parent = parent
        try:
            self.comar = ComarIface.ComarIface(self.handler, self.errHandler)
        except:
            self.parent.showErrorMessage("Cannot connect to Comar daemon")
            self.parent.setReadOnly(True)

    def errHandler(self):
        self.comar.com_lock.unlock()
        self.parent.finished("System.Manager.cancelled")

    def handler(self, signal, data):
        print "Signal: ", signal
        print "Data: ", data
        args = data[1:] if len(data) > 1 else None

        if signal == "finished":
            command = data[0]
            self.comar.com_lock.unlock()
            self.parent.finished(command)
        elif signal == "progress":
            self.parent.displayProgress(data)
        elif signal == "error":
            self.comar.com_lock.unlock()
            print "Error: ", str(data)
            self.parent.showErrorMessage(str(args))
        elif signal == "status":
            operation = data[0]
            self.parent.pisiNotify(operation, args)
        elif signal == "warning":
            self.comar.com_lock.unlock()
            self.parent.showWarningMessage(str(args))
            print "Warning: ", str(data)
        else:
            print "Got notification : %s with data : %s" % (signal, data)


    def inProgress(self):
        return self.comar.com_lock.locked()

    def cancel(self):
        self.comar.cancel()

    def takeSnapshot(self):
        self.comar.takeSnapshot()

    def takeBack(self, op):
        self.comar.takeBack(op)

