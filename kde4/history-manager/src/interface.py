#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import pisi
import sys

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

class PisiIface:
    """ Pisi Iface """

    def __init__(self):

    def get_history_dir():
        return pisi.ctx.config.history_dir()

    def getPlan(op):
        return pisi.api.get_takeback_plan(op)

    def reloadPisi():
        for module in sys.modules.keys():
            if module.startswith("pisi."):
                """removal from sys.modules forces reload via import"""
                del sys.modules[module]
        reload(pisi)
