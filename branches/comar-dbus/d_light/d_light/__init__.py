# -*- coding: utf-8 -*-

__all__ = []

import threading
import time

import d_light
from d_light import BUS_SYSTEM, BUS_SESSION

class DLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            d_light.fetch()
            time.sleep(0.1)
            d_light.exec_()

    def call(self, dest, path,iface, method, args, callbackFunc, bustype):
        d_light.call(dest, path, iface, method, args, callbackFunc, bustype)

    def call_blocking(self, dest, path,iface, method, args, bustype, timeout):
        return d_light.call_blocking(dest, path, iface, method, args, bustype, timeout)

    def register(self, rule, callbackFunc, bustype):
        d_light.registerSignal(rule, callbackFunc, bustype)
