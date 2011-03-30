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
from pds.thread import PThread

from PyQt4.QtCore import QObject

class PisiUI(QObject, pisi.ui.UI):

    def __init__(self, *args):
        pisi.ui.UI.__init__(self)
        apply(QObject.__init__, (self,) + args)
        self.lastPackage = ''

    def notify(self, event, **keywords):
        print "UM DEBUG:", event, keywords

    def display_progress(self, **keywords):
        print "$keywords",keywords

class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Iface(QObject, Singleton):

    """ Pisi Iface for UM """

    def __init__(self):
        apply(QObject.__init__, (self,))
        options = pisi.config.Options()

        options.yes_all = True
        options.ignore_dependency = True
        options.ignore_safety = True

        self.ui = PisiUI()
        pisi.api.set_userinterface(self.ui)
        pisi.api.set_options(options)
        pisi.api.set_signal_handling(False)

    def runThreaded(self, action, args=[], kwargs={}):
        def hede():
            return
        thread = PThread(self, action, hede, args, kwargs)
        thread.start()

    # Std Package Actions ------------------------------------------------->>-

    def installPackages(self, packages):
        self.runThreaded(lambda:pisi.api.install(packages))

    # Std Package Actions -------------------------------------------------<<-

