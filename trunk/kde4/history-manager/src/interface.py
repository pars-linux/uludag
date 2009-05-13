#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import pisi

from PyQt4.QtCore import *

from listitem import *

class ComarIface:
    """ COMAR Interface """

    def __init__(self):
        self.link = comar.Link()

    def listen(self, func):
        self.handler = func
        self.link.listenSignals("System.Manager", func)

    def takeSnap(self):
        self.link.System.Manager["pisi"].takeSnapshot(async=self.handler)

    def takeBack(self, num):
        self.link.System.Manager["pisi"].takeBack(num, async=self.handler)

class PisiIface(QThread):
    """ Pisi Api Interface """

    def __init__(self, parent=None):
        super(PisiIface, self).__init__(parent)
        self.parent = parent

        self.max_fetch = None
        self.pdb = pisi.db.historydb.HistoryDB()
        self.pdb.init()

    def run(self):
        self.parent.ops = {}
        cntr = 0
        for operation in self.pdb.get_last():
            self.parent.ops[operation.no] = operation
            cntr += 1
            if self.max_fetch != None:
                if cntr == self.max_fetch:
                    self.emit(SIGNAL("loadFetched(PyQt_PyObject)"), self.max_fetch)
                    break

    def historyPlan(self, op):
        return pisi.api.get_takeback_plan(op)

    def historyDir(self):
        return pisi.ctx.config.history_dir()

    def historyConfigs(self, op):
        return self.pdb.get_config_files(op)

    def reloadPisi(self):
        import sys
        for module in sys.modules.keys():
            if module.startswith("pisi."):
                """removal from sys.modules forces reload via import"""
                del sys.modules[module]
            reload(pisi)

    def setMaxFetch(self, num):
        if num == 0:
            self.max_fetch = None
            return
        self.max_fetch = num

