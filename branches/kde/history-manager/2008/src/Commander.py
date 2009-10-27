#!/usr/bin/python
# -*- coding: utf-8 -*-

import string

from kdecore import i18n
from qt import QObject, QTimer
import ComarIface

class Commander(QObject):
    """ Gui uses this class instead of directly ComarIface """
    def __init__(self, parent):
        QObject.__init__(self)
        self.parent = parent
        try:
            self.comar = ComarIface.ComarIface(self.handler, self.errHandler)
        except:
            self.parent.showErrorMessage(i18n("Cannot connect to Comar daemon"))
            self.parent.updateGui()

    def errHandler(self, err=None):
        self.comar.com_lock.unlock()
        # parent's finished function prints messages
        if err:
            self.parent.finished("System.Manager.cancelled", err)
        else:
            self.parent.finished("System.Manager.cancelled")

    def handler(self, signal=None, data=None):
        try:
            if len(data) > 1:
                args = data[1:]
            else:
                args = None
        except:
            pass

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
            self.parent.showWarningMessage(str(args))
            print "Warning: ", str(data)
        elif signal == "PolicyKit":
            self.parent.pisiNotify(data[0], args)
        else:
            # None of above signals, unhandled
            print "Got notification : %s with data : %s" % (signal, data)

    def inProgress(self):
        return self.comar.com_lock.locked()

    def cancel(self):
        self.comar.cancel()

    def takeSnapshot(self):
        self.comar.takeSnapshot()

    def takeBack(self, op):
        self.comar.takeBack(op)

