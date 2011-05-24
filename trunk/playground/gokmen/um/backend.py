#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import pisi
import threading
from pds.thread import PThread

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

def threaded(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
    return run

class PisiUI(QObject, pisi.ui.UI):

    def __init__(self, *args):
        pisi.ui.UI.__init__(self)
        apply(QObject.__init__, (self,) + args)

    def notify(self, event, **keywords):
        self.emit(SIGNAL("notify(int, PyQt_PyObject)"), \
                  event, keywords)

    def info(self, message, verbose = False, noln = False):
        pass
        # print "MM:", message

    def warning(self, message):
        pass
        # print "WR:", message

    def display_progress(self, **keywords):
        self.emit(SIGNAL("progress(PyQt_PyObject)"), keywords)

class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Iface(QObject, Singleton):

    """ Pisi Iface for UM """

    def __init__(self, parent):
        apply(QObject.__init__, (self,))
        options = pisi.config.Options()

        # Make something crazy.
        # options.yes_all = True
        # options.ignore_dependency = True
        # options.ignore_safety = True

        self.ui = PisiUI()
        self.connect(self.ui,\
                SIGNAL("progress(PyQt_PyObject)"),\
                parent.updateProgress)

        self.connect(self.ui,\
                SIGNAL("notify(int, PyQt_PyObject)"),\
                parent.processNotify)

        pisi.api.set_userinterface(self.ui)
        pisi.api.set_options(options)
        pisi.api.set_signal_handling(False)

    @threaded
    def installPackages(self, packages, with_comar = True, reinstall = True):
        pisi.api.set_comar(with_comar)
        pisi.api.install(packages, reinstall = reinstall)

    @threaded
    def downloadPackages(self, packages):
        pisi.api.fetch(packages)

