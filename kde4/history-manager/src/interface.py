#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import pisi
import time

from PyQt4.QtCore import *

from listitem import *

class ComarIface:
    """ COMAR Interface """

    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()

    def listen(self, func):
        self.handle = func
        self.link.listenSignals("System.Manager", self.handlerInternal)

    def takeSnap(self):
        self.link.System.Manager["pisi"].takeSnapshot(async=self.handlerInternal)

    def takeBack(self, num):
        self.link.System.Manager["pisi"].takeBack(num, async=self.handlerInternal)

    def handlerInternal(self, package, signal, args):
        if signal == "finished":
            pisi.db.invalidate_caches()

        self.handle(package, signal, args)

class PisiIface(QThread):
    """ Pisi Api Interface """

    def __init__(self, parent=None):
        super(PisiIface, self).__init__(parent)
        self.parent = parent

        self.ops = {}
        self.pdb = None
        self.initDb()

    def initDb(self):
        self.pdb = pisi.db.historydb.HistoryDB()

    def run(self):
        for operation in self.pdb.get_last():
            self.ops[operation.no] = operation
            self.emit(SIGNAL("loadFetched(PyQt_PyObject)"), operation.no)
            time.sleep(0.01)

    def historyPlan(self, op):
        return pisi.api.get_takeback_plan(op)

    def historyDir(self):
        return pisi.ctx.config.history_dir()

    def historyConfigs(self, op):
        return self.pdb.get_config_files(op)

    def getLastOperation(self):
        op = self.pdb.get_last()
        return op.next()
