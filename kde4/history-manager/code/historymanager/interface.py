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
        self.link.useAgent()
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

        self.settings = QSettings()
        self.ops = {}
        self.pdb = None
        self.initDb()

    def initDb(self):
        self.pdb = pisi.db.historydb.HistoryDB()

    def run(self):
        _max = int(self.pdb.get_last().next().no)

        fetch = self.settings.value("maxhistory", QVariant(100)).toInt()[0]

        _min = _max-fetch
        if _max <= fetch:
            _min = 0

        for i in range(_max, _min, -1):
            QCoreApplication.processEvents()
            operation = self.pdb.get_operation(i)
            if operation:
                self.ops[int(operation.no)] = [int(operation.no), str(operation.type),
                                               str(operation.date), str(operation.time),
                                              [ i for i in operation.packages ],
                                              [ i for i in operation.repos ]]
            del operation

        self.emit(SIGNAL("loadFetched(PyQt_PyObject)"), len(self.ops))
        self.deinit()

    def historyPlan(self, op):
        return pisi.api.get_takeback_plan(op)

    def historyDir(self):
        return pisi.ctx.config.history_dir()

    def historyConfigs(self, op):
        return self.pdb.get_config_files(op)

    def getLastOperation(self):
        op = self.pdb.get_last()
        op = op.next()
        return [int(op.no), str(op.type), str(op.date), str(op.time), [ i.__str__() for i in op.packages ], [ i.__str__() for i in op.repos ]]

    def deinit(self):
        if self.pdb:
            del self.pdb
            self.initDb()
