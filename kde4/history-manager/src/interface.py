#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import pisi
import sys

from PyQt4.QtCore import QThread

class ComarIface:
    """ COMAR Interface """

    def __init__(self):
        self.link = comar.Link()

    def handler(self, *args):
        pass

    def listen(self, func):
        self.link.listenSignals("System.Manager", func)

    def takeSnap(self):
        self.link.System.Manager["pisi"].takeSnapshot()

    def takeBack(self, num):
        self.link.System.Manager["pisi"].takeBack(num)

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

    def historyDir(self):
        return pisi.ctx.config.history_dir()

    def plan(self, op):
        return pisi.api.get_takeback_plan(op)

    def reloadPisi(self):
        for module in sys.modules.keys():
            if module.startswith("pisi."):
                """removal from sys.modules forces reload via import"""
                del sys.modules[module]
        reload(pisi)

    def historyDb(self):
        return self.pdb

    def updateHdb(self):
        #FIXME
        self.pdb.init()

    def getConfigFiles(self, op):
        self.pdb.get_config_files(op)

