#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import pisi

from PyQt4.QtCore import *

class ComarIface(QThread):
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

        self.pdb = pisi.db.historydb.HistoryDB()
        self.pdb.init()

        self.start()

    def run(self):
        for operation in self.pdb.get_last():
            self.parent.ops.append(operation)

    def historyPlan(self, op):
        return pisi.api.get_takeback_plan(op)

    def historyDir(self):
        return pisi.ctx.config.history_dir()

    def historyConfigs(self, op):
        return self.pdb.get_config_files(op)

    def reloadPisi():
        import sys
        for module in sys.modules.keys():
            if module.startswith("pisi."):
                """removal from sys.modules forces reload via import"""
                del sys.modules[module]
            reload(pisi)
