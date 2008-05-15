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
            self.parent.showErrorMessage(i18n("Cannot connect to Comar daemon"))
            #self.parent.setReadOnly(True)
            self.parent.updateGui()

    def errHandler(self, err=None):
        self.comar.com_lock.unlock()
        if err:
            self.parent.finished("System.Manager.cancelled", err)
        else:
            self.parent.finished("System.Manager.cancelled")

    def handler(self, signal=None, data=None):
        print "Signal: ", signal
        print "Data: ", data
        args = data[1:] if len(data) > 1 else None

        if signal == "finished":
            self.comar.com_lock.unlock()
            self.parent.finished(data[0])
        elif signal == "progress":
            self.parent.displayProgress(data)
        elif signal == "error":
            self.comar.com_lock.unlock()
            print "Error: ", str(data)
            self.parent.showErrorMessage(str(args))
        elif signal == "status":
            self.parent.pisiNotify(data[0], args)
        elif signal == "warning":
            #self.comar.com_lock.unlock()
            self.parent.showWarningMessage(str(args))
            print "Warning: ", str(data)
        elif signal == "PolicyKit":
            self.parent.pisiNotify(data[0], args)
        else:
            print "Got notification : %s with data : %s" % (signal, data)

    def inProgress(self):
        return self.comar.com_lock.locked()

    def cancel(self):
        self.comar.cancel()

    def takeSnapshot(self):
        qApp.progressEvents()
        self.comar.takeSnapshot()

    def takeBack(self, op):
        qApp.processEvents()
        self.comar.takeBack(op)

