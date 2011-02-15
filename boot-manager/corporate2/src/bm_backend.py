#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import comar

from kdecore import i18n
from kdeui import KMessageBox

class Backend:

    def __init__(self, parent):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("Boot.Loader", parent.handleSignals)
        self.parent = parent

    def show_error(self, msg):
        return KMessageBox.error(self.parent, msg, i18n('Error'))

    def run(self, method, async = None):
        try:
            if async:
                method(async = async)
            else:
                method()
            return True
        except Exception, msg:
            # fixme: dbuserrors may also be handled in here.
            if 'PolicyKit' in unicode(msg):
                self.show_error(i18n('You are not authorized for this operation.'))
            else:
                self.show_error(i18n('An error occured:\n%s' % unicode(msg)))
            return False

    def removeUnused(self, package, version, async = None):
        if async:
            return self.link.Boot.Loader[package].removeUnused(version, async = async)
        else:
            return self.run(lambda:self.link.Boot.Loader[package].removeUnused(version))

    def setEntry(self, package, title, os_type, root, kernel, initrd, options, default, index, async = None):
        if async:
            return self.link.Boot.Loader[package].setEntry(title, os_type, root, kernel, initrd, options, default, index, async = async)
        else:
            return self.run(lambda:self.link.Boot.Loader[package].setEntry(title, os_type, root, kernel, initrd, options, default, index))

    def listUnused(self, package, async = None):
        if async:
            return self.link.Boot.Loader[package].listUnused(async = async)
        else:
            return self.run(lambda:self.link.Boot.Loader[package].listUnused)

    def removeEntry(self, package, index, title, uninstall, async = None):
        if async:
            return self.link.Boot.Loader[package].removeEntry(index, title, uninstall, async = async)
        else:
            return self.run(lambda:self.link.Boot.Loader[package].removeEntry(index, title, uninstall))

    def listEntries(self, package, async = None):
        if async:
            return self.run(self.link.Boot.Loader[package].listEntries, async = async)
        else:
            return self.run(lambda:self.link.Boot.Loader[package].listEntries)

    def listSystems(self, package, async = None):
        if async:
            return self.run(self.link.Boot.Loader[package].listSystems, async = async)
        else:
            return self.run(lambda:self.link.Boot.Loader[package].listSystems)

    def getOptions(self, package, async = None):
        if async:
            return self.run(self.link.Boot.Loader[package].getOptions, async = async)
        else:
            return self.run(lambda:self.link.Boot.Loader[package].getOptions)

    def setOption(self, package, label, value, async = None):
        if async:
            return self.link.Boot.Loader[package].setOption(label, value, async = async)
        else:
            return self.run(lambda:self.link.Boot.Loader[package].setOption(label, value))

